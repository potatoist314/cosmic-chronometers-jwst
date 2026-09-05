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


if __name__ == "__main__":
    unittest.main()
