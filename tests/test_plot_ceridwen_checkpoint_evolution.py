from __future__ import annotations

import pickle

import numpy as np

from scripts import plot_ceridwen_checkpoint_evolution as animation


def test_load_checkpoint_metadata_accepts_legacy_snapshot(tmp_path):
    path = tmp_path / "legacy.pkl"
    legacy = {
        "positions": {"x": np.arange(4.0)[:, None]},
        "loglikelihood": np.arange(4.0),
        "loglikelihood_birth": np.arange(4.0) - 1,
        "logZ": 2.5,
        "n_dead": 4,
        "partial": True,
    }
    with path.open("wb") as handle:
        pickle.dump(legacy, handle)

    loaded = animation.load_checkpoint_metadata(path)

    assert loaded["schema_version"] == 1
    assert loaded["progress"] == {}
    assert loaded["n_dead"] == 4


def test_render_html_has_controls_metadata_and_static_fallback():
    shared = {
        "wavelength": np.array([4000.0, 4100.0, 4200.0]),
        "observed": np.array([1.0, 1.2, 0.9]),
        "uncertainty": np.array([0.1, 0.1, 0.2]),
        "target": "fixture",
        "source_run": "/tmp/run",
        "source_data": "/tmp/data.fits",
        "source_checkpoint": "/tmp/checkpoint.pkl",
        "source_rescue": "/tmp/rescue.pkl",
        "source_result": "/tmp/result.h5",
        "n_draws": 4,
    }
    frames = [
        {
            "label": "Checkpoint 1",
            "kind": "posterior model spectrum",
            "iteration": 10,
            "likelihood_calls": 100,
            "discarded": 8,
            "live": 2,
            "ess": 3.5,
            "logZ": 1.25,
            "delta_logZ": 0.2,
            "calibration_fraction": 0.03,
            "residual_uncertainty": np.array([0.1, 0.1, 0.2]),
            "model_q16": np.array([0.8, 1.0, 0.7]),
            "model_q50": np.array([0.9, 1.1, 0.8]),
            "model_q84": np.array([1.0, 1.2, 0.9]),
        }
    ]

    document = animation.render_html(
        shared, frames, title="Fixture", command="python generate.py"
    )

    assert '<button id="play"' in document
    assert '<input id="frame" type="range"' in document
    assert "Likelihood calls" in document
    assert "Weighted ESS" in document
    assert "Calibration floor" in document
    assert "Static final checkpoint" in document
    assert "<polyline" not in document
    assert "<polygon" not in document
    assert "Nested-sampling bands can widen or narrow" in document
    assert "axis rescales for each state" in document
    assert "https://" not in document
    assert "NaN" not in document
