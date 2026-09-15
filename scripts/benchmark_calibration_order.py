#!/usr/bin/env python3
"""Time the joint likelihood against calibration order for the old and new
polynomial arithmetic in one process (same boot, same device).

Old: explicit (n_pix, k, k) Gram reduction, LU solve, separate slogdet
(frozen in ``validate_ceridwen_speedups.calibration_normal_reduce``).
New: Chebyshev-moment Gram matrix and one Cholesky (installed Ceridwen).
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from benchmark_ceridwen_vast import build_joint_workload  # noqa: E402
from validate_ceridwen_speedups import calibration_normal_reduce  # noqa: E402


def old_calibrate(self, y, mu, sigma, mask):
    """The pre-2026-09-15 ``calibrate``: LU solve plus an independent slogdet."""
    import jax.numpy as jnp

    mask = jnp.asarray(mask, dtype=bool)
    mu = jnp.asarray(mu)
    safe_sigma = jnp.where(mask, jnp.asarray(sigma), 1.0)
    normal = self.normal_matrix(mu, safe_sigma, mask)
    design = self.design(mu, safe_sigma, mask)
    target = jnp.where(mask, (jnp.asarray(y) - mu) / safe_sigma, 0.0)
    coeffs = jnp.linalg.solve(normal, design.T @ target)
    return (self.polynomial(coeffs) * mu, coeffs,
            self.log_marginal_terms(coeffs, normal))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--orders", type=int, nargs="+", default=[0, 3, 5, 10, 24],
                        help="0 means no calibration polynomial")
    parser.add_argument("--particles", type=int, nargs="+", default=[100, 500])
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260915)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import jax
    import jax.numpy as jnp
    from ceridwen.likelihood import (
        DiagonalGaussianLikelihood,
        DiagonalNoiseModel,
        MultiObservationLikelihood,
        PolynomialCalibration,
    )
    from benchmark_ceridwen_vast import _make_log_functions, _sample_prior

    workload = build_joint_workload(PROJECT_ROOT)
    model = workload.model
    spectrum = model.obs_dict["spectrum"]
    prior = _sample_prior(model, jax.random.PRNGKey(args.seed))
    max_particles = max(args.particles)
    prior = {name: value[:max_particles] for name, value in prior.items()}
    device = jax.devices()[0]

    new_normal = PolynomialCalibration.normal_matrix
    new_calibrate = PolynomialCalibration.calibrate
    variants = {
        "old": (calibration_normal_reduce, old_calibrate),
        "new": (new_normal, new_calibrate),
    }
    rows = []
    for order in args.orders:
        calibration = None if order == 0 else PolynomialCalibration.from_spectrum(
            spectrum, order, prior_sigma=0.1
        )
        likelihood = MultiObservationLikelihood(
            keys=("photometry", "spectrum"),
            likelihoods=(
                DiagonalGaussianLikelihood(),
                DiagonalGaussianLikelihood(
                    noise_model=DiagonalNoiseModel(use_fractional=True),
                    calibration=calibration,
                ),
            ),
        )
        for variant, (normal_method, calibrate_method) in variants.items():
            if calibration is None and variant == "old":
                continue
            PolynomialCalibration.normal_matrix = normal_method
            PolynomialCalibration.calibrate = calibrate_method
            loglike, _ = _make_log_functions(model, likelihood)
            batched = jax.jit(jax.vmap(loglike))
            for count in args.particles:
                points = {name: value[:count] for name, value in prior.items()}
                started = time.perf_counter()
                values = batched(points).block_until_ready()
                compile_s = time.perf_counter() - started
                samples = []
                for _ in range(args.repeats):
                    started = time.perf_counter()
                    batched(points).block_until_ready()
                    samples.append(time.perf_counter() - started)
                median_s = statistics.median(samples)
                rows.append({
                    "order": order,
                    "variant": variant,
                    "particles": count,
                    "n_coeff": 0 if calibration is None else calibration.n_coeff,
                    "compile_s": compile_s,
                    "median_s": median_s,
                    "min_s": min(samples),
                    "us_per_call": 1e6 * median_s / count,
                    "loglike_sum": float(jnp.sum(values)),
                })
                print(json.dumps(rows[-1]), flush=True)
    PolynomialCalibration.normal_matrix = new_normal
    PolynomialCalibration.calibrate = new_calibrate

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "target": workload.metadata["target"],
        "spectral_pixels": workload.metadata["spectral_pixels"],
        "device": str(device),
        "device_kind": device.device_kind,
        "jax": jax.__version__,
        "seed": args.seed,
        "repeats": args.repeats,
        "rows": rows,
    }, indent=1))
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
