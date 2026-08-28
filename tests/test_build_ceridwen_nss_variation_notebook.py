import json
import re
from pathlib import Path

from scripts.build_ceridwen_nss_variation_notebook import build_notebook

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MASKED_CONNECTED_SPECTRUM = re.compile(
    r"\.(?:plot|errorbar|fill_between)\(\s*"
    r"(?:spectrum_wave|wave_vacuum|wave)\s*"
    r"\[\s*[A-Za-z_]\w*(?:mask|valid)\s*\]"
)


def _notebook_source(notebook):
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_builds_complete_variation_notebook(tmp_path):
    output = tmp_path / "variation.ipynb"
    build_notebook(output)

    notebook = json.loads(output.read_text(encoding="utf-8"))
    source = _notebook_source(notebook)

    assert "default-default: 6 pairs" in source
    assert notebook["metadata"]["kernelspec"]["name"] == "ceridwen"
    assert "matched fast-default: 4 pairs" in source
    assert "mass_weighted_age_gyr" in source
    assert "posterior_predictive_spectra.png" in source
    assert "combined_physical_corner.png" in source
    assert source.index("sys.path.insert") < source.index("from scripts import")
    assert "run_sampler(" not in source
    assert all(
        cell.get("cell_type") != "code"
        or (cell["execution_count"] is None and cell["outputs"] == [])
        for cell in notebook["cells"]
    )


def test_connected_spectrum_plots_keep_full_wavelength_grid(tmp_path):
    generated_path = tmp_path / "variation.ipynb"
    build_notebook(generated_path)
    notebook_paths = [
        *sorted((PROJECT_ROOT / "notebooks").glob("ceridwen*.ipynb")),
        generated_path,
    ]

    violations = []
    for notebook_path in notebook_paths:
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        for match in MASKED_CONNECTED_SPECTRUM.finditer(_notebook_source(notebook)):
            violations.append(f"{notebook_path}: {match.group(0)}")

    assert violations == []
