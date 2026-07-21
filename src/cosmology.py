import numpy as np
from astropy import units as u
from scipy.integrate import quad

def E(z, omega_m):
    ''' Dimensionless hubble parameter, E(z) = H(z) / H (0) '''
    ''' Radiation neglible, curvature negligible, only matter and dark energy'''
    return np.sqrt(omega_m * (1+z)**3 + (1 - omega_m))

@u.quantity_input #@ calls a decorator, quantity_input is the astropy function
def H(z, H0: u.Quantity[u.km/u.s/u.Mpc], omega_m):
    return E(z, omega_m) * H0


def age_integrand(z, omega_m):
    return 1/((1+z)*E(z, omega_m))


# Before calling scipy.integrate, we should convert back into si units

