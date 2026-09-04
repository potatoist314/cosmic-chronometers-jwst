---
title: Ceridwen: SSP grids to composite spectra
date: 2026-08-30
section: Codebase
tags: [ceridwen, ssp]
job: 
old: _old/codebase/ceridwen-ssp-csp.html
---

This layer converts precomputed single-age spectra into one composite galaxy spectrum. A grid stores numerical values. A basis is the algorithm that weights and combines these values.

### SSP containers

`SSPData` stores five numerical arrays:

- `ssp_lgmet` has shape `(n_met,)` and stores `log10` absolute metallicity.
- `ssp_lg_age_gyr` has shape `(n_age,)` and stores `log10(age/Gyr)`.
- `ssp_wave` has shape `(n_wave,)` and uses Angstrom.
- `ssp_flux` has shape `(n_met, n_age, n_wave)` and uses `L_sun/Hz/M_sun`.
- `ssp_resolution` has shape `(n_wave,)`. It stores the library Gaussian velocity width in km/s.

`ceridwen/ceridwen/ssps/ssp_data.py:227-326` defines the contract and shape check. Lines 508-566 load HDF5 files. FSPS grid generation starts at line 568.

`SSPDataAfe` adds a leading composition axis:

- `ssp_afe` has shape `(n_afe,)` and stores `[alpha/Fe]` in dex.
- `ssp_flux` has shape `(n_afe, n_met, n_age, n_wave)`.

`ssp_data_afe.py:83-176` defines this contract. The strict loader requires a four-dimensional schema-2.x grid. It rejects legacy files that do not record resolution provenance (`lines 341-408`).

1. **Alpha abundance**`n_afe`
2. **Metallicity**`n_met`
3. **Age**`n_age`
4. **Wavelength**`n_wave`

<figure>
<figcaption><code>SSPDataAfe.ssp_flux</code> follows this four-axis order.</figcaption>
</figure>

`ceridwen/ceridwen/ssps/ssp_data.py:297-307 · SSPData.__post_init__`

```
def __post_init__(self):
    """Validate grid consistency."""
    if self.ssp_flux.shape != (self.ssp_lgmet.size,
                               self.ssp_lg_age_gyr.size,
                               self.ssp_wave.size):
        raise ValueError(
            f"SSP flux grid shape mismatch: expected "
            f"({self.ssp_lgmet.size}, {self.ssp_lg_age_gyr.size}, "
            f"{self.ssp_wave.size}) but got {self.ssp_flux.shape}.  "
            f"Grid dimensions must be consistent (n_met, n_ages, n_wave)."
        )`
```

**Documented contract:** The class docstring defines the metallicity, age, wavelength, and flux-array shapes (`ceridwen/ceridwen/ssps/ssp_data.py:227-261`).

**Why it matters:** The tuple on the right defines the axis contract. The flux cube must align exactly with the metallicity, age, and wavelength coordinate arrays.

### Available grids

`grid_fetch.py:57-153` registers these grids:

- The MIST+MILES grid uses a Chabrier IMF and solar abundances.
- The BPASS grid contains binary SSPs and uses a Chabrier IMF.
- The low-resolution aMIST+C3K grid uses a Chabrier IMF and five alpha planes.
- The high-resolution aMIST+C3K grid uses a Kroupa IMF and five alpha planes.
- The aMIST+C3K null-control grid is currently unpublished.

`fetch_grid` caches each grid by name and checks its SHA-256 value. It downloads the grid to a temporary file. It then moves the file atomically (`grid_fetch.py:157-227`). The active notebooks request `amist_c3k_hr_krou_afe`. Its published schema-2.1 file has shape `(5, 13, 107, 10992)`.

### CSP construction

`CSPBasis` uses a three-dimensional `SSPData` object. `CSPBasis_afe` requires a four-dimensional `SSPDataAfe` object. The alpha basis checks the leading axis and rejects an incompatible grid at `csp/csp_afe.py:367-404`.

A CSP construction establishes static structure:

- The lookback-time nodes increase from today to the oldest time.
- Each node or bin has one SFH value.
- The metallicity is either constant `Z` or time-varying `zh`.
- The construction selects the dust, nebular, IGM, and smoothing components.

`CSPBasis.initialize_model_structure` checks this contract at `csp/csp.py:544-732`. Both `Z` and `zh` store `log10` absolute metallicity. They do not store `[Z/H]` or `log10(Z/Z_sun)` (`csp/csp.py:1817-1842`).

### From SFH parameters to weights

The notebooks sample consecutive SFR log-ratios. The transform uses this sequence:

1. **`logsfr_ratios`**Sampled ratios
2. **Cumulative log SFR**Anchor the first node
3. **Linear SFR**Apply `10 ** log_sfr`
4. **Unit-mass SFH**Store as `theta["sfh"]`

<figure>
<figcaption>The transform converts sampled ratios into normalized SFH weights.</figcaption>
</figure>

`logsfr_ratios_to_sfh` implements this sequence at `ceridwen/ceridwen/model/transforms.py:79-169`. The CSP weight kernel integrates the SFH over the SSP age cells. It also interpolates metallicity (`csp/csp.py:1817-2015`). Small wrappers select constant or time-varying metallicity. They also select linear or step SFH behavior (`lines 2017-2050`).

`ceridwen/ceridwen/model/transforms.py:142-167`

```
ratios  = jnp.asarray(logsfr_ratios, dtype=float)            # (n-1,)
# Anchor log10(SFR[0]) = 0, then cumulate the negative ratios
log_sfr = jnp.concatenate([jnp.zeros(1),
                            -jnp.cumsum(ratios)])             # (n,)
sfr     = 10.0 ** log_sfr                                     # (n,)

if sfh_times_yr is not None:
    times = jnp.asarray(sfh_times_yr, dtype=float)            # (n,)
    dt    = jnp.abs(jnp.diff(times))                          # (n-1,)
    # Standard trapezoidal quadrature weights (yr):
    #   w[0]   = 0.5 * dt[0]
    #   w[i]   = 0.5 * (dt[i-1] + dt[i])   for 0 < i < n-1
    #   w[n-1] = 0.5 * dt[n-2]
    w_lo  = jnp.concatenate([jnp.zeros(1), dt])               # (n,)
    w_hi  = jnp.concatenate([dt, jnp.zeros(1)])               # (n,)
    w     = 0.5 * (w_lo + w_hi)                               # (n,)
    # Unit-mass normalisation: ∫SFR dt = sum(sfr * w) = 1 Msun.
    # GOTCHA: normalise to total mass, NOT mean SFR — dividing by
    # sum(w) instead would leave an implicit factor of t_universe[yr]
    # (~1.4e10) in the spectrum and bias every logmass estimate by
    # ~10 dex at z=0 (less at higher z).
    total_mass = jnp.sum(sfr * w)
    sfh   = sfr / total_mass
else:
    # Discrete fallback: sum(sfh) = 1.
    sfh = sfr / jnp.sum(sfr)`
```

The first five lines reconstruct relative SFR values. The branch then normalizes a time integral or a discrete sum. Therefore, the later `logmass` parameter controls the total amplitude.

### Alpha interpolation

`CSPBasis_afe._afe_coords` finds the two adjacent alpha planes and the interpolation weight (`csp/csp_afe.py:841-864`). `_flux_at_afe` reads only these two planes and interpolates them linearly (`lines 866-896`). A one-plane grid removes this operation during compilation.

1. **Adjacent alpha planes**Lower and upper spectra
2. **Linear weight**`w` from sampled `afe`
3. **Interpolated grid**One spectrum cube

<figure>
<figcaption>Only two neighbouring alpha planes enter each interpolation.</figcaption>
</figure>

The production eight-node model precontracts the age axis once. The forward pass then interpolates alpha, metallicity, and SFH nodes without forming the full age cube. Matching models use this path automatically.

`ceridwen/ceridwen/csp/csp_afe.py:527-545 · CSPBasis_afe._configure_sfh_basis_fastpath`

```
if (self._n_afe, self._n_z, self._n_age) != (5, 13, 107):
    return self
elif self.n_time != 8 or self.sfh_per_bin:
    return self
elif not self.zh_const or self.sfh_interp != "step":
    return self
elif self.track_zred_age:
    return self
elif self._has_age_dependent_dust or self._has_dust_emission:
    return self

self._sfh_node_to_age = self._make_sfh_node_to_age_operator()
self._sfh_basis = jnp.einsum(
    "na,pzaw->pznw",
    self._sfh_node_to_age,
    self.flux,
)
self.sfh_basis_fastpath = True
return self`
```

**Documented contract:** The method docstring enables the fixed-grid basis when the model contract matches.

**Why it matters:** The production model uses the compact five-by-thirteen-by-eight basis. Other model structures retain the general calculation.

### Spectrum and prediction

The weight calculation produces coefficients over metallicity and age. These coefficients combine the SSP flux cube into a rest-frame spectrum. The enabled physics components modify this spectrum. `predict` then applies mass, distance, redshift, and IGM scaling. Finally, it projects the spectrum into observation space (`csp/csp.py:1139-1203`, `1303-1429`).

During model setup, the CSP sends the grid `ssp_resolution` curve to each `Spectrum`. The observation subtracts that library width in quadrature. It then applies the requested instrumental and LOSVD broadening.

`CSPBasis_afe` does not contain a nebular model. It returns a zero line component and rejects line observations (`csp/csp_afe.py:1114-1195`).
