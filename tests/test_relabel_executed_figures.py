"""Relabelling an executed notebook replaces two figures and moves progress lines out."""

import base64
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(PROJECT_ROOT / "tests"))

import relabel_executed_figures as relabel  # noqa: E402
from test_per_galaxy_diagnostics import synthetic_galaxy  # noqa: E402

OLD_PNG = base64.b64encode(b"old").decode() + "\n"
PROGRESS = ["  [iter    1]    13.4 s  logZ=-2.5  ΔlogZ=9.1  dead=100\n",
            "\rNS  logZ=-2.5: 100 dead [00:13,  7.32 dead/s]"]


def stream(name, text):
    return {"output_type": "stream", "name": name, "text": [text]}


def image(png=OLD_PNG):
    return {"output_type": "display_data", "metadata": {}, "data": {"image/png": png, "text/plain": ["<Figure>"]}}


def code(source, outputs):
    return {"cell_type": "code", "execution_count": 1, "metadata": {}, "source": [source], "outputs": outputs}


def write_folder(folder, log_lines):
    notebook = {"cells": [
        code("result = run_sampler(model, likelihood, adapter, key)\n", [
            stream("stdout", "sampler settings: {}\n"), stream("stdout", PROGRESS[0]),
            stream("stderr", PROGRESS[1]), stream("stdout", "  Converged  logZ = 1.0\n")]),
        code("def posterior_batch(samples, model, count):\n", [image(), image(), stream("stdout", "chi2\n")]),
        code('axes[0].set_title(f"{TARGET_ID}: native LEGA-C versus joint C3K_HR Ceridwen fit")\n', [image()]),
    ], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    (folder / "M0_0_executed.ipynb").write_text(json.dumps(notebook, indent=1) + "\n")
    (folder / "ceridwen_result.h5").touch()
    (folder / "ceridwen_derived_outputs.h5").touch()
    (folder / "execution.log").write_text("".join(log_lines))
    return folder / "M0_0_executed.ipynb"


def run(tmp_path, monkeypatch, log_lines):
    path = write_folder(tmp_path, log_lines)
    monkeypatch.setattr(relabel.pgd, "load_galaxy", lambda folder: synthetic_galaxy())
    status = relabel.relabel(path)
    return status, json.loads(path.read_text())["cells"], path


def test_figures_replaced_and_progress_moved_out(tmp_path, monkeypatch):
    status, cells, path = run(tmp_path, monkeypatch, PROGRESS)
    assert status.startswith("relabelled: 2 ")
    assert len(cells) == 3
    assert ["".join(o["text"]) for o in cells[0]["outputs"]] == ["sampler settings: {}\n", "  Converged  logZ = 1.0\n"]
    first, second = (o["data"]["image/png"] for o in cells[1]["outputs"][:2])
    assert first == OLD_PNG                                   # photometry figure untouched
    for png in (second, cells[2]["outputs"][0]["data"]["image/png"]):
        assert base64.b64decode(png).startswith(b"\x89PNG")
    assert relabel.relabel(path) == "skipped: already labelled"


def test_progress_kept_when_the_log_lacks_it(tmp_path, monkeypatch):
    status, cells, _ = run(tmp_path, monkeypatch, PROGRESS[:1])
    assert status.startswith("relabelled: 0 ")
    assert len(cells[0]["outputs"]) == 4


def test_folder_without_stored_arrays_is_skipped(tmp_path, monkeypatch):
    path = write_folder(tmp_path, PROGRESS)
    (tmp_path / "ceridwen_derived_outputs.h5").unlink()
    before = path.read_text()
    assert relabel.relabel(path) == "skipped: no stored arrays"
    assert path.read_text() == before
