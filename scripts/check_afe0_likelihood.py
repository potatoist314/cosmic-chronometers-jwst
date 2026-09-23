#!/usr/bin/env python3
"""CPU check: one M1_210210 likelihood evaluates with afe fixed at 0.0.

Executes the fit notebook's own cells (imports/settings, data, observations,
model, likelihood setup) verbatim with ``SETTINGS["fix_afe"] = 0.0``, then
evaluates the joint photometry+spectrum log-likelihood once at the model's
initial theta, using the same call ``run_sampler`` makes internally
(``likelihood.loglike(static_data, model.predict(theta), theta)``).

CPU-only, no sampling, no GPU, no result files. Run from ``notebooks/``::

    cd notebooks && ../ceridwen/.venv/bin/python ../scripts/check_afe0_likelihood.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

NOTEBOOK = Path("ceridwen_integrated_photometry_spectra.ipynb")
# Cells reused verbatim from the notebook: 2 settings, 4 data, 6 observations,
# 8 model, 10 likelihood setup (cut before run_sampler).
CELLS = (2, 4, 6, 8)


def main() -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
    os.environ["CERIDWEN_RESULT_DIR"] = "/tmp/check_afe0_result"
    nb = json.loads(NOTEBOOK.read_text())
    ns: dict = {"__name__": "__check__"}
    for index in CELLS:
        src = "".join(nb["cells"][index]["source"])
        if index == 2:
            src += '\nSETTINGS["fix_afe"] = 0.0\n'
        exec(compile(src, f"<notebook-cell-{index}>", "exec"), ns)

    setup_src = "".join(nb["cells"][10]["source"]).split(
        "joint_result = run_sampler")[0]
    exec(compile(setup_src, "<notebook-cell-10-setup>", "exec"), ns)

    model, likelihood = ns["joint_model"], ns["joint_likelihood"]
    assert "afe" not in model.priors, "afe must be fixed, not sampled"
    full = model.apply_transforms(model.theta_init)
    assert float(full["afe"][0]) == 0.0, full["afe"]
    obs = model.obs_dict
    static = {k: (obs[k].flux, obs[k].uncertainty, obs[k].mask)
              for k in likelihood.keys}
    loglike = float(likelihood.loglike(static, model.predict(model.theta_init),
                                       model.theta_init))
    assert loglike == loglike and abs(loglike) != float("inf"), loglike
    print(f"[afe0-check] M1_210210 fix_afe=0.0 joint log-likelihood: {loglike:.6f}")
    print("[afe0-check] OK: afe fixed at 0.0, single likelihood finite")


if __name__ == "__main__":
    sys.exit(main())
