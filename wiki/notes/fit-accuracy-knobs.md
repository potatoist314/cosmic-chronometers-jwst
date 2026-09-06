---
title: Fit-accuracy knobs after the calibration polynomial
date: 2026-09-06
section: Analyses
tags: [calibration, ceridwen, dr2-quiescent-sample, lick-indices]
job:
figures: [stage0_chi2_map.png, stage0_prior_rails.png, stage0_lick_residuals.png, parameters-shift.png, sfh-continuity.png, sfh-histories.png, lick-by-arm.png, mock-sfh-prior.png, chi2-M5_173928.png, corner-M5_173928.png]
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

Default flipped
: Liu Hao's call on 2026-09-06, before the stage-1 fits finished: the StudentT(0, 0.3, df 2) continuity prior is now the production default in the notebook (`CERIDWEN_SFH_PRIOR` unset means `student`). The `poly3_total` reference arm and its seed repeats pin `uniform`, so the stored fits stay reproducible. The results section shows how the SFH differs per galaxy under the two priors.

Verdict rule
: Written before the fits ran. An arm goes into production only if it beats the seed floor on a physics parameter or improves Lick or Borghi agreement. Chi2 alone is not enough, f_calib can always buy chi2.

Run
: 43 cells (36 arm-galaxy pairs, 6 seed repeats, 1 mock), one RTX 5060, `CERIDWEN_ARMS_RESULTS=results/fit-accuracy-knobs`. 3.99 GPU-hours of sampling over 4 h 56 min of rental, $0.665. Every cell has `passed = True` and posterior ESS above 3250.

Validator incident
: The runner's cell validator rejected `dust_free/98104-M12_98104` because `diffuse_dust_index` is a sampled nuisance the validator did not know. The fit itself is complete and valid, and the analysis reads it. Fixed in commit 190b39d after the cell had already run, so the run log shows 42 done and 1 failed for 43 finished fits.

## Stage 1 results

Notebook
: `results/fit-accuracy-knobs/analysis.ipynb`, executed on CPU. Tables `arms.csv`, `before-after.csv`, `verdict.csv`, `lick-by-arm.csv`, `borghi-by-arm.csv`, `sfh-prior-compare.csv`, `mock-pulls.csv`.

Comparability
: Delta chi2 is measured on the pixels and bands both fits keep, at f_calib = 3 percent. `mask_cn` drops 114-349 pixels and `emis_wide` drops 181-488, so ln Z for those two arms is not on the same data and is not read. `no_irac` drops 2 bands, same rule. Only `floor20`, `dust_free` and `sfh_cont` carry a comparable ln Z.

### Seed floor

Floor
: Largest shift over the six repeat fits, in units of the reference posterior half-width. Age 1.20, log Z 0.49, [alpha/Fe] 0.96, tau_dust 0.32, log M 0.49. An arm counts only above these.

Split by galaxy
: M4_108989 repeats to 0.06 in age, 0.12 in log Z, 0.12 in [alpha/Fe], 0.25 in tau_dust and 0.15 in log M. M5_172669 carries the whole floor: 1.20 in age, 0.96 in [alpha/Fe], 0.49 in log Z. The floor is a property of the galaxy, not of the sampler settings.

ln Z floor
: Seed-to-seed ln Z spread reaches 2.0 (4.2 combined NSS sigma) on M5_172669, against the 0.2-0.35 per-fit error the scoring rule assumed. The |Delta ln Z| > 1 threshold written before the run therefore sits below the seed floor and cannot separate arms on its own.

| arm | Delta chi2 spec, median | Delta chi2 phot, median | Delta ln Z, median | pairs above floor | verdict |
| --- | --- | --- | --- | --- | --- |
| floor20 | +0.9 | -0.6 | +0.1 | 3 of 30 | no, one galaxy only |
| dust_free | -1.9 | -10.7 | +8.2 | 18 of 30 | adopt |
| no_irac | -0.5 | +1.9 | not comparable | 16 of 30 | no, diagnostic |
| mask_cn | -13.8 | -2.2 | not comparable | 13 of 30 | no |
| sfh_cont | +2.8 | -0.8 | -4.5 | 12 of 30 | already the default |
| emis_wide | -2.4 | -4.6 | not comparable | 24 of 30 | no |

<figure>
<img src="figures/fit-accuracy-knobs/parameters-shift.png" alt="Shift of each physics parameter per arm and galaxy in units of the reference posterior half-width">
<figcaption>Parameter shifts against poly3_total, seed band shaded</figcaption>
</figure>

### dust_free

Result
: The only arm that improves the fit and beats the seed floor everywhere. Photometric chi2 falls in five of six galaxies, by 38 on M5_172669, 17 on M1_206545 and 15 on M5_173928. ln Z rises in all six, by +0.8 to +14.8 on identical data.

Dust index
: The Kriek and Conroy index does not want the fixed -0.7. Three galaxies rail at the lower prior edge (M1_206545 -0.988, M5_173928 -0.971, M5_172669 -0.958, half-widths 0.014-0.030), three sit near zero (M12_98104 -0.000 +/- 0.162, M4_108989 +0.021 +/- 0.338, M12_185653 +0.296 +/- 0.105). M12_98104 alone is 4.3 sigma from -0.7.

Physics
: A free index buys the attenuation-curve slope, so tau_dust moves 3.0-5.2 half-widths in every galaxy and log M follows by up to 2.2. The stage-0 finding that the model SED is too red in the near-infrared was a curve-shape problem, not a dust-column problem.

Cost
: `dust_free` cells average 7.6 minutes against 5.8 for the reference, the slowest arm in the run.

### no_irac

Result
: Four of six galaxies barely move. M5_173928 jumps to a different solution: mass-weighted age 4.50 to 3.01 Gyr, log Z -2.23 to -1.49, tau_dust 0.54 to 0.73, at 14.2, 42.1 and 9.7 half-widths.

Reading
: The two solutions differ by 0.19 in ln Z, so the spectrum alone cannot choose between them. IRAC ch1 and ch2 were the only data pinning M5_173928 to the old-and-metal-poor branch. Dropping them makes the remaining ten bands fit worse by 87 in chi2, so the new branch is not better, only unblocked.

Lick
: Mean absolute Lick residual falls from 2.31 to 2.14 sigma, entirely from M5_173928 (2.82 to 1.55). Every other galaxy is unchanged, so this is one galaxy's degeneracy, not a model improvement.

<figure>
<img src="figures/fit-accuracy-knobs/chi2-M5_173928.png" alt="Spectral residuals and photometric pulls per arm for M5_173928">
<figcaption>M5_173928 residuals per arm</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/corner-M5_173928.png" alt="Posterior corner plot of the six arms on M5_173928">
<figcaption>M5_173928 posteriors, no_irac on a separate branch</figcaption>
</figure>

### floor20

Result
: Only M12_98104 was truly railed. Its f_calib goes 9.98 to 14.59 percent and ln Z rises 86.6. M5_173928 sat at 9.01 percent and stays at 8.99 with the ceiling at 20, so it prefers 9 percent and was never railed.

Physics
: On M12_98104 the physics barely moves: age +0.16, log Z -0.13, log M -0.03 half-widths. The extra evidence is bought by the noise model, not by a better spectrum, since Delta chi2 at fixed f = 3 percent is +0.4.

### mask_cn

Result
: Removing the CN and C4668 windows lowers the spectral chi2 by 14 in the median, as removing 114-349 pixels must. [alpha/Fe] moves 4.0 half-widths on M5_172669 and 2.2 on M1_206545, log Z 3.6 on M1_206545.

Lick
: Mean absolute Lick residual rises from 2.31 to 2.47 sigma. Masking the pixels stops the fit from trying, so the predicted CN and C4668 drift further from the catalogue. The arm hides the carbon and nitrogen problem rather than fixing it, and the [alpha/Fe] rail at -0.2 does not clear.

### emis_wide

Result
: Adding [NeIII] 3869, H-epsilon, H-delta and H-gamma to the masked-line list removes 181-488 pixels, and those pixels are the Balmer absorption lines that carry the age. Age moves 13.7 half-widths on M4_108989 (4.61 to 3.03 Gyr) and 4.8 on M1_206545, log M by up to 8.9.

Reading
: The arm was written as an emission-infill test but the switch masks rather than models, so it measures how much the fit depends on the Balmer lines. The answer is: all of it. Any real infill test needs an emission component in the model, not a wider mask.

### sfh_cont

Result
: The StudentT(0, 0.3, df 2) prior on logsfr_ratios raises the mass-weighted age in five of six galaxies and widens every error bar. Delta chi2 is +2.8 in the median and ln Z falls by 0.7 to 6.8 on identical data, so the likelihood prefers the flexible uniform prior.

| galaxy | t_MW uniform [Gyr] | t_MW student [Gyr] | Delta t_MW [Gyr] | Delta in half-widths | half-width uniform | half-width student |
| --- | --- | --- | --- | --- | --- | --- |
| M5_172669 | 1.85 | 2.35 | +0.50 | +5.1 | 0.099 | 0.237 |
| M5_173928 | 4.50 | 4.81 | +0.31 | +2.9 | 0.105 | 0.380 |
| M4_108989 | 4.61 | 4.75 | +0.14 | +1.2 | 0.116 | 0.125 |
| M12_98104 | 4.40 | 4.52 | +0.11 | +0.4 | 0.267 | 0.253 |
| M1_206545 | 5.07 | 5.17 | +0.10 | +7.0 | 0.015 | 0.088 |
| M12_185653 | 5.02 | 4.89 | -0.13 | -0.4 | 0.370 | 0.420 |

Error bars
: The half-width in units of which the shift is quoted is itself the thing the prior fixes. M1_206545 gives 5.065 +/- 0.015 Gyr under the uniform prior, a 0.3 percent age from one LEGA-C spectrum, which is not credible; the continuity prior returns 5.167 +/- 0.088. M5_173928 goes 0.105 to 0.380 and M5_172669 0.099 to 0.237. The shift in half-widths is large mostly because the old denominator was too small.

Late-time tail
: The uniform prior puts spikes at the young end that the data cannot resolve. Under the continuity prior t80 moves later by 2.1-7.1 half-widths in four galaxies and the recent star formation flattens, which is what raises t_MW.

<figure>
<img src="figures/fit-accuracy-knobs/sfh-continuity.png" alt="Star formation history and cumulative mass fraction under the uniform and StudentT ratio priors, per galaxy">
<figcaption>SFH under the two priors, six galaxies</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/sfh-histories.png" alt="Star formation history and cumulative mass fraction for every arm, per galaxy">
<figcaption>SFH per arm, six galaxies</figcaption>
</figure>

Mock
: On the 4 percent tilt mock the continuity prior makes every pull worse: age 0.64 to 1.82, log M 1.38 to 1.89, tau_dust 0.71 to 1.53. The mock truth was drawn from a uniform-prior fit, so its input SFH is spiky by construction and the uniform prior is the matched prior. The mock cannot referee this choice.

<figure>
<img src="figures/fit-accuracy-knobs/mock-sfh-prior.png" alt="Parameter pulls against mock truth and recovered star formation history for the two ratio priors">
<figcaption>Mock tilt4 under the two ratio priors</figcaption>
</figure>

### Sanity checks

Lick
: Mean absolute residual over the available indices, against 2.31 sigma for `poly3_total`: `no_irac` 2.14, `sfh_cont` 2.26, `floor20` 2.34, `dust_free` 2.36, `mask_cn` 2.47, `emis_wide` 2.47. Seed repeats scatter by 0.06, so only `no_irac` moves. The caveat from stage 0 stands: the catalogue indices come from the uncalibrated DR2 spectra.

Borghi+22
: No arm improves the two overlap galaxies. M4_108989 [alpha/Fe] stays at -5.2 sigma in every arm and M12_185653 [alpha/Fe] at +3.6 to +4.1. `dust_free` moves M12_185653 age from 3.5 to 2.9 sigma and [Z/H] from -3.5 to -3.2, inside the seed scatter of the other arms. Borghi's ages are SSP-equivalent against our mass-weighted, so this is a direction, not a test.

<figure>
<img src="figures/fit-accuracy-knobs/lick-by-arm.png" alt="Predicted minus catalogue Lick index over catalogue error, per index, galaxy and arm">
<figcaption>Lick residuals per arm</figcaption>
</figure>

### Verdict

Adopt
: `dust_free`. It is the only arm that improves the data fit, raises ln Z on identical data in every galaxy, and moves a physics parameter well past the seed floor for a reason stage 0 predicted.

Reject
: `mask_cn` and `emis_wide` remove information without fixing what they targeted. `floor20` fixes one galaxy's noise floor and changes no physics. `no_irac` is a diagnostic that found a second solution branch on M5_173928, not a production setting.

Keep
: `sfh_cont` stays the default on Liu Hao's 2026-09-06 call. The measurement here is that it costs a little evidence and buys honest age error bars, three to six times wider on the galaxies whose uniform-prior ages were implausibly tight.

Open
: M5_173928 has two solutions separated by 0.19 in ln Z and 1.5 Gyr in age, held apart only by two IRAC bands. The [alpha/Fe] rail at -0.2 and the carbon and nitrogen deficit survive every arm in this stage.
