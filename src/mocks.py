"""Mock age-redshift samples for the cosmic chronometer forecast.

The generator carries every systematic from brief step 4 as a parameter that
defaults to zero, so step 3's null case is the all-zeros call and step 4 varies
arguments rather than rewriting anything.
"""

from dataclasses import dataclass

import numpy as np
from astropy import units as u
from astropy.cosmology import FlatLambdaCDM


@dataclass
class MockSample:
    """One realisation. `age_obs` is what an observer would report."""

    z: np.ndarray
    age_true: np.ndarray      # Gyr, cosmology + intrinsic scatter, no measurement error
    age_obs: np.ndarray       # Gyr, after systematics and noise
    age_err: np.ndarray       # Gyr, the reported 1-sigma uncertainty
    truth: dict               # the input parameters, for recovery tests


def true_ages(z, H0, omega_m, z_form):
    """Time elapsed since z_form, in Gyr, for a flat LCDM cosmology.

    This is the quantity a cosmic chronometer measures: not the age of the
    universe at z, but the age of a stellar population that formed at z_form.
    """
    cosmo = FlatLambdaCDM(H0=H0 * u.km / u.s / u.Mpc, Om0=omega_m)
    return (cosmo.age(z) - cosmo.age(z_form)).to_value(u.Gyr)


def draw_redshifts(n, z_min, z_max, rng):
    """Uniform in z. Deliberately simple - swap in a survey selection later."""
    return np.sort(rng.uniform(z_min, z_max, n))


def make_mock(
    n,
    z_min=0.6,
    z_max=1.0,
    H0=70.0,
    omega_m=0.3,
    z_form=3.0,
    age_err=0.3,
    intrinsic_scatter=0.0,
    age_offset=0.0,
    bias_per_unit_z=0.0,
    seed=0,
):
    """Generate a mock age-redshift sample.

    Parameters
    ----------
    n : int
        Number of galaxies.
    z_min, z_max : float
        Redshift range to draw from.
    H0, omega_m, z_form : float
        The cosmology and formation redshift a recovery test should return.
    age_err : float
        Reported 1-sigma measurement uncertainty per galaxy, in Gyr. Noise is
        drawn from this, so it is honest by construction unless you also set
        one of the systematics below.
    intrinsic_scatter : float
        Real galaxy-to-galaxy spread in formation time, in Gyr. Physical, so it
        enters `age_true` - the population genuinely is not coeval.
    age_offset : float
        Constant additive bias in the measured age, in Gyr. Models an SPS or
        SFH systematic. Cosmic chronometers are differential, so this should
        leave a recovered H(z) untouched - which is worth testing.
    bias_per_unit_z : float
        Redshift-dependent bias, in Gyr per unit z, applied as
        `bias_per_unit_z * (z - z_min)`. Unlike a constant offset this tilts
        the age-redshift relation, so it does bias H(z).
    seed : int
        Recorded with the output; per AGENTS.md mock analyses use fixed seeds.

    Returns
    -------
    MockSample
    """
    rng = np.random.default_rng(seed)

    z = draw_redshifts(n, z_min, z_max, rng)
    age = true_ages(z, H0, omega_m, z_form)

    # intrinsic scatter is part of the population, not of the measurement
    if intrinsic_scatter:
        age = age + rng.normal(0.0, intrinsic_scatter, n)

    systematic = age_offset + bias_per_unit_z * (z - z_min)
    noise = rng.normal(0.0, age_err, n)
    age_obs = age + systematic + noise

    return MockSample(
        z=z,
        age_true=age,
        age_obs=age_obs,
        age_err=np.full(n, float(age_err)),
        truth=dict(n=n, z_min=z_min, z_max=z_max, H0=H0, omega_m=omega_m,
                   z_form=z_form, age_err=age_err,
                   intrinsic_scatter=intrinsic_scatter, age_offset=age_offset,
                   bias_per_unit_z=bias_per_unit_z, seed=seed),
    )
