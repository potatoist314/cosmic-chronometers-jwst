"""Lane kernel against the carry kernel on every state of one seeded carry run of M1_210210.

The carry kernel drives the run. At each iteration the lane kernel takes the same
state and key, and the two results are compared bit for bit. Where they differ,
the start particles are tested: BlackJAX draws them with a float32 cumulative
sum, and the carry chains are rerun from the neighbouring survivors.

Reuses scripts/benchmark_baked_runtime.build and
scripts/benchmark_ceridwen_vast._make_log_functions, as free_arm.py does.
"""
import json
import os
import pickle
import sys
import tempfile
import time
from functools import partial
from pathlib import Path

ROOT = Path(os.environ["SPEEDUP_ROOT"])
OUT = Path(os.environ["SPEEDUP_OUT"])
OUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
os.environ["MPLBACKEND"] = "Agg"
os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp(dir=OUT)
sys.path.insert(0, str(ROOT / "scripts"))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from blackjax.mcmc.slice import build_kernel as build_slice_kernel  # noqa: E402
from blackjax.ns import base, nss  # noqa: E402
import benchmark_baked_runtime  # noqa: E402
from benchmark_ceridwen_vast import _make_log_functions  # noqa: E402
import ceridwen  # noqa: E402
from ceridwen.model.model import SedModel  # noqa: E402
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter, stepping_out_carry  # noqa: E402

if os.environ["EXPECT_CERIDWEN"] not in ceridwen.__file__:
    raise SystemExit(f"ceridwen loaded from {ceridwen.__file__}")
SedModel._prior_upper_bound = lambda self, name: None  # 2n pad, as in the carry and lanes arms

script_start = time.perf_counter()
ns = benchmark_baked_runtime.build(True, True)
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior = _make_log_functions(model, likelihood)
sampler = (dict(num_live=16, num_inner_steps=2, num_delete=8, logZ_tol=1e4) if os.environ.get("RUN_SMOKE")
           else dict(num_live=500, num_inner_steps=65, num_delete=100, logZ_tol=-5.0))
INNER, DELETE = sampler["num_inner_steps"], sampler["num_delete"]
FORCE = int(os.environ.get("CHECK_FORCE", "-1"))  # diagnose this iteration even when the kernels agree
reference = np.load(os.environ["CHECK_REFERENCE"]) if os.environ.get("CHECK_REFERENCE") else None


def build(kernel):
    return BlackJAXNestedSamplerAdapter(model.priors, **sampler, verbose=False, slice_kernel=kernel)


lanes_step = jax.jit(build("lanes")._build_nested_sampler(loglike, logprior, INNER, DELETE).step)
delete = jax.jit(partial(base.delete_fn, num_delete=DELETE))
init_state_fn = partial(base.init_state_strategy, logprior_fn=logprior, loglikelihood_fn=loglike)
carry_move = nss.slice_constrained_step(
    init_state_fn, build_slice_kernel(interval=stepping_out_carry, max_expansions=10, max_shrinkage=100),
    nss.covariance_proposal)


@jax.jit
def start_draw(inner_key, loglikelihood, loglikelihood_0):
    """The start particles of blackjax.ns.from_mcmc.update_with_mcmc_take_last, with their inputs."""
    choice_key, _ = jax.random.split(inner_key)
    weights = (loglikelihood > loglikelihood_0).astype(jnp.float32)
    weights = jnp.where(weights.sum() > 0.0, weights, jnp.ones_like(weights))
    p = weights / weights.sum()
    index = jax.random.choice(choice_key, len(weights), shape=(DELETE,), p=p, replace=True)
    return index, jnp.cumsum(p), jax.random.uniform(choice_key, (DELETE,), dtype=p.dtype), weights


@jax.jit
def carry_chains(inner_key, state, loglikelihood_0, cov, start_index):
    """update_with_mcmc_take_last with the carry slice step and given start particles."""
    _, sample_key = jax.random.split(inner_key)
    start_state = jax.tree.map(lambda x: x[start_index], state.particles)

    def chain(key, particle):
        return jax.lax.scan(lambda s, k: carry_move(k, s, loglikelihood_0, cov=cov), particle,
                            jax.random.split(key, INNER))

    return jax.vmap(chain)(jax.random.split(sample_key, DELETE), start_state)


def flat(position, index=None):
    parts = [np.asarray(v).reshape(np.asarray(v).shape[0], -1) for _, v in sorted(position.items())]
    parts = np.concatenate(parts, axis=1)
    return parts if index is None else parts[index]


def diagnose(k, subkey, incoming, carry, lanes):
    dead_index, target_index = (np.asarray(x) for x in delete(incoming))
    loglikelihood_0 = incoming.particles.loglikelihood[dead_index].max()
    _, inner_key = jax.random.split(subkey)
    start, p_cuml, u, weights = (np.asarray(x) for x in start_draw(
        inner_key, incoming.particles.loglikelihood, loglikelihood_0))
    new_carry = flat(carry[0].particles.position, target_index)
    new_lanes = flat(lanes[0].particles.position, target_index)
    differ = np.flatnonzero((new_carry != new_lanes).any(axis=1)).tolist()
    survivors = np.flatnonzero(weights > 0)
    out = {"lanes_that_differ": differ, "survivors": int(survivors.size), "lane_tests": []}
    for lane in (differ or [0]):
        rank = int(np.searchsorted(survivors, start[lane]))
        r = np.float32(p_cuml[-1] * (np.float32(1) - u[lane]))
        test = {"lane": lane, "u": float(u[lane]), "r": float(r), "ulp_r": float(np.spacing(r)),
                "start_in_side_program": int(start[lane]), "survivor_rank": rank, "candidates": []}
        for offset in (-1, 0, 1):
            if not 0 <= rank + offset < survivors.size:
                continue
            candidate = int(survivors[rank + offset])
            index = start.copy()
            index[lane] = candidate
            particles, _ = carry_chains(inner_key, incoming, loglikelihood_0,
                                        incoming.inner_kernel_params["cov"], jnp.asarray(index))
            new = flat(particles.position)
            others = np.arange(DELETE) != lane
            test["candidates"].append({
                "start": candidate, "survivor_rank": rank + offset,
                "p_cuml_minus_r_ulp": float((np.float64(p_cuml[candidate]) - np.float64(r)) / np.spacing(r)),
                "max_abs_diff_from_carry": float(np.abs(new[lane] - new_carry[lane]).max()),
                "max_abs_diff_from_lanes": float(np.abs(new[lane] - new_lanes[lane]).max()),
                "other_lanes_equal_to_carry": int((new[others] == new_carry[others]).all(axis=1).sum()),
                "other_lanes_max_abs_diff_from_carry": float(np.abs(new[others] - new_carry[others]).max())})
        out["lane_tests"].append(test)
    np.savez(OUT / f"iteration_{k}.npz", weights=weights, p_cuml=p_cuml, u=u, start=start,
             dead_index=dead_index, target_index=target_index, new_carry=new_carry, new_lanes=new_lanes,
             loglikelihood=np.asarray(incoming.particles.loglikelihood),
             loglikelihood_0=np.asarray(loglikelihood_0), subkey=np.asarray(subkey))
    with open(OUT / f"iteration_{k}_state.pkl", "wb") as fh:
        pickle.dump(jax.tree.map(np.asarray, incoming), fh)
    return out


rows = []


def callback(it, subkey, incoming, live, dead_info, step_fn, dt):
    k = it - 1
    lanes = lanes_step(subkey, incoming)
    ours, theirs = jax.tree.leaves((live, dead_info)), jax.tree.leaves(lanes)
    equal = len(ours) == len(theirs) and all(
        np.array_equal(np.asarray(a), np.asarray(b), equal_nan=True) for a, b in zip(ours, theirs))
    row = {"iteration": k, "bitwise_equal": bool(equal), "carry_step_s": float(dt)}
    if reference is not None and DELETE * (k + 1) <= len(reference["loglikelihood"]):
        rows_ref = slice(DELETE * k, DELETE * (k + 1))
        mine = flat(dead_info.particles.position)
        theirs_ref = np.concatenate([reference[f"position__{name}"][rows_ref].reshape(DELETE, -1)
                                     for name in sorted(dead_info.particles.position)], axis=1)
        row["dead_max_abs_diff_from_first_run"] = float(np.abs(mine - theirs_ref).max())
    if not equal or k == FORCE:
        row["diagnosis"] = diagnose(k, subkey, incoming, (live, dead_info), lanes)
    rows.append(row)
    print("ITER", json.dumps(row), flush=True)


adapter = build("carry")
adapter.iteration_callback = callback
result = adapter.run(loglike, logprior, model.theta_init, jax.random.PRNGKey(20260930))
report = {
    "ceridwen": ceridwen.__file__, "device": jax.devices()[0].device_kind, "x64": bool(jax.config.jax_enable_x64),
    "iterations": len(rows), "iterations_bitwise_equal": sum(row["bitwise_equal"] for row in rows),
    "iterations_that_differ": [row["iteration"] for row in rows if not row["bitwise_equal"]],
    "log_evidence": float(result.log_evidence), "n_dead": int(len(result.log_likelihoods)),
    "script_wall_s": time.perf_counter() - script_start, "rows": rows,
}
(OUT / "report.json").write_text(json.dumps(report, indent=1))
print("DONE", json.dumps({k: v for k, v in report.items() if k != "rows"}), flush=True)
