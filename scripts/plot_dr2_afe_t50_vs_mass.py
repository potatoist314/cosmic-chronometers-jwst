"""[alpha/Fe] and t50 against log stellar mass for the DR2 quiescent sample (CPU only).

Reads ``results/dr2-quiescent-new-defaults-summary.csv`` (187 galaxies) and draws two
panels on one shared mass axis. One point per galaxy: posterior median with 16-84%
bars in x and y. Open markers have an [alpha/Fe] median within 0.02 dex of an edge
of the Uniform(-0.2, 0.6) prior; the area outside the prior is shaded. Dotted lines
mark the SFH lookback bin edges inside the t50 range. The orange line is the median
of the posterior medians in 10 equal-count mass bins. t50 is the lookback time from
the epoch of observation before which 50% of the stellar mass formed.

Writes ``wiki/analyses/dr2-quiescent-sample/afe-t50-vs-mass.png``.

Usage: ``ceridwen/.venv/bin/python scripts/plot_dr2_afe_t50_vs_mass.py``
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
OUT_PATH = PROJECT_ROOT / "wiki/analyses/dr2-quiescent-sample/afe-t50-vs-mass.png"

BLUE, ORANGE, GREY, WASH = "#0072B2", "#E69F00", "#7A7A7A", "#EFEFEF"
AFE_PRIOR = (-0.2, 0.6)  # Uniform prior on afe stored in every ceridwen_result.h5
EDGE_TOL = 0.02  # dex; a median closer than this to a prior edge is drawn open
SFH_EDGES = (3.0, 5.0)  # sfh_lookback_gyr edges inside the plotted t50 range
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
    }
)


def running_median(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Median x and median y in N_RUN equal-count bins of x."""
    bins = np.array_split(np.argsort(x), N_RUN)
    return np.array([np.median(x[b]) for b in bins]), np.array([np.median(y[b]) for b in bins])


def main() -> None:
    fits = pd.read_csv(SUMMARY_PATH)
    mass = fits.logmass_q50.to_numpy()
    mass_err = np.array([mass - fits.logmass_q16, fits.logmass_q84 - mass])

    def points(ax, name, mask, **kwargs):
        q16, q50, q84 = (fits[f"{name}_{q}"].to_numpy() for q in ("q16", "q50", "q84"))
        ax.errorbar(
            mass[mask], q50[mask], xerr=mass_err[:, mask], yerr=[(q50 - q16)[mask], (q84 - q50)[mask]],
            fmt="o", ms=3.2, color=BLUE, ecolor=BLUE, elinewidth=0.6, alpha=0.4, zorder=2, **kwargs,
        )

    def trend(ax, name):
        return ax.plot(*running_median(mass, fits[f"{name}_q50"].to_numpy()), color=ORANGE, lw=1.8, zorder=3)[0]

    fig, (top, bot) = plt.subplots(2, 1, figsize=(6.4, 6.3), sharex=True, gridspec_kw={"hspace": 0.06})

    afe = fits.alpha_fe_q50.to_numpy()
    at_edge = np.minimum(afe - AFE_PRIOR[0], AFE_PRIOR[1] - afe) < EDGE_TOL
    top.axhspan(-1, AFE_PRIOR[0], color=WASH, lw=0, zorder=0)
    top.axhspan(AFE_PRIOR[1], 2, color=WASH, lw=0, zorder=0)
    for edge in AFE_PRIOR:
        top.axhline(edge, color=GREY, lw=0.8, ls=(0, (4, 3)), zorder=0.5)
    points(top, "alpha_fe", ~at_edge)
    points(top, "alpha_fe", at_edge, mfc="white", mew=0.8)
    line = trend(top, "alpha_fe")
    top.set_ylim(-0.29, 0.69)
    top.set_yticks([-0.2, 0, 0.2, 0.4, 0.6])
    top.set_ylabel(r"$[\alpha/\mathrm{Fe}]$ [dex]")
    top.text(
        0.992, AFE_PRIOR[1] + 0.045, "outside the prior, Uniform($-0.2$, $0.6$)",
        transform=top.get_yaxis_transform(), ha="right", va="center", fontsize=7.5, color="#555555",
    )

    for edge in SFH_EDGES:
        bot.axhline(edge, color=GREY, lw=0.7, ls=":", zorder=0.5)
    bot.text(
        0.992, SFH_EDGES[0] - 0.06, "SFH bin edges, 3 and 5 Gyr",
        transform=bot.get_yaxis_transform(), ha="right", va="top", fontsize=7.5, color="#555555",
    )
    points(bot, "t50", np.ones(len(fits), bool))
    trend(bot, "t50")
    bot.set_ylim(1.0, 7.0)
    bot.set_ylabel(r"$t_{50}$, lookback from observation [Gyr]")
    bot.set_xlabel(r"$\log_{10}(M_\star/M_\odot)$")
    bot.set_xlim(10.68, 12.17)
    bot.set_xticks([10.8, 11.0, 11.2, 11.4, 11.6, 11.8, 12.0])

    dot = plt.Line2D([], [], marker="o", ms=3.6, ls="", color=BLUE, alpha=0.7)
    ring = plt.Line2D([], [], marker="o", ms=3.6, ls="", color=BLUE, mfc="white", mew=0.8)
    top.legend(
        [dot, ring, line, plt.Line2D([], [], ls="")],
        [
            f"galaxy, posterior median, 16-84% bars ({len(fits)})",
            f"median within {EDGE_TOL} dex of a prior edge ({int(at_edge.sum())})",
            f"median of medians, {N_RUN} equal-count mass bins",
            "",
        ],
        loc="lower left", bbox_to_anchor=(-0.01, 1.0), ncol=2, fontsize=7.5, frameon=False,
        handletextpad=0.5, labelspacing=0.45, columnspacing=1.6, borderaxespad=0.2,
    )

    fig.align_ylabels([top, bot])
    fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.08)
    print(OUT_PATH)


if __name__ == "__main__":
    main()
