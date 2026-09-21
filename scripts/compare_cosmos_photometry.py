#!/usr/bin/env python3
"""Compare COSMOS2020 and COSMOS2025 photometry with the COSMOS2015 fit input.

Writes three tables to results/cosmos-photometry-comparison/ for the 187 fitted
LEGA-C DR2 quiescent galaxies:

- match.csv       one row per galaxy: match separation in each catalogue
- bands.csv       one row per galaxy, catalogue and band: catalogue flux, the
                  total flux that would enter the fit, and its statistical error
- ratios.csv      bands.csv joined to COSMOS2015 on the same filter: flux ratio
                  and error ratio new/2015

scripts/cosmos_photometry.py defines the total flux of each catalogue.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from cosmos_photometry import FILES, read_matches, total_photometry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
OUTPUT = PROJECT_ROOT / "results/cosmos-photometry-comparison"
# Bands of the comparison tables and figure; the fit also uses the other intermediate bands.
COMPARISON_BANDS = [
    "NUV", "u", "u*", "IB427", "B", "IB464", "g", "IA484", "V", "r", "r+", "i", "i+", "F814W",
    "z", "z++", "y", "Y", "F115W", "J", "F150W", "H", "Ks", "F277W", "ch1", "F444W", "ch2",
]


def main() -> None:
    summary = pd.read_csv(SUMMARY)
    tables = read_matches()

    match_rows, band_frames = [], []
    for spect_id in summary["spect_id"]:
        match = {"spect_id": spect_id}
        for catalogue, rows in tables.items():
            match[f"sep_{catalogue}_arcsec"] = (
                float(rows[spect_id]["MATCH_SEP_ARCSEC"]) if spect_id in rows else np.nan
            )
        match_rows.append(match)
        band_frames.append(total_photometry(tables, spect_id, COMPARISON_BANDS))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    matches = pd.DataFrame(match_rows)
    bands = pd.concat(band_frames, ignore_index=True)
    reference = bands[bands["catalogue"] == "cosmos2015"][
        ["spect_id", "band", "total_flux_ujy", "total_error_ujy"]
    ]
    ratios = bands[bands["catalogue"] != "cosmos2015"].merge(
        reference, on=["spect_id", "band"], suffixes=("", "_2015")
    )
    ratios["flux_ratio"] = ratios["total_flux_ujy"] / ratios["total_flux_ujy_2015"]
    ratios["error_ratio"] = ratios["total_error_ujy"] / ratios["total_error_ujy_2015"]
    matches.to_csv(OUTPUT / "match.csv", index=False)
    bands.to_csv(OUTPUT / "bands.csv", index=False)
    ratios.to_csv(OUTPUT / "ratios.csv", index=False)

    for catalogue in FILES:
        separation = matches[f"sep_{catalogue}_arcsec"].dropna()
        print(
            f"{catalogue}: {len(separation)}/{len(matches)} matched, separation median "
            f"{separation.median():.3f} max {separation.max():.3f} arcsec"
        )


if __name__ == "__main__":
    main()
