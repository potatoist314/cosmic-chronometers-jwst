#!/usr/bin/env python3
"""A/B the static-smoothing change on an already-provisioned Vast instance.

Reusing a stopped instance skips the clone, the data upload, the SSP grid
download, and the CUDA bootstrap -- about ten minutes of the fifteen a fresh
rental costs, at a lower hourly rate. A stopped instance also keeps holding
capacity on its host, which is why fresh rentals from that host can fail.

The instance is STOPPED, never destroyed: it carries production results.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import sweep_ceridwen_vast_gpus as S  # noqa: E402

REMOTE = "/workspace/cosmic-chronometers-jwst"
PATCHED = ("ceridwen/observation/_smoothing.py", "ceridwen/observation/spectrum.py")


def _log(m: str) -> None:
    print(datetime.now(timezone.utc).strftime("%H:%M:%S"), m, flush=True)


def _wait_running(iid: int, limit: int = 40) -> None:
    for _ in range(limit):
        st = S._instance_state(iid)
        if st.get("actual_status") == "running":
            return
        time.sleep(15)
    raise S.SweepError("instance did not reach running")


def _existing_results(iid: int) -> list[str]:
    """Completed benchmark directories already on the instance for today."""
    out = S._ssh(
        iid,
        f"ls -d {REMOTE}/results/*joint_full_benchmark_complete* 2>/dev/null || true",
        timeout=120.0,
    ).stdout
    names = [Path(line.strip()).name for line in out.splitlines() if line.strip()]
    keep = []
    for name in names:
        probe = S._ssh(
            iid,
            f"test -f {shlex.quote(f'{REMOTE}/results/{name}/benchmark.json')} "
            "&& echo yes || echo no",
            timeout=120.0,
        ).stdout.strip()
        if probe.endswith("yes"):
            keep.append(name)
    return keep


def _read_result(iid: int, name: str, label: str) -> dict:
    record = json.loads(S._ssh(
        iid, f"cat {shlex.quote(f'{REMOTE}/results/{name}/benchmark.json')}", timeout=120.0
    ).stdout)
    record["result_directory"] = name
    t = record["timings"]
    _log(f"{label}: {t['likelihood_calls_per_second']:.2f} calls/s "
         f"({t['median_step_seconds']:.3f} s/step, setup {t.get('setup_seconds', 0):.1f} s)")
    return record


def _archive(iid: int, name: str, suffix: str) -> str:
    """Free the date-based directory name so the next run can write it."""
    new = f"{name}__{suffix}"
    S._ssh(iid, f"mv {shlex.quote(f'{REMOTE}/results/{name}')} "
                f"{shlex.quote(f'{REMOTE}/results/{new}')}", timeout=120.0)
    _log(f"archived {name} -> {new}")
    return new


def _benchmark(iid: int, dph: float, host: int, label: str) -> dict:
    _log(f"=== {label} benchmark ===")
    out = S._ssh(
        iid,
        f"cd {shlex.quote(REMOTE)} && LD_LIBRARY_PATH= JAX_PLATFORMS=cuda "
        f"JAX_ENABLE_X64=1 .venv-ceridwen-gpu/bin/python scripts/benchmark_ceridwen_vast.py run "
        f"--price-usd-per-hour {dph!r} --vast-host {host} --vast-instance {iid}",
        timeout=S.BENCHMARK_TIMEOUT_SECONDS,
    ).stdout
    saved = [l.split("saved:", 1)[1].strip() for l in out.splitlines() if l.startswith("saved:")]
    if len(saved) != 1:
        raise S.SweepError(f"{label}: runner reported {len(saved)} directories")
    name = Path(saved[0]).name
    record = json.loads(S._ssh(
        iid, f"cat {shlex.quote(f'{REMOTE}/results/{name}/benchmark.json')}", timeout=120.0
    ).stdout)
    record["result_directory"] = name
    t = record.get("timings", {})
    if "likelihood_calls_per_second" not in t:
        raise S.SweepError(
            f"{label}: benchmark.json has no timings.likelihood_calls_per_second; "
            f"top-level keys are {sorted(record)}"
        )
    _log(f"{label}: {t['likelihood_calls_per_second']:.2f} calls/s "
         f"({t['median_step_seconds']:.3f} s/step, "
         f"setup {t.get('setup_seconds', float('nan')):.1f} s)")
    return record


def _rate(record: dict) -> float:
    return float(record["timings"]["likelihood_calls_per_second"])


def _peak_mib(record: dict) -> float:
    return float(record.get("memory", {}).get("jax", {})
                 .get("peak_bytes_in_use_mib", float("nan")))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--instance", type=int, required=True)
    ap.add_argument("--leave-running", action="store_true")
    args = ap.parse_args()
    iid = args.instance

    state = S._instance_state(iid)
    dph, host = float(state["dph_total"]), int(state["host_id"])
    _log(f"reusing instance {iid} ({state.get('gpu_name')}) at ${dph:.4f}/hr on host {host}")
    started = time.time()
    report = {"schema_version": 1, "mode": "reused_instance", "vast_instance": iid,
              "vast_host": host, "gpu_name": state.get("gpu_name"),
              "price_usd_per_hour": dph,
              "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "ceridwen_baseline": "afe37fe", "ceridwen_patched": "a38982a (local only)"}
    try:
        if state.get("actual_status") != "running":
            S._vastai(["start", "instance", str(iid)])
            _wait_running(iid)
        S._attach_ssh_key(iid)
        S._wait_for_ssh(iid, _log)
        S._verify_cuda_backend(iid, _log)

        # A completed run from the unmodified tree is a valid baseline: the
        # ceridwen files were checksum-matched to afe37fe before it ran.  The
        # runner names directories by date, so reuse it and free the name.
        existing = _existing_results(iid)
        if existing:
            _log(f"reusing the baseline already on disk: {existing[0]}")
            report["baseline"] = _read_result(iid, existing[0], "BASELINE")
            report["baseline_reused"] = True
        else:
            report["baseline"] = _benchmark(iid, dph, host, "BASELINE")
            report["baseline_reused"] = False
        base_dir = _archive(iid, report["baseline"]["result_directory"], "baseline")
        report["baseline"]["result_directory"] = base_dir

        # The bootstrap installs ceridwen NON-editable
        # (`uv pip install "${PROJECT_ROOT}/ceridwen"`), so the benchmark
        # imports from site-packages, not from the source tree.  Patching the
        # tree alone silently changes nothing.
        installed = S._ssh(
            iid,
            f"cd {shlex.quote(REMOTE)} && LD_LIBRARY_PATH= .venv-ceridwen-gpu/bin/python "
            "-c \"import ceridwen, pathlib; print(pathlib.Path(ceridwen.__file__).parent)\"",
            timeout=180.0,
        ).stdout.strip().splitlines()[-1]
        _log(f"installed ceridwen package: {installed}")
        report["installed_package_path"] = installed

        _log("uploading patched files into the installed package")
        target, port = S._ssh_target(iid)
        for rel in PATCHED:
            leaf = rel.split("/", 1)[1]          # observation/...
            S._rsync(port, str(PROJECT_ROOT / "ceridwen" / rel),
                     f"{target}:{installed}/{leaf}", timeout=300.0)
            S._rsync(port, str(PROJECT_ROOT / "ceridwen" / rel),
                     f"{target}:{REMOTE}/ceridwen/{rel}", timeout=300.0)
        S._ssh(iid, f"find {shlex.quote(installed)} -name '__pycache__' -type d "
                    "-exec rm -rf {} + 2>/dev/null || true", timeout=120.0)

        # Prove the patch is live before trusting any number it produces.
        probe = S._ssh(
            iid,
            f"cd {shlex.quote(REMOTE)} && LD_LIBRARY_PATH= JAX_PLATFORMS=cpu "
            ".venv-ceridwen-gpu/bin/python -c \""
            "from ceridwen.observation._smoothing import make_static_smoother; "
            "from ceridwen.observation.spectrum import Spectrum; "
            "import numpy as np; "
            "wo=np.linspace(5800,9500,600); "
            "wm=4500*np.exp(np.arange(int(np.log(11000/4500)*6000))/6000); "
            "s=Spectrum(wavelength=wo, flux=np.ones_like(wo), uncertainty=np.ones_like(wo), "
            "resolution=2600.0, smoothtype='R', res_convention='fwhm', inres=0.0, "
            "sigma_losvd=259.5, name='probe'); "
            "s.setup_for_model(wm, zred=0.0); "
            "print('PATCH_LIVE grid=%d H_built=%s' % (s.smoother_grid_size, s._H_cached is not None))"
            "\"",
            timeout=600.0,
        ).stdout
        _log(f"patch probe: {probe.strip().splitlines()[-1]}")
        if "PATCH_LIVE" not in probe:
            raise S.SweepError("the patched code is not the code being imported")
        report["patch_probe"] = probe.strip().splitlines()[-1]
        report["patched"] = _benchmark(iid, dph, host, "PATCHED")
        report["patched"]["result_directory"] = _archive(
            iid, report["patched"]["result_directory"], "patched")

        b, p = _rate(report["baseline"]), _rate(report["patched"])
        report["speedup"] = p / b
        report["baseline_calls_per_second"] = b
        report["patched_calls_per_second"] = p
        mb, mp = _peak_mib(report["baseline"]), _peak_mib(report["patched"])
        report["peak_mib_baseline"], report["peak_mib_patched"] = mb, mp
        _log(f"GPU SPEEDUP: {p / b:.3f}x  ({b:.1f} -> {p:.1f} calls/s)")
        _log(f"JAX peak memory: {mb:.0f} -> {mp:.0f} MiB")

        _log("restoring the baseline files")
        for dest in (f"{installed}/observation/spectrum.py",
                     f"{REMOTE}/ceridwen/ceridwen/observation/spectrum.py"):
            S._rsync(port, str(PROJECT_ROOT / ".baseline_spectrum.py"),
                     f"{target}:{dest}", timeout=300.0)
        S._ssh(iid, f"rm -f {shlex.quote(installed)}/observation/_smoothing.py "
                    f"{REMOTE}/ceridwen/ceridwen/observation/_smoothing.py; "
                    f"find {shlex.quote(installed)} -name '__pycache__' -type d "
                    "-exec rm -rf {} + 2>/dev/null || true", timeout=120.0)
    finally:
        report["elapsed_seconds"] = time.time() - started
        report["cost_usd"] = report["elapsed_seconds"] / 3600.0 * dph
        out = PROJECT_ROOT / "benchmarks/ceridwen/runs"
        out.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = out / f"static_smoothing_gpu_verification_{stamp}.json"
        path.write_text(json.dumps(report, indent=2, default=str))
        _log(f"report: {path}")
        _log(f"elapsed {report['elapsed_seconds']/60:.1f} min, cost ${report['cost_usd']:.3f}")
        if args.leave_running:
            _log(f"instance {iid} LEFT RUNNING and still billing")
        else:
            _log(f"stopping instance {iid} (not destroying: it holds production results)")
            S._vastai(["stop", "instance", str(iid)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
