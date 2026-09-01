import json
from pathlib import Path

import h5py
import numpy as np
import pytest

from src.chronometer import (
    GYR_INV_TO_KM_S_MPC,
    fit_common_age_slope,
    hubble_from_age_difference,
    hubble_from_age_slope,
    hubble_uncertainty_from_age_errors,
    inverse_variance_combine,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    PROJECT_ROOT
    / "results/rtx-5060-dr2-quiescent-full-spectrum"
    / "ceridwen_cosmic_chronometer.ipynb"
)
SUMMARY_PATH = NOTEBOOK_PATH.with_name("ceridwen_cosmic_chronometer_summary.h5")


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


def test_common_age_slope_ignores_group_intercept_offsets():
    redshift = np.array([0.60, 0.70, 0.80, 0.90] * 2)
    groups = np.array(["low"] * 4 + ["high"] * 4)
    age = -4.0 * redshift + np.where(groups == "low", 6.0, 9.0)

    slope, slope_error = fit_common_age_slope(redshift, age, groups)

    assert slope == pytest.approx(-4.0)
    assert slope_error == pytest.approx(0.0, abs=1e-12)


def test_common_age_slope_handles_negative_zero_and_mixed_intercepts():
    redshift = np.array([0.60, 0.75, 0.90] * 3)
    groups = np.repeat(["negative", "zero", "positive"], 3)
    intercept = {"negative": -2.0, "zero": 0.0, "positive": 4.0}
    age = np.array([-2.5 * z + intercept[group] for z, group in zip(redshift, groups)])

    slope, _ = fit_common_age_slope(redshift, age, groups)

    assert slope == pytest.approx(-2.5)


def test_hubble_from_age_slope_units_and_sign():
    hubble = hubble_from_age_slope(0.75, -5.0)

    assert hubble == pytest.approx(GYR_INV_TO_KM_S_MPC / (1.75 * 5.0))
    assert hubble > 0


def test_zero_age_slope_is_undefined():
    with pytest.raises(ValueError, match="age slope"):
        hubble_from_age_slope(0.75, 0.0)


def test_notebook_preserves_full_uncertainty_and_no_separate_pngs():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "N_BOOTSTRAP = 10_000" in source
    assert "size=len(galaxies)" in source
    assert "np.median(posterior_ages[sampled])" in source
    assert "np.mean(bootstrap_joint_h > 0)" in source
    assert "analysis_choice_spread_km_s_Mpc" in source
    assert 'combine_as_total_uncertainty\"] = False' in source
    assert "fit_common_age_slope" in source
    assert "formation_time_planck18_gyr" in source
    assert "leave_one_out" in source
    assert 'cosmology_independent\"] = False' in source
    assert ".savefig(" not in source
    assert "plt.show()" in source


def test_executed_audit_summary_has_expected_cohorts_and_finite_draws():
    with h5py.File(SUMMARY_PATH, "r") as summary:
        assert summary.attrs["schema_version"] == 2
        assert summary.attrs["random_seed"] == 20260901
        cohort_group = summary["cohorts/summary"]
        cohort_names = [value.decode() for value in cohort_group["cohort"][:]]
        cohort_counts = dict(zip(cohort_names, cohort_group["n"][:]))
        assert cohort_counts == {
            "Borghi full": 140,
            "Borghi overlap": 68,
            "Ceridwen overlap": 68,
            "Ceridwen full": 164,
        }
        borghi_index = cohort_names.index("Borghi full")
        assert cohort_group["H_km_s_Mpc"][borghi_index] == pytest.approx(98.0, abs=1.0)
        assert cohort_group["sigma_H_km_s_Mpc"][borghi_index] == pytest.approx(31.4, abs=0.5)
        for cohort_name in [
            "borghi_full",
            "borghi_overlap",
            "ceridwen_overlap",
            "ceridwen_full",
        ]:
            assert np.all(np.isfinite(summary[f"regression/{cohort_name}/H_km_s_Mpc"][:]))
        assert len(summary["influence/top_five/object_id"]) == 5
        assert len(summary["diagnostics/by_bin/z_bin"]) == 8
