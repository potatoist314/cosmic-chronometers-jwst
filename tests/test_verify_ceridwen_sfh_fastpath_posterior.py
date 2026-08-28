from __future__ import annotations

import numpy as np
import pytest

from scripts import verify_ceridwen_sfh_fastpath_posterior as verification


def test_normalized_weights_are_finite_and_sum_to_one() -> None:
    weights = verification.normalized_weights(np.array([-1001.0, -1000.0]))

    assert np.isfinite(weights).all()
    assert weights.sum() == pytest.approx(1.0)
    assert weights[1] > weights[0]


def test_weighted_quantiles_follow_weighted_sample() -> None:
    values = np.array([0.0, 1.0, 2.0])
    weights = np.array([0.1, 0.8, 0.1])

    quantiles = verification.weighted_quantiles(values, weights)

    assert quantiles[1] == pytest.approx(0.5)
    assert quantiles[0] < quantiles[1] < quantiles[2]


def test_identical_components_pass() -> None:
    values = np.linspace(-2.0, 2.0, 101)
    weights = np.full(values.size, 1.0 / values.size)

    comparison = verification.compare_component(values, weights, values, weights)

    assert comparison["passed"] is True
    assert comparison["wasserstein_pooled_sd"] == pytest.approx(0.0)


def test_materially_shifted_components_fail() -> None:
    baseline = np.linspace(-2.0, 2.0, 101)
    fastpath = baseline + 1.0
    weights = np.full(baseline.size, 1.0 / baseline.size)

    comparison = verification.compare_component(
        baseline,
        weights,
        fastpath,
        weights,
    )

    assert comparison["passed"] is False
    assert comparison["mean_shift_pooled_sd"] > verification.MAX_MEAN_SHIFT_SD


def test_full_settings_match_the_requested_converged_contract() -> None:
    assert verification.SEED == 20260812
    assert verification.NUM_LIVE == 300
    assert verification.NUM_INNER_STEPS == 40
    assert verification.NUM_DELETE == 25
    assert verification.LOGZ_TOL == -3.0
    assert verification.MIN_WEIGHT_ESS == 200.0
