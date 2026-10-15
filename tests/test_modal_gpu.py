"""Exercise the Modal backend of experiment.py without Modal calls or a GPU."""
import io
import json
import tarfile
from types import SimpleNamespace

import pytest

from scripts import experiment as exp
from scripts import modal_gpu


@pytest.mark.parametrize('value, name', [
    ('L40S', 'L40S'), ('l40s', 'L40S'), ('a100', 'A100-40GB'), ('A100 80GB', 'A100-80GB'),
    ('RTX PRO 6000', 'RTX-PRO-6000'), ('a10g', 'A10'), ('h100', 'H100'), ('T4', 'T4'),
])
def test_gpu_values_map_to_modal_names(value, name):
    assert modal_gpu.gpu_type(value) == name


@pytest.mark.parametrize('value', ['RTX 5090', 'RTX 5060 Ti', 'B300', 'H100:2'])
def test_vast_and_unsupported_gpu_values_fail_locally(value):
    with pytest.raises(ValueError, match='not a Modal GPU'):
        modal_gpu.gpu_type(value)


def test_cost_is_gpu_cpu_and_memory_seconds_at_published_rates():
    # https://modal.com/pricing: L40S $0.000542/s, $0.0000131/core/s, $0.00000222/GiB/s.
    assert modal_gpu.cost_usd('L40S', 100) == pytest.approx(100 * (0.000542 + 2 * 0.0000131 + 16 * 0.00000222))
    assert modal_gpu.cost_usd('T4', 0) == 0


CELL = {'name': 'fit/M1_210210', 'arm': 'fit', 'target': 'M1_210210', 'seed': 12, 'priors': {},
        'settings': {'ssp_grid': '/workspace/cosmic-chronometers-jwst/grid/123.h5'},
        'target_metadata': {'object_id': 210210, 'spect_id': 'M1_210210', 'seed': 12}}


def result_archive(cells, exit_codes, started=1000.0, finished=1150.0):
    """A container's tar.gz as modal_gpu.fit returns it for the request's cells."""
    status = {'exit': {'bootstrap': exit_codes['bootstrap']}, 'gpu': 'NVIDIA L40S', 'started': started,
              'finished': finished, 'cells': {str(c['index']): {'exit': exit_codes['fit'], 'mode': 'alone', 'tuned': 3, 'compiled': 5}
                                              for c in cells}}
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
        files = {'status.json': json.dumps(status), 'bootstrap.log': 'ready'}
        for c in cells:
            metadata = c['cell']['target_metadata']
            files[f"fit-{c['index']}.log"] = 'fitting'
            files[f"results/{c['index']}/{c['cell']['arm']}/{metadata['object_id']}-{metadata['spect_id']}/ceridwen_result.h5"] = 'h5'
        for name, text in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(text.encode())
            archive.addfile(info, io.BytesIO(text.encode()))
    return buffer.getvalue()


@pytest.fixture
def modal_run(tmp_path, monkeypatch):
    source = {'commit': 'abc', 'submodules': {}, 'image': 'example/image@sha256:abc', 'input_files': [],
              'grids': [{'grid': str(tmp_path / 'grid.h5'), 'grid_sha256': '123', 'remote_name': '123.h5'}],
              'experiment': [CELL]}
    args = SimpleNamespace(output=tmp_path / 'run', gpu='L40S')
    args.output.mkdir()
    run = exp.ModalRun(args, source)
    state = {'launches': [], 'stopped': [], 'billing': {'billed_cost': '0E-8', 'adjustments': {'plan_cost': '0E-8', 'credits': '-1.01'}},
             'report': [], 'exit': {'bootstrap': 0, 'fit': 0}, 'running': ['ap-other'], 'interrupt': False}

    def client(*arguments, **options):
        if arguments[0] == 'scripts/modal_gpu.py':
            work = exp.Path(arguments[2])
            state['launches'].append(json.loads(exp.Path(arguments[1]).read_text()))
            containers = state['launches'][-1]['containers']
            (work / 'calls.json').write_text(json.dumps({'app_id': 'ap-1', 'calls': {
                str(n): f'fc-{n + 1}' for n in range(len(containers))}}))
            if state['interrupt']:
                raise KeyboardInterrupt
            for number, cells in enumerate(containers):
                (work / f'{number}.tar.gz').write_bytes(result_archive(cells, state['exit']))
        elif arguments[2:4] == ('app', 'stop'):
            # Without a terminal, `modal app stop` aborts unless -y skips its confirmation.
            if '-y' not in arguments:
                return SimpleNamespace(returncode=1)
            state['stopped'].append(arguments[-1])
        return SimpleNamespace(returncode=0)

    def modal_json(*arguments):
        if arguments[:2] == ('container', 'list'):
            return [{'app_id': app, 'container_id': 'ta-1'} for app in state['running'] if app not in state['stopped']]
        return {('billing', 'summary'): state['billing'], ('billing', 'report'): state['report']}[arguments[:2]]

    monkeypatch.setattr(run, 'client', client)
    monkeypatch.setattr(run, 'modal_json', modal_json)
    monkeypatch.setattr(run, 'archives', lambda work: [])
    monkeypatch.setattr(exp.time, 'sleep', lambda _: None)
    monkeypatch.setattr(exp, 'validate_local_result', lambda directory: None)
    return run, state


def test_modal_fit_lands_in_vast_results_layout_with_cost(modal_run):
    run, state = modal_run
    assert run.execute() == 0
    root = run.root
    assert (root / 'fits/fit/210210-M1_210210/ceridwen_result.h5').read_text() == 'h5'
    assert (root / 'fc-1-bootstrap.log').read_text() == 'ready'
    assert (root / 'fc-1-fit-0.log').read_text() == 'fitting'
    assert [p.name for p in (root / '.modal/0').iterdir()] == ['calls.json']
    saved = json.loads((root / 'manifest.json').read_text())
    assert saved['backend'] == 'modal'
    assert saved['completed_cells'] == ['fit/M1_210210']
    attempt = saved['attempts'][0]
    assert attempt['app_id'] == 'ap-1' and attempt['status'] == 'complete'
    cell = attempt['cells']['fit/M1_210210']
    assert cell['container_seconds'] == 150
    assert cell['estimated_usd'] == pytest.approx(modal_gpu.cost_usd('L40S', 150))
    assert (cell['mode'], cell['tuned'], cell['compiled']) == ('alone', 3, 5)
    assert saved['estimated_total_usd'] == pytest.approx(cell['estimated_usd'])
    assert state['launches'][0]['gpu'] == 'L40S'
    assert state['launches'][0]['containers'][0][0]['grid'] == '123.h5'


def arms(count):
    """Cells of identical arms: the same compiled programs, so one cache key."""
    return [{**CELL, 'name': f'a{i}/M1_210210', 'arm': f'a{i}'} for i in range(count)]


def test_cells_beyond_the_gpu_limit_share_containers_and_their_cost(modal_run, monkeypatch):
    run, state = modal_run
    run.data['source']['experiment'] = arms(3)
    monkeypatch.setattr(modal_gpu, 'MAX_CONTAINERS', 2)
    assert run.execute() == 0
    containers = state['launches'][0]['containers']
    assert [len(cells) for cells in containers] == [1, 2]
    assert len({c['key'] for cells in containers for c in cells}) == 1
    saved = json.loads((run.root / 'manifest.json').read_text())
    shared = [saved['attempts'][0]['cells'][c['cell']['name']] for c in containers[1]]
    assert all(r['estimated_usd'] == pytest.approx(modal_gpu.cost_usd('L40S', 150) / 2) for r in shared)
    assert saved['estimated_total_usd'] == pytest.approx(2 * modal_gpu.cost_usd('L40S', 150))
    assert {p.name for p in run.root.glob('fc-2-*.log')} == {
        'fc-2-bootstrap.log', *(f"fc-2-fit-{c['index']}.log" for c in containers[1])}
    assert sorted(saved['completed_cells']) == sorted(c['name'] for c in arms(3))


def test_one_container_per_cell_up_to_the_gpu_limit(modal_run):
    run, _ = modal_run
    pending = list(enumerate(arms(modal_gpu.MAX_CONTAINERS + 3)))
    assert [len(cells) for cells in run.containers(pending[:4])] == [1, 1, 1, 1]
    packed = run.containers(pending)
    assert len(packed) == modal_gpu.MAX_CONTAINERS
    assert sorted(i for cells in packed for i, _ in cells) == list(range(len(pending)))


def test_cache_key_ignores_name_and_arm_only(modal_run):
    run, _ = modal_run
    key = run.cache_key(CELL)
    assert run.cache_key({**CELL, 'name': 'b/M1_210210', 'arm': 'b'}) == key
    assert run.cache_key({**CELL, 'seed': 99, 'target_metadata': {**CELL['target_metadata'], 'seed': 99}}) != key
    assert run.cache_key({**CELL, 'settings': {**CELL['settings'], 'calibration_order': 4}}) != key
    run.data['source']['commit'] = 'def'
    assert run.cache_key(CELL) != key


def test_uncached_cells_fit_alone_then_cached_cells_share_and_incomplete_caches_refit_alone():
    saved, calls, saves, shares = {'a', 'c'}, [], [], []

    def fit_one(cell, mode):
        calls.append((cell['index'], mode))
        return {'exit': 0, 'mode': mode, 'tuned': 2 if (cell['index'], mode) == (3, 'shared') else 0,
                'compiled': 5 if (cell['key'], mode) == ('c', 'shared') else 0}

    def save(key):
        saves.append(key)
        saved.add(key)

    @modal_gpu.contextlib.contextmanager
    def sharing():
        shares.append('start')
        yield
        shares.append('stop')

    cells = [{'index': i, 'key': k} for i, k in enumerate('abbac')]
    records = modal_gpu.schedule(cells, saved.__contains__, fit_one, save, sharing)
    assert calls[0] == (1, 'alone')
    assert sorted(calls[1:5]) == [(0, 'shared'), (2, 'shared'), (3, 'shared'), (4, 'shared')]
    # Cell 3's shared fit autotuned: every shared fit of its cache (0 and 3) fits again alone.
    assert calls[5:] == [(0, 'alone'), (3, 'alone')]
    assert shares == ['start', 'stop']
    assert records[0] == records[3] == {'exit': 0, 'mode': 'alone', 'tuned': 0, 'compiled': 0, 'retuned': 2}
    assert records[2]['mode'] == records[4]['mode'] == 'shared'
    # New cache b after its first fit; c gained programs compiled for this host; a after each refit.
    assert saves == ['b', 'c', 'a', 'a']


def test_one_cached_cell_fits_alone_from_its_cache_without_mps():
    saves = []
    records = modal_gpu.schedule([{'index': 0, 'key': 'a'}], {'a'}.__contains__,
                                 lambda cell, mode: {'exit': 0, 'mode': mode, 'tuned': 0, 'compiled': 0},
                                 saves.append, sharing=None)
    assert records == {0: {'exit': 0, 'mode': 'cached', 'tuned': 0, 'compiled': 0}}
    assert not saves


def test_failed_first_fit_saves_no_cache():
    saves = []
    records = modal_gpu.schedule([{'index': 0, 'key': 'a'}], set().__contains__,
                                 lambda cell, mode: {'exit': 1, 'mode': mode, 'tuned': 9, 'compiled': 9},
                                 saves.append, sharing=None)
    assert records[0]['exit'] == 1 and not saves


def test_resume_does_not_launch_completed_cells(modal_run):
    run, state = modal_run
    assert run.execute() == 0
    assert run.execute() == 0
    assert len(state['launches']) == 1


def test_failed_stage_keeps_partial_results_and_never_completes(modal_run):
    run, state = modal_run
    state['exit'] = {'bootstrap': 0, 'fit': 1}
    assert run.execute() == 1
    assert (run.root / 'fits/fit/210210-M1_210210/ceridwen_result.h5').exists()
    assert not run.data.get('completed_cells')
    assert 'stage exit' in run.data['attempts'][0]['cells']['fit/M1_210210']['error']


def test_guard_allows_launch_while_credits_and_allowances_cover_usage(modal_run):
    run, state = modal_run
    # `modal billing summary --json`, 2026-10-15: metered cost exceeds credits by the egress allowance.
    state['billing'] = {'metered_cost': '9.69315129', 'billed_cost': '0E-8', 'adjustments': {
        'free_storage': '-0E-8', 'plan_cost': '0E-8', 'credits': '-9.69000000',
        'reservation_adjustment': '-0E-8', 'network_egress_allowance': '-0.00315129'}}
    assert run.execute() == 0
    assert len(state['launches']) == 1


def test_credit_guard_stops_before_launch(modal_run):
    run, state = modal_run
    state['billing'] = {'billed_cost': '1.5', 'adjustments': {'plan_cost': '0', 'credits': '-30'}}
    with pytest.raises(exp.vast.SweepError, match='credits'):
        run.execute()
    assert not state['launches']


def test_billed_cost_from_modal_report_raises_the_total(modal_run):
    run, state = modal_run
    state['report'] = [{'object_id': 'ap-1', 'cost': '0.5'}, {'object_id': 'ap-other', 'cost': '9'}]
    assert run.execute() == 0
    assert run.data['attempts'][0]['billed_usd'] == 0.5
    assert run.data['estimated_total_usd'] == 0.5


def test_backend_defaults_to_modal_and_resume_keeps_saved_vast(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(exp, 'preflight', lambda *a, **kw: {'commit': 'abc', 'input_files': []})
    exp.main(['run', 'config.json', '--gpu', 'l40s', '--output', str(tmp_path / 'new'), '--dry-run'])
    plan = json.loads(capsys.readouterr().out)
    assert (plan['backend'], plan['gpu']) == ('modal', 'L40S')
    old = tmp_path / 'old'
    old.mkdir()
    (old / 'manifest.json').write_text(json.dumps({'source': {'commit': 'abc', 'input_files': []}}))
    exp.main(['run', 'config.json', '--gpu', 'RTX 5090', '--output', str(old), '--dry-run'])
    assert json.loads(capsys.readouterr().out)['backend'] == 'vast'


def test_leftover_container_is_stopped_and_other_apps_are_untouched(modal_run):
    run, state = modal_run
    state['running'].append('ap-1')
    assert run.execute() == 0
    assert state['stopped'] == ['ap-1']


def test_interrupted_launch_stops_the_app_and_keeps_the_attempt(modal_run):
    run, state = modal_run
    state['running'].append('ap-1')
    state['interrupt'] = True
    with pytest.raises(KeyboardInterrupt):
        run.execute()
    assert state['stopped'] == ['ap-1']
    saved = json.loads((run.root / 'manifest.json').read_text())
    assert saved['attempts'][0]['app_id'] == 'ap-1'
    assert not saved.get('completed_cells')
