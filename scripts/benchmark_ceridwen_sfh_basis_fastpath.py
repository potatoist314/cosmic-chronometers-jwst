#!/usr/bin/env python3
"""Verify and benchmark experimental Ceridwen SFH-basis implementations."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
import sys
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from scripts import benchmark_ceridwen_vast as vast_benchmark

SEED = 20260827
IMPLEMENTATIONS = ("baseline", "variant_a", "variant_b")
DEFAULT_RANDOM_POINTS = 4
DEFAULT_WARMUP_CALLS = 1
DEFAULT_TIMED_CALLS = 5
FORBIDDEN_EXPANSION = (13, 107, 10992)
PREDICTION_RTOL = 5.0e-5
PREDICTION_ATOL = 1.0e-12
LOGLIKE_RTOL = 1.0e-4
LOGLIKE_ATOL = 1.0e-5


class BenchmarkError(RuntimeError):
    """Report an invalid experimental benchmark or comparison."""


@dataclass(frozen=True)
class Evaluation:
    """Store predictions and a full multi-observation log likelihood."""

    label: str
    predictions: dict[str, np.ndarray]
    log_likelihood: float


def _git_commit(repository: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def require_ceridwen_commit(ceridwen_root: Path, expected_commit: str) -> str:
    """Require the explicitly selected local Ceridwen source revision."""
    commit = _git_commit(ceridwen_root)
    if commit != expected_commit:
        raise BenchmarkError(
            f"expected Ceridwen commit {expected_commit}, found {commit}"
        )
    return commit


def _sha256_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def comparison_contract(
    *,
    implementation: str,
    ceridwen_commit: str,
    workload: Mapping[str, Any],
    runtime: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a fingerprint whose only implementation-specific field is named."""
    if implementation not in IMPLEMENTATIONS:
        raise BenchmarkError(f"unknown implementation: {implementation}")
    return {
        "implementation": implementation,
        "ceridwen_commit": ceridwen_commit,
        "seed": SEED,
        "workload": dict(workload),
        "runtime": dict(runtime),
    }


def normalized_fingerprint(contract: Mapping[str, Any]) -> str:
    payload = dict(contract)
    payload.pop("implementation", None)
    return _sha256_json(payload)


def require_comparable_contracts(contracts: Iterable[Mapping[str, Any]]) -> None:
    contracts = list(contracts)
    implementations = [contract.get("implementation") for contract in contracts]
    if implementations != list(IMPLEMENTATIONS):
        raise BenchmarkError(
            "contracts must be ordered baseline, variant_a, variant_b"
        )
    fingerprints = {normalized_fingerprint(contract) for contract in contracts}
    if len(fingerprints) != 1:
        raise BenchmarkError(
            "benchmark fingerprints differ in fields other than implementation"
        )


def timing_metrics(durations: Iterable[float]) -> dict[str, Any]:
    values = [float(value) for value in durations]
    if not values or any(value <= 0.0 for value in values):
        raise BenchmarkError("timed call durations must be positive")
    quartiles = statistics.quantiles(values, n=4, method="inclusive")
    return {
        "call_seconds": values,
        "calls": len(values),
        "total_seconds": sum(values),
        "calls_per_second": len(values) / sum(values),
        "median_step_seconds": statistics.median(values),
        "iqr_step_seconds": quartiles[2] - quartiles[0],
    }


def _shape_text(shape: tuple[int, ...]) -> str:
    return "x".join(str(size) for size in shape)


def stablehlo_evidence(
    stablehlo: str,
    forbidden_shape: tuple[int, ...] = FORBIDDEN_EXPANSION,
) -> dict[str, Any]:
    compact = "".join(stablehlo.split())
    shape_text = _shape_text(forbidden_shape)
    token = f"tensor<{shape_text}x"
    matching_lines = [
        line.strip()[:240]
        for line in stablehlo.splitlines()
        if shape_text in "".join(line.split())
    ]
    return {
        "dialect": "stablehlo",
        "forbidden_expansion_shape": list(forbidden_shape),
        "forbidden_expansion_occurrences": compact.count(token),
        "forbidden_expansion_lines": matching_lines[:8],
        "omits_forbidden_expansion": token not in compact,
        "stablehlo_sha256": hashlib.sha256(stablehlo.encode()).hexdigest(),
    }


def _memory_metadata(device: Any) -> dict[str, float | None]:
    stats = device.memory_stats() or {}

    def to_mib(name: str) -> float | None:
        value = stats.get(name)
        return None if value is None else float(value) / 2**20

    return {
        "bytes_in_use_mib": to_mib("bytes_in_use"),
        "peak_bytes_in_use_mib": to_mib("peak_bytes_in_use"),
        "bytes_limit_mib": to_mib("bytes_limit"),
    }


def install_implementation(csp: Any, implementation: str) -> list[int]:
    """Select one implementation supplied by the pinned core-fastpath commit."""
    selector = {"baseline": None, "variant_a": "A", "variant_b": "B"}.get(
        implementation
    )
    if implementation not in IMPLEMENTATIONS:
        raise BenchmarkError(f"unknown implementation: {implementation}")
    if not hasattr(csp, "select_sfh_basis_fastpath"):
        raise BenchmarkError(
            "the pinned Ceridwen commit does not expose the SFH-basis selector"
        )
    csp.select_sfh_basis_fastpath(selector)
    if implementation == "baseline":
        return list(csp.flux.shape)
    if implementation == "variant_a":
        return list(csp._sfh_basis.shape)
    return list(csp._sfh_basis_flat.shape)


def _copy_theta(theta: Mapping[str, Any]) -> dict[str, Any]:
    import jax.numpy as jnp

    return {name: jnp.array(value) for name, value in theta.items()}


def deterministic_prior_points(model: Any, count: int, seed: int = SEED) -> list[Any]:
    import jax

    if count <= 0:
        raise BenchmarkError("random point count must be positive")
    keys = jax.random.split(jax.random.PRNGKey(seed), count)
    points = []
    for key in keys:
        point = {}
        for name, initial_value in model.theta_init.items():
            key, subkey = jax.random.split(key)
            point[name] = model.priors[name].sample(subkey, shape=initial_value.shape)
        points.append(point)
    return points


def edge_points(model: Any) -> list[tuple[str, dict[str, Any]]]:
    """Return initialization and documented prior-boundary cases."""
    import jax.numpy as jnp

    initial = _copy_theta(model.theta_init)
    lower = _copy_theta(model.theta_init)
    upper = _copy_theta(model.theta_init)
    for name, value in initial.items():
        prior = model.priors[name]
        bounds = getattr(prior, "bounds", None)
        if callable(bounds):
            bounds = bounds()
        if bounds is None:
            continue
        low, high = bounds
        if bool(jnp.all(jnp.isfinite(low))):
            lower[name] = jnp.broadcast_to(jnp.asarray(low), value.shape)
        if bool(jnp.all(jnp.isfinite(high))):
            upper[name] = jnp.broadcast_to(jnp.asarray(high), value.shape)
    return [("initial", initial), ("lower_edges", lower), ("upper_edges", upper)]


def evaluate(model: Any, likelihood: Any, label: str, theta: Any) -> Evaluation:
    import jax

    loglike_fn, _ = vast_benchmark._make_log_functions(model, likelihood)
    predictions = model.predict(theta)
    log_likelihood = loglike_fn(theta)
    jax.block_until_ready((predictions, log_likelihood))
    return Evaluation(
        label=label,
        predictions={
            name: np.asarray(value) for name, value in predictions.items()
        },
        log_likelihood=float(np.asarray(log_likelihood)),
    )


def _delta(reference: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    absolute = np.abs(candidate - reference)
    denominator = np.maximum(np.abs(reference), PREDICTION_ATOL)
    return {
        "max_absolute": float(np.max(absolute, initial=0.0)),
        "max_relative": float(np.max(absolute / denominator, initial=0.0)),
    }


def compare_evaluations(
    reference: Evaluation,
    candidate: Evaluation,
) -> dict[str, Any]:
    if reference.predictions.keys() != candidate.predictions.keys():
        raise BenchmarkError("prediction keys differ")
    prediction_deltas = {}
    for name in reference.predictions:
        expected = reference.predictions[name]
        actual = candidate.predictions[name]
        np.testing.assert_allclose(
            actual,
            expected,
            rtol=PREDICTION_RTOL,
            atol=PREDICTION_ATOL,
        )
        prediction_deltas[name] = _delta(expected, actual)
    np.testing.assert_allclose(
        candidate.log_likelihood,
        reference.log_likelihood,
        rtol=LOGLIKE_RTOL,
        atol=LOGLIKE_ATOL,
    )
    loglike_absolute = abs(candidate.log_likelihood - reference.log_likelihood)
    loglike_relative = loglike_absolute / max(
        abs(reference.log_likelihood), LOGLIKE_ATOL
    )
    return {
        "label": candidate.label,
        "prediction_deltas": prediction_deltas,
        "log_likelihood_delta": {
            "absolute": loglike_absolute,
            "relative": loglike_relative,
        },
    }


def _lower_stablehlo(function: Callable[[Any], Any], theta: Any) -> str:
    import jax

    lowered = jax.jit(function).lower(theta)
    return str(lowered.compiler_ir(dialect="stablehlo"))


def _benchmark_function(
    function: Callable[[Any], Any],
    theta: Any,
    warmup_calls: int,
    timed_calls: int,
) -> dict[str, Any]:
    import jax

    compiled = jax.jit(function)
    for _ in range(warmup_calls):
        jax.block_until_ready(compiled(theta))
    durations = []
    for _ in range(timed_calls):
        start = time.perf_counter()
        jax.block_until_ready(compiled(theta))
        durations.append(time.perf_counter() - start)
    return timing_metrics(durations)


def _runtime_metadata(jax: Any) -> dict[str, Any]:
    import ceridwen
    import jaxlib

    return {
        "python": sys.version.split()[0],
        "jax": jax.__version__,
        "jaxlib": jaxlib.__version__,
        "ceridwen": getattr(ceridwen, "__version__", None),
        "jax_enable_x64": bool(jax.config.jax_enable_x64),
        "backend": jax.default_backend(),
        "device_kind": getattr(jax.devices()[0], "device_kind", str(jax.devices()[0])),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    ceridwen_root = args.ceridwen_root.resolve()
    commit = require_ceridwen_commit(ceridwen_root, args.expected_ceridwen_commit)
    sys.path.insert(0, str(ceridwen_root))

    import ceridwen
    import jax

    imported_root = Path(ceridwen.__file__).resolve().parents[1]
    if imported_root != ceridwen_root:
        raise BenchmarkError(
            f"imported Ceridwen from {imported_root}, expected {ceridwen_root}"
        )
    jax.config.update("jax_enable_x64", True)
    runtime = _runtime_metadata(jax)
    workload_metadata: dict[str, Any] | None = None
    contracts = []
    implementation_results = []
    evaluations: dict[str, list[Evaluation]] = {}

    for implementation in IMPLEMENTATIONS:
        workload = vast_benchmark.build_joint_workload(args.project_root.resolve())
        if workload_metadata is None:
            workload_metadata = {
                **workload.metadata,
                "input_sha256": {
                    name: vast_benchmark._sha256(path)
                    for name, path in workload.input_paths.items()
                },
                "random_points": args.random_points,
                "warmup_calls": args.warmup_calls,
                "timed_calls": args.timed_calls,
            }
        elif workload.metadata != {
            name: workload_metadata[name] for name in workload.metadata
        }:
            raise BenchmarkError("workload metadata changed between implementations")
        basis_shape = install_implementation(workload.model.csp, implementation)
        random_points = deterministic_prior_points(
            workload.model, args.random_points, seed=SEED
        )
        labelled_points = edge_points(workload.model) + [
            (f"random_{index}", point)
            for index, point in enumerate(random_points)
        ]
        implementation_evaluations = [
            evaluate(workload.model, workload.likelihood, label, theta)
            for label, theta in labelled_points
        ]
        evaluations[implementation] = implementation_evaluations

        loglike_fn, _ = vast_benchmark._make_log_functions(
            workload.model, workload.likelihood
        )
        benchmark_theta = random_points[0]
        stablehlo = _lower_stablehlo(loglike_fn, benchmark_theta)
        hlo = stablehlo_evidence(stablehlo)
        if implementation == "baseline" and hlo["omits_forbidden_expansion"]:
            raise BenchmarkError(
                "baseline StableHLO does not expose the reference SSP expansion"
            )
        if implementation != "baseline" and not hlo["omits_forbidden_expansion"]:
            raise BenchmarkError(
                f"{implementation} StableHLO contains the full SSP expansion"
            )
        timings = _benchmark_function(
            loglike_fn,
            benchmark_theta,
            args.warmup_calls,
            args.timed_calls,
        )
        contract = comparison_contract(
            implementation=implementation,
            ceridwen_commit=commit,
            workload=workload_metadata,
            runtime=runtime,
        )
        contracts.append(contract)
        implementation_results.append(
            {
                "implementation": implementation,
                "fingerprint": contract,
                "normalized_fingerprint": normalized_fingerprint(contract),
                "basis_shape": basis_shape,
                "stablehlo": hlo,
                "timings": timings,
                "memory": _memory_metadata(jax.devices()[0]),
            }
        )

    require_comparable_contracts(contracts)
    equivalence = []
    baseline_evaluations = evaluations["baseline"]
    for implementation in IMPLEMENTATIONS[1:]:
        candidate_evaluations = evaluations[implementation]
        if [item.label for item in candidate_evaluations] != [
            item.label for item in baseline_evaluations
        ]:
            raise BenchmarkError("evaluation point labels differ")
        equivalence.extend(
            compare_evaluations(reference, candidate)
            for reference, candidate in zip(
                baseline_evaluations, candidate_evaluations, strict=True
            )
        )

    return {
        "schema_version": 1,
        "ceridwen_commit": commit,
        "seed": SEED,
        "implementations": implementation_results,
        "workload": workload_metadata,
        "equivalence": equivalence,
        "tolerances": {
            "prediction_rtol": PREDICTION_RTOL,
            "prediction_atol": PREDICTION_ATOL,
            "log_likelihood_rtol": LOGLIKE_RTOL,
            "log_likelihood_atol": LOGLIKE_ATOL,
            "reason": "float32 precontraction changes reduction order",
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--ceridwen-root", type=Path, required=True)
    parser.add_argument("--expected-ceridwen-commit", required=True)
    parser.add_argument("--random-points", type=int, default=DEFAULT_RANDOM_POINTS)
    parser.add_argument("--warmup-calls", type=int, default=DEFAULT_WARMUP_CALLS)
    parser.add_argument("--timed-calls", type=int, default=DEFAULT_TIMED_CALLS)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="use one random point, one warmup, and two timed CPU calls",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.smoke:
        args.random_points = 1
        args.warmup_calls = 1
        args.timed_calls = 2
    result = run(args)
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
