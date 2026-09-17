"""Equations, limiting cases and bookkeeping of the per-galaxy diagnostics."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import per_galaxy_diagnostics as pgd  # noqa: E402
from build_dr2_quiescent_summary import formation_times  # noqa: E402

EDGES = np.array([0.0, 1.0, 2.0, 3.0])


class FormationTimes(unittest.TestCase):
    def test_burst_in_one_bin(self):
        # All mass in the oldest bin: every t_X lies inside [2, 3] Gyr, older X first.
        tx = pgd.formation_lookback_times(EDGES, np.array([[0.0, 0.0, 1.0]]))
        self.assertAlmostEqual(float(tx[0.10][0]), 2.9)
        self.assertAlmostEqual(float(tx[0.50][0]), 2.5)
        self.assertAlmostEqual(float(tx[0.90][0]), 2.1)

    def test_uniform_sfh_is_linear(self):
        # Constant SFR over 3 Gyr: the mass formed before lookback t is 1 - t/3.
        tx = pgd.formation_lookback_times(EDGES, np.array([[1 / 3, 1 / 3, 1 / 3]]))
        for level, draws in tx.items():
            self.assertAlmostEqual(float(draws[0]), 3.0 * (1.0 - level))

    def test_ordering_over_draws(self):
        fracs = np.array([[1.0, 0.0, 0.0], [0.0, 0.5, 0.5], [0.2, 0.3, 0.5]])
        tx = pgd.formation_lookback_times(EDGES, fracs)
        self.assertTrue(np.all(tx[0.10] >= tx[0.20]))
        self.assertTrue(np.all(tx[0.20] >= tx[0.50]))
        self.assertTrue(np.all(tx[0.50] >= tx[0.80]))
        self.assertTrue(np.all(tx[0.80] >= tx[0.90]))

    def test_mirrors_project_summary_convention(self):
        # summary t20 (20 percent younger) == diagnostics t80 (80 percent older), etc.
        rng = np.random.default_rng(3)
        fracs = rng.dirichlet(np.ones(3), size=50)
        t20, t50, t80 = formation_times(EDGES, fracs)
        tx = pgd.formation_lookback_times(EDGES, fracs, levels=(0.2, 0.5, 0.8))
        np.testing.assert_allclose(tx[0.8], t20)
        np.testing.assert_allclose(tx[0.5], t50)
        np.testing.assert_allclose(tx[0.2], t80)

    def test_cumulative_curve_matches_t_x(self):
        fracs = np.array([[0.2, 0.3, 0.5]])
        grid = np.linspace(0.0, 3.0, 3001)
        older = pgd.cumulative_mass_older_than(EDGES, fracs, grid)[0]
        self.assertAlmostEqual(float(older[0]), 1.0)
        self.assertAlmostEqual(float(older[-1]), 0.0)
        t50 = float(pgd.formation_lookback_times(EDGES, fracs, levels=(0.5,))[0.5][0])
        self.assertAlmostEqual(float(np.interp(t50, grid, older)), 0.5, places=3)


class ChiSquared(unittest.TestCase):
    def test_contributions_sum_and_mask(self):
        pull = np.array([1.0, -2.0, 3.0, 100.0])
        mask = np.array([True, True, True, False])
        out = pgd.chi2_contributions(pull, mask)
        self.assertEqual(out["n"], 3)
        self.assertAlmostEqual(out["total"], 14.0)
        self.assertAlmostEqual(float(out["cumulative"][-1]), 14.0)
        self.assertAlmostEqual(float(out["cumulative_fraction"][-1]), 1.0)
        self.assertEqual(float(out["contribution"][3]), 0.0)

    def test_binned_mean_pull2_unit_noise(self):
        rng = np.random.default_rng(1)
        wave = np.linspace(6000.0, 9000.0, 6001)
        pull = rng.standard_normal(wave.size)
        mask = np.ones(wave.size, dtype=bool)
        edges, mean, counts = pgd.binned_mean_pull2(wave, pull, mask, width=250.0)
        self.assertEqual(len(mean), len(edges) - 1)
        self.assertEqual(int(counts.sum()), wave.size)
        self.assertAlmostEqual(float(np.nanmean(mean)), 1.0, delta=0.1)


class Priors(unittest.TestCase):
    def test_parse_uniform_json_and_repr_round_trip(self):
        uniform = pgd.parse_prior('{"type": "Uniform", "low": -3.0, "high": 3.0, "name": ""}')
        self.assertEqual(type(uniform).__name__, "Uniform")
        self.assertEqual(pgd.describe_prior(uniform), "Uniform(-3, 3)")
        clipped = pgd.parse_prior("ClippedNormal(mean=1.0, sigma=0.3, low=0.2, high=3.0)")
        self.assertEqual(type(clipped).__name__, "ClippedNormal")
        self.assertEqual(pgd.describe_prior(clipped), "ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3)")
        self.assertEqual(pgd.describe_prior(pgd.parse_prior(repr(clipped))), pgd.describe_prior(clipped))

    def test_unknown_prior_text_is_rejected(self):
        with self.assertRaises(ValueError):
            pgd.parse_prior("not a prior")


class ImfNames(unittest.TestCase):
    def test_kroupa_code(self):
        self.assertEqual(pgd.IMF_NAMES[2], "Kroupa (2001)")


class RebuildCalibratedModel(unittest.TestCase):
    """The rebuilt likelihood of a calibration-polynomial fit reproduces the stored ln L."""

    FOLDER = PROJECT_ROOT / "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989"

    def test_max_likelihood_theta_reproduces_stored_lnl(self):
        if not (self.FOLDER / "ceridwen_result.h5").exists():
            self.skipTest("poly3_total fit not present")
        import os
        os.environ.setdefault("JAX_PLATFORMS", "cpu")
        galaxy = pgd.load_galaxy(self.FOLDER)
        try:
            ssp = pgd.load_ssp()
        except Exception as error:  # grid not fetched on this machine
            self.skipTest(f"grid unavailable: {error}")
        model, likelihood, _ = pgd.rebuild_model(galaxy, ssp)
        index = pgd.max_likelihood_index(galaxy)
        terms = pgd.likelihood_terms(model, likelihood, pgd.theta_at(galaxy, index))
        # The stored value comes from the GPU fit; float32 photometry and a
        # 3735-pixel Gaussian sum agree to a few 1e-4 in ln L ~ 2.4e5.
        self.assertAlmostEqual(terms["lnl"] / galaxy.log_likelihoods[index], 1.0, places=5)
        self.assertEqual(terms["spectrum"]["ndof"], int(galaxy.spec["mask"].sum()))


class RebuildFreeDustModel(unittest.TestCase):
    """A fit with a sampled dust index rebuilds with that index free, not transformed."""

    FOLDER = Path(__import__("os").environ.get(
        "PGD_FREE_DUST_FOLDER",
        PROJECT_ROOT / "results/fit-accuracy-knobs/dust_free/108989-M4_108989"))

    def test_free_dust_index_reproduces_stored_lnl(self):
        if not (self.FOLDER / "ceridwen_result.h5").exists():
            self.skipTest("dust_free fit not present")
        import os
        os.environ.setdefault("JAX_PLATFORMS", "cpu")
        galaxy = pgd.load_galaxy(self.FOLDER)
        self.assertIn("diffuse_dust_index", galaxy.theta_init)
        try:
            ssp = pgd.load_ssp()
        except Exception as error:
            self.skipTest(f"grid unavailable: {error}")
        model, likelihood, _ = pgd.rebuild_model(galaxy, ssp)
        self.assertNotIn("diffuse_dust_index", model.transforms)
        index = pgd.max_likelihood_index(galaxy)
        terms = pgd.likelihood_terms(model, likelihood, pgd.theta_at(galaxy, index))
        self.assertAlmostEqual(terms["lnl"] / galaxy.log_likelihoods[index], 1.0, places=5)



class MarginalKL(unittest.TestCase):
    """D_KL(posterior || prior) per parameter against closed forms, in bits."""

    PRIOR = '{"type": "Uniform", "low": 0.0, "high": 10.0, "name": ""}'

    def kl(self, draws, prior_text=None):
        prior = pgd.parse_prior(prior_text or self.PRIOR)
        return pgd.marginal_kl_bits(pgd.prior_unit_values(draws, prior), np.ones(len(draws)))

    def test_gaussian_under_uniform(self):
        # log2(W) - 0.5 log2(2 pi e s^2) for a Gaussian well inside a Uniform of width W.
        sigma = 0.05
        draws = np.random.default_rng(1).normal(5.0, sigma, 40000)
        expected = np.log2(10.0) - 0.5 * np.log2(2 * np.pi * np.e * sigma**2)
        self.assertAlmostEqual(self.kl(draws), expected, delta=0.03)

    def test_posterior_equal_to_prior_is_zero(self):
        draws = np.random.default_rng(2).uniform(0.0, 10.0, 40000)
        self.assertAlmostEqual(self.kl(draws), 0.0, delta=0.01)
        draws = 0.3 * np.random.default_rng(3).standard_t(2.0, 40000)
        self.assertAlmostEqual(self.kl(draws, "StudentT(mean=0.0, scale=0.3, df=2.0)"), 0.0, delta=0.01)

    def test_railing_at_the_prior_edge(self):
        # Posterior flat over the top tenth of the prior: log2(10) bits.
        draws = np.random.default_rng(4).uniform(9.0, 10.0, 40000)
        self.assertAlmostEqual(self.kl(draws), np.log2(10.0), delta=0.01)

    def test_weights_match_resampling(self):
        # Prior draws weighted by a Gaussian likelihood equal the Gaussian posterior.
        draws = np.random.default_rng(5).uniform(0.0, 10.0, 400000)
        weights = np.exp(-0.5 * ((draws - 5.0) / 0.2) ** 2)
        prior = pgd.parse_prior(self.PRIOR)
        expected = np.log2(10.0) - 0.5 * np.log2(2 * np.pi * np.e * 0.2**2)
        self.assertAlmostEqual(pgd.marginal_kl_bits(pgd.prior_unit_values(draws, prior), weights), expected, delta=0.03)


def synthetic_galaxy(z=0.7, n=400):
    """The fields the spectrum figures read, with 40 unusable and 60 masked pixels."""
    from types import SimpleNamespace

    wave = np.linspace(6300.0, 8800.0, n)
    model = 3e-28 * (1 + 0.1 * np.sin(wave / 90.0))
    uncertainty = np.full(n, 1e-29)
    uncertainty[:40] = pgd.INVALID_PIXEL_UNCERTAINTY
    mask = np.ones(n, bool)
    mask[:100] = False
    observed = np.where(uncertainty == pgd.INVALID_PIXEL_UNCERTAINTY, 0.0, model)
    filters = ["subaru_suprimecam_rp", "subaru_suprimecam_ip", "subaru_suprimecam_zp"]
    return SimpleNamespace(
        spect_id="M0_0", z=z, spec={"wavelength": wave},
        phot={"filters": filters, "flux": np.ones(3), "uncertainty": np.full(3, 0.1), "mask": np.ones(3, bool)},
        derived_spec={"observed": observed, "uncertainty": uncertainty, "effective_uncertainty": uncertainty,
                      "mask": mask, "posterior_q16": 0.99 * model, "posterior_q50": model,
                      "posterior_q84": 1.01 * model, "pull": np.zeros(n)})


class SpectrumFigures(unittest.TestCase):
    """The redrawn notebook figures carry the absorption-feature windows and one legend."""

    def feature_windows_on(self, ax):
        return sorted((p.get_x(), p.get_x() + p.get_width()) for p in ax.patches
                      if (p.get_gid() or "").startswith("absorption-feature:"))

    def check(self, plot):
        import matplotlib.pyplot as plt
        from ceridwen.observation.absorption_features import feature_windows
        from spectral_figures import MARKED_FEATURES

        galaxy = synthetic_galaxy()
        fig = plot(galaxy)
        lower, upper = fig.axes[0].get_xlim()
        expected = sorted((lo, hi) for lo, hi in feature_windows([n for n, _ in MARKED_FEATURES], zred=galaxy.z)
                          if hi >= lower and lo <= upper)
        self.assertTrue(expected)
        for ax in fig.axes[:2]:
            np.testing.assert_allclose(self.feature_windows_on(ax), expected)
        titles = [legend.get_title().get_text() for legend in fig.legends]
        self.assertEqual(titles.count("Absorption features"), 1)
        plt.close(fig)
        return fig

    def test_fit_spectrum(self):
        fig = self.check(pgd.plot_fit_spectrum)
        excluded = fig.axes[0].collections[0].get_offsets()
        self.assertEqual(len(excluded), 60)      # usable pixels outside the fit mask
        fitted = fig.axes[0].lines[0].get_ydata()
        self.assertEqual(int(np.isfinite(fitted).sum()), 300)

    def test_predictive_spectrum(self):
        self.check(pgd.plot_predictive_spectrum)


if __name__ == "__main__":
    unittest.main()
