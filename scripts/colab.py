#!/usr/bin/env python3
"""Colab transport for experiment.py: fit the pending cells on a Colab GPU runtime.

`experiment.py run CONFIG --gpu A100` uses Colab while the account has compute units, then Modal.
The `colab` command (google-colab-cli) allocates the runtime and bridges SSH to it
(`colab ssh --proxy-mode`). The runtime gets the files of the image pinned in vast.py (its
/opt/ceridwen environment, uv and Python 3.11, each layer checked by digest), the pinned source,
the selected inputs and the checked grids. It runs the unchanged Vast bootstrap and one
`experiment.py remote` per cell, as a Modal container does; each result comes back by rsync and
is validated as soon as its fit ends.
"""
from __future__ import annotations

import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

if __package__:
    from . import benchmark as engine
else:
    import benchmark as engine

vast = engine.vast
ROOT = engine.ROOT
REMOTE = engine.REMOTE  # the cell settings name their grid under REMOTE/grid
CLI = [shutil.which('colab') or str(Path.home() / '.local/bin/colab'), '--auth', 'adc']
GPUS = ('T4', 'L4', 'G4', 'H100', 'A100')  # `colab new --help`, google-colab-cli 0.7.4
ALIASES = {'A100-40GB': 'A100', 'A100-80GB': 'A100', 'A100-40G': 'A100', 'A100-80G': 'A100'}
KEY = vast.SSH_KEY_PATH
HAND_OVER = 3  # execute() stopped with cells pending: no compute units or no runtime
# Units for one more fit: an A100 fit stage took 146-177 s on 2026-11-13, and `colab usage`
# showed the units used some minutes late.
RESERVE_HOURS = 0.25
POLL_SECONDS = 10

# The pinned image's environment, without Docker: Colab runs no containers.
IMAGE_FILES = ('opt/ceridwen/', 'opt/ceridwen-requirements.txt', 'usr/local/bin/uv',
               'usr/local/bin/python3.11', 'usr/local/lib/python3.11/', 'usr/local/lib/libpython3.11')
IMAGE_PROGRAM = r'''
import concurrent.futures, hashlib, json, os, sys, tarfile, time, urllib.request
reference, prefixes = sys.argv[1], tuple(sys.argv[2:])
registry, path = reference.split('/', 1)
repository, digest = path.split('@')
kinds = ('application/vnd.oci.image.index.v1+json,application/vnd.oci.image.manifest.v1+json,'
         'application/vnd.docker.distribution.manifest.v2+json')
def get(name, offset=0):
    token = json.load(urllib.request.urlopen(f'https://{registry}/token?scope=repository:{repository}:pull',
                                             timeout=60))['token']
    headers = {'Authorization': f'Bearer {token}', 'Accept': kinds}
    if offset:
        headers['Range'] = f'bytes={offset}-'
    request = urllib.request.Request(f'https://{registry}/v2/{repository}/{name}', headers=headers)
    return urllib.request.urlopen(request, timeout=120)
def document(digest):
    data = get(f'manifests/{digest}').read()
    if 'sha256:' + hashlib.sha256(data).hexdigest() != digest:
        raise SystemExit(f'manifest digest mismatch: {digest}')
    return json.loads(data)
def download(layer):
    # Resume a dropped connection from the bytes on disk; the digest check covers the joined file.
    target = f"/tmp/layer-{layer['digest'][7:]}.tar.gz"
    for attempt in range(8):
        offset = os.path.getsize(target) if os.path.exists(target) else 0
        if offset == layer['size']:
            break
        try:
            with get(f"blobs/{layer['digest']}", offset) as response, open(target, 'ab' if offset else 'wb') as out:
                if offset and response.status != 206:
                    out.truncate(0)
                while block := response.read(1 << 20):
                    out.write(block)
        except OSError as error:
            print(f"layer {layer['digest'][7:19]}: {error}; retry {attempt + 1}", flush=True)
            time.sleep(5)
    with open(target, 'rb') as stream:
        if 'sha256:' + hashlib.file_digest(stream, 'sha256').hexdigest() != layer['digest']:
            raise SystemExit(f"layer digest mismatch: {layer['digest']}")
    return target
manifest = next(m['digest'] for m in document(digest)['manifests']
                if (m.get('platform', {}).get('os'), m.get('platform', {}).get('architecture')) == ('linux', 'amd64'))
layers = document(manifest)['layers']
with concurrent.futures.ThreadPoolExecutor(len(layers)) as pool:
    files = list(pool.map(download, layers))
links = {}
for file in files:  # in layer order: a later layer replaces an earlier one's files
    with tarfile.open(file, mode='r|gz') as archive:
        for member in archive:
            if member.name.startswith(prefixes) and '.wh.' not in member.name:
                archive.extract(member, '/', filter='tar')
            elif member.name.startswith('usr/local/bin/python') and member.issym():
                links[member.name] = member.linkname
    os.remove(file)
# The venv's python links to /usr/local/bin/python, which on Colab is Colab's own Python:
# link it to the interpreter that the image's /usr/local/bin/python names.
target = 'python'
while f'usr/local/bin/{target}' in links:
    target = links[f'usr/local/bin/{target}']
os.remove('/opt/ceridwen/bin/python')
os.symlink(f'/usr/local/bin/{target}', '/opt/ceridwen/bin/python')
print(f'image files extracted: {reference}; /opt/ceridwen/bin/python -> /usr/local/bin/{target}')
'''


def gpu_type(value):
    """Colab GPU name for a --gpu value, so one value names the same card on Colab and Modal."""
    name = '-'.join(value.upper().replace('_', ' ').split())
    name = ALIASES.get(name, name)
    if name not in GPUS:
        raise ValueError(f'{value!r} is not a Colab GPU; choose one of {", ".join(GPUS)}')
    return name


def colab(*arguments, timeout=300):
    return subprocess.run([*CLI, *arguments], capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL)


def usage():
    """(compute units left, units per hour of the account's runtimes) from `colab usage`."""
    result = colab('usage', timeout=120)
    found = dict(re.findall(r'^(Current balance|Usage rate): ([0-9.]+)', result.stdout, re.M))
    if result.returncode or len(found) < 2:
        detail = (result.stderr.strip() or result.stdout.strip() or 'no output').splitlines()[-1]
        raise vast.SweepError(f'Colab compute units unreadable: {detail}')
    return float(found['Current balance']), float(found['Usage rate'])


def preferred(gpu, offline=False):
    """'colab' while the account has compute units and the GPU type, else 'modal'. Offline: the GPU type only."""
    try:
        gpu_type(gpu)
    except ValueError:
        return 'modal'
    if offline:
        return 'colab'
    try:
        units, _ = usage()
    except (vast.SweepError, subprocess.SubprocessError, OSError) as error:
        engine.log(f'Colab not used: {error}; backend modal')
        return 'modal'
    engine.log(f'Colab compute units: {units:.2f}; backend colab')
    return 'colab' if units > 0 else 'modal'


def hand_over(output, gpu):
    """Give a Colab run's pending cells to Modal: one manifest, completed cells and Colab attempts kept."""
    path = output / 'manifest.json'
    data = json.loads(path.read_text())
    data.setdefault('colab', []).append({'gpus': data['gpus'], 'attempts': data['attempts'], 'ended': time.time()})
    data.update(backend='modal', gpus=[gpu], attempts=[])
    path.write_text(json.dumps(data, indent=2) + '\n')
    engine.log(f"Colab stopped with cells pending; {len(data['source']['experiment']) - len(data.get('completed_cells', []))} "
               f'cell(s) continue on Modal {gpu}')


class ColabRun:
    """Fit the pending cells on Colab runtimes; the manifest and results match Run and ModalRun."""

    def __init__(self, args, source):
        self.args = args
        self.root = args.output.resolve()
        self.path = self.root / 'manifest.json'
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {
            'backend': 'colab', 'source': source, 'gpus': [args.gpu], 'created': time.time(), 'attempts': []}
        for key, value in (('source', source), ('gpus', [args.gpu])):
            if self.data[key] != value:
                raise vast.SweepError(f'{key} differs from the saved run; use a new --output directory')
        self.tag = hashlib.sha256(str(self.root).encode()).hexdigest()[:6]
        self.save()

    def save(self):
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.data, indent=2) + '\n')
        temporary.replace(self.path)

    def ssh_options(self, session):
        proxy = shlex.join([*CLI, 'ssh', '--proxy-mode', '-s', session, '--identity', str(KEY)])
        return ['-i', str(KEY), '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', f'ProxyCommand={proxy}',
                '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'LogLevel=ERROR',
                '-o', 'ServerAliveInterval=30', '-o', 'ServerAliveCountMax=20',
                # One bridge per runtime: each new `colab ssh` costs an authentication.
                '-o', 'ControlMaster=auto', '-o', 'ControlPath=/tmp/colab-ssh-%C', '-o', 'ControlPersist=120']

    def ssh(self, session, command, *, timeout=120, data=None):
        result = subprocess.run(['ssh', *self.ssh_options(session), f'root@{session}', command], input=data,
                                capture_output=True, timeout=timeout)
        if result.returncode:
            detail = (result.stderr or result.stdout).decode(errors='replace').strip().splitlines()
            raise vast.SweepError('\n'.join(detail[-20:]) or f'remote command failed: {command}')
        return result.stdout.decode(errors='replace')

    def rsync(self, session, *paths, timeout=1800):
        subprocess.run(['rsync', '-a', '--partial', '-e', shlex.join(['ssh', *self.ssh_options(session)]), *paths],
                       check=True, capture_output=True, timeout=timeout)

    def launch(self, session, name, command):
        """Detach once; the stage's lock and exit files survive SSH disconnects, as in Run.stage."""
        prefix = f'{REMOTE}/.colab/{name}'
        inner = (f'exec 9>{prefix}.lock; flock -n 9 || exit 0; test ! -f {prefix}.exit || exit 0; '
                 f'exec > {prefix}.log 2>&1; ( {command} ); rc=$?; echo "$rc" > {prefix}.exit; exit "$rc"')
        self.ssh(session, f'mkdir -p {REMOTE}/.colab; test -f {prefix}.exit || '
                          f'setsid -f bash -c {shlex.quote(inner)} > /dev/null 2>&1 < /dev/null')

    def wait(self, attempt, name):
        """Poll the stage until it exits; keep its log beside the manifest."""
        session, prefix, failures, shown = attempt['session'], f'{REMOTE}/.colab/{name}', 0, time.monotonic()
        while True:
            time.sleep(POLL_SECONDS)
            try:
                # `colab ssh --proxy-mode -s NAME` creates a new runtime when NAME is gone: no log there.
                status, _, tail = self.ssh(session, (
                    f'if [ -f {prefix}.exit ]; then cat {prefix}.exit; elif [ ! -f {prefix}.log ]; then echo lost; '
                    f'elif flock -n {prefix}.lock true; then cat {prefix}.exit 2>/dev/null || echo lost; '
                    f'else echo running; fi; tail -c 200 {prefix}.log 2>/dev/null')).partition('\n')
                failures = 0
            except (vast.SweepError, subprocess.TimeoutExpired) as error:
                failures += 1
                if failures >= 6:
                    raise vast.SweepError(f'{name}: Colab runtime unreachable: {error}') from error
                continue
            if status.strip() == 'lost':
                raise vast.SweepError(f'{name}: the Colab runtime lost the stage (runtime replaced or process killed)')
            if status.strip() != 'running':
                break
            if time.monotonic() - shown > 60:
                engine.log(f"{name}: running; {tail.strip().splitlines()[-1] if tail.strip() else ''}")
                shown = time.monotonic()
        log = self.root / f"colab-{attempt['number']}-{name}.log"
        self.rsync(session, f'root@{session}:{prefix}.log', str(log))
        if status.strip() != '0':
            raise engine.StageFailed(f'{name} exited {status.strip()}; inspect {log}')

    def allocate(self, attempt):
        deadline = time.monotonic() + self.args.wait_minutes * 60
        while (result := colab('new', '-s', attempt['session'], '--gpu', self.args.gpu, timeout=600)).returncode:
            error = ' '.join((result.stderr.strip() or result.stdout.strip()).splitlines()[-2:])
            # "Service Unavailable": no free GPU of the type now; --wait-minutes waits for one, as for Vast supply.
            if 'Service Unavailable' not in error or time.monotonic() >= deadline:
                raise vast.SweepError(f'Colab allocation failed: {error}')
            engine.log(f'no free Colab {self.args.gpu}; next request in 60 s')
            time.sleep(60)
        attempt['allocated'] = time.time()
        self.save()

    def release(self, attempt):
        """Stop the runtime, then confirm that the server no longer lists it."""
        session = attempt['session']
        for _ in range(3):
            colab('stop', '-s', session)
            listed = colab('sessions')
            if listed.returncode == 0 and session not in listed.stdout:
                attempt['released'] = time.time()
                return
            time.sleep(5)
        engine.log(f'Colab session {session} may still run: check `colab sessions`, then `colab stop -s {session}`')

    def prepare(self, attempt):
        """Image files, pinned source, inputs and grids on the runtime; then the unchanged bootstrap."""
        if __package__:
            from . import experiment
        else:
            import experiment
        session, source = attempt['session'], self.data['source']
        attempt['gpu_name'] = self.ssh(session, 'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader').strip()
        engine.log(f"Colab runtime {session}: {attempt['gpu_name']}")
        self.save()
        self.ssh(session, f'mkdir -p {REMOTE}/grid {REMOTE}/.colab && cat > {REMOTE}/.colab/image.py',
                 data=IMAGE_PROGRAM.encode())
        self.launch(session, 'image', shlex.join(['python3', f'{REMOTE}/.colab/image.py', source['image'],
                                                  *IMAGE_FILES]))
        # The source, inputs and grids upload while the runtime downloads the image files.
        self.ssh(session, 'command -v rsync || (apt-get update -qq && apt-get install -y -qq rsync)', timeout=600)
        with tempfile.TemporaryDirectory() as temporary:
            for prefix, path in experiment.ModalRun.archives(self, Path(temporary)):
                destination = shlex.quote(f'{REMOTE}/{prefix}'.rstrip('/'))
                self.ssh(session, f'mkdir -p {destination} && tar -xz -C {destination}',
                         data=Path(path).read_bytes(), timeout=600)
        for entry in source['grids']:
            remote = f"{REMOTE}/grid/{entry['remote_name']}"
            self.rsync(session, entry['grid'], f'root@{session}:{remote}')
            self.ssh(session, f"printf %s {shlex.quote(entry['grid_sha256'] + '  ' + remote)} | sha256sum -c -")
        self.wait(attempt, 'image')
        grid = f"{REMOTE}/grid/{Path(source['experiment'][0]['settings']['ssp_grid']).name}"
        # Colab finds its NVIDIA driver libraries only through LD_LIBRARY_PATH, which the bootstrap unsets.
        # Colab's system IPython config makes every kernel a google.colab kernel; Modal and Vast have none.
        self.launch(session, 'bootstrap', 'echo /usr/lib64-nvidia > /etc/ld.so.conf.d/zz-colab-nvidia.conf && '
                                          'ldconfig 2>/dev/null && (test ! -f /etc/ipython/ipython_config.py || '
                                          'mv /etc/ipython/ipython_config.py /etc/ipython/ipython_config.py.colab) && '
                                          f'cd {REMOTE} && unset PYTHONPATH && '
                                          f'export CERIDWEN_GRID_DIR={REMOTE}/grid CERIDWEN_GRID_PATH={grid} && '
                                          'bash scripts/bootstrap_vast_ai.sh')
        self.wait(attempt, 'bootstrap')

    def fit(self, attempt, index, cell):
        """One cell in its own kernel with the environment of a Modal fit; results return at once."""
        if __package__:
            from . import experiment
        else:
            import experiment
        session = attempt['session']
        key = experiment.ModalRun.cache_key(self, cell)
        self.ssh(session, f'cat > {REMOTE}/.colab/config-{index}.json', data=json.dumps([cell]).encode())
        # One compile cache per cell setup at Modal's path; a later fit of the setup reads it.
        cache = f'/tmp/xla/{key}'
        command = (f'cd {REMOTE} && unset PYTHONPATH && mkdir -p {cache} && export CERIDWEN_GRID_DIR={REMOTE}/grid '
                   f"CERIDWEN_GRID_PATH={REMOTE}/grid/{Path(cell['settings']['ssp_grid']).name} "
                   f'JAX_COMPILATION_CACHE_DIR={cache} JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS=0 '
                   f'SPS_HOME={REMOTE}/external/fsps MPLBACKEND=Agg && .venv-ceridwen-gpu/bin/python '
                   f'scripts/experiment.py remote --config .colab/config-{index}.json --output .colab/results-{index}')
        record = attempt['cells'][cell['name']] = {'started': time.time()}
        self.save()
        try:
            self.launch(session, f'fit-{index}', command)
            self.wait(attempt, f'fit-{index}')
        finally:
            # Recover partial outputs too; keep a failed fit's own error.
            record['finished'] = time.time()
            error = sys.exception()
            try:
                (self.root / 'fits').mkdir(exist_ok=True)
                self.rsync(session, f'root@{session}:{REMOTE}/.colab/results-{index}/', f"{self.root / 'fits'}/")
            except (subprocess.SubprocessError, OSError) as caught:
                if error is None:
                    raise vast.SweepError(f"result retrieval failed: {cell['name']}: {caught}") from caught
                engine.log(f"partial result retrieval failed: {cell['name']}: {caught}")
        experiment.validate_local_result(self.root / 'fits' / cell['arm']
                                         / f"{cell['target_metadata']['object_id']}-{cell['target']}")
        self.data.setdefault('completed_cells', []).append(cell['name'])
        self.save()

    def execute(self):
        cells = self.data['source']['experiment']
        failed = []
        # A driver that was killed outright cannot have stopped its runtime.
        listed = colab('sessions')
        for session in set(re.findall(rf'ceridwen-{self.tag}-\d+', listed.stdout)):
            engine.log(f'stopping Colab session {session} left by an earlier driver of this run')
            colab('stop', '-s', session)
        for tries in range(self.args.max_attempts):
            pending = [(i, c) for i, c in enumerate(cells)
                       if c['name'] not in self.data.get('completed_cells', []) and c['name'] not in failed]
            if not pending:
                break
            try:
                units, _ = usage()
            except vast.SweepError as error:
                engine.log(str(error))
                return HAND_OVER
            if units <= 0:
                engine.log(f'Colab compute units: {units:.2f}; {len(pending)} cell(s) pending')
                return HAND_OVER
            number = len(self.data['attempts'])
            attempt = {'number': number, 'session': f'ceridwen-{self.tag}-{number}', 'gpu': self.args.gpu,
                       'units_before': units, 'cells': {}, 'started': time.time(), 'status': 'running'}
            self.data['attempts'].append(attempt)
            self.save()
            try:
                self.allocate(attempt)
            except vast.SweepError as error:
                attempt.update(status='failed', error=str(error))
                self.save()
                engine.log(str(error))
                # Colab answers "Service Unavailable" while it has no free GPU of the type; it often has one soon.
                if tries == self.args.max_attempts - 1:
                    return HAND_OVER
                time.sleep(30)
                continue
            try:
                self.prepare(attempt)
                for index, cell in pending:
                    units, rate = usage()
                    attempt['units_per_hour'] = rate
                    if units < rate * RESERVE_HOURS:
                        engine.log(f'Colab compute units: {units:.2f}, below one fit at {rate:.2f}/h')
                        attempt['status'] = 'units exhausted'
                        return HAND_OVER
                    engine.log(f"fitting {cell['name']}, seed {cell['seed']} ({units:.2f} units left)")
                    try:
                        self.fit(attempt, index, cell)
                    except (engine.StageFailed, subprocess.SubprocessError, OSError, ValueError) as error:
                        # A fit's own failure: the next fit still runs; this cell is not refitted here.
                        attempt['cells'][cell['name']]['error'] = f'{type(error).__name__}: {error}'
                        failed.append(cell['name'])
                        engine.log(attempt['cells'][cell['name']]['error'])
                        self.save()
                attempt['status'] = 'failed' if failed else 'complete'
            except engine.StageFailed as error:
                # Setup failed on code or inputs: another runtime cannot fix it.
                attempt.update(status='failed', error=str(error))
                engine.log(str(error))
                return 1
            except (vast.SweepError, subprocess.SubprocessError) as error:
                attempt.update(status='failed', error=f'{type(error).__name__}: {error}')
                engine.log(f'Colab attempt {number} failed: {error}')
            except KeyboardInterrupt:
                attempt['status'] = 'interrupted'
                raise
            finally:
                attempt['elapsed'] = time.time() - attempt['started']
                self.release(attempt)
                try:
                    attempt['units_after'] = usage()[0]
                except vast.SweepError as error:
                    engine.log(str(error))
                self.save()
        missing = [c['name'] for c in cells if c['name'] not in self.data.get('completed_cells', [])]
        engine.log(f"Colab: {len(cells) - len(missing)} of {len(cells)} cell(s) complete; pending: {missing or 'none'}")
        return 1 if missing else 0

