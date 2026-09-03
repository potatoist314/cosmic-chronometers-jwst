"""Build a tidy one-row-per-galaxy summary of the DR2 quiescent run.

Reads every target in
``results/rtx-5060-dr2-quiescent-full-spectrum/targets.json`` directly from
its ``ceridwen_derived_outputs.h5`` / ``ceridwen_result.h5`` pair and writes
``results/dr2-quiescent-summary.csv``. Every sample-level plot is then
reproducible from that single CSV.

Usage (CPU only): ``.venv/bin/python scripts/build_dr2_quiescent_summary.py``
"""

from __future__ import annotations

import json
from pathlib import Path

import h5py
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
OUT_PATH = PROJECT_ROOT / "results/dr2-quiescent-summary.csv"

SUMMARY_PARAMS = {
    "logmass": "logmass",
    "Z": "logZ_abs",
    "afe": "alpha_fe",
    "diffuse_tau_kc": "tau_dust",
}


def _str(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def load_target(target: dict) -> dict:
    """Summarise one target folder into a flat dict."""
    folder = RESULT_ROOT / f"{target['object_id']}-{target['spect_id']}"
    row: dict = {
        "target": f"{target['object_id']}-{target['spect_id']}",
        "object_id": target["object_id"],
        "spect_id": target["spect_id"],
    }
    with h5py.File(folder / "ceridwen_derived_outputs.h5", "r") as derived:
        row["z"] = float(derived.attrs["redshift"])
        row["sigma_star_kms"] = float(derived.attrs["sigma_star_kms"])
        row["catalogue_sn"] = float(derived.attrs["catalogue_sn"])
        row["manifest_index"] = int(derived.attrs["manifest_index"])
        row["seed"] = int(derived.attrs["random_seed"])
        names = [_str(v) for v in derived["summary/parameter"][:]]
        q16 = derived["summary/q16"][:]
        q50 = derived["summary/q50"][:]
        q84 = derived["summary/q84"][:]
        table = {name: (a, b, c) for name, a, b, c in zip(names, q16, q50, q84)}
        for raw, prefix in SUMMARY_PARAMS.items():
            a, b, c = table[raw]
            row[f"{prefix}_q16"], row[f"{prefix}_q50"], row[f"{prefix}_q84"] = (
                float(a),
                float(b),
                float(c),
            )
        age = derived["sfh/mass_weighted_age_gyr"][:]
        row["age_q16"], row["age_q50"], row["age_q84"] = (float(v) for v in np.quantile(age, [0.16, 0.5, 0.84]))
        diag = derived["diagnostics"].attrs
        row["passed"] = bool(diag["passed"])
        row["joint_chi2"] = float(diag["joint_chi2"])
        row["joint_ndof"] = int(diag["joint_ndof"])
        row["spectrum_chi2"] = float(diag["spectrum_chi2"])
        row["spectrum_ndof"] = int(diag["spectrum_ndof"])
        row["photometry_chi2"] = float(diag["photometry_chi2"])
        row["photometry_ndof"] = int(diag["photometry_ndof"])
        row["ess"] = float(diag["posterior_weight_ess"])
        row["lnZ"] = float(diag["log_evidence"])
        row["lnZ_err"] = float(diag["log_evidence_err"])
    with h5py.File(folder / "ceridwen_result.h5", "r") as result:
        samples = result["samples"]
        row["n_calls"] = int(samples.attrs["n_likelihood_calls"])
        row["n_samples"] = int(samples.attrs["n_samples"])
        row["wall_time_s"] = float(samples.attrs["wall_time_s"])
    return row


def main() -> None:
    manifest = json.loads((RESULT_ROOT / "targets.json").read_text())
    rows = [load_target(target) for target in manifest["targets"]]
    frame = pd.DataFrame(rows).sort_values("object_id").reset_index(drop=True)
    frame["joint_chi2_per_ndof"] = frame["joint_chi2"] / frame["joint_ndof"]
    frame.to_csv(OUT_PATH, index=False)
    print(f"wrote {OUT_PATH} with {len(frame)} rows")
    print(f"passed diagnostics: {int(frame['passed'].sum())}/{len(frame)}")


if __name__ == "__main__":
    main()
