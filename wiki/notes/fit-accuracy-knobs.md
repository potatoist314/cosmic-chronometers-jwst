---
title: Fit-accuracy knobs after the calibration polynomial
date: 2026-09-06
section: Analyses
theme: Single-fit accuracy
tags: [calibration, ceridwen, dr2-quiescent-sample, lick-indices]
job:
figures: [stage0_chi2_map.png, stage0_prior_rails.png, stage0_lick_residuals.png, parameters-shift.png, sfh-continuity.png, sfh-histories.png, lick-by-arm.png, mock-sfh-prior.png, chi2-M5_173928.png, corner-M5_173928.png, nd-parameters-shift.png, nd-dust-index.png, nd-sfh-histories.png, nd-lick.png]
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

Default flipped again
: Liu Hao's call on 2026-09-06, after the stage-1 results: the Kriek and Conroy dust index is free with Uniform(-1.0, 0.4), Ceridwen's own documented default (`CERIDWEN_FREE_DUST_INDEX` unset means `1`). The fixed -0.7 was a project-local choice made by an LLM, not by Liu Hao, and the stage-1 posteriors reject it. The `poly3_total` reference arm pins the fixed index so the stored fits stay reproducible. No stored fit has both flips yet.

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

Adopted
: Production default since 2026-09-06 (see "Default flipped again" above). The three galaxies that rail at -1.0 say the prior edge, not the data, sets their slope, so a wider lower bound is a candidate stage-2 arm.

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

## New defaults

Run
: 2026-09-06 22:17 to 2026-09-07 01:45 UTC on one RTX 5060 (offer 48742494, $0.1028/h, instance 50103374, destroyed). 22 fits landed, 1 mock cell aborted. Executed notebook `results/fit-accuracy-knobs/new-defaults.ipynb`; every table below is a CSV beside it.

Reference
: `poly3_total`, the original production model: order-3 marginalised Chebyshev, cosmos_total photometry, uniform SFH prior, Kriek and Conroy index fixed at -0.7, tau_dust Uniform(0, 2). 13 sampled parameters.

Arms
: `new_default` is the notebook with no environment set since 2026-09-06: StudentT(0, 0.3, df 2) on logsfr_ratios and the dust index sampled with Uniform(-1.0, 0.4). 14 parameters. `new_default_rep1` and `rep2` repeat it on M4_108989 and M5_172669 with the base seed shifted by 1000 and 2000. `tau_cn` adds Ceridwen's documented ClippedNormal(0.3, 1.0, 0, 4) on tau_dust. `dust_wide` widens the index to Prospector's alpha range, Uniform(-2.0, 0.5). All arms share the data with the reference, so Delta ln Z is comparable everywhere.

Sampler
: gpu-full profile unchanged (num_live 500, num_inner_steps 65, num_delete 100, logZ_tol -5). Ceridwen's 5 n rule would ask 70 inner steps for 14 parameters; 65 was kept so only the priors differ. Median wall 495 s per fit against 354 s for `poly3_total`; `dust_wide` 539 s, `tau_cn` 489 s. The stored `n_likelihood_calls` is now counted as `logical_including_initialization`, about 7.5 million per fit against about 1.2 million under the old counting, so the two runs cannot be compared on calls.

### Seed floor

Floor
: max |shift| between seed repeats, in half-widths of the reference posterior. Old model from six `seed_rep` fits, new model from four `new_default_rep` fits (M4_108989 and M5_172669 only).

| parameter | old model | new model |
|---|---|---|
| age | 1.20 | 0.34 |
| log Z | 0.49 | 0.54 |
| [alpha/Fe] | 0.96 | 0.23 |
| tau_dust | 0.32 | 0.07 |
| log M | 0.49 | 0.29 |
| dust index | - | 0.15 |
| ln Z spread | 1.99 | 3.13 |

Reading
: the new model is more repeatable on age, [alpha/Fe] and tau_dust because its posteriors are wider, so the same absolute scatter is a smaller fraction of a half-width. The ln Z spread grew to 3.1, so a Delta ln Z under about 3 between two 14-parameter fits is seed noise.

### Per galaxy

Shifts
: `new_default` minus `poly3_total` medians, in reference half-widths, tested against the old floor. `new-defaults-headline.csv` has every column, `new-defaults.csv` the full table.

| galaxy | age old to new (Gyr) | age shift | tau_dust old to new | tau shift | dust index | Delta ln Z |
|---|---|---|---|---|---|---|
| M12_98104 | 4.40 to 4.51 | +0.4 | 0.36 to 0.49 | +3.7 | -0.09 +/- 0.20 | +0.5 |
| M5_173928 | 4.50 to 4.93 | +4.1 | 0.54 to 0.45 | -4.7 | -0.98, 88% within 0.05 of the wall | +5.6 |
| M4_108989 | 4.61 to 4.70 | +0.8 | 0.25 to 0.35 | +3.4 | +0.11 +/- 0.29 | -3.2 |
| M12_185653 | 5.02 to 5.00 | -0.0 | 0.17 to 0.31 | +4.6 | +0.26 +/- 0.14 | +4.0 |
| M1_206545 | 5.06 to 5.16 | +6.8 | 0.46 to 0.39 | -3.2 | -0.99, 98% at the wall | +7.6 |
| M5_172669 | 1.85 to 2.48 | +6.4 | 0.58 to 0.47 | -5.6 | -0.97, 89% at the wall | +9.0 |

Beyond the old floor
: age 3 of 6, log Z 4 of 6, [alpha/Fe] 0 of 6, tau_dust 6 of 6, log M 5 of 6. Only M4_108989 loses evidence, and by an amount inside the new ln Z spread.

Two regimes
: the three galaxies whose index pins to the -1.0 wall (M5_173928, M1_206545, M5_172669) get older by 4 to 7 half-widths and lose tau_dust. A steeper attenuation curve reddens the blue end for less total column, so the fit trades dust for age. The three galaxies whose index settles inside the prior (M12_98104, M4_108989, M12_185653) keep their age and gain tau_dust by 3 to 5 half-widths: the index moves toward Calzetti (0) or flatter, the curve reddens less per unit column, and the fit asks for more column.

Additivity
: the stage-1 `sfh_cont` and `dust_free` shifts add to the `new_default` shift within about 1 half-width on every parameter, except age on M5_172669 (-1.35) and M5_173928 (+1.33), the two galaxies where both priors act on the same young tail (`new-defaults-additivity.csv`).

<figure>
<img src="figures/fit-accuracy-knobs/nd-parameters-shift.png" alt="Shift of each physics parameter from poly3_total to new_default in reference half-widths, per galaxy, with the old and new seed floors">
<figcaption>Parameter shifts of the new defaults against the original production fit; the shaded band is the old seed floor</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/nd-dust-index.png" alt="Posterior of the Kriek and Conroy dust index per galaxy under new_default and dust_wide">
<figcaption>Dust-index posteriors: three galaxies pin to -1.0 under the default bounds and follow the wall to -2.0 when it moves</figcaption>
</figure>

<figure>
<img src="figures/fit-accuracy-knobs/nd-sfh-histories.png" alt="Star-formation histories of the six galaxies under poly3_total and new_default">
<figcaption>Star-formation histories, original production model against the new defaults</figcaption>
</figure>

### tau_cn

Result
: every physics shift is at or below 0.5 half-widths, tau_dust medians are unchanged to two decimals, Delta ln Z between -1.5 and +0.5. With the index free the column posterior sits at 0.3 to 0.5 with a half-width of about 0.05, far inside the ClippedNormal's 1.0 sigma, so the prior has nothing to act on.

Verdict
: reject, no effect.

### dust_wide

Result
: the three wall-pinned galaxies follow the wall. M1_206545 goes from -0.99 to -1.90 (58% within 0.1 of -2.0), Delta ln Z +24, tau_dust 0.39 to 0.20, log Z +4.6 half-widths, [alpha/Fe] +2.0. M5_173928 goes to -1.75 (20% at the wall), Delta ln Z +31, age -4.4, log Z +24, tau_dust 0.45 to 0.30. M4_108989 flips from +0.11 to a bimodal posterior at -1.94 (78% at the wall), Delta ln Z +28, age -6.0, log Z +12, tau_dust 0.35 to 0.17, raw spectral chi2 -122. M5_172669 settles off the wall at -1.14 +/- 0.08 with Delta ln Z 0. M12_98104 and M12_185653 do not move.

Reading
: an index of -1.0 is already the steepest curve in Prospector's template library and -2.0 is far outside anything measured in attenuation studies. A parameter that runs to whatever wall it is given, with the evidence rising all the way, is a continuum-tilt nuisance the polynomial does not absorb, not a dust measurement. For quiescent galaxies with tau_dust 0.2 to 0.5 the tilt from the index and the tilt from age are degenerate, which is why age and log Z jump by tens of half-widths.

Sanity
: Lick mean |residual| falls from 2.31 to 1.97 (M4_108989 3.61 to 2.48, M5_173928 2.61 to 1.56), but the Borghi+22 comparison on M4_108989 flips [Z/H] from -1.67 sigma to +3.32 sigma. Better line fits at the cost of an unphysical dust curve and an unrecognisable metallicity.

Verdict
: reject as a production setting. Recommend a tight prior on the index instead of the flat Uniform(-1.0, 0.4): Normal(-0.3, 0.3) clipped to [-1, 0.4], or revert to the fixed -0.7 and accept the stage-1 chi2 penalty. Decide after the DR2-wide refit shows how many galaxies pin.

### Sanity checks

Lick
: mean |residual| over all indices and galaxies: `poly3_total` 2.32, `new_default` 2.31, `tau_cn` 2.32, `sfh_cont` 2.27, `dust_free` 2.36. Seed scatter is about 0.05, so no arm moves the Lick agreement.

Borghi+22
: `new_default` on M12_185653 disagrees by 3.6 sigma in age, -3.7 in [Z/H], +3.8 in [alpha/Fe]; on M4_108989 by 1.1, -1.7, -5.3 against 0.95, -1.34, -5.19 for `poly3_total`. Unchanged within the run-to-run noise (`borghi-new-defaults.csv`).

<figure>
<img src="figures/fit-accuracy-knobs/nd-lick.png" alt="Predicted minus catalogue Lick index over catalogue error, per index, galaxy and arm, for poly3_total, new_default, tau_cn and dust_wide">
<figcaption>Lick residuals for the new-defaults arms</figcaption>
</figure>

### Mock

Status
: `mock_tilt4_new_default` did not run. The stored tilt-4 truth has no `diffuse_dust_index`, so the free-index mock check aborted before sampling (two attempts, 60 s). Only `mock_tilt4_poly3` (age pull 0.64) and `mock_tilt4_sfh_cont` (1.82) exist. A new mock truth with a dust index is needed before the new defaults can be checked on a mock.

### Bookkeeping

Spend
: the runner's counter read $1.63 for this run because it measures the whole-account credit drop, and the independent DR2-wide refit was renting two boxes at the same time. This run's own cost at $0.1028/h for 3.5 h is about $0.36.

Derived summary
: the h5 `summary/parameter` block does not carry `diffuse_dust_index`. The notebook reads it from the posterior samples through `pgd.load_galaxy` with `pgd.posterior_weights`.

Offer rule
: after this run Liu Hao fixed the Vast rule: RTX 5060 or 5060 Ti only, under $0.10/h, reliability above 99.5%. It is now `fit_offer_qualifies` in `scripts/sweep_ceridwen_vast_gpus.py`, shared by every fit runner (commit 0b55f35). The offer used here, $0.1028/h, would no longer qualify.

### Verdict

Keep
: the new defaults. Six of six galaxies move tau_dust past the old floor, five of six gain evidence on identical data, and the direction of every shift follows from the attenuation-curve slope. Lick and Borghi agreement is unchanged, so the gain is in the dust and age posteriors, not in the line fits.

Reject
: `tau_cn`, no effect. `dust_wide`, unphysical wall-chasing.

Open
: the flat index prior lets three of six galaxies pin at -1.0. A tight prior or a fixed value is the next decision, after the DR2-wide refit reports the pinned fraction. A mock truth with a dust index is needed to test truth recovery under the new defaults.
