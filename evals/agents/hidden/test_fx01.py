import matplotlib.pyplot as plt
import numpy as np
from spectral_figures import mark_rest_wavelength_axis


def test_top_axis_is_observed_over_one_plus_z():
    for z, title in ((0.65, None), (1.0, "M1_210210")):
        fig, ax = plt.subplots()
        ax.set_xlim(6000, 9000)
        top = mark_rest_wavelength_axis(ax, z, title=title)
        fig.draw_without_rendering()
        assert np.allclose(top.get_xlim(), [6000 / (1 + z), 9000 / (1 + z)], rtol=1e-6)
        plt.close(fig)
