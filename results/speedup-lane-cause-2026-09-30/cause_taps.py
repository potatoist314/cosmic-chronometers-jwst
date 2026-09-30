"""Stage taps: which stage of the likelihood first differs between the two GPU programs.

Input: the ten states of results/speedup-lane-check-2026-09-30/run/check where one
lane differed. Each kernel runs on a state twice, plain and with a host callback
that records every batch the likelihood and the prior receive and return. The
records give, for each lane, the sequence of candidates and the values each
program computed for them.

Reuses scripts/benchmark_baked_runtime.build and
scripts/benchmark_ceridwen_vast._make_log_functions, as lane_check.py does.
"""
import json
import os
import pickle
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(os.environ["SPEEDUP_ROOT"])
OUT = Path(os.environ["SPEEDUP_OUT"])
STATES = Path(os.environ["CAUSE_STATES"])
OUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
os.environ["MPLBACKEND"] = "Agg"
os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp()
sys.path.insert(0, str(ROOT / "scripts"))

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
import benchmark_baked_runtime  # noqa: E402
if "SPEEDUP_NOTEBOOK" in os.environ:  # local: the notebook of the pinned revision
    benchmark_baked_runtime.NOTEBOOK = Path(os.environ["SPEEDUP_NOTEBOOK"])
from benchmark_ceridwen_vast import _make_log_functions  # noqa: E402
import ceridwen  # noqa: E402
from ceridwen.model.model import SedModel  # noqa: E402
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter  # noqa: E402

if os.environ["EXPECT_CERIDWEN"] not in ceridwen.__file__:
    raise SystemExit(f"ceridwen loaded from {ceridwen.__file__}")
SedModel._prior_upper_bound = lambda self, name: None  # 2n pad, as in the lane check

TAG = os.environ.get("CAUSE_TAG", "trace")
TRACE = os.environ.get("CAUSE_TRACE", "1") == "1"
INNER, DELETE = 65, 100
script_start = time.perf_counter()
check = json.loads((STATES / "report.json").read_text())
EVENTS = ([int(x) for x in os.environ["CAUSE_EVENTS"].split(",")] if os.environ.get("CAUSE_EVENTS")
          else check["iterations_that_differ"])
INJECT = dict(zip(("event", "lane", "at"), map(int, os.environ["CAUSE_INJECT"].split(":")))) \
    if os.environ.get("CAUSE_INJECT") else {}  # self-test: corrupt one likelihood value of the lane program

ns = benchmark_baked_runtime.build(True, True)
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior = _make_log_functions(model, likelihood)


# Taps: jax.debug.callback leaves the data flow (and the fusion) of the program unchanged.
# Each tap records the first N batches it sees, keyed by the batch's parameter bytes.
N = int(os.environ.get("CAUSE_TAP_RECORDS", "6"))
TAPS = {}


def key_of(theta):
    return jnp.concatenate([jnp.ravel(theta[name]) for name in sorted(theta)])


def tap(name, key, value):
    def record(k, *leaves):
        store = TAPS.setdefault(name, {})
        if len(store) < N:
            store.setdefault(np.asarray(k).tobytes(), [np.array(l, copy=True) for l in leaves])
    jax.debug.callback(record, key, *jax.tree.leaves(value))
    return value


def wrap(obj, method, name, key_from):
    original = getattr(obj, method)

    def wrapped(*args, **kwargs):
        value = original(*args, **kwargs)
        return tap(name, key_of(key_from(*args, **kwargs)), value)
    setattr(obj, method, wrapped)


csp = model.csp
wrap(model, "apply_transforms", "1_transforms", lambda theta: theta)
wrap(csp, "attenuate_dust", "2a_attenuate_dust", lambda wave, theta: theta)
wrap(csp, "_spectrum_from_sfh_basis", "2b_sfh_basis_einsum", lambda theta: theta)
if hasattr(csp, "_dust_group_attenuation"):
    wrap(csp, "_dust_group_attenuation", "2c_group_attenuation", lambda attn, theta: theta)
wrap(csp, "get_spectrum_components", "2_native_spectrum", lambda theta: theta)
wrap(csp, "_apply_mass_redshift_igm", "3_mass_redshift_igm", lambda a, b, c, theta: theta)
wrap(csp, "_project_observations", "4_predictions", lambda a, b, c, obs, theta: theta)
object.__setattr__(likelihood, "likelihoods", tuple(
    (lambda comp, nm: (lambda *a, params, **k: tap(f"5_{nm}", key_of(params), comp(*a, params=params, **k))))(component, name)
    for name, component in zip(likelihood.keys, likelihood.likelihoods)))

loglike, logprior = _make_log_functions(model, likelihood)


def keyed_loglike(theta):
    return tap("6_total", key_of(theta), loglike(theta))


def steps(like, prior):
    settings = dict(num_live=500, num_inner_steps=INNER, num_delete=DELETE, logZ_tol=-5.0, verbose=False)
    return {kernel: jax.jit(BlackJAXNestedSamplerAdapter(model.priors, **settings, slice_kernel=kernel)
                            ._build_nested_sampler(like, prior, INNER, DELETE).step)
            for kernel in ("carry", "lanes")}


def flat(position, index=None):
    parts = np.concatenate([np.asarray(v).reshape(np.asarray(v).shape[0], -1)
                            for _, v in sorted(position.items())], axis=1)
    return parts if index is None else parts[index]


def ulps(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if a.dtype.kind != "f":
        return None
    spacing = np.spacing(np.maximum(np.abs(a), np.abs(b)).astype(a.dtype)).astype(np.float64)
    return np.abs(a.astype(np.float64) - b.astype(np.float64)) / spacing


kernels = steps(keyed_loglike, logprior)
report = {"tag": TAG, "jax": jax.__version__, "device": jax.devices()[0].device_kind,
          "xla_flags": os.environ.get("XLA_FLAGS", ""), "records_per_tap": N, "events": []}
for event in EVENTS:
    data = np.load(STATES / f"iteration_{event}.npz")
    with open(STATES / f"iteration_{event}_state.pkl", "rb") as fh:
        state = jax.tree.map(jnp.asarray, pickle.load(fh))
    key, target = jnp.asarray(data["subkey"]), data["target_index"]
    taps, new = {}, {}
    for kernel, step in kernels.items():
        TAPS.clear()
        out = step(key, state)
        jax.block_until_ready(out)
        taps[kernel] = {name: dict(store) for name, store in TAPS.items()}
        new[kernel] = flat(out[0].particles.position, target)
    row = {"event": event, "tapped_lanes_that_differ": np.flatnonzero((new["carry"] != new["lanes"]).any(axis=1)).tolist(),
           "new_equals_first_instance": {k: bool(np.array_equal(new[k], data[f"new_{k}"])) for k in new},
           "stages": {}}
    # The 6_total tap tells which stage-1 keys (raw theta) both programs evaluated; stage 2-4 keys are model_theta.
    raw_common = [k for k in taps["carry"].get("6_total", {}) if k in taps["lanes"].get("6_total", {})]
    for name in sorted(set(taps["carry"]) | set(taps["lanes"])):
        a, b = taps["carry"].get(name, {}), taps["lanes"].get(name, {})
        common = [k for k in a if k in b]
        stage = {"records": [len(a), len(b)], "batches_in_both": len(common), "leaves": []}
        for k in common[:1]:
            for leaf_a, leaf_b in zip(a[k], b[k]):
                equal = np.array_equal(leaf_a, leaf_b, equal_nan=True)
                u = ulps(leaf_a, leaf_b)
                leaf = {"shape": list(leaf_a.shape), "dtype": str(leaf_a.dtype), "equal": bool(equal)}
                if u is not None and not equal:
                    d = np.abs(leaf_a.astype(np.float64) - leaf_b.astype(np.float64))
                    leaf.update(elements_that_differ=int((d > 0).sum()), elements=int(d.size),
                                max_ulps=float(np.nanmax(u)), median_ulps_of_differing=float(np.median(u[d > 0])),
                                max_abs=float(np.nanmax(d)),
                                max_rel=float(np.nanmax(d / np.maximum(np.abs(leaf_a.astype(np.float64)), 1e-300))),
                                rows_that_differ=int((d.reshape(d.shape[0], -1) > 0).any(axis=1).sum()) if d.ndim > 1 else None)
                stage["leaves"].append(leaf)
        row["stages"][name] = stage
    row["raw_batches_in_both"] = len(raw_common)
    report["events"].append(row)
    print("EVENT", json.dumps(row), flush=True)
    np.savez(OUT / f"{TAG}_event_{event}_taps.npz", **{f"{kernel}__{name}__{i}": leaf
             for kernel in taps for name, store in taps[kernel].items()
             for k in list(store)[:1] for i, leaf in enumerate(store[k])})
report["script_wall_s"] = time.perf_counter() - script_start
(OUT / f"{TAG}.json").write_text(json.dumps(report, indent=1))
print("DONE", json.dumps({k: v for k, v in report.items() if k != "events"}), flush=True)
