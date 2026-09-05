"""Execute unchanged production fits and measure exact observation speedups.

Each arm saves the production notebook, including fit, SFH and corner plots.
The rejected wavelength proposal remains an experiment in this runner.
Numerical and timing comparisons run after the full fit, on that same model
and GPU. The retained package change is unsmoothed spectral interpolation.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = PROJECT_ROOT / "results/rtx-5060-observation-speedups"
SEEDS = (20260905, 20260906)
TARGETS = ("M1_210210", "M5_172669")


def prepare_wavelength_experiment(model):
    """Reproduce the rejected wavelength proposal without changing package defaults."""
    from copy import copy
    from inspect import getclosurevars
    import jax.numpy as jnp
    import numpy as np
    from ceridwen.observation import Photometry, Spectrum

    csp = model.csp
    assert csp.sfh_basis_fastpath and csp._losvd_kernel_fft is None and csp.igm is None
    assert "zred" not in model.param_names
    assert not {"zred", "lookback_time"}.intersection(model.transforms)
    diffuse = getattr(csp, "diff_dust", None)
    assert diffuse is None or diffuse.law_names_resolved == ["kriek_conroy"]
    required = np.zeros(csp.wave.size, dtype=bool)
    for obs in model.observations:
        if type(obs) is Spectrum:
            assert not obs.fit_sigma_smooth
            closure = getclosurevars(obs._predict_fn).nonlocals
            indices = closure.get("_idx", np.union1d(*obs._H_factors[:2]))
            required[np.asarray(indices)] = True
        else:
            assert type(obs) is Photometry and not getattr(obs, "free_z", False)
            required |= np.any(np.asarray(obs._T) != 0., axis=0)
    indices = jnp.asarray(np.flatnonzero(required))
    compact_csp = copy(csp)
    compact_csp._sfh_basis = csp._sfh_basis[..., indices]

    def compact_spectrum(theta, *, include_lines=None):
        csp._warn_unknown_theta_keys(theta)
        spectrum = compact_csp._spectrum_from_sfh_basis(theta)
        if diffuse is not None:
            attenuation = diffuse.compute_attenuation(csp.wave[indices], theta)
            spectrum *= jnp.exp(-attenuation.astype(jnp.float32))
        return jnp.zeros_like(csp.wave, dtype=jnp.float32).at[indices].set(spectrum.reshape(-1))

    compact_csp.get_spectrum = compact_spectrum
    compact_model = copy(model)
    compact_model.csp = compact_csp
    reference_predict = model.predict
    model._observation_predictor = compact_model.predict

    def selected_predict(theta):
        if model._observation_predictor is None:
            return reference_predict(theta)
        return model._observation_predictor(theta)

    model.predict = selected_predict
    return model._observation_predictor


def validate(model, likelihood, posterior, predictor, output):
    import importlib.metadata
    import jax
    import jax.numpy as jnp
    import numpy as np
    from benchmark_ceridwen_vast import _make_log_functions
    from ceridwen.observation import Spectrum

    keys = tuple(model.theta_init)
    key = jax.random.PRNGKey(20260905)
    particles = {}
    for name in keys:
        key, subkey = jax.random.split(key)
        prior = model.priors[name].sample(subkey, shape=(64, *model.theta_init[name].shape))
        values = jnp.asarray(posterior[name]).reshape((-1, *model.theta_init[name].shape))
        indices = np.linspace(0, len(values) - 1, 64, dtype=int)
        particles[name] = jnp.concatenate([prior, values[indices]], axis=0)
    timed_particles = jax.tree.map(lambda v: v[:100], particles)
    gradient_particles = jax.tree.map(lambda v: v[::16], particles)
    original = model._observation_predictor
    functions = {}
    compile_times = {}
    try:
        for arm, selected in (("baseline", None), ("candidate", predictor)):
            model._observation_predictor = selected
            loglike, _ = _make_log_functions(model, likelihood)
            start = time.perf_counter()
            functions[arm] = dict(
                prediction=jax.jit(jax.vmap(model.predict)).lower(particles).compile(),
                loglike=jax.jit(jax.vmap(loglike)).lower(particles).compile(),
                timed=jax.jit(jax.vmap(loglike)).lower(timed_particles).compile(),
                gradient=jax.jit(jax.vmap(jax.grad(loglike))).lower(gradient_particles).compile(),
            )
            compile_times[arm] = time.perf_counter() - start
    finally:
        model._observation_predictor = original

    reference = functions["baseline"]["prediction"](particles)
    actual = functions["candidate"]["prediction"](particles)
    prediction_errors = {}
    for name in reference:
        obs = model.obs_dict[name]
        error = np.asarray(jnp.abs(actual[name] - reference[name]) / obs.uncertainty)
        prediction_errors[name] = float(np.max(error[:, np.asarray(obs.mask)]))
    baseline_lnl = functions["baseline"]["loglike"](particles)
    candidate_lnl = functions["candidate"]["loglike"](particles)
    lnl_error = float(jnp.max(jnp.abs(candidate_lnl - baseline_lnl)))
    baseline_grad = functions["baseline"]["gradient"](gradient_particles)
    candidate_grad = functions["candidate"]["gradient"](gradient_particles)
    bg = np.concatenate([np.asarray(baseline_grad[k]).reshape(8, -1) for k in keys], axis=1)
    cg = np.concatenate([np.asarray(candidate_grad[k]).reshape(8, -1) for k in keys], axis=1)
    gradient_error = float(np.max(np.linalg.norm(cg - bg, axis=1)
                                  / np.maximum(np.linalg.norm(bg, axis=1), 1e-30)))
    timings = {arm: [] for arm in functions}
    for bundle in functions.values():
        jax.block_until_ready(bundle["timed"](timed_particles))
    for repeat in range(20):
        order = ("baseline", "candidate") if repeat % 2 == 0 else ("candidate", "baseline")
        for arm in order:
            start = time.perf_counter()
            jax.block_until_ready(functions[arm]["timed"](timed_particles))
            timings[arm].append(time.perf_counter() - start)

    calibration_probe = None
    if (os.environ["CERIDWEN_SPEEDUP_ARM"] == "candidate"
            and os.environ["CERIDWEN_TARGET_ID"] == "M1_210210"
            and os.environ["CERIDWEN_RANDOM_SEED"] == "20260905"):
        from ceridwen.likelihood import PolynomialCalibration
        from jax.scipy.linalg import cho_solve

        def cholesky_calibrate(self, y, mu, sigma, mask):
            design = self.design(mu, sigma, mask)
            target = jnp.where(mask, (y - mu) / jnp.where(mask, sigma, 1.), 0.)
            normal = self.normal_matrix(mu, sigma, mask)
            lower = jnp.linalg.cholesky(normal)
            coeffs = cho_solve((lower, True), design.T @ target)
            extra = self.log_prior(coeffs)
            if self.marginalize:
                extra -= jnp.sum(jnp.log(jnp.diag(lower)))
                extra += (.5 * self.n_coeff * np.log(2 * np.pi) if self.prior_sigma is None
                          else -jnp.sum(jnp.log(jnp.asarray(self.prior_sigma))))
            return self.polynomial(coeffs) * mu, coeffs, extra

        saved_calibrate = PolynomialCalibration.calibrate
        try:
            model._observation_predictor = None
            PolynomialCalibration.calibrate = cholesky_calibrate
            probe, _ = _make_log_functions(model, likelihood)
            probe_all = jax.jit(jax.vmap(probe)).lower(particles).compile()
            probe_timed = jax.jit(jax.vmap(probe)).lower(timed_particles).compile()
        finally:
            PolynomialCalibration.calibrate = saved_calibrate
            model._observation_predictor = original
        error = float(jnp.max(jnp.abs(probe_all(particles) - baseline_lnl)))
        probe_timings = {"baseline": [], "cholesky": []}
        probe_functions = {"baseline": functions["baseline"]["timed"], "cholesky": probe_timed}
        for fn in probe_functions.values():
            jax.block_until_ready(fn(timed_particles))
        for repeat in range(40):
            order = tuple(probe_functions.items())
            for name, fn in order if repeat % 2 == 0 else reversed(order):
                start = time.perf_counter()
                jax.block_until_ready(fn(timed_particles))
                probe_timings[name].append(time.perf_counter() - start)
        calibration_probe = dict(max_abs_loglike_error=error, batch_seconds=probe_timings,
                                 speedup=float(np.median(probe_timings["baseline"])
                                               / np.median(probe_timings["cholesky"])))

    # The dense reference remains available lazily for this separate path.
    csp = model.csp
    observed = model.obs_dict["spectrum"]
    interp = Spectrum(wavelength=observed.wavelength, name="interpolation_check")
    interp.setup_for_model(csp.wave, zred=model.zred)
    spectrum = csp.get_spectrum(csp.theta_init)
    dense = jax.jit(lambda s: interp._H @ s)
    dense_highest = jax.jit(lambda s: jnp.matmul(interp._H, s, precision="highest"))
    gather = jax.jit(lambda s: interp.predict(s, csp.wave))
    # Default CUDA matrix products can use TF32. Check interpolation accuracy
    # against a float64 CPU product of the same float32 matrix coefficients.
    reference64 = np.asarray(interp._H, dtype=np.float64) @ np.asarray(spectrum, dtype=np.float64)
    interpolation_functions = {"dense": dense, "dense_highest": dense_highest, "gather": gather}
    interpolation_errors = {
        name: float(np.max(np.abs(np.asarray(fn(spectrum)) - reference64) / np.abs(reference64)))
        for name, fn in interpolation_functions.items()
    }
    interpolation = {name: [] for name in interpolation_functions}
    for repeat in range(40):
        order = tuple(interpolation_functions.items())
        for name, fn in order if repeat % 2 == 0 else reversed(order):
            start = time.perf_counter()
            jax.block_until_ready(fn(spectrum))
            interpolation[name].append(time.perf_counter() - start)

    passed = (all(v <= 1e-5 for v in prediction_errors.values())
              and lnl_error <= 1e-3 and gradient_error <= 1e-4
              and interpolation_errors["gather"] <= 2e-7)
    report = dict(
        workload="dr2_poly3_total", target=os.environ["CERIDWEN_TARGET_ID"],
        fit_arm=os.environ["CERIDWEN_SPEEDUP_ARM"], fit_seed=int(os.environ["CERIDWEN_RANDOM_SEED"]),
        validation_seed=20260905, prior_points=64, posterior_points=64,
        batch_size=100, numerical_passed=passed,
        prediction_error_in_sigma=prediction_errors, max_abs_loglike_error=lnl_error,
        max_relative_gradient_error=gradient_error, compile_seconds=compile_times,
        batch_seconds=timings, interpolation_seconds=interpolation,
        interpolation_relative_error_vs_float64=interpolation_errors,
        calibration_probe=calibration_probe,
        likelihood_speedup=float(np.median(timings["baseline"]) / np.median(timings["candidate"])),
        interpolation_speedup=float(np.median(interpolation["dense"]) / np.median(interpolation["gather"])),
        software={name: importlib.metadata.version(name) for name in ("jax", "jaxlib", "blackjax", "ceridwen", "sedpy-jax")},
        devices=[device.device_kind for device in jax.devices()], x64=jax.config.jax_enable_x64,
        validation_instance_id=os.environ.get("CERIDWEN_VAST_INSTANCE"),
    )
    Path(output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if not k.endswith("seconds")}, indent=2))
    assert passed, "Before/after numerical comparison exceeded the fixed acceptance thresholds"
    if (calibration_probe is not None and report["likelihood_speedup"] < 1.05
            and (calibration_probe["speedup"] < 1.05
                 or calibration_probe["max_abs_loglike_error"] > 1e-3)):
        decision = dict(reason="Neither joint-fit candidate passed the performance and accuracy gates",
                        wavelength_speedup=report["likelihood_speedup"],
                        calibration_probe=calibration_probe,
                        interpolation_retained=True)
        (Path(output).parent.parent / "rejected_joint_candidates.json").write_text(
            json.dumps(decision, indent=2) + "\n")
    return report


def comparison_notebook(arm, resume=False):
    import nbformat

    notebook = nbformat.read(PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb", as_version=4)
    inserted = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs = []
        cell.execution_count = None
        marker = "initial_photometry = np.asarray("
        if marker in cell.source:
            setup = (
                "sys.path.insert(0, str(PROJECT_ROOT / 'scripts'))\n"
                "from validate_ceridwen_speedups import prepare_wavelength_experiment\n"
                "_speedup_predictor = prepare_wavelength_experiment(joint_model)\n"
                f"joint_model._observation_predictor = {'None' if arm == 'baseline' else '_speedup_predictor'}\n"
            )
            cell.source = cell.source.replace(marker, setup + marker, 1)
            inserted += 1
        if resume and "joint_result = run_sampler(" in cell.source:
            start = cell.source.index("joint_result = run_sampler(")
            end = cell.source.index("saved_result = load_result_h5", start)
            cell.source = (cell.source[:start]
                           + "result_path = RESULT_DIR / 'ceridwen_result.h5'\n"
                           + "joint_result = load_result_h5(result_path)\n"
                           + cell.source[end:])
    assert inserted == 1, "Production model construction changed"
    notebook.cells.extend([
        nbformat.v4.new_markdown_cell("- Compare equivalent predictions and time completed GPU calculations."),
        nbformat.v4.new_code_cell(
            "from validate_ceridwen_speedups import validate\n"
            "speedup_validation = validate(joint_model, joint_likelihood, joint_posterior,\n"
            "    _speedup_predictor, RESULT_DIR / 'validation.json')\n"
        ),
    ])
    return notebook


def worker(args):
    import nbformat
    from nbclient import NotebookClient

    if (RESULT_ROOT / "rejected_joint_candidates.json").exists():
        print("Joint-fit candidates rejected by the measured gates; remaining fits skipped.")
        return
    folder = RESULT_ROOT / f"{args.target}-{args.seed}-{args.arm}"
    folder.mkdir(parents=True, exist_ok=True)
    os.environ.update(
        CERIDWEN_PROJECT_ROOT=str(PROJECT_ROOT), CERIDWEN_RESULT_DIR=str(folder),
        CERIDWEN_TARGET_ID=args.target, CERIDWEN_OBJECT_ID=args.target.split("_")[-1],
        CERIDWEN_RANDOM_SEED=str(args.seed), CERIDWEN_SPEEDUP_ARM=args.arm,
        CERIDWEN_NOTEBOOK_QUICK="0", CERIDWEN_EXPECT_SINGLE_GPU="1",
        CERIDWEN_CALIBRATION_ORDER="3", CERIDWEN_CALIBRATION_PRIOR="0.1",
        CERIDWEN_PHOTOMETRY="cosmos_total", CERIDWEN_FIT_MODE="full_spectrum",
        CERIDWEN_SPECTRUM_PIXELS="all",
        MPLBACKEND="module://matplotlib_inline.backend_inline",
    )
    resume = (folder / "ceridwen_result.h5").exists()
    notebook = comparison_notebook(args.arm, resume=resume)
    if resume:
        previous = nbformat.read(folder / "analysis.ipynb", as_version=4)
        for old_cell, cell in zip(previous.cells, notebook.cells):
            if "joint_result = load_result_h5(result_path)" in cell.source:
                cell.metadata["fit_execution"] = old_cell.metadata.get(
                    "fit_execution", old_cell.metadata.get("execution", {}))

    class StreamingClient(NotebookClient):
        def process_message(self, msg, cell, cell_index):
            if msg["msg_type"] == "stream":
                print(msg["content"]["text"], end="", flush=True)
            return super().process_message(msg, cell, cell_index)

    client = StreamingClient(notebook, timeout=None, kernel_name="ceridwen",
                             resources={"metadata": {"path": str(PROJECT_ROOT)}})
    try:
        client.execute()
    finally:
        nbformat.write(notebook, folder / "analysis.ipynb")


def rent():
    """Run on available RTX 5060s within the cumulative two-dollar budget."""
    if (RESULT_ROOT / "rejected_joint_candidates.json").exists():
        print("The measured speed gate already rejected the joint-fit candidates; no rental needed.")
        return
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime
    from types import SimpleNamespace
    import threading
    import subprocess
    import calibration_arms_vast as calibration
    import absorption_mask_vast as absorption

    sweep = calibration._sweep()
    busy = {int(i["host_id"]) for i in sweep._vastai_json(["show", "instances"])}
    offers = calibration.offers_rtx_5060(sweep, busy)
    # Limit transfer rates before splitting the remaining budget across boxes.
    offers = [o for o in offers if float(o["inet_up_cost"]) <= .02
              and float(o["inet_down_cost"]) <= .02][:2]
    if not offers:
        raise RuntimeError("No available RTX 5060 fits the transfer budget")
    state_dir = PROJECT_ROOT / "benchmarks/ceridwen/runs/exact-speedups"
    state_dir.mkdir(parents=True, exist_ok=True)
    record_path = state_dir / "vast.json"
    records = json.loads(record_path.read_text()) if record_path.exists() else []
    previous_reservation = sum(r.get("compute_storage_estimate_usd", .8) + .2 for r in records)
    available = 2. - previous_reservation
    # The remaining budget is split across the available boxes, including transfers.
    if available <= .4:
        raise RuntimeError("Insufficient budget remains for another environment installation")
    per_box_cap = available / len(offers)
    lock = threading.Lock()

    def save():
        with lock:
            (state_dir / "vast.json").write_text(json.dumps(records, indent=2) + "\n")

    def run_box(index, offer):
        targets = TARGETS[index::len(offers)]
        rate = float(offer["dph_total"]) + 40 * float(offer["storage_cost"]) / 24 / 30
        limit = min(3 * 3600, (per_box_cap - .2) / rate * 3600)
        log = calibration._log(f"GPU {index}")
        record = dict(targets=targets, offer=offer, total_cap_usd=per_box_cap,
                      maximum_runtime_seconds=limit, hourly_rate_with_storage=rate,
                      started=datetime.now(UTC).isoformat())
        records.append(record)
        save()
        instance = None
        timer = None
        start = time.monotonic()
        try:
            instance = sweep._create_instance(offer, SimpleNamespace(
                image="vastai/base-image:cuda-12.6.3-auto", disk=40))
            record["instance_id"] = instance
            save()
            log(f"created {instance}; cap includes setup and transfer time")
            timer = threading.Timer(limit, lambda: sweep._destroy(instance, log))
            timer.daemon = True
            timer.start()
            sweep._wait_for_running(instance, log)
            sweep._attach_ssh_key(instance)
            sweep._wait_for_ssh(instance, log)
            absorption._checkout(instance, "absorption-mask", log)
            target, port = sweep._ssh_target(instance)
            remote = sweep.REMOTE_ROOT
            # These full fits consume two spectra and the complete catalogues.
            from astropy.table import Table
            catalogue = Table.read(PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz")
            files = ["data/raw/legac_dr2/legaCdr2.fits.gz",
                     "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits",
                     "data/raw/cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits"]
            for row in catalogue:
                if str(row["SPECT_ID"]).strip() in targets:
                    files.append("data/raw/legac_dr2/sp/" + str(row["Filename"]).strip())
            for relative in files:
                sweep._ssh(instance, f"mkdir -p {shlex.quote(str(Path(remote, relative).parent))}", timeout=60.)
                sweep._rsync(port, str(PROJECT_ROOT / relative), f"{target}:{remote}/{relative}", timeout=180.)
            log(f"uploaded {len(files) - 3} selected spectra and all three catalogues")
            for relative in ("scripts/validate_ceridwen_speedups.py",
                             "scripts/benchmark_ceridwen_vast.py",
                             "notebooks/ceridwen_integrated_photometry_spectra.ipynb"):
                sweep._rsync(port, str(PROJECT_ROOT / relative), f"{target}:{remote}/{relative}", timeout=180.)
            # Reuse completed task-owned fits if only their later checks failed.
            if RESULT_ROOT.exists():
                sweep._ssh(instance, f"mkdir -p {remote}/results/rtx-5060-observation-speedups", timeout=60.)
                sweep._rsync(port, str(RESULT_ROOT) + "/",
                             f"{target}:{remote}/results/rtx-5060-observation-speedups/", timeout=180.)
            sweep._ssh(instance, "mkdir -p /root/.ceridwen/grids", timeout=60.)
            for attempt in range(3):
                target, port = sweep._ssh_target(instance)
                shell = shlex.join(["ssh", *sweep._ssh_options(port)])
                transfer = subprocess.run(
                    ["rsync", "-a", "--partial", "-e", shell,
                     str(Path.home() / ".ceridwen/grids/amist_c3k_hr_krou_afe.h5"),
                     f"{target}:/root/.ceridwen/grids/amist_c3k_hr_krou_afe.h5"],
                    capture_output=True, text=True, timeout=600.)
                if transfer.returncode == 0:
                    break
                if attempt == 2:
                    raise RuntimeError(transfer.stderr[-1000:])
                log("grid transfer disconnected; reconnecting and resuming")
                sweep._wait_for_ssh(instance, log)

            # Reuse production installation pins, then start full fits directly.
            bootstrap = (PROJECT_ROOT / "scripts/bootstrap_vast_ai.sh").read_text()
            install = bootstrap.split("# The installed package", 1)[0]
            install = install.replace('SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"',
                                      f"SCRIPT_DIR={shlex.quote(remote + '/scripts')}")
            kernel = bootstrap[bootstrap.index('"${PYTHON_BIN}" -m ipykernel install'):bootstrap.index('CATALOG_PATH=')]
            log("installing the production environment")
            result = sweep._ssh(instance, "bash -c " + shlex.quote(install + kernel), timeout=1800.)
            record["installation_tail"] = result.stdout[-1200:]
            save()
            commands = []
            for target_id in targets:
                for seed in SEEDS:
                    for arm in ("baseline", "candidate"):
                        folder = f"results/rtx-5060-observation-speedups/{target_id}-{seed}-{arm}"
                        argv = [".venv-ceridwen-gpu/bin/python", "scripts/validate_ceridwen_speedups.py",
                                "--target", target_id, "--seed", str(seed), "--arm", arm]
                        commands.append(f"mkdir -p {shlex.quote(folder)} && "
                                        f"{shlex.join(argv)} > {shlex.quote(folder + '/execution.log')} 2>&1")
            script = "set -e\ncd " + shlex.quote(remote) + "\n" + "\n".join(commands)
            script += "\ntouch results/rtx-5060-observation-speedups/complete\n"
            remaining = max(1, int(limit - (time.monotonic() - start) - 180))
            launch = (f"cd {shlex.quote(remote)} && mkdir -p results/rtx-5060-observation-speedups && "
                      f"setsid -f env LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                      f"CERIDWEN_VAST_INSTANCE={instance} "
                      f"XLA_FLAGS=--xla_gpu_enable_command_buffer= "
                      f"timeout {remaining}s bash -c {shlex.quote(script)} "
                      "> results/rtx-5060-observation-speedups/controller.log 2>&1 < /dev/null")
            sweep._ssh(instance, launch, timeout=60.)
            log(f"full comparison fits started: {targets}")
            while time.monotonic() - start < limit - 120:
                time.sleep(30)
                status = sweep._ssh(instance,
                    f"cd {shlex.quote(remote)} && "
                    "find results/rtx-5060-observation-speedups -name validation.json | wc -l; "
                    "nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader; "
                    "test -f results/rtx-5060-observation-speedups/complete && echo COMPLETE; "
                    "pgrep -af '^.venv-ceridwen-gpu/bin/python scripts/validate_ceridwen_speedups.py' || true",
                    timeout=60.).stdout
                log(status.strip().replace("\n", " | "))
                record["last_status"] = status
                save()
                if "COMPLETE" in status:
                    record["complete"] = True
                    break
                record["needs_attention"] = "scripts/validate_ceridwen_speedups.py" not in status
                if record["needs_attention"]:
                    log("worker exited; retaining the instance for repair within its existing deadline")
                    save()
        except Exception as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log(record["error"])
        finally:
            if instance is not None:
                try:
                    target, port = sweep._ssh_target(instance)
                    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
                    for target_id in targets:
                        pattern = f"{sweep.REMOTE_ROOT}/results/rtx-5060-observation-speedups/{target_id}-*"
                        if sweep._ssh(instance, f"compgen -G {shlex.quote(pattern)}", timeout=60.,
                                      check=False).returncode != 0:
                            continue
                        sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/results/rtx-5060-observation-speedups/{target_id}-*",
                                     str(RESULT_ROOT) + "/", timeout=180.)
                    decision = "results/rtx-5060-observation-speedups/rejected_joint_candidates.json"
                    if sweep._ssh(instance, f"test -f {sweep.REMOTE_ROOT}/{decision}", timeout=60.,
                                  check=False).returncode == 0:
                        sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/{decision}",
                                     str(RESULT_ROOT) + "/", timeout=180.)
                except Exception as error:
                    record["pull_error"] = str(error)
                sweep._destroy(instance, log)
            if timer is not None:
                timer.cancel()
            record["elapsed_seconds"] = time.monotonic() - start
            record["compute_storage_estimate_usd"] = record["elapsed_seconds"] / 3600 * rate
            record["finished"] = datetime.now(UTC).isoformat()
            save()

    with ThreadPoolExecutor(max_workers=len(offers)) as pool:
        list(pool.map(lambda item: run_box(*item), enumerate(offers)))
    if not all(record.get("complete") for record in records[-len(offers):]):
        raise RuntimeError("At least one comparison did not complete; inspect vast.json")


def main():
    if sys.argv[1:] == ["rent"]:
        rent()
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=TARGETS)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--arm", required=True, choices=("baseline", "candidate"))
    worker(parser.parse_args())


if __name__ == "__main__":
    main()
