import sys
from pathlib import Path

import numpy as np
import pytest
from astropy import units as u
from specutils.utils.wcs_utils import air_to_vac

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gama_spectra as gama  # noqa: E402


def test_lsf_matches_dogruel_table_3():
    # FWHM 4.8 A at 4800 A and 4.5 A at 7250 A: R = 1000 and 1611.
    fwhm = gama.lsf_sigma(np.array([4800.0, 7250.0])) / gama.FWHM_TO_SIGMA
    assert fwhm == pytest.approx([4.8, 4.5])
    assert np.array([4800.0, 7250.0]) / fwhm == pytest.approx([1000.0, 1611.11], rel=1e-5)
    assert gama.lsf_sigma(np.array([3700.0, 9000.0])) == pytest.approx(np.array([4.8, 4.5]) * gama.FWHM_TO_SIGMA)


def test_air_to_vacuum_shift_at_h_beta():
    # NIST ASD, H I 2s-4p observed: 4861.283363 A in air, 4862.64130267 A in vacuum.
    assert air_to_vac(4861.283363 * u.AA).to_value(u.AA) == pytest.approx(4862.64130267, abs=0.005)


def test_gkv_jansky_to_maggies_and_missing_bands():
    row = {f"flux_{band}t": "0.003631" for band in gama.GKV_FILTERS}
    row.update({f"flux_err_{band}t": "0.0003631" for band in gama.GKV_FILTERS})
    row.update(flux_FUVt="1e20", flux_err_FUVt="0", flux_ut="-999", flux_err_ut="-999")
    bands, filters, maggies, errors = gama.gkv_maggies(row)
    assert "FUV" not in bands and "u" not in bands
    assert filters[bands.index("K")] == "vista_vircam_Ks"
    assert maggies == pytest.approx([1e-6] * len(bands))
    assert errors == pytest.approx([1e-7] * len(bands))
