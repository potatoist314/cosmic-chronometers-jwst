---
title: M1_210210 without the emission-line mask
date: 2026-09-21
section: Analyses
theme: Single-fit accuracy
tags: [ceridwen, emission-lines, masking, reference-galaxy]
job:
figures: [fit-M1_210210.png, sfh-M1_210210.png, corner-M1_210210.png]
---

## Fits

Target
: M1_210210, LEGA-C DR2, \(z=0.6542\). Record: `wiki/research/experiments/e-no-emission-mask.md`.

Masked
: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`. Lines at 3726.0, 3728.8, 4861.3, 4958.9 and 5006.8 \(\mathrm{\AA}\) masked within \(\pm1500\,\mathrm{km/s}\). Ceridwen c540bc7; not re-run.

No mask
: `results/no-emission-mask/no_emission_mask/210210-M1_210210`. `SETTINGS["emission_lines"] = []` through arm `no_emission_mask` of `scripts/calibration_arms_vast.py`; telluric mask kept. Branch at 92e203c, ceridwen b419fd1.

Common
: Seed 20260832, calibration order 10, \(\tau_{\mathrm{dust}}\) Uniform(0, 1), sampled \(z\) and \(\sigma_\star\), BlackJAX NSS, 12 `cosmos_total` bands, one RTX 5060 Ti on Vast.ai. Notebook: `results/no-emission-mask/analysis.ipynb`.

<figure>
<img src="figures/no-emission-mask/fit-M1_210210.png" alt="M1_210210 spectrum, calibration polynomial and photometry with the posterior medians of the masked and no-mask fits">
<figcaption>Spectrum, calibration polynomial and photometry with posterior medians of the masked and no-mask fits.</figcaption>
</figure>

<figure>
<img src="figures/no-emission-mask/sfh-M1_210210.png" alt="Star-formation history and cumulative mass fraction of M1_210210 for the masked and no-mask fits">
<figcaption>SFH and cumulative mass fraction, both fits.</figcaption>
</figure>

<figure>
<img src="figures/no-emission-mask/corner-M1_210210.png" alt="Overlaid corner plot of mass-weighted age, [Fe/H], [alpha/Fe], stellar mass, dust optical depth and velocity dispersion for the masked and no-mask fits">
<figcaption>Grey shapes are the fit with emission lines masked and red outlines the fit with no mask, each the \(1\sigma\) contour with the 1D posteriors on the diagonal: an offset between a red outline and its grey shape means those parameters moved, and a smaller red outline means a tighter constraint.</figcaption>
</figure>

## Parameters

| Quantity | Masked | No mask |
| --- | --- | --- |
| Emission-line mask | 5 lines, \(\pm1500\,\mathrm{km\,s^{-1}}\) | none |
| Fitted spectral pixels | 3523 | 3939 |
| \(\ln Z\) | 231153.16 ± 0.35 | 258237.78 ± 0.45 |
| Spectral \(\chi^2\), catalogue uncertainties, own pixels | 10772.1 | 12368.4 |
| Spectral \(\chi^2\), catalogue uncertainties, 3523 common pixels | 10772.1 | 10955.5 |
| Photometric \(\chi^2\) | 55.0 | 50.9 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.650 ± 0.013 | 11.645 ± 0.013 |
| \([\mathrm{Fe}/\mathrm{H}]\) | -0.159 ± 0.022 | -0.153 ± 0.019 |
| \([\alpha/\mathrm{Fe}]\) | +0.060 ± 0.010 | +0.045 ± 0.010 |
| \(\tau_{\mathrm{dust}}\) | 0.405 ± 0.013 | 0.398 ± 0.015 |
| \(\delta_{\mathrm{dust}}\) | -0.987 ± 0.014 | -0.987 ± 0.015 |
| \(t_{\mathrm{MW}}\) [Gyr] | 5.19 ± 0.12 | 5.18 ± 0.10 |
| \(t_{50}\) [Gyr] | 5.32 ± 0.17 | 5.35 ± 0.17 |
| \(f_{\mathrm{calib}}\) [%] | 2.52 ± 0.05 | 2.55 ± 0.05 |
| \(z\) | 0.654219 ± 0.000015 | 0.654207 ± 0.000016 |
| \(\sigma_\star\) [km/s] | 263.4 ± 3.1 | 266.0 ± 2.9 |
| ESS | 4923 | 4862 |
| Likelihood calls | 10 455 667 | 10 215 612 |
| Sampler wall time [s] | 1502 | 1475 |
| Vast instance, spend | 51331110, $0.086 | 51896980, $0.082 |

Posterior median and half the 16-84% width. Shift: no-mask median minus masked median, in masked half-widths. KL from each fit's own prior, `kl_table` in `scripts/plot_prior_kl.py`.

| Parameter | Shift [masked half-widths] | Width, no mask / masked | KL masked [bits] | KL no mask [bits] |
| --- | --- | --- | --- | --- |
| \([\mathrm{Fe}/\mathrm{H}]\) | +0.34 | 0.92 | 5.11 | 5.20 |
| \([\alpha/\mathrm{Fe}]\) | -1.72 | 1.01 | 4.33 | 4.32 |
| \(\delta_{\mathrm{dust}}\) | +0.01 | 1.10 | 4.98 | 4.82 |
| \(\tau_{\mathrm{dust}}\) | -0.65 | 1.11 | 4.17 | 4.05 |
| \(\log f_{\mathrm{calib}}\) | +0.29 | 0.96 | 4.92 | 5.00 |
| \(\log_{10}(M_\star/M_\odot)\) | -0.37 | 0.94 | 6.61 | 6.69 |
| \(\log[\mathrm{SFR}(0)/\mathrm{SFR}(0.03\,\mathrm{Gyr})]\) | +0.11 | 1.18 | 5.84 | 5.69 |
| \(\log[\mathrm{SFR}(0.03)/\mathrm{SFR}(0.1\,\mathrm{Gyr})]\) | -0.09 | 1.07 | 0.20 | 0.13 |
| \(\log[\mathrm{SFR}(0.1)/\mathrm{SFR}(0.3\,\mathrm{Gyr})]\) | -0.05 | 0.98 | 0.09 | 0.09 |
| \(\log[\mathrm{SFR}(0.3)/\mathrm{SFR}(1\,\mathrm{Gyr})]\) | -0.05 | 1.04 | 0.14 | 0.13 |
| \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) | -0.14 | 1.05 | 5.02 | 6.16 |
| \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) | +0.56 | 0.88 | 2.80 | 2.53 |
| \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) | -0.33 | 0.96 | 0.74 | 0.47 |
| \(\sigma_\star\) | +0.87 | 0.97 | 0.79 | 1.32 |
| spectrum scaling | -0.44 | 1.02 | 3.26 | 3.25 |
| \(z\) | -0.63 | 1.00 | 11.57 | 11.58 |
| \(t_{\mathrm{MW}}\) | -0.08 | 0.86 |  |  |

## Residual pull at the formerly masked lines

| Line | Window [km/s] | Pixels | Mean pull | \(1/\sqrt{N}\) | RMS pull |
| --- | --- | --- | --- | --- | --- |
| \([\mathrm{O\,II}]\) 3726 | ±1500 | 5 | -1.83 | 0.45 | 0.68 |
| \([\mathrm{O\,II}]\) 3726 | ±300 | 0 | | | |
| \([\mathrm{O\,II}]\) 3729 | ±1500 | 13 | -1.40 | 0.28 | 1.11 |
| \([\mathrm{O\,II}]\) 3729 | ±300 | 0 | | | |
| \(\mathrm{H}\beta\) | ±1500 | 134 | +0.05 | 0.09 | 0.53 |
| \(\mathrm{H}\beta\) | ±300 | 27 | +0.09 | 0.19 | 0.53 |
| \([\mathrm{O\,III}]\) 4959 | ±1500 | 137 | +0.30 | 0.09 | 1.26 |
| \([\mathrm{O\,III}]\) 4959 | ±300 | 27 | +0.85 | 0.19 | 1.18 |
| \([\mathrm{O\,III}]\) 5007 | ±1500 | 138 | +0.08 | 0.09 | 0.72 |
| \([\mathrm{O\,III}]\) 5007 | ±300 | 28 | +0.57 | 0.19 | 0.68 |

<details>
<summary>Table notes</summary>

No-mask fit only. Pull is (observed − posterior-median model) over the total uncertainty with the fitted calibration floor. Windows about each rest wavelength at the catalogue redshift. Errors are \(1/\sqrt{N}\). Source: `results/no-emission-mask/line-residual-pulls.csv`.

</details>
