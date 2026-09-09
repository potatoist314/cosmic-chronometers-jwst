"""Tests for the stacked-pull equations, units, limits and null values."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from plot_dr2_stacked_pull import (  # noqa: E402
    RECIPES,
    apply_recipe,
    bin_average,
    bin_native_pulls,
    bootstrap_sigma,
    inverse_variance_weights,
    reduced_chi2,
    stack_inverse_variance,
    stacked_mean_pull2,
    window_averages,
)

GRID = np.arange(4000.0, 4020.0, 2.0)


class TestBinning(unittest.TestCase):
    def test_pixels_land_in_the_nearest_bin(self):
        """A bin holds the pixels within half a bin width of its centre."""
        wave = np.array([3999.4, 4000.0, 4000.9, 4001.1, 4002.0])
        totals, squares, counts = bin_native_pulls(wave, np.ones(5), GRID)
        self.assertEqual(list(counts[:2]), [3.0, 2.0])
        self.assertEqual(list(totals[:2]), [3.0, 2.0])
        self.assertEqual(list(squares[:2]), [3.0, 2.0])

    def test_pixels_off_the_grid_are_dropped(self):
        """Wavelengths outside the grid contribute to no bin."""
        wave = np.array([100.0, 4000.0, 99999.0])
        _, _, counts = bin_native_pulls(wave, np.ones(3), GRID)
        self.assertEqual(counts.sum(), 1.0)

    def test_bin_average_is_the_mean_per_pixel(self):
        """The bin average divides the pull sum by the pixel count."""
        average = bin_average(np.array([6.0, 0.0]), np.array([3.0, 0.0]))
        self.assertAlmostEqual(average[0], 2.0)
        self.assertTrue(np.isnan(average[1]))


class TestNullValues(unittest.TestCase):
    def test_mean_pull2_null_is_one(self):
        """Standard-normal pulls stack to mean pull-squared 1, the null line."""
        rng = np.random.default_rng(42)
        pulls = rng.normal(0.0, 1.0, size=(200, 6, 40))
        squares = np.sum(pulls**2, axis=1)
        counts = np.full(squares.shape, 6.0)
        mean_pull2, n_cover = stacked_mean_pull2(squares, counts, min_cover=10)
        self.assertTrue(np.all(n_cover == 200))
        self.assertAlmostEqual(float(np.mean(mean_pull2)), 1.0, delta=0.02)

    def test_binning_does_not_change_mean_pull2(self):
        """Regression: the old regrid scaled sigma and pushed this below 1.

        Mean pull-squared per native pixel must not depend on the bin width,
        because binning only groups pixels that are already counted.
        """
        rng = np.random.default_rng(7)
        wave = np.linspace(4000.0, 4015.0, 600)
        pull = rng.normal(0.0, 1.0, size=wave.size)
        for grid_dl in (0.5, 2.0, 5.0):
            grid = np.arange(4000.0, 4020.0, grid_dl)
            _, squares, counts = bin_native_pulls(wave, pull, grid)
            mean_pull2, _ = stacked_mean_pull2(
                squares[None, :], counts[None, :], min_cover=1)
            self.assertAlmostEqual(
                float(np.nansum(squares) / np.nansum(counts)),
                float(np.mean(pull**2)), places=10)
            self.assertAlmostEqual(
                float(np.nanmean(mean_pull2)), float(np.mean(pull**2)), delta=0.35)

    def test_min_cover_gives_nan(self):
        """Bins below the cover threshold are NaN, so edges cannot fake signal."""
        counts = np.zeros((5, 4))
        counts[:, 0] = 1.0
        counts[:2, 1] = 1.0
        mean_pull2, n_cover = stacked_mean_pull2(counts.copy(), counts, min_cover=3)
        self.assertTrue(np.isfinite(mean_pull2[0]))
        self.assertTrue(np.all(np.isnan(mean_pull2[1:])))
        self.assertEqual(list(n_cover), [5, 2, 0, 0])

    def test_reduced_chi2(self):
        """Reduced chi-squared is the exact mean of squared pulls."""
        self.assertAlmostEqual(reduced_chi2(np.array([1.0, -1.0, 2.0])), 2.0)


class TestRecipes(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(11)
        self.values = rng.normal(0.4, 1.0, size=(400, 8))
        self.weights = np.ones_like(self.values)

    def test_every_recipe_recovers_a_coherent_offset(self):
        """All five recipes return the +0.4 offset the sample carries."""
        for name in RECIPES:
            stacked = apply_recipe(name, self.values, self.weights, min_cover=10)
            self.assertTrue(np.all(np.abs(stacked - 0.4) < 0.25), name)

    def test_robust_recipes_resist_one_bad_galaxy(self):
        """One extreme galaxy moves the mean far more than the robust recipes."""
        spoilt = self.values.copy()
        spoilt[0] = 500.0
        shift = {
            name: np.abs(apply_recipe(name, spoilt, self.weights, min_cover=10)
                         - apply_recipe(name, self.values, self.weights,
                                        min_cover=10)).max()
            for name in RECIPES
        }
        self.assertGreater(shift["Mean"], 1.0)
        for name in ("Median", "Sigma-clipped mean", "Biweight location"):
            self.assertLess(shift[name], 0.1, name)

    def test_inverse_variance_weighting_follows_the_weights(self):
        """A galaxy with twice the weight counts twice in the stack."""
        values = np.array([[1.0], [4.0]])
        weights = np.array([[2.0], [1.0]])
        stacked = stack_inverse_variance(values, weights)
        self.assertAlmostEqual(float(stacked[0]), 2.0)

    def test_weights_are_pixels_over_reduced_chi2(self):
        """The weight is the inverse of the estimated bin-average variance."""
        weights = inverse_variance_weights(np.array([[8.0, 0.0]]), np.array([2.0]))
        self.assertAlmostEqual(weights[0, 0], 4.0)
        self.assertAlmostEqual(weights[0, 1], 0.0)

    def test_uncovered_columns_stay_nan(self):
        """A column below min_cover is NaN for every recipe."""
        values = np.full((20, 2), np.nan)
        values[:, 0] = 1.0
        values[:3, 1] = 1.0
        for name in RECIPES:
            stacked = apply_recipe(name, values, np.ones_like(values), min_cover=10)
            self.assertTrue(np.isfinite(stacked[0]), name)
            self.assertTrue(np.isnan(stacked[1]), name)


class TestBootstrap(unittest.TestCase):
    def test_width_falls_as_one_over_root_n(self):
        """Four times the galaxies halves the bootstrap width of the mean."""
        rng = np.random.default_rng(3)
        small = rng.normal(0.0, 1.0, size=(50, 4))
        large = rng.normal(0.0, 1.0, size=(200, 4))
        sigma_small = bootstrap_sigma(
            "Mean", small, np.ones_like(small), n_boot=300, min_cover=5)
        sigma_large = bootstrap_sigma(
            "Mean", large, np.ones_like(large), n_boot=300, min_cover=5)
        ratio = float(np.mean(sigma_small) / np.mean(sigma_large))
        self.assertAlmostEqual(ratio, 2.0, delta=0.3)

    def test_width_matches_the_standard_error(self):
        """The bootstrap width of the mean matches sigma / sqrt(N)."""
        rng = np.random.default_rng(5)
        values = rng.normal(0.0, 2.0, size=(400, 3))
        sigma = bootstrap_sigma(
            "Mean", values, np.ones_like(values), n_boot=400, min_cover=10)
        self.assertAlmostEqual(float(np.mean(sigma)), 2.0 / np.sqrt(400), delta=0.02)


class TestWindows(unittest.TestCase):
    def setUp(self):
        self.wave = np.arange(3900.0, 4100.0, 0.5)
        self.pull = np.zeros_like(self.wave)
        self.windows = np.array([[3950.0, 3960.0], [4000.0, 4010.0]])

    def test_window_average_uses_only_its_own_pixels(self):
        """Each window averages the pulls inside its own edges."""
        self.pull[(self.wave >= 3950.0) & (self.wave <= 3960.0)] = 3.0
        per_window, continuum, n_window, _ = window_averages(
            self.wave, self.pull, self.windows)
        self.assertAlmostEqual(per_window[0], 3.0)
        self.assertAlmostEqual(per_window[1], 0.0)
        self.assertEqual(n_window[0], 21)
        self.assertAlmostEqual(continuum, 0.0)

    def test_continuum_excludes_every_window(self):
        """No pixel counts in both a window and the continuum."""
        self.pull[:] = 1.0
        _, _, n_window, n_continuum = window_averages(
            self.wave, self.pull, self.windows)
        self.assertEqual(n_continuum + int(n_window.sum()), self.wave.size)

    def test_thin_window_is_nan(self):
        """A window with too few fitted pixels reports NaN, not a noisy value."""
        per_window, _, _, _ = window_averages(
            np.array([3955.0, 3956.0]), np.zeros(2), self.windows, min_pixels=5)
        self.assertTrue(np.all(np.isnan(per_window)))


if __name__ == "__main__":
    unittest.main()
