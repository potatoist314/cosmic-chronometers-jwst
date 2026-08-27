#!/usr/bin/env python3
"""Rent one Vast.ai GPU per model and run the fixed Ceridwen benchmark on it."""

from __future__ import annotations

import argparse
import json
import shlex
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/potatoist314/cosmic-chronometers-jwst.git"
REMOTE_ROOT = "/workspace/cosmic-chronometers-jwst"

# Schema-v1 published rows normalize to this schema-v2 comparison fingerprint.
# Script and allocator changes remain provenance, not workload identity.
REFERENCE_FINGERPRINT = (
    "26b63c693d339d9093e68b311df48719ee5697555522b13bf8e85dc0521735cc"
)
BENCHMARK_SCRIPT = "scripts/benchmark_ceridwen_vast.py"
BENCHMARK_SCRIPT_COMMIT = "30f3fc0"
BENCHMARK_SCRIPT_SHA256 = (
    "1fb69b1c89ec54afb82383d75991c8b801f7afa99a756bbb75c98b20e400fd75"
)

DEFAULT_IMAGE = "vastai/pytorch:cuda-12.8.1-auto"
DEFAULT_DISK_GB = 40
DEFAULT_BATCH_SIZE = 3
DEFAULT_ATTEMPTS = 2
DESTROY_ATTEMPTS = 3
BENCHMARK_GPU_MEMORY_MIB = 6000

MAX_INET_COST_USD_PER_TB = 5.0
MARKET_RATE_MULTIPLE = 1.3
MINIMUM_RELIABILITY = 0.98
MINIMUM_GPU_RAM_MIB = 8000
MINIMUM_DISK_GB = 40.0
MINIMUM_CUDA_VERSION = 12.8
MINIMUM_COMPUTE_CAPABILITY = 700
MINIMUM_DIRECT_PORTS = 2

ESTIMATED_HOURS_PER_RUN = 0.35
RUNNING_TIMEOUT_SECONDS = 900
SSH_TIMEOUT_SECONDS = 600
SSH_POLL_SECONDS = 15
BOOTSTRAP_TIMEOUT_SECONDS = 3600
BENCHMARK_TIMEOUT_SECONDS = 3600

# Already measured with this workload; the sweep covers everything else.
BENCHMARKED_GPU_NAMES = (
    "A100 SXM4",
    "H100 SXM",
    "RTX 3060",
    "RTX 3080 Ti",
    "RTX 3090",
    "RTX 4070S",
    "RTX 4090",
    "Tesla V100",
)


class SweepError(RuntimeError):
    """Report an unusable offer, instance, or remote command."""


@dataclass
class RunRecord:
    """Hold one GPU model's outcome across its offer attempts."""

    gpu_name: str
    status: str = "pending"
    attempts: list[dict[str, Any]] = field(default_factory=list)
    offer_id: int | None = None
    instance_id: int | None = None
    vast_host: int | None = None
    price_usd_per_hour: float | None = None
    result_directory: str | None = None
    comparison_fingerprint: str | None = None
    comparable: bool | None = None
    likelihood_calls_per_second: float | None = None
    cost_per_100k_likelihood_calls_usd: float | None = None
    rented_seconds: float | None = None
    estimated_spend_usd: float | None = None
    failure_stage: str | None = None
    failure_detail: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {key: value for key, value in vars(self).items()}


def _vastai(arguments: list[str], timeout: float = 180.0) -> str:
    command = ["vastai", *arguments]
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise SweepError(f"{shlex.join(command)} failed: {detail}")
    return result.stdout


def _vastai_json(arguments: list[str], timeout: float = 180.0) -> Any:
    output = _vastai([*arguments, "--raw"], timeout=timeout)
    start = min(
        (index for index in (output.find("["), output.find("{")) if index >= 0),
        default=-1,
    )
    if start < 0:
        raise SweepError(f"vastai returned no JSON: {output.strip()[:200]}")
    return json.loads(output[start:])


def search_offers(extra_query: str = "") -> list[dict[str, Any]]:
    """Return every rentable single-GPU offer Vast currently lists."""
    query = f"num_gpus=1 rentable=true {extra_query}".strip()
    offers = _vastai_json(["search", "offers", query, "--limit", "5000"])
    if not isinstance(offers, list):
        raise SweepError("vastai search offers did not return a list")
    return offers


def offer_satisfies_constraints(offer: dict[str, Any]) -> bool:
    """Report whether one offer meets the sweep's cost and capability rules."""
    return (
        offer.get("rentable", False)
        and offer.get("verification") == "verified"
        and float(offer.get("reliability2", 0.0)) > MINIMUM_RELIABILITY
        and float(offer.get("internet_down_cost_per_tb", float("inf")))
        <= MAX_INET_COST_USD_PER_TB
        and float(offer.get("internet_up_cost_per_tb", float("inf")))
        <= MAX_INET_COST_USD_PER_TB
        and float(offer.get("gpu_ram", 0.0)) >= MINIMUM_GPU_RAM_MIB
        and float(offer.get("disk_space", 0.0)) >= MINIMUM_DISK_GB
        and float(offer.get("cuda_max_good", 0.0)) >= MINIMUM_CUDA_VERSION
        and int(offer.get("compute_cap", 0)) >= MINIMUM_COMPUTE_CAPABILITY
        and int(offer.get("direct_port_count", 0)) >= MINIMUM_DIRECT_PORTS
    )


def market_rate_usd_per_hour(offers: list[dict[str, Any]]) -> float:
    """Return the median hourly price across every listed offer for one model."""
    if not offers:
        raise SweepError("cannot take a market rate from an empty offer list")
    return statistics.median(float(offer["dph_total"]) for offer in offers)


def rank_offers_for_gpu(
    offers: list[dict[str, Any]],
    gpu_name: str,
) -> list[dict[str, Any]]:
    """Rank one model's usable offers, cheapest first, near the market rate.

    The market rate comes from every listed offer for the model, not from the
    filtered subset, so a model whose cheap offers all fail the cost rules is
    still measured against its real price.
    """
    model_offers = [offer for offer in offers if offer.get("gpu_name") == gpu_name]
    if not model_offers:
        return []
    ceiling = MARKET_RATE_MULTIPLE * market_rate_usd_per_hour(model_offers)
    usable = [
        offer
        for offer in model_offers
        if offer_satisfies_constraints(offer) and float(offer["dph_total"]) <= ceiling
    ]
    return sorted(usable, key=lambda offer: float(offer["dph_total"]))


def untested_gpu_queue(
    offers: list[dict[str, Any]],
    benchmarked: tuple[str, ...] = BENCHMARKED_GPU_NAMES,
) -> list[tuple[str, dict[str, Any]]]:
    """Return each unmeasured model with its best offer, cheapest model first."""
    queue = []
    for gpu_name in sorted({offer["gpu_name"] for offer in offers}):
        if gpu_name in benchmarked:
            continue
        ranked = rank_offers_for_gpu(offers, gpu_name)
        if ranked:
            queue.append((gpu_name, ranked[0]))
    return sorted(queue, key=lambda entry: float(entry[1]["dph_total"]))


def split_batches(
    names: list[str],
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> list[list[str]]:
    """Split the queue into fixed-size batches, the last one possibly short."""
    if batch_size < 1:
        raise SweepError("batch size must be at least one")
    return [
        names[start : start + batch_size]
        for start in range(0, len(names), batch_size)
    ]


def estimate_batch_cost_usd(
    offers: list[dict[str, Any]],
    hours: float = ESTIMATED_HOURS_PER_RUN,
) -> float:
    """Estimate what one batch of offers costs to rent for the benchmark."""
    return sum(float(offer["dph_total"]) * hours for offer in offers)


def _ssh_target(instance_id: int) -> tuple[str, str]:
    url = _vastai(["ssh-url", str(instance_id)]).strip()
    remainder = url.removeprefix("ssh://")
    credentials, _, address = remainder.rpartition("@")
    host, _, port = address.partition(":")
    if not host or not port:
        raise SweepError(f"could not parse the ssh url: {url}")
    return f"{credentials or 'root'}@{host}", port


def _ssh(
    instance_id: int,
    command: str,
    timeout: float,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    target, port = _ssh_target(instance_id)
    result = subprocess.run(
        [
            "ssh",
            "-p",
            port,
            "-o",
            "StrictHostKeyChecking=accept-new",
            "-o",
            "UserKnownHostsFile=/dev/null",
            "-o",
            "LogLevel=ERROR",
            "-o",
            "ConnectTimeout=20",
            target,
            command,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise SweepError("\n".join(detail[-20:]) or "remote command failed")
    return result


def _instance_state(instance_id: int) -> dict[str, Any]:
    payload = _vastai_json(["show", "instance", str(instance_id)])
    if isinstance(payload, list):
        return payload[0] if payload else {}
    return payload


def _wait_for_running(instance_id: int, log: Any) -> None:
    deadline = time.monotonic() + RUNNING_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        state = _instance_state(instance_id)
        status = state.get("actual_status")
        if status == "running":
            return
        if status in {"exited", "offline"}:
            raise SweepError(f"instance entered status {status!r} before running")
        log(f"waiting for instance {instance_id}: status={status}")
        time.sleep(SSH_POLL_SECONDS)
    raise SweepError("instance did not reach the running status in time")


def _wait_for_ssh(instance_id: int, log: Any) -> None:
    deadline = time.monotonic() + SSH_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            probe = _ssh(instance_id, "true", timeout=60.0, check=False)
        except (SweepError, subprocess.TimeoutExpired):
            probe = None
        if probe is not None and probe.returncode == 0:
            return
        log(f"waiting for ssh on instance {instance_id}")
        time.sleep(SSH_POLL_SECONDS)
    raise SweepError("ssh did not become available in time")


def _prepare_checkout(instance_id: int, log: Any) -> None:
    log("cloning the project and pinning the benchmark script")
    _ssh(
        instance_id,
        " && ".join(
            [
                "set -eu",
                "mkdir -p /workspace",
                "cd /workspace",
                f"rm -rf {shlex.quote(REMOTE_ROOT)}",
                f"git clone --quiet {REPOSITORY_URL} {shlex.quote(REMOTE_ROOT)}",
                f"cd {shlex.quote(REMOTE_ROOT)}",
                "git submodule update --init --quiet ceridwen",
                f"git checkout --quiet {BENCHMARK_SCRIPT_COMMIT} -- {BENCHMARK_SCRIPT}",
                f'test "$(sha256sum {BENCHMARK_SCRIPT} | cut -d" " -f1)"'
                f" = {BENCHMARK_SCRIPT_SHA256}",
            ]
        ),
        timeout=900.0,
    )


def _upload_inputs(instance_id: int, log: Any) -> None:
    log("uploading data/raw")
    _vastai(
        [
            "copy",
            f"local:{PROJECT_ROOT / 'data/raw'}",
            f"C.{instance_id}:{REMOTE_ROOT}/data/",
        ],
        timeout=1800.0,
    )


def _bootstrap(instance_id: int, log: Any) -> None:
    log("bootstrapping the CUDA environment")
    _ssh(
        instance_id,
        f"cd {shlex.quote(REMOTE_ROOT)} && "
        f"CERIDWEN_MIN_GPU_MEMORY_MIB={BENCHMARK_GPU_MEMORY_MIB} "
        "bash scripts/bootstrap_vast_ai.sh",
        timeout=BOOTSTRAP_TIMEOUT_SECONDS,
    )


def _run_benchmark(
    instance_id: int,
    offer: dict[str, Any],
    log: Any,
) -> dict[str, Any]:
    log("running the fixed benchmark")
    _ssh(
        instance_id,
        f"cd {shlex.quote(REMOTE_ROOT)} && "
        f".venv-ceridwen-gpu/bin/python {BENCHMARK_SCRIPT} run "
        f"--price-usd-per-hour {float(offer['dph_total'])!r} "
        f"--vast-host {int(offer['host_id'])} "
        f"--vast-instance {instance_id}",
        timeout=BENCHMARK_TIMEOUT_SECONDS,
    )
    listing = _ssh(
        instance_id,
        f"ls -1 {shlex.quote(REMOTE_ROOT)}/results",
        timeout=120.0,
    ).stdout.split()
    if len(listing) != 1:
        raise SweepError(f"expected one result directory, found {listing}")
    name = listing[0]
    record = json.loads(
        _ssh(
            instance_id,
            f"cat {shlex.quote(f'{REMOTE_ROOT}/results/{name}/benchmark.json')}",
            timeout=120.0,
        ).stdout
    )
    record["result_directory"] = name
    return record


def _download_result(instance_id: int, name: str, log: Any) -> None:
    log(f"downloading {name}")
    results_root = PROJECT_ROOT / "results"
    destination = results_root / name
    if destination.exists():
        raise SweepError(f"result directory already exists: {destination}")
    _vastai(
        [
            "copy",
            f"C.{instance_id}:{REMOTE_ROOT}/results/{name}",
            f"local:{results_root}",
        ],
        timeout=1800.0,
    )
    if not (destination / "benchmark.json").is_file():
        raise SweepError(f"the copied result is incomplete: {destination}")


def _instance_exists(instance_id: int) -> bool:
    instances = _vastai_json(["show", "instances"])
    return any(int(entry["id"]) == instance_id for entry in instances)


def _destroy(instance_id: int, log: Any) -> None:
    """Destroy the instance and confirm it is gone, so a rental cannot leak.

    ``vastai destroy instance`` prompts for confirmation and exits zero when it
    reads no answer, so a return code alone does not prove the rental ended.
    """
    for _ in range(DESTROY_ATTEMPTS):
        try:
            _vastai(["destroy", "instance", str(instance_id), "--yes"])
            if not _instance_exists(instance_id):
                log(f"destroyed instance {instance_id}")
                return
        except SweepError as error:
            log(f"destroy attempt failed for {instance_id}: {error}")
        time.sleep(SSH_POLL_SECONDS)
    log(f"LEAKED INSTANCE {instance_id}: destroy it manually, it is still billing")


def _create_instance(offer: dict[str, Any], args: argparse.Namespace) -> int:
    slug = str(offer["gpu_name"]).lower().replace(" ", "-")
    payload = _vastai_json(
        [
            "create",
            "instance",
            str(offer["id"]),
            "--image",
            args.image,
            "--disk",
            str(args.disk),
            "--ssh",
            "--direct",
            "--cancel-unavail",
            "--label",
            f"ceridwen-bench-{slug}",
        ],
        timeout=300.0,
    )
    if not payload.get("success", False):
        raise SweepError(f"vastai refused the rental: {payload}")
    return int(payload["new_contract"])


def _measure_offer(
    offer: dict[str, Any],
    args: argparse.Namespace,
    log: Any,
) -> dict[str, Any]:
    started = time.monotonic()
    instance_id = _create_instance(offer, args)
    log(f"rented instance {instance_id} at ${float(offer['dph_total']):.4f}/h")
    try:
        _wait_for_running(instance_id, log)
        _wait_for_ssh(instance_id, log)
        _prepare_checkout(instance_id, log)
        _upload_inputs(instance_id, log)
        _bootstrap(instance_id, log)
        record = _run_benchmark(instance_id, offer, log)
        _download_result(instance_id, record["result_directory"], log)
    finally:
        _destroy(instance_id, log)
    record["instance_id"] = instance_id
    record["rented_seconds"] = time.monotonic() - started
    return record


def measure_gpu(
    gpu_name: str,
    offers: list[dict[str, Any]],
    args: argparse.Namespace,
) -> RunRecord:
    """Benchmark one GPU model, retrying with the next-best offer on failure."""

    def log(message: str) -> None:
        print(f"[{gpu_name}] {message}", flush=True)

    run = RunRecord(gpu_name=gpu_name)
    ranked = rank_offers_for_gpu(offers, gpu_name)
    if not ranked:
        run.status = "unavailable"
        run.failure_stage = "select_offer"
        run.failure_detail = "no offer satisfies the sweep constraints"
        log("no offer satisfies the sweep constraints")
        return run

    for offer in ranked[: args.attempts]:
        run.offer_id = int(offer["id"])
        run.vast_host = int(offer["host_id"])
        run.price_usd_per_hour = float(offer["dph_total"])
        try:
            record = _measure_offer(offer, args, log)
        except (SweepError, subprocess.TimeoutExpired, OSError) as error:
            detail = str(error).strip()[-1500:]
            run.attempts.append({"offer_id": int(offer["id"]), "error": detail})
            log(f"attempt failed: {detail.splitlines()[-1] if detail else error!r}")
            continue

        timings = record["timings"]
        run.status = "complete"
        run.instance_id = record["instance_id"]
        run.result_directory = record["result_directory"]
        run.comparison_fingerprint = record["comparison_fingerprint"]
        run.comparable = record["comparison_fingerprint"] == REFERENCE_FINGERPRINT
        run.likelihood_calls_per_second = timings["likelihood_calls_per_second"]
        run.cost_per_100k_likelihood_calls_usd = timings[
            "cost_per_100k_likelihood_calls_usd"
        ]
        run.rented_seconds = record["rented_seconds"]
        run.estimated_spend_usd = (
            run.price_usd_per_hour * record["rented_seconds"] / 3600.0
        )
        log(
            f"{timings['likelihood_calls_per_second']:.1f} calls/s, "
            f"${run.estimated_spend_usd:.3f} spent"
            + ("" if run.comparable else "  WARNING: fingerprint mismatch")
        )
        return run

    run.status = "failed"
    run.failure_stage = "measure"
    run.failure_detail = run.attempts[-1]["error"] if run.attempts else "no attempt ran"
    return run


def _manifest_path(args: argparse.Namespace) -> Path:
    date = datetime.now(UTC).date().isoformat()
    return args.output_root.resolve() / f"ceridwen_vast_gpu_sweep_manifest_{date}.json"


def _merge_manifest(path: Path, runs: list[RunRecord]) -> dict[str, Any]:
    manifest: dict[str, Any] = {"schema_version": 1, "runs": {}}
    if path.is_file():
        manifest = json.loads(path.read_text(encoding="utf-8"))
    for run in runs:
        manifest["runs"][run.gpu_name] = run.as_dict()
    manifest["updated_at_utc"] = datetime.now(UTC).isoformat()
    manifest["reference_fingerprint"] = REFERENCE_FINGERPRINT
    manifest["total_estimated_spend_usd"] = sum(
        float(entry.get("estimated_spend_usd") or 0.0)
        for entry in manifest["runs"].values()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def command_plan(args: argparse.Namespace) -> int:
    offers = search_offers()
    queue = untested_gpu_queue(offers)
    manifest_path = _manifest_path(args)
    done = set()
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        done = {
            name
            for name, entry in manifest["runs"].items()
            if entry.get("status") == "complete"
        }
    remaining = [(name, offer) for name, offer in queue if name not in done]
    batches = split_batches([name for name, _ in remaining], args.batch_size)
    by_name = dict(remaining)

    print(f"{len(offers)} listed offers, {len(remaining)} unmeasured models")
    if done:
        print(f"already complete: {', '.join(sorted(done))}")
    print()
    running = 0.0
    for index, batch in enumerate(batches, start=1):
        cost = estimate_batch_cost_usd([by_name[name] for name in batch])
        running += cost
        print(f"batch {index}  ~${cost:.2f}  (cumulative ~${running:.2f})")
        for name in batch:
            offer = by_name[name]
            print(
                f"    {name:18s} ${float(offer['dph_total']):7.4f}/h  "
                f"{float(offer['gpu_ram']) / 1024:5.1f} GB  cc{offer['compute_cap']}  "
                f"${float(offer['internet_down_cost_per_tb']):.2f}/"
                f"${float(offer['internet_up_cost_per_tb']):.2f} per TB  "
                f"host={offer['host_id']}"
            )
    print(f"\nqueue total ~${running:.2f} at {ESTIMATED_HOURS_PER_RUN} h per run")
    return 0


def command_run(args: argparse.Namespace) -> int:
    offers = search_offers()
    if args.batch:
        names = list(args.batch)
    else:
        manifest_path = _manifest_path(args)
        done = set()
        if manifest_path.is_file():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            done = {
                name
                for name, entry in manifest["runs"].items()
                if entry.get("status") == "complete"
            }
        queue = [name for name, _ in untested_gpu_queue(offers) if name not in done]
        names = queue[: args.batch_size]
    if not names:
        print("nothing left to measure")
        return 0

    listed = {offer["gpu_name"] for offer in offers}
    unknown = [name for name in names if name not in listed]
    if unknown:
        raise SweepError(f"Vast does not list these GPU names: {unknown}")

    ranked = {name: rank_offers_for_gpu(offers, name) for name in names}
    estimate = estimate_batch_cost_usd(
        [entries[0] for entries in ranked.values() if entries]
    )
    print(f"batch: {', '.join(names)}  (estimated ~${estimate:.2f})")

    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        runs = list(pool.map(lambda name: measure_gpu(name, offers, args), names))

    manifest = _merge_manifest(_manifest_path(args), runs)
    print("\nbatch report")
    for run in runs:
        if run.status == "complete":
            print(
                f"  {run.gpu_name:18s} {run.likelihood_calls_per_second:8.1f} calls/s  "
                f"${run.cost_per_100k_likelihood_calls_usd:.5f}/100k  "
                f"spent ${run.estimated_spend_usd:.3f}  "
                f"{'comparable' if run.comparable else 'FINGERPRINT MISMATCH'}"
            )
        else:
            print(f"  {run.gpu_name:18s} {run.status}: {run.failure_detail}")
    print(
        f"\nsweep spend so far: ${manifest['total_estimated_spend_usd']:.2f}\n"
        f"manifest: {_manifest_path(args)}"
    )
    return 0 if all(run.status == "complete" for run in runs) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark Ceridwen on many Vast.ai GPU models, in batches."
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "results",
        help="Parent directory for results and the sweep manifest.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="GPU models per batch. Default: 3.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser(
        "plan",
        help="list the remaining models and estimated cost without renting",
    )
    plan_parser.set_defaults(function=command_plan)

    run_parser = subparsers.add_parser("run", help="rent and benchmark one batch")
    run_parser.add_argument(
        "--batch",
        nargs="+",
        help="Vast GPU names to measure. Default: the next batch in the queue.",
    )
    run_parser.add_argument(
        "--image",
        default=DEFAULT_IMAGE,
        help=f"Vast instance image. Default: {DEFAULT_IMAGE}.",
    )
    run_parser.add_argument(
        "--disk",
        type=int,
        default=DEFAULT_DISK_GB,
        help=f"Instance disk in GB. Default: {DEFAULT_DISK_GB}.",
    )
    run_parser.add_argument(
        "--attempts",
        type=int,
        default=DEFAULT_ATTEMPTS,
        help="Offers to try per GPU model before giving up. Default: 2.",
    )
    run_parser.set_defaults(function=command_run)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.function(args))
    except SweepError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
