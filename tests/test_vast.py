from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import vast as sweep


def offer(**overrides) -> dict:
    base = {
        "id": 1,
        "gpu_name": "RTX 5080",
        "host_id": 466789,
        "dph_total": 0.18,
        "rentable": True,
        "verification": "verified",
        "reliability2": 0.995,
        "internet_down_cost_per_tb": 1.33,
        "internet_up_cost_per_tb": 1.33,
        "gpu_ram": 16303,
        "disk_space": 118.0,
        "cuda_max_good": 13.0,
        "compute_cap": 1200,
        "direct_port_count": 24,
    }
    return {**base, **overrides}


def test_vastai_json_retries_an_empty_response(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = iter(["", '{"success": true}'])
    calls = []
    monkeypatch.setattr(
        sweep,
        "_vastai",
        lambda arguments, timeout: calls.append((arguments, timeout))
        or next(responses),
    )
    monkeypatch.setattr(sweep.time, "sleep", lambda _seconds: None)

    assert sweep._vastai_json(["show", "instances"]) == {"success": True}
    assert len(calls) == 2


def test_ssh_options_offer_only_the_registered_key(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    private_key = tmp_path / "benchmark-key"
    monkeypatch.setattr(sweep, "SSH_KEY_PATH", private_key)

    options = sweep._ssh_options("22022")

    assert options[:4] == ["-p", "22022", "-i", str(private_key)]
    assert "IdentitiesOnly=yes" in options
    assert "ServerAliveInterval=30" in options


def test_upload_inputs_copies_only_requested_files_and_verifies_them(monkeypatch):
    copied, commands = [], []
    files = ['data/raw/legac_dr2/sp/example.fits', 'data/raw/hst_f814w/example.fits']
    monkeypatch.setattr(sweep, 'target_inputs', lambda targets: files if targets == ['example'] else [])
    monkeypatch.setattr(sweep, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(sweep.subprocess, 'run', lambda cmd, **kw: copied.append(cmd))
    monkeypatch.setattr(sweep, '_ssh', lambda _, cmd, **kw: commands.append(cmd))
    sweep._upload_inputs(123, lambda _: None, targets=['example'])
    assert len(copied) == 1
    assert copied[0][:3] == ['rsync', '-aR', '--partial']
    assert '--delete' not in copied[0]
    assert all(any('/./' + name == arg[-len('/./' + name):] for arg in copied[0]) for name in files)
    assert all('test -f ' + sweep.REMOTE_ROOT + '/' + name in commands[-1] for name in files)
    assert 'input-files.json' in commands[-1]


def fit_offer(**overrides) -> dict:
    base = offer(gpu_name="RTX 5060", dph_total=0.09, reliability2=0.997,
                 inet_down_cost=0.002, inet_up_cost=0.002)
    return {**base, **overrides}


def test_fit_offer_rule_has_no_hourly_cap_and_strict_bandwidth_guard():
    good = fit_offer(dph_total=1.5)
    assert sweep.fit_offer_qualifies(good)
    assert not sweep.fit_offer_qualifies({**good, "reliability2": .995})
    for field in ("inet_down_cost", "inet_up_cost"):
        assert sweep.fit_offer_qualifies({**good, field: .0099})
        assert not sweep.fit_offer_qualifies({**good, field: .010})
        assert not sweep.fit_offer_qualifies({**good, field: .011})


def test_interruptible_price_includes_disk():
    row = fit_offer(dph_total=.90, min_bid=.08, storage_total_cost=.02)
    assert sweep.fit_offer_price(row, interruptible=True) == pytest.approx(.105)


@pytest.mark.parametrize("amount", [0, -1, 1.01, float("nan"), float("inf")])
def test_experiment_cap_cannot_exceed_one_dollar(amount):
    import argparse
    with pytest.raises(argparse.ArgumentTypeError):
        sweep.experiment_cap(amount)


@pytest.mark.parametrize('blocked_by', ['host', 'hardware', 'bandwidth'])
def test_fit_fallback_after_all_filters(monkeypatch, blocked_by):
    preferred = fit_offer(host_id=10)
    if blocked_by == 'hardware':
        preferred['gpu_ram'] = 100
    if blocked_by == 'bandwidth':
        preferred['inet_down_cost'] = .01
    rows = [preferred, fit_offer(id=2, reliability2=.97, dph_total=.45),
            fit_offer(id=3, reliability2=.98, dph_total=.6),
            fit_offer(id=4, reliability2=.96, dph_total=.01),
            fit_offer(id=5, reliability2=.98, inet_up_cost=.01)]
    queries = []
    monkeypatch.setattr(sweep, 'search_offers', lambda query, **kw: queries.append(query) or rows)
    result = sweep.fit_offers(exclude_hosts={10} if blocked_by == 'host' else ())
    assert [o['id'] for o in result] == [2, 3]
    assert len(queries) == 2
    assert 'reliability>0.96' in queries[-1]


def test_fit_prefers_high_reliability_and_only_queries_once(monkeypatch):
    queries = []
    rows = [fit_offer(), fit_offer(id=2, reliability2=.97, dph_total=.01)]
    monkeypatch.setattr(sweep, 'search_offers', lambda query, **kw: queries.append(query) or rows)
    assert [o['id'] for o in sweep.fit_offers()] == [1]
    assert len(queries) == 1


def test_fit_empty_after_both_tiers(monkeypatch):
    queries = []
    monkeypatch.setattr(sweep, 'search_offers', lambda query, **kw: queries.append(query) or [])
    assert sweep.fit_offers() == []
    assert len(queries) == 2


def test_local_ssh_preflight_does_not_connect(monkeypatch):
    calls = []
    monkeypatch.setattr(sweep.subprocess, 'run', lambda args, **kw:
                        calls.append(args) or SimpleNamespace(returncode=0, stderr=''))
    sweep.check_local_ssh()
    assert calls[0][:2] == ['ssh', '-G']
    assert 'BatchMode=yes' in calls[0]


def test_local_ssh_uid_error_fails_preflight(monkeypatch):
    monkeypatch.setattr(sweep.subprocess, 'run', lambda *a, **kw:
                        SimpleNamespace(returncode=255, stderr='No user exists for uid 501'))
    with pytest.raises(sweep.LocalSSHError, match='uid 501'):
        sweep.check_local_ssh()


def test_local_ssh_uid_error_is_fatal_even_with_check_false(monkeypatch):
    monkeypatch.setattr(sweep, '_ssh_target', lambda _: ('root@test', '22'))
    monkeypatch.setattr(sweep.subprocess, 'run', lambda *a, **kw:
                        SimpleNamespace(returncode=255, stderr='No user exists for uid 501'))
    with pytest.raises(sweep.LocalSSHError, match='uid 501'):
        sweep._ssh(1, 'true', timeout=2, check=False)


def test_legacy_wait_also_stops_on_local_ssh_failure(monkeypatch):
    monkeypatch.setattr(sweep, '_ssh', lambda *a, **kw:
                        (_ for _ in ()).throw(sweep.LocalSSHError('No user exists for uid 501')))
    monkeypatch.setattr(sweep.time, 'sleep', lambda _: pytest.fail('waited on local error'))
    with pytest.raises(sweep.LocalSSHError):
        sweep._wait_for_ssh(1, lambda _: None)


def test_bootstrap_reuses_cached_grid_and_checks_digest(tmp_path, monkeypatch):
    import hashlib
    grid = tmp_path / 'amist_c3k_hr_krou_afe.h5'
    grid.write_bytes(b'cached grid')
    monkeypatch.setenv('CERIDWEN_GRID_DIR', str(tmp_path))
    monkeypatch.setattr(sweep, '_ssh_target', lambda _: ('root@test', '22'))
    copied, commands = [], []
    monkeypatch.setattr(sweep, '_rsync', lambda *a, **kw: copied.append(a))
    monkeypatch.setattr(sweep, '_ssh', lambda _, cmd, **kw:
                        commands.append(cmd) or SimpleNamespace(stdout='ready'))
    sweep._bootstrap(123, lambda _: None)
    assert copied[0][1] == str(grid)
    assert any(hashlib.sha256(b'cached grid').hexdigest() in cmd and 'sha256sum -c' in cmd for cmd in commands)
    assert 'CERIDWEN_GRID_PATH=' in commands[-1]
    assert 'bootstrap_vast_ai.sh' in commands[-1]


def test_missing_optional_cache_retains_bootstrap_fetch(tmp_path, monkeypatch):
    monkeypatch.setenv('CERIDWEN_GRID_DIR', str(tmp_path))
    commands = []
    monkeypatch.setattr(sweep, '_rsync', lambda *a, **kw: pytest.fail('missing grid transfer'))
    monkeypatch.setattr(sweep, '_ssh', lambda _, cmd, **kw:
                        commands.append(cmd) or SimpleNamespace(stdout='ready'))
    sweep._bootstrap(123, lambda _: None)
    assert len(commands) == 1
    assert 'CERIDWEN_GRID_PATH=' not in commands[0]
