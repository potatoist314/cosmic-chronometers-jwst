from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from scripts import benchmark_ceridwen_sfh_basis_fastpath as harness


def test_prediction_comparison_accepts_fp32_roundoff() -> None:
    references = [{"spectrum": np.array([1.0, 2.0], dtype=np.float32)}]
    candidates = [
        {"spectrum": np.array([1.0 + 1e-6, 2.0 - 1e-6], dtype=np.float32)}
    ]

    errors = harness._compare_predictions(references, candidates)

    assert errors["max_absolute_error"] > 0.0
    assert errors["max_relative_error"] < 5e-5


def test_prediction_comparison_rejects_scientific_mismatch() -> None:
    references = [{"spectrum": np.array([1.0, 2.0], dtype=np.float32)}]
    candidates = [{"spectrum": np.array([1.0, 2.1], dtype=np.float32)}]

    with pytest.raises(harness.benchmark.BenchmarkError, match="verification failed"):
        harness._compare_predictions(references, candidates)


def test_legacy_result_defaults_to_baseline() -> None:
    implementation = harness._implementation_from_record({"runtime": {}})

    assert implementation["experiment_id"] == harness.EXPERIMENT_ID
    assert implementation["mode"] == "baseline"
    assert implementation["basis_bytes"] == 0


def test_implementation_metadata_records_source_hashes() -> None:
    implementation = harness._base_implementation("corners")

    assert implementation["mode"] == "corners"
    assert len(implementation["harness_sha256"]) == 64
    assert len(implementation["fastpath_source_sha256"]) == 64


def test_run_wrapper_installs_metadata_and_restores_hooks(monkeypatch) -> None:
    benchmark = harness.benchmark
    original_build = benchmark.build_joint_workload
    original_runtime = benchmark._runtime_metadata
    original_directory_name = benchmark.result_directory_name
    original_flat_row = benchmark._flat_result_row
    fake_workload = SimpleNamespace(model=SimpleNamespace())

    monkeypatch.setattr(
        benchmark,
        "build_joint_workload",
        lambda project_root: fake_workload,
    )
    monkeypatch.setattr(
        benchmark,
        "_runtime_metadata",
        lambda jax, device: {"device": "mock"},
    )
    monkeypatch.setattr(
        benchmark,
        "result_directory_name",
        lambda gpu_name, host, date: "base-result",
    )
    monkeypatch.setattr(
        benchmark,
        "_flat_result_row",
        lambda result: {"gpu_name": "mock"},
    )
    monkeypatch.setattr(
        harness,
        "_install_and_verify",
        lambda workload, mode: {
            "experiment_id": harness.EXPERIMENT_ID,
            "mode": mode,
            "basis_shape": [5, 13, 7, 64],
            "basis_bytes": 1234,
            "source_verification": {},
            "prediction_verification": {},
        },
    )

    wrapped_build = benchmark.build_joint_workload
    wrapped_runtime = benchmark._runtime_metadata
    wrapped_directory_name = benchmark.result_directory_name
    wrapped_flat_row = benchmark._flat_result_row

    def fake_command_run(args) -> int:
        workload = benchmark.build_joint_workload(Path("."))
        assert workload is fake_workload
        runtime = benchmark._runtime_metadata(None, None)
        assert runtime["ceridwen_fastpath"]["mode"] == "sfh-basis-sparse"
        assert benchmark.result_directory_name("GPU", "12", "2026-08-27") == (
            "base-result_implementation_sfh_basis_sparse"
        )
        row = benchmark._flat_result_row({"runtime": runtime})
        assert row["implementation"] == "sfh-basis-sparse"
        assert row["fastpath_basis_bytes"] == 1234
        return 17

    monkeypatch.setattr(benchmark, "command_run", fake_command_run)
    args = SimpleNamespace(implementation="sfh-basis-sparse")

    assert harness.command_run(args) == 17
    assert benchmark.build_joint_workload is wrapped_build
    assert benchmark._runtime_metadata is wrapped_runtime
    assert benchmark.result_directory_name is wrapped_directory_name
    assert benchmark._flat_result_row is wrapped_flat_row

    monkeypatch.setattr(benchmark, "build_joint_workload", original_build)
    monkeypatch.setattr(benchmark, "_runtime_metadata", original_runtime)
    monkeypatch.setattr(benchmark, "result_directory_name", original_directory_name)
    monkeypatch.setattr(benchmark, "_flat_result_row", original_flat_row)


def test_parser_accepts_all_experimental_modes() -> None:
    parser = harness.build_parser()

    for mode in harness.IMPLEMENTATIONS:
        args = parser.parse_args(
            [
                "run",
                "--implementation",
                mode,
                "--price-usd-per-hour",
                "0.1",
            ]
        )
        assert args.implementation == mode
