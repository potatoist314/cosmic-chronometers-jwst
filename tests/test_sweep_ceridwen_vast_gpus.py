from __future__ import annotations

from dataclasses import replace

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


BENCHMARK_PATHS = ("baseline", "basis_fast", "projection_fast")
REQUIRED_ARTIFACTS = ("benchmark.json", "environment.json", "hlo.txt")
SHA256_A = "a" * 64


def benchmark_plan() -> sweep.BenchmarkPlan:
    selection = sweep.select_benchmark_offer(
        [offer(id=5060, gpu_name="RTX 5060", dph_total=0.25)],
        projected_runtime_hours=4.0,
    )
    return sweep.build_benchmark_plan(
        selection,
        instance_id=812345,
        benchmark_paths=BENCHMARK_PATHS,
        required_artifacts=REQUIRED_ARTIFACTS,
    )


def observation(path: str, **overrides) -> sweep.BenchmarkObservation:
    base = {
        "benchmark_path": path,
        "instance_id": 812345,
        "gpu_name": "RTX 5060",
        "gpu_utilization_percent": 73.0,
        "result_markers": (0, 4),
        "completed": True,
    }
    return sweep.BenchmarkObservation(**{**base, **overrides})


def complete_lifecycle() -> sweep.BenchmarkLifecycle:
    return sweep.BenchmarkLifecycle(
        observations=tuple(observation(path) for path in BENCHMARK_PATHS),
        actual_spend_by_instance={812345: 0.84},
        copy_manifest=tuple(
            sweep.CopyManifestEntry(path, SHA256_A, SHA256_A)
            for path in REQUIRED_ARTIFACTS
        ),
        environment_metadata={
            "benchmark_commit": "abc1234",
            "cuda_version": "12.8",
            "gpu_name": "RTX 5060",
            "instance_id": "812345",
            "jax_version": "0.7.1",
            "jaxlib_version": "0.7.1",
            "python_version": "3.11.13",
        },
        retries_used=0,
        terminated_instance_id=812345,
        termination_confirmed=True,
    )


def test_reference_fingerprint_matches_published_runs() -> None:
    assert sweep.DEFAULT_IMAGE == "vastai/base-image:cuda-12.6.3-auto"
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


def test_benchmark_selection_prefers_a_suitable_rtx_5060() -> None:
    offers = [
        offer(id=1, gpu_name="RTX 5070", dph_total=0.10),
        offer(id=2, gpu_name="RTX 5060", dph_total=0.20),
    ]

    selected = sweep.select_benchmark_offer(
        offers,
        projected_runtime_hours=2.0,
    )

    assert selected.offer_id == 2
    assert selected.projected_total_additional_cost_usd == pytest.approx(0.40)


def test_benchmark_selection_uses_cheapest_when_rtx_5060_is_unsuitable() -> None:
    offers = [
        offer(id=1, gpu_name="RTX 5060", dph_total=0.08, disk_space=20.0),
        offer(id=2, gpu_name="RTX 5070", dph_total=0.15),
        offer(id=3, gpu_name="RTX 5080", dph_total=0.12),
    ]

    selected = sweep.select_benchmark_offer(
        offers,
        projected_runtime_hours=2.0,
    )

    assert selected.offer_id == 3


def test_benchmark_selection_rejects_every_over_cap_plan() -> None:
    offers = [
        offer(id=1, gpu_name="RTX 5060", dph_total=5.01),
        offer(id=2, gpu_name="RTX 5070", dph_total=5.50),
    ]

    with pytest.raises(sweep.SweepError, match="USD 10"):
        sweep.select_benchmark_offer(offers, projected_runtime_hours=2.0)


def test_over_cap_rtx_5060_falls_back_to_cheapest_under_cap_offer() -> None:
    offers = [
        offer(id=1, gpu_name="RTX 5060", dph_total=5.01),
        offer(id=2, gpu_name="RTX 5070", dph_total=4.50),
    ]

    selected = sweep.select_benchmark_offer(
        offers,
        projected_runtime_hours=2.0,
    )

    assert selected.offer_id == 2
    assert selected.projected_total_additional_cost_usd == pytest.approx(9.0)


def test_benchmark_selection_includes_fixed_cost_in_the_cap() -> None:
    offers = [offer(id=1, gpu_name="RTX 5060", dph_total=4.75)]

    with pytest.raises(sweep.SweepError, match="USD 10"):
        sweep.select_benchmark_offer(
            offers,
            projected_runtime_hours=2.0,
            projected_fixed_cost_usd=0.51,
        )


def test_benchmark_selection_cannot_raise_the_ten_dollar_cap() -> None:
    with pytest.raises(sweep.SweepError, match="between USD 0 and USD 10"):
        sweep.select_benchmark_offer(
            [offer()],
            projected_runtime_hours=1.0,
            spend_cap_usd=10.01,
        )


def test_plan_requires_baseline_and_two_distinct_fast_paths() -> None:
    selection = sweep.select_benchmark_offer(
        [offer(gpu_name="RTX 5060")],
        projected_runtime_hours=1.0,
    )

    with pytest.raises(sweep.SweepError, match="baseline and two distinct"):
        sweep.build_benchmark_plan(
            selection,
            instance_id=812345,
            benchmark_paths=("baseline", "basis_fast", "basis_fast"),
            required_artifacts=REQUIRED_ARTIFACTS,
        )


def test_spend_is_keyed_by_the_exact_instance_id() -> None:
    spend = sweep.spend_by_instance(benchmark_plan(), complete_lifecycle())

    assert spend == {
        812345: {"projected_usd": pytest.approx(1.0), "actual_usd": 0.84}
    }


def test_spend_rejects_an_unrelated_instance_id() -> None:
    lifecycle = replace(
        complete_lifecycle(),
        actual_spend_by_instance={999999: 0.84},
    )

    with pytest.raises(sweep.SweepError, match="unrelated instance ID"):
        sweep.spend_by_instance(benchmark_plan(), lifecycle)


def test_stall_policy_waits_then_allows_exactly_one_retry() -> None:
    common = {"planned_instance_id": 812345, "observed_instance_id": 812345}

    assert (
        sweep.stalled_benchmark_action(
            **common,
            stalled_seconds=299,
            retries_used=0,
        )
        == "wait"
    )
    assert (
        sweep.stalled_benchmark_action(
            **common,
            stalled_seconds=300,
            retries_used=0,
        )
        == "retry"
    )
    assert (
        sweep.stalled_benchmark_action(
            **common,
            stalled_seconds=300,
            retries_used=1,
        )
        == "abort"
    )


def test_stall_policy_rejects_an_unrelated_instance_id() -> None:
    with pytest.raises(sweep.SweepError, match="unrelated instance ID"):
        sweep.stalled_benchmark_action(
            planned_instance_id=812345,
            observed_instance_id=999999,
            stalled_seconds=300,
            retries_used=0,
        )


def test_complete_lifecycle_satisfies_every_success_safeguard() -> None:
    sweep.validate_benchmark_success(benchmark_plan(), complete_lifecycle())


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        (
            {"gpu_utilization_percent": 0.0},
            "no GPU-use evidence",
        ),
        (
            {"result_markers": (7, 7)},
            "no advancing results",
        ),
        (
            {"gpu_name": "RTX 5070"},
            "same GPU",
        ),
        (
            {"instance_id": 999999},
            "unrelated instance ID",
        ),
    ],
)
def test_success_rejects_invalid_run_evidence(
    replacement: dict,
    message: str,
) -> None:
    lifecycle = complete_lifecycle()
    bad_observation = replace(lifecycle.observations[1], **replacement)
    lifecycle = replace(
        lifecycle,
        observations=(
            lifecycle.observations[0],
            bad_observation,
            lifecycle.observations[2],
        ),
    )

    with pytest.raises(sweep.SweepError, match=message):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)


def test_success_rejects_more_than_one_retry() -> None:
    lifecycle = replace(complete_lifecycle(), retries_used=2)

    with pytest.raises(sweep.SweepError, match="more than one retry"):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)


def test_success_rejects_an_incomplete_copy_manifest() -> None:
    lifecycle = complete_lifecycle()
    lifecycle = replace(lifecycle, copy_manifest=lifecycle.copy_manifest[:-1])

    with pytest.raises(sweep.SweepError, match="copy manifest is incomplete"):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)


def test_success_rejects_a_copy_hash_mismatch() -> None:
    lifecycle = complete_lifecycle()
    bad_entry = replace(lifecycle.copy_manifest[0], copied_sha256="b" * 64)
    lifecycle = replace(
        lifecycle,
        copy_manifest=(bad_entry, *lifecycle.copy_manifest[1:]),
    )

    with pytest.raises(sweep.SweepError, match="integrity check"):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)


def test_success_rejects_incomplete_environment_metadata() -> None:
    lifecycle = complete_lifecycle()
    metadata = dict(lifecycle.environment_metadata)
    del metadata["cuda_version"]
    lifecycle = replace(lifecycle, environment_metadata=metadata)

    with pytest.raises(sweep.SweepError, match="metadata is incomplete"):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        ({"terminated_instance_id": 999999}, "termination is not confirmed"),
        ({"termination_confirmed": False}, "termination is not confirmed"),
        ({"actual_spend_by_instance": {812345: 10.01}}, "actual benchmark spend"),
    ],
)
def test_success_rejects_unsafe_final_lifecycle_state(
    replacement: dict,
    message: str,
) -> None:
    lifecycle = replace(complete_lifecycle(), **replacement)

    with pytest.raises(sweep.SweepError, match=message):
        sweep.validate_benchmark_success(benchmark_plan(), lifecycle)
