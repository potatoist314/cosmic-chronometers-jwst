"""Compare each arm of the free-speedup check with the carry arm."""
import json
import os
import sys
from pathlib import Path

import numpy as np

OUT = Path(os.environ.get("SPEEDUP_OUT", Path(__file__).resolve().parent / "run/arms"))
REFERENCE = sys.argv[1] if len(sys.argv) > 1 else "carry"


def load(tag):
    return json.loads((OUT / tag / "summary.json").read_text()), dict(np.load(OUT / tag / "result.npz"))


def moments(data):
    weights = np.exp(data["log_weights"] - data["log_weights"].max())
    weights /= weights.sum()
    out = {}
    for key in sorted(k for k in data if k.startswith("position__")):
        values = data[key].reshape(len(weights), -1)
        mean = weights @ values
        out[key[10:]] = (mean, np.sqrt(weights @ (values - mean) ** 2))
    return out


ref_summary, ref = load(REFERENCE)
ref_moments = moments(ref)
report = {"reference": REFERENCE, "arms": {REFERENCE: ref_summary}}
for tag in sorted(p.name for p in OUT.iterdir() if (p / "summary.json").exists() and p.name != REFERENCE):
    summary, data = load(tag)
    same_shape = data["loglikelihood"].shape == ref["loglikelihood"].shape
    row = {**summary, "same_n_dead": bool(same_shape),
           "speedup_sampling_wall": ref_summary["sampling_wall_s"] / summary["sampling_wall_s"],
           "speedup_later_iterations": ref_summary["later_iterations_s"] / summary["later_iterations_s"],
           "d_log_evidence": summary["log_evidence"] - ref_summary["log_evidence"],
           "d_sampler_logZ": summary["sampler_logZ"] - ref_summary["sampler_logZ"],
           "d_n_likelihood_calls": summary["n_likelihood_calls"] - ref_summary["n_likelihood_calls"]}
    if same_shape:
        positions = [k for k in ref if k.startswith("position__")]
        row["positions_bitwise"] = all(np.array_equal(data[k], ref[k], equal_nan=True) for k in positions)
        row["positions_max_abs_diff"] = float(max(np.nanmax(np.abs(data[k] - ref[k])) for k in positions))
        differs = np.any([(data[k] != ref[k]).reshape(len(ref[k]), -1).any(axis=1) for k in positions], axis=0)
        row["first_dead_point_that_differs"] = int(np.argmax(differs)) if differs.any() else None
        dl = data["loglikelihood"] - ref["loglikelihood"]
        row["loglikelihood_bitwise"] = bool(np.array_equal(data["loglikelihood"], ref["loglikelihood"]))
        row["loglikelihood_max_abs_diff"] = float(np.abs(dl).max())
        row["loglikelihood_max_rel_diff"] = float(np.max(np.abs(dl) / np.abs(ref["loglikelihood"])))
        row["log_weights_max_abs_diff"] = float(np.nanmax(np.abs(data["log_weights"] - ref["log_weights"])))
    shifts = {name: (np.abs(mean - ref_moments[name][0]) / ref_moments[name][1], np.abs(std / ref_moments[name][1] - 1))
              for name, (mean, std) in moments(data).items()}
    row["posterior_max_mean_shift_sigma"] = float(max(np.max(s[0]) for s in shifts.values()))
    row["posterior_max_std_rel_change"] = float(max(np.max(s[1]) for s in shifts.values()))
    report["arms"][tag] = row
(OUT / "compare.json").write_text(json.dumps(report, indent=1))
print("COMPARE", json.dumps(report))
