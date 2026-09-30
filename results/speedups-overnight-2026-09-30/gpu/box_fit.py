"""One seeded nested run of the production M1_210210 model, as BlackJAXNestedSamplerAdapter.run steps it.

Env: RUN_TAG, RUN_KERNEL (slice kernel; unset: the adapter default), RUN_ITERS (stop after
this many iterations; 0: run to logZ_tol), RUN_SEED, SPEEDUP_OUT, EXPECT_CERIDWEN
(substring of ceridwen.__file__), RUN_TRACE ("a:b": jax.profiler trace of iterations a..b-1),
RUN_SMOKE (the notebook's quick sampler settings, for a local check).
"""
import json
import os
import time
from pathlib import Path

import common  # noqa: F401  (sets the working directory and environment first)
import jax
import numpy as np
import ceridwen
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter

TAG = os.environ["RUN_TAG"]
OUT = Path(os.environ["SPEEDUP_OUT"]) / TAG
OUT.mkdir(parents=True, exist_ok=True)
if os.environ.get("EXPECT_CERIDWEN", "") not in ceridwen.__file__:
    raise SystemExit(f"ceridwen loaded from {ceridwen.__file__}")

script_start = time.perf_counter()
ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior, _ = common.log_functions(model, likelihood)
settings = ns["SETTINGS"]["sampler_quick" if os.environ.get("RUN_SMOKE") else "sampler"]
kernel = {"slice_kernel": os.environ["RUN_KERNEL"]} if os.environ.get("RUN_KERNEL") else {}
adapter = BlackJAXNestedSamplerAdapter(model.priors, **settings, verbose=False, **kernel)
inner, delete = settings["num_inner_steps"], settings["num_delete"]
limit = int(os.environ.get("RUN_ITERS", "0"))
trace = [int(v) for v in os.environ["RUN_TRACE"].split(":")] if os.environ.get("RUN_TRACE") else None


def log_z(state):
    for owner in (state, getattr(state, "integrator", None), getattr(state, "sampler_state", None)):
        if owner is not None and hasattr(owner, "logZ") and hasattr(owner, "logZ_live"):
            return float(owner.logZ), float(owner.logZ_live)
    raise AttributeError(type(state).__name__)


built_s = time.perf_counter() - script_start
rng_key = jax.random.PRNGKey(int(os.environ.get("RUN_SEED", "20260930")))
rng_key, prior_key = jax.random.split(rng_key)
particles = adapter._sample_prior(model.theta_init, prior_key)
sampler = adapter._build_nested_sampler(loglike, logprior, inner, delete)
init_fn, step_fn = jax.jit(sampler.init), jax.jit(sampler.step)
t0 = time.perf_counter()
live = init_fn(particles)
logz, logz_live = log_z(live)
init_s = time.perf_counter() - t0
rows, dead_logl, dead_birth, dead_pos = [], [], [], []
calls = settings["num_live"]
t_start = time.perf_counter()
iteration = 0
while logz_live - logz >= settings["logZ_tol"] and (limit == 0 or iteration < limit):
    if trace and iteration == trace[0]:
        jax.profiler.start_trace(str(OUT / "trace"), create_perfetto_trace=True)
    rng_key, subkey = jax.random.split(rng_key)
    t = time.perf_counter()
    live, dead = step_fn(subkey, live)
    iteration += 1
    logz, logz_live = log_z(live)
    dt = time.perf_counter() - t
    if trace and iteration == trace[1]:
        jax.profiler.stop_trace()
    calls += int(adapter._logical_likelihood_calls(dead))
    dead_logl.append(np.asarray(dead.particles.loglikelihood))
    dead_birth.append(np.asarray(dead.particles.loglikelihood_birth))
    dead_pos.append({k: np.asarray(v) for k, v in dead.particles.position.items()})
    rows.append({"iteration": iteration, "iteration_s": dt, "logZ": logz, "logZ_live": logz_live, "calls": calls})
sampling_s = time.perf_counter() - t_start
np.savez(OUT / "dead.npz", loglikelihood=np.concatenate(dead_logl), loglikelihood_birth=np.concatenate(dead_birth),
         **{f"position__{k}": np.concatenate([p[k] for p in dead_pos]) for k in dead_pos[0]})
summary = {
    "tag": TAG, "kernel": getattr(adapter, "slice_kernel", "n/a"), "ceridwen": ceridwen.__file__,
    "device": jax.devices()[0].device_kind, "jax": jax.__version__, "x64": bool(jax.config.jax_enable_x64),
    "xla_flags": os.environ.get("XLA_FLAGS", ""), "iterations": iteration, "converged": limit == 0,
    "logZ": logz, "logZ_live": logz_live, "n_likelihood_calls": calls,
    "build_s": built_s, "init_s": init_s, "sampling_s": sampling_s,
    "first_iteration_s": rows[0]["iteration_s"], "later_iterations_s": sum(r["iteration_s"] for r in rows[1:]),
    "script_s": time.perf_counter() - script_start, "rows": rows,
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=1))
print("DONE", json.dumps({k: v for k, v in summary.items() if k != "rows"}), flush=True)
