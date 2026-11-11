"""Restore error-free executed notebooks after a failed local figure rebuild, on CPU.

The local rebuild (scripts/experiment.py regenerate_figures) stops with KeyError 'cfe' in
scripts/plot_prior_kl.py for C/N fits and writes the failed notebook over the GPU one.
This re-executes the same compact notebook with plots off (as on the GPU), from pinned code
and the saved samples. The sampler is not rerun; the GPU derived outputs are restored byte
for byte. Usage: ceridwen/.venv/bin/python results/chronometer-135-2026-11-10/recover.py <run dir>
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


def main(run):
    os.nice(10)
    manifest = json.loads((run / "manifest.json").read_text())
    revision = manifest["source"]["commit"]
    template = nbformat.reads(subprocess.check_output(
        ["git", "show", f"{revision}:notebooks/ceridwen_integrated_photometry_spectra.ipynb"],
        cwd=ROOT, text=True), as_version=4)
    grids = {g["remote_name"]: g["grid"] for g in manifest["source"]["grids"]}
    receipt_path = run / "recovery.json"
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {
        "source_commit": revision, "method": __doc__.split("\n\n")[0], "fits": {}}
    todo = []
    for cell in manifest["source"]["experiment"]:
        directory = run / "fits" / cell["arm"] / f"{cell['target_metadata']['object_id']}-{cell['target']}"
        try:
            validate_result(directory)
        except ValueError as error:
            if "executed notebook contains an error" not in str(error):
                raise
            todo.append((cell, directory))
    print(f"{len(todo)} notebooks to restore", flush=True)
    with tempfile.TemporaryDirectory(prefix="chronometer-recover-") as temporary:
        paths = []
        for tree, commit in manifest["source"]["submodules"].items():
            destination = Path(temporary) / tree
            destination.mkdir(parents=True)
            archive = subprocess.check_output(["git", "archive", commit], cwd=ROOT / tree)
            with tarfile.open(fileobj=io.BytesIO(archive)) as contents:
                contents.extractall(destination, filter="data")
            paths.append(str(destination))
        environment = {**os.environ, "PYTHONPATH": os.pathsep.join(paths), "CERIDWEN_PLOTS": "0",
                       "JAX_PLATFORMS": "cpu", "MPLBACKEND": "Agg", "SPS_HOME": str(ROOT / "external/fsps"),
                       "OMP_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2"}
        client = NotebookClient(nbformat.v4.new_notebook(), timeout=None, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        with client.setup_kernel(env=environment):
            for cell, directory in todo:
                result, derived = directory / "ceridwen_result.h5", directory / "ceridwen_derived_outputs.h5"
                result_hash, gpu_derived = digest(result), derived.read_bytes()
                settings = dict(cell["settings"])
                settings["ssp_grid"] = grids[Path(settings["ssp_grid"]).name]
                with patch.object(regenerate.nbformat, "read", return_value=copy.deepcopy(template)):
                    notebook = regenerate.compact_notebook(directory, regenerate.stored_fit(directory),
                                                           settings, cell["priors"])
                notebook.metadata["offline_recovery"] = {"source_commit": revision, "sample_sha256": result_hash,
                                                         "plots": False, "sampler_rerun": False}
                executed = directory / f"{cell['target']}_executed.ipynb"
                executed.rename(directory / f"{cell['target']}_rebuild_failed.ipynb")
                client.nb = notebook
                client.reset_execution_trackers()
                try:
                    for index, notebook_cell in enumerate(notebook.cells):
                        client.execute_cell(notebook_cell, index)
                finally:
                    nbformat.write(notebook, executed)
                    derived.write_bytes(gpu_derived)
                assert digest(result) == result_hash, "saved posterior changed"
                validate_result(directory)
                receipt["fits"][cell["name"]] = {"sample_sha256": result_hash,
                                                 "derived_sha256": hashlib.sha256(gpu_derived).hexdigest(),
                                                 "sampler_rerun": False, "validated": True}
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
                print(f"validated {cell['name']}", flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
