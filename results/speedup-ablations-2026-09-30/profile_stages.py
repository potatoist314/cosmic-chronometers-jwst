"""CPU stage profile of the run3 production likelihood (research only, scratch).

Reuses scripts/benchmark_baked_runtime.build and
scripts/benchmark_ceridwen_vast._make_log_functions. Changes no project file.
"""
import json
import os
import pickle
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(os.environ.get("SPEEDUP_ROOT", "/Users/liuhao/Downloads/Astro project"))
SCRATCH = Path(os.environ.get("SPEEDUP_OUT", Path(__file__).resolve().parent))
SCRATCH.mkdir(parents=True, exist_ok=True)
RUN3 = Path(os.environ.get("SPEEDUP_RUN3", ROOT / "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210"))
os.chdir(ROOT)
os.environ["MPLBACKEND"] = "Agg"
os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp(dir=SCRATCH)
sys.path.insert(0, str(ROOT / "scripts"))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import benchmark_baked_runtime  # noqa: E402
if "SPEEDUP_NOTEBOOK" in os.environ:  # local: notebook at run3 pin d522c76; remote: committed HEAD
    benchmark_baked_runtime.NOTEBOOK = Path(os.environ["SPEEDUP_NOTEBOOK"])
build = benchmark_baked_runtime.build
from benchmark_ceridwen_vast import _make_log_functions  # noqa: E402

BATCHES = [int(b) for b in os.environ.get("PROFILE_BATCH", "100").split(",")]
REPEATS = int(os.environ.get("PROFILE_REPEATS", "15"))

ns = build(True, True)
model = ns["joint_model"]
likelihood = ns["joint_likelihood"]
csp = model.csp
phot_obs = model.obs_dict["photometry"]
spec_obs = model.obs_dict["spectrum"]
loglike, logprior = _make_log_functions(model, likelihood)

def profile(BATCH):
    with open(RUN3 / "ns_raw_dead_943.pkl", "rb") as fh:
        dead = pickle.load(fh)
    logl = np.asarray(dead["loglikelihood"])
    order = np.argsort(logl)
    top = order[-BATCH:]  # highest-likelihood points of run3
    theta = {
        name: jnp.asarray(np.asarray(values)[top]).reshape((BATCH, *model.theta_init[name].shape))
        for name, values in dead["positions"].items()
    }
    report = {
        "batch": BATCH,
        "repeats": REPEATS,
        "device": str(jax.devices()[0]),
        "device_kind": jax.devices()[0].device_kind,
        "n_free": int(sum(np.size(v) for v in model.theta_init.values())),
        "free_names": {k: list(np.shape(v)) for k, v in model.theta_init.items()},
        "n_wave_model": int(csp.wave.shape[0]),
        "sfh_basis_shape": list(csp._sfh_basis.shape),
        "sfh_basis_dtype": str(csp._sfh_basis.dtype),
        "fastpath": bool(csp.sfh_basis_fastpath),
        "n_pix_spectrum": int(np.asarray(spec_obs.wavelength).shape[0]),
        "n_pix_fitted": int(np.asarray(spec_obs.mask).sum()),
        "n_filters": int(len(phot_obs.filterset.filters)),
    }


    def timed(name, fn, *args):
        compiled = jax.jit(jax.vmap(fn))
        out = compiled(*args)
        jax.block_until_ready(out)
        samples = []
        for _ in range(REPEATS):
            start = time.perf_counter()
            jax.block_until_ready(compiled(*args))
            samples.append(time.perf_counter() - start)
        row = {
            "median_us_per_call": 1e6 * float(np.median(samples)) / BATCH,
            "min_us_per_call": 1e6 * float(np.min(samples)) / BATCH,
        }
        report.setdefault("stages", {})[name] = row
        print(name, json.dumps(row), flush=True)
        return out


    # Full likelihood and its check against run3's stored values.
    total = timed("total_loglike", loglike, theta)
    report["max_abs_dlnl_vs_run3"] = float(np.max(np.abs(np.asarray(total) - logl[top])))
    timed("logprior", logprior, theta)

    # Stage 1: transforms.
    mtheta = timed("transforms", model.apply_transforms, theta)
    mtheta = dict(mtheta)

    # Stage 2: dust curves on the model grid.
    attn, attn_diffuse = timed("dust_curves", lambda t: csp.attenuate_dust(csp.wave, t), mtheta)

    # Stage 3: basis gather, alpha/Z interpolation and SFH contraction.
    groups = timed("basis_contraction", csp._spectrum_from_sfh_basis, mtheta)
    report["n_dust_groups"] = int(groups.shape[1])


    # Stage 4: apply the dust to the groups.
    def apply_dust(groups_, attn_, attn_diffuse_, t):
        out = groups_ * csp._dust_group_attenuation(attn_, t) if csp._has_age_dependent_dust else groups_
        return out.sum(axis=0) * jnp.exp(-attn_diffuse_.astype(jnp.float32))


    spectrum = timed("dust_apply", apply_dust, groups, attn, attn_diffuse, mtheta)


    # Stage 5: mass and flux factor (128-node distance quadrature per call).
    def scale(spec, t):
        return csp._apply_mass_redshift_igm(spec, spec, jnp.zeros_like(spec), t)[0]


    scaled = timed("mass_fluxfactor", scale, spectrum, mtheta)

    # Stage 6: photometry at the sampled redshift.
    zred = mtheta["zred"][:, 0]
    sigma = mtheta["sigma_smooth"][:, 0]
    report["photometry_free_z_flag"] = bool(getattr(phot_obs, "free_z", False))
    phot = timed("photometry_fixed_z_matrix", lambda s: phot_obs.predict(s, csp.wave), scaled)

    # Stage 7: spectrum smoothing and resampling.
    apply_instr, apply_losvd = spec_obs._predict_fn.__defaults__
    trim_idx = [c.cell_contents for c in spec_obs._predict_fn.__closure__ if hasattr(c.cell_contents, "shape")][0]
    report["n_wave_trim"] = int(trim_idx.shape[0])
    trimmed = scaled[:, trim_idx]
    losvd_out = timed("losvd_fft", lambda s, sv: apply_losvd(s, sv), trimmed, sigma)
    instr_out = timed("instrument_lsf_fft", apply_instr, losvd_out)
    report["smoothing_dtype"] = str(instr_out.dtype)
    wo = jnp.asarray(spec_obs._wavelength)


    def stretch(mu, z):
        return spec_obs._stretch_interp(wo * (1.0 + spec_obs._zred_setup) / (1.0 + z), mu)


    spec_pred = timed("redshift_stretch", stretch, instr_out, zred)
    timed("spectrum_predict_whole", lambda s, sv, z: spec_obs.predict(s, csp.wave, sigma_smooth=sv, zred=z), scaled, sigma, zred)

    # Stage 8: likelihoods.
    data = {k: (model.obs_dict[k].flux, model.obs_dict[k].uncertainty, model.obs_dict[k].mask) for k in likelihood.keys}
    components = dict(zip(likelihood.keys, likelihood.likelihoods))
    timed("photometry_likelihood", lambda mu, t: components["photometry"](*data["photometry"][:1], mu, *data["photometry"][1:], params=t)[0], phot, theta)
    timed("spectrum_likelihood_calibration", lambda mu, t: components["spectrum"](*data["spectrum"][:1], mu, *data["spectrum"][1:], params=t)[0], spec_pred, theta)
    timed("model_predict_whole", model.predict, theta)

    stages = report["stages"]
    parts = ["transforms", "dust_curves", "basis_contraction", "dust_apply", "mass_fluxfactor",
             "photometry_fixed_z_matrix", "losvd_fft", "instrument_lsf_fft", "redshift_stretch",
             "photometry_likelihood", "spectrum_likelihood_calibration"]
    report["sum_of_parts_median_us"] = sum(stages[p]["median_us_per_call"] for p in parts)
    report["share_of_sum_percent"] = {
        p: 100 * stages[p]["median_us_per_call"] / report["sum_of_parts_median_us"] for p in parts
    }
    out_path = SCRATCH / f"stage_profile_b{BATCH}.json"
    out_path.write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


for BATCH in BATCHES:
    profile(BATCH)
