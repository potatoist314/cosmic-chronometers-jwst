"""Candidate headline layouts for the DR2 quiescent sample (CPU only).

Reads ``results/dr2-quiescent-summary.csv`` plus the published Borghi+2022
match table already in the repo, and writes three candidate age-redshift
headline figures (PDF + PNG) into the bridge reports folder for style
selection. The winning style is then applied to the full figure set.

Usage: ``.venv/bin/python scripts/plot_dr2_headline_candidates.py``
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams

matplotlib.use("Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"
BORGHI_PATH = PROJECT_ROOT / (
    "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_spectrum_matches copy.tsv"
)
OUT_DIR = Path.home() / ".claude/scripts/hermes-bridge/reports/ceridwen-plots"

# Okabe-Ito colour-blind-safe palette.
BLUE, ORANGE, GREEN, GREY = "#0072B2", "#E69F00", "#009E73", "#999999"
SIGMA_SPLIT = 215.0
Z_EDGES = np.array([0.6, 0.675, 0.75, 0.825, 0.9])

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


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Sample table plus the Borghi overlap joined on object id."""
    galaxies = pd.read_csv(SUMMARY_PATH)
    borghi = pd.read_csv(BORGHI_PATH, sep="\t", comment="#")
    best = borghi.sort_values("dr2_sn_per_pixel").drop_duplicates(
        "mms2013_id", keep="last"
    )
    overlap = galaxies.merge(
        best[
            [
                "mms2013_id",
                "borghi_age_gyr",
                "borghi_age_err_lower_gyr",
                "borghi_age_err_upper_gyr",
            ]
        ],
        left_on="object_id",
        right_on="mms2013_id",
        how="inner",
    )
    return galaxies, overlap


def add_bands(frame: pd.DataFrame) -> pd.DataFrame:
    """Attach sigma group and fixed redshift bin labels (Borghi construction)."""
    out = frame.copy()
    out["group"] = np.where(
        out["sigma_star_kms"] > SIGMA_SPLIT, "high sigma", "low sigma"
    )
    out["zbin"] = pd.cut(
        out["z"], Z_EDGES, labels=[1, 2, 3, 4], include_lowest=True
    )
    return out


def binned_median(frame: pd.DataFrame, value: str) -> pd.DataFrame:
    """Median age per bin with NMAD/sqrt(N) uncertainty (Borghi estimator)."""
    rows = []
    grouped = frame.dropna(subset=["zbin"]).groupby(["group", "zbin"], observed=True)
    for (group, zbin), members in grouped:
        values = members[value].to_numpy()
        median = float(np.median(values))
        nmad = float(1.4826 * np.median(np.abs(values - median)))
        rows.append(
            {
                "group": group,
                "zbin": zbin,
                "z": float(members["z"].median()),
                "median": median,
                "err": nmad / np.sqrt(len(values)),
                "n": len(values),
            }
        )
    return pd.DataFrame(rows)


def style_axes(axes) -> None:
    for axis in np.atleast_1d(axes):
        axis.grid(False)
        for spine in axis.spines.values():
            spine.set_visible(True)


def layout_a_split_panels(galaxies: pd.DataFrame, overlap: pd.DataFrame) -> None:
    """Two panels split by velocity dispersion; binned Ceridwen vs Borghi."""
    binned = binned_median(galaxies, "age_q50")
    binned_borghi = binned_median(overlap, "borghi_age_gyr")
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.1), sharey=True)
    titles = {"low sigma": "Low sigma (<215 km/s)", "high sigma": "High sigma (>215 km/s)"}
    for axis, (group, color) in zip(axes, [("low sigma", BLUE), ("high sigma", ORANGE)]):
        members = galaxies[add_bands(galaxies)["group"] == group]
        axis.errorbar(
            members["z"],
            members["age_q50"],
            yerr=[members["age_q50"] - members["age_q16"], members["age_q84"] - members["age_q50"]],
            fmt="o",
            ms=2.5,
            alpha=0.35,
            color=color,
            ecolor=color,
            elinewidth=0.6,
        )
        b = binned[binned["group"] == group]
        h1 = axis.errorbar(b["z"] - 0.004, b["median"], yerr=b["err"], fmt="s", ms=5, color=color, ecolor="black", elinewidth=1, capsize=3, label="Ceridwen binned")
        bb = binned_borghi[binned_borghi["group"] == group]
        h2 = axis.errorbar(bb["z"] + 0.004, bb["median"], yerr=bb["err"], fmt="D", ms=5, mfc="none", mec=GREY, ecolor=GREY, elinewidth=1, capsize=3, label="Borghi+22 binned")
        axis.set_xlabel("Redshift $z$")
        axis.set_title(titles[group])
        if group == "low sigma":
            handles = [h1, h2]
    axes[0].set_ylabel("Mass-weighted age [Gyr]")
    fig.suptitle(f"Ceridwen DR2 quiescent ages vs redshift (N={len(galaxies)})", fontsize=10)
    style_axes(axes)
    fig.legend(handles=handles, frameon=False, fontsize=8, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.04, 1, 0.92))
    fig.savefig(OUT_DIR / "candidate-A-split-panels.pdf")
    fig.savefig(OUT_DIR / "candidate-A-split-panels.png")
    plt.close(fig)


def layout_b_single_with_residual(galaxies: pd.DataFrame, overlap: pd.DataFrame) -> None:
    """Single age-z panel for the full sample plus a Ceridwen-Borghi residual strip."""
    binned = binned_median(galaxies, "age_q50")
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    banded = galaxies
    for group, color, dx in [("low sigma", BLUE, -0.005), ("high sigma", ORANGE, 0.005)]:
        members = galaxies[banded["group"] == group]
        axes[0].errorbar(
            members["z"],
            members["age_q50"],
            yerr=[members["age_q50"] - members["age_q16"], members["age_q84"] - members["age_q50"]],
            fmt="o",
            ms=2.5,
            alpha=0.35,
            color=color,
            ecolor=color,
            elinewidth=0.6,
            label=f"{group} (N={(banded['group'] == group).sum()})",
        )
        b = binned[binned["group"] == group]
        axes[0].errorbar(b["z"] + dx, b["median"], yerr=b["err"], fmt="s", ms=5, color=color, ecolor="black", elinewidth=1, capsize=3)
    axes[0].set_ylabel("Mass-weighted age [Gyr]")
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper right")
    axes[0].set_title(f"Ceridwen DR2 quiescent ages vs redshift (N={len(galaxies)})", fontsize=10)
    resid = overlap["age_q50"] - overlap["borghi_age_gyr"]
    axes[1].axhline(0, color="black", lw=0.8)
    axes[1].scatter(overlap["z"], resid, s=8, alpha=0.5, color=GREEN)
    axes[1].set_xlabel("Redshift $z$")
    axes[1].set_ylabel("Ceridwen $-$ Borghi+22 [Gyr]")
    style_axes(axes)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "candidate-B-single-with-residual.pdf")
    fig.savefig(OUT_DIR / "candidate-B-single-with-residual.png")
    plt.close(fig)


def layout_c_mass_tinted_shifts(galaxies: pd.DataFrame, overlap: pd.DataFrame) -> None:
    """Age-z tinted by stellar mass; segments link each overlap galaxy to its Borghi age."""
    binned = binned_median(galaxies, "age_q50")
    fig, axis = plt.subplots(figsize=(6.4, 3.6))
    order = np.argsort(galaxies["logmass_q50"].to_numpy())
    sc = axis.scatter(
        galaxies["z"].to_numpy()[order],
        galaxies["age_q50"].to_numpy()[order],
        c=galaxies["logmass_q50"].to_numpy()[order],
        s=10,
        alpha=0.8,
        cmap="viridis",
        vmin=10,
        vmax=12,
    )
    for _, row in overlap.iterrows():
        axis.plot([row["z"], row["z"]], [row["age_q50"], row["borghi_age_gyr"]], color=GREY, lw=0.5, alpha=0.5)
    for group, marker in [("low sigma", "s"), ("high sigma", "^")]:
        b = binned[binned["group"] == group]
        axis.errorbar(b["z"], b["median"], yerr=b["err"], fmt=marker, ms=6, mfc="white", mec="black", ecolor="black", elinewidth=1, capsize=3, label=f"{group} binned")
    axis.set_xlabel("Redshift $z$")
    axis.set_ylabel("Mass-weighted age [Gyr]")
    axis.set_title(f"Ceridwen DR2 quiescent ages vs redshift (N={len(galaxies)}; grey links to Borghi+22)", fontsize=10)
    fig.colorbar(sc, ax=axis, label=r"$\log M_\star\,[M_\odot]$")
    axis.legend(frameon=False, fontsize=7.5)
    style_axes(axis)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "candidate-C-mass-tinted-shifts.pdf")
    fig.savefig(OUT_DIR / "candidate-C-mass-tinted-shifts.png")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    galaxies, overlap = load()
    galaxies, overlap = add_bands(galaxies), add_bands(overlap)
    print(f"sample N={len(galaxies)}, Borghi overlap N={len(overlap)}")
    layout_a_split_panels(galaxies, overlap)
    layout_b_single_with_residual(galaxies, overlap)
    layout_c_mass_tinted_shifts(galaxies, overlap)
    print("wrote candidates A/B/C (PDF + PNG) to", OUT_DIR)


if __name__ == "__main__":
    main()
