import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from build_dr2_quiescent_summary import formation_times

EDGES = np.array([0.0, 1.0, 2.0, 3.0])


def test_burst_confined_to_one_bin():
    t20, t50, t80 = formation_times(EDGES, np.array([[0.0, 0.0, 1.0]]))
    assert t20[0] == pytest.approx(2.2)
    assert t50[0] == pytest.approx(2.5)
    assert t80[0] == pytest.approx(2.8)


def test_uniform_sfh_spans_sixty_percent():
    t20, t50, t80 = formation_times(EDGES, np.array([[1 / 3, 1 / 3, 1 / 3]]))
    assert t20[0] == pytest.approx(0.6)
    assert t50[0] == pytest.approx(1.5)
    assert t80[0] == pytest.approx(2.4)


def test_ordering_and_batching():
    fracs = np.array([[1.0, 0.0, 0.0], [0.0, 0.5, 0.5]])
    t20, t50, t80 = formation_times(EDGES, fracs)
    assert np.all(t20 <= t50) and np.all(t50 <= t80)
    assert t20[0] < t20[1]  # younger burst first
