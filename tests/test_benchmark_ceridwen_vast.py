from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from scripts import benchmark_ceridwen_vast as benchmark


def result(workload_id: str, calls_per_second: float, cost: float) -> dict:
    workload = {"id": workload_id}
    input_sha256 = {"mock": "input-sha"}
    runtime = {
        "python": "3.11",
        "jax": "0.10.2",
        "jaxlib": "0.10.2",
        "blackjax": "test",
        "ceridwen": "test",
        "jax_enable_x64": True,
        "xla_preallocate_env": "false",
        "xla_memory_fraction_env": None,
    }
    ceridwen_commit = "ceridwen-commit"
    record = {
        "schema_version": benchmark.RESULT_SCHEMA_VERSION,
        "benchmark_script_sha256": "script-sha",
        "workload": workload,
        "input_sha256": input_sha256,
        "runtime": runtime,
        "git": {"ceridwen_commit": ceridwen_commit},
        "timings": {
            "likelihood_calls_per_second": calls_per_second,
            "cost_per_100k_likelihood_calls_usd": cost,
        },
    }
    record["comparison_fingerprint"] = benchmark._comparison_fingerprint(
        workload,
        input_sha256,
        ceridwen_commit,
        runtime,
    )
    return record


def test_fixed_workload_contract() -> None:
    assert benchmark.WORKLOAD_ID == "m1_210210_joint_full_v1"
    assert benchmark.EXPECTED_PHOTOMETRY_BANDS == 11
    assert benchmark.EXPECTED_SPECTRAL_PIXELS == 3523
    assert benchmark.TIMED_STEPS == 5
    assert benchmark.CALLS_PER_STEP == 1000
    assert benchmark.RESULT_SCHEMA_VERSION == 2


def test_cuda_environment_reduces_jax_preallocation(monkeypatch) -> None:
    monkeypatch.setenv("JAX_PLATFORMS", "cpu")
    monkeypatch.setenv("JAX_ENABLE_X64", "0")
    monkeypatch.setenv("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
    monkeypatch.setenv("XLA_CLIENT_MEM_FRACTION", "0.75")
    monkeypatch.setenv("JAX_DEFAULT_MATMUL_PRECISION", "default")
    monkeypatch.setenv("LD_LIBRARY_PATH", "/system/cuda")

    benchmark._configure_cuda_environment()

    assert benchmark.os.environ["JAX_PLATFORMS"] == "cuda"
    assert benchmark.os.environ["JAX_ENABLE_X64"] == "1"
    assert benchmark.os.environ["JAX_DEFAULT_MATMUL_PRECISION"] == "highest"
    assert "XLA_PYTHON_CLIENT_PREALLOCATE" not in benchmark.os.environ
    assert benchmark.os.environ["XLA_CLIENT_MEM_FRACTION"] == "0.50"
    assert "LD_LIBRARY_PATH" not in benchmark.os.environ


def test_metrics_use_all_timed_steps() -> None:
    metrics = benchmark.calculate_metrics(
        [2.0, 4.0],
        calls_per_step=1000,
        price_usd_per_hour=1.8,
    )

    assert metrics["timed_likelihood_calls"] == 2000
    assert metrics["total_timed_seconds"] == 6.0
    assert metrics["likelihood_calls_per_second"] == pytest.approx(1000 / 3)
    assert metrics["cost_per_100k_likelihood_calls_usd"] == pytest.approx(0.15)


def test_metrics_reject_invalid_durations() -> None:
    with pytest.raises(benchmark.BenchmarkError, match="must be positive"):
        benchmark.calculate_metrics(
            [1.0, 0.0],
            calls_per_step=1000,
            price_usd_per_hour=1.0,
        )


def test_result_directory_name_is_human_readable() -> None:
    name = benchmark.result_directory_name(
        "NVIDIA A100-SXM4-40GB",
        "148498",
        "2026-08-26",
    )

    assert name == (
        "ceridwen_vast_a100_sxm4_40gb_host_148498_"
        "joint_full_baseline_benchmark_complete_2026-08-26"
    )

    fast_name = benchmark.result_directory_name(
        "NVIDIA GeForce RTX 5060",
        "154485",
        "2026-08-28",
        "A",
    )
    assert fast_name == (
        "ceridwen_vast_geforce_rtx_5060_host_154485_"
        "joint_full_fastpath_a_benchmark_complete_2026-08-28"
    )


def test_select_sfh_basis_implementation_requires_requested_path() -> None:
    class CSP:
        flux = SimpleNamespace(shape=(5, 13, 107, 10992))
        _sfh_basis = SimpleNamespace(shape=(5, 13, 8, 10992))
        _sfh_basis_flat = SimpleNamespace(shape=(520, 10992))
        sfh_basis_fastpath = None

        def select_sfh_basis_fastpath(self, selector):
            self.sfh_basis_fastpath = selector

    workload = SimpleNamespace(model=SimpleNamespace(csp=CSP()))
    selected = benchmark.select_sfh_basis_implementation(workload, "A")

    assert selected == {
        "sfh_basis_fastpath": "A",
        "basis_shape": [5, 13, 8, 10992],
    }


def test_select_sfh_basis_implementation_rejects_fallback() -> None:
    class CSP:
        sfh_basis_fastpath = None

        def select_sfh_basis_fastpath(self, selector):
            del selector

    workload = SimpleNamespace(model=SimpleNamespace(csp=CSP()))

    with pytest.raises(benchmark.BenchmarkError, match="did not activate"):
        benchmark.select_sfh_basis_implementation(workload, "A")


def test_rank_records_uses_cost() -> None:
    expensive = result("same", calls_per_second=200.0, cost=0.2)
    cheap = result("same", calls_per_second=100.0, cost=0.1)

    assert benchmark.rank_records([expensive, cheap]) == [cheap, expensive]


def test_rank_records_rejects_mismatched_fingerprints() -> None:
    with pytest.raises(benchmark.BenchmarkError, match="different workloads"):
        benchmark.rank_records(
            [
                result("first", calls_per_second=100.0, cost=0.1),
                result("second", calls_per_second=100.0, cost=0.1),
            ]
        )


def test_allocator_and_script_changes_remain_comparable() -> None:
    first = result("same", calls_per_second=100.0, cost=0.1)
    second = result("same", calls_per_second=110.0, cost=0.09)
    second["runtime"]["xla_preallocate_env"] = None
    second["runtime"]["xla_memory_fraction_env"] = "0.50"
    second["benchmark_script_sha256"] = "different-script-sha"

    assert benchmark._normalized_comparison_fingerprint(first) == (
        benchmark._normalized_comparison_fingerprint(second)
    )


def test_legacy_and_current_results_remain_comparable() -> None:
    current = result("same", calls_per_second=110.0, cost=0.09)
    legacy = json.loads(json.dumps(result("same", calls_per_second=100.0, cost=0.1)))
    legacy["schema_version"] = benchmark.LEGACY_RESULT_SCHEMA_VERSION
    legacy["runtime"]["xla_preallocate_env"] = None
    legacy["comparison_fingerprint"] = benchmark._legacy_comparison_fingerprint(legacy)

    assert benchmark.rank_records([legacy, current]) == [current, legacy]


def test_invalid_legacy_fingerprint_is_rejected() -> None:
    legacy = result("same", calls_per_second=100.0, cost=0.1)
    legacy["schema_version"] = benchmark.LEGACY_RESULT_SCHEMA_VERSION
    legacy["comparison_fingerprint"] = "invalid"

    with pytest.raises(benchmark.BenchmarkError, match="invalid comparison"):
        benchmark.rank_records([legacy])


def test_flat_result_row_keeps_comparison_metrics() -> None:
    record = {
        "schema_version": benchmark.RESULT_SCHEMA_VERSION,
        "comparison_fingerprint": "same",
        "started_at_utc": "2026-08-26T12:00:00+00:00",
        "workload": {"id": benchmark.WORKLOAD_ID},
        "runtime": {"jax_device_kind": "NVIDIA A100-SXM4-40GB"},
        "vast": {
            "host": "148498",
            "instance": "48652928",
            "price_usd_per_hour": 0.67,
        },
        "timings": {
            "timed_steps": 5,
            "timed_likelihood_calls": 5000,
            "total_timed_seconds": 40.0,
            "median_step_seconds": 8.0,
            "iqr_step_seconds": 0.2,
            "likelihood_calls_per_second": 125.0,
            "cost_per_100k_likelihood_calls_usd": 0.148888,
        },
        "memory": {
            "jax": {"peak_bytes_in_use_mib": 1500.0},
            "nvidia_process_memory_mib": 26000.0,
        },
        "git": {"project_commit": "root", "ceridwen_commit": "submodule"},
    }

    row = benchmark._flat_result_row(record)

    assert row["workload_id"] == benchmark.WORKLOAD_ID
    assert row["timed_likelihood_calls"] == 5000
    assert row["likelihood_calls_per_second"] == 125.0
    assert row["cost_per_100k_likelihood_calls_usd"] == 0.148888
    assert row["ceridwen_commit"] == "submodule"


def test_result_file_discovery_accepts_directories(tmp_path) -> None:
    result_dir = tmp_path / "ceridwen_vast_a100_benchmark"
    result_dir.mkdir()
    result_path = result_dir / "benchmark.json"
    result_path.write_text(json.dumps({"schema_version": 1}), encoding="utf-8")

    assert benchmark._result_json_paths([tmp_path]) == [result_path]


def test_fixed_step_runner_uses_pinned_blackjax_layout(monkeypatch) -> None:
    monkeypatch.setenv("JAX_PLATFORMS", "cpu")
    monkeypatch.setattr(benchmark, "NUM_LIVE", 8)
    monkeypatch.setattr(benchmark, "NUM_DELETE", 2)
    monkeypatch.setattr(benchmark, "NUM_INNER_STEPS", 2)
    monkeypatch.setattr(benchmark, "WARMUP_STEPS", 1)
    monkeypatch.setattr(benchmark, "TIMED_STEPS", 2)

    import jax
    import jax.numpy as jnp

    class Prior:
        def sample(self, key, shape):
            return jax.random.uniform(key, shape, minval=-1.0, maxval=1.0)

    class LikelihoodComponent:
        def __call__(self, values, prediction, uncertainty, mask, params):
            del params
            residual = (values - prediction) / uncertainty
            return -0.5 * jnp.sum(jnp.where(mask, residual**2, 0.0)), None

    observation = SimpleNamespace(
        flux=jnp.array([0.0]),
        uncertainty=jnp.array([1.0]),
        mask=jnp.array([True]),
    )
    model = SimpleNamespace(
        obs_dict={"mock": observation},
        theta_init={"x": jnp.array([0.0])},
        priors={"x": Prior()},
        predict=lambda theta: {"mock": theta["x"]},
        ln_prior=lambda theta: jnp.where(
            jnp.abs(theta["x"][0]) <= 1.0,
            0.0,
            -jnp.inf,
        ),
    )
    likelihood = SimpleNamespace(
        keys=("mock",),
        likelihoods=(LikelihoodComponent(),),
    )

    timings = benchmark.run_fixed_steps(
        benchmark.BuiltWorkload(
            model=model,
            likelihood=likelihood,
            metadata={},
            input_paths={},
        )
    )

    assert len(timings["warmup_step_seconds"]) == 1
    assert len(timings["iteration_seconds"]) == 2
    assert all(value > 0 for value in timings["iteration_seconds"])
