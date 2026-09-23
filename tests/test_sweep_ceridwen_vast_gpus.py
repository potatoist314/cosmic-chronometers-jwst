from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import sweep_ceridwen_vast_gpus as sweep


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


def test_reference_fingerprint_matches_published_runs() -> None:
    assert sweep.DEFAULT_IMAGE == "vastai/base-image:cuda-12.6.3-auto"
    assert sweep.REFERENCE_FINGERPRINT == (
        "26b63c693d339d9093e68b311df48719ee5697555522b13bf8e85dc0521735cc"
    )


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


def test_run_benchmark_reads_the_reported_result_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result_name = "ceridwen_vast_test_complete_2026-08-28"
    responses = iter(
        [
            SimpleNamespace(stdout=f"setup complete\nsaved: results/{result_name}\n"),
            SimpleNamespace(stdout=json.dumps({"timings": {"timed_steps": 5}})),
        ]
    )
    commands = []

    def fake_ssh(instance_id, command, **_kwargs):
        commands.append((instance_id, command))
        return next(responses)

    monkeypatch.setattr(sweep, "_ssh", fake_ssh)

    record = sweep._run_benchmark(
        123,
        {"dph_total": 0.1, "host_id": 456},
        lambda _message: None,
    )

    assert record["result_directory"] == result_name
    assert all("ls -1" not in command for _, command in commands)


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
    assert sweep.BENCHMARK_SCRIPT_SHA256 == (
        "6d8cf1bb1e78ce6a721618655443edcd7832bf286d0b9227f85553ba0463afcb"
    )


def test_constraints_accept_a_conforming_offer() -> None:
    assert sweep.offer_satisfies_constraints(offer())


@pytest.mark.parametrize(
    "override",
    [
        {"internet_down_cost_per_tb": 5.01},
        {"internet_up_cost_per_tb": 5.01},
        {"rentable": False},
        {"verification": "unverified"},
        {"reliability2": 0.97},
        {"gpu_ram": 6144},
        {"disk_space": 30.0},
        {"cuda_max_good": 12.4},
        {"compute_cap": 610},
        {"direct_port_count": 0},
    ],
)
def test_each_constraint_rejects_its_violation(override: dict) -> None:
    assert not sweep.offer_satisfies_constraints(offer(**override))


def test_inet_cost_boundary_is_inclusive() -> None:
    assert sweep.offer_satisfies_constraints(
        offer(internet_down_cost_per_tb=5.0, internet_up_cost_per_tb=5.0)
    )


def test_eight_gib_gpu_is_eligible() -> None:
    assert sweep.offer_satisfies_constraints(offer(gpu_ram=8192))


def test_market_rate_uses_every_listed_offer() -> None:
    offers = [offer(dph_total=price) for price in (0.10, 0.20, 0.60)]

    assert sweep.market_rate_usd_per_hour(offers) == pytest.approx(0.20)


def test_ranking_rejects_offers_above_the_market_multiple() -> None:
    cheap = offer(id=1, dph_total=0.20)
    overpriced = offer(id=2, dph_total=0.27)
    others = [offer(id=3, dph_total=0.20), offer(id=4, dph_total=0.20)]

    ranked = sweep.rank_offers_for_gpu([cheap, overpriced, *others], "RTX 5080")

    # The median is 0.20, so the ceiling is 0.26 and the 0.27 offer drops out.
    assert [entry["id"] for entry in ranked] == [1, 3, 4]


def test_ranking_keeps_an_offer_exactly_at_the_ceiling() -> None:
    offers = [offer(id=1, dph_total=0.20), offer(id=2, dph_total=0.26)]

    ranked = sweep.rank_offers_for_gpu(offers, "RTX 5080")

    assert [entry["id"] for entry in ranked] == [1, 2]


def test_ranking_orders_by_price_and_drops_unusable_offers() -> None:
    offers = [
        offer(id=1, dph_total=0.20),
        offer(id=2, dph_total=0.15, internet_up_cost_per_tb=8.0),
        offer(id=3, dph_total=0.18),
    ]

    ranked = sweep.rank_offers_for_gpu(offers, "RTX 5080")

    assert [entry["id"] for entry in ranked] == [3, 1]


def test_ranking_returns_nothing_when_no_offer_qualifies() -> None:
    offers = [offer(id=1, compute_cap=610), offer(id=2, compute_cap=610)]

    assert sweep.rank_offers_for_gpu(offers, "RTX 5080") == []


def test_ranking_ignores_other_models() -> None:
    offers = [offer(id=1, gpu_name="RTX 5070 Ti", dph_total=0.11), offer(id=2)]

    ranked = sweep.rank_offers_for_gpu(offers, "RTX 5080")

    assert [entry["id"] for entry in ranked] == [2]


def test_queue_skips_measured_models_and_sorts_by_price() -> None:
    offers = [
        offer(id=1, gpu_name="RTX 4090", dph_total=0.30),
        offer(id=2, gpu_name="RTX 5080", dph_total=0.18),
        offer(id=3, gpu_name="RTX 5070 Ti", dph_total=0.11),
    ]

    queue = sweep.untested_gpu_queue(offers, benchmarked=("RTX 4090",))

    assert [name for name, _ in queue] == ["RTX 5070 Ti", "RTX 5080"]


@pytest.mark.parametrize(
    "gpu_name",
    [
        "A10",
        "A100 PCIE",
        "CMP 170HX",
        "L4",
        "RTX 3050",
        "RTX 3080",
        "RTX 4070S Ti",
        "RTX 4080",
        "RTX A6000",
    ],
)
def test_default_queue_skips_newly_published_models(gpu_name: str) -> None:
    assert sweep.untested_gpu_queue([offer(gpu_name=gpu_name)]) == []


def test_queue_omits_a_model_with_no_usable_offer() -> None:
    offers = [offer(id=1, gpu_name="Tesla P40", compute_cap=610), offer(id=2)]

    queue = sweep.untested_gpu_queue(offers, benchmarked=())

    assert [name for name, _ in queue] == ["RTX 5080"]


def test_batches_are_three_wide_with_a_short_tail() -> None:
    names = [f"gpu{index}" for index in range(7)]

    assert sweep.split_batches(names) == [
        ["gpu0", "gpu1", "gpu2"],
        ["gpu3", "gpu4", "gpu5"],
        ["gpu6"],
    ]


def test_batch_size_must_be_positive() -> None:
    with pytest.raises(sweep.SweepError, match="at least one"):
        sweep.split_batches(["gpu0"], batch_size=0)


def test_batch_cost_is_price_times_hours() -> None:
    offers = [offer(dph_total=0.10), offer(dph_total=0.30)]

    assert sweep.estimate_batch_cost_usd(offers, hours=0.5) == pytest.approx(0.20)


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
    """From results/gpu-benchmark-2026-09-23/sol/summary.json (5060 Ti baseline); 5090 is the conservative host."""
    assert sweep.FIT_SPEED_VS_5060_TI == {
        "RTX 5060": 0.9, "RTX 5060 Ti": 1.00, "RTX 5070": 1.33,
        "RTX 5080": 2.39, "RTX 5090": 2.84,
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
