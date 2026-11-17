"""Differential-age cosmic-chronometer calculations."""

from __future__ import annotations

import numpy as np
from astropy import units as u


GYR_INV_TO_KM_S_MPC = (1 / u.Gyr).to_value(u.km / u.s / u.Mpc)


def hubble_from_age_difference(
    z_low: float,
    z_high: float,
    age_low_z_gyr: float,
    age_high_z_gyr: float,
) -> tuple[float, float]:
    """Return effective redshift and H(z) from two population ages.

    For a positive expansion rate, the lower-redshift population is older.
    """
    z_eff = 0.5 * (z_low + z_high)
    delta_z = z_high - z_low
    delta_age_gyr = age_high_z_gyr - age_low_z_gyr
    if delta_z <= 0:
        raise ValueError("z_high must exceed z_low")
    if delta_age_gyr == 0:
        raise ValueError("the age difference must be non-zero")
    hubble = -GYR_INV_TO_KM_S_MPC * delta_z / (
        (1.0 + z_eff) * delta_age_gyr
    )
    return z_eff, float(hubble)


def hubble_uncertainty_from_age_errors(
    hubble: float,
    age_difference_gyr: float,
    age_error_low_gyr: float,
    age_error_high_gyr: float,
) -> float:
    """Propagate independent age errors while treating redshift as exact."""
    if age_difference_gyr == 0:
        raise ValueError("the age difference must be non-zero")
    age_difference_error = np.hypot(age_error_low_gyr, age_error_high_gyr)
    return float(abs(hubble) * age_difference_error / abs(age_difference_gyr))


def inverse_variance_combine(
    values: np.ndarray,
    errors: np.ndarray,
) -> tuple[float, float]:
    """Combine independent Gaussian estimates with inverse-variance weights."""
    values = np.asarray(values, dtype=float)
    errors = np.asarray(errors, dtype=float)
    if values.shape != errors.shape or values.ndim != 1:
        raise ValueError("values and errors must be matching one-dimensional arrays")
    if np.any(~np.isfinite(values)) or np.any(~np.isfinite(errors)):
        raise ValueError("values and errors must be finite")
    if np.any(errors <= 0):
        raise ValueError("errors must be positive")
    weights = errors**-2
    return float(np.sum(weights * values) / np.sum(weights)), float(
        np.sqrt(1.0 / np.sum(weights))
    )


def fit_common_age_slope(
    redshift: np.ndarray,
    age_gyr: np.ndarray,
    groups: np.ndarray,
) -> tuple[float, float]:
    """Fit one age-redshift slope with a separate intercept per group.

    The returned uncertainty is the ordinary least-squares standard error.
    """
    redshift = np.asarray(redshift, dtype=float)
    age_gyr = np.asarray(age_gyr, dtype=float)
    groups = np.asarray(groups)
    if redshift.ndim != 1 or age_gyr.shape != redshift.shape:
        raise ValueError("redshift and age_gyr must be matching one-dimensional arrays")
    if groups.shape != redshift.shape:
        raise ValueError("groups must match redshift")
    if np.any(~np.isfinite(redshift)) or np.any(~np.isfinite(age_gyr)):
        raise ValueError("redshift and age_gyr must be finite")

    _, group_codes = np.unique(groups, return_inverse=True)
    intercepts = np.eye(group_codes.max() + 1)[group_codes]
    design = np.column_stack((redshift, intercepts))
    if len(redshift) <= design.shape[1]:
        raise ValueError("the fit needs more rows than fitted coefficients")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("the slope and group intercepts are not identifiable")

    coefficients, _, _, _ = np.linalg.lstsq(design, age_gyr, rcond=None)
    residual = age_gyr - design @ coefficients
    residual_variance = np.sum(residual**2) / (len(redshift) - design.shape[1])
    covariance = residual_variance * np.linalg.inv(design.T @ design)
    return float(coefficients[0]), float(np.sqrt(covariance[0, 0]))


def hubble_from_age_slope(
    z_eff: float,
    age_slope_gyr_per_redshift: float,
) -> float:
    """Return H(z) for a fitted differential-age slope dt/dz."""
    if not np.isfinite(z_eff) or z_eff <= -1:
        raise ValueError("z_eff must be finite and exceed -1")
    if not np.isfinite(age_slope_gyr_per_redshift):
        raise ValueError("the age slope must be finite")
    if age_slope_gyr_per_redshift == 0:
        raise ValueError("the age slope must be non-zero")
    return float(
        -GYR_INV_TO_KM_S_MPC
        / ((1.0 + z_eff) * age_slope_gyr_per_redshift)
    )


def effective_redshift(
    redshift: np.ndarray,
    reference=None,
    H0: tuple[float, ...] = (60.0, 67.5, 75.0),
    Om0: tuple[float, ...] = (0.25, 0.325, 0.40),
) -> dict[str, float]:
    """Return the redshift at which a straight-line age slope equals dt/dz.

    z_eff is the z where the reference dt/dz = -1 / ((1 + z) H(z)) equals the
    least-squares slope of reference ages at ``redshift``. Then
    ``hubble_from_age_slope(z_eff, slope)`` is H(z_eff). The spread is the range
    of z_eff over flat clones of the reference on the H0 x Om0 grid.
    """
    from astropy.cosmology import Planck18
    from scipy.optimize import brentq

    reference = Planck18 if reference is None else reference
    redshift = np.asarray(redshift, dtype=float)

    def solve(cosmo):
        slope = np.polyfit(redshift, cosmo.age(redshift).to_value(u.Gyr), 1)[0]
        dt_dz = lambda z: -(1 / ((1 + z) * cosmo.H(z))).to_value(u.Gyr)
        return brentq(lambda z: dt_dz(z) - slope, redshift.min(), redshift.max(), xtol=1e-10)

    spread = [solve(reference.clone(H0=h, Om0=m)) for h in H0 for m in Om0]
    return dict(z_eff=float(solve(reference)), z_eff_min=float(min(spread)), z_eff_max=float(max(spread)))


def fit_age_plane(
    redshift: np.ndarray,
    age_gyr: np.ndarray,
    covariate: np.ndarray,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Fit age = a + b * redshift + c * covariate by least squares.

    Return b (Gyr per unit redshift) and c (Gyr per unit covariate). The last
    axis holds the galaxies; leading axes hold independent fits. Weights
    multiply the squared residuals; a weight of zero removes a galaxy.
    """
    redshift, age_gyr, covariate, weights = np.broadcast_arrays(
        np.asarray(redshift, dtype=float),
        np.asarray(age_gyr, dtype=float),
        np.asarray(covariate, dtype=float),
        1.0 if weights is None else np.asarray(weights, dtype=float),
    )
    design = np.stack((np.ones_like(redshift), redshift, covariate), axis=-1)
    transposed = np.swapaxes(design * weights[..., None], -1, -2)
    coefficients = np.linalg.solve(transposed @ design, transposed @ age_gyr[..., None])
    return coefficients[..., 1, 0], coefficients[..., 2, 0]


def binned_difference_hubble(
    redshift: np.ndarray,
    age_gyr: np.ndarray,
    groups: np.ndarray,
    redshift_edges: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Return H(z) from median ages in redshift bins, one relation per group.

    Each redshift bin of a group gives one point: the median redshift, the
    median age and the error MAD / sqrt(N). Each group compares its i-th and
    (i + N_z / 2)-th points. The H(z) values are averaged with
    inverse-variance weights (Borghi et al. 2022b, ApJL 928, L4, Sect. 3;
    Jiao et al. 2023, arXiv:2205.05701, Sect. 5.1 and 5.2).
    """
    redshift = np.asarray(redshift, dtype=float)
    age_gyr = np.asarray(age_gyr, dtype=float)
    groups = np.asarray(groups)
    redshift_edges = np.asarray(redshift_edges, dtype=float)
    n_bins = len(redshift_edges) - 1
    step = n_bins // 2
    bin_index = np.clip(np.searchsorted(redshift_edges, redshift, side="right") - 1, 0, n_bins - 1)

    counts, pair_z, pair_hubble, pair_error = [], [], [], []
    for group in np.unique(groups):
        z_point, age_point, age_error = [], [], []
        for index in range(n_bins):
            cell = (groups == group) & (bin_index == index)
            counts.append(int(cell.sum()))
            median_age = np.median(age_gyr[cell])
            z_point.append(np.median(redshift[cell]))
            age_point.append(median_age)
            age_error.append(np.median(np.abs(age_gyr[cell] - median_age)) / np.sqrt(cell.sum()))
        for low in range(n_bins - step):
            high = low + step
            z_eff, hubble = hubble_from_age_difference(
                z_point[low], z_point[high], age_point[low], age_point[high]
            )
            pair_z.append(z_eff)
            pair_hubble.append(hubble)
            pair_error.append(
                hubble_uncertainty_from_age_errors(
                    hubble, age_point[high] - age_point[low], age_error[low], age_error[high]
                )
            )

    pair_z, pair_hubble, pair_error = (np.array(v) for v in (pair_z, pair_hubble, pair_error))
    hubble, error = inverse_variance_combine(pair_hubble, pair_error)
    weights = pair_error**-2
    return {
        "z_eff": float(np.sum(weights * pair_z) / np.sum(weights)),
        "hubble": hubble,
        "error": error,
        "pair_z_eff": pair_z,
        "pair_hubble": pair_hubble,
        "pair_error": pair_error,
        "counts": np.array(counts),
    }
