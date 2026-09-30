"""The production M1_210210 model and likelihood, built from the notebook cells.

Same cells as scripts/benchmark_baked_runtime.build; the log-likelihood is the one
of ceridwen.sampler.runner.run_sampler (MultiObservationLikelihood.loglike, which
shares the emission-line fluxes between the spectrum and the photometry).
Env: SPEEDUP_ROOT (project checkout with inputs), CERIDWEN_GRID_PATH (grid file, box only),
SPEEDUP_SETTINGS (JSON settings overrides), SPEEDUP_NOTEBOOK (notebook, default in SPEEDUP_ROOT).
"""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("SPEEDUP_ROOT", "/Users/liuhao/Downloads/Astro project"))
NOTEBOOK = Path(os.environ.get("SPEEDUP_NOTEBOOK", ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"))
os.chdir(ROOT)
os.environ.setdefault("SPS_HOME", str(ROOT / "external/fsps"))
os.environ.update(MPLBACKEND="Agg", CERIDWEN_PLOTS="0", CERIDWEN_TARGET_ID="M1_210210")
os.environ.setdefault("CERIDWEN_RESULT_DIR", tempfile.mkdtemp())
sys.path.insert(0, str(ROOT / "scripts"))


def build():
    cells = ["".join(cell["source"]) for cell in json.loads(NOTEBOOK.read_text())["cells"]]
    ns = {"display": lambda *a, **k: None}
    exec(cells[2], ns)
    if os.environ.get("CERIDWEN_GRID_PATH"):
        ns["SETTINGS"]["ssp_grid"] = os.environ["CERIDWEN_GRID_PATH"]
    ns["SETTINGS"].update(json.loads(os.environ.get("SPEEDUP_SETTINGS", "{}")))
    for index in (4, 6, 8):
        exec(cells[index], ns)
    likelihood = cells[10].split("calibration_polynomial =")[1].split("model_parameter_block_text")[0]
    exec("calibration_polynomial =" + likelihood, ns)
    return ns


def log_functions(model, likelihood):
    """loglike_fn and logprior_fn as run_sampler builds them."""
    import jax

    data = {k: (model.obs_dict[k].flux, model.obs_dict[k].uncertainty, model.obs_dict[k].mask)
            for k in likelihood.keys}

    @jax.jit
    def loglike_fn(theta):
        return likelihood.loglike(data, model.predict(theta), theta)

    @jax.jit
    def logprior_fn(theta):
        return model.ln_prior(theta)

    return loglike_fn, logprior_fn, data
