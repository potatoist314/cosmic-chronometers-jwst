import numpy as np
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from _kl import run


def test_kl_values_are_points_not_bars(monkeypatch, tmp_path):
    saved = run(monkeypatch, tmp_path)
    assert saved
    fig = saved[0][0]
    axes = [ax for ax in fig.axes if ax.get_visible()]
    for ax in axes:
        assert not any(isinstance(c, BarContainer) for c in ax.containers)
        assert not any(isinstance(p, Rectangle) and p.get_width() * p.get_height() > 0 for p in ax.patches)
    marks = 0
    for ax in axes:
        for line in ax.lines:
            if isinstance(line, Line2D) and line.get_marker() not in (None, "None", "", " ") and len(line.get_xdata()) > 0:
                marks += len(line.get_xdata())
        for col in ax.collections:
            if isinstance(col, PathCollection):
                marks += len(col.get_offsets())
    assert marks >= 8  # 4 parameters x 2 fits
    assert any("KL" in ax.get_xlabel() or "KL" in ax.get_ylabel() for ax in axes)
