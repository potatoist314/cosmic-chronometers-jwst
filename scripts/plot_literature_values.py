"""Literature values for quiescent galaxies against redshift, with Ceridwen DR2.

Plots published age, metallicity and alpha-enhancement measurements of
quiescent galaxies (values as tabulated in
``papers/quiescent populations/README.md``) against redshift, and overlays the
187-galaxy Ceridwen DR2 sample from ``results/dr2-quiescent-summary.csv`` as
the sample median with the 16-84 percentile spread across galaxies.

Ceridwen metallicity is absolute log Z; it is shown for two solar references
because the project has not fixed one (wiki roadmap, "metallicity").

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
from matplotlib.patches import Rectangle

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
OUT_DIR = PROJECT_ROOT / "wiki/analyses/papers-quiescent-parameters"

BLUE, GREY = "#0072B2", "#555555"
SOLAR_Z = {"0.0142": 0.0142, "0.020": 0.020}  # Asplund+2009, Anders & Grevesse 1989

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

# Each entry: label (None = no text), redshift, value or (low, high) range,
# symmetric error, kind, and where the text goes relative to the point:
# "right" of the top of the bar (default), "left" of the value, or "below".
# Numbers are copied from the tables in papers/quiescent populations/README.md.
AGE = [
    ("Conroy+14", 0.05, (6.0, 12.0), None, "light-weighted", "right"),
    ("Borghi+22", 0.70, (2.0, 4.0), None, "SSP-equivalent", "right"),
]
METALLICITY = [
    ("Conroy+14", 0.05, (-0.05, 0.05), None, "[Fe/H]", "right"),
    ("Borghi+22", 0.70, 0.08, 0.18, "[Z/H]", "right"),
    ("Beverage+21,\nCheng+25", 0.70, (-0.1, 0.0), None, "[Fe/H]", "below"),
    ("Carnall+22", 1.15, 0.04, 0.14, "[Z/H]", "right"),
    (None, 1.15, -0.13, 0.08, "[Z/H]", "right"),
    (None, 1.15, -0.18, 0.08, "[Fe/H]", "right"),
    ("Kriek+19, Beverage+24", 1.40, -0.2, None, "[Fe/H]", "right"),
    ("Beverage+24", 2.10, -0.3, None, "[Fe/H]", "right"),
]
ALPHA = [
    ("Conroy+14", 0.05, (0.0, 0.25), None, "[Mg/Fe]", "right"),
    ("Bevacqua+23", 0.68, 0.24, 0.01, "[α/Fe]", "left"),
    ("Borghi+22", 0.70, 0.13, 0.11, "[α/Fe]", "left"),
    ("Beverage+21/23", 0.72, (0.2, 0.3), None, "[Mg/Fe]", "right"),
    ("Kriek+19", 1.40, 0.44, None, "[Mg/Fe]", "right"),
    ("Beverage+24", 1.40, 0.3, None, "[Mg/Fe]", "right"),
    ("Beverage+24", 2.10, 0.5, None, "[Mg/Fe]", "right"),
]
MARKER = {"[Z/H]": "o", "[Fe/H]": "s", "[α/Fe]": "o", "[Mg/Fe]": "s",
          "light-weighted": "s", "SSP-equivalent": "o"}
LEGEND_NAME = {"[Z/H]": r"$[Z/\mathrm{H}]$", "[Fe/H]": r"$[\mathrm{Fe}/\mathrm{H}]$",
               "[α/Fe]": r"$[\alpha/\mathrm{Fe}]$", "[Mg/Fe]": r"$[\mathrm{Mg}/\mathrm{Fe}]$",
               "light-weighted": "light-weighted", "SSP-equivalent": "SSP-equivalent"}
TEXT_POS = {  # (dx, ha, va, anchor on "top" of the bar, "mid" or "bottom")
    "right": (0.025, "left", "bottom", "top"),
    "left": (-0.025, "right", "center", "mid"),
    "below": (0.03, "left", "top", "bottom"),
}


def draw_literature(axis, entries):
    """Points (with error bars) or vertical range bars, each labelled in place."""
    seen = set()
    for label, z, value, err, kind, where in entries:
        marker = MARKER[kind]
        name = LEGEND_NAME[kind] if kind not in seen else None
        seen.add(kind)
        if isinstance(value, tuple):
            lo, hi = value
            mid = 0.5 * (lo + hi)
            axis.plot([z, z], [lo, hi], color=GREY, lw=2.5, solid_capstyle="butt", zorder=2)
            axis.plot(z, mid, marker=marker, color=GREY, ms=4, ls="none", label=name, zorder=3)
        else:
            lo, mid, hi = value - (err or 0.0), value, value + (err or 0.0)
            axis.errorbar(z, value, yerr=err, fmt=marker, color=GREY, ms=4, capsize=2,
                          lw=1, label=name, zorder=3)
        if label is None:
            continue
        dx, ha, va, anchor = TEXT_POS[where]
        y_text = {"top": hi, "mid": mid, "bottom": lo}[anchor]
        axis.annotate(label, (z + dx, y_text), fontsize=8, color=GREY, ha=ha, va=va, zorder=4)


def draw_ceridwen(axis, z, q16, q50, q84, label, **style):
    """Sample median (diamond) over a band spanning the 16-84 percentiles in y and z."""
    zlo, zmid, zhi = np.percentile(z, [16, 50, 84])
    axis.add_patch(Rectangle((zlo, q16), zhi - zlo, q84 - q16, facecolor=BLUE, alpha=0.15,
                             edgecolor="none", zorder=1))
    axis.plot(zmid + style.pop("dz", 0.0), q50, "D", color=BLUE, ms=7, mec=BLUE, zorder=5,
              label=label, **style)


def legend(axis, loc):
    """Literature entries first, Ceridwen last."""
    handles, labels = axis.get_legend_handles_labels()
    order = sorted(range(len(labels)), key=lambda i: labels[i].startswith("Ceridwen"))
    axis.legend([handles[i] for i in order], [labels[i] for i in order],
                fontsize=8, loc=loc, frameon=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SUMMARY_PATH)
    z = df["z"].to_numpy()
    fig, axes = plt.subplots(3, 1, figsize=(6.0, 9.0), sharex=True)

    # Age
    axis = axes[0]
    draw_literature(axis, AGE)
    lo, mid, hi = np.percentile(df["age_q50"], [16, 50, 84])
    draw_ceridwen(axis, z, lo, mid, hi, "Ceridwen DR2 (N=%d), mass-weighted; band: 16–84" % len(df))
    axis.set_ylabel("age [Gyr]")
    axis.set_ylim(0, 13.5)
    legend(axis, "upper right")

    # Metallicity: Ceridwen log Z is absolute, so show two solar references.
    axis = axes[1]
    draw_literature(axis, METALLICITY)
    lo, mid, hi = np.percentile(df["logZ_abs_q50"], [16, 50, 84])
    for i, (name, zsun) in enumerate(SOLAR_Z.items()):
        shift = np.log10(zsun)
        draw_ceridwen(axis, z, lo - shift, mid - shift, hi - shift,
                      r"Ceridwen DR2, $Z_\odot=%s$" % name, dz=0.08 * i,
                      mfc=BLUE if i == 0 else "white")
    axis.set_ylabel(r"$[Z/\mathrm{H}]$ or $[\mathrm{Fe}/\mathrm{H}]$ [dex]")
    axis.set_ylim(-0.7, 0.5)
    axis.axhline(0, color="k", lw=0.5, ls=":")
    legend(axis, "lower left")

    # Alpha enhancement
    axis = axes[2]
    draw_literature(axis, ALPHA)
    lo, mid, hi = np.percentile(df["alpha_fe_q50"], [16, 50, 84])
    draw_ceridwen(axis, z, lo, mid, hi, "Ceridwen DR2")
    axis.set_ylabel(r"$[\alpha/\mathrm{Fe}]$ or $[\mathrm{Mg}/\mathrm{Fe}]$ [dex]")
    axis.set_ylim(-0.3, 0.75)
    axis.axhline(0, color="k", lw=0.5, ls=":")
    legend(axis, "upper left")

    axes[0].set_xlim(-0.1, 2.55)
    axes[-1].set_xlabel(r"$z$")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "literature-vs-ceridwen.pdf")
    fig.savefig(OUT_DIR / "literature-vs-ceridwen.png")
    plt.close(fig)
    print("wrote literature figure to", OUT_DIR)


if __name__ == "__main__":
    main()
