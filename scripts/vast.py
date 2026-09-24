#!/usr/bin/env python3
"""Shared Vast.ai transport and offer policy for experiment and benchmark runners."""

from __future__ import annotations

import argparse
import json
import math
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/potatoist314/cosmic-chronometers-jwst.git"
REMOTE_ROOT = "/workspace/cosmic-chronometers-jwst"

# The bootstrap installs CUDA JAX, so avoid pulling an unused PyTorch stack.
DEFAULT_IMAGE = "vastai/base-image:cuda-12.6.3-auto"
DEFAULT_DISK_GB = 40
DESTROY_ATTEMPTS = 3
VASTAI_JSON_ATTEMPTS = 3
BENCHMARK_GPU_MEMORY_MIB = 6000
SSH_KEY_PATH = Path.home() / ".ssh/id_ed25519"
EXPECTED_SPECTRUM_FILES = 1988

MAX_INET_COST_USD_PER_TB = 10.0
FIT_GPU_NAMES = ("RTX 5060", "RTX 5060 Ti", "RTX 5070", "RTX 5080", "RTX 5090")
FIT_MIN_RELIABILITY = 0.995
RELIABILITY_TIERS = (FIT_MIN_RELIABILITY, 0.96)
FIT_BID_MARGIN_USD = 0.005
FIT_MAX_INET_COST_USD_PER_TB = MAX_INET_COST_USD_PER_TB


def experiment_cap(value):
    amount = float(value)
    if not math.isfinite(amount) or not 0 < amount <= 1:
        raise argparse.ArgumentTypeError("experiment spend cap must be above zero and at most USD 1")
    return amount


def bandwidth_qualifies(offer):
    return all(float(offer.get(field, math.inf)) < MAX_INET_COST_USD_PER_TB / 1000
               for field in ("inet_down_cost", "inet_up_cost"))


FIT_OFFER_QUERY_BASE = (f"gpu_name in [RTX_5060,RTX_5060_Ti,RTX_5070,RTX_5080,RTX_5090] verified=true rentable=true num_gpus=1 "
                        f"inet_down>200 disk_space>=40 reliability>{FIT_MIN_RELIABILITY} "
                        f"inet_down_cost<{FIT_MAX_INET_COST_USD_PER_TB / 1000} "
                        f"inet_up_cost<{FIT_MAX_INET_COST_USD_PER_TB / 1000}")
FIT_OFFER_QUERY = FIT_OFFER_QUERY_BASE


RUNNING_TIMEOUT_SECONDS = 600
SSH_TIMEOUT_SECONDS = 600
SSH_POLL_SECONDS = 15
BOOTSTRAP_TIMEOUT_SECONDS = 3600


def fit_bid_price(offer: dict[str, Any]) -> float:
    """Interruptible bid: the host's minimum bid plus a small margin; you pay the bid."""
    return round(float(offer["min_bid"]) + FIT_BID_MARGIN_USD, 4)


def fit_offer_price(offer: dict[str, Any], *, interruptible: bool = False) -> float:
    """Hourly price: the bid for an interruptible rental, else on-demand."""
    if interruptible and "min_bid" in offer:
        return fit_bid_price(offer) + float(offer.get("storage_total_cost") or 0)
    return float(offer.get("dph_total") or 1e9)


def fit_offer_qualifies(offer: dict[str, Any], *, interruptible: bool = False,
                        min_reliability: float = FIT_MIN_RELIABILITY) -> bool:
    """Require supported GPUs, the selected reliability tier, and bandwidth below $10/TB."""
    return (offer.get("gpu_name") in FIT_GPU_NAMES
            and float(offer.get("reliability2") or 0.0) > min_reliability
            and bandwidth_qualifies(offer))


def fit_offers(*, exclude_hosts=(), minimum_gpu_ram_mib=8000, interruptible=False):
    """Use the first reliability tier with eligible offers, ordered by hourly price."""
    for minimum in RELIABILITY_TIERS:
        query = FIT_OFFER_QUERY.replace(f"reliability>{FIT_MIN_RELIABILITY}",
                                        f"reliability>{minimum}")
        offers = [o for o in search_offers(query, rental_type="bid" if interruptible else "on-demand")
                  if fit_offer_qualifies(o, min_reliability=minimum)
                  and float(o.get("gpu_ram") or 0) >= minimum_gpu_ram_mib
                  and float(o.get("cuda_max_good") or 0) >= 12.6
                  and int(o.get("host_id") or 0) not in exclude_hosts]
        if offers:
            return sorted(offers, key=lambda o: fit_offer_price(o, interruptible=interruptible))
    return []


class SweepError(RuntimeError):
    """Report an unusable offer, instance, or remote command."""


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
    attempts = 1 if arguments[:2] == ["create", "instance"] else VASTAI_JSON_ATTEMPTS
    for attempt in range(attempts):
        output = _vastai([*arguments, "--raw"], timeout=timeout)
        start = min(
            (index for index in (output.find("["), output.find("{")) if index >= 0),
            default=-1,
        )
        if start >= 0:
            return json.loads(output[start:])
        if attempt + 1 < attempts:
            time.sleep(SSH_POLL_SECONDS)
    raise SweepError(f"vastai returned no JSON: {output.strip()[:200]}")


def search_offers(extra_query: str = "", *, rental_type: str = "on-demand",
                  disk: int = DEFAULT_DISK_GB) -> list[dict[str, Any]]:
    """Search explicit rental terms, sorted by hourly price for the requested disk."""
    query = f"num_gpus=1 rentable=true {extra_query}".strip()
    offers = _vastai_json(["search", "offers", query, "--no-default",
                          "--type", rental_type, "--storage", str(disk),
                          "--order", "dph", "--limit", "5000"])
    if not isinstance(offers, list):
        raise SweepError("vastai search offers did not return a list")
    if len(offers) >= 5000:
        raise SweepError("offer search reached its limit; narrow the GPU query before renting")
    return [{**offer, "rental_type": rental_type} for offer in offers]


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


def _rsync(
    port: str,
    source: str,
    destination: str,
    timeout: float,
    mirror: bool = False,
) -> None:
    shell = " ".join(shlex.quote(part) for part in ["ssh", *_ssh_options(port)])
    command = ["rsync", "-a", "--partial", "-e", shell]
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
            getattr(args, "label", f"ceridwen-bench-{slug}"),
            *(["--bid_price", str(args.bid)] if getattr(args, "bid", None) else []),
        ],
        timeout=300.0,
    )
    if not payload.get("success", False):
        raise SweepError(f"vastai refused the rental: {payload}")
    return int(payload["new_contract"])
