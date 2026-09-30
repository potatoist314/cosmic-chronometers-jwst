"""Time BlackJAXNestedSamplerAdapter.run itself from its start to the end of its first iterations.

Env: RUN_TAG, SPEEDUP_OUT, EXPECT_CERIDWEN, RUN_ITERS (iterations before stopping, default 3),
RUN_SEED, RUN_SMOKE. Writes <RUN_TAG>/start.json and dead.npz (the dead points of those iterations).
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
ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior, _ = common.log_functions(model, likelihood)
settings = ns["SETTINGS"]["sampler_quick" if os.environ.get("RUN_SMOKE") else "sampler"]
limit = int(os.environ.get("RUN_ITERS", "3"))
marks, dead = [], []


class Stop(Exception):
    pass


def callback(iteration, key, incoming, outgoing, info, step, elapsed):
    marks.append({"iteration": iteration, "t": time.perf_counter() - t0, "iteration_s": elapsed})
    dead.append((np.asarray(info.particles.loglikelihood),
                 {k: np.asarray(v) for k, v in info.particles.position.items()}))
    if iteration == limit:
        raise Stop


adapter = BlackJAXNestedSamplerAdapter(model.priors, **settings, verbose=False, iteration_callback=callback)
t0 = time.perf_counter()
try:
    adapter.run(loglike, logprior, model.theta_init, jax.random.PRNGKey(int(os.environ.get("RUN_SEED", "20260930"))))
except Stop:
    pass
np.savez(OUT / "dead.npz", loglikelihood=np.concatenate([d[0] for d in dead]),
         **{f"position__{k}": np.concatenate([d[1][k] for d in dead]) for k in dead[0][1]})
summary = {"tag": TAG, "ceridwen": ceridwen.__file__, "device": jax.devices()[0].device_kind,
           "xla_flags": os.environ.get("XLA_FLAGS", ""), "first_iteration_done_s": marks[0]["t"],
           "first_iteration_s": marks[0]["iteration_s"], "marks": marks}
(OUT / "start.json").write_text(json.dumps(summary, indent=1))
print("DONE", json.dumps({k: v for k, v in summary.items() if k != "marks"}), flush=True)
