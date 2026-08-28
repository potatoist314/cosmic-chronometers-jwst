import json
from pathlib import Path

from scripts.build_ceridwen_result_notebook import build_notebook

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_builds_report_only_notebook_with_saved_figures(tmp_path):
    output = tmp_path / "report.ipynb"
    build_notebook(
        PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
        output,
    )

    notebook = json.loads(output.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) for cell in notebook["cells"]
    )

    assert "run_sampler(" not in source
    assert "loaded converged result" in source
    assert "CERIDWEN_SFH_BASIS_FASTPATH" in source
    for filename in (
        "input_photometry_spectrum.png",
        "photometry_posterior_fit.png",
        "spectrum_posterior_fit.png",
        "spectrum_native_fit.png",
        "corner_physical.png",
        "corner_age_mass_fractions.png",
        "sfh_age_history.png",
    ):
        assert filename in source
    assert all(
        cell.get("cell_type") != "code"
        or (cell["execution_count"] is None and cell["outputs"] == [])
        for cell in notebook["cells"]
    )
