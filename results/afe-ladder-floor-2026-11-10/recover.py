"""Recover fixed-afe derived outputs from pinned code and saved samples, on CPU.

Run with ceridwen/.venv/bin/python after experiment.py finishes retrieval.
The production notebook stays untouched. Original failed notebooks and logs stay.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
from unittest.mock import patch

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import regenerate_fit_notebooks as regenerate
from experiment import validate_result


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    os.nice(10)
    manifest_path = OUT / "run/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    revision = manifest["source"]["commit"]
    source = subprocess.check_output([
        "git", "show", f"{revision}:notebooks/ceridwen_integrated_photometry_spectra.ipynb"
    ], cwd=ROOT, text=True)
    template = nbformat.reads(source, as_version=4)
    grids = {g["remote_name"]: g["grid"] for g in manifest["source"]["grids"]}
    receipt_path = OUT / "recovery.json"
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {
        "source_commit": revision,
        "method": "existing compact_notebook; load_result_h5; fixed afe in local export only; plots disabled",
        "fits": {},
    }
    cells = [c for c in manifest["source"]["experiment"] if c["settings"]["fix_afe"] is not None]
    with tempfile.TemporaryDirectory(prefix="afe-postprocess-") as temporary:
        pinned = Path(temporary)
        paths = []
        for tree, commit in manifest["source"]["submodules"].items():
            destination = pinned / tree
            destination.mkdir(parents=True)
            archive = subprocess.check_output(["git", "archive", commit], cwd=ROOT / tree)
            with tarfile.open(fileobj=io.BytesIO(archive)) as contents:
                contents.extractall(destination, filter="data")
            paths.append(str(destination))
        environment = {
            **os.environ,
            "PYTHONPATH": os.pathsep.join(paths),
            "CERIDWEN_PLOTS": "0", "JAX_PLATFORMS": "cpu", "MPLBACKEND": "Agg",
            "SPS_HOME": str(ROOT / "external/fsps"),
            "OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2",
        }
        client = NotebookClient(nbformat.v4.new_notebook(), timeout=None, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        with client.setup_kernel(env=environment):
            for cell in cells:
                directory = OUT / "run/fits" / cell["arm"] / f"{cell['target_metadata']['object_id']}-{cell['target']}"
                result = directory / "ceridwen_result.h5"
                original_hash = digest(result)
                if cell["name"] in receipt["fits"]:
                    assert receipt["fits"][cell["name"]]["sample_sha256"] == original_hash
                    validate_result(directory)
                    continue
                settings = dict(cell["settings"])
                settings["ssp_grid"] = grids[Path(settings["ssp_grid"]).name]
                with patch.object(regenerate.nbformat, "read", return_value=copy.deepcopy(template)):
                    notebook = regenerate.compact_notebook(directory, regenerate.stored_fit(directory),
                                                           settings, cell["priors"])
                summary = next(c for c in notebook.cells if "def scalar_draws(name):" in c.source)
                marker = "def scalar_draws(name):"
                summary.source = summary.source.replace(marker,
                    'selected_posterior["afe"] = np.full((len(posterior_indices), 1), SETTINGS["fix_afe"])\n\n' + marker,
                    1)
                notebook.metadata["offline_recovery"] = {
                    "source_commit": revision, "sample_sha256": original_hash,
                    "fixed_afe": settings["fix_afe"], "sampler_rerun": False,
                }
                executed = directory / f"{cell['target']}_executed.ipynb"
                failed = directory / f"{cell['target']}_failed.ipynb"
                if not failed.exists():
                    executed.rename(failed)
                client.nb = notebook
                client.reset_execution_trackers()
                print(f"recovering {cell['name']}", flush=True)
                try:
                    for index, notebook_cell in enumerate(notebook.cells):
                        client.execute_cell(notebook_cell, index)
                finally:
                    nbformat.write(notebook, executed)
                assert digest(result) == original_hash, "saved posterior changed"
                validate_result(directory)
                receipt["fits"][cell["name"]] = {
                    "sample_sha256": original_hash, "fixed_afe": settings["fix_afe"],
                    "sampler_rerun": False, "validated": True,
                }
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
                print(f"validated {cell['name']}", flush=True)
    for cell in cells:
        if cell["name"] not in manifest["completed_cells"]:
            manifest["completed_cells"].append(cell["name"])
    manifest["offline_recovery"] = {
        "receipt": "../recovery.json", "cells": list(receipt["fits"]),
        "sampler_rerun": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Recovered {len(cells)} fixed-afe fits without resampling", flush=True)


if __name__ == "__main__":
    main()
