#!/usr/bin/env python3
"""Run the absorption-line pixel-mask experiment as a grid of notebook fits.

Every cell executes ``notebooks/ceridwen_integrated_photometry_spectra.ipynb``
once through the same worker the DR2 shard runner uses, with the cell's
environment (pixel-selection mode, mock settings, seeds).  Cells that share a
``group`` are one comparison (the three pixel modes of one target or one mock
realisation) and always run on the same machine, in sequence.

Sub-commands::

    make-grid  [--out results/absorption-mask/grid.json]
    run        --grid grid.json [--shard k/n] [--only-group NAME] [--quick] [--gpu]
    status     --grid grid.json [--output-root DIR]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = PROJECT_ROOT / "scripts/run_ceridwen_vast_multi_gpu.py"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "results/absorption-mask"
DEFAULT_GRID = DEFAULT_OUTPUT_ROOT / "grid.json"
DEFAULT_TRUTH = "results/absorption-mask/truth_M5_172669.json"
BASE_SEED = 20260902

MODES = {
    "all": {"CERIDWEN_SPECTRUM_PIXELS": "all"},
    "features": {"CERIDWEN_SPECTRUM_PIXELS": "features"},
    "features_downweight": {
        "CERIDWEN_SPECTRUM_PIXELS": "features_downweight",
        "CERIDWEN_FEATURE_DOWNWEIGHT": "balance",
    },
}
REAL_TARGETS = {"M5_172669": 172669, "M9_232005": 232005, "M11_214430": 214430}
MOCK_TARGET = ("M5_172669", 172669)
MOCK_TILTS = (0.0, 0.03, 0.06)
MOCK_SNR_SCALES = (1.0, 0.25)
MOCK_SEEDS = (1, 2)
WINDOW_KMS = 1000.0


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def make_grid() -> list[dict]:
    cells = []
    group_index = 0
    for spect_id, object_id in REAL_TARGETS.items():
        group = f"real_{spect_id}"
        for mode, env in MODES.items():
            cells.append({
                "name": f"{group}_{mode}", "group": group, "mode": mode,
                "target": spect_id, "object_id": object_id,
                "seed": BASE_SEED + group_index,
                "env": {"CERIDWEN_FEATURE_WINDOW_KMS": str(WINDOW_KMS), **env},
            })
        group_index += 1
    for tilt in MOCK_TILTS:
        for snr in MOCK_SNR_SCALES:
            for seed in MOCK_SEEDS:
                group = f"mock_tilt{tilt:.2f}_snr{snr:.2f}_seed{seed}"
                mock_env = {
                    "CERIDWEN_MOCK_TRUTH": DEFAULT_TRUTH,
                    "CERIDWEN_MOCK_SEED": str(1000 * seed + int(round(100 * tilt)) + int(round(10 * snr))),
                    "CERIDWEN_MOCK_TILT": f"{tilt:.4f}",
                    "CERIDWEN_MOCK_SNR_SCALE": f"{snr:.4f}",
                    "CERIDWEN_FEATURE_WINDOW_KMS": str(WINDOW_KMS),
                }
                for mode, env in MODES.items():
                    cells.append({
                        "name": f"{group}_{mode}", "group": group, "mode": mode,
                        "target": MOCK_TARGET[0], "object_id": MOCK_TARGET[1],
                        "seed": BASE_SEED + group_index,
                        "env": {**mock_env, **env},
                    })
                group_index += 1
    return cells


def shard_groups(cells: list[dict], shard: str | None) -> list[dict]:
    if not shard:
        return cells
    k, n = (int(part) for part in shard.split("/"))
    groups = sorted({cell["group"] for cell in cells})
    keep = {group for index, group in enumerate(groups) if index % n == k}
    return [cell for cell in cells if cell["group"] in keep]


def _load_runner():
    spec = importlib.util.spec_from_file_location("dr2_runner", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _cell_environment(cell: dict, result_dir: Path, quick: bool, gpu: bool) -> dict:
    env = {
        **os.environ,
        "CERIDWEN_FIT_MODE": "full_spectrum",
        "CERIDWEN_NOTEBOOK_QUICK": "1" if quick else "0",
        "CERIDWEN_PROJECT_ROOT": str(PROJECT_ROOT),
        "CERIDWEN_RANDOM_SEED": str(cell["seed"]),
        "CERIDWEN_RESULT_DIR": str(result_dir),
        "CERIDWEN_TARGET_ID": cell["target"],
        "CERIDWEN_OBJECT_ID": str(cell["object_id"]),
        "CERIDWEN_MANIFEST_INDEX": "0",
        **cell["env"],
    }
    if gpu:
        env["CERIDWEN_EXPECT_SINGLE_GPU"] = "1"
    truth = env.get("CERIDWEN_MOCK_TRUTH")
    if truth and not Path(truth).is_absolute():
        env["CERIDWEN_MOCK_TRUTH"] = str(PROJECT_ROOT / truth)
    return env


def _write_json(path: Path, value) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value, indent=1))
    tmp.replace(path)


def _manifest_path(output_root: Path, shard: str | None) -> Path:
    suffix = f"_shard{shard.replace('/', 'of')}" if shard else ""
    return output_root / f"grid_manifest{suffix}.json"


def run(args) -> int:
    cells = json.loads(Path(args.grid).read_text())
    cells = shard_groups(cells, args.shard)
    if args.only_group:
        cells = [cell for cell in cells if cell["group"] in set(args.only_group)]
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    manifest_path = _manifest_path(output_root, args.shard)
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    runner = _load_runner()
    for cell in cells:
        record = manifest.get(cell["name"], {})
        result_dir = output_root / cell["name"]
        if record.get("status") == "done" and (result_dir / "ceridwen_result.h5").exists():
            continue
        for attempt in range(1, args.max_attempts + 1):
            started = time.monotonic()
            manifest[cell["name"]] = {
                "status": "running", "attempt": attempt, "started": _utc_now(),
                "group": cell["group"], "mode": cell["mode"], "target": cell["target"],
            }
            _write_json(manifest_path, manifest)
            result_dir.mkdir(parents=True, exist_ok=True)
            notebook = result_dir / f"{cell['target']}_executed.ipynb"
            log_path = result_dir / "execution.log"
            with log_path.open("a", encoding="utf-8") as log:
                log.write(f"\n[{_utc_now()}] {cell['name']} attempt {attempt}\n")
                log.flush()
                code = subprocess.run(
                    [sys.executable, str(RUNNER_PATH), "--worker-output", str(notebook)],
                    cwd=PROJECT_ROOT,
                    env=_cell_environment(cell, result_dir, args.quick, args.gpu),
                    stdout=log, stderr=subprocess.STDOUT, text=True,
                ).returncode
            wall = time.monotonic() - started
            error = None
            if code == 0 and not args.quick:
                try:
                    runner._validate_result(result_dir, cell["target"])
                except Exception as exc:  # noqa: BLE001 - recorded, not hidden
                    error = f"validation: {exc}"
            elif code != 0:
                error = f"worker exit {code}"
            manifest[cell["name"]].update({
                "status": "done" if error is None else "failed",
                "wall_s": round(wall, 1), "finished": _utc_now(), "error": error,
            })
            _write_json(manifest_path, manifest)
            print(f"{cell['name']}: {manifest[cell['name']]['status']} in {wall:.0f} s"
                  + (f" ({error})" if error else ""), flush=True)
            if error is None:
                break
    failed = [name for name, rec in manifest.items() if rec.get("status") != "done"]
    return 1 if failed else 0


def status(args) -> int:
    output_root = Path(args.output_root)
    records = {}
    for path in sorted(output_root.glob("grid_manifest*.json")):
        records.update(json.loads(path.read_text()))
    cells = json.loads(Path(args.grid).read_text())
    for cell in cells:
        rec = records.get(cell["name"], {"status": "pending"})
        print(f"{cell['name']:<48} {rec.get('status'):<8} {rec.get('wall_s', ''):>7} {rec.get('error') or ''}")
    counts = {}
    for cell in cells:
        state = records.get(cell["name"], {}).get("status", "pending")
        counts[state] = counts.get(state, 0) + 1
    print(counts)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    mk = sub.add_parser("make-grid")
    mk.add_argument("--out", type=Path, default=DEFAULT_GRID)
    rn = sub.add_parser("run")
    rn.add_argument("--grid", type=Path, default=DEFAULT_GRID)
    rn.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    rn.add_argument("--shard", help="k/n: run the groups with index %% n == k")
    rn.add_argument("--only-group", action="append")
    rn.add_argument("--quick", action="store_true", help="16-live-point smoke profile")
    rn.add_argument("--gpu", action="store_true", help="require one pinned GPU")
    rn.add_argument("--max-attempts", type=int, default=2)
    st = sub.add_parser("status")
    st.add_argument("--grid", type=Path, default=DEFAULT_GRID)
    st.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    args = parser.parse_args(argv)
    if args.command == "make-grid":
        cells = make_grid()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        _write_json(args.out, cells)
        groups = sorted({cell["group"] for cell in cells})
        print(f"{len(cells)} cells in {len(groups)} groups -> {args.out}")
        return 0
    if args.command == "run":
        return run(args)
    return status(args)


if __name__ == "__main__":
    sys.exit(main())
