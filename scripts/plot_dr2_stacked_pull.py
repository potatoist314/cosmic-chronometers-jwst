"""Stacked pull (chi-squared) diagnostic for large-scale DR2 runs.

Method note (reusable pattern for future 180+ galaxy runs):
- Source: per-galaxy ``ceridwen_derived_outputs.h5`` from the run directory.
  Pull uses the posterior-median model and the effective uncertainty actually
  used by the likelihood: ``pull = (observed - posterior_q50) /
  effective_uncertainty`` over fitted (masked) spectrum pixels.
- Each spectrum shifts to rest frame (observed wavelength divided by 1+z)
  and regrids onto one common uniform rest-frame grid by linear
  interpolation. Regridded errors scale by the square root of the
  bin-width ratio: ``sigma_new = sigma_old * sqrt(dlambda_new /
  dlambda_native)`` with each galaxy's median native rest spacing.
- Galaxies carry equal weight: every stacked bin averages over the
  galaxies covering it, so bright objects cannot dominate. A bin counts
  as covered only where the interpolated fitted-pixel mask exceeds 0.5.
- Bins covered by fewer than ``MIN_COVER`` galaxies are set to NaN and
  left out of the connected lines, so edge bins cannot fake structure.
- Rest frame is used because template mismatches live in rest frame;
  sky-subtraction residuals live in observed frame and wash out here.

Outputs one figure with three panels: mean pull-squared per bin with the
null-expectation line at 1, median pull per bin with 16-84 bands, and a
histogram of per-galaxy reduced chi-squared (native pixels, no regrid).

Reuse: ``.venv/bin/python scripts/plot_dr2_stacked_pull.py
[--run-dir DIR] [--out-dir DIR]``. Defaults target the current DR2 run.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DIR = PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
DEFAULT_SUMMARY = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
DEFAULT_OUT_DIR = PROJECT_ROOT / "wiki/analyses/dr2-quiescent-sample"

GRID_LO, GRID_HI, GRID_DL = 2900.0, 5950.0, 2.0
MIN_COVER = 10
BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#999999"

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


def regrid_galaxy(wave_rest, observed, model, sigma, mask, grid):
    """Interpolate one galaxy onto the common grid with scaled errors.

    Returns ``(data, model, sigma, covered)`` on ``grid``. ``covered`` is
    True where the interpolated fitted-pixel mask exceeds 0.5.
    """
    wave_rest = np.asarray(wave_rest, dtype=float)
    native_dl = float(np.median(np.diff(wave_rest)))
    grid_dl = float(grid[1] - grid[0])
    data = np.interp(grid, wave_rest, np.asarray(observed, dtype=float))
    mod = np.interp(grid, wave_rest, np.asarray(model, dtype=float))
    sig = np.interp(grid, wave_rest, np.asarray(sigma, dtype=float))
    sig = sig * np.sqrt(grid_dl / native_dl)
    frac = np.interp(grid, wave_rest,
                     np.asarray(mask, dtype=float), left=0.0, right=0.0)
    return data, mod, sig, frac > 0.5


def stack_pulls(pull_matrix, min_cover=MIN_COVER):
    """Stack equal-weight pulls over galaxies.

    ``pull_matrix`` is (n_galaxies, n_bins) with NaN where uncovered.
    Returns ``(mean_pull2, median, q16, q84, n_cover)`` with NaN where
    fewer than ``min_cover`` galaxies cover the bin.
    """
    pull_matrix = np.asarray(pull_matrix, dtype=float)
    n_cover = np.sum(np.isfinite(pull_matrix), axis=0)
    ok = n_cover >= min_cover
    mean_pull2 = np.full(pull_matrix.shape[1], np.nan)
    median = np.full(pull_matrix.shape[1], np.nan)
    q16 = np.full(pull_matrix.shape[1], np.nan)
    q84 = np.full(pull_matrix.shape[1], np.nan)
    mean_pull2[ok] = np.nanmean(pull_matrix[:, ok] ** 2, axis=0)
    median[ok] = np.nanmedian(pull_matrix[:, ok], axis=0)
    q16[ok] = np.nanquantile(pull_matrix[:, ok], 0.16, axis=0)
    q84[ok] = np.nanquantile(pull_matrix[:, ok], 0.84, axis=0)
    return mean_pull2, median, q16, q84, n_cover


def reduced_chi2(pull_native):
    """Mean pull-squared over fitted native pixels."""
    pull_native = np.asarray(pull_native, dtype=float)
    return float(np.mean(pull_native**2))


def load_run(run_dir, summary_path):
    """Pull matrices for every summary galaxy with derived outputs."""
    import h5py

    galaxies = pd.read_csv(summary_path)
    grid = np.arange(GRID_LO, GRID_HI + GRID_DL, GRID_DL)
    pulls = np.full((len(galaxies), len(grid)), np.nan)
    redchi2 = np.full(len(galaxies), np.nan)
    redshifts = np.full(len(galaxies), np.nan)
    n_used = 0
    for i, target in enumerate(galaxies["target"]):
        path = Path(run_dir) / str(target) / "ceridwen_derived_outputs.h5"
        if not path.exists():
            continue
        with h5py.File(path, "r") as f:
            z = float(f.attrs["redshift"])
            spec = f["spectrum"]
            wave = np.asarray(spec["wavelength"], dtype=float) / (1.0 + z)
            obs = np.asarray(spec["observed"], dtype=float)
            mod = np.asarray(spec["posterior_q50"], dtype=float)
            sig = np.asarray(spec["effective_uncertainty"], dtype=float)
            mask = np.asarray(spec["mask"], dtype=bool)
        data, mod_g, sig_g, covered = regrid_galaxy(
            wave, obs, mod, sig, mask, grid)
        with np.errstate(divide="ignore", invalid="ignore"):
            pulls[i][covered] = (data[covered] - mod_g[covered]) / sig_g[covered]
        native = (obs[mask] - mod[mask]) / sig[mask]
        redchi2[i] = reduced_chi2(native)
        redshifts[i] = z
        n_used += 1
    return grid, pulls, redchi2, redshifts, n_used


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args(argv)

    grid, pulls, redchi2, redshifts, n_used = load_run(
        args.run_dir, args.summary)
    mean_pull2, median, q16, q84, n_cover = stack_pulls(pulls)
    ok = np.isfinite(mean_pull2)
    print(f"galaxies used: {n_used}/{len(pulls)}")
    print(f"bins with >={MIN_COVER} galaxies: {int(ok.sum())}/{len(grid)}")
    print(f"median per-galaxy reduced chi2: {np.nanmedian(redchi2):.3f}")
    print(f"max stacked mean pull-squared: {np.nanmax(mean_pull2):.3f}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.4),
                             gridspec_kw={"width_ratios": [1.4, 1.4, 1.0]})
    axes[0].plot(grid, mean_pull2, color=BLUE, lw=1.0)
    axes[0].axhline(1.0, color="black", lw=1.0, ls="--")
    axes[0].set_xlabel(r"Rest wavelength [$\mathrm{\AA}$]")
    axes[0].set_ylabel("Mean pull$^2$ per bin")
    axes[0].set_title("Stacked chi-squared", fontsize=10)
    axes[1].plot(grid, median, color=BLUE, lw=1.0, label="Median pull")
    axes[1].fill_between(grid, q16, q84, color=BLUE, alpha=0.25,
                         linewidth=0, label="16-84%")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--")
    axes[1].set_xlabel(r"Rest wavelength [$\mathrm{\AA}$]")
    axes[1].set_ylabel("Pull per bin")
    axes[1].legend(frameon=False, fontsize=7.5)
    axes[1].set_title("Median pull", fontsize=10)
    finite = redchi2[np.isfinite(redchi2)]
    axes[2].hist(finite, bins=25, color=BLUE, alpha=0.7,
                 edgecolor="white", linewidth=0.5)
    axes[2].axvline(1.0, color="black", lw=1.0, ls="--")
    axes[2].set_xlabel(r"Per-galaxy reduced $\chi^2$")
    axes[2].set_ylabel("Galaxies")
    axes[2].set_title(f"Fit quality (N={len(finite)})", fontsize=10)
    for axis in axes:
        axis.set_xlim(axis.get_xlim())
    fig.suptitle(f"Ceridwen DR2 stacked pulls, rest frame (N={n_used} galaxies, "
                 f"bins with >={MIN_COVER} shown)", fontsize=10)
    caption = ("Template issues live in rest frame; sky residuals live in "
               "observed frame and wash out in this stack.")
    fig.text(0.5, 0.005, caption, ha="center", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 0.9))
    fig.savefig(out_dir / "stacked-pull.pdf")
    fig.savefig(out_dir / "stacked-pull.png")
    plt.close(fig)
    print("wrote stacked-pull.{pdf,png} to", out_dir)


if __name__ == "__main__":
    main()
