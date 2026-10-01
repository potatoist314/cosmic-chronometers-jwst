"""The production sampler path: BlackJAXNestedSamplerAdapter.run on the M1_210210 model.

Env: RUN_TAG, EXPECT_CERIDWEN, RUN_SEED, SPEEDUP_OUT. Records run() wall time (init, threaded
step compile, NS loop, finalisation), the adapter's sampling wall time, logZ and the samples.
"""
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import common  # noqa: E402
import jax  # noqa: E402
import numpy as np  # noqa: E402
import ceridwen  # noqa: E402
from ceridwen.sampler.nested import BlackJAXNestedSamplerAdapter  # noqa: E402

TAG = os.environ["RUN_TAG"]
OUT = Path(os.environ["SPEEDUP_OUT"]) / TAG
OUT.mkdir(parents=True, exist_ok=True)
if os.environ.get("EXPECT_CERIDWEN", "") not in ceridwen.__file__:
    raise SystemExit(f"ceridwen loaded from {ceridwen.__file__}")
ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior, _ = common.log_functions(model, likelihood)
adapter = BlackJAXNestedSamplerAdapter(model.priors, **ns["SETTINGS"]["sampler"], verbose=False,
                                       progress_path=str(OUT / "progress.jsonl"))
t = time.perf_counter()
result = adapter.run(loglike, logprior, model.theta_init, jax.random.PRNGKey(int(os.environ.get("RUN_SEED", "20260930"))))
run_s = time.perf_counter() - t
np.savez(OUT / "samples.npz", log_likelihoods=np.asarray(result.log_likelihoods),
         log_weights=np.asarray(result.log_weights),
         **{f"samples__{k}": np.asarray(v) for k, v in result.samples.items()})
summary = {"tag": TAG, "ceridwen": ceridwen.__file__, "run_s": run_s, "wall_time_s": result.wall_time_s,
           "logZ": float(result.log_evidence), "logZ_err": float(result.log_evidence_err),
           "n_likelihood_calls": int(result.n_likelihood_calls)}
(OUT / "summary.json").write_text(json.dumps(summary, indent=1))
print("DONE", json.dumps(summary), flush=True)
