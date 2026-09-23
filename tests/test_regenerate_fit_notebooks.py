"""Local post-fit regen reproduces the GPU-executed fit notebook.

The GPU run stops after the sampler; ``regenerate_fit_notebooks.py`` runs the
post-fit cells on this machine. Printed numbers and posterior-only derived
outputs match exactly; model predictions match to 1e-3, the pre-existing
CPU/GPU platform spread (the checked-in COSMOS Mac regens show the same
~1e-4 spread against their GPU originals).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import regenerate_fit_notebooks as regen  # noqa: E402

GPU_DIR = PROJECT_ROOT / "results/emission-line-marginalisation/eline_off/210210-M1_210210"
GRID = Path.home() / ".ceridwen/grids/amist_c3k_hr_krou_afe.h5"
CATALOG = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"

needs_fit = pytest.mark.skipif(
    not (GPU_DIR / "ceridwen_result.h5").exists(), reason="needs the stored eline_off fit"
)
needs_regen_data = pytest.mark.skipif(
    not ((GPU_DIR / "ceridwen_result.h5").exists() and GRID.exists() and CATALOG.exists()),
    reason="needs the stored fit, the HR alpha grid and the LEGA-C catalogue",
)


@needs_fit
def test_stored_fit_reads_the_sampler_result():
    fit = regen.stored_fit(GPU_DIR)
    assert fit["target_id"] == "M1_210210"
    assert fit["seed"] == 20260832
    assert fit["calibration_order"] == 10
    assert fit["photometry"] == "cosmos2025"


@needs_fit
def test_compact_notebook_applies_overrides_like_the_worker():
    fit = regen.stored_fit(GPU_DIR)
    notebook = regen.compact_notebook(
        GPU_DIR, fit,
        settings_override={"emission_line_marginalisation": True},
        priors_override={"diffuse_dust_index": "Uniform(low=-3.0, high=0.4)"},
    )
    top = notebook.cells[2].source
    assert "SETTINGS.update({'emission_line_marginalisation': True})" in top
    assert "PRIORS['diffuse_dust_index'] = Uniform(low=-3.0, high=0.4)" in top
    assert 'joint_result = load_result_h5(RESULT_DIR / "ceridwen_result.h5")' in notebook.cells[10].source
    assert "run_sampler(" not in notebook.cells[10].source
    plain = regen.compact_notebook(GPU_DIR, fit)
    assert "SETTINGS.update" not in plain.cells[2].source


def _stream_lines(notebook_path):
    document = json.loads(notebook_path.read_text())
    lines = []
    for cell in document["cells"]:
        for output in cell.get("outputs", []):
            lines.extend("".join(output.get("text", []) or []).splitlines())
    return lines


@needs_regen_data
def test_regen_matches_the_gpu_executed_notebook():
    import h5py
    import numpy as np

    scratch = PROJECT_ROOT / "results" / ".tmp-regen-test"
    if scratch.exists():
        shutil.rmtree(scratch)
    target_dir = scratch / "eline_off" / "210210-M1_210210"
    target_dir.mkdir(parents=True)
    try:
        shutil.copy(GPU_DIR / "ceridwen_result.h5", target_dir / "ceridwen_result.h5")
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "scripts/regenerate_fit_notebooks.py"), str(target_dir)],
            cwd=PROJECT_ROOT, check=True, capture_output=True, text=True, timeout=900.0,
        )
        # Printed numbers match exactly.
        gpu_lines = _stream_lines(GPU_DIR / "M1_210210_executed.ipynb")
        new_lines = _stream_lines(target_dir / "M1_210210_executed.ipynb")
        for key in ("photometry chi2/datum:", "spectrum chi2/bin:", "joint chi2/datum:",
                    "sampled calibration floor:", "posterior-weight ESS:", "likelihood calls:"):
            gpu = [line.strip() for line in gpu_lines if key in line]
            new = [line.strip() for line in new_lines if key in line]
            assert gpu and gpu == new, key
        # Every derived dataset matches: posterior-only ones exactly,
        # model predictions within the CPU/GPU platform spread.
        gpu_h5 = h5py.File(GPU_DIR / "ceridwen_derived_outputs.h5", "r")
        new_h5 = h5py.File(target_dir / "ceridwen_derived_outputs.h5", "r")
        names = []

        def collect(name, obj):
            if isinstance(obj, h5py.Dataset):
                names.append(name)

        gpu_h5.visititems(collect)
        assert names
        for name in names:
            va = np.asarray(gpu_h5[name])
            vb = np.asarray(new_h5[name])
            assert va.shape == vb.shape, name
            if va.dtype.kind not in "fc":
                continue
            va = np.asarray(va, dtype=float)
            vb = np.asarray(vb, dtype=float)
            predicted = name.startswith(("photometry/posterior", "spectrum/posterior", "calibration/")) \
                or name.endswith("/pull") or name.startswith("summary/q") \
                or name.endswith("/effective_uncertainty")
            if predicted:
                # 0.1% of the dataset peak: platform spread plus near-zero elements.
                peak = float(np.nanmax(np.abs(va))) if np.isfinite(va).any() else 0.0
                np.testing.assert_allclose(vb, va, rtol=1e-3, atol=1e-3 * peak,
                                           equal_nan=True, err_msg=name)
            else:
                np.testing.assert_allclose(vb, va, rtol=1e-12, atol=0.0,
                                           equal_nan=True, err_msg=name)
        attrs = {}

        def collect_attrs(name, obj):
            for key, value in obj.attrs.items():
                attrs[f"{name}@{key}"] = value

        gpu_h5.visititems(collect_attrs)
        for key, value in gpu_h5.attrs.items():
            attrs[f"@{key}"] = value
        new_attrs = {}

        def collect_new(name, obj):
            for key, value in obj.attrs.items():
                new_attrs[f"{name}@{key}"] = value

        new_h5.visititems(collect_new)
        for key, value in new_h5.attrs.items():
            new_attrs[f"@{key}"] = value
        assert sorted(new_attrs) == sorted(attrs)
        for key, value in attrs.items():
            other = new_attrs[key]
            if isinstance(value, (bytes, str)):
                assert str(other) == str(value), key
            else:
                value = np.asarray(value, dtype=float)
                other = np.asarray(other, dtype=float)
                predicted = key.split("@")[-1] in ("joint_chi2", "photometry_chi2", "spectrum_chi2")
                np.testing.assert_allclose(other, value, rtol=1e-3 if predicted else 1e-12,
                                           atol=0.0, err_msg=key)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
