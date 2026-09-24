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
                 inet_down_cost=0.002)
    return {**base, **overrides}


def test_fit_offer_rule_accepts_reliable_cards_under_loose_guards() -> None:
    """Liu Hao's rule (2026-09-23): 5060/5060 Ti/5070/5080/5090 above 99.5% reliable; $0.80/h and $25/TB are loose disaster guards."""
    good = fit_offer()
    assert sweep.fit_offer_qualifies(good)
    for gpu_name in ("RTX 5060 Ti", "RTX 5070", "RTX 5080", "RTX 5090"):
        assert sweep.fit_offer_qualifies({**good, "gpu_name": gpu_name})
    assert sweep.fit_offer_qualifies({**good, "dph_total": 0.79})
    assert not sweep.fit_offer_qualifies({**good, "dph_total": 0.80})
    assert not sweep.fit_offer_qualifies({**good, "reliability2": 0.995})
    assert not sweep.fit_offer_qualifies({**good, "gpu_name": "RTX 5070 Ti"})
    assert not sweep.fit_offer_qualifies({**good, "inet_down_cost": 0.025})
    assert (sweep.FIT_GPU_NAMES, sweep.FIT_MAX_DPH_USD, sweep.FIT_MIN_RELIABILITY,
            sweep.FIT_MAX_INET_COST_USD_PER_TB) == (
        ("RTX 5060", "RTX 5060 Ti", "RTX 5070", "RTX 5080", "RTX 5090"),
        0.80, 0.995, 25.0)


def test_fit_speed_factors_match_the_benchmark() -> None:
    """From results/gpu-benchmark-2026-09-23/sol/summary.json (5060 Ti baseline); 5090 is the 150k calls/s host."""
    assert sweep.FIT_SPEED_VS_5060_TI == {
        "RTX 5060": 0.9, "RTX 5060 Ti": 1.00, "RTX 5070": 1.33,
        "RTX 5080": 2.39, "RTX 5090": 4.49,
    }


def test_fit_ranking_prefers_lower_cost_per_work_over_lower_hourly() -> None:
    ti = fit_offer(id=1, gpu_name="RTX 5060 Ti", dph_total=0.10,
                   inet_down_cost=0.001)  # (0.10 + 0.006) / 1.00 = 0.106
    faster = fit_offer(id=2, gpu_name="RTX 5080", dph_total=0.20,
                       inet_down_cost=0.001)  # (0.20 + 0.006) / 2.39 = 0.0862
    assert sweep.fit_offer_cost_per_work(faster) == pytest.approx(0.206 / 2.39)
    ranked = sorted([ti, faster], key=sweep.fit_offer_cost_per_work)
    assert [entry["id"] for entry in ranked] == [2, 1]


def test_fit_total_cost_judges_interruptible_offers_on_the_bid() -> None:
    dear_on_demand = fit_offer(dph_total=0.90, min_bid=0.08)
    assert sweep.fit_offer_total_cost(dear_on_demand, interruptible=True) == pytest.approx(0.085 + 0.012)
    assert sweep.fit_offer_qualifies(dear_on_demand, interruptible=True)
    assert not sweep.fit_offer_qualifies(dear_on_demand)
