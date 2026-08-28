#!/usr/bin/env python3
"""Run and compare converged baseline and SFH-fast-path Ceridwen posteriors."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scripts import benchmark_ceridwen_vast as benchmark
except ModuleNotFoundError:
    import benchmark_ceridwen_vast as benchmark

DEFAULT_SEED = 20260812
NUM_LIVE = 300
NUM_INNER_STEPS = 40
NUM_DELETE = 25
LOGZ_TOL = -3.0
MIN_WEIGHT_ESS = 200.0
MAX_EVIDENCE_SIGMA = 3.0
MAX_MEAN_SHIFT_SD = 0.20
MAX_MEDIAN_SHIFT_SD = 0.20
MAX_QUANTILE_SHIFT_WIDTH = 0.20
MAX_WASSERSTEIN_SD = 0.20
QUANTILES = (0.16, 0.50, 0.84)


class VerificationError(RuntimeError):
    """Report an invalid run or a failed comparison contract."""


def normalized_weights(log_weights: Any) -> np.ndarray:
    values = np.asarray(log_weights, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise VerificationError("log weights must be a finite one-dimensional array")
    shifted = values - np.max(values)
    weights = np.exp(shifted)
    total = np.sum(weights)
    if not np.isfinite(total) or total <= 0:
        raise VerificationError("log weights cannot be normalized")
    return weights / total


def weighted_quantiles(values: Any, weights: Any) -> np.ndarray:
    samples = np.asarray(values, dtype=float)
    probabilities = np.asarray(weights, dtype=float)
    order = np.argsort(samples)
    ordered = samples[order]
    cumulative = np.cumsum(probabilities[order])
    cumulative /= cumulative[-1]
    return np.interp(QUANTILES, cumulative, ordered)


def weighted_summary(values: Any, weights: Any) -> dict[str, Any]:
    samples = np.asarray(values, dtype=float)
    probabilities = np.asarray(weights, dtype=float)
    mean = float(np.sum(probabilities * samples))
    variance = float(np.sum(probabilities * (samples - mean) ** 2))
    quantiles = weighted_quantiles(samples, probabilities)
    return {
        "mean": mean,
        "standard_deviation": math.sqrt(max(variance, 0.0)),
        "q16": float(quantiles[0]),
        "median": float(quantiles[1]),
        "q84": float(quantiles[2]),
    }


def compare_component(
    baseline_values: Any,
    baseline_weights: Any,
    fastpath_values: Any,
    fastpath_weights: Any,
) -> dict[str, Any]:
    from scipy.stats import wasserstein_distance

    baseline = weighted_summary(baseline_values, baseline_weights)
    fastpath = weighted_summary(fastpath_values, fastpath_weights)
    pooled_sd = math.sqrt(
        0.5
        * (
            baseline["standard_deviation"] ** 2
            + fastpath["standard_deviation"] ** 2
        )
    )
    pooled_width = 0.5 * (
        baseline["q84"]
        - baseline["q16"]
        + fastpath["q84"]
        - fastpath["q16"]
    )
    if pooled_sd <= 0 or pooled_width <= 0:
        raise VerificationError("a posterior component has zero comparison scale")
    quantile_shifts = [
        abs(baseline[name] - fastpath[name]) / pooled_width
        for name in ("q16", "median", "q84")
    ]
    metrics = {
        "mean_shift_pooled_sd": abs(baseline["mean"] - fastpath["mean"])
        / pooled_sd,
        "median_shift_pooled_sd": abs(
            baseline["median"] - fastpath["median"]
        )
        / pooled_sd,
        "max_quantile_shift_central_width": max(quantile_shifts),
        "wasserstein_pooled_sd": wasserstein_distance(
            np.asarray(baseline_values, dtype=float),
            np.asarray(fastpath_values, dtype=float),
            u_weights=np.asarray(baseline_weights, dtype=float),
            v_weights=np.asarray(fastpath_weights, dtype=float),
        )
        / pooled_sd,
    }
    passed = bool(
        metrics["mean_shift_pooled_sd"] <= MAX_MEAN_SHIFT_SD
        and metrics["median_shift_pooled_sd"] <= MAX_MEDIAN_SHIFT_SD
        and metrics["max_quantile_shift_central_width"]
        <= MAX_QUANTILE_SHIFT_WIDTH
        and metrics["wasserstein_pooled_sd"] <= MAX_WASSERSTEIN_SD
    )
    return {
        "baseline": baseline,
        "fastpath_a": fastpath,
        **metrics,
        "passed": passed,
    }


def _science_contract(workload: Any) -> dict[str, Any]:
    git = benchmark._git_metadata(Path(__file__).resolve().parents[1])
    return {
        "workload": workload.metadata,
        "lookback_time_gyr": (
            np.asarray(workload.model.csp.sfh_times, dtype=float) / 1e9
        ).tolist(),
        "input_files": {
            name: {
                "name": path.name,
                "size_bytes": path.stat().st_size,
            }
            for name, path in workload.input_paths.items()
        },
        "sampler": {
            "name": "blackjax.nss",
            "num_live": NUM_LIVE,
            "num_inner_steps": NUM_INNER_STEPS,
            "num_delete": NUM_DELETE,
            "logZ_tol": LOGZ_TOL,
        },
        "precision": "highest",
        "project_commit": os.environ.get(
            "CERIDWEN_PROJECT_COMMIT", git["project_commit"]
        ),
        "ceridwen_commit": os.environ.get(
            "CERIDWEN_SOURCE_COMMIT", git["ceridwen_commit"]
        ),
    }


def command_run(args: argparse.Namespace) -> int:
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        raise VerificationError(f"output directory already exists: {output_dir}")

    benchmark._configure_cuda_environment()
    import blackjax
    import jax
    import jaxlib
    from ceridwen.fit import load_result_h5, write_result_h5
    from ceridwen.sampler import run_sampler
    from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter

    import ceridwen

    jax.config.update("jax_enable_x64", True)
    devices = jax.devices()
    if len(devices) != 1 or devices[0].platform != "gpu":
        raise VerificationError(f"expected one CUDA GPU, found {devices}")

    output_dir.mkdir(parents=True)
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir()
    started_at = datetime.now(UTC)
    workload = benchmark.build_joint_workload(args.project_root.resolve())
    implementation = benchmark.select_sfh_basis_implementation(
        workload,
        args.sfh_basis_fastpath,
    )
    runtime = {
        "python": sys.version.split()[0],
        "jax": jax.__version__,
        "jaxlib": jaxlib.__version__,
        "blackjax": getattr(blackjax, "__version__", None),
        "ceridwen": getattr(ceridwen, "__version__", None),
        "device": getattr(devices[0], "device_kind", str(devices[0])),
        "jax_enable_x64": bool(jax.config.jax_enable_x64),
    }
    contract = _science_contract(workload)
    adapter = BlackJAXNestedSamplerAdapter(
        priors=workload.model.priors,
        num_live=NUM_LIVE,
        num_inner_steps=NUM_INNER_STEPS,
        num_delete=NUM_DELETE,
        logZ_tol=LOGZ_TOL,
        checkpoint_interval_s=600.0,
        checkpoint_dir=str(checkpoint_dir),
        verbose=True,
    )
    result = run_sampler(
        workload.model,
        workload.likelihood,
        adapter,
        jax.random.PRNGKey(args.seed),
    )
    result_path = output_dir / "ceridwen_result.h5"
    write_result_h5(result_path, workload.model, result)
    saved = load_result_h5(result_path)
    if saved.param_names != result.param_names:
        raise VerificationError("saved parameter names do not match the fit")
    if saved.log_likelihoods.shape != result.log_likelihoods.shape:
        raise VerificationError("saved likelihood array does not match the fit")

    weights = normalized_weights(saved.log_weights)
    manifest = {
        "schema_version": 1,
        "status": "complete",
        "seed": args.seed,
        "started_at_utc": started_at.isoformat(),
        "completed_at_utc": datetime.now(UTC).isoformat(),
        "implementation": implementation,
        "science_contract": contract,
        "runtime": {
            **runtime,
            "vast_instance_id": os.environ.get("CONTAINER_ID"),
            "vast_host_id": os.environ.get("VAST_HOST_ID"),
        },
        "result": {
            "path": result_path.name,
            "param_names": saved.param_names,
            "log_evidence": saved.log_evidence,
            "log_evidence_err": saved.log_evidence_err,
            "n_likelihood_calls": saved.n_likelihood_calls,
            "wall_time_s": saved.wall_time_s,
            "n_samples": int(saved.log_likelihoods.size),
            "posterior_weight_ess": float(1.0 / np.sum(weights**2)),
        },
    }
    (output_dir / "run.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"saved converged run: {output_dir}")
    return 0


def _load_run(path: Path, expected_implementation: str) -> tuple[Any, dict[str, Any]]:
    from ceridwen.fit import load_result_h5

    manifest_path = path / "run.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "complete":
        raise VerificationError(f"run is not complete: {path}")
    if manifest.get("implementation", {}).get("sfh_basis_fastpath") != (
        expected_implementation
    ):
        raise VerificationError(f"unexpected implementation in {path}")
    result_path = path / manifest["result"]["path"]
    if not result_path.is_file():
        raise VerificationError(f"result file is missing: {result_path}")
    return load_result_h5(result_path), manifest


def command_compare(args: argparse.Namespace) -> int:
    baseline, baseline_manifest = _load_run(args.baseline_dir.resolve(), "baseline")
    fastpath, fastpath_manifest = _load_run(args.fastpath_dir.resolve(), "A")
    if baseline_manifest["science_contract"] != fastpath_manifest["science_contract"]:
        raise VerificationError("the converged run contracts do not match")
    if baseline.param_names != fastpath.param_names:
        raise VerificationError("the converged runs returned different parameters")

    baseline_weights = normalized_weights(baseline.log_weights)
    fastpath_weights = normalized_weights(fastpath.log_weights)
    baseline_ess = float(1.0 / np.sum(baseline_weights**2))
    fastpath_ess = float(1.0 / np.sum(fastpath_weights**2))

    evidence_scale = math.hypot(
        baseline.log_evidence_err,
        fastpath.log_evidence_err,
    )
    if not np.isfinite(evidence_scale) or evidence_scale <= 0:
        raise VerificationError("the evidence uncertainties are not finite")
    evidence_sigma = abs(baseline.log_evidence - fastpath.log_evidence) / evidence_scale

    components = []
    for name in baseline.param_names:
        baseline_values = np.asarray(baseline.samples[name]).reshape(
            baseline_weights.size,
            -1,
        )
        fastpath_values = np.asarray(fastpath.samples[name]).reshape(
            fastpath_weights.size,
            -1,
        )
        if baseline_values.shape[1] != fastpath_values.shape[1]:
            raise VerificationError(f"parameter shape differs: {name}")
        for index in range(baseline_values.shape[1]):
            label = name if baseline_values.shape[1] == 1 else f"{name}[{index}]"
            components.append(
                {
                    "parameter": label,
                    **compare_component(
                        baseline_values[:, index],
                        baseline_weights,
                        fastpath_values[:, index],
                        fastpath_weights,
                    ),
                }
            )

    thresholds = {
        "minimum_posterior_weight_ess": MIN_WEIGHT_ESS,
        "maximum_evidence_difference_sigma": MAX_EVIDENCE_SIGMA,
        "maximum_mean_shift_pooled_sd": MAX_MEAN_SHIFT_SD,
        "maximum_median_shift_pooled_sd": MAX_MEDIAN_SHIFT_SD,
        "maximum_quantile_shift_central_width": MAX_QUANTILE_SHIFT_WIDTH,
        "maximum_wasserstein_pooled_sd": MAX_WASSERSTEIN_SD,
    }
    passed = (
        baseline_ess >= MIN_WEIGHT_ESS
        and fastpath_ess >= MIN_WEIGHT_ESS
        and evidence_sigma <= MAX_EVIDENCE_SIGMA
        and all(component["passed"] for component in components)
    )
    comparison = {
        "schema_version": 1,
        "status": "passed" if passed else "failed",
        "scope": "matched_converged_nss_weighted_posterior_equivalence",
        "science_contract": baseline_manifest["science_contract"],
        "thresholds_declared_before_runs": thresholds,
        "baseline": {
            **baseline_manifest["result"],
            "posterior_weight_ess": baseline_ess,
        },
        "fastpath_a": {
            **fastpath_manifest["result"],
            "posterior_weight_ess": fastpath_ess,
        },
        "evidence": {
            "absolute_log_evidence_difference": abs(
                baseline.log_evidence - fastpath.log_evidence
            ),
            "combined_uncertainty": evidence_scale,
            "difference_sigma": evidence_sigma,
            "passed": evidence_sigma <= MAX_EVIDENCE_SIGMA,
        },
        "parameters": components,
        "all_returned_parameters_passed": all(
            component["passed"] for component in components
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    csv_path = args.output.with_suffix(".csv")
    rows = [
        {
            "parameter": item["parameter"],
            "baseline_median": item["baseline"]["median"],
            "fastpath_a_median": item["fastpath_a"]["median"],
            "mean_shift_pooled_sd": item["mean_shift_pooled_sd"],
            "median_shift_pooled_sd": item["median_shift_pooled_sd"],
            "max_quantile_shift_central_width": item[
                "max_quantile_shift_central_width"
            ],
            "wasserstein_pooled_sd": item["wasserstein_pooled_sd"],
            "passed": item["passed"],
        }
        for item in components
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"posterior equivalence: {comparison['status']}")
    print(f"saved: {args.output}")
    return 0 if passed else 1


def posterior_components(result: Any, science_contract: dict[str, Any]) -> dict[str, np.ndarray]:
    """Return direct and derived posterior components on aligned dead points."""
    components: dict[str, np.ndarray] = {}
    sample_count = np.asarray(result.log_weights).size
    for name in result.param_names:
        values = np.asarray(result.samples[name]).reshape(sample_count, -1)
        for index in range(values.shape[1]):
            label = name if values.shape[1] == 1 else f"{name}[{index}]"
            components[label] = values[:, index]

    if "logsfr_ratios" not in result.samples:
        return components

    import jax
    import jax.numpy as jnp
    from ceridwen.model import logsfr_ratios_to_sfh

    lookback_gyr = np.asarray(science_contract["lookback_time_gyr"], dtype=float)
    lookback_yr = jnp.asarray(lookback_gyr * 1e9)
    ratios = jnp.asarray(result.samples["logsfr_ratios"])
    histories = np.asarray(
        jax.vmap(
            lambda value: logsfr_ratios_to_sfh(
                value,
                sfh_times_yr=lookback_yr,
            )
        )(ratios)
    )
    durations_yr = np.diff(lookback_gyr) * 1e9
    interval_masses = 0.5 * (
        histories[:, :-1] + histories[:, 1:]
    ) * durations_yr
    total_mass = interval_masses.sum(axis=1)
    mass_fractions = interval_masses / total_mass[:, None]
    interval_age_gyr = 0.5 * (lookback_gyr[:-1] + lookback_gyr[1:])
    components["mass_weighted_age_gyr"] = (
        interval_masses * interval_age_gyr
    ).sum(axis=1) / total_mass
    for index in range(mass_fractions.shape[1]):
        components[f"formed_mass_fraction[{index}]"] = mass_fractions[:, index]
    return components


def compare_runs(
    left: tuple[Any, dict[str, Any]],
    right: tuple[Any, dict[str, Any]],
) -> dict[str, Any]:
    """Compare two converged weighted posteriors with one science contract."""
    left_result, left_manifest = left
    right_result, right_manifest = right
    if left_manifest["science_contract"] != right_manifest["science_contract"]:
        raise VerificationError("the converged run contracts do not match")

    left_weights = normalized_weights(left_result.log_weights)
    right_weights = normalized_weights(right_result.log_weights)
    left_components = posterior_components(
        left_result,
        left_manifest["science_contract"],
    )
    right_components = posterior_components(
        right_result,
        right_manifest["science_contract"],
    )
    if left_components.keys() != right_components.keys():
        raise VerificationError("the converged runs returned different components")

    evidence_scale = math.hypot(
        left_result.log_evidence_err,
        right_result.log_evidence_err,
    )
    if not np.isfinite(evidence_scale) or evidence_scale <= 0:
        raise VerificationError("the evidence uncertainties are not finite")

    parameters = []
    for label in left_components:
        comparison = compare_component(
            left_components[label],
            left_weights,
            right_components[label],
            right_weights,
        )
        parameters.append(
            {
                "parameter": label,
                "left": comparison.pop("baseline"),
                "right": comparison.pop("fastpath_a"),
                **comparison,
            }
        )

    return {
        "left_seed": left_manifest["seed"],
        "right_seed": right_manifest["seed"],
        "left_implementation": left_manifest["implementation"][
            "sfh_basis_fastpath"
        ],
        "right_implementation": right_manifest["implementation"][
            "sfh_basis_fastpath"
        ],
        "evidence": {
            "absolute_log_evidence_difference": abs(
                left_result.log_evidence - right_result.log_evidence
            ),
            "combined_uncertainty": evidence_scale,
            "difference_sigma": abs(
                left_result.log_evidence - right_result.log_evidence
            )
            / evidence_scale,
        },
        "parameters": parameters,
    }


def _empirical_envelope(
    default_pairs: list[dict[str, Any]],
    matched_pairs: list[dict[str, Any]],
) -> dict[str, Any]:
    metric_names = (
        "mean_shift_pooled_sd",
        "median_shift_pooled_sd",
        "max_quantile_shift_central_width",
        "wasserstein_pooled_sd",
    )

    def summarize(default_values: list[float], fast_values: list[float]) -> dict[str, Any]:
        maximum = float(np.max(default_values))
        return {
            "default_min": float(np.min(default_values)),
            "default_median": float(np.median(default_values)),
            "default_max": maximum,
            "fast_default_values": [float(value) for value in fast_values],
            "fast_inside_default_max": [
                bool(value <= maximum) for value in fast_values
            ],
        }

    envelope: dict[str, Any] = {"evidence": {}, "parameters": {}}
    for metric in ("absolute_log_evidence_difference", "difference_sigma"):
        envelope["evidence"][metric] = summarize(
            [pair["evidence"][metric] for pair in default_pairs],
            [pair["evidence"][metric] for pair in matched_pairs],
        )

    labels = [item["parameter"] for item in default_pairs[0]["parameters"]]
    for index, label in enumerate(labels):
        envelope["parameters"][label] = {}
        for metric in metric_names:
            envelope["parameters"][label][metric] = summarize(
                [pair["parameters"][index][metric] for pair in default_pairs],
                [pair["parameters"][index][metric] for pair in matched_pairs],
            )
    return envelope


def _run_summary(run: tuple[Any, dict[str, Any]]) -> dict[str, Any]:
    result, manifest = run
    weights = normalized_weights(result.log_weights)
    return {
        "seed": manifest["seed"],
        "implementation": manifest["implementation"]["sfh_basis_fastpath"],
        "runtime": manifest["runtime"],
        **manifest["result"],
        "posterior_weight_ess": float(1.0 / np.sum(weights**2)),
    }


def command_compare_ensemble(args: argparse.Namespace) -> int:
    """Compare four default runs with four seed-matched fast-path runs."""
    baseline_runs = [
        _load_run(path.resolve(), "baseline") for path in args.baseline_dir
    ]
    fastpath_runs = [_load_run(path.resolve(), "A") for path in args.fastpath_dir]
    if len(baseline_runs) < 2 or len(fastpath_runs) < 2:
        raise VerificationError("ensemble comparison requires at least two runs per group")

    baseline_by_seed = {run[1]["seed"]: run for run in baseline_runs}
    fastpath_by_seed = {run[1]["seed"]: run for run in fastpath_runs}
    if len(baseline_by_seed) != len(baseline_runs):
        raise VerificationError("baseline seeds must be unique")
    if len(fastpath_by_seed) != len(fastpath_runs):
        raise VerificationError("fast-path seeds must be unique")
    if baseline_by_seed.keys() != fastpath_by_seed.keys():
        raise VerificationError("baseline and fast-path seed sets must match")

    seeds = sorted(baseline_by_seed)
    default_pairs = [
        compare_runs(baseline_by_seed[left], baseline_by_seed[right])
        for position, left in enumerate(seeds)
        for right in seeds[position + 1 :]
    ]
    matched_pairs = [
        compare_runs(baseline_by_seed[seed], fastpath_by_seed[seed])
        for seed in seeds
    ]
    all_cross_pairs = [
        compare_runs(baseline_by_seed[left], fastpath_by_seed[right])
        for left in seeds
        for right in seeds
    ]

    comparison = {
        "schema_version": 2,
        "status": "complete",
        "scope": "nss_default_variation_vs_fastpath_variation",
        "science_contract": baseline_runs[0][1]["science_contract"],
        "baseline_runs": [_run_summary(run) for run in baseline_runs],
        "fastpath_runs": [_run_summary(run) for run in fastpath_runs],
        "comparisons": {
            "default_default": default_pairs,
            "matched_fast_default": matched_pairs,
            "all_fast_default": all_cross_pairs,
        },
        "empirical_default_envelopes": _empirical_envelope(
            default_pairs,
            matched_pairs,
        ),
    }

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / "comparison.json"
    output_json.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")

    rows = []
    for pair_type, pairs in comparison["comparisons"].items():
        for pair in pairs:
            for parameter in pair["parameters"]:
                rows.append(
                    {
                        "pair_type": pair_type,
                        "left_seed": pair["left_seed"],
                        "right_seed": pair["right_seed"],
                        "parameter": parameter["parameter"],
                        "mean_shift_pooled_sd": parameter[
                            "mean_shift_pooled_sd"
                        ],
                        "median_shift_pooled_sd": parameter[
                            "median_shift_pooled_sd"
                        ],
                        "max_quantile_shift_central_width": parameter[
                            "max_quantile_shift_central_width"
                        ],
                        "wasserstein_pooled_sd": parameter[
                            "wasserstein_pooled_sd"
                        ],
                    }
                )
    output_csv = output_dir / "comparison.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"saved ensemble comparison: {output_json}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run one converged NSS fit")
    run_parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    run_parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    run_parser.add_argument(
        "--sfh-basis-fastpath",
        choices=("baseline", "A"),
        required=True,
    )
    run_parser.add_argument("--output-dir", type=Path, required=True)
    run_parser.set_defaults(function=command_run)

    compare_parser = subparsers.add_parser(
        "compare",
        help="compare two weighted converged posteriors",
    )
    compare_parser.add_argument("--baseline-dir", type=Path, required=True)
    compare_parser.add_argument("--fastpath-dir", type=Path, required=True)
    compare_parser.add_argument("--output", type=Path, required=True)
    compare_parser.set_defaults(function=command_compare)

    ensemble_parser = subparsers.add_parser(
        "compare-ensemble",
        help="compare repeated default and fast-path weighted posteriors",
    )
    ensemble_parser.add_argument(
        "--baseline-dir",
        type=Path,
        action="append",
        required=True,
    )
    ensemble_parser.add_argument(
        "--fastpath-dir",
        type=Path,
        action="append",
        required=True,
    )
    ensemble_parser.add_argument("--output-dir", type=Path, required=True)
    ensemble_parser.set_defaults(function=command_compare_ensemble)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.function(args)


if __name__ == "__main__":
    raise SystemExit(main())
