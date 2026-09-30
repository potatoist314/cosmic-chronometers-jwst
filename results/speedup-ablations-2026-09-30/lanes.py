"""Sampler lane waste on CPU for the run3 configuration (research only, scratch).

Reuses scripts/benchmark_baked_runtime.build, scripts/benchmark_ceridwen_vast._make_log_functions
and the kernel construction pattern of scripts/validate_ceridwen_speedups.build_algorithm.
Changes no project file.
"""
import json
import os
import pickle
import sys
import tempfile
import time
from functools import partial
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

import h5py  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import random  # noqa: E402
import blackjax  # noqa: E402
from blackjax.mcmc.slice import build_kernel as slice_kernel  # noqa: E402
from blackjax.ns import adaptive, base, from_mcmc, nss  # noqa: E402
import benchmark_baked_runtime  # noqa: E402
if "SPEEDUP_NOTEBOOK" in os.environ:  # local: notebook at run3 pin d522c76; remote: committed HEAD
    benchmark_baked_runtime.NOTEBOOK = Path(os.environ["SPEEDUP_NOTEBOOK"])
from benchmark_ceridwen_vast import _make_log_functions  # noqa: E402

INNER = int(os.environ.get("LANES_INNER", "65"))
DELETE = int(os.environ.get("LANES_DELETE", "100"))
ITERS = [int(x) for x in os.environ.get("LANES_ITERS", "20,100,180,250").split(",")]
REPEATS = int(os.environ.get("LANES_REPEATS", "2"))
OUT = SCRATCH / os.environ.get("LANES_OUT", "lanes.json")

ns = benchmark_baked_runtime.build(True, True)
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
csp = model.csp
loglike, logprior = _make_log_functions(model, likelihood)
report = {"inner_steps": INNER, "num_delete": DELETE, "device": str(jax.devices()[0]),
          "device_kind": jax.devices()[0].device_kind, "iterations": {}}


def save():
    OUT.write_text(json.dumps(report, indent=1))


# A. Inputs against the arrays that run3 stored.
report["inputs"] = {}
with h5py.File(RUN3 / "ceridwen_result.h5") as h:
    for name in ("photometry", "spectrum"):
        obs = model.obs_dict[name]
        for field in ("flux", "uncertainty", "mask", "wavelength"):
            stored = np.asarray(h[f"obs/{name}/{field}"][()])
            mine = np.asarray(getattr(obs, field))
            same_shape = stored.shape == mine.shape
            row = {"same_shape": same_shape, "equal": bool(same_shape and np.array_equal(stored, mine))}
            if same_shape and stored.dtype != bool:
                ok = np.isfinite(stored) & np.isfinite(mine) & (stored != 0)
                row["max_rel_diff"] = float(np.max(np.abs(mine[ok] / stored[ok] - 1.0))) if ok.any() else None
            report["inputs"][f"{name}.{field}"] = row
    stored_wave = np.asarray(h["model/wave"][()])
    report["inputs"]["model.wave_equal"] = bool(np.array_equal(stored_wave, np.asarray(csp.wave)))
print("INPUTS", json.dumps(report["inputs"]), flush=True)

with open(RUN3 / "ns_raw_dead_943.pkl", "rb") as fh:
    dead = pickle.load(fh)
logl = np.asarray(dead["loglikelihood"])
birth = np.asarray(dead["loglikelihood_birth"])
positions = {k: np.asarray(v) for k, v in dead["positions"].items()}
n_iter = (len(logl) - 500) // DELETE
report["run3_iterations"] = int(n_iter)


def live_set(k):
    """Live points of run3 before iteration k (0-based)."""
    alive = np.arange(len(logl)) >= DELETE * k
    if k > 0:
        threshold = logl[DELETE * (k - 1):DELETE * k].max()
        alive &= ~(birth > threshold)  # NaN birth (initial points) stays
    return np.flatnonzero(alive)


def stepping_out_carry(rng_key, in_slice, width, max_expansions):
    """Neal (2003) Fig. 3 with the slice test in the loop body, its result carried.

    Same sequence of evaluations as blackjax.mcmc.slice.stepping_out.
    """
    u_key, jk_key = random.split(rng_key)
    u = random.uniform(u_key)
    left = -width * u
    right = left + width
    v = random.uniform(jk_key)
    j = jnp.floor(max_expansions * v).astype(int)
    k = (max_expansions - 1) - j

    def cond(carry):
        _, n, inside = carry
        return inside & (n > 0)

    def left_body(carry):
        edge, n, _ = carry
        edge = edge - width
        return edge, n - 1, in_slice(edge)

    def right_body(carry):
        edge, n, _ = carry
        edge = edge + width
        return edge, n - 1, in_slice(edge)

    left, jl, _ = jax.lax.while_loop(cond, left_body, (left, j, in_slice(left)))
    right, kr, _ = jax.lax.while_loop(cond, right_body, (right, k, in_slice(right)))
    return left, right, (j - jl) + (k - kr), lambda t: jnp.asarray(True)


def carry_algorithm():
    init_state = partial(base.init_state_strategy, logprior_fn=logprior, loglikelihood_fn=loglike)
    constrained = nss.slice_constrained_step(
        init_state,
        slice_kernel(interval=stepping_out_carry, max_expansions=10, max_shrinkage=100),
        nss.covariance_proposal,
    )
    kernel = from_mcmc.build_kernel(constrained, INNER, nss.live_covariance, DELETE)
    initializer = partial(adaptive.init, init_state_fn=jax.vmap(init_state),
                          update_inner_kernel_params_fn=nss.live_covariance)
    return blackjax.SamplingAlgorithm(initializer, kernel)


stock = blackjax.nss(logprior_fn=logprior, loglikelihood_fn=loglike,
                     num_inner_steps=INNER, num_delete=DELETE)
carry = carry_algorithm()
init_fn = jax.jit(stock.init)
steps = {"stock": jax.jit(stock.step), "carry": jax.jit(carry.step)}
batch_like = jax.jit(jax.vmap(loglike))


def lane_counts(update_info):
    nexp = np.asarray(update_info.num_expansions)      # (lanes, inner steps)
    nshrink = np.asarray(update_info.num_shrink)
    n_left = np.floor(-np.asarray(update_info.bracket_left)).astype(int)   # width = 1
    n_right = np.floor(np.asarray(update_info.bracket_right)).astype(int)
    lanes = nexp.shape[0]
    logical = int((nexp + nshrink + 2).sum())
    out = {
        "logical_calls": logical,
        "logical_per_slice_step": logical / nexp.size,
        "left_right_split_matches": float(np.mean(n_left + n_right == nexp)),
        "mean_expansions": float(nexp.mean()),
        "mean_shrink": float(nshrink.mean()),
        "max_shrink": int(nshrink.max()),
    }
    for width in (lanes, lanes // 2, lanes // 4, lanes // 10):
        groups = [slice(a, a + width) for a in range(0, lanes, width)]
        executed_stock = executed_carry = executed_machine = 0
        for g in groups:
            ml, mr, ms = n_left[g].max(axis=0), n_right[g].max(axis=0), nshrink[g].max(axis=0)
            executed_stock += int((2 * (ml + mr) + 2 + ms).sum()) * width
            executed_carry += int((ml + mr + 2 + ms).sum()) * width
            executed_machine += int((nexp[g] + nshrink[g] + 2).sum(axis=1).max()) * width
        out[f"lanes_{width}"] = {
            "executed_stock": executed_stock,
            "executed_carry": executed_carry,
            "executed_state_machine": executed_machine,
            "waste_stock": executed_stock / logical,
            "waste_carry": executed_carry / logical,
            "waste_state_machine": executed_machine / logical,
        }
    return out


def batch_time(theta):
    jax.block_until_ready(batch_like(theta))
    samples = []
    for _ in range(7):
        start = time.perf_counter()
        jax.block_until_ready(batch_like(theta))
        samples.append(time.perf_counter() - start)
    return float(np.min(samples)), float(np.median(samples))


key = random.key(20260929)
compiled = set()
for k in ITERS:
    if k >= n_iter:
        continue
    idx = live_set(k)
    row = {"n_live_rebuilt": int(idx.size), "threshold_run3": float(logl[DELETE * k:DELETE * (k + 1)].max())}
    print("ITER", k, json.dumps(row), flush=True)
    live = {name: jnp.asarray(values[idx]) for name, values in positions.items()}
    state = init_fn(live)
    theta100 = {name: value[:DELETE] for name, value in live.items()}
    row["batch_eval_s_min"], row["batch_eval_s_median"] = batch_time(theta100)
    key, step_key = random.split(key)
    results = {}
    for name, step in steps.items():
        if name not in compiled:
            start = time.perf_counter()
            jax.block_until_ready(step(step_key, state))
            row[f"{name}_first_call_s"] = time.perf_counter() - start
            compiled.add(name)
    for repeat in range(REPEATS):
        for name, step in steps.items():  # interleaved, so machine load affects both
            start = time.perf_counter()
            out = step(step_key, state)
            jax.block_until_ready(out)
            row.setdefault(f"{name}_step_s", []).append(time.perf_counter() - start)
            results[name] = out
            print("STEP", k, name, repeat, row[f"{name}_step_s"][-1], flush=True)
    (s_state, s_info), (c_state, c_info) = results["stock"], results["carry"]
    row["carry_equals_stock"] = {
        "loglikelihood_bitwise": bool(np.array_equal(np.asarray(s_state.particles.loglikelihood),
                                                     np.asarray(c_state.particles.loglikelihood))),
        "max_abs_dloglikelihood": float(np.max(np.abs(np.asarray(s_state.particles.loglikelihood)
                                                      - np.asarray(c_state.particles.loglikelihood)))),
        "num_expansions_equal": bool(np.array_equal(np.asarray(s_info.update_info.num_expansions),
                                                    np.asarray(c_info.update_info.num_expansions))),
        "num_shrink_equal": bool(np.array_equal(np.asarray(s_info.update_info.num_shrink),
                                                np.asarray(c_info.update_info.num_shrink))),
    }
    row["counts"] = lane_counts(s_info.update_info)
    row["stock_over_carry_time_min"] = min(row["stock_step_s"]) / min(row["carry_step_s"])
    full = row["counts"][f"lanes_{DELETE}"]
    row["predicted_stock_s"] = full["executed_stock"] / DELETE * row["batch_eval_s_min"]
    row["predicted_carry_s"] = full["executed_carry"] / DELETE * row["batch_eval_s_min"]
    report["iterations"][str(k)] = row
    print("RESULT", k, json.dumps(row), flush=True)
    save()

