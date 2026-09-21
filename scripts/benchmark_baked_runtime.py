#!/usr/bin/env python3
"""Time the production joint likelihood with ``Spectrum(baked_runtime=False)``
against ``baked_runtime=True`` in one process (same boot, same device), with
z and sigma_star free, and compare their log-likelihoods on prior draws.

The model and likelihood come from the cells of
``notebooks/ceridwen_integrated_photometry_spectra.ipynb``. The fixed z and
sigma_star model is timed beside them as the reference cost.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import tempfile
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
ARMS = {  # label: (free z and sigma_star, baked_runtime)
    "fixed": (False, False),
    "free_current": (True, False),
    "free_baked": (True, True),
}


def build(free: bool, baked: bool) -> dict:
    """Run the settings, data, observation, model and likelihood cells."""
    cells = ["".join(cell["source"]) for cell in json.loads(NOTEBOOK.read_text())["cells"]]
    namespace = {"display": lambda *args, **kwargs: None}
    exec(cells[2], namespace)
    namespace["SETTINGS"]["baked_runtime"] = baked
    if not free:
        namespace["PRIORS"].pop("zred")
        namespace["PRIORS"].pop("sigma_smooth")
    for index in (4, 6, 8):
        exec(cells[index], namespace)
    likelihood_lines = cells[10].split("calibration_polynomial =")[1].split("model_parameter_block_text")[0]
    exec("calibration_polynomial =" + likelihood_lines, namespace)
    namespace["plt"].close("all")
    return namespace


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="M1_210210")
    parser.add_argument("--particles", type=int, nargs="+", default=[100, 500])
    parser.add_argument("--draws", type=int, default=500, help="prior draws for the lnL comparison")
    parser.add_argument("--rounds", type=int, default=30, help="interleaved timing rounds")
    parser.add_argument("--repeats", type=int, default=20, help="timed calls per arm per round")
    parser.add_argument("--seed", type=int, default=20260921)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    os.environ["MPLBACKEND"] = "Agg"
    os.environ["CERIDWEN_TARGET_ID"] = args.target
    os.environ["CERIDWEN_RESULT_DIR"] = tempfile.mkdtemp()

    import jax
    import jax.numpy as jnp
    import numpy as np
    from benchmark_ceridwen_vast import _make_log_functions

    device = jax.devices()[0]
    count = max(args.draws, *args.particles)
    batched, points = {}, {}
    for label, (free, baked) in ARMS.items():
        namespace = build(free, baked)
        model = namespace["joint_model"]
        loglike, _ = _make_log_functions(model, namespace["joint_likelihood"])
        batched[label] = jax.jit(jax.vmap(loglike))
        key = jax.random.PRNGKey(args.seed)
        points[label] = {
            name: jnp.asarray(
                model.priors[name].sample(jax.random.fold_in(key, index), (count, *np.shape(template)))
            ).reshape((count, *np.shape(template)))
            for index, (name, template) in enumerate(model.theta_init.items())
        }

    # Log-likelihood of the two free paths on the same prior draws.
    draws = {name: value[: args.draws] for name, value in points["free_current"].items()}
    current = np.asarray(batched["free_current"](draws))
    baked = np.asarray(batched["free_baked"](draws))
    difference = np.abs(baked - current)
    lnl = {
        "draws": args.draws,
        "finite": bool(np.isfinite(current).all() and np.isfinite(baked).all()),
        "lnl_min": float(current.min()),
        "lnl_max": float(current.max()),
        "max_abs_dlnl": float(difference.max()),
        "max_rel_dlnl": float((difference / np.abs(current)).max()),
        # tolerance of ceridwen/tests/test_baked_runtime.py
        "within_test_tolerance": bool(np.allclose(baked, current, rtol=1e-9, atol=1e-5)),
    }
    print(json.dumps(lnl), flush=True)

    # Interleaved rounds: every arm is timed inside every round, so a change in
    # the load of the host moves all arms of that round together.
    rounds = []
    for particles in args.particles:
        batch = {label: {name: value[:particles] for name, value in points[label].items()} for label in ARMS}
        for label in ARMS:
            batched[label](batch[label]).block_until_ready()
        for index in range(args.rounds):
            row = {"particles": particles, "round": index}
            for label in ARMS:
                samples = []
                for _ in range(args.repeats):
                    started = time.perf_counter()
                    batched[label](batch[label]).block_until_ready()
                    samples.append(time.perf_counter() - started)
                row[label] = 1e6 * statistics.median(samples) / particles
            row["speedup"] = row["free_current"] / row["free_baked"]
            rounds.append(row)
            print(json.dumps(row), flush=True)

    summary = []
    for particles in args.particles:
        rows = [row for row in rounds if row["particles"] == particles]
        entry = {"particles": particles}
        for label in ARMS:
            entry[f"{label}_us_per_call"] = statistics.median(row[label] for row in rows)
        speedups = [row["speedup"] for row in rows]
        entry.update(speedup_median=statistics.median(speedups), speedup_min=min(speedups),
                     speedup_max=max(speedups))
        summary.append(entry)
        print(json.dumps(entry), flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "target": args.target,
        "device": str(device),
        "device_kind": device.device_kind,
        "jax": jax.__version__,
        "x64": bool(jax.config.jax_enable_x64),
        "xla_flags": os.environ.get("XLA_FLAGS", ""),
        "seed": args.seed,
        "rounds_per_arm": args.rounds,
        "repeats_per_round": args.repeats,
        "log_likelihood": lnl,
        "summary": summary,
        "rounds": rounds,
    }, indent=1))
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
