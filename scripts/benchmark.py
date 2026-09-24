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
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

if __package__:
    from . import vast
else:
    import vast

ROOT = vast.PROJECT_ROOT
NOTEBOOK = 'notebooks/ceridwen_integrated_photometry_spectra.ipynb'
SUBMODULES = ('ceridwen', 'external/sedpy_jax')
INPUT_DIRS = ('legac_dr2', 'cosmos2015', 'cosmos2020', 'cosmos2025')
REMOTE = vast.REMOTE_ROOT
POLL_SECONDS = 15


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


def preflight(revision):
    """Resolve committed source and check local inputs before renting."""
    for command in ('git', 'ssh', 'rsync', 'vastai'):
        if not shutil.which(command):
            raise vast.SweepError(f'missing command: {command}')
    for path in (vast.SSH_KEY_PATH, vast.SSH_KEY_PATH.with_suffix('.pub')):
        if not path.is_file():
            raise vast.SweepError(f'missing SSH key file: {path}')
    commit = git('rev-parse', f'{revision}^{{commit}}')
    modules = {tree: git('ls-tree', commit, tree).split()[2] for tree in SUBMODULES}
    for tree, sha in modules.items():
        git('cat-file', '-e', f'{sha}^{{commit}}', tree=ROOT / tree)
    document = json.loads(git('show', f'{commit}:{NOTEBOOK}'))
    settings = literal(next(''.join(c['source']) for c in document['cells']
                            if 'SETTINGS = {' in ''.join(c['source'])), 'SETTINGS')
    registry = literal(git('show', f"{modules['ceridwen']}:ceridwen/ssps/grid_fetch.py",
                           tree=ROOT / 'ceridwen'), 'REGISTRY')
    grid_name = settings['ssp_grid']
    grid = Path(os.environ.get('CERIDWEN_GRID_DIR', Path.home() / '.ceridwen/grids')) / f'{grid_name}.h5'
    if not grid.is_file():
        raise vast.SweepError(f'grid cache missing: {grid}; fetch_grid({grid_name!r}) before renting')
    with grid.open('rb') as stream:
        checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
    if checksum != registry[grid_name]['sha256']:
        raise vast.SweepError(f'grid checksum mismatch: {grid}')
    for directory in INPUT_DIRS:
        if not (ROOT / 'data/raw' / directory).is_dir():
            raise vast.SweepError(f'missing input directory: data/raw/{directory}')
    spectra = list((ROOT / 'data/raw/legac_dr2/sp').glob('legac_M*_v2.0.fits'))
    if len(spectra) != vast.EXPECTED_SPECTRUM_FILES:
        raise vast.SweepError(f'expected {vast.EXPECTED_SPECTRUM_FILES} local spectra, found {len(spectra)}')
    # Compile the pinned worker, not an unrelated dirty working copy.
    for name in ('benchmark_baked_runtime.py', 'benchmark_ceridwen_vast.py'):
        compile(git('show', f'{commit}:scripts/{name}'), name, 'exec')
    return {'commit': commit, 'submodules': modules, 'grid': str(grid), 'grid_sha256': checksum}


def offer_terms(offer, max_hourly):
    if (offer.get('verification') != 'verified' or not offer.get('rentable')
            or float(offer.get('reliability2') or 0) <= .995
            or float(offer.get('gpu_ram') or 0) < 8000
            or float(offer.get('disk_space') or 0) < vast.DEFAULT_DISK_GB
            or float(offer.get('cuda_max_good') or 0) < 12.6
            or int(offer.get('direct_port_count') or 0) < 2
            or float(offer.get('inet_down_cost', math.inf)) >= .025):
        return None
    price = float(offer.get('dph_total') or math.inf)
    if price <= max_hourly:
        return price, None
    bid = float(offer.get('min_bid') or math.inf) + .005
    return (bid, bid) if bid <= max_hourly else None


def estimated_spend(attempt):
    elapsed = max(0, time.time() - attempt['started']) if not attempt.get('destroyed') else attempt['elapsed']
    # Use a conservative rental estimate while billing is incomplete.
    return max(float(attempt.get('billed_usd', 0)),
               attempt['price'] * elapsed / 3600 + attempt['transfer_estimate'])


class Run:
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
        result = []
        for offer in vast.search_offers('verified=true reliability>0.995'):
            if offer['gpu_name'] != gpu or offer['host_id'] in hosts or offer['id'] in ids:
                continue
            terms = offer_terms(offer, self.args.max_hourly)
            if terms:
                price, bid = terms
                expected = price * .5 + 8 * float(offer['inet_down_cost'])
                result.append((expected, offer, price, bid))
        return sorted(result, key=lambda row: row[0])

    def wait_ready(self, attempt):
        last_message, last_progress, cheaper_checks = None, time.monotonic(), 0
        while True:
            self.budget(reserve=attempt['price'] * .25)
            state = vast._instance_state(attempt['instance_id'])
            if not state or state.get('actual_status') in ('offline', 'exited'):
                raise vast.SweepError('instance unavailable')
            attempt['price'] = float(state.get('dph_total') or attempt['price'])
            if attempt['price'] > self.args.max_hourly:
                raise vast.SweepError('actual hourly price exceeds --max-hourly')
            message = (state.get('actual_status'), state.get('status_msg'))
            if message != last_message:
                log(f"instance {attempt['instance_id']}: {message}")
                last_message, last_progress = message, time.monotonic()
            if state.get('actual_status') == 'running':
                vast._attach_ssh_key(attempt['instance_id'])
                try:
                    if vast._ssh(attempt['instance_id'], 'true', timeout=self.timeout(attempt, 30), check=False).returncode == 0:
                        return
                except (vast.SweepError, subprocess.TimeoutExpired):
                    pass
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

    def upload(self, attempt):
        instance = attempt['instance_id']
        source = self.data['source']
        self.archive(attempt, ROOT, source['commit'], ('scripts', NOTEBOOK))
        for tree, revision in source['submodules'].items():
            self.archive(attempt, ROOT / tree, revision)
        target, port = vast._ssh_target(instance)
        vast._ssh(instance, f'mkdir -p {REMOTE}/data/raw {REMOTE}/grid; command -v rsync || (apt-get update -qq && apt-get install -y -qq rsync)', timeout=self.timeout(attempt))
        for directory in INPUT_DIRS:
            vast._rsync(port, str(ROOT / 'data/raw' / directory), f'{target}:{REMOTE}/data/raw/', timeout=self.timeout(attempt, 600))
        grid = Path(source['grid'])
        vast._rsync(port, str(grid), f'{target}:{REMOTE}/grid/', timeout=self.timeout(attempt, 600))
        check = f"{source['grid_sha256']}  {REMOTE}/grid/{grid.name}"
        vast._ssh(instance, f'printf %s {shlex.quote(check)} | sha256sum -c -', timeout=self.timeout(attempt))

    def stage(self, attempt, name, command):
        """Detach once; stage locks and exit files survive SSH disconnects."""
        directory = f'{REMOTE}/.benchmark/{attempt["instance_id"]}'
        prefix = f'{directory}/{name}'
        # flock prevents a reconnect from starting a second bootstrap or worker.
        inner = (f'exec 9>{prefix}.lock; flock -n 9 || exit 0; '
                 f'test ! -f {prefix}.exit || exit 0; exec > {prefix}.log 2>&1; '
                 f'( {command} ); rc=$?; echo "$rc" > {prefix}.exit; exit "$rc"')
        launch = (f'mkdir -p {directory}; if test ! -f {prefix}.exit; then '
                  f'setsid -f bash -c {shlex.quote(inner)} '
                  f'> /dev/null 2>&1 < /dev/null; fi')
        while True:
            self.budget(reserve=attempt['price'] / 120)
            try:
                vast._ssh(attempt['instance_id'], launch, timeout=self.timeout(attempt, 40))
                reply = vast._ssh(attempt['instance_id'],
                                  f'if test -f {prefix}.exit; then cat {prefix}.exit; else echo running; fi; tail -c 300 {prefix}.log',
                                  timeout=self.timeout(attempt, 40)).stdout
                status, _, tail = reply.partition('\n')
                log(f'{name}: {status}; {tail.strip()}')
                if status != 'running':
                    # Always preserve the complete stage log, including failed setup.
                    contents = vast._ssh(attempt['instance_id'], f'cat {prefix}.log', timeout=self.timeout(attempt)).stdout
                    (self.root / f'{attempt["instance_id"]}-{name}.log').write_text(contents)
                    if status != '0':
                        raise RuntimeError(f'{name} exited {status}')
                    return
            except (vast.SweepError, subprocess.TimeoutExpired) as error:
                log(f'{name}: {error}; reconnecting to the same instance')
                self.wait_ready(attempt)
            time.sleep(POLL_SECONDS)

    def measure(self, attempt):
        instance = attempt['instance_id']
        self.wait_ready(attempt)
        if not attempt.get('uploaded'):
            log('uploading pinned source, inputs and cached grid')
            # Partial rsync and tar extraction are repeatable after a disconnect.
            for retry in range(2):
                try:
                    self.upload(attempt)
                    break
                except (vast.SweepError, subprocess.SubprocessError):
                    if retry:
                        raise
                    self.wait_ready(attempt)
            attempt['uploaded'] = True
            self.save()
        environment = f'cd {REMOTE} && export CERIDWEN_GRID_DIR={REMOTE}/grid && '
        self.stage(attempt, 'bootstrap', environment + 'bash scripts/bootstrap_vast_ai.sh')
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
                               'transfer_estimate': 8 * float(offer['inet_down_cost']), 'status': 'renting'}
        if existing is None:
            self.data['attempts'].append(attempt)
            self.save()  # Failed offers are recorded before the create request.
        try:
            if not attempt.get('instance_id'):
                label = f"ceridwen-run-{hashlib.sha256(str(self.root).encode()).hexdigest()[:12]}-{len(self.data['attempts'])}"
                attempt['label'] = label
                self.save()
                args = argparse.Namespace(image=vast.DEFAULT_IMAGE, disk=vast.DEFAULT_DISK_GB, bid=bid, label=label)
                attempt['instance_id'] = vast._create_instance(offer, args)
                self.save()  # Ownership is durable before setup begins.
            self.measure(attempt)
        except (Exception, KeyboardInterrupt) as error:
            attempt.update(status='failed', error=f'{type(error).__name__}: {error}')
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
                vast._destroy(attempt['instance_id'], log)
                attempt['destroyed'] = not vast._instance_exists(attempt['instance_id'])
            else:
                attempt['destroyed'] = True
                attempt['transfer_estimate'] = 0
            attempt['elapsed'] = time.time() - attempt['started'] if attempt.get('instance_id') else 0
            self.save()
            try:
                self.invoices()
            except (vast.SweepError, subprocess.SubprocessError) as error:
                log(f'invoices pending: {error}; conservative estimate retained')
            self.save()
            if not attempt['destroyed']:
                raise vast.SweepError(f"cleanup failed for owned instance {attempt['instance_id']}; repeat this command before renting again")

    def execute(self):
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
                else:
                    attempt.update(destroyed=True, elapsed=time.time() - attempt['started'], status='failed')
                    self.save()
        count = 0
        deadline = time.monotonic() + self.args.wait_minutes * 60
        for gpu in self.args.gpus:
            while sum(a['status'] == 'complete' and a['offer']['gpu_name'] == gpu for a in self.data['attempts']) < self.args.hosts:
                if count >= self.args.max_attempts:
                    return 1
                self.budget()
                candidates = self.candidates(gpu)
                if not candidates:
                    if time.monotonic() >= deadline:
                        log(f'no fresh qualifying {gpu} offer; repeat with the same --output to continue')
                        return 1
                    log(f'waiting for {gpu} supply')
                    time.sleep(30)
                    continue
                cost, offer, price, bid = candidates[0]
                self.budget(reserve=cost)
                log(f"renting {gpu}, host {offer['host_id']}, ${price:.3f}/h; estimate ${cost:.3f}")
                self.attempt(offer, price, bid)
                count += 1
        return 0


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return number


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest='command', required=True)
    run = sub.add_parser('run', help='preflight, rent, measure, download and destroy')
    run.add_argument('gpus', nargs='+', help='Vast GPU names, e.g. "RTX 5090"')
    run.add_argument('--spend-cap', type=positive, required=True, help='total USD for this output directory, including retries')
    run.add_argument('--max-hourly', type=positive, default=.80)
    run.add_argument('--hosts', type=int, default=1, help='successful hosts per GPU')
    run.add_argument('--max-attempts', type=int, default=3, help='new rentals per invocation')
    run.add_argument('--wait-minutes', type=float, default=0)
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
    source = preflight(args.revision)
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
