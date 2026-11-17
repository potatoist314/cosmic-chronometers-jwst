"""Same-container A/B fits of DR3 common-window cells on a Modal A100.

    python3 modal_ab.py cells TARGET [TARGET ...]          # benchmark-cells.json from the production manifest
    python3 modal_ab.py stage LABEL [--commit REV] [--ceridwen REV]
    python3 modal_ab.py run PLAN.json OUTDIR                # needs AB_LABELS=<labels of the plan>
    python3 modal_ab.py summary OUTDIR

A plan is a list of steps {"label", "cells": ["dr3_cn_free_w/M1_210210", ...], "env", "seed", "settings",
"profile", "seed_cache", "persist", "prefix"}; steps run in order in one container, each as the production `scripts/experiment.py remote`
call on an empty JAX compile cache (the state of every first-time fit). Several cells in one step share one
notebook kernel. "seed_cache": N starts the step on a copy of step N's finished cache, at step N's path
(JAX 0.10 keys each program by the cache path). A staged label is a source tree: this worktree's scripts and notebook at --commit, ceridwen
at --ceridwen (a revision of the ceridwen worktree), sedpy_jax at the pin of --commit.
"profile" records JAX's trace, lowering, compile and cache durations per notebook cell.
Adapted from results/hillclimb-2026-10-14/modal_ab.py.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] if len(HERE.parents) > 1 else HERE  # the container imports this file from /root
MAIN = Path('/Users/liuhao/Downloads/Astro project')  # data, sedpy_jax and fsps live in the main checkout
STAGE = HERE / '.stage'
MANIFEST = MAIN / 'results/legac-dr3-2026-11-11/window-194/run/manifest.json'
IMAGE = 'ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34'
REMOTE = '/workspace/cosmic-chronometers-jwst'  # the cell settings name the grid under REMOTE/grid
GRID = '6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67.h5'
GPU, CPU, MEMORY_GIB = 'A100-40GB', float(os.environ.get('AB_CPU', 2.0)), 16  # scripts/modal_gpu.py; AB_CPU: a core-count test
USD_PER_SECOND = 0.000583 + CPU * 0.0000131 + MEMORY_GIB * 0.00000222  # scripts/modal_gpu.py
PROFILE_HOOK = '''
import collections, json, os, threading, time
import jax.monitoring
_events, _cell, _long, _cells, _start = collections.defaultdict(lambda: [0, 0.0]), [0], [], [], [time.time()]
def _record(event, duration, **_):
    entry = _events[(_cell[0], event)]
    entry[0] += 1
    entry[1] += duration
    if duration >= 0.3:
        _long.append({"cell": _cell[0], "event": event, "end": time.time(), "seconds": duration,
                      "thread": threading.current_thread().name})
jax.monitoring.register_event_duration_secs_listener(_record)
def _begin(info=None):
    _start[0] = time.time()
def _dump(result=None):
    progress = os.path.join(str(get_ipython().user_ns.get("RESULT_DIR", "")), "ns_progress.jsonl")
    _cells.append({"cell": _cell[0], "start": _start[0], "end": time.time(),
                   "sampler_end": os.path.getmtime(progress) if os.path.exists(progress) else None})
    rows = [{"cell": cell, "event": event, "count": n, "seconds": s} for (cell, event), (n, s) in _events.items()]
    with open(os.environ["AB_PROFILE_OUT"], "w") as handle:
        json.dump({"events": rows, "long": _long, "cells": _cells}, handle)
    _cell[0] += 1
get_ipython().events.register("pre_run_cell", _begin)
get_ipython().events.register("post_run_cell", _dump)
'''


def git(*args, cwd=ROOT, **kw):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, **kw).stdout


def extract(archive: bytes, destination: Path):
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(destination, filter='data')


def cells(targets):
    wanted = [cell for cell in json.loads(MANIFEST.read_text())['source']['experiment']
              if cell['target'] in targets and cell['arm'] in ('dr3_cn_free_w', 'dr3_plain_w')]
    (HERE / 'benchmark-cells.json').write_text(json.dumps(wanted, indent=1))
    print([cell['name'] for cell in wanted])


def stage(label, commit, ceridwen):
    destination = STAGE / label
    if destination.exists():
        raise SystemExit(f'{destination} exists')
    destination.mkdir(parents=True)
    extract(git('archive', commit, 'scripts', 'notebooks', 'pyproject.toml'), destination)
    extract(git('archive', ceridwen, cwd=ROOT / 'ceridwen'), destination / 'ceridwen')
    shutil.rmtree(destination / 'ceridwen/tests')  # 89 MB that no fit reads
    sedpy = git('rev-parse', f'{commit}:external/sedpy_jax', text=True).strip()
    extract(git('archive', sedpy, cwd=MAIN / 'external/sedpy_jax'), destination / 'external/sedpy_jax')
    (destination / 'external/fsps/data').mkdir(parents=True)
    (destination / 'external/fsps/data/emlines_info.dat').write_bytes(
        (MAIN / 'external/fsps/data/emlines_info.dat').read_bytes())
    (destination / 'STAGED').write_text(json.dumps({
        'commit': git('rev-parse', commit, text=True).strip(),
        'ceridwen': git('rev-parse', ceridwen, cwd=ROOT / 'ceridwen', text=True).strip(), 'sedpy_jax': sedpy}))


def inputs(chosen):
    sys.path.insert(0, str(ROOT / 'scripts'))
    import vast
    vast.PROJECT_ROOT = MAIN  # the alf response files are listed from the data directory
    return sorted(str(name) for name in vast.selected_inputs(chosen))


import modal

LABELS = [x for x in os.environ.get('AB_LABELS', '').split(',') if x]
image = (modal.Image.from_registry(IMAGE)
         .run_commands('/opt/ceridwen/bin/python -m ipykernel install --user --name ceridwen',
                       "/opt/ceridwen/bin/python -c \"import json,pathlib;p=pathlib.Path('/root/.local/share/jupyter/kernels/ceridwen/kernel.json');k=json.loads(p.read_text());k['env']={'JAX_ENABLE_X64':'1','JAX_PLATFORMS':'cuda'};p.write_text(json.dumps(k))\""))
if modal.is_local() and LABELS:
    CELLS = json.loads((HERE / 'benchmark-cells.json').read_text())
    INPUTS = inputs(CELLS)
    for name in INPUTS:
        image = image.add_local_file(MAIN / name, f'/workspace/data-shared/{name}')
    for label in LABELS:
        image = image.add_local_dir(STAGE / label, f'/workspace/v/{label}')
    # bench steps: lnl_check.py and the dead points of the production fit of each cell
    image = image.add_local_file(HERE / 'lnl_check.py', '/workspace/bench/lnl_check.py')
    for cell in CELLS:
        fit = MANIFEST.parent / 'fits' / cell['arm'] / f"{cell['target_metadata']['object_id']}-{cell['target']}"
        image = image.add_local_file(next(fit.glob('ns_raw_dead_*.pkl')),
                                     f"/workspace/bench/dead/{cell['name'].replace('/', '-')}.pkl")
app = modal.App('speedups-overnight-ab', image=image)
grids = modal.Volume.from_name('ceridwen-grids')
scratch = modal.Volume.from_name('speedups-overnight-scratch', create_if_missing=True)  # times save and keep only


@app.function(gpu=GPU, timeout=3 * 3600, cpu=CPU, memory=MEMORY_GIB * 1024, volumes={'/grids': grids.read_only(), '/scratch': scratch})
def run(plan, cells, input_files, called_at):
    import glob
    import shutil
    entered = time.time()
    info = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader'],
                          capture_output=True, text=True).stdout.strip()
    cpu_info = subprocess.run(['sh', '-c', "grep -m1 'model name' /proc/cpuinfo; nproc"], capture_output=True, text=True).stdout
    Path(REMOTE).mkdir(parents=True, exist_ok=True)
    if not Path(REMOTE, 'grid').exists():
        Path(REMOTE, 'grid').symlink_to('/grids')
    by_name = {cell['name']: cell for cell in cells}
    hook = Path.home() / '.ipython/profile_default/startup/00-ab-profile.py'
    out = []
    for index, step in enumerate(plan):
        tree = Path('/workspace/trees') / step['label']
        if not tree.exists():  # one copy per label, byte-compiled once, as an installed package is
            shutil.copytree(Path('/workspace/v') / step['label'], tree, symlinks=True)
            (tree / 'data').symlink_to('/workspace/data-shared/data')
            (tree / 'input-files.json').write_text(json.dumps(input_files))
            subprocess.run(['/opt/ceridwen/bin/python', '-m', 'compileall', '-q', str(tree / 'ceridwen/ceridwen'),
                            str(tree / 'external/sedpy_jax'), str(tree / 'scripts')], capture_output=True)
        work = Path(f'/workspace/run/{index}')
        work.mkdir(parents=True)
        chosen = [json.loads(json.dumps(by_name[name])) for name in step['cells']]
        for cell in chosen:
            if 'seed' in step:
                cell['seed'] = cell['target_metadata']['seed'] = step['seed']
            cell['settings'].update(step.get('settings', {}))
        (work / 'config.json').write_text(json.dumps(chosen))
        cache = Path(f"/tmp/xla/{step.get('seed_cache', index)}")
        if 'seed_cache' in step:
            shutil.copytree(f"/tmp/xla-kept/{step['seed_cache']}", cache)
        else:
            cache.mkdir(parents=True)
        autotune = cache / 'xla_gpu_per_fusion_autotune_cache_dir'
        count = lambda: (sum(1 for path in cache.iterdir() if path.is_file()), len(list(autotune.glob('*'))))
        before = count()
        # scripts/modal_gpu.py fit and fit_cell: no PYTHONPATH from Modal's client, no XLA_FLAGS.
        env = {**{k: v for k, v in os.environ.items() if k != 'PYTHONPATH'},
               'SPS_HOME': f'{tree}/external/fsps', 'MPLBACKEND': 'Agg',
               'CERIDWEN_GRID_DIR': f'{REMOTE}/grid', 'CERIDWEN_GRID_PATH': f'{REMOTE}/grid/{GRID}',
               'JAX_COMPILATION_CACHE_DIR': str(cache), 'JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS': '0',
               'PYTHONPATH': f'{tree}/ceridwen:{tree}/external/sedpy_jax', **step.get('env', {})}
        if step.get('profile'):
            hook.parent.mkdir(parents=True, exist_ok=True)
            hook.write_text(PROFILE_HOOK)
            env['AB_PROFILE_OUT'] = str(work / 'results/jax-profile.json')
            (work / 'results').mkdir()
        argv = [*step.get('prefix', []), '/opt/ceridwen/bin/python', 'scripts/experiment.py', 'remote',
                '--config', str(work / 'config.json'), '--output', str(work / 'results')]
        if step.get('bench'):  # ln L parts on the GPU instead of a fit: lnl_check.py parts
            (work / 'results').mkdir(exist_ok=True)
            env.update(LNL_CHECK_TREE=str(tree), JAX_PLATFORMS='cuda', JAX_ENABLE_X64='1')
            argv = ['/opt/ceridwen/bin/python', '/workspace/bench/lnl_check.py', 'parts',
                    str(work / 'results/parts.npz'), '--cell', str(work / 'config.json'),
                    '--dead', f"/workspace/bench/dead/{step['cells'][0].replace('/', '-')}.pkl",
                    '--data-root', str(tree), *step.get('bench_args', [])]
        start = time.time()
        with open(work / 'stdout.txt', 'w') as log:
            returncode = subprocess.run(argv, cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        end = time.time()
        hook.unlink(missing_ok=True)
        persist = {}
        if step.get('persist'):  # scripts/modal_gpu.py save and keep, on a scratch Volume
            mark = time.time()
            with tarfile.open(f'/scratch/.cache-{index}', 'w') as archive:
                archive.add(cache, '.')
            Path(f'/scratch/.cache-{index}').replace(f'/scratch/cache-{index}.tar')
            scratch.commit()
            persist['save_s'] = time.time() - mark
            mark = time.time()
            with tarfile.open(f'/scratch/.results-{index}', 'w:gz') as archive:
                archive.add(work / 'results', 'results')
            Path(f'/scratch/.results-{index}').replace(f'/scratch/results-{index}.tar.gz')
            scratch.commit()
            persist['keep_s'] = time.time() - mark
            persist['results_bytes'] = sum(path.stat().st_size for path in (work / 'results').rglob('*') if path.is_file())
        print(f"step {index} {step['label']} {step['cells']}: exit {returncode} after {end - start:.1f} s", flush=True)
        files = {}
        for path in glob.glob(f'{work}/results/**/*', recursive=True):
            p = Path(path)
            if p.is_file() and (p.suffix in ('.h5', '.ipynb', '.jsonl', '.log', '.json', '.npz') or p.name.startswith('ns_raw_dead')):
                files[str(p.relative_to(work))] = p.read_bytes()
        out.append({'index': index, 'label': step['label'], 'cells': step['cells'], 'start': start, 'end': end,
                    'returncode': returncode, 'persist': persist, 'stdout': (work / 'stdout.txt').read_text()[-20000:],
                    'compiled': count()[0] - before[0], 'tuned': count()[1] - before[1],
                    'cache_bytes': sum(path.stat().st_size for path in cache.rglob('*') if path.is_file()),
                    'files': files})
        shutil.rmtree(work)
        Path('/tmp/xla-kept').mkdir(exist_ok=True)
        shutil.move(cache, f'/tmp/xla-kept/{index}')
    return {'called_at': called_at, 'entered': entered, 'finished': time.time(), 'gpu': info, 'cpu_info': cpu_info,
            'steps': out}


def launch(plan_path, out):
    plan = json.loads(plan_path.read_text())
    if sorted({step['label'] for step in plan}) != sorted(LABELS):
        raise SystemExit('set AB_LABELS to the plan labels')
    out.mkdir(parents=True, exist_ok=True)
    called = time.time()
    with app.run():
        result = run.remote(plan, CELLS, INPUTS, called)
    returned = time.time()
    for step in result['steps']:
        directory = out / f"{step['index']:02d}-{step['label']}"
        for name, data in step.pop('files', {}).items():
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    result.update(returned=returned, plan=plan, usd=(result['finished'] - result['entered']) * USD_PER_SECOND,
                  staged={label: json.loads((STAGE / label / 'STAGED').read_text()) for label in LABELS})
    (out / 'timings.json').write_text(json.dumps(result, indent=1))
    summary(out)


def cell_seconds(notebook):
    """Seconds of each code cell of an executed notebook (nbclient's execution timestamps)."""
    from datetime import datetime
    seconds = []
    for cell in json.loads(notebook.read_text())['cells']:
        timing = cell.get('metadata', {}).get('execution', {})
        if cell['cell_type'] == 'code' and 'shell.execute_reply' in timing:
            stamp = lambda key: datetime.fromisoformat(timing[key].replace('Z', '+00:00')).timestamp()
            seconds.append(stamp('shell.execute_reply') - stamp('iopub.execute_input'))
    return seconds


def summary(out):
    result = json.loads((out / 'timings.json').read_text())
    print(f"gpu {result['gpu']} | cold start {result['entered'] - result['called_at']:.0f} s | "
          f"container {result['finished'] - result['entered']:.0f} s | ${result['usd']:.2f}")
    for step in result['steps']:
        directory = out / f"{step['index']:02d}-{step['label']}"
        print(f"{step['index']:2d} {step['label']:10s} exit {step['returncode']} process {step['end'] - step['start']:6.1f} s  "
              f"compiled {step['compiled']} tuned {step['tuned']} cache {step['cache_bytes'] / 1e6:.0f} MB")
        if step.get('persist'):
            print(f"     save {step['persist']['save_s']:.1f} s  keep {step['persist']['keep_s']:.1f} s  "
                  f"results {step['persist']['results_bytes'] / 1e6:.0f} MB")
        for progress in sorted(directory.rglob('ns_progress.jsonl')):
            last = json.loads(progress.read_text().splitlines()[-1])
            cells_s = [second for notebook in progress.parent.glob('*_executed.ipynb') for second in cell_seconds(notebook)]
            print(f"     {progress.parent.parent.name}/{progress.parent.name}: sampler {last['elapsed_s']:6.1f} s  "
                  f"calls {last['n_likelihood_calls'] / 1e6:.3f} M  {last['n_likelihood_calls'] / last['elapsed_s']:7.0f} /s  "
                  f"logZ {last['logZ']:.4f}  cells " + ' '.join(f'{second:.1f}' for second in cells_s))
        if result['plan'][step['index']].get('bench'):
            print(''.join(f'     {line}\n' for line in step['stdout'].splitlines() if ' batch of ' in line), end='')
        profile = directory / 'results/jax-profile.json'
        if profile.exists():
            data = json.loads(profile.read_text())
            data = data if isinstance(data, dict) else {'events': data, 'long': [], 'cells': []}
            for row in sorted(data['events'], key=lambda row: (row['cell'], row['event'])):
                if row['seconds'] >= 0.5:
                    print(f"     cell {row['cell']:2d} {row['event']:60s} n {row['count']:5d}  {row['seconds']:7.1f} s")
            starts = {cell['cell']: cell for cell in data['cells']}
            for cell in data['cells']:  # the sampler cell: seconds before the first iteration and after the last
                if cell['sampler_end'] and cell['start'] < cell['sampler_end']:
                    progress = sorted(directory.rglob('ns_progress.jsonl'))
                    wall = json.loads(progress[0].read_text().splitlines()[-1])['elapsed_s'] if len(progress) == 1 else float('nan')
                    print(f"     cell {cell['cell']:2d} before sampler {cell['sampler_end'] - wall - cell['start']:.1f} s, "
                          f"after sampler {cell['end'] - cell['sampler_end']:.1f} s")
            for row in data['long']:
                if row['seconds'] >= 1.0:
                    print(f"     cell {row['cell']:2d} +{row['end'] - starts[row['cell']]['start'] if row['cell'] in starts else float('nan'):6.1f} s "
                          f"{row['seconds']:5.1f} s {row['thread']:22s} {row['event'].rsplit('/', 1)[-1]}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('cells')
    c.add_argument('targets', nargs='+')
    s = sub.add_parser('stage')
    s.add_argument('label')
    s.add_argument('--commit', default='HEAD')
    s.add_argument('--ceridwen', default='HEAD')
    r = sub.add_parser('run')
    r.add_argument('plan', type=Path)
    r.add_argument('out', type=Path)
    m = sub.add_parser('summary')
    m.add_argument('out', type=Path)
    args = parser.parse_args()
    if args.command == 'cells':
        return cells(args.targets)
    if args.command == 'stage':
        return stage(args.label, args.commit, args.ceridwen)
    if args.command == 'summary':
        return summary(args.out)
    return launch(args.plan, args.out)


if __name__ == '__main__':
    sys.exit(main())
