"""Run a deterministic Ceridwen DR2 target shard on one Vast GPU."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
CATALOG_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
PHOTOMETRY_PATH = (
    PROJECT_ROOT
    / "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits"
)
DEFAULT_OUTPUT_ROOT = (
    PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
)
DEFAULT_BASE_SEED = 20260830
DEFAULT_MINIMUM_GPU_MEMORY_MIB = int(
    os.environ.get("CERIDWEN_MIN_GPU_MEMORY_MIB", "8000")
)
REMOTE_RESULT_ROOT = "/workspace/cosmic-chronometers-jwst/results/rtx-5060-dr2-quiescent-full-spectrum"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _decode(value):
    return value.decode() if isinstance(value, bytes) else value


def build_target_manifest(*, num_shards: int, base_seed: int) -> dict:
    """Select one highest-S/N spectrum for each eligible DR2 object."""
    from astropy.table import Table

    legac = Table.read(CATALOG_PATH).to_pandas()
    for column in ("SPECT_ID", "Filename"):
        legac[column] = legac[column].map(_decode)
    phot = Table.read(PHOTOMETRY_PATH).to_pandas().set_index("LEGAC_INDEX")
    phot_columns = [
        "Area",
        "Sat",
        "Cfl",
        "Flag",
        "NUVMag",
        "RMag",
        "JMag",
        "Fuap3",
        "e_Fuap3",
        "FBap3",
        "e_FBap3",
        "FVap3",
        "e_FVap3",
        "Frap3",
        "e_Frap3",
        "Fipap3",
        "e_Fipap3",
        "Fzppap3",
        "e_Fzppap3",
        "FYap3",
        "e_FYap3",
        "FJap3",
        "e_FJap3",
        "FHap3",
        "e_FHap3",
        "FKsap3",
        "e_FKsap3",
        "F3.6um",
        "e_F3.6um",
        "F4.5um",
        "e_F4.5um",
    ]
    parent = legac.join(phot[phot_columns], how="inner")
    quality = (
        (parent["f_use"] == 1)
        & (parent["f_ppxf"] == 0)
        & (parent["f_z"] == 0)
        & (parent["f_int"] == 0)
        & (parent["SN"] > 0)
        & (parent["z"] >= 0.6)
        & (parent["z"] < 1.0)
    )
    valid_rest = (parent[["NUVMag", "RMag", "JMag"]] > -40).all(axis=1)
    parent = parent[quality & valid_rest].copy()
    nuv_r = parent["NUVMag"] - parent["RMag"]
    r_j = parent["RMag"] - parent["JMag"]
    passive = parent[(nuv_r > 3 * r_j + 1) & (nuv_r > 3.1)]
    oii_ew = passive["OII_3727_EW"]
    weak_oii = passive[(oii_ew > -5) | oii_ew.isna()]
    oii_sig = (weak_oii["OII_3727_EW"] / weak_oii["OII_3727_EW_err"]).abs()
    oiii_sig = (weak_oii["OIII_5007_EW"] / weak_oii["OIII_5007_EW_err"]).abs()
    bona_fide = weak_oii[~((oii_sig >= 3) | (oiii_sig >= 3))]
    clean = (
        (bona_fide["Area"] == 0)
        & (bona_fide["Sat"] == 0)
        & (bona_fide["Cfl"] == 1)
        & (bona_fide["Flag"] == 0)
    )
    usable = bona_fide[clean].copy()
    if len(usable) != 194:
        raise RuntimeError(f"Expected 194 eligible spectra, found {len(usable)}")

    selected = (
        usable.sort_values(["SN", "SPECT_ID"], ascending=[False, True])
        .drop_duplicates("OBJECT", keep="first")
        .sort_values(["SN", "SPECT_ID"], ascending=[False, True])
    )
    if len(selected) != 187:
        raise RuntimeError(f"Expected 187 unique objects, found {len(selected)}")

    targets = []
    for index, row in enumerate(selected.itertuples(index=False)):
        targets.append(
            {
                "manifest_index": index,
                "object_id": int(row.OBJECT),
                "spect_id": str(row.SPECT_ID),
                "sn": float(row.SN),
                "shard_index": index % num_shards,
                "seed": base_seed + index,
            }
        )
    return {
        "schema_version": 1,
        "sample": "LEGA-C DR2 quiescent, clean 12-band photometry",
        "selection": "highest-S/N eligible spectrum per OBJECT",
        "num_shards": num_shards,
        "base_seed": base_seed,
        "eligible_spectra": 194,
        "unique_objects": 187,
        "targets": targets,
    }


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _load_target_manifest(path: Path | None, *, num_shards: int, base_seed: int):
    if path is None:
        return build_target_manifest(num_shards=num_shards, base_seed=base_seed)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("unique_objects") != 187 or len(manifest.get("targets", [])) != 187:
        raise ValueError("The target manifest must contain 187 unique objects")
    if manifest.get("num_shards") != num_shards:
        raise ValueError("The target manifest num_shards does not match --num-shards")
    return manifest


def _visible_gpu(minimum_memory_mib: int) -> dict:
    command = [
        "nvidia-smi",
        "--query-gpu=index,uuid,name,memory.total",
        "--format=csv,noheader,nounits",
    ]
    try:
        rows = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("nvidia-smi could not list the Vast GPU") from exc
    if len(rows) != 1:
        raise RuntimeError(f"Expected one visible GPU, found {len(rows)}")
    index, uuid, name, memory = [part.strip() for part in rows[0].split(",")]
    gpu = {
        "index": int(index),
        "uuid": uuid,
        "name": name,
        "memory_mib": int(memory),
    }
    if gpu["memory_mib"] < minimum_memory_mib:
        raise RuntimeError(
            f"GPU has {gpu['memory_mib']} MiB. Required: {minimum_memory_mib} MiB"
        )
    return gpu


def _worker_environment(target: dict, result_dir: Path) -> dict[str, str]:
    return {
        **os.environ,
        "CUDA_DEVICE_ORDER": "PCI_BUS_ID",
        "CUDA_VISIBLE_DEVICES": "0",
        "CERIDWEN_EXPECT_SINGLE_GPU": "1",
        "CERIDWEN_FIT_MODE": "full_spectrum",
        "CERIDWEN_NOTEBOOK_QUICK": "0",
        "CERIDWEN_PROJECT_ROOT": str(PROJECT_ROOT),
        "CERIDWEN_RANDOM_SEED": str(target["seed"]),
        "CERIDWEN_RESULT_DIR": str(result_dir),
        "CERIDWEN_TARGET_ID": str(target["spect_id"]),
        "CERIDWEN_OBJECT_ID": str(target["object_id"]),
        "CERIDWEN_MANIFEST_INDEX": str(target["manifest_index"]),
        "JAX_ENABLE_X64": "1",
        "JAX_PLATFORMS": "cuda",
        "LD_LIBRARY_PATH": "",
    }


def _validate_result(result_dir: Path, spect_id: str) -> None:
    import h5py
    import nbformat
    import numpy as np
    from ceridwen.fit import load_result_h5

    result_path = result_dir / "ceridwen_result.h5"
    derived_path = result_dir / "ceridwen_derived_outputs.h5"
    notebook_path = result_dir / f"{spect_id}_executed.ipynb"
    loaded = load_result_h5(result_path)
    if len(loaded.param_names) != 7:
        raise RuntimeError(f"Expected seven parameter groups, found {loaded.param_names}")
    if not np.isfinite(np.asarray(loaded.log_weights)).all():
        raise RuntimeError("Posterior log weights contain non-finite values")
    if not np.isfinite([loaded.log_evidence, loaded.log_evidence_err]).all():
        raise RuntimeError("Nested-sampling evidence is not finite")
    with h5py.File(derived_path, "r") as derived:
        required = {"summary", "sfh", "photometry", "spectrum", "diagnostics"}
        missing = required.difference(derived.keys())
        if missing:
            raise RuntimeError(f"Missing derived-output groups: {sorted(missing)}")
        if not bool(derived["diagnostics"].attrs["passed"]):
            raise RuntimeError("Posterior diagnostics did not pass")
    notebook = nbformat.read(notebook_path, as_version=4)
    images = sum(
        "image/png" in output.get("data", {})
        for cell in notebook.cells
        for output in cell.get("outputs", [])
    )
    if images < 5:
        raise RuntimeError(f"Expected at least five embedded figures, found {images}")


def _execute_target(target: dict, result_dir: Path) -> int:
    notebook_path = result_dir / f"{target['spect_id']}_executed.ipynb"
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker-output",
        str(notebook_path),
    ]
    result_dir.mkdir(parents=True, exist_ok=True)
    log_path = result_dir / "execution.log"
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n[{_utc_now()}] starting fixed-seed attempt\n")
        log.flush()
        return subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            env=_worker_environment(target, result_dir),
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        ).returncode


def _worker(output_notebook: Path) -> int:
    import nbformat
    from nbclient import NotebookClient

    class StreamingNotebookClient(NotebookClient):
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
        output_notebook.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(document, output_notebook)
    return 0


def _monitor_endpoint(value: str) -> dict:
    instance_id, host, port, shard_index = value.split(":", maxsplit=3)
    return {
        "instance_id": int(instance_id),
        "host": host,
        "port": int(port),
        "shard_index": int(shard_index),
    }


def _remote_manifest(endpoint: dict) -> dict:
    path = f"{REMOTE_RESULT_ROOT}/shard_{endpoint['shard_index']}_manifest.json"
    result = subprocess.run(
        [
            "ssh",
            "-p",
            str(endpoint["port"]),
            f"root@{endpoint['host']}",
            "cat",
            path,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _rsync_command(endpoint: dict, *arguments: str) -> None:
    subprocess.run(
        ["rsync", "-aP", "-e", f"ssh -p {endpoint['port']}", *arguments],
        check=True,
    )


def _pull_completed(endpoint: dict, manifest: dict, output_root: Path) -> set[str]:
    output_root.mkdir(parents=True, exist_ok=True)
    remote = f"root@{endpoint['host']}"
    _rsync_command(
        endpoint,
        f"{remote}:{REMOTE_RESULT_ROOT}/targets.json",
        f"{remote}:{REMOTE_RESULT_ROOT}/shard_{endpoint['shard_index']}_manifest.json",
        f"{output_root}/",
    )

    completed = set()
    targets = {target["spect_id"]: target for target in manifest["targets"]}
    for spect_id, result in manifest["results"].items():
        if result.get("status") != "complete":
            continue
        target = targets[spect_id]
        result_dir = output_root / f"{target['object_id']}-{spect_id}"
        try:
            _validate_result(result_dir, spect_id)
        except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError):
            result_dir.mkdir(parents=True, exist_ok=True)
            remote_dir = f"{remote}:{REMOTE_RESULT_ROOT}/{target['object_id']}-{spect_id}/"
            _rsync_command(
                endpoint,
                "--include=execution.log",
                "--include=ceridwen_result.h5",
                "--include=ceridwen_derived_outputs.h5",
                f"--include={spect_id}_executed.ipynb",
                "--exclude=*",
                remote_dir,
                f"{result_dir}/",
            )
            _validate_result(result_dir, spect_id)
        completed.add(spect_id)
    return completed


def _vast_credit() -> float:
    result = subprocess.run(
        ["vastai", "show", "user", "--raw"],
        check=True,
        capture_output=True,
        text=True,
    )
    start = result.stdout.find("{")
    if start < 0:
        raise RuntimeError("Vast user response did not contain JSON")
    return float(json.loads(result.stdout[start:])["credit"])


def _set_instances(endpoints: list[dict], action: str) -> None:
    for endpoint in endpoints:
        subprocess.run(
            ["vastai", action, "instance", str(endpoint["instance_id"])],
            check=True,
        )


def _monitor(args: argparse.Namespace) -> int:
    os.environ["JAX_PLATFORMS"] = "cpu"
    endpoints = [_monitor_endpoint(value) for value in args.monitor_instance]
    if {endpoint["shard_index"] for endpoint in endpoints} != {0, 1}:
        raise ValueError("--monitor-instance must specify shards 0 and 1")
    if args.credit_baseline is None:
        raise ValueError("--credit-baseline is required with --monitor")

    while True:
        manifests = []
        completed = set()
        try:
            for endpoint in endpoints:
                manifest = _remote_manifest(endpoint)
                manifests.append(manifest)
                completed.update(
                    _pull_completed(endpoint, manifest, args.output_root)
                )
            credit = _vast_credit()
            spend = args.credit_baseline - credit
            print(
                f"[{_utc_now()}] locally validated {len(completed)}/187; "
                f"Vast spend ${spend:.3f}/${args.spend_cap:.2f}",
                flush=True,
            )

            if spend >= args.spend_cap:
                _set_instances(endpoints, "stop")
                raise RuntimeError("Stopped both instances at the Vast spend cap")
            if any(manifest.get("status") == "incomplete" for manifest in manifests):
                _set_instances(endpoints, "stop")
                raise RuntimeError("Stopped both instances after an incomplete shard")
            if all(manifest.get("status") == "complete" for manifest in manifests):
                if len(completed) != 187:
                    _set_instances(endpoints, "stop")
                    raise RuntimeError(
                        f"Both shards completed but only {len(completed)} local results validate"
                    )
                _set_instances(endpoints, "destroy")
                print("All 187 local results validated; destroyed both instances", flush=True)
                return 0
        except RuntimeError:
            _set_instances(endpoints, "stop")
            raise
        except (json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
            print(f"[{_utc_now()}] monitor retry: {exc}", flush=True)
        time.sleep(args.poll_seconds)


def _run(args: argparse.Namespace) -> int:
    # Result validation imports JAX in this long-lived control process. Keep it
    # on CPU so it cannot reserve VRAM needed by the notebook kernel.
    os.environ["JAX_PLATFORMS"] = "cpu"
    manifest = _load_target_manifest(
        args.targets_file,
        num_shards=args.num_shards,
        base_seed=args.base_seed,
    )
    if args.write_targets_file is not None:
        _write_json(args.write_targets_file, manifest)
        print(f"Wrote {args.write_targets_file}")
        return 0

    if not 0 <= args.shard_index < args.num_shards:
        raise ValueError("--shard-index must be between zero and num_shards minus one")
    gpu = _visible_gpu(args.minimum_gpu_memory_mib)
    targets = [
        target
        for target in manifest["targets"]
        if target["shard_index"] == args.shard_index
    ]
    if args.only_target is not None:
        targets = [target for target in targets if target["spect_id"] == args.only_target]
        if len(targets) != 1:
            raise ValueError(f"Target {args.only_target} is not in shard {args.shard_index}")

    args.output_root.mkdir(parents=True, exist_ok=True)
    run_manifest_path = args.output_root / f"shard_{args.shard_index}_manifest.json"
    run_manifest = {
        "schema_version": 1,
        "status": "running",
        "started_at_utc": _utc_now(),
        "shard_index": args.shard_index,
        "num_shards": args.num_shards,
        "gpu": gpu,
        "vast_instance_id": os.environ.get("VAST_INSTANCE_ID"),
        "project_commit": os.environ.get("CERIDWEN_PROJECT_COMMIT"),
        "ceridwen_commit": os.environ.get("CERIDWEN_SOURCE_COMMIT"),
        "targets": targets,
        "results": {},
    }
    _write_json(run_manifest_path, run_manifest)

    failed = []
    for target in targets:
        key = str(target["spect_id"])
        result_dir = args.output_root / f"{target['object_id']}-{key}"
        try:
            _validate_result(result_dir, key)
            run_manifest["results"][key] = {"status": "complete", "attempts": 0}
            _write_json(run_manifest_path, run_manifest)
            continue
        except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError):
            pass

        completed = False
        for attempt in range(1, args.max_attempts + 1):
            return_code = _execute_target(target, result_dir)
            try:
                if return_code != 0:
                    raise RuntimeError(f"Notebook returned {return_code}")
                _validate_result(result_dir, key)
                completed = True
                run_manifest["results"][key] = {
                    "status": "complete",
                    "attempts": attempt,
                    "completed_at_utc": _utc_now(),
                }
                break
            except (FileNotFoundError, KeyError, OSError, RuntimeError, ValueError) as exc:
                run_manifest["results"][key] = {
                    "status": "failed",
                    "attempts": attempt,
                    "error": str(exc),
                }
                _write_json(run_manifest_path, run_manifest)
        if not completed:
            failed.append(key)
        _write_json(run_manifest_path, run_manifest)

    run_manifest["completed_at_utc"] = _utc_now()
    run_manifest["status"] = "incomplete" if failed else "complete"
    run_manifest["failed_targets"] = failed
    _write_json(run_manifest_path, run_manifest)
    return 1 if failed else 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one deterministic Ceridwen DR2 shard on one Vast GPU."
    )
    parser.add_argument("--worker-output", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--targets-file", type=Path)
    parser.add_argument("--write-targets-file", type=Path)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--num-shards", type=int, default=2)
    parser.add_argument("--base-seed", type=int, default=DEFAULT_BASE_SEED)
    parser.add_argument("--only-target")
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument(
        "--minimum-gpu-memory-mib",
        type=int,
        default=DEFAULT_MINIMUM_GPU_MEMORY_MIB,
    )
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--monitor", action="store_true")
    parser.add_argument("--monitor-instance", action="append", default=[])
    parser.add_argument("--credit-baseline", type=float)
    parser.add_argument("--spend-cap", type=float, default=20.0)
    parser.add_argument("--poll-seconds", type=float, default=300.0)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.worker_output is not None:
        return _worker(args.worker_output)
    if args.monitor:
        return _monitor(args)
    return _run(args)


if __name__ == "__main__":
    raise SystemExit(main())
