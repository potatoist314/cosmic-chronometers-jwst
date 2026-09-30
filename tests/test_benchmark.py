"""Exercise the rental lifecycle without making paid API calls."""
import json
import subprocess
import time
from types import SimpleNamespace

import pytest

from scripts import benchmark as bench


@pytest.fixture
def run(tmp_path, monkeypatch):
    args = bench.parser().parse_args(['run', 'RTX 5090', '--spend-cap', '1', '--output', str(tmp_path)])
    source = {'commit': 'abc', 'submodules': {}, 'grid': '/grid.h5', 'grid_sha256': '123'}
    monkeypatch.setattr(bench.time, 'sleep', lambda _: None)
    monkeypatch.setattr(bench, 'pack', lambda grid, sha256: tmp_path / f'{sha256}.zlib')
    return bench.Run(args, source)


@pytest.fixture
def cloud(run, monkeypatch):
    offer = dict(id=1, host_id=42, gpu_name='RTX 5090', dph_total=.2, inet_down_cost=.001, inet_up_cost=.001,
                 verification='verified', rentable=True, reliability2=.999,
                 gpu_ram=32000, disk_space=80, cuda_max_good=13, direct_port_count=4)
    state = {'live': {}, 'created': [], 'destroyed': [], 'commands': [], 'sent': []}
    def create(offer, args):
        saved = json.loads(run.path.read_text())
        assert saved['attempts'][-1]['label'] == args.label
        state['created'].append(offer['id'])
        state['live'][100] = dict(id=100, host_id=42, label=args.label, actual_status='running', dph_total=.2)
        return 100
    def api(args):
        if args[:2] == ['show', 'instances']:
            return list(state['live'].values())
        assert args[:2] == ['show', 'invoices-v1']
        assert '--start-date' in args and '--end-date' in args
        return {'results': [{'source': 'instance-100', 'amount': .05},
                            {'source': 'instance-999', 'amount': 99}], 'next_token': None}
    def ssh(instance, command, **kwargs):
        state['commands'].append(command)
        if 'tail -c' in command:
            return SimpleNamespace(stdout='0\nfinished', returncode=0)
        if command.startswith('cat ') and command.endswith('timing.json'):
            return SimpleNamespace(stdout=json.dumps(dict(
                x64=True, device_kind='NVIDIA GeForce RTX 5090',
                log_likelihood={'finite': True, 'within_test_tolerance': True},
                summary=[{'particles': 500, 'free_baked_us_per_call': 10}],
            )), returncode=0)
        return SimpleNamespace(stdout='stage log', returncode=0)
    def destroy(instance, log):
        # Timing must already be local before teardown after successful measurement.
        state['destroyed'].append(instance)
        state['live'].pop(instance, None)
    monkeypatch.setattr(bench.vast, '_create_instance', create)
    monkeypatch.setattr(bench.vast, '_vastai_json', api)
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kwargs: [offer] if kwargs['rental_type'] == 'on-demand' else [])
    monkeypatch.setattr(bench.vast, '_instance_state', lambda i: state['live'].get(i, {}))
    monkeypatch.setattr(bench.vast, '_instance_exists', lambda i: i in state['live'])
    monkeypatch.setattr(bench.vast, '_attach_ssh_key', lambda i: None)
    monkeypatch.setattr(bench.vast, '_ssh', ssh)
    monkeypatch.setattr(bench.vast, '_destroy', destroy)
    monkeypatch.setattr(bench.vast, '_rsync_background', lambda *a: state['sent'].append(a) or SimpleNamespace(
        communicate=lambda timeout: ('', ''), poll=lambda: 0, returncode=0))
    monkeypatch.setattr(run, 'upload', lambda a: None)
    return offer, state


def test_complete_command_downloads_before_cleanup_and_filters_invoices(run, cloud):
    _, state = cloud
    assert run.execute() == 0
    assert state['created'] == [1]
    assert state['destroyed'] == [100]
    assert (run.root / 'timing-100.json').exists()
    assert (run.root / '100-bootstrap.log').exists()
    assert (run.root / '100-measure.log').exists()
    assert json.loads((run.root / 'charges.json').read_text()) == [{'source': 'instance-100', 'amount': .05}]
    saved = json.loads(run.path.read_text())
    assert saved['attempts'][0]['status'] == 'complete'
    assert saved['attempts'][0]['billed_usd'] == .05
    assert run.execute() == 0
    assert state['created'] == [1]  # A completed run never rents twice.


def test_failure_cleans_up_and_does_not_report_success(run, cloud, monkeypatch):
    _, state = cloud
    monkeypatch.setattr(run, 'measure', lambda _: (_ for _ in ()).throw(RuntimeError('bad likelihood')))
    assert run.execute() == 1
    assert state['destroyed'] == [100]
    assert run.data['attempts'][0]['status'] == 'failed'


def test_budget_stops_before_renting(run, cloud):
    _, state = cloud
    run.args.spend_cap = .01
    with pytest.raises(bench.vast.SweepError, match='budget'):
        run.execute()
    assert state['created'] == []


def test_cap_reached_during_stage_destroys_instance(run, cloud, monkeypatch):
    _, state = cloud
    def uploaded(attempt):
        run.args.spend_cap = .001
    monkeypatch.setattr(run, 'upload', uploaded)
    with pytest.raises(bench.vast.SweepError, match='budget'):
        run.execute()
    assert state['destroyed'] == [100]


def test_interrupt_cleans_up_owned_instance_only(run, cloud, monkeypatch):
    _, state = cloud
    state['live'][999] = dict(id=999, host_id=900, label='other-task')
    monkeypatch.setattr(run, 'measure', lambda _: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        run.execute()
    assert state['destroyed'] == [100]
    assert 999 in state['live']


def test_cleanup_failure_blocks_another_rental(run, cloud, monkeypatch):
    monkeypatch.setattr(bench.vast, '_destroy', lambda *_: None)
    with pytest.raises(bench.vast.SweepError, match='cleanup failed'):
        run.execute()
    assert cloud[1]['created'] == [1]
    assert run.data['attempts'][0]['destroyed'] is False


def test_resume_adopts_only_durable_owned_label_without_rerenting(run, cloud):
    offer, state = cloud
    run.data['attempts'].append(dict(offer=offer, price=.2, bid=None, started=time.time(),
                                   transfer_estimate=.008, label='owned', status='renting'))
    state['live'][100] = dict(id=100, host_id=42, label='owned', actual_status='running', dph_total=.2)
    assert run.execute() == 0
    assert state['created'] == []
    assert state['destroyed'] == [100]


def test_lost_create_response_recovers_and_destroys_owned_instance(run, cloud, monkeypatch):
    create = bench.vast._create_instance
    def lost(offer, args):
        create(offer, args)
        raise bench.vast.SweepError('empty create response')
    monkeypatch.setattr(bench.vast, '_create_instance', lost)
    assert run.execute() == 1
    assert cloud[1]['destroyed'] == [100]
    assert run.data['attempts'][0]['instance_id'] == 100


def refusing(cloud, monkeypatch, refused_ids, status=410):
    """Offers 1-3 on separate hosts; Vast rejects creates for refused_ids."""
    offer, state = cloud
    offers = [{**offer, 'id': i, 'host_id': 40 + i} for i in (1, 2, 3)]
    searches = []
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kw: searches.append(kw['rental_type'])
                        or (offers if kw['rental_type'] == 'on-demand' else []))
    create = bench.vast._create_instance
    def refuse(offer, args):
        if offer['id'] in refused_ids:
            raise bench.vast.VastAPIError(f'{status} no_such_ask', status)
        return create(offer, args)
    monkeypatch.setattr(bench.vast, '_create_instance', refuse)
    return state, searches


def test_refused_create_takes_next_ranked_offer_without_using_an_attempt(run, cloud, monkeypatch):
    state, searches = refusing(cloud, monkeypatch, {1, 2})
    run.args.max_attempts = 1
    assert run.execute() == 0
    assert state['created'] == [3]
    assert state['destroyed'] == [100]
    assert [a['refused'] for a in run.data['attempts'][:2]] == [True, True]
    assert all('no_such_ask' in a['error'] for a in run.data['attempts'][:2])
    assert run.data['attempts'][2]['status'] == 'complete'
    assert len(searches) == 2  # One on-demand and one bid search; refusals reuse the ranking.
    assert len(run.data['selections']) == 1
    assert run.data['estimated_total_usd'] == pytest.approx(bench.estimated_spend(run.data['attempts'][2]))


def test_refusals_are_bounded(run, cloud, monkeypatch):
    offer, state = cloud
    offers = [{**offer, 'id': i, 'host_id': 100 + i} for i in range(2 * bench.MAX_REFUSALS)]
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kw: offers if kw['rental_type'] == 'on-demand' else [])
    monkeypatch.setattr(bench.vast, '_create_instance', lambda offer, args:
                        (_ for _ in ()).throw(bench.vast.VastAPIError('410 no_such_ask', 410)))
    assert run.execute() == 1
    assert len(run.data['attempts']) == bench.MAX_REFUSALS
    assert state['destroyed'] == []
    assert run.data['estimated_total_usd'] == 0


def test_server_error_on_create_uses_an_attempt(run, cloud, monkeypatch):
    state, _ = refusing(cloud, monkeypatch, {1, 2, 3}, status=502)
    run.args.max_attempts = 2
    assert run.execute() == 1
    assert len(run.data['attempts']) == 2
    assert not any(a['refused'] for a in run.data['attempts'])


def test_rejected_create_with_owned_label_is_destroyed_and_counted(run, cloud, monkeypatch):
    create = bench.vast._create_instance
    def rejected_after_rental(offer, args):
        create(offer, args)
        raise bench.vast.VastAPIError('410 no_such_ask', 410)
    monkeypatch.setattr(bench.vast, '_create_instance', rejected_after_rental)
    assert run.execute() == 1
    assert cloud[1]['destroyed'] == [100]
    assert run.data['attempts'][0]['instance_id'] == 100
    assert 'refused' not in run.data['attempts'][0]


def test_source_change_rejected_before_new_rental(run):
    with pytest.raises(bench.vast.SweepError, match='source differs'):
        bench.Run(run.args, {'commit': 'other'})


def test_reconnect_does_not_launch_a_second_worker_or_truncate_logs(run, cloud, monkeypatch):
    original = bench.vast._ssh
    dropped = []
    def ssh(instance, command, **kwargs):
        if 'tail -c' in command and not dropped:
            dropped.append(True)
            raise subprocess.TimeoutExpired('ssh', 40)
        return original(instance, command, **kwargs)
    monkeypatch.setattr(bench.vast, '_ssh', ssh)
    assert run.execute() == 0
    launches = [c for c in cloud[1]['commands'] if 'setsid' in c]
    assert all('flock -n 9 || exit 0' in c for c in launches)
    assert all(c.index('flock -n 9') < c.index('exec > ') for c in launches)
    assert cloud[1]['created'] == [1]


def test_stage_polls_briskly_until_the_exit_file_lands(run, monkeypatch):
    polls, sleeps = [], []
    def ssh(instance, command, **kwargs):
        if 'tail -c' in command:
            polls.append(command)
            return SimpleNamespace(stdout='running\n...', returncode=0) if len(polls) < 3 \
                else SimpleNamespace(stdout='0\ndone', returncode=0)
        return SimpleNamespace(stdout='full stage log', returncode=0)
    monkeypatch.setattr(bench.vast, '_ssh', ssh)
    monkeypatch.setattr(bench.time, 'sleep', sleeps.append)
    run.stage({'instance_id': 100, 'price': .2}, 'fit-0', 'true')
    assert len(polls) == 3
    assert sleeps == [bench.POLL_SECONDS] * 2 == [5, 5]
    assert (run.root / '100-fit-0.log').read_text() == 'full stage log'


def test_create_is_not_retried_on_empty_response(monkeypatch):
    calls = []
    monkeypatch.setattr(bench.vast, '_vastai', lambda args, **kw: calls.append(args) or '')
    with pytest.raises(bench.vast.SweepError, match='no JSON'):
        bench.vast._vastai_json(['create', 'instance', '1'])
    assert len(calls) == 1


def test_dry_run_never_contacts_cloud_or_writes_output(tmp_path, monkeypatch):
    monkeypatch.setattr(bench, 'preflight', lambda *a, **kw: {'commit': 'abc'})
    monkeypatch.setattr(bench, 'git', lambda *a, **kw: 'input-files.json')
    monkeypatch.setattr(bench.vast, 'target_inputs', lambda targets: ['selected.fits'])
    monkeypatch.setattr(bench.vast, '_vastai_json', lambda *_: pytest.fail('network on dry run'))
    output = tmp_path / 'absent'
    assert bench.main(['run', 'RTX 5090', '--spend-cap', '1', '--output', str(output), '--dry-run']) == 0
    assert not output.exists()


@pytest.mark.parametrize('price', ['0', '-1', 'nan', 'inf', '1.01'])
def test_invalid_budget_rejected(price):
    with pytest.raises(SystemExit):
        bench.parser().parse_args(['run', 'RTX 5090', '--spend-cap', price])


def test_cheaper_valid_offer_wins_even_when_expensive_offer_is_first(run, cloud, monkeypatch):
    offer, _ = cloud
    expensive = {**offer, 'id': 10, 'host_id': 10, 'dph_total': .744}
    cheap = {**offer, 'id': 20, 'host_id': 20, 'dph_total': .45}
    unreliable = {**offer, 'id': 30, 'host_id': 30, 'dph_total': .10, 'reliability2': .995}
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kw:
                        [expensive, unreliable, cheap] if kw['rental_type'] == 'on-demand' else [])
    ranked = run.candidates('RTX 5090')
    assert [row[1]['id'] for row in ranked] == [20, 10]
    assert next(r for r in run.selection['offers'] if r['offer_id'] == 30)['rejected'] == 'reliability <= 99.5%'


def test_bid_competes_below_cap_and_includes_disk_cost(run, cloud, monkeypatch):
    offer, _ = cloud
    on_demand = {**offer, 'dph_total': .744, 'rental_type': 'on-demand'}
    bid = {**offer, 'id': 2, 'dph_total': .45, 'dph_base': .40,
           'min_bid': .40, 'storage_total_cost': .05, 'rental_type': 'bid'}
    calls = []
    def search(query, **kwargs):
        calls.append((query, kwargs['rental_type']))
        return [bid] if kwargs['rental_type'] == 'bid' else [on_demand]
    monkeypatch.setattr(bench.vast, 'search_offers', search)
    ranked = run.candidates('RTX 5090')
    assert ranked[0][1]['id'] == 2
    assert ranked[0][2] == pytest.approx(.455)
    assert ranked[0][3] == pytest.approx(.405)
    assert all('gpu_name=RTX_5090' in query for query, _ in calls)
    assert {kind for _, kind in calls} == {'bid', 'on-demand'}


def test_hourly_price_wins_with_bandwidth_under_guard(run, cloud, monkeypatch):
    offer, _ = cloud
    cheap_hourly = {**offer, 'id': 1, 'dph_total': .45, 'inet_down_cost': .009}
    cheap_total = {**offer, 'id': 2, 'dph_total': .50, 'inet_down_cost': .001}
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kw:
                        [cheap_hourly, cheap_total] if kw['rental_type'] == 'on-demand' else [])
    ranked = run.candidates('RTX 5090')
    assert ranked[0][1]['id'] == 1
    assert run.selection['offers'][0]['hourly_usd'] == .45
    assert run.selection['offers'][0]['expected_usd'] > run.selection['offers'][1]['expected_usd']


def test_host_record_then_cost_per_fit_sets_rank(run, cloud, monkeypatch):
    offer, _ = cloud
    offers = [{**offer, 'id': i, 'host_id': i, 'dph_total': price}
              for i, price in ((1, .30), (2, .40), (3, .50), (4, .35), (5, .45), (6, .55))]
    monkeypatch.setattr(bench.vast, 'search_offers', lambda _, **kw: offers if kw['rental_type'] == 'on-demand' else [])
    monkeypatch.setattr(bench.vast, 'host_outcomes', lambda: {1: 'poor', 2: 'good', 3: 'good', 6: 'good'})
    # Host 3 costs more per hour than host 2 but is twice as fast; host 6 has no speed, so it gets the median.
    monkeypatch.setattr(bench.vast, 'host_speeds', lambda gpu: {2: 100., 3: 200., 4: 150.})
    assert [row[1]['id'] for row in run.candidates('RTX 5090')] == [3, 6, 2, 4, 5, 1]
    assert {r['offer_id']: r['fit_usd'] for r in run.selection['offers']}[3] == pytest.approx(.50 * .5 * 150 / 200)


def test_poor_host_is_rented_when_nothing_else_qualifies(run, cloud, monkeypatch):
    offer, _ = cloud
    monkeypatch.setattr(bench.vast, 'host_outcomes', lambda: {offer['host_id']: 'poor'})
    monkeypatch.setattr(bench.vast, 'host_speeds', lambda gpu: {})
    assert [row[1]['id'] for row in run.candidates('RTX 5090')] == [offer['id']]
    assert run.selection['offers'][0]['host_record'] == 'poor'


def test_search_sets_disk_price_and_price_sort_explicitly(monkeypatch):
    calls = []
    monkeypatch.setattr(bench.vast, '_vastai_json', lambda args: calls.append(args) or [{'id': 1}])
    assert bench.vast.search_offers('gpu_name=RTX_5090', rental_type='bid') == [{'id': 1, 'rental_type': 'bid'}]
    args = calls[0]
    assert args[args.index('--type') + 1] == 'bid'
    assert args[args.index('--storage') + 1] == '40'
    assert args[args.index('--order') + 1] == 'dph'
    assert '--no-default' in args


def test_reliability_fallback_after_host_and_hardware_filters(run, cloud, monkeypatch):
    offer, _ = cloud
    queries = []
    rows = [
        {**offer, 'id': 10, 'host_id': 10, 'reliability2': .999},
        {**offer, 'id': 11, 'gpu_ram': 100, 'reliability2': .999},
        {**offer, 'id': 20, 'reliability2': .97, 'dph_total': .45},
        {**offer, 'id': 21, 'reliability2': .98, 'dph_total': .60},
        {**offer, 'id': 22, 'reliability2': .96, 'dph_total': .01},
        {**offer, 'id': 23, 'reliability2': .99, 'inet_up_cost': .01},
    ]
    monkeypatch.setattr(bench.vast, '_vastai_json', lambda _: [{'host_id': 10}])
    def search(query, **kwargs):
        queries.append(query)
        return rows if kwargs['rental_type'] == 'on-demand' else []
    monkeypatch.setattr(bench.vast, 'search_offers', search)
    assert [r[1]['id'] for r in run.candidates('RTX 5090')] == [20, 21]
    assert run.selection['min_reliability'] == .96
    assert len(queries) == 4
    assert 'reliability>0.995' in queries[0]
    assert 'reliability>0.96' in queries[2]


def test_no_fallback_when_preferred_offer_exists(run, cloud, monkeypatch):
    offer, _ = cloud
    queries = []
    def search(query, **kwargs):
        queries.append(query)
        return [offer, {**offer, 'id': 2, 'reliability2': .97, 'dph_total': .01}]
    monkeypatch.setattr(bench.vast, 'search_offers', search)
    assert all(r[1]['id'] == offer['id'] for r in run.candidates('RTX 5090'))
    assert len(queries) == 2
    assert run.selection['min_reliability'] == .995


def test_missing_target_cutout_fails_before_source_or_cloud(tmp_path, monkeypatch):
    monkeypatch.setattr(bench, 'ROOT', tmp_path)
    key = tmp_path / 'key'
    key.touch()
    key.with_suffix('.pub').touch()
    monkeypatch.setattr(bench.vast, 'SSH_KEY_PATH', key)
    monkeypatch.setattr(bench.shutil, 'which', lambda _: 'available')
    monkeypatch.setattr(bench.vast, 'check_local_ssh', lambda: None)
    monkeypatch.setattr(bench, 'git', lambda *a, **kw: pytest.fail('source work before input check'))
    with pytest.raises(bench.vast.SweepError, match='hst_f814w/target.fits'):
        bench.preflight('HEAD', targets=['target'])


def test_upload_includes_hst_cutouts_and_line_table(run, cloud, monkeypatch):
    copied = []
    monkeypatch.setattr(run, 'archive', lambda *a: None)
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(bench.vast, '_rsync', lambda port, source, dest, **kw: copied.append(source))
    attempt = {'instance_id': 100, 'price': .2}
    bench.Run.upload(run, attempt)
    assert str(bench.ROOT / 'data/raw/hst_f814w') in copied
    assert str(bench.ROOT / 'external/fsps/data/emlines_info.dat') in copied


def float_grid(path):
    import hashlib
    import struct
    # Smooth float64 values plus a tail shorter than one word.
    path.write_bytes(b''.join(struct.pack('<d', 1 + i / 997) for i in range(20000)) + b'tail5')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_packed_grid_unpacks_exactly_with_the_remote_code(tmp_path, monkeypatch):
    import sys
    grid = tmp_path / 'grid.h5'
    sha = float_grid(grid)
    monkeypatch.setattr(bench, 'PACKED', tmp_path / 'packed')
    packed = bench.pack(grid, sha)
    assert packed == tmp_path / 'packed' / f'{sha}.zlib'
    assert [p.name for p in packed.parent.iterdir()] == [packed.name]
    assert packed.stat().st_size < grid.stat().st_size / 2
    subprocess.run([sys.executable, '-c', bench.UNPACK, packed, tmp_path / 'out.h5'], check=True)
    assert (tmp_path / 'out.h5').read_bytes() == grid.read_bytes()
    monkeypatch.setattr(bench.zlib, 'compress', lambda _: pytest.fail('packed twice'))
    assert bench.pack(grid, sha) == packed


def test_pack_that_does_not_match_the_grid_sha_is_not_kept(tmp_path, monkeypatch):
    grid = tmp_path / 'grid.h5'
    float_grid(grid)
    monkeypatch.setattr(bench, 'PACKED', tmp_path / 'packed')
    with pytest.raises(bench.vast.SweepError, match='does not unpack'):
        bench.pack(grid, '0' * 64)
    assert list((tmp_path / 'packed').iterdir()) == []


def test_grids_are_packed_before_renting(run, cloud, monkeypatch):
    _, state = cloud
    packed = []
    monkeypatch.setattr(bench, 'pack', lambda grid, sha256: packed.append((grid, sha256, list(state['created']))))
    assert run.execute() == 0
    assert packed == [('/grid.h5', '123', [])]


def test_grid_is_sent_during_source_upload_then_unpacked_and_checked(run, cloud, monkeypatch):
    _, state = cloud
    order = []
    monkeypatch.setattr(run, 'archive', lambda *a: order.append(('archive', len(state['sent']))))
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(bench.vast, '_rsync', lambda *a, **kw: None)
    bench.Run.upload(run, {'instance_id': 100, 'price': .2})
    assert state['sent'] == [('22', [str(run.root / '123.zlib')], f'root@test:{bench.REMOTE}/grid/')]
    assert order[0] == ('archive', 1)
    assert state['commands'][-1] == (
        f'python3 -c {bench.shlex.quote(bench.UNPACK)} {bench.REMOTE}/grid/123.zlib {bench.REMOTE}/grid/grid.h5'
        f" && printf %s '123  {bench.REMOTE}/grid/grid.h5' | sha256sum -c -")


def test_failed_source_upload_stops_the_grid_transfer(run, cloud, monkeypatch):
    killed = []
    sending = SimpleNamespace(poll=lambda: None, kill=lambda: killed.append(True), wait=lambda: None)
    monkeypatch.setattr(bench.vast, '_rsync_background', lambda *a: sending)
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(run, 'archive', lambda *a: (_ for _ in ()).throw(subprocess.CalledProcessError(1, 'ssh')))
    with pytest.raises(subprocess.CalledProcessError):
        bench.Run.upload(run, {'instance_id': 100, 'price': .2})
    assert killed == [True]


def test_failed_grid_transfer_is_not_unpacked(run, cloud, monkeypatch):
    _, state = cloud
    monkeypatch.setattr(bench.vast, '_rsync_background', lambda *a: SimpleNamespace(
        communicate=lambda timeout: ('', 'connection reset'), poll=lambda: 12, returncode=12))
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(bench.vast, '_rsync', lambda *a, **kw: None)
    monkeypatch.setattr(run, 'archive', lambda *a: None)
    with pytest.raises(bench.vast.SweepError, match='connection reset'):
        bench.Run.upload(run, {'instance_id': 100, 'price': .2})
    assert not any('sha256sum' in command for command in state['commands'])


def test_upload_leaves_unused_submodule_source_out(run, cloud, monkeypatch):
    archives = []
    monkeypatch.setattr(run, 'archive', lambda attempt, tree, revision, paths=(): archives.append((tree, paths)))
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(bench.vast, '_rsync', lambda *a, **kw: None)
    run.data['source']['submodules'] = {'ceridwen': 'a', 'external/sedpy_jax': 'b'}
    bench.Run.upload(run, {'instance_id': 100, 'price': .2})
    assert archives[1:] == [(bench.ROOT / 'ceridwen', ('.', ':(exclude)tests')),
                            (bench.ROOT / 'external/sedpy_jax', ('.', ':(exclude)dist'))]


def test_archive_pathspec_excludes_a_directory(run, tmp_path, monkeypatch):
    import io
    import tarfile
    tree = tmp_path / 'ceridwen'
    for name in ('tests/fixture.h5', 'ceridwen/model.py', 'pyproject.toml'):
        (tree / name).parent.mkdir(parents=True, exist_ok=True)
        (tree / name).write_text(name)
    for command in (['init', '-q'], ['add', '.'], ['-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x']):
        subprocess.run(['git', '-C', str(tree), *command], check=True)
    monkeypatch.setattr(bench, 'ROOT', tmp_path)
    monkeypatch.setattr(bench.vast, '_ssh_target', lambda _: ('root@test', '22'))
    sent, original = [], subprocess.run
    monkeypatch.setattr(bench.subprocess, 'run', lambda command, **kw: sent.append(kw['input'])
                        if command[0] == 'ssh' else original(command, **kw))
    run.archive({'instance_id': 100, 'price': .2}, tree, 'HEAD', ('.', ':(exclude)tests'))
    names = tarfile.open(fileobj=io.BytesIO(sent[0])).getnames()
    assert {'ceridwen/model.py', 'pyproject.toml'} <= set(names)
    assert not any(name.startswith('tests') for name in names)


def test_local_ssh_failure_destroys_once_without_waiting_or_replacement(run, cloud, monkeypatch):
    offer, state = cloud
    monkeypatch.setattr(bench.vast, 'search_offers', lambda *a, **kw:
                        [offer, {**offer, 'id': 2, 'host_id': 43}])
    monkeypatch.setattr(bench.vast, '_ssh', lambda *a, **kw:
                        (_ for _ in ()).throw(bench.vast.LocalSSHError('No user exists for uid 501')))
    monkeypatch.setattr(bench.time, 'sleep', lambda _: pytest.fail('waited on a local SSH failure'))
    assert run.execute() == 1
    assert state['created'] == [1]
    assert state['destroyed'] == [100]
    assert run.data['attempts'][0]['retryable'] is False


def test_remote_stage_exit_does_not_rent_another_host(run, cloud, monkeypatch):
    offer, state = cloud
    monkeypatch.setattr(bench.vast, 'search_offers', lambda *a, **kw:
                        [offer, {**offer, 'id': 2, 'host_id': 43}])
    original = bench.vast._ssh
    def ssh(instance, command, **kwargs):
        if 'tail -c' in command and '/measure.' in command:
            return SimpleNamespace(stdout='1\nFileNotFoundError: missing cutout', returncode=0)
        return original(instance, command, **kwargs)
    monkeypatch.setattr(bench.vast, '_ssh', ssh)
    assert run.execute() == 1
    assert state['created'] == [1]
    assert state['destroyed'] == [100]
    assert (run.root / '100-measure.log').exists()
    assert run.data['attempts'][0]['retryable'] is False


def test_transient_ssh_error_is_reported_then_retried(run, cloud, monkeypatch, capsys):
    original = bench.vast._ssh
    calls = []
    def ssh(instance, command, **kwargs):
        if command == 'true' and not calls:
            calls.append(command)
            return SimpleNamespace(stdout='', stderr='Connection refused', returncode=255)
        return original(instance, command, **kwargs)
    monkeypatch.setattr(bench.vast, '_ssh', ssh)
    assert run.execute() == 0
    assert 'SSH not ready: Connection refused' in capsys.readouterr().out


def test_benchmark_default_image_and_inputs_are_recorded(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(bench, 'preflight', lambda *a, **kw: {'commit': 'abc'})
    monkeypatch.setattr(bench, 'git', lambda *a, **kw: 'input-files.json')
    monkeypatch.setattr(bench.vast, 'target_inputs', lambda targets: ['selected.fits'])
    bench.main(['run', 'RTX 5090', '--output', str(tmp_path), '--dry-run'])
    output = capsys.readouterr().out
    plan = json.loads(output[output.index('{'):])
    assert plan['source']['image'] == bench.vast.DEFAULT_IMAGE
    assert plan['source']['input_files'] == ['selected.fits']


def test_saved_benchmark_does_not_gain_new_defaults(tmp_path, monkeypatch, capsys):
    (tmp_path / 'manifest.json').write_text(json.dumps({'source': {'commit': 'abc'}}))
    monkeypatch.setattr(bench, 'preflight', lambda *a, **kw: {'commit': 'abc'})
    monkeypatch.setattr(bench, 'git', lambda *a, **kw: pytest.fail('changed saved setup'))
    bench.main(['run', 'RTX 5090', '--output', str(tmp_path), '--dry-run'])
    output = capsys.readouterr().out
    assert json.loads(output[output.index('{'):])['source'] == {'commit': 'abc'}
