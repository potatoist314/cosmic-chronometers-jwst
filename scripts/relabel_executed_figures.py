"""Redraw the spectrum figures of executed fit notebooks with absorption-feature labels.

Method notes
------------
- Source: ``ceridwen_result.h5`` and ``ceridwen_derived_outputs.h5`` beside each
  executed notebook. No model is rebuilt and no fit is rerun.
- The fit figure (cell with ``native LEGA-C versus joint``) and the posterior-
  predictive spectrum figure (second image of the ``posterior_batch`` cell) are
  redrawn by ``per_galaxy_diagnostics`` and replace the saved ``image/png`` in place.
- Sampler progress lines leave the fit cell's saved output only when every
  removed line is present in ``execution.log`` beside the notebook.
- No cell is added, removed or reordered. Each changed cell gets the metadata
  key ``relabelled_by``; a notebook that has it, or whose fit cell already calls
  ``mark_absorption_features``, is left alone. Git history keeps the originals.

Usage
-----
``ceridwen/.venv/bin/python scripts/relabel_executed_figures.py [ROOT ...] [--limit N]``
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import per_galaxy_diagnostics as pgd  # noqa: E402

FIT_CELL_TEXT = "native LEGA-C versus joint"
PREDICTIVE_CELL_TEXT = "def posterior_batch("
SAMPLER_CELL_TEXT = "run_sampler("
MARKER = "relabelled_by"
MARKER_VALUE = "scripts/relabel_executed_figures.py"
NOTEBOOK_DPI = 100
PROGRESS_LINE = re.compile(r"^\s*\[iter\s+\d+\]")
PROGRESS_BAR = "\rNS "


def _source(cell) -> str:
    return "".join(cell["source"])


def _image_outputs(cell) -> list[dict]:
    return [o for o in cell.get("outputs", []) if "image/png" in o.get("data", {})]


def _png(fig) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=NOTEBOOK_DPI)
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode("ascii") + "\n"


def strip_progress(cell, log_text: str) -> int:
    """Remove sampler progress from a cell's stream outputs; return the lines removed."""
    kept, removed = [], []
    for output in cell["outputs"]:
        if output["output_type"] != "stream":
            kept.append(output)
            continue
        text = "".join(output["text"])
        if output["name"] == "stderr" and (text.startswith(PROGRESS_BAR) or not text.strip()):
            removed.append(text)
            continue
        lines = text.splitlines(keepends=True)
        rest = [line for line in lines if not PROGRESS_LINE.match(line)]
        removed.extend(line for line in lines if PROGRESS_LINE.match(line))
        if rest:
            kept.append({**output, "text": rest})
    if not all(text.strip("\r\n") in log_text for text in removed):
        return 0
    cell["outputs"] = kept
    return len(removed)


def relabel(notebook_path: Path) -> str:
    """Relabel one executed notebook in place; return a one-word status plus detail."""
    folder = notebook_path.parent
    if not ((folder / "ceridwen_result.h5").exists() and (folder / "ceridwen_derived_outputs.h5").exists()):
        return "skipped: no stored arrays"
    notebook = json.loads(notebook_path.read_text())
    cells = notebook["cells"]
    fit = [c for c in cells if c["cell_type"] == "code" and FIT_CELL_TEXT in _source(c)]
    predictive = [c for c in cells if c["cell_type"] == "code" and PREDICTIVE_CELL_TEXT in _source(c)]
    if len(fit) != 1 or len(predictive) != 1:
        return "skipped: no single fit and predictive cell"
    fit, predictive = fit[0], predictive[0]
    if MARKER in fit["metadata"] or "mark_absorption_features" in _source(fit):
        return "skipped: already labelled"
    if len(_image_outputs(fit)) != 1 or len(_image_outputs(predictive)) != 2:
        return "skipped: unexpected figure outputs"

    galaxy = pgd.load_galaxy(folder)
    _image_outputs(fit)[0]["data"]["image/png"] = _png(pgd.plot_fit_spectrum(galaxy))
    _image_outputs(predictive)[1]["data"]["image/png"] = _png(pgd.plot_predictive_spectrum(galaxy))
    fit["metadata"][MARKER] = predictive["metadata"][MARKER] = MARKER_VALUE

    removed = 0
    log = folder / "execution.log"
    sampler = [c for c in cells if c["cell_type"] == "code" and SAMPLER_CELL_TEXT in _source(c)]
    if log.exists() and len(sampler) == 1:
        removed = strip_progress(sampler[0], log.read_text(errors="replace"))
        if removed:
            sampler[0]["metadata"][MARKER] = MARKER_VALUE
    notebook_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    return f"relabelled: {removed} progress lines moved out"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("roots", nargs="*", type=Path, default=[PROJECT_ROOT / "results"])
    parser.add_argument("--limit", type=int, default=None, help="stop after this many relabelled notebooks")
    args = parser.parse_args()
    done = 0
    for root in args.roots:
        for path in sorted(root.rglob("*executed*.ipynb")):
            status = relabel(path)
            print(f"{path.relative_to(PROJECT_ROOT) if path.is_absolute() else path}: {status}", flush=True)
            done += status.startswith("relabelled")
            if args.limit is not None and done >= args.limit:
                return


if __name__ == "__main__":
    main()
