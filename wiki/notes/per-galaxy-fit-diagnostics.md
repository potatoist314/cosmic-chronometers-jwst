---
title: Per-galaxy fit diagnostics
date: 2026-09-05
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_8a78968d
---

Sample
: 187 galaxies, DR2 quiescent full-spectrum fits, `results/rtx-5060-dr2-quiescent-full-spectrum/`

Per galaxy
: three figures and one model-parameter file in each `<target>/diagnostics/` folder. All 187 are inline in [Per-galaxy fit diagnostics, gallery](../per-galaxy-diagnostics-gallery/)

Fit inputs
: stored masks, sigma and ndof equal the sampler's observation arrays for 187 of 187 galaxies

Photometric chi²/N
: median 7.04, 5-95 percent range 2.00 to 17.49, above 3 for 157 galaxies

Spectral chi²/N
: median 1.120, 5-95 percent range 1.026 to 1.488, above 1.5 for 10 galaxies

Calibration floor
: median 4.8 percent. 17 galaxies sit at the 10 percent prior bound

Table
: `results/per-galaxy-diagnostics.csv`, one row per galaxy, 80 columns

Notebook
: `notebooks/ceridwen_per_galaxy_diagnostics.ipynb`, executed

Commit
: `9d7fb7b` · `origin/absorption-mask`

## Definitions

pull = (observed − model) / sigma. Every figure shows two model choices:

- **stored**: the fitting notebook's numbers. The model is the pointwise posterior median q50 of 200 predictive draws. sigma_eff² = sigma_obs² + (f_calib · |q50|)². f_calib is the posterior-median calibration floor. q50 is not one model realisation.
- **at theta_ML**: the diagnostics rebuild the `SedModel` from `ceridwen_result.h5`. They evaluate Ceridwen's own `DiagonalGaussianLikelihood` at the dead point with the highest stored log-likelihood. `LikelihoodOutput.chi` is the per-datum pull with exactly the sigma the sampler used. That sigma includes the sampled f_calib · |mu(theta)| term.

Reduced chi-squared:

- per data set: chi²/N over its fitted data
- spectrum and photometry share the 13 free parameters, so no per-data-set ndof exists
- joint: chi² / (N_phot + N_spec − 13)

t_X is the lookback time by which X percent of the final stellar mass had formed. So t10 ≥ t20 ≥ t50 ≥ t80 ≥ t90. The summary CSV counts mass younger than t. Therefore t20 here equals t80 there, and t50 equals t50. Within a bin the SFR is constant, so mass accumulates linearly. 400 posterior mass-fraction draws give the 16-84 and 2.5-97.5 percent intervals.

## Checks

- The stored masks, sigma and ndof equal the observation arrays in `ceridwen_result.h5` for every galaxy. The stored pulls and chi-squared totals reproduce from their definitions to 1e-12.
- The rebuilt effective sigma matches the stored one to 0.3 percent. The residual comes from the notebook's 2000-draw equal-weight resampling of f_calib.
- Spectral chi² at theta_ML differs from the stored value by +0.1 percent in the median and at most 2 percent. Photometric chi² differs by ±4 percent (16-84 percent) and at most 57 percent. The pointwise median of 12 bands is far from any single draw.
- ln L recomputed on the CPU at theta_ML differs from the stored GPU value. Median −1.4, 16-84 percent range −4.0 to +0.3, extremes −10.7 and +4.6. 16 galaxies lie beyond ±5. The offset is systematic per galaxy, with sample-to-sample scatter 0.4 to 1.2 for the three galaxies probed. It grows with S/N (Spearman −0.32). Candidate cause: the float32 SSP grid combined with TF32 matrix precision on the GPU. The GPU verification below tests it.

## Example: M1_210210

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-photometric_chi2.png" alt="M1_210210: per-band pull and chi-squared contribution against wavelength">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_210210. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 116.2 stored and 117.0 at theta_ML over 12 bands. Caveat: the spectrum dominates the joint fit.</figcaption>
</figure>

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-spectral_chi2.png" alt="M1_210210: per-pixel pull, binned mean pull squared and cumulative chi-squared against wavelength with masked windows and outliers marked">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of M1_210210, mean pull squared in 25 Å bins, and the cumulative chi-squared fraction. Sigma includes the fitted 4.62 percent calibration floor. Shaded bands mark masked pixels and red points mark 10 pixels beyond 4 sigma. Total chi-squared 3919.2 stored and 3935.2 at theta_ML over 3523 pixels. Caveat: the fitted floor absorbs model mismatch.</figcaption>
</figure>

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-sf_timescales.png" alt="M1_210210: fraction of final mass formed earlier than each lookback time with t10 to t90 and their posterior intervals">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of M1_210210 formed earlier than each lookback time, median and 16-84 percent band over 400 posterior draws. Points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals. t10 6.99, t50 4.68, t90 1.50 Gyr. Caveat: the 7-bin SFH quantises these times.</figcaption>
</figure>

The blue 40 percent of the fitted pixels carry 60 percent of the spectral chi². They cover rest 3800 to 4300 Å, from Ca H and K to the G band. The photometry is misfit at 5.5 sigma in u*, 4.9 sigma in V and 4.9 sigma at 4.5 µm. The spectrum sits at chi²/N 1.11. The spectrum outweighs the twelve bands by two to three orders of magnitude in summed (S/N)². The joint fit therefore ignores the broadband shape.

## Model parameters, generated from the model object

```
MODEL PARAMETERS (generated from the SedModel object)
Stellar population grid
  library: C3K v2.3 high-res (c3k_hr, vt=10 km/s); isochrones: MIST v2.5 (aMIST, alpha-variable); IMF: imf_type=2 (Kroupa (2001)); schema 2.1
  grid axes: [alpha/Fe] [-0.2, 0, 0.2, 0.4, 0.6]; log10 Z 13 nodes [-4.233, -1.233] (absolute Z); log10(age/Gyr) 107 nodes; wavelength 10992 pts [100, 99595855] A
Star-formation history
  form: piecewise-constant SFR ('step' interpolation) on 7 lookback bins; metallicity history: constant Z
  bin edges (lookback, Gyr): [0, 0.03, 0.1, 0.3, 1, 3, 5, 7.566]  (last edge = universe age at z)
  free parameters: logsfr_ratios[7] = log10(SFR_i / SFR_i+1), transform 'sfh_from_ratios' -> unit-mass SFH (integral 1 Msun); logmass scales the total formed mass
Free parameters and priors
  Z: shape (1,); prior Uniform(-4.233, -1.233); init [-1.85]
  afe: shape (1,); prior Uniform(-0.2, 0.6); init [0.2]
  diffuse_tau_kc: shape (1,); prior Uniform(0, 2); init [0.2]
  log_f_calib: shape (1,); prior Uniform(-4.605, -2.303); init [-3.507]
  logmass: shape (1,); prior Uniform(8, 13); init [11.1]
  logsfr_ratios: shape (7,); prior Uniform(-3, 3); init [0, 0, 0, 0, 0, 0, 0]
  spectrum_scaling: shape (1,); prior ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3); init [1]
Fixed and derived quantities
  redshift: fixed at z = 0.654200 (SedModel.zred); SFH age grid tracks z: False
  diffuse_dust_index: fixed by transform '<lambda>' = [-0.7]
Dust, nebular emission, IGM
  diffuse attenuation: law 'kriek_conroy', parameters ['diffuse_tau_kc', 'diffuse_dust_index']; birth-cloud (age-dependent) dust: False; dust emission: False
  nebular emission: none (spectrum model 'get_spectrum_dattn_nodem_noneb')
  IGM absorption: none
  cosmology: Cosmology(H0=67.66, Om0=0.30966, Tcmb0=2.7255, Neff=3.046, m_nu_ev_sum=0.06)
Observations and calibration
  photometry: Photometry, 12 bands, 12 fitted; filters ['cfht_megacam_us_9301', 'subaru_suprimecam_B', 'subaru_suprimecam_V', 'subaru_suprimecam_rp', 'subaru_suprimecam_ip', 'subaru_suprimecam_zp', 'vista_vircam_Y', 'vista_vircam_J', 'vista_vircam_H', 'vista_vircam_Ks', 'spitzer_irac_ch1', 'spitzer_irac_ch2']
  spectrum: Spectrum, 3523 of 6166 native pixels fitted, 6199-8635 A observed; instrument R = 2500 (R, fwhm); fixed stellar sigma_losvd = 259.5 km/s; CSP-level LOSVD 0.0 km/s
  likelihood[photometry]: DiagonalGaussianLikelihood with DiagonalNoiseModel: var = sigma_obs^2 (no extra terms)
  likelihood[spectrum]: DiagonalGaussianLikelihood with DiagonalNoiseModel: var = sigma_obs^2 + model-scaled fractional floor f_calib*|mu| (log_f_calib free in [1%, 10%])
  likelihood[spectrum] calibration polynomial: none
  spectrum normalisation: free multiplicative spectrum_scaling, prior ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3)
Sampler
  blackjax.nss: num_live 500, num_inner_steps 65, num_delete 100, logZ_tol -5.0; random seed 20260832
```

`model_parameter_block()` in `scripts/per_galaxy_diagnostics.py` reads every line above from these objects:

- `SedModel` (free parameters, priors, transforms, redshift)
- `CSPBasis_afe` (SFH form and bins, dust law, nebular and IGM switches, cosmology)
- `SSPDataAfe` (library, isochrones, IMF, grid axes)
- `Photometry`, `Spectrum` (bands, fitted pixels, resolution, fixed sigma_losvd)
- `DiagonalGaussianLikelihood` and its `DiagonalNoiseModel` (variance terms, calibration polynomial)

Across the 187 galaxies six values change:

- the redshift
- the last SFH edge (universe age at z)
- the fixed sigma_losvd
- the fitted pixel count and range
- the logmass initial value
- the seed

Each `<target>/diagnostics/model_parameters.txt` holds that galaxy's block. The fitting notebook now prints the same block from the live model. It stores the text as `parameter_block` in both HDF5 files. `write_result_h5` does not persist the CSP switches, the fixed dust index or the smoothing convention. The rebuild takes those from constants that mirror the notebook. The diagnostics compare a stored block with the rebuilt one when a result carries one.

## Flags

157 galaxies have photometric chi²/N above 3. 17 have the calibration floor at its bound. 173 have at least one pixel with |pull| above 4 (median 5, maximum 82). 3 galaxies have no flag.

<figure>
<img src="figures/per-galaxy-diagnostics/photometry-summary.png" alt="Median photometric pull per band over all galaxies, mean chi-squared contribution per band, and the histogram of photometric chi-squared per band">
<figcaption><code>photometry-summary.png</code> Left: median photometric pull per band over 187 galaxies. Uncertainty: bars span the 16-84 percent range over galaxies. Middle: mean chi-squared contribution per band. Right: histogram of chi-squared per band. Pull equals observed minus model over sigma with the 5 percent floor. Comparison: the IRAC bands sit 3.7 and 4.2 sigma above the model. Caveat: the spectrum dominates the joint fit.</figcaption>
</figure>

| Band | u* | B | V | r+ | i+ | z+ | Y | J | H | Ks | 3.6 µm | 4.5 µm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| median pull | −0.59 | −1.67 | +1.59 | −0.08 | −1.95 | +0.23 | −1.76 | −1.02 | −0.97 | +0.67 | +3.65 | +4.23 |
| mean chi² | 5.8 | 11.2 | 4.8 | 5.0 | 6.8 | 3.5 | 3.8 | 1.9 | 3.4 | 4.0 | 20.7 | 23.7 |

The photometric misfit is systematic, not per-galaxy noise. The two IRAC bands are brighter than the model by 3.7 and 4.2 sigma in the median. With the 5 percent floor that is about 20 percent of the flux. They supply half of the photometric chi². B, i+ and Y sit 1.7 to 2 sigma below the model. V sits 1.6 sigma above it. The worst cases are the highest-S/N spectra: S/N 30 to 45, chi²/N 19 to 29, IRAC pulls up to 11. The better the spectrum, the less the photometry counts. Two explanations remain open. Either the 3-arcsecond aperture photometry is inconsistent with the IRAC total fluxes, or the stellar model lacks rest-frame 2 µm flux. The per-band pattern shows this before any refit. The 5 percent floor does not describe the errors of these bands.

The 17 galaxies at the calibration bound (f_calib ≥ 9.8 percent) are the only ones with spectral chi²/N above 1.5. The fit wanted a larger error floor than the prior allows. For them the spectrum errors or the model are wrong. Sorted by spectral chi²/N:

- 139662 (2.69), 253688 (2.55), 101089 (2.34), 185631 (1.80), 104877 (1.78)
- 216899 (1.71), 98104 (1.55), 244680 (1.55), 101830 (1.54), 259737 (1.53)
- 258753, 255047, 162587, 36550, 231554, 87207, 89072 (all below 1.5)

Their pixel outliers, 13 to 82 per galaxy, mark residual sky and template features the floor cannot absorb. For the other 170 galaxies chi²/N sits at 1.03 to 1.49 by construction. The fitted floor absorbs the misfit. So f_calib (median 4.8 percent) measures the model-data mismatch, not chi².

## Formation timescales across the sample

<figure>
<img src="figures/per-galaxy-diagnostics/sf-timescale-summary.png" alt="Galaxies sorted by t50 with t10 to t90 bands, t_X against redshift, and histograms of t10, t50 and t90">
<figcaption><code>sf-timescale-summary.png</code> t10 to t90 for 187 galaxies. Left: galaxies sorted by t50 with the t80 to t20 and t90 to t10 bands and 16-84 percent bars on t50. Middle: t10, t50 and t90 against redshift with the universe age. Right: histograms of the posterior medians. Caveat: the 7-bin SFH quantises every t_X.</figcaption>
</figure>

Sample medians: t10 4.64, t20 4.23, t50 3.02, t80 1.80, t90 1.39 Gyr. Median 16-84 percent half-widths are 0.04 to 0.09 Gyr. 66 galaxies have t50 within 0.1 Gyr of 3.0 Gyr. 12 have t50 within 0.1 Gyr of 4.6 Gyr. The 2-Gyr bins at 1-3 and 3-5 Gyr quantise every t_X. The small posterior widths are widths within a bin, not the age resolution. Treat t_X differences below one bin width as unresolved.

## GPU verification

Instance
: Vast.ai 49915972, `NVIDIA GeForce RTX 5060, 8151 MiB, 580.82.09` (`gpu.txt`), host 166946 (UK), offer $0.1028/h, $0.1222/h with the 40 GB disk

Spend
: 0.427 h. $0.052 at the instance rate, $0.044 at the offer rate (`spend_estimate_usd`). Account credit fell $0.090, which includes a concurrent job's instance in the same window. Cap $2

Destroyed
: yes, verified absent after the destroy call (`vast_run_20260905T011450Z.json`)

Refits
: M1_210210 and M2_139662 with the production settings and seeds, both exit 0, both pass `_validate_result`

Files
: `results/rtx-5060-per-galaxy-diagnostics-verification/` with the executed notebooks, both HDF5 files, `gpu_lnl_check.log`, `refit_vs_production.csv`, `diagnostics/` figures

Refit against the August production fit:

| Galaxy | ln Z production | ln Z refit | wall production | wall refit | age production | age refit | largest median shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M2_139662 | 222329.41 ± 0.25 | 222330.47 ± 0.25 | 1119 s | 252 s | 5.21 Gyr | 5.10 Gyr (−0.6σ) | 0.4σ (logmass) |
| M1_210210 | 229449.03 ± 0.19 | 229441.28 ± 0.38 | 1196 s | 291 s | 4.50 Gyr | 4.94 Gyr (+7σ) | 3.6σ (logmass, +0.028 dex) |

GPU log-likelihood check (`gpu_lnl_check.log`). The rebuilt model on the GPU reproduces the stored ln L(theta_ML) of the fresh fits. Differences: −0.002 (M1_210210) and +0.001 (M2_139662). On the CPU the same check gives −0.06 and −0.02. For the August production fits the GPU gives −4.56 (M1_210210) and +0.01 (M2_139662). The CPU gives the same: −4.63 and −0.003. The offset therefore comes from neither device precision nor sigma nor masks. It comes from a change of the Ceridwen forward model between the August production code and the current tree. The project's own re-projection of the 187 stored medians recorded Δχ² mean +3.3 and rms 6.2 for that change (`benchmarks/ceridwen/runs/dr2_stored_fit_revalidation_2026-09-01.json`). The four times shorter wall time is the same code change.

Flag: for the high-S/N galaxy M1_210210 the current model moves the mass-weighted age by 0.44 Gyr, seven posterior sigma. The production errors (±0.06 Gyr) do not include this implementation systematic. The lower-S/N galaxy M2_139662 reproduces within one sigma.

The block the notebook stored from the live model equals the rebuilt block line for line, order-insensitive, for both refits.

## Commands

```
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py run
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py check results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py block results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py gallery
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics_vast.py run --target M1_210210 --target M2_139662 --spend-cap-usd 2
ceridwen/.venv/bin/python -m pytest tests/test_per_galaxy_diagnostics.py -q
```
