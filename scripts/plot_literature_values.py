"""Literature values for quiescent galaxies against redshift, with Ceridwen DR2.

Dot plot, one row per paper ordered by redshift, of published age, metallicity
and alpha-enhancement values of quiescent galaxies (as tabulated in
``papers/quiescent populations/README.md``), with the 187-galaxy Ceridwen DR2
sample from ``results/dr2-quiescent-new-defaults-summary.csv`` as the top row: sample median
and the 16-84 percentile spread across galaxies, plus a vertical median line.

The summary CSV's ``feh_q50`` is Ceridwen's grid ``Z`` shifted to [Fe/H]
(``FEH_OFFSET`` in ``scripts/build_dr2_quiescent_summary.py``).

Usage: ``python3 scripts/plot_literature_values.py``
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
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
OUT_DIR = PROJECT_ROOT / "wiki/analyses/papers-quiescent-parameters"

BLUE, GREY = "#0072B2", "#555555"

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

# Each entry: row label, redshift, value or (low, high) range, symmetric error,
# kind (sets the marker). Numbers are copied from the tables in
# papers/quiescent populations/README.md.
AGE = [
    ("Borghi+22", 0.7, (2.0, 4.0), None, "SSP-equivalent"),
    ("Conroy+14", 0.05, (6.0, 12.0), None, "light-weighted"),
]
METALLICITY = [
    ("Borghi+22", 0.7, 0.08, 0.18, "[Z/H]"),
    ("Beverage+21, Cheng+25", 0.7, (-0.1, 0.0), None, "[Fe/H]"),
    ("Conroy+14", 0.05, (-0.05, 0.05), None, "[Fe/H]"),
    ("Carnall+22 (Bagpipes)", 1.15, -0.13, 0.08, "[Z/H]"),
    ("Carnall+22 (alf)", 1.15, 0.04, 0.14, "[Z/H]"),
    ("Carnall+22", 1.15, -0.18, 0.08, "[Fe/H]"),
    ("Kriek+19", 1.4, -0.2, None, "[Fe/H]"),
    ("Beverage+24", 1.4, -0.2, None, "[Fe/H]"),
    ("Beverage+24", 2.1, -0.3, None, "[Fe/H]"),
]
ALPHA = [
    ("Bevacqua+23", 0.68, 0.24, 0.01, "[α/Fe]"),
    ("Borghi+22", 0.7, 0.13, 0.11, "[α/Fe]"),
    ("Beverage+21/23", 0.7, (0.2, 0.3), None, "[Mg/Fe]"),
    ("Conroy+14", 0.05, (0.0, 0.25), None, "[Mg/Fe]"),
    ("Kriek+19", 1.4, 0.44, None, "[Mg/Fe]"),
    ("Beverage+24", 1.4, 0.3, None, "[Mg/Fe]"),
    ("Beverage+24", 2.1, 0.5, None, "[Mg/Fe]"),
]
MARKER = {"[Z/H]": "o", "[Fe/H]": "s", "[α/Fe]": "o", "[Mg/Fe]": "s",
          "light-weighted": "s", "SSP-equivalent": "o", "mass-weighted": "D"}
LEGEND_NAME = {"[Z/H]": r"$[Z/\mathrm{H}]$", "[Fe/H]": r"$[\mathrm{Fe}/\mathrm{H}]$",
               "[α/Fe]": r"$[\alpha/\mathrm{Fe}]$", "[Mg/Fe]": r"$[\mathrm{Mg}/\mathrm{Fe}]$",
               "light-weighted": "light-weighted", "SSP-equivalent": "SSP-equivalent",
               "mass-weighted": "mass-weighted"}


def row_label(label, z):
    return "%s, $z$ %s" % (label, ("%.2f" % z).rstrip("0").rstrip("."))


def draw_rows(axis, ceridwen, entries, xlabel, xlim, zero_line=True):
    """One row per entry: Ceridwen rows first (blue), then papers by redshift."""
    rows = list(ceridwen) + sorted(entries, key=lambda e: e[1])
    seen = set()
    labels = []
    for i, (label, z, value, err, kind) in enumerate(rows):
        y = len(rows) - 1 - i
        blue = i < len(ceridwen)
        colour = BLUE if blue else GREY
        name = LEGEND_NAME[kind] if kind not in seen else None
        seen.add(kind)
        if isinstance(value, tuple):
            lo, hi = value
            axis.plot([lo, hi], [y, y], color=colour, lw=4, solid_capstyle="butt", alpha=0.5, zorder=2)
            axis.plot(0.5 * (lo + hi), y, marker=MARKER[kind], color=colour, ms=6, ls="none",
                      label=name, zorder=3)
        else:
            xerr = [[err[0]], [err[1]]] if isinstance(err, tuple) else err
            axis.errorbar(value, y, xerr=xerr, fmt=MARKER[kind], color=colour, ms=6, capsize=3,
                          lw=1.2, label=name, zorder=3)
        if blue:
            axis.axvline(value if not isinstance(value, tuple) else 0.5 * sum(value),
                         color=BLUE, lw=1, ls="-" if i == 0 else "--", alpha=0.6, zorder=1)
        labels.append(row_label(label, z))
    axis.set_yticks(range(len(rows) - 1, -1, -1))
    axis.set_yticklabels(labels)
    for tick, (label, *_rest) in zip(axis.get_yticklabels(), rows):
        if label.startswith("Ceridwen"):
            tick.set_color(BLUE)
    axis.set_ylim(-0.7, len(rows) - 0.3)
    axis.set_xlim(*xlim)
    axis.set_xlabel(xlabel)
    axis.tick_params(axis="y", length=0)
    axis.grid(axis="y", color="#e5e5e5", lw=0.6, zorder=0)
    if zero_line:
        axis.axvline(0, color="k", lw=0.5, ls=":", zorder=1)
    axis.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False,
                handletextpad=0.4, borderaxespad=0.0)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SUMMARY_PATH)
    z_med = float(np.median(df["z"]))
    n = len(df)

    def ceridwen_row(column, tag=""):
        lo, mid, hi = np.percentile(df[column], [16, 50, 84])
        return ("Ceridwen DR2%s, N=%d" % (tag, n), z_med, mid, (mid - lo, hi - mid), "mass-weighted")

    fig, axes = plt.subplots(3, 1, figsize=(8.0, 7.9), layout="constrained",
                             gridspec_kw={"height_ratios": [3, 10, 8]})
    draw_rows(axes[0], [ceridwen_row("age_q50")], AGE, "age [Gyr]", (0, 13), zero_line=False)
    draw_rows(axes[1],
              [ceridwen_row("feh_q50", r" $[\mathrm{Fe}/\mathrm{H}]$")],
              METALLICITY, r"$[Z/\mathrm{H}]$ or $[\mathrm{Fe}/\mathrm{H}]$ [dex]", (-0.5, 0.5))
    draw_rows(axes[2], [ceridwen_row("alpha_fe_q50")], ALPHA,
              r"$[\alpha/\mathrm{Fe}]$ or $[\mathrm{Mg}/\mathrm{Fe}]$ [dex]", (-0.2, 0.6))
    fig.savefig(OUT_DIR / "literature-vs-ceridwen.pdf")
    fig.savefig(OUT_DIR / "literature-vs-ceridwen.png")
    plt.close(fig)
    print("wrote literature figure to", OUT_DIR)


if __name__ == "__main__":
    main()
