#!/usr/bin/env python3
"""Re-execute the compact fit notebook on stored fits without re-running the sampler.

For each result directory the script reads ``ceridwen_result.h5`` (target,
seed, manifest index, calibration order, photometry source, tau prior bounds, sampled parameters),
sets those literals in the top cell of
``notebooks/ceridwen_integrated_photometry_spectra.ipynb``, replaces the
``run_sampler``/``write_result_h5`` block by ``load_result_h5`` of the stored
file, executes the notebook on the local CPU in ``ceridwen/.venv`` and writes
``<TARGET_ID>_executed.ipynb`` in place of the old executed copy. The derived
outputs cell rewrites ``ceridwen_derived_outputs.h5`` from the same posterior
and seeds.

Usage::

    ceridwen/.venv/bin/python scripts/regenerate_fit_notebooks.py [--dry-run] DIR [DIR ...]
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import h5py
import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"


def stored_fit(result_dir: Path) -> dict:
    with h5py.File(result_dir / "ceridwen_result.h5", "r") as result_file:
        attrs = result_file["model"].attrs
        names = [
            name.decode() if isinstance(name, bytes) else str(name)
            for name in result_file["model/param_names"][()]
        ]
        tau_line = next(
            line for line in attrs["parameter_block"].splitlines() if line.strip().startswith("diffuse_tau_kc:")
        )
        low, high = re.search(r"Uniform\(([^,]+), ([^)]+)\)", tau_line).groups()
        return {
            "target_id": result_dir.name.split("-", 1)[1],
            "seed": int(attrs["random_seed"]),
            "manifest_index": int(attrs["manifest_index"]),
            "calibration_order": int(attrs["calibration_order"]),
            "photometry": str(attrs.get("photometry_source", "cosmos_total")),
            "tau_bounds": (float(low), float(high)),
            "free_zred": "zred" in names,
            "free_sigma": "sigma_smooth" in names,
        }


def compact_notebook(result_dir: Path, fit: dict) -> nbformat.NotebookNode:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    top = notebook.cells[2]
    assert top.source.startswith("import os")
    replacements = [
        (r'TARGET_ID = os\.environ\.get\("CERIDWEN_TARGET_ID", "[^"]*"\)', f'TARGET_ID = "{fit["target_id"]}"'),
        (r'MANIFEST_INDEX = int\(os\.environ\.get\("CERIDWEN_MANIFEST_INDEX", "\d+"\)\)', f'MANIFEST_INDEX = {fit["manifest_index"]}'),
        (r'SEED = int\(os\.environ\.get\("CERIDWEN_RANDOM_SEED", "\d+"\)\)', f'SEED = {fit["seed"]}'),
        (r'RESULT_DIR = Path\(os\.environ\.get\("CERIDWEN_RESULT_DIR", [^\n]*\)\)', f'RESULT_DIR = PROJECT_ROOT / "{result_dir.relative_to(PROJECT_ROOT)}"'),
        (r'QUICK = os\.environ\.get\("CERIDWEN_NOTEBOOK_QUICK"\) == "1"', "QUICK = False"),
        (r'"calibration_order": \d+,', f'"calibration_order": {fit["calibration_order"]},'),
        (r'"photometry": "[^"]*",', f'"photometry": "{fit["photometry"]}",'),
        (r'"diffuse_tau_kc": Uniform\(low=[^)]*\),', f'"diffuse_tau_kc": Uniform(low={fit["tau_bounds"][0]:g}, high={fit["tau_bounds"][1]:g}),'),
    ]
    if not fit["free_zred"]:
        replacements.append((r'\n    "zred": "[^\n]*\n', "\n"))
    if not fit["free_sigma"]:
        replacements.append((r'\n    "sigma_smooth": "[^\n]*\n', "\n"))
    for pattern, replacement in replacements:
        top.source, count = re.subn(pattern, replacement, top.source)
        assert count == 1, pattern
    top.source = top.source.replace(
        "from ceridwen.fit import write_result_h5", "from ceridwen.fit import load_result_h5"
    )

    fit_markdown = notebook.cells[9]
    fit_cell = notebook.cells[10]
    assert "joint_result = run_sampler(" in fit_cell.source
    head, _ = fit_cell.source.split("joint_result = run_sampler(", 1)
    fit_cell.source = head + 'joint_result = load_result_h5(RESULT_DIR / "ceridwen_result.h5")\nprint(joint_result.summary())'
    fit_markdown.source += "\n- Posterior reloaded from the stored fit; the sampler is not re-run."
    return notebook


def execute(notebook: nbformat.NotebookNode, output_path: Path) -> None:
    from nbclient import NotebookClient

    metadata = dict(notebook.metadata)
    client = NotebookClient(
        notebook,
        timeout=None,
        kernel_name="python3",
        resources={"metadata": {"path": str(PROJECT_ROOT)}},
    )
    try:
        client.execute()
    finally:
        notebook.metadata = metadata
        nbformat.write(notebook, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("result_dirs", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="print the per-fit literals and stop")
    args = parser.parse_args()
    failed = 0
    for result_dir in args.result_dirs:
        result_dir = result_dir.resolve()
        fit = stored_fit(result_dir)
        line = (
            f"{result_dir.relative_to(PROJECT_ROOT)}  seed={fit['seed']} order={fit['calibration_order']} "
            f"tau={fit['tau_bounds']} zred={fit['free_zred']} sigma={fit['free_sigma']}"
        )
        if args.dry_run:
            print(line)
            continue
        started = time.perf_counter()
        notebook = compact_notebook(result_dir, fit)
        output_path = result_dir / f"{fit['target_id']}_executed.ipynb"
        try:
            execute(notebook, output_path)
        except Exception as error:  # noqa: BLE001
            print(f"{line}  FAILED {type(error).__name__}: {str(error).splitlines()[0][:200]}", flush=True)
            failed += 1
            continue
        print(f"{line}  ok {time.perf_counter() - started:.0f}s", flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
