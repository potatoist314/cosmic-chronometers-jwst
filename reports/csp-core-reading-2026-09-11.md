# Ceridwen forward model: the code that runs in a DR2 fit

This file shows only the code that runs in a DR2 fit, with the unused slow path retained in section 8 for reference. A composite stellar population (CSP) combines simple stellar populations (SSPs) through a star-formation history (SFH). The fit interpolates their spectra, applies diffuse dust, scales the flux, and projects it onto each observation.

predicted data = observation projection(10^logmass × distance/redshift factor × exp(-diffuse optical depth) × sum over SFH nodes(node star-formation rate × node basis spectrum))

SedModel.predict -> CSPBasis_afe.predict -> _assemble_observer_spectra -> get_spectrum_components -> get_spectrum (= get_spectrum_dattn_nodem_noneb) -> _spectrum_from_sfh_basis -> diffuse attenuation -> _apply_mass_redshift_igm -> _project_observations -> obs.predict

## 1. Entry point

### `predict` — `ceridwen/ceridwen/csp/csp_afe.py:1210`

- `SedModel.predict` first applies parameter transforms and inserts the fixed redshift. Its `theta` includes `sfh` from `logsfr_ratios_to_sfh`, but excludes `lookback_time`.
- This CSP method builds one spectrum, applies mass and distance factors, and returns predictions keyed by observation name.

```python
def predict(self, theta: dict, observations: list) -> dict:
    spectrum_phot, spectrum_slit, line_slit = \
        self._assemble_observer_spectra(theta)
    spectrum_phot, spectrum_slit, line_slit = self._apply_mass_redshift_igm(
        spectrum_phot, spectrum_slit, line_slit, theta
    )
    return self._project_observations(
        spectrum_phot, spectrum_slit, line_slit, observations, theta
    )
```

## 2. Build the rest-frame spectrum

### `get_spectrum_components` — `ceridwen/ceridwen/csp/csp_afe.py:1184`

- Returns the dust-attenuated stellar spectrum and a zero emission-line component, each with shape `(n_wave,)`. Here `n_wave` counts model wavelengths.
- This class has no nebular emission, meaning emission from gas. The stellar spectrum retains its absorption features.

```python
def get_spectrum_components(self, theta: dict) -> tuple:
    self._warn_unknown_theta_keys(theta)
    continuum = self.get_spectrum(theta=theta, include_lines=False)
    return continuum, jnp.zeros_like(continuum)
```

### `_assemble_observer_spectra` — `ceridwen/ceridwen/csp/csp_afe.py:1278`

- Supplies the same stellar spectrum to photometry and slit spectroscopy. The third array contains only zeros.
- Any optional relative scaling of the spectroscopic prediction occurs later, in `_project_observations`.

```python
def _assemble_observer_spectra(self, theta):
    spectrum_cont, line_component = self.get_spectrum_components(theta)
    return (spectrum_cont, spectrum_cont, line_component)
```

### `get_spectrum_dattn_nodem_noneb` — `ceridwen/ceridwen/csp/csp_afe.py:1926`

- Setup assigns this function to `get_spectrum` because DR2 uses dust attenuation without dust emission. The zero CSP velocity dispersion disables its smoothing wrapper.
- DR2 satisfies the fast-path conditions and supplies no runtime `lookback_time`. It combines the cached basis spectra, then multiplies by diffuse transmission, `exp(-attn_diffuse)`.
- Returns shape `(n_wave,)`. The remaining branch uses explicit SSP weights only when the fast-path conditions fail.

```python
def get_spectrum_dattn_nodem_noneb(self, theta, *, include_lines=None):
    _ = include_lines
    attn, attn_diffuse = self.attenuate_dust(self.wave, theta)

    if (
        self.sfh_basis_fastpath
        and "lookback_time" not in theta
    ):
        spectrum = self._spectrum_from_sfh_basis(theta)
        spectrum *= jnp.exp(-attn_diffuse.astype(jnp.float32))
        return spectrum.reshape((-1,))

    flux = self._flux_at_afe(theta)               # (n_z, n_age, n_wave)

    M       = self._age_bin_mix
    tau_age = jnp.einsum("ab,bw->aw", M, attn.astype(jnp.float32))
    attn_age= jnp.exp(-tau_age)

    if "frac_obrun" in theta:
        fo = jnp.ravel(theta["frac_obrun"])[0].astype(jnp.float32)
        attn_age = (jnp.float32(1.0) - fo) * attn_age + fo

    weights  = self.calculate_ssp_weights(theta).astype(jnp.float32)
    spectrum = jnp.einsum("za,zaw,aw->w", weights, flux, attn_age)
    spectrum *= jnp.exp(-attn_diffuse.astype(jnp.float32))

    return spectrum.reshape((-1,))
```

## 3. Fast path, built once at setup

### `_configure_sfh_basis_fastpath` — `ceridwen/ceridwen/csp/csp_afe.py:525`

- Enables a cached basis for eight SFH nodes, constant metallicity, step interpolation, fixed ages, and no age-dependent dust or dust emission.
- The SSP array has shape `(5, 13, 107, n_wave)`: alpha enhancement, metallicity, age, and wavelength. Alpha enhancement is the abundance coordinate `[alpha/Fe]`.
- Combines the 107 ages into eight node basis spectra, producing `(5, 13, 8, n_wave)`. Each fit evaluation then uses this smaller array.

```python
def _configure_sfh_basis_fastpath(self):
    self.sfh_basis_fastpath = False
    self._sfh_basis = None
    self._sfh_node_to_age = None
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
    return self
```

### `_make_sfh_node_to_age_operator` — `ceridwen/ceridwen/csp/csp_afe.py:550`

- The eight lookback nodes are 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr, and the universe age at the galaxy redshift. Internally, times use years.
- The seven intervals overlap 107 SSP age cells, whose internal boundaries lie halfway between adjacent ages in years. `overlap` has shape `(7, 107)`.
- Normalizes each interval's age contributions to its duration and assigns half to each endpoint. The `(8, 107)` operator encodes the step model's adjacent-node average.

```python
def _make_sfh_node_to_age_operator(self):
    t_young = self.sfh_times[:-1]
    t_old = self.sfh_times[1:]
    dt = t_old - t_young
    overlap = jnp.maximum(
        0.0,
        jnp.minimum(t_old[:, None], self._ssp_voronoi_hi[None, :])
        - jnp.maximum(t_young[:, None], self._ssp_voronoi_lo[None, :]),
    )
    bin_to_age = (
        overlap * (dt / overlap.sum(axis=1))[:, None]
    ).astype(jnp.float32)
    operator = jnp.zeros((8, 107), dtype=jnp.float32)
    operator = operator.at[:-1].add(0.5 * bin_to_age)
    return operator.at[1:].add(0.5 * bin_to_age)
```

## 4. Fast path, run on every likelihood call

### `_afe_coords` — `ceridwen/ceridwen/csp/csp_afe.py:890`

- Finds the two grid values surrounding `theta["afe"]`. Returns the upper index and the linear interpolation weight.
- Clips the weight to `[0, 1]`, so values outside the grid select an edge spectrum.

```python
def _afe_coords(self, theta):
    target_afe = jnp.ravel(theta["afe"])[0]
    k = jnp.clip(
        jnp.searchsorted(
            self.afe_grid, target_afe, side='left', method='compare_all'
        ),
        1, self._n_afe - 1,
    )
    a0 = self.afe_grid[k - 1]
    a1 = self.afe_grid[k]
    w  = jnp.clip((target_afe - a0) / (a1 - a0), 0.0, 1.0)
    return k, w
```

### `_sfh_basis_coords` — `ceridwen/ceridwen/csp/csp_afe.py:952`

- Finds scalar indices and weights for interpolation across alpha enhancement and metallicity. One metallicity applies to all stellar ages.
- `theta["Z"]` means log10 of absolute metallicity, in `ssp_lgmet` units. It does not mean log10 metallicity relative to solar.
- Missing `afe` selects the solar-alpha plane. Metallicity values outside the grid select the nearest edge.

```python
def _sfh_basis_coords(self, theta):
    if "afe" in theta:
        afe_hi, afe_weight = self._afe_coords(theta)
    else:
        afe_hi = jnp.asarray(self._afe_solar_idx, dtype=jnp.int32)
        afe_weight = jnp.asarray(0.0, dtype=jnp.float32)

    target_z = jnp.ravel(theta["Z"])[0]
    z_hi = jnp.clip(
        jnp.searchsorted(
            self.zmet, target_z, side="left", method="compare_all"
        ),
        1,
        self._n_z - 1,
    )
    z0 = self.zmet[z_hi - 1]
    z1 = self.zmet[z_hi]
    z_weight = jnp.clip((target_z - z0) / (z1 - z0), 0.0, 1.0)
    return afe_hi, afe_weight, z_hi, z_weight
```

### `_spectrum_from_sfh_basis` — `ceridwen/ceridwen/csp/csp_afe.py:973`

- Interpolates four neighboring basis slices in metallicity and alpha enhancement. Each slice and the resulting `node_basis` have shape `(8, n_wave)`.
- Weights the eight basis spectra by `theta["sfh"]`, shape `(8,)`, and sums them into `(n_wave,)`. These are linear star-formation rates, with a positive floor.
- The cached basis already includes age integration. This step therefore avoids summing 107 SSP ages on each call.

```python
def _spectrum_from_sfh_basis(self, theta):
    sfh = jnp.clip(theta["sfh"], 1e-30, None).astype(jnp.float32)
    afe_hi, afe_weight, z_hi, z_weight = self._sfh_basis_coords(theta)
    afe_weight = afe_weight.astype(jnp.float32)
    z_weight = z_weight.astype(jnp.float32)

    if "afe" not in theta:
        afe_lo = afe_hi
    else:
        afe_lo = afe_hi - 1

    basis00 = self._sfh_basis[afe_lo, z_hi - 1]
    basis01 = self._sfh_basis[afe_lo, z_hi]
    basis10 = self._sfh_basis[afe_hi, z_hi - 1]
    basis11 = self._sfh_basis[afe_hi, z_hi]
    lower = (1.0 - z_weight) * basis00 + z_weight * basis01
    upper = (1.0 - z_weight) * basis10 + z_weight * basis11
    node_basis = (1.0 - afe_weight) * lower + afe_weight * upper
    return jnp.einsum("n,nw->w", sfh, node_basis)
```

## 5. Dust

### `attenuate_diffuse_only` — `ceridwen/ceridwen/csp/csp_afe.py:876`

- Selects one diffuse attenuation curve for all stellar ages. The age-dependent optical-depth array is zero, with shape `(1, n_wave)`.
- Both outputs represent optical depth. The spectrum calculation converts diffuse optical depth into transmission after combining the stellar populations.

```python
elif add_diffuse_dust and not add_dust:
    self.bin_low  = jnp.array([-jnp.inf])
    self.bin_high = jnp.array([jnp.inf])
    def attenuate_diffuse_only(wave, theta):
        attn_diffuse = self.diff_dust.compute_attenuation(wave, theta)
        attn         = jnp.zeros((1, wave.shape[0]))
        return attn, attn_diffuse
    print("Using only diffuse dust attenuation.")
    self.attenuate_dust = attenuate_diffuse_only
```

### `kriek_conroy` — `external/sedpy_jax/sedpy_jax/attenuation_dust.py:354`

- Returns wavelength-dependent optical depth on the input wavelength grid, in angstroms. `tau_kc` controls its amplitude.
- Modifies a Calzetti-like curve with a power-law slope and a Drude profile, the broad feature centered at 2175 angstroms.
- `dust_index` changes both the slope and the feature strength. The fit therefore cannot vary those two properties independently through this function.

```python
def kriek_conroy(wave, tau_kc=1.0, dust_index=0.0, **kwargs):
    lamuvb = 2175.0  # Å, central wavelength of UV bump
    dlam = 350.0     # Å, width of UV bump
    lamv = 5500.0    # Å, normalization wavelength

    cal00 = jnp.where(
        wave >= 6300.0,
        1.17 * (-1.857 + 1.04 * (1e4 / wave)) + 1.78,
        1.17 * (-2.156 + 1.509 * (1e4 / wave) -
                0.198 * (1e4 / wave) ** 2 +
                0.011 * (1e4 / wave) ** 3) + 1.78
    )

    cal00 = jnp.maximum(cal00 / (0.44 * 4.05), 0.0)

    eb = 0.85 - 1.9 * dust_index

    drude = (eb * (wave * dlam) ** 2) / (
        (wave**2 - lamuvb**2) ** 2 + (wave * dlam) ** 2
    )

    tau_lambda = tau_kc * (cal00 + drude / 4.05) * (wave / lamv) ** dust_index
    return tau_lambda
```

## 6. Mass and distance

### `_apply_mass_redshift_igm` — `ceridwen/ceridwen/csp/csp_afe.py:1302`

- The SFH transform normalizes the integrated star formation to one solar mass. Multiplication by `10^logmass` sets the model's mass amplitude.
- Applies the cosmological flux factor at the fixed redshift. `SedModel.predict` can supply its cached value through `flux_factor`, avoiding repeated distance integration.
- DR2 disables intergalactic medium (IGM) attenuation, so `self.igm` is `None`. This function scales flux without changing `self.wave`.

```python
def _apply_mass_redshift_igm(self, spectrum_phot, spectrum_slit,
                             line_slit, theta):
    if "logmass" in theta:
        mass_scale = jnp.float32(10.0 ** theta["logmass"][0])
        spectrum_phot = spectrum_phot * mass_scale
        spectrum_slit = spectrum_slit * mass_scale
        line_slit     = line_slit     * mass_scale

    if "zred" in theta:
        from ..cosmology import flux_factor_maggies
        z_scalar = jnp.ravel(theta["zred"])[0]
        if "flux_factor" in theta:
            ff = jnp.ravel(theta["flux_factor"])[0].astype(jnp.float32)
        else:
            ff = jnp.float32(flux_factor_maggies(z_scalar, self.cosmo))
        spectrum_phot = spectrum_phot * ff
        spectrum_slit = spectrum_slit * ff
        line_slit     = line_slit     * ff
        if self.igm is not None:
            if "igm_factor" in theta:
                ig_factor = jnp.ravel(theta["igm_factor"])[0]
            else:
                ig_factor = jnp.float32(self.igm_factor)
            transmission = self.igm.attenuation(
                self.wave, z_scalar, factor=ig_factor,
            ).astype(spectrum_phot.dtype)
            spectrum_phot = spectrum_phot * transmission
            spectrum_slit = spectrum_slit * transmission
            line_slit     = line_slit     * transmission

    return spectrum_phot, spectrum_slit, line_slit
```

## 7. Project onto the data

### `_project_observations` — `ceridwen/ceridwen/csp/csp_afe.py:1342`

- Each observation maps the model spectrum to its data: filter-integrated fluxes for photometry and values on the observed wavelength grid for spectroscopy.
- The DR2 spectrum observation has its velocity dispersion configured separately. Zero CSP velocity dispersion therefore does not remove broadening from the observation model.
- Optional `spectrum_scaling` multiplies only the spectroscopic prediction, allowing relative flux calibration against photometry. The returned dictionary supplies the predictions for the likelihood.

```python
def _project_observations(self, spectrum_phot, spectrum_slit, line_slit,
                          observations, theta):
    from ..observation.observation import (
        Photometry as _Photometry,
        Spectrum   as _Spectrum,
    )
    ...
    out = {}
    free_z_in_theta = "zred" in theta
    spectrum_scaling = (jnp.ravel(theta["spectrum_scaling"])[0]
                 if "spectrum_scaling" in theta else None)
    for obs in observations:
        spec_for_obs = (spectrum_phot if isinstance(obs, _Photometry)
                        else spectrum_slit)
        if (isinstance(obs, _Photometry)
                and getattr(obs, "free_z", False)
                and free_z_in_theta):
            out[obs.name] = obs.predict_at_redshift(
                spec_for_obs, self.wave, jnp.ravel(theta["zred"])[0]
            )
        elif (isinstance(obs, _Spectrum)
              and getattr(obs, "fit_sigma_smooth", False)
              and "sigma_smooth" in theta):
            pred = obs.predict(
                spec_for_obs, self.wave,
                sigma_smooth=jnp.ravel(theta["sigma_smooth"])[0],
            )
            out[obs.name] = (pred * spectrum_scaling.astype(pred.dtype)
                             if spectrum_scaling is not None else pred)
        else:
            pred = obs.predict(spec_for_obs, self.wave)
            if spectrum_scaling is not None and isinstance(obs, _Spectrum):
                pred = pred * spectrum_scaling.astype(pred.dtype)
            out[obs.name] = pred
    return out
```

## 8. Slow path, for reference

### `_flux_at_afe` — `ceridwen/ceridwen/csp/csp_afe.py:920`

- Interpolates the full SSP spectra across alpha enhancement, producing shape `(13, 107, n_wave)` for the DR2 grid.
- This supplies individual age spectra when the fast-path conditions fail. The normal DR2 call instead interpolates the cached eight-node basis.

```python
def _flux_at_afe(self, theta):
    if self._n_afe == 1:
        return self.flux[0]
    if "afe" not in theta:
        return self.flux[self._afe_solar_idx]
    k, w = self._afe_coords(theta)
    f_lo = jnp.take(self.flux, k - 1, axis=0)
    f_hi = jnp.take(self.flux, k,     axis=0)
    w32  = w.astype(jnp.float32)
    return (jnp.float32(1.0) - w32) * f_lo + w32 * f_hi
```

### `_ssp_weights` — `ceridwen/ceridwen/csp/csp_afe.py:1713`

- Recomputes age weights from the chosen lookback grid. A runtime `lookback_time` overrides the setup grid and bypasses the cached basis.
- Step interpolation averages adjacent node rates. It distributes each interval's formed mass over overlapping SSP age cells, then normalizes to preserve that interval's mass.
- Constant metallicity distributes these age weights between two metallicity planes, returning `(13, 107)`. The spectrum calculation sums the corresponding SSP spectra with these weights.

```python
def _ssp_weights(self, theta, *, zh_mode, sfh_mode):
    floor = 1e-30
    sfh = jnp.clip(theta["sfh"], floor, None)

    if "lookback_time" in theta:
        _times = jnp.atleast_1d(
            jnp.asarray(theta["lookback_time"], dtype=float)) * 1e9  # Gyr->yr
    elif self.track_zred_age and "zred" in theta:
        _times = self._lookback_from_zred(theta["zred"])             # years
    else:
        _times = self.sfh_times
    t_young = _times[:-1]
    t_old   = _times[1:]
    dt      = t_old - t_young

    if sfh_mode == "linear":
        ...
    else:  # sfh_mode == "step"
        if self.sfh_per_bin:
            sfh_mid = sfh
        else:
            sfh_mid = 0.5 * (sfh[:-1] + sfh[1:])
        m2 = sfh_mid * dt

        overlap = jnp.maximum(
            0.0,
            jnp.minimum(t_old[:, None],   self._ssp_voronoi_hi[None, :])
            - jnp.maximum(t_young[:, None], self._ssp_voronoi_lo[None, :])
        )
        w1 = sfh_mid[:, None] * overlap

    m1          = jnp.maximum(w1.sum(axis=1), 1e-30)
    sfh_weights = w1 * (m2 / m1)[:, None]

    if zh_mode == "const":
        total_sfh_weights = jnp.maximum(0.0, sfh_weights.sum(axis=0))

        target_Z = theta["Z"]
        z_idx = jnp.clip(
            jnp.searchsorted(self.zmet, target_Z, side='left'),
            1, self._n_z - 1,
        )
        z1 = self.zmet[z_idx - 1]
        z2 = self.zmet[z_idx]
        w  = jnp.clip((target_Z - z1) / (z2 - z1), 0.0, 1.0)

        total_weights = jnp.zeros((self._n_z, self._n_age))
        total_weights = total_weights.at[z_idx - 1].add((1 - w) * total_sfh_weights)
        total_weights = total_weights.at[z_idx    ].add(      w  * total_sfh_weights)
        return total_weights

    ...
```