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
