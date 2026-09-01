import json
from pathlib import Path

import numpy as np
import pytest

from src.chronometer import (
    GYR_INV_TO_KM_S_MPC,
    hubble_from_age_difference,
    hubble_uncertainty_from_age_errors,
    inverse_variance_combine,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    PROJECT_ROOT
    / "results/rtx-5060-dr2-quiescent-full-spectrum"
    / "ceridwen_cosmic_chronometer.ipynb"
)


def test_gyr_inverse_conversion_matches_astronomy_value():
    assert GYR_INV_TO_KM_S_MPC == pytest.approx(977.79222168)


def test_borghi_lower_sigma_bins_one_and_three():
    z_eff, hubble = hubble_from_age_difference(
        z_low=0.666,
        z_high=0.780,
        age_low_z_gyr=3.0,
        age_high_z_gyr=2.486,
    )

    assert z_eff == pytest.approx(0.723)
    # The paper's unrounded medians give 126.3; its rounded deltas give 125.9.
    assert hubble == pytest.approx(126.3, abs=0.5)


def test_constant_age_offset_does_not_change_hubble():
    _, baseline = hubble_from_age_difference(0.65, 0.80, 4.0, 3.0)
    _, shifted = hubble_from_age_difference(0.65, 0.80, 6.5, 5.5)

    assert shifted == pytest.approx(baseline)


def test_flat_age_relation_is_undefined():
    with pytest.raises(ValueError, match="age difference"):
        hubble_from_age_difference(0.65, 0.80, 4.0, 4.0)


def test_increasing_age_with_redshift_gives_negative_hubble():
    _, hubble = hubble_from_age_difference(0.65, 0.80, 3.0, 4.0)

    assert hubble < 0


def test_age_error_propagation_and_inverse_variance_combination():
    sigma = hubble_uncertainty_from_age_errors(100.0, -1.0, 0.3, 0.4)
    combined, combined_error = inverse_variance_combine(
        np.array([90.0, 110.0]), np.array([10.0, 10.0])
    )

    assert sigma == pytest.approx(50.0)
    assert combined == pytest.approx(100.0)
    assert combined_error == pytest.approx(10.0 / np.sqrt(2.0))


def test_notebook_preserves_full_uncertainty_and_no_separate_pngs():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "N_BOOTSTRAP = 10_000" in source
    assert "size=len(galaxies)" in source
    assert "np.median(posterior_ages[sampled])" in source
    assert "np.mean(bootstrap_joint_h > 0)" in source
    assert "available_analysis_systematic_km_s_Mpc" in source
    assert 'cosmology_independent\"] = False' in source
    assert ".savefig(" not in source
    assert "plt.show()" in source
