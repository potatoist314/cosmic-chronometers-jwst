import numpy as np
import pytest
from build_dr2_quiescent_summary import formation_times

EDGES = np.array([0.0, 1.0, 2.0, 3.0])


@pytest.mark.parametrize("fracs, expected", [
    ([0.0, 0.0, 1.0], (2.2, 2.5, 2.8)),
    ([1.0, 0.0, 0.0], (0.2, 0.5, 0.8)),
    ([1 / 3, 1 / 3, 1 / 3], (0.6, 1.5, 2.4)),
])
def test_formation_lookback_percentiles(fracs, expected):
    t20, t50, t80 = formation_times(EDGES, np.array([fracs]))
    assert (t20[0], t50[0], t80[0]) == pytest.approx(expected)
