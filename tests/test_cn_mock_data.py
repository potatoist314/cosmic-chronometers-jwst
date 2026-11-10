"""Check the injection units, recorded noise, and real notebook input path."""

import numpy as np

from scripts.generate_cn_mocks import notebook_model, observations, RESPONSE


def test_real_model_injection_round_trips_in_spectrum_and_photometry(monkeypatch, tmp_path):
    monkeypatch.setenv("CERIDWEN_TARGET_ID", "M1_210210")
    monkeypatch.setenv("CERIDWEN_RESULT_DIR", str(tmp_path))
    monkeypatch.setenv("CERIDWEN_PLOTS", "0")
    enabled = notebook_model({"abundance_response": RESPONSE}, tmp_path / "truth")
    truth = dict(enabled["joint_model"].theta_init)
    a = observations(enabled, truth, .15, .3, 20261111)
    b = observations(enabled, truth, .3, .6, 20261111)
    repeated = observations(enabled, truth, .15, .3, 20261111)
    for key in a:
        np.testing.assert_array_equal(a[key], repeated[key])
    assert a["spectrum_unit"] == "erg s-1 cm-2 Hz-1"
    assert a["photometry_unit"] == "maggies"
    for prefix in ("photometry", "spectrum"):
        mean_key = "mean_" + prefix
        expected = np.hypot(a[prefix + "_uncertainty"],
                            (.05 if prefix == "photometry" else np.exp(truth["log_f_calib"][0]))
                            * np.abs(a[mean_key]))
        np.testing.assert_allclose(a[prefix + "_noise_sigma"], expected)
        use = slice(None) if prefix == "photometry" else a["native_valid"]
        np.testing.assert_allclose(
            ((a[prefix + "_flux"] - a[mean_key]) / a[prefix + "_noise_sigma"])[use],
            ((b[prefix + "_flux"] - b[mean_key]) / b[prefix + "_noise_sigma"])[use],
            rtol=2e-12, atol=2e-12)
    path = tmp_path / "injection.npz"
    np.savez_compressed(path, **a)
    loaded = notebook_model({"mock_data": str(path)}, tmp_path / "recovery")
    np.testing.assert_array_equal(loaded["phot_flux"], a["photometry_flux"])
    np.testing.assert_array_equal(loaded["phot_error_stat"], a["photometry_uncertainty"])
    np.testing.assert_array_equal(loaded["spectrum_flux"], a["spectrum_flux"])
    np.testing.assert_array_equal(loaded["native_uncertainty"], a["spectrum_uncertainty"])
    np.testing.assert_array_equal(loaded["spectrum_wave"], a["spectrum_wave"])
    np.testing.assert_array_equal(loaded["FILTER_NAMES"], a["filter_names"])
    np.testing.assert_array_equal(loaded["spectrum_mask"], enabled["spectrum_mask"])
    assert loaded["cn_response"] is None


def test_mock_file_is_a_selected_modal_input():
    from scripts.vast import selected_inputs

    cell = {"target": "M1_210210", "target_metadata": {"filename": "legac_M1_210210_v2.0.fits"},
            "settings": {"photometry": "cosmos2025_uv", "mock_data": "data/processed/cn-mocks/test.npz"}}
    assert cell["settings"]["mock_data"] in selected_inputs([cell])
