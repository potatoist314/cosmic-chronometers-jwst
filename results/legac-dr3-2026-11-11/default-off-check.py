"""Default data_source: notebook cells 0-8 at HEAD and in the working tree give bitwise-equal arrays.

Run from the repository root with ceridwen/.venv/bin/python and PYTHONPATH=external/sedpy_jax.
Optional argument: a target; the default is M1_210210. Prints one line per compared array.
"""
import json
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
from astropy.units import UnitsWarning

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
TARGET = sys.argv[1] if len(sys.argv) > 1 else "M1_210210"


def build(document, directory, settings=None):
    os.chdir(ROOT)
    os.environ.update(CERIDWEN_RESULT_DIR=str(directory), CERIDWEN_TARGET_ID=TARGET, CERIDWEN_PLOTS="0")
    namespace = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        for index, cell in enumerate(document["cells"][:9]):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            if "SETTINGS = {" in source and settings:
                source += "".join(f"\nSETTINGS[{k!r}] = {v!r}" for k, v in settings.items()) + "\n"
            exec(compile(source, f"cell-{index}", "exec"), namespace)
    return namespace


def arrays(ns):
    model = ns["joint_model"]
    out = {name: np.asarray(ns[name]) for name in
           ("spectrum_wave", "spectrum_flux", "spectrum_uncertainty", "native_valid", "phot_flux", "phot_uncertainty")}
    out["spectrum_mask"] = np.asarray(ns["spectrum_mask"])
    for i, (afe, feh, scale) in enumerate([(-.1, -.8, -1.), (.1, -.3, 0.), (.3, .1, 1.)]):
        theta = dict(model.theta_init)
        theta.update(afe=np.array([afe]), logzsol=np.array([feh]),
                     logsfr_ratios=scale * np.linspace(-.2, .2, ns["N_RATIOS"]))
        for mode, predict in (("eager", model.predict), ("jit", model.predict_jit)):
            prediction = predict(theta)
            for key in ("photometry", "spectrum"):
                out[f"{mode}_{key}_{i}"] = np.asarray(prediction[key])
    return out


if __name__ == "__main__":
    head = json.loads(subprocess.check_output(["git", "show", f"HEAD:{NOTEBOOK}"], cwd=ROOT, text=True))
    work = json.loads((ROOT / NOTEBOOK).read_text())
    scratch = Path(os.environ.get("TMPDIR", "/tmp"))
    a = arrays(build(head, scratch / "default-off-head"))
    b = arrays(build(work, scratch / "default-off-work"))
    assert a.keys() == b.keys()
    equal = True
    for key in a:
        same = a[key].shape == b[key].shape and np.array_equal(a[key], b[key])
        equal &= same
        print(f"{key}: shape {a[key].shape}, bitwise equal {same}")
    print(f"{TARGET}: all {len(a)} arrays bitwise equal: {equal}")
    sys.exit(0 if equal else 1)
