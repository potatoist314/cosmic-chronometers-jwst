#!/usr/bin/env python3
"""Experiment with exact sparse fast paths for the Ceridwen alpha SSP model."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MethodType
from typing import Any, Literal

import jax
import jax.numpy as jnp
import numpy as np

FastPathMode = Literal["four-corner", "sfh-basis"]


class FastPathError(RuntimeError):
    """Report that a CSP configuration is not supported by the experiment."""


@dataclass(frozen=True)
class FastPathHandle:
    """State required to inspect and remove an installed experimental path."""

    mode: FastPathMode
    original_get_spectrum: Callable[..., Any]
    basis_build_seconds: float = 0.0
    basis_shape: tuple[int, ...] | None = None
    basis_nbytes: int = 0


def _scalar(value: Any) -> jax.Array:
    return jnp.ravel(jnp.asarray(value))[0]


def _bracket(grid: jax.Array, value: Any) -> tuple[jax.Array, jax.Array]:
    """Return the upper grid index and clipped linear interpolation fraction."""
    target = _scalar(value)
    upper = jnp.clip(jnp.searchsorted(grid, target, side="left"), 1, grid.size - 1)
    lower_value = grid[upper - 1]
    upper_value = grid[upper]
    fraction = jnp.clip(
        (target - lower_value) / (upper_value - lower_value),
        0.0,
        1.0,
    )
    return upper, fraction.astype(jnp.float32)


def _corner_indices_and_coefficients(
    csp: Any,
    theta: Mapping[str, Any],
) -> tuple[jax.Array, jax.Array, jax.Array]:
    alpha_upper, alpha_fraction = _bracket(csp.afe_grid, theta["afe"])
    z_upper, z_fraction = _bracket(csp.zmet, theta["Z"])

    alpha_indices = jnp.stack((alpha_upper - 1, alpha_upper))
    z_indices = jnp.stack((z_upper - 1, z_upper))
    alpha_coefficients = jnp.stack((1.0 - alpha_fraction, alpha_fraction))
    z_coefficients = jnp.stack((1.0 - z_fraction, z_fraction))
    coefficients = alpha_coefficients[:, None] * z_coefficients[None, :]
    return alpha_indices, z_indices, coefficients.astype(jnp.float32)


def _apply_diffuse_attenuation(
    csp: Any,
    theta: Mapping[str, Any],
    spectrum: jax.Array,
) -> jax.Array:
    _age_attenuation, diffuse_attenuation = csp.attenuate_dust(csp.wave, theta)
    return spectrum * jnp.exp(-diffuse_attenuation.astype(jnp.float32))


def _require_supported_configuration(csp: Any) -> None:
    if not bool(getattr(csp, "zh_const", False)):
        raise FastPathError(
            "the experiment requires constant metallicity (zh_const=True)"
        )
    if getattr(csp, "sfh_interp", None) != "step":
        raise FastPathError("the experiment requires sfh_interp='step'")
    if bool(getattr(csp, "track_zred_age", False)):
        raise FastPathError("the experiment requires a fixed lookback-time grid")
    if jnp.asarray(csp.flux).ndim != 4:
        raise FastPathError(
            "the experiment requires a 4-D alpha-enhanced SSP flux grid"
        )
    if csp.afe_grid.size < 2 or csp.zmet.size < 2:
        raise FastPathError("the experiment requires at least two alpha and Z planes")

    method_name = getattr(csp.get_spectrum, "__name__", "")
    supported_methods = {
        "get_spectrum_dattn_nodem_noneb",
        "get_spectrum_nodattn_nodem_noneb",
    }
    if method_name not in supported_methods:
        raise FastPathError(
            "the experiment supports only continuum paths without dust emission, "
            f"nebular emission, or LOSVD wrapping; found {method_name!r}"
        )
    if method_name == "get_spectrum_dattn_nodem_noneb" and hasattr(
        csp, "dust_attn"
    ):
        raise FastPathError(
            "the experiment supports diffuse-only attenuation, not age-dependent dust"
        )


def _four_corner_spectrum(
    csp: Any,
    theta: Mapping[str, Any],
    *,
    apply_diffuse: bool,
) -> jax.Array:
    alpha_indices, z_indices, coefficients = _corner_indices_and_coefficients(
        csp, theta
    )
    corners = csp.flux[
        alpha_indices[:, None],
        z_indices[None, :],
        :,
        :,
    ]
    dense_weights = csp.calculate_ssp_weights(theta).astype(jnp.float32)
    age_weights = jnp.sum(dense_weights, axis=0)
    spectrum = jnp.einsum(
        "ij,a,ijaw->w",
        coefficients,
        age_weights,
        corners,
        optimize="optimal",
    )
    if apply_diffuse:
        spectrum = _apply_diffuse_attenuation(csp, theta, spectrum)
    return spectrum.reshape((-1,))


def _build_bin_to_age_operator(csp: Any) -> jax.Array:
    """Reproduce the static step-SFH overlap map used by ``_ssp_weights``."""
    t_young = csp.sfh_times[:-1]
    t_old = csp.sfh_times[1:]
    dt = t_old - t_young
    overlap = jnp.maximum(
        0.0,
        jnp.minimum(t_old[:, None], csp._ssp_voronoi_hi[None, :])
        - jnp.maximum(t_young[:, None], csp._ssp_voronoi_lo[None, :]),
    )
    overlap_sum = jnp.maximum(jnp.sum(overlap, axis=1), 1e-30)
    return (overlap * (dt / overlap_sum)[:, None]).astype(jnp.float32)


def build_sfh_basis(csp: Any) -> tuple[jax.Array, float]:
    """Precontract the static 107-age SSP axis into the seven SFH bins."""
    start = time.perf_counter()
    bin_to_age = _build_bin_to_age_operator(csp)
    basis = jnp.einsum(
        "ba,pzaw->pzbw",
        bin_to_age,
        csp.flux,
        optimize="optimal",
    ).astype(jnp.float32)
    jax.block_until_ready(basis)
    return basis, time.perf_counter() - start


def _sfh_basis_spectrum(
    csp: Any,
    theta: Mapping[str, Any],
    basis: jax.Array,
    *,
    apply_diffuse: bool,
) -> jax.Array:
    alpha_indices, z_indices, coefficients = _corner_indices_and_coefficients(
        csp, theta
    )
    corners = basis[
        alpha_indices[:, None],
        z_indices[None, :],
        :,
        :,
    ]
    sfh = jnp.clip(jnp.ravel(jnp.asarray(theta["sfh"])), 1e-30, None)
    if csp.sfh_per_bin:
        sfh_bin = sfh
    else:
        sfh_bin = 0.5 * (sfh[:-1] + sfh[1:])
    spectrum = jnp.einsum(
        "ij,b,ijbw->w",
        coefficients,
        sfh_bin.astype(jnp.float32),
        corners,
        optimize="optimal",
    )
    if apply_diffuse:
        spectrum = _apply_diffuse_attenuation(csp, theta, spectrum)
    return spectrum.reshape((-1,))


def install_fastpath(csp: Any, mode: FastPathMode) -> FastPathHandle:
    """Replace ``csp.get_spectrum`` with one exact benchmark-specific fast path."""
    _require_supported_configuration(csp)
    original = csp.get_spectrum
    apply_diffuse = original.__name__ == "get_spectrum_dattn_nodem_noneb"

    if mode == "four-corner":

        def get_spectrum(
            self: Any,
            theta: Mapping[str, Any],
            *,
            include_lines: Any = None,
        ) -> jax.Array:
            del include_lines
            return _four_corner_spectrum(
                self, theta, apply_diffuse=apply_diffuse
            )

        csp.get_spectrum = MethodType(get_spectrum, csp)
        return FastPathHandle(mode=mode, original_get_spectrum=original)

    if mode == "sfh-basis":
        basis, build_seconds = build_sfh_basis(csp)

        def get_spectrum(
            self: Any,
            theta: Mapping[str, Any],
            *,
            include_lines: Any = None,
        ) -> jax.Array:
            del include_lines
            return _sfh_basis_spectrum(
                self, theta, basis, apply_diffuse=apply_diffuse
            )

        csp.get_spectrum = MethodType(get_spectrum, csp)
        return FastPathHandle(
            mode=mode,
            original_get_spectrum=original,
            basis_build_seconds=build_seconds,
            basis_shape=tuple(int(size) for size in basis.shape),
            basis_nbytes=int(basis.size * basis.dtype.itemsize),
        )

    raise FastPathError(f"unknown fast-path mode: {mode}")


def restore_fastpath(csp: Any, handle: FastPathHandle) -> None:
    csp.get_spectrum = handle.original_get_spectrum


def _sample_theta_batch(model: Any, count: int, seed: int) -> dict[str, jax.Array]:
    key = jax.random.PRNGKey(seed)
    particles: dict[str, jax.Array] = {}
    for name, initial_value in model.theta_init.items():
        key, subkey = jax.random.split(key)
        particles[name] = model.priors[name].sample(
            subkey,
            shape=(count, *initial_value.shape),
        )
    return particles


def _tree_max_error(reference: Any, candidate: Any) -> tuple[float, float]:
    reference_leaves, reference_tree = jax.tree.flatten(reference)
    candidate_leaves, candidate_tree = jax.tree.flatten(candidate)
    if reference_tree != candidate_tree:
        raise FastPathError("prediction trees differ")

    max_absolute = 0.0
    max_relative = 0.0
    for expected, actual in zip(reference_leaves, candidate_leaves, strict=True):
        expected_array = np.asarray(expected)
        actual_array = np.asarray(actual)
        if not (
            np.all(np.isfinite(expected_array))
            and np.all(np.isfinite(actual_array))
        ):
            raise FastPathError("validation produced a non-finite value")
        absolute = np.abs(actual_array - expected_array)
        denominator = np.maximum(np.abs(expected_array), np.finfo(np.float32).tiny)
        max_absolute = max(max_absolute, float(np.max(absolute)))
        max_relative = max(max_relative, float(np.max(absolute / denominator)))
    return max_absolute, max_relative


def validate_mode(
    workload: Any,
    mode: FastPathMode,
    *,
    points: int,
    seed: int,
) -> dict[str, Any]:
    model = workload.model
    csp = model.csp
    theta_batch = _sample_theta_batch(model, points, seed)
    baseline_predict = jax.jit(jax.vmap(model.predict))
    baseline_predictions = jax.block_until_ready(baseline_predict(theta_batch))

    baseline_loglike, _baseline_logprior = _benchmark_module()._make_log_functions(
        model,
        workload.likelihood,
    )
    baseline_loglikes = jax.block_until_ready(jax.vmap(baseline_loglike)(theta_batch))
    gradient_theta = jax.tree.map(lambda value: value[0], theta_batch)
    baseline_gradient = jax.block_until_ready(
        jax.grad(baseline_loglike)(gradient_theta)
    )

    handle = install_fastpath(csp, mode)
    try:
        fast_predict = jax.jit(jax.vmap(model.predict))
        fast_predictions = jax.block_until_ready(fast_predict(theta_batch))
        fast_loglike, _fast_logprior = _benchmark_module()._make_log_functions(
            model,
            workload.likelihood,
        )
        fast_loglikes = jax.block_until_ready(jax.vmap(fast_loglike)(theta_batch))
        fast_gradient = jax.block_until_ready(jax.grad(fast_loglike)(gradient_theta))
    finally:
        restore_fastpath(csp, handle)

    prediction_absolute, prediction_relative = _tree_max_error(
        baseline_predictions,
        fast_predictions,
    )
    loglike_absolute, loglike_relative = _tree_max_error(
        baseline_loglikes,
        fast_loglikes,
    )
    gradient_absolute, gradient_relative = _tree_max_error(
        baseline_gradient,
        fast_gradient,
    )
    return {
        "mode": mode,
        "validation_points": points,
        "prediction_max_abs": prediction_absolute,
        "prediction_max_rel": prediction_relative,
        "loglike_max_abs": loglike_absolute,
        "loglike_max_rel": loglike_relative,
        "gradient_max_abs": gradient_absolute,
        "gradient_max_rel": gradient_relative,
        "basis_build_seconds": handle.basis_build_seconds,
        "basis_shape": handle.basis_shape,
        "basis_nbytes": handle.basis_nbytes,
    }


def benchmark_mode(workload: Any, mode: FastPathMode | None) -> dict[str, Any]:
    csp = workload.model.csp
    handle: FastPathHandle | None = None
    if mode is not None:
        handle = install_fastpath(csp, mode)
    try:
        timings = _benchmark_module().run_fixed_steps(workload)
    finally:
        if handle is not None:
            restore_fastpath(csp, handle)
    return {
        "mode": "baseline" if mode is None else mode,
        "likelihood_calls_per_second": timings["likelihood_calls_per_second"],
        "total_timed_seconds": timings["total_timed_seconds"],
        "iteration_seconds": timings["iteration_seconds"],
        "basis_build_seconds": 0.0 if handle is None else handle.basis_build_seconds,
        "basis_shape": None if handle is None else handle.basis_shape,
        "basis_nbytes": 0 if handle is None else handle.basis_nbytes,
    }


def _benchmark_module() -> Any:
    try:
        from scripts import benchmark_ceridwen_vast as benchmark
    except ModuleNotFoundError:
        import benchmark_ceridwen_vast as benchmark
    return benchmark


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("four-corner", "sfh-basis", "all"),
        default="all",
    )
    parser.add_argument("--validation-points", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260827)
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="also run the full fixed 5,000-call NSS benchmark",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    benchmark = _benchmark_module()
    project_root = Path(__file__).resolve().parents[1]
    workload = benchmark.build_joint_workload(project_root)
    modes: tuple[FastPathMode, ...]
    if args.mode == "all":
        modes = ("four-corner", "sfh-basis")
    else:
        modes = (args.mode,)

    output: dict[str, Any] = {
        "validation": [
            validate_mode(
                workload,
                mode,
                points=args.validation_points,
                seed=args.seed,
            )
            for mode in modes
        ]
    }
    if args.benchmark:
        benchmark_results = [
            benchmark_mode(workload, None),
            *(benchmark_mode(workload, mode) for mode in modes),
        ]
        baseline_speed = benchmark_results[0]["likelihood_calls_per_second"]
        for result in benchmark_results:
            result["speedup_vs_baseline"] = (
                result["likelihood_calls_per_second"] / baseline_speed
            )
        output["benchmark"] = benchmark_results
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
