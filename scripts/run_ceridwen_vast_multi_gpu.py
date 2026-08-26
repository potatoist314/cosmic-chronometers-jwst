"""Run four independent Ceridwen notebook fits on four visible Vast GPUs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TextIO

DEFAULT_TARGETS = (
    "M1_210210",
    "M12_181945",
    "M2_133501",
    "M14_38648",
)
MINIMUM_GPU_MEMORY_MIB = 12_000
PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"


@dataclass
class Worker:
    """One target fit and its assigned physical GPU process."""

    target: str
    gpu: dict[str, str | int]
    seed: int
    result_dir: Path
    log_handle: TextIO
    process: subprocess.Popen[str]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _visible_gpus() -> list[dict[str, str | int]]:
    command = [
        "nvidia-smi",
        "--query-gpu=index,uuid,name,memory.total",
        "--format=csv,noheader,nounits",
    ]
    try:
        output = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("nvidia-smi could not list the Vast GPUs") from exc

    gpus = []
    for row in csv.reader(output.splitlines(), skipinitialspace=True):
        index, uuid, name, memory_mib = (value.strip() for value in row)
        gpus.append(
            {
                "index": int(index),
                "uuid": uuid,
                "name": name,
                "memory_mib": int(memory_mib),
            }
        )
    gpus.sort(key=lambda gpu: int(gpu["index"]))
    return gpus


def _write_manifest(path: Path, manifest: dict[str, object]) -> None:
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _worker_command(output_notebook: Path) -> list[str]:
    return [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker-output",
        str(output_notebook),
    ]


def _worker_environment(
    *,
    target: str,
    gpu_index: int,
    seed: int,
    result_dir: Path,
    profile: str,
) -> dict[str, str]:
    return {
        **os.environ,
        "CUDA_DEVICE_ORDER": "PCI_BUS_ID",
        "CUDA_VISIBLE_DEVICES": str(gpu_index),
        "CERIDWEN_EXPECT_SINGLE_GPU": "1",
        "CERIDWEN_NOTEBOOK_QUICK": "1" if profile == "quick" else "0",
        "CERIDWEN_PROJECT_ROOT": str(PROJECT_ROOT),
        "CERIDWEN_RANDOM_SEED": str(seed),
        "CERIDWEN_RESULT_DIR": str(result_dir),
        "CERIDWEN_TARGET_ID": target,
        "JAX_ENABLE_X64": "1",
        "JAX_PLATFORMS": "cuda",
        "LD_LIBRARY_PATH": "",
    }


def _launch_workers(
    *,
    targets: list[str],
    gpus: list[dict[str, str | int]],
    profile: str,
    run_root: Path,
    base_seed: int,
) -> list[Worker]:
    workers = []
    for offset, (target, gpu) in enumerate(zip(targets, gpus, strict=True)):
        gpu_index = int(gpu["index"])
        seed = base_seed + offset
        result_dir = run_root / f"gpu_{gpu_index}_{target.lower()}"
        result_dir.mkdir()
        output_notebook = result_dir / f"{target.lower()}_executed.ipynb"
        log_handle = (result_dir / "execution.log").open("w", encoding="utf-8")
        process = subprocess.Popen(
            _worker_command(output_notebook),
            cwd=PROJECT_ROOT,
            env=_worker_environment(
                target=target,
                gpu_index=gpu_index,
                seed=seed,
                result_dir=result_dir,
                profile=profile,
            ),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
        )
        workers.append(
            Worker(
                target=target,
                gpu=gpu,
                seed=seed,
                result_dir=result_dir,
                log_handle=log_handle,
                process=process,
            )
        )
        print(f"GPU {gpu_index}: started {target} as PID {process.pid}")
    return workers


def _worker_records(workers: list[Worker]) -> list[dict[str, object]]:
    records = []
    for worker in workers:
        return_code = worker.process.poll()
        records.append(
            {
                "target": worker.target,
                "physical_gpu_index": worker.gpu["index"],
                "gpu_uuid": worker.gpu["uuid"],
                "gpu_name": worker.gpu["name"],
                "gpu_memory_mib": worker.gpu["memory_mib"],
                "seed": worker.seed,
                "pid": worker.process.pid,
                "status": (
                    "running"
                    if return_code is None
                    else "complete"
                    if return_code == 0
                    else "failed"
                ),
                "return_code": return_code,
                "result_directory": worker.result_dir.name,
            }
        )
    return records


def _run(args: argparse.Namespace) -> int:
    targets = list(args.targets)
    if len(set(targets)) != len(targets):
        raise ValueError("Each GPU requires a distinct galaxy target")

    gpus = _visible_gpus()
    if len(gpus) != 4:
        raise RuntimeError(f"Expected four visible GPUs, found {len(gpus)}")
    small_gpus = [gpu for gpu in gpus if int(gpu["memory_mib"]) < MINIMUM_GPU_MEMORY_MIB]
    if small_gpus:
        raise RuntimeError("Every visible GPU must provide at least 12000 MiB")

    gpu_names = {str(gpu["name"]) for gpu in gpus}
    hardware = _slug(gpu_names.pop()) if len(gpu_names) == 1 else "mixed_gpu"
    analysis = "joint_full" if args.profile == "full" else "joint_quick"
    date = datetime.now(UTC).date().isoformat()
    incomplete_name = (
        f"ceridwen_vast_4x_{hardware}_four_galaxy_{analysis}_incomplete_{date}"
    )
    run_root = args.output_root.resolve() / incomplete_name
    if run_root.exists():
        raise FileExistsError(f"Result directory already exists: {run_root}")
    run_root.mkdir(parents=True)

    manifest_path = run_root / "run_manifest.json"
    manifest: dict[str, object] = {
        "schema_version": 1,
        "status": "running",
        "profile": args.profile,
        "notebook": str(NOTEBOOK_PATH.relative_to(PROJECT_ROOT)),
        "started_at_utc": _utc_now(),
        "workers": [],
    }
    _write_manifest(manifest_path, manifest)

    workers = _launch_workers(
        targets=targets,
        gpus=gpus,
        profile=args.profile,
        run_root=run_root,
        base_seed=args.base_seed,
    )
    try:
        while any(worker.process.poll() is None for worker in workers):
            manifest["workers"] = _worker_records(workers)
            _write_manifest(manifest_path, manifest)
            time.sleep(5)
    finally:
        for worker in workers:
            worker.log_handle.close()

    failed_targets = []
    for worker in workers:
        result_path = worker.result_dir / "ceridwen_result.h5"
        executed_notebook = worker.result_dir / f"{worker.target.lower()}_executed.ipynb"
        if worker.process.returncode != 0 or not result_path.is_file():
            failed_targets.append(worker.target)
        if not executed_notebook.is_file():
            failed_targets.append(worker.target)

    manifest["completed_at_utc"] = _utc_now()
    manifest["workers"] = _worker_records(workers)
    if failed_targets:
        manifest["status"] = "incomplete"
        manifest["failed_targets"] = sorted(set(failed_targets))
        _write_manifest(manifest_path, manifest)
        print(f"Incomplete targets: {', '.join(sorted(set(failed_targets)))}")
        print(f"Results retained in {run_root}")
        return 1

    manifest["status"] = "complete"
    _write_manifest(manifest_path, manifest)
    complete_root = run_root.with_name(run_root.name.replace("_incomplete_", "_complete_"))
    if complete_root.exists():
        raise FileExistsError(f"Completed result directory already exists: {complete_root}")
    run_root.rename(complete_root)
    print(f"All four fits completed: {complete_root}")
    return 0


def _worker(args: argparse.Namespace) -> int:
    import nbformat
    from nbclient import NotebookClient

    class StreamingNotebookClient(NotebookClient):
        """Copy live notebook stream output into the worker log."""

        def process_message(self, msg, cell, cell_index):
            if msg["msg_type"] == "stream":
                print(msg["content"]["text"], end="", flush=True)
            return super().process_message(msg, cell, cell_index)

    document = nbformat.read(NOTEBOOK_PATH, as_version=4)
    client = StreamingNotebookClient(
        document,
        timeout=None,
        kernel_name="ceridwen",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    try:
        client.execute()
    finally:
        args.output_notebook.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(document, args.output_notebook)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one joint Ceridwen fit on each of four visible Vast GPUs."
    )
    parser.add_argument("--worker-output", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--targets",
        nargs=4,
        default=DEFAULT_TARGETS,
        metavar=("GPU0", "GPU1", "GPU2", "GPU3"),
        help="Four distinct LEGA-C SPECT_ID values, in physical GPU order.",
    )
    parser.add_argument(
        "--profile",
        choices=("quick", "full"),
        default="full",
        help="Use quick smoke-test or full GPU sampler settings.",
    )
    parser.add_argument(
        "--base-seed",
        type=int,
        default=20260812,
        help="First deterministic seed; later GPUs increment it by one.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=PROJECT_ROOT / "results",
        help="Parent directory for the human-readable run directory.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.worker_output is not None:
        args.output_notebook = args.worker_output
        return _worker(args)
    return _run(args)


if __name__ == "__main__":
    raise SystemExit(main())
