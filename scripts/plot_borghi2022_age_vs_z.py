"""Recreate Borghi+2022a Fig. 9 (median age vs redshift) with our sample.

Reads ``results/dr2-quiescent-summary.csv`` and the tabulated Borghi+2022
match catalogue already in the repo. Left: individual mass-weighted ages
(``age_q50`` with 16-84 bars), the flat-737-LCDM cosmic age (grey = older
than the Universe), and dotted pure-passive tracks of constant formation
redshift. Right: median-binned relations in Borghi's bins (dz = 0.075 over
0.6 < z < 0.9, sigma split 215 km/s) with NMAD/sqrt(N) errors, overlaid
with the tabulated Borghi ages binned identically. CPU only.

Usage: ``.venv/bin/python scripts/plot_borghi2022_age_vs_z.py``
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
from matplotlib import rcParams

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
BORGHI_PATH = PROJECT_ROOT / (
    "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_spectrum_matches copy.tsv"
)
OUT_DIR = PROJECT_ROOT / "results/figures"

# Reference cosmology of Borghi+2022b ('737'), used for illustration only.
COSMO = FlatLambdaCDM(H0=70, Om0=0.3)
SIGMA_SPLIT = 215.0
Z_EDGES = np.array([0.6, 0.675, 0.75, 0.825, 0.9])
Z_FORM_TRACKS = (1.0, 1.5, 2.5, 5.0)

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


def binned(frame: pd.DataFrame, value: str) -> pd.DataFrame:
    """Median per Borghi bin with NMAD/sqrt(N) median errors."""
    rows = []
    work = frame[frame["z"].between(0.6, 0.9, inclusive="left")].copy()
    work["group"] = np.where(work["sigma_star_kms"] > SIGMA_SPLIT, "high", "low")
    work["zbin"] = pd.cut(work["z"], Z_EDGES, include_lowest=True)
    for (group, zbin), members in work.groupby(["group", "zbin"], observed=True):
        values = members[value].to_numpy()
        median = float(np.median(values))
        rows.append(
            {
                "group": group,
                "zbin": str(zbin),
                "z": float(members["z"].mean()),
                "dz": float((zbin.right - zbin.left) / 2),
                "median": median,
                "err": float(1.4826 * np.median(np.abs(values - median))
                             / np.sqrt(len(values))),
                "n": len(values),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    galaxies = pd.read_csv(SUMMARY_PATH)
    borghi = pd.read_csv(BORGHI_PATH, sep="\t", comment="#")
    full = (borghi.sort_values("dr2_sn_per_pixel")
            .drop_duplicates("mms2013_id", keep="last"))
    full = full[full["borghi_age_gyr"].notna()].copy()
    full["z"] = full["dr2_z_spec"]
    full["sigma_star_kms"] = full["dr2_sigma_stars_prime_km_s"]
    print(f"full deduplicated Borghi catalogue N={len(full)}")
    groups = np.where(full["sigma_star_kms"] > SIGMA_SPLIT, "high", "low")
    print({group: int((groups == group).sum()) for group in ("low", "high")})

    ours = binned(galaxies, "age_q50")
    theirs = binned(full, "borghi_age_gyr")

    zz = np.linspace(0.55, 1.0, 400)
    age_universe = COSMO.age(zz).value

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4), sharey=True)
    axes[0].fill_between(zz, age_universe, 14, color="grey", alpha=0.25,
                         linewidth=0)
    for zform in Z_FORM_TRACKS:
        track = age_universe - COSMO.age(zform).value
        positive = np.where(track > 0, track, np.nan)
        axes[0].plot(zz, positive, color="black", lw=0.8, ls=":", alpha=0.7)
        axes[0].text(0.9, float(np.interp(0.9, zz, positive)), f"{zform:g}",
                     fontsize=7, va="center", ha="left", alpha=0.8)
    for group, color in [("low", BLUE), ("high", ORANGE)]:
        members = galaxies[
            (np.where(galaxies["sigma_star_kms"] > SIGMA_SPLIT, "high", "low")
             == group)]
        axes[0].errorbar(
            members["z"], members["age_q50"],
            yerr=[members["age_q50"] - members["age_q16"],
                  members["age_q84"] - members["age_q50"]],
            fmt="o", ms=2.5, alpha=0.3, color=color, ecolor=color,
            elinewidth=0.6, label=f"{group} sigma (N={(members['z'] < 99).sum()})")
    axes[0].set_xlim(0.55, 1.0)
    axes[0].set_ylim(0, 9)
    axes[0].set_xlabel("Redshift $z$")
    axes[0].set_ylabel("Mass-weighted age [Gyr]")
    axes[0].legend(frameon=False, fontsize=7.5)
    axes[0].set_title("Individual ages", fontsize=10)

    for group, color in [("low", BLUE), ("high", ORANGE)]:
        b = ours[ours["group"] == group]
        axes[1].errorbar(b["z"], b["median"], xerr=b["dz"], yerr=b["err"],
                         fmt="s", ms=5, color=color, ecolor="black",
                         elinewidth=1, capsize=3, label=f"Ceridwen {group}")
        t = theirs[theirs["group"] == group]
        axes[1].errorbar(t["z"], t["median"], xerr=t["dz"], yerr=t["err"],
                         fmt="D", ms=5, mfc="none", mec=GREY, ecolor=GREY,
                         elinewidth=1, capsize=3, label=f"Borghi+22 {group}")
    axes[1].plot(zz, age_universe, color="black", lw=1)
    axes[1].set_xlim(0.55, 1.0)
    axes[1].set_xlabel("Redshift $z$")
    axes[1].legend(frameon=False, fontsize=7.5, loc="upper left")
    axes[1].set_title("Binned medians (Borghi bins)", fontsize=10)
    fig.suptitle("Ceridwen DR2 quiescent ages vs redshift, Borghi+2022 style "
                 f"(N={len(galaxies)})", fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(OUT_DIR / "borghi2022-age-vs-z.pdf")
    fig.savefig(OUT_DIR / "borghi2022-age-vs-z.png")
    plt.close(fig)

    comp = ours.merge(theirs, on=["group", "zbin"],
                      suffixes=("_cer", "_bor"))
    comp["delta"] = comp["median_cer"] - comp["median_bor"]
    print(comp[["group", "zbin", "n_cer", "median_cer", "n_bor",
                "median_bor", "delta"]].to_string(index=False))
    print(f"mean Ceridwen-Borghi binned offset: {comp['delta'].mean():.2f} Gyr")
    print("wrote", OUT_DIR / "borghi2022-age-vs-z.{pdf,png}")


if __name__ == "__main__":
    main()
