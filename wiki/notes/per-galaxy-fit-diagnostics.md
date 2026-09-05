---
title: Per-galaxy fit diagnostics
date: 2026-09-05
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_8a78968d
---

## Model settings

Sample
: 187 galaxies, DR2 quiescent full-spectrum fits, `results/rtx-5060-dr2-quiescent-full-spectrum/`. Every galaxy: [gallery](../per-galaxy-diagnostics-gallery/).

Stellar grid
: C3K v2.3 high-res (c3k_hr, vt=10 km/s), MIST v2.5 (aMIST, alpha-variable) isochrones, Kroupa (2001) IMF. Axes [alpha/Fe] -0.2, 0, 0.2, 0.4, 0.6, log10 Z 13 nodes, log10(age/Gyr) 107 nodes.

Star-formation history
: Constant star-formation rate in each of 7 lookback bins. Edges 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr, then the universe age at the galaxy redshift. Metallicity constant in time.

Free parameters and priors
: 13 free values. Z Uniform(-4.233, -1.233). afe Uniform(-0.2, 0.6). diffuse_tau_kc Uniform(0, 2). log_f_calib Uniform(-4.605, -2.303). logmass Uniform(8, 13). logsfr_ratios Uniform(-3, 3), 7 values. spectrum_scaling ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3).

Fixed
: Redshift at each galaxy's catalogue value, 0.603 to 0.987 across the sample. Dust index of the attenuation curve at -0.7. Stellar velocity dispersion at the catalogue value.

Dust, nebular emission and IGM
: kriek_conroy attenuation on the diffuse component. Birth-cloud dust false. Dust emission false. Nebular emission none. IGM absorption none.

Spectrum calibration
: No polynomial, order 0. A free fractional noise floor f_calib between 1 and 10 percent of the model flux. A free multiplicative scale spectrum_scaling.

Photometry anchor
: cosmos_ap3, the 12 COSMOS2015 3 arcsecond aperture fluxes with total IRAC and no offsets. The model photometry never carries the spectrum scale or a calibration polynomial.

## Sample

<figure>
<img src="figures/per-galaxy-diagnostics/photometry-summary.png" alt="Median photometric pull per band over all galaxies, mean chi-squared contribution per band, and the histogram of photometric chi-squared per band">
<figcaption>Median pull per band over 187 galaxies, the mean chi-squared per band, and its spread: the two IRAC bands carry half of it.</figcaption>
</figure>

<figure>
<img src="figures/per-galaxy-diagnostics/sf-timescale-summary.png" alt="Galaxies sorted by t50 with t10 to t90 bands, t_X against redshift, and histograms of t10, t50 and t90">
<figcaption>Formation times t10 to t90 for 187 galaxies, sorted by t50 and against redshift: sample medians 4.64, 3.02 and 1.39 Gyr.</figcaption>
</figure>

## Example: M1_210210

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-photometric_chi2.png" alt="M1_210210: per-band pull and chi-squared contribution against wavelength">
<figcaption>Pull of the 12 fitted fluxes of galaxy M1_210210 against the model: 116.2 over 12 bands with a 5 percent error floor.</figcaption>
</figure>

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-spectral_chi2.png" alt="M1_210210: per-pixel pull, binned mean pull squared and cumulative chi-squared against wavelength with masked windows and outliers marked">
<figcaption>Pull of 3523 fitted spectrum pixels of galaxy M1_210210 against the model: 1.11 per pixel at a 4.62 percent error floor.</figcaption>
</figure>

<figure>
<img src="figures/per-galaxy-diagnostics/M1_210210-sf_timescales.png" alt="M1_210210: fraction of final mass formed earlier than each lookback time with t10 to t90 and their posterior intervals">
<figcaption>Mass formed in galaxy M1_210210 against lookback time: t10 6.99, t50 4.68, t90 1.50 Gyr, only a 16-84 percent range.</figcaption>
</figure>

<details>
<summary>Details</summary>

Method, checks, flags and the GPU verification in full: `reports/astro-chisq-sf-plots-2026-09-06.md`.

| Term | Definition |
| --- | --- |
| pull | (observed − model) / sigma |
| stored | pointwise posterior median q50 of 200 draws, sigma_eff² = sigma_obs² + (f_calib · abs(q50))² |
| at theta_ML | Ceridwen's own likelihood at the dead point with the highest stored log-likelihood, with the sampler's sigma |
| chi²/N | chi² over the fitted data of one data set. The 13 free parameters are shared, so no per-data-set ndof exists |
| t_X | lookback time by which X percent of the final stellar mass had formed, so t10 ≥ t20 ≥ t50 ≥ t80 ≥ t90 |

| Sample quantity | Median | 5-95 percent | Flagged |
| --- | --- | --- | --- |
| photometric χ²/N | 7.04 | 2.00 to 17.49 | 157 above 3 |
| spectral χ²/N | 1.120 | 1.026 to 1.488 | 10 above 1.5 |
| calibration floor f_calib | 4.8% | — | 17 at the 10% prior bound |
| pixels with abs(pull) > 4 | 5 | — | 173 galaxies, maximum 82 |
| t10, t20, t50, t80, t90 [Gyr] | 4.64, 4.23, 3.02, 1.80, 1.39 | — | — |

3 of the 187 galaxies carry no flag.

| Band | u* | B | V | r+ | i+ | z+ | Y | J | H | Ks | 3.6 µm | 4.5 µm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| median pull | −0.59 | −1.67 | +1.59 | −0.08 | −1.95 | +0.23 | −1.76 | −1.02 | −0.97 | +0.67 | +3.65 | +4.23 |
| mean χ² | 5.8 | 11.2 | 4.8 | 5.0 | 6.8 | 3.5 | 3.8 | 1.9 | 3.4 | 4.0 | 20.7 | 23.7 |

| Check | Result |
| --- | --- |
| stored masks, sigma and ndof against the sampler's arrays | equal for 187 of 187 |
| stored pulls and χ² totals from their definitions | reproduce to 1e-12 |
| rebuilt effective sigma against the stored one | 0.3 percent |
| spectral χ² at theta_ML against the stored value | +0.1 percent median, 2 percent maximum |
| photometric χ² at theta_ML against the stored value | ±4 percent (16-84), 57 percent maximum |
| ln L recomputed on the CPU against the stored GPU value | median −1.4, 16-84 range −4.0 to +0.3 |

RTX 5060 refits of two galaxies with the production settings and seeds, Vast.ai instance 49915972, $0.052 for 0.427 h, destroyed. Files in `results/rtx-5060-per-galaxy-diagnostics-verification/`.

| Galaxy | ln Z production | ln Z refit | wall production | wall refit | age production | age refit |
| --- | --- | --- | --- | --- | --- | --- |
| M2_139662 | 222329.41 ± 0.25 | 222330.47 ± 0.25 | 1119 s | 252 s | 5.21 Gyr | 5.10 Gyr (−0.6σ) |
| M1_210210 | 229449.03 ± 0.19 | 229441.28 ± 0.38 | 1196 s | 291 s | 4.50 Gyr | 4.94 Gyr (+7σ) |

The offset comes from a change of the Ceridwen forward model, not from device precision, sigma or masks. For M1_210210 the current model moves the mass-weighted age by 0.44 Gyr, seven posterior sigma.

```
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py run
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py check results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py block results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py gallery
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics_vast.py run --target M1_210210 --target M2_139662 --spend-cap-usd 2
ceridwen/.venv/bin/python -m pytest tests/test_per_galaxy_diagnostics.py -q
```

Table, one row per galaxy: `results/per-galaxy-diagnostics.csv`. Executed notebook: `notebooks/ceridwen_per_galaxy_diagnostics.ipynb`. Commit `9d7fb7b` on `origin/absorption-mask`.

</details>
