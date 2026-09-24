#!/usr/bin/env python3
"""Run configured Ceridwen fits on Vast: experiment.py run CONFIG --gpu 'RTX 5090'."""
from __future__ import annotations

import argparse
import ast
import fcntl
import json
import math
import os
import re
import shlex
import signal
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

if __package__:
    from . import benchmark as engine
else:
    import benchmark as engine

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


def preflight(path, revision, *, fetch_missing=False):
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
            source = engine.preflight(revision, grid_name=name, targets={c['target'] for c in cells},
                                      workers=('experiment.py', 'run_ceridwen_vast_multi_gpu.py'))
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
    for cell in cells:
        if cell['target'] not in targets:
            raise ValueError(f"target not in the production selection: {cell['target']}")
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


def remote(config, output):
    if __package__:
        from . import run_ceridwen_vast_multi_gpu as worker
    else:
        import run_ceridwen_vast_multi_gpu as worker
    # Keep the controller off the GPU, which belongs to the notebook kernel.
    os.environ['JAX_PLATFORMS'] = 'cpu'
    for cell in json.loads(config.read_text()):
        target = cell['target_metadata']
        directory = output / cell['arm'] / f"{target['object_id']}-{target['spect_id']}"
        os.environ.update(CERIDWEN_SETTINGS_OVERRIDE=json.dumps(cell['settings']),
                          CERIDWEN_PRIORS_OVERRIDE=json.dumps(cell['priors']), CERIDWEN_SAMPLER_ONLY='0')
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

    def measure(self, attempt):
        environment = self.prepare(attempt)
        instance = attempt['instance_id']
        target, port = vast._ssh_target(instance)
        for index, cell in enumerate(self.data['source']['experiment']):
            if cell['name'] in self.data.get('completed_cells', []):
                continue
            remote_root = f'{engine.REMOTE}/.experiment/{instance}/{index}'
            vast._ssh(instance, f'mkdir -p {remote_root}', timeout=self.timeout(attempt))
            payload = json.dumps([cell])
            vast._ssh(instance, f'printf %s {shlex.quote(payload)} > {remote_root}/config.json',
                      timeout=self.timeout(attempt))
            command = environment + "MPLBACKEND=Agg XLA_FLAGS='--xla_gpu_enable_command_buffer=' " + shlex.join([
                '.venv-ceridwen-gpu/bin/python', 'scripts/experiment.py', 'remote',
                '--config', f'{remote_root}/config.json', '--output', f'{remote_root}/results'])
            try:
                self.stage(attempt, f'fit-{index}', command)
            finally:
                # Keep partial notebooks and logs too, before the shared lifecycle destroys the box.
                destination = self.root / 'fits'
                destination.mkdir(exist_ok=True)
                shell = shlex.join(['ssh', *vast._ssh_options(port)])
                stage_error = sys.exception()
                try:
                    subprocess.run(['rsync', '-a', '-e', shell, f'{target}:{remote_root}/results/',
                                    f'{destination}/'], check=True, capture_output=True,
                                   timeout=max(1, min(120, int(super().budget() / attempt['price'] * 3600))))
                except (vast.SweepError, subprocess.SubprocessError, OSError) as error:
                    if stage_error is None:
                        raise
                    # Preserve a fatal stage error even if it produced no results to pull.
                    engine.log(f'partial result download failed: {error}')
            self.data.setdefault('completed_cells', []).append(cell['name'])
            self.save()
        attempt['status'] = 'complete'


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='command', required=True)
    run = commands.add_parser('run', help='preflight, rent, fit, download and destroy')
    run.add_argument('config', type=Path, help='JSON targets, seed, settings, priors and named arms')
    run.add_argument('--gpu', required=True, help='Vast GPU name, e.g. RTX 5090')
    run.add_argument('--output', type=Path, help='reuse this directory to resume the same experiment')
    run.add_argument('--image', help='container image reference; saved in the run manifest')
    run.add_argument('--revision', default='HEAD', help='committed project revision; saved revision on resume')
    run.add_argument('--spend-cap', type=vast.experiment_cap, default=1., help='total USD across arms and retries; maximum 1')
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
    source = preflight(args.config.resolve(), args.revision, fetch_missing=not args.dry_run)
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
        print(json.dumps({'source': source, 'gpu': args.gpu, 'spend_cap': args.spend_cap}, indent=2))
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
    engine.log(f"committed source {source['commit'][:12]}; output {args.output}")
    with (args.output / '.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise vast.SweepError('another driver owns this output directory') from error
        return Run(args, source).execute()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        raise SystemExit(main())
    except (vast.SweepError, subprocess.SubprocessError, OSError, ValueError, SyntaxError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(2)
