#!/usr/bin/env python3
"""Rent one Vast.ai RTX 5060 and run the calibration-polynomial arms on it.

Every cell executes the production notebook
(``notebooks/ceridwen_integrated_photometry_spectra.ipynb``) through
``scripts/run_ceridwen_vast_multi_gpu.py --only-target`` with the production
sampler settings and the production seed of the target, so the arms of one
galaxy differ only in the environment switches below.

Arms::

    baseline      CERIDWEN_CALIBRATION_ORDER=0  CERIDWEN_PHOTOMETRY=cosmos_ap3    production
    poly3         CERIDWEN_CALIBRATION_ORDER=3  CERIDWEN_PHOTOMETRY=cosmos_ap3    polynomial only
    poly3_total   CERIDWEN_CALIBRATION_ORDER=3  CERIDWEN_PHOTOMETRY=cosmos_total  polynomial + Laigle+16 total SED
    mock_tilt4_baseline / mock_tilt4_poly3
                  M5_172669 mock (stored truth, 4 percent end-to-end tilt on the
                  spectrum only), without and with the polynomial

Results land in ``results/calibration-polynomial-dr2/<arm>/<object>-<target>/``
with the same files as the production run.  The instance is destroyed at the
end, also on failure, and the spend is recorded in
``results/calibration-polynomial-dr2/vast_run_<timestamp>.json``.

Sub-commands::

    plan                          show the offer and the cells
    run                           rent, prepare, launch, poll, pull, destroy
    attach  --instance ID         launch/poll/pull/destroy on a prepared box
    pull    --instance ID         pull results from a running box
    remote  --cells FILE          (on the box) run the cells sequentially
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shlex
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS = "results/calibration-polynomial-dr2"
DEFAULT_TARGETS = [
    # spect_id: spans catalogue S/N 6.6-105 and z 0.60-0.98 of the DR2 quiescent sample
    "M12_98104", "M5_173928", "M12_185653", "M4_108989", "M1_206545", "M5_172669",
]
ARMS = {
    "baseline": {"CERIDWEN_CALIBRATION_ORDER": "0", "CERIDWEN_PHOTOMETRY": "cosmos_ap3"},
    "poly3": {"CERIDWEN_CALIBRATION_ORDER": "3", "CERIDWEN_PHOTOMETRY": "cosmos_ap3"},
    "poly3_total": {"CERIDWEN_CALIBRATION_ORDER": "3", "CERIDWEN_PHOTOMETRY": "cosmos_total"},
}
MOCK_ENV = {
    "CERIDWEN_MOCK_TRUTH": "results/absorption-mask/truth_M5_172669.json",
    "CERIDWEN_MOCK_TILT": "0.04",
    "CERIDWEN_MOCK_SEED": "1",
    "CERIDWEN_PHOTOMETRY": "cosmos_ap3",
}
MOCK_ARMS = {
    "mock_tilt4_baseline": {**MOCK_ENV, "CERIDWEN_CALIBRATION_ORDER": "0"},
    "mock_tilt4_poly3": {**MOCK_ENV, "CERIDWEN_CALIBRATION_ORDER": "3"},
}
POLL_SECONDS = 120
PULL_SECONDS = 900
RUN_TIMEOUT_SECONDS = 12 * 3600
RUNNER_PATTERN = "scripts/calibration_arms_vast.py remote"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PROJECT_ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _log(prefix: str):
    def log(message: str) -> None:
        stamp = datetime.now(UTC).strftime("%H:%M:%S")
        print(f"[{stamp}] {prefix}: {message}", flush=True)
    return log


# ---------------------------------------------------------------------------
# Cells
# ---------------------------------------------------------------------------
def build_cells(targets: list[str], arms: list[str], mocks: bool) -> list[dict]:
    multi = _load("multi_gpu", "run_ceridwen_vast_multi_gpu.py")
    manifest = multi.build_target_manifest(num_shards=1, base_seed=multi.DEFAULT_BASE_SEED)
    by_id = {t["spect_id"]: t for t in manifest["targets"]}
    missing = [t for t in targets if t not in by_id]
    if missing:
        raise SystemExit(f"targets not in the DR2 quiescent manifest: {missing}")
    cells = []
    if mocks:
        for arm, env in MOCK_ARMS.items():
            target = by_id["M5_172669"]
            cells.append(dict(name=f"{arm}/M5_172669", arm=arm, target="M5_172669",
                              object_id=target["object_id"], seed=target["seed"], env=env))
    for spect_id in targets:                     # arms interleaved per galaxy
        target = by_id[spect_id]
        for arm in arms:
            cells.append(dict(name=f"{arm}/{spect_id}", arm=arm, target=spect_id,
                              object_id=target["object_id"], seed=target["seed"],
                              env=ARMS[arm]))
    return cells


# ---------------------------------------------------------------------------
# Remote runner (executes on the Vast box)
# ---------------------------------------------------------------------------
def command_remote(args) -> int:
    cells = json.loads(Path(args.cells).read_text())
    root = PROJECT_ROOT / RESULTS
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / "arms_manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    log = _log("remote")

    def write():
        tmp = manifest_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(manifest, indent=1))
        tmp.replace(manifest_path)

    for cell in cells:
        name = cell["name"]
        result_dir = root / cell["arm"] / f"{cell['object_id']}-{cell['target']}"
        if (result_dir / "ceridwen_derived_outputs.h5").exists() and \
                manifest.get(name, {}).get("status") == "done":
            log(f"{name}: already done")
            continue
        manifest[name] = {"status": "running", "started": datetime.now(UTC).isoformat()}
        write()
        env = {**os.environ, **cell["env"]}
        if "CERIDWEN_MOCK_TRUTH" in env:
            env["CERIDWEN_MOCK_TRUTH"] = str(PROJECT_ROOT / env["CERIDWEN_MOCK_TRUTH"])
        command = [
            sys.executable, str(PROJECT_ROOT / "scripts/run_ceridwen_vast_multi_gpu.py"),
            "--num-shards", "1", "--shard-index", "0", "--only-target", cell["target"],
            "--output-root", str(root / cell["arm"]), "--max-attempts", "1",
        ]
        started = time.monotonic()
        log(f"{name}: start {cell['env']}")
        completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env)
        wall = time.monotonic() - started
        manifest[name].update(
            status="done" if completed.returncode == 0 else "failed",
            returncode=completed.returncode, wall_s=round(wall, 1),
            finished=datetime.now(UTC).isoformat(),
        )
        write()
        log(f"{name}: {manifest[name]['status']} in {wall / 60:.1f} min")
    return 0 if all(v.get("status") == "done" for v in manifest.values()) else 1


# ---------------------------------------------------------------------------
# Local driver
# ---------------------------------------------------------------------------
def _sweep():
    return _load("vast_sweep", "sweep_ceridwen_vast_gpus.py")


def offers_rtx_5060(sweep, exclude_hosts: set[int]) -> list[dict]:
    query = ("gpu_name=RTX_5060 verified=true rentable=true num_gpus=1 "
             "inet_down>200 disk_space>=40 reliability>0.98")
    offers = sweep._vastai_json(["search", "offers", query, "-o", "dph"])
    offers = [
        o for o in offers
        if (o.get("inet_down_cost") or 0) <= sweep.MAX_INET_COST_USD_PER_TB
        and float(o.get("gpu_ram") or 0) >= 8000
        and float(o.get("cuda_max_good") or 0) >= 12.6
        and int(o.get("host_id") or 0) not in exclude_hosts
    ]
    offers.sort(key=lambda o: o["dph_total"])
    return offers


def _describe(offer: dict) -> str:
    return (f"offer {offer['id']} {offer['gpu_name']} ${offer['dph_total']:.4f}/h "
            f"{offer.get('geolocation')} host {offer.get('host_id')} "
            f"rel {offer.get('reliability2', 0):.3f}")


def _remote_manifest(sweep, instance_id: int) -> dict:
    path = f"{sweep.REMOTE_ROOT}/{RESULTS}/arms_manifest.json"
    result = sweep._ssh(instance_id, f"cat {shlex.quote(path)} 2>/dev/null || echo '{{}}'",
                        timeout=60.0, check=False)
    try:
        return json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return {}


def _runner_alive(sweep, instance_id: int) -> bool:
    probe = sweep._ssh(
        instance_id,
        f"pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo yes || echo no",
        timeout=60.0, check=False)
    return "yes" in probe.stdout


def _pull(sweep, instance_id: int, log) -> None:
    target, port = sweep._ssh_target(instance_id)
    local = PROJECT_ROOT / RESULTS
    local.mkdir(parents=True, exist_ok=True)
    shell = " ".join(shlex.quote(part) for part in ["ssh", *sweep._ssh_options(port)])
    log("pulling results")
    result = subprocess.run(
        ["rsync", "-a", "-e", shell, "--exclude=*.pkl", "--exclude=*.tmp",
         f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/", f"{local}/"],
        check=False, capture_output=True, text=True, timeout=1800.0,
    )
    if result.returncode != 0:
        raise sweep.SweepError(f"pull failed: {(result.stderr or result.stdout)[-400:]}")


def _launch(sweep, instance_id: int, log) -> None:
    remote = sweep.REMOTE_ROOT
    command = (
        f"cd {shlex.quote(remote)} && mkdir -p {RESULTS} && "
        f"setsid -f .venv-ceridwen-gpu/bin/python scripts/calibration_arms_vast.py remote "
        f"--cells {RESULTS}/cells.json > {RESULTS}/arms.log 2>&1 < /dev/null; "
        f"sleep 2; pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo launched"
    )
    result = sweep._ssh(instance_id, command, timeout=60.0)
    if "launched" not in result.stdout:
        raise sweep.SweepError("the remote runner did not start")
    log("launched the remote runner")


def _prepare(sweep, instance_id: int, args, cells: list[dict], log) -> None:
    absorption = _load("absorption_mask_vast", "absorption_mask_vast.py")
    sweep._wait_for_running(instance_id, log)
    sweep._attach_ssh_key(instance_id)
    sweep._wait_for_ssh(instance_id, log)
    absorption._checkout(instance_id, args.branch, log)      # clone + submodule trees
    sweep._upload_inputs(instance_id, log)
    target, port = sweep._ssh_target(instance_id)
    local_cells = PROJECT_ROOT / RESULTS / "cells.json"
    local_cells.parent.mkdir(parents=True, exist_ok=True)
    local_cells.write_text(json.dumps(cells, indent=1))
    sweep._ssh(instance_id, f"mkdir -p {shlex.quote(sweep.REMOTE_ROOT)}/{RESULTS}", timeout=60.0)
    sweep._rsync(port, str(local_cells), f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/cells.json",
                 timeout=120.0)
    sweep._bootstrap(instance_id, log)
    sweep._verify_cuda_backend(instance_id, log)


def _credit(sweep) -> float:
    return float(sweep._vastai_json(["show", "user"]).get("credit", 0.0))


def run_instance(sweep, offer, args, cells, record: dict, instance_id: int | None = None) -> None:
    log = _log("calibration arms")
    started = time.monotonic()
    last_pull = time.monotonic()
    try:
        if instance_id is None:
            instance_id = sweep._create_instance(offer, args)
            record["instance_id"] = instance_id
            log(f"rented instance {instance_id}: {_describe(offer)}")
            _prepare(sweep, instance_id, args, cells, log)
        else:
            record["instance_id"] = instance_id
            log(f"attached to instance {instance_id}")
        if _runner_alive(sweep, instance_id):
            log("a runner is already active; not launching another")
        else:
            _launch(sweep, instance_id, log)
        expected = [c["name"] for c in cells]
        while time.monotonic() - started < RUN_TIMEOUT_SECONDS:
            time.sleep(POLL_SECONDS)
            manifest = _remote_manifest(sweep, instance_id)
            done = [n for n in expected if manifest.get(n, {}).get("status") == "done"]
            failed = [n for n in expected if manifest.get(n, {}).get("status") == "failed"]
            running = [n for n in expected if manifest.get(n, {}).get("status") == "running"]
            spend = record["credit_before"] - _credit(sweep)
            record["spend_so_far_usd"] = round(spend, 4)
            log(f"{len(done)}/{len(expected)} done, {len(failed)} failed, running {running}; "
                f"spend ${spend:.3f} of cap ${args.spend_cap:.2f}")
            if spend >= args.spend_cap:
                record["error"] = f"spend cap ${args.spend_cap:.2f} reached"
                log(record["error"])
                break
            if not _runner_alive(sweep, instance_id):
                log("runner has exited" if len(done) == len(expected)
                    else "runner exited before every cell finished")
                break
            if time.monotonic() - last_pull > PULL_SECONDS:
                _pull(sweep, instance_id, log)
                last_pull = time.monotonic()
        _pull(sweep, instance_id, log)
        record["manifest"] = _remote_manifest(sweep, instance_id)
    except Exception as error:  # noqa: BLE001 - always destroy, then report
        record["error"] = f"{type(error).__name__}: {error}"
        log(f"failed: {record['error']}")
        if instance_id is not None:
            try:
                _pull(sweep, instance_id, log)
            except Exception as pull_error:  # noqa: BLE001
                log(f"pull failed: {pull_error}")
    finally:
        if instance_id is not None and not args.keep_instance:
            sweep._destroy(instance_id, log)


def _finish(sweep, record: dict, args) -> int:
    record["credit_after"] = _credit(sweep)
    record["spent_usd"] = round(record["credit_before"] - record["credit_after"], 4)
    record["finished"] = datetime.now(UTC).isoformat(timespec="seconds")
    record["instances_left"] = [
        int(i["id"]) for i in sweep._vastai_json(["show", "instances"])
        if int(i["id"]) == record.get("instance_id")
    ]
    out = PROJECT_ROOT / RESULTS / f"vast_run_{record['finished'].replace(':', '')}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=1))
    print(json.dumps({k: record.get(k) for k in ("instance_id", "spent_usd", "instances_left", "error")}, indent=1))
    statuses = [v.get("status") for v in record.get("manifest", {}).values()]
    return 0 if statuses and all(s == "done" for s in statuses) and not record["instances_left"] else 1


def command_plan(args) -> int:
    sweep = _sweep()
    for offer in offers_rtx_5060(sweep, set())[:5]:
        print(_describe(offer))
    for cell in build_cells(args.targets, args.arms, not args.no_mocks):
        print(cell["name"], cell["seed"], cell["env"])
    return 0


def command_run(args) -> int:
    sweep = _sweep()
    busy_hosts = {int(i.get("host_id") or 0) for i in sweep._vastai_json(["show", "instances"])}
    offers = offers_rtx_5060(sweep, busy_hosts | {int(h) for h in args.exclude_host})
    if not offers:
        print("no suitable RTX 5060 offer", file=sys.stderr)
        return 1
    cells = build_cells(args.targets, args.arms, not args.no_mocks)
    offer = offers[0]
    record = {
        "started": datetime.now(UTC).isoformat(timespec="seconds"),
        "branch": args.branch,
        "offer": {k: offer.get(k) for k in ("id", "gpu_name", "dph_total", "geolocation", "host_id")},
        "cells": [c["name"] for c in cells],
        "credit_before": _credit(sweep),
    }
    run_instance(sweep, offer, args, cells, record)
    return _finish(sweep, record, args)


def command_attach(args) -> int:
    sweep = _sweep()
    cells = build_cells(args.targets, args.arms, not args.no_mocks)
    record = {"started": datetime.now(UTC).isoformat(timespec="seconds"), "branch": args.branch,
              "cells": [c["name"] for c in cells], "credit_before": _credit(sweep)}
    run_instance(sweep, None, args, cells, record, instance_id=args.instance)
    return _finish(sweep, record, args)


def command_pull(args) -> int:
    sweep = _sweep()
    _pull(sweep, args.instance, _log("pull"))
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--targets", nargs="+", default=DEFAULT_TARGETS, metavar="SPECT_ID")
        p.add_argument("--arms", nargs="+", default=list(ARMS), choices=list(ARMS))
        p.add_argument("--no-mocks", action="store_true")
        p.add_argument("--branch", default="absorption-mask")
        p.add_argument("--image", default="vastai/base-image:cuda-12.6.3-auto")
        p.add_argument("--disk", type=int, default=40)
        p.add_argument("--spend-cap", type=float, default=1.0, help="USD; stop and destroy beyond it")
        p.add_argument("--keep-instance", action="store_true", help="do not destroy at the end")
        p.add_argument("--exclude-host", nargs="*", default=[])

    plan = sub.add_parser("plan"); common(plan); plan.set_defaults(function=command_plan)
    run = sub.add_parser("run"); common(run); run.set_defaults(function=command_run)
    attach = sub.add_parser("attach"); common(attach)
    attach.add_argument("--instance", type=int, required=True); attach.set_defaults(function=command_attach)
    pull = sub.add_parser("pull"); pull.add_argument("--instance", type=int, required=True)
    pull.set_defaults(function=command_pull)
    remote = sub.add_parser("remote"); remote.add_argument("--cells", required=True)
    remote.set_defaults(function=command_remote)
    args = parser.parse_args(argv)
    return int(args.function(args))


if __name__ == "__main__":
    sys.exit(main())
