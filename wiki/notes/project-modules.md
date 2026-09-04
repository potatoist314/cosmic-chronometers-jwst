---
title: Project support modules
date: 2026-08-25
section: Codebase
tags: [repository]
job: 
old: _old/codebase/project-modules.html
---

The active notebooks call Ceridwen for stellar-population inference. Project-owned scripts prepare the data. The `src/` modules remain from earlier project stages and are not current fit entry points.

### Current flow

1. **`scripts/`**Prepare observations
2. **`notebooks/`**Configure fits
3. **`ceridwen/`**Predict and sample
4. **`results/`**Store checkpoints and HDF5

`src/` retains support code from earlier project stages.

<figure>
<figcaption>Project scripts and notebooks drive the active Ceridwen fit.</figcaption>
</figure>

### Retained `src/cosmology.py`

This early module contains small cosmology functions. No active notebook currently imports it.

- `E(z, omega_m)` calculates the flat matter-plus-dark-energy expansion factor (`src/cosmology.py:5-8`).
- `H(z, H0, omega_m)` multiplies this factor by an Astropy quantity with units (`src/cosmology.py:10-12`).
- `age_integrand(z, omega_m)` returns the dimensionless integrand for SciPy quadrature (`src/cosmology.py:15-16`).

The module ends at line 20. It imports `quad` but does not implement the full age integral. This module is a partial learning module, not a complete cosmology API.

`src/cosmology.py:5-16 · E, H, age_integrand`

```
def E(z, omega_m):
    ''' Dimensionless hubble parameter, E(z) = H(z) / H (0) '''
    ''' Radiation neglible, curvature negligible, only matter and dark energy'''
    return np.sqrt(omega_m * (1+z)**3 + (1 - omega_m))

@u.quantity_input #@ calls a decorator, quantity_input is the astropy function
def H(z, H0: u.Quantity[u.km/u.s/u.Mpc], omega_m):
    return E(z, omega_m) * H0

def age_integrand(z, omega_m):
    return 1/((1+z)*E(z, omega_m))`
```

**Documented contract:** The inline documentation defines `E` as `H(z) / H(0)`. The decorator requires Astropy units for `H0` (`src/cosmology.py:5-12`).

**Why it matters:** `H` calls `E` for the dimensionless calculation. `age_integrand` also calls `E`. These calls show the module dependency direction.

### Retained `src/mocks.py`

This inactive module generates controlled age-redshift samples for earlier cosmic-chronometer work.

1. **Draw redshifts**
2. **Calculate true ages**
3. **Add intrinsic scatter**
4. **Add bias and noise**
5. **Build MockSample**

<figure>
<figcaption>Retained workflow from the inactive cosmic-chronometer mock module.</figcaption>
</figure>

- `MockSample` defines four arrays and one truth dictionary (`lines 15-23`).
- `true_ages` subtracts formation time from observation time (`lines 26-33`).
- `draw_redshifts` uses the supplied random generator (`lines 36-38`).
- `make_mock` controls the scatter, offset, redshift bias, noise, and seed (`lines 41-108`).

All four sample arrays have shape `(n,)`. Ages and age uncertainties use Gyr. The redshift `z` is dimensionless.

`src/mocks.py:86-97 · make_mock`

```
rng = np.random.default_rng(seed)

z = draw_redshifts(n, z_min, z_max, rng)
age = true_ages(z, H0, omega_m, z_form)

# intrinsic scatter is part of the population, not of the measurement
if intrinsic_scatter:
    age = age + rng.normal(0.0, intrinsic_scatter, n)

systematic = age_offset + bias_per_unit_z * (z - z_min)
noise = rng.normal(0.0, age_err, n)
age_obs = age + systematic + noise`
```

**Documented contract:** The docstring defines every mock input and returns a `MockSample` (`src/mocks.py:54-84`).

**Why it matters:** The cosmology creates `age`. Physical scatter modifies this value. The systematic term and measurement noise then create the reported `age_obs`.

Other inactive method modules remain in `src/` for reproducibility. This page does not include them in the current workflow.

### Active data scripts

`build_borghi2022_legac_dr2_subset.py` is the main data transformation script. Its `main` function reads both catalogues and checks the required columns. It matches object IDs and checks coordinate separations. It retains repeat spectra and applies the strict 215 km/s split. Finally, it writes the joined and audit tables (`lines 176-358`).

`download_legac_dr2_spectra.py` can continue an incomplete download. It checks the catalogue filenames (`lines 47-61`) and each FITS structure (`lines 64-79`). It downloads each file with a `.part` suffix and then renames the complete file atomically (`lines 82-110`). Finally, it checks the complete file set (`lines 113-146`).

`download_cosmos2015_legac_dr2_photometry.py` queries VizieR in batches. It keeps the nearest match for each LEGA-C row. It adds object identifiers and match separations. Finally, it writes a FITS table (`lines 61-125`).
