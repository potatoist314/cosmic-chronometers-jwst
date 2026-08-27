from __future__ import annotations

from types import MethodType
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from scripts import benchmark_ceridwen_sfh_basis_fastpath as fastpath


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
        self.sfh_per_bin = False
        self.theta_init = {
            "sfh": jnp.ones(4),
            "Z": jnp.array([-0.7]),
            "afe": jnp.array([0.0]),
            "tau": jnp.array([0.1]),
        }
        self.zh_const = True
        self.sfh_interp = "step"
        self.track_zred_age = False
        self.get_spectrum = MethodType(
            FakeCSP.get_spectrum_dattn_nodem_noneb,
            self,
        )

    def calculate_ssp_weights(self, theta: dict[str, jax.Array]) -> jax.Array:
        sfh = jnp.clip(theta["sfh"], 1e-30, None)
        sfh_mid = 0.5 * (sfh[:-1] + sfh[1:])
        age_weights = sfh_mid @ fastpath._build_bin_to_age_operator(self)
        z_upper, z_fraction = fastpath._bracket(self.zmet, theta["Z"])
        weights = jnp.zeros(
            (self.zmet.size, age_weights.size),
            dtype=jnp.float32,
        )
        weights = weights.at[z_upper - 1].add(
            (1.0 - z_fraction) * age_weights
        )
        return weights.at[z_upper].add(z_fraction * age_weights)

    def attenuate_dust(
        self,
        wave: jax.Array,
        theta: dict[str, jax.Array],
    ) -> tuple[jax.Array, jax.Array]:
        diffuse = jnp.ravel(theta["tau"])[0] * (wave / wave.mean())
        return jnp.zeros((1, wave.size)), diffuse

    def _flux_at_afe(self, theta: dict[str, jax.Array]) -> jax.Array:
        upper, fraction = fastpath._bracket(self.afe_grid, theta["afe"])
        return (
            (1.0 - fraction) * self.flux[upper - 1]
            + fraction * self.flux[upper]
        )

    def get_spectrum_dattn_nodem_noneb(
        self,
        theta: dict[str, jax.Array],
        *,
        include_lines: Any = None,
    ) -> jax.Array:
        del include_lines
        flux = self._flux_at_afe(theta)
        weights = self.calculate_ssp_weights(theta).astype(jnp.float32)
        spectrum = jnp.einsum("za,zaw->w", weights, flux)
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


@pytest.mark.parametrize("mode", ["four-corner", "sfh-basis"])
def test_fastpath_matches_dense_spectrum_and_gradient(mode: str) -> None:
    csp = FakeCSP()
    parameters = theta()
    original = csp.get_spectrum
    baseline = jax.jit(csp.get_spectrum)(parameters)
    baseline_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(parameters)

    handle = fastpath.install_fastpath(csp, mode)
    actual = jax.jit(csp.get_spectrum)(parameters)
    actual_gradient = jax.grad(
        lambda values: jnp.sum(csp.get_spectrum(values))
    )(parameters)
    fastpath.restore_fastpath(csp, handle)

    assert_tree_close(baseline, actual)
    assert_tree_close(baseline_gradient, actual_gradient)
    assert csp.get_spectrum == original


def test_sfh_basis_removes_the_age_axis() -> None:
    csp = FakeCSP()
    handle = fastpath.install_fastpath(csp, "sfh-basis")

    assert handle.basis_shape == (3, 4, 3, 7)
    assert handle.basis_nbytes == 3 * 4 * 3 * 7 * 4


def test_age_dependent_dust_is_rejected() -> None:
    csp = FakeCSP()
    csp.dust_attn = object()

    with pytest.raises(fastpath.FastPathError, match="age-dependent dust"):
        fastpath.install_fastpath(csp, "four-corner")
