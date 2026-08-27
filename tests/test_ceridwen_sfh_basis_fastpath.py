from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from scripts.ceridwen_sfh_basis_fastpath import (
    FASTPATH_MODES,
    build_step_sfh_operator,
    install_sfh_basis_fastpath,
    verify_sfh_basis_fastpath,
)


class FakeCSP:
    """Small CSP object exposing the contracts used by the fast path."""

    def __init__(self) -> None:
        self._n_afe = 5
        self._n_z = 13
        self._n_age = 107
        self.n_time = 8
        self.sfh_per_bin = False
        self.zh_const = True
        self.sfh_interp = "step"
        self.track_zred_age = False
        self._losvd_kernel_fft = None
        self._afe_solar_idx = 1
        self.afe_grid = jnp.linspace(-0.2, 0.6, self._n_afe)
        self.zmet = jnp.linspace(-2.0, -0.2, self._n_z)
        self.wave = jnp.linspace(1000.0, 10000.0, 64)
        self.flux = jax.random.uniform(
            jax.random.PRNGKey(7),
            (self._n_afe, self._n_z, self._n_age, self.wave.size),
            dtype=jnp.float32,
        )
        self.sfh_times = jnp.asarray([0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 5.0, 8.0])
        ages = jnp.linspace(0.02, 9.5, self._n_age)
        midpoints = 0.5 * (ages[:-1] + ages[1:])
        self._ssp_voronoi_lo = jnp.concatenate([jnp.zeros(1), midpoints])
        self._ssp_voronoi_hi = jnp.concatenate(
            [midpoints, jnp.asarray([ages[-1] + ages[-1] - ages[-2]])]
        )
        self.diff_dust = object()
        self.get_spectrum = self._baseline_spectrum

    @staticmethod
    def _coordinates(grid: Any, value: Any) -> tuple[Any, Any, Any]:
        high = jnp.clip(jnp.searchsorted(grid, value, side="left"), 1, len(grid) - 1)
        low = high - 1
        fraction = jnp.clip(
            (value - grid[low]) / (grid[high] - grid[low]),
            0.0,
            1.0,
        )
        return low, high, fraction

    def calculate_ssp_weights(self, theta: dict[str, Any]) -> Any:
        sfh = jnp.clip(theta["sfh"], 1e-30, None)
        sfh_mid = 0.5 * (sfh[:-1] + sfh[1:])
        t_young = self.sfh_times[:-1]
        t_old = self.sfh_times[1:]
        dt = t_old - t_young
        overlap = jnp.maximum(
            0.0,
            jnp.minimum(t_old[:, None], self._ssp_voronoi_hi[None, :])
            - jnp.maximum(t_young[:, None], self._ssp_voronoi_lo[None, :]),
        )
        raw_weights = sfh_mid[:, None] * overlap
        bin_mass = sfh_mid * dt
        normalization = jnp.maximum(jnp.sum(raw_weights, axis=1), 1e-30)
        age_weights = jnp.sum(
            raw_weights * (bin_mass / normalization)[:, None],
            axis=0,
        )

        low, high, fraction = self._coordinates(self.zmet, theta["Z"][0])
        weights = jnp.zeros((self._n_z, self._n_age))
        weights = weights.at[low].add((1.0 - fraction) * age_weights)
        return weights.at[high].add(fraction * age_weights)

    def attenuate_dust(self, wave: Any, theta: dict[str, Any]) -> tuple[Any, Any]:
        diffuse = theta["diffuse_tau_kc"][0] * (wave / jnp.mean(wave)) ** -0.7
        return jnp.zeros((1, wave.size)), diffuse[None, :]

    def _baseline_spectrum(
        self,
        theta: dict[str, Any],
        *,
        include_lines: Any = None,
    ) -> Any:
        del include_lines
        low, high, fraction = self._coordinates(self.afe_grid, theta["afe"][0])
        flux = (1.0 - fraction) * self.flux[low] + fraction * self.flux[high]
        weights = self.calculate_ssp_weights(theta).astype(jnp.float32)
        spectrum = jnp.einsum("za,zaw->w", weights, flux)
        _, diffuse = self.attenuate_dust(self.wave, theta)
        return (spectrum * jnp.exp(-diffuse.astype(jnp.float32))).reshape((-1,))


def theta_points() -> list[dict[str, Any]]:
    sfh = jnp.exp(jnp.linspace(-1.5, 1.5, 8))
    return [
        {
            "sfh": sfh,
            "Z": jnp.asarray([-1.85]),
            "afe": jnp.asarray([0.2]),
            "diffuse_tau_kc": jnp.asarray([0.4]),
        },
        {
            "sfh": sfh[::-1],
            "Z": jnp.asarray([-2.0]),
            "afe": jnp.asarray([-0.2]),
            "diffuse_tau_kc": jnp.asarray([0.0]),
        },
        {
            "sfh": jnp.ones(8),
            "Z": jnp.asarray([-0.2]),
            "afe": jnp.asarray([0.6]),
            "diffuse_tau_kc": jnp.asarray([1.8]),
        },
    ]


def assert_tree_close(reference: Any, candidate: Any) -> None:
    reference_leaves, reference_tree = jax.tree.flatten(reference)
    candidate_leaves, candidate_tree = jax.tree.flatten(candidate)
    assert reference_tree == candidate_tree
    for expected, actual in zip(reference_leaves, candidate_leaves, strict=True):
        np.testing.assert_allclose(
            np.asarray(actual),
            np.asarray(expected),
            rtol=5e-5,
            atol=1e-5,
        )


def test_step_operator_reproduces_dense_age_weights() -> None:
    csp = FakeCSP()
    theta = theta_points()[0]
    operator = build_step_sfh_operator(
        csp.sfh_times,
        csp._ssp_voronoi_lo,
        csp._ssp_voronoi_hi,
    )
    bin_sfr = 0.5 * (theta["sfh"][:-1] + theta["sfh"][1:])
    operator_age_weights = jnp.einsum("b,ba->a", bin_sfr, operator)
    dense_age_weights = jnp.sum(csp.calculate_ssp_weights(theta), axis=0)

    np.testing.assert_allclose(
        np.asarray(operator_age_weights),
        np.asarray(dense_age_weights),
        rtol=2e-6,
        atol=2e-6,
    )


@pytest.mark.parametrize("mode", FASTPATH_MODES)
def test_fastpath_matches_dense_source_spectrum_and_gradient(mode: str) -> None:
    csp = FakeCSP()
    points = theta_points()
    baseline_spectra = [np.asarray(csp.get_spectrum(theta)) for theta in points]
    gradient_theta = points[0]
    baseline_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(gradient_theta)

    state = install_sfh_basis_fastpath(csp, mode)
    verification = verify_sfh_basis_fastpath(csp, points)
    candidate_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(gradient_theta)

    assert verification["max_relative_error"] < 5e-5
    assert_tree_close(baseline_gradient, candidate_gradient)
    for reference, theta in zip(baseline_spectra, points, strict=True):
        np.testing.assert_allclose(
            np.asarray(csp.get_spectrum(theta)),
            reference,
            rtol=5e-5,
            atol=1e-5,
        )

    if mode == "corners":
        assert state.basis_shape is None
        assert state.basis_bytes == 0
    else:
        assert state.basis_shape == (5, 13, 7, 64)
        assert state.basis_bytes == 5 * 13 * 7 * 64 * 4


@pytest.mark.parametrize("mode", ("sfh-basis-sparse", "sfh-basis-dense"))
def test_runtime_hlo_does_not_capture_the_107_age_flux_cube(mode: str) -> None:
    csp = FakeCSP()
    install_sfh_basis_fastpath(csp, mode)

    stablehlo = jax.jit(csp.get_spectrum).lower(theta_points()[0]).as_text()

    expected_basis = (
        "tensor<5x13x7x64xf32>"
        if mode == "sfh-basis-sparse"
        else "tensor<455x64xf32>"
    )
    assert expected_basis in stablehlo
    assert "tensor<5x13x107x64xf32>" not in stablehlo


def test_runtime_lookback_grid_is_rejected() -> None:
    csp = FakeCSP()
    install_sfh_basis_fastpath(csp, "sfh-basis-sparse")
    theta = {**theta_points()[0], "lookback_time": jnp.linspace(0.0, 8.0, 8)}

    with pytest.raises(ValueError, match="runtime lookback"):
        csp.get_spectrum(theta)


@pytest.mark.parametrize(
    ("attribute", "value", "message"),
    (
        ("track_zred_age", True, "fixed lookback"),
        ("sfh_interp", "linear", "sfh_interp='step'"),
        ("zh_const", False, "zh_const=True"),
        ("_losvd_kernel_fft", True, "LOSVD smoothing off"),
        ("dust_attn", object(), "age-dependent dust"),
        ("dust_emi", object(), "dust emission"),
    ),
)
def test_incompatible_csp_is_rejected(
    attribute: str,
    value: Any,
    message: str,
) -> None:
    csp = FakeCSP()
    setattr(csp, attribute, value)

    with pytest.raises(ValueError, match=message):
        install_sfh_basis_fastpath(csp, "sfh-basis-sparse")
