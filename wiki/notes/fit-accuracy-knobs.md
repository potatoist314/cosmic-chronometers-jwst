---
title: Fit-accuracy knobs after the calibration polynomial
date: 2026-09-06
section: Analyses
tags: [calibration, ceridwen, dr2-quiescent-sample, lick-indices]
job:
figures: [stage0_chi2_map.png, stage0_prior_rails.png, stage0_lick_residuals.png]
---

## Stage 0, diagnostics on the poly3_total fits

Inputs
: The six `results/calibration-polynomial-dr2/poly3_total/*` fits. No new sampling. Notebook `results/fit-accuracy-knobs/stage0_diagnostics.ipynb`, table `stage0_summary.csv`.

Raw chi2
: Spectral chi2 recomputed at one fixed f_calib = 0.03 so the arms are comparable (the stored chi2 uses each fit's own f_calib). Photometric chi2 over the 12 cosmos_total bands at the maximum-likelihood draw.

Windows
: Share of the spectral chi2 inside +/-1500 km/s of [NeIII] 3869, H-epsilon 3970, H-delta 4102 and H-gamma 4340, and inside rest 3800-4300 A, against the share of pixels there.

Rails
: A parameter is railed when more than 0.5 of the posterior mass sits within 5 percent of a prior edge.

Lick indices
: HdA, Fe4383, Dn4000 and Hbeta predicted from 200 weighted posterior draws with `StellarIndices` and the DR2 definitions, minus the DR2 catalogue value, over the catalogue error. Caveat: the catalogue indices come from the uncalibrated DR2 spectra.

Borghi+22
: Age, [Z/H] and [alpha/Fe] for the two overlap galaxies. Borghi's ages are SSP-equivalent, ours are mass-weighted, so the age column is a direction, not a test.

```
chi2_raw(f) = sum_i (d_i - s P_i mu_i)^2 / (sigma_i^2 + (f s P_i mu_i)^2)
```

| galaxy | f_calib fit | chi2/nu at f=0.03 | pixels with pull > 4 | phot chi2 (12 bands) | IRAC share of phot chi2 | blue chi2 share / pixel share | railed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M4_108989 | 0.044 | 1.50 | 12 | 13.4 | 0.00 | 0.33 / 0.38 | afe (-0.2) |
| M5_172669 | 0.027 | 0.86 | 18 | 99.9 | 0.18 | 0.06 / 0.15 | none |
| M5_173928 | 0.090 | 2.61 | 77 | 51.0 | 0.25 | 0.23 / 0.39 | log_f_calib (near 0.10) |
| M12_185653 | 0.063 | 2.00 | 24 | 9.8 | 0.27 | 0.26 / 0.26 | none |
| M1_206545 | 0.039 | 1.59 | 19 | 62.5 | 0.13 | 0.49 / 0.42 | afe (-0.2) |
| M12_98104 | 0.100 | 2.17 | 32 | 10.6 | 0.32 | 0.42 / 0.40 | log_f_calib (0.10) |

Balmer windows
: Each of the four line windows carries at most 0.055 of the spectral chi2. The blue share tracks the pixel share. The misfit is spread over the continuum, not concentrated in emission infill.

Photometric pulls
: M5_172669 V +4.6, r +5.4, i +3.8, Ks -2.7, IRAC -3.5 and -2.5. M5_173928 r, i, z near +3.5, IRAC -2.6 and -2.5. M1_206545 u -3.4, B -4.4. The optical and IRAC pulls have opposite signs: the SED is too red in the model.

Lick residuals
: M4_108989 CN1 -5.4, CN2 -5.1, C4668 -7.5, HdA +2.6, Dn4000 -2.8. M1_206545 C4668 -5.8, HgA +4.4. Fe4383 negative in 4 of 5, Dn4000 negative in 4 of 4, C4668 negative in 3 of 3. The model has too little carbon and nitrogen absorption, and [alpha/Fe] sits at the -0.2 grid edge for the two galaxies with the strongest CN and C4668 residuals.

Borghi+22
: M4_108989 age 4.61 vs 4.03 Gyr, [Z/H] -0.03 vs +0.07, [alpha/Fe] -0.19 vs +0.06. M12_185653 age 5.02 vs 3.11 Gyr, [Z/H] -0.34 vs -0.01, [alpha/Fe] +0.23 vs -0.06.

<figure>
<img src="figures/fit-accuracy-knobs/stage0_chi2_map.png" alt="Spectral chi2 per rest wavelength and photometric pull per band for the six poly3_total fits">
<figcaption>Where the chi2 lives, six galaxies, f_calib = 0.03</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/stage0_prior_rails.png" alt="Posterior mass within 5 percent of a prior edge, per parameter and galaxy">
<figcaption>Prior rails, afe at -0.2 for two galaxies and log_f_calib at the 10 percent ceiling for two others</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/stage0_lick_residuals.png" alt="Predicted minus catalogue Lick index over catalogue error, per index and galaxy">
<figcaption>Lick-index residuals against the DR2 catalogue</figcaption>
</figure>

## Stage 1, one switch per arm

Setup
: Every arm is `poly3_total` plus one environment switch read in cell 2 of `notebooks/ceridwen_integrated_photometry_spectra.ipynb`. Every default is the production value, checked by an identical quick-profile run against HEAD (same ln Z, same likelihood-call count). The switch is written to the run log line `name: start seed=... {env}` and to the h5 `model` attributes. Arms live in `scripts/calibration_arms_vast.py`, results under `results/fit-accuracy-knobs/<arm>/`, tests in `tests/test_calibration_arms.py`.

| arm | switch | value | tests |
| --- | --- | --- | --- |
| seed_rep1..3 | `--base-seed` forwarded to multi_gpu | +1000, +2000, +3000 | scatter floor between independent NSS runs, M4_108989 and M5_172669 only |
| floor20 | `CERIDWEN_FCALIB_MAX` | 0.20 | two fits sit at the 0.10 ceiling; does unrailing f_calib move the physics |
| dust_free | `CERIDWEN_FREE_DUST_INDEX` | Uniform(-1.0, 0.4) on the Kriek and Conroy index | optical-versus-IRAC pulls of opposite sign, SED too red |
| no_irac | `CERIDWEN_PHOT_DROP` | spitzer_irac_ch1, spitzer_irac_ch2 | IRAC carries 0.13-0.32 of the photometric chi2 |
| mask_cn | `CERIDWEN_MASK_REST_WINDOWS` | rest 4142-4177 and 4634-4720 A | CN and C4668 residuals of -5 to -7.5 sigma with afe railed |
| sfh_cont | `CERIDWEN_SFH_PRIOR` | StudentT(0, 0.3, df 2) on logsfr_ratios | continuity prior against Uniform(-3, 3); also on the tilt4 mock |
| emis_wide | `CERIDWEN_EMISSION_LINES` | add [NeIII] 3869, H-epsilon, H-delta, H-gamma | Balmer infill; low priority, each window is under 0.055 of chi2 |

Dtype
: `StudentT` needs `df=2.0`. An integer df makes TensorFlow Probability refuse the mixed dtypes at the first prior draw. Caught by the all-switches quick run, not by the defaults run.

Pixel guard
: The line and CN masks remove about 800 more pixels, so the guard is now `good_pixel.sum() > 3000` and `ndof > 0.7 good_pixel.sum()`.

Scoring
: Delta raw spectral chi2 at f = 0.03. Delta photometric chi2. Delta ln Z, counted only when |Delta| > 1 (NSS error 0.2-0.35). Shift of t_MW, log Z, [alpha/Fe], tau_dust and log M in units of the poly3_total posterior half-width, against the seed_rep scatter. Lick residuals and Borghi+22 agreement. Null check on the new nuisance posterior (dust index away from -0.7, f_calib below 0.10).

Verdict rule
: Written before the fits ran. An arm goes into production only if it beats the seed floor on a physics parameter or improves Lick or Borghi agreement. Chi2 alone is not enough, f_calib can always buy chi2.

Run
: 43 cells (36 arm-galaxy pairs, 6 seed repeats, 1 mock), one RTX 5060, `CERIDWEN_ARMS_RESULTS=results/fit-accuracy-knobs`. Results section added when the fits land.
