"""Experimental low-rank fast paths for the fixed Ceridwen benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import jax
import jax.numpy as jnp
import numpy as np
from jax import lax

FASTPATH_MODES = (
    "corners",
    "sfh-basis-sparse",
    "sfh-basis-dense",
)


@dataclass(frozen=True)
class FastpathState:
    """Hold immutable arrays and the original spectrum implementation."""

    mode: str
    original_get_spectrum: Callable[..., Any]
    step_operator: Any | None
    sfh_basis: Any | None
    sfh_basis_flat: Any | None

    @property
    def basis_shape(self) -> tuple[int, ...] | None:
        if self.sfh_basis is None:
            return None
        return tuple(int(size) for size in self.sfh_basis.shape)

    @property
    def basis_bytes(self) -> int:
        if self.sfh_basis is None:
            return 0
        return int(self.sfh_basis.size * self.sfh_basis.dtype.itemsize)


def build_step_sfh_operator(
    sfh_times: Any,
    voronoi_lo: Any,
    voronoi_hi: Any,
) -> Any:
    """Map one fixed step-SFH bin onto the SSP-age Voronoi cells."""
    times = jnp.asarray(sfh_times)
    t_young = times[:-1]
    t_old = times[1:]
    dt = t_old - t_young
    overlap = jnp.maximum(
        0.0,
        jnp.minimum(t_old[:, None], jnp.asarray(voronoi_hi)[None, :])
        - jnp.maximum(t_young[:, None], jnp.asarray(voronoi_lo)[None, :]),
    )
    normalizer = jnp.maximum(jnp.sum(overlap, axis=1), 1e-30)
    return overlap * (dt / normalizer)[:, None]


def _bin_sfr(csp: Any, theta: dict[str, Any]) -> Any:
    sfh = jnp.clip(theta["sfh"], 1e-30, None)
    if csp.sfh_per_bin:
        return sfh.astype(jnp.float32)
    return (0.5 * (sfh[:-1] + sfh[1:])).astype(jnp.float32)


def _alpha_coordinates(csp: Any, theta: dict[str, Any]) -> tuple[Any, Any]:
    if csp._n_afe == 1:
        index = jnp.asarray(0, dtype=jnp.int32)
        return jnp.stack([index, index]), jnp.array([1.0, 0.0], dtype=jnp.float32)
    if "afe" not in theta:
        index = jnp.asarray(csp._afe_solar_idx, dtype=jnp.int32)
        return jnp.stack([index, index]), jnp.array([1.0, 0.0], dtype=jnp.float32)

    high = jnp.clip(
        jnp.searchsorted(
            csp.afe_grid,
            jnp.ravel(theta["afe"])[0],
            side="left",
        ),
        1,
        csp._n_afe - 1,
    )
    low = high - 1
    value = jnp.ravel(theta["afe"])[0]
    fraction = jnp.clip(
        (value - csp.afe_grid[low]) / (csp.afe_grid[high] - csp.afe_grid[low]),
        0.0,
        1.0,
    ).astype(jnp.float32)
    return jnp.stack([low, high]), jnp.stack([1.0 - fraction, fraction])


def _metallicity_coordinates(csp: Any, theta: dict[str, Any]) -> tuple[Any, Any]:
    value = jnp.ravel(theta["Z"])[0]
    high = jnp.clip(
        jnp.searchsorted(csp.zmet, value, side="left"),
        1,
        csp._n_z - 1,
    )
    low = high - 1
    fraction = jnp.clip(
        (value - csp.zmet[low]) / (csp.zmet[high] - csp.zmet[low]),
        0.0,
        1.0,
    ).astype(jnp.float32)
    return jnp.stack([low, high]), jnp.stack([1.0 - fraction, fraction])


def _interpolation_coordinates(
    csp: Any,
    theta: dict[str, Any],
) -> tuple[Any, Any, Any]:
    alpha_indices, alpha_weights = _alpha_coordinates(csp, theta)
    z_indices, z_weights = _metallicity_coordinates(csp, theta)
    coefficients = alpha_weights[:, None] * z_weights[None, :]
    return alpha_indices, z_indices, coefficients


def _corner_spectrum(csp: Any, theta: dict[str, Any]) -> Any:
    alpha_indices, z_indices, coefficients = _interpolation_coordinates(csp, theta)
    dense_weights = csp.calculate_ssp_weights(theta).astype(jnp.float32)
    age_weights = jnp.sum(dense_weights, axis=0)
    corners = csp.flux[
        alpha_indices[:, None],
        z_indices[None, :],
        :,
        :,
    ]
    return jnp.einsum(
        "ij,a,ijaw->w",
        coefficients,
        age_weights,
        corners,
        precision=lax.Precision.HIGHEST,
    )


def _basis_sparse_spectrum(
    csp: Any,
    state: FastpathState,
    theta: dict[str, Any],
) -> Any:
    alpha_indices, z_indices, coefficients = _interpolation_coordinates(csp, theta)
    corners = state.sfh_basis[
        alpha_indices[:, None],
        z_indices[None, :],
        :,
        :,
    ]
    return jnp.einsum(
        "ij,b,ijbw->w",
        coefficients,
        _bin_sfr(csp, theta),
        corners,
        precision=lax.Precision.HIGHEST,
    )


def _basis_dense_spectrum(
    csp: Any,
    state: FastpathState,
    theta: dict[str, Any],
) -> Any:
    alpha_indices, z_indices, coefficients = _interpolation_coordinates(csp, theta)
    bin_sfr = _bin_sfr(csp, theta)
    coefficient_cube = jnp.zeros(
        (csp._n_afe, csp._n_z, csp.n_time - 1),
        dtype=jnp.float32,
    )
    for alpha_position in range(2):
        for z_position in range(2):
            coefficient_cube = coefficient_cube.at[
                alpha_indices[alpha_position],
                z_indices[z_position],
                :,
            ].add(coefficients[alpha_position, z_position] * bin_sfr)
    return jnp.matmul(
        coefficient_cube.reshape((-1,)),
        state.sfh_basis_flat,
        precision=lax.Precision.HIGHEST,
    )


def _validate_csp(csp: Any, mode: str) -> None:
    if mode not in FASTPATH_MODES:
        raise ValueError(f"unsupported Ceridwen fast-path mode: {mode!r}")
    if not csp.zh_const:
        raise ValueError("the experimental fast path requires zh_const=True")
    if csp.sfh_interp != "step":
        raise ValueError("the experimental fast path requires sfh_interp='step'")
    if csp.track_zred_age:
        raise ValueError("the experimental fast path requires a fixed lookback grid")
    if csp._losvd_kernel_fft is not None:
        raise ValueError("the experimental fast path requires source LOSVD smoothing off")
    if hasattr(csp, "dust_attn"):
        raise ValueError("the experimental fast path does not support age-dependent dust")
    if hasattr(csp, "dust_emi"):
        raise ValueError("the experimental fast path does not support dust emission")


def install_sfh_basis_fastpath(csp: Any, mode: str) -> FastpathState:
    """Replace one compatible CSP instance's source-spectrum implementation."""
    _validate_csp(csp, mode)
    original_get_spectrum = csp.get_spectrum
    step_operator = None
    sfh_basis = None
    sfh_basis_flat = None

    if mode.startswith("sfh-basis"):
        step_operator = build_step_sfh_operator(
            csp.sfh_times,
            csp._ssp_voronoi_lo,
            csp._ssp_voronoi_hi,
        ).astype(jnp.float32)
        sfh_basis = jnp.einsum(
            "ba,pzaw->pzbw",
            step_operator,
            csp.flux,
            precision=lax.Precision.HIGHEST,
        )
        sfh_basis = jax.block_until_ready(sfh_basis)
        sfh_basis_flat = sfh_basis.reshape((-1, sfh_basis.shape[-1]))

    state = FastpathState(
        mode=mode,
        original_get_spectrum=original_get_spectrum,
        step_operator=step_operator,
        sfh_basis=sfh_basis,
        sfh_basis_flat=sfh_basis_flat,
    )

    has_diffuse_dust = hasattr(csp, "diff_dust")

    def get_spectrum_fast(theta: dict[str, Any], *, include_lines: Any = None) -> Any:
        del include_lines
        if "lookback_time" in theta:
            raise ValueError(
                "the experimental fast path cannot use a runtime lookback grid"
            )
        if mode == "corners":
            spectrum = _corner_spectrum(csp, theta)
        elif mode == "sfh-basis-sparse":
            spectrum = _basis_sparse_spectrum(csp, state, theta)
        else:
            spectrum = _basis_dense_spectrum(csp, state, theta)

        if has_diffuse_dust:
            _, attenuation = csp.attenuate_dust(csp.wave, theta)
            spectrum = spectrum * jnp.exp(-attenuation.astype(jnp.float32))
        return spectrum.reshape((-1,))

    get_spectrum_fast.__name__ = f"get_spectrum_{mode.replace('-', '_')}"
    csp.get_spectrum = get_spectrum_fast
    csp._experimental_sfh_basis_fastpath = state
    return state


def verify_sfh_basis_fastpath(
    csp: Any,
    thetas: list[dict[str, Any]],
    *,
    rtol: float = 5e-5,
    atol_fraction: float = 1e-7,
) -> dict[str, float]:
    """Compare the installed implementation with the saved dense path."""
    state = getattr(csp, "_experimental_sfh_basis_fastpath", None)
    if state is None:
        raise ValueError("no experimental Ceridwen fast path is installed")

    max_relative_error = 0.0
    max_absolute_error = 0.0
    for theta in thetas:
        reference = state.original_get_spectrum(theta)
        candidate = csp.get_spectrum(theta)
        reference, candidate = jax.block_until_ready((reference, candidate))
        reference_np = np.asarray(reference)
        candidate_np = np.asarray(candidate)
        scale = float(np.max(np.abs(reference_np)))
        atol = max(np.finfo(np.float32).tiny, atol_fraction * scale)
        difference = np.abs(candidate_np - reference_np)
        denominator = np.maximum(np.abs(reference_np), atol)
        max_absolute_error = max(max_absolute_error, float(np.max(difference)))
        max_relative_error = max(
            max_relative_error,
            float(np.max(difference / denominator)),
        )
        if not np.allclose(candidate_np, reference_np, rtol=rtol, atol=atol):
            raise AssertionError(
                "experimental Ceridwen fast path failed numerical equivalence: "
                f"max_abs={np.max(difference):.6e}, "
                f"max_scaled_rel={np.max(difference / denominator):.6e}"
            )
    return {
        "max_absolute_error": max_absolute_error,
        "max_relative_error": max_relative_error,
    }
