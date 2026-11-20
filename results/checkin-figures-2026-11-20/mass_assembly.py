"""Check-in figure, 2026-11-20: fraction of stellar mass formed against cosmic time, by COSMOS2020 stellar mass.

Follows Kaushal et al. 2024, ApJ 961:118, Fig. 7 (quiescent column). Main C/N-free fits with a COSMOS2020 mass (327).
Run from the repository root:
    ceridwen/.venv/bin/python -B results/checkin-figures-2026-11-20/mass_assembly.py
Inputs (read only): results/dr3-trends-2026-11-18/per-galaxy.csv and the ceridwen_derived_outputs.h5 of each fit
folder it names, as sfh_quantiles.py reads them.
Per galaxy: cosmic time at which a fraction f of the formed mass was in place, sfh_quantiles' definition per posterior
draw, then the median over draws; so each curve crosses 0.2, 0.5, 0.8 at that code's t20, t50, t80.
Per mass bin: median across galaxies; band, 16-84% across galaxies.
Output: wiki/analyses/dr3-trends/mass-assembly.png
"""

import importlib.util
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import patheffects  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TRENDS = ROOT / "results/dr3-trends-2026-11-18"
OUT = ROOT / "wiki/analyses/dr3-trends/mass-assembly.png"
_spec = importlib.util.spec_from_file_location("sfh_quantiles", TRENDS / "sfh_quantiles.py")
sq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sq)
trends = sq.trends

F = np.round(np.linspace(0, 1, 101), 2)  # fraction of the formed mass in place
LEVELS = {0.2: r"$t_{20}$", 0.5: r"$t_{50}$", 0.8: r"$t_{80}$"}
# COSMOS2020 log M bins: Kaushal's 10.5 / 11 / 11.5 edges, top two merged (3 galaxies above 11.5)
BINS = [(r"$\log M_\star \geq 11$", "#a83c3c", 11, np.inf), (r"$10.5$–$11$", "#b5832a", 10.5, 11),
        (r"$< 10.5$", "#2d5f9a", -np.inf, 10.5)]

# Style of scripts/plot_afe_age_chronometer.py at slide size
PAPER, INK, INK2, INK3 = "#fafaf8", "#1c2024", "#4b535b", "#7d858d"
WIDTH = 7.6
RC = {
    "font.family": "Charter", "font.size": 12,
    "mathtext.fontset": "custom", "mathtext.rm": "Charter", "mathtext.it": "Charter:italic",
    "mathtext.bf": "Charter:bold", "mathtext.fallback": "stix",
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "axes.edgecolor": INK3, "axes.linewidth": 0.8, "axes.labelcolor": INK2, "axes.labelsize": 12.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK3, "ytick.color": INK3, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11.5, "xtick.major.size": 4, "ytick.major.size": 4,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "xtick.minor.size": 0, "ytick.minor.size": 0,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.top": False, "ytick.right": False,
    "lines.solid_capstyle": "round", "lines.dash_capstyle": "butt",
}
RING = [patheffects.withStroke(linewidth=5, foreground=PAPER)]


def curve(path):
    """Median over posterior draws of the cosmic time [Gyr] at which each fraction F of the formed mass was in place."""
    with h5py.File(trends.ROOT / path / "ceridwen_derived_outputs.h5") as h:
        edges = h["sfh/lookback_time_gyr"][:]
        fractions = h["sfh/mass_fraction_draws"][:]
    return np.median(edges[-1] - trends.lookback_quantile(edges, fractions, 1 - F), axis=0)


def main():
    g = pd.read_csv(TRENDS / "per-galaxy.csv")
    g = g[(g.arm == "cn_free") & g.main & g.logmass_cosmos2020.notna()]
    t = np.array([curve(p) for p in g.path])
    mass = g.logmass_cosmos2020.to_numpy()
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(WIDTH, 4.9), layout="constrained")
        fig.get_layout_engine().set(h_pad=0.08, w_pad=0.1)
        for f, label in LEVELS.items():
            ax.axhline(f, color=INK3, lw=0.9, ls=(0, (1, 2.2)), zorder=1)
            ax.text(7.95, f + 0.015, label, color=INK2, fontsize=13, ha="right", va="bottom")
        for label, colour, lo, hi in BINS:
            s = t[(mass >= lo) & (mass < hi)]
            med = np.median(s, axis=0)
            ax.fill_betweenx(F, np.quantile(s, 0.16, axis=0), np.quantile(s, 0.84, axis=0), color=colour, alpha=0.09,
                             lw=0, zorder=2)
            ax.plot(med, F, color=colour, lw=2.4, path_effects=RING, zorder=3)
            print(label, len(s), {k: round(float(med[F == f][0]), 2) for f, k in zip(LEVELS, ("t20", "t50", "t80"))})
        for i, (label, colour, lo, hi) in enumerate(BINS):  # key: high mass first, the curves' left-to-right order
            y = 0.42 - 0.075 * i
            ax.plot([5.75, 6.15], [y, y], color=colour, lw=2.4, solid_capstyle="butt")
            ax.text(6.27, y, f"{label} ({((mass >= lo) & (mass < hi)).sum()})", color=INK, fontsize=12.5, va="center")
        ax.set(xlim=(0, 8), ylim=(0, 1.02), xticks=[0, 2, 4, 6, 8], yticks=[0, 0.2, 0.5, 0.8, 1],
               xlabel="Cosmic time (Gyr)", ylabel="Fraction of stellar mass formed")
        ax.set_yticklabels(["0", "0.2", "0.5", "0.8", "1"])
        top = ax.secondary_xaxis("top", functions=(trends.time_to_z, trends.z_to_time))
        top.set_xticks([5, 3, 2, 1.5, 1, 0.8, 0.6], ["5", "3", "2", "1.5", "1", "0.8", "0.6"])
        top.set_xlabel(r"$z$", color=INK2)
        top.tick_params(colors=INK2)
        fig.suptitle(r"C/N-free fits: mass assembly by $M_\star$", x=0.012, ha="left", color=INK, fontsize=14)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUT, dpi=200)
        plt.close(fig)


if __name__ == "__main__":
    main()
