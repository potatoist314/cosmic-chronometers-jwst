#!/usr/bin/env python3
"""Modal transport for experiment.py: each Modal GPU container fits one or more cells.

experiment.py runs `CLIENT scripts/modal_gpu.py REQUEST OUTPUT`; the driver's own Python
needs no `modal` package. The container uses the compact image pinned in vast.py, runs the
unchanged Vast bootstrap and one `experiment.py remote` per cell, and returns the results
directory. JAX compile caches, with XLA's autotune choices, persist per cell setup on a Volume.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    import modal
except ModuleNotFoundError:  # the driver's Python; CLIENT supplies the package
    modal = None

PROFILE = 'initalincrease'  # Modal workspace initialincrease
CLIENT = ['uv', 'run', '--quiet', '--no-project', '--python', '3.13', '--with', 'modal==1.6.1', 'python']
APP_NAME = 'ceridwen-experiment'
GRID_VOLUME = 'ceridwen-grids'
CACHE_VOLUME = 'ceridwen-xla-cache'
CACHE = Path('/xla-cache')  # <cache key>.tar: one cell setup's JAX compile cache
FITS_PER_GPU = 4  # cached fits sharing one GPU (results/hillclimb-2026-10-14/LEDGER.md entries 15, 18)
MAX_CONTAINERS = 10  # Starter plan, "10 GPU concurrency": https://modal.com/pricing (read 2026-10-15)
MPS = {'CUDA_MPS_PIPE_DIRECTORY': '/tmp/mps-pipe', 'CUDA_MPS_LOG_DIRECTORY': '/tmp/mps-log'}
REMOTE = '/workspace/cosmic-chronometers-jwst'  # vast.REMOTE_ROOT: the settings name grids under REMOTE/grid
CPU_CORES = 2.0
MEMORY_GIB = 16
TIMEOUT_SECONDS = 6 * 3600

# USD per second, https://modal.com/pricing (read 2026-10-14). B300 needs CUDA 13.1; the image has CUDA 12.
GPU_USD_PER_SECOND = {
    'T4': 0.000164, 'L4': 0.000222, 'A10': 0.000306, 'L40S': 0.000542, 'A100-40GB': 0.000583,
    'A100-80GB': 0.000694, 'RTX-PRO-6000': 0.000842, 'H100': 0.001097, 'H200': 0.001261, 'B200': 0.001736,
}
CPU_USD_PER_CORE_SECOND = 0.0000131
MEMORY_USD_PER_GIB_SECOND = 0.00000222
ALIASES = {'A10G': 'A10', 'A100': 'A100-40GB', 'A100-40G': 'A100-40GB', 'A100-80G': 'A100-80GB', 'RTX-6000-PRO': 'RTX-PRO-6000'}


def gpu_type(value):
    """Modal GPU name for a --gpu value; spaces, underscores and case do not matter."""
    name = '-'.join(value.upper().replace('_', ' ').split())
    name = ALIASES.get(name, name)
    if name not in GPU_USD_PER_SECOND:
        raise ValueError(f'{value!r} is not a Modal GPU; choose one of {", ".join(GPU_USD_PER_SECOND)}, '
                         'or pass --backend vast for a Vast GPU such as "RTX 5090"')
    return name


def cost_usd(gpu, seconds):
    """Published per-second price of the GPU plus the requested CPU cores and memory."""
    rate = (GPU_USD_PER_SECOND[gpu] + CPU_CORES * CPU_USD_PER_CORE_SECOND
            + MEMORY_GIB * MEMORY_USD_PER_GIB_SECOND)
    return rate * seconds


@contextlib.contextmanager
def mps():
    """CUDA MPS daemon, so that fits sharing the GPU run their kernels side by side."""
    for path in MPS.values():
        os.makedirs(path, exist_ok=True)
    subprocess.run(['nvidia-cuda-mps-control', '-d'], env={**os.environ, **MPS}, check=True)
    try:
        yield
    finally:
        subprocess.run(['nvidia-cuda-mps-control'], input='quit\n', text=True, env={**os.environ, **MPS})


def schedule(cells, cached, fit_one, save, sharing=mps):
    """Fit each cell once; returns {index: record}.

    A cell without a saved compile cache fits alone, on an empty cache, and saves it: XLA times its
    autotuning candidates, and on a shared GPU it picks differently (LEDGER entry 14). The other cells
    then share the GPU, FITS_PER_GPU at a time, reading their caches. If a shared fit autotuned any
    fusion, its cache was incomplete: every shared fit of that cache fits again alone. Programs that
    JAX compiled anew without autotuning (another host type) are added to the saved cache.
    """
    records, ready = {}, []
    for cell in cells:
        if cached(cell['key']):
            ready.append(cell)
        else:
            records[cell['index']] = fit_one(cell, 'alone')
            if records[cell['index']]['exit'] == 0:
                save(cell['key'])
    mode = 'shared' if len(ready) > 1 else 'cached'
    with sharing() if mode == 'shared' else contextlib.nullcontext():
        with ThreadPoolExecutor(FITS_PER_GPU) as pool:
            for cell, record in zip(ready, pool.map(lambda cell: fit_one(cell, mode), ready)):
                records[cell['index']] = record
    missed = {}
    for cell in ready:
        if records[cell['index']]['mode'] == 'shared' and records[cell['index']]['tuned']:
            missed[cell['key']] = missed.get(cell['key'], 0) + records[cell['index']]['tuned']
    for key in {cell['key'] for cell in ready if records[cell['index']]['compiled']} - missed.keys():
        if all(records[cell['index']]['exit'] == 0 for cell in ready if cell['key'] == key):
            save(key)
    for cell in ready:
        if missed.get(cell['key']):
            records[cell['index']] = {**fit_one(cell, 'alone'), 'retuned': missed[cell['key']]}
            if records[cell['index']]['exit'] == 0:
                save(cell['key'])
    return records


def stage(root, name, command, environment):
    """Run one shell stage in root; its output goes to <name>.log and to the Modal log."""
    with (root / f'{name}.log').open('w') as log:
        process = subprocess.Popen(['bash', '-c', command], cwd=root, env=environment, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in process.stdout:
            log.write(line)
            print(f'{name}: {line}', end='', flush=True)
        return process.wait()


if modal:
    app = modal.App(APP_NAME)
    grids = modal.Volume.from_name(GRID_VOLUME, create_if_missing=True)
    caches = modal.Volume.from_name(CACHE_VOLUME, create_if_missing=True)
    reference = os.environ.get('CERIDWEN_MODAL_IMAGE')  # set by the local client only
    image = modal.Image.from_registry(reference) if reference else None

    extracting = threading.Lock()

    def fit_cell(root, cell, mode, environment):
        """One cell in its own kernel. JAX's compile cache, with XLA's autotune cache inside it, has one
        directory per cache key, at the same path wherever it is written or read: JAX 0.10 keys each
        compiled program by the autotune directory's path as well (jax/_src/cache_key.py)."""
        index, cache = cell['index'], Path('/tmp/xla') / cell['key']
        shutil.rmtree(root / 'results' / str(index), ignore_errors=True)
        with extracting:
            if mode == 'alone':
                shutil.rmtree(cache, ignore_errors=True)
            if not cache.exists():
                cache.mkdir(parents=True)
                if mode != 'alone':
                    with tarfile.open(CACHE / f"{cell['key']}.tar") as archive:
                        archive.extractall(cache, filter='data')
        # JAX keeps XLA's per-fusion autotune cache in this subdirectory (jax_persistent_cache_enable_xla_caches).
        tuned = lambda: len(list((cache / 'xla_gpu_per_fusion_autotune_cache_dir').glob('*')))
        compiled = lambda: sum(1 for path in cache.iterdir() if path.is_file())
        before = tuned(), compiled()
        (root / f'config-{index}.json').write_text(json.dumps([cell['cell']]))
        environment = {**environment, 'JAX_COMPILATION_CACHE_DIR': str(cache),
                       'JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS': '0'}
        if mode == 'shared':
            # run_ceridwen_vast_multi_gpu.py's --fits-per-gpu share of GPU memory.
            environment.update(MPS, XLA_CLIENT_MEM_FRACTION=f'{0.85 / FITS_PER_GPU:.2f}')
        started = time.time()
        code = stage(root, f'fit-{index}', f'SPS_HOME={REMOTE}/external/fsps MPLBACKEND=Agg .venv-ceridwen-gpu/bin/python '
                     f'scripts/experiment.py remote --config config-{index}.json --output results/{index}', environment)
        return {'exit': code, 'mode': mode, 'started': started, 'finished': time.time(),
                'tuned': tuned() - before[0], 'compiled': compiled() - before[1]}

    def save(key):
        """The key's cache directory to the Volume: a complete file under a temporary name, renamed,
        so that no reader or commit sees a partial cache."""
        temporary = CACHE / f'.{key}.{uuid.uuid4().hex}'
        with tarfile.open(temporary, 'w') as archive:
            archive.add(Path('/tmp/xla') / key, '.')
        temporary.replace(CACHE / f'{key}.tar')
        caches.commit()

    @app.function(image=image, gpu='L4', cpu=CPU_CORES, memory=MEMORY_GIB * 1024, timeout=TIMEOUT_SECONDS,
                  volumes={'/grids': grids.read_only(), str(CACHE): caches}, scaledown_window=2)
    def fit(archives, cells):
        """Unpack pinned source and inputs, bootstrap once, fit the cells; return the results as tar.gz."""
        started = time.time()
        root = Path(REMOTE)
        for prefix, data in archives:
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                archive.extractall(root / prefix, filter='data')
        (root / 'grid').symlink_to('/grids')
        for grid, digest in {(cell['grid'], cell['grid_sha256']) for cell in cells}:
            with open(f'/grids/{grid}', 'rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != digest:
                    raise RuntimeError(f'grid checksum mismatch: {grid}')
        # Modal's client libraries must not leak into the fit interpreter.
        environment = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
        environment.update(CERIDWEN_GRID_DIR=f'{REMOTE}/grid')
        # The bootstrap checks the first cell's grid; each fit reads its own.
        status = {'exit': {'bootstrap': stage(root, 'bootstrap', 'bash scripts/bootstrap_vast_ai.sh', {
            **environment, 'CERIDWEN_GRID_PATH': f"{REMOTE}/grid/{cells[0]['grid']}"})}}
        if not status['exit']['bootstrap']:
            status['cells'] = schedule(cells, lambda key: (CACHE / f'{key}.tar').exists(),
                                       lambda cell, mode: fit_cell(root, cell, mode, {
                                           **environment, 'CERIDWEN_GRID_PATH': f"{REMOTE}/grid/{cell['grid']}"}),
                                       save)
        gpu = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                             capture_output=True, text=True).stdout.strip()
        (root / 'status.json').write_text(json.dumps({**status, 'gpu': gpu, 'started': started,
                                                      'finished': time.time()}))
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            for path in ['status.json', 'bootstrap.log', *sorted(root.glob('fit-*.log')), 'results']:
                if (root / path).exists():
                    archive.add(root / path, Path(path).name)
        return buffer.getvalue()


def upload_grids(entries):
    """Upload each grid once; later runs find it in the Volume by its SHA-256 name."""
    present = {entry.path.strip('/') for entry in grids.listdir('/')}
    missing = [entry for entry in entries if entry['remote_name'] not in present]
    if missing:
        with grids.batch_upload() as batch:
            for entry in missing:
                print(f"uploading grid {entry['grid']} to Volume {GRID_VOLUME}", flush=True)
                batch.put_file(entry['grid'], f"/{entry['remote_name']}")


def main(request_path, output):
    """Run every requested container concurrently; write <container>.tar.gz as each finishes."""
    request = json.loads(Path(request_path).read_text())
    output = Path(output)
    archives = [(prefix, Path(path).read_bytes()) for prefix, path in request['archives']]
    with modal.enable_output(), app.run():
        upload_grids(request['grids'])
        calls = {number: fit.with_options(gpu=request['gpu']).spawn(archives, cells)
                 for number, cells in enumerate(request['containers'])}
        (output / 'calls.json').write_text(json.dumps(
            {'app_id': app.app_id, 'calls': {i: c.object_id for i, c in calls.items()}}))
        failures = 0
        for number, call in calls.items():
            try:
                (output / f'{number}.tar.gz').write_bytes(call.get())
            except Exception as error:  # one failed container must not discard the others
                failures += 1
                (output / f'{number}.error').write_text(f'{type(error).__name__}: {error}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main(*sys.argv[1:]))
