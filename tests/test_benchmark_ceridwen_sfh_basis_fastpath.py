from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

from scripts import benchmark_ceridwen_sfh_basis_fastpath as benchmark


def contract(implementation: str, *, seed: int = benchmark.SEED) -> dict:
    value = benchmark.comparison_contract(
        implementation=implementation,
        ceridwen_commit="core-fastpath-commit",
        workload={"id": "fixed-workload", "shape": [5, 13, 107, 10992]},
        runtime={"jax": "0.10.2", "jax_enable_x64": True},
    )
    value["seed"] = seed
    return value


def test_fixed_experiment_contract() -> None:
    assert benchmark.IMPLEMENTATIONS == ("baseline", "variant_a", "variant_b")
    assert benchmark.SEED == 20260827
    assert benchmark.FORBIDDEN_EXPANSION == (13, 107, 10992)
    assert benchmark.PREDICTION_RTOL == 5.0e-5
    assert benchmark.LOGLIKE_RTOL == 1.0e-4


def test_fingerprints_differ_only_by_implementation() -> None:
    contracts = [contract(name) for name in benchmark.IMPLEMENTATIONS]

    benchmark.require_comparable_contracts(contracts)

    assert len({benchmark.normalized_fingerprint(item) for item in contracts}) == 1
    assert [item["implementation"] for item in contracts] == list(
        benchmark.IMPLEMENTATIONS
    )


def test_fingerprints_reject_scientific_drift() -> None:
    contracts = [contract(name) for name in benchmark.IMPLEMENTATIONS]
    contracts[-1] = contract("variant_b", seed=1)

    with pytest.raises(benchmark.BenchmarkError, match="other than implementation"):
        benchmark.require_comparable_contracts(contracts)


def test_stablehlo_evidence_detects_full_expansion() -> None:
    baseline_hlo = """
      %0 = stablehlo.add %arg0, %arg1
        : tensor<13x107x10992xf32>
    """
    fast_hlo = """
      %0 = stablehlo.dot_general %arg0, %arg1
        : (tensor<2x2x107x10992xf32>, tensor<2xf32>) -> tensor<10992xf32>
    """

    baseline = benchmark.stablehlo_evidence(baseline_hlo)
    fast = benchmark.stablehlo_evidence(fast_hlo)

    assert baseline["forbidden_expansion_occurrences"] == 1
    assert not baseline["omits_forbidden_expansion"]
    assert len(baseline["forbidden_expansion_lines"][0]) <= 240
    assert fast["forbidden_expansion_occurrences"] == 0
    assert fast["omits_forbidden_expansion"]
    assert len(fast["stablehlo_sha256"]) == 64


def test_timing_metrics_report_requested_fields() -> None:
    metrics = benchmark.timing_metrics([1.0, 2.0, 3.0, 4.0])

    assert metrics["calls_per_second"] == pytest.approx(0.4)
    assert metrics["median_step_seconds"] == pytest.approx(2.5)
    assert metrics["iqr_step_seconds"] == pytest.approx(1.5)
    assert metrics["total_seconds"] == pytest.approx(10.0)


def test_timing_metrics_reject_nonpositive_values() -> None:
    with pytest.raises(benchmark.BenchmarkError, match="must be positive"):
        benchmark.timing_metrics([1.0, 0.0])


def test_compare_evaluations_checks_predictions_and_full_loglike() -> None:
    reference = benchmark.Evaluation(
        label="random_0",
        predictions={
            "photometry": np.array([1.0, 2.0]),
            "spectrum": np.array([3.0, 4.0]),
        },
        log_likelihood=-100.0,
    )
    candidate = benchmark.Evaluation(
        label="random_0",
        predictions={
            "photometry": np.array([1.0 + 1e-6, 2.0]),
            "spectrum": np.array([3.0, 4.0 - 1e-6]),
        },
        log_likelihood=-100.0001,
    )

    result = benchmark.compare_evaluations(reference, candidate)

    assert result["prediction_deltas"]["photometry"]["max_absolute"] == (
        pytest.approx(1e-6)
    )
    assert result["log_likelihood_delta"]["absolute"] == pytest.approx(1e-4)


def test_compare_evaluations_rejects_out_of_tolerance_result() -> None:
    reference = benchmark.Evaluation(
        label="edge",
        predictions={"spectrum": np.array([1.0])},
        log_likelihood=-1.0,
    )
    candidate = benchmark.Evaluation(
        label="edge",
        predictions={"spectrum": np.array([2.0])},
        log_likelihood=-1.0,
    )

    with pytest.raises(AssertionError):
        benchmark.compare_evaluations(reference, candidate)


def test_install_implementation_records_core_basis_shapes() -> None:
    import jax.numpy as jnp

    class CSP:
        flux = jnp.ones((5, 13, 107, 11))
        _sfh_basis = None
        _sfh_basis_flat = None

        def select_sfh_basis_fastpath(self, selector):
            if selector == "A":
                self._sfh_basis = jnp.ones((5, 13, 8, 11))
            elif selector == "B":
                self._sfh_basis_flat = jnp.ones((520, 11))

    csp = CSP()

    assert benchmark.install_implementation(csp, "baseline") == [5, 13, 107, 11]
    assert benchmark.install_implementation(csp, "variant_a") == [5, 13, 8, 11]
    assert benchmark.install_implementation(csp, "variant_b") == [520, 11]

    with pytest.raises(benchmark.BenchmarkError, match="unknown implementation"):
        benchmark.install_implementation(csp, "unknown")


def test_deterministic_prior_points_use_fixed_seed() -> None:
    import jax
    import jax.numpy as jnp

    class Prior:
        def sample(self, key, shape):
            return jax.random.uniform(key, shape)

    model = SimpleNamespace(
        theta_init={"x": jnp.zeros(3), "y": jnp.zeros(1)},
        priors={"x": Prior(), "y": Prior()},
    )

    first = benchmark.deterministic_prior_points(model, 3)
    second = benchmark.deterministic_prior_points(model, 3)

    for first_point, second_point in zip(first, second, strict=True):
        np.testing.assert_array_equal(first_point["x"], second_point["x"])
        np.testing.assert_array_equal(first_point["y"], second_point["y"])
    assert not np.array_equal(first[0]["x"], first[1]["x"])


def test_edge_points_include_prior_boundaries() -> None:
    import jax.numpy as jnp

    model = SimpleNamespace(
        theta_init={"x": jnp.array([0.5]), "fixed": jnp.array([2.0])},
        priors={
            "x": SimpleNamespace(bounds=(jnp.array(-1.0), jnp.array(1.0))),
            "fixed": SimpleNamespace(),
        },
    )

    points = dict(benchmark.edge_points(model))

    np.testing.assert_array_equal(points["initial"]["x"], [0.5])
    np.testing.assert_array_equal(points["lower_edges"]["x"], [-1.0])
    np.testing.assert_array_equal(points["upper_edges"]["x"], [1.0])
    np.testing.assert_array_equal(points["lower_edges"]["fixed"], [2.0])
