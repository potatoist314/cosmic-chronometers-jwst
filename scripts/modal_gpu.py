#!/usr/bin/env python3
"""Modal transport for experiment.py: each fit runs in its own Modal GPU container.

experiment.py runs `CLIENT scripts/modal_gpu.py REQUEST OUTPUT`; the driver's own Python
needs no `modal` package. The container uses the compact image pinned in vast.py, runs the
unchanged Vast bootstrap and `experiment.py remote`, and returns the results directory.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

try:
    import modal
except ModuleNotFoundError:  # the driver's Python; CLIENT supplies the package
    modal = None

PROFILE = 'initalincrease'  # Modal workspace initialincrease
CLIENT = ['uv', 'run', '--quiet', '--no-project', '--python', '3.13', '--with', 'modal==1.6.1', 'python']
APP_NAME = 'ceridwen-experiment'
GRID_VOLUME = 'ceridwen-grids'
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


if modal:
    app = modal.App(APP_NAME)
    grids = modal.Volume.from_name(GRID_VOLUME, create_if_missing=True)
    reference = os.environ.get('CERIDWEN_MODAL_IMAGE')  # set by the local client only
    image = modal.Image.from_registry(reference) if reference else None

    @app.function(image=image, gpu='L4', cpu=CPU_CORES, memory=MEMORY_GIB * 1024, timeout=TIMEOUT_SECONDS,
                  volumes={'/grids': grids.read_only()}, scaledown_window=2)
    def fit(archives, config, grid, grid_sha256):
        """Unpack pinned source and inputs, bootstrap, fit one cell; return the results as tar.gz."""
        started = time.time()
        root = Path(REMOTE)
        for prefix, data in archives:
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                archive.extractall(root / prefix, filter='data')
        (root / 'grid').symlink_to('/grids')
        (root / 'config.json').write_text(config)
        with open(f'/grids/{grid}', 'rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != grid_sha256:
                raise RuntimeError(f'grid checksum mismatch: {grid}')
        # Modal's client libraries must not leak into the fit interpreter.
        environment = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
        environment.update(CERIDWEN_GRID_DIR=f'{REMOTE}/grid', CERIDWEN_GRID_PATH=f'{REMOTE}/grid/{grid}')
        stages = {'bootstrap': 'bash scripts/bootstrap_vast_ai.sh',
                  'fit': f"SPS_HOME={REMOTE}/external/fsps MPLBACKEND=Agg XLA_FLAGS='--xla_gpu_enable_command_buffer=' "
                         '.venv-ceridwen-gpu/bin/python scripts/experiment.py remote --config config.json --output results'}
        status = {}
        for name, command in stages.items():
            with (root / f'{name}.log').open('w') as log:
                process = subprocess.Popen(['bash', '-c', command], cwd=root, env=environment, text=True,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in process.stdout:
                    log.write(line)
                    print(f'{name}: {line}', end='', flush=True)
                status[name] = process.wait()
            if status[name]:
                break
        gpu = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                             capture_output=True, text=True).stdout.strip()
        (root / 'status.json').write_text(json.dumps({'exit': status, 'gpu': gpu, 'started': started,
                                                      'finished': time.time()}))
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            for name in ('status.json', 'bootstrap.log', 'fit.log', 'results'):
                if (root / name).exists():
                    archive.add(root / name, name)
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
    """Run every requested cell concurrently; write <index>.tar.gz as each finishes."""
    request = json.loads(Path(request_path).read_text())
    output = Path(output)
    archives = [(prefix, Path(path).read_bytes()) for prefix, path in request['archives']]
    with modal.enable_output(), app.run():
        upload_grids(request['grids'])
        calls = {}
        for cell in request['cells']:
            calls[cell['index']] = fit.with_options(gpu=request['gpu']).spawn(
                archives, json.dumps([cell['cell']]), cell['grid'], cell['grid_sha256'])
        (output / 'calls.json').write_text(json.dumps(
            {'app_id': app.app_id, 'calls': {i: c.object_id for i, c in calls.items()}}))
        failures = 0
        for index, call in calls.items():
            try:
                (output / f'{index}.tar.gz').write_bytes(call.get())
            except Exception as error:  # one failed container must not discard the others
                failures += 1
                (output / f'{index}.error').write_text(f'{type(error).__name__}: {error}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main(*sys.argv[1:]))
