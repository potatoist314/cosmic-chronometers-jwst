"""Formation times against age, and October refit against September run (CPU only).

Reads the refit summary CSV (same columns as
``results/dr2-quiescent-new-defaults-summary.csv``) and writes two figures:

- ``formation-times-vs-age``: t20, t50 and t80 against mass-weighted age, each with
  16-84 intervals, a running median and the one-to-one line.
- ``old-vs-new``: refit posterior median against the September run for seven
  parameters, both 16-84 intervals, joined on ``object_id``, with the one-to-one line.

Usage: ``ceridwen/.venv/bin/python scripts/plot_dr2_refit_figures.py``
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
from matplotlib.lines import Line2D

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-refit-2026-10-12/dr2-refit-summary.csv"
OLD_SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
OUT_DIR = PROJECT_ROOT / "wiki/analyses/dr2-refit-sample"

BLUE, ORANGE, GREEN, GREY = "#0072B2", "#E69F00", "#009E73", "#999999"
N_RUN = 10  # equal-count running-median bins

rcParams.update(
    {
        "font.size": 9,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "savefig.dpi": 150,
        "legend.frameon": False,
    }
)

# Marker shape repeats the colour: t80 sits above the one-to-one line, t20 below.
FORMATION_SERIES = [
    ("t80", r"$t_{80}$", GREEN, "^"),
    ("t50", r"$t_{50}$", ORANGE, "o"),
    ("t20", r"$t_{20}$", BLUE, "v"),
]

# Timing row first, then mass, chemistry and dust; grid cell 3 stays empty.
COMPARED = [
    ("age", "Mass-weighted age [Gyr]"),
    ("t50", r"$t_{50}$ [Gyr]"),
    ("dt", r"$\Delta t = t_{80}-t_{20}$ [Gyr]"),
    ("logmass", r"$\log M_\star\,[M_\odot]$"),
    ("feh", r"$[\mathrm{Fe}/\mathrm{H}]$ [dex]"),
    ("alpha_fe", r"$[\alpha/\mathrm{Fe}]$ [dex]"),
    ("tau_dust", r"$\tau_{\rm diffuse}$"),
]
CELLS = [0, 1, 2, 4, 5, 6, 7]


def median_interval(frame: pd.DataFrame, key: str,
                    run: str = "") -> tuple[np.ndarray, np.ndarray]:
    """Posterior median and its asymmetric 16-84 error bars."""
    mid = frame[f"{key}_q50{run}"].to_numpy()
    return mid, np.vstack([mid - frame[f"{key}_q16{run}"].to_numpy(),
                           frame[f"{key}_q84{run}"].to_numpy() - mid])


def running_median(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Median x and y in equal-count x bins."""
    bins = np.array_split(np.argsort(x), N_RUN)
    return (np.array([np.median(x[b]) for b in bins]),
            np.array([np.median(y[b]) for b in bins]))


def plot_formation_times(frame: pd.DataFrame, out_dir: Path) -> None:
    age, age_err = median_interval(frame, "age")
    top = float(np.ceil(frame["t80_q84"].max() + 0.25))
    lim = (0.0, top)
    fig, axis = plt.subplots(figsize=(5.0, 4.9))
    axis.plot(lim, lim, color=GREY, lw=0.9, zorder=0)
    for key, _, colour, marker in FORMATION_SERIES:
        t, t_err = median_interval(frame, key)
        # One age interval per galaxy, drawn on t50.
        axis.errorbar(age, t, xerr=age_err if key == "t50" else None, yerr=t_err,
                      fmt=marker, ms=3.4, color=colour, alpha=0.35,
                      elinewidth=0.5, mew=0)
        axis.plot(*running_median(age, t), color=colour, lw=1.8)
    axis.legend(handles=[Line2D([], [], color=c, marker=m, lw=1.8, ms=5, label=l)
                         for _, l, c, m in FORMATION_SERIES],
                loc="upper left", handlelength=2.2)
    axis.set(xlim=lim, ylim=lim, aspect="equal",
             xlabel="Mass-weighted age [Gyr]",
             ylabel="Formation lookback [Gyr]")
    axis.set_title(f"Ceridwen DR2 quiescent formation times (N={len(frame)})",
                   fontsize=10)
    fig.tight_layout()
    fig.savefig(out_dir / "formation-times-vs-age.pdf")
    fig.savefig(out_dir / "formation-times-vs-age.png")
    plt.close(fig)


def plot_old_vs_new(joined: pd.DataFrame, out_dir: Path) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(8.0, 4.15), layout="constrained")
    fig.get_layout_engine().set(h_pad=0.1)
    for cell, (key, label) in zip(CELLS, COMPARED):
        axis = axes.flat[cell]
        x, x_err = median_interval(joined, key, "_old")
        y, y_err = median_interval(joined, key, "_new")
        lo = min(joined[f"{key}_q16_old"].min(), joined[f"{key}_q16_new"].min())
        hi = max(joined[f"{key}_q84_old"].max(), joined[f"{key}_q84_new"].max())
        pad = 0.06 * (hi - lo)
        lim = (lo - pad, hi + pad)
        axis.plot(lim, lim, color=GREY, lw=0.9, zorder=0)
        axis.errorbar(x, y, xerr=x_err, yerr=y_err, fmt="o", ms=3, color=BLUE,
                      alpha=0.5, elinewidth=0.6, mew=0)
        axis.set(xlim=lim, ylim=lim, aspect="equal")
        axis.set_title(label, fontsize=9)
    # The two runs use different diffuse-dust laws.
    axes.flat[7].set_xlabel("Kriek & Conroy", fontsize=8)
    axes.flat[7].set_ylabel("Noll", fontsize=8)
    axes.flat[3].axis("off")
    fig.supxlabel("September run", fontsize=9)
    fig.supylabel("October refit", fontsize=9)
    fig.suptitle("Ceridwen DR2 quiescent, October refit against September run "
                 f"(N={len(joined)})", fontsize=10)
    fig.savefig(out_dir / "old-vs-new.pdf")
    fig.savefig(out_dir / "old-vs-new.png")
    plt.close(fig)


def main(summary: Path, old_summary: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    new = pd.read_csv(summary)
    old = pd.read_csv(old_summary)
    plot_formation_times(new, out_dir)
    joined = old.merge(new, on="object_id", suffixes=("_old", "_new"))
    plot_old_vs_new(joined, out_dir)
    print(f"wrote 2 figures for {len(new)} refit galaxies "
          f"({len(joined)} joined) to {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--summary", type=Path, default=SUMMARY_PATH)
    parser.add_argument("--old-summary", type=Path, default=OLD_SUMMARY_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    main(args.summary, args.old_summary, args.out_dir)
