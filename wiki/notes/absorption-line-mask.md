---
title: Absorption-line pixel mask
date: 2026-09-02
section: Analyses
tags: [absorption-mask, ceridwen]
job: t_8f62974f
old: _old/analyses/absorption-line-mask.html
---

Draft. Does fitting only the absorption-feature pixels of a LEGA-C spectrum, so that the photometry carries more weight, improve the accuracy of a Ceridwen fit?

### Answer

**No.** Fitting only the absorption-feature pixels, or keeping every pixel and inflating the continuum errors until the continuum carries no more weight than the photometry, does not make the recovered mass, age, metallicity or dust more accurate. It costs precision and, on real spectra, moves the answers by many sigma.

- **Weight.** The spectrum outweighs the twelve bands by a factor of 220 to 760 in summed (S/N)2 once the fitted 3 percent calibration floor is included, and the photometry's share of the Fisher information stays below one percent with or without the mask. No pixel selection makes the photometry matter.
- **Mocks.** A 3 percent linear continuum tilt biases tMW by +0.16 Gyr (full spectrum), +0.12 Gyr (features only) and +0.16 Gyr (down-weighted) at the native S/N; log M⋆ by +0.051, +0.049 and +0.050 dex; τdust by +0.11, +0.10 and +0.10. The masked modes are as biased as the full fit, and their posteriors are 0.9 to 1.6 times as wide (medians per parameter and S/N scale; single realisations range from 0.5 to 2.4).
- **Real targets.** On M5_172669, M9_232005 and M11_214430 the masked posteriors sit up to 22 full-spectrum sigma away from the full-spectrum ones (M9 age 3.0 → 4.3 Gyr, M5 log Z -1.72 → -1.97, [α/Fe] 0.13 → 0.36). The continuum and the features do not agree under the current model, and the mock test cannot say which side is right.
- **Cost.** The masked fits take 90% (features only) and 87% (down-weighted) of the full-spectrum sampler wall time, a saving too small to buy back the lost precision.
- **Recommendation.** Keep the option off by default (`CERIDWEN_SPECTRUM_PIXELS=all`). Use `features` as a diagnostic: a many-sigma shift flags a spectrum whose continuum shape the model cannot reproduce. Tilt-shaped calibration errors need a multiplicative calibration polynomial or continuum-normalised indices, not a pixel mask.

### How the current likelihood weighs spectrum against photometry

The joint log-likelihood is the plain sum of one diagonal Gaussian per data set (`ceridwen/ceridwen/likelihood/likelihood.py:840-875`, `MultiObservationLikelihood.__call__`). No term rebalances the two. Photometry uses the catalogue error with a 5 percent floor in quadrature (`notebooks/ceridwen_integrated_photometry_spectra.ipynb`, heading "Photometric observation", `PHOTOMETRY_FLOOR`). The spectrum uses `DiagonalNoiseModel(use_fractional=True)`, so its per-pixel variance is `sigma^2 + (f_calib * mu)^2` with `log_f_calib` a fitted parameter, uniform between 1 and 10 percent (`ceridwen/ceridwen/likelihood/noise_model.py:283-369`). A free scalar `spectrum_scaling` multiplies the model spectrum only (`ceridwen/ceridwen/csp/csp.py:1351-1362`), so the spectrum constrains shape and the photometry alone fixes the absolute flux.

For a diagonal Gaussian the information on a pure amplitude is the sum of (S/N)2. That sum, over the fitted pixels against the twelve bands, is the weight ratio for anything that moves the flux level:

Weight budget of the current likelihood. Feature pixels are those inside the absorption windows defined below. The balance factor is the sigma inflation of the continuum pixels that equalises the continuum and photometry budgets.

| Target | z | Fitted pixels | Median pixel S/N | Photometry sum (S/N)2 | Spectrum / photometry, raw | Spectrum / photometry, fcalib = 3% | Feature pixels | Balance factor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M5_172669 | 0.604 | 3,602 | 106 | 4,654 | 8,090 | 756 | 1,389 (39%) | 71 |
| M9_232005 | 0.611 | 3,494 | 29 | 3,961 | 757 | 390 | 1,521 (44%) | 21 |
| M11_214430 | 0.891 | 3,810 | 15 | 3,776 | 308 | 220 | 1,088 (29%) | 14 |

Twelve bands at S/N 20 cannot compete with thousands of pixels at S/N 15 to 100 by count. Keeping only the feature pixels removes 56 to 71 percent of the pixels and leaves the ratio between 80 and 3,000. The mask therefore cannot rebalance the two data sets; what it does is remove the continuum shape from the spectrum, which is the information a multiplicative calibration error corrupts.

A sum of (S/N)2 only measures amplitude information. The Fisher matrix of the notebook model at the mock truth (Jacobians of the predicted photometry and spectrum, the notebook noise model with fcalib = 2.9 percent, and the prior curvature added as a diagonal) splits the information per parameter and forecasts the marginal posterior width of a photometry-only, spectrum-only, and joint fit in every pixel mode. For M5_172669:

Fisher forecast for M5_172669 at the mock truth. "Spectrum share" is the spectrum's fraction of the diagonal information; widths are 1-sigma Laplace forecasts. The down-weighted mode (factor 71) is indistinguishable from features-only to three digits because a factor 71 leaves the continuum 1/5000 of its weight. `results/absorption-mask/fisher_M5_172669.json`.

| Parameter | Spectrum share, full | Spectrum share, features | Width, photometry only | Width, spectrum only | Width, joint full | Width, joint features | Prior width |
| --- | --- | --- | --- | --- | --- | --- | --- |
| log Z | 0.997 | 0.992 | 0.25 | 0.015 | 0.015 | 0.023 | 0.87 |
| [α/Fe] | 0.998 | 0.994 | 0.17 | 0.016 | 0.015 | 0.021 | 0.23 |
| τdust | 0.997 | 0.993 | 0.099 | 0.0057 | 0.0056 | 0.0080 | 0.58 |
| log M⋆ | 0.999 | 0.997 | 0.012 | 0.105 | 0.0071 | 0.0077 | 1.44 |
| spectrum scaling | 1.000 | 1.000 | 0.30 | 0.30 | 0.019 | 0.019 | 0.30 |

Two readings. First, the photometry's share of the raw information is below one percent for every parameter, and the feature mask leaves it below one percent, so no pixel selection makes the twelve bands "carry weight" by count. Second, the photometry matters through degeneracy breaking, not weight: a spectrum with a free scaling cannot fix the stellar mass (spectrum-only width 0.105 dex against 0.012 dex from photometry alone), so the mass is photometric in every mode, and the scaling is only determined once both are present. For metallicity, [α/Fe] and dust the spectrum sets the width, and the feature mask costs a factor 1.3 to 1.5 in forecast width. The SFH ratios are prior- and degeneracy-dominated in this linear forecast and are omitted from the table. Project synthesis: the only way the mask can improve accuracy is by removing continuum-shape information that a calibration error has corrupted; the mocks below test that.

Source: `scripts/absorption_mask_analysis.py budget --features` and `fisher`; catalogue S/N percentiles of the 187-object passive sample are 8, 13, 22, 31 and 39 at the 10th to 90th percentile, so M5_172669 is the best case and M11_214430 is typical.

### The mask

`Spectrum.select_absorption_features` (`ceridwen/ceridwen/observation/spectrum.py`) builds an observed-frame pixel mask from a rest-frame, in-air feature catalogue (`ceridwen/ceridwen/observation/absorption_features.py`), converts it to vacuum with the same `air2vac` the stellar-index code uses, and redshifts it by 1 + z. Lick feature bandpasses are used where they exist; other features are line centres with a ±`window_kms` window (1000 km/s here, ±13 Å at Ca K).

- Balmer: H10, H9, H8 (centres), HdA 4083.5–4122.3, HgA 4319.8–4363.5, Hβ 4847.9–4876.6, Hα (centre).
- Calcium: Ca K 3933.7 and Ca H 3968.5 (centres), Ca4227, Ca4455, and the near-infrared triplet (centres).
- Molecular and carbon: CN 4142.1–4177.1, G band 4281.4–4316.4, C2 4634.0–4720.3.
- Iron: Fe4383, Fe4531, Fe5015, Fe5270, Fe5335, Fe5406, Fe5709, Fe5782 (Lick bandpasses).
- Mg b 5160.1–5192.6, Na D 5876.9–5909.4, TiO1 5936.6–5994.1, TiO2 6189.6–6272.1.

Two modes: `drop` removes every other pixel from the likelihood (`mask &= in_feature`); `downweight` keeps every pixel but multiplies the continuum `uncertainty` by a factor. Both are edits to the observation arrays that the jitted log-posterior reads once at build time, so the compiled likelihood is unchanged. In the notebook the modes are `CERIDWEN_SPECTRUM_PIXELS=all|features|features_downweight`; the factor `CERIDWEN_FEATURE_DOWNWEIGHT` is a number or `balance` (the table above). The fitted `f_calib` term still adds in quadrature to the inflated sigma.

`ceridwen/ceridwen/observation/spectrum.py · Spectrum.select_absorption_features`

```
        if mode == "drop":
            new_mask = np.asarray(self.mask) & in_feature
            if not new_mask.any():
                raise ValueError(
                    "select_absorption_features: no fitted pixels fall inside "
                    "an absorption-feature window at this redshift"
                )
            self.mask = jnp.asarray(new_mask)
        else:
            factor = np.where(in_feature, 1.0, float(downweight))
            self.uncertainty = self.uncertainty * jnp.asarray(factor)`
```

<figure>
<img src="figures/absorption-mask/feature_windows_M5_172669.png" alt="Observed-frame spectrum of M5_172669 with the pixels inside absorption-feature windows highlighted">
<figcaption>Pixels of M5_172669 kept by the feature mask (orange) against every fitted pixel (grey).</figcaption>
</figure>

Tests: `ceridwen/tests/test_absorption_features.py` (vacuum and redshift of the windows, mask membership, drop and down-weight arithmetic including the chi-squared scaling, error paths).

### Experiment

Every fit is the production notebook run through the DR2 shard-runner worker (`scripts/absorption_mask_grid.py`): BlackJAX NSS with 500 live points, 65 inner steps, 100 deletions, logZ tolerance −5, the schema-2.1 C3K alpha-enhanced grid, seven-bin step SFH, constant metallicity, [α/Fe], diffuse dust with fixed slope, fixed redshift and dispersion, fitted `log_f_calib` and `spectrum_scaling`. One comparison group is one target or one mock realisation fitted in all three pixel modes on the same GPU boot.

- Mocks: the truth is the weighted posterior median of the stored full-spectrum fit of M5_172669 (`results/absorption-mask/truth_M5_172669.json`). The mock keeps the real pixel grid, per-pixel errors, masks and filters; the spectrum is the model prediction times a linear continuum tilt from 1 − ε to 1 + ε across the fitted range plus Gaussian noise; the photometry is the prediction plus Gaussian noise. ε ∈ {0, 0.03, 0.06}; per-pixel errors × {1, 4} (S/N ≈ 106 and 26); two noise realisations each; 36 fits.
- Real targets: M5_172669, M9_232005, M11_214430 in the three modes; 9 fits.
- Hardware: five Vast.ai Blackwell instances (RTX 5060, RTX 5070), one fit per GPU, comparison groups never split across boots.

All 45 fits passed the DR2 diagnostics (45/45 finite evidence and ESS ≥ 200; lowest ESS 2970). Median sampler wall time: 214 s full spectrum, 193 s features only, 186 s down-weighted. Total Vast.ai spend for the job, including failed launches and the notebook re-run, was $2.24. One mock cell (tilt 0.03, S/N 0.25, seed 1, down-weighted) needed two extra single-cell re-runs: its first executed notebook was truncated by a GPU out-of-memory error after the fit, and the second attempt died in a CUDA illegal-address fault; the third attempt is the one recorded.

| cell | mode | pixels | ESS | calls | sampler wall [s] | ln Z | spec chi2/pixel | phot chi2/band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mock_tilt0.00_snr0.25_seed1_all | all | 3602 | 3085 | 1,072,500 | 232 | 231918.0 ± 0.19 | 0.91 | 1.12 |
| mock_tilt0.00_snr0.25_seed1_features | features | 1389 | 3064 | 1,020,500 | 193 | 89702.3 ± 0.23 | 0.90 | 1.15 |
| mock_tilt0.00_snr0.25_seed1_features_downweight | features_downweight | 3602 | 3139 | 1,014,000 | 193 | 226595.4 ± 0.25 | 0.35 | 1.14 |
| mock_tilt0.00_snr0.25_seed2_all | all | 3602 | 3038 | 1,105,000 | 150 | 231920.0 ± 0.31 | 0.91 | 0.57 |
| mock_tilt0.00_snr0.25_seed2_features | features | 1389 | 2970 | 1,020,500 | 186 | 89693.6 ± 0.23 | 0.92 | 0.62 |
| mock_tilt0.00_snr0.25_seed2_features_downweight | features_downweight | 3602 | 3105 | 1,040,000 | 139 | 226583.8 ± 0.22 | 0.36 | 0.61 |
| mock_tilt0.00_snr1.00_seed1_all | all | 3602 | 3176 | 1,365,000 | 217 | 236513.8 ± 0.40 | 0.50 | 1.00 |
| mock_tilt0.00_snr1.00_seed1_features | features | 1389 | 3157 | 1,261,000 | 195 | 91449.3 ± 0.20 | 0.53 | 1.03 |
| mock_tilt0.00_snr1.00_seed1_features_downweight | features_downweight | 3602 | 3097 | 1,306,500 | 208 | 228314.3 ± 0.28 | 0.20 | 1.02 |
| mock_tilt0.00_snr1.00_seed2_all | all | 3602 | 3220 | 1,378,000 | 184 | 236464.7 ± 0.31 | 0.52 | 1.29 |
| mock_tilt0.00_snr1.00_seed2_features | features | 1389 | 3254 | 1,241,500 | 166 | 91451.9 ± 0.31 | 0.52 | 1.26 |
| mock_tilt0.00_snr1.00_seed2_features_downweight | features_downweight | 3602 | 3190 | 1,306,500 | 176 | 228418.7 ± 0.32 | 0.20 | 1.24 |
| mock_tilt0.03_snr0.25_seed1_all | all | 3602 | 3099 | 1,118,000 | 227 | 231882.3 ± 0.20 | 0.93 | 2.03 |
| mock_tilt0.03_snr0.25_seed1_features | features | 1389 | 3459 | 1,046,500 | 204 | 89672.5 ± 0.17 | 0.94 | 1.87 |
| mock_tilt0.03_snr0.25_seed1_features_downweight | features_downweight | 3602 | 3388 | 1,066,000 | 148 | 226546.4 ± 0.24 | 0.36 | 1.84 |
| mock_tilt0.03_snr0.25_seed2_all | all | 3602 | 3331 | 1,144,000 | 227 | 231815.0 ± 0.41 | 0.96 | 2.04 |
| mock_tilt0.03_snr0.25_seed2_features | features | 1389 | 3346 | 1,066,000 | 206 | 89657.2 ± 0.31 | 0.95 | 1.42 |
| mock_tilt0.03_snr0.25_seed2_features_downweight | features_downweight | 3602 | 3539 | 1,066,000 | 148 | 226582.0 ± 0.21 | 0.37 | 1.47 |
| mock_tilt0.03_snr1.00_seed1_all | all | 3602 | 3488 | 1,417,000 | 199 | 236461.4 ± 0.31 | 0.52 | 2.84 |
| mock_tilt0.03_snr1.00_seed1_features | features | 1389 | 3532 | 1,339,000 | 186 | 91461.1 ± 0.29 | 0.50 | 2.76 |
| mock_tilt0.03_snr1.00_seed1_features_downweight | features_downweight | 3602 | 3583 | 1,339,000 | 186 | 228377.9 ± 0.23 | 0.19 | 2.72 |
| mock_tilt0.03_snr1.00_seed2_all | all | 3602 | 3578 | 1,423,500 | 234 | 236510.4 ± 0.35 | 0.50 | 1.04 |
| mock_tilt0.03_snr1.00_seed2_features | features | 1389 | 3486 | 1,287,000 | 216 | 91465.2 ± 0.23 | 0.51 | 1.00 |
| mock_tilt0.03_snr1.00_seed2_features_downweight | features_downweight | 3602 | 3389 | 1,319,500 | 217 | 228374.1 ± 0.28 | 0.20 | 0.98 |
| mock_tilt0.06_snr0.25_seed1_all | all | 3602 | 3886 | 1,202,500 | 171 | 231856.5 ± 0.22 | 0.92 | 7.49 |
| mock_tilt0.06_snr0.25_seed1_features | features | 1389 | 3915 | 1,144,000 | 158 | 89660.2 ± 0.13 | 0.91 | 6.30 |
| mock_tilt0.06_snr0.25_seed1_features_downweight | features_downweight | 3602 | 3515 | 1,118,000 | 158 | 226524.6 ± 0.30 | 0.35 | 6.27 |
| mock_tilt0.06_snr0.25_seed2_all | all | 3602 | 3298 | 1,150,500 | 225 | 231834.2 ± 0.18 | 0.94 | 4.89 |
| mock_tilt0.06_snr0.25_seed2_features | features | 1389 | 3628 | 1,085,500 | 211 | 89656.2 ± 0.35 | 0.94 | 3.92 |
| mock_tilt0.06_snr0.25_seed2_features_downweight | features_downweight | 3602 | 3524 | 1,098,500 | 218 | 226530.8 ± 0.30 | 0.36 | 3.96 |
| mock_tilt0.06_snr1.00_seed1_all | all | 3602 | 3380 | 1,508,000 | 214 | 236415.4 ± 0.33 | 0.53 | 7.67 |
| mock_tilt0.06_snr1.00_seed1_features | features | 1389 | 3828 | 1,345,500 | 196 | 91406.8 ± 0.30 | 0.54 | 7.54 |
| mock_tilt0.06_snr1.00_seed1_features_downweight | features_downweight | 3602 | 3390 | 1,358,500 | 193 | 228312.4 ± 0.28 | 0.21 | 7.55 |
| mock_tilt0.06_snr1.00_seed2_all | all | 3602 | 3597 | 1,449,500 | 205 | 236426.7 ± 0.36 | 0.53 | 5.32 |
| mock_tilt0.06_snr1.00_seed2_features | features | 1389 | 3315 | 1,319,500 | 189 | 91439.8 ± 0.42 | 0.52 | 5.09 |
| mock_tilt0.06_snr1.00_seed2_features_downweight | features_downweight | 3602 | 3453 | 1,384,500 | 196 | 228292.4 ± 0.19 | 0.20 | 5.31 |
| real_M11_214430_all | all | 3810 | 4010 | 1,384,500 | 216 | 251147.9 ± 0.27 | 1.17 | 17.44 |
| real_M11_214430_features | features | 1088 | 3339 | 1,189,500 | 234 | 71696.5 ± 0.20 | 1.06 | 7.87 |
| real_M11_214430_features_downweight | features_downweight | 3810 | 3578 | 1,202,500 | 189 | 246488.0 ± 0.15 | 0.32 | 7.96 |
| real_M5_172669_all | all | 3602 | 3070 | 1,176,500 | 157 | 232731.2 ± 0.33 | 1.06 | 14.12 |
| real_M5_172669_features | features | 1389 | 3254 | 1,170,000 | 156 | 90430.5 ± 0.32 | 1.03 | 12.22 |
| real_M5_172669_features_downweight | features_downweight | 3602 | 3208 | 1,209,000 | 161 | 227369.5 ± 0.36 | 0.40 | 12.33 |
| real_M9_232005_all | all | 3494 | 3497 | 1,202,500 | 160 | 230695.7 ± 0.26 | 1.11 | 7.34 |
| real_M9_232005_features | features | 1521 | 3811 | 1,170,000 | 175 | 100541.2 ± 0.25 | 1.13 | 6.98 |
| real_M9_232005_features_downweight | features_downweight | 3494 | 3636 | 1,170,000 | 165 | 226195.2 ± 0.29 | 0.50 | 7.01 |

### Mock recovery

Truth: the weighted posterior median of the stored full-spectrum fit of M5_172669. Each cell is two noise realisations; bias is the mean of (posterior median − truth), the width column is the 16–84 half-width relative to the full-spectrum fit of the same cell, and coverage counts the realisations of that S/N scale (three tilts, two seeds) whose 16–84 interval contains the truth.

##### Pixel S/N scale 1

| parameter | mode | bias, ε=0.00 | bias, ε=0.03 | bias, ε=0.06 | width / full, median (range) | 68% coverage |
| --- | --- | --- | --- | --- | --- | --- |
| log M⋆ | full spectrum | +0.005 | +0.051 | +0.077 | 1.00 (1.00–1.00) | 1/6 |
| log M⋆ | features only | +0.004 | +0.049 | +0.078 | 1.23 (0.92–2.15) | 0/6 |
| log M⋆ | continuum down-weighted | +0.006 | +0.050 | +0.074 | 1.18 (1.08–1.73) | 1/6 |
| tMW [Gyr] | full spectrum | +0.01 | +0.16 | +0.13 | 1.00 (1.00–1.00) | 2/6 |
| tMW [Gyr] | features only | +0.01 | +0.12 | +0.14 | 1.11 (0.92–2.44) | 2/6 |
| tMW [Gyr] | continuum down-weighted | +0.01 | +0.16 | +0.07 | 1.17 (0.80–1.84) | 2/6 |
| log Z | full spectrum | -0.003 | -0.012 | +0.004 | 1.00 (1.00–1.00) | 5/6 |
| log Z | features only | -0.007 | +0.001 | +0.009 | 1.48 (0.86–1.93) | 4/6 |
| log Z | continuum down-weighted | -0.007 | -0.001 | +0.009 | 1.46 (0.79–1.71) | 3/6 |
| [α/Fe] | full spectrum | +0.006 | +0.004 | -0.006 | 1.00 (1.00–1.00) | 3/6 |
| [α/Fe] | features only | +0.013 | -0.006 | -0.015 | 1.35 (0.87–1.83) | 3/6 |
| [α/Fe] | continuum down-weighted | +0.012 | -0.006 | -0.009 | 1.39 (0.84–1.51) | 3/6 |
| τdust | full spectrum | -0.001 | +0.106 | +0.212 | 1.00 (1.00–1.00) | 2/6 |
| τdust | features only | +0.000 | +0.099 | +0.199 | 1.60 (1.12–2.05) | 2/6 |
| τdust | continuum down-weighted | +0.001 | +0.098 | +0.201 | 1.39 (0.78–1.93) | 2/6 |

##### Pixel S/N scale 0.25

| parameter | mode | bias, ε=0.00 | bias, ε=0.03 | bias, ε=0.06 | width / full, median (range) | 68% coverage |
| --- | --- | --- | --- | --- | --- | --- |
| log M⋆ | full spectrum | +0.005 | +0.048 | +0.078 | 1.00 (1.00–1.00) | 2/6 |
| log M⋆ | features only | +0.008 | +0.040 | +0.079 | 1.01 (0.48–1.40) | 1/6 |
| log M⋆ | continuum down-weighted | +0.008 | +0.044 | +0.077 | 1.20 (0.64–1.58) | 1/6 |
| tMW [Gyr] | full spectrum | +0.04 | +0.22 | +0.25 | 1.00 (1.00–1.00) | 0/6 |
| tMW [Gyr] | features only | +0.04 | +0.16 | +0.35 | 0.87 (0.72–1.54) | 1/6 |
| tMW [Gyr] | continuum down-weighted | +0.04 | +0.20 | +0.35 | 1.10 (0.75–2.09) | 1/6 |
| log Z | full spectrum | -0.013 | -0.018 | -0.011 | 1.00 (1.00–1.00) | 4/6 |
| log Z | features only | -0.038 | -0.004 | -0.003 | 1.60 (1.35–1.89) | 5/6 |
| log Z | continuum down-weighted | -0.036 | -0.011 | -0.000 | 1.55 (1.07–1.97) | 5/6 |
| [α/Fe] | full spectrum | +0.029 | -0.014 | -0.048 | 1.00 (1.00–1.00) | 3/6 |
| [α/Fe] | features only | +0.060 | -0.035 | -0.079 | 1.35 (1.28–1.61) | 1/6 |
| [α/Fe] | continuum down-weighted | +0.059 | -0.036 | -0.077 | 1.44 (1.32–1.58) | 1/6 |
| τdust | full spectrum | -0.002 | +0.097 | +0.198 | 1.00 (1.00–1.00) | 2/6 |
| τdust | features only | +0.004 | +0.080 | +0.165 | 1.56 (1.25–1.96) | 2/6 |
| τdust | continuum down-weighted | +0.004 | +0.080 | +0.164 | 1.55 (1.15–1.81) | 2/6 |

<figure>
<img src="figures/absorption-mask/mock_bias_vs_tilt.png" alt="Posterior median and 16-84 interval minus the truth for five parameters against the continuum tilt amplitude, in three pixel modes and two S/N scales">
<figcaption>Posterior median and 16–84 interval relative to the truth against the tilt amplitude ε, for the native pixel S/N (left) and the noise inflated four times (right). Blue: full spectrum; orange: features only; green: continuum down-weighted. Two realisations per cell, offset for legibility.</figcaption>
</figure>

<figure>
<img src="figures/absorption-mask/mock_width_ratio.png" alt="Ratio of the masked-mode posterior half-width to the full-spectrum half-width for each parameter and mock cell">
<figcaption>Posterior half-width of the masked modes relative to the full-spectrum fit of the same mock.</figcaption>
</figure>

Bias is posterior median minus truth, averaged over realisations; width is the 16-84 half-width; z is bias/width (RMS over realisations); cov68 is the fraction of realisations whose 16-84 interval contains the truth.

##### log M*

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | 0.005 | 0.008 | 1.00 | 0.68 | 1.00 |
| 0.00 | 0.25 | features only | 2 | 0.008 | 0.010 | 1.19 | 0.84 | 0.50 |
| 0.00 | 0.25 | continuum down-weighted | 2 | 0.008 | 0.010 | 1.19 | 0.88 | 0.50 |
| 0.00 | 1.00 | full spectrum | 2 | 0.005 | 0.007 | 1.00 | 1.65 | 0.50 |
| 0.00 | 1.00 | features only | 2 | 0.004 | 0.007 | 0.99 | 1.77 | 0.00 |
| 0.00 | 1.00 | continuum down-weighted | 2 | 0.006 | 0.008 | 1.19 | 1.53 | 0.50 |
| 0.03 | 0.25 | full spectrum | 2 | 0.048 | 0.020 | 1.00 | 2.71 | 0.00 |
| 0.03 | 0.25 | features only | 2 | 0.040 | 0.014 | 0.68 | 3.04 | 0.00 |
| 0.03 | 0.25 | continuum down-weighted | 2 | 0.044 | 0.019 | 0.95 | 2.40 | 0.00 |
| 0.03 | 1.00 | full spectrum | 2 | 0.051 | 0.009 | 1.00 | 5.65 | 0.00 |
| 0.03 | 1.00 | features only | 2 | 0.049 | 0.013 | 1.40 | 3.87 | 0.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | 0.050 | 0.010 | 1.10 | 4.94 | 0.00 |
| 0.06 | 0.25 | full spectrum | 2 | 0.078 | 0.020 | 1.00 | 4.31 | 0.00 |
| 0.06 | 0.25 | features only | 2 | 0.079 | 0.022 | 1.10 | 3.68 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | 0.077 | 0.023 | 1.19 | 3.29 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | 0.077 | 0.008 | 1.00 | 10.23 | 0.00 |
| 0.06 | 1.00 | features only | 2 | 0.078 | 0.013 | 1.74 | 6.21 | 0.00 |
| 0.06 | 1.00 | continuum down-weighted | 2 | 0.074 | 0.011 | 1.47 | 6.92 | 0.00 |

##### t_MW [Gyr]

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | 0.037 | 0.071 | 1.00 | 0.52 | 0.00 |
| 0.00 | 0.25 | features only | 2 | 0.043 | 0.083 | 1.17 | 0.49 | 0.50 |
| 0.00 | 0.25 | continuum down-weighted | 2 | 0.042 | 0.081 | 1.14 | 0.48 | 0.50 |
| 0.00 | 1.00 | full spectrum | 2 | 0.015 | 0.033 | 1.00 | 0.45 | 1.00 |
| 0.00 | 1.00 | features only | 2 | 0.013 | 0.034 | 1.03 | 0.39 | 1.00 |
| 0.00 | 1.00 | continuum down-weighted | 2 | 0.014 | 0.046 | 1.38 | 0.36 | 1.00 |
| 0.03 | 0.25 | full spectrum | 2 | 0.220 | 0.265 | 1.00 | 0.86 | 0.00 |
| 0.03 | 0.25 | features only | 2 | 0.160 | 0.200 | 0.75 | 0.84 | 0.00 |
| 0.03 | 0.25 | continuum down-weighted | 2 | 0.201 | 0.263 | 0.99 | 0.93 | 0.00 |
| 0.03 | 1.00 | full spectrum | 2 | 0.163 | 0.111 | 1.00 | 1.47 | 0.00 |
| 0.03 | 1.00 | features only | 2 | 0.123 | 0.132 | 1.19 | 0.93 | 0.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | 0.156 | 0.126 | 1.14 | 1.18 | 0.00 |
| 0.06 | 0.25 | full spectrum | 2 | 0.254 | 0.264 | 1.00 | 0.99 | 0.00 |
| 0.06 | 0.25 | features only | 2 | 0.354 | 0.290 | 1.10 | 1.19 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | 0.345 | 0.362 | 1.37 | 0.97 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | 0.128 | 0.098 | 1.00 | 1.30 | 0.00 |
| 0.06 | 1.00 | features only | 2 | 0.136 | 0.179 | 1.83 | 0.77 | 0.00 |
| 0.06 | 1.00 | continuum down-weighted | 2 | 0.068 | 0.125 | 1.27 | 0.66 | 0.00 |

##### log Z

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | -0.013 | 0.019 | 1.00 | 0.87 | 0.50 |
| 0.00 | 0.25 | features only | 2 | -0.038 | 0.030 | 1.59 | 1.35 | 0.50 |
| 0.00 | 0.25 | continuum down-weighted | 2 | -0.036 | 0.029 | 1.55 | 1.37 | 0.50 |
| 0.00 | 1.00 | full spectrum | 2 | -0.003 | 0.007 | 1.00 | 0.69 | 1.00 |
| 0.00 | 1.00 | features only | 2 | -0.007 | 0.011 | 1.55 | 0.88 | 0.50 |
| 0.00 | 1.00 | continuum down-weighted | 2 | -0.007 | 0.011 | 1.54 | 0.91 | 0.50 |
| 0.03 | 0.25 | full spectrum | 2 | -0.018 | 0.025 | 1.00 | 0.77 | 1.00 |
| 0.03 | 0.25 | features only | 2 | -0.004 | 0.042 | 1.67 | 0.32 | 1.00 |
| 0.03 | 0.25 | continuum down-weighted | 2 | -0.011 | 0.042 | 1.65 | 0.45 | 1.00 |
| 0.03 | 1.00 | full spectrum | 2 | -0.012 | 0.008 | 1.00 | 1.81 | 0.50 |
| 0.03 | 1.00 | features only | 2 | 0.001 | 0.013 | 1.63 | 1.03 | 1.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | -0.001 | 0.012 | 1.52 | 1.14 | 0.50 |
| 0.06 | 0.25 | full spectrum | 2 | -0.011 | 0.028 | 1.00 | 1.13 | 0.50 |
| 0.06 | 0.25 | features only | 2 | -0.003 | 0.045 | 1.58 | 0.78 | 1.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | -0.000 | 0.037 | 1.32 | 0.80 | 1.00 |
| 0.06 | 1.00 | full spectrum | 2 | 0.004 | 0.012 | 1.00 | 0.57 | 1.00 |
| 0.06 | 1.00 | features only | 2 | 0.009 | 0.013 | 1.13 | 1.26 | 0.50 |
| 0.06 | 1.00 | continuum down-weighted | 2 | 0.009 | 0.013 | 1.09 | 1.48 | 0.50 |

##### [α/Fe]

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | 0.029 | 0.020 | 1.00 | 1.56 | 0.50 |
| 0.00 | 0.25 | features only | 2 | 0.060 | 0.027 | 1.35 | 2.29 | 0.00 |
| 0.00 | 0.25 | continuum down-weighted | 2 | 0.059 | 0.028 | 1.40 | 2.14 | 0.00 |
| 0.00 | 1.00 | full spectrum | 2 | 0.006 | 0.007 | 1.00 | 0.94 | 0.50 |
| 0.00 | 1.00 | features only | 2 | 0.013 | 0.010 | 1.43 | 1.26 | 0.50 |
| 0.00 | 1.00 | continuum down-weighted | 2 | 0.012 | 0.010 | 1.41 | 1.19 | 0.50 |
| 0.03 | 0.25 | full spectrum | 2 | -0.014 | 0.022 | 1.00 | 0.71 | 1.00 |
| 0.03 | 0.25 | features only | 2 | -0.035 | 0.033 | 1.48 | 1.14 | 0.50 |
| 0.03 | 0.25 | continuum down-weighted | 2 | -0.036 | 0.032 | 1.46 | 1.20 | 0.50 |
| 0.03 | 1.00 | full spectrum | 2 | 0.004 | 0.007 | 1.00 | 1.28 | 0.50 |
| 0.03 | 1.00 | features only | 2 | -0.006 | 0.011 | 1.56 | 0.90 | 0.50 |
| 0.03 | 1.00 | continuum down-weighted | 2 | -0.006 | 0.011 | 1.46 | 0.84 | 0.50 |
| 0.06 | 0.25 | full spectrum | 2 | -0.048 | 0.023 | 1.00 | 2.10 | 0.00 |
| 0.06 | 0.25 | features only | 2 | -0.079 | 0.030 | 1.29 | 2.67 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | -0.077 | 0.033 | 1.44 | 2.38 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | -0.006 | 0.010 | 1.00 | 0.90 | 0.50 |
| 0.06 | 1.00 | features only | 2 | -0.015 | 0.010 | 1.01 | 1.96 | 0.50 |
| 0.06 | 1.00 | continuum down-weighted | 2 | -0.009 | 0.010 | 1.08 | 1.57 | 0.50 |

##### τ_dust

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | -0.002 | 0.006 | 1.00 | 0.43 | 1.00 |
| 0.00 | 0.25 | features only | 2 | 0.004 | 0.009 | 1.47 | 0.56 | 1.00 |
| 0.00 | 0.25 | continuum down-weighted | 2 | 0.004 | 0.009 | 1.51 | 0.47 | 1.00 |
| 0.00 | 1.00 | full spectrum | 2 | -0.001 | 0.003 | 1.00 | 0.55 | 1.00 |
| 0.00 | 1.00 | features only | 2 | 0.000 | 0.004 | 1.52 | 0.17 | 1.00 |
| 0.00 | 1.00 | continuum down-weighted | 2 | 0.001 | 0.004 | 1.39 | 0.24 | 1.00 |
| 0.03 | 0.25 | full spectrum | 2 | 0.097 | 0.010 | 1.00 | 9.64 | 0.00 |
| 0.03 | 0.25 | features only | 2 | 0.080 | 0.018 | 1.79 | 4.48 | 0.00 |
| 0.03 | 0.25 | continuum down-weighted | 2 | 0.080 | 0.017 | 1.69 | 4.74 | 0.00 |
| 0.03 | 1.00 | full spectrum | 2 | 0.106 | 0.004 | 1.00 | 28.88 | 0.00 |
| 0.03 | 1.00 | features only | 2 | 0.099 | 0.007 | 1.88 | 14.53 | 0.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | 0.098 | 0.007 | 1.89 | 14.12 | 0.00 |
| 0.06 | 0.25 | full spectrum | 2 | 0.198 | 0.013 | 1.00 | 16.73 | 0.00 |
| 0.06 | 0.25 | features only | 2 | 0.165 | 0.018 | 1.41 | 9.28 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | 0.164 | 0.017 | 1.36 | 9.38 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | 0.212 | 0.005 | 1.00 | 44.25 | 0.00 |
| 0.06 | 1.00 | features only | 2 | 0.199 | 0.007 | 1.32 | 30.03 | 0.00 |
| 0.06 | 1.00 | continuum down-weighted | 2 | 0.201 | 0.005 | 1.00 | 40.52 | 0.00 |

##### s_spec

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | 0.008 | 0.019 | 1.00 | 0.46 | 1.00 |
| 0.00 | 0.25 | features only | 2 | 0.014 | 0.019 | 1.04 | 0.72 | 1.00 |
| 0.00 | 0.25 | continuum down-weighted | 2 | 0.012 | 0.019 | 1.03 | 0.65 | 1.00 |
| 0.00 | 1.00 | full spectrum | 2 | -0.004 | 0.018 | 1.00 | 1.66 | 0.00 |
| 0.00 | 1.00 | features only | 2 | -0.003 | 0.018 | 1.01 | 1.67 | 0.00 |
| 0.00 | 1.00 | continuum down-weighted | 2 | -0.006 | 0.018 | 1.00 | 1.68 | 0.00 |
| 0.03 | 0.25 | full spectrum | 2 | 0.043 | 0.021 | 1.00 | 2.11 | 0.00 |
| 0.03 | 0.25 | features only | 2 | 0.024 | 0.021 | 0.99 | 1.29 | 0.50 |
| 0.03 | 0.25 | continuum down-weighted | 2 | 0.029 | 0.023 | 1.09 | 1.33 | 0.50 |
| 0.03 | 1.00 | full spectrum | 2 | 0.032 | 0.019 | 1.00 | 1.72 | 0.00 |
| 0.03 | 1.00 | features only | 2 | 0.029 | 0.022 | 1.11 | 1.37 | 0.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | 0.029 | 0.020 | 1.03 | 1.55 | 0.00 |
| 0.06 | 0.25 | full spectrum | 2 | 0.099 | 0.022 | 1.00 | 4.45 | 0.00 |
| 0.06 | 0.25 | features only | 2 | 0.078 | 0.023 | 1.05 | 3.34 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | 0.082 | 0.024 | 1.09 | 3.46 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | 0.099 | 0.023 | 1.00 | 4.40 | 0.00 |
| 0.06 | 1.00 | features only | 2 | 0.088 | 0.020 | 0.90 | 4.41 | 0.00 |
| 0.06 | 1.00 | continuum down-weighted | 2 | 0.088 | 0.020 | 0.88 | 4.42 | 0.00 |

##### f_calib [%]

| tilt | S/N scale | mode | n | bias | width | width / full | RMS z | cov68 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.00 | 0.25 | full spectrum | 2 | -1.867 | 0.033 | 1.00 | 58.17 | 0.00 |
| 0.00 | 0.25 | features only | 2 | -1.829 | 0.071 | 2.16 | 26.08 | 0.00 |
| 0.00 | 0.25 | continuum down-weighted | 2 | -1.828 | 0.078 | 2.37 | 23.71 | 0.00 |
| 0.00 | 1.00 | full spectrum | 2 | -1.896 | 0.001 | 1.00 | 2071.08 | 0.00 |
| 0.00 | 1.00 | features only | 2 | -1.894 | 0.003 | 2.76 | 749.91 | 0.00 |
| 0.00 | 1.00 | continuum down-weighted | 2 | -1.895 | 0.002 | 2.34 | 885.67 | 0.00 |
| 0.03 | 0.25 | full spectrum | 2 | -1.849 | 0.043 | 1.00 | 51.71 | 0.00 |
| 0.03 | 0.25 | features only | 2 | -1.786 | 0.107 | 2.48 | 17.19 | 0.00 |
| 0.03 | 0.25 | continuum down-weighted | 2 | -1.795 | 0.097 | 2.26 | 19.54 | 0.00 |
| 0.03 | 1.00 | full spectrum | 2 | -1.896 | 0.001 | 1.00 | 2625.67 | 0.00 |
| 0.03 | 1.00 | features only | 2 | -1.895 | 0.003 | 3.69 | 709.60 | 0.00 |
| 0.03 | 1.00 | continuum down-weighted | 2 | -1.894 | 0.003 | 4.11 | 644.87 | 0.00 |
| 0.06 | 0.25 | full spectrum | 2 | -1.856 | 0.047 | 1.00 | 40.11 | 0.00 |
| 0.06 | 0.25 | features only | 2 | -1.794 | 0.100 | 2.11 | 17.94 | 0.00 |
| 0.06 | 0.25 | continuum down-weighted | 2 | -1.794 | 0.082 | 1.74 | 22.72 | 0.00 |
| 0.06 | 1.00 | full spectrum | 2 | -1.896 | 0.001 | 1.00 | 1961.09 | 0.00 |
| 0.06 | 1.00 | features only | 2 | -1.894 | 0.003 | 2.69 | 741.84 | 0.00 |
| 0.06 | 1.00 | continuum down-weighted | 2 | -1.894 | 0.002 | 2.37 | 825.94 | 0.00 |

### Real targets

Shift of the masked-mode posterior median from the full-spectrum median, in units of the full-spectrum 16–84 half-width. Feature pixels kept by the 1000 km/s windows: M11_214430: 1088 of 3810 pixels (29%); M5_172669: 1389 of 3602 pixels (39%); M9_232005: 1521 of 3494 pixels (44%).

| parameter | M11_214430 features only | M11_214430 continuum down-weighted | M5_172669 features only | M5_172669 continuum down-weighted | M9_232005 features only | M9_232005 continuum down-weighted |
| --- | --- | --- | --- | --- | --- | --- |
| log M⋆ | +0.038 (+1.8σ) | +0.019 (+0.9σ) | +0.009 (+1.3σ) | +0.010 (+1.4σ) | +0.084 (+7.4σ) | +0.108 (+9.4σ) |
| tMW [Gyr] | +0.60 (+3.0σ) | +0.30 (+1.5σ) | +0.03 (+1.4σ) | +0.04 (+1.4σ) | +1.27 (+13.6σ) | +1.59 (+17.0σ) |
| log Z | -0.179 (-5.6σ) | -0.168 (-5.3σ) | -0.249 (-21.7σ) | -0.250 (-21.8σ) | -0.082 (-4.9σ) | -0.107 (-6.4σ) |
| [α/Fe] | -0.041 (-2.9σ) | -0.040 (-2.8σ) | +0.225 (+15.0σ) | +0.224 (+14.9σ) | +0.025 (+2.3σ) | +0.028 (+2.6σ) |
| τdust | -0.110 (-6.9σ) | -0.109 (-6.9σ) | +0.044 (+9.5σ) | +0.043 (+9.5σ) | +0.013 (+1.4σ) | +0.010 (+1.1σ) |

<figure>
<img src="figures/absorption-mask/real_targets_posteriors.png" alt="Posterior medians with 16-84 intervals for three real targets in the three pixel modes">
<figcaption>Posterior medians with 16–84 intervals for the three DR2 targets in each pixel mode.</figcaption>
</figure>

Photometry reduced chi-squared per band, full spectrum → masked modes: M11_214430: 17.44 → 7.87 (features), 7.96 (down-weighted); M5_172669: 14.12 → 12.22 (features), 12.33 (down-weighted); M9_232005: 7.34 → 6.98 (features), 7.01 (down-weighted). The masked fits do not fit the photometry better; they fit a different spectrum model to the same photometry.

Shift is (median - full-spectrum median) / full-spectrum half-width.

##### log M*

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | 11.496 | [11.473, 11.514] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | 11.533 | [11.514, 11.551] | 1.85 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | 11.514 | [11.491, 11.536] | 0.92 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 11.110 | [11.103, 11.117] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 11.119 | [11.111, 11.127] | 1.33 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 11.119 | [11.112, 11.128] | 1.39 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 10.851 | [10.841, 10.864] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 10.935 | [10.902, 10.962] | 7.37 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 10.958 | [10.936, 10.980] | 9.41 | 3636 | 1,170,000 |

##### t_MW [Gyr]

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | 3.829 | [3.600, 3.995] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | 4.427 | [4.156, 4.680] | 3.03 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | 4.131 | [3.927, 4.368] | 1.53 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 1.666 | [1.654, 1.703] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 1.700 | [1.659, 1.763] | 1.38 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 1.702 | [1.660, 1.775] | 1.45 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 3.019 | [2.982, 3.170] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 4.293 | [3.871, 4.569] | 13.59 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 4.613 | [4.239, 4.988] | 17.00 | 3636 | 1,170,000 |

##### log Z

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | -1.645 | [-1.675, -1.611] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | -1.824 | [-1.851, -1.797] | -5.64 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | -1.813 | [-1.844, -1.781] | -5.30 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | -1.723 | [-1.733, -1.710] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | -1.972 | [-1.985, -1.954] | -21.74 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | -1.973 | [-1.985, -1.955] | -21.80 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | -1.670 | [-1.687, -1.654] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | -1.753 | [-1.789, -1.698] | -4.91 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | -1.777 | [-1.793, -1.749] | -6.37 | 3636 | 1,170,000 |

##### [α/Fe]

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | -0.155 | [-0.168, -0.140] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | -0.196 | [-0.199, -0.190] | -2.91 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | -0.195 | [-0.199, -0.189] | -2.84 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 0.134 | [0.120, 0.150] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 0.359 | [0.342, 0.375] | 15.02 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 0.358 | [0.342, 0.374] | 14.94 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 0.097 | [0.086, 0.108] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 0.122 | [0.098, 0.137] | 2.28 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 0.125 | [0.106, 0.140] | 2.58 | 3636 | 1,170,000 |

##### τ_dust

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | 0.602 | [0.586, 0.617] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | 0.492 | [0.464, 0.522] | -6.94 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | 0.493 | [0.464, 0.523] | -6.87 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 0.011 | [0.007, 0.016] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 0.055 | [0.049, 0.061] | 9.52 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 0.055 | [0.049, 0.061] | 9.47 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 0.164 | [0.154, 0.173] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 0.177 | [0.160, 0.191] | 1.36 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 0.174 | [0.163, 0.184] | 1.06 | 3636 | 1,170,000 |

##### s_spec

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | 1.650 | [1.615, 1.684] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | 1.436 | [1.391, 1.477] | -6.21 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | 1.441 | [1.395, 1.484] | -6.09 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 1.237 | [1.219, 1.256] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 1.261 | [1.242, 1.280] | 1.29 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 1.261 | [1.242, 1.280] | 1.30 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 1.051 | [1.032, 1.068] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 1.059 | [1.041, 1.078] | 0.41 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 1.059 | [1.037, 1.078] | 0.41 | 3636 | 1,170,000 |

##### f_calib [%]

| target | mode | pixels | median | 16-84 | shift | ESS | calls |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M11_214430 | full spectrum | 3810 | 5.193 | [5.045, 5.345] | 0.00 | 4010 | 1,384,500 |
| M11_214430 | features only | 1088 | 4.061 | [3.812, 4.280] | -7.53 | 3339 | 1,189,500 |
| M11_214430 | continuum down-weighted | 3810 | 3.934 | [3.758, 4.150] | -8.38 | 3578 | 1,202,500 |
| M5_172669 | full spectrum | 3602 | 2.894 | [2.855, 2.937] | 0.00 | 3070 | 1,176,500 |
| M5_172669 | features only | 1389 | 1.992 | [1.947, 2.044] | -22.02 | 3254 | 1,170,000 |
| M5_172669 | continuum down-weighted | 3602 | 1.990 | [1.940, 2.043] | -22.08 | 3208 | 1,209,000 |
| M9_232005 | full spectrum | 3494 | 2.847 | [2.758, 2.942] | 0.00 | 3497 | 1,202,500 |
| M9_232005 | features only | 1521 | 3.208 | [3.098, 3.353] | 3.92 | 3811 | 1,170,000 |
| M9_232005 | continuum down-weighted | 3494 | 3.202 | [3.089, 3.312] | 3.85 | 3636 | 1,170,000 |

### Interpretation and recommendation

*Project synthesis.*

1. **Why the mask does not remove a tilt.** Each absorption window keeps its local continuum level, and the windows span the fitted range from H10 to TiO. The run of window levels traces the tilt as well as the full continuum does, only with fewer pixels, so the tilt still enters as a colour term. The model absorbs it the same way in every mode: τdust rises by +0.10 to +0.11 per 3 percent of tilt and by +0.20 to +0.21 per 6 percent, and the age and mass move with it. Removing the tilt needs a multiplicative calibration polynomial fitted with the model, or windows normalised by their own pseudo-continuum (index fitting), not fewer pixels.
2. **Why the photometry cannot take over.** The balance factor of 14 to 71 equalises the continuum pixels with the twelve bands, but the feature pixels keep their full weight and carry the same slope information, so the photometry's Fisher share stays below one percent. Only a calibration model that decouples the spectral shape from the stellar-population shape gives the bands a say.
3. **What the real-target shifts mean.** The masked posteriors are 0.9 to 1.6 times as wide as the full-spectrum ones in the mocks (medians per parameter and S/N scale) but move by up to 22 sigma on real spectra, so the full-spectrum posteriors are precise about a model the continuum and the lines do not share. Candidates are the relative flux calibration of LEGA-C beyond a linear tilt, and template systematics (the C3K continuum against its line strengths). This test cannot rank them; a fit with a free low-order calibration vector can.
4. **Coverage.** With no tilt the 68 percent intervals cover the truth in 10/16 (full), 7/16 (features) and 8/16 (down-weighted) parameter-realisations; with a tilt it collapses to 10/32, 10/32 and 9/32 over the four tilted cells. The posteriors are too narrow to absorb a few-percent calibration error whichever pixels are used.
5. **Recommendation.** Default off. Keep `features` and `features_downweight` as diagnostics behind `CERIDWEN_SPECTRUM_PIXELS`. The line list is the Lick set plus the Balmer, Ca H&K and Ca triplet centres; 1000 km/s windows keep 29 to 44 percent of the pixels. Neither the list nor the window changes the conclusion, because the failure is in what the windows still contain, not in which windows are chosen.

### Evidence

- Code: branch `absorption-mask` in the project and in the ceridwen submodule; `scripts/absorption_mask_analysis.py`, `scripts/absorption_mask_grid.py`, `scripts/absorption_mask_vast.py`, `scripts/absorption_mask_report.py`.
- Results: `results/absorption-mask/<cell>/` (executed notebook, `ceridwen_result.h5`, `ceridwen_derived_outputs.h5`), `summary.csv`, `summary.json`, `fisher_M5_172669.json`, run records `vast_run_*.json`.
- Figures: `wiki/analyses/absorption-mask/`.
