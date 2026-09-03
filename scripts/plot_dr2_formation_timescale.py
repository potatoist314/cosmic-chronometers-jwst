"""Formation-timescale (delta-t) plots for the DR2 quiescent sample (CPU only).

Reads ``results/dr2-quiescent-summary.csv`` and plots delta-t = t80 - t20
against formation epoch (t50 lookback with a Planck18 z_form top axis, and
observed redshift), stellar mass, and [alpha/Fe], each with a running median.
Writes PDF + PNG into the bridge reports folder.

Usage: ``.venv/bin/python scripts/plot_dr2_formation_timescale.py``
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.cosmology import Planck18
from matplotlib import rcParams

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
OUT_DIR = Path.home() / ".claude/scripts/hermes-bridge/reports/ceridwen-plots"

BLUE, ORANGE = "#0072B2", "#E69F00"
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

_Z_GRID = np.linspace(0.0, 10.0, 4000)
_AGE_GRID = Planck18.age(_Z_GRID).value  # cosmic age at each redshift


def z_form_of(t50_lookback: np.ndarray, z_obs: np.ndarray) -> np.ndarray:
    """Formation redshift from formation lookback measured at z_obs.

    t50 is lookback from the observation epoch, so the formation cosmic age
    is age(z_obs) - t50, inverted to redshift. Planck18 is assumed.
    """
    age_obs = np.interp(z_obs, _Z_GRID, _AGE_GRID)
    age_form = np.clip(age_obs - t50_lookback, _AGE_GRID[-1], _AGE_GRID[0])
    return np.interp(age_form, _AGE_GRID[::-1], _Z_GRID[::-1])


def running_median(x: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    """Median y in equal-count x bins with 16-84 percentile spread."""
    order = np.argsort(x)
    bins = np.array_split(order, N_RUN)
    rows = [
        {
            "x": float(np.median(x[b])),
            "y": float(np.median(y[b])),
            "y16": float(np.quantile(y[b], 0.16)),
            "y84": float(np.quantile(y[b], 0.84)),
            "n": len(b),
        }
        for b in bins
    ]
    return pd.DataFrame(rows)


def panel(axis, x, y, yerr, run, xlabel, xlim=None):
    axis.errorbar(x, y, yerr=yerr, fmt="o", ms=3, alpha=0.3, color=BLUE,
                  ecolor=BLUE, elinewidth=0.6)
    axis.plot(run["x"], run["y"], color=ORANGE, lw=1.8, label="Running median")
    axis.fill_between(run["x"], run["y16"], run["y84"], color=ORANGE, alpha=0.25)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(r"$\Delta t = t_{80}-t_{20}$ [Gyr]")
    if xlim is not None:
        axis.set_xlim(xlim)
    axis.grid(False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(SUMMARY_PATH)
    n = len(frame)
    y = frame["dt_q50"].to_numpy()
    yerr = [y - frame["dt_q16"].to_numpy(), frame["dt_q84"].to_numpy() - y]

    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.1), sharey=True)
    t50 = frame["t50_q50"].to_numpy()
    zobs = frame["z"].to_numpy()
    zform = z_form_of(t50, zobs)
    panel(axes[0], t50, y, yerr, running_median(t50, y),
          "Formation epoch $t_{50}$ lookback [Gyr]")
    panel(axes[1], zform, y, yerr, running_median(zform, y),
          r"Formation redshift $z_{\rm form}$ (Planck18)")
    panel(axes[2], zobs, y, yerr, running_median(zobs, y),
          "Observed redshift $z_{\\rm obs}$")
    fig.suptitle(f"Ceridwen DR2 quiescent formation timescale (N={n})", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig(OUT_DIR / "dt-vs-formation-epoch.pdf")
    fig.savefig(OUT_DIR / "dt-vs-formation-epoch.png")
    plt.close(fig)

    for key, xlabel, stem in [
        ("logmass_q50", r"$\log M_\star\,[M_\odot]$", "dt-vs-mass"),
        ("alpha_fe_q50", r"$[\alpha/{\rm Fe}]$ [dex]", "dt-vs-alpha"),
    ]:
        fig, axis = plt.subplots(figsize=(5.2, 3.4))
        x = frame[key].to_numpy()
        panel(axis, x, y, yerr, running_median(x, y), xlabel)
        axis.set_title(f"Ceridwen DR2 quiescent formation timescale (N={n})",
                       fontsize=10)
        fig.tight_layout()
        fig.savefig(OUT_DIR / f"{stem}.pdf")
        fig.savefig(OUT_DIR / f"{stem}.png")
        plt.close(fig)

    report = frame[["target", "z", "t50_q50", "dt_q50"]].copy()
    report["z_form_planck18"] = z_form_of(
        report["t50_q50"].to_numpy(), report["z"].to_numpy())
    print(report.sort_values("dt_q50").head(3).to_string(index=False))
    print(f"median dt={np.median(y):.2f} Gyr; "
          f"spearman(dt,t50)={pd.Series(y).corr(pd.Series(t50), method='spearman'):.2f}, "
          f"spearman(dt,logM)={pd.Series(y).corr(frame['logmass_q50'], method='spearman'):.2f}, "
          f"spearman(dt,afe)={pd.Series(y).corr(frame['alpha_fe_q50'], method='spearman'):.2f}")
    print("wrote dt plots to", OUT_DIR)


if __name__ == "__main__":
    main()
