"""Check-in figure, 2026-11-20: [alpha/Fe] against COSMOS2020 stellar mass and against sigma_star.

Follows Bevacqua et al. 2023, MNRAS 525:4219, Fig. 6 (top row). Main C/N-free fits: 327 with a COSMOS2020 mass,
333 with sigma_star.
Run from the repository root:
    ceridwen/.venv/bin/python -B results/checkin-figures-2026-11-20/afe_relations.py
Input (read only): results/dr3-trends-2026-11-18/per-galaxy.csv.
Dots: per-galaxy posterior medians. Line: trends.binned medians in 6 quantile bins of x. Bar (lower left): median
half-width of the per-galaxy 16-84% range of [alpha/Fe].
Output: wiki/analyses/dr3-trends/afe-mass-sigma.png
"""

import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import patheffects  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.ticker import FixedLocator, NullLocator  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TRENDS = ROOT / "results/dr3-trends-2026-11-18"
OUT = ROOT / "wiki/analyses/dr3-trends/afe-mass-sigma.png"
_spec = importlib.util.spec_from_file_location("trends", TRENDS / "trends.py")
trends = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(trends)

AFE = r"$[\mathsf{\alpha}/\mathrm{Fe}]$"  # \mathsf -> STIX italic: Charter's italic alpha reads as "a"
MASS = r"$\log_{10}\,M_\star/M_\odot$ (COSMOS2020)"
SIGMA = r"$\sigma_\star$ (km s$^{-1}$)"

# Style of scripts/plot_afe_age_chronometer.py at slide size
PAPER, INK, INK2, INK3 = "#fafaf8", "#1c2024", "#4b535b", "#7d858d"
CN = "#b5832a"  # C/N-free arm
WIDTH = 7.6
RC = {
    "font.family": "Charter", "font.size": 12,
    "mathtext.fontset": "custom", "mathtext.rm": "Charter", "mathtext.it": "Charter:italic",
    "mathtext.bf": "Charter:bold", "mathtext.sf": "STIXGeneral:italic", "mathtext.fallback": "stix",
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "axes.edgecolor": INK3, "axes.linewidth": 0.8, "axes.labelcolor": INK2, "axes.labelsize": 12.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK3, "ytick.color": INK3, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11.5, "xtick.major.size": 4, "ytick.major.size": 4,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.minor.size": 0, "ytick.minor.size": 0,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.top": False, "ytick.right": False,
    "lines.solid_capstyle": "round", "lines.dash_capstyle": "butt",
}
DOT = tuple(0.5 * c + 0.5 * p for c, p in zip(to_rgb(CN), to_rgb(PAPER)))


def panel(ax, x, g):
    """Dots, trends.binned median line (6 bins) and the typical-error bar; returns the bin medians and the error."""
    y = g.afe_q50.to_numpy()
    ax.scatter(x, y, s=11, color=DOT, lw=0, zorder=1)
    xb, yb, _, _ = trends.binned(np.asarray(x, float), y, 6)
    ax.plot(xb, yb, color=CN, lw=1.8, path_effects=[patheffects.withStroke(linewidth=4.5, foreground=PAPER)], zorder=3)
    err = float(np.median(g.afe_q84 - g.afe_q16) / 2)
    ax.errorbar(0.06, -0.1, yerr=err, fmt="none", color=INK, lw=1.4, capsize=3, capthick=1.4,
                transform=ax.get_yaxis_transform(), zorder=4)
    ax.set(ylim=(-0.2, 0.6), yticks=[-0.2, 0, 0.2, 0.4, 0.6])  # the fits' [alpha/Fe] prior (trends.PRIORS)
    ax.set_yticklabels(["−0.2", "0", "0.2", "0.4", "0.6"])
    return yb, err


def main():
    g = pd.read_csv(TRENDS / "per-galaxy.csv")
    g = g[(g.arm == "cn_free") & g.main]
    gm = g[g.logmass_cosmos2020.notna()]
    with plt.rc_context(RC):
        fig, (am, ss) = plt.subplots(1, 2, figsize=(WIDTH, 4.0), sharey=True, layout="constrained")
        fig.get_layout_engine().set(h_pad=0.08, w_pad=0.1, wspace=0.06)
        ym, err = panel(am, gm.logmass_cosmos2020.to_numpy(), gm)
        am.set(xlim=(10.15, 12.0), xticks=[10.5, 11, 11.5], xlabel=MASS, ylabel=AFE)
        ys, _ = panel(ss, g.sigma_star.to_numpy(), g)
        ss.set_xscale("log")
        ss.set_xlim(80, 400)
        ss.xaxis.set_major_locator(FixedLocator((100, 200, 300)))
        ss.xaxis.set_minor_locator(NullLocator())
        ss.set_xticklabels(["100", "200", "300"])
        ss.set(xlabel=SIGMA)
        fig.suptitle(r"C/N-free fits: " + AFE + r" against $M_\star$ and $\sigma_\star$", x=0.012, ha="left", color=INK,
                     fontsize=14)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUT, dpi=200)
        plt.close(fig)
    print(f"N {len(gm)} (mass), {len(g)} (sigma_star); median [alpha/Fe] {g.afe_q50.median():.3f}; typical error {err:.3f}")
    print("bin medians, mass:", ym.round(3), "sigma_star:", ys.round(3))


if __name__ == "__main__":
    main()
