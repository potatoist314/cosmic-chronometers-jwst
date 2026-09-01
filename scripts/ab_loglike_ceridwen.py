#!/usr/bin/env python3
"""Fixed-theta A/B report for the joint M1_210210 log-likelihood.

Evaluates the production likelihood at 64 fixed prior draws on CPU and
records the values next to the compiled cost ledger. Run once per ceridwen
revision; diff two reports to prove an optimisation is numerically
equivalent and cheaper. Baseline against patched is two runs of this script
in two processes, one with PYTHONPATH pointing at a git worktree of the
baseline ceridwen commit.

Usage:
    JAX_PLATFORMS=cpu JAX_ENABLE_X64=1 python scripts/ab_loglike_ceridwen.py out.json
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

NUM_SAMPLES = 64
SEED = 20260901
VMAP_WIDTH = 25


def main() -> int:
    out_path = Path(sys.argv[1])

    import jax
    import numpy as np

    import ceridwen
    from benchmark_ceridwen_vast import build_joint_workload, _make_log_functions

    workload = build_joint_workload(PROJECT_ROOT)
    loglike_fn, _ = _make_log_functions(workload.model, workload.likelihood)

    model = workload.model
    key = jax.random.PRNGKey(SEED)
    theta = {}
    for name, initial_value in model.theta_init.items():
        key, subkey = jax.random.split(key)
        theta[name] = model.priors[name].sample(
            subkey, shape=(NUM_SAMPLES, *initial_value.shape)
        )

    lnl = np.asarray(jax.vmap(loglike_fn)(theta))

    theta_batch = {k: v[:VMAP_WIDTH] for k, v in theta.items()}
    batched = jax.jit(jax.vmap(loglike_fn))
    compiled = batched.lower(theta_batch).compile()
    cost = {
        k: float(v)
        for k, v in (compiled.cost_analysis() or {}).items()
        if isinstance(v, (int, float))
    }
    hlo = compiled.as_text()

    start = time.perf_counter()
    for _ in range(10):
        jax.block_until_ready(batched(theta_batch))
    wall_per_batch = (time.perf_counter() - start) / 10

    ceridwen_rev = subprocess.run(
        ["git", "-C", str(Path(ceridwen.__file__).resolve().parents[1]),
         "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=False,
    ).stdout.strip() or None

    report = {
        "schema_version": 1,
        "seed": SEED,
        "num_samples": NUM_SAMPLES,
        "vmap_width": VMAP_WIDTH,
        "ceridwen_rev": ceridwen_rev,
        "ceridwen_path": str(Path(ceridwen.__file__).resolve().parent),
        "jax": jax.__version__,
        "lnl": lnl.tolist(),
        "cost_analysis": cost,
        "kernel_count_fusions": hlo.count(" fusion("),
        "cpu_wall_per_vmap25_call_s": wall_per_batch,
    }
    out_path.write_text(json.dumps(report, indent=2))
    print(f"saved: {out_path}")
    print(
        f"rev={ceridwen_rev} fusions={report['kernel_count_fusions']} "
        f"flops={cost.get('flops')} bytes={cost.get('bytes accessed')} "
        f"transcendentals={cost.get('transcendentals')} "
        f"wall/batch={wall_per_batch*1e3:.2f} ms"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
