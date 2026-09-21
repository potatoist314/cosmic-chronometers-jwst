---
title: Notebook map
date: 2026-09-09
section: Notebooks
theme: Model and code reference
tags: [notebooks]
job:
old: _old/notebooks/notebook-map.html
---

<details>
<summary>Scope</summary>

Two Ceridwen notebooks are the current fitting entry points. One post-processing notebook presents a completed feature-spectrum result. Older inference branches are inactive. The practice notebooks are in `archive/notebooks/practice/`. Saved outputs are evidence only when the cell source, execution order, inputs, and kernel still match.

</details>

<details>
<summary>Ceridwen notebooks</summary>

- **Spectral notebook**One Spectrum observation
- **Joint notebook**Photometry and Spectrum observations

1. **SedModel**Shared forward model
2. **BlackJAX NSS**Checkpointed fit
3. **HDF5 result**Reloadable posterior
4. **Posterior report**Tables and corner plots

</details>

<figure>
<figcaption>The notebooks differ in observations but use the same inference path.</figcaption>
</figure>

<details>
<summary>Details</summary>

`ceridwen_test_spectra.ipynb` fits one LEGA-C spectrum. It fetches the published high-resolution Kroupa grid with schema 2.1. It converts wavelength and flux, creates a `Spectrum`, and adds calibration noise. It then runs BlackJAX nested sampling. Its full profile uses 500 live points, 100 deletions, and 60 inner steps. It uses `logZ_tol=-5`.

`CERIDWEN_SPECTRUM_MODE` selects `full` or `features`. Full mode fits 3,523 pixels. Feature mode fits 1,924 pixels from the LEGA-C DR2 feature definitions and their local continuum bands. The notebook fits native flux pixels. It does not fit the catalogue index values. \(\mathrm{H}\beta\) is absent because the nebular-emission mask removes its central band.

Both modes compact the spectrum before Ceridwen builds the model. They retain two masked endpoint pixels. These endpoints preserve the same smoothing boundaries as the native 6,166-pixel spectrum.

`notebooks/ceridwen_test_spectra.ipynb` · “Build the native-resolution spectrum” · `fit_pixel_mask` and `compact_indices`

</details>

```
fit_pixel_mask = native_fit_mask.copy()
if SPECTRUM_MODE == "features":
    fit_pixel_mask &= feature_pixel_mask

projection_anchor_indices = np.array([0, len(wave_vacuum) - 1])
compact_indices = np.unique(
    np.concatenate((np.flatnonzero(fit_pixel_mask), projection_anchor_indices))
)`
```

<details>
<summary>Details</summary>

The notebook markdown requires compact arrays and two endpoint pixels for identical smoothing boundaries.

Full and feature modes use the same projection boundary while they select different likelihood pixels.

`ceridwen_integrated_photometry_spectra.ipynb` combines all 12 photometric bands with the full native LEGA-C spectrum (more than 3,000 pixels) in one `SedModel` and one `MultiObservationLikelihood`. Since 2026-09-18 the notebook has eleven code cells: settings and priors, data and target, observations, model, fit, sampling diagnostics, output fit, spectrum fit, calibration polynomial, corners and SFH. Since 2026-09-20 a figure shows the prior-to-posterior KL divergence in bits for each sampled parameter, using `kl_table` from `scripts/plot_prior_kl.py`; since 2026-09-21 it shows points with bootstrap error bars on a log axis, a grey band at the measured estimator noise floor and a dashed line at 1 bit, a stated convention for a factor-two narrowing of the prior. Every fit setting and prior is a literal in the `SETTINGS` and `PRIORS` dicts of the top cell; the launcher only passes the target, manifest index, seed and result directory through the environment. A parameter is sampled when it has a `PRIORS` entry, so removing the `zred` or `sigma_smooth` line fixes that parameter. The earlier stellar-index mode and the mock, pixel-selection, prior and photometry switches were removed with the executed notebooks regenerated from the stored posteriors (`scripts/regenerate_fit_notebooks.py`).

The fit samples `spectrum_scaling` for the slit normalization. Photometry anchors the total flux. The spectral likelihood also samples its fractional calibration floor.

The production profile uses 500 live points, 100 deletions, 65 inner steps, and `logZ_tol=-5`.

The full-spectrum fit figure shades nine major absorption features from `ceridwen.observation.absorption_features` on both panels: Ca K, Ca H, \(\mathrm{H}\delta\), G band, \(\mathrm{H}\gamma\), Fe4383, \(\mathrm{H}\beta\), Mg b and Fe5270. Bands span their Lick bandpass and lines span \(\pm\)1000 \(\mathrm{km\,s^{-1}}\), redshifted with the catalogue redshift, so the pull near each feature can be read directly.

That marking is the production standard for every plot with a wavelength axis. `scripts/spectral_figures.py` holds it: `mark_absorption_features(ax, zred)` gives each feature a fixed colour for its shading and dotted edges. One legend lists the visible features on the right. `spectral_tight_layout(fig)` reserves the legend column without narrowing the original figure. Photometric SED panels in observed μm and non-wavelength plots (corner, SFH, histograms) stay bare. Tests: `tests/test_spectral_figures.py`.

The fit notebook’s photometry figure uses `plot_photometry_fit` in `scripts/spectral_figures.py`, showing the median continuum and LEGA-C spectral range. Spacing places band names with leader lines on a rail between flux and pull panels, keeping 12–30 bands readable; do not call `spectral_tight_layout` on this figure.

`scripts/spectral_figures.py` holds `FIT_FIGURE_RCPARAMS`, applied on import: font size 9, axes linewidth 0.8, inward ticks on all sides; `scripts/per_galaxy_diagnostics.py`, fit notebook figures and `scripts/plot_cosmos_photometry_comparison.py` use this style.

The sampler cell of both template notebooks runs `BlackJAXNestedSamplerAdapter` with `verbose=False` and `progress_path=RESULT_DIR / "ns_progress.jsonl"`. The cell output holds the `sampler settings:` line, one `sampler progress:` line and `result.summary()`. The progress line gives iterations, dead points per second, likelihood calls per second and the file path. The sampler appends one JSON line per iteration and flushes it, so a killed run keeps its history. Each line holds `iteration`, `n_discarded`, `n_likelihood_calls`, `logZ`, `logZ_live`, `delta_logZ`, `elapsed_s`, `iteration_s`, `dead_per_s` and `likelihood_calls_per_s`. Both rates are cumulative over `elapsed_s`. `scripts/run_ceridwen_vast_multi_gpu.py` fetches the file with the other results. Tests: `ceridwen/tests/test_ns_checkpoint.py`, `tests/test_ceridwen_dr2_production.py`.

Executed notebooks older than the marking standard were not refitted. `scripts/relabel_executed_figures.py` redraws the fit figure and the posterior-predictive spectrum figure from `ceridwen_derived_outputs.h5`, with `plot_fit_spectrum` and `plot_predictive_spectrum` in `scripts/per_galaxy_diagnostics.py`. It replaces the PNG in the same cell and output slot, so wiki figure references by cell and output index still resolve. It finds cells by source text, not by index. It removes sampler progress lines from the sampler cell only when `execution.log` beside the notebook holds the same text. Changed cells carry the metadata key `relabelled_by`, and a second run skips them. The data legend of the fit figure sits below the panels. Inside the axes it covered the band names. Tests: `tests/test_relabel_executed_figures.py`, `tests/test_per_galaxy_diagnostics.py`.

An early cell shows the target itself. It reads the HST ACS F814W cutout from `data/raw/hst_f814w/`. It draws the cutout with an asinh stretch. The axes give the offset from the catalogue position in arcseconds. North is up and east is left. A circle of 1.5-arcsecond radius marks the COSMOS2015 3-arcsecond aperture. The cell prints a note and draws nothing when the cutout is absent. `scripts/backfill_hst_cutout_cell.py` inserted the same cell, with its output, into the 187 executed notebooks under `results/dr2-quiescent-new-defaults/`. That backfill repeated no fit.

The joint notebook reads `CERIDWEN_TARGET_ID`, `CERIDWEN_RESULT_DIR`, and `CERIDWEN_RANDOM_SEED`. The defaults retain the original M1_210210 run. The Vast multi-GPU launcher sets one fixed target and seed for each sequential one-GPU worker.

The joint notebook selects at most 400 deterministic posterior rows. It uses those same rows for direct parameters, mass-weighted age, and formed-mass fractions. It checks finite values, equal row counts, non-negative mass fractions, and unit row sums before plotting.

The physical corner output shows mass, metallicity, alpha enhancement, diffuse dust, calibration floor, spectrum scaling, and mass-weighted age. The second corner output shows age with each formed-mass fraction. A third corner output shows the dust parameters against every formed-mass fraction with per-pair Spearman rank correlations. Executed notebooks from before this default got the same figure from their saved posteriors through `scripts/add_dust_sfh_corner.py`, with no refit. All three figures remain embedded in the executed notebook. Index mode also stores observed indices, posterior predictions, uncertainties, masks, units, and pulls in `ceridwen_derived_outputs.h5`.

All current corner plots use 40-bin blue density maps with Gaussian smoothing. Darker blue marks higher relative posterior density. Existing quantiles and contour probability levels remain unchanged.

The paired RTX 5060 result keeps separate executed reports in its `baseline/` and `fastpath_a/` directories. Each report loads its matching HDF5 posterior and contains the complete fit, residual, corner, and SFH output set. The reports do not overlay the two implementations.

Both notebooks supply the observed FWHM resolving power with `res_convention="fwhm"`. Ceridwen reads the SSP resolution curve from the grid. It calculates the additional smoothing automatically.

Both notebooks configure nested-sampling checkpoints every 20 minutes. Each completed run also writes a rescue snapshot and a final reloadable `ceridwen_result.h5` file. A UTC-stamped results directory contains these files.

The DR2 production notebook also writes analysis-ready summary, SFH, photometry, spectrum, and diagnostics groups to `ceridwen_derived_outputs.h5`.

The spectra notebook also writes `ceridwen_derived_outputs.h5`. It contains normalized and equal-weight posterior samples, compact and native-grid predictions, star-formation histories, summary values, and diagnostics.

`archive/notebooks/ceridwen_feature_spectrum_posterior_report.ipynb` reads the completed feature-spectrum HDF5 files without rerunning Ceridwen. It presents run metadata, 13 one-dimensional marginals, a physical corner plot, an age-SFH corner plot, and the SFH beside its age posterior. The fit samples seven log-SFR ratios. The report uses the 400 stored, index-aligned SFH draws to show mass-weighted age as a derived posterior quantity.

`archive/results/dr2-quiescent-no-polynomial/ceridwen_cosmic_chronometer.ipynb` loads the 187 validated production summaries. It follows the Borghi differential-age construction: two velocity-dispersion groups, four fixed redshift bins, alternate-bin age differences, and inverse-variance combination. It propagates the stored Ceridwen age draws with 10,000 fixed-seed galaxy bootstrap samples. Each realization draws one age per unique galaxy before it resamples galaxies. It also fits an unbinned common slope with a separate intercept for each dispersion group. Its tables and seven figures stay embedded; the numerical tables and bootstrap draws are also stored in `ceridwen_cosmic_chronometer_summary.h5`.

The aggregate notebook contains an exploratory analysis. Its age is the mass-weighted SFH lookback age, not the Lick SSP-equivalent age. The production fit also sets the oldest SFH node from `age_gyr(z)` under the Planck-2018 defaults, so the derived quantity is not a cosmology-independent chronometer measurement.

The executed notebook uses 164 galaxies inside the Borghi redshift range. The fixed-bin combination gives \(H(z=0.741)=-63.6\pm17.8\) \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\). The posterior-plus-bootstrap median is -77.4 \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\) with a 68-percent interval from -196.3 to -39.9 \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\); 14.6 percent of draws are positive. The public Borghi reconstruction gives \(97.5\pm31.3\) \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\), close to the published central value but not its exact bin membership or uncertainty. The exact 68-galaxy overlap gives \(86.3\pm38.0\) with Borghi ages and \(228.5\pm43.6\) with Ceridwen ages.

The overlap age residual has a 7.32 Gyr-per-redshift slope. The Planck-based formation-time diagnostic also decreases with redshift. The unbinned Ceridwen slope is only 1.2 standard errors below zero, while binning, \(\mathrm{S/N}\) cuts, and the dispersion split can change the result's sign or scale.

</details>

<details>
<summary>Practice</summary>

`archive/notebooks/practice/fits-viewer.ipynb` contains one cell that inspects a FITS table. It is a viewer, not an analysis pipeline.

</details>

<details>
<summary>Kernels</summary>

- `archive/notebooks/practice/fits-viewer.ipynb` records the root Python 3.14 kernel.
- The two Ceridwen notebooks record Python 3.11 kernels.
- The posterior report records the project Python 3.14 kernel.

Kernel choice is part of each notebook’s executable contract.

</details>

<details>
<summary>Examples</summary>

`notebooks/ceridwen_integrated_photometry_spectra.ipynb` · “Fit” · `joint_likelihood` through `write_result_h5`

</details>

```
joint_likelihood = MultiObservationLikelihood(
    keys=("photometry", "spectrum"),
    likelihoods=(
        DiagonalGaussianLikelihood(),
        DiagonalGaussianLikelihood(
            noise_model=DiagonalNoiseModel(use_fractional=True),
            calibration=calibration_polynomial,
        ),
    ),
)
...
joint_result = run_sampler(joint_model, joint_likelihood, joint_adapter, jax.random.PRNGKey(SEED))
result_path = RESULT_DIR / "ceridwen_result.h5"
write_result_h5(result_path, joint_model, joint_result)`
```

<details>
<summary>Details</summary>

The notebook markdown requires independent photometric and spectroscopic likelihoods, checkpoints, and a saved posterior.

One sampler call combines both observation types. The reload checks preserve parameter and likelihood shapes.

`src/chronometer.py:101-115` · `hubble_from_age_slope`

</details>

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

<details>
<summary>Details</summary>

`tests/test_chronometer.py` checks the conversion, sign, zero-slope limit, and group-intercept invariance.

A slope near zero maps to a broad, non-Gaussian \(H(z)\) distribution. The notebook therefore reports quantiles and the positive fraction.

</details>
