from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from jax import lax

from scripts import ceridwen_sfh_basis_fastpath as fastpath


class FakeCSP:
    def __init__(self) -> None:
        key = jax.random.PRNGKey(0)
        self.flux = jax.random.uniform(
            key,
            (3, 4, 5, 7),
            minval=0.1,
            maxval=1.0,
        )
        self.afe_grid = jnp.array([-0.2, 0.1, 0.6])
        self.zmet = jnp.array([-2.0, -1.0, -0.2, 0.3])
        self.wave = jnp.linspace(1000.0, 2000.0, 7)
        self.sfh_times = jnp.array([0.0, 1.0, 3.0, 6.0])
        self._ssp_voronoi_lo = jnp.array([0.0, 0.7, 1.8, 3.4, 5.0])
        self._ssp_voronoi_hi = jnp.array([0.7, 1.8, 3.4, 5.0, 8.0])
        self._n_afe = self.afe_grid.size
        self._afe_solar_idx = 1
        self._n_z = self.zmet.size
        self.n_time = self.sfh_times.size
        self.sfh_per_bin = False
        self.zh_const = True
        self.sfh_interp = "step"
        self.track_zred_age = False
        self._losvd_kernel_fft = None
        self.diff_dust = object()

    def calculate_ssp_weights(self, theta: dict[str, jax.Array]) -> jax.Array:
        sfh = jnp.clip(theta["sfh"], 1e-30, None)
        sfh_mid = 0.5 * (sfh[:-1] + sfh[1:])
        operator = fastpath.build_step_sfh_operator(
            self.sfh_times,
            self._ssp_voronoi_lo,
            self._ssp_voronoi_hi,
        )
        age_weights = sfh_mid @ operator
        z_indices, z_weights = fastpath._metallicity_coordinates(self, theta)
        weights = jnp.zeros(
            (self._n_z, age_weights.size),
            dtype=jnp.float32,
        )
        weights = weights.at[z_indices[0]].add(z_weights[0] * age_weights)
        return weights.at[z_indices[1]].add(z_weights[1] * age_weights)

    def attenuate_dust(
        self,
        wave: jax.Array,
        theta: dict[str, jax.Array],
    ) -> tuple[jax.Array, jax.Array]:
        diffuse = jnp.ravel(theta["tau"])[0] * (wave / wave.mean())
        return jnp.zeros((1, wave.size)), diffuse

    def _flux_at_afe(self, theta: dict[str, jax.Array]) -> jax.Array:
        indices, weights = fastpath._alpha_coordinates(self, theta)
        return weights[0] * self.flux[indices[0]] + weights[1] * self.flux[
            indices[1]
        ]

    def get_spectrum(
        self,
        theta: dict[str, jax.Array],
        *,
        include_lines: Any = None,
    ) -> jax.Array:
        del include_lines
        flux = self._flux_at_afe(theta)
        weights = self.calculate_ssp_weights(theta).astype(jnp.float32)
        spectrum = jnp.einsum(
            "za,zaw->w",
            weights,
            flux,
            precision=lax.Precision.HIGHEST,
        )
        _, diffuse = self.attenuate_dust(self.wave, theta)
        return spectrum * jnp.exp(-diffuse.astype(jnp.float32))


def theta() -> dict[str, jax.Array]:
    return {
        "sfh": jnp.array([0.3, 0.8, 1.2, 0.6]),
        "Z": jnp.array([-0.55]),
        "afe": jnp.array([0.22]),
        "tau": jnp.array([0.13]),
    }


def assert_tree_close(expected: Any, actual: Any) -> None:
    expected_leaves, expected_tree = jax.tree.flatten(expected)
    actual_leaves, actual_tree = jax.tree.flatten(actual)
    assert expected_tree == actual_tree
    for expected_leaf, actual_leaf in zip(
        expected_leaves,
        actual_leaves,
        strict=True,
    ):
        np.testing.assert_allclose(
            actual_leaf,
            expected_leaf,
            rtol=2e-5,
            atol=2e-6,
        )


@pytest.mark.parametrize("mode", fastpath.FASTPATH_MODES)
def test_fastpath_matches_dense_spectrum_and_gradient(mode: str) -> None:
    csp = FakeCSP()
    parameters = theta()
    baseline = jax.jit(csp.get_spectrum)(parameters)
    baseline_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(parameters)

    state = fastpath.install_sfh_basis_fastpath(csp, mode)
    actual = jax.jit(csp.get_spectrum)(parameters)
    actual_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(parameters)

    assert_tree_close(baseline, actual)
    assert_tree_close(baseline_gradient, actual_gradient)
    verification = fastpath.verify_sfh_basis_fastpath(csp, [parameters])
    assert verification["max_relative_error"] < 2e-5
    assert state.original_get_spectrum is not csp.get_spectrum


def test_sfh_basis_removes_the_age_axis() -> None:
    csp = FakeCSP()
    state = fastpath.install_sfh_basis_fastpath(csp, "sfh-basis-sparse")

    assert state.basis_shape == (3, 4, 3, 7)
    assert state.basis_bytes == 3 * 4 * 3 * 7 * 4


def test_age_dependent_dust_is_rejected() -> None:
    csp = FakeCSP()
    csp.dust_attn = object()

    with pytest.raises(ValueError, match="age-dependent dust"):
        fastpath.install_sfh_basis_fastpath(csp, "corners")


def test_runtime_lookback_grid_is_rejected() -> None:
    csp = FakeCSP()
    fastpath.install_sfh_basis_fastpath(csp, "sfh-basis-sparse")
    parameters = {**theta(), "lookback_time": jnp.array([0.0, 1.0, 3.0, 6.0])}

    with pytest.raises(ValueError, match="runtime lookback grid"):
        csp.get_spectrum(parameters)
