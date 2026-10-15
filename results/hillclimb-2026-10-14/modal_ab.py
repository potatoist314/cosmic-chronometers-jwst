"""Same-container A/B fits of the benchmark galaxy on Modal.

    python3 modal_ab.py stage LABEL [--commit REV] [--patch FILE] [--ceridwen-patch FILE]
    python3 modal_ab.py run PLAN.json OUTDIR [--gpu L40S]

A plan is a list of steps {"label", "env", "cells", "seed", "settings", "concurrent", "mps", "cpus", "argv"}; steps run in
order in one container, each as the production `scripts/experiment.py remote`
call. Each staged label is a full source tree: project scripts and notebook at
REV (plus PATCH), and the ceridwen and sedpy_jax trees pinned by REV.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] if len(HERE.parents) > 1 else HERE  # the container imports this file from /root
STAGE = Path(os.environ.get('HILLCLIMB_STAGE', HERE / '.stage'))
# benchmark-cells.json: the benchmark galaxy M5_238580 first, then M4_107643 (warm-up fit only).
CELLS = json.loads((HERE / 'benchmark-cells.json').read_text()) if (HERE / 'benchmark-cells.json').exists() else None
IMAGE = 'ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34'
GRID = Path.home() / '.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5'
GRID_REMOTE = '/workspace/cosmic-chronometers-jwst/grid/6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67.h5'
INPUTS = ['data/raw/cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits',
          'data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits',
          'data/raw/cosmos2020/cosmos2020_classic_legac_dr2_1arcsec.fits',
          'data/raw/cosmos2020/cosmos2020_farmer_legac_dr2_1arcsec.fits',
          'data/raw/cosmos2025/cosmos2025_phot_legac_dr2_1arcsec.fits',
          'data/raw/hst_f814w/M5_238580.fits', 'data/raw/legac_dr2/legaCdr2.fits.gz',
          'data/raw/legac_dr2/sp/legac_M5_238580_v2.0.fits',
          'data/raw/hst_f814w/M4_107643.fits', 'data/raw/legac_dr2/sp/legac_M4_107643_v2.0.fits']


def git(*args, cwd=ROOT, **kw):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, **kw).stdout


def extract(archive: bytes, destination: Path):
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(destination, filter='data')


def stage(label, commit, patch=None, ceridwen_patch=None):
    destination = STAGE / label
    if destination.exists():
        raise SystemExit(f'{destination} exists')
    destination.mkdir(parents=True)
    extract(git('archive', commit, 'scripts', 'notebooks', 'pyproject.toml'), destination)
    if patch:
        subprocess.run(['git', 'apply', str(Path(patch).resolve())], cwd=destination, check=True)
    for path, sub in (('ceridwen', 'ceridwen'), ('external/sedpy_jax', 'external/sedpy_jax')):
        pinned = git('rev-parse', f'{commit}:{path}', text=True).strip()
        extract(git('archive', pinned, cwd=ROOT / sub), destination / path)
    if ceridwen_patch:
        subprocess.run(['git', 'apply', str(Path(ceridwen_patch).resolve())], cwd=destination / 'ceridwen', check=True)
    (destination / 'external/fsps/data').mkdir(parents=True)
    (destination / 'external/fsps/data/emlines_info.dat').write_bytes((ROOT / 'external/fsps/data/emlines_info.dat').read_bytes())
    (destination / 'STAGED').write_text(json.dumps({'commit': git('rev-parse', commit, text=True).strip(),
                                                     'patch': patch, 'ceridwen_patch': ceridwen_patch}))


import modal

LABELS = [x for x in os.environ.get('HILLCLIMB_LABELS', '').split(',') if x]
GPU = os.environ.get('HILLCLIMB_GPU', 'L40S')
# modal_gpu.py (modal-gpu branch) requests 2 cores and 16 GiB per fit container.
CPU = float(os.environ.get('HILLCLIMB_CPU', '2'))
MEMORY_GIB = int(os.environ.get('HILLCLIMB_MEMORY_GIB', '16'))
image = (modal.Image.from_registry(IMAGE)
         .run_commands('/opt/ceridwen/bin/python -m ipykernel install --user --name ceridwen',
                       "/opt/ceridwen/bin/python -c \"import json,pathlib;p=pathlib.Path('/root/.local/share/jupyter/kernels/ceridwen/kernel.json');k=json.loads(p.read_text());k['env']={'JAX_ENABLE_X64':'1','JAX_PLATFORMS':'cuda'};p.write_text(json.dumps(k))\""))
if modal.is_local():
    image = image.add_local_file(GRID, GRID_REMOTE)
    for name in INPUTS:
        image = image.add_local_file(ROOT / name, f'/workspace/data-shared/{name}')
    for label in LABELS:
        image = image.add_local_dir(STAGE / label, f'/workspace/v/{label}')
app = modal.App('hillclimb-ab', image=image)

@app.function(gpu=GPU, timeout=6 * 3600, cpu=CPU, memory=MEMORY_GIB * 1024)
def run(plan, cells, called_at):
    import glob
    import shutil
    entered = time.time()
    info = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader'],
                          capture_output=True, text=True).stdout.strip()
    cpu_info = subprocess.run(['sh', '-c', "grep -m1 'model name' /proc/cpuinfo; nproc"], capture_output=True, text=True).stdout
    out = []
    mps = None
    for index, step in enumerate(plan):
        if step.get('mps') and mps is None:
            os.makedirs('/tmp/mps-pipe', exist_ok=True)
            os.makedirs('/tmp/mps-log', exist_ok=True)
            os.environ.update(CUDA_MPS_PIPE_DIRECTORY='/tmp/mps-pipe', CUDA_MPS_LOG_DIRECTORY='/tmp/mps-log')
            mps = subprocess.run(['nvidia-cuda-mps-control', '-d'], capture_output=True, text=True)
            out.append({'index': index, 'label': 'mps-start', 'returncode': mps.returncode,
                        'stdout': mps.stdout, 'stderr': mps.stderr, 'start': time.time(), 'end': time.time()})
        procs = []
        for copy in range(step.get('concurrent', 1)):
            root = Path('/workspace/v') / step['label']
            work = Path(f'/workspace/run/{index}-{copy}')
            if work.exists():
                shutil.rmtree(work)
            tree = work / 'tree'
            shutil.copytree(root, tree, symlinks=True)
            (tree / 'data').symlink_to('/workspace/data-shared/data')
            # As the Vast upload: the bootstrap verifies the selected inputs listed here.
            (tree / 'input-files.json').write_text(json.dumps(INPUTS + ['external/fsps/data/emlines_info.dat']))
            config = work / 'config.json'
            by_target = {c['target']: c for c in cells}
            chosen = [json.loads(json.dumps(by_target[t])) for t in step.get('cells', ['M5_238580'])]
            for cell in chosen:  # proposal steps: another seed or changed settings
                if 'seed' in step:
                    cell['seed'] = cell['target_metadata']['seed'] = step['seed']
                cell['settings'].update(step.get('settings', {}))
            config.write_text(json.dumps(chosen))
            env = {**os.environ, 'SPS_HOME': f'{tree}/external/fsps', 'MPLBACKEND': 'Agg',
                   'XLA_FLAGS': '--xla_gpu_enable_command_buffer=',
                   'CERIDWEN_GRID_DIR': str(Path(GRID_REMOTE).parent), 'CERIDWEN_GRID_PATH': GRID_REMOTE,
                   'PYTHONPATH': f'{tree}/ceridwen:{tree}/external/sedpy_jax', **step.get('env', {})}
            if step.get('concurrent', 1) > 1:
                env['XLA_CLIENT_MEM_FRACTION'] = f"{round(0.85 / step['concurrent'], 2):.2f}"
            argv = step.get('argv', ['/opt/ceridwen/bin/python', 'scripts/experiment.py', 'remote',
                                     '--config', str(config), '--output', str(work / 'results')])
            if 'cpus' in step:  # pin this step's processes to a subset of the container's cores
                argv = ['taskset', '-c', step['cpus'], *argv]
            log = open(work / 'stdout.txt', 'w')
            procs.append((work, time.time(), subprocess.Popen(argv, cwd=tree, env=env, stdout=log,
                                                              stderr=subprocess.STDOUT, text=True)))
        ends = {}
        while len(ends) < len(procs):
            for copy, (_, _, proc) in enumerate(procs):
                if copy not in ends and proc.poll() is not None:
                    ends[copy] = time.time()
            time.sleep(0.5)
        for copy, (work, start, proc) in enumerate(procs):
            returncode, end = proc.returncode, ends[copy]
            print(f"step {index} copy {copy} {step['label']}: exit {returncode} after {end - start:.1f} s", flush=True)
            files = {}
            for path in glob.glob(f'{work}/results/**/*', recursive=True):
                p = Path(path)
                if p.is_file() and p.suffix in ('.h5', '.ipynb', '.jsonl', '.log', '.json'):
                    files[str(p.relative_to(work))] = p.read_bytes()
            out.append({'index': index, 'copy': copy, 'label': step['label'], 'env': step.get('env', {}),
                        'concurrent': step.get('concurrent', 1), 'start': start, 'end': end,
                        'returncode': returncode, 'stdout': (work / 'stdout.txt').read_text()[-20000:],
                        'files': files})
        for work, _, _ in procs:
            shutil.rmtree(work)
    if mps is not None:
        subprocess.run(['sh', '-c', 'echo quit | nvidia-cuda-mps-control'], capture_output=True)
    return {'called_at': called_at, 'entered': entered, 'finished': time.time(), 'gpu': info, 'cpu_info': cpu_info, 'steps': out}


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    s = sub.add_parser('stage')
    s.add_argument('label')
    s.add_argument('--commit', default='HEAD')
    s.add_argument('--patch')
    s.add_argument('--ceridwen-patch')
    r = sub.add_parser('run')
    r.add_argument('plan', type=Path)
    r.add_argument('out', type=Path)
    r.add_argument('--gpu', default='L40S')
    args = parser.parse_args()
    if args.command == 'stage':
        return stage(args.label, args.commit, args.patch, args.ceridwen_patch)
    plan = json.loads(args.plan.read_text())
    if sorted({step['label'] for step in plan}) != sorted(LABELS) or args.gpu != GPU:
        raise SystemExit('set HILLCLIMB_LABELS to the plan labels and HILLCLIMB_GPU to --gpu')
    args.out.mkdir(parents=True, exist_ok=True)
    called = time.time()
    with app.run():
        result = run.remote(plan, CELLS, called)
    returned = time.time()
    for step in result['steps']:
        directory = args.out / f"{step['index']:02d}-{step['label']}-{step.get('copy', 0)}"
        for name, data in step.pop('files', {}).items():
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    result.update(returned=returned, plan=plan, gpu_requested=args.gpu, cpu=CPU, memory_gib=MEMORY_GIB)
    (args.out / 'timings.json').write_text(json.dumps(result, indent=1))
    print(json.dumps({'cold_start_s': result['entered'] - called, 'gpu': result['gpu'],
                      'steps': [(s['label'], round(s['end'] - s['start'], 1), s['returncode']) for s in result['steps']]}))


if __name__ == '__main__':
    sys.exit(main())
