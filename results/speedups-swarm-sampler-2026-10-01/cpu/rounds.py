"""New lane kernel vs the kernel at HEAD on production live sets: bitwise equality and batch count (CPU)."""
import os, sys, pickle, time, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prod as common
import jax, jax.numpy as jnp, numpy as np
from functools import partial
import ceridwen.sampler.nested as new_mod
_lane = new_mod.lane_update
new_mod.lane_update = partial(_lane, free_moves=int(os.environ.get("FREE_MOVES", "8")),
                              lookahead=int(os.environ.get("LOOKAHEAD", "4")))
spec = importlib.util.spec_from_file_location("ceridwen.sampler.nested_base", os.environ["BASE_NESTED"])
base_mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(base_mod)
print("new", new_mod.__file__, "\nbase", base_mod.__file__, flush=True)

ns = common.build()
model, likelihood = ns["joint_model"], ns["joint_likelihood"]
loglike, logprior, _ = common.log_functions(model, likelihood)
S = ns["SETTINGS"]["sampler"]; DELETE, INNER = S["num_delete"], S["num_inner_steps"]
dead = pickle.load(open(common.DEAD, "rb"))
logl = np.asarray(dead["loglikelihood"]); birth = np.asarray(dead["loglikelihood_birth"])
pos = {k: np.asarray(v) for k, v in dead["positions"].items() if k in model.theta_init}
def live_set(k):
    alive = np.arange(len(logl)) >= DELETE * k
    if k > 0:
        alive &= ~(birth > logl[DELETE * (k - 1):DELETE * k].max())
    return np.flatnonzero(alive)

calls = [0]
def count(*_):
    calls[0] += 1
def counted(theta):
    jax.debug.callback(count)
    return loglike(theta)

def sampler(mod, ll):
    ad = mod.BlackJAXNestedSamplerAdapter({}, verbose=False, slice_kernel="lanes")
    return ad._build_nested_sampler(ll, logprior, INNER, DELETE)
new_s, base_s, cnt_s = sampler(new_mod, loglike), sampler(base_mod, loglike), sampler(new_mod, counted)
init = jax.jit(new_s.init)
steps = {"new": jax.jit(new_s.step), "base": jax.jit(base_s.step), "count": jax.jit(cnt_s.step)}
out = {}
for k in [int(x) for x in os.environ.get("ITERS", "20,80,140").split(",")]:
    idx = live_set(k); assert len(idx) == 500
    live = init({n: jnp.asarray(v[idx]).reshape((500, *np.shape(model.theta_init[n]))) for n, v in pos.items()})
    key = jax.random.PRNGKey(3000 + k)
    res, secs = {}, {}
    for name in os.environ.get("ARMS", "base,new,count").split(","):
        calls[0] = 0
        t = time.perf_counter(); r = steps[name](key, live); jax.block_until_ready(r); secs[name] = time.perf_counter() - t
        res[name] = r
    info = res["base"][1].update_info
    per_lane = (np.asarray(info.num_expansions) + np.asarray(info.num_shrink) + 2).sum(1)
    same = all(np.array_equal(np.asarray(a), np.asarray(b), equal_nan=True)
               for a, b in zip(jax.tree.leaves(res["base"]), jax.tree.leaves(res["new"])))
    rec = dict(bitwise=same, base_rounds=int(per_lane.max()), base_mean=float(per_lane.mean()),
               new_rounds=calls[0] / DELETE, secs={n: round(v, 1) for n, v in secs.items()})
    print(k, rec, flush=True); out[k] = rec
    json.dump(out, open(os.environ["OUT"], "w"))
