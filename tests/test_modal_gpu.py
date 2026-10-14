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


def result_archive(exit_codes, started=1000.0, finished=1150.0):
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
        files = {'status.json': json.dumps({'exit': exit_codes, 'gpu': 'NVIDIA L40S',
                                            'started': started, 'finished': finished}),
                 'bootstrap.log': 'ready', 'fit.log': 'fitting',
                 'results/fit/210210-M1_210210/ceridwen_result.h5': 'h5'}
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
    state = {'launches': [], 'stopped': [], 'billing': {'metered_cost': '0', 'adjustments': {'credits': '0'}},
             'report': [], 'exit': {'bootstrap': 0, 'fit': 0}, 'running': ['ap-other']}

    def client(*arguments, **options):
        if arguments[0] == 'scripts/modal_gpu.py':
            work = exp.Path(arguments[2])
            state['launches'].append(json.loads(exp.Path(arguments[1]).read_text()))
            (work / 'calls.json').write_text(json.dumps({'app_id': 'ap-1', 'calls': {'0': 'fc-1'}}))
            (work / '0.tar.gz').write_bytes(result_archive(state['exit']))
        elif arguments[2:4] == ('app', 'stop'):
            state['stopped'].append(arguments[4])
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
    saved = json.loads((root / 'manifest.json').read_text())
    assert saved['backend'] == 'modal'
    assert saved['completed_cells'] == ['fit/M1_210210']
    attempt = saved['attempts'][0]
    assert attempt['app_id'] == 'ap-1' and attempt['status'] == 'complete'
    cell = attempt['cells']['fit/M1_210210']
    assert cell['container_seconds'] == 150
    assert cell['estimated_usd'] == pytest.approx(modal_gpu.cost_usd('L40S', 150))
    assert saved['estimated_total_usd'] == pytest.approx(cell['estimated_usd'])
    assert state['launches'][0]['gpu'] == 'L40S'
    assert state['launches'][0]['cells'][0]['grid'] == '123.h5'


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


def test_credit_guard_stops_before_launch(modal_run):
    run, state = modal_run
    state['billing'] = {'metered_cost': '31.5', 'adjustments': {'credits': '-30'}}
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
