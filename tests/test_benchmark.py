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
    return bench.Run(args, source)


@pytest.fixture
def cloud(run, monkeypatch):
    offer = dict(id=1, host_id=42, gpu_name='RTX 5090', dph_total=.2, inet_down_cost=.001, inet_up_cost=.001,
                 verification='verified', rentable=True, reliability2=.999,
                 gpu_ram=32000, disk_space=80, cuda_max_good=13, direct_port_count=4)
    state = {'live': {}, 'created': [], 'destroyed': [], 'commands': []}
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


def test_create_is_not_retried_on_empty_response(monkeypatch):
    calls = []
    monkeypatch.setattr(bench.vast, '_vastai', lambda args, **kw: calls.append(args) or '')
    with pytest.raises(bench.vast.SweepError, match='no JSON'):
        bench.vast._vastai_json(['create', 'instance', '1'])
    assert len(calls) == 1


def test_dry_run_never_contacts_cloud_or_writes_output(tmp_path, monkeypatch):
    monkeypatch.setattr(bench, 'preflight', lambda _: {'commit': 'abc'})
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
