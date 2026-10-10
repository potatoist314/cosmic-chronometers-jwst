#!/usr/bin/env python3
"""Merge equivalence: the production notebook's model at fixed posterior points.

The model is built by executing the production notebook's own cells (settings,
data, observations, model, likelihood); nothing here builds a model.  Each run
evaluates every (configuration, target, point) under one ceridwen checkout on
CPU in float64 and saves lnL and the model outputs.  ``compare`` diffs two runs;
``timing`` times the jitted batched lnL of two checkouts in interleaved rounds.

  points   draw the points from the ten-galaxy run (max-likelihood row + 20 draws)
  run      evaluate all points under one ceridwen checkout
  compare  per configuration and target: max |dlnL|, max relative output difference
  timing   interleaved CPU timing, reference vs candidate checkout
  verify   run + compare against the reference run + timing, for one checkout
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

PROJECT = Path("/Users/liuhao/Downloads/Astro project")
HERE = Path(__file__).resolve().parent
SEDPY_JAX = PROJECT / "external/sedpy_jax"
FIT_ROOT = PROJECT / "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit"
# The notebook the ten-galaxy run executed (parent a6fba80, ceridwen 2d5edc9).
NOTEBOOK = "a6fba80:notebooks/ceridwen_integrated_photometry_spectra.ipynb"
TARGETS = ("M1_210210", "M8_150848", "M5_238314", "M3_120308", "M2_134021",
           "M7_146213", "M3_117010", "M4_107370", "M14_37219", "M8_161113")
MANIFEST_INDEX = {"M1_210210": 2, "M8_150848": 14, "M5_238314": 35, "M3_120308": 61,
                  "M2_134021": 74, "M7_146213": 106, "M3_117010": 114, "M4_107370": 117,
                  "M14_37219": 129, "M8_161113": 145}
RUN_SEED = 20260832  # every target of the ten-galaxy run
POINT_SEED = 20261010
N_DRAWS = 20
ZRED_OFFSET_KMS = 200.0  # free_z: zred = z_cat + U(-200, 200) km/s, first point at z_cat
TIMING_SEED = 20261011
# Configuration -> edits applied to the notebook's SETTINGS (and PRIORS) before the data cell.
CONFIGS = {
    "production": {},
    "elines_off": {"emission_line_marginalisation": False, "_fixed_z": True},
    "zevo_off": {"metallicity_evolution": False},
    "afe_grid": {"ssp_grid": "~/.ceridwen/grids/amist_c3k_hr_krou_afe.h5"},
    "free_z": {"emission_line_marginalisation": False},
    "baked_off": {"baked_runtime": False},
    "cal_order0": {"calibration_order": 0},
}
OUTPUTS = ("spectrum", "photometry", "spectrum_calibrated", "calibration_polynomial",
           "calibration_coeffs", "line_fluxes", "photometry_with_lines")


def git(path, *args):
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def target_dir(target):
    return next(FIT_ROOT.glob(f"*-{target}"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# --------------------------------------------------------------------------- points
def cmd_points(args):
    import h5py
    from scipy.special import softmax
    out = Path(args.out)
    with h5py.File(out, "w") as dst:
        dst.attrs.update(seed=POINT_SEED, n_draws=N_DRAWS, zred_offset_kms=ZRED_OFFSET_KMS,
                         rule="row 0: argmax log_likelihoods; rows 1-20: "
                              "default_rng(seed).choice(n, 20, p=softmax(log_weights)); "
                              "zred_offset_kms: row 0 zero, rows 1-20 uniform(-200, 200)")
        for target in TARGETS:
            path = target_dir(target) / "ceridwen_result.h5"
            rng = np.random.default_rng(POINT_SEED)
            with h5py.File(path, "r") as src:
                samples = src["samples"]
                loglike = samples["log_likelihoods"][:]
                weights = softmax(samples["log_weights"][:])
                rows = np.concatenate([[int(np.argmax(loglike))],
                                       rng.choice(len(weights), N_DRAWS, p=weights)])
                offsets = np.concatenate([[0.0], rng.uniform(-ZRED_OFFSET_KMS, ZRED_OFFSET_KMS,
                                                             N_DRAWS)])
                group = dst.create_group(target)
                for name in src["model/param_names"][:]:
                    name = name.decode() if isinstance(name, bytes) else name
                    group[name] = samples[name][:][rows]
                group["rows"] = rows
                group["stored_log_likelihood"] = loglike[rows]
                group["zred_offset_kms"] = offsets
                group.attrs.update(source=str(path), source_sha256=sha256(path),
                                   zred=float(src["model"].attrs["zred"]))
    print(out)


def load_points(path, target):
    import h5py
    with h5py.File(path, "r") as f:
        g = f[target]
        return {k: g[k][:] for k in g}, dict(g.attrs)


# --------------------------------------------------------------------------- notebook
def notebook_cells(spec):
    if Path(spec).exists():
        text, origin = Path(spec).read_text(), f"{spec} sha256 {sha256(spec)}"
    else:
        rev, path = spec.split(":", 1)
        text = git(PROJECT, "show", f"{rev}:{path}")
        origin = f"{git(PROJECT, 'rev-parse', rev)}:{path}"
    cells = ["".join(c["source"]) for c in json.loads(text)["cells"] if c["cell_type"] == "code"]

    def cell(marker):
        return next(c for c in cells if marker in c)
    return dict(settings=cell("SETTINGS = {"), data=cell("legac = Table.read("),
                observations=cell("spectrum_obs = Spectrum("),
                model=cell("joint_csp = CSPBasis_afe("),
                fit=cell("calibration_polynomial =")), origin


def run_cell(source, env, name, keep=None):
    tree = ast.parse(source)
    if keep is not None:  # only the assignments to these names
        tree.body = [n for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id in keep for t in n.targets)]
    exec(compile(tree, name, "exec"), env)


def build(cells, config, target, scratch):
    """Execute the notebook cells for one configuration and target; return its namespace."""
    os.environ.update(CERIDWEN_TARGET_ID=target, CERIDWEN_MANIFEST_INDEX=str(MANIFEST_INDEX[target]),
                      CERIDWEN_RANDOM_SEED=str(RUN_SEED), CERIDWEN_PLOTS="0",
                      CERIDWEN_RESULT_DIR=str(scratch), CERIDWEN_NOTEBOOK_QUICK="0")
    env = {"__name__": "__notebook__"}
    run_cell(cells["settings"], env, "settings")
    edits = dict(CONFIGS[config])
    if edits.pop("_fixed_z", False):
        env["PRIORS"].pop("zred")
    env["SETTINGS"].update(edits)
    for name in ("data", "observations", "model"):
        run_cell(cells[name], env, name)
    run_cell(cells["fit"], env, "fit", keep={"calibration_polynomial", "joint_likelihood"})
    return env


RENAME = {}  # candidate parameter name -> point name, from --rename point=candidate


def batch_for(env, points, offsets):
    import jax.numpy as jnp
    model, n = env["joint_model"], len(offsets)
    batch = {}
    for name, template in model.theta_init.items():
        if name == "zred":
            values = env["z_catalog"] + offsets * (1.0 + env["z_catalog"]) / env["C_KMS"]
        else:
            values = points[RENAME.get(name, name)]
        batch[name] = jnp.asarray(values, dtype=jnp.float64).reshape((n,) + np.shape(template))
    return batch


def loglike_of(env):
    """The likelihood the sampler sees: run_sampler's own loglike_fn."""
    import jax
    from types import SimpleNamespace
    capture = SimpleNamespace(run=lambda loglike, logprior, theta, key: loglike)
    return env["run_sampler"](env["joint_model"], env["joint_likelihood"], capture,
                              jax.random.PRNGKey(0))


def outputs_of(env):
    """Model outputs at theta: uncalibrated spectrum and photometry, the calibration
    polynomial at its conditional optimum, the line fluxes and the calibrated model,
    from the same calibration calls the likelihood makes."""
    import jax.numpy as jnp
    model, likelihood = env["joint_model"], env["joint_likelihood"]
    lh = dict(zip(likelihood.keys, likelihood.likelihoods))
    spec, phot = model.obs_dict["spectrum"], model.obs_dict["photometry"]

    def pieces(theta):
        pred = model.predict(theta)
        mu, mu_p = pred["spectrum"], pred["photometry"]
        s = lh["spectrum"]
        noise = s.noise_model.compute(spec.uncertainty, mu, spec.mask, theta, data=spec.flux)
        sigma = jnp.sqrt(1.0 / noise.inv_var)
        lines = s.emission_lines
        if lines is None:
            mu_cal, coeffs, _ = s.calibration.calibrate(spec.flux, mu, sigma, spec.mask)
            fluxes, mu_pl = jnp.zeros(0), mu_p
        else:
            p = lh[lines.photometry_key]
            noise_p = p.noise_model.compute(phot.uncertainty, mu_p, phot.mask, theta,
                                            data=phot.flux)
            band = jnp.asarray(lines.band_matrix)
            mu_cal, coeffs, fluxes, _ = s.calibration.calibrate_with_lines(
                spec.flux, mu, sigma, spec.mask, lines.columns(theta), lines.pairs, lines.ridge,
                (band, phot.flux, mu_p, jnp.sqrt(1.0 / noise_p.inv_var), phot.mask))
            mu_pl = mu_p + band @ fluxes
        return dict(spectrum=mu, photometry=mu_p, spectrum_calibrated=mu_cal,
                    calibration_polynomial=s.calibration.polynomial(coeffs),
                    calibration_coeffs=coeffs, line_fluxes=fluxes, photometry_with_lines=mu_pl)
    return pieces


def describe(env):
    model = env["joint_model"]
    obs = {k: hashlib.sha256(b"".join(np.ascontiguousarray(np.asarray(getattr(o, a))).tobytes()
                                       for a in ("flux", "uncertainty", "mask"))).hexdigest()
           for k, o in model.obs_dict.items()}
    lines = env.get("emission_line_columns")
    return dict(observations_sha256=obs, param_names=list(model.theta_init),
                line_names=[] if lines is None else list(lines.free_names),
                sfh_basis_fastpath=getattr(env["joint_csp"], "sfh_basis_fastpath", None),
                n_spectrum_fitted=int(np.sum(np.asarray(model.obs_dict["spectrum"].mask))),
                settings={k: v for k, v in env["SETTINGS"].items() if k not in ("sampler", "sampler_quick")},
                priors=sorted(model.priors))


def checkout_info(path):
    import ceridwen
    import sedpy_jax
    return dict(ceridwen=str(path), commit=git(path, "rev-parse", "HEAD"),
                dirty=bool(git(path, "status", "--porcelain", "--untracked-files=no")),
                ceridwen_file=ceridwen.__file__, sedpy_jax_file=sedpy_jax.__file__,
                sedpy_jax_commit=git(SEDPY_JAX, "rev-parse", "HEAD"))


def rename_map(text):
    """'Z=logzsol,sigma_smooth=sigma' -> {'logzsol': 'Z', 'sigma': 'sigma_smooth'}"""
    return {new: old for old, new in (item.split("=") for item in (text or "").split(",") if item)}


def worker_env(ceridwen):
    env = dict(os.environ, JAX_PLATFORMS="cpu", JAX_ENABLE_X64="1", MPLBACKEND="Agg",
               PYTHONPATH=os.pathsep.join([str(ceridwen), str(SEDPY_JAX)]))
    env.pop("CERIDWEN_TARGET_ID", None)
    return env


# --------------------------------------------------------------------------- run
def cmd_worker(args):
    """One process, one checkout: evaluate the listed (configuration, target) jobs."""
    RENAME.update(rename_map(args.rename))
    import jax
    import traceback
    import warnings
    from astropy.units import UnitsWarning
    warnings.simplefilter("ignore", UnitsWarning)
    jax.config.update("jax_enable_x64", True)
    out, ceridwen = Path(args.out), Path(args.ceridwen).resolve()
    info = checkout_info(ceridwen)
    assert Path(info["ceridwen_file"]).is_relative_to(ceridwen), info
    cells, origin = notebook_cells(args.notebook)
    os.chdir(PROJECT)
    for job in args.jobs.split(","):
        config, target = job.split(":")
        dest = out / config
        dest.mkdir(parents=True, exist_ok=True)
        meta = dict(config=config, target=target, notebook=origin, **info)
        started = time.perf_counter()
        try:
            env = build(cells, config, target, out / "scratch" / f"{config}-{target}")
            meta.update(describe(env), build_s=time.perf_counter() - started)
            points, attrs = load_points(args.points, target)
            batch = batch_for(env, points, points["zred_offset_kms"])
            loglike, pieces = loglike_of(env), outputs_of(env)
            t0 = time.perf_counter()
            lnl = np.asarray(jax.block_until_ready(jax.jit(jax.vmap(loglike))(batch)))
            meta["lnl_s"] = time.perf_counter() - t0
            t0 = time.perf_counter()
            result = jax.device_get(jax.jit(jax.vmap(pieces))(batch))
            meta["outputs_s"] = time.perf_counter() - t0
            # Rounding floor of this code: the same points through a second
            # compilation (one point per call instead of the batch).
            single_lnl, single_pieces = jax.jit(loglike), jax.jit(pieces)
            point = [jax.tree.map(lambda x: x[i], batch) for i in range(len(lnl))]
            lnl_single = np.array([float(single_lnl(t)) for t in point])
            single = jax.device_get([single_pieces(t) for t in point])
            meta["floor_abs_dlnl"] = float(np.max(np.abs(lnl - lnl_single)))
            meta["floor_rel"] = {k: rel_diff(result[k], np.stack([s[k] for s in single]))
                                 for k in OUTPUTS}
            np.savez_compressed(dest / f"{target}.npz", lnl=lnl, **result,
                                **{f"theta_{k}": np.asarray(v) for k, v in batch.items()})
            meta.update(status="ok", stored_log_likelihood=points["stored_log_likelihood"].tolist(),
                        lnl=lnl.tolist())
        except Exception as error:  # a configuration this checkout cannot build
            meta.update(status="unavailable", error=f"{type(error).__name__}: {error}",
                        traceback=traceback.format_exc())
        (dest / f"{target}.json").write_text(json.dumps(meta, indent=1, default=str) + "\n")
        print(job, meta["status"], f"{time.perf_counter() - started:.1f}s",
              meta.get("error", ""), flush=True)


def cmd_run(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    configs = args.configs.split(",") if args.configs else list(CONFIGS)
    targets = args.targets.split(",") if args.targets else list(TARGETS)
    jobs = [f"{c}:{t}" for c in configs for t in targets]
    shards = [jobs[i::args.jobs] for i in range(args.jobs)]
    record = out / "commands.txt"
    with record.open("a") as f:
        f.write(f"# {time.strftime('%Y-%m-%d %H:%M:%S')}\n{shlex.join([sys.executable, *sys.argv])}\n")
    procs = []
    for i, shard in enumerate(s for s in shards if s):
        cmd = [sys.executable, str(Path(__file__).resolve()), "worker", "--ceridwen", args.ceridwen,
               "--out", str(out), "--notebook", args.notebook, "--points", args.points,
               "--jobs", ",".join(shard), "--rename", args.rename or ""]
        with record.open("a") as f:
            f.write("  worker: JAX_PLATFORMS=cpu JAX_ENABLE_X64=1 PYTHONPATH="
                    f"{shlex.quote(worker_env(args.ceridwen)['PYTHONPATH'])} {shlex.join(cmd)}\n")
        log = (out / f"worker-{i}.log").open("a")
        procs.append(subprocess.Popen(cmd, env=worker_env(args.ceridwen), stdout=log,
                                      stderr=subprocess.STDOUT, cwd=PROJECT))
    codes = [p.wait() for p in procs]
    print(out, "worker exit codes", codes)
    return max(codes)


# --------------------------------------------------------------------------- compare
def rel_diff(a, b):
    """max |a - b| / max |a| per point (row), then the max over points; 0 when both are 0."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape:
        return float("inf")
    if a.size == 0:
        return 0.0
    a2, b2 = a.reshape(len(a), -1), b.reshape(len(b), -1)
    num = np.max(np.abs(a2 - b2), axis=1)
    den = np.max(np.abs(a2), axis=1)
    return float(np.max(np.where(num == 0, 0.0, num / np.where(den == 0, np.inf, den))))


def compare_runs(ref, cand):
    rows = []
    for config in CONFIGS:
        for target in TARGETS:
            row = dict(config=config, target=target)
            mr, mc = (Path(d) / config / f"{target}.json" for d in (ref, cand))
            if not mr.exists() or not mc.exists():
                row["status"] = "missing"
                rows.append(row)
                continue
            mr, mc = json.loads(mr.read_text()), json.loads(mc.read_text())
            if mr["status"] != "ok" or mc["status"] != "ok":
                row["status"] = "unavailable"
                row["error"] = mc.get("error") or mr.get("error")
                rows.append(row)
                continue
            a = np.load(Path(ref) / config / f"{target}.npz")
            b = np.load(Path(cand) / config / f"{target}.npz")
            row.update(status="ok", max_abs_dlnl=float(np.max(np.abs(a["lnl"] - b["lnl"]))),
                       lnl_ref_max=float(np.max(a["lnl"])),
                       same_observations=mr["observations_sha256"] == mc["observations_sha256"],
                       same_lines=mr["line_names"] == mc["line_names"],
                       fastpath=mc["sfh_basis_fastpath"],
                       **{f"rel_{k}": rel_diff(a[k], b[k]) for k in OUTPUTS})
            # Rounding floor: the larger of the two runs' batch-versus-single differences.
            row["floor_abs_dlnl"] = max(mr["floor_abs_dlnl"], mc["floor_abs_dlnl"])
            row["floor_rel"] = {k: max(mr["floor_rel"][k], mc["floor_rel"][k]) for k in OUTPUTS}
            row["verdict"] = classify(row)
            rows.append(row)
    return rows


ROUNDING_FACTOR = 10.0


def classify(row):
    """bitwise: every difference is 0.  rounding: every difference is at most
    ROUNDING_FACTOR times the floor of that quantity (lnL, or an output; a zero floor
    allows 1e-12 relative).  differs: anything else."""
    diffs = [row["max_abs_dlnl"]] + [row[f"rel_{k}"] for k in OUTPUTS]
    if not any(diffs) and row["same_observations"] and row["same_lines"]:
        return "bitwise"
    within = row["max_abs_dlnl"] <= ROUNDING_FACTOR * max(row["floor_abs_dlnl"], 1e-8) and all(
        row[f"rel_{k}"] <= ROUNDING_FACTOR * max(row["floor_rel"][k], 1e-12) for k in OUTPUTS)
    return "rounding" if within and row["same_observations"] and row["same_lines"] else "differs"


def table(rows):
    keys = ["max_abs_dlnl"] + [f"rel_{k}" for k in OUTPUTS]
    head = ["config", "target", "verdict", "max abs dlnL", "lnL floor",
            *[k.replace("_", " ") for k in OUTPUTS], "same obs/lines", "fast path"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        if r["status"] != "ok":
            lines.append(f"| {r['config']} | {r['target']} | {r['status']}: "
                         f"{(r.get('error') or '')[:120]} |" + " |" * (len(head) - 3))
            continue
        lines.append("| " + " | ".join([r["config"], r["target"], r["verdict"], f"{r['max_abs_dlnl']:.2e}",
                                        f"{r['floor_abs_dlnl']:.2e}", *[f"{r[k]:.2e}" for k in keys[1:]],
                                        f"{r['same_observations']}/{r['same_lines']}",
                                        str(r["fastpath"])]) + " |")
    return "\n".join(lines)


def summary(rows):
    lines = ["| config | targets run | verdicts | max abs dlnL | max lnL floor | "
             "max rel output diff (output) |", "|---|---|---|---|---|---|"]
    for config in CONFIGS:
        ok = [r for r in rows if r["config"] == config and r["status"] == "ok"]
        if not ok:
            why = next((r.get("error") or r["status"] for r in rows if r["config"] == config), "")
            lines.append(f"| {config} | 0/{len(TARGETS)} | not run: {why[:100]} | - | - | - |")
            continue
        worst = max(((r[f"rel_{k}"], k) for r in ok for k in OUTPUTS))
        counts = {v: sum(r["verdict"] == v for r in ok) for v in ("bitwise", "rounding", "differs")}
        lines.append(f"| {config} | {len(ok)}/{len(TARGETS)} | "
                     + ", ".join(f"{n} {v}" for v, n in counts.items() if n)
                     + f" | {max(r['max_abs_dlnl'] for r in ok):.2e} | "
                     f"{max(r['floor_abs_dlnl'] for r in ok):.2e} | {worst[0]:.2e} ({worst[1]}) |")
    return "\n".join(lines)


def cmd_compare(args):
    rows = compare_runs(args.reference, args.candidate)
    if args.json:
        Path(args.json).write_text(json.dumps(rows, indent=1) + "\n")
    print(summary(rows))
    print()
    print(table(rows))


# --------------------------------------------------------------------------- timing
def cmd_timing_worker(args):
    """Compile the batched lnL once; then time ``n`` calls per stdin line."""
    RENAME.update(rename_map(args.rename))
    import h5py
    import jax
    from scipy.special import softmax
    jax.config.update("jax_enable_x64", True)
    protocol, sys.stdout = sys.stdout, sys.stderr  # notebook and ceridwen prints stay off the protocol
    ceridwen = Path(args.ceridwen).resolve()
    info = checkout_info(ceridwen)
    assert Path(info["ceridwen_file"]).is_relative_to(ceridwen), info
    cells, _ = notebook_cells(args.notebook)
    os.chdir(PROJECT)
    env = build(cells, args.config, args.target, Path(args.scratch))
    with h5py.File(target_dir(args.target) / "ceridwen_result.h5", "r") as f:
        s = f["samples"]
        rows = np.random.default_rng(TIMING_SEED).choice(
            len(s["log_weights"]), args.batch, p=softmax(s["log_weights"][:]))
        points = {RENAME.get(k, k): s[RENAME.get(k, k)][:][rows] for k in env["joint_model"].theta_init
                  if RENAME.get(k, k) in s}
    batch = batch_for(env, points, np.zeros(args.batch))
    fn = jax.jit(jax.vmap(loglike_of(env)))
    t0 = time.perf_counter()
    value = np.asarray(jax.block_until_ready(fn(batch)))
    print(json.dumps(dict(ready=True, compile_s=time.perf_counter() - t0, commit=info["commit"],
                          lnl_sum=float(value.sum()))), file=protocol, flush=True)
    for line in sys.stdin:
        times = []
        for _ in range(int(line)):
            t0 = time.perf_counter()
            jax.block_until_ready(fn(batch))
            times.append(time.perf_counter() - t0)
        print(json.dumps(times), file=protocol, flush=True)


def timing(reference, candidate, notebooks, config, target, batch, rounds, calls, scratch, rename=""):
    procs = {}
    for label, ceridwen, notebook, names in (("reference", reference, notebooks[0], ""),
                                             ("candidate", candidate, notebooks[1], rename)):
        cmd = [sys.executable, str(Path(__file__).resolve()), "timing-worker", "--ceridwen", ceridwen,
               "--notebook", notebook, "--config", config, "--target", target, "--rename", names,
               "--batch", str(batch), "--scratch", str(Path(scratch) / label)]
        procs[label] = subprocess.Popen(cmd, env=worker_env(ceridwen), stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, text=True, cwd=PROJECT)
    ready = {k: json.loads(p.stdout.readline()) for k, p in procs.items()}
    times = {k: [] for k in procs}
    for r in range(rounds):  # alternate the order every round
        for label in (("reference", "candidate") if r % 2 == 0 else ("candidate", "reference")):
            procs[label].stdin.write(f"{calls}\n")
            procs[label].stdin.flush()
            times[label] += json.loads(procs[label].stdout.readline())
    for p in procs.values():
        p.stdin.close()
        p.wait()
    med = {k: float(np.median(v)) for k, v in times.items()}
    return dict(config=config, target=target, batch=batch, rounds=rounds, calls_per_round=calls,
                ready=ready, median_s=med, ratio_candidate_over_reference=med["candidate"] / med["reference"],
                quartiles_s={k: np.percentile(v, [25, 75]).tolist() for k, v in times.items()},
                times_s=times)


def cmd_timing(args):
    result = timing(args.reference, args.candidate, (args.notebook, args.candidate_notebook or args.notebook),
                    args.config, args.target, args.batch, args.rounds, args.calls, args.scratch,
                    args.rename or "")
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "times_s"}, indent=1))


# --------------------------------------------------------------------------- verify
REFERENCE_CERIDWEN = HERE.parent / "wt-equiv-2d5edc9"
REFERENCE_RUN = HERE / "runs/reference-2d5edc9"


def cmd_verify(args):
    """Run every point under a checkout, compare with the reference run, time the
    production lnL against the reference checkout, and write the verdict section."""
    out = HERE / "runs" / args.label
    reference_run, reference_ceridwen = Path(args.reference_run), Path(args.reference_ceridwen)
    if not args.skip_run:
        cmd_run(argparse.Namespace(ceridwen=args.ceridwen, out=str(out), notebook=args.notebook,
                                   points=str(HERE / "points.h5"), configs=None, targets=None,
                                   jobs=args.jobs, rename=args.rename))
    rows = compare_runs(reference_run, out)
    (out / "compare.json").write_text(json.dumps(rows, indent=1) + "\n")
    meta = next(json.loads(f.read_text()) for f in sorted(out.glob("*/*.json")))
    timed = None
    if args.timing and any(r["status"] == "ok" and r["config"] == "production" for r in rows):
        timed = timing(str(reference_ceridwen), args.ceridwen, (NOTEBOOK, args.notebook), "production",
                       "M1_210210", 128, 20, 5, out / "scratch-timing", args.rename or "")
        (out / "timing.json").write_text(json.dumps(timed, indent=1) + "\n")
    text = [f"## {args.label}: ceridwen {meta['commit'][:12]}"
            + (" (uncommitted changes)" if meta["dirty"] else "") + f", {time.strftime('%Y-%m-%d %H:%M')}",
            "", f"- Checkout: `{meta['ceridwen']}`; notebook `{meta['notebook']}`",
            f"- Run: `runs/{args.label}/` (commands.txt); reference `runs/{reference_run.name}/`",
            f"- Command: `{shlex.join(['python', 'harness.py', *sys.argv[1:]])}`"]
    if timed:
        text.append(f"- CPU timing, production lnL, M1_210210, batch 128, {timed['rounds']} interleaved rounds "
                    f"x {timed['calls_per_round']} calls: reference {timed['median_s']['reference']*1e3:.1f} ms, "
                    f"candidate {timed['median_s']['candidate']*1e3:.1f} ms per batch; "
                    f"ratio candidate/reference {timed['ratio_candidate_over_reference']:.3f}")
    else:
        text.append("- CPU timing: not run (production configuration unavailable on this checkout)")
    text += ["", summary(rows), "", "<details><summary>Per target</summary>", "", table(rows), "",
             "</details>", ""]
    (out / "verdict-section.md").write_text("\n".join(text))
    print("\n".join(text))


# --------------------------------------------------------------------------- cli
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("points")
    s.add_argument("--out", default=str(HERE / "points.h5"))
    for name in ("run", "worker"):
        s = sub.add_parser(name)
        s.add_argument("--ceridwen", required=True)
        s.add_argument("--out", required=True)
        s.add_argument("--notebook", default=NOTEBOOK)
        s.add_argument("--points", default=str(HERE / "points.h5"))
        s.add_argument("--rename", help="point=candidate parameter names, comma separated")
        if name == "run":
            s.add_argument("--configs")
            s.add_argument("--targets")
            s.add_argument("--jobs", type=int, default=3)
        else:
            s.add_argument("--jobs", required=True)
    s = sub.add_parser("compare")
    s.add_argument("--reference", required=True)
    s.add_argument("--candidate", required=True)
    s.add_argument("--json")
    for name in ("timing", "timing-worker"):
        s = sub.add_parser(name)
        s.add_argument("--notebook", default=NOTEBOOK)
        s.add_argument("--config", default="production")
        s.add_argument("--target", default="M1_210210")
        s.add_argument("--batch", type=int, default=128)
        s.add_argument("--rename", help="point=candidate parameter names (candidate side)")
        if name == "timing":
            s.add_argument("--reference", required=True)
            s.add_argument("--candidate", required=True)
            s.add_argument("--candidate-notebook")
            s.add_argument("--rounds", type=int, default=20)
            s.add_argument("--calls", type=int, default=5)
            s.add_argument("--scratch", default=str(HERE / "scratch-timing"))
            s.add_argument("--json")
        else:
            s.add_argument("--ceridwen", required=True)
            s.add_argument("--scratch", required=True)
    s = sub.add_parser("verify")
    s.add_argument("--ceridwen", required=True)
    s.add_argument("--label", required=True)
    s.add_argument("--notebook", default=NOTEBOOK)
    s.add_argument("--jobs", type=int, default=3)
    s.add_argument("--reference-run", default=str(REFERENCE_RUN))
    s.add_argument("--reference-ceridwen", default=str(REFERENCE_CERIDWEN))
    s.add_argument("--skip-run", action="store_true")
    s.add_argument("--rename", help="point=candidate parameter names, comma separated")
    s.add_argument("--timing", action=argparse.BooleanOptionalAction, default=True)
    args = p.parse_args()
    return {"points": cmd_points, "run": cmd_run, "worker": cmd_worker, "compare": cmd_compare,
            "timing": cmd_timing, "timing-worker": cmd_timing_worker,
            "verify": cmd_verify}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
