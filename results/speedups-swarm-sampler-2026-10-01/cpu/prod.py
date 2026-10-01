"""The production M1_210210 zevo fit (e2e config of the integrator), built from the notebook cells."""
import json, os, sys, tempfile
from pathlib import Path
ROOT = Path("/Users/liuhao/Downloads/Astro project")
W = ROOT / "tmp/worktrees/swarm-sampler"
NOTEBOOK = Path(os.environ.get("SPEEDUP_NOTEBOOK", W / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"))
CONFIG = json.loads((W / "results/speedups-overnight-2026-09-30/e2e/experiment.json").read_text())
os.chdir(ROOT)
os.environ.setdefault("SPS_HOME", str(ROOT / "external/fsps"))
os.environ.update(MPLBACKEND="Agg", CERIDWEN_PLOTS="0", CERIDWEN_TARGET_ID="M1_210210")
os.environ.setdefault("CERIDWEN_RESULT_DIR", tempfile.mkdtemp())
sys.path.insert(0, str(ROOT / "scripts"))
DEAD = ROOT / "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/ns_raw_dead_728.pkl"

def build():
    cells = ["".join(c["source"]) for c in json.loads(NOTEBOOK.read_text())["cells"]]
    ns = {"display": lambda *a, **k: None}
    exec(cells[2], ns)
    arm = next(iter(CONFIG["arms"].values()))
    ns["SETTINGS"].update(CONFIG["settings"]); ns["SETTINGS"].update(arm["settings"])
    if os.environ.get("CERIDWEN_GRID_PATH"):
        ns["SETTINGS"]["ssp_grid"] = os.environ["CERIDWEN_GRID_PATH"]
    for name, expr in {**CONFIG["priors"], **arm.get("priors", {})}.items():
        exec(f"PRIORS[{name!r}] = {expr}", ns)
    for index in (4, 6, 8):
        exec(cells[index], ns)
    lk = cells[10].split("calibration_polynomial =")[1].split("model_parameter_block_text")[0]
    exec("calibration_polynomial =" + lk, ns)
    return ns

def log_functions(model, likelihood):
    import jax
    data = {k: (model.obs_dict[k].flux, model.obs_dict[k].uncertainty, model.obs_dict[k].mask) for k in likelihood.keys}
    @jax.jit
    def loglike_fn(theta):
        return likelihood.loglike(data, model.predict(theta), theta)
    @jax.jit
    def logprior_fn(theta):
        return model.ln_prior(theta)
    return loglike_fn, logprior_fn, data
