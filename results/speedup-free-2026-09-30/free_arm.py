"""One seeded nested run of the production M1_210210 model for the free-speedup check.

Reuses scripts/benchmark_baked_runtime.build (the committed notebook model) and
scripts/benchmark_ceridwen_vast._make_log_functions. The arm selects the slice
kernel (RUN_KERNEL), the LOSVD zero pad (RUN_PAD) and, through PYTHONPATH, the
ceridwen and sedpy_jax trees.
"""
import json
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(os.environ["SPEEDUP_ROOT"])
TAG = os.environ["RUN_TAG"]
OUT = Path(os.environ["SPEEDUP_OUT"]) / TAG
OUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)
os.environ["MPLBACKEND"] = "Agg"
os.environ["CERIDWEN_TARGET_ID"] = "M1_210210"
os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp(dir=OUT)
sys.path.insert(0, str(ROOT / "scripts"))

import jax  # noqa: E402
import numpy as np  # noqa: E402
import benchmark_baked_runtime  # noqa: E402
from benchmark_ceridwen_vast import _make_log_functions  # noqa: E402
import ceridwen  # noqa: E402
import sedpy_jax  # noqa: E402
from ceridwen.model.model import SedModel  # noqa: E402
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter  # noqa: E402

for module, expected in ((ceridwen, os.environ["EXPECT_CERIDWEN"]), (sedpy_jax, os.environ["EXPECT_SEDPY"])):
    if expected not in module.__file__:
        raise SystemExit(f"{module.__name__} loaded from {module.__file__}, expected {expected}")
if os.environ["RUN_PAD"] == "0" and hasattr(SedModel, "_prior_upper_bound"):
    SedModel._prior_upper_bound = lambda self, name: None  # 2n pad, the current path

script_start = time.perf_counter()
ns = benchmark_baked_runtime.build(True, True)
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior = _make_log_functions(model, likelihood)

progress = OUT / "progress.jsonl"
progress.unlink(missing_ok=True)
# Production sampler settings; RUN_SMOKE is the notebook's smoke set, for a local script check.
sampler = (dict(num_live=16, num_inner_steps=2, num_delete=8, logZ_tol=1e4) if os.environ.get("RUN_SMOKE")
           else dict(num_live=500, num_inner_steps=65, num_delete=100, logZ_tol=-5.0))
adapter = BlackJAXNestedSamplerAdapter(
    model.priors, **sampler,
    verbose=False, checkpoint_interval_s=0.0, progress_path=str(progress),
    slice_kernel=os.environ["RUN_KERNEL"])
result = adapter.run(loglike, logprior, model.theta_init, jax.random.PRNGKey(20260930))
rows = [json.loads(line) for line in progress.read_text().splitlines()]
np.savez(OUT / "result.npz",
         loglikelihood=np.asarray(result.raw["loglikelihood"]),
         loglikelihood_birth=np.asarray(result.raw["loglikelihood_birth"]),
         log_weights=np.asarray(result.log_weights),
         iteration_s=np.asarray([row["iteration_s"] for row in rows]),
         **{f"position__{k}": np.asarray(v) for k, v in result.raw["positions"].items()})
summary = {
    "tag": TAG, "kernel": os.environ["RUN_KERNEL"], "pad": os.environ["RUN_PAD"],
    "ceridwen": ceridwen.__file__, "sedpy_jax": sedpy_jax.__file__,
    "device": jax.devices()[0].device_kind, "x64": bool(jax.config.jax_enable_x64),
    "log_evidence": float(result.log_evidence), "sampler_logZ": rows[-1]["logZ"],
    "n_dead": int(len(result.log_likelihoods)), "n_likelihood_calls": int(result.n_likelihood_calls),
    "iterations": len(rows), "sampling_wall_s": float(result.wall_time_s),
    "first_iteration_s": rows[0]["iteration_s"],
    "later_iterations_s": float(sum(row["iteration_s"] for row in rows[1:])),
    "script_wall_s": time.perf_counter() - script_start,
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=1))
print("DONE", json.dumps(summary), flush=True)
