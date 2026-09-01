#!/usr/bin/env python3
"""Verify the static-smoothing change on one rented Vast.ai GPU.

Runs the fixed benchmark twice on the SAME instance -- once on the committed
baseline and once with the smoothing change applied -- so the comparison is free
of host-to-host variation. The instance is always destroyed, including on
failure.

The change lives in a local ceridwen commit that cannot be pushed (the submodule
is a third-party repository), so the patched files are copied over the clone
with rsync rather than fetched.

Usage:
    python scripts/verify_smoothing_speedup_vast.py --gpu "RTX 5060"
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

# Files carrying the change, relative to the ceridwen submodule root.
PATCHED_FILES = (
    "ceridwen/observation/_smoothing.py",
    "ceridwen/observation/spectrum.py",
    "tests/test_static_smoothing.py",
)


def _local_ceridwen_commit() -> str:
    import subprocess
    try:
        return subprocess.run(
            ["git", "-C", str(PROJECT_ROOT / "ceridwen"), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def _log(message: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"{stamp} {message}", flush=True)


def _upload_patch(instance_id: int) -> None:
    """Copy the changed ceridwen files over the freshly cloned submodule."""
    _log("uploading the patched ceridwen files")
    target, port = S._ssh_target(instance_id)
    local_root = PROJECT_ROOT / "ceridwen"
    for relative in PATCHED_FILES:
        source = local_root / relative
        if not source.is_file():
            raise S.SweepError(f"missing patched file: {source}")
        remote_dir = f"{S.REMOTE_ROOT}/ceridwen/{Path(relative).parent}"
        S._ssh(instance_id, f"mkdir -p {shlex.quote(remote_dir)}", timeout=60.0)
        S._rsync(port, str(source), f"{target}:{remote_dir}/", timeout=300.0)
    _log(f"uploaded {len(PATCHED_FILES)} files")


def _restore_baseline(instance_id: int) -> None:
    """Return the submodule to its committed state."""
    _log("restoring the committed baseline")
    S._ssh(
        instance_id,
        f"cd {shlex.quote(S.REMOTE_ROOT)}/ceridwen && "
        "git checkout -- ceridwen/observation/spectrum.py && "
        "rm -f ceridwen/observation/_smoothing.py tests/test_static_smoothing.py && "
        "git status --short",
        timeout=120.0,
    )


def _pytest(instance_id: int, paths: str) -> str:
    """Run pytest inside the CUDA venv. Never fatal: the benchmark numbers are
    already collected by this point, and the bootstrap does not guarantee that
    pytest is installed."""
    try:
        S._ssh(
            instance_id,
            f"cd {shlex.quote(S.REMOTE_ROOT)} && "
            "LD_LIBRARY_PATH= .venv-ceridwen-gpu/bin/python -m pip install -q pytest",
            timeout=600.0,
        )
        return S._ssh(
            instance_id,
            f"cd {shlex.quote(S.REMOTE_ROOT)}/ceridwen && "
            "LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
            f".venv-ceridwen-gpu/bin/python -m pytest {paths} -q -p no:randomly",
            timeout=1800.0,
        ).stdout
    except Exception as error:  # noqa: BLE001 - diagnostics only
        return f"pytest step failed: {type(error).__name__}: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gpu", default="RTX 5060")
    parser.add_argument("--image", default=S.DEFAULT_IMAGE)
    parser.add_argument("--disk", type=int, default=S.DEFAULT_DISK_GB)
    parser.add_argument("--attempts", type=int, default=4,
                        help="rental attempts before giving up")
    parser.add_argument("--keep", action="store_true",
                        help="leave the instance running (it still costs money)")
    args = parser.parse_args()

    # Some hosts re-issue offer IDs every few seconds, so an ID resolved once
    # is often stale by the time the rental call reaches Vast.  Re-search on
    # every attempt and fall through to the next offer.
    offer = None
    instance_id = None
    started = time.time()
    for attempt in range(1, args.attempts + 1):
        ranked = S.rank_offers_for_gpu(S.search_offers(), args.gpu)
        if not ranked:
            print(f"no {args.gpu} offers satisfy the benchmark constraints",
                  file=sys.stderr)
            return 2
        candidate = ranked[min(attempt - 1, len(ranked) - 1)]
        _log(f"attempt {attempt}/{args.attempts}: renting offer {candidate['id']} "
             f"at ${float(candidate['dph_total']):.3f}/hr (host {candidate['host_id']})")
        try:
            instance_id = S._create_instance(candidate, args)
            offer = candidate
            break
        except S.SweepError as error:
            _log(f"rental failed: {error}")
    if instance_id is None or offer is None:
        print(f"could not rent an {args.gpu} after {args.attempts} attempts",
              file=sys.stderr)
        return 2
    _log(f"instance {instance_id} created")
    report: dict = {
        "schema_version": 1,
        "gpu_name": args.gpu,
        "vast_instance": instance_id,
        "vast_host": offer["host_id"],
        "price_usd_per_hour": float(offer["dph_total"]),
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "local_ceridwen_commit": _local_ceridwen_commit(),
        "note": ("the change lives in a local ceridwen commit that cannot be "
                 "pushed; the patched files are rsynced over the clone"),
    }
    try:
        S._attach_ssh_key(instance_id)
        S._wait_for_running(instance_id, _log)
        S._wait_for_ssh(instance_id, _log)
        S._prepare_checkout(instance_id, _log)
        S._upload_inputs(instance_id, _log)
        S._bootstrap(instance_id, _log)
        S._verify_cuda_backend(instance_id, _log)

        _log("=== BASELINE run (committed ceridwen) ===")
        baseline = S._run_benchmark(instance_id, offer, _log)
        report["baseline"] = baseline
        _log(f"baseline: {baseline['likelihood_calls_per_second']:.2f} calls/s")

        _upload_patch(instance_id)
        _log("=== PATCHED run (static smoothing) ===")
        patched = S._run_benchmark(instance_id, offer, _log)
        report["patched"] = patched
        _log(f"patched:  {patched['likelihood_calls_per_second']:.2f} calls/s")

        speedup = (patched["likelihood_calls_per_second"]
                   / baseline["likelihood_calls_per_second"])
        report["speedup"] = speedup
        _log(f"SPEEDUP: {speedup:.3f}x")

        _log("=== new tests on CUDA ===")
        report["pytest_static_smoothing"] = _pytest(
            instance_id, "tests/test_static_smoothing.py")
        _log(report["pytest_static_smoothing"].strip().splitlines()[-1])

        _log("=== existing spectrum tests on CUDA ===")
        report["pytest_spectrum"] = _pytest(
            instance_id, "tests/test_spectrum_fixes.py tests/test_spectrum_scaling.py")
        _log(report["pytest_spectrum"].strip().splitlines()[-1])

        for tag in ("baseline", "patched"):
            S._download_result(instance_id, report[tag]["result_directory"], _log)
    finally:
        report["elapsed_seconds"] = time.time() - started
        report["cost_usd"] = (report["elapsed_seconds"] / 3600.0
                              * float(offer["dph_total"]))
        out = PROJECT_ROOT / "benchmarks/ceridwen/runs"
        out.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = out / f"static_smoothing_verification_{stamp}.json"
        path.write_text(json.dumps(report, indent=2, default=str))
        _log(f"report: {path}")
        _log(f"elapsed {report['elapsed_seconds']/60:.1f} min, "
             f"cost ${report['cost_usd']:.3f}")
        if args.keep:
            _log(f"KEEPING instance {instance_id} -- it is still billing")
        elif S._instance_exists(instance_id):
            S._destroy(instance_id, _log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# TODO(next GPU run): prefer restarting a stopped instance over renting a new one.
# `vastai show instances` lists stopped RTX 5060s that retain their bootstrapped
# CUDA venv on disk, which is the slowest step here (~10 min). Reusing one needs
# `vastai start instance <id>`, skipping _bootstrap, and replacing the `rm -rf`
# in _prepare_checkout with a fetch, since their disk has little free space.
# Stopped instances also hold capacity on their host, which is why fresh rentals
# from that host fail.
