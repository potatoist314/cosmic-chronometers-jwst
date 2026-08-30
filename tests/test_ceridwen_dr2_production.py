import json
import os
from pathlib import Path

import pytest

from scripts import run_ceridwen_vast_multi_gpu as runner


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"


@pytest.fixture(scope="module")
def target_manifest():
    return runner.build_target_manifest(num_shards=2, base_seed=20260830)


def test_manifest_selects_187_unique_objects(target_manifest):
    targets = target_manifest["targets"]

    assert target_manifest["eligible_spectra"] == 194
    assert target_manifest["unique_objects"] == 187
    assert len({target["object_id"] for target in targets}) == 187
    assert [target["sn"] for target in targets] == sorted(
        (target["sn"] for target in targets), reverse=True
    )


def test_manifest_has_stable_seeds_and_balanced_shards(target_manifest):
    targets = target_manifest["targets"]

    assert [target["manifest_index"] for target in targets] == list(range(187))
    assert [target["seed"] for target in targets] == list(
        range(20260830, 20260830 + 187)
    )
    assert [target["shard_index"] for target in targets] == [
        index % 2 for index in range(187)
    ]
    assert sum(target["shard_index"] == 0 for target in targets) == 94
    assert sum(target["shard_index"] == 1 for target in targets) == 93


def test_reference_target_keeps_manifest_seed(target_manifest):
    target = next(
        target for target in target_manifest["targets"] if target["spect_id"] == "M1_210210"
    )

    assert target == {
        "manifest_index": 2,
        "object_id": 210210,
        "spect_id": "M1_210210",
        "sn": pytest.approx(62.2),
        "shard_index": 0,
        "seed": 20260832,
    }


def test_control_process_keeps_validation_off_gpu(monkeypatch, tmp_path):
    monkeypatch.delenv("JAX_PLATFORMS", raising=False)
    args = runner._parser().parse_args(
        ["--write-targets-file", str(tmp_path / "targets.json")]
    )

    assert runner._run(args) == 0
    assert os.environ["JAX_PLATFORMS"] == "cpu"


def test_notebook_uses_production_model_and_sampler_contract():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "drop_duplicates(\"OBJECT\", keep=\"first\")" in source
    assert "assert len(selected_passive) == 187" in source
    assert "assert phot_fit_mask.sum() == 12" in source
    assert "ClippedNormal(\n        mean=1.0, sigma=0.3, low=0.2, high=3.0" in source
    assert '"num_live": 500' in source
    assert '"num_inner_steps": 65' in source
    assert '"num_delete": 100' in source
    assert '"logZ_tol": -5.0' in source
    assert "assert sum(np.size(value) for value in joint_model.theta_init.values())" in source
    assert '"Z": "log10 absolute metallicity"' in source
    assert r"$\log_{10}(Z/Z_\odot)$" not in source
    assert "aperture_transfer" not in source


def test_notebook_embeds_figures_and_writes_analysis_ready_hdf5():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert ".savefig(" not in source
    assert 'RESULT_DIR / "' not in source or ".png" not in source
    for group in ("summary", "sfh", "photometry", "spectrum", "diagnostics"):
        assert f'create_group("{group}")' in source
    assert "plt.show()" in source
    assert "np.where(spectrum_mask, spectrum_flux, np.nan)" in source
