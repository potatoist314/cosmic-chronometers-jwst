---
title: M1_210210 reference fit
date: 2026-09-17
section: Analyses
theme: Single-fit accuracy
tags: [ceridwen, calibration, reference-galaxy, priors]
job:
figures: [fit-M1_210210.png, sfh-M1_210210.png, corner-M1_210210.png, kl-M1_210210.png]
---

## Fits

Target
: M1_210210, LEGA-C DR2, \(z = 0.6542\), \(\sigma_\star = 260\,\mathrm{km/s}\), catalogue S/N 62.2. Roadmap task `strong-spectrum`. Record: `wiki/research/experiments/e-m1-210210-reference.md`.

A
: `results/dr2-quiescent-new-defaults/210210-M1_210210`. Calibration order 3, \(\tau_{\mathrm{dust}}\) Uniform(0, 2), fixed \(z\) and \(\sigma_\star\).

B
: `results/m1-210210-reference/tau-0p2/poly10/210210-M1_210210`. Order 10, \(\tau_{\mathrm{dust}}\) Uniform(0, 0.2), fixed \(z\) and \(\sigma_\star\). Branch at 55ff5f4, ceridwen 56505a6.

C
: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`. Order 10, \(\tau_{\mathrm{dust}}\) Uniform(0, 1), \(z\) Uniform(\(z_{\mathrm{cat}} \pm 0.1\)), \(\sigma_\star\) ClippedNormal(259.5, 6.5). Branch at cc983ce, ceridwen c540bc7. Production defaults.

Common
: Seed 20260832, BlackJAX NSS, 3523 spectral pixels, 12 `cosmos_total` bands, one RTX 5060 Ti on Vast.ai. Notebook: `results/m1-210210-reference/analysis.ipynb`.

## Parameters

| Quantity | A | B | C |
| --- | --- | --- | --- |
| Calibration order | 3 | 10 | 10 |
| \(\tau_{\mathrm{dust}}\) prior | Uniform(0, 2) | Uniform(0, 0.2) | Uniform(0, 1) |
| \(z\), \(\sigma_\star\) | fixed | fixed | sampled |
| \(\ln Z\) | 230683.02 ± 0.38 | 231041.38 ± 0.37 | 231153.16 ± 0.35 |
| Spectral \(\chi^2\), catalogue uncertainties | 13970.3 | 11308.6 | 10773.3 |
| Spectral \(\chi^2\) at fit A's floor | 3692.8 | 3059.2 | 2857.2 |
| Photometric \(\chi^2\) | 90.0 | 89.9 | 55.0 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.551 ± 0.018 | 11.561 ± 0.012 | 11.650 ± 0.013 |
| \([\mathrm{Fe}/\mathrm{H}]\) | +0.146 ± 0.019 | -0.273 ± 0.044 | -0.159 ± 0.022 |
| \([\alpha/\mathrm{Fe}]\) | -0.022 ± 0.007 | +0.036 ± 0.010 | +0.060 ± 0.010 |
| \(\tau_{\mathrm{dust}}\) | 0.443 ± 0.012 | 0.199 ± 0.001 | 0.405 ± 0.013 |
| \(\delta_{\mathrm{dust}}\) | -0.992 ± 0.009 | -0.995 ± 0.005 | -0.987 ± 0.014 |
| \(t_{\mathrm{MW}}\) [Gyr] | 3.92 ± 0.18 | 5.20 ± 0.14 | 5.19 ± 0.12 |
| \(t_{50}\) [Gyr] | 3.83 ± 0.18 | 5.37 ± 0.19 | 5.32 ± 0.17 |
| \(f_{\mathrm{calib}}\) [%] | 3.08 ± 0.05 | 2.62 ± 0.05 | 2.52 ± 0.05 |
| \(z\) | 0.6542 | 0.6542 | 0.654219 ± 0.000015 |
| \(\sigma_\star\) [km/s] | 259.5 | 259.5 | 263.4 ± 3.1 |
| ESS | 4094 | 4531 | 4923 |
| Likelihood calls | 8 706 256 | 8 415 066 | 10 455 667 |
| Sampler wall time [s] | 488 | 468 | 1502 |
| Vast instance, spend | | 51329179, $0.052 | 51331110, $0.086 |

Posterior median and half the 16-84% width.

<details>
<summary>Table notes</summary>

Spectral \(\chi^2\) is at the posterior median. Stored \(\chi^2\) values use each fit's own floor, with no comparison across fits.

</details>

<figure>
<img src="figures/m1-210210-reference/fit-M1_210210.png" alt="M1_210210 spectrum, calibration polynomial and photometry with the posterior medians of fits A, B and C">
<figcaption>Spectrum, calibration polynomial over fitted pixels with 16-84% band, and photometry, with the posterior medians of fits A, B and C.</figcaption>
</figure>

<figure>
<img src="figures/m1-210210-reference/sfh-M1_210210.png" alt="Star-formation history and cumulative mass fraction of M1_210210 for fits A, B and C">
<figcaption>Star-formation history and cumulative mass fraction.</figcaption>
</figure>

<figure>
<img src="figures/m1-210210-reference/corner-M1_210210.png" alt="Corner plot of stellar mass, [Fe/H], [alpha/Fe], dust optical depth, dust index and mass-weighted age for fits A, B and C">
<figcaption>Physical-parameter posteriors, 1\(\sigma\) contours.</figcaption>
</figure>

## KL divergence from the prior

Quantity
: \(D_{\mathrm{KL}}(\mathrm{posterior}\,\|\,\mathrm{prior}) = \int p(\theta) \log_2 [p(\theta)/\pi(\theta)]\,d\theta\) per sampled parameter, in bits. 0 bits: posterior equal to prior. One bit: the prior range halved.

Estimate
: `scripts/plot_prior_kl.py`, `marginal_kl_bits` in `scripts/per_galaxy_diagnostics.py`. \(u = F_{\mathrm{prior}}(\theta)\) makes the prior Uniform(0, 1). Weighted histogram of \(u\) over the dead points, 40 bins across the 0.05-99.95% range plus one outer bin each side. Bootstrap half-widths are 0.03 bits or less. Tests: Gaussian under a Uniform prior, posterior equal to prior, posterior at a prior edge.

<figure>
<img src="figures/m1-210210-reference/kl-M1_210210.png" alt="Horizontal bars of KL divergence in bits for each sampled parameter of M1_210210, fits A, B and C, sorted by fit C">
<figcaption>KL divergence of each sampled parameter from its own fit's prior, sorted by fit C.</figcaption>
</figure>

The \(\tau_{\mathrm{dust}}\) prior widths are 2, 0.2 and 1, and fit B sits at its 0.2 bound.

| Parameter | A | B | C |
| --- | --- | --- | --- |
| \(z\) | | | 11.57 |
| \(\log_{10}(M_\star/M_\odot)\) | 6.23 | 6.60 | 6.61 |
| \(\log[\mathrm{SFR}(0)/\mathrm{SFR}(0.03\,\mathrm{Gyr})]\) | 6.89 | 0.95 | 5.84 |
| \([\mathrm{Fe}/\mathrm{H}]\) | 5.14 | 4.40 | 5.11 |
| \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) | 7.75 | 4.86 | 5.02 |
| \(\delta_{\mathrm{dust}}\) | 5.60 | 6.31 | 4.98 |
| \(\log f_{\mathrm{calib}}\) | 5.01 | 4.87 | 4.92 |
| \([\alpha/\mathrm{Fe}]\) | 4.72 | 4.26 | 4.33 |
| \(\tau_{\mathrm{dust}}\) | 5.33 | 6.06 | 4.17 |
| Spectrum scaling | 3.23 | 3.53 | 3.26 |
| \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) | 1.96 | 1.58 | 2.80 |
| \(\sigma_\star\) | | | 0.79 |
| \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) | 0.50 | 0.15 | 0.74 |
| \(\log[\mathrm{SFR}(0.03)/\mathrm{SFR}(0.1\,\mathrm{Gyr})]\) | 0.09 | 1.10 | 0.20 |
| \(\log[\mathrm{SFR}(0.3)/\mathrm{SFR}(1\,\mathrm{Gyr})]\) | 0.04 | 0.13 | 0.14 |
| \(\log[\mathrm{SFR}(0.1)/\mathrm{SFR}(0.3\,\mathrm{Gyr})]\) | 0.06 | 0.28 | 0.09 |
| Sum of marginals | 52.5 | 45.1 | 60.6 |
| Joint, \((\langle\ln L\rangle - \ln Z)/\ln 2\) | 66.1 | 58.1 | 77.1 |

<details>
<summary>Table notes</summary>

SFR ratios are between the SFH nodes at the two lookback times. Joint: \((\langle\ln L\rangle - \ln Z)/\ln 2\) over all parameters.

</details>
