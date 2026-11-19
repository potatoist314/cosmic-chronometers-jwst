#!/usr/bin/env python3
"""Fake-galaxy age against redshift: true and fitted mass-weighted ages of the 194 window mocks.

    ceridwen/.venv/bin/python results/mock-slope-figures-2026-11-18/age_redshift.py

Reads results/mock-chronometer-window-2026-11-13/per-mock.csv. Lines are least squares through all 194 mocks;
H(z_eff) from the slope as in that experiment.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patheffects

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
MOCK = ROOT / "results/mock-chronometer-window-2026-11-13"
OUT = Path(__file__).resolve().parent / "mock-age-redshift.png"

spec = importlib.util.spec_from_file_location("mocks", MOCK / "mocks.py")
mocks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mocks)  # line_fit: least squares and galaxy bootstrap

from scripts.plot_afe_age_chronometer import AGE_LABEL, ARMS, INK, INK3, PAPER, REDSHIFT, STYLE, WIDTH  # noqa: E402
from src.chronometer import effective_redshift, hubble_from_age_slope  # noqa: E402

TRUE, FIT = INK3, ARMS["plain"][1]
DOT = {"true_age_gyr": (TRUE, 0.45), "age_q50": (FIT, 0.30)}  # colour, alpha of the per-mock dots
LABELS = {"age_q50": (0.83, 4.86), "true_age_gyr": (0.606, 3.62)}  # lower-left corner of each line label
LARGE = {"font.size": 12, "axes.linewidth": 0.8, "axes.labelsize": 12.5, "xtick.labelsize": 11.5,
         "ytick.labelsize": 11.5, "xtick.major.size": 4, "ytick.major.size": 4, "xtick.major.width": 0.8,
         "ytick.major.width": 0.8,
         # the ceridwen import sets inward ticks on all four sides
         "xtick.direction": "out", "ytick.direction": "out", "xtick.top": False, "ytick.right": False}


def main():
    d = pd.read_csv(MOCK / "per-mock.csv")
    z = d.z.to_numpy()
    z_eff = effective_redshift(z)["z_eff"]
    fits = {col: mocks.line_fit(z, d[col].to_numpy()) for col in DOT}
    H = {col: hubble_from_age_slope(z_eff, f["slope"]) for col, f in fits.items()}
    dH = hubble_from_age_slope(z_eff, fits["age_q50"]["q84"]) - H["age_q50"]
    words = {"true_age_gyr": "True: $H$ = %.0f km/s/Mpc" % H["true_age_gyr"],
             "age_q50": "Fitted: $H$ = %.0f ± %.0f km/s/Mpc" % (H["age_q50"], dH)}

    with plt.rc_context(STYLE | LARGE):
        fig, ax = plt.subplots(figsize=(WIDTH, 4.7), layout="constrained")
        fig.get_layout_engine().set(h_pad=0.08, w_pad=0.1)
        x = np.array([z.min(), z.max()])
        ring = [patheffects.withStroke(linewidth=5, foreground=PAPER)]
        for col, (colour, alpha) in DOT.items():
            ax.scatter(z, d[col], s=9, color=colour, alpha=alpha, lw=0, zorder=1)
            # true ages lie on the true line, so only the fitted line keeps the paper ring that parts the dots
            ax.plot(x, d[col].mean() + fits[col]["slope"] * (x - z.mean()), color=colour, lw=2.2, zorder=2,
                    path_effects=ring if col == "age_q50" else [])
            ax.text(*LABELS[col], words[col], color=INK, fontsize=12.5, ha="left", va="bottom", zorder=5)
        ax.set(xlim=(0.585, 1.015), xticks=[0.6, 0.7, 0.8, 0.9, 1.0], ylim=(2.55, 6.25), yticks=[3, 4, 5, 6],
               xlabel=REDSHIFT, ylabel=AGE_LABEL)
        fig.suptitle("Fake galaxies: age against redshift", x=0.012, ha="left", color=INK, fontsize=14)
        fig.savefig(OUT, dpi=200)
        plt.close(fig)

    print(f"{len(d)} mocks, z_eff {z_eff:.4f}")
    for col, f in fits.items():
        print(f"{col}: slope {f['slope']:.4f} ({f['q16']:.4f} to {f['q84']:.4f}), H {H[col]:.2f}")


if __name__ == "__main__":
    main()
