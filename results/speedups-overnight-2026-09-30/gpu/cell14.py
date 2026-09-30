"""Time the fit notebook's posterior-predictive cell (cell 14): wall time, XLA compile time within
it (jax.monitoring backend-compile events), and a second run with every executable cached.

Env: PROF_DEAD (dead points standing in for the posterior), SPEEDUP_OUT, RUN_TAG, SPEEDUP_NOTEBOOK.
Writes <RUN_TAG>/cell14.json.
"""
import json
import os
import pickle
import time
from pathlib import Path

import common
import jax
import numpy as np

OUT = Path(os.environ["SPEEDUP_OUT"]) / os.environ["RUN_TAG"]
OUT.mkdir(parents=True, exist_ok=True)
ns = common.build()
model = ns["joint_model"]
with open(os.environ["PROF_DEAD"], "rb") as fh:
    dead = pickle.load(fh)
n = len(dead["loglikelihood"])
ns["joint_posterior"] = {name: np.asarray(v).reshape((n, *np.shape(model.theta_init[name])))
                         for name, v in dead["positions"].items() if name in model.theta_init}
cell = "".join(json.loads(common.NOTEBOOK.read_text())["cells"][14]["source"])
times, compiles = {}, []
jax.monitoring.register_event_duration_secs_listener(
    lambda event, seconds, **kw: compiles.append(seconds) if event.endswith("backend_compile_duration") else None)


def timed(name, function):
    start = time.perf_counter()
    value = jax.block_until_ready(function())
    times[name] = time.perf_counter() - start
    return value


timed("cell14", lambda: exec(cell, ns))
first = {"compiles": len(compiles), "compile_s": sum(compiles)}
compiles.clear()
timed("cell14 again", lambda: exec(cell, ns))
result = {"times_s": times, "first_run": first, "second_run": {"compiles": len(compiles), "compile_s": sum(compiles)}}
(OUT / "cell14.json").write_text(json.dumps(result, indent=1))
print(json.dumps(result, indent=1))
