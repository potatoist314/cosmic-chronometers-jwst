"""Stage profile and batch scaling of the production likelihood on dead points of a production fit.

Env: SPEEDUP_OUT, PROF_TAG, PROF_DEAD (ns_raw_dead pickle), PROF_BATCH (comma list),
PROF_REPEATS, PROF_TRACE (1: jax.profiler trace of the batch-100 likelihood).
"""
import json
import os
import pickle
import time
from pathlib import Path

import common
import jax
import jax.numpy as jnp
import numpy as np

OUT = Path(os.environ["SPEEDUP_OUT"]) / os.environ.get("PROF_TAG", "prof")
OUT.mkdir(parents=True, exist_ok=True)
REPEATS = int(os.environ.get("PROF_REPEATS", "30"))
ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, _, data = common.log_functions(model, likelihood)
components = dict(zip(likelihood.keys, likelihood.likelihoods))
spec_lh, phot_noise = components["spectrum"], components["photometry"].noise_model
lines = spec_lh.emission_lines
with open(os.environ["PROF_DEAD"], "rb") as fh:
    dead = pickle.load(fh)
stored = np.asarray(dead["loglikelihood"])


def points(batch):
    top = np.argsort(stored)[-batch:]
    return ({name: jnp.asarray(np.asarray(v)[top]).reshape((batch, *np.shape(model.theta_init[name])))
             for name, v in dead["positions"].items() if name in model.theta_init}, stored[top])


def timed(stages, name, fn, *args):
    compiled = jax.jit(jax.vmap(fn))
    start = time.perf_counter()
    out = jax.block_until_ready(compiled(*args))
    compile_s = time.perf_counter() - start
    samples = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        jax.block_until_ready(compiled(*args))
        samples.append(time.perf_counter() - start)
    batch = jax.tree_util.tree_leaves(args)[0].shape[0]
    stages[name] = {"median_us_per_call": 1e6 * float(np.median(samples)) / batch,
                    "min_us_per_call": 1e6 * float(np.min(samples)) / batch, "compile_s": compile_s}
    print(name, json.dumps(stages[name]), flush=True)
    return out


report = {"device": jax.devices()[0].device_kind, "jax": jax.__version__, "xla_flags": os.environ.get("XLA_FLAGS", ""),
          "n_line": int(lines.n_line), "batches": {}}
y, sig, mask = data["spectrum"]
y_p, sig_p, mask_p = data["photometry"]
for batch in [int(b) for b in os.environ.get("PROF_BATCH", "100,500").split(",")]:
    theta, logl = points(batch)
    stages = {}
    total = timed(stages, "total_loglike", loglike, theta)
    row = {"stages": stages, "max_abs_dlnl_vs_stored": float(np.max(np.abs(np.asarray(total) - logl)))}
    report["batches"][batch] = row
    if batch == 100 and os.environ.get("PROF_TRACE") == "1":
        compiled = jax.jit(jax.vmap(loglike))
        jax.block_until_ready(compiled(theta))
        jax.profiler.start_trace(str(OUT / "trace"), create_perfetto_trace=True)
        for _ in range(5):
            jax.block_until_ready(compiled(theta))
        jax.profiler.stop_trace()
    pred = timed(stages, "model_predict", model.predict, theta)
    timed(stages, "transforms", model.apply_transforms, theta)
    cols = timed(stages, "line_columns", lines.columns, theta)

    def spec_with_phot(mu, mu_p, t):
        return spec_lh.with_photometry(y, mu, sig, mask, t, (y_p, mu_p, sig_p, mask_p, phot_noise))

    timed(stages, "spectrum_with_photometry", spec_with_phot, pred["spectrum"], pred["photometry"], theta)

    def solve_only(mu, mu_p, c, t):
        noise = spec_lh.noise_model.compute(sig, mu, mask, t, data=y)
        noise_p = phot_noise.compute(sig_p, mu_p, mask_p, t, data=y_p)
        return spec_lh.calibration.calibrate_with_lines(
            y, mu, jnp.sqrt(1.0 / noise.inv_var), mask, c, lines.pairs, lines.ridge,
            (jnp.asarray(lines.band_matrix), y_p, mu_p, jnp.sqrt(1.0 / noise_p.inv_var), mask_p))[3]

    timed(stages, "calibrate_with_lines", solve_only, pred["spectrum"], pred["photometry"], cols, theta)
    (OUT / "profile.json").write_text(json.dumps(report, indent=1))
print("DONE", flush=True)
