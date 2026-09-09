"""Stacked pull diagnostics for large DR2 runs.

Pull is ``(observed - posterior_q50) / effective_uncertainty`` on the fitted
(masked) native spectrum pixels of each galaxy's
``ceridwen_derived_outputs.h5``.  Wavelengths shift to rest frame (observed
divided by 1+z) because template mismatch lives in rest frame, while
sky-subtraction residuals live in observed frame and wash out here.

Binning: every fitted native pixel is assigned to the rest-frame bin it falls
in, and the bin sums the pixels it received.  Nothing is interpolated and no
error is rescaled, so the two stacked quantities keep their null values.

- ``mean pull^2`` per bin averages ``pull^2`` over all native pixels of all
  galaxies in the bin.  Its null expectation is exactly 1 for any pixel-to-pixel
  noise correlation, so the line at 1 is the reference for the chi-squared
  panel.
- ``mean pull`` per bin is a per-galaxy average over that galaxy's native
  pixels in the bin.  Its null expectation is 0.  Its null width depends on how
  strongly neighbouring pixels correlate, so the width comes from a bootstrap
  over galaxies rather than from an assumed value.

Five stacking recipes combine the per-galaxy bin averages:

1. mean, equal weight per galaxy;
2. median, equal weight per galaxy;
3. inverse-variance weighted mean, weight ``n_pix / chi2_red`` per galaxy and
   bin, the inverse of the estimated variance of that galaxy's bin average;
4. sigma-clipped mean, 3 sigma and 5 iterations (``astropy.stats``);
5. biweight location, Beers, Flynn & Gebhardt (1990), AJ 100, 32
   (``astropy.stats.biweight_location``, tuning constant 6).

Three figures:

- ``stacked-pull``: mean pull-squared per bin against the null line at 1,
  median pull per bin with a 16-84 percent galaxy band, and a histogram of
  per-galaxy reduced chi-squared on native pixels.
- ``stacked-pull-recipes``: one panel per recipe, each with the bootstrap
  1-sigma band around zero.
- ``stacked-pull-by-feature``: the stacked pull inside each labelled
  absorption window and in the continuum between the windows, one point per
  feature per recipe.

Absorption windows come from ``scripts/spectral_figures.py``.  They are the
known Lick/IDS features of a quiescent sample.  This script never searches for
a line.

Reuse: ``ceridwen/.venv/bin/python scripts/plot_dr2_stacked_pull.py
[--run-dir DIR] [--summary CSV] [--out-dir DIR] [--n-boot N]``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.stats import biweight_location, sigma_clipped_stats
from matplotlib import rcParams
from matplotlib.lines import Line2D

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from spectral_figures import (  # noqa: E402
    MARKED_FEATURES,
    mark_absorption_features,
)

from ceridwen.observation.absorption_features import feature_windows  # noqa: E402

DEFAULT_RUN_DIR = PROJECT_ROOT / "results/dr2-quiescent-new-defaults"
DEFAULT_SUMMARY = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
DEFAULT_OUT_DIR = PROJECT_ROOT / "wiki/analyses/dr2-quiescent-sample"

GRID_LO, GRID_HI, GRID_DL = 2900.0, 5950.0, 2.0
MIN_COVER = 10  # galaxies a bin needs before it is plotted
MIN_WINDOW_PIX = 5  # native pixels a galaxy needs inside a feature window
WINDOW_KMS = 1000.0  # half-width of a line window, matches the fits
SIGMA_CLIP, CLIP_ITERS = 3.0, 5
BIWEIGHT_C = 6.0
N_BOOT, BOOT_SEED = 400, 20260909

# Okabe-Ito, readable for the common colour-vision deficiencies.
BLUE, ORANGE, GREEN, PINK, SKY = (
    "#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9")
RECIPE_STYLE = {
    "Mean": (BLUE, "o"),
    "Median": (ORANGE, "s"),
    "Inverse-variance": (GREEN, "^"),
    "Sigma-clipped mean": (PINK, "D"),
    "Biweight location": (SKY, "v"),
}

rcParams.update(
    {
        "font.size": 9,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "savefig.dpi": 150,
    }
)


def bin_native_pulls(wave_rest, pull, grid):
    """Sum native pulls into the grid bin each pixel falls in.

    ``wave_rest`` and ``pull`` cover the fitted pixels only.  Bins are centred
    on ``grid``, so bin ``b`` holds the pixels within half a bin width of
    ``grid[b]``.  Pixels outside the grid are dropped.  Returns
    ``(sum_pull, sum_pull2, n_pix)``, each of length ``len(grid)``.
    """
    grid = np.asarray(grid, dtype=float)
    grid_dl = float(grid[1] - grid[0])
    index = np.rint((np.asarray(wave_rest, dtype=float) - grid[0]) / grid_dl)
    index = index.astype(int)
    inside = (index >= 0) & (index < len(grid))
    index = index[inside]
    values = np.asarray(pull, dtype=float)[inside]
    n_bins = len(grid)
    return (
        np.bincount(index, weights=values, minlength=n_bins),
        np.bincount(index, weights=values**2, minlength=n_bins),
        np.bincount(index, minlength=n_bins).astype(float),
    )


def bin_average(sum_pull, n_pix):
    """Mean native pull per pixel, NaN where the galaxy has no pixel."""
    n_pix = np.asarray(n_pix, dtype=float)
    out = np.full(n_pix.shape, np.nan)
    filled = n_pix > 0
    out[filled] = np.asarray(sum_pull, dtype=float)[filled] / n_pix[filled]
    return out


def stacked_mean_pull2(sum_pull2, n_pix, min_cover=MIN_COVER):
    """Mean pull-squared over every native pixel of every galaxy in the bin.

    ``sum_pull2`` and ``n_pix`` are (n_galaxies, n_bins).  Returns
    ``(mean_pull2, n_cover)`` with NaN where fewer than ``min_cover``
    galaxies reach the bin.  The null expectation of ``mean_pull2`` is 1.
    """
    n_pix = np.asarray(n_pix, dtype=float)
    n_cover = np.sum(n_pix > 0, axis=0)
    total_pix = np.sum(n_pix, axis=0)
    out = np.full(n_pix.shape[1], np.nan)
    ok = (n_cover >= min_cover) & (total_pix > 0)
    out[ok] = np.sum(np.asarray(sum_pull2, dtype=float), axis=0)[ok] / total_pix[ok]
    return out, n_cover


def reduced_chi2(pull_native):
    """Mean pull-squared over fitted native pixels."""
    pull_native = np.asarray(pull_native, dtype=float)
    return float(np.mean(pull_native**2))


def stack_mean(values, weights=None):
    """Equal-weight mean over galaxies."""
    return np.nanmean(values, axis=0)


def stack_median(values, weights=None):
    """Equal-weight median over galaxies."""
    return np.nanmedian(values, axis=0)


def stack_inverse_variance(values, weights):
    """Weighted mean over galaxies with the supplied inverse-variance weights."""
    weights = np.where(np.isfinite(values), np.asarray(weights, dtype=float), np.nan)
    return np.nansum(weights * values, axis=0) / np.nansum(weights, axis=0)


def stack_sigma_clipped(values, weights=None):
    """Mean over galaxies after 3-sigma clipping."""
    mean, _, _ = sigma_clipped_stats(
        np.ma.masked_invalid(values), axis=0, sigma=SIGMA_CLIP, maxiters=CLIP_ITERS
    )
    return np.ma.filled(np.ma.masked_invalid(mean), np.nan)


def stack_biweight(values, weights=None):
    """Biweight location over galaxies (Beers, Flynn & Gebhardt 1990)."""
    return np.asarray(
        biweight_location(values, axis=0, c=BIWEIGHT_C, ignore_nan=True), dtype=float
    )


RECIPES = {
    "Mean": stack_mean,
    "Median": stack_median,
    "Inverse-variance": stack_inverse_variance,
    "Sigma-clipped mean": stack_sigma_clipped,
    "Biweight location": stack_biweight,
}


def apply_recipe(recipe, values, weights, min_cover=MIN_COVER):
    """Run one recipe over galaxies, on the columns that clear ``min_cover``.

    Columns below the threshold are NaN.  They are dropped before the recipe
    runs, so an empty column never reaches the estimator.
    """
    values = np.asarray(values, dtype=float)
    keep = np.sum(np.isfinite(values), axis=0) >= min_cover
    out = np.full(values.shape[1], np.nan)
    if not keep.any():
        return out
    out[keep] = RECIPES[recipe](values[:, keep], np.asarray(weights)[:, keep])
    return out


def bootstrap_sigma(recipe, values, weights, n_boot=N_BOOT, seed=BOOT_SEED,
                    min_cover=MIN_COVER):
    """1-sigma width of a recipe from resampling galaxies with replacement.

    Galaxies are independent objects, so this width absorbs both the noise and
    the pixel-to-pixel correlation inside a bin.
    """
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    rng = np.random.default_rng(seed)
    n_gal = values.shape[0]
    draws = np.empty((n_boot, values.shape[1]))
    for k in range(n_boot):
        pick = rng.integers(0, n_gal, n_gal)
        draws[k] = apply_recipe(recipe, values[pick], weights[pick], min_cover)
    sigma = np.full(values.shape[1], np.nan)
    keep = np.sum(np.isfinite(draws), axis=0) > 1
    sigma[keep] = np.nanstd(draws[:, keep], axis=0, ddof=1)
    return sigma


def window_averages(wave_rest, pull, windows, min_pixels=MIN_WINDOW_PIX):
    """Mean native pull inside each window, and in the continuum outside all.

    Returns ``(per_window, continuum, n_window, n_continuum)``.  The continuum
    covers the fitted pixels between ``GRID_LO`` and ``GRID_HI`` that no window
    contains.  A window with fewer than ``min_pixels`` fitted pixels is NaN.
    """
    wave_rest = np.asarray(wave_rest, dtype=float)
    pull = np.asarray(pull, dtype=float)
    on_grid = (wave_rest >= GRID_LO) & (wave_rest <= GRID_HI)
    inside_any = np.zeros(wave_rest.shape, dtype=bool)
    per_window = np.full(len(windows), np.nan)
    n_window = np.zeros(len(windows), dtype=int)
    for k, (lower, upper) in enumerate(windows):
        selected = on_grid & (wave_rest >= lower) & (wave_rest <= upper)
        inside_any |= selected
        n_window[k] = int(selected.sum())
        if n_window[k] >= min_pixels:
            per_window[k] = float(np.mean(pull[selected]))
    continuum_pixels = on_grid & ~inside_any
    n_continuum = int(continuum_pixels.sum())
    continuum = (float(np.mean(pull[continuum_pixels]))
                 if n_continuum >= min_pixels else np.nan)
    return per_window, continuum, n_window, n_continuum


def load_run(run_dir, summary_path, grid, windows):
    """Read every summary galaxy that has derived outputs.

    Returns a dict of stacked inputs: per-galaxy bin averages, per-bin pixel
    counts and squared-pull sums, per-galaxy reduced chi-squared, and the
    per-galaxy feature-window and continuum averages.
    """
    import h5py

    galaxies = pd.read_csv(summary_path)
    n_gal, n_bins = len(galaxies), len(grid)
    n_feat = len(windows)
    sum_pull2 = np.zeros((n_gal, n_bins))
    n_pix = np.zeros((n_gal, n_bins))
    averages = np.full((n_gal, n_bins), np.nan)
    redchi2 = np.full(n_gal, np.nan)
    feature_avg = np.full((n_gal, n_feat), np.nan)
    feature_pix = np.zeros((n_gal, n_feat))
    continuum_avg = np.full(n_gal, np.nan)
    continuum_pix = np.zeros(n_gal)
    used = np.zeros(n_gal, dtype=bool)
    for i, target in enumerate(galaxies["target"]):
        path = Path(run_dir) / str(target) / "ceridwen_derived_outputs.h5"
        if not path.exists():
            continue
        with h5py.File(path, "r") as f:
            zred = float(f.attrs["redshift"])
            spec = f["spectrum"]
            mask = np.asarray(spec["mask"], dtype=bool)
            wave = np.asarray(spec["wavelength"], dtype=float)[mask] / (1.0 + zred)
            observed = np.asarray(spec["observed"], dtype=float)[mask]
            model = np.asarray(spec["posterior_q50"], dtype=float)[mask]
            sigma = np.asarray(spec["effective_uncertainty"], dtype=float)[mask]
        pull = (observed - model) / sigma
        totals, squares, counts = bin_native_pulls(wave, pull, grid)
        sum_pull2[i] = squares
        n_pix[i] = counts
        averages[i] = bin_average(totals, counts)
        redchi2[i] = reduced_chi2(pull)
        (feature_avg[i], continuum_avg[i],
         feature_pix[i], continuum_pix[i]) = window_averages(wave, pull, windows)
        used[i] = True
    return {
        "targets": np.asarray(galaxies["target"])[used],
        "averages": averages[used],
        "sum_pull2": sum_pull2[used],
        "n_pix": n_pix[used],
        "redchi2": redchi2[used],
        "feature_avg": feature_avg[used],
        "feature_pix": feature_pix[used],
        "continuum_avg": continuum_avg[used],
        "continuum_pix": continuum_pix[used],
    }


def inverse_variance_weights(n_pix, redchi2):
    """Weight each galaxy and bin by the inverse of its estimated variance.

    A galaxy's bin average of ``n`` native pulls has variance about
    ``chi2_red / n``, so the weight is ``n / chi2_red``.  Zero-pixel bins get
    weight zero.
    """
    scatter = np.asarray(redchi2, dtype=float)[:, None]
    return np.asarray(n_pix, dtype=float) / np.where(scatter > 0, scatter, np.nan)


def stack_all_recipes(values, weights, n_boot, min_cover=MIN_COVER):
    """Every recipe and its bootstrap width, keyed by recipe name."""
    return {
        name: (
            apply_recipe(name, values, weights, min_cover),
            bootstrap_sigma(name, values, weights, n_boot, min_cover=min_cover),
        )
        for name in RECIPES
    }


def _label_axes(axes, labelled_axis, xlabel):
    """Shade the absorption windows on every panel, name them under one."""
    for axis in axes:
        axis.set_xlim(axis.get_xlim())
        mark_absorption_features(
            axis,
            0.0,
            show_labels=axis is labelled_axis,
            window_kms=WINDOW_KMS,
            xlabel=xlabel if axis is labelled_axis else None,
        )


def figure_overview(grid, mean_pull2, averages, redchi2, n_used, out_dir):
    """Stacked chi-squared, median pull and the per-galaxy chi-squared histogram."""
    keep = np.sum(np.isfinite(averages), axis=0) >= MIN_COVER
    median = np.full(len(grid), np.nan)
    q16, q84 = median.copy(), median.copy()
    median[keep] = np.nanmedian(averages[:, keep], axis=0)
    q16[keep] = np.nanquantile(averages[:, keep], 0.16, axis=0)
    q84[keep] = np.nanquantile(averages[:, keep], 0.84, axis=0)

    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4),
                             gridspec_kw={"width_ratios": [1.4, 1.4, 1.0]})
    axes[0].plot(grid, mean_pull2, color=BLUE, lw=1.0)
    axes[0].axhline(1.0, color="black", lw=1.0, ls="--")
    axes[0].set_ylabel(r"Mean pull$^2$ per native pixel")
    axes[0].set_title("Stacked $\\chi^2$", fontsize=10)
    axes[1].plot(grid, median, color=BLUE, lw=1.0, label="Median")
    axes[1].fill_between(grid, q16, q84, color=BLUE, alpha=0.25,
                         linewidth=0, label="16-84% of galaxies")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--")
    axes[1].set_ylabel("Mean pull per native pixel")
    axes[1].legend(frameon=False, fontsize=7.5)
    axes[1].set_title("Median pull", fontsize=10)
    finite = redchi2[np.isfinite(redchi2)]
    axes[2].hist(finite, bins=25, color=BLUE, alpha=0.7,
                 edgecolor="white", linewidth=0.5)
    axes[2].axvline(1.0, color="black", lw=1.0, ls="--")
    axes[2].set_xlabel(r"Per-galaxy reduced $\chi^2$")
    axes[2].set_ylabel("Galaxies")
    axes[2].set_title(f"Fit quality (N={len(finite)})", fontsize=10)
    for axis in axes[:2]:
        _label_axes([axis], axis, r"Rest wavelength [$\mathrm{\AA}$]")
    fig.suptitle(
        f"Ceridwen DR2 stacked pulls, rest frame (N={n_used} galaxies, "
        f"bins with >={MIN_COVER} galaxies shown)", fontsize=10)
    caption = (
        "Native pixels go into rest-frame bins with no interpolation, so the "
        "line at 1 is the null expectation of mean pull$^2$."
    )
    fig.text(0.5, 0.005, caption, ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 0.9))
    _save(fig, out_dir, "stacked-pull")


def figure_recipes(grid, stacks, n_used, out_dir):
    """One panel per stacking recipe, each with its bootstrap 1-sigma band."""
    span = np.nanmax([np.nanmax(np.abs(stacked)) for stacked, _ in stacks.values()])
    fig, axes = plt.subplots(len(stacks), 1, figsize=(9.0, 11.0), sharex=True,
                             sharey=True)
    for axis, (name, (stacked, sigma)) in zip(axes, stacks.items(), strict=True):
        colour, _ = RECIPE_STYLE[name]
        axis.fill_between(grid, -sigma, sigma, color="0.55", alpha=0.55,
                          linewidth=0,
                          label=(r"Bootstrap $1\sigma$ (median "
                                 f"{np.nanmedian(sigma):.03f})"))
        axis.plot(grid, stacked, color=colour, lw=1.0, label=name)
        axis.axhline(0.0, color="black", lw=1.0, ls="--")
        axis.set_ylabel("Mean pull")
        axis.legend(frameon=False, fontsize=7.5, loc="lower left", ncol=2)
    axes[0].set_ylim(-1.15 * span, 1.15 * span)
    _label_axes(axes, axes[-1], r"Rest wavelength [$\mathrm{\AA}$]")
    fig.suptitle(
        f"Five stacking recipes for the DR2 pull, rest frame (N={n_used} "
        f"galaxies)", fontsize=10)
    caption = (
        "Each panel stacks the same per-galaxy mean pull with a different "
        "recipe.\nThe grey band is the 1-sigma spread from resampling "
        "galaxies. Grey columns mark the known absorption windows."
    )
    fig.text(0.5, 0.004, caption, ha="center", va="bottom", fontsize=7,
             color="#555555", linespacing=1.5)
    fig.tight_layout(rect=(0, 0.045, 1, 0.965))
    _save(fig, out_dir, "stacked-pull-recipes")


def figure_by_feature(feature_stacks, continuum_stacks, feature_names,
                      n_cover, n_continuum_gal, out_dir):
    """Stacked pull inside each absorption window against the continuum."""
    categories = ["Continuum"] + list(feature_names)
    counts = [n_continuum_gal] + list(n_cover)
    positions = np.arange(len(categories), dtype=float)
    offsets = np.linspace(-0.3, 0.3, len(RECIPES))
    fig, axis = plt.subplots(figsize=(9.5, 4.4))
    axis.axhline(0.0, color="black", lw=1.0, ls="--", zorder=1)
    for offset, name in zip(offsets, RECIPES, strict=True):
        colour, marker = RECIPE_STYLE[name]
        value = np.concatenate(
            ([continuum_stacks[name][0]], feature_stacks[name][0]))
        error = np.concatenate(
            ([continuum_stacks[name][1]], feature_stacks[name][1]))
        axis.errorbar(positions + offset, value, yerr=error, fmt=marker,
                      color=colour, markersize=4.5, elinewidth=1.0,
                      capsize=2.0, lw=0, label=name, zorder=3)
    for position in positions[:-1] + 0.5:
        axis.axvline(position, color="0.85", lw=0.6, zorder=0)
    axis.set_xticks(positions)
    axis.set_xticklabels([f"{name}\nN={count}"
                          for name, count in zip(categories, counts, strict=True)],
                         fontsize=7.5)
    for position, count in zip(positions, counts, strict=True):
        if count == 0:
            axis.text(position, 0.5, "masked\nin the fits", color="0.45",
                      fontsize=7, ha="center", va="center", rotation=90,
                      transform=axis.get_xaxis_transform())
    axis.set_xlim(-0.6, len(categories) - 0.4)
    axis.set_ylabel("Mean pull per native pixel")
    axis.legend(frameon=False, fontsize=7.5, ncol=5, loc="upper center",
                bbox_to_anchor=(0.5, 1.14))
    caption = (
        "Points give the stacked pull inside one absorption window. "
        "Continuum is every fitted pixel outside all windows. Error bars are "
        "the 1-sigma spread from resampling galaxies. N counts the galaxies "
        "that cover the window."
    )
    fig.text(0.5, 0.008, caption, ha="center", fontsize=7, color="#555555",
             wrap=True)
    fig.tight_layout(rect=(0, 0.085, 1, 0.97))
    _save(fig, out_dir, "stacked-pull-by-feature")


def _save(fig, out_dir, stem):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_dir / f"{stem}.pdf")
    fig.savefig(out_dir / f"{stem}.png")
    plt.close(fig)
    print(f"wrote {stem}.{{pdf,png}} to {out_dir}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--n-boot", type=int, default=N_BOOT)
    args = parser.parse_args(argv)

    grid = np.arange(GRID_LO, GRID_HI + GRID_DL, GRID_DL)
    names = [name for name, _ in MARKED_FEATURES]
    labels = [label for _, label in MARKED_FEATURES]
    windows = feature_windows(names, zred=0.0, window_kms=WINDOW_KMS)

    run = load_run(args.run_dir, args.summary, grid, windows)
    n_used = len(run["targets"])
    mean_pull2, n_cover = stacked_mean_pull2(run["sum_pull2"], run["n_pix"])
    weights = inverse_variance_weights(run["n_pix"], run["redchi2"])
    stacks = stack_all_recipes(run["averages"], weights, args.n_boot)

    feature_weights = inverse_variance_weights(run["feature_pix"], run["redchi2"])
    continuum_weights = inverse_variance_weights(
        run["continuum_pix"][:, None], run["redchi2"])
    feature_stacks = stack_all_recipes(
        run["feature_avg"], feature_weights, args.n_boot)
    continuum_stacks = {
        name: (float(value[0]), float(sigma[0]))
        for name, (value, sigma) in stack_all_recipes(
            run["continuum_avg"][:, None], continuum_weights, args.n_boot).items()
    }
    feature_cover = np.sum(np.isfinite(run["feature_avg"]), axis=0)
    continuum_cover = int(np.sum(np.isfinite(run["continuum_avg"])))

    covered = np.isfinite(mean_pull2)
    print(f"galaxies used: {n_used}")
    print(f"bins with >={MIN_COVER} galaxies: {int(covered.sum())}/{len(grid)}")
    print(f"median per-galaxy reduced chi2: {np.nanmedian(run['redchi2']):.3f}")
    print(f"median stacked mean pull^2: {np.nanmedian(mean_pull2):.3f}")
    peak = int(np.nanargmax(np.where(covered, mean_pull2, -np.inf)))
    print(f"peak bin: {grid[peak]:.0f} A, mean pull^2 {mean_pull2[peak]:.2f}, "
          f"{int(n_cover[peak])} galaxies")
    well = covered & (n_cover >= n_used // 2)
    best = int(np.nanargmax(np.where(well, mean_pull2, -np.inf)))
    print(f"peak bin with >={n_used // 2} galaxies: {grid[best]:.0f} A, "
          f"mean pull^2 {mean_pull2[best]:.2f}, {int(n_cover[best])} galaxies")
    for name, (stacked, sigma) in stacks.items():
        significance = np.abs(stacked) / sigma
        print(f"{name:20s} max |stacked pull| {np.nanmax(np.abs(stacked)):.3f}, "
              f"max |z| {np.nanmax(significance):.1f}")
    print("feature".ljust(13), "N".rjust(4),
          " ".join(f"{name[:13]:>13s}" for name in RECIPES))
    for k, label in enumerate(["Continuum"] + labels):
        if k == 0:
            row = [continuum_stacks[name] for name in RECIPES]
            count = continuum_cover
        else:
            row = [(feature_stacks[name][0][k - 1], feature_stacks[name][1][k - 1])
                   for name in RECIPES]
            count = int(feature_cover[k - 1])
        plain = label.replace("$", "").replace("\\", "")
        print(plain.ljust(13), str(count).rjust(4),
              " ".join(f"{value:+.3f}+-{sigma:.3f}" for value, sigma in row))

    out_dir = Path(args.out_dir)
    figure_overview(grid, mean_pull2, run["averages"], run["redchi2"],
                    n_used, out_dir)
    figure_recipes(grid, stacks, n_used, out_dir)
    figure_by_feature(feature_stacks, continuum_stacks, labels,
                      feature_cover, continuum_cover, out_dir)


if __name__ == "__main__":
    main()
