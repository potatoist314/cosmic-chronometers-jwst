import numpy as np
from matplotlib.axes._secondary_axes import SecondaryAxis

from _phot import Z, figure


def test_photometry_figure_has_rest_frame_top_axis():
    fig, ax, _ = figure()
    tops = [c for a in fig.axes for c in [a, *a.child_axes] if isinstance(c, SecondaryAxis) and c._orientation == "x"]
    good = [t for t in tops if np.allclose(t.get_xlim(), np.array(ax.get_xlim()) / (1 + Z), rtol=1e-6)
            and t.xaxis.get_label_position() == "top" and "rest" in t.get_xlabel().lower()]
    assert good
    assert "observed" in fig.axes[-1].get_xlabel().lower() or any("observed" in a.get_xlabel().lower() for a in fig.axes)
