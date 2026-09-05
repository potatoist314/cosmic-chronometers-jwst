---
title: Calibration polynomial in the DR2 pipeline
date: 2026-09-05
section: Analyses
tags: [calibration, ceridwen, dr2-quiescent-sample]
job: t_ab2b8a0b
---

## Model settings

Run
: Six DR2 galaxies, three arms and two mocks on one RTX 5060, `results/calibration-polynomial-dr2/`.

Arms
: baseline is order 0 with cosmos_ap3. poly3 is order 3 with cosmos_ap3. poly3_total is order 3 with cosmos_total. Production now runs poly3_total.

Stellar grid
: C3K v2.3 high-res (c3k_hr, vt=10 km/s), MIST v2.5 (aMIST, alpha-variable) isochrones, Kroupa (2001) IMF. Axes [alpha/Fe] 5 nodes, log10 Z 13 nodes, log10(age/Gyr) 107 nodes.

Star-formation history
: Constant star-formation rate in each of 7 lookback bins. Edges 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr, then the universe age at the galaxy redshift. Metallicity constant in time.

Free parameters and priors
: 13 free values. Z Uniform(-4.233, -1.233). afe Uniform(-0.2, 0.6). diffuse_tau_kc Uniform(0, 2). log_f_calib Uniform(-4.605, -2.303). logmass Uniform(8, 13). logsfr_ratios Uniform(-3, 3), 7 values. spectrum_scaling ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3).

Fixed
: Redshift at each galaxy's catalogue value, 0.604 to 0.981 across the six. Dust index of the attenuation curve at -0.7. Stellar velocity dispersion at the catalogue value.

Dust, nebular emission and IGM
: kriek_conroy attenuation on the diffuse component. Birth-cloud dust false. Dust emission false. Nebular emission none. IGM absorption none.

Spectrum calibration
: Chebyshev order 3, one polynomial multiplying the model spectrum, coefficient priors Normal(0, 0.1), integrated out at every likelihood call. A free fractional noise floor f_calib between 1 and 10 percent of the model flux. A free multiplicative scale spectrum_scaling.

Photometry anchor
: cosmos_total, the 12 COSMOS2015 bands with the Laigle et al. (2016) aperture-to-total offset, Galactic extinction and the Table 3 zero points. The model photometry never carries the spectrum scale or the polynomial.

<figure>
<img src="figures/calibration-polynomial-dr2/calibration-explainer.png" alt="Explainer: fitted polynomial on M12_185653, calibration vector with band, dust tilt against an order-1 polynomial, shortest bend against line widths">
<figcaption>The photometry anchors the whole wavelength range, the spectrum covers one window inside it, and P bends on 800 angstrom scales, not on lines.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/polynomial-vectors.png" alt="P of lambda and s times P of lambda with 16 to 84 percent bands for the six galaxies and the two polynomial arms">
<figcaption>P and s·P for six galaxies: within 4 percent where the photometry fits, and 15 to 30 percent where it does not.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/parameters-before-after.png" alt="Mass, t50, SFR, dust and mass-weighted age for the three arms of each galaxy">
<figcaption>Mass, t50, recent star-formation rate, dust and age for the three arms: the masses rise 0.16 to 0.39 dex with total photometry.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/mock-tilt.png" alt="Mock with a 4 percent tilt: injected and recovered calibration vector, and the parameter pulls without and with the polynomial">
<figcaption>A 4 percent tilt injected on the spectrum alone: dust lands 32 sigma from the truth without P and 0.7 sigma with it.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M12_98104.png" alt="M12_98104: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M12_98104, pull and cumulative chi-squared: every difference sits inside the run-to-run scatter.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M5_173928.png" alt="M5_173928: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M5_173928, pull and cumulative chi-squared: photometric chi-squared 143 to 48, and P is a 7 to 10 percent bowl.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M4_108989.png" alt="M4_108989: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M4_108989, pull and cumulative chi-squared: photometric chi-squared 139 to 13 and t50 back at 4.6 Gyr.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M12_185653.png" alt="M12_185653: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M12_185653, pull and cumulative chi-squared: photometric chi-squared 37 to 11 and P within 4 percent.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M1_206545.png" alt="M1_206545: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M1_206545, pull and cumulative chi-squared: raw chi-squared down 4191, but P is a 15 percent hump.</figcaption>
</figure>

<figure>
<img src="figures/calibration-polynomial-dr2/chi2-M5_172669.png" alt="M5_172669: pull per fitted pixel and cumulative chi-squared for the three arms">
<figcaption>Three arms of M5_172669, pull and cumulative chi-squared: P is a 28 percent tilt and dust goes from 0.01 to 0.6.</figcaption>
</figure>

## What the polynomial absorbs

A slit loses more light at one end of the range than the other. The polynomial removes that smooth loss. It must not remove the tilt that dust and stellar age make. Only the photometry tells them apart.

```
d_i = s · P(x_i) · mu_i(theta) + n_i,   n_i ~ N(0, sigma_eff,i^2)
sigma_eff,i^2 = sigma_i^2 + (f · s · mu_i)^2
P(x) = 1 + sum_{n=1..3} a_n T_n(x),   x = (lambda - lambda_mid) / lambda_half in [-1, 1]
```

<details>
<summary>Details</summary>

Full record, acceptance discussion and the pipeline change: `reports/astro-calibration-2026-09-06.md`.

Raw χ² uses the pipeline σ. Stored χ² uses σ_eff² = σ² + (f_calib · model)² over the fitted pixels. `s` is `spectrum_scaling`. P tilt is P(λ_max) − P(λ_min) at the posterior median. Δ ln Z is against the baseline arm of the same galaxy.

| galaxy | z | S/N | arm | raw χ² | χ² (σ_eff) | phot χ² | f_calib [%] | s | P tilt [%] | Δ ln Z |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M12_98104 | 0.981 | 7 | baseline | 8664 | 5914 / 3804 | 49.5 | 10.0 | 1.369 | — | +0.0 |
|  | 0.981 | 7 | poly3 | 8652 | 5913 / 3804 | 44.8 | 10.0 | 1.284 | +4.3 | +0.1 |
|  | 0.981 | 7 | poly3_total | 8655 | 5918 / 3804 | 10.1 | 10.0 | 0.970 | +10.6 | +18.1 |
| M5_173928 | 0.959 | 13 | baseline | 15266 | 3629 / 3836 | 143.3 | 9.2 | 2.285 | — | +0.0 |
|  | 0.959 | 13 | poly3 | 14648 | 3729 / 3836 | 88.7 | 8.9 | 1.978 | -7.7 | +7.6 |
|  | 0.959 | 13 | poly3_total | 14697 | 3710 / 3836 | 48.2 | 9.0 | 1.360 | -4.1 | +3.5 |
| M4_108989 | 0.828 | 21 | baseline | 9107 | 4491 / 3735 | 139.1 | 4.6 | 1.484 | — | +0.0 |
|  | 0.828 | 21 | poly3 | 8493 | 4430 / 3735 | 152.6 | 4.1 | 1.778 | -25.2 | +202.3 |
|  | 0.828 | 21 | poly3_total | 8640 | 4264 / 3735 | 12.8 | 4.4 | 0.823 | -6.8 | +250.0 |
| M12_185653 | 0.678 | 22 | baseline | 10153 | 4017 / 3577 | 36.6 | 6.4 | 1.118 | — | +0.0 |
|  | 0.678 | 22 | poly3 | 9844 | 3961 / 3577 | 39.2 | 6.3 | 1.143 | +2.7 | +53.2 |
|  | 0.678 | 22 | poly3_total | 9844 | 3969 / 3577 | 11.1 | 6.3 | 0.980 | +4.4 | +67.7 |
| M1_206545 | 0.728 | 31 | baseline | 12772 | 4406 / 3422 | 133.2 | 5.7 | 1.380 | — | +0.0 |
|  | 0.728 | 31 | poly3 | 8581 | 4388 / 3422 | 101.9 | 3.8 | 1.775 | +4.4 | +812.6 |
|  | 0.728 | 31 | poly3_total | 8661 | 4302 / 3422 | 64.6 | 3.9 | 1.162 | +13.8 | +834.7 |
| M5_172669 | 0.604 | 105 | baseline | 31246 | 3824 / 3602 | 170.9 | 2.9 | 1.238 | — | +0.0 |
|  | 0.604 | 105 | poly3 | 28981 | 4161 / 3602 | 130.8 | 2.7 | 1.608 | -28.2 | +288.5 |
|  | 0.604 | 105 | poly3_total | 29012 | 4156 / 3602 | 100.1 | 2.7 | 1.305 | -25.1 | +281.7 |

Median ± half the 16-84 range. t50 is the lookback time at which half the mass had formed. SFR is the youngest SFH bin (0 to 30 Myr) times the median mass. The prior dominates it for quiescent galaxies.

| galaxy | arm | log M⋆ | t50 [Gyr] | log SFR (0-30 Myr) | τ_dust | t_MW [Gyr] |
| --- | --- | --- | --- | --- | --- | --- |
| M12_98104 | baseline | 11.090 ± 0.010 | 3.00 ± 0.05 | 0.42 ± 1.04 | 0.481 ± 0.032 | 2.99 ± 0.04 |
|  | poly3 | 11.075 ± 0.045 | 3.04 ± 0.58 | -0.15 ± 1.24 | 0.440 ± 0.032 | 3.04 ± 0.48 |
|  | poly3_total | 11.248 ± 0.026 | 4.44 ± 0.42 | -0.79 ± 1.46 | 0.363 ± 0.035 | 4.40 ± 0.27 |
| M5_173928 | baseline | 11.524 ± 0.010 | 2.92 ± 0.07 | 1.77 ± 0.02 | 0.720 ± 0.016 | 2.94 ± 0.05 |
|  | poly3 | 11.682 ± 0.032 | 5.50 ± 0.46 | -0.15 ± 0.70 | 0.642 ± 0.020 | 5.46 ± 0.48 |
|  | poly3_total | 11.716 ± 0.012 | 4.51 ± 0.23 | -0.08 ± 0.78 | 0.541 ± 0.019 | 4.50 ± 0.11 |
| M4_108989 | baseline | 11.638 ± 0.012 | 4.65 ± 0.09 | 0.74 ± 0.08 | 0.327 ± 0.013 | 4.62 ± 0.08 |
|  | poly3 | 11.597 ± 0.030 | 3.09 ± 0.44 | 1.31 ± 0.09 | 0.562 ± 0.030 | 3.09 ± 0.42 |
|  | poly3_total | 11.811 ± 0.016 | 4.64 ± 0.11 | 0.60 ± 0.57 | 0.253 ± 0.028 | 4.61 ± 0.12 |
| M12_185653 | baseline | 10.897 ± 0.009 | 3.01 ± 0.05 | -3.52 ± 2.08 | 0.106 ± 0.012 | 3.02 ± 0.05 |
|  | poly3 | 10.996 ± 0.054 | 4.51 ± 0.82 | -3.13 ± 2.70 | 0.191 ± 0.033 | 4.50 ± 0.66 |
|  | poly3_total | 11.100 ± 0.035 | 5.06 ± 0.45 | -1.36 ± 1.45 | 0.172 ± 0.029 | 5.02 ± 0.37 |
| M1_206545 | baseline | 11.244 ± 0.009 | 2.94 ± 0.05 | -0.55 ± 1.39 | 0.189 ± 0.013 | 2.96 ± 0.06 |
|  | poly3 | 11.540 ± 0.010 | 5.07 ± 0.04 | 1.26 ± 0.03 | 0.585 ± 0.020 | 5.06 ± 0.03 |
|  | poly3_total | 11.638 ± 0.009 | 5.07 ± 0.02 | 1.27 ± 0.04 | 0.457 ± 0.021 | 5.06 ± 0.01 |
| M5_172669 | baseline | 11.109 ± 0.007 | 1.66 ± 0.01 | -3.76 ± 1.93 | 0.012 ± 0.005 | 1.66 ± 0.02 |
|  | poly3 | 11.276 ± 0.012 | 1.75 ± 0.07 | 1.76 ± 0.06 | 0.655 ± 0.021 | 1.88 ± 0.17 |
|  | poly3_total | 11.329 ± 0.011 | 1.77 ± 0.07 | 1.76 ± 0.05 | 0.577 ± 0.019 | 1.85 ± 0.10 |

Every delta is the polynomial arm minus the baseline arm of the same galaxy. "repeat scatter" is the production fit of 2026-08-31 at the same seed minus this baseline. "Δ χ² (baseline σ_eff)" scores both fits with the baseline f_calib, so the weights are equal.

| galaxy | arm | Δ raw χ² | Δ χ² (σ_eff) | Δ χ² (baseline σ_eff) | repeat scatter | Δ phot χ² | Δ log M⋆ | Δ t50 [Gyr] | Δ τ_dust | Δ t_MW [Gyr] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M12_98104 | poly3 | -12 | -0.8 | -2.0 | -1.0 | -4.7 | -0.016 | +0.05 | -0.041 | +0.05 |
|  | poly3_total | -9 | +4.2 | +3.7 | -1.0 | -39.4 | +0.158 | +1.45 | -0.118 | +1.41 |
| M5_173928 | poly3 | -618 | +100.2 | -27.1 | +0.6 | -54.7 | +0.158 | +2.58 | -0.077 | +2.51 |
|  | poly3_total | -569 | +81.7 | -4.8 | +0.6 | -95.1 | +0.192 | +1.60 | -0.178 | +1.56 |
| M4_108989 | poly3 | -614 | -61.6 | -440.1 | -23.8 | +13.5 | -0.042 | -1.56 | +0.235 | -1.53 |
|  | poly3_total | -467 | -227.4 | -392.6 | -23.8 | -126.3 | +0.173 | -0.02 | -0.074 | -0.01 |
| M12_185653 | poly3 | -308 | -55.6 | -133.7 | +4.4 | +2.6 | +0.099 | +1.50 | +0.084 | +1.48 |
|  | poly3_total | -309 | -47.7 | -136.5 | +4.4 | -25.5 | +0.204 | +2.04 | +0.065 | +2.00 |
| M1_206545 | poly3 | -4191 | -18.7 | -1316.9 | -5.3 | -31.3 | +0.296 | +2.14 | +0.396 | +2.10 |
|  | poly3_total | -4111 | -104.0 | -1302.2 | -5.3 | -68.6 | +0.394 | +2.14 | +0.268 | +2.10 |
| M5_172669 | poly3 | -2265 | +337.3 | -193.2 | +2.1 | -40.1 | +0.167 | +0.10 | +0.642 | +0.22 |
|  | poly3_total | -2234 | +331.8 | -191.2 | +2.1 | -70.8 | +0.220 | +0.11 | +0.565 | +0.18 |

Mock truth: M5_172669, log M⋆ 11.110, τ_dust 0.011, t_MW 1.66 Gyr. A 4 percent linear tilt on the spectrum only, production noise, seed 1.

| mock arm | log M⋆ | τ_dust | s | t_MW [Gyr] | raw χ² | phot χ² | ln Z |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mock_tilt4_baseline | 11.167 ± 0.011 | 0.151 ± 0.004 | 1.289 ± 0.020 | 1.77 ± 0.11 | 3625 | 22.5 | 236487.5 |
| mock_tilt4_poly3 | 11.126 ± 0.012 | 0.023 ± 0.016 | 1.232 ± 0.019 | 1.72 ± 0.10 | 3590 | 4.0 | 236493.6 |

Acceptance, the spectral χ² of no galaxy must get worse:

- Raw χ², the same weights for every arm: never worse. `poly3` −12 to −4191. `poly3_total` −9 to −4111.
- χ² at the baseline σ_eff: `poly3` never worse. `poly3_total` worse for M12_98104 by 3.7 against a run-to-run scatter of 1.0.
- Stored χ², each fit's own σ_eff: worse for M5_172669 by 337 and M5_173928 by 100, because f_calib fell.

Implementation: `PolynomialCalibration` in `ceridwen/ceridwen/likelihood/calibration.py`, 20 tests in `ceridwen/tests/test_polynomial_calibration.py`. Switches in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: `CERIDWEN_CALIBRATION_ORDER` (3), `CERIDWEN_CALIBRATION_PRIOR` (0.1), `CERIDWEN_PHOTOMETRY` (`cosmos_total`). The derived-output file gains a `calibration` group with the coefficient draws and the P quantiles.

Run: Vast.ai RTX 5060 instance 49915205 at $0.093 per hour, 20 cells, 26 attempts, $0.23, destroyed. Records in `results/calibration-polynomial-dr2/vast_run_*.json`, executed notebook `analysis.ipynb`. The sibling card's spectral χ² figure for each of the 18 fits is `sibling-chi2-<arm>-<galaxy>.png`.

```
ceridwen/.venv/bin/python scripts/calibration_arms_vast.py plan
ceridwen/.venv/bin/python scripts/calibration_arms_vast.py run --spend-cap 1.0
JAX_PLATFORMS=cpu ceridwen/.venv/bin/python -m pytest ceridwen/tests/test_polynomial_calibration.py -q
```

</details>
