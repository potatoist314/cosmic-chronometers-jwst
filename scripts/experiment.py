#!/usr/bin/env python3
"""Run configured Ceridwen fits on Modal: experiment.py run CONFIG --gpu L40S (--backend vast --gpu 'RTX 5090')."""
from __future__ import annotations

import argparse
import ast
import fcntl
import hashlib
import io
import json
import math
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

if __package__:
    from . import benchmark as engine
    from . import modal_gpu
else:
    import benchmark as engine
    import modal_gpu

vast = engine.vast
ROOT = engine.ROOT
WORKER = 'scripts/run_ceridwen_vast_multi_gpu.py'
DEFAULT_IMAGE = vast.DEFAULT_IMAGE


def merge(base, changes):
    """Merge nested settings, so a sampler override preserves unspecified controls."""
    if not isinstance(changes, dict):
        raise ValueError('configuration overrides must be objects')
    result = dict(base)
    for key, value in changes.items():
        if key not in base:
            raise ValueError(f'unknown configuration key: {key}')
        result[key] = merge(base[key], value) if isinstance(base[key], dict) else value
    return result


def configuration(path, revision):
    raw = json.loads(path.read_text())
    if not isinstance(raw, dict):
        raise ValueError('experiment configuration must be an object')
    unknown = raw.keys() - {'targets', 'seed', 'settings', 'priors', 'arms'}
    if unknown:
        raise ValueError(f'unknown experiment fields: {sorted(unknown)}')
    notebook = json.loads(engine.git('show', f'{revision}:{engine.NOTEBOOK}'))
    top = next(''.join(c['source']) for c in notebook['cells'] if 'SETTINGS = {' in ''.join(c['source']))
    defaults = engine.literal(top, 'SETTINGS')
    prior_node = next(n.value for n in ast.parse(top).body if isinstance(n, ast.Assign)
                      and any(getattr(t, 'id', None) == 'PRIORS' for t in n.targets))
    priors = {ast.literal_eval(k): ast.unparse(v) for k, v in zip(prior_node.keys, prior_node.values)}
    settings = merge(defaults, raw.get('settings', {}))
    priors = merge(priors, raw.get('priors', {}))
    targets = raw.get('targets', ['M1_210210'])
    if not isinstance(targets, list) or not targets or any(not isinstance(t, str) for t in targets):
        raise ValueError('targets must be a nonempty list of spectrum IDs')
    if len(set(targets)) != len(targets):
        raise ValueError('targets must be unique')
    seed = raw.get('seed', 20260832)
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError('seed must be an integer from 0 to 2**32 - 1')
    arms = raw.get('arms', {'fit': {}})
    if not isinstance(arms, dict) or not arms:
        raise ValueError('arms must be a nonempty object of named configurations')
    cells = []
    for name, arm in arms.items():
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
            raise ValueError(f'invalid arm name: {name}')
        if not isinstance(arm, dict):
            raise ValueError(f'arm {name} must be an object')
        if arm.keys() - {'settings', 'priors'}:
            raise ValueError(f'unknown fields in arm {name}')
        arm_settings = merge(settings, arm.get('settings', {}))
        arm_priors = merge(priors, arm.get('priors', {}))
        for expression in arm_priors.values():
            if not isinstance(expression, str):
                raise ValueError('priors must be Python expression strings')
            ast.parse(expression, mode='eval')
        for target in targets:
            cells.append({'name': f'{name}/{target}', 'arm': name, 'target': target,
                          'seed': seed, 'settings': arm_settings, 'priors': arm_priors})
    return cells


def preflight(path, revision, *, fetch_missing=False, commands=('git', 'ssh', 'rsync', 'vastai')):
    """Freeze settings, source, target metadata and every grid before renting."""
    revision = engine.git('rev-parse', f'{revision}^{{commit}}')
    cells = configuration(path, revision)
    if not (ROOT / 'external/fsps/data/emlines_info.dat').is_file():
        raise ValueError('missing external/fsps/data/emlines_info.dat')
    grid_revision = engine.git('ls-tree', revision, 'ceridwen').split()[2]
    grid_code = engine.git('show', f'{grid_revision}:ceridwen/ssps/grid_fetch.py', tree=ROOT / 'ceridwen')
    grid_module = {'__name__': 'pinned_grid_fetch'}
    exec(compile(grid_code, 'grid_fetch.py', 'exec'), grid_module)
    grids = {}
    for cell in cells:
        name = cell['settings']['ssp_grid']
        if name not in grids:
            # A local grid path is relative to the configuration file.
            candidate = Path(name).expanduser()
            if candidate.suffix == '.h5':
                name = str((path.parent / candidate).resolve())
            elif fetch_missing and name in grid_module['REGISTRY']:
                grid_module['fetch_grid'](name)
            source = engine.preflight(revision, grid_name=name, targets={c['target'] for c in cells if not manga(c)},
                                      workers=('experiment.py', 'run_ceridwen_vast_multi_gpu.py'), commands=commands)
            grids[cell['settings']['ssp_grid']] = {
                'grid': source['grid'], 'grid_sha256': source['grid_sha256'],
                'remote_name': f"{source['grid_sha256']}.h5"}
    # Reuse the pinned target selector with the local scientific environment.
    worker = engine.git('show', f'{revision}:{WORKER}')
    program = worker + """
from astropy.table import Table
manifest = build_target_manifest(num_shards=1, base_seed=0)
filenames = {_decode(row['SPECT_ID']): _decode(row['Filename']) for row in Table.read(CATALOG_PATH)}
for target in manifest['targets']:
    target['filename'] = filenames[target['spect_id']]
print(json.dumps(manifest))
"""
    code = 'import sys; exec(sys.stdin.read(), {"__name__": "experiment_preflight", "__file__": sys.argv[1]})'
    completed = subprocess.run([str(ROOT / 'ceridwen/.venv/bin/python'), '-c', code, str(ROOT / WORKER)],
                               input=program, text=True, capture_output=True, check=True)
    targets = {t['spect_id']: t for t in json.loads(completed.stdout)['targets']}
    dr3_targets = legac_dr3_targets() if any(legac_dr3(cell) for cell in cells) else {}
    for cell in cells:
        if manga(cell):
            cell['target_metadata'] = {**manga_target(cell['target']), 'seed': cell['seed']}
        elif legac_dr3(cell):
            cell['target_metadata'] = {**dr3_targets[cell['target']], 'seed': cell['seed']}
        elif cell['target'] not in targets:
            raise ValueError(f"target not in the production selection: {cell['target']}")
        else:
            cell['target_metadata'] = {**targets[cell['target']], 'seed': cell['seed']}
        grid = grids[cell['settings']['ssp_grid']]
        cell['settings'] = {**cell['settings'], 'ssp_grid': f"{engine.REMOTE}/grid/{grid['remote_name']}"}
    source.update(grids=list(grids.values()), experiment=cells)
    bootstrap = engine.git('show', f'{revision}:scripts/bootstrap_vast_ai.sh')
    if 'input-files.json' in bootstrap:
        inputs = selected_inputs(cells)
        for name in inputs:
            if not (ROOT / name).is_file():
                raise ValueError(f'missing selected input: {name}')
        source['input_files'] = inputs
    else:
        # Historical bootstrap scripts require the complete spectrum directory.
        for cell in cells:
            cell['target_metadata'].pop('filename')
    return json.loads(json.dumps(source))


selected_inputs = vast.selected_inputs
manga = vast.manga_cell
legac_dr3 = vast.legac_dr3_cell


def legac_dr3_targets():
    """Target metadata of every LEGA-C DR3 spectrum, keyed by SPECT_ID; DR3 has no production selection."""
    code = """
import json, sys
from astropy.table import Table
def text(value):
    return (value.decode() if isinstance(value, bytes) else str(value)).strip()
rows = Table.read(sys.argv[1], hdu=1)
print(json.dumps({text(row['SPECT_ID']): {'spect_id': text(row['SPECT_ID']), 'object_id': int(row['OBJECT']),
                  'manifest_index': index, 'sn': float(row['SN']), 'filename': text(row['Filename'])}
                  for index, row in enumerate(rows)}))
"""
    return json.loads(subprocess.check_output([str(ROOT / 'ceridwen/.venv/bin/python'), '-c', code,
                                               str(ROOT / vast.LEGAC_DR3_CATALOGUE)], text=True))


def manga_target(plateifu):
    """Target metadata of a MaNGA aperture spectrum from scripts/manga_aperture_spectra.py."""
    path = ROOT / 'data/processed/manga_dr17' / f'{plateifu}.fits'
    if not path.is_file():
        raise ValueError(f'missing MaNGA aperture spectrum: {path}; run scripts/manga_aperture_spectra.py')
    header = subprocess.run([str(ROOT / 'ceridwen/.venv/bin/python'), '-c',
                             'import sys; from astropy.io import fits; print(fits.getheader(sys.argv[1])["NSAID"])',
                             str(path)], text=True, capture_output=True, check=True)
    return {'spect_id': plateifu, 'object_id': int(header.stdout), 'manifest_index': 0, 'filename': path.name}


def validate_result(directory):
    """Check fit artifacts without assuming a fixed set of model parameters."""
    import h5py
    import nbformat
    import numpy as np
    from ceridwen.fit import load_result_h5

    fit = load_result_h5(directory / 'ceridwen_result.h5')
    if not np.isfinite(np.asarray(fit.log_weights)).all() or not np.isfinite(
            [fit.log_evidence, fit.log_evidence_err]).all():
        raise ValueError(f'non-finite posterior weights or evidence: {directory}')
    with h5py.File(directory / 'ceridwen_derived_outputs.h5') as derived:
        missing = {'summary', 'sfh', 'photometry', 'spectrum', 'diagnostics'} - derived.keys()
        if missing or not bool(derived['diagnostics'].attrs['passed']):
            raise ValueError(f'incomplete derived outputs or failed diagnostics: {directory}')
    notebooks = list(directory.glob('*_executed.ipynb'))
    if len(notebooks) != 1:
        raise ValueError(f'expected one executed notebook: {directory}')
    document = nbformat.read(notebooks[0], as_version=4)
    if any(o.get('output_type') == 'error' for c in document.cells for o in c.get('outputs', [])):
        raise ValueError(f'executed notebook contains an error: {directory}')


def validate_local_result(directory):
    """Use the scientific interpreter even when the driver uses system Python."""
    subprocess.run([str(ROOT / 'ceridwen/.venv/bin/python'), '-c',
                    'from pathlib import Path; import sys; '
                    'from scripts.experiment import validate_result; '
                    'validate_result(Path(sys.argv[1]))', str(directory)],
                   cwd=ROOT, check=True, capture_output=True, text=True, timeout=60)


def notebook_has_figures(path):
    document = json.loads(path.read_text())
    return any('image/png' in output.get('data', {})
               for cell in document.get('cells', []) for output in cell.get('outputs', []))


def regenerate_figures(output):
    """Rebuild figures locally for retrieved fits; best-effort, never fails the run.

    Fits run with CERIDWEN_PLOTS=0, so the retrieved notebook has no figures;
    re-executing it locally (CPU, unbilled) restores the standard figures for
    result pages. The GPU-computed derived outputs are kept byte-identical:
    regeneration only adds the notebook figures.
    """
    try:
        manifest = json.loads((output / 'manifest.json').read_text())
        grids = {entry['remote_name']: entry['grid'] for entry in manifest['source'].get('grids', [])}
        cells = {cell['name']: cell for cell in manifest['source']['experiment']}
        completed = manifest.get('completed_cells', [])
    except (OSError, ValueError, KeyError) as error:
        engine.log(f'skipping local figures: unreadable manifest: {error}')
        return
    for name in completed:
        try:
            cell = cells[name]
            directory = (output / 'fits' / cell['arm']
                         / f"{cell['target_metadata']['object_id']}-{cell['target']}")
            notebooks = list(directory.glob('*_executed.ipynb'))
            if len(notebooks) != 1 or notebook_has_figures(notebooks[0]):
                continue
        except (KeyError, OSError, ValueError) as error:
            engine.log(f'skipping local figures for {name}: {error}')
            continue
        settings = dict(cell['settings'])
        remote_grid = Path(settings.get('ssp_grid', '')).name
        if remote_grid in grids:
            # The identical grid file the box used, at its local path.
            settings['ssp_grid'] = grids[remote_grid]
        else:
            engine.log(f'skipping local figures for {name}: grid {remote_grid} is not local')
            continue
        derived = directory / 'ceridwen_derived_outputs.h5'
        gpu_derived = derived.read_bytes() if derived.is_file() else None
        try:
            subprocess.run([str(ROOT / 'ceridwen/.venv/bin/python'),
                            'scripts/regenerate_fit_notebooks.py',
                            '--settings-override', json.dumps(settings),
                            '--priors-override', json.dumps(cell['priors']), str(directory)],
                           cwd=ROOT, check=True, capture_output=True, text=True, timeout=3600)
            engine.log(f'local figures rebuilt for {name}')
        except (subprocess.SubprocessError, OSError) as error:
            engine.log(f'local figure rebuild failed for {name}: {error}; GPU artifacts kept')
        finally:
            if gpu_derived is not None:
                derived.write_bytes(gpu_derived)


def remote(config, output):
    if __package__:
        from . import run_ceridwen_vast_multi_gpu as worker
    else:
        import run_ceridwen_vast_multi_gpu as worker
    # Keep the controller off the GPU, which belongs to the notebook kernel.
    os.environ['JAX_PLATFORMS'] = 'cpu'
    cells = json.loads(config.read_text())
    if len(cells) > 1:
        # Several cells share one notebook kernel; results are those of one kernel per cell.
        os.environ.update(CERIDWEN_SAMPLER_ONLY='0', CERIDWEN_PLOTS='0')
        fits = [{'target': cell['target_metadata'], 'settings_override': json.dumps(cell['settings']),
                 'priors_override': json.dumps(cell['priors']),
                 'result_dir': output / cell['arm'] / '{object_id}-{spect_id}'.format(**cell['target_metadata'])}
                for cell in cells]
        engine.log('fitting ' + ', '.join(f"{c['name']} (seed {c['seed']})" for c in cells) + ' in one kernel')
        worker._execute_targets(fits)
        for cell, fit in zip(cells, fits):
            try:
                validate_result(fit['result_dir'])
            except (OSError, KeyError, ValueError) as error:
                raise RuntimeError(f"fit failed: {cell['name']}") from error
        return 0
    for cell in cells:
        target = cell['target_metadata']
        directory = output / cell['arm'] / f"{target['object_id']}-{target['spect_id']}"
        # Figures render nothing on the box (Agg backend) and are rebuilt locally by
        # regenerate_fit_notebooks.py, so the fit skips their construction entirely.
        os.environ.update(CERIDWEN_SETTINGS_OVERRIDE=json.dumps(cell['settings']),
                          CERIDWEN_PRIORS_OVERRIDE=json.dumps(cell['priors']), CERIDWEN_SAMPLER_ONLY='0',
                          CERIDWEN_PLOTS='0')
        engine.log(f"fitting {cell['name']}, seed {cell['seed']}")
        if worker._execute_target(target, directory) != 0:
            raise RuntimeError(f"fit failed: {cell['name']}")
        validate_result(directory)
    return 0


class Run(engine.Run):
    def __init__(self, args, source):
        grid_bytes = sum(Path(g['grid']).stat().st_size for g in source['grids'])
        input_bytes = (sum((ROOT / p).stat().st_size for p in source['input_files'])
                       if 'input_files' in source else sum(p.stat().st_size for d in engine.INPUT_DIRS
                       for p in (ROOT / 'data/raw' / d).rglob('*') if p.is_file()))
        # Include setup downloads in the transfer reserve, and installed software on disk.
        self.download_gb = max(8, math.ceil((grid_bytes + input_bytes) / 1e9) + 4)
        self.disk_gb = max(40, self.download_gb + 20)
        saved = args.output / 'manifest.json'
        if saved.exists():
            args.spend_cap = min(args.spend_cap, json.loads(saved.read_text())['spend_cap'])
        super().__init__(args, source)

    def budget(self, reserve=0):
        # Leave up to two minutes of rental time to retrieve results before teardown.
        prices = [a['price'] for a in self.data['attempts'] if not a.get('destroyed')]
        return super().budget(reserve + max(prices, default=0) / 30)

    def retrieve(self, attempt, cell, remote_root, *, complete):
        destination = self.root / 'fits'
        result = destination / cell['arm'] / f"{cell['target_metadata']['object_id']}-{cell['target']}"
        error = None
        for retry in range(3):
            remaining = self.args.spend_cap - sum(engine.estimated_spend(a) for a in self.data['attempts'])
            if retry and remaining <= 0:
                break
            timeout = max(1, min(120, int(max(0, remaining) / attempt['price'] * 3600)))
            try:
                target, port = vast._ssh_target(attempt['instance_id'])
                destination.mkdir(exist_ok=True)
                subprocess.run(['rsync', '-a', '--partial', *(['--checksum'] if retry else []),
                                '-e', shlex.join(['ssh', *vast._ssh_options(port)]),
                                f'{target}:{remote_root}/results/', f'{destination}/'],
                               check=True, capture_output=True, timeout=timeout)
                if complete:
                    validate_local_result(result)
                return
            except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError) as caught:
                error = caught
                engine.log(f'result retrieval attempt {retry + 1} failed: {caught}')
        raise engine.StageFailed(f'result retrieval failed; local files: {destination}; '
                                 f'no automatic refit: {error}') from error

    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt['instance_id']
        for index, cell in enumerate(self.data['source']['experiment']):
            if cell['name'] in self.data.get('completed_cells', []):
                continue
            remote_root = f'{engine.REMOTE}/.experiment/{instance}/{index}'
            vast._ssh(instance, f'mkdir -p {remote_root}', timeout=self.timeout(attempt))
            payload = json.dumps([cell])
            vast._ssh(instance, f'printf %s {shlex.quote(payload)} > {remote_root}/config.json',
                      timeout=self.timeout(attempt))
            command = environment + f"SPS_HOME={engine.REMOTE}/external/fsps MPLBACKEND=Agg XLA_FLAGS='--xla_gpu_enable_command_buffer=' " + shlex.join([
                '.venv-ceridwen-gpu/bin/python', 'scripts/experiment.py', 'remote',
                '--config', f'{remote_root}/config.json', '--output', f'{remote_root}/results'])
            try:
                self.stage(attempt, f'fit-{index}', command)
            finally:
                # Recover partial outputs too; preserve a failed fit's original error.
                stage_error = sys.exception()
                try:
                    self.retrieve(attempt, cell, remote_root, complete=stage_error is None)
                except engine.StageFailed as error:
                    if stage_error is None:
                        raise
                    engine.log(str(error))
            self.data.setdefault('completed_cells', []).append(cell['name'])
            self.save()
        attempt['status'] = 'complete'


class ModalRun:
    """Fit the pending cells in Modal GPU containers; the manifest and results match Run."""

    def __init__(self, args, source):
        self.args = args
        self.root = args.output.resolve()
        self.path = self.root / 'manifest.json'
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {
            'backend': 'modal', 'source': source, 'gpus': [args.gpu], 'created': time.time(), 'attempts': []}
        for key, value in (('source', source), ('gpus', [args.gpu])):
            if self.data[key] != value:
                raise vast.SweepError(f'{key} differs from the saved run; use a new --output directory')
        self.data.setdefault('kept', uuid.uuid4().hex)  # this run's directory in each results Volume
        self.profile = modal_gpu.PROFILES[0]  # guard() sets the profile of a launch
        self.refused = set()  # profiles in which Modal started no container for this driver
        self.save()

    def save(self):
        self.data['estimated_total_usd'] = sum(max(a.get('billed_usd', 0), a.get('estimated_usd', 0))
                                               for a in self.data['attempts'])
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.data, indent=2) + '\n')
        temporary.replace(self.path)

    def client(self, *arguments, profile=None, **options):
        environment = {**os.environ, 'MODAL_PROFILE': profile or self.profile,
                       'MODAL_IMAGE_BUILDER_VERSION': modal_gpu.IMAGE_BUILDER,
                       'CERIDWEN_MODAL_IMAGE': self.data['source']['image']}
        return subprocess.run([*modal_gpu.CLIENT, *arguments], cwd=ROOT, env=environment, **options)

    def modal_json(self, *arguments, profile=None):
        return json.loads(self.client('-m', 'modal', *arguments, '--json', profile=profile, capture_output=True,
                                      text=True, check=True, timeout=300).stdout)

    @staticmethod
    def profile_of(attempt):
        """The attempt's Modal profile. Attempts before 2026-11-11 name none: they ran in initalincrease."""
        return attempt.get('profile', 'initalincrease')

    def billed(self):
        """This month's cost in the profile after credits and allowances (network egress, free storage)."""
        return float(self.modal_json('billing', 'summary')['billed_cost'])

    def guard(self):
        """Launch in the first profile whose month the credits cover and that starts containers; stop
        when none is left. Modal bills real money in a profile once billed_cost is above 0."""
        reasons = []
        for profile in modal_gpu.PROFILES:
            self.profile = profile
            if profile in self.refused:
                reasons.append(f'{profile} started no container')
            elif (billed := self.billed()) > 0:
                reasons.append(f'{profile} has ${billed:.2f} billed above credits')
            else:
                return
        raise vast.SweepError('no Modal profile can launch: ' + '; '.join(reasons))

    def watch(self, attempt, work, done):
        """While the containers run: stop the app once Modal bills the profile above its credits."""
        while not done.wait(modal_gpu.CREDIT_CHECK_SECONDS):
            try:
                billed = self.billed()
            except (subprocess.SubprocessError, ValueError) as error:
                engine.log(f'Modal billing summary unavailable: {error}')
                continue
            if billed > 0 and (work / 'calls.json').exists():
                engine.log(f'Modal credits of {self.profile} are used up: ${billed:.2f} billed; stopping the app')
                attempt['credit_stop'] = time.time()
                self.stop(json.loads((work / 'calls.json').read_text())['app_id'])
                return

    def archives(self, work):
        """Pinned source as Run.upload sends it, plus the selected inputs."""
        source = self.data['source']
        trees = [('', ROOT, source['commit'], ('scripts', engine.NOTEBOOK))]
        trees += [(tree, ROOT / tree, revision, ()) for tree, revision in source['submodules'].items()]
        archives = []
        for index, (prefix, tree, revision, paths) in enumerate(trees):
            path = work / f'source-{index}.tar.gz'
            path.write_bytes(subprocess.check_output(['git', '-C', str(tree), 'archive', '--format=tar.gz',
                                                      revision, *paths]))
            archives.append((prefix, str(path)))
        path = work / 'inputs.tar.gz'
        with tarfile.open(path, 'w:gz') as archive:
            for name in source['input_files']:
                archive.add(ROOT / name, name)
            listing = json.dumps(source['input_files']).encode()
            info = tarfile.TarInfo('input-files.json')
            info.size = len(listing)
            archive.addfile(info, io.BytesIO(listing))
        return archives + [('', str(path))]

    def cache_key(self, cell):
        """Everything that fixes a fit's compiled programs: image, GPU, pinned source, and the cell
        without its name and arm. The seed stays: a new seed compiles and autotunes a few new programs."""
        source = self.data['source']
        fixed = {k: v for k, v in cell.items() if k not in ('name', 'arm')}
        text = json.dumps([source['image'], self.args.gpu, source['commit'], source['submodules'], fixed],
                          sort_keys=True)
        return hashlib.sha256(text.encode()).hexdigest()

    def containers(self, pending):
        """Up to the GPU limit, one container per cell; beyond it, cells sorted by cache key share them."""
        ordered = sorted(pending, key=lambda item: self.cache_key(item[1]))
        count = min(len(ordered), modal_gpu.MAX_CONTAINERS)
        return [ordered[i * len(ordered) // count:(i + 1) * len(ordered) // count] for i in range(count)]

    def unpack(self, path, call=None):
        """Results to fits/ exactly as the Vast rsync places them; stage logs beside the manifest.
        A kept fit names its own call; a provisional one is not unpacked."""
        destination = self.root / 'fits'
        with tarfile.open(path) as archive:
            status = json.load(archive.extractfile('status.json'))
            if status.get('provisional'):
                return status
            call = call or status['call']
            for member in archive.getmembers():
                if member.name.startswith('results/') and member.name.count('/') > 1:
                    member.name = member.name.split('/', 2)[2]
                    archive.extract(member, destination, filter='data')
                elif member.name.endswith('.log'):
                    (self.root / f'{call}-{member.name}').write_bytes(archive.extractfile(member).read())
        return status

    def stop(self, app_id, profile=None):
        """Confirm no container of the app is still running."""
        for _ in range(3):
            if all(c['app_id'] != app_id for c in self.modal_json('container', 'list', profile=profile)):
                return
            self.client('-m', 'modal', 'app', 'stop', '-y', app_id, profile=profile, capture_output=True,
                        timeout=300)
            time.sleep(5)
        engine.log(f'Modal app {app_id} still running: stop it with `modal app stop {app_id}`')

    def invoices(self):
        """Modal's own billed cost for each attempt's app, once its hourly intervals have closed."""
        owned = [a for a in self.data['attempts'] if a.get('app_id')]
        start = datetime.fromtimestamp(self.data['created'], UTC).date().isoformat()
        end = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()  # includes the current hour
        for profile in sorted({self.profile_of(a) for a in owned}):
            try:
                rows = self.modal_json('billing', 'report', '--start', start, '--end', end, '-r', 'h',
                                       profile=profile)
            except (subprocess.SubprocessError, ValueError) as error:
                engine.log(f'Modal billing report unavailable: {error}; estimate retained')
                continue
            for attempt in owned:
                costs = [float(row['cost']) for row in rows if row.get('object_id') == attempt['app_id']]
                if costs and self.profile_of(attempt) == profile:
                    attempt['billed_usd'] = sum(costs)

    def pending(self):
        done = self.data.get('completed_cells', [])
        return [(i, c) for i, c in enumerate(self.data['source']['experiment']) if c['name'] not in done]

    def settle(self, attempt, call, index, cell, status, share):
        """One cell's stage exits and cost into the attempt; validate its unpacked result and complete it.
        `status` is the status.json of the cell's archive, or the error that left no archive."""
        record = attempt['cells'][cell['name']] = {'call_id': call, 'profile': self.profile_of(attempt)}
        try:
            if isinstance(status, Exception):
                raise status
            seconds = status['finished'] - status['started']
            fit = status.get('cells', {}).get(str(index), {})
            # The archive's cost is shared equally by its cells.
            record.update(gpu_name=status['gpu'], container_seconds=seconds, container_cells=share,
                          estimated_usd=modal_gpu.cost_usd(self.args.gpu, seconds) / share,
                          exit={**status['exit'], **({'fit': fit['exit']} if fit else {})},
                          **{k: fit[k] for k in ('mode', 'tuned', 'compiled', 'retuned') if k in fit})
            if any(record['exit'].values()) or len(record['exit']) < 2:
                raise engine.StageFailed(f"{cell['name']}: stage exit {record['exit']}; inspect {self.root}/{call}-*.log")
            validate_local_result(self.root / 'fits' / cell['arm']
                                  / f"{cell['target_metadata']['object_id']}-{cell['target']}")
            self.data.setdefault('completed_cells', []).append(cell['name'])
        except (vast.SweepError, engine.StageFailed, subprocess.SubprocessError, OSError, KeyError) as caught:
            record['error'] = f'{type(caught).__name__}: {caught}'
            engine.log(record['error'])
        self.save()

    def recover(self, attempt):
        """The fits that the attempt's containers kept on the results Volume and did not return:
        complete each pending one that is final, then empty the run's directory in that Volume."""
        profile, local = self.profile_of(attempt), self.root / '.modal' / self.data['kept']
        shutil.rmtree(local, ignore_errors=True)
        self.client('-m', 'modal', 'volume', 'get', modal_gpu.RESULT_VOLUME, self.data['kept'] + '/',
                    str(local.parent), profile=profile, capture_output=True, timeout=3600)
        if not local.is_dir():  # the Volume has no fit of this run
            return
        pending = dict(self.pending())
        for path in sorted(local.glob('[0-9]*.tar.gz')):
            index = int(path.name.split('.')[0])
            if index in pending:
                status = self.unpack(path)
                if status.get('provisional'):  # its key's cache autotuned in a shared fit
                    engine.log(f"{pending[index]['name']}: provisional on Volume {modal_gpu.RESULT_VOLUME}; fitted again")
                    continue
                self.settle(attempt, status['call'], index, pending[index], status, 1)
                engine.log(f"{pending[index]['name']}: from Volume {modal_gpu.RESULT_VOLUME} of {profile}")
        shutil.rmtree(local)
        self.forget(profile)

    def forget(self, profile):
        """Empty the run's directory in the profile's results Volume: every kept fit is local or refitted."""
        self.client('-m', 'modal', 'volume', 'rm', '-r', modal_gpu.RESULT_VOLUME, self.data['kept'],
                    profile=profile, capture_output=True, timeout=300)

    def execute(self):
        self.invoices()
        if self.data['attempts'] and self.pending():
            self.recover(self.data['attempts'][-1])
        pending = self.pending()
        if not pending:
            self.save()
            return 0
        self.guard()
        work = self.root / '.modal' / str(len(self.data['attempts']))
        work.mkdir(parents=True, exist_ok=True)
        grids = {entry['remote_name']: entry for entry in self.data['source']['grids']}
        attempt = {'gpu': self.args.gpu, 'profile': self.profile, 'cells': {}, 'started': time.time(),
                   'status': 'running'}
        self.data['attempts'].append(attempt)
        self.save()
        containers = self.containers(pending)
        engine.log(f'launching {len(containers)} Modal {self.args.gpu} container(s) for {len(pending)} cell(s) '
                   f'in {self.profile}')
        done = threading.Event()
        threading.Thread(target=self.watch, args=(attempt, work, done), daemon=True).start()
        try:
            # Source and input archives are transient; only calls and result archives land in work.
            with tempfile.TemporaryDirectory() as temporary:
                request = {'gpu': self.args.gpu, 'grids': list(grids.values()), 'kept': self.data['kept'],
                           'archives': self.archives(Path(temporary)), 'containers': [[
                    {'index': i, 'cell': c, 'key': self.cache_key(c), 'grid': Path(c['settings']['ssp_grid']).name,
                     'grid_sha256': grids[Path(c['settings']['ssp_grid']).name]['grid_sha256']} for i, c in members]
                    for members in containers]}
                (Path(temporary) / 'request.json').write_text(json.dumps(request))
                self.client('scripts/modal_gpu.py', str(Path(temporary) / 'request.json'), str(work))
        finally:
            done.set()
            attempt['elapsed'] = time.time() - attempt['started']
            calls = json.loads((work / 'calls.json').read_text()) if (work / 'calls.json').exists() else {}
            attempt['app_id'] = calls.get('app_id')
            if attempt['app_id']:
                self.stop(attempt['app_id'])
            self.save()
        if not calls:
            # censusgalaxy, 2026-11-11: "InvalidError: Please add a payment method to use L4 GPU functions."
            reason = (work / 'refused').read_text() if (work / 'refused').exists() else 'no message from Modal'
            engine.log(f'skipping {self.profile}: Modal started no container ({reason}); the next profile launches')
            attempt['status'] = 'refused'
            self.save()
            self.refused.add(self.profile)
            return self.execute()
        lost = False
        for number, members in enumerate(containers):
            call = calls.get('calls', {}).get(str(number), f'container-{number}')
            try:
                if (work / f'{number}.error').exists():
                    raise vast.SweepError((work / f'{number}.error').read_text())
                status = self.unpack(work / f'{number}.tar.gz', call)
            except (vast.SweepError, OSError, KeyError) as caught:
                status, lost = caught, True
            for index, cell in members:
                self.settle(attempt, call, index, cell, status, len(members))
            if not isinstance(status, Exception) and all(
                    c['name'] in self.data.get('completed_cells', []) for _, c in members):
                (work / f'{number}.tar.gz').unlink()
        if lost:
            self.recover(attempt)
        else:
            self.forget(self.profile)
        failed = [c['name'] for _, c in self.pending()]
        attempt['estimated_usd'] = sum(r.get('estimated_usd', 0) for r in attempt['cells'].values())
        attempt['status'] = 'failed' if failed else 'complete'
        self.invoices()
        self.save()
        engine.log(f"Modal attempt: ${attempt['estimated_usd']:.4f} estimated; failed cells: {failed or 'none'}")
        if failed and 'credit_stop' in attempt:
            return self.execute()  # the missing fits, in the next profile that the credits cover
        return 1 if failed else 0


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='command', required=True)
    run = commands.add_parser('run', help='preflight, rent, fit, download and destroy')
    run.add_argument('config', type=Path, help='JSON targets, seed, settings, priors and named arms')
    run.add_argument('--gpu', required=True, help='Modal GPU, e.g. L40S; Vast GPU name with --backend vast, e.g. RTX 5090')
    run.add_argument('--backend', choices=('modal', 'vast'), help='default: the saved run\'s backend, else modal')
    run.add_argument('--output', type=Path, help='reuse this directory to resume the same experiment')
    run.add_argument('--image', help='container image reference; saved in the run manifest')
    run.add_argument('--revision', default='HEAD', help='committed project revision; saved revision on resume')
    run.add_argument('--spend-cap', type=vast.experiment_cap, default=1., help='Vast only: total USD across arms and retries; maximum 1')
    run.add_argument('--max-attempts', type=int, default=3)
    run.add_argument('--wait-minutes', type=float, default=0)
    run.add_argument('--dry-run', action='store_true', help='check cached inputs and print the plan; no network or rental')
    worker = commands.add_parser('remote', help=argparse.SUPPRESS)
    worker.add_argument('--config', type=Path, required=True)
    worker.add_argument('--output', type=Path, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    if args.command == 'remote':
        return remote(args.config, args.output)
    if args.max_attempts < 1 or not math.isfinite(args.wait_minutes) or args.wait_minutes < 0:
        raise ValueError('attempts must be positive; wait must be finite and nonnegative')
    args.output = args.output or ROOT / 'results/experiments' / datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')
    saved = args.output / 'manifest.json'
    if saved.exists() and args.revision == 'HEAD':
        args.revision = json.loads(saved.read_text())['source']['commit']
    if args.backend is None:
        args.backend = json.loads(saved.read_text()).get('backend', 'vast') if saved.exists() else 'modal'
    if args.backend == 'modal':
        args.gpu = modal_gpu.gpu_type(args.gpu)
    commands = ('git', 'uv') if args.backend == 'modal' else ('git', 'ssh', 'rsync', 'vastai')
    source = preflight(args.config.resolve(), args.revision, fetch_missing=not args.dry_run, commands=commands)
    if saved.exists() and 'input_files' not in json.loads(saved.read_text())['source']:
        source.pop('input_files', None)
        for cell in source.get('experiment', []):
            cell['target_metadata'].pop('filename', None)
    if args.image:
        source['image'] = args.image
    elif saved.exists() and 'image' in json.loads(saved.read_text())['source']:
        source['image'] = json.loads(saved.read_text())['source']['image']
    elif not saved.exists() and 'input_files' in source:
        source['image'] = DEFAULT_IMAGE
    args.gpus, args.hosts, args.target, args.seed = [args.gpu], 1, 'experiment', 0
    if args.dry_run:
        print(json.dumps({'source': source, 'backend': args.backend, 'gpu': args.gpu,
                          **({'spend_cap': args.spend_cap} if args.backend == 'vast' else {})}, indent=2))
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
    engine.log(f"committed source {source['commit'][:12]}; output {args.output}")
    with (args.output / '.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise vast.SweepError('another driver owns this output directory') from error
        code = (ModalRun if args.backend == 'modal' else Run)(args, source).execute()
        # After teardown, while nothing bills: restore the standard figures locally.
        if code == 0:
            regenerate_figures(args.output)
        return code


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(2)
