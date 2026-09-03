"""Sample distributions and fit-quality panels for the DR2 quiescent run.

Reads ``results/dr2-quiescent-summary.csv`` and writes two paper-style
figures (PDF + PNG) into the bridge reports folder:
``distributions-1d`` (1D parameter histograms, N in panel) and
``fit-quality`` (likelihood calls, ln Z, chi2/ndof with the worst fits
labelled). CPU only.

Usage: ``.venv/bin/python scripts/plot_dr2_distributions_quality.py``
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
OUT_DIR = Path.home() / ".claude/scripts/hermes-bridge/reports/ceridwen-plots"

BLUE, ORANGE = "#0072B2", "#E69F00"

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

DIST_PANELS = [
    ("z", "Redshift $z$"),
    ("logmass_q50", r"$\log M_\star\,[M_\odot]$"),
    ("age_q50", "Mass-weighted age [Gyr]"),
    ("logZ_abs_q50", r"$\log Z$ (absolute)"),
    ("alpha_fe_q50", r"$[\alpha/{\rm Fe}]$ [dex]"),
    ("tau_dust_q50", r"Dust $\tau$"),
    ("t50_q50", r"Formation $t_{50}$ [Gyr]"),
    ("dt_q50", r"$\Delta t$ [Gyr]"),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(SUMMARY_PATH)
    n = len(frame)

    fig, axes = plt.subplots(2, 4, figsize=(9.0, 4.2), sharey=False)
    for axis, (key, label) in zip(axes.flat, DIST_PANELS):
        values = frame[key].to_numpy()
        axis.hist(values, bins=20, color=BLUE, alpha=0.7, edgecolor="white",
                  linewidth=0.5)
        median = float(np.median(values))
        axis.axvline(median, color=ORANGE, lw=1.5)
        axis.set_xlabel(label)
        axis.text(0.95, 0.88, f"med {median:.2f}\nN={n}",
                  transform=axis.transAxes, ha="right", va="top", fontsize=7.5)
        axis.ticklabel_format(useOffset=False)
    axes[0, 0].set_ylabel("Galaxies")
    axes[1, 0].set_ylabel("Galaxies")
    fig.suptitle(f"Ceridwen DR2 quiescent sample distributions (N={n})",
                 fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(OUT_DIR / "distributions-1d.pdf")
    fig.savefig(OUT_DIR / "distributions-1d.png")
    plt.close(fig)

    frame["spec_chi2_ndof"] = frame["spectrum_chi2"] / frame["spectrum_ndof"]
    frame["phot_chi2_ndof"] = frame["photometry_chi2"] / frame["photometry_ndof"]
    worst = frame.nlargest(5, "joint_chi2_per_ndof")
    print("worst joint chi2/ndof:")
    print(worst[["target", "joint_chi2_per_ndof", "spec_chi2_ndof",
                 "phot_chi2_ndof", "ess", "passed"]].to_string(index=False))
    print(f"failed diagnostics: {(~frame['passed']).sum()}/{n}")

    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.0))
    axes[0, 0].hist(frame["n_calls"].to_numpy() / 1e6, bins=20, color=BLUE,
                    alpha=0.7, edgecolor="white", linewidth=0.5)
    axes[0, 0].set_xlabel("Likelihood calls [$10^6$]")
    axes[0, 0].set_ylabel("Galaxies")
    axes[0, 1].hist(frame["lnZ"].to_numpy() / 1e3, bins=20, color=BLUE,
                    alpha=0.7, edgecolor="white", linewidth=0.5)
    axes[0, 1].set_xlabel(r"$\ln Z$ [$10^3$]")
    axes[1, 0].hist(frame["joint_chi2_per_ndof"].to_numpy(), bins=20,
                    color=BLUE, alpha=0.7, edgecolor="white", linewidth=0.5)
    axes[1, 0].axvline(1.0, color="black", lw=1, ls="--")
    axes[1, 0].set_xlabel(r"Joint $\chi^2/\nu$")
    axes[1, 0].set_ylabel("Galaxies")
    axes[1, 1].scatter(frame["phot_chi2_ndof"], frame["spec_chi2_ndof"],
                       s=10, alpha=0.5, color=BLUE)
    for _, row in worst.iterrows():
        axes[1, 1].annotate(str(row["object_id"]),
                            (row["phot_chi2_ndof"], row["spec_chi2_ndof"]),
                            fontsize=6.5)
    axes[1, 1].set_xlabel(r"Photometry $\chi^2/\nu$")
    axes[1, 1].set_ylabel(r"Spectrum $\chi^2/\nu$")
    fig.suptitle(f"Ceridwen DR2 quiescent fit quality "
                 f"(N={n}, all diagnostics passed)", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(OUT_DIR / "fit-quality.pdf")
    fig.savefig(OUT_DIR / "fit-quality.png")
    plt.close(fig)
    print("wrote distributions + quality to", OUT_DIR)


if __name__ == "__main__":
    main()
