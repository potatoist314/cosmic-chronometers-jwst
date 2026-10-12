import pytest
import experiment

BASE = {"ssp_grid": "g", "sampler": {"num_live": 500, "num_inner_steps": 65, "num_delete": 100, "logZ_tol": -5.0}}


def test_arm_override_keeps_unspecified_sampler_controls():
    out = experiment.merge(BASE, {"sampler": {"num_live": 1000}})
    assert out["sampler"] == {"num_live": 1000, "num_inner_steps": 65, "num_delete": 100, "logZ_tol": -5.0}
    assert out["ssp_grid"] == "g" and BASE["sampler"]["num_live"] == 500


def test_unknown_keys_still_fail():
    with pytest.raises(ValueError):
        experiment.merge(BASE, {"sampler": {"nope": 1}})
