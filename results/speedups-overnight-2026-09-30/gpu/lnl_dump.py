"""Log-likelihood and log-prior of every dead point of a production fit, for bitwise comparison of two trees.

Env: PROF_DEAD (ns_raw_dead pickle), DUMP_OUT (.npz path), DUMP_BATCH (vmap batch, default 500).
"""
import os
import pickle

import common
import jax
import jax.numpy as jnp
import numpy as np

ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior, _ = common.log_functions(model, likelihood)
with open(os.environ["PROF_DEAD"], "rb") as fh:
    dead = pickle.load(fh)
n = len(dead["loglikelihood"])
theta = {name: np.asarray(v).reshape((n, *np.shape(model.theta_init[name])))
         for name, v in dead["positions"].items() if name in model.theta_init}
batch = int(os.environ.get("DUMP_BATCH", "500"))
fl, fp = jax.jit(jax.vmap(loglike)), jax.jit(jax.vmap(logprior))
pad = -n % batch
lnl, lnp = [], []
for start in range(0, n + pad, batch):
    chunk = {k: jnp.asarray(np.concatenate([v, v[:pad]])[start:start + batch]) for k, v in theta.items()}
    lnl.append(np.asarray(fl(chunk)))
    lnp.append(np.asarray(fp(chunk)))
np.savez(os.environ["DUMP_OUT"], loglikelihood=np.concatenate(lnl)[:n], logprior=np.concatenate(lnp)[:n],
         stored=np.asarray(dead["loglikelihood"]))
print("DONE", n, flush=True)
