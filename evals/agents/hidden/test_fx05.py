import pytest
from src.chronometer import GYR_INV_TO_KM_S_MPC, hubble_from_age_difference, hubble_from_age_slope


def test_slope_and_difference_agree():
    z_eff, h = hubble_from_age_difference(0.4, 0.6, 9.0, 8.0)
    assert hubble_from_age_slope(z_eff, (8.0 - 9.0) / (0.6 - 0.4)) == pytest.approx(h, rel=1e-12)


def test_h_is_minus_one_over_one_plus_z_dz_dt():
    assert hubble_from_age_slope(1.0, -2.0) == pytest.approx(GYR_INV_TO_KM_S_MPC / 4.0, rel=1e-12)
