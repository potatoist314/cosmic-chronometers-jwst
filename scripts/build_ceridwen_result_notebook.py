#!/usr/bin/env python3
"""Build a report-only Ceridwen notebook for one completed NSS result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class NotebookBuildError(RuntimeError):
    """Report an incompatible source notebook."""


def _source(cell: dict[str, Any]) -> str:
    return "".join(cell.get("source", []))


def _set_source(cell: dict[str, Any], source: str) -> None:
    cell["source"] = source.splitlines(keepends=True)


def _replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise NotebookBuildError(f"expected one notebook source match: {old!r}")
    return source.replace(old, new)


def _code_cell_after_heading(notebook: dict[str, Any], heading: str) -> dict[str, Any]:
    cells = notebook["cells"]
    for index, cell in enumerate(cells[:-1]):
        if cell.get("cell_type") == "markdown" and heading in _source(cell):
            following = cells[index + 1]
            if following.get("cell_type") != "code":
                break
            return following
    raise NotebookBuildError(f"missing code cell after heading: {heading}")


def build_notebook(source_path: Path, output_path: Path) -> None:
    notebook = json.loads(source_path.read_text(encoding="utf-8"))
    if not notebook.get("cells"):
        raise NotebookBuildError("source notebook has no cells")

    title = notebook["cells"][0]
    _set_source(
        title,
        "# Completed Ceridwen photometry and spectrum fit\n\n"
        "This report loads one converged NSS result. It does not rerun the sampler.\n",
    )

    setup = _code_cell_after_heading(notebook, "## Setup")
    setup_source = _source(setup)
    setup_source = _replace_once(setup_source, "import os\n", "import json\nimport os\n")
    _set_source(setup, setup_source)

    model = _code_cell_after_heading(notebook, "## Joint model")
    model_source = _source(model)
    selector_code = (
        "requested_implementation = os.environ.get(\n"
        "    \"CERIDWEN_SFH_BASIS_FASTPATH\", \"baseline\"\n"
        ")\n"
        "if requested_implementation == \"A\":\n"
        "    joint_csp.select_sfh_basis_fastpath(\"A\")\n"
        "elif requested_implementation != \"baseline\":\n"
        "    raise ValueError(\n"
        "        f\"Unsupported SFH-basis implementation: {requested_implementation}\"\n"
        "    )\n"
        "print(f\"SFH-basis implementation: {requested_implementation}\")\n\n"
    )
    model_source = _replace_once(
        model_source,
        "initial_photometry = np.asarray(\n",
        selector_code + "initial_photometry = np.asarray(\n",
    )
    _set_source(model, model_source)

    posterior = _code_cell_after_heading(notebook, "## Joint posterior")
    _set_source(
        posterior,
        "result_path = RESULT_DIR / \"ceridwen_result.h5\"\n"
        "manifest_path = RESULT_DIR / \"run.json\"\n"
        "run_manifest = json.loads(manifest_path.read_text(encoding=\"utf-8\"))\n"
        "if run_manifest.get(\"status\") != \"complete\":\n"
        "    raise RuntimeError(f\"Result is not complete: {manifest_path}\")\n"
        "recorded_implementation = run_manifest[\"implementation\"][\n"
        "    \"sfh_basis_fastpath\"\n"
        "]\n"
        "if recorded_implementation != requested_implementation:\n"
        "    raise RuntimeError(\n"
        "        \"Notebook implementation does not match run.json: \"\n"
        "        f\"{requested_implementation} != {recorded_implementation}\"\n"
        "    )\n"
        "joint_settings = run_manifest[\"science_contract\"][\"sampler\"]\n"
        "joint_result = load_result_h5(result_path)\n"
        "RUN_PROFILE = \"completed-fit\"\n"
        "print(f\"loaded converged result: {result_path}\")\n"
        "print(f\"sampler settings: {joint_settings}\")\n"
        "print(joint_result.summary())\n",
    )

    diagnostics = _code_cell_after_heading(notebook, "## Sampling diagnostics")
    diagnostics_source = _source(diagnostics)
    diagnostics_source = _replace_once(
        diagnostics_source,
        'if RUN_PROFILE == "gpu-full" and joint_diagnostics_passed',
        'if run_manifest["status"] == "complete" and joint_diagnostics_passed',
    )
    _set_source(diagnostics, diagnostics_source)

    data_cell = _code_cell_after_heading(notebook, "## Spectroscopic observation")
    data_source = _source(data_cell)
    data_source = _replace_once(
        data_source,
        "plt.tight_layout()\nplt.show()",
        "plt.tight_layout()\n"
        "fig.savefig(RESULT_DIR / \"input_photometry_spectrum.png\", dpi=180, bbox_inches=\"tight\")\n"
        "plt.show()",
    )
    _set_source(data_cell, data_source)

    predictive = _code_cell_after_heading(notebook, "## Posterior predictive checks")
    predictive_source = _source(predictive)
    marker = "plt.tight_layout()\nplt.show()"
    if predictive_source.count(marker) != 2:
        raise NotebookBuildError("expected two posterior-predictive figures")
    predictive_source = predictive_source.replace(
        marker,
        "plt.tight_layout()\n"
        "fig.savefig(RESULT_DIR / \"photometry_posterior_fit.png\", dpi=180, bbox_inches=\"tight\")\n"
        "plt.show()",
        1,
    )
    predictive_source = predictive_source.replace(
        marker,
        "plt.tight_layout()\n"
        "fig.savefig(RESULT_DIR / \"spectrum_posterior_fit.png\", dpi=180, bbox_inches=\"tight\")\n"
        "plt.show()",
        1,
    )
    _set_source(predictive, predictive_source)

    native = _code_cell_after_heading(notebook, "## Full native-spectrum comparison")
    native_source = _source(native)
    native_source = _replace_once(
        native_source,
        "plt.tight_layout()\nplt.show()",
        "plt.tight_layout()\n"
        "fig.savefig(RESULT_DIR / \"spectrum_native_fit.png\", dpi=180, bbox_inches=\"tight\")\n"
        "plt.show()",
    )
    _set_source(native, native_source)

    population = _code_cell_after_heading(notebook, "## Population summary")
    population_source = _source(population)
    population_source = _replace_once(
        population_source,
        "ax.set(\n"
        "    yscale=\"log\",\n"
        "    xlabel=\"lookback time [Gyr]\",\n"
        "    ylabel=\"normalized SFR\",\n"
        ")\n"
        "plt.show()",
        "ax.set(\n"
        "    yscale=\"log\",\n"
        "    xlabel=\"lookback time [Gyr]\",\n"
        "    ylabel=\"normalized SFR\",\n"
        ")\n"
        "fig.savefig(RESULT_DIR / \"sfh_age_history.png\", dpi=180, bbox_inches=\"tight\")\n"
        "plt.show()",
    )
    _set_source(population, population_source)

    for cell in notebook["cells"]:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    notebook.setdefault("metadata", {})["kernelspec"] = {
        "display_name": "Ceridwen (Vast.ai GPU)",
        "language": "python",
        "name": "ceridwen",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    project_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--source",
        type=Path,
        default=project_root / "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build_notebook(args.source.resolve(), args.output.resolve())
    print(f"saved result-report notebook: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
