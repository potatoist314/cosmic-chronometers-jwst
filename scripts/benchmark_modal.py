#!/usr/bin/env python3
"""Time one Ceridwen fit configuration on Modal GPUs, stage by stage.

python3 scripts/benchmark_modal.py run CONFIG --gpu T4 --containers 4 --fits 2 --output DIR
ceridwen/.venv/bin/python scripts/benchmark_modal.py summarize DIR... --reference L40S --output OUT

Each container times, in order: source unpack, the grid read from the Volume, the
bootstrap and --fits repeats of the one configured fit (experiment.py remote). Image,
grid Volume, resources and prices come from modal_gpu.py; the manifest, archives,
app stop and billed costs from experiment.ModalRun.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import io
import json
import os
import statistics
import subprocess
import sys
import tarfile
import threading
import time
from pathlib import Path
from types import SimpleNamespace

if __package__:
    from . import modal_gpu
else:
    import modal_gpu

# USD per second, https://modal.com/pricing (read 2026-10-14). "H100!" opts out of the
# automatic H200 upgrade (https://modal.com/docs/guide/gpu) and bills as an H100.
GPU_USD_PER_SECOND = {**modal_gpu.GPU_USD_PER_SECOND, 'H100!': modal_gpu.GPU_USD_PER_SECOND['H100'],
                      'B300': 0.001972}
STAGE_PREFIX = (f'SPS_HOME={modal_gpu.REMOTE}/external/fsps MPLBACKEND=Agg '
                "XLA_FLAGS='--xla_gpu_enable_command_buffer=' ")
KEY_PARAMETERS = ('logmass', 'logzsol', 'afe', 'diffuse_tau_noll', 'sigma_smooth', 'mass-weighted age [Gyr]')
SAMPLER_CELL = 'joint_result = run_sampler('
GRID_CELL = 'ssp = SSPDataAfe.load('


def rate_usd_per_second(gpu):
    """Published GPU price plus the requested CPU cores and memory, as modal_gpu.cost_usd."""
    return (GPU_USD_PER_SECOND[gpu] + modal_gpu.CPU_CORES * modal_gpu.CPU_USD_PER_CORE_SECOND
            + modal_gpu.MEMORY_GIB * modal_gpu.MEMORY_USD_PER_GIB_SECOND)


if modal_gpu.modal:
    modal = modal_gpu.modal
    app = modal.App('ceridwen-gpu-bench')

    # Modal mounts only the entry module; the container imports modal_gpu too.
    image = modal_gpu.image.add_local_python_source('modal_gpu') if modal_gpu.image else None

    @app.function(image=image, gpu='L4', cpu=modal_gpu.CPU_CORES, memory=modal_gpu.MEMORY_GIB * 1024,
                  timeout=modal_gpu.TIMEOUT_SECONDS, volumes={'/grids': modal_gpu.grids.read_only()},
                  scaledown_window=2)
    def bench(archives, config, grid, grid_sha256, fits):
        """Unpack, read the grid, bootstrap and time each fit; return the results as tar.gz."""
        marks = {'entered': time.time()}
        root = Path(modal_gpu.REMOTE)
        for prefix, data in archives:
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                archive.extractall(root / prefix, filter='data')
        (root / 'grid').symlink_to('/grids')
        (root / 'config.json').write_text(config)
        marks['unpacked'] = time.time()
        with open(f'/grids/{grid}', 'rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != grid_sha256:
                raise RuntimeError(f'grid checksum mismatch: {grid}')
        marks['grid_read'] = time.time()
        cell = json.loads(config)[0]
        fit_dir = f"{cell['arm']}/{cell['target_metadata']['object_id']}-{cell['target']}"
        environment = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
        environment.update(CERIDWEN_GRID_DIR=f'{modal_gpu.REMOTE}/grid',
                           CERIDWEN_GRID_PATH=f'{modal_gpu.REMOTE}/grid/{grid}')
        stages = [('bootstrap', 'bash scripts/bootstrap_vast_ai.sh')]
        stages += [(f'fit-{k}', STAGE_PREFIX + '.venv-ceridwen-gpu/bin/python scripts/experiment.py remote '
                    f'--config config.json --output results/fit-{k}') for k in range(fits)]
        records = {}
        for name, command in stages:
            record = records[name] = {'started': time.time()}
            progress = root / 'results' / name / fit_dir / 'ns_progress.jsonl'
            done = threading.Event()

            def watch(path=progress, record=record, done=done):
                # The first progress line lands one iteration after the sampler clock starts.
                while not done.is_set():
                    if path.is_file() and path.stat().st_size:
                        record['progress_seen'] = time.time()
                        return
                    time.sleep(0.05)

            watcher = threading.Thread(target=watch, daemon=True)
            if name.startswith('fit-'):
                watcher.start()
            with (root / f'{name}.log').open('w') as log:
                record['exit'] = subprocess.run(['bash', '-c', command], cwd=root, env=environment,
                                                stdout=log, stderr=subprocess.STDOUT).returncode
            record['finished'] = time.time()
            done.set()
            if record['exit']:
                break
        query = 'name,driver_version,memory.total,clocks.max.sm,power.limit,compute_cap'
        gpu = subprocess.run(['nvidia-smi', f'--query-gpu={query}', '--format=csv,noheader'],
                             capture_output=True, text=True).stdout.strip()
        (root / 'hardware.txt').write_text(subprocess.run(['nvidia-smi', '-q'], capture_output=True,
                                                          text=True).stdout)
        marks['finished'] = time.time()
        (root / 'status.json').write_text(json.dumps({'marks': marks, 'stages': records, 'gpu': gpu,
                                                      'query': query, 'cpu_count': os.cpu_count()}))
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            for name in ['status.json', 'hardware.txt', 'results', *(f'{s}.log' for s, _ in stages)]:
                if (root / name).exists():
                    archive.add(root / name, name)
        return {'archive': buffer.getvalue(), 'packed': time.time()}


def launch(request_path, work):
    """Keep at most `concurrent` containers running until `containers` have finished."""
    request = json.loads(Path(request_path).read_text())
    work = Path(work)
    archives = [(prefix, Path(path).read_bytes()) for prefix, path in request['archives']]
    calls, lock = {'calls': {}}, threading.Lock()

    def save():
        with lock:
            (work / 'calls.json').write_text(json.dumps(calls, indent=1))

    def one(index):
        record = calls['calls'][str(index)] = {'spawned': time.time()}
        call = bench.with_options(gpu=request['gpu']).spawn(
            archives, json.dumps([request['cell']]), request['grid'], request['grid_sha256'], request['fits'])
        record['call_id'] = call.object_id
        save()
        try:
            returned = call.get()
            record['received'] = time.time()
            record['packed'] = returned['packed']
            (work / f'{index}.tar.gz').write_bytes(returned['archive'])
        except Exception as error:  # one failed container must not discard the others
            record['received'] = time.time()
            (work / f'{index}.error').write_text(f'{type(error).__name__}: {error}')
        save()

    with modal.enable_output(), app.run():
        modal_gpu.upload_grids(request['grids'])
        calls['app_id'] = app.app_id
        save()
        with concurrent.futures.ThreadPoolExecutor(request['concurrent']) as pool:
            list(pool.map(one, range(request['containers'])))
    return 0


def run(args):
    if __package__:
        from . import experiment as exp
    else:
        import experiment as exp
    engine = exp.engine
    if args.gpu not in GPU_USD_PER_SECOND:
        raise ValueError(f'{args.gpu!r} is not a Modal GPU; choose one of {", ".join(GPU_USD_PER_SECOND)}')
    source = exp.preflight(args.config.resolve(), args.revision, fetch_missing=True, commands=('git', 'uv'))
    source['image'] = exp.DEFAULT_IMAGE
    if len(source['experiment']) != 1:
        raise ValueError('a benchmark configuration has one arm and one target')
    cell = source['experiment'][0]
    grid = Path(cell['settings']['ssp_grid']).name
    entry = next(g for g in source['grids'] if g['remote_name'] == grid)
    args.output.mkdir(parents=True, exist_ok=True)
    holder = exp.ModalRun(SimpleNamespace(output=args.output, gpu=args.gpu), source)
    # billed_cost is the month's cost after credits and allowances (ModalRun.guard omits the latter).
    if float(holder.modal_json('billing', 'summary')['billed_cost']) > 0:
        raise ValueError('Modal credits no longer cover this month')
    work = args.output / '.modal' / str(len(holder.data['attempts']))
    work.mkdir(parents=True, exist_ok=True)
    request = {'gpu': args.gpu, 'containers': args.containers, 'concurrent': args.concurrent,
               'fits': args.fits, 'grids': source['grids'], 'archives': holder.archives(work), 'cell': cell,
               'grid': grid, 'grid_sha256': entry['grid_sha256']}
    (work / 'request.json').write_text(json.dumps(request))
    attempt = {'gpu': args.gpu, 'containers': {}, 'fits_per_container': args.fits, 'started': time.time(),
               'status': 'running'}
    holder.data['attempts'].append(attempt)
    holder.save()
    engine.log(f'launching {args.containers} Modal {args.gpu} container(s), {args.concurrent} at a time')
    try:
        holder.client('scripts/benchmark_modal.py', 'launch', str(work / 'request.json'), str(work))
    finally:
        attempt['elapsed'] = time.time() - attempt['started']
        calls = json.loads((work / 'calls.json').read_text()) if (work / 'calls.json').exists() else {}
        attempt['app_id'] = calls.get('app_id')
        if attempt['app_id']:
            holder.stop(attempt['app_id'])
        holder.save()
    failed = []
    for index, call in sorted(calls.get('calls', {}).items(), key=lambda item: int(item[0])):
        name = f"{index}-{call.get('call_id', 'unspawned')}"
        record = attempt['containers'][name] = dict(call)
        destination = args.output / 'containers' / name
        try:
            if (work / f'{index}.error').exists():
                raise RuntimeError((work / f'{index}.error').read_text())
            with tarfile.open(work / f'{index}.tar.gz') as archive:
                archive.extractall(destination, filter='data')
            status = json.loads((destination / 'status.json').read_text())
            seconds = status['marks']['finished'] - status['marks']['entered']
            record.update(gpu=status['gpu'], exit={k: v['exit'] for k, v in status['stages'].items()},
                          container_seconds=seconds,
                          estimated_usd=rate_usd_per_second(args.gpu) * seconds)
            for k in range(args.fits):
                exp.validate_local_result(destination / 'results' / f'fit-{k}' / cell['arm']
                                          / f"{cell['target_metadata']['object_id']}-{cell['target']}")
        except (RuntimeError, OSError, KeyError, ValueError, subprocess.SubprocessError, tarfile.TarError) as error:
            record['error'] = f'{type(error).__name__}: {error}'
            failed.append(name)
            engine.log(f'{name}: {record["error"]}')
        holder.save()
    attempt['estimated_usd'] = sum(r.get('estimated_usd', 0) for r in attempt['containers'].values())
    attempt['status'] = 'failed' if failed else 'complete'
    holder.invoices()
    holder.save()
    engine.log(f"{args.gpu}: ${attempt['estimated_usd']:.4f} estimated; failed containers: {failed or 'none'}")
    return 1 if failed else 0


def cell_seconds(notebook):
    """Kernel-clock start and end of each executed code cell, keyed by cell index."""
    from datetime import datetime
    spans = {}
    for index, cell in enumerate(notebook['cells']):
        timing = cell.get('metadata', {}).get('execution', {})
        if 'iopub.execute_input' in timing and 'shell.execute_reply' in timing:
            spans[index] = tuple(datetime.fromisoformat(timing[key].replace('Z', '+00:00')).timestamp()
                                 for key in ('iopub.execute_input', 'shell.execute_reply'))
    return spans


def fit_record(directory, stage):
    """Stage times, evidence and key posteriors of one fit."""
    import h5py
    notebook = json.loads(next(directory.glob('*_executed.ipynb')).read_text())
    spans = cell_seconds(notebook)
    sampler = next(i for i, c in enumerate(notebook['cells']) if SAMPLER_CELL in ''.join(c['source']))
    grid_cell = next(i for i, c in enumerate(notebook['cells']) if GRID_CELL in ''.join(c['source']))
    first = json.loads((directory / 'ns_progress.jsonl').read_text().splitlines()[0])
    with h5py.File(directory / 'ceridwen_result.h5') as result:
        samples = dict(result['samples'].attrs)
    with h5py.File(directory / 'ceridwen_derived_outputs.h5') as derived:
        summary = derived['summary']
        names = [n.decode() if isinstance(n, bytes) else str(n) for n in summary['parameter'][()]]
        posterior = {n: {'q16': float(a), 'q50': float(b), 'q84': float(c)} for n, a, b, c in
                     zip(names, summary['q16'][()], summary['q50'][()], summary['q84'][()])}
    sampling = float(samples['wall_time_s'])
    # The sampler clock starts after the init and step compile; its first line follows one iteration.
    clock_start = stage['progress_seen'] - first['elapsed_s']
    start, end = spans[sampler]
    before = [spans[i] for i in spans if i < sampler]
    return {
        'notebook_setup_s': spans[sampler][0] - min(s for s, _ in before) if before else None,
        'model_and_grid_cell_s': spans[grid_cell][1] - spans[grid_cell][0],
        'compile_s': clock_start - start,
        'sampling_s': sampling,
        'sampler_cell_after_s': end - (clock_start + sampling),
        'post_fit_cells_s': max(e for _, e in spans.values()) - end,
        'fit_stage_s': stage['finished'] - stage['started'],
        'n_likelihood_calls': int(samples['n_likelihood_calls']),
        'sampling_calls_per_s': int(samples['n_likelihood_calls']) / sampling,
        'log_evidence': float(samples['log_evidence']),
        'log_evidence_err': float(samples['log_evidence_err']),
        'posterior': {n: posterior[n] for n in KEY_PARAMETERS if n in posterior},
    }


def container_record(directory, call, gpu, fits_dir):
    status = json.loads((directory / 'status.json').read_text())
    marks, stages = status['marks'], status['stages']
    fits = []
    for name in sorted((s for s in stages if s.startswith('fit-')), key=lambda s: int(s[4:])):
        if stages[name]['exit'] == 0:
            fits.append(fit_record(directory / 'results' / name / fits_dir, stages[name]))
    return {
        'call_id': call['call_id'], 'gpu': status['gpu'], 'requested_gpu': gpu,
        'container_start_s': marks['entered'] - call['spawned'],
        'unpack_s': marks['unpacked'] - marks['entered'],
        'grid_read_s': marks['grid_read'] - marks['unpacked'],
        'bootstrap_s': stages['bootstrap']['finished'] - stages['bootstrap']['started'],
        'pack_s': call['packed'] - marks['finished'],
        'retrieval_s': call['received'] - call['packed'],
        'container_s': marks['finished'] - marks['entered'],
        'fits': fits,
    }


def spread(values):
    return {'median': statistics.median(values), 'min': min(values), 'max': max(values), 'n': len(values)}


def summarize(args):
    cards = {}
    for run_dir in args.runs:
        manifest = json.loads((run_dir / 'manifest.json').read_text())
        cell = manifest['source']['experiment'][0]
        fits_dir = f"{cell['arm']}/{cell['target_metadata']['object_id']}-{cell['target']}"
        gpu = manifest['gpus'][0]
        card = cards.setdefault(gpu, {'gpu': gpu, 'run': str(run_dir), 'containers': [], 'billed_usd': 0.0,
                                      'commit': manifest['source']['commit']})
        for attempt in manifest['attempts']:
            card['billed_usd'] += attempt.get('billed_usd', 0)
            for name, call in attempt.get('containers', {}).items():
                if 'error' in call or not (run_dir / 'containers' / name / 'status.json').is_file():
                    continue
                card['containers'].append(container_record(run_dir / 'containers' / name, call, gpu, fits_dir))
    if len({c['commit'] for c in cards.values()}) != 1:
        raise ValueError('runs come from different commits')
    for card in cards.values():
        per_container = [statistics.mean(f['sampling_s'] for f in c['fits']) for c in card['containers'] if c['fits']]
        card['sampling_s'] = spread([f['sampling_s'] for c in card['containers'] for f in c['fits']])
        card['container_mean_sampling_s'] = per_container
        card['sampling_calls_per_s'] = spread([f['sampling_calls_per_s'] for c in card['containers'] for f in c['fits']])
        for stage in ('container_start_s', 'unpack_s', 'grid_read_s', 'bootstrap_s', 'retrieval_s'):
            card[stage] = spread([c[stage] for c in card['containers']])
        for stage in ('model_and_grid_cell_s', 'compile_s', 'post_fit_cells_s', 'fit_stage_s'):
            card[stage] = spread([f[stage] for c in card['containers'] for f in c['fits']])
        rate = rate_usd_per_second(card['gpu'])
        card['usd_per_second'] = rate
        card['sampling_usd_per_fit'] = rate * card['sampling_s']['median']
        # One production container: setup, bootstrap, the first fit of each container and packing.
        card['container_usd_per_fit'] = rate * statistics.median(
            c['unpack_s'] + c['grid_read_s'] + c['bootstrap_s'] + c['fits'][0]['fit_stage_s'] + c['pack_s']
            for c in card['containers'] if c['fits'])
    reference = cards[args.reference]
    ref_time = reference['sampling_s']['median']
    for card in cards.values():
        relative = [ref_time / t for t in card['container_mean_sampling_s']]
        card['relative_sampling_speed'] = {**spread(relative), 'median': ref_time / card['sampling_s']['median']}
        card['relative_calls_per_s'] = (card['sampling_calls_per_s']['median']
                                        / reference['sampling_calls_per_s']['median'])
        card['relative_sampling_cost'] = card['sampling_usd_per_fit'] / reference['sampling_usd_per_fit']
        card['relative_container_cost'] = card['container_usd_per_fit'] / reference['container_usd_per_fit']
    fits = [f for card in cards.values() for c in card['containers'] for f in c['fits']]
    agreement = {'log_evidence': spread([f['log_evidence'] for f in fits]),
                 'log_evidence_err_median': statistics.median(f['log_evidence_err'] for f in fits)}
    for name in KEY_PARAMETERS:
        medians = [f['posterior'][name]['q50'] for f in fits if name in f['posterior']]
        widths = [(f['posterior'][name]['q84'] - f['posterior'][name]['q16']) / 2 for f in fits
                  if name in f['posterior']]
        if medians:  # a configuration can fix a parameter, e.g. afe
            agreement[name] = {**spread(medians), 'half_width_median': statistics.median(widths)}
    args.output.write_text(json.dumps({'reference': args.reference, 'commit': reference['commit'],
                                       'cards': cards, 'agreement': agreement}, indent=1) + '\n')
    print(f'wrote {args.output}')
    return 0


def parser():
    result = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = result.add_subparsers(dest='command', required=True)
    command = commands.add_parser('run', help='preflight, launch containers, retrieve and stop')
    command.add_argument('config', type=Path, help='experiment JSON with one arm and one target')
    command.add_argument('--gpu', required=True, help=f'Modal GPU: {", ".join(GPU_USD_PER_SECOND)}')
    command.add_argument('--output', type=Path, required=True)
    command.add_argument('--containers', type=int, default=3)
    command.add_argument('--concurrent', type=int, default=3, help='containers running at one time')
    command.add_argument('--fits', type=int, default=2, help='fit repeats in each container')
    command.add_argument('--revision', default='HEAD')
    command = commands.add_parser('launch', help=argparse.SUPPRESS)
    command.add_argument('request')
    command.add_argument('work')
    command = commands.add_parser('summarize', help='stage times, relative speed and cost per card')
    command.add_argument('runs', type=Path, nargs='+')
    command.add_argument('--reference', required=True, help='GPU whose median sampling time is 1')
    command.add_argument('--output', type=Path, required=True)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    if args.command == 'launch':
        return launch(args.request, args.work)
    if args.command == 'summarize':
        return summarize(args)
    return run(args)


if __name__ == '__main__':
    raise SystemExit(main())
