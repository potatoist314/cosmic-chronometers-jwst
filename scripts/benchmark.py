#!/usr/bin/env python3
"""Run a reproducible Ceridwen likelihood benchmark on Vast.ai.

python3 scripts/benchmark.py run 'RTX 5090' --spend-cap 1
Repeat with --output <run-directory> to resume the same task and budget.
"""
from __future__ import annotations

import argparse
import ast
import fcntl
import hashlib
import json
import math
import os
import shlex
import shutil
import signal
import statistics
import subprocess
import sys
import time
import zlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

if __package__:
    from . import vast
else:
    import vast

ROOT = vast.PROJECT_ROOT
NOTEBOOK = 'notebooks/ceridwen_integrated_photometry_spectra.ipynb'
SUBMODULES = ('ceridwen', 'external/sedpy_jax')
# Not in the installed wheels, so not uploaded: ceridwen test fixtures (64 MB
# compressed) and old sedpy_jax build outputs (4 MB).
UNUSED_SOURCE = {'ceridwen': 'tests', 'external/sedpy_jax': 'dist'}
# Grids are float64 arrays. Sent as eight byte planes, the 612 MB grid compresses
# to 77% with zlib (91% without the planes). The image has python3 but no zstd.
PACKED = Path.home() / '.ceridwen' / 'packed'
# The packed grid travels as this many byte ranges, one rsync each: from this Mac
# four SSH streams carry 1.6-2x the bytes per second of one.
GRID_STREAMS = 4
UNPACK = """import sys, zlib
planes = zlib.decompress(b''.join(open(part, 'rb').read() for part in sys.argv[1:-1]))
whole = len(planes) - len(planes) % 8
data = bytearray(planes)
for k in range(8):
    data[k:whole:8] = planes[k * whole // 8:(k + 1) * whole // 8]
open(sys.argv[-1], 'wb').write(data)
"""
INPUT_DIRS = ('legac_dr2', 'cosmos2015', 'cosmos2020', 'cosmos2025', 'hst_f814w')
INPUT_FILES = ('external/fsps/data/emlines_info.dat',)
REMOTE = vast.REMOTE_ROOT
# Created once every uploaded grid passes its sha256 check; an early bootstrap waits for it.
GRID_CHECKED = f'{REMOTE}/grid/.checked'
# Stage-end detection lags by up to one interval on a billing instance, so poll
# briskly; each poll is one cheap SSH round trip now that the target is cached.
POLL_SECONDS = 5
# Refused creates rent nothing and cost nothing, so they do not use --max-attempts.
MAX_REFUSALS = 20


def log(message):
    print(f'{datetime.now(UTC):%H:%M:%S} {message}', flush=True)


def git(*args, tree=ROOT):
    return subprocess.check_output(['git', '-C', str(tree), *args], text=True).strip()


def literal(source, name):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return ast.literal_eval(node.value)
        if isinstance(node, ast.AnnAssign) and getattr(node.target, 'id', None) == name:
            return ast.literal_eval(node.value)
    raise vast.SweepError(f'{name} is missing from the pinned source')


def check_target_inputs(targets):
    for target in targets:
        path = ROOT / 'data/raw/hst_f814w' / f'{target}.fits'
        if not path.is_file():
            raise vast.SweepError(f'missing target input: {path}')
    for name in INPUT_FILES:
        if not (ROOT / name).is_file():
            raise vast.SweepError(f'missing notebook input: {name}')


class StageFailed(RuntimeError):
    """A completed remote stage failed; inspect its log before renting again."""


def preflight(revision, *, grid_name=None, targets=(), workers=('benchmark_baked_runtime.py', 'benchmark_ceridwen_vast.py')):
    """Resolve committed source and check local inputs before renting."""
    for command in ('git', 'ssh', 'rsync', 'vastai'):
        if not shutil.which(command):
            raise vast.SweepError(f'missing command: {command}')
    for path in (vast.SSH_KEY_PATH, vast.SSH_KEY_PATH.with_suffix('.pub')):
        if not path.is_file():
            raise vast.SweepError(f'missing SSH key file: {path}')
    vast.check_local_ssh()
    check_target_inputs(targets)
    commit = git('rev-parse', f'{revision}^{{commit}}')
    modules = {tree: git('ls-tree', commit, tree).split()[2] for tree in SUBMODULES}
    for tree, sha in modules.items():
        git('cat-file', '-e', f'{sha}^{{commit}}', tree=ROOT / tree)
    document = json.loads(git('show', f'{commit}:{NOTEBOOK}'))
    settings = literal(next(''.join(c['source']) for c in document['cells']
                            if 'SETTINGS = {' in ''.join(c['source'])), 'SETTINGS')
    registry = literal(git('show', f"{modules['ceridwen']}:ceridwen/ssps/grid_fetch.py",
                           tree=ROOT / 'ceridwen'), 'REGISTRY')
    grid_name = grid_name or settings['ssp_grid']
    grid = (Path(os.environ.get('CERIDWEN_GRID_DIR', Path.home() / '.ceridwen/grids')) / f'{grid_name}.h5'
            if grid_name in registry else Path(grid_name).expanduser().resolve())
    if not grid.is_file():
        raise vast.SweepError(f'grid cache missing: {grid}; fetch_grid({grid_name!r}) before renting')
    with grid.open('rb') as stream:
        checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
    if grid_name in registry and checksum != registry[grid_name]['sha256']:
        raise vast.SweepError(f'grid checksum mismatch: {grid}')
    for directory in INPUT_DIRS:
        if not (ROOT / 'data/raw' / directory).is_dir():
            raise vast.SweepError(f'missing input directory: data/raw/{directory}')
    spectra = list((ROOT / 'data/raw/legac_dr2/sp').glob('legac_M*_v2.0.fits'))
    if len(spectra) != vast.EXPECTED_SPECTRUM_FILES:
        raise vast.SweepError(f'expected {vast.EXPECTED_SPECTRUM_FILES} local spectra, found {len(spectra)}')
    # Compile the pinned worker, not an unrelated dirty working copy.
    for name in workers:
        compile(git('show', f'{commit}:scripts/{name}'), name, 'exec')
    return {'commit': commit, 'submodules': modules, 'grid': str(grid), 'grid_sha256': checksum}


def planes(data):
    """Byte k of every 8-byte word, for k = 0..7, then the remainder."""
    whole = len(data) - len(data) % 8
    return b''.join([*(data[k:whole:8] for k in range(8)), data[whole:]])


def pack(grid, sha256):
    """Return the cached packed grid's GRID_STREAMS parts; new parts must unpack to the grid's sha256."""
    parts = [PACKED / f'{sha256}.zlib.{k}' for k in range(GRID_STREAMS)]
    if not all(part.exists() for part in parts):
        PACKED.mkdir(parents=True, exist_ok=True)
        partials = [PACKED / f'{sha256}.{os.getpid()}.partial{k}' for k in range(GRID_STREAMS)]
        restored = PACKED / f'{sha256}.{os.getpid()}.h5'
        try:
            packed = zlib.compress(planes(Path(grid).read_bytes()))
            for k, partial in enumerate(partials):
                partial.write_bytes(packed[k * len(packed) // GRID_STREAMS:(k + 1) * len(packed) // GRID_STREAMS])
            subprocess.run([sys.executable, '-c', UNPACK, *partials, restored], check=True)
            with restored.open('rb') as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != sha256:
                    raise vast.SweepError(f'packed {grid} does not unpack to sha256 {sha256}')
            for partial, part in zip(partials, parts):
                partial.replace(part)
        finally:
            restored.unlink(missing_ok=True)
            for partial in partials:
                partial.unlink(missing_ok=True)
    return parts


def offer_rejection(offer, min_reliability=vast.FIT_MIN_RELIABILITY):
    checks = (
        (offer.get('verification') != 'verified', 'unverified'),
        (not offer.get('rentable'), 'unavailable'),
        (float(offer.get('reliability2') or 0) <= min_reliability, f'reliability <= {min_reliability * 100:g}%'),
        (float(offer.get('gpu_ram') or 0) < 8000, 'GPU RAM < 8000 MiB'),
        (float(offer.get('disk_space') or 0) < vast.DEFAULT_DISK_GB, 'disk < 40 GB'),
        (float(offer.get('cuda_max_good') or 0) < 12.6, 'CUDA < 12.6'),
        (int(offer.get('direct_port_count') or 0) < 2, 'direct ports < 2'),
        (not vast.bandwidth_qualifies(offer), 'bandwidth >= $10/TB or missing'),
    )
    return next((reason for rejected, reason in checks if rejected), None)


def offer_terms(offer, min_reliability=vast.FIT_MIN_RELIABILITY):
    if offer_rejection(offer, min_reliability):
        return None
    bid = None
    price = float(offer.get('dph_total') or math.inf)
    if offer.get('rental_type') == 'bid':
        bid = round(float(offer['min_bid']) + vast.FIT_BID_MARGIN_USD, 4)
        # The bid covers compute. The total quote also includes the requested disk.
        price = price - float(offer['dph_base']) + bid
    return price, bid


def estimated_spend(attempt):
    elapsed = max(0, time.time() - attempt['started']) if not attempt.get('destroyed') else attempt['elapsed']
    # Use a conservative rental estimate while billing is incomplete.
    return max(float(attempt.get('billed_usd', 0)),
               attempt['price'] * elapsed / 3600 + attempt['transfer_estimate'])


class Run:
    download_gb = 8
    disk_gb = vast.DEFAULT_DISK_GB

    def __init__(self, args, source):
        self.args = args
        self.root = args.output.resolve()
        self.path = self.root / 'manifest.json'
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {
            'source': source, 'gpus': args.gpus, 'hosts': args.hosts,
            'target': args.target, 'seed': args.seed, 'created': time.time(), 'attempts': [],
        }
        for key, value in (('source', source), ('gpus', args.gpus), ('hosts', args.hosts),
                           ('target', args.target), ('seed', args.seed)):
            if self.data[key] != value:
                raise vast.SweepError(f'{key} differs from the saved run; use a new --output directory')
        self.data['spend_cap'] = args.spend_cap
        self.save()

    def save(self):
        self.data['estimated_total_usd'] = sum(estimated_spend(a) for a in self.data['attempts'])
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.data, indent=2) + '\n')
        temporary.replace(self.path)

    def budget(self, reserve=0):
        spent = sum(estimated_spend(a) for a in self.data['attempts'])
        if spent + reserve >= self.args.spend_cap:
            raise vast.SweepError(f'task budget exhausted: estimate ${spent:.3f}, cap ${self.args.spend_cap:.2f}')
        return self.args.spend_cap - spent - reserve

    def timeout(self, attempt, maximum=120):
        return max(1, min(maximum, int(self.budget(reserve=attempt['price'] / 120) / attempt['price'] * 3600)))

    def candidates(self, gpu):
        hosts = {a['offer']['host_id'] for a in self.data['attempts']}
        ids = {a['offer']['id'] for a in self.data['attempts']}
        hosts.update(i['host_id'] for i in vast._vastai_json(['show', 'instances']))
        outcomes, speeds = vast.host_outcomes(), vast.host_speeds(gpu)
        # A host without a recorded speed runs at the median recorded speed of this GPU type.
        typical = statistics.median(speeds.values()) if speeds else None
        result = []
        audit = []
        for min_reliability in vast.RELIABILITY_TIERS:
            query = f'gpu_name={gpu.replace(" ", "_")} verified=true reliability>{min_reliability}'
            offers = [offer for kind in ('on-demand', 'bid')
                      for offer in vast.search_offers(query, rental_type=kind, disk=self.disk_gb)]
            for offer in offers:
                terms = offer_terms(offer, min_reliability)
                reason = offer_rejection(offer, min_reliability)
                if float(offer.get('disk_space') or 0) < self.disk_gb:
                    reason = f'disk < {self.disk_gb} GB'
                if offer['host_id'] in hosts or offer['id'] in ids:
                    reason = 'host active or already tried in this task'
                row = {'offer_id': offer['id'], 'host_id': offer['host_id'],
                       'rental_type': offer.get('rental_type', 'on-demand'),
                       'reliability': offer['reliability2'], 'rejected': reason}
                if terms and reason is None:
                    price, bid = terms
                    expected = price * .5 + self.download_gb * float(offer['inet_down_cost'])
                    speed = speeds.get(offer['host_id'])
                    row.update(hourly_usd=price, download_usd_per_gb=offer['inet_down_cost'],
                               expected_usd=expected, host_record=outcomes.get(offer['host_id'], 'unknown'),
                               calls_per_second=speed, fit_usd=price * .5 * (typical / speed if speed else 1))
                    result.append((row, (expected, offer, price, bid)))
                audit.append(row)
            if result:
                break
        # Poor hosts in scripts/vast_hosts.csv rank last, so they are rented only when nothing else qualifies.
        order = lambda row: (('good', 'unknown', 'poor', None).index(row.get('host_record')),
                             row.get('fit_usd', math.inf), row.get('hourly_usd', math.inf),
                             row.get('expected_usd', math.inf), row['offer_id'], row['rental_type'] == 'bid')
        result.sort(key=lambda pair: order(pair[0]))
        self.selection = {'gpu': gpu, 'queried_at': datetime.now(UTC).isoformat(),
                          'min_reliability': min_reliability, 'estimated_hours': .5, 'estimated_download_gb': self.download_gb,
                          'ranking': 'host record (good, unknown, poor), then USD per fit at recorded speed, then hourly USD',
                          'offers': sorted(audit, key=order)}
        return [candidate for _, candidate in result]

    def wait_ready(self, attempt):
        last_message, last_progress, cheaper_checks = None, time.monotonic(), 0
        while True:
            self.budget(reserve=attempt['price'] * .25)
            state = vast._instance_state(attempt['instance_id'])
            # Vast stops an outbid interruptible instance; it would stay in 'loading' indefinitely.
            if not state or state.get('actual_status') in ('offline', 'exited') or state.get('intended_status') == 'stopped':
                raise vast.SweepError('instance unavailable')
            attempt['price'] = float(state.get('dph_total') or attempt['price'])
            message = (state.get('actual_status'), state.get('status_msg'))
            if message != last_message:
                log(f"instance {attempt['instance_id']}: {message}")
                last_message, last_progress = message, time.monotonic()
            if state.get('actual_status') == 'running':
                vast._attach_ssh_key(attempt['instance_id'])
                try:
                    probe = vast._ssh(attempt['instance_id'], 'true', timeout=self.timeout(attempt, 30), check=False)
                    if probe.returncode == 0:
                        return
                    log(f'SSH not ready: {probe.stderr.strip()}')
                except vast.LocalSSHError:
                    raise
                except (vast.SweepError, subprocess.TimeoutExpired) as error:
                    log(f'SSH not ready: {error}')
            stalled = time.monotonic() - last_progress
            if stalled >= 240:
                fresh = self.candidates(attempt['offer']['gpu_name'])
                waiting_rate = float(state.get('storage_total_cost') or 0) if message[0] in ('created', 'loading') else attempt['price']
                remaining = waiting_rate * (1 + 1.2 * (stalled / 60 - 4)) / 60 + attempt['price'] * .5 + attempt['transfer_estimate']
                cheaper = bool(fresh and fresh[0][0] + max(.01, .1 * remaining) < remaining)
                cheaper_checks = cheaper_checks + 1 if cheaper else 0
                log(f"waiting: remaining estimate ${remaining:.3f}; replacement ${fresh[0][0]:.3f}" if fresh else 'waiting: no replacement available')
                if cheaper_checks >= 3:
                    raise vast.SweepError('replacement is consistently cheaper')
            time.sleep(POLL_SECONDS)

    def archive(self, attempt, tree, revision, paths=()):
        archive = subprocess.check_output(['git', '-C', str(tree), 'archive', '--format=tar.gz', revision, *paths])
        target, port = vast._ssh_target(attempt['instance_id'])
        destination = REMOTE if tree == ROOT else f'{REMOTE}/{tree.relative_to(ROOT)}'
        subprocess.run(['ssh', *vast._ssh_options(port), target,
                        f'mkdir -p {shlex.quote(destination)} && tar -xz -C {shlex.quote(destination)}'],
                       input=archive, capture_output=True, check=True, timeout=self.timeout(attempt, 180))

    def grids(self):
        source = self.data['source']
        return source.get('grids', [{'grid': source['grid'], 'grid_sha256': source['grid_sha256'],
                                     'remote_name': Path(source['grid']).name}])

    def upload(self, attempt, bootstrap=None):
        """Send source, inputs and grids; start the bootstrap command, if given, once the source
        and inputs are on the box, so it runs while the grid is still on its way."""
        instance = attempt['instance_id']
        source = self.data['source']
        target, port = vast._ssh_target(instance)
        vast._ssh(instance, f'mkdir -p {REMOTE}/data/raw {REMOTE}/grid; command -v rsync || (apt-get update -qq && apt-get install -y -qq rsync)', timeout=self.timeout(attempt))
        grids = [(entry, pack(entry['grid'], entry['grid_sha256'])) for entry in self.grids()]
        # The packed grids travel while the source and inputs follow one by one.
        sending = [vast._rsync_background(port, [str(part)], f'{target}:{REMOTE}/grid/')
                   for _, parts in grids for part in parts]
        try:
            self.archive(attempt, ROOT, source['commit'], ('scripts', NOTEBOOK))
            for tree, revision in source['submodules'].items():
                self.archive(attempt, ROOT / tree, revision, ('.', f':(exclude){UNUSED_SOURCE[tree]}'))
            if 'input_files' in source:
                payload = json.dumps(source['input_files'])
                vast._ssh(instance, f'printf %s {shlex.quote(payload)} > {REMOTE}/input-files.json', timeout=self.timeout(attempt))
                subprocess.run(['rsync', '-aR', '-e', shlex.join(['ssh', *vast._ssh_options(port)]),
                                *source['input_files'], f'{target}:{REMOTE}/'], cwd=ROOT,
                               check=True, capture_output=True,
                               timeout=self.timeout(attempt, 600))
            else:
                for directory in INPUT_DIRS:
                    vast._rsync(port, str(ROOT / 'data/raw' / directory), f'{target}:{REMOTE}/data/raw/', timeout=self.timeout(attempt, 600))
                for name in INPUT_FILES:
                    remote_parent = f'{REMOTE}/{Path(name).parent}'
                    vast._ssh(instance, f'mkdir -p {remote_parent}', timeout=self.timeout(attempt))
                    vast._rsync(port, str(ROOT / name), f'{target}:{remote_parent}/', timeout=self.timeout(attempt))
            if bootstrap:
                vast._ssh(instance, self.launch(attempt, 'bootstrap', bootstrap), timeout=self.timeout(attempt))
            errors = [process.communicate(timeout=self.timeout(attempt, 600))[1] for process in sending]
        finally:
            for process in sending:
                if process.poll() is None:
                    process.kill()
                    process.wait()
        for process, error in zip(sending, errors):
            if process.returncode:
                raise vast.SweepError(f'rsync failed: {error.strip()[-1000:] or "unknown"}')
        unpack = [f"python3 -c {shlex.quote(UNPACK)} {' '.join(f'{REMOTE}/grid/{part.name}' for part in parts)} "
                  f"{REMOTE}/grid/{entry['remote_name']}" for entry, parts in grids]
        checks = '\n'.join(f"{entry['grid_sha256']}  {REMOTE}/grid/{entry['remote_name']}" for entry, _ in grids)
        vast._ssh(instance, ' && '.join([*unpack, f'printf %s {shlex.quote(checks)} | sha256sum -c -', f'touch {GRID_CHECKED}']),
                  timeout=self.timeout(attempt))

    def launch(self, attempt, name, command):
        """Shell command that starts a stage once, detached; a started or finished stage is left alone."""
        directory = f'{REMOTE}/.benchmark/{attempt["instance_id"]}'
        prefix = f'{directory}/{name}'
        # flock prevents a reconnect from starting a second bootstrap or worker.
        inner = (f'exec 9>{prefix}.lock; flock -n 9 || exit 0; '
                 f'test ! -f {prefix}.exit || exit 0; exec > {prefix}.log 2>&1; '
                 f'( {command} ); rc=$?; echo "$rc" > {prefix}.exit; exit "$rc"')
        return (f'mkdir -p {directory}; if test ! -f {prefix}.exit; then '
                f'setsid -f bash -c {shlex.quote(inner)} '
                f'> /dev/null 2>&1 < /dev/null; fi')

    def stage(self, attempt, name, command):
        """Detach once; stage locks and exit files survive SSH disconnects."""
        prefix = f'{REMOTE}/.benchmark/{attempt["instance_id"]}/{name}'
        # One SSH call per poll: the exit status with the complete log, or the log tail.
        # The first poll can run before the detached stage creates its log.
        poll = (f'{self.launch(attempt, name, command)}; if test -f {prefix}.exit; then cat {prefix}.exit {prefix}.log; '
                f'else echo running; tail -c 300 {prefix}.log 2> /dev/null || true; fi')
        while True:
            self.budget(reserve=attempt['price'] / 120)
            try:
                reply = vast._ssh(attempt['instance_id'], poll, timeout=self.timeout(attempt, 40)).stdout
                status, _, contents = reply.partition('\n')
                log(f'{name}: {status}; {contents[-300:].strip()}')
                if status != 'running':
                    # Always preserve the complete stage log, including failed setup.
                    (self.root / f'{attempt["instance_id"]}-{name}.log').write_text(contents)
                    if status != '0':
                        log_path = self.root / f"{attempt['instance_id']}-{name}.log"
                        raise StageFailed(f'{name} exited {status}; inspect {log_path} before retrying')
                    return
            except vast.LocalSSHError:
                raise
            except (vast.SweepError, subprocess.TimeoutExpired) as error:
                log(f'{name}: {error}; reconnecting to the same instance')
                self.wait_ready(attempt)
            time.sleep(POLL_SECONDS)

    def prepare(self, attempt):
        self.wait_ready(attempt)
        grid = self.data['source'].get('grids', [{'remote_name': Path(self.data['source']['grid']).name}])[0]['remote_name']
        remote_grid = shlex.quote(REMOTE + '/grid/' + grid)
        environment = f'cd {REMOTE} && export CERIDWEN_GRID_DIR={REMOTE}/grid CERIDWEN_GRID_PATH={remote_grid} && '
        if not attempt.get('uploaded'):
            log('uploading pinned source, inputs and cached grid')
            # Partial rsync and tar extraction are repeatable after a disconnect.
            for retry in range(2):
                try:
                    self.upload(attempt, environment + f'CERIDWEN_GRID_READY={GRID_CHECKED} bash scripts/bootstrap_vast_ai.sh')
                    break
                except vast.LocalSSHError:
                    raise
                except (vast.SweepError, subprocess.SubprocessError):
                    if retry:
                        raise
                    self.wait_ready(attempt)
            attempt['uploaded'] = True
            self.save()
        # Polls the bootstrap that the upload started, or starts it on a resumed run.
        self.stage(attempt, 'bootstrap', environment + 'bash scripts/bootstrap_vast_ai.sh')
        return environment

    def measure(self, attempt):
        instance = attempt['instance_id']
        environment = self.prepare(attempt)
        remote_output = f'{REMOTE}/.benchmark/{instance}/timing.json'
        command = (environment + 'MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 '
                   "XLA_FLAGS='--xla_gpu_enable_command_buffer=' .venv-ceridwen-gpu/bin/python scripts/benchmark_baked_runtime.py "
                   f'--target {shlex.quote(self.args.target)} --particles 500 --draws 500 --rounds 5 --repeats 10 '
                   f'--seed {self.args.seed} --output {remote_output}')
        self.stage(attempt, 'measure', command)
        raw = json.loads(vast._ssh(instance, f'cat {remote_output}', timeout=self.timeout(attempt)).stdout)
        if (not raw['x64'] or not raw['log_likelihood']['finite']
                or not raw['log_likelihood']['within_test_tolerance']
                or attempt['offer']['gpu_name'] not in raw['device_kind']):
            raise vast.SweepError('benchmark device or numerical validation failed')
        row = next(row for row in raw['summary'] if row['particles'] == 500)
        rate = 1e6 / float(row['free_baked_us_per_call'])
        if not math.isfinite(rate) or rate <= 0:
            raise vast.SweepError('invalid benchmark throughput')
        (self.root / f'timing-{instance}.json').write_text(json.dumps(raw, indent=2) + '\n')
        attempt.update(status='complete', calls_per_second=rate)
        log(f"{attempt['offer']['gpu_name']}: {rate:,.0f} likelihood calls/s")

    def invoices(self):
        args = ['show', 'invoices-v1', '--charges', '--charge-type', 'instance',
                '--start-date', datetime.fromtimestamp(self.data['created'], UTC).date().isoformat(),
                '--end-date', (datetime.now(UTC) + timedelta(days=1)).date().isoformat(), '--limit', '100']
        rows, token = [], None
        while True:
            response = vast._vastai_json(args + (['--next-token', token] if token else []))
            rows.extend(response['results'])
            token = response.get('next_token')
            if not token:
                break
        own = {f"instance-{a['instance_id']}" for a in self.data['attempts'] if a.get('instance_id')}
        rows = [row for row in rows if row.get('source') in own]
        (self.root / 'charges.json').write_text(json.dumps(rows, indent=2) + '\n')
        for attempt in self.data['attempts']:
            matching = [r for r in rows if r.get('source') == f"instance-{attempt.get('instance_id')}"]
            if matching:
                attempt['billed_usd'] = sum(float(row['amount']) for row in matching)

    def attempt(self, offer, price, bid, existing=None):
        attempt = existing or {'offer': offer, 'price': price, 'bid': bid, 'started': time.time(),
                               'transfer_estimate': self.download_gb * float(offer['inet_down_cost']), 'status': 'renting'}
        if existing is None:
            self.data['attempts'].append(attempt)
            self.save()  # Failed offers are recorded before the create request.
        refused = False
        try:
            if not attempt.get('instance_id'):
                label = f"ceridwen-run-{hashlib.sha256(str(self.root).encode()).hexdigest()[:12]}-{len(self.data['attempts'])}"
                attempt['label'] = label
                self.save()
                args = argparse.Namespace(image=self.data['source'].get('image', vast.LEGACY_IMAGE), disk=self.disk_gb, bid=bid, label=label)
                try:
                    attempt['instance_id'] = vast._create_instance(offer, args)
                except vast.VastAPIError as error:
                    refused = error.rejected
                    raise
                self.save()  # Ownership is durable before setup begins.
            self.measure(attempt)
        except (Exception, KeyboardInterrupt) as error:
            attempt.update(status='failed', error=f'{type(error).__name__}: {error}')
            if isinstance(error, (vast.LocalSSHError, StageFailed)):
                attempt['retryable'] = False
            log(attempt['error'])
            if isinstance(error, KeyboardInterrupt):
                raise
        finally:
            if not attempt.get('instance_id') and attempt.get('label'):
                # A create response can be lost after Vast accepted the rental.
                matches = [i for i in vast._vastai_json(['show', 'instances']) if i.get('label') == attempt['label']]
                if len(matches) == 1:
                    attempt['instance_id'] = matches[0]['id']
                    self.save()
            if attempt.get('instance_id'):
                attempt['destroyed'] = vast._destroy(attempt['instance_id'], log)
            else:
                attempt['destroyed'] = True
                attempt['transfer_estimate'] = 0
                # Vast rejected the create and no instance has the label: nothing was rented.
                attempt['refused'] = refused
            attempt['elapsed'] = time.time() - attempt['started'] if attempt.get('instance_id') else 0
            self.save()
            if not attempt.get('refused'):
                try:
                    self.invoices()
                except (vast.SweepError, subprocess.SubprocessError) as error:
                    log(f'invoices pending: {error}; conservative estimate retained')
                self.save()
            if not attempt['destroyed']:
                raise vast.SweepError(f"cleanup failed for owned instance {attempt['instance_id']}; repeat this command before renting again")

    def execute(self):
        # Pack new grids before renting: 20-30 s for 612 MB, once per grid.
        for entry in self.grids():
            pack(entry['grid'], entry['grid_sha256'])
        for attempt in self.data['attempts']:
            if not attempt.get('destroyed'):
                if not attempt.get('instance_id') and attempt.get('label'):
                    matches = [i for i in vast._vastai_json(['show', 'instances'])
                               if i.get('label') == attempt['label']]
                    if len(matches) > 1:
                        raise vast.SweepError(f"multiple instances have owned label {attempt['label']}; resolve before resuming")
                    if matches:
                        attempt['instance_id'] = matches[0]['id']
                        self.save()
                if attempt.get('instance_id') and vast._instance_exists(attempt['instance_id']):
                    self.attempt(attempt['offer'], attempt['price'], attempt['bid'], existing=attempt)
                    if attempt.get('retryable') is False:
                        return 1
                else:
                    attempt.update(destroyed=True, elapsed=time.time() - attempt['started'], status='failed')
                    self.save()
        count = refusals = 0
        deadline = time.monotonic() + self.args.wait_minutes * 60
        for gpu in self.args.gpus:
            candidates = []
            while sum(a['status'] == 'complete' and a['offer']['gpu_name'] == gpu for a in self.data['attempts']) < self.args.hosts:
                if count >= self.args.max_attempts:
                    return 1
                self.budget()
                tried = {a['offer']['host_id'] for a in self.data['attempts']}
                candidates = [c for c in candidates if c[1]['host_id'] not in tried]
                if not candidates:
                    candidates = self.candidates(gpu)
                    if not candidates:
                        if time.monotonic() >= deadline:
                            log(f'no fresh qualifying {gpu} offer; repeat with the same --output to continue')
                            return 1
                        log(f'waiting for {gpu} supply')
                        time.sleep(30)
                        continue
                    self.data.setdefault('selections', []).append(self.selection)
                    log(f'ranking: host record, then USD per fit; estimates use 0.5 hours plus {self.download_gb:g} GB download; ' + '; '.join(
                        f"{r['offer_id']} {r['host_record']} {r['rental_type']} ${r['hourly_usd']:.3f}/h, ${r['fit_usd']:.3f}/fit, ${r['expected_usd']:.3f} total"
                        for r in self.selection['offers'] if r['rejected'] is None)[:600])
                cost, offer, price, bid = candidates.pop(0)
                self.budget(reserve=cost)
                self.save()
                log(f"renting {gpu}, host {offer['host_id']}, ${price:.3f}/h; estimate ${cost:.3f}")
                self.attempt(offer, price, bid)
                if self.data['attempts'][-1].get('retryable') is False:
                    return 1
                if self.data['attempts'][-1].get('refused'):
                    # Nothing was rented: try the next offer of the same ranking at once.
                    refusals += 1
                    if refusals >= MAX_REFUSALS:
                        log(f'{refusals} rentals refused; repeat with the same --output to continue')
                        return 1
                    continue
                count += 1
                candidates = []
        return 0


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest='command', required=True)
    run = sub.add_parser('run', help='preflight, rent, measure, download and destroy')
    run.add_argument('gpus', nargs='+', help='Vast GPU names, e.g. "RTX 5090"')
    run.add_argument('--spend-cap', type=vast.experiment_cap, default=1.0, help='total USD including retries; maximum and default: 1')
    run.add_argument('--hosts', type=int, default=1, help='successful hosts per GPU')
    run.add_argument('--max-attempts', type=int, default=3, help='new rentals per invocation')
    run.add_argument('--wait-minutes', type=float, default=0)
    run.add_argument('--image', help='override the default compact image; recorded in the manifest')
    run.add_argument('--revision', default='HEAD', help='committed project revision; defaults to saved revision on resume')
    run.add_argument('--output', type=Path, help='reuse this directory to resume')
    run.add_argument('--target', default='M1_210210')
    run.add_argument('--seed', type=int, default=20260921)
    run.add_argument('--dry-run', action='store_true', help='check local inputs and print the plan; no network or rental')
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    if args.hosts < 1 or args.max_attempts < 1 or not math.isfinite(args.wait_minutes) or args.wait_minutes < 0:
        raise vast.SweepError('hosts and attempts must be positive; wait must be finite and nonnegative')
    args.output = args.output or ROOT / 'benchmarks/ceridwen/runs' / datetime.now(UTC).strftime('vast-%Y%m%dT%H%M%S%f')
    saved = args.output / 'manifest.json'
    if saved.exists() and args.revision == 'HEAD':
        args.revision = json.loads(saved.read_text())['source']['commit']
    source = preflight(args.revision, targets=[args.target])
    if saved.exists():
        previous = json.loads(saved.read_text())['source']
        for key in ('image', 'input_files'):
            if key in previous:
                source[key] = previous[key]
    else:
        bootstrap = git('show', f"{source['commit']}:scripts/bootstrap_vast_ai.sh")
        if 'input-files.json' in bootstrap:
            source['input_files'] = vast.target_inputs([args.target])
            source['image'] = vast.DEFAULT_IMAGE
    if args.image:
        source['image'] = args.image
    log(f"committed source {source['commit'][:12]}; output {args.output}")
    if args.dry_run:
        print(json.dumps({'source': source, 'gpus': args.gpus, 'spend_cap': args.spend_cap}, indent=2))
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
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
    except (vast.SweepError, subprocess.SubprocessError, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(2)
