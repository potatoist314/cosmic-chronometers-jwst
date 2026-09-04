"""Tests for the stacked-pull diagnostic equations and edge cases."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from plot_dr2_stacked_pull import (  # noqa: E402
    GRID_DL,
    reduced_chi2,
    regrid_galaxy,
    stack_pulls,
)


class TestStackedPull(unittest.TestCase):
    def test_null_expectation_is_one(self):
        """Mean pull-squared of standard-normal pulls is ~1 (null line)."""
        rng = np.random.default_rng(42)
        pulls = rng.normal(0.0, 1.0, size=(200, 50))
        mean_pull2, median, _, _, n_cover = stack_pulls(pulls, min_cover=10)
        self.assertTrue(np.all(n_cover == 200))
        self.assertAlmostEqual(float(np.mean(mean_pull2)), 1.0, delta=0.1)
        self.assertAlmostEqual(float(np.mean(median)), 0.0, delta=0.1)

    def test_equal_weighting(self):
        """One galaxy's pull shifts the bin mean by 1/N (equal weights)."""
        pulls = np.zeros((10, 5))
        pulls[0, 2] = 10.0
        mean_pull2, _, _, _, n_cover = stack_pulls(pulls, min_cover=2)
        self.assertEqual(n_cover[2], 10)
        self.assertAlmostEqual(mean_pull2[2], 10.0)

    def test_min_cover_gives_nan(self):
        """Bins below the cover threshold are NaN (no edge artefacts)."""
        pulls = np.full((5, 4), np.nan)
        pulls[:, 0] = 1.0
        pulls[:2, 1] = 1.0
        mean_pull2, median, q16, q84, n_cover = stack_pulls(
            pulls, min_cover=3)
        self.assertTrue(np.isfinite(mean_pull2[0]))
        for arr in (mean_pull2[1:], median[1:], q16[1:], q84[1:]):
            self.assertTrue(np.all(np.isnan(arr)))
        self.assertEqual(list(n_cover), [5, 2, 0, 0])

    def test_error_scales_with_bin_width_ratio(self):
        """Regridded sigma scales by sqrt(new/native bin width)."""
        wave = np.arange(5000.0, 5100.0, 0.5)
        n = len(wave)
        grid = np.arange(5000.0, 5100.0, GRID_DL)
        _, _, sig, covered = regrid_galaxy(
            wave, np.ones(n), np.ones(n), np.ones(n),
            np.ones(n, dtype=bool), grid)
        self.assertTrue(bool(np.all(covered)))
        self.assertAlmostEqual(float(sig[0]), np.sqrt(GRID_DL / 0.5))

    def test_masked_pixels_not_covered(self):
        """Fully masked regions report uncovered (NaN downstream)."""
        wave = np.arange(5000.0, 5100.0, 0.5)
        n = len(wave)
        mask = np.ones(n, dtype=bool)
        mask[50:150] = False
        _, _, _, covered = regrid_galaxy(
            wave, np.ones(n), np.ones(n), np.ones(n), mask,
            np.arange(5000.0, 5100.0, GRID_DL))
        self.assertFalse(bool(np.all(covered)))
        self.assertTrue(bool(np.any(covered)))

    def test_reduced_chi2(self):
        """Reduced chi-squared is the exact mean of squared pulls."""
        self.assertAlmostEqual(reduced_chi2(np.array([1.0, -1.0, 2.0])), 2.0)

    def test_median_tracks_systematic_shift(self):
        """A coherent +0.5 pull offset appears in the median band."""
        rng = np.random.default_rng(7)
        pulls = rng.normal(0.5, 1.0, size=(100, 20))
        _, median, q16, q84, _ = stack_pulls(pulls, min_cover=10)
        self.assertTrue(bool(np.all(median > 0.2)))
        self.assertTrue(bool(np.all(q16 < median)) and bool(np.all(median < q84)))


if __name__ == "__main__":
    unittest.main()
