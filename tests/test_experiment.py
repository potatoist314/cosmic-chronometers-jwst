"""Exercise experiment configuration and paid-instance lifecycle without rentals."""
import json
from types import SimpleNamespace

import pytest

from scripts import experiment as exp
from test_benchmark import cloud as fake_cloud

cloud = fake_cloud


@pytest.fixture
def run(tmp_path, monkeypatch):
    grid = tmp_path / 'grid.h5'
    grid.write_bytes(b'grid')
    source = {'commit': 'abc', 'submodules': {}, 'grid': str(grid), 'grid_sha256': '123',
              'grids': [{'grid': str(grid), 'grid_sha256': '123', 'remote_name': '123.h5'}],
              'experiment': [{'name': 'baseline/M1_210210', 'arm': 'baseline', 'target': 'M1_210210',
                              'seed': 12, 'settings': {}, 'priors': {},
                              'target_metadata': {'object_id': 210210, 'spect_id': 'M1_210210', 'seed': 12}}]}
    args = exp.parser().parse_args(['run', 'config.json', '--gpu', 'RTX 5090', '--output', str(tmp_path)])
    args.gpus, args.hosts, args.target, args.seed = [args.gpu], 1, 'experiment', 0
    monkeypatch.setattr(exp.engine.time, 'sleep', lambda _: None)
    monkeypatch.setattr(exp.vast, '_ssh_target', lambda _: ('root@test', '22'))
    return exp.Run(args, source)


@pytest.fixture
def config(tmp_path, monkeypatch):
    top = 'SETTINGS = {"ssp_grid": "default", "sampler": {"num_live": 500, "logZ_tol": -5.0}}\nPRIORS = {"dust": Uniform(low=0, high=1)}'
    notebook = {'cells': [{'source': [top]}]}
    monkeypatch.setattr(exp.engine, 'git', lambda *args, **kw: json.dumps(notebook))
    path = tmp_path / 'config.json'
    path.write_text('{}')
    return path


def test_arms_merge_nested_controls_and_preserve_baseline(config):
    config.write_text(json.dumps({'seed': 4, 'arms': {
        'baseline': {}, 'alternative': {'settings': {'sampler': {'num_live': 50}, 'ssp_grid': 'other'},
                                       'priors': {'dust': 'Uniform(low=0, high=2)'}}}}))
    baseline, changed = exp.configuration(config, 'abc')
    assert baseline['settings']['sampler']['num_live'] == 500
    assert changed['settings']['sampler'] == {'num_live': 50, 'logZ_tol': -5.0}
    assert changed['settings']['ssp_grid'] == 'other'
    assert changed['priors']['dust'] == 'Uniform(low=0, high=2)'
    assert baseline['seed'] == changed['seed'] == 4


@pytest.mark.parametrize('bad', [
    {'settings': {'typo': 1}}, {'priors': {'typo': 'Uniform(0, 1)'}},
    {'arms': {}}, {'arms': {'../escape': {}}}, {'targets': []},
    {'targets': ['a', 'a']}, {'seed': -1}, {'seed': True},
    {'priors': {'dust': 'Uniform('}}, {'typo': 1},
])
def test_invalid_configuration_fails_locally(config, bad):
    config.write_text(json.dumps(bad))
    with pytest.raises((ValueError, SyntaxError)):
        exp.configuration(config, 'abc')


def test_fit_downloads_then_destroys_and_resume_does_not_rent(run, cloud, monkeypatch):
    _, state = cloud
    pulls = []
    def pull(command, **kwargs):
        assert state['live']
        pulls.append(command)
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(exp.subprocess, 'run', pull)
    assert run.execute() == 0
    assert state['destroyed'] == [100]
    assert len(pulls) == 1
    assert run.data['completed_cells'] == ['baseline/M1_210210']
    assert run.execute() == 0
    assert state['created'] == [1]


def test_fit_failure_pulls_partial_outputs_and_destroys(run, cloud, monkeypatch):
    _, state = cloud
    monkeypatch.setattr(run, 'stage', lambda *args: (_ for _ in ()).throw(RuntimeError('fit failed')))
    monkeypatch.setattr(run, 'prepare', lambda _: '')
    pulls = []
    monkeypatch.setattr(exp.subprocess, 'run', lambda *args, **kw: pulls.append(args))
    assert run.execute() == 1
    assert pulls
    assert state['destroyed'] == [100]
    assert not run.data.get('completed_cells')


def test_failed_download_never_marks_cell_complete(run, cloud, monkeypatch):
    import subprocess
    monkeypatch.setattr(exp.subprocess, 'run', lambda *a, **kw:
                        (_ for _ in ()).throw(subprocess.CalledProcessError(23, 'rsync')))
    assert run.execute() == 1
    assert not run.data.get('completed_cells')
    assert cloud[1]['destroyed'] == [100]


def test_configuration_change_rejected_on_resume(run):
    changed = {**run.data['source'], 'experiment': []}
    with pytest.raises(exp.vast.SweepError, match='source differs'):
        exp.Run(run.args, changed)


def test_resume_skips_completed_arm_on_new_instance(run, cloud, monkeypatch):
    first = run.data['source']['experiment'][0]
    run.data['source']['experiment'].append({**first, 'name': 'alternative/M1_210210', 'arm': 'alternative'})
    run.data['completed_cells'] = [first['name']]
    monkeypatch.setattr(exp.subprocess, 'run', lambda *a, **kw: None)
    assert run.execute() == 0
    commands = cloud[1]['commands']
    assert any('fit-1' in c for c in commands)
    assert not any('fit-0' in c for c in commands)


def test_dry_run_does_not_contact_vast_or_create_output(tmp_path, monkeypatch):
    monkeypatch.setattr(exp, 'preflight', lambda *a, **kw: {'commit': 'abc'})
    monkeypatch.setattr(exp.vast, '_vastai_json', lambda *_: pytest.fail('Vast call during dry run'))
    output = tmp_path / 'absent'
    assert exp.main(['run', 'config.json', '--gpu', 'RTX 5090', '--output', str(output), '--dry-run']) == 0
    assert not output.exists()


def test_remote_passes_configuration_and_exact_seed_to_existing_worker(tmp_path, monkeypatch):
    from scripts import run_ceridwen_vast_multi_gpu as worker
    cell = {'name': 'arm/target', 'arm': 'arm', 'seed': 7,
            'target_metadata': {'object_id': 1, 'spect_id': 'target', 'seed': 7},
            'settings': {'ssp_grid': '/grid/123.h5'}, 'priors': {'dust': 'Uniform(0, 2)'}}
    config = tmp_path / 'config.json'
    config.write_text(json.dumps([cell]))
    calls = []
    def execute(target, directory):
        import os
        calls.append((target, directory))
        assert json.loads(os.environ['CERIDWEN_SETTINGS_OVERRIDE']) == cell['settings']
        assert json.loads(os.environ['CERIDWEN_PRIORS_OVERRIDE']) == cell['priors']
        assert os.environ['CERIDWEN_SAMPLER_ONLY'] == '0'
        return 0
    for name in ('CERIDWEN_SETTINGS_OVERRIDE', 'CERIDWEN_PRIORS_OVERRIDE', 'CERIDWEN_SAMPLER_ONLY', 'JAX_PLATFORMS'):
        monkeypatch.setenv(name, '')
    monkeypatch.setattr(worker, '_execute_target', execute)
    monkeypatch.setattr(exp, 'validate_result', lambda _: None)
    assert exp.remote(config, tmp_path) == 0
    assert calls == [(cell['target_metadata'], tmp_path / 'arm/1-target')]


def test_preflight_freezes_every_grid_and_target_before_rental(tmp_path, monkeypatch):
    config = tmp_path / 'experiment.json'
    config.write_text('{}')
    table = tmp_path / 'external/fsps/data/emlines_info.dat'
    table.parent.mkdir(parents=True)
    table.write_text('table')
    monkeypatch.setattr(exp, 'ROOT', tmp_path)
    cells = [dict(name=f'{name}/target', target='target', seed=42, settings={'ssp_grid': grid, 'window': (1, 2), 'photometry': 'cosmos_total'})
             for name, grid in [('base', 'registered'), ('other', 'local.h5')]]
    monkeypatch.setattr(exp, 'configuration', lambda *a: cells)
    def git(*args, **kwargs):
        if args[0] == 'rev-parse':
            return 'pinned'
        if args[0] == 'ls-tree':
            return '160000 commit module'
        return 'REGISTRY = {}' if 'grid_fetch' in args[1] else ''
    monkeypatch.setattr(exp.engine, 'git', git)
    checked = []
    def inspect(revision, **kwargs):
        checked.append(kwargs['grid_name'])
        return {'commit': revision, 'submodules': {'ceridwen': 'module'},
                'grid': kwargs['grid_name'], 'grid_sha256': str(len(checked))}
    monkeypatch.setattr(exp.engine, 'preflight', inspect)
    monkeypatch.setattr(exp.subprocess, 'run', lambda *a, **kw: SimpleNamespace(stdout=json.dumps(
        {'targets': [{'spect_id': 'target', 'object_id': 123, 'manifest_index': 2, 'seed': 2, 'filename': 'spectrum.fits'}]})))
    for name in exp.selected_inputs([{**c, 'target_metadata': {'filename': 'spectrum.fits'}} for c in cells]):
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
    source = exp.preflight(config, 'HEAD')
    assert checked == ['registered', str(tmp_path / 'local.h5')]
    assert source == json.loads(json.dumps(source))
    assert source['commit'] == 'pinned'
    assert len(source['grids']) == 2
    assert [c['settings']['ssp_grid'] for c in source['experiment']] == [
        f'{exp.engine.REMOTE}/grid/1.h5', f'{exp.engine.REMOTE}/grid/2.h5']
    assert all(c['target_metadata']['seed'] == 42 for c in source['experiment'])


def test_resume_keeps_lower_original_budget(run):
    run.data['spend_cap'] = .5
    run.save()
    resumed = exp.Run(run.args, run.data['source'])
    assert resumed.args.spend_cap == .5


def test_budget_failure_destroys_without_marking_cells_complete(run, cloud, monkeypatch):
    monkeypatch.setattr(run, 'upload', lambda _: setattr(run.args, 'spend_cap', .001))
    with pytest.raises(exp.vast.SweepError, match='budget'):
        run.execute()
    assert cloud[1]['destroyed'] == [100]
    assert not run.data.get('completed_cells')


def test_fatal_stage_error_survives_failed_partial_download(run, cloud, monkeypatch):
    import subprocess
    offer, state = cloud
    monkeypatch.setattr(exp.vast, 'search_offers', lambda *a, **kw:
                        [offer, {**offer, 'id': 2, 'host_id': 43}])
    monkeypatch.setattr(run, 'prepare', lambda _: '')
    monkeypatch.setattr(run, 'stage', lambda *a:
                        (_ for _ in ()).throw(exp.engine.StageFailed('fit exited 1')))
    monkeypatch.setattr(exp.subprocess, 'run', lambda *a, **kw:
                        (_ for _ in ()).throw(subprocess.CalledProcessError(23, 'rsync')))
    assert run.execute() == 1
    assert state['created'] == [1]
    assert state['destroyed'] == [100]
    assert run.data['attempts'][0]['retryable'] is False
    assert run.data['attempts'][0]['error'].startswith('StageFailed:')


def test_selected_inputs_include_uv_fallback_but_no_unrelated_targets():
    cells = [{'target': 'M1_210210', 'target_metadata': {'filename': 'legac_M1_210210_v2.0.fits'},
              'settings': {'photometry': 'cosmos2025_uv'}}]
    files = exp.selected_inputs(cells * 2)
    assert len(files) == len(set(files))
    assert 'data/raw/cosmos2020/cosmos2020_classic_legac_dr2_1arcsec.fits' in files
    assert 'data/raw/cosmos2025/cosmos2025_phot_legac_dr2_1arcsec.fits' in files
    assert [p for p in files if '/sp/' in p] == ['data/raw/legac_dr2/sp/legac_M1_210210_v2.0.fits']
    assert [p for p in files if '/hst_f814w/' in p] == ['data/raw/hst_f814w/M1_210210.fits']


def test_upload_selected_inputs_preserves_paths_and_checks_grid(run, monkeypatch):
    run.data['source']['input_files'] = ['data/raw/hst_f814w/M1_210210.fits']
    monkeypatch.setattr(run, 'archive', lambda *a: None)
    monkeypatch.setattr(run, 'timeout', lambda *a: 60)
    commands, copies, grids = [], [], []
    monkeypatch.setattr(exp.vast, '_ssh', lambda _, cmd, **kw: commands.append(cmd))
    monkeypatch.setattr(exp.vast, '_rsync', lambda *a, **kw: grids.append(a))
    monkeypatch.setattr(exp.subprocess, 'run', lambda cmd, **kw: copies.append(cmd))
    run.upload({'instance_id': 1})
    assert len(copies) == 1 and copies[0][:2] == ['rsync', '-aR']
    assert any('/./data/raw/hst_f814w/M1_210210.fits' in arg for arg in copies[0])
    assert len(grids) == 1
    assert any('sha256sum -c' in cmd for cmd in commands)
    assert any('input-files.json' in cmd for cmd in commands)
