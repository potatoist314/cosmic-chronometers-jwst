"""Same-runtime A/B fits on a Colab A100: the steps of ab.py on one runtime, through scripts/colab.py.

    python3 colab_ab.py up SESSION LABEL [LABEL ...]     # allocate, image files, grid, inputs, staged trees
    python3 colab_ab.py push SESSION LABEL [LABEL ...]   # more staged trees
    python3 colab_ab.py run SESSION PLAN.json OUTDIR
    python3 colab_ab.py collect SESSION PLAN.json OUTDIR   # a launched plan, after a lost connection
    python3 colab_ab.py down SESSION

The runtime gets the image files and grid as scripts/colab.py prepares them; each step runs the staged
tree's `scripts/experiment.py remote` with the image's /opt/ceridwen Python, as results/speedups-overnight-
2026-11-16/modal_ab.py did on Modal.
"""
from __future__ import annotations

import argparse
import io
import json
import shlex
import sys
import tarfile
import time
from pathlib import Path

import ab

sys.path.insert(0, str(ab.ROOT / 'scripts'))
import colab  # noqa: E402

UNITS_PER_HOUR = 6.73  # one A100 runtime, results/dr3-more-galaxies-2026-11-16/first-10/run/manifest.json


class Runtime(colab.ColabRun):
    """ColabRun's SSH, rsync, detached stages and allocation, without a run manifest."""

    def __init__(self, out):
        self.args = argparse.Namespace(gpu='A100', wait_minutes=30)
        self.root = out
        self.data = {}

    def save(self):
        pass


def attempt(session):
    return {'session': session, 'number': 'ab'}


def tar(entries):
    """A tar of (name in archive, local path) pairs."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as archive:
        for name, path in entries:
            archive.add(path, name)
    return buffer.getvalue()


def push(runtime, session, labels):
    for label in labels:
        runtime.ssh(session, f'mkdir -p /workspace/v/{label} && tar -x -C /workspace/v/{label}',
                    data=tar([('.', ab.STAGE / label)]), timeout=600)


def up(session, labels):
    runtime = Runtime(ab.HERE / 'runs')
    runtime.root.mkdir(exist_ok=True)
    state = attempt(session)
    runtime.allocate(state)
    print(runtime.ssh(session, 'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader; nproc; free -g | head -2'))
    runtime.ssh(session, f'mkdir -p {ab.REMOTE}/.colab /workspace/grid && cat > {ab.REMOTE}/.colab/image.py',
                data=colab.IMAGE_PROGRAM.encode())
    runtime.launch(session, 'image', shlex.join(['python3', f'{ab.REMOTE}/.colab/image.py', ab.IMAGE, *colab.IMAGE_FILES]))
    runtime.ssh(session, 'command -v rsync || (apt-get update -qq && apt-get install -y -qq rsync)', timeout=600)
    source = json.loads(ab.MANIFEST.read_text())['source']
    for entry in source['grids']:
        remote = f"/workspace/grid/{entry['remote_name']}"
        runtime.rsync(session, entry['grid'], f'root@{session}:{remote}')
        runtime.ssh(session, f"printf %s {shlex.quote(entry['grid_sha256'] + '  ' + remote)} | sha256sum -c -")
    chosen = json.loads((ab.HERE / 'benchmark-cells.json').read_text())
    names = ab.inputs(chosen)
    runtime.ssh(session, 'mkdir -p /workspace/data-shared && tar -x -C /workspace/data-shared',
                data=tar([(name, ab.MAIN / name) for name in names]), timeout=900)
    bench = [('lnl_check.py', ab.HERE / 'lnl_check.py')]
    bench += [(f"dead/{cell['name'].replace('/', '-')}.pkl", ab.dead_points(cell)) for cell in chosen]
    runtime.ssh(session, 'mkdir -p /workspace/bench && tar -x -C /workspace/bench', data=tar(bench), timeout=900)
    push(runtime, session, labels)
    runtime.wait(state, 'image')
    # scripts/colab.py prepare: the NVIDIA libraries and the plain IPython kernel; the bootstrap's kernel
    runtime.ssh(session, 'echo /usr/lib64-nvidia > /etc/ld.so.conf.d/zz-colab-nvidia.conf && ldconfig 2>/dev/null; '
                         '(test ! -f /etc/ipython/ipython_config.py || '
                         'mv /etc/ipython/ipython_config.py /etc/ipython/ipython_config.py.colab); '
                         f'{ab.PYTHON} -m ipykernel install --user --name ceridwen >/dev/null && '
                         f'{ab.PYTHON} -c "import json,pathlib;from jupyter_core.paths import jupyter_data_dir;'
                         "p=pathlib.Path(jupyter_data_dir())/'kernels/ceridwen/kernel.json';k=json.loads(p.read_text());"
                         "k['env']={'JAX_ENABLE_X64':'1','JAX_PLATFORMS':'cuda'};p.write_text(json.dumps(k))\"",
                timeout=300)
    print(runtime.ssh(session, f'{ab.PYTHON} -c "import jax; print(jax.__version__, jax.devices())"', timeout=300))


def run(session, plan_path, out):
    runtime = Runtime(out)
    out.mkdir(parents=True, exist_ok=True)
    plan = json.loads(plan_path.read_text())
    chosen = json.loads((ab.HERE / 'benchmark-cells.json').read_text())
    name = out.name
    request = {'plan': plan, 'cells': chosen, 'inputs': ab.inputs(chosen), 'called_at': time.time(),
               'grid_dir': '/workspace/grid'}
    runtime.ssh(session, f'mkdir -p /workspace/ab && cat > /workspace/ab/{name}.json', data=json.dumps(request).encode())
    runtime.ssh(session, 'cat > /workspace/ab/ab.py', data=(ab.HERE / 'ab.py').read_bytes())
    runtime.launch(session, f'ab-{name}', f'cd /workspace/ab && {ab.PYTHON} ab.py remote {name}.json /workspace/out/{name}')
    collect(session, plan_path, out)


def collect(session, plan_path, out):
    """Wait for a launched plan and fetch its outputs; also picks a plan up again after a lost connection."""
    runtime = Runtime(out)
    plan = json.loads(plan_path.read_text())
    name = out.name
    runtime.wait(attempt(session), f'ab-{name}')
    runtime.rsync(session, f'root@{session}:/workspace/out/{name}/', f'{out}/')
    result = json.loads((out / 'record.json').read_text())
    seconds = result['finished'] - result['entered']
    result.update(returned=time.time(), plan=plan, cost=f'{seconds / 3600 * UNITS_PER_HOUR:.2f} Colab units',
                  staged={label: json.loads((ab.STAGE / label / 'STAGED').read_text())
                          for label in {step['label'] for step in plan}})
    (out / 'timings.json').write_text(json.dumps(result, indent=1))
    ab.summary(out)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('up', 'push'):
        p = sub.add_parser(command)
        p.add_argument('session')
        p.add_argument('labels', nargs='*')
    for command in ('run', 'collect'):
        r = sub.add_parser(command)
        r.add_argument('session')
        r.add_argument('plan', type=Path)
        r.add_argument('out', type=Path)
    d = sub.add_parser('down')
    d.add_argument('session')
    args = parser.parse_args()
    if args.command == 'up':
        return up(args.session, args.labels)
    if args.command == 'push':
        return push(Runtime(ab.HERE / 'runs'), args.session, args.labels)
    if args.command == 'run':
        return run(args.session, args.plan, args.out)
    if args.command == 'collect':
        return collect(args.session, args.plan, args.out)
    Runtime(ab.HERE / 'runs').release(attempt(args.session))


if __name__ == '__main__':
    sys.exit(main())
