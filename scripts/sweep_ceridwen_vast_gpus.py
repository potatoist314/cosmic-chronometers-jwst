#!/usr/bin/env python3
"""Rent one Vast.ai GPU per model and run the fixed Ceridwen benchmark on it."""

from __future__ import annotations

import argparse
import json
import os
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
BENCHMARK_SCRIPT_COMMIT = "63b4296"
BENCHMARK_SCRIPT_SHA256 = (
    "6d8cf1bb1e78ce6a721618655443edcd7832bf286d0b9227f85553ba0463afcb"
)

# The bootstrap installs CUDA JAX, so avoid pulling an unused PyTorch stack.
DEFAULT_IMAGE = "vastai/base-image:cuda-12.6.3-auto"
DEFAULT_DISK_GB = 40
DEFAULT_BATCH_SIZE = 3
DEFAULT_ATTEMPTS = 3
DESTROY_ATTEMPTS = 3
VASTAI_JSON_ATTEMPTS = 3
BENCHMARK_GPU_MEMORY_MIB = 6000
SSH_KEY_PATH = Path.home() / ".ssh/id_ed25519"
EXPECTED_SPECTRUM_FILES = 1988

MAX_INET_COST_USD_PER_TB = 5.0
MARKET_RATE_MULTIPLE = 1.3
MINIMUM_RELIABILITY = 0.98
MINIMUM_GPU_RAM_MIB = 8000
MINIMUM_DISK_GB = 40.0
MINIMUM_CUDA_VERSION = 12.8

# Liu Hao's rule for every Ceridwen fit run (2026-09-23): a 5060-class card
# or better on a host above 99.5% reliability; take the cheapest available
# offer ranked by cost per unit of work (total run cost divided by the card's
# benchmark speed factor). The caps below are loose guards against a disaster,
# not targets; the per-task total spend cap is the real control.
# An interruptible (bid) rental is fine for any run under two hours.
FIT_GPU_NAMES = ("RTX 5060", "RTX 5060 Ti", "RTX 5070", "RTX 5080", "RTX 5090")
# Likelihood speed relative to the RTX 5060 Ti, from the 2026-09-23 Vast
# benchmark in results/gpu-benchmark-2026-09-23/sol/summary.json: 5070 1.33,
# 5080 2.39, 5090 4.49. Two of three 5090 hosts measured about 150,000
# calls/s (host 406325: 148,930; the diagnostic host: about 150,000 at
# batch 500 to 8,000 with the GPU 96% busy); host 213578 at 94,294 is
# treated as a bad or shared host. The RTX 5060 timing ran at commit
# 1e1f6c8 with cosmos_total photometry while the benchmark pins c869309
# (cosmos2025), so it is not comparable; Liu Hao set 0.9.
FIT_SPEED_VS_5060_TI = {
    "RTX 5060": 0.9,
    "RTX 5060 Ti": 1.00,
    "RTX 5070": 1.33,
    "RTX 5080": 2.39,
    "RTX 5090": 4.49,
}
# Either guard can be raised for one rental that Liu Hao approved by name.
FIT_MAX_DPH_USD = float(os.environ.get("CERIDWEN_FIT_MAX_DPH_USD", "0.80"))
FIT_MIN_RELIABILITY = 0.995
FIT_BID_MARGIN_USD = 0.005
FIT_MAX_INET_COST_USD_PER_TB = float(os.environ.get("CERIDWEN_FIT_MAX_INET_COST_USD_PER_TB", "25.0"))
# Total-cost ranking weights: about an hour on the box and ~6 GB down
# (image, data, bootstrap); _replacement_cost below uses the same 6 GB.
FIT_EXPECTED_HOURS = 1.0
FIT_TRANSFER_GB = 6.0
FIT_OFFER_QUERY_BASE = (f"gpu_name in [RTX_5060,RTX_5060_Ti,RTX_5070,RTX_5080,RTX_5090] verified=true rentable=true num_gpus=1 "
                        f"inet_down>200 disk_space>=40 reliability>{FIT_MIN_RELIABILITY} "
                        f"inet_down_cost<{FIT_MAX_INET_COST_USD_PER_TB / 1000}")
FIT_OFFER_QUERY = f"{FIT_OFFER_QUERY_BASE} dph<{FIT_MAX_DPH_USD}"


def fit_bid_price(offer: dict[str, Any]) -> float:
    """Interruptible bid: the host's minimum bid plus a small margin; you pay the bid."""
    return round(float(offer["min_bid"]) + FIT_BID_MARGIN_USD, 4)


def fit_offer_price(offer: dict[str, Any], *, interruptible: bool = False) -> float:
    """Hourly price: the bid for an interruptible rental, else on-demand."""
    if interruptible and "min_bid" in offer:
        return fit_bid_price(offer)
    return float(offer.get("dph_total") or 1e9)


def fit_offer_total_cost(offer: dict[str, Any], *, interruptible: bool = False,
                         hours: float = FIT_EXPECTED_HOURS,
                         transfer_gb: float = FIT_TRANSFER_GB) -> float:
    """Expected total run cost: hourly price plus bandwidth for the transfer."""
    return (fit_offer_price(offer, interruptible=interruptible) * hours
            + float(offer.get("inet_down_cost", 1e9)) * transfer_gb)


def fit_offer_cost_per_work(offer: dict[str, Any], *, interruptible: bool = False,
                            hours: float = FIT_EXPECTED_HOURS,
                            transfer_gb: float = FIT_TRANSFER_GB) -> float:
    """Ranking key: total run cost divided by the card's benchmark speed factor."""
    return (fit_offer_total_cost(offer, interruptible=interruptible,
                                 hours=hours, transfer_gb=transfer_gb)
            / FIT_SPEED_VS_5060_TI[offer["gpu_name"]])


def fit_offer_qualifies(offer: dict[str, Any], *, interruptible: bool = False) -> bool:
    """The rule above, applied to a returned row (Vast's own dph filter is not exact).

    On-demand offers are judged on ``dph_total``; interruptible ones on the bid.
    """
    return (offer.get("gpu_name") in FIT_GPU_NAMES
            and fit_offer_price(offer, interruptible=interruptible) < FIT_MAX_DPH_USD
            and float(offer.get("reliability2") or 0.0) > FIT_MIN_RELIABILITY
            and float(offer.get("inet_down_cost", 1e9)) * 1000 < FIT_MAX_INET_COST_USD_PER_TB)
MINIMUM_COMPUTE_CAPABILITY = 700
MINIMUM_DIRECT_PORTS = 2

ESTIMATED_HOURS_PER_RUN = 0.35
# Every observed successful boot finished within 5 minutes; every stalled
# host never booted at all and burned the whole window. Fail fast so the
# runner can try another offer inside the 30-minute attempt cap.
RUNNING_TIMEOUT_SECONDS = 600
SSH_TIMEOUT_SECONDS = 600
SSH_POLL_SECONDS = 15
BOOTSTRAP_TIMEOUT_SECONDS = 3600
BENCHMARK_TIMEOUT_SECONDS = 3600

# Already measured with this workload; the sweep covers everything else.
BENCHMARKED_GPU_NAMES = (
    "A10",
    "A100 PCIE",
    "A100 SXM4",
    "B200",
    "CMP 170HX",
    "H100 SXM",
    "L4",
    "RTX 3050",
    "RTX 3060",
    "RTX 3060 Ti",
    "RTX 3070",
    "RTX 3070 Ti",
    "RTX 3080",
    "RTX 3080 Ti",
    "RTX 3090",
    "RTX 3090 Ti",
    "RTX 4060 Ti",
    "RTX 4070 Ti",
    "RTX 4070S Ti",
    "RTX 4070S",
    "RTX 4080",
    "RTX 4090",
    "RTX 5000Ada",
    "RTX 5060",
    "RTX 5060 Ti",
    "RTX 5070",
    "RTX 5070 Ti",
    "RTX 5080",
    "RTX 5090",
    "RTX 6000Ada",
    "RTX A4000",
    "RTX A6000",
    "RTX PRO 4000",
    "RTX PRO 4500",
    "RTX PRO 5000",
    "RTX PRO 6000 S",
    "RTX PRO 6000 WS",
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
    """Run a vastai command and parse its JSON, retrying an empty response."""
    for attempt in range(VASTAI_JSON_ATTEMPTS):
        output = _vastai([*arguments, "--raw"], timeout=timeout)
        start = min(
            (index for index in (output.find("["), output.find("{")) if index >= 0),
            default=-1,
        )
        if start >= 0:
            return json.loads(output[start:])
        if attempt + 1 < VASTAI_JSON_ATTEMPTS:
            time.sleep(SSH_POLL_SECONDS)
    raise SweepError(f"vastai returned no JSON: {output.strip()[:200]}")


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
        names[start : start + batch_size] for start in range(0, len(names), batch_size)
    ]


def estimate_batch_cost_usd(
    offers: list[dict[str, Any]],
    hours: float = ESTIMATED_HOURS_PER_RUN,
) -> float:
    """Estimate what one batch of offers costs to rent for the benchmark."""
    return sum(float(offer["dph_total"]) * hours for offer in offers)


def _ssh_options(port: str) -> list[str]:
    """Offer only the Vast-registered key, so sshd cannot exhaust its tries."""
    return [
        "-p",
        port,
        "-i",
        str(SSH_KEY_PATH),
        "-o",
        "IdentitiesOnly=yes",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "LogLevel=ERROR",
        "-o",
        "ConnectTimeout=20",
        # Bootstrap runs for minutes without output; keep the channel alive.
        "-o",
        "ServerAliveInterval=30",
        "-o",
        "ServerAliveCountMax=20",
    ]


def _attach_ssh_key(instance_id: int) -> None:
    """Install the account key on the instance.

    A freshly created instance does not reliably carry the account key, so
    ``vastai ssh-url`` can resolve while every login is refused.
    """
    public_key = SSH_KEY_PATH.with_suffix(".pub").read_text().strip()
    _vastai(["attach", "ssh", str(instance_id), public_key])


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
        ["ssh", *_ssh_options(port), target, command],
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
                "command -v rsync >/dev/null 2>&1 || "
                "(apt-get update -qq && apt-get install -y -qq rsync)",
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


def _rsync(
    port: str,
    source: str,
    destination: str,
    timeout: float,
    mirror: bool = False,
) -> None:
    shell = " ".join(shlex.quote(part) for part in ["ssh", *_ssh_options(port)])
    command = ["rsync", "-a", "-e", shell]
    if mirror:
        command.append("--delete")
    result = subprocess.run(
        [*command, source, destination],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise SweepError("rsync failed: " + ("\n".join(detail[-10:]) or "unknown"))


def _upload_inputs(instance_id: int, log: Any, timeout: float = 3600.0) -> None:
    """Copy the LEGA-C inputs over ssh and prove they arrived.

    ``vastai copy`` reports success for a transfer that moves nothing, so the
    bootstrap used to fail its own data check instead. rsync over the ssh
    channel transfers, and the count below is the proof.
    """
    log("uploading data/raw")
    target, port = _ssh_target(instance_id)
    _ssh(instance_id, f"mkdir -p {shlex.quote(REMOTE_ROOT)}/data/raw", timeout=60)
    _rsync(
        port,
        f"{PROJECT_ROOT / 'data/raw'}/",
        f"{target}:{REMOTE_ROOT}/data/raw/",
        timeout=timeout,
        mirror=True,
    )
    counted = _ssh(
        instance_id,
        f"find {shlex.quote(REMOTE_ROOT)}/data/raw/legac_dr2/sp -maxdepth 1 "
        "-type f -name 'legac_M*_v2.0.fits' | wc -l",
        timeout=180.0,
    ).stdout.strip()
    if int(counted) != EXPECTED_SPECTRUM_FILES:
        raise SweepError(
            f"uploaded {counted} spectra, expected {EXPECTED_SPECTRUM_FILES}"
        )
    log(f"uploaded {counted} spectra")


def _bootstrap(instance_id: int, log: Any, timeout: float = BOOTSTRAP_TIMEOUT_SECONDS) -> None:
    log("bootstrapping the CUDA environment")
    result = _ssh(
        instance_id,
        f"cd {shlex.quote(REMOTE_ROOT)} && "
        f"CERIDWEN_MIN_GPU_MEMORY_MIB={BENCHMARK_GPU_MEMORY_MIB} "
        "bash scripts/bootstrap_vast_ai.sh",
        timeout=timeout,
    )
    for line in result.stdout.strip().splitlines()[-4:]:
        log(f"bootstrap: {line}")


def _verify_cuda_backend(instance_id: int, log: Any, timeout: float = 600.0) -> None:
    """Prove the benchmark interpreter sees a GPU before the benchmark runs.

    The bootstrap checks CUDA in its own shell. Checking again here, through
    the same command form the benchmark uses, catches an environment that
    passed the bootstrap and still cannot reach the GPU.
    """
    probe = (
        "import jax;"
        "print('devices', jax.devices());"
        "print('backend', jax.default_backend())"
    )
    result = _ssh(
        instance_id,
        f"cd {shlex.quote(REMOTE_ROOT)} && "
        "JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 LD_LIBRARY_PATH= "
        f".venv-ceridwen-gpu/bin/python -c {shlex.quote(probe)} 2>&1 | tail -4; "
        "df -h /workspace | tail -1",
        timeout=timeout,
        check=False,
    )
    output = result.stdout.strip()
    for line in output.splitlines():
        log(f"probe: {line}")
    if "backend gpu" not in output:
        raise SweepError(f"the benchmark interpreter has no GPU backend: {output}")


def _run_benchmark(
    instance_id: int,
    offer: dict[str, Any],
    log: Any,
) -> dict[str, Any]:
    log("running the fixed benchmark")
    completed = _ssh(
        instance_id,
        f"cd {shlex.quote(REMOTE_ROOT)} && "
        "LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
        f".venv-ceridwen-gpu/bin/python {BENCHMARK_SCRIPT} run "
        f"--price-usd-per-hour {float(offer['dph_total'])!r} "
        f"--vast-host {int(offer['host_id'])} "
        f"--vast-instance {instance_id}",
        timeout=BENCHMARK_TIMEOUT_SECONDS,
    )
    # The clone already carries committed result directories, so read the path
    # the runner reports instead of guessing which entry is new.
    saved = [
        line.split("saved:", 1)[1].strip()
        for line in completed.stdout.splitlines()
        if line.startswith("saved:")
    ]
    if len(saved) != 1:
        raise SweepError(f"the runner reported {len(saved)} saved directories")
    name = Path(saved[0]).name
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
    target, port = _ssh_target(instance_id)
    _rsync(
        port,
        f"{target}:{REMOTE_ROOT}/results/{name}",
        f"{results_root}/",
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
            _vastai(["destroy", "instance", str(instance_id), "-y"])
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
            *(["--bid_price", str(args.bid)] if getattr(args, "bid", None) else []),
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
        _attach_ssh_key(instance_id)
        _wait_for_ssh(instance_id, log)
        _prepare_checkout(instance_id, log)
        _upload_inputs(instance_id, log)
        _bootstrap(instance_id, log)
        _verify_cuda_backend(instance_id, log, timeout=left())
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
        stamp = datetime.now(UTC).strftime("%H:%M:%S")
        print(f"{stamp} [{gpu_name}] {message}", flush=True)

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


# The price comparison uses the current notebook likelihood, timed by the
# existing benchmark_baked_runtime.py. Keep this separate from the historical
# fixed-NSS sweep above so its workload and offer policy do not change.
PRICE_GPUS = ("RTX 5060 Ti", "RTX 5070", "RTX 5070 Ti", "RTX 5080", "RTX 5090")
PRICE_LIMITS = {"RTX 5060 Ti": 0.20, "RTX 5070": 0.25,
                "RTX 5070 Ti": 0.30, "RTX 5080": 0.40, "RTX 5090": 0.70}
PRICE_CAP_PATH = Path.home() / ".claude/scripts/workspace-overseers/caps/gpu-bench.json"
PRICE_RESULT_ROOT = PROJECT_ROOT / "results/gpu-benchmark-2026-09-23/sol"
PRIOR_MATRIX = PROJECT_ROOT / "results/gpu-benchmark-2026-09-23/matrix.json"
PRICE_PROJECT_COMMIT = "c869309c374bb7976b4bb9729a0650043fbfb4f7"


def _replacement_cost(gpu_name: str, current_host: int) -> float | None:
    """Estimate boot, setup, and download on a fresh, untried host."""
    _, tried_hosts, tried_offers = _price_spend_state()
    tried_hosts.add(current_host)
    prices = []
    for offer in search_offers("gpu_name in [RTX_5060_Ti,RTX_5070,RTX_5070_Ti,RTX_5080,RTX_5090] reliability>0.995"):
        if (offer.get("gpu_name") == gpu_name
                and int(offer.get("host_id") or 0) not in tried_hosts
                and int(offer.get("id") or 0) not in tried_offers):
            terms = _price_offer(offer)
            if terms:
                prices.append(
                    terms[0] * 8 / 60
                    + float(offer.get("storage_total_cost") or 0.0) * 14 / 60
                    + 6 * float(offer.get("inet_down_cost") or 0.0)
                )
    return min(prices) if prices else None


def _replace_loading_host(gpu_name: str, host_id: int, hourly_price: float,
                          waiting_hourly_price: float, download_price: float,
                          no_progress_seconds: float,
                          log: Any) -> bool:
    """Compare remaining image/setup/download cost with a fresh rental."""
    if no_progress_seconds < 4 * 60:
        return False
    fresh_cost = _replacement_cost(gpu_name, host_id)
    if fresh_cost is None:
        return False
    remaining_minutes = 1 + 1.2 * (no_progress_seconds / 60 - 4)
    continue_cost = (
        waiting_hourly_price * remaining_minutes / 60
        + hourly_price * 8 / 60 + 6 * download_price
    )
    log(f"image wait estimate: continue ${continue_cost:.4f}, fresh ${fresh_cost:.4f}")
    # The estimate cannot resolve a cent-scale difference in setup cost.
    margin = max(0.01, 0.10 * continue_cost)
    return fresh_cost + margin < continue_cost


def _price_spend_state() -> tuple[float, set[int], set[int]]:
    old = json.loads(PRIOR_MATRIX.read_text())
    prior = sum(float(entry.get("spent_usd") or 0.0)
                for entry in old.get("rentals", []) + old.get("failures", []))
    hosts = {int(entry["offer"]["host_id"])
             for entry in old.get("rentals", []) + old.get("failures", [])
             if entry.get("offer", {}).get("host_id") is not None}
    # These two rentals were interrupted before the previous worker wrote
    # their failure records; their host IDs remain in driver.log.
    hosts.update({102063, 91303})
    offers = {int(value) for value in old.get("tried_offers", [])}
    manifest = PRICE_RESULT_ROOT / "manifest.json"
    if manifest.exists():
        current = json.loads(manifest.read_text())
        prior = float(current.get("prior_billed_spend_usd", prior))
        entries = current["attempts"]
        prior += _unique_rental_spend(entries)
        hosts.update(int(entry["host_id"]) for entry in entries)
        offers.update(int(entry["offer_id"]) for entry in entries)
    return prior, hosts, offers


def _unique_rental_spend(entries: list[dict[str, Any]]) -> float:
    """Count a resumed instance once and use its bill when available."""
    estimated: dict[int, float] = {}
    billed: dict[int, float] = {}
    for entry in entries:
        instance_id = entry.get("instance_id")
        if instance_id is None:
            continue
        key = int(instance_id)
        estimated[key] = max(
            estimated.get(key, 0.0),
            float(entry.get("estimated_spend_usd") or 0.0),
        )
        if entry.get("billed_spend_usd") is not None:
            billed[key] = max(billed.get(key, 0.0), float(entry["billed_spend_usd"]))
    return sum(billed.get(key, amount) for key, amount in estimated.items())


def _price_offer(offer: dict[str, Any]) -> tuple[float, float | None] | None:
    name = offer.get("gpu_name")
    if name not in PRICE_LIMITS or offer.get("verification") != "verified":
        return None
    if (not offer.get("rentable") or float(offer.get("reliability2") or 0) <= 0.995
            or float(offer.get("disk_space") or 0) < DEFAULT_DISK_GB
            or float(offer.get("gpu_ram") or 0) < 7500
            or float(offer.get("cuda_max_good") or 0) < 12.6
            or int(offer.get("direct_port_count") or 0) < 2):
        return None
    on_demand = float(offer.get("dph_total") or 1e9)
    if on_demand <= PRICE_LIMITS[name]:
        return on_demand, None
    bid = round(float(offer.get("min_bid") or 1e9) + 0.005, 4)
    return (bid, bid) if bid <= PRICE_LIMITS[name] else None


def _upload_pinned_submodules(instance_id: int, timeout: float) -> None:
    """Send the committed submodule revisions without remote GitHub credentials."""
    target, port = _ssh_target(instance_id)
    for tree in ("ceridwen", "external/sedpy_jax"):
        listing = subprocess.run(
            ["git", "ls-tree", PRICE_PROJECT_COMMIT, tree], cwd=PROJECT_ROOT,
            check=True, capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        revision = listing.split()[2]
        archive = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT / tree), "archive", "--format=tar.gz", revision],
            check=True, capture_output=True, timeout=180,
        ).stdout
        remote = f"{REMOTE_ROOT}/{tree}"
        sent = subprocess.run(
            ["ssh", *_ssh_options(port), target,
             f"mkdir -p {shlex.quote(remote)} && tar -xz -C {shlex.quote(remote)}"],
            input=archive, capture_output=True, timeout=timeout,
        )
        if sent.returncode:
            raise SweepError(f"submodule upload failed for {tree}: {sent.stderr.decode()[-500:]}")


def _upload_pinned_project(instance_id: int, timeout: float) -> None:
    """Transfer only the committed source needed by the likelihood benchmark."""
    target, port = _ssh_target(instance_id)
    archive = subprocess.run(
        ["git", "archive", "--format=tar.gz", PRICE_PROJECT_COMMIT, "scripts",
         "notebooks/ceridwen_integrated_photometry_spectra.ipynb"],
        cwd=PROJECT_ROOT, check=True, capture_output=True, timeout=180,
    ).stdout
    remote = shlex.quote(REMOTE_ROOT)
    sent = subprocess.run(
        ["ssh", *_ssh_options(port), target,
         f"mkdir -p {remote} && tar -xz -C {remote} && "
         f"printf '%s\\n' {shlex.quote(PRICE_PROJECT_COMMIT)} > "
         f"{remote}/.benchmark-source-revision"],
        input=archive, capture_output=True, timeout=timeout,
    )
    if sent.returncode:
        raise SweepError(f"source upload failed: {sent.stderr.decode()[-500:]}")


def _retry_after_ssh_disconnect(instance_id: int, offer: dict[str, Any],
                                hourly_price: float, rental_started: float,
                                stage: str,
                                action: Any, log: Any) -> Any:
    """Resume a live rental after a dropped SSH channel when that is cheaper."""
    first_disconnect: float | None = None
    replacement_checks = 0
    while True:
        try:
            return action()
        except (SweepError, subprocess.TimeoutExpired) as error:
            detail = str(error).lower()
            if not any(word in detail for word in
                       ("connection", "broken pipe", "timed out", "timeout", "ssh")):
                raise
            if first_disconnect is None:
                first_disconnect = time.monotonic()
            log(f"{stage}: SSH channel lost; checking the same instance")
            while True:
                state = _instance_state(instance_id)
                if int(state.get("id") or 0) != instance_id:
                    raise SweepError(f"{stage}: instance no longer exists") from error
                if state.get("actual_status") in {"offline", "exited"}:
                    raise SweepError(f"{stage}: instance is {state['actual_status']}") from error
                try:
                    probe = _ssh(instance_id, "true", timeout=40, check=False)
                except (SweepError, subprocess.TimeoutExpired):
                    probe = None
                if probe is not None and probe.returncode == 0:
                    log(f"{stage}: SSH reconnected; resuming on instance {instance_id}")
                    break
                stalled = time.monotonic() - first_disconnect
                spent, _, _ = _price_spend_state()
                cap = float(json.loads(PRICE_CAP_PATH.read_text())["usd"])
                projected = spent + hourly_price * (
                    time.monotonic() - rental_started + 25 * 60
                ) / 3600
                if projected > cap:
                    raise SweepError(f"{stage}: task spend cap would be exceeded") from error
                cheaper = _replace_loading_host(
                    offer["gpu_name"], int(offer["host_id"]), hourly_price,
                    hourly_price,
                    float(offer.get("inet_down_cost") or 0.0), stalled, log,
                )
                replacement_checks = replacement_checks + 1 if cheaper else 0
                if replacement_checks >= 3:
                    raise SweepError(f"{stage}: replacement is consistently cheaper") from error
                time.sleep(SSH_POLL_SECONDS)


def _price_attempt(offer: dict[str, Any], price: float, bid: float | None,
                   log: Any, attach_instance: int | None = None) -> dict[str, Any]:
    instance_id: int | None = attach_instance
    existing_state = _instance_state(attach_instance) if attach_instance else None
    elapsed = max(0.0, datetime.now(UTC).timestamp() - float(existing_state["start_date"])) if existing_state else 0.0
    started = time.monotonic() - elapsed
    disk_price = float(existing_state.get("storage_total_cost") or 0.0) if existing_state else 0.0
    ever_running = False
    result: dict[str, Any] = {
        "gpu_name": offer["gpu_name"], "host_id": int(offer["host_id"]),
        "offer_id": int(offer["id"]), "price_usd_per_hour": price,
        "download_usd_per_gb": float(offer.get("inet_down_cost") or 0.0),
        "interruptible": bid is not None, "reliability": offer["reliability2"],
        "status": "failed", "instance_id": None,
        "project_commit": PRICE_PROJECT_COMMIT,
    }
    try:
        if instance_id is None:
            args = argparse.Namespace(image=DEFAULT_IMAGE, disk=DEFAULT_DISK_GB, bid=bid)
            instance_id = _create_instance(offer, args)
        result["instance_id"] = instance_id
        state = _instance_state(instance_id)
        result["price_usd_per_hour"] = float(state.get("dph_total") or price)
        disk_price = float(state.get("storage_total_cost") or 0.0)
        if result["price_usd_per_hour"] > PRICE_LIMITS[offer["gpu_name"]]:
            raise SweepError("actual instance hourly price exceeds the card limit")
        log(f"rented {instance_id}: {offer['gpu_name']} host {offer['host_id']} ${price:.4f}/h")
        attached = False
        last_message = None
        last_status = None
        last_progress = time.monotonic()
        replacement_checks = 0
        while True:
            state = _instance_state(instance_id)
            if int(state.get("id") or 0) != instance_id:
                raise SweepError("instance no longer exists")
            status = state.get("actual_status")
            if status in {"offline", "exited"}:
                raise SweepError(f"instance entered {status}")
            message = (status, state.get("status_msg"))
            if status != last_status or (status == "loading" and message != last_message):
                last_progress = time.monotonic()
            last_status = status
            last_message = message
            spent, _, _ = _price_spend_state()
            cap = float(json.loads(PRICE_CAP_PATH.read_text())["usd"])
            waiting_price = (result["price_usd_per_hour"] if status == "running"
                             else float(state.get("storage_total_cost") or 0.0))
            projected = (spent + waiting_price * (time.monotonic() - started) / 3600
                         + result["price_usd_per_hour"] * 25 / 60)
            if projected > cap:
                raise SweepError("continuing would exceed the task spend cap")
            if status == "running":
                ever_running = True
                if not attached:
                    _attach_ssh_key(instance_id)
                    attached = True
                try:
                    probe = _ssh(instance_id, "true", timeout=40, check=False)
                except (SweepError, subprocess.TimeoutExpired):
                    probe = None
                if probe is not None and probe.returncode == 0:
                    break
            cheaper = _replace_loading_host(
                offer["gpu_name"], int(offer["host_id"]),
                result["price_usd_per_hour"], waiting_price,
                float(offer.get("inet_down_cost") or 0.0),
                time.monotonic() - last_progress, log,
            )
            replacement_checks = replacement_checks + 1 if cheaper else 0
            if replacement_checks >= 3:
                raise SweepError("fresh host has consistently lower estimated setup cost")
            time.sleep(SSH_POLL_SECONDS)

        def stage(name: str, action: Any) -> Any:
            return _retry_after_ssh_disconnect(
                instance_id, offer, result["price_usd_per_hour"], started,
                name, action, log,
            )
        stage("source", lambda: _upload_pinned_project(instance_id, timeout=1800))
        stage("submodules", lambda: _upload_pinned_submodules(instance_id, timeout=1800))
        stage("inputs", lambda: _upload_inputs(instance_id, log, timeout=1800))
        stage("bootstrap", lambda: _bootstrap(instance_id, log, timeout=1800))
        stage("CUDA check", lambda: _verify_cuda_backend(instance_id, log))

        host = int(offer["host_id"])
        slug = offer["gpu_name"].lower().replace(" ", "-")
        remote_path = f"results/gpu-benchmark-2026-09-23/timing-{slug}-host-{host}.json"
        command = (f"cd {shlex.quote(REMOTE_ROOT)} && mkdir -p results/gpu-benchmark-2026-09-23 && "
                   "MPLBACKEND=Agg LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                   "XLA_FLAGS='--xla_gpu_enable_command_buffer=' "
                   ".venv-ceridwen-gpu/bin/python scripts/benchmark_baked_runtime.py "
                   "--particles 500 --draws 500 --rounds 5 --repeats 10 --seed 20260921 "
                   f"--output {remote_path}")
        log(f"measuring {offer['gpu_name']} on host {host}")
        absolute_output = REMOTE_ROOT + "/" + remote_path
        def run_or_resume_benchmark() -> None:
            while True:
                saved = _ssh(instance_id, f"test -s {shlex.quote(absolute_output)}",
                             timeout=40, check=False)
                if saved.returncode == 0:
                    return
                running = _ssh(
                    instance_id,
                    "pgrep -f '^[.]venv-ceridwen-gpu/bin/python scripts/benchmark_baked_runtime.py'",
                    timeout=40, check=False,
                )
                if running.returncode != 0:
                    break
                spent, _, _ = _price_spend_state()
                cap = float(json.loads(PRICE_CAP_PATH.read_text())["usd"])
                if spent + result["price_usd_per_hour"] * (
                    time.monotonic() - started + 5 * 60
                ) / 3600 > cap:
                    raise SweepError("continuing the benchmark would exceed the spend cap")
                time.sleep(SSH_POLL_SECONDS)
            _ssh(instance_id, command, timeout=720)
        stage("benchmark", run_or_resume_benchmark)
        raw = json.loads(stage(
            "result read",
            lambda: _ssh(instance_id, f"cat {shlex.quote(absolute_output)}", timeout=60),
        ).stdout)
        if not raw["log_likelihood"]["finite"] or not raw["log_likelihood"]["within_test_tolerance"]:
            raise SweepError("likelihood validation failed")
        entry = next(row for row in raw["summary"] if row["particles"] == 500)
        result["calls_per_second"] = 1e6 / float(entry["free_baked_us_per_call"])
        local = PRICE_RESULT_ROOT / Path(remote_path).name
        local.write_text(json.dumps(raw, indent=2) + "\n")
        result["raw_json"] = str(local.relative_to(PROJECT_ROOT))
        result["status"] = "complete"
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {error}"
        log(result["error"][-300:])
    finally:
        if instance_id is not None:
            retain = False
            if result["status"] == "failed" and not any(
                phrase in result.get("error", "") for phrase in
                ("exceeds the card limit", "exceed the task spend cap",
                 "exceed the spend cap", "likelihood validation failed",
                 "instance entered offline", "instance entered exited")
            ):
                state = _instance_state(instance_id)
                spent, _, _ = _price_spend_state()
                cap = float(json.loads(PRICE_CAP_PATH.read_text())["usd"])
                fresh = _replacement_cost(offer["gpu_name"], int(offer["host_id"]))
                repair = result["price_usd_per_hour"] * 5 / 60
                retain = (state.get("actual_status") == "running"
                          and spent + result["price_usd_per_hour"] *
                          (time.monotonic() - started + 10 * 60) / 3600 < cap
                          and (fresh is None or repair < fresh))
                if retain:
                    result["status"] = "needs_recovery"
                    log(f"retaining instance {instance_id} for a cheaper same-host repair")
            if not retain:
                _destroy(instance_id, log)
            result["destroyed"] = not _instance_exists(instance_id)
        else:
            result["destroyed"] = None
        result["rented_seconds"] = time.monotonic() - started if instance_id else 0.0
        charged_rate = result["price_usd_per_hour"] if ever_running else disk_price
        result["estimated_spend_usd"] = charged_rate * result["rented_seconds"] / 3600
    return result


def command_price_matrix(args: argparse.Namespace) -> int:
    PRICE_RESULT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = PRICE_RESULT_ROOT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"attempts": []}
    attempts_at_start = len(manifest["attempts"])
    if args.attach_instance is not None:
        state = _instance_state(args.attach_instance)
        if int(state.get("id") or 0) != args.attach_instance:
            raise SweepError("the requested instance is not live")
        if args.attach_offer_id is None:
            raise SweepError("--attach-offer-id is required with --attach-instance")
        offer = {"gpu_name": state["gpu_name"], "host_id": state["host_id"],
                 "id": args.attach_offer_id, "reliability2": state["reliability2"]}
        def log(message: str) -> None:
            print(f"{datetime.now(UTC):%H:%M:%S} {message}", flush=True)
        outcome = _price_attempt(offer, float(state["dph_total"]), None, log,
                                 attach_instance=args.attach_instance)
        manifest["attempts"].append(outcome)
        manifest["prior_estimated_spend_usd"] = float(
            manifest.get("prior_billed_spend_usd", manifest.get("prior_estimated_spend_usd", 0.0)))
        manifest["total_estimated_spend_usd"] = (
            manifest["prior_estimated_spend_usd"] + _unique_rental_spend(manifest["attempts"]))
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        return 0 if outcome["status"] == "complete" and outcome["destroyed"] else 1
    deadline = time.monotonic() + args.wait_minutes * 60
    while True:
        spent, tried_hosts, tried_offers = _price_spend_state()
        cap = float(json.loads(PRICE_CAP_PATH.read_text())["usd"])
        completed = {name: {int(entry["host_id"]) for entry in manifest["attempts"]
                            if entry["gpu_name"] == name and entry["status"] == "complete"}
                     for name in PRICE_GPUS}
        if all(len(hosts) >= 2 for hosts in completed.values()):
            return 0
        if spent + 0.20 >= cap:
            print(f"spend guard: ${spent:.3f} of ${cap:.2f}; stopping", flush=True)
            return 1
        offers = search_offers("gpu_name in [RTX_5060_Ti,RTX_5070,RTX_5070_Ti,RTX_5080,RTX_5090] reliability>0.995")
        candidates = []
        for name in PRICE_GPUS:
            if len(completed[name]) >= 2:
                continue
            for offer in offers:
                if offer.get("gpu_name") != name or int(offer.get("host_id") or 0) in tried_hosts or int(offer.get("id") or 0) in tried_offers:
                    continue
                terms = _price_offer(offer)
                # Reserve enough for a slow setup and measurement before renting.
                download_cost = 8 * float(offer.get("inet_down_cost") or 0.0)
                if terms and spent + terms[0] * 0.66 + download_cost <= cap:
                    expected_cost = terms[0] * 0.33 + 6 * float(offer.get("inet_down_cost") or 0.0)
                    candidates.append((len(completed[name]), terms[0], offer, terms[1], expected_cost))
        if candidates:
            _, price, offer, bid, _ = min(
                candidates,
                key=lambda item: (item[2]["gpu_name"] != "RTX 5060 Ti", item[0], item[4]),
            )
            def log(message: str) -> None:
                print(f"{datetime.now(UTC):%H:%M:%S} {message}", flush=True)
            outcome = _price_attempt(offer, price, bid, log)
            manifest["attempts"].append(outcome)
            manifest["prior_estimated_spend_usd"] = float(
                manifest.get("prior_billed_spend_usd", manifest.get("prior_estimated_spend_usd", 0.0)))
            manifest["total_estimated_spend_usd"] = (
                manifest["prior_estimated_spend_usd"] + _unique_rental_spend(manifest["attempts"]))
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
            if outcome.get("destroyed") is False:
                raise SweepError(f"instance {outcome['instance_id']} still exists; stop further rentals")
            if len(manifest["attempts"]) - attempts_at_start >= args.max_attempts:
                return 0
        elif time.monotonic() >= deadline:
            print("no remaining qualifying fresh host was listed", flush=True)
            return 1
        else:
            time.sleep(60)


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
        help=f"Offers to try per GPU model before giving up. Default: {DEFAULT_ATTEMPTS}.",
    )
    run_parser.set_defaults(function=command_run)

    price_parser = subparsers.add_parser(
        "price-matrix", help="measure current M1_210210 likelihood on two hosts per card"
    )
    price_parser.add_argument("--wait-minutes", type=float, default=0)
    price_parser.add_argument("--max-attempts", type=int, default=1)
    price_parser.add_argument("--attach-instance", type=int)
    price_parser.add_argument("--attach-offer-id", type=int)
    price_parser.set_defaults(function=command_price_matrix)
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
