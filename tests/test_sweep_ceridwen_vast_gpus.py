from __future__ import annotations

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
    assert sweep.REFERENCE_FINGERPRINT == (
        "26b63c693d339d9093e68b311df48719ee5697555522b13bf8e85dc0521735cc"
    )
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
