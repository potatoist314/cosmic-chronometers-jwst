import numpy as np
import pytest
from cosmos_photometry import from_magnitude


def test_ab_magnitude_gives_microjansky():
    row = {"f": 99.0, "m": 23.9, "fe": 9.0, "me": 0.1}
    flux, err = from_magnitude(row, "f", "m", "fe", "me")
    assert flux == pytest.approx(1.0, rel=1e-9)
    assert err == pytest.approx(0.1 * np.log(10) / 2.5, rel=1e-9)
    row["m"] = 21.4
    assert from_magnitude(row, "f", "m", "fe", "me")[0] == pytest.approx(10.0, rel=1e-9)


def test_nondetection_falls_back_to_flux_columns():
    assert from_magnitude({"f": 2.5, "m": 99.0, "fe": 0.5, "me": 9.0}, "f", "m", "fe", "me") == (2.5, 0.5)
