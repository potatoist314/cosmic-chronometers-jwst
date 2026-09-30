"""CPU replay of the GPU iterations where the lane kernel and the carry kernel differed (scratch)."""
import json, os, pickle, sys, tempfile
from pathlib import Path
ROOT = Path(os.environ["SPEEDUP_ROOT"]); OUT = Path(os.environ["SPEEDUP_OUT"]); OUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
os.environ["MPLBACKEND"] = "Agg"; os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp(dir=OUT)
sys.path.insert(0, str(ROOT / "scripts"))
import jax, jax.numpy as jnp, numpy as np
import benchmark_baked_runtime
benchmark_baked_runtime.NOTEBOOK = Path(os.environ["SPEEDUP_NOTEBOOK"])
from benchmark_ceridwen_vast import _make_log_functions
import ceridwen
from ceridwen.model.model import SedModel
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter
assert "ceridwen-lanes" in ceridwen.__file__
SedModel._prior_upper_bound = lambda self, name: None
CHECK = ROOT / "results/speedup-lane-check-2026-09-30/run/check"
report = json.loads((CHECK / "report.json").read_text())
ns = benchmark_baked_runtime.build(True, True)
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior = _make_log_functions(model, likelihood)
settings = dict(num_live=500, num_inner_steps=65, num_delete=100, logZ_tol=-5.0)
steps = {k: jax.jit(BlackJAXNestedSamplerAdapter(model.priors, **settings, verbose=False, slice_kernel=k)._build_nested_sampler(loglike, logprior, 65, 100).step) for k in ("carry", "lanes")}
def flat(position, index):
    return np.concatenate([np.asarray(v).reshape(np.asarray(v).shape[0], -1) for _, v in sorted(position.items())], axis=1)[index]
for row in report["rows"]:
    if "diagnosis" not in row: continue
    k = row["iteration"]; lane = row["diagnosis"]["lanes_that_differ"][0]
    data = np.load(CHECK / f"iteration_{k}.npz")
    with open(CHECK / f"iteration_{k}_state.pkl", "rb") as fh: state = jax.tree.map(jnp.asarray, pickle.load(fh))
    key = jnp.asarray(data["subkey"])
    out = {name: step(key, state) for name, step in steps.items()}
    new = {name: flat(o[0].particles.position, data["target_index"]) for name, o in out.items()}
    info = out["carry"][1].update_info
    others = np.arange(100) != lane
    res = {"iteration": k, "lane": lane, "cpu_carry_equals_cpu_lanes": bool(np.array_equal(new["carry"], new["lanes"])),
           "cpu_vs_gpu_carry_lane": float(np.abs(new["carry"][lane] - data["new_carry"][lane]).max()),
           "cpu_vs_gpu_lanes_lane": float(np.abs(new["carry"][lane] - data["new_lanes"][lane]).max()),
           "gpu_carry_vs_gpu_lanes_lane": float(np.abs(data["new_carry"][lane] - data["new_lanes"][lane]).max()),
           "other_lanes_cpu_vs_gpu_carry_gt_1e-6": int((np.abs(new["carry"][others] - data["new_carry"][others]).max(axis=1) > 1e-6).sum()),
           "lane_max_shrink": int(np.asarray(info.num_shrink)[lane].max()), "lane_accepted_all": bool(np.asarray(info.is_accepted)[lane].all()),
           "lane_calls": int((np.asarray(info.num_shrink)[lane] + np.asarray(info.num_expansions)[lane] + 2).sum()),
           "max_calls_any_lane": int((np.asarray(info.num_shrink) + np.asarray(info.num_expansions) + 2).sum(axis=1).max()),
           "rank_of_lane_calls": int(((np.asarray(info.num_shrink) + np.asarray(info.num_expansions) + 2).sum(axis=1) > (np.asarray(info.num_shrink)[lane] + np.asarray(info.num_expansions)[lane] + 2).sum()).sum())}
    print("EVENT", json.dumps(res), flush=True)
