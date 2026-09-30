"""Cause of the GPU differences between the lane kernel and the carry kernel.

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
if os.environ.get("CAUSE_ONLY"):   # keep only these likelihood components (photometry, spectrum)
    import dataclasses
    kept = [(k, l) for k, l in zip(likelihood.keys, likelihood.likelihoods) if k in os.environ["CAUSE_ONLY"].split(",")]
    likelihood = dataclasses.replace(likelihood, keys=type(likelihood.keys)(k for k, _ in kept),
                                     likelihoods=type(likelihood.likelihoods)(l for _, l in kept))
loglike, logprior = _make_log_functions(model, likelihood)

REC = {"x": [], "ll": [], "lp": {}, "inject": None}


def _record_loglike(x, value):
    value = np.array(value, copy=True)
    if REC["inject"] is not None and len(REC["ll"]) == REC["inject"]["at"]:
        value.reshape(-1)[REC["inject"]["lane"]] -= 1e6
    REC["x"].append(np.array(x, copy=True).reshape(-1, np.shape(x)[-1]))
    REC["ll"].append(value.reshape(-1).copy())
    return value


def _record_logprior(x, value):   # keyed by the batch: XLA sets the order of the two callbacks
    REC["lp"][np.asarray(x).tobytes()] = np.array(value, copy=True).reshape(-1)
    return np.asarray(value)


def traced_loglike(theta):
    value = loglike(theta)
    x = jnp.concatenate([jnp.ravel(theta[name]) for name in sorted(theta)])
    return jax.pure_callback(_record_loglike, jax.ShapeDtypeStruct((), value.dtype), x, value,
                             vmap_method="broadcast_all")


def traced_logprior(theta):
    value = logprior(theta)
    x = jnp.concatenate([jnp.ravel(theta[name]) for name in sorted(theta)])
    return jax.pure_callback(_record_logprior, jax.ShapeDtypeStruct((), value.dtype), x, value,
                             vmap_method="broadcast_all")


def steps(like, prior):
    settings = dict(num_live=500, num_inner_steps=INNER, num_delete=DELETE, logZ_tol=-5.0, verbose=False)
    return {kernel: jax.jit(BlackJAXNestedSamplerAdapter(model.priors, **settings, slice_kernel=kernel)
                            ._build_nested_sampler(like, prior, INNER, DELETE).step)
            for kernel in ("carry", "lanes")}


plain = steps(loglike, logprior)
traced = steps(traced_loglike, traced_logprior) if TRACE else {}
batch_loglike = jax.jit(jax.vmap(loglike))
bits = lambda a: np.ascontiguousarray(a, dtype=np.float64).view(np.uint64)  # noqa: E731


def flat(position, index=None):
    parts = np.concatenate([np.asarray(v).reshape(np.asarray(v).shape[0], -1)
                            for _, v in sorted(position.items())], axis=1)
    return parts if index is None else parts[index]


def same(a, b):
    a, b = jax.tree.leaves(a), jax.tree.leaves(b)
    return len(a) == len(b) and all(np.array_equal(np.asarray(x), np.asarray(y), equal_nan=True)
                                    for x, y in zip(a, b))


def run(step, key, state, inject=None):
    REC.update(x=[], ll=[], lp={}, inject=inject)
    out = step(key, state)
    jax.block_until_ready(out)
    missing = np.full(DELETE, np.nan)
    return out, dict(x=REC["x"], ll=REC["ll"], lp=[REC["lp"].get(x.tobytes(), missing) for x in REC["x"]])


def expansion_counts(info):
    left = np.floor(-np.asarray(info.bracket_left)).astype(int)   # width = 1
    right = np.floor(np.asarray(info.bracket_right)).astype(int)
    return left, right, np.asarray(info.num_shrink), bool((left + right == np.asarray(info.num_expansions)).all())


LAYOUTS = [("iL", "iR", "lL", "lR"), ("iL", "iR", "lR", "lL"), ("iR", "iL", "lL", "lR"),
           ("iR", "iL", "lR", "lL"), ("iL", "lL", "iR", "lR"), ("iR", "lR", "iL", "lL")]


def logical_lanes(info):
    """One loop for each lane: evaluation n of a lane is record n."""
    n_left, n_right, n_shrink, split_ok = expansion_counts(info)
    index, label = [[] for _ in range(DELETE)], [[] for _ in range(DELETE)]
    for lane in range(DELETE):
        for s in range(INNER):
            for phase, m in (("left", n_left[lane, s] + 1), ("right", n_right[lane, s] + 1),
                             ("shrink", n_shrink[lane, s])):
                for j in range(m):
                    index[lane].append(len(index[lane]))
                    label[lane].append((s, phase, j))
    return index, label, max(len(i) for i in index), split_ok


def logical_carry(info, x=None, reference=None):
    """The same for the carry program.

    Each slice step has two first edge tests, two expansion loops and one shrink loop; each
    loop is as long as its slowest lane. XLA sets the order of the four edge blocks. For each
    step, the order is the one under which the most lanes get the positions of ``reference``
    (the lane program).
    """
    n_left, n_right, n_shrink, split_ok = expansion_counts(info)
    index, label = [[] for _ in range(DELETE)], [[] for _ in range(DELETE)]
    r, chosen, agree = 0, [], []
    for s in range(INNER):
        counts = {"L": n_left[:, s], "R": n_right[:, s]}
        options = []
        for layout in LAYOUTS:
            at, first, loop = r, {}, {}
            for block in layout:
                if block[0] == "i":
                    first[block[1]], at = at, at + 1
                else:
                    loop[block[1]], at = at, at + counts[block[1]].max()
            edges = [[first["L"], *range(loop["L"], loop["L"] + counts["L"][lane]),
                      first["R"], *range(loop["R"], loop["R"] + counts["R"][lane])] for lane in range(DELETE)]
            score = 0 if x is None else sum(
                reference[lane].get(s) is not None and len(reference[lane][s]) >= len(edges[lane])
                and np.array_equal(x[edges[lane], lane], reference[lane][s][:len(edges[lane])])
                for lane in range(DELETE))
            options.append((score, edges, at))
        best = int(np.argmax([o[0] for o in options]))
        score, edges, at = options[best]
        chosen.append(best)
        agree.append(int(score))
        for lane in range(DELETE):
            index[lane] += edges[lane] + list(range(at, at + n_shrink[lane, s]))
            label[lane] += ([(s, "left", j) for j in range(counts["L"][lane] + 1)]
                            + [(s, "right", j) for j in range(counts["R"][lane] + 1)]
                            + [(s, "shrink", j) for j in range(n_shrink[lane, s])])
        r = at + n_shrink[:, s].max()
    return index, label, r, split_ok, chosen, agree


def lane_sequence(rec, index, lane):
    rows = np.asarray(index[lane])
    return (np.stack([rec["x"][r][lane] for r in rows]), np.array([rec["ll"][r][lane] for r in rows]),
            np.array([rec["lp"][r][lane] for r in rows]))


def context(rec_by_kernel):
    """Does one position in one lane always get one likelihood value? Frozen lanes repeat their position."""
    seen = {}
    for kernel, rec in rec_by_kernel.items():
        for x, ll in zip(rec["x"], rec["ll"]):
            for lane in range(x.shape[0]):
                seen.setdefault((lane, x[lane].tobytes()), {}).setdefault(kernel, []).append(ll[lane])
    out = {"positions": len(seen), "positions_evaluated_more_than_once": 0, "positions_with_two_values": 0,
           "positions_in_both_programs": 0, "positions_in_both_with_different_value": 0, "max_abs_difference": 0.0}
    for values in seen.values():
        every = np.array([v for vs in values.values() for v in vs])
        out["positions_evaluated_more_than_once"] += every.size > 1
        if np.unique(bits(every)).size > 1:
            out["positions_with_two_values"] += 1
            out["max_abs_difference"] = max(out["max_abs_difference"], float(np.nanmax(every) - np.nanmin(every)))
        if len(values) == 2:
            out["positions_in_both_programs"] += 1
            out["positions_in_both_with_different_value"] += np.unique(bits(every)).size > 1
    return {k: (float(v) if isinstance(v, float) else int(v)) for k, v in out.items()}


def unflatten(rows, template):
    out, at = {}, 0
    for name in sorted(template):
        shape = np.asarray(template[name]).shape[1:]
        size = int(np.prod(shape, dtype=int))
        out[name] = jnp.asarray(rows[:, at:at + size].reshape((rows.shape[0],) + shape))
        at += size
    return out


def stages(theta):
    model_theta = model.apply_transforms(theta)
    continuum, line = model.csp.get_spectrum_components(model_theta)
    phot, slit, line = model.csp._apply_mass_redshift_igm(continuum, continuum, line, model_theta)
    predictions = model.csp._project_observations(phot, slit, line, model.observations, model_theta)
    parts = {}
    for key, component in zip(likelihood.keys, likelihood.likelihoods):
        obs = model.obs_dict[key]
        parts[key] = component(obs.flux, predictions[key], obs.uncertainty, obs.mask, params=theta)[0]
    return {"1_transforms": {k: v for k, v in model_theta.items() if hasattr(v, "dtype")},
            "2_native_spectrum": continuum, "3_mass_redshift_igm": (phot, slit),
            "4_predictions": predictions, "5_likelihood_parts": parts, "6_total": sum(parts.values())}


batch_stages = jax.jit(jax.vmap(stages))


def replay(event, lane, template, batches, recorded, x_star):
    """The recorded batches again through a plain batched likelihood, then stage by stage."""
    out = {"recorded": {k: float(v) for k, v in recorded.items()}, "again": {}, "stages": {}}
    for name, rows in batches.items():
        value = np.asarray(batch_loglike(unflatten(rows, template)))[lane]
        out["again"][name] = {"value": float(value), "equals_recorded": bool(bits(value) == bits(recorded[name]))}
    copies = np.asarray(batch_loglike(unflatten(np.repeat(x_star[None], DELETE, axis=0), template)))
    single = np.asarray(loglike({k: v[0] for k, v in unflatten(x_star[None], template).items()}))
    out["again"]["100_copies"] = {"distinct_values": int(np.unique(bits(copies)).size), "value_in_lane": float(copies[lane]),
                                  "min": float(copies.min()), "max": float(copies.max())}
    out["again"]["single"] = float(single)
    try:
        staged = {name: jax.tree.map(lambda v: np.asarray(v)[lane], batch_stages(unflatten(rows, template)))
                  for name, rows in batches.items()}
        (a_name, a), (b_name, b) = staged.items()
        for stage in sorted(a):
            la, lb = jax.tree.leaves(a[stage]), jax.tree.leaves(b[stage])
            differ = [int((np.asarray(x) != np.asarray(y)).sum()) for x, y in zip(la, lb)]
            largest = [float(np.nanmax(np.abs(np.asarray(x, float) - np.asarray(y, float)) /
                                       np.maximum(np.abs(np.asarray(x, float)), 1e-300))) for x, y in zip(la, lb)]
            out["stages"][stage] = {"elements_that_differ": differ, "elements": [int(np.asarray(x).size) for x in la],
                                    "max_relative_difference": largest, "dtype": [str(np.asarray(x).dtype) for x in la]}
        out["stages"]["total_equals_recorded"] = {
            name: bool(bits(staged[name]["6_total"]) == bits(recorded[name])) for name in staged}
        np.savez(OUT / f"{TAG}_event_{event}_stages.npz",
                 **{f"{name}__{stage}__{i}": leaf for name in staged for stage in staged[name]
                    for i, leaf in enumerate(jax.tree.leaves(staged[name][stage]))})
    except Exception as error:  # the stage split is a convenience; the recorded values stand without it
        out["stages"]["error"] = repr(error)
    return out


def describe(seq, label, q):
    x, ll, lp = seq
    return None if q >= len(ll) else {"label": list(label[q]), "loglikelihood": float(ll[q]), "logprior": float(lp[q])}


rows = []
for event in EVENTS:
    data = np.load(STATES / f"iteration_{event}.npz")
    with open(STATES / f"iteration_{event}_state.pkl", "rb") as fh:
        state = jax.tree.map(jnp.asarray, pickle.load(fh))
    key, target, L0 = jnp.asarray(data["subkey"]), data["target_index"], float(data["loglikelihood_0"])
    first = {kernel: run(step, key, state)[0] for kernel, step in plain.items()}
    second = {kernel: run(step, key, state)[0] for kernel, step in plain.items()}
    new = {kernel: flat(out[0].particles.position, target) for kernel, out in first.items()}
    row = {"event": event, "L0": L0,
           "plain_lanes_that_differ": np.flatnonzero((new["carry"] != new["lanes"]).any(axis=1)).tolist(),
           "plain_all_leaves_equal": same(first["carry"], first["lanes"]),
           "second_call_equal": {kernel: same(first[kernel], second[kernel]) for kernel in plain},
           "lanes_that_differ_from_first_instance": {
               kernel: np.flatnonzero((new[kernel] != data[f"new_{kernel}"]).any(axis=1)).tolist() for kernel in plain}}
    if TRACE:
        outs, recs = {}, {}
        for kernel, step in traced.items():
            inject = INJECT if INJECT and INJECT["event"] == event and kernel == "lanes" else None
            outs[kernel], recs[kernel] = run(step, key, state, inject)
        row["traced_equals_plain"] = {kernel: same(outs[kernel], first[kernel]) for kernel in traced}
        row["context"] = context(recs)
        sequences, labels, row["structure"] = {}, {}, {}
        indices = {}
        for kernel in ("lanes", "carry"):
            info = outs[kernel][1].update_info
            if kernel == "lanes":
                indices[kernel], labels[kernel], expected, split_ok = logical_lanes(info)
            else:
                expected, split_ok = logical_carry(info)[2:4]
            row["structure"][kernel] = {"records": len(recs[kernel]["ll"]), "expected": int(expected), "split_ok": split_ok,
                                        "prior_missing": int(sum(np.isnan(v).all() for v in recs[kernel]["lp"]))}
            if len(recs[kernel]["ll"]) != expected:
                break
            if kernel == "carry":
                reference = []
                for lane in range(DELETE):
                    by_step = {}
                    for row_x, (s, _, _) in zip(sequences["lanes"][lane][0], labels["lanes"][lane]):
                        by_step.setdefault(s, []).append(row_x)
                    reference.append({s: np.stack(v) for s, v in by_step.items()})
                indices[kernel], labels[kernel], _, _, chosen, agree = logical_carry(info, np.stack(recs[kernel]["x"]), reference)
                row["structure"]["carry"].update(layouts_used=sorted(set(chosen)), fewest_lanes_that_agree_in_a_step=min(agree))
            sequences[kernel] = [lane_sequence(recs[kernel], indices[kernel], lane) for lane in range(DELETE)]
        row["lanes"] = []
        for lane in range(DELETE) if len(sequences) == 2 else ():
            (xc, lc, pc), (xl, ll_, pl) = sequences["carry"][lane], sequences["lanes"][lane]
            n = min(len(lc), len(ll_))
            dx, dl, dp = (xc[:n] != xl[:n]).any(axis=1), bits(lc[:n]) != bits(ll_[:n]), bits(pc[:n]) != bits(pl[:n])
            bad = np.flatnonzero(dx | dl | dp)
            if not bad.size and len(lc) == len(ll_):
                continue
            q = int(bad[0]) if bad.size else n
            found = {"lane": lane, "evaluation": q, "evaluations": {"carry": len(lc), "lanes": len(ll_)},
                     "position_differs": bool(q < n and dx[q]), "loglikelihood_differs": bool(q < n and dl[q]),
                     "logprior_differs": bool(q < n and dp[q]),
                     "carry": describe(sequences["carry"][lane], labels["carry"][lane], q),
                     "lanes": describe(sequences["lanes"][lane], labels["lanes"][lane], q),
                     "carry_before": describe(sequences["carry"][lane], labels["carry"][lane], max(q - 1, 0)),
                     "lanes_before": describe(sequences["lanes"][lane], labels["lanes"][lane], max(q - 1, 0)),
                     "carry_after": describe(sequences["carry"][lane], labels["carry"][lane], q + 1),
                     "lanes_after": describe(sequences["lanes"][lane], labels["lanes"][lane], q + 1)}
            if q < n:
                found["max_abs_position_difference"] = float(np.abs(xc[q] - xl[q]).max())
                index_c = indices["carry"][lane][q]
                batches = {"carry": recs["carry"]["x"][index_c], "lanes": recs["lanes"]["x"][q]}
                np.savez(OUT / f"{TAG}_event_{event}_lane_{lane}.npz", q=q, L0=L0, x_carry=xc, x_lanes=xl,
                         ll_carry=lc, ll_lanes=ll_, lp_carry=pc, lp_lanes=pl,
                         batch_carry=batches["carry"], batch_lanes=batches["lanes"],
                         ll_batch_carry=recs["carry"]["ll"][index_c], ll_batch_lanes=recs["lanes"]["ll"][q],
                         labels_carry=np.array([f"{s}:{p}:{j}" for s, p, j in labels["carry"][lane]]),
                         labels_lanes=np.array([f"{s}:{p}:{j}" for s, p, j in labels["lanes"][lane]]))
                if found["loglikelihood_differs"] and not found["position_differs"]:
                    found["replay"] = replay(event, lane, state.particles.position, batches,
                                             {"carry": lc[q], "lanes": ll_[q]}, xc[q])
            row["lanes"].append(found)
    rows.append(row)
    print("EVENT", json.dumps(row), flush=True)

report = {"tag": TAG, "ceridwen": ceridwen.__file__, "jax": jax.__version__, "device": jax.devices()[0].device_kind,
          "x64": bool(jax.config.jax_enable_x64), "xla_flags": os.environ.get("XLA_FLAGS", ""),
          "script_wall_s": time.perf_counter() - script_start, "events": rows}
(OUT / f"{TAG}.json").write_text(json.dumps(report, indent=1))
print("DONE", json.dumps({k: v for k, v in report.items() if k != "events"}), flush=True)
