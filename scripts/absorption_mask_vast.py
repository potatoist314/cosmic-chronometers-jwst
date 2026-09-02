#!/usr/bin/env python3
"""Rent Blackwell GPUs on Vast.ai and run the absorption-mask grid on them.

Each instance clones one branch of this repository, receives ``data/raw`` by
rsync, bootstraps the CUDA environment, and runs one shard of the grid
(``scripts/absorption_mask_grid.py run --shard k/n``) so every comparison
group stays on one boot.  Results are pulled back into
``results/absorption-mask/`` and every instance is destroyed at the end,
also on failure.

Sub-commands::

    plan     [--instances N]                 show the offers that would be rented
    run      --instances N --branch NAME     rent, run, pull, destroy
    pull     --instance ID                   pull results from a running instance
    destroy-all                              destroy every instance on the account
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
SWEEP_PATH = PROJECT_ROOT / "scripts/sweep_ceridwen_vast_gpus.py"
RESULTS = "results/absorption-mask"
BLACKWELL = ["RTX_5060", "RTX_5060Ti", "RTX_5070", "RTX_5070Ti", "RTX_5080"]
POLL_SECONDS = 90
RUN_TIMEOUT_SECONDS = 4 * 3600


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


def blackwell_offers(minimum_gpu_ram_mib: int = 8000) -> list[dict]:
    query = (
        f"gpu_name in [{','.join(BLACKWELL)}] verified=true rentable=true num_gpus=1 "
        "inet_down>200 disk_space>=40 reliability>0.98"
    )
    offers = sweep._vastai_json(["search", "offers", query, "-o", "dph"])
    # gpu_ram and cuda_max_good are not query fields; filter on the returned rows.
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
            f"{offer.get('geolocation')} host {offer.get('host_id')} "
            f"rel {offer.get('reliability2', 0):.3f}")


SUBMODULE_TREES = {
    # The ceridwen and sedpy_jax forks are private, so the box cannot clone
    # them; their committed working trees are rsynced from this machine
    # instead (the bootstrap skips its submodule update when the trees exist).
    "ceridwen": ["--exclude=.git", "--exclude=venv", "--exclude=.venv", "--exclude=*.h5",
                 "--exclude=*.pdf", "--exclude=*.png", "--exclude=.ruff_cache",
                 "--exclude=__pycache__", "--exclude=*.egg-info", "--exclude=docs"],
    "external/sedpy_jax": ["--exclude=.git", "--exclude=build", "--exclude=__pycache__",
                           "--exclude=*.egg-info"],
}


def _checkout(instance_id: int, branch: str, log) -> None:
    log(f"cloning branch {branch}")
    sweep._ssh(
        instance_id,
        " && ".join([
            "set -eu",
            "command -v rsync >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq rsync)",
            "mkdir -p /workspace && cd /workspace",
            f"rm -rf {shlex.quote(sweep.REMOTE_ROOT)}",
            f"git clone --quiet --branch {shlex.quote(branch)} {sweep.REPOSITORY_URL} {shlex.quote(sweep.REMOTE_ROOT)}",
            f"cd {shlex.quote(sweep.REMOTE_ROOT)} && git rev-parse --short HEAD",
        ]),
        timeout=900.0,
    )
    target, port = sweep._ssh_target(instance_id)
    for tree, excludes in SUBMODULE_TREES.items():
        log(f"uploading {tree} working tree")
        shell = " ".join(shlex.quote(part) for part in ["ssh", *sweep._ssh_options(port)])
        result = subprocess.run(
            ["rsync", "-a", "-e", shell, *excludes,
             f"{PROJECT_ROOT / tree}/", f"{target}:{sweep.REMOTE_ROOT}/{tree}/"],
            check=False, capture_output=True, text=True, timeout=900.0,
        )
        if result.returncode != 0:
            raise sweep.SweepError(f"rsync of {tree} failed: {(result.stderr or result.stdout)[-500:]}")
    commits = {
        tree: subprocess.run(["git", "-C", str(PROJECT_ROOT / tree), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, check=False).stdout.strip()
        for tree in SUBMODULE_TREES
    }
    sweep._ssh(instance_id,
               f"test -f {sweep.REMOTE_ROOT}/ceridwen/pyproject.toml && "
               f"test -f {sweep.REMOTE_ROOT}/external/sedpy_jax/setup.py", timeout=60.0)
    log(f"submodule trees uploaded: {commits}")


RUNNER_PATTERN = "^.venv-ceridwen-gpu/bin/python scripts/absorption_mask_grid.py"


def _launch(instance_id: int, shard: str, log, grid_name: str = "grid.json") -> None:
    # A top-level `cmd &` in the ssh command keeps the session open until the
    # runner exits (measured: 40 s timeout); `setsid -f` double-forks the
    # runner into its own session and returns at once.
    remote = sweep.REMOTE_ROOT
    command = (
        f"cd {shlex.quote(remote)} && mkdir -p {RESULTS} && "
        f"setsid -f .venv-ceridwen-gpu/bin/python scripts/absorption_mask_grid.py run "
        f"--grid {RESULTS}/{grid_name} --shard {shard} --gpu --output-root {RESULTS} "
        f"> {RESULTS}/shard_{shard.replace('/', 'of')}.log 2>&1 < /dev/null; "
        f"sleep 2; pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo launched"
    )
    result = sweep._ssh(instance_id, command, timeout=60.0)
    if "launched" not in result.stdout:
        raise sweep.SweepError(f"runner did not start for shard {shard}")
    log(f"launched shard {shard}")


def _remote_manifest(instance_id: int, shard: str) -> dict:
    path = f"{sweep.REMOTE_ROOT}/{RESULTS}/grid_manifest_shard{shard.replace('/', 'of')}.json"
    result = sweep._ssh(instance_id, f"cat {shlex.quote(path)} 2>/dev/null || echo '{{}}'",
                        timeout=60.0, check=False)
    try:
        return json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        return {}


def _runner_alive(instance_id: int) -> bool:
    probe = sweep._ssh(instance_id, f"pgrep -f {shlex.quote(RUNNER_PATTERN)} >/dev/null && echo yes || echo no",
                       timeout=60.0, check=False)
    return "yes" in probe.stdout


def _pull(instance_id: int, log) -> None:
    target, port = sweep._ssh_target(instance_id)
    local = PROJECT_ROOT / RESULTS
    local.mkdir(parents=True, exist_ok=True)
    log("pulling results")
    sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/", f"{local}/", timeout=1800.0)


def _expected_cells(shard: str, grid_name: str = "grid.json") -> list[str]:
    grid_module_path = PROJECT_ROOT / "scripts/absorption_mask_grid.py"
    spec = importlib.util.spec_from_file_location("grid", grid_module_path)
    grid = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grid)
    cells = json.loads((PROJECT_ROOT / RESULTS / grid_name).read_text())
    return [cell["name"] for cell in grid.shard_groups(cells, shard)]


def _prepare(instance_id: int, args, log) -> None:
    sweep._wait_for_running(instance_id, log)
    sweep._attach_ssh_key(instance_id)
    sweep._wait_for_ssh(instance_id, log)
    _checkout(instance_id, args.branch, log)
    sweep._upload_inputs(instance_id, log)
    target, port = sweep._ssh_target(instance_id)
    grid_name = getattr(args, "grid_name", "grid.json")
    sweep._rsync(port, f"{PROJECT_ROOT / RESULTS}/{grid_name}",
                 f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/{grid_name}", timeout=120.0)
    sweep._rsync(port, f"{PROJECT_ROOT / RESULTS}/truth_M5_172669.json",
                 f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/truth_M5_172669.json", timeout=120.0)
    if getattr(args, "seed_results", True):
        # Seed the box with cells already completed elsewhere so the runner
        # skips them.  Pulls then carry the seeded copies back, so seed only
        # when every local cell directory is final.
        sweep._rsync(port, f"{PROJECT_ROOT / RESULTS}/", f"{target}:{sweep.REMOTE_ROOT}/{RESULTS}/", timeout=900.0)
    sweep._bootstrap(instance_id, log)
    sweep._verify_cuda_backend(instance_id, log)


def run_instance(offer: dict | None, shard: str, args, outcome: dict, instance_id: int | None = None) -> None:
    """Rent (or attach to) one box, run one shard on it, pull, destroy."""
    log = _log(f"shard {shard}")
    try:
        if instance_id is None:
            instance_id = sweep._create_instance(offer, args)
            outcome["instance_id"] = instance_id
            log(f"rented instance {instance_id}: {_describe(offer)}")
            _prepare(instance_id, args, log)
        else:
            outcome["instance_id"] = instance_id
            log(f"attached to prepared instance {instance_id}")
        if _runner_alive(instance_id):
            log("a runner is already active on the box; not launching another")
        else:
            _launch(instance_id, shard, log, getattr(args, "grid_name", "grid.json"))
        expected = _expected_cells(shard, getattr(args, "grid_name", "grid.json"))
        deadline = time.monotonic() + RUN_TIMEOUT_SECONDS
        last_pull = time.monotonic()
        while time.monotonic() < deadline:
            time.sleep(POLL_SECONDS)
            manifest = _remote_manifest(instance_id, shard)
            done = [n for n in expected if manifest.get(n, {}).get("status") == "done"]
            failed = [n for n in expected if manifest.get(n, {}).get("status") == "failed"]
            running = [n for n in expected if manifest.get(n, {}).get("status") == "running"]
            log(f"{len(done)}/{len(expected)} done, {len(failed)} failed, running: {running}")
            # Stale "failed" entries from a seeded manifest are re-run, so the
            # manifest alone cannot say the shard is over: wait for the runner.
            if not _runner_alive(instance_id):
                log("runner process has exited" if len(done) == len(expected)
                    else "runner process is gone before every cell is done")
                break
            if time.monotonic() - last_pull > 900:
                _pull(instance_id, log)
                last_pull = time.monotonic()
        _pull(instance_id, log)
        outcome["manifest"] = _remote_manifest(instance_id, shard)
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
    offers = blackwell_offers()
    for offer in offers[: args.instances]:
        print(_describe(offer))
    return 0


def command_run(args) -> int:
    shards = args.only_shard or [f"{k}/{args.instances}" for k in range(args.instances)]
    busy_hosts = {int(i.get("host_id") or 0) for i in sweep._vastai_json(["show", "instances"])}
    excluded = busy_hosts | {int(h) for h in args.exclude_host}
    offers = [o for o in blackwell_offers() if int(o.get("host_id") or 0) not in excluded]
    if len(offers) < len(shards):
        print(f"only {len(offers)} suitable offers for {len(shards)} shards", file=sys.stderr)
        return 1
    credit_before = sweep._vastai_json(["show", "user"]).get("credit", 0.0)
    chosen = offers[: len(shards)]
    outcomes = [dict(shard=shard) for shard in shards]
    threads = [
        threading.Thread(target=run_instance, args=(offer, shard, args, outcomes[k]))
        for k, (offer, shard) in enumerate(zip(chosen, shards))
    ]
    for thread in threads:
        thread.start()
        time.sleep(5)
    for thread in threads:
        thread.join()
    mine = {o.get("instance_id") for o in outcomes}
    leftover = [i for i in sweep._vastai_json(["show", "instances"]) if int(i["id"]) in mine]
    credit_after = sweep._vastai_json(["show", "user"]).get("credit", 0.0)
    record = {
        "finished": datetime.now(UTC).isoformat(timespec="seconds"),
        "branch": args.branch,
        "offers": [{k: o.get(k) for k in ("id", "gpu_name", "dph_total", "geolocation", "host_id")} for o in chosen],
        "outcomes": outcomes,
        "credit_before": credit_before,
        "credit_after": credit_after,
        "spent_usd": round(credit_before - credit_after, 4),
        "instances_left": [int(i["id"]) for i in leftover],
    }
    out = PROJECT_ROOT / RESULTS / f"vast_run_{record['finished'].replace(':', '')}.json"
    out.write_text(json.dumps(record, indent=1))
    print(json.dumps({k: record[k] for k in ("spent_usd", "instances_left")}, indent=1))
    for outcome in outcomes:
        print(outcome["shard"], outcome.get("instance_id"), outcome.get("error") or "ok")
    return 1 if leftover or any(o.get("error") for o in outcomes) else 0


def command_attach(args) -> int:
    """Run one shard on an instance that is already bootstrapped."""
    outcome = {"shard": args.shard}
    run_instance(None, args.shard, args, outcome, instance_id=args.instance)
    print(json.dumps({k: v for k, v in outcome.items() if k != "manifest"}, indent=1))
    return 1 if outcome.get("error") else 0


def command_pull(args) -> int:
    _pull(args.instance, _log("pull"))
    return 0


def command_destroy_all(args) -> int:
    log = _log("destroy")
    for instance in sweep._vastai_json(["show", "instances"]):
        sweep._destroy(int(instance["id"]), log)
    print("instances left:", [int(i["id"]) for i in sweep._vastai_json(["show", "instances"])])
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--instances", type=int, default=3)
    run = sub.add_parser("run")
    run.add_argument("--instances", type=int, default=3)
    run.add_argument("--branch", default="absorption-mask")
    run.add_argument("--only-shard", action="append", help="k/n shard to run (repeatable); default: all n shards")
    run.add_argument("--grid-name", default="grid.json", help="grid file inside results/absorption-mask")
    run.add_argument("--no-seed", dest="seed_results", action="store_false", help="do not upload local results to the box")
    run.add_argument("--exclude-host", action="append", default=[], help="Vast host id to avoid")
    run.add_argument("--image", default=sweep.DEFAULT_IMAGE)
    run.add_argument("--disk", type=int, default=sweep.DEFAULT_DISK_GB)
    attach = sub.add_parser("attach")
    attach.add_argument("--instance", type=int, required=True)
    attach.add_argument("--shard", required=True, help="k/n")
    attach.add_argument("--branch", default="absorption-mask")
    pull = sub.add_parser("pull")
    pull.add_argument("--instance", type=int, required=True)
    sub.add_parser("destroy-all")
    args = parser.parse_args(argv)
    return {"plan": command_plan, "run": command_run, "attach": command_attach,
            "pull": command_pull, "destroy-all": command_destroy_all}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
