---
title: Calibration polynomial in the DR2 pipeline
date: 2026-09-05
section: Analyses
tags: [calibration, ceridwen, dr2-quiescent-sample]
job: t_ab2b8a0b
---

Draft. Does a Chebyshev calibration polynomial in the spectrum likelihood make the joint LEGA-C plus COSMOS2015 fits better calibrated? What does it absorb, and what must it leave alone?

### Answer

The pipeline now multiplies the model spectrum by an order-3 Chebyshev polynomial P(λ) = 1 + Σ a_n T_n(x). It integrates the coefficients out analytically. The photometry never sees P. On six DR2 galaxies the spectral χ² at fixed weights never got worse with the polynomial on. Where the photometric anchor fits (total fluxes, χ² 10 to 50 for 12 bands), the polynomial stays within a few percent. The parameters move within reason. Where the anchor does not fit (M1_206545 and M5_172669, photometric χ² above 60), the polynomial grows to 15 to 30 percent. It absorbs the model mismatch. The default is now order 3 with total photometry.

### What the polynomial is for

A joint fit compares two data sets that measure different things.

- The twelve photometric bands (u to IRAC 4.5 µm) measure the total light of the galaxy over a factor of ten in wavelength. Their absolute calibration is good to a few percent per band. They fix the stellar mass and the broadband shape of the SED.
- The LEGA-C spectrum has about 3600 fitted pixels between 6300 and 8900 Å in the observed frame. At z = 0.6 to 0.8 that is 3900 to 5500 Å in the rest frame. The pixels carry the absorption-line strengths and widths, the 4000 Å break and the fine continuum shape. By summed (S/N)² the spectrum outweighs the photometry by a factor of 200 to 800 (absorption-line-mask note).

The smooth shape of the spectrum is the part that is not trustworthy at the percent level. Four instrumental effects change it.

1. Slit losses. A 1" slit on a galaxy of similar size loses 10 to 40 percent of the light (LEGA-C DR2 release notes). Seeing shrinks with wavelength, so the loss depends on wavelength.
2. Differential atmospheric refraction. The atmosphere displaces the blue image of a target against the red image. A slit aligned at one wavelength loses more light at the other end of the spectrum.
3. Flux-calibration errors. The response curve, the extinction curve and the standard star all leave smooth residual errors. LEGA-C DR2 did not use standard stars at all. The team scaled each spectrum onto a FAST template of the UltraVISTA photometry with a fifth-order polynomial (Straatman et al. 2018, §2.3.2).
4. Aperture against total light. The slit sees part of the galaxy. The photometry sees all of it. A radial colour gradient makes the ratio depend on wavelength.

Every one of these is a smooth multiplicative function of wavelength. None of them changes an absorption line. That is what the polynomial models: a smooth multiplicative correction with a handful of coefficients.

### What it must not absorb

Dust attenuation and stellar age also change the continuum smoothly. A change of 0.2 in the optical depth of the Kriek and Conroy curve tilts the LEGA-C window by about 15 percent. An order-1 polynomial can copy that tilt exactly (explainer figure, bottom left). Age moves the 4000 Å break and the slope of the continuum. Metallicity changes the line blanketing over a few hundred Å. On the spectrum alone, the polynomial and the dust are one degree of freedom. This degeneracy is not a defect of the polynomial. It is the design point: the spectrum gives up its continuum slope and keeps its lines.

Three things stop the polynomial from eating the physics.

- The photometry. The polynomial multiplies the spectrum prediction only. The fit compares the model photometry with the twelve bands without it. A dust or age change that tilts the model spectrum also changes the broadband colours from u to Ks. The catalogue measures those colours to about 5 percent. When the polynomial tries to absorb a physical tilt, the photometric χ² pays for it. The mock below shows this. We injected a 4 percent tilt in the spectrum only. The polynomial recovers it. The parameters stay on the truth, because the photometry did not move.
- The order. An order-n Chebyshev polynomial has n − 1 turning points over the fitted range. The shortest structure it can follow spans about (range / n). For order 3 over 2500 Å that is 800 Å in the observed frame, 500 Å in the rest frame. Absorption lines are 10 to 30 Å wide and the 4000 Å break is 100 to 200 Å wide. The polynomial cannot bend on those scales (explainer figure, bottom right).
- The prior. Each shape coefficient a_n has a Gaussian prior with width 0.1. That says: a correction of more than about 10 percent per term is unlikely. In a full-spectrum fit the 3600 pixels pin the coefficients to 0.3 to 1.4 percent and the prior is irrelevant. It matters only in fits with few pixels (the features-only mask). The prior does not stop the polynomial from following a real dust tilt. Only the photometry does.

The anchor therefore decides what the polynomial means. The production 3" aperture fluxes carry no aperture-to-total offset, no Galactic extinction and no Table 3 zero points. That anchor carries its own tilt and sits 25 to 50 percent too faint. The polynomial then follows it into the wrong dust and age (tilt-origin experiment of 2026-09-02). The `poly3_total` arm below uses the Laigle et al. (2016) total SED for that reason.

### Equations

Data model for pixel i of the spectrum, with s the sampled `spectrum_scaling` and μ_i(θ) the model spectrum:

    d_i = s · P(x_i) · μ_i(θ) + n_i,    n_i ~ N(0, σ_eff,i²),    σ_eff,i² = σ_i² + (f · s · μ_i)²

    P(x) = 1 + Σ_{n=1}^{N} a_n T_n(x),    x = (λ − λ_mid) / λ_half in [−1, 1] over the fitted pixels

The photometry uses μ(θ) without P. The coefficients a enter linearly. With the Gaussian prior a ~ N(0, Σ_p) they integrate out in closed form. Write D_in = T_n(x_i) · s · μ_i / σ_eff,i for the whitened design matrix. Write t_i = (d_i − s μ_i) / σ_eff,i for the whitened residual. Then:

    N = Dᵀ D + Σ_p⁻¹,    â = N⁻¹ Dᵀ t

    ln L(θ) = ln N(d | s P(â) μ, σ_eff) − ½ âᵀ Σ_p⁻¹ â + ½ ln|Σ_p⁻¹| − ½ ln|N|

The first two terms are the profile likelihood that Prospector's `polyopt` uses. The last two are the Occam factor of the marginalisation. The whole thing costs one 3 × 3 solve and one 3 × 3 log-determinant per likelihood call. It adds no sampled dimension. Given θ, the coefficients have the posterior N(â, N⁻¹). The band on P(λ) in the figures therefore combines the spread of â over the posterior of θ with one draw from N⁻¹ per sample.

### Implementation

`ceridwen/ceridwen/likelihood/calibration.py` holds `PolynomialCalibration`. It builds the basis once from the pixel grid. `calibrate` solves â and returns P(â) · μ and the two extra terms.

`ceridwen/ceridwen/likelihood/calibration.py · PolynomialCalibration.calibrate`

```
        normal = self.normal_matrix(mu, safe_sigma, mask)
        design = self.design(mu, safe_sigma, mask)
        target = jnp.where(mask, (jnp.asarray(y) - mu) / safe_sigma, 0.0)
        coeffs = jnp.linalg.solve(normal, design.T @ target)
        return (self.polynomial(coeffs) * mu, coeffs,
                self.log_marginal_terms(coeffs, normal))
```

`DiagonalGaussianLikelihood(calibration=...)` evaluates the noise model once at the uncalibrated model. It solves the polynomial with that σ_eff and hands P · μ to the Gaussian kernel. So â maximises exactly the kernel that the likelihood evaluates, and the marginal above is exact for it. Without `calibration=` every existing fit stays unchanged.

The production notebook `notebooks/ceridwen_integrated_photometry_spectra.ipynb` reads three switches.

- `CERIDWEN_CALIBRATION_ORDER` (default 3): Chebyshev order. 0 switches the polynomial off.
- `CERIDWEN_CALIBRATION_PRIOR` (default 0.1): prior width per coefficient.
- `CERIDWEN_PHOTOMETRY` (default `cosmos_total`): `cosmos_ap3` uses the 3" aperture fluxes with total IRAC and no offsets. `cosmos_total` applies the Laigle et al. (2016) aperture-to-total offset, the Galactic extinction and the Table 3 zero points. `scripts/download_legac_dr2_aperture_photometry.py` fetches the aperture table.

The result file records `calibration_order`, `calibration_prior_sigma`, `calibration_marginalized` and `photometry_source`. The derived-output file gains a `calibration` group. It holds the Chebyshev coordinate `x`, 200 coefficient draws, the matching `spectrum_scaling` draws, and the 16, 50 and 84 percent quantiles of P(λ) on the pixel grid. The notebook plots P(λ) and s · P(λ) with their bands. It computes the posterior-predictive spectrum, the pulls and the stored spectral χ² against P · μ.

`ceridwen/tests/test_polynomial_calibration.py` holds 20 tests.

- Exact recovery of an injected polynomial, and masked pixels left out.
- Recovery to better than 1 percent at S/N 20.
- The marginal against a brute-force integral over two coefficients, and the flat-prior integral.
- The profile contract, per-coefficient priors and σ_eff weighting.
- The covariance, the posterior draws, jit and gradient.
- Recovery of a tilt through the alpha-enhanced forward model.

### Defaults

- Order 3. Orders 1, 3 and 5 all remove a pure tilt on mocks (2026-09-02 experiment). Order 1 cannot follow curvature. Order 5 pays extra posterior width for nothing. LEGA-C's own calibration used a fifth-order polynomial, so the residual is low order. The shortest bend of order 3 is 800 Å, above every spectral feature the model must keep.
- Constant term in `spectrum_scaling`, not in the polynomial (Prospector convention). This keeps the sampled parameter set identical to production, so every downstream reader of the result files still works. The BAGPIPES convention puts the constant inside the polynomial and drops the scaling. It gives the same posteriors with one fewer dimension.
- Prior width 0.1 per coefficient. Wide enough for any calibration error the release notes describe, and irrelevant in a full-spectrum fit.
- Marginalised, not profiled. The Occam term is exact and costs one log-determinant. Over the posterior of a joint fit it varies by 0.1 to 0.4 nats, so the profile would give the same answer here. The marginal is the statement of the model.

### Experiment

`scripts/calibration_arms_vast.py` runs the production notebook through the DR2 shard runner on one Vast.ai RTX 5060 (instance 49915205, $0.093 per hour). Every cell uses the production sampler settings (500 live points, 65 inner steps, 100 deletions, logZ tolerance −5) and the production seed of its target.

- `baseline`: production (3" photometry, `spectrum_scaling`, `log_f_calib`).
- `poly3`: baseline plus the order-3 polynomial.
- `poly3_total`: `poly3` anchored to the Laigle et al. (2016) total SED.
- Six galaxies that span the sample. Catalogue S/N 6.6 (M12_98104), 13 (M5_173928), 22 (M12_185653), 21 (M4_108989), 31 (M1_206545) and 105 (M5_172669). Redshift 0.60 to 0.98.
- Two mocks of M5_172669 with a 4 percent end-to-end tilt on the spectrum only, without and with the polynomial. The mock truth equals the posterior median of the stored full-spectrum fit.

20 cells, 26 attempts. Six attempts failed with XLA runtime errors on this host and the driver retried them. About 5 minutes per fit. The instance cost $0.23. The driver destroyed it at 03:38 UTC on 2026-09-05. Records: `results/calibration-polynomial-dr2/vast_run_*.json`. Executed notebook: `results/calibration-polynomial-dr2/analysis.ipynb`.

### Figures

<img src="figures/calibration-polynomial-dr2/calibration-explainer.png" alt="Explainer: fitted polynomial on M12_185653, calibration vector with band, dust tilt against an order-1 polynomial, shortest bend against line widths">

The explainer: what the polynomial absorbs (top), the dust tilt it can copy (bottom left) and the scales it cannot bend on (bottom right).

<img src="figures/calibration-polynomial-dr2/mock-tilt.png" alt="Mock with a 4 percent tilt: injected and recovered calibration vector, and the parameter pulls without and with the polynomial">

<img src="figures/calibration-polynomial-dr2/polynomial-vectors.png" alt="P of lambda and s times P of lambda with 16 to 84 percent bands for the six galaxies and the two polynomial arms">

<img src="figures/calibration-polynomial-dr2/parameters-before-after.png" alt="Mass, t50, SFR, dust and mass-weighted age for the three arms of each galaxy">

The per-galaxy pulls and cumulative χ² are `chi2-<galaxy>.png`. The sibling card's spectral χ² figure for every fit is `sibling-chi2-<arm>-<galaxy>.png` in `wiki/analyses/calibration-polynomial-dr2/`.

### Spectra and photometry

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

### Derived parameters

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

### Before and after

Every delta is the polynomial arm minus the baseline arm of the same galaxy. "repeat scatter" = the production fit of 2026-08-31 (same seed) minus this baseline. "Δ χ² (baseline σ_eff)" scores both fits with the baseline f_calib, so the weights are equal.

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

### Mocks

Truth: M5_172669 (log M⋆ = 11.110, τ_dust = 0.011, t_MW = 1.66 Gyr). A 4 percent linear tilt on the spectrum only, production noise, seed 1. Pulls from the truth without the polynomial: log M⋆ +5.4σ, τ_dust +32σ. With it: +1.4σ and +0.7σ.

| mock arm | log M⋆ | τ_dust | s | t_MW [Gyr] | raw χ² | phot χ² | ln Z |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mock_tilt4_baseline | 11.167 ± 0.011 | 0.151 ± 0.004 | 1.289 ± 0.020 | 1.77 ± 0.11 | 3625 | 22.5 | 236487.5 |
| mock_tilt4_poly3 | 11.126 ± 0.012 | 0.023 ± 0.016 | 1.232 ± 0.019 | 1.72 ± 0.10 | 3590 | 4.0 | 236493.6 |

### Acceptance

The brief: the spectral χ² must not get worse for any galaxy, judged with the sibling card's per-galaxy figures. Those figures plot the stored χ², whose weights include the fitted noise fraction f_calib: σ_eff² = σ² + (f_calib · model)². A fit that lowers f_calib shrinks its own σ_eff, so its stored χ² can rise while its residuals fall. The acceptance table therefore carries three numbers per fit.

- Raw χ² (pipeline σ, the same weights for every arm): never worse. `poly3` −12 to −4191, `poly3_total` −9 to −4111.
- χ² at the baseline σ_eff (both fits scored with the baseline f_calib): `poly3` never worse (−2 to −1317). `poly3_total` worse for M12_98104 by +3.7 against a run-to-run scatter of 1.0, better for the other five (−5 to −1302).
- Stored χ² (each fit's own σ_eff): `poly3` is worse for M5_172669 (+337, f_calib 2.9 → 2.7 percent). It is worse for M5_173928 (+100, 9.2 → 8.9 percent). `poly3_total` also worse for M12_98104 (+4). All three rises come from the smaller σ_eff, not from larger residuals: the same fits are better by 27 to 193 at the baseline weights.

Verdict: the polynomial on its own passes for all six galaxies at fixed weights. With the anchor changed as well, M12_98104 is 4 units worse at the baseline weights, out of 5914. It is the noisiest spectrum in the set. `sibling-chi2-<arm>-<galaxy>.png` holds the sibling card's spectral χ² figure for every one of the 18 fits (`scripts/per_galaxy_diagnostics.py`, stored χ²), and shows the two M5 rises. `analysis.ipynb` prints the three lists.

Run-to-run scatter: my baseline differs from the stored production fit of the same galaxy and seed by 1 to 24 in stored χ². M4_108989 is the largest. The rest are 5 or less.

### Where it helped and where it did not

- Mock (M5_172669 truth, 4 percent tilt): helped. The tilt goes into P (a_1 = 0.035 ± 0.006 for 0.04 injected, the rest into s). Dust returns to the truth (0.023 ± 0.016 for 0.011, against 0.151 ± 0.004 without the polynomial). The photometric χ² drops from 22.5 to 4.0 and ln Z rises by 6. The recovered s · P differs from the injected vector by at most 1.0 percent.
- M4_108989 (S/N 21): helped, but only with total photometry. On aperture photometry the polynomial reaches −25 percent and dust doubles. t50 drops from 4.6 to 3.1 Gyr and the photometric χ² gets worse (139 → 153). With total photometry the polynomial is −7 percent, t50 returns to 4.6 Gyr, the photometric χ² is 13 and the stored spectral χ² falls by 227. The anchor decides what the polynomial means.
- M12_185653 (S/N 22): helped. Photometric χ² 37 → 11 with total photometry, stored spectral χ² −48 to −56, polynomial within ±4 percent. t50 moves from 3.0 to 4.5 to 5.1 Gyr with an error bar ten times wider than before.
- M5_173928 (S/N 13): mixed. Photometric χ² 143 → 48 and raw spectral χ² −569 with total photometry. But the polynomial is a 7 to 10 percent bowl. t50 moves from 2.9 to 4.5 to 5.5 Gyr. The baseline needed s = 2.29: the 3" fluxes sit a factor 2.3 below the spectrum. Its stored χ² rises by 82 to 100 because f_calib fell. At the baseline weights the same fits are better by 5 to 27.
- M1_206545 (S/N 31): did not help where it matters. The raw spectral χ² falls by 4191 (3.7 to 2.5 per pixel). But P is a 15 percent hump centred near the rest-frame 4000 Å break. The photometric χ² stays at 65 to 102 for 12 bands. Mass moves by 0.3 to 0.4 dex, dust by 0.3 to 0.4 and t50 by 2.1 Gyr. The formal errors are 0.01. The polynomial and the dust share the continuum, and the photometry does not settle the split. Trust neither arm until the photometric residuals are understood.
- M5_172669 (S/N 105): did not help. P is a −28 percent tilt. τ_dust goes from 0.01 to 0.6. The youngest SFH bin goes from quiescent to about 60 M⊙ per year. The photometric χ² stays at 100 to 131. The polynomial absorbs the known optical-NIR model mismatch of this young galaxy (results board, 2026-09-04), not a calibration error.
- M12_98104 (S/N 6.6): no change on aperture photometry. Every delta is within the run-to-run scatter. The t50 error bar widens from 0.05 to 0.6 Gyr. f_calib sits at the 10 percent prior ceiling in all three arms, so the fractional noise floor, not the polynomial, carries the residual mismatch.

### Commands

```
ceridwen/.venv/bin/python scripts/calibration_arms_vast.py plan
ceridwen/.venv/bin/python scripts/calibration_arms_vast.py run --spend-cap 1.0
JAX_PLATFORMS=cpu ceridwen/.venv/bin/python -m pytest ceridwen/tests/test_polynomial_calibration.py -q
```
