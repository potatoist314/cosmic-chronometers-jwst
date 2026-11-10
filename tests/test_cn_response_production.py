"""Exercise the C/N option through the production notebook on M1_210210."""

import json
from pathlib import Path
import warnings

from astropy.units import UnitsWarning
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESPONSE = "data/raw/alf/cda32111c721efe586945d7dfcb9f605a9f6a105"


def build_model(monkeypatch, directory, enabled):
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("CERIDWEN_RESULT_DIR", str(directory))
    monkeypatch.setenv("CERIDWEN_TARGET_ID", "M1_210210")
    monkeypatch.setenv("CERIDWEN_PLOTS", "0")
    notebook = json.loads((ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb").read_text())
    namespace = {}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UnitsWarning)
        for index, cell in enumerate(notebook["cells"][:9]):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            if "SETTINGS = {" in source:
                source += f'\nSETTINGS["abundance_response"] = {RESPONSE if enabled else None!r}\n'
            exec(compile(source, f"production-cell-{index}", "exec"), namespace)
    return namespace


def test_real_spectrum_and_photometry_zero_response_are_bitwise(monkeypatch, tmp_path):
    plain = build_model(monkeypatch, tmp_path / "plain", False)
    enabled = build_model(monkeypatch, tmp_path / "enabled", True)
    assert enabled["joint_csp"].sfh_basis_fastpath
    assert min(enabled["cn_response"].minimum_total_sigma.values()) > 100.
    a, b = plain["joint_model"], enabled["joint_model"]
    for afe, feh, scale in [(-.1, -.8, -1.), (.1, -.3, 0.), (.3, .1, 1.)]:
        x, y = dict(a.theta_init), dict(b.theta_init)
        for theta in (x, y):
            theta.update(afe=np.array([afe]), logzsol=np.array([feh]),
                         logsfr_ratios=scale * np.linspace(-.2, .2, plain["N_RATIOS"]))
        for predict in (lambda m, t: m.predict(t), lambda m, t: m.predict_jit(t)):
            expected, actual = predict(a, x), predict(b, y)
            for key in ("photometry", "spectrum"):
                np.testing.assert_array_equal(actual[key], expected[key])
    y.update(cfe=np.array([.2]), nfe=np.array([.3]))
    modified = b.predict(y)
    for key in ("photometry", "spectrum"):
        assert np.isfinite(modified[key]).all()
        assert np.min(modified[key]) > 0.
        assert not np.array_equal(modified[key], actual[key])
