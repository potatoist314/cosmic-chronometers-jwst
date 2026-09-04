---
title: Notebook map
date: 2026-09-01
section: Notebooks
tags: [notebooks]
job: 
old: _old/notebooks/notebook-map.html
---

### Scope

Two Ceridwen notebooks are the current fitting entry points. One post-processing notebook presents a completed feature-spectrum result. Older inference branches are inactive. The `notebooks/practice/` directory contains the practice notebooks. Saved outputs are evidence only when the cell source, execution order, inputs, and kernel still match.

### Ceridwen notebooks

- **Spectral notebook**One Spectrum observation
- **Joint notebook**Photometry and Spectrum observations

1. **SedModel**Shared forward model
2. **BlackJAX NSS**Checkpointed fit
3. **HDF5 result**Reloadable posterior
4. **Posterior report**Tables and corner plots

<figure>
<figcaption>The notebooks differ in observations but use the same inference path.</figcaption>
</figure>

`ceridwen_test_spectra.ipynb` fits one LEGA-C spectrum. It fetches the published high-resolution Kroupa grid with schema 2.1. It converts wavelength and flux, creates a `Spectrum`, and adds calibration noise. It then runs BlackJAX nested sampling. Its full profile uses 500 live points, 100 deletions, and 60 inner steps. It uses `logZ_tol=-5`.

`CERIDWEN_SPECTRUM_MODE` selects `full` or `features`. Full mode fits 3,523 pixels. Feature mode fits 1,924 pixels from the LEGA-C DR2 feature definitions and their local continuum bands. The notebook fits native flux pixels. It does not fit the catalogue index values. Hβ is absent because the nebular-emission mask removes its central band.

Both modes compact the spectrum before Ceridwen builds the model. They retain two masked endpoint pixels. These endpoints preserve the same smoothing boundaries as the native 6,166-pixel spectrum.

`notebooks/ceridwen_test_spectra.ipynb` · “Build the native-resolution spectrum” · `fit_pixel_mask` and `compact_indices`

```
fit_pixel_mask = native_fit_mask.copy()
if SPECTRUM_MODE == "features":
    fit_pixel_mask &= feature_pixel_mask

projection_anchor_indices = np.array([0, len(wave_vacuum) - 1])
compact_indices = np.unique(
    np.concatenate((np.flatnonzero(fit_pixel_mask), projection_anchor_indices))
)`
```

**Documented contract:** The notebook markdown requires compact arrays and two endpoint pixels for identical smoothing boundaries.

**Why it matters:** Full and feature modes use the same projection boundary while they select different likelihood pixels.

`ceridwen_integrated_photometry_spectra.ipynb` combines photometry with one selectable stellar-spectroscopy observation in one `SedModel` and one `MultiObservationLikelihood`. `CERIDWEN_FIT_MODE=full_spectrum` fits more than 3,000 native pixels and all 12 photometric bands. `stellar_indices` fits up to 14 published absorption indices and all 12 photometric bands.

Full-spectrum mode fits `spectrum_scaling` for the slit normalization. Photometry anchors the total flux. The spectral likelihood also samples its fractional calibration floor. Stellar-index mode remains scale invariant and uses catalogue diagonal uncertainties.

Both modes use the published high-resolution grid. The production profile uses 500 live points, 100 deletions, 65 inner steps, and `logZ_tol=-5`.

The joint notebook reads `CERIDWEN_TARGET_ID`, `CERIDWEN_RESULT_DIR`, and `CERIDWEN_RANDOM_SEED`. The defaults retain the original M1_210210 run. The Vast multi-GPU launcher sets one fixed target and seed for each sequential one-GPU worker.

The joint notebook selects at most 400 deterministic posterior rows. It uses those same rows for direct parameters, mass-weighted age, and formed-mass fractions. It checks finite values, equal row counts, non-negative mass fractions, and unit row sums before plotting.

The physical corner output shows mass, metallicity, alpha enhancement, diffuse dust, calibration floor, spectrum scaling, and mass-weighted age. The second corner output shows age with each formed-mass fraction. Both figures remain embedded in the executed notebook. Index mode also stores observed indices, posterior predictions, uncertainties, masks, units, and pulls in `ceridwen_derived_outputs.h5`.

All current corner plots use 40-bin blue density maps with Gaussian smoothing. Darker blue marks higher relative posterior density. Existing quantiles and contour probability levels remain unchanged.

The paired RTX 5060 result keeps separate executed reports in its `baseline/` and `fastpath_a/` directories. Each report loads its matching HDF5 posterior and contains the complete fit, residual, corner, and SFH output set. The reports do not overlay the two implementations.

Both notebooks supply the observed FWHM resolving power with `res_convention="fwhm"`. Ceridwen reads the SSP resolution curve from the grid. It calculates the additional smoothing automatically.

Both notebooks configure nested-sampling checkpoints every 20 minutes. Each completed run also writes a rescue snapshot and a final reloadable `ceridwen_result.h5` file. A UTC-stamped results directory contains these files.

The DR2 production notebook also writes analysis-ready summary, SFH, photometry, spectrum, and diagnostics groups to `ceridwen_derived_outputs.h5`.

The spectra notebook also writes `ceridwen_derived_outputs.h5`. It contains normalized and equal-weight posterior samples, compact and native-grid predictions, star-formation histories, summary values, and diagnostics.

`ceridwen_feature_spectrum_posterior_report.ipynb` reads the completed feature-spectrum HDF5 files without rerunning Ceridwen. It presents run metadata, 13 one-dimensional marginals, a physical corner plot, an age-SFH corner plot, and the SFH beside its age posterior. The fit samples seven log-SFR ratios. The report uses the 400 stored, index-aligned SFH draws to show mass-weighted age as a derived posterior quantity.

`results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer.ipynb` loads the 187 validated production summaries. It follows the Borghi differential-age construction: two velocity-dispersion groups, four fixed redshift bins, alternate-bin age differences, and inverse-variance combination. It propagates the stored Ceridwen age draws with 10,000 fixed-seed galaxy bootstrap samples. Each realization draws one age per unique galaxy before it resamples galaxies. It also fits an unbinned common slope with a separate intercept for each dispersion group. Its tables and seven figures stay embedded; the numerical tables and bootstrap draws are also stored in `ceridwen_cosmic_chronometer_summary.h5`.

The aggregate notebook labels its result as exploratory. Its age is the mass-weighted SFH lookback age, not the Lick SSP-equivalent age. The production fit also sets the oldest SFH node from `age_gyr(z)` under the Planck-2018 defaults, so the derived quantity is not a cosmology-independent chronometer measurement.

The executed notebook uses 164 galaxies inside the Borghi redshift range. The fixed-bin combination gives `H(z=0.741)=-63.6 +/- 17.8` km/s/Mpc. The posterior-plus-bootstrap median is -77.4 km/s/Mpc with a 68-percent interval from -196.3 to -39.9 km/s/Mpc; 14.6 percent of draws are positive. The public Borghi reconstruction gives `97.5 +/- 31.3` km/s/Mpc, close to the published central value but not its exact bin membership or uncertainty. The exact 68-galaxy overlap gives `86.3 +/- 38.0` with Borghi ages and `228.5 +/- 43.6` with Ceridwen ages.

The overlap age residual has a 7.32 Gyr-per-redshift slope. The Planck-based formation-time diagnostic also decreases with redshift. The unbinned Ceridwen slope is only 1.2 standard errors below zero, while binning, S/N cuts, and the dispersion split can change the result's sign or scale. These checks identify age-definition drift, population drift, and estimator instability. They do not support a stable positive Ceridwen chronometer measurement.

### Practice

`notebooks/practice/fits-viewer.ipynb` contains one cell that inspects a FITS table. It is a viewer, not an analysis pipeline.

### Kernels

- `notebooks/practice/fits-viewer.ipynb` records the root Python 3.14 kernel.
- The two Ceridwen notebooks record Python 3.11 kernels.
- The posterior report records the project Python 3.14 kernel.

Kernel choice is part of each notebook’s executable contract.

### Examples

`notebooks/ceridwen_integrated_photometry_spectra.ipynb` · “Joint posterior” · `spectroscopic_likelihood` through `write_result_h5`

```
spectroscopic_likelihood = (
    DiagonalGaussianLikelihood(
        noise_model=DiagonalNoiseModel(use_fractional=True)
    )
    if FIT_MODE == "full_spectrum"
    else DiagonalGaussianLikelihood()
)
joint_likelihood = MultiObservationLikelihood(
    keys=(phot_obs.name, spectroscopic_obs.name),
    likelihoods=(DiagonalGaussianLikelihood(), spectroscopic_likelihood),
)
joint_result = run_sampler(
    joint_model,
    joint_likelihood,
    joint_adapter,
    jax.random.PRNGKey(SEED),
)
result_path = RESULT_DIR / "ceridwen_result.h5"
write_result_h5(result_path, joint_model, joint_result)`
```

**Documented contract:** The notebook markdown requires independent photometric and spectroscopic likelihoods, checkpoints, and a saved posterior.

**Why it matters:** One sampler call combines both observation types. The reload checks preserve parameter and likelihood shapes.

`src/chronometer.py:101-115` · `hubble_from_age_slope`

```
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
    )`
```

**Documented contract:** `tests/test_chronometer.py` checks the conversion, sign, zero-slope limit, and group-intercept invariance.

**Why it matters:** A slope near zero maps to a broad, non-Gaussian H(z) distribution. The notebook therefore reports quantiles and the positive fraction.
