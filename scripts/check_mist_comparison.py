#!/usr/bin/env python3
"""CPU check: one M1_210210 likelihood evaluates for each comparison option.

Executes the fit notebook's own cells (imports/settings, data, observations,
model, likelihood setup) verbatim for each option, then evaluates the joint
photometry+spectrum log-likelihood once at the model's initial theta, using
the same call ``run_sampler`` makes internally
(``likelihood.loglike(static_data, model.predict(theta), theta)``).

Options: default grid with afe sampled, default grid with ``fix_afe=0.0``,
and the local old-MIST control grid (single afe plane, fixed by the grid).

CPU-only, no sampling, no GPU, no result files. Run from ``notebooks/``::

    cd notebooks && ../ceridwen/.venv/bin/python ../scripts/check_mist_comparison.py
"""

from __future__ import annotations

import gc
import json
import os
import sys
from pathlib import Path

NOTEBOOK = Path("ceridwen_integrated_photometry_spectra.ipynb")
# Cells reused verbatim from the notebook: 2 settings, 4 data, 6 observations,
# 8 model, 10 likelihood setup (cut before run_sampler).
CELLS = (2, 4, 6, 8)

OPTIONS = (
    # (label, SETTINGS["ssp_grid"], SETTINGS["fix_afe"], expect_afe_sampled)
    ("default", "amist_c3k_hr_krou_afe", None, True),
    ("afe-fixed-0", "amist_c3k_hr_krou_afe", 0.0, False),
    ("old-mist-miles", str(Path.home() / ".ceridwen/grids/mist_miles_krou_afe1.h5"),
     None, False),
)


def run_option(label: str, ssp_grid: str, fix_afe, sampled: bool) -> float:
    nb = json.loads(NOTEBOOK.read_text())
    ns: dict = {"__name__": "__check__"}
    for index in CELLS:
        src = "".join(nb["cells"][index]["source"])
        if index == 2:
            src += f'\nSETTINGS["ssp_grid"] = {ssp_grid!r}\n'
            src += f'SETTINGS["fix_afe"] = {fix_afe!r}\n'
        exec(compile(src, f"<notebook-cell-{index}>", "exec"), ns)

    setup_src = "".join(nb["cells"][10]["source"]).split(
        "joint_result = run_sampler")[0]
    exec(compile(setup_src, "<notebook-cell-10-setup>", "exec"), ns)

    model, likelihood = ns["joint_model"], ns["joint_likelihood"]
    assert ("afe" in model.priors) == sampled, (label, sorted(model.priors))
    full = model.apply_transforms(model.theta_init)
    if not sampled:
        assert float(full["afe"][0]) == 0.0, (label, full["afe"])
    obs = model.obs_dict
    static = {k: (obs[k].flux, obs[k].uncertainty, obs[k].mask)
              for k in likelihood.keys}
    loglike = float(likelihood.loglike(static, model.predict(model.theta_init),
                                       model.theta_init))
    assert loglike == loglike and abs(loglike) != float("inf"), (label, loglike)
    print(f"[mist-check] M1_210210 {label}: joint log-likelihood {loglike:.6f} "
          f"(afe {'sampled' if sampled else 'fixed at 0.0'})", flush=True)
    return loglike


def main() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
    os.environ["CERIDWEN_RESULT_DIR"] = "/tmp/check_mist_comparison"
    for label, grid, afe, sampled in OPTIONS:
        run_option(label, grid, afe, sampled)
        gc.collect()
    print("[mist-check] OK: one finite likelihood for each option")


if __name__ == "__main__":
    sys.exit(main())
