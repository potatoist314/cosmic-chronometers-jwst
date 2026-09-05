#!/usr/bin/env python3
"""Verify the per-galaxy diagnostics on one Vast.ai RTX 5060 under a hard spend cap.

The box clones the branch, receives the private submodule trees and
``data/raw`` by rsync, bootstraps the CUDA environment, then:

1. refits each requested target with the production notebook and settings
   (same seed as the DR2 run, via ``scripts/run_ceridwen_vast_multi_gpu.py``),
   writing into ``results/rtx-5060-per-galaxy-diagnostics-verification/``;
2. re-evaluates the stored best-sample log-likelihood of the production result
   and of the fresh result on the GPU (``per_galaxy_diagnostics.py check``), so
   the CPU-versus-GPU difference seen locally can be attributed.

Results are pulled back, the instance is destroyed (also on failure), and the
rental is recorded with its estimated spend in ``vast_run_<stamp>.json`` inside
the verification directory. The run aborts and destroys the instance when the
running estimate ``price * hours`` reaches 90 percent of ``--spend-cap-usd``.

Sub-commands::

    plan                                         show the RTX 5060 offers that qualify
    run   --target SPECT_ID [--target ...]       rent, refit, check, pull, destroy
    destroy --instance ID                        destroy one instance rented by this script
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import shlex
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = "results/rtx-5060-dr2-quiescent-full-spectrum"
VERIFICATION = "results/rtx-5060-per-galaxy-diagnostics-verification"
LABEL = "ceridwen-diag-rtx-5060"
POLL_SECONDS = 60
PULL_EVERY_SECONDS = 600
RUN_TIMEOUT_SECONDS = 3 * 3600
EXPECTED_HOURS = 2.0
REMOTE_JOB = "per_galaxy_diagnostics_remote_job.sh"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


absorption = _load(PROJECT_ROOT / "scripts/absorption_mask_vast.py", "absorption_mask_vast")
sweep = absorption.sweep


def _log(message: str) -> None:
    print(f"[{datetime.now(UTC).strftime('%H:%M:%S')}] {message}", flush=True)


def rtx5060_offers() -> list[dict]:
    query = ("gpu_name=RTX_5060 verified=true rentable=true num_gpus=1 "
             "inet_down>200 disk_space>=40 reliability>0.98")
    offers = sweep._vastai_json(["search", "offers", query, "-o", "dph"])
    offers = [
        o for o in offers
        if (o.get("inet_down_cost") or 0) <= sweep.MAX_INET_COST_USD_PER_TB
        and float(o.get("gpu_ram") or 0) >= 8000
        and float(o.get("cuda_max_good") or 0) >= 12.6
    ]
    offers.sort(key=lambda o: o["dph_total"])
    return offers


def shard_of(spect_id: str, targets: list[dict]) -> int:
    for target in targets:
        if target["spect_id"] == spect_id:
            return int(target["shard_index"])
    raise SystemExit(f"{spect_id} is not in {PRODUCTION}/targets.json")


def remote_job_script(pairs: list[tuple[str, int]], production_dirs: list[str]) -> str:
    remote = sweep.REMOTE_ROOT
    lines = [
        "#!/usr/bin/env bash",
        "set -u",
        f"cd {shlex.quote(remote)}",
        "export JAX_ENABLE_X64=1 LD_LIBRARY_PATH=",
        f"OUT={VERIFICATION}",
        'mkdir -p "$OUT"',
        'echo "started $(date -u +%FT%TZ)" > "$OUT/REMOTE_STATUS"',
        'nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader > "$OUT/gpu.txt" 2>&1',
    ]
    for spect, shard in pairs:
        lines.append(
            f"JAX_PLATFORMS=cpu .venv-ceridwen-gpu/bin/python scripts/run_ceridwen_vast_multi_gpu.py "
            f"--targets-file \"$OUT/targets.json\" --shard-index {shard} --only-target {shlex.quote(spect)} "
            f"--output-root \"$OUT\" --max-attempts 1 > \"$OUT/run_{spect}.log\" 2>&1"
        )
        lines.append(f'echo "refit {spect} exit $?" >> "$OUT/REMOTE_STATUS"')
    lines.append(': > "$OUT/gpu_lnl_check.log"')
    for folder in production_dirs:
        lines.append(
            f"JAX_PLATFORMS=cuda .venv-ceridwen-gpu/bin/python scripts/per_galaxy_diagnostics.py check "
            f"{shlex.quote(folder)} >> \"$OUT/gpu_lnl_check.log\" 2>&1"
        )
    lines.append(
        'for d in "$OUT"/*/; do [ -f "$d/ceridwen_result.h5" ] && JAX_PLATFORMS=cuda '
        '.venv-ceridwen-gpu/bin/python scripts/per_galaxy_diagnostics.py check "$d" >> "$OUT/gpu_lnl_check.log" 2>&1; done'
    )
    lines.append('echo "finished $(date -u +%FT%TZ)" >> "$OUT/REMOTE_STATUS"')
    lines.append('touch "$OUT/REMOTE_DONE"')
    return "\n".join(lines) + "\n"


def _upload_verification_inputs(instance_id: int, pairs: list[tuple[str, int]], targets_manifest: Path, script: str) -> None:
    target, port = sweep._ssh_target(instance_id)
    remote = sweep.REMOTE_ROOT
    sweep._ssh(instance_id, f"mkdir -p {shlex.quote(remote)}/{VERIFICATION}", timeout=60.0)
    sweep._rsync(port, str(targets_manifest), f"{target}:{remote}/{VERIFICATION}/targets.json", timeout=120.0)
    local_script = PROJECT_ROOT / VERIFICATION / REMOTE_JOB
    local_script.write_text(script, encoding="utf-8")
    sweep._rsync(port, str(local_script), f"{target}:{remote}/{VERIFICATION}/{REMOTE_JOB}", timeout=120.0)
    for spect, _ in pairs:
        folders = sorted((PROJECT_ROOT / PRODUCTION).glob(f"*-{spect}"))
        if not folders:
            raise sweep.SweepError(f"no production folder for {spect}")
        folder = folders[0]
        sweep._ssh(instance_id, f"mkdir -p {shlex.quote(remote)}/{PRODUCTION}/{folder.name}", timeout=60.0)
        for name in ("ceridwen_result.h5", "ceridwen_derived_outputs.h5"):
            sweep._rsync(port, str(folder / name), f"{target}:{remote}/{PRODUCTION}/{folder.name}/{name}", timeout=600.0)


def _launch(instance_id: int) -> None:
    remote = sweep.REMOTE_ROOT
    command = (
        f"cd {shlex.quote(remote)} && setsid -f bash {VERIFICATION}/{REMOTE_JOB} "
        f"> {VERIFICATION}/remote_job.log 2>&1 < /dev/null; sleep 2; "
        f"pgrep -f {shlex.quote(REMOTE_JOB)} >/dev/null && echo launched"
    )
    result = sweep._ssh(instance_id, command, timeout=60.0)
    if "launched" not in result.stdout:
        raise sweep.SweepError("the remote job did not start")


def _remote_status(instance_id: int) -> tuple[str, bool, bool]:
    remote = sweep.REMOTE_ROOT
    probe = sweep._ssh(
        instance_id,
        f"cat {remote}/{VERIFICATION}/REMOTE_STATUS 2>/dev/null; echo '@@'; "
        f"test -f {remote}/{VERIFICATION}/REMOTE_DONE && echo done; echo '@@'; "
        f"pgrep -f {shlex.quote(REMOTE_JOB)} >/dev/null && echo alive",
        timeout=60.0, check=False,
    )
    status, _, rest = probe.stdout.partition("@@")
    done_text, _, alive_text = rest.partition("@@")
    return status.strip(), "done" in done_text, "alive" in alive_text


def _pull(instance_id: int) -> None:
    target, port = sweep._ssh_target(instance_id)
    local = PROJECT_ROOT / VERIFICATION
    local.mkdir(parents=True, exist_ok=True)
    sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/{VERIFICATION}/", f"{local}/", timeout=1800.0)


def _credit() -> float:
    try:
        return float(sweep._vastai_json(["show", "user"]).get("credit", float("nan")))
    except sweep.SweepError:
        return float("nan")


def command_plan(args) -> int:
    for offer in rtx5060_offers()[: args.count]:
        print(absorption._describe(offer))
    return 0


def command_run(args) -> int:
    manifest_path = PROJECT_ROOT / PRODUCTION / "targets.json"
    targets = json.loads(manifest_path.read_text())["targets"]
    pairs = [(spect, shard_of(spect, targets)) for spect in args.target]
    production_dirs = [f"{PRODUCTION}/{sorted((PROJECT_ROOT / PRODUCTION).glob(f'*-{s}'))[0].name}" for s, _ in pairs]
    record_dir = PROJECT_ROOT / VERIFICATION
    record_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    record_path = record_dir / f"vast_run_{stamp}.json"
    record = {
        "started": datetime.now(UTC).isoformat(timespec="seconds"),
        "branch": args.branch, "targets": pairs, "spend_cap_usd": args.spend_cap_usd,
        "credit_before": _credit(), "instance_id": None, "offer": None, "events": [],
    }

    def save(**fields):
        record.update(fields)
        record_path.write_text(json.dumps(record, indent=1, default=str))

    busy_hosts = {int(i.get("host_id") or 0) for i in sweep._vastai_json(["show", "instances"])}
    offers = [o for o in rtx5060_offers() if int(o.get("host_id") or 0) not in busy_hosts]
    if not offers:
        print("no qualifying RTX 5060 offer", file=sys.stderr)
        return 1
    offer = offers[0]
    if offer["dph_total"] * EXPECTED_HOURS > args.spend_cap_usd:
        print(f"cheapest offer ${offer['dph_total']:.4f}/h would exceed the cap over {EXPECTED_HOURS} h", file=sys.stderr)
        return 1
    save(offer={k: offer.get(k) for k in ("id", "gpu_name", "dph_total", "geolocation", "host_id", "reliability2", "cuda_max_good")})

    instance_id = None
    rented_at = None
    error = None
    try:
        instance_id = sweep._create_instance(offer, args)
        rented_at = time.monotonic()
        save(instance_id=instance_id, rented_at=datetime.now(UTC).isoformat(timespec="seconds"))
        _log(f"rented instance {instance_id}: {absorption._describe(offer)}")
        sweep._wait_for_running(instance_id, _log)
        # The instance bills GPU plus disk; the offer price is the GPU alone.
        billed = sweep._instance_state(instance_id).get("dph_total")
        if billed:
            offer = {**offer, "dph_total": float(billed)}
            save(instance_dph_total=float(billed))
            _log(f"instance hourly rate incl. disk: ${float(billed):.4f}/h")
        sweep._attach_ssh_key(instance_id)
        sweep._wait_for_ssh(instance_id, _log)
        absorption._checkout(instance_id, args.branch, _log)
        sweep._upload_inputs(instance_id, _log)
        sweep._bootstrap(instance_id, _log)
        sweep._verify_cuda_backend(instance_id, _log)
        _upload_verification_inputs(instance_id, pairs, manifest_path, remote_job_script(pairs, production_dirs))
        _launch(instance_id)
        _log("remote job launched")
        record["events"].append({"launched": datetime.now(UTC).isoformat(timespec="seconds"),
                                 "setup_hours": round((time.monotonic() - rented_at) / 3600, 3)})
        save()
        deadline = time.monotonic() + RUN_TIMEOUT_SECONDS
        last_pull = time.monotonic()
        while time.monotonic() < deadline:
            time.sleep(POLL_SECONDS)
            hours = (time.monotonic() - rented_at) / 3600
            estimate = hours * offer["dph_total"]
            status, done, alive = _remote_status(instance_id)
            _log(f"{hours:.2f} h, est ${estimate:.3f}; status: {status.splitlines()[-1] if status else '-'}; alive={alive} done={done}")
            if estimate >= 0.9 * args.spend_cap_usd:
                error = f"spend estimate ${estimate:.2f} reached 90% of the ${args.spend_cap_usd:.2f} cap; aborting"
                _log(error)
                break
            if done or not alive:
                if not done:
                    error = "remote job exited before REMOTE_DONE"
                break
            if time.monotonic() - last_pull > PULL_EVERY_SECONDS:
                _pull(instance_id)
                last_pull = time.monotonic()
        else:
            error = "run timeout"
        _pull(instance_id)
    except Exception as exc:  # noqa: BLE001 - always destroy, then report
        error = f"{type(exc).__name__}: {exc}"
        _log(f"failed: {error}")
        if instance_id is not None:
            try:
                _pull(instance_id)
            except Exception as pull_error:  # noqa: BLE001
                _log(f"pull failed: {pull_error}")
    finally:
        if instance_id is not None:
            sweep._destroy(instance_id, _log)
            leftover = sweep._instance_exists(instance_id)
            hours = (time.monotonic() - rented_at) / 3600 if rented_at else 0.0
            save(
                finished=datetime.now(UTC).isoformat(timespec="seconds"),
                billed_hours_estimate=round(hours, 4),
                spend_estimate_usd=round(hours * offer["dph_total"], 4),
                credit_after=_credit(),
                instance_destroyed=not leftover,
                error=error,
            )
            record["credit_spent_usd"] = (
                round(record["credit_before"] - record["credit_after"], 4)
                if record["credit_before"] == record["credit_before"] and record["credit_after"] == record["credit_after"]
                else None
            )
            save()
    print(json.dumps({k: record.get(k) for k in ("instance_id", "billed_hours_estimate", "spend_estimate_usd",
                                                  "credit_spent_usd", "instance_destroyed", "error")}, indent=1))
    return 1 if error else 0


def command_destroy(args) -> int:
    sweep._destroy(args.instance, _log)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--count", type=int, default=5)
    run = sub.add_parser("run")
    run.add_argument("--target", action="append", required=True, help="SPECT_ID from the DR2 manifest (repeatable)")
    run.add_argument("--branch", default="absorption-mask")
    run.add_argument("--spend-cap-usd", type=float, default=2.0)
    run.add_argument("--image", default=sweep.DEFAULT_IMAGE)
    run.add_argument("--disk", type=int, default=sweep.DEFAULT_DISK_GB)
    destroy = sub.add_parser("destroy")
    destroy.add_argument("--instance", type=int, required=True)
    args = parser.parse_args(argv)
    return {"plan": command_plan, "run": command_run, "destroy": command_destroy}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
