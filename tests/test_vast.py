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


def test_upload_inputs_verifies_the_complete_spectrum_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    copied = []
    monkeypatch.setattr(sweep, "_ssh_target", lambda _instance_id: ("root@test", "22"))
    monkeypatch.setattr(
        sweep,
        "_rsync",
        lambda *args, **kwargs: copied.append((args, kwargs)),
    )
    monkeypatch.setattr(
        sweep,
        "_ssh",
        lambda *_args, **_kwargs: SimpleNamespace(stdout="1988\n"),
    )

    sweep._upload_inputs(123, lambda _message: None)

    assert copied[0][1]["mirror"] is True


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
