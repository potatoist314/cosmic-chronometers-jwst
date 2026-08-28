import json

from scripts.build_ceridwen_nss_variation_notebook import build_notebook


def test_builds_complete_variation_notebook(tmp_path):
    output = tmp_path / "variation.ipynb"
    build_notebook(output)

    notebook = json.loads(output.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", [])) for cell in notebook["cells"]
    )

    assert "default-default: 6 pairs" in source
    assert "matched fast-default: 4 pairs" in source
    assert "mass_weighted_age_gyr" in source
    assert "posterior_predictive_spectra.png" in source
    assert "combined_physical_corner.png" in source
    assert "run_sampler(" not in source
    assert all(
        cell.get("cell_type") != "code"
        or (cell["execution_count"] is None and cell["outputs"] == [])
        for cell in notebook["cells"]
    )
