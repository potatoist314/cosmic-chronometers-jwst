#!/usr/bin/env python3
"""Shared Vast.ai transport and offer policy for experiment and benchmark runners."""

from __future__ import annotations

import argparse
import json
import os
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

MAX_INET_COST_USD_PER_TB = 5.0

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
# (image, data, bootstrap).
FIT_EXPECTED_HOURS = 1.0
FIT_TRANSFER_GB = 6.0
FIT_OFFER_QUERY_BASE = (f"gpu_name in [RTX_5060,RTX_5060_Ti,RTX_5070,RTX_5080,RTX_5090] verified=true rentable=true num_gpus=1 "
                        f"inet_down>200 disk_space>=40 reliability>{FIT_MIN_RELIABILITY} "
                        f"inet_down_cost<{FIT_MAX_INET_COST_USD_PER_TB / 1000}")
FIT_OFFER_QUERY = f"{FIT_OFFER_QUERY_BASE} dph<{FIT_MAX_DPH_USD}"


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


def search_offers(extra_query: str = "") -> list[dict[str, Any]]:
    """Return every rentable single-GPU offer Vast currently lists."""
    query = f"num_gpus=1 rentable=true {extra_query}".strip()
    offers = _vastai_json(["search", "offers", query, "--limit", "5000"])
    if not isinstance(offers, list):
        raise SweepError("vastai search offers did not return a list")
    return offers


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
