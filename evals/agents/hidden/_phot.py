import numpy as np
from spectral_figures import plot_photometry_fit

Z = 0.65


def figure():
    labels = ["u", "g", "r", "i", "z", "J"]
    wave = np.array([3600.0, 4800.0, 6200.0, 7700.0, 9000.0, 12500.0])
    flux = np.array([1.0, 3.0, 6.0, 9.0, 11.0, 14.0])
    fig, (ax, ax_pull) = plot_photometry_fit(labels, wave, flux, 0.05 * flux, 0.9 * flux, flux, 1.1 * flux,
                                             redshift=Z, data_label="COSMOS2025")
    fig.draw_without_rendering()
    return fig, ax, ax_pull
