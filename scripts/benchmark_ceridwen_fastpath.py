#!/usr/bin/env python3
"""Benchmark experimental Ceridwen source-spectrum fast paths."""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

if __package__:
    from . import benchmark_ceridwen_vast as baseline
else:
    import benchmark_ceridwen_vast as baseline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "ceridwen_sfh_basis_fastpath_v1"
FASTPATH_MODES = (
    "corners",
    "sfh-basis-sparse",
    "sfh-basis-dense",
)
KERNEL_MODES = ("baseline", *FASTPATH_MODES)


def _probe_free_thetas(model: Any) -> list[dict[str, Any]]:
    """Build deterministic prior-interior probes for numerical verification."""
    import jax.numpy as jnp
    import numpy as np

    csp = model.csp
    initial = {name: jnp.asarray(value) for name, value in model.theta_init.items()}
    z_grid = np.asarray(csp.zmet, dtype=float)
    alpha_grid = np.asarray(csp.afe_grid, dtype=float)
    n_ratio = int(initial["logsfr_ratios"].size)

    probes = [initial]
    settings = (
        (
            0.35 * z_grid[2] + 0.65 * z_grid[3],
            0.4 * alpha_grid[1] + 0.6 * alpha_grid[2],
            np.linspace(-2.5, 2.5, n_ratio),
            0.0,
        ),
        (
            0.7 * z_grid[-2] + 0.3 * z_grid[-1],
            0.2 * alpha_grid[-2] + 0.8 * alpha_grid[-1],
            np.linspace(2.5, -2.5, n_ratio),
            1.7,
        ),
    )
    for metallicity, alpha, ratios, diffuse_tau in settings:
        theta = dict(initial)
        theta["Z"] = jnp.asarray([metallicity])
        theta["afe"] = jnp.asarray([alpha])
        theta["logsfr_ratios"] = jnp.asarray(ratios)
        theta["diffuse_tau_kc"] = jnp.asarray([diffuse_tau])
        probes.append(theta)
    return probes


def _prediction_error(
    reference: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
) -> dict[str, float]:
    """Return scaled prediction errors and reject a scientific mismatch."""
    import numpy as np

    max_absolute_error = 0.0
    max_relative_error = 0.0
    for reference_map, candidate_map in zip(reference, candidate, strict=True):
        if set(reference_map) != set(candidate_map):
            raise AssertionError("fast-path prediction keys differ from the baseline")
        for name in reference_map:
            reference_array = np.asarray(reference_map[name])
            candidate_array = np.asarray(candidate_map[name])
            scale = float(np.max(np.abs(reference_array)))
            atol = max(np.finfo(np.float32).tiny, 1e-7 * scale)
            difference = np.abs(candidate_array - reference_array)
            denominator = np.maximum(np.abs(reference_array), atol)
            scaled_relative = difference / denominator
            max_absolute_error = max(
                max_absolute_error,
                float(np.max(difference)),
            )
            max_relative_error = max(
                max_relative_error,
                float(np.max(scaled_relative)),
            )
            if not np.allclose(
                candidate_array,
                reference_array,
                rtol=5e-5,
                atol=atol,
            ):
                raise AssertionError(
                    f"fast-path {name!r} prediction disagrees with baseline: "
                    f"max_abs={np.max(difference):.6e}, "
                    f"max_scaled_rel={np.max(scaled_relative):.6e}"
                )
    return {
        "max_absolute_error": max_absolute_error,
        "max_relative_error": max_relative_error,
    }


def build_experimental_workload(
    project_root: Path,
    mode: str,
) -> tuple[baseline.BuiltWorkload, dict[str, Any]]:
    """Build the unchanged workload, then install and verify one fast path."""
    import jax

    if mode not in KERNEL_MODES:
        raise baseline.BenchmarkError(f"unsupported CSP kernel mode: {mode!r}")

    workload = baseline.build_joint_workload(project_root)
    implementation: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "csp_kernel": mode,
        "basis_shape": None,
        "basis_bytes": 0,
        "source_verification": None,
        "prediction_verification": None,
    }
    if mode == "baseline":
        return workload, implementation

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
    free_probes = _probe_free_thetas(model)
    baseline_predictions = [
        jax.block_until_ready(model.predict(theta)) for theta in free_probes
    ]
    model_probes = [model.apply_transforms(theta) for theta in free_probes]

    state = install_sfh_basis_fastpath(model.csp, mode)
    source_verification = verify_sfh_basis_fastpath(model.csp, model_probes)
    candidate_predictions = [
        jax.block_until_ready(model.predict(theta)) for theta in free_probes
    ]
    prediction_verification = _prediction_error(
        baseline_predictions,
        candidate_predictions,
    )

    implementation.update(
        {
            "basis_shape": state.basis_shape,
            "basis_bytes": state.basis_bytes,
            "source_verification": source_verification,
            "prediction_verification": prediction_verification,
        }
    )
    return workload, implementation


def result_directory_name(
    gpu_name: str,
    vast_host: str | None,
    mode: str,
    date: str,
) -> str:
    hardware = baseline._slug(gpu_name.removeprefix("NVIDIA "))
    host = f"_host_{baseline._slug(vast_host)}" if vast_host else ""
    kernel = baseline._slug(mode)
    return (
        f"ceridwen_{kernel}_{hardware}{host}_"
        f"joint_full_benchmark_complete_{date}"
    )


def _flat_result_row(result: dict[str, Any]) -> dict[str, Any]:
    row = baseline._flat_result_row(result)
    implementation = result["implementation"]
    return {
        "csp_kernel": implementation["csp_kernel"],
        "basis_bytes": implementation["basis_bytes"],
        **row,
    }


def command_run(args: argparse.Namespace) -> int:
    baseline._configure_cuda_environment()

    import jax

    jax.config.update("jax_enable_x64", True)
    devices = jax.devices()
    if not devices or any(device.platform != "gpu" for device in devices):
        raise baseline.BenchmarkError(f"expected CUDA GPU devices, found {devices}")
    device = devices[0]
    print(f"device: {getattr(device, 'device_kind', device)}")
    print(f"workload: {baseline.WORKLOAD_ID}")
    print(f"CSP kernel: {args.csp_kernel}")

    project_root = args.project_root.resolve()
    started_at = datetime.now(UTC)
    setup_start = time.perf_counter()
    workload, implementation = build_experimental_workload(
        project_root,
        args.csp_kernel,
    )
    input_sha256 = {
        name: baseline._sha256(path) for name, path in workload.input_paths.items()
    }
    git = baseline._git_metadata(project_root)
    setup_seconds = time.perf_counter() - setup_start
    print(
        "validated workload: "
        f"{workload.metadata['photometric_bands']} bands, "
        f"{workload.metadata['spectral_pixels']} spectral pixels"
    )
    if implementation["source_verification"] is not None:
        print(
            "verified source spectrum: max scaled relative error "
            f"{implementation['source_verification']['max_relative_error']:.3e}"
        )
        print(
            "verified projected predictions: max scaled relative error "
            f"{implementation['prediction_verification']['max_relative_error']:.3e}"
        )
        print(
            "precontracted basis: "
            f"shape={implementation['basis_shape']}, "
            f"bytes={implementation['basis_bytes']}"
        )

    raw_timings = baseline.run_fixed_steps(workload)
    metrics = baseline.calculate_metrics(
        raw_timings["iteration_seconds"],
        baseline.CALLS_PER_STEP,
        args.price_usd_per_hour,
    )
    timings = {
        "setup_seconds": setup_seconds,
        "initialization_seconds": raw_timings["initialization_seconds"],
        "warmup_step_seconds": raw_timings["warmup_step_seconds"],
        **metrics,
    }
    runtime = baseline._runtime_metadata(jax, device)
    contract = {
        "id": baseline.WORKLOAD_ID,
        **workload.metadata,
        "seed": baseline.SEED,
        "num_live": baseline.NUM_LIVE,
        "num_inner_steps": baseline.NUM_INNER_STEPS,
        "num_delete": baseline.NUM_DELETE,
        "reference_logZ_tol": baseline.REFERENCE_LOGZ_TOL,
        "warmup_steps": baseline.WARMUP_STEPS,
        "timed_steps": baseline.TIMED_STEPS,
        "likelihood_calls_per_step": baseline.CALLS_PER_STEP,
    }
    completed_at = datetime.now(UTC)
    result = {
        "schema_version": baseline.RESULT_SCHEMA_VERSION,
        "started_at_utc": started_at.isoformat(),
        "completed_at_utc": completed_at.isoformat(),
        "workload": contract,
        "comparison_fingerprint": baseline._comparison_fingerprint(
            contract,
            input_sha256,
            git["ceridwen_commit"],
            runtime,
        ),
        "benchmark_script_sha256": baseline._sha256(Path(__file__).resolve()),
        "input_sha256": input_sha256,
        "input_paths": {
            name: str(path.resolve()) for name, path in workload.input_paths.items()
        },
        "git": git,
        "runtime": runtime,
        "memory": {
            "jax": baseline._jax_memory(device),
            "nvidia_process_memory_mib": baseline._nvidia_process_memory_mib(),
        },
        "vast": {
            "host": args.vast_host,
            "instance": args.vast_instance,
            "price_usd_per_hour": args.price_usd_per_hour,
        },
        "implementation": implementation,
        "timings": timings,
    }

    result_name = result_directory_name(
        runtime["jax_device_kind"],
        args.vast_host,
        args.csp_kernel,
        started_at.date().isoformat(),
    )
    result_dir = args.output_root.resolve() / result_name
    if result_dir.exists():
        raise baseline.BenchmarkError(f"result directory already exists: {result_dir}")
    result_dir.mkdir(parents=True)
    json_path = result_dir / "benchmark.json"
    csv_path = result_dir / "benchmark.csv"
    log_path = result_dir / "benchmark.log"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    baseline._write_csv(csv_path, [_flat_result_row(result)])
    log_lines = [
        f"experiment: {EXPERIMENT_ID}",
        f"workload: {baseline.WORKLOAD_ID}",
        f"CSP kernel: {args.csp_kernel}",
        f"device: {runtime['jax_device_kind']}",
        f"timed likelihood calls: {timings['timed_likelihood_calls']}",
        f"timed wall: {timings['total_timed_seconds']:.3f} s",
        f"throughput: {timings['likelihood_calls_per_second']:.3f} calls/s",
        (
            "cost per 100000 calls: "
            f"${timings['cost_per_100k_likelihood_calls_usd']:.6f}"
        ),
        f"comparison fingerprint: {result['comparison_fingerprint']}",
    ]
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(log_lines[5])
    print(log_lines[6])
    print(log_lines[7])
    print(f"saved: {result_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the fixed Ceridwen GPU benchmark with an experimental "
            "source-spectrum kernel."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=PROJECT_ROOT,
        help="Project checkout. Default: the checkout containing this script.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "results",
        help="Parent directory for benchmark results.",
    )
    parser.add_argument(
        "--csp-kernel",
        choices=KERNEL_MODES,
        default="sfh-basis-sparse",
        help="Source-spectrum implementation to benchmark.",
    )
    parser.add_argument(
        "--price-usd-per-hour",
        type=baseline._positive_float,
        required=True,
        help="Current Vast offer price in USD per hour.",
    )
    parser.add_argument("--vast-host", help="Vast host ID.")
    parser.add_argument("--vast-instance", help="Vast instance ID.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return command_run(args)
    except (baseline.BenchmarkError, AssertionError, ValueError) as error:
        parser.error(str(error))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
