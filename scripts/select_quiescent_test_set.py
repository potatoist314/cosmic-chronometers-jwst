"""Select the 10-galaxy quiescent test set spread over physical properties.

Parent: DR2 quiescent fits with COSMOS2025 warn-flag = 0 and COSMOS2020
Classic FlagCOMBINED = 0. Galaxies with data problems and galaxies outside the
parent 5.6-94.4 percentile band on any axis are removed. The 10 chosen have
sorted parent percentiles on each axis closest to 10, 18.9, ..., 90 (least
squares); M1_210210 is fixed; the search is seeded.

Usage (CPU only)::

    .venv/bin/python scripts/select_quiescent_test_set.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import cosmos_photometry

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_CSV = PROJECT_ROOT / "results/dr2-quiescent-new-defaults-summary.csv"
DIAGNOSTICS_CSV = PROJECT_ROOT / "results/per-galaxy-diagnostics.csv"
OUT_DIR = PROJECT_ROOT / "results/quiescent-test-set"

SEED = 20260929
FIXED = "M1_210210"
N_STARTS = 200
# summary column: weight in the least-squares match
AXES = {"logmass_q50": 1.0, "age_q50": 1.0, "sigma_star_kms": 1.0, "feh_q50": 1.0,
        "tau_dust_q50": 1.0, "z": 0.5}
TARGET_Q = np.linspace(0.10, 0.90, 10)
HALF_STEP = (TARGET_Q[1] - TARGET_Q[0]) / 2


def parent() -> pd.DataFrame:
    """Fits whose COSMOS2025 and COSMOS2020 Classic photometry flags are 0."""
    tables = cosmos_photometry.read_matches()
    summary = pd.read_csv(SUMMARY_CSV)
    clean = [
        sid in tables["cosmos2025"] and int(tables["cosmos2025"][sid]["warn-flag"]) == 0
        and sid in tables["classic"] and int(tables["classic"][sid]["FlagCOMBINED"]) == 0
        for sid in summary.spect_id
    ]
    keep = ["spect_id", "phot_redchi2_stored", "spec_redchi2_stored", "calib_saturated",
            "n_outlier_pixels", "worst_band_pull"]
    table = summary[clean].merge(pd.read_csv(DIAGNOSTICS_CSV)[keep], on="spect_id")
    for axis in AXES:
        table["u_" + axis] = [stats.percentileofscore(table[axis], x, kind="mean") / 100
                              for x in table[axis]]
    return table


def data_problems(table: pd.DataFrame) -> tuple[pd.Series, dict]:
    thresholds = {
        "sn_p16": table.catalogue_sn.quantile(0.16),
        "phot_p84": table.phot_redchi2_stored.quantile(0.84),
        "outlier_p84": table.n_outlier_pixels.quantile(0.84),
        "bandpull_p84": table.worst_band_pull.abs().quantile(0.84),
    }
    bad = ((table.catalogue_sn < thresholds["sn_p16"])
           | (table.spec_redchi2_stored > 1.5)
           | (table.phot_redchi2_stored > thresholds["phot_p84"])
           | table.calib_saturated.astype(bool)
           | (table.n_outlier_pixels > thresholds["outlier_p84"])
           | (table.worst_band_pull.abs() > thresholds["bandpull_p84"]))
    return bad, thresholds


def select(pool: pd.DataFrame) -> list[int]:
    """Best of N_STARTS swap searches from seeded random starts."""
    u = pool[["u_" + a for a in AXES]].to_numpy()
    weights = np.array(list(AXES.values()))

    def cost(idx):
        return float((weights * (np.sort(u[idx], axis=0) - TARGET_Q[:, None]) ** 2).sum())

    fixed = int(np.flatnonzero(pool.spect_id == FIXED)[0])
    free = np.array([i for i in range(len(pool)) if i != fixed])
    rng = np.random.default_rng(SEED)
    best, best_cost = None, np.inf
    for _ in range(N_STARTS):
        chosen = [fixed] + list(rng.choice(free, 9, replace=False))
        current = cost(chosen)
        improved = True
        while improved:
            improved = False
            for i in range(1, 10):
                for j in free:
                    if j in chosen:
                        continue
                    trial = chosen.copy()
                    trial[i] = j
                    trial_cost = cost(trial)
                    if trial_cost < current - 1e-12:
                        chosen, current, improved = trial, trial_cost, True
        if current < best_cost:
            best, best_cost = sorted(chosen), current
    return best


def target_entry(row) -> dict:
    pct = {axis: round(100 * row["u_" + axis]) for axis in AXES}
    reason = (f"Parent percentiles: log M* {pct['logmass_q50']}, age {pct['age_q50']}, "
              f"sigma* {pct['sigma_star_kms']}, [Fe/H] {pct['feh_q50']}, "
              f"tau_dust {pct['tau_dust_q50']}, z {pct['z']}.")
    if row.spect_id == FIXED:
        reason = "Reference galaxy, fixed. " + reason
    return {
        "spect_id": row.spect_id, "object_id": int(row.object_id),
        "manifest_index": int(row.manifest_index), "z": round(row.z, 4),
        "sn": round(row.catalogue_sn, 1), "sigma_star_kms": round(row.sigma_star_kms, 1),
        "logmass": round(row.logmass_q50, 2), "age_gyr": round(row.age_q50, 2),
        "feh": round(row.feh_q50, 2), "tau_dust": round(row.tau_dust_q50, 2),
        "joint_chi2_per_ndof": round(row.joint_chi2_per_ndof, 2), "reason": reason,
    }


def main() -> None:
    table = parent()
    bad, th = data_problems(table)
    u = table[["u_" + a for a in AXES]]
    inside = ((u >= TARGET_Q[0] - HALF_STEP) & (u <= TARGET_Q[-1] + HALF_STEP)).all(axis=1)
    pool = table[~bad & inside].reset_index(drop=True)
    chosen = pool.iloc[select(pool)].sort_values("manifest_index")
    targets = [target_entry(row) for _, row in chosen.iterrows()]
    out = {
        "schema_version": 1,
        "sample": "LEGA-C DR2 quiescent test set, 10 galaxies",
        "selected_on": "2026-09-29",
        "parent_manifest": "results/dr2-quiescent-new-defaults/targets.json",
        "method": "Spread over physical properties, inside the parent population",
        "seed": SEED,
        "selection": [
            f"Parent: {len(table)} of the 187 fits with COSMOS2025 warn-flag = 0 and COSMOS2020 Classic FlagCOMBINED = 0.",
            (f"Excluded data problems: S/N below parent P16 ({th['sn_p16']:.1f}); spectrum chi2/N > 1.5; "
             f"photometry chi2/N above parent P84 ({th['phot_p84']:.1f}); f_calib at its prior bound; "
             f"pixels with |pull| > 4 above parent P84 ({th['outlier_p84']:.0f}); "
             f"worst band |pull| above parent P84 ({th['bandpull_p84']:.1f})."),
            "Axes: posterior-median log M*, mass-weighted age, [Fe/H] and tau_dust; catalogue sigma*; z at half weight.",
            f"Kept galaxies with every axis between parent percentiles 5.6 and 94.4; {len(pool)} remain.",
            ("Chose the 10 whose sorted parent percentiles on each axis best match 10, 18.9, ..., 90 (least squares); "
             f"{FIXED} fixed; best of {N_STARTS} swap searches from random starts drawn with numpy default_rng(seed)."),
        ],
        "sources": {
            "z, sn, sigma_star_kms": "LEGA-C DR2 z, SN (overall median S/N per pixel), SIGMA_STARS_PRIME; data/raw/legac_dr2/VizieR_ReadMe.txt",
            "logmass, age_gyr, feh, tau_dust, joint_chi2_per_ndof": "posterior medians of the 187 fits (7 SFH bins, order-3 calibration, cosmos_total photometry, tau_dust Uniform(0, 2)); results/dr2-quiescent-new-defaults-summary.csv",
            "chi2/N, f_calib, pulls": "results/per-galaxy-diagnostics.csv, scripts/per_galaxy_diagnostics.py",
            "COSMOS2025": "Shuntov et al. (2025), VizieR J/A+A/704/A339/phot, 1 arcsec match; data/raw/cosmos2025/README.md",
            "COSMOS2020 Classic": "Weaver et al. (2022), VizieR J/ApJS/258/11/classic; data/raw/cosmos2020/README.md",
            "Photometry flag that stops a fit": "scripts/cosmos_photometry.py, fit_photometry",
        },
        "targets": targets,
    }
    (OUT_DIR / "targets.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    (OUT_DIR / "experiment.json").write_text(
        json.dumps({"targets": [t["spect_id"] for t in targets]}, indent=2) + "\n")


if __name__ == "__main__":
    main()
