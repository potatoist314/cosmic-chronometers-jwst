#!/usr/bin/env python3
"""Benchmark experimental low-rank Ceridwen source-spectrum fast paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

if __package__:
    from . import benchmark_ceridwen_vast as benchmark
else:
    import benchmark_ceridwen_vast as benchmark

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "ceridwen_sfh_basis_fastpath_v1"
IMPLEMENTATIONS = (
    "baseline",
    "corners",
    "sfh-basis-sparse",
    "sfh-basis-dense",
)


def _verification_free_thetas(model: Any) -> list[dict[str, Any]]:
    """Return deterministic free-parameter points spanning the benchmark prior."""
    import jax.numpy as jnp

    base = {name: jnp.array(value) for name, value in model.theta_init.items()}
    csp = model.csp
    z_min = csp.zmet[0]
    z_max = csp.zmet[-1]
    afe_min = csp.afe_grid[0]
    afe_max = csp.afe_grid[-1]

    low = dict(base)
    low["logsfr_ratios"] = jnp.linspace(-2.5, 2.5, base["logsfr_ratios"].size)
    low["Z"] = jnp.atleast_1d(z_min + 0.1 * (z_max - z_min))
    low["afe"] = jnp.atleast_1d(afe_min)
    low["diffuse_tau_kc"] = jnp.array([0.0])

    high = dict(base)
    high["logsfr_ratios"] = jnp.linspace(2.5, -2.5, base["logsfr_ratios"].size)
    high["Z"] = jnp.atleast_1d(z_min + 0.9 * (z_max - z_min))
    high["afe"] = jnp.atleast_1d(afe_max)
    high["diffuse_tau_kc"] = jnp.array([1.8])
    return [base, low, high]


def _compare_predictions(
    references: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    rtol: float = 5e-5,
    atol_fraction: float = 1e-7,
) -> dict[str, float]:
    """Check complete photometric and spectral predictions at fixed points."""
    import numpy as np

    max_absolute_error = 0.0
    max_relative_error = 0.0
    for reference, candidate in zip(references, candidates, strict=True):
        if reference.keys() != candidate.keys():
            raise benchmark.BenchmarkError(
                "fast-path verification changed the prediction keys"
            )
        for name in reference:
            reference_array = np.asarray(reference[name])
            candidate_array = np.asarray(candidate[name])
            scale = float(np.max(np.abs(reference_array)))
            atol = max(np.finfo(np.float32).tiny, atol_fraction * scale)
            difference = np.abs(candidate_array - reference_array)
            denominator = np.maximum(np.abs(reference_array), atol)
            absolute_error = float(np.max(difference))
            relative_error = float(np.max(difference / denominator))
            max_absolute_error = max(max_absolute_error, absolute_error)
            max_relative_error = max(max_relative_error, relative_error)
            if not np.allclose(
                candidate_array,
                reference_array,
                rtol=rtol,
                atol=atol,
            ):
                raise benchmark.BenchmarkError(
                    "fast-path verification failed for "
                    f"{name}: max_abs={absolute_error:.6e}, "
                    f"max_scaled_rel={relative_error:.6e}"
                )
    return {
        "max_absolute_error": max_absolute_error,
        "max_relative_error": max_relative_error,
    }


def _base_implementation(mode: str) -> dict[str, Any]:
    fastpath_path = Path(__file__).with_name("ceridwen_sfh_basis_fastpath.py")
    return {
        "experiment_id": EXPERIMENT_ID,
        "mode": mode,
        "harness_sha256": benchmark._sha256(Path(__file__).resolve()),
        "fastpath_source_sha256": benchmark._sha256(fastpath_path),
        "basis_shape": None,
        "basis_bytes": 0,
        "source_verification": None,
        "prediction_verification": None,
    }


def _install_and_verify(workload: Any, mode: str) -> dict[str, Any]:
    """Install one implementation and prove it matches the dense model."""
    implementation = _base_implementation(mode)
    if mode == "baseline":
        return implementation

    import jax

    if __package__:
        from .ceridwen_sfh_basis_fastpath import (
            install_sfh_basis_fastpath,
            verify_sfh_basis_fastpath,
        )
    else:
        from ceridwen_sfh_basis_fastpath import (
            install_sfh_basis_fastpath,
            verify_sfh_basis_fastpath,
        )

    model = workload.model
    free_thetas = _verification_free_thetas(model)
    references = [
        jax.block_until_ready(model.predict(theta)) for theta in free_thetas
    ]

    state = install_sfh_basis_fastpath(model.csp, mode)
    model_thetas = [model.apply_transforms(theta) for theta in free_thetas]
    source_verification = verify_sfh_basis_fastpath(model.csp, model_thetas)
    candidates = [
        jax.block_until_ready(model.predict(theta)) for theta in free_thetas
    ]
    prediction_verification = _compare_predictions(references, candidates)

    implementation.update(
        {
            "basis_shape": state.basis_shape,
            "basis_bytes": state.basis_bytes,
            "source_verification": source_verification,
            "prediction_verification": prediction_verification,
        }
    )
    return implementation


def _implementation_from_record(record: dict[str, Any]) -> dict[str, Any]:
    return record.get("runtime", {}).get(
        "ceridwen_fastpath",
        {
            "experiment_id": EXPERIMENT_ID,
            "mode": "baseline",
            "basis_shape": None,
            "basis_bytes": 0,
            "source_verification": None,
            "prediction_verification": None,
        },
    )


def command_run(args: argparse.Namespace) -> int:
    """Run the existing fixed benchmark after installing one fast path."""
    original_build = benchmark.build_joint_workload
    original_runtime_metadata = benchmark._runtime_metadata
    original_result_directory_name = benchmark.result_directory_name
    original_flat_result_row = benchmark._flat_result_row
    implementation: dict[str, Any] = {"mode": args.implementation}

    def build_with_implementation(project_root: Path) -> Any:
        nonlocal implementation
        workload = original_build(project_root)
        implementation = _install_and_verify(workload, args.implementation)
        print(
            "implementation: "
            f"{implementation['mode']}, "
            f"basis={implementation['basis_shape']}, "
            f"basis_bytes={implementation['basis_bytes']}",
            flush=True,
        )
        return workload

    def runtime_metadata_with_implementation(jax: Any, device: Any) -> dict[str, Any]:
        metadata = original_runtime_metadata(jax, device)
        metadata["ceridwen_fastpath"] = implementation
        return metadata

    def implementation_result_directory_name(
        gpu_name: str,
        vast_host: str | None,
        date: str,
    ) -> str:
        base_name = original_result_directory_name(gpu_name, vast_host, date)
        return f"{base_name}_implementation_{benchmark._slug(args.implementation)}"

    def flat_result_row_with_implementation(result: dict[str, Any]) -> dict[str, Any]:
        row = original_flat_result_row(result)
        fastpath = _implementation_from_record(result)
        row["implementation"] = fastpath["mode"]
        row["fastpath_basis_bytes"] = fastpath.get("basis_bytes", 0)
        return row

    benchmark.build_joint_workload = build_with_implementation
    benchmark._runtime_metadata = runtime_metadata_with_implementation
    benchmark.result_directory_name = implementation_result_directory_name
    benchmark._flat_result_row = flat_result_row_with_implementation
    try:
        return benchmark.command_run(args)
    finally:
        benchmark.build_joint_workload = original_build
        benchmark._runtime_metadata = original_runtime_metadata
        benchmark.result_directory_name = original_result_directory_name
        benchmark._flat_result_row = original_flat_result_row


def command_summarize(args: argparse.Namespace) -> int:
    paths = benchmark._result_json_paths(args.inputs)
    records = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    ranked = benchmark.rank_records(records)
    rows = []
    for record in ranked:
        row = benchmark._flat_result_row(record)
        fastpath = _implementation_from_record(record)
        row["implementation"] = fastpath["mode"]
        row["fastpath_basis_bytes"] = fastpath.get("basis_bytes", 0)
        rows.append(row)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        benchmark._write_csv(args.output, rows)
        print(f"saved: {args.output}")

    print("rank  implementation  gpu  calls/s  USD/100k  USD/hour  host")
    for rank, row in enumerate(rows, start=1):
        print(
            f"{rank:>4}  {row['implementation']:<20}  {row['gpu_name']}  "
            f"{float(row['likelihood_calls_per_second']):.2f}  "
            f"{float(row['cost_per_100k_likelihood_calls_usd']):.5f}  "
            f"{float(row['price_usd_per_hour']):.3f}  "
            f"{row['vast_host'] or '-'}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark exact low-rank variants of the fixed Ceridwen workload."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run one implementation")
    run_parser.add_argument(
        "--implementation",
        choices=IMPLEMENTATIONS,
        required=True,
    )
    run_parser.add_argument(
        "--project-root",
        type=Path,
        default=PROJECT_ROOT,
    )
    run_parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "results",
    )
    run_parser.add_argument(
        "--price-usd-per-hour",
        type=benchmark._positive_float,
        required=True,
    )
    run_parser.add_argument("--vast-host")
    run_parser.add_argument("--vast-instance")
    run_parser.set_defaults(function=command_run)

    summary_parser = subparsers.add_parser(
        "summarize",
        help="compare baseline and fast-path benchmark results",
    )
    summary_parser.add_argument("inputs", nargs="+", type=Path)
    summary_parser.add_argument("--output", type=Path)
    summary_parser.set_defaults(function=command_summarize)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.function(args))
    except (benchmark.BenchmarkError, AssertionError, ValueError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
