#!/usr/bin/env python3
"""Rent one Blackwell GPU per target on Vast.ai and run the tilt-origin arms.

Every arm of a target runs on one box, one after the other, so each target's
comparisons share one boot.  The box clones branch ``calibration-polynomial``,
receives the ``ceridwen`` and ``sedpy_jax`` working trees and ``data/raw`` by
rsync, bootstraps the CUDA environment, and runs
``scripts/tilt_origin_runner.py``.  Results are pulled into
``results/tilt-origin-2026-09-02/`` and every instance is destroyed at the
end, also on failure.

Sub-commands::

    plan                        write the arm lists and show the offers
    run  [--target T ...]       rent, run, pull, destroy
    destroy-all                 destroy every instance on the account
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shlex
import subprocess
import sys
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_CHECKOUT = Path("/Users/liuhao/Downloads/Astro project")
CERIDWEN_TREE = MAIN_CHECKOUT / "tmp/worktrees/ceridwen-calibration-polynomial"
SEDPY_TREE = MAIN_CHECKOUT / "external/sedpy_jax"
SWEEP_PATH = MAIN_CHECKOUT / "scripts/sweep_ceridwen_vast_gpus.py"
RESULTS = "results/tilt-origin-2026-09-02"
BRANCH = "calibration-polynomial"
TARGETS = ("M5_172669", "M4_108989")
BLACKWELL = ["RTX_5060", "RTX_5060Ti", "RTX_5070", "RTX_5070Ti", "RTX_5080", "RTX_5090"]
POLL_SECONDS = 90
RUN_TIMEOUT_SECONDS = 4 * 3600
RUNNER_PATTERN = "scripts/tilt_origin_runner.py"


def _load_sweep():
    spec = importlib.util.spec_from_file_location("vast_sweep", SWEEP_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sweep = _load_sweep()


def _log(prefix: str):
    def log(message: str) -> None:
        stamp = datetime.now(UTC).strftime("%H:%M:%S")
        print(f"[{stamp}] {prefix}: {message}", flush=True)
    return log


def arms(target: str) -> list[dict]:
    base = ["--target", target, "--profile", "gpu-full"]
    rows = [
        # photometry-only first: fast, and the dust-prior arm reads it
        dict(name=f"{target}_photonly_cosmos_total", args=base + ["--fit", "photometry", "--photometry", "cosmos_total"]),
        dict(name=f"{target}_photonly_ap3", args=base + ["--fit", "photometry"]),
        dict(name=f"{target}_cosmos_total_baseline", args=base + ["--photometry", "cosmos_total"]),
        dict(name=f"{target}_cosmos_total_poly3", args=base + ["--photometry", "cosmos_total", "--poly-order", "3"]),
        dict(name=f"{target}_uvista_total_baseline", args=base + ["--photometry", "uvista_total"]),
        dict(name=f"{target}_uvista_total_poly3", args=base + ["--photometry", "uvista_total", "--poly-order", "3"]),
        dict(name=f"{target}_speconly", args=base + ["--fit", "spectrum"]),
    ]
    for floor in (0.05, 0.02, 0.15):
        tag = f"ap3_floor{int(round(floor * 100)):02d}"
        rows.append(dict(name=f"{target}_{tag}_baseline", args=base + ["--phot-floor", str(floor)]))
        rows.append(dict(name=f"{target}_{tag}_poly3", args=base + ["--phot-floor", str(floor), "--poly-order", "3"]))
    rows += [
        dict(name=f"{target}_ap3_freeindex", args=base + ["--free-dust-index"]),
        dict(name=f"{target}_ap3_calzetti", args=base + ["--dust-law", "calzetti"]),
        dict(name=f"{target}_cosmos_total_poly1_dustprior", args=base + ["--photometry", "cosmos_total", "--poly-order", "1"],
             dust_prior_from=f"{target}_photonly_cosmos_total"),
    ]
    return rows


def blackwell_offers(minimum_gpu_ram_mib: int = 8000) -> list[dict]:
    query = (
        f"gpu_name in [{','.join(BLACKWELL)}] verified=true rentable=true num_gpus=1 "
        "inet_down>200 disk_space>=40 reliability>0.98"
    )
    offers = sweep._vastai_json(["search", "offers", query, "-o", "dph"])
    offers = [
        o for o in offers
        if (o.get("inet_down_cost") or 0) <= sweep.MAX_INET_COST_USD_PER_TB
        and float(o.get("gpu_ram") or 0) >= minimum_gpu_ram_mib
        and float(o.get("cuda_max_good") or 0) >= 12.6
    ]
    offers.sort(key=lambda o: o["dph_total"])
    return offers


def _describe(offer: dict) -> str:
    return (f"offer {offer['id']} {offer['gpu_name']} ${offer['dph_total']:.4f}/h "
            f"{offer.get('geolocation')} host {offer.get('host_id')} rel {offer.get('reliability2', 0):.3f}")


def _rsync_tree(port: str, source: Path, destination: str, excludes: list[str], timeout: float = 900.0) -> None:
    shell = " ".join(shlex.quote(part) for part in ["ssh", *sweep._ssh_options(port)])
    result = subprocess.run(
        ["rsync", "-a", "--copy-links", "-e", shell, *excludes, f"{source}/", destination],
        check=False, capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise sweep.SweepError(f"rsync of {source} failed: {(result.stderr or result.stdout)[-500:]}")


def _prepare(instance_id: int, args, log) -> None:
    remote = sweep.REMOTE_ROOT
    sweep._wait_for_running(instance_id, log)
    sweep._attach_ssh_key(instance_id)
    sweep._wait_for_ssh(instance_id, log)
    log(f"cloning branch {BRANCH}")
    sweep._ssh(instance_id, " && ".join([
        "set -eu",
        "command -v rsync >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq rsync)",
        "mkdir -p /workspace && cd /workspace",
        f"rm -rf {shlex.quote(remote)}",
        f"git clone --quiet --branch {BRANCH} {sweep.REPOSITORY_URL} {shlex.quote(remote)}",
        f"cd {shlex.quote(remote)} && git rev-parse --short HEAD",
    ]), timeout=900.0)
    target, port = sweep._ssh_target(instance_id)
    # The ceridwen and sedpy_jax forks are private: upload their working trees.
    log("uploading ceridwen and sedpy_jax working trees")
    _rsync_tree(port, CERIDWEN_TREE, f"{target}:{remote}/ceridwen/",
                ["--exclude=.git", "--exclude=venv", "--exclude=.venv", "--exclude=*.h5", "--exclude=*.pdf",
                 "--exclude=*.png", "--exclude=.ruff_cache", "--exclude=__pycache__", "--exclude=*.egg-info",
                 "--exclude=docs"])
    _rsync_tree(port, SEDPY_TREE, f"{target}:{remote}/external/sedpy_jax/",
                ["--exclude=.git", "--exclude=build", "--exclude=__pycache__", "--exclude=*.egg-info"])
    log("uploading data/raw")
    _rsync_tree(port, PROJECT_ROOT / "data/raw", f"{target}:{remote}/data/raw/", [], timeout=3600.0)
    counted = sweep._ssh(instance_id, f"find {shlex.quote(remote)}/data/raw/legac_dr2/sp -maxdepth 1 -type f "
                         "-name 'legac_M*_v2.0.fits' | wc -l; "
                         f"ls {shlex.quote(remote)}/data/raw/ultravista {shlex.quote(remote)}/data/raw/cosmos2015",
                         timeout=180.0).stdout.strip()
    log(f"uploaded: {counted.replace(chr(10), ' | ')}")
    if int(counted.splitlines()[0]) != sweep.EXPECTED_SPECTRUM_FILES:
        raise sweep.SweepError("spectra upload incomplete")
    sweep._ssh(instance_id, f"mkdir -p {shlex.quote(remote)}/{RESULTS}", timeout=60.0)
    sweep._rsync(port, str(PROJECT_ROOT / RESULTS / f"arms_{args.target}.json"),
                 f"{target}:{remote}/{RESULTS}/arms_{args.target}.json", timeout=120.0)
    sweep._bootstrap(instance_id, log)
    sweep._verify_cuda_backend(instance_id, log)


def _launch(instance_id: int, target_name: str, log) -> None:
    remote = sweep.REMOTE_ROOT
    command = (
        f"cd {shlex.quote(remote)} && "
        f"JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 LD_LIBRARY_PATH= setsid -f .venv-ceridwen-gpu/bin/python "
        f"scripts/tilt_origin_runner.py --arms {RESULTS}/arms_{target_name}.json --out-root {RESULTS} "
        f"--project-root {shlex.quote(remote)} > {RESULTS}/runner_{target_name}.log 2>&1 < /dev/null; "
        f"sleep 2; pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo launched"
    )
    result = sweep._ssh(instance_id, command, timeout=60.0)
    if "launched" not in result.stdout:
        raise sweep.SweepError(f"runner did not start for {target_name}")
    log("launched runner")


def _runner_alive(instance_id: int) -> bool:
    probe = sweep._ssh(instance_id, f"pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo yes || echo no",
                       timeout=60.0, check=False)
    return "yes" in probe.stdout


def _progress(instance_id: int) -> str:
    result = sweep._ssh(instance_id, f"tail -n 2 {sweep.REMOTE_ROOT}/{RESULTS}/progress.log 2>/dev/null; "
                        f"test -f {sweep.REMOTE_ROOT}/{RESULTS}/ALL_DONE && echo ALL_DONE", timeout=60.0, check=False)
    return result.stdout.strip().replace("\n", " | ")


def _pull(instance_id: int, log) -> None:
    target, port = sweep._ssh_target(instance_id)
    local = PROJECT_ROOT / RESULTS
    local.mkdir(parents=True, exist_ok=True)
    log("pulling results")
    sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/", f"{local}/", timeout=1800.0)


def run_instance(offer: dict, args, outcome: dict) -> None:
    log = _log(args.target)
    instance_id = None
    try:
        instance_id = sweep._create_instance(offer, args)
        outcome["instance_id"] = instance_id
        log(f"rented instance {instance_id}: {_describe(offer)}")
        _prepare(instance_id, args, log)
        _launch(instance_id, args.target, log)
        deadline = time.monotonic() + RUN_TIMEOUT_SECONDS
        last_pull = time.monotonic()
        while time.monotonic() < deadline:
            time.sleep(POLL_SECONDS)
            status = _progress(instance_id)
            log(status or "no progress yet")
            if "ALL_DONE" in status or not _runner_alive(instance_id):
                break
            if time.monotonic() - last_pull > 900:
                _pull(instance_id, log)
                last_pull = time.monotonic()
        _pull(instance_id, log)
        outcome["progress"] = _progress(instance_id)
    except Exception as error:  # noqa: BLE001 - always destroy, then report
        outcome["error"] = f"{type(error).__name__}: {error}"
        log(f"failed: {outcome['error']}")
        if instance_id is not None:
            try:
                _pull(instance_id, log)
            except Exception as pull_error:  # noqa: BLE001
                log(f"pull failed: {pull_error}")
    finally:
        if instance_id is not None:
            sweep._destroy(instance_id, log)


def command_plan(args) -> int:
    out = PROJECT_ROOT / RESULTS
    out.mkdir(parents=True, exist_ok=True)
    for target in TARGETS:
        rows = arms(target)
        (out / f"arms_{target}.json").write_text(json.dumps(rows, indent=1) + "\n")
        print(f"{target}: {len(rows)} arms -> {out / f'arms_{target}.json'}")
    for offer in blackwell_offers()[:6]:
        print(_describe(offer))
    return 0


def command_run(args) -> int:
    targets = args.target or list(TARGETS)
    busy_hosts = {int(i.get("host_id") or 0) for i in sweep._vastai_json(["show", "instances"])}
    offers = [o for o in blackwell_offers() if int(o.get("host_id") or 0) not in busy_hosts]
    if len(offers) < len(targets):
        print(f"only {len(offers)} suitable offers for {len(targets)} targets", file=sys.stderr)
        return 1
    credit_before = sweep._vastai_json(["show", "user"]).get("credit", 0.0)
    outcomes = [dict(target=t) for t in targets]
    threads = []
    for k, target_name in enumerate(targets):
        run_args = argparse.Namespace(**vars(args), target=target_name)
        threads.append(threading.Thread(target=run_instance, args=(offers[k], run_args, outcomes[k])))
    for thread in threads:
        thread.start()
        time.sleep(5)
    for thread in threads:
        thread.join()
    mine = {o.get("instance_id") for o in outcomes}
    leftover = [int(i["id"]) for i in sweep._vastai_json(["show", "instances"]) if int(i["id"]) in mine]
    credit_after = sweep._vastai_json(["show", "user"]).get("credit", 0.0)
    record = {
        "finished": datetime.now(UTC).isoformat(timespec="seconds"), "branch": BRANCH,
        "offers": [{k: o.get(k) for k in ("id", "gpu_name", "dph_total", "geolocation", "host_id")} for o in offers[:len(targets)]],
        "outcomes": outcomes, "credit_before": credit_before, "credit_after": credit_after,
        "spent_usd": round(credit_before - credit_after, 4), "instances_left": leftover,
    }
    out = PROJECT_ROOT / RESULTS / f"vast_run_{record['finished'].replace(':', '')}.json"
    out.write_text(json.dumps(record, indent=1))
    print(json.dumps({k: record[k] for k in ("spent_usd", "instances_left")}, indent=1))
    for outcome in outcomes:
        print(outcome["target"], outcome.get("instance_id"), outcome.get("error") or outcome.get("progress"))
    return 1 if leftover or any(o.get("error") for o in outcomes) else 0


def command_destroy_all(args) -> int:
    log = _log("destroy")
    for instance in sweep._vastai_json(["show", "instances"]):
        sweep._destroy(int(instance["id"]), log)
    print("instances left:", [int(i["id"]) for i in sweep._vastai_json(["show", "instances"])])
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan")
    run = sub.add_parser("run")
    run.add_argument("--target", action="append", choices=TARGETS, help="default: both targets")
    run.add_argument("--image", default=sweep.DEFAULT_IMAGE)
    run.add_argument("--disk", type=int, default=sweep.DEFAULT_DISK_GB)
    sub.add_parser("destroy-all")
    args = parser.parse_args(argv)
    return {"plan": command_plan, "run": command_run, "destroy-all": command_destroy_all}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
