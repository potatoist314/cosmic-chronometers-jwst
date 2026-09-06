---
title: Ceridwen: observations and SedModel
date: 2026-09-06
section: Codebase
tags: [ceridwen]
job: 
old: _old/codebase/ceridwen-observations-model.html
---

Observations define the measured data space. `SedModel` connects these data containers to the CSP forward model. It also selects the sampled parameters.

### Observation contract

- **Photometry**Filters
- **Spectrum**Observed pixels
- **Lines**Line fluxes
- **StellarIndices**Absorption features

<figure>
<figcaption>Each subclass projects the same model spectrum into a different measured space.</figcaption>
</figure>

Every `Observation` stores:

- `flux` contains one-dimensional measured values.
- `uncertainty` contains one-dimensional one-sigma errors.
- `mask` is Boolean. `True` includes a datum.
- `name` is the unique key in prediction dictionaries.

`ceridwen/ceridwen/observation/base.py:59-89` constructs observations and converts the arrays to JAX arrays. `rectify` checks the shapes and masks invalid values automatically (`lines 189-233`).

Forward prediction can use an observation without flux values. The observation must contain known filters or a known wavelength grid (`base.py:194-202`).

`ceridwen/ceridwen/observation/base.py:204-216 · Observation.rectify`

```
assert self.flux.ndim == 1,        "flux must be 1-D"
assert self.uncertainty is not None, "uncertainty is required when flux is provided"
assert self.uncertainty.ndim == 1, "uncertainty must be 1-D"
assert len(self.flux) == len(self.uncertainty), \
    "flux and uncertainty lengths differ"

if self.wavelength is not None:
    assert self.wavelength.ndim == 1, "wavelength must be 1-D"
    assert len(self.wavelength) == len(self.flux), \
        f"wavelength length ({len(self.wavelength)}) ≠ flux length ({len(self.flux)})"

self._automask()
assert self.ndof > 0, "no valid unmasked data points after masking"`
```

**Documented contract:** The base-class docstring defines flux, one-sigma uncertainty, and a mask where `True` includes the datum (`ceridwen/ceridwen/observation/base.py:25-46`).

**Why it matters:** The assertions define the data contract. The input arrays must be one-dimensional and aligned. Automatic masking must leave at least one usable datum.

### Projection contract

`setup_for_model(wave_model)` performs the static work before JIT compilation. `predict` performs the numerical projection at each model evaluation (`base.py:270-319`). `SedModel.__init__` prepares every observation automatically. It also supplies the SSP library resolution curve (`model/model.py:219-240`).

1. **Model wavelength grid**Static input
2. **`setup_for_model`**Prepare matrices or closure
3. **`predict`**Project each spectrum
4. **Measured-space values**Match observation length

<figure>
<figcaption>Setup prepares fixed work before repeated numerical predictions.</figcaption>
</figure>

#### Photometry

`Photometry` stores AB maggies. One maggie is 3631 Jy (`observation/photometry.py:19-46`). The class converts model `F_nu` to `F_lambda`. It then integrates the filter transmission (`lines 117-151`). The prediction contains one value for each filter.

`ceridwen/ceridwen/observation/photometry.py:264-266`

```
if getattr(self, "_has_precomputed_T", False):
    return self._T @ spectrum
return self.get_maggies(wave_model, spectrum)`
```

The fast path uses one matrix-vector multiplication. The alternative path performs the same filter projection without a precomputed matrix.

#### Spectrum

`ceridwen/ceridwen/observation/spectrum.py:477-482 · Spectrum.setup_for_model`

```python
        if not has_instr and not has_losvd:
            # Preserve the dense matrix's independently rounded coefficients.
            lo, hi = jnp.asarray(j_lo), jnp.asarray(j_hi)
            w_lo = jnp.asarray((1.0 - alpha).astype(np.float32))
            w_hi = jnp.asarray(alpha.astype(np.float32))
            self._predict_fn = lambda spec: w_lo * spec[lo] + w_hi * spec[hi]
```

When every width is known at setup, the two broadening stages become one. Gaussians add in quadrature, so a LOSVD followed by an instrumental LSF is a single Gaussian of width `sqrt(losvd^2 + instrument^2 - library^2)` at each wavelength. `observation/_smoothing.py` builds that one convolution and bakes its interpolation indices and its Fourier taper at setup, so no call recomputes them. The chained form remains for `fit_sigma_smooth=True`, where the width is a traced value.

No flag or environment variable selects the combined form. The installed ceridwen package decides. The superproject records the ceridwen commit that contains `_smoothing.py`, and `.gitmodules` points at the project copy `potatoist314/ceridwen`, because the upstream repository does not carry these commits. `scripts/bootstrap_vast_ai.sh` reinstalls ceridwen from the tree on every run and stops when `ceridwen.observation._smoothing` does not import. That check exists because a non-editable install ignores files copied into the source tree after bootstrap.

The combined form is both cheaper and closer to the analytic width, because it interpolates once rather than twice. The resampling grid is also floored at the input grid size: sizing it from the kernel width alone let a wide kernel undersample the model spectrum. Photometry predictions are unchanged.

`res_convention="fwhm"` means that the supplied instrumental resolution is a FWHM value. With `inres="auto"`, Ceridwen uses the schema-2.1 grid resolution curve. It applies only the additional width required in quadrature (`lines 291-366`). The project GPU workflows install sedpy_jax from the `external/sedpy_jax` submodule: upstream commit `0291d58`, which accepts that per-pixel array, plus one commit that builds filters in NumPy instead of JAX. Filter construction happens once per fit, at setup, and that change cut per-fit setup from about 150 s to about 27 s on a rented GPU.

`ceridwen/ceridwen/observation/spectrum.py:790-804 · Spectrum.predict`

```
if self.fit_sigma_smooth:
    if sigma_smooth is None:
        # Fall back to the constructor default; lets a caller
        # invoke ``predict(spec, wave)`` for warmup / debugging
        # even when the closure is the runtime-sigma variant.
        sigma_smooth = self.sigma_losvd
    # Pass sigma through without forcing a dtype -- JAX's
    # dtype-promotion rules with jax_enable_x64=True will
    # promote to float64 to match the cached smoother grids,
    # giving the same precision the static fast path achieved.
    # Forcing float32 here would round-trip-degrade the smoother
    # output even when the user is fitting in double precision.
    sv = jnp.asarray(sigma_smooth).reshape(())
    return self._predict_fn(spectrum, sv)
return self._predict_fn(spectrum)`
```

**Documented contract:** The method docstring requires prior setup and returns model `F_nu` on the observed pixels (`ceridwen/ceridwen/observation/spectrum.py:740-778`).

**Why it matters:** Both branches call the closure that setup prepared. Only the fitted velocity branch supplies a traced smoothing parameter.

#### Lines

`Lines` represents continuum-subtracted emission-line fluxes. The solar-scaled `CSPBasis` can predict these fluxes from nebular grids. `CSPBasis_afe` cannot predict them because it has no nebular component.

#### Stellar indices

`StellarIndices` represents integrated stellar absorption indices and continuum breaks. It is separate from `Lines`, which represents nebular emission fluxes. The LEGA-C definition set contains 13 Lick indices and `Dn4000`.

The class converts the standard rest-air bandpasses to vacuum. Its internal `Spectrum` projector applies the SSP-library, instrumental, and fixed stellar-velocity broadening. Equivalent widths and CN magnitudes use `F_lambda`. `Dn4000` is the red-to-blue `F_nu` ratio (`ceridwen/ceridwen/observation/stellar_indices.py:115-123` and `209-317`).

### Spectrum scaling

Ceridwen can calculate one analytic multiplicative scale for each spectrum before it evaluates the likelihood (`csp/csp.py:1357-1429` and `csp/csp_afe.py:1291-1363`). The project notebooks disable this scale. Full-spectrum mode uses a fixed i-band aperture transfer. Stellar-index mode is scale invariant and uses no aperture transfer.

### SedModel parameter bookkeeping

`SedModel.__init__` starts with `csp.theta_init`. It removes parameters that transforms will derive. It then adds the replacement free parameters (`model/model.py:141-195`). It contains these items:

- `theta_init` contains the initial arrays for free parameters.
- `param_names` contains the ordered free parameter names.
- `priors` contains probability distributions for free parameters.
- `transforms` contains calculations from free parameters to derived parameters.
- `observations` contains the projection targets.

The active notebooks use this parameter structure:

1. **Free parameters**SFR ratios, Z, afe, mass, and dust
2. **Transforms**Derive SFH values
3. **Model parameters**Add fixed or derived values
4. **CSP prediction**Use one named dictionary

<figure>
<figcaption>SedModel converts sampled values into the complete CSP parameter dictionary.</figcaption>
</figure>

### One prediction

`SedModel.predict(theta)` performs these steps:

1. It applies every transform (`model/model.py:313-342`).
2. It inserts the fixed redshift when sampling does not include it (`lines 384-398`).
3. It calls `csp.predict(model_theta, observations)` (`line 401`).
4. It receives a dictionary keyed by unique observation names.

`predict_jit` caches compilation for one parameter tree. `predict_vmap` adds a leading sample dimension for posterior predictions (`model/model.py:407-452`).

`ceridwen/ceridwen/model/model.py:395-401`

```
if self._zred_fixed is not None and "zred" not in model_theta:
    if model_theta is theta:          # apply_transforms may not copy
        model_theta = dict(model_theta)
    model_theta["zred"] = self._zred_fixed
# Mass scaling is handled inside csp.predict() — the spectrum is
# scaled once before projection, rather than per-observation.
return self.csp.predict(model_theta, self.observations)`
```

The code inserts a fixed redshift only when the sampled dictionary does not contain one. The final line returns a dictionary. The observation names are its keys.

### Shapes and units

- A scalar free parameter usually has shape `(1,)`.
- `logsfr_ratios` has shape `(n_sfh_bins - 1,)`.
- Each prediction dictionary value matches its observation length.
- `logmass` is the `log10` formed stellar mass in solar masses.
- `Z` is `log10` absolute metallicity.
- `afe` is `[alpha/Fe]` in dex.
- `zred` is dimensionless.
