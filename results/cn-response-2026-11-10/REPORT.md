# C/N responses and injection recovery

All 78 real-data fits and 27 plain-grid mock recoveries are retrieved and independently validated. Every owned background job has finished and no owned Modal container remains.

## Experiment 3 results

Free C/N raises the paired median [α/Fe] by +0.032 dex in LEGA-C, +0.200 dex in full-range MaNGA and +0.097 dex in the MaNGA rest window. The carbon mask still moves [α/Fe] with C/N free: +0.028, +0.011 and +0.025 dex, respectively. The paired LEGA-C age change from masking is +0.361 Gyr.

The median LEGA-C Mg b and C2 pulls improve, but remain negative. Full-range MaNGA has a near-zero median Mg b pull while C2 remains negative and CN4150 changes sign. The window fits retain substantial negative Mg b and C2 pulls. Full-range MaNGA diffuse dust remains close to its upper prior bound: median τ ≈ 0.994, with τ > 0.99 in 5/8 baseline and 6/8 C/N fits. No priors or masks were retuned.

The LEGA-C response depends on Mg b coverage. In the five covered galaxies, [α/Fe] rises in 5/5 and age falls in 4/5; median C/Fe is +0.287 and N/Fe is −0.020. In the five without Mg b, [α/Fe] falls in 4/5 and age rises in 4/5; median C/Fe is −0.230 and N/Fe is +0.222. Offsets use the adopted response approximation.

Group medians. Age is in Gyr; abundances are in dex; τ is `diffuse_tau_noll`.

| group | arm | n | afe | C/Fe | N/Fe | age | Fe/H | τ | lnZ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| legac | baseline | 10 | -0.022 | — | — | 4.161 | -0.270 | 0.448 | 235552.5 |
| legac | cn | 10 | 0.004 | -0.002 | 0.110 | 3.969 | -0.312 | 0.448 | 235572.9 |
| legac | cn_carbon_mask | 10 | 0.045 | -0.202 | 0.268 | 4.450 | -0.462 | 0.448 | 201194.4 |
| manga-full | baseline | 8 | 0.199 | — | — | 9.352 | -0.196 | 0.994 | 260066.3 |
| manga-full | cn | 8 | 0.361 | 0.089 | 0.299 | 10.484 | -0.350 | 0.995 | 260163.1 |
| manga-full | cn_carbon_mask | 8 | 0.383 | 0.064 | 0.350 | 11.588 | -0.385 | 0.994 | 247822.2 |
| manga-window | baseline | 8 | 0.138 | — | — | 8.704 | -0.301 | 0.474 | 78148.5 |
| manga-window | cn | 8 | 0.226 | 0.103 | 0.003 | 7.603 | -0.337 | 0.465 | 78155.7 |
| manga-window | cn_carbon_mask | 8 | 0.255 | -0.001 | 0.161 | 9.142 | -0.429 | 0.465 | 65756.2 |

Band-summed pulls divided by sqrt(n). Parentheses give galaxies with fitted band pixels.

| group | arm | Mg b | C2 4668 | CN4150 | G4300 | Fe4383 |
|---|---|---:|---:|---:|---:|---:|
| legac | baseline | -4.13 (5) | -3.59 (9) | -1.57 (10) | 1.21 (10) | -0.35 (10) |
| legac | cn | -2.23 (5) | -2.97 (9) | -0.71 (10) | 1.44 (10) | -0.79 (10) |
| legac | cn_carbon_mask | -2.69 (5) | — | — | — | — |
| manga-full | baseline | -0.56 (8) | -5.08 (8) | -1.39 (8) | 1.51 (8) | 1.05 (8) |
| manga-full | cn | 0.27 (8) | -4.78 (8) | 1.89 (8) | 0.92 (8) | -0.75 (8) |
| manga-full | cn_carbon_mask | 0.25 (8) | — | — | — | — |
| manga-window | baseline | -4.89 (8) | -8.39 (8) | -1.36 (8) | 1.99 (8) | -2.45 (8) |
| manga-window | cn | -3.26 (8) | -7.38 (8) | -0.61 (8) | 2.47 (8) | -2.26 (8) |
| manga-window | cn_carbon_mask | -3.64 (8) | — | — | — | — |

Medians of matched-galaxy differences; these differ from differences between group medians. Evidence changes use identical fitted pixels.

| group | n | C/N − baseline afe | age | Fe/H | lnZ | mask − C/N afe | age | Fe/H |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| legac | 10 | 0.032 | 0.007 | -0.063 | 17.06 | 0.028 | 0.361 | -0.041 |
| manga-full | 8 | 0.200 | 0.656 | -0.175 | 130.14 | 0.011 | 0.974 | -0.022 |
| manga-window | 8 | 0.097 | -1.092 | -0.016 | 13.66 | 0.025 | 1.516 | -0.099 |

All galaxies and intervals: [per-galaxy table](exp3-per-galaxy.csv). [Group medians](exp3-medians.csv). [Matched changes](exp3-paired-changes.csv).

## Experiment 4 results

Within these mocks, omitted C/N biases [α/Fe] downward. Carbon-only injections make the recovered age older; nitrogen-only injections make it younger. At C/Fe=+0.15, N/Fe=+0.30, the paired changes from zero injection are −0.169 dex in [α/Fe], −0.114 Gyr in age and +0.139 dex in [Fe/H]. At +0.30/+0.60, they are −0.338 dex, −0.285 Gyr and +0.249 dex.

The task records carbon-mask shifts of about +0.13 dex and +0.32 Gyr. The moderate injection has a comparable [α/Fe] effect but a smaller age effect. The strongest injection has an age effect near that scale but a substantially larger [α/Fe] effect. Neither tested case reproduces both median shifts together. The individual paired age shifts are −0.159…−0.040 Gyr for +0.15/+0.30 and −0.360…−0.240 Gyr for +0.30/+0.60 across the three seeds.

No nonzero tested pair reproduces the median signs of all five observed M1_210210 bands. The real baseline pulls are Mg b −4.19, C2 −6.10, CN4150 −4.31, G4300 +4.21 and Fe4383 +2.14. All carbon-positive cases have negative median G4300 pulls. Nitrogen without carbon can make G4300 positive, but its C2 pull is positive. These injections therefore reproduce part of the downward [α/Fe] bias, with a C/N-dependent age bias, rather than the full observed residual pattern.

Medians over three noise seeds. Bias is recovered median minus recorded truth. Age is in Gyr and abundances are in dex.

| C/Fe injected | N/Fe injected | afe recovered | age recovered | Fe/H recovered | afe bias | age bias | Fe/H bias |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.199 | 3.579 | -0.222 | -0.001 | -0.010 | -0.022 |
| 0.000 | 0.300 | 0.140 | 2.726 | -0.090 | -0.060 | -0.863 | 0.110 |
| 0.000 | 0.600 | 0.087 | 2.268 | 0.026 | -0.113 | -1.320 | 0.226 |
| 0.150 | 0.000 | 0.086 | 4.190 | -0.191 | -0.114 | 0.601 | 0.009 |
| 0.150 | 0.300 | 0.030 | 3.466 | -0.083 | -0.170 | -0.123 | 0.117 |
| 0.150 | 0.600 | -0.033 | 2.602 | 0.025 | -0.233 | -0.987 | 0.225 |
| 0.300 | 0.000 | -0.050 | 4.498 | -0.149 | -0.250 | 0.909 | 0.051 |
| 0.300 | 0.300 | -0.096 | 3.908 | -0.060 | -0.296 | 0.319 | 0.140 |
| 0.300 | 0.600 | -0.140 | 3.340 | 0.025 | -0.340 | -0.249 | 0.225 |

Band-summed pulls divided by sqrt(n), medians over the same three seeds.

| C/Fe injected | N/Fe injected | Mg b | C2 4668 | CN4150 | G4300 | Fe4383 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.00 | -0.33 | -0.57 | 0.03 | -1.32 | 0.41 |
| 0.00 | 0.30 | -0.36 | 1.54 | -3.22 | -0.33 | 1.39 |
| 0.00 | 0.60 | -0.46 | 3.41 | -6.26 | 0.59 | 2.22 |
| 0.15 | 0.00 | -1.56 | -2.17 | -0.99 | -2.65 | 0.40 |
| 0.15 | 0.30 | -1.65 | -0.08 | -4.10 | -1.85 | 1.32 |
| 0.15 | 0.60 | -1.96 | 2.17 | -6.75 | -1.07 | 2.27 |
| 0.30 | 0.00 | -3.25 | -3.55 | -1.72 | -4.15 | 0.60 |
| 0.30 | 0.30 | -3.33 | -1.28 | -4.46 | -3.30 | 1.35 |
| 0.30 | 0.60 | -3.57 | 0.92 | -7.02 | -2.46 | 2.05 |

[All 27 recoveries and intervals](injection/per-mock.csv). [Medians, absolute biases and same-seed zero-injection differences](injection/medians.csv). [Truth, input hashes and seeds](injection/mocks.json).

### Injection choices

A single recorded 14-bin SFH uses the M1_210210 baseline posterior medians for SFH, dust and mass. Truth [α/Fe]=+0.2, mass-weighted [Fe/H]=−0.2 and catalogue dispersion 259.5 km/s are set explicitly. The true mass-weighted age is 3.588756 Gyr. C/Fe takes 0, +0.15, +0.30 and N/Fe takes 0, +0.30, +0.60 dex. Isochrones are unchanged. The native wavelength grid, filters, instrument, masks and statistical uncertainties come from M1_210210.

Gaussian noise uses seeds 20261111, 20261112 and 20261113, with identical standardized draws across C/N at each seed. Spectrum variance is the recorded statistical variance plus the squared true model-scaled calibration floor (2.377%). Photometric draws use 5% of true model flux; recovery keeps the normal observed-flux floor. The true calibration polynomial is unity and emission-line amplitudes are zero. Median spectral statistical S/N is 64.9–66.6; total S/N is 35.3–35.6. Recovery uses the plain grid, production priors and inference seed 20261110. NPZ inputs carry synthetic fluxes and the target’s unchanged statistical uncertainties.

Recovery source: Astro `5be040e`, Ceridwen `13791e0`. Generation records Astro `99c179ba`; its notebook and generator blobs are identical to `5be040e`. All 27 input hashes, units, shapes and finite arrays were checked. Zero-injection mean spectrum and photometry are bitwise equal to the plain-grid prediction. The mock test covers this one SFH and nonnegative C/N offsets through the same independent-response prescription used for fitting.

## Model and run record

Science source: Astro `0a419b8`, Ceridwen `13791e0`; alf `cda32111c721efe586945d7dfcb9f605a9f6a105`. The four experiment configurations record seed 20261110. Baseline uses the existing target configuration. `cn` adds only C/N freedom. `cn_carbon_mask` also excludes CN4150, G4300, Fe4383 and C4668. MaNGA runs use either their existing full range or rest 3860–5330 Å. Production priors, SFH, calibration, emission-line marginalisation and isochrones are unchanged. C/N are sampled because their multiplicative response depends on SFH, metallicity and both abundances. Their priors are C/Fe = −0.3…+0.5 and N/Fe = −0.3…+1 dex. The SFH basis fast path remains active. The default response setting is off.

The unchanged Kroupa files contain vacuum wavelengths and L_lambda in L_sun/um. Zero-based columns 8/9 give C ±0.15 dex, and 11/12 give N ±0.3 dex. The loader converts to proportional F_nu before smoothing. It interpolates flux in log age and metallicity, clamps to the response endpoints (1–13 Gyr, −1.5…0 dex), and excludes the broken +0.2 files as alf does. See the pinned [alf manual](https://github.com/cconroy20/alf/blob/cda32111c721efe586945d7dfcb9f605a9f6a105/doc/alf.pdf), [setup](https://github.com/cconroy20/alf/blob/cda32111c721efe586945d7dfcb9f605a9f6a105/src/setup.f90), and [response interpolation](https://github.com/cconroy20/alf/blob/cda32111c721efe586945d7dfcb9f605a9f6a105/src/add_response.f90); [Conroy et al. 2018](https://arxiv.org/abs/1801.10185).

Base and enhanced spectra are separately broadened from their native 100 km/s to the catalogue stellar dispersion plus instrument LSF. Their ratio multiplies the already broadened Park spectrum. The response is fixed at catalogue dispersion; the Park dispersion remains sampled. Across all 18 targets, catalogue total dispersion exceeds 100 km/s. The largest one-sigma change in the response is 1.280% at one pixel, 0.0542% RMS, and 0.0966% at the 95th percentile, measured over the fitted pixels and all response age/metallicity templates at C=N=+0.3 dex. The lower three-sigma dispersion tail of 8999-12702 reaches 98.685 km/s; that tail cannot be represented by the native response library. Per-target checks are in `validation.json`.

Independent C and N responses are multiplied, with unity outside the response wavelength coverage. Photometry uses the unsmoothed ratio. The public files have no joint C+N column, and their nominal joint-alpha column is identically zero in all 25 Kroupa files. Thus these files cannot establish that individual responses reproduce a joint abundance change, especially its continuum; alf itself fits continuum-normalised spectra. Injection through the same prescription tests fitting bias within this approximation, not its independent physical validity. [Park et al. 2025, §§2.4 and 3.2.3](https://arxiv.org/abs/2410.21375) is the lockstep-alpha reference.

## Table definitions

`exp3-per-galaxy.csv` contains all 78 fits. Scalar parameters use weighted nested-sampling quantiles; mass-weighted age uses the notebook's 400 resampled posterior histories. `exp3-medians.csv` gives medians over galaxies. Baseline C/N columns are empty because they are fixed at zero. `exp3-paired-changes.csv` compares the same galaxy between arms.

Band metric: sum of stored (observed − fitted)/effective-uncertainty pulls divided by sqrt(number of fitted band pixels), following `results/afe-feh-investigation-2026-10-13/REPORT.md`, section 1. Band definitions come from `ceridwen.observation.absorption_features`; negative means the model absorption is too weak. A band with no fitted pixels is empty, including carbon bands in the mask arm. Evidence is comparable only between baseline and C/N on the same pixels; masked and unmasked lnZ are not comparable.

## Baseline preservation and requested test checks

The initial zero-response test compared zero C/N against default-off **within Ceridwen 13791e0**. A separate cross-pin check then compared default-off Astro `0a419b8` / Ceridwen `13791e0` against Astro `9b189a36` / Ceridwen `a0b1f6e`, loaded from isolated worktrees. On real M1_210210 data, all 12 spectrum and photometry arrays were bitwise identical: eager and JIT predictions at three parameter points. Arrays, import paths and logs are in `validation/`. The later synthetic-reader change at Astro `5be040e`, with both options off, also preserves all 12 arrays bitwise.

Both existing tests below fail at both revisions. Existing tests were not edited.

- `test_notebook_uses_production_model_and_sampler_contract`: `AssertionError` at `tests/test_ceridwen_dr2_production.py:125`; `At index 2 diff: 'CERIDWEN_PLOTS' != 'CERIDWEN_RANDOM_SEED'`; `Left contains one more item: 'CERIDWEN_TARGET_ID'`.
- `test_constant_calibration_active_assembly_and_exports`: `NameError: name 'mass_mapped_beta' is not defined`; old assembly line 75, new assembly line 83.

The exact outputs are in `validation/baseline-existing-tests.log` and `validation/current-existing-tests.log`; `validation/cross-pin-checks.txt` records the comparison. Focused response/fast-path tests: 35 passed. The wider selected suite: 106 passed, these two pre-existing failures. Existing wiki test failures are recorded in `validation.json`. Synthetic-input and related production checks: 62 passed. The final 105-artifact check verifies stored result/derived hashes, unchanged mock inputs and zero image outputs.

## Noticed, not done

Ca offsets; experiments 1, 2 and the full-sample chronometer experiment 5 (owned by the lead/other worker); pre-existing production/wiki test faults. The existing model-page photometry row still says 12 bands. Visual wiki check: Not tested. On the M1, `freespace` opened no new Safari window and macOS denied Apple Events (`-1743`). Live NAS text readback passed. No new figures or wiki result pages.

## Experiment 6 results

C/N freedom removes the large injection-dependent [alpha/Fe] bias with the full spectrum. The red cut leaves a smaller negative [alpha/Fe] bias. Neither arm fully recovers N/Fe. The carbon mask does not remove the [alpha/Fe] or age biases.

- **With Mg b in range (A):** truth lies inside the 16–84% interval in 27/27 fits for [alpha/Fe], mass-weighted age, [Fe/H] and C/Fe. Across the nine injections, median biases are −0.004…−0.001 dex, −0.230…−0.038 Gyr and −0.006…+0.007 dex for [alpha/Fe], age and [Fe/H]. N/Fe is low by 0.053–0.072 dex; its truth is inside 9/27 intervals.
- **With the red cut (C):** age, [Fe/H] and C/Fe truth remain inside 27/27 intervals; [alpha/Fe] truth is inside 19/27. Median biases are −0.020…−0.017 dex, −0.231…−0.080 Gyr and −0.008…+0.009 dex. The zero-C/N control already has [alpha/Fe] bias −0.017 dex and age bias −0.220 Gyr. N/Fe is low by 0.058–0.077 dex; its truth is inside 9/27 intervals.
- **Carbon mask (D):** at C/Fe=+0.30, N/Fe=+0.60, [alpha/Fe] bias is −0.329 dex, versus −0.340 dex for the plain full-range arm. Only 2/27 [alpha/Fe] intervals contain truth in either arm. Masked median age biases still span −0.898…+0.553 Gyr; age truth is inside 16/27 intervals, versus 11/27 for the plain full-range arm.
- **C/Fe sign without Mg b:** all 18 positive-carbon injections have positive fitted C/Fe medians. Five of nine zero-carbon fits have negative medians, but none has its 84th percentile below zero. Only two of the nine injection-cell medians are negative, both about −0.001 dex at zero injected carbon. The real no-Mg-b fits have four negative medians out of five, −0.261…−0.207 dex, all with their 84th percentile below zero. These mocks do not reproduce that negative-C/Fe pattern.

### Inputs, cut and table definitions

The 27 experiment-4 NPZ inputs and hashes are unchanged. Inference seed 20261110, production priors, photometry and the SFH-basis fast path are retained. The cut uses notebook `rest_range = [0.0, 5015.155244540448]` Å: the red limit is the median fitted rest-frame red edge of M4_107370, M3_117010, M8_161113, M5_238314 and M14_37219. The zero lower limit leaves the original blue coverage unchanged. [Input hashes and individual red edges](injection-arms/inputs-and-cut.json).

Actual fitted spectrum pixels are 3607 for A, 3050 for B/C and 3034 for D. A/D retain 89 Mg b pixels; B/C retain zero. B/C retain all four carbon bands. D excludes CN4150, G4300, Fe4383 and C4668 completely. No notebook or model code changes were needed. All 108 saved fits passed artifact and diagnostic checks; executed notebooks contain no image outputs. Own Modal apps have no active containers. [Artifact checks](injection-arms/artifact-checks.json), [configuration checks](injection-arms/configuration-checks.json), [Modal state](injection-arms/modal-state.json).

Each row below is a median over the same three noise seeds, following the experiment-4 table. Truth is [alpha/Fe]=+0.2 dex, mass-weighted age=3.588756 Gyr and [Fe/H]=−0.2 dex. Bias is recovered median minus truth. Ages are in Gyr; abundances are in dex. The 27 fits reuse three common noise realisations across nine injections.

For C/Fe and N/Fe, each displayed q16/q50/q84 is the median of the corresponding three per-seed quantiles; these are not pooled-posterior intervals. “Truth inside” is the number of individual fits whose unrounded 16–84% interval contains the injected value, out of three. [All 108 individual recoveries and intervals](injection-arms/per-mock.csv), [36 injection-cell medians](injection-arms/medians.csv), [five-arm biases](injection-arms/five-arm-biases.csv), [coverage and sign checks](injection-arms/recovery-checks.json).

### A: C and N free, full range

| C/Fe injected | N/Fe injected | afe recovered | age recovered | Fe/H recovered | afe bias | age bias | Fe/H bias | C/Fe q50 [q16, q84]; truth inside | N/Fe q50 [q16, q84]; truth inside |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.197 | 3.378 | -0.200 | -0.003 | -0.211 | 0.000 | 0.013 [-0.012, 0.035]; 3/3 | -0.069 [-0.116, -0.026]; 1/3 |
| 0.000 | 0.300 | 0.196 | 3.415 | -0.206 | -0.004 | -0.174 | -0.006 | 0.013 [-0.011, 0.035]; 3/3 | 0.247 [0.208, 0.284]; 1/3 |
| 0.000 | 0.600 | 0.198 | 3.551 | -0.203 | -0.002 | -0.038 | -0.003 | 0.012 [-0.012, 0.032]; 3/3 | 0.543 [0.503, 0.584]; 1/3 |
| 0.150 | 0.000 | 0.199 | 3.483 | -0.200 | -0.001 | -0.106 | 0.000 | 0.163 [0.143, 0.185]; 3/3 | -0.071 [-0.117, -0.028]; 1/3 |
| 0.150 | 0.300 | 0.197 | 3.512 | -0.194 | -0.003 | -0.077 | 0.006 | 0.164 [0.141, 0.186]; 3/3 | 0.244 [0.208, 0.279]; 1/3 |
| 0.150 | 0.600 | 0.198 | 3.482 | -0.197 | -0.002 | -0.107 | 0.003 | 0.161 [0.138, 0.182]; 3/3 | 0.539 [0.502, 0.580]; 1/3 |
| 0.300 | 0.000 | 0.199 | 3.359 | -0.193 | -0.001 | -0.230 | 0.007 | 0.312 [0.290, 0.335]; 3/3 | -0.072 [-0.114, -0.030]; 1/3 |
| 0.300 | 0.300 | 0.199 | 3.455 | -0.197 | -0.001 | -0.134 | 0.003 | 0.309 [0.286, 0.332]; 3/3 | 0.241 [0.206, 0.276]; 1/3 |
| 0.300 | 0.600 | 0.197 | 3.461 | -0.194 | -0.003 | -0.128 | 0.006 | 0.314 [0.290, 0.337]; 3/3 | 0.534 [0.493, 0.576]; 1/3 |

### B: plain grid, red cut

| C/Fe injected | N/Fe injected | afe recovered | age recovered | Fe/H recovered | afe bias | age bias | Fe/H bias |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.188 | 3.557 | -0.219 | -0.012 | -0.032 | -0.019 |
| 0.000 | 0.300 | 0.123 | 2.781 | -0.103 | -0.077 | -0.808 | 0.097 |
| 0.000 | 0.600 | 0.063 | 2.350 | -0.002 | -0.137 | -1.239 | 0.198 |
| 0.150 | 0.000 | 0.061 | 4.149 | -0.191 | -0.139 | 0.560 | 0.009 |
| 0.150 | 0.300 | -0.019 | 3.279 | -0.096 | -0.219 | -0.310 | 0.104 |
| 0.150 | 0.600 | -0.086 | 2.554 | -0.009 | -0.286 | -1.035 | 0.191 |
| 0.300 | 0.000 | -0.095 | 4.373 | -0.163 | -0.295 | 0.784 | 0.037 |
| 0.300 | 0.300 | -0.160 | 3.560 | -0.094 | -0.360 | -0.029 | 0.106 |
| 0.300 | 0.600 | -0.193 | 2.973 | -0.021 | -0.393 | -0.615 | 0.179 |

### C: C and N free, red cut

| C/Fe injected | N/Fe injected | afe recovered | age recovered | Fe/H recovered | afe bias | age bias | Fe/H bias | C/Fe q50 [q16, q84]; truth inside | N/Fe q50 [q16, q84]; truth inside |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.183 | 3.368 | -0.205 | -0.017 | -0.220 | -0.005 | 0.002 [-0.027, 0.029]; 3/3 | -0.058 [-0.108, -0.011]; 1/3 |
| 0.000 | 0.300 | 0.183 | 3.509 | -0.206 | -0.017 | -0.080 | -0.006 | -0.001 [-0.031, 0.026]; 3/3 | 0.242 [0.204, 0.279]; 1/3 |
| 0.000 | 0.600 | 0.180 | 3.500 | -0.208 | -0.020 | -0.089 | -0.008 | -0.001 [-0.028, 0.024]; 3/3 | 0.534 [0.492, 0.577]; 1/3 |
| 0.150 | 0.000 | 0.183 | 3.434 | -0.208 | -0.017 | -0.155 | -0.008 | 0.155 [0.126, 0.181]; 3/3 | -0.070 [-0.123, -0.020]; 1/3 |
| 0.150 | 0.300 | 0.183 | 3.460 | -0.199 | -0.017 | -0.128 | 0.001 | 0.157 [0.131, 0.183]; 3/3 | 0.242 [0.201, 0.280]; 1/3 |
| 0.150 | 0.600 | 0.182 | 3.377 | -0.197 | -0.018 | -0.212 | 0.003 | 0.151 [0.125, 0.178]; 3/3 | 0.536 [0.496, 0.576]; 1/3 |
| 0.300 | 0.000 | 0.183 | 3.416 | -0.195 | -0.017 | -0.173 | 0.005 | 0.302 [0.274, 0.332]; 3/3 | -0.077 [-0.127, -0.027]; 1/3 |
| 0.300 | 0.300 | 0.182 | 3.357 | -0.193 | -0.018 | -0.231 | 0.007 | 0.306 [0.277, 0.336]; 3/3 | 0.238 [0.197, 0.281]; 1/3 |
| 0.300 | 0.600 | 0.181 | 3.418 | -0.191 | -0.019 | -0.171 | 0.009 | 0.305 [0.277, 0.335]; 3/3 | 0.541 [0.500, 0.588]; 1/3 |

### D: plain grid, carbon mask

| C/Fe injected | N/Fe injected | afe recovered | age recovered | Fe/H recovered | afe bias | age bias | Fe/H bias |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | 0.198 | 3.586 | -0.243 | -0.002 | -0.003 | -0.043 |
| 0.000 | 0.300 | 0.133 | 3.291 | -0.136 | -0.067 | -0.298 | 0.064 |
| 0.000 | 0.600 | 0.073 | 2.691 | -0.015 | -0.127 | -0.898 | 0.185 |
| 0.150 | 0.000 | 0.097 | 3.943 | -0.211 | -0.103 | 0.354 | -0.011 |
| 0.150 | 0.300 | 0.035 | 3.663 | -0.114 | -0.165 | 0.075 | 0.086 |
| 0.150 | 0.600 | -0.032 | 3.434 | -0.012 | -0.232 | -0.154 | 0.188 |
| 0.300 | 0.000 | -0.025 | 4.141 | -0.173 | -0.225 | 0.553 | 0.027 |
| 0.300 | 0.300 | -0.080 | 3.983 | -0.086 | -0.280 | 0.394 | 0.114 |
| 0.300 | 0.600 | -0.129 | 3.750 | 0.008 | -0.329 | 0.161 | 0.208 |

### Five-arm bias comparison

Each cell is the median [alpha/Fe] bias in dex / age bias in Gyr, against truth.

| C/Fe injected | N/Fe injected | Plain full (Exp. 4) | A: free full | B: plain cut | C: free cut | D: carbon mask |
|---:|---:|---:|---:|---:|---:|---:|
| 0.000 | 0.000 | -0.001 / -0.010 | -0.003 / -0.211 | -0.012 / -0.032 | -0.017 / -0.220 | -0.002 / -0.003 |
| 0.000 | 0.300 | -0.060 / -0.863 | -0.004 / -0.174 | -0.077 / -0.808 | -0.017 / -0.080 | -0.067 / -0.298 |
| 0.000 | 0.600 | -0.113 / -1.320 | -0.002 / -0.038 | -0.137 / -1.239 | -0.020 / -0.089 | -0.127 / -0.898 |
| 0.150 | 0.000 | -0.114 / 0.601 | -0.001 / -0.106 | -0.139 / 0.560 | -0.017 / -0.155 | -0.103 / 0.354 |
| 0.150 | 0.300 | -0.170 / -0.123 | -0.003 / -0.077 | -0.219 / -0.310 | -0.017 / -0.128 | -0.165 / 0.075 |
| 0.150 | 0.600 | -0.233 / -0.987 | -0.002 / -0.107 | -0.286 / -1.035 | -0.018 / -0.212 | -0.232 / -0.154 |
| 0.300 | 0.000 | -0.250 / 0.909 | -0.001 / -0.230 | -0.295 / 0.784 | -0.017 / -0.173 | -0.225 / 0.553 |
| 0.300 | 0.300 | -0.296 / 0.319 | -0.001 / -0.134 | -0.360 / -0.029 | -0.018 / -0.231 | -0.280 / 0.394 |
| 0.300 | 0.600 | -0.340 / -0.249 | -0.003 / -0.128 | -0.393 / -0.615 | -0.019 / -0.171 | -0.329 / 0.161 |

## Experiment 7 results

| Definition | Value |
|---|---|
| Inputs | 135 October baseline fits and 135 C/N-free fits. Loader paths from the other job’s [analysis.ipynb](../chronometer-135-2026-11-10/analysis.ipynb), read only. |
| Groups | 61 galaxies with fitted Mg b pixels; 74 without. Membership comes from the baseline and agrees between arms. |
| Stored pull | (observed − posterior-median fitted spectrum) / effective uncertainty. Paired masks, observed fluxes, wavelengths and redshifts agree for all 135 galaxies. |
| Rest grid | Vacuum wavelength = stored observed vacuum wavelength / (1 + stored redshift). Bin width 2 Å; centres 2900–5950 Å. |
| Stack | Existing native-pixel binning: mean fitted pull per galaxy per bin, then equal-galaxy median. Excluded pixels and empty bins stay NaN. No interpolation. CSV includes every bin and its galaxy count. |
| Feature metric | Sum of native fitted band pulls / sqrt(number of fitted band pixels), then median across galaxies. Empty bands have zero galaxies. All 29 [defined features](../../ceridwen/ceridwen/observation/absorption_features.py) are included; line windows use the existing ±1000 km/s default. |
| Off-feature ranking | 15 non-overlapping 10 Å intervals per arm. Score is the largest absolute mean of five stacked 2 Å bins across the two groups. Ranking uses the existing minimum of 10 galaxies in every bin; all lower-coverage stacks remain in the CSV. Both group values and minimum–maximum counts are shown. |
| Excluded ranking windows | Every defined vacuum feature window and the actual masked emission-line windows: vacuum centres 3934.77, 3966.60, 3973.30, 4227.92 Å, each ±1500 km/s. Modelled emission lines are not treated as masked lines. |
| Candidate labels | Cited atomic-line coincidences inside the selected interval, not established causes of its residual. Published air wavelengths use the existing air2vac conversion. Other intervals remain unidentified. [Source wavelengths](residual-stack/candidate-identifications.json). |
| Group differences | Baseline only. Delta = median without Mg b − median with Mg b. Native metric matches table 1. Matched metric uses each galaxy’s mean pull on fixed common 2 Å bins wholly inside the band; only galaxies finite on every selected bin enter. |
| Bootstrap | 10000 independent galaxy resamples within each group; pointwise 95% percentile intervals. Seeds are 20261111 + zero-based feature index for native metrics, and 20262111 + index for matched metrics. |
| Chi-square excess | Spectral native fitted pixels only: E = sum(pull² − 1) = chi-square − pixel count. Fractions are signed regional E / total E, with no clipping. Carbon is the union of CN4150, G4300, Fe4383 and C4668. Elsewhere includes every other fitted pixel. Each arm retains its own stored effective uncertainty. |
| Saved data | [Stacks](residual-stack/stacks.csv), [feature table](residual-stack/features.csv), [per-galaxy band metrics](residual-stack/per-galaxy-features.csv), [intervals](residual-stack/intervals.csv), [group differences](residual-stack/group-differences.csv), [chi-square partition](residual-stack/chi2-excess.csv). |
| Evidence | All 270 input hashes unchanged. All 6104 stack rows independently reproduced with histogram binning. [Inputs and methods](residual-stack/inputs-and-methods.json), [checks](residual-stack/checks.json). No fits, GPU, figures, wiki pages, model or notebook changes. |
| Noticed, not done | Existing state-checker failure at an absent temporary worktree; no repair. |

### 1. Defined feature residuals

| Feature | Vacuum rest window, Å | Baseline with Mg b: metric (N) | Baseline without Mg b: metric (N) | C/N free with Mg b: metric (N) | C/N free without Mg b: metric (N) |
|---|---|---|---|---|---|
| H10 | 3786.30–3811.65 | -0.245 (17) | -2.524 (74) | -0.168 (17) | -1.855 (74) |
| H9 | 3823.68–3849.27 | 0.616 (21) | -0.003 (73) | 0.604 (21) | 0.088 (73) |
| H8 | 3877.18–3903.13 | 0.226 (33) | 1.512 (73) | 0.066 (33) | 1.242 (73) |
| HdA | 4084.65–4123.41 | 0.403 (59) | -0.617 (74) | 0.268 (59) | -0.604 (74) |
| HgA | 4320.96–4364.73 | 0.256 (61) | 1.482 (71) | 0.740 (61) | 1.260 (71) |
| Hbeta | 4849.23–4877.99 | 0.877 (61) | 0.350 (43) | 0.469 (61) | 0.202 (43) |
| Halpha | 6542.72–6586.51 | — (0) | — (0) | — (0) | — (0) |
| CaK | 3921.65–3947.90 | — (0) | — (0) | — (0) | — (0) |
| CaH | 3956.35–3982.83 | — (0) | — (0) | — (0) | — (0) |
| Ca4227 | 4223.44–4235.94 | — (0) | — (0) | — (0) | — (0) |
| Ca4455 | 4453.37–4475.88 | 1.302 (61) | -0.506 (66) | 1.288 (61) | -0.412 (66) |
| CaT1 | 8472.00–8528.71 | — (0) | — (0) | — (0) | — (0) |
| CaT2 | 8515.94–8572.94 | — (0) | — (0) | — (0) | — (0) |
| CaT3 | 8635.62–8693.42 | — (0) | — (0) | — (0) | — (0) |
| CN4150 | 4143.29–4178.30 | -1.677 (61) | -1.300 (73) | -0.541 (61) | 0.256 (73) |
| G4300 | 4282.58–4317.59 | 1.738 (61) | 1.515 (72) | 1.833 (61) | 0.520 (72) |
| C4668 | 4635.30–4721.57 | -5.200 (61) | -2.368 (56) | -5.557 (61) | -3.101 (56) |
| Fe4383 | 4370.35–4421.62 | -0.911 (61) | -0.194 (70) | -1.062 (61) | -0.677 (70) |
| Fe4531 | 4515.52–4560.53 | -0.426 (61) | -0.877 (62) | -0.428 (61) | -0.769 (62) |
| Fe5015 | 4979.14–5055.41 | -0.771 (61) | -0.076 (32) | -1.061 (61) | -0.133 (32) |
| Fe5270 | 5247.11–5287.12 | -0.362 (44) | — (0) | -0.672 (44) | — (0) |
| Fe5335 | 5313.60–5353.61 | -1.211 (38) | — (0) | -1.290 (38) | — (0) |
| Fe5406 | 5389.00–5416.51 | -0.324 (25) | — (0) | -0.259 (25) | — (0) |
| Fe5709 | 5698.21–5721.96 | — (0) | — (0) | — (0) | — (0) |
| Fe5782 | 5778.23–5798.23 | — (0) | — (0) | — (0) | — (0) |
| Mgb | 5161.56–5194.07 | -3.276 (61) | — (0) | -2.159 (61) | — (0) |
| NaD | 5878.50–5911.01 | — (0) | — (0) | — (0) | — (0) |
| TiO1 | 5938.27–5995.79 | — (0) | — (0) | — (0) | — (0) |
| TiO2 | 6191.34–6273.86 | — (0) | — (0) | — (0) | — (0) |

### 2. Largest residual intervals outside defined features and masked lines

#### Baseline

| Rank | Vacuum rest interval, Å | With Mg b: stacked pull | N per bin | Without Mg b: stacked pull | N per bin | Ranking group | Candidate vacuum line, Å |
|---|---|---|---|---|---|---|---|
| 1 | 4583–4593 | 0.707 | 57–59 | 0.362 | 57–59 | with Mgb | [Fe II 4585.12 A](https://faculty.epss.ucla.edu/~eyoung/reprints/Doyle_2023_ApJ.pdf#page=14) |
| 2 | 4593–4603 | 0.631 | 57–58 | 0.385 | 58–59 | with Mgb | unidentified |
| 3 | 3415–3425 | — | 0 | 0.532 | 24–25 | without Mgb | unidentified |
| 4 | 3501–3511 | — | 0 | -0.505 | 33–34 | without Mgb | unidentified |
| 5 | 3745–3755 | 0.347 | 8 | 0.495 | 73 | without Mgb | [Fe I 3746.63 A; Fe I 3749.33 A; Fe I 3750.55 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 6 | 3403–3413 | — | 0 | 0.466 | 22–24 | without Mgb | [Fe I 3408.44 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 7 | 4505–4515 | -0.458 | 52–54 | -0.262 | 56–61 | with Mgb | unidentified |
| 8 | 4625–4635 | 0.457 | 58–60 | 0.303 | 56 | with Mgb | unidentified |
| 9 | 4819–4829 | 0.454 | 60–61 | 0.157 | 42–44 | with Mgb | unidentified |
| 10 | 4431–4441 | -0.453 | 56–60 | -0.421 | 64–67 | with Mgb | unidentified |
| 11 | 4915–4925 | -0.452 | 61 | -0.201 | 38–39 | with Mgb | [Fe I 4921.88 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 12 | 4607–4617 | 0.436 | 57 | 0.203 | 55–56 | with Mgb | unidentified |
| 13 | 3705–3715 | — | 0–1 | 0.413 | 69–71 | without Mgb | [Fe I 3706.62 A; Fe I 3708.97 A; Fe I 3710.30 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 14 | 4573–4583 | 0.364 | 57–59 | 0.311 | 57–58 | with Mgb | unidentified |
| 15 | 4495–4505 | -0.362 | 50–53 | -0.229 | 58–60 | with Mgb | unidentified |

#### C/N free

| Rank | Vacuum rest interval, Å | With Mg b: stacked pull | N per bin | Without Mg b: stacked pull | N per bin | Ranking group | Candidate vacuum line, Å |
|---|---|---|---|---|---|---|---|
| 1 | 4583–4593 | 0.624 | 57–59 | 0.289 | 57–59 | with Mgb | [Fe II 4585.12 A](https://faculty.epss.ucla.edu/~eyoung/reprints/Doyle_2023_ApJ.pdf#page=14) |
| 2 | 4593–4603 | 0.549 | 57–58 | 0.253 | 58–59 | with Mgb | unidentified |
| 3 | 4819–4829 | 0.508 | 60–61 | 0.214 | 42–44 | with Mgb | unidentified |
| 4 | 4915–4925 | -0.492 | 61 | -0.186 | 38–39 | with Mgb | [Fe I 4921.88 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 5 | 4625–4635 | 0.438 | 58–60 | 0.297 | 56 | with Mgb | unidentified |
| 6 | 4431–4441 | -0.437 | 56–60 | -0.351 | 64–67 | with Mgb | unidentified |
| 7 | 4055–4065 | -0.227 | 53–55 | -0.416 | 74 | without Mgb | [Fe I 4064.74 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 8 | 4607–4617 | 0.415 | 57 | 0.234 | 55–56 | with Mgb | unidentified |
| 9 | 3403–3413 | — | 0 | 0.405 | 22–24 | without Mgb | [Fe I 3408.44 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 10 | 4573–4583 | 0.403 | 57–59 | 0.308 | 57–58 | with Mgb | unidentified |
| 11 | 3415–3425 | — | 0 | 0.375 | 24–25 | without Mgb | unidentified |
| 12 | 4793–4803 | 0.374 | 61 | 0.223 | 45–46 | with Mgb | unidentified |
| 13 | 3745–3755 | 0.371 | 8 | 0.367 | 73 | without Mgb | [Fe I 3746.63 A; Fe I 3749.33 A; Fe I 3750.55 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |
| 14 | 4505–4515 | -0.357 | 52–54 | -0.093 | 56–61 | with Mgb | unidentified |
| 15 | 3573–3583 | — | 0 | 0.351 | 41–45 | without Mgb | [Fe I 3582.22 A](https://physics.nist.gov/PhysRefData/Handbook/Tables/irontable2_a.htm) |

### 3. Baseline group differences at shared rest wavelengths

| Band | Native N with/without | Native metric delta [95% interval] | Common 2 Å bins; span, Å | Matched N with/without | Matched mean-pull delta [95% interval] | Matched interval excludes zero |
|---|---|---|---|---|---|---|
| H10 | 17/74 | -2.279 [-3.171, -1.730] | 12; 3787–3811 | 13/72 | -0.262 [-0.363, -0.090] | yes |
| H9 | 21/73 | -0.619 [-1.776, 0.233] | 12; 3825–3849 | 19/72 | -0.078 [-0.209, 0.016] | no |
| H8 | 33/73 | 1.286 [0.425, 1.871] | 12; 3879–3903 | 28/70 | 0.137 [0.046, 0.221] | yes |
| HdA | 59/74 | -1.020 [-1.510, -0.433] | 19; 4085–4123 | 57/67 | -0.087 [-0.142, -0.033] | yes |
| HgA | 61/71 | 1.226 [0.428, 1.823] | 21; 4321–4363 | 58/60 | 0.108 [0.046, 0.173] | yes |
| Hbeta | 61/43 | -0.528 [-1.161, 0.281] | 13; 4851–4877 | 60/36 | -0.094 [-0.159, -0.005] | yes |
| Ca4455 | 61/66 | -1.808 [-2.559, -0.818] | 10; 4455–4475 | 54/61 | -0.216 [-0.303, -0.129] | yes |
| CN4150 | 61/73 | 0.378 [-0.630, 1.125] | 16; 4145–4177 | 59/65 | -0.007 [-0.070, 0.125] | no |
| G4300 | 61/72 | -0.223 [-1.057, 0.635] | 17; 4283–4317 | 61/66 | -0.057 [-0.148, 0.046] | no |
| C4668 | 61/56 | 2.832 [1.528, 3.984] | 42; 4637–4721 | 49/45 | 0.171 [0.091, 0.239] | yes |
| Fe4383 | 61/70 | 0.717 [0.154, 1.399] | 25; 4371–4421 | 48/49 | 0.058 [-0.004, 0.101] | no |
| Fe4531 | 61/62 | -0.451 [-1.156, 0.555] | 21; 4517–4559 | 40/49 | -0.005 [-0.079, 0.103] | no |
| Fe5015 | 61/32 | 0.695 [-0.497, 1.680] | 37; 4981–5055 | 49/13 | -0.046 [-0.112, 0.039] | no |

### 4. Native spectral chi-square excess partition

| Arm | Group | Galaxies | Fitted pixels | Total excess E | Carbon excess, % | Mg b excess, % | Elsewhere excess, % |
|---|---|---|---|---|---|---|---|
| baseline | all | 135 | 488915 | 62413.5 | 3.61 | 3.91 | 92.48 |
| baseline | with Mgb | 61 | 224267 | 23310.9 | 6.23 | 10.47 | 83.30 |
| baseline | without Mgb | 74 | 264648 | 39102.6 | 2.04 | 0.00 | 97.96 |
| cn free | all | 135 | 488915 | 61423.2 | 3.77 | 3.06 | 93.18 |
| cn free | with Mgb | 61 | 224267 | 23216.5 | 4.82 | 8.09 | 87.10 |
| cn free | without Mgb | 74 | 264648 | 38206.7 | 3.13 | 0.00 | 96.87 |

## Experiment 8 results

| Result | Measured value |
|---|---|
| [alpha/Fe], five galaxies with Mg b | Baseline: Mg b carries 20.0% of data information; the four carbon bands together carry 20.9%. With C/N free: 18.7% and 12.8%. |
| Opposed [alpha/Fe] tugs | With Mg b coverage, baseline median Mg b tug is +0.060 dex and combined carbon tug is −0.067 dex. C/N-free values are +0.044 and −0.021 dex. |
| Age information | For the same five galaxies, Mg b carries 1.34% / 1.54% of age data information in baseline / C/N-free fits. Carbon bands carry 36.7% / 37.1%. The prior contributes median 67.1% / 67.2% of total age information under the expected-prior approximation below. |
| Width check | Fisher sigma / posterior 16–84 half-width spans 0.79–8.22 for [alpha/Fe] and 0.53–1.40 for age. M8_161113 baseline has median [alpha/Fe]=−0.19544 near the −0.2 bound: Fisher sigma 0.04391 dex, posterior half-width 0.00534 dex. |
| Tug closure | Pixel contributions sum to their reported global linear shift. Nonzero totals are retained. Componentwise medians, stored predictive-median pulls and omitted score terms do not provide a stationary expansion point. |

### Definitions and approximations

| Definition | Choice or limitation |
|---|---|
| Inputs | The 10 [test-set targets](../quiescent-test-set/targets.json), using the existing experiment-3 baseline and C/N-free arms recorded in [per-galaxy results](exp3-per-galaxy.csv). All 40 raw/derived file hashes match experiment 3. Each arm has five galaxies with Mg b and five without. |
| Model and point | Existing production notebook model assembly with each fit’s recorded settings and priors. Componentwise weighted posterior medians for every sampled coordinate. Local CPU, JAX x64; the production float32 SFH basis remains unchanged. No sampler or predictive-warmup thread runs. |
| Sampled Jacobian | 24 sampled scalar coordinates in baseline, 26 with C/N free. Includes all 14 SFH ratios, metallicity, metallicity-history parameter, [alpha/Fe], dust, mass, dispersion and C/N where sampled. Every derivative is available. |
| Linear nuisance columns | The production calibration assignment and EmissionLineColumns provide the same polynomial, tied spectral lines, shared photometry columns, Gaussian polynomial precisions and line ridge. There are 26–33 nuisance columns. The Gaussian-kernel conditional unconstrained nuisance mode defines the mean-point Jacobian; physical derivatives include polynomial multiplication and changing line profiles. |
| Nuisance approximation | Gaussian local treatment of the analytic nuisance integral. The positive-line-flux orthant factor and parameter-dependent marginal-volume curvature are omitted. Hard flux positivity and hard sampled-prior boundaries do not truncate the Fisher covariance. |
| Weights and null direction | W is fixed at stored effective inverse variance; photometry uses its stored uncertainty where no separate effective-uncertainty dataset exists. Noise/covariance derivatives are omitted. log_f_calib has an exactly zero mean Jacobian column and zero curvature with these fixed weights. Its disconnected null direction is excluded from inversion and remains listed in the parameter CSV. |
| Fisher and prior | F = A^T A + P, with A = W^(1/2) J including nuisance columns. Student-t SFH priors use expected negative log-density curvature (nu+1)/((nu+3) scale²) = 6.666667 for nu=2, scale=0.3. Other sampled priors use their exact local negative Hessian; flat priors contribute zero. Polynomial precision and the likelihood’s line ridge are retained. |
| Prior approximation check | The exact local Student-t curvature makes the full matrix indefinite in 16/20 fits. Those statuses and negative-curvature coordinates are preserved in inputs.json. The expected-prior Fisher matrices are positive definite on identifiable coordinates for all 20 fits; no eigenvalue clipping or additional ridge is used. Expected Student-t curvature is checked by independent quadrature. |
| Age propagation | The existing SFH mapping and notebook formed-mass convention define age in Gyr. g_age is differentiated through all SFH ratios. g_afe selects the [alpha/Fe] coordinate. Age values match the existing age helper; age derivatives also pass finite differences. |
| Marginal information | C = F^-1 on identifiable coordinates; v = g^T C g; q = C g. The nuisance-projected derivative is A q / v. Pixel information is (A q)² / v². Its sum plus q^T P q / v² equals 1/v. CSVs contain both fractions of total marginal information and fractions normalized over data only. |
| Regions | Disjoint partition: Mg b; CN4150; G4300; Fe4383; C4668; remaining defined Balmer features; remaining Fe features; other defined features; remaining fitted spectral pixels; photometry. The four named carbon bands take precedence over the Fe grouping. Feature windows use the existing vacuum conversion and ±1000 km/s line default. |
| Window-deletion forecasts | All three forecasts use the same median point, Jacobian, stored weights, nuisance basis and prior curvature. The matrix and all nuisance projections are recomputed after removing the specified rows. These are local forecasts without refitting. |
| Tugs | Pixel delta = (A C g) times the stored pull. Regional deltas sum over their pixels. A positive value pushes the named quantity upward. The separate prior tug uses the actual log-prior gradient plus Gaussian nuisance-prior gradients, with the same approximate C. No recentering forces a zero sum. |
| Posterior width | Reported actual width is (q84 − q16)/2, not a Gaussian standard-deviation estimate. [alpha/Fe] uses weighted stored samples; age uses the notebook’s stored 400 histories. Hard bounds and nonlinear SFH/abundance correlations can make these differ strongly from the local forecast. |
| Validation | 80 finite-difference comparisons: [alpha/Fe] and the most informative SFH coordinate, at steps 0.001 and 0.0005. Largest whitened relative L2 discrepancy is 0.693%. The nuisance normal matrix matches the production likelihood; all pixel/region information and tug identities pass. [Checks](information-map/checks.json). |
| Median convention | Group rows are medians of per-galaxy values. Component medians need not add to 100% or to the median total tug. Carbon-union values sum the four bands inside each galaxy before taking the group median. |
| Files and reproduction | [Script](information-map/analyse.py), [input records and approximations](information-map/inputs.json), [all sampled/nuisance derivatives and curvatures](information-map/parameters.csv), [finite differences](information-map/finite-differences.csv), [pixel contributions](information-map/pixels.csv). Run with ceridwen/.venv/bin/python; --self-test and --check-only validate equations and saved outputs. |
| Noticed, not done | Fitted weighting, model code, notebook code and priors are unchanged. No new fits, GPU, figures or wiki pages. The pre-existing state-checker fault remains. |

### Information fractions by region

| Arm | Mg b coverage | Quantity | N | Mg b % | CN4150 % | G4300 % | Fe4383 % | C4668 % | Balmer % | Other Fe % | Other features % | Remaining spectrum % | Photometry % | Prior % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | with_Mgb | afe | 5 | 19.73 | 1.53 | 3.64 | 8.93 | 4.95 | 7.52 | 5.17 | 1.62 | 39.79 | 3.07 | 2.59 |
| baseline | with_Mgb | age_gyr | 5 | 0.42 | 2.09 | 4.37 | 2.50 | 0.31 | 5.08 | 0.45 | 0.89 | 9.77 | 3.64 | 67.12 |
| baseline | without_Mgb | afe | 5 | 0.00 | 3.01 | 3.81 | 5.38 | 4.89 | 22.47 | 0.90 | 1.50 | 55.04 | 2.11 | 0.83 |
| baseline | without_Mgb | age_gyr | 5 | 0.00 | 0.81 | 8.80 | 0.57 | 0.75 | 8.52 | 1.22 | 1.51 | 17.96 | 3.35 | 56.89 |
| cn | with_Mgb | afe | 5 | 18.25 | 2.45 | 1.39 | 6.32 | 2.50 | 9.34 | 6.33 | 2.17 | 47.41 | 2.63 | 1.79 |
| cn | with_Mgb | age_gyr | 5 | 0.52 | 0.29 | 7.70 | 1.67 | 1.53 | 3.06 | 0.81 | 1.16 | 10.48 | 4.18 | 67.15 |
| cn | without_Mgb | afe | 5 | 0.00 | 3.34 | 4.64 | 4.90 | 4.58 | 19.31 | 2.33 | 1.96 | 55.03 | 1.99 | 1.87 |
| cn | without_Mgb | age_gyr | 5 | 0.00 | 0.23 | 1.24 | 0.39 | 0.64 | 7.88 | 0.87 | 0.43 | 12.99 | 4.07 | 71.45 |

### Data-information comparison and combined carbon tug

| Arm | Mg b coverage | N | Mg b data % | Four-carbon data % | Remaining-spectrum data % | Mg b tug, dex | Carbon tug, dex | Remaining-spectrum tug, dex |
|---|---|---|---|---|---|---|---|---|
| baseline | with_Mgb | 5 | 19.98 | 20.87 | 40.27 | 0.060 | -0.067 | 0.006 |
| cn | with_Mgb | 5 | 18.67 | 12.81 | 48.11 | 0.044 | -0.021 | -0.020 |
| baseline | without_Mgb | 5 | 0.00 | 17.34 | 56.00 | 0.000 | -0.026 | -0.054 |
| cn | without_Mgb | 5 | 0.00 | 17.02 | 55.55 | 0.000 | -0.043 | -0.057 |

### Regional tugs

#### afe (dex)

| Arm | Mg b coverage | Mg b | CN4150 | G4300 | Fe4383 | C4668 | Balmer | Other Fe | Other features | Remaining | Photometry | Prior | Total data | Data + prior |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | with_Mgb | 0.060 | -0.009 | -0.008 | -0.007 | -0.029 | 0.011 | 0.003 | -0.008 | 0.006 | -0.003 | 0.004 | 0.025 | 0.030 |
| baseline | without_Mgb | 0.000 | -0.019 | 0.008 | -0.007 | 0.000 | 0.015 | 0.000 | -0.007 | -0.054 | -0.001 | -0.002 | -0.045 | -0.045 |
| cn | with_Mgb | 0.044 | -0.008 | -0.003 | -0.003 | -0.003 | 0.003 | -0.001 | -0.003 | -0.020 | -0.005 | 0.000 | 0.026 | 0.026 |
| cn | without_Mgb | 0.000 | -0.015 | 0.013 | -0.014 | 0.000 | 0.028 | 0.001 | 0.000 | -0.057 | -0.005 | 0.021 | -0.048 | -0.035 |

#### age_gyr (Gyr)

| Arm | Mg b coverage | Mg b | CN4150 | G4300 | Fe4383 | C4668 | Balmer | Other Fe | Other features | Remaining | Photometry | Prior | Total data | Data + prior |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | with_Mgb | 0.161 | -0.101 | -0.021 | 0.120 | 0.042 | 0.092 | 0.006 | 0.125 | -0.354 | 0.099 | 0.798 | 0.453 | 1.022 |
| baseline | without_Mgb | 0.000 | -0.012 | -0.098 | 0.009 | 0.000 | 0.175 | -0.030 | 0.045 | -0.133 | -0.029 | 0.347 | -0.227 | 0.302 |
| cn | with_Mgb | 0.062 | 0.026 | -0.060 | 0.084 | -0.161 | 0.141 | -0.013 | 0.118 | -0.347 | 0.116 | 0.910 | -0.059 | 1.002 |
| cn | without_Mgb | 0.000 | 0.018 | 0.017 | 0.024 | -0.013 | 0.123 | -0.042 | 0.022 | -0.074 | 0.004 | 0.417 | 0.148 | 0.330 |

### Per-galaxy widths and total shifts

#### afe (dex)

| Galaxy | Arm | Mg b coverage | Sigma all | Sigma no Mg b | Sigma no carbon | Posterior half-width | Sigma / posterior | Total data tug | Prior tug | Data + prior |
|---|---|---|---|---|---|---|---|---|---|---|
| M1_210210 | baseline | with_Mgb | 0.017 | 0.020 | 0.019 | 0.014 | 1.15 | 0.024 | 0.004 | 0.028 |
| M1_210210 | cn | with_Mgb | 0.024 | 0.030 | 0.027 | 0.023 | 1.04 | 0.026 | 0.000 | 0.026 |
| M4_107370 | baseline | without_Mgb | 0.079 | 0.079 | 0.089 | 0.036 | 2.22 | 0.015 | 0.015 | 0.029 |
| M3_117010 | baseline | without_Mgb | 0.049 | 0.049 | 0.056 | 0.043 | 1.14 | -0.066 | -0.002 | -0.068 |
| M3_120308 | baseline | with_Mgb | 0.031 | 0.037 | 0.038 | 0.039 | 0.79 | 0.033 | 0.008 | 0.041 |
| M2_134021 | baseline | with_Mgb | 0.037 | 0.045 | 0.045 | 0.034 | 1.09 | 0.046 | 0.003 | 0.049 |
| M7_146213 | baseline | with_Mgb | 0.038 | 0.046 | 0.044 | 0.037 | 1.02 | 0.020 | 0.001 | 0.021 |
| M8_150848 | baseline | with_Mgb | 0.022 | 0.029 | 0.027 | 0.023 | 0.99 | 0.025 | 0.005 | 0.030 |
| M8_161113 | baseline | without_Mgb | 0.044 | 0.044 | 0.048 | 0.005 | 8.22 | -0.242 | -0.002 | -0.244 |
| M5_238314 | baseline | without_Mgb | 0.031 | 0.031 | 0.036 | 0.030 | 1.03 | -0.045 | 0.000 | -0.045 |
| M14_37219 | baseline | without_Mgb | 0.042 | 0.042 | 0.047 | 0.041 | 1.02 | 0.010 | -0.003 | 0.007 |
| M4_107370 | cn | without_Mgb | 0.130 | 0.130 | 0.145 | 0.034 | 3.86 | -0.314 | 0.021 | -0.293 |
| M3_117010 | cn | without_Mgb | 0.084 | 0.084 | 0.098 | 0.042 | 2.01 | -0.099 | 0.023 | -0.076 |
| M3_120308 | cn | with_Mgb | 0.039 | 0.047 | 0.042 | 0.034 | 1.14 | 0.015 | 0.005 | 0.020 |
| M2_134021 | cn | with_Mgb | 0.048 | 0.055 | 0.053 | 0.048 | 1.01 | 0.068 | 0.001 | 0.069 |
| M7_146213 | cn | with_Mgb | 0.050 | 0.061 | 0.054 | 0.051 | 0.97 | 0.031 | -0.005 | 0.026 |
| M8_150848 | cn | with_Mgb | 0.031 | 0.043 | 0.033 | 0.022 | 1.41 | -0.001 | -0.009 | -0.009 |
| M8_161113 | cn | without_Mgb | 0.092 | 0.092 | 0.101 | 0.046 | 2.00 | -0.048 | 0.027 | -0.021 |
| M5_238314 | cn | without_Mgb | 0.054 | 0.054 | 0.063 | 0.021 | 2.54 | -0.046 | 0.011 | -0.035 |
| M14_37219 | cn | without_Mgb | 0.076 | 0.076 | 0.086 | 0.044 | 1.72 | -0.014 | -0.001 | -0.015 |

#### age_gyr (Gyr)

| Galaxy | Arm | Mg b coverage | Sigma all | Sigma no Mg b | Sigma no carbon | Posterior half-width | Sigma / posterior | Total data tug | Prior tug | Data + prior |
|---|---|---|---|---|---|---|---|---|---|---|
| M1_210210 | baseline | with_Mgb | 0.412 | 0.414 | 0.459 | 0.414 | 0.99 | -0.219 | 0.839 | 0.620 |
| M1_210210 | cn | with_Mgb | 0.459 | 0.460 | 0.473 | 0.441 | 1.04 | 0.949 | 0.579 | 1.528 |
| M4_107370 | baseline | without_Mgb | 0.327 | 0.327 | 0.347 | 0.301 | 1.09 | -0.045 | 0.347 | 0.302 |
| M3_117010 | baseline | without_Mgb | 0.384 | 0.384 | 0.420 | 0.332 | 1.16 | -0.357 | 0.567 | 0.210 |
| M3_120308 | baseline | with_Mgb | 0.467 | 0.473 | 0.516 | 0.427 | 1.10 | 0.495 | 0.238 | 0.733 |
| M2_134021 | baseline | with_Mgb | 0.528 | 0.529 | 0.569 | 0.495 | 1.07 | 0.062 | 0.960 | 1.022 |
| M7_146213 | baseline | with_Mgb | 0.552 | 0.554 | 0.602 | 0.576 | 0.96 | 0.690 | 0.347 | 1.037 |
| M8_150848 | baseline | with_Mgb | 0.483 | 0.488 | 0.572 | 0.446 | 1.08 | 0.453 | 0.798 | 1.251 |
| M8_161113 | baseline | without_Mgb | 0.292 | 0.292 | 0.316 | 0.280 | 1.04 | 0.028 | 0.298 | 0.326 |
| M5_238314 | baseline | without_Mgb | 0.236 | 0.236 | 0.258 | 0.205 | 1.15 | -0.343 | 0.316 | -0.027 |
| M14_37219 | baseline | without_Mgb | 0.409 | 0.409 | 0.437 | 0.330 | 1.24 | -0.227 | 0.708 | 0.481 |
| M4_107370 | cn | without_Mgb | 0.352 | 0.352 | 0.368 | 0.253 | 1.39 | -0.330 | 0.417 | 0.087 |
| M3_117010 | cn | without_Mgb | 0.447 | 0.447 | 0.459 | 0.320 | 1.40 | 0.148 | 0.486 | 0.635 |
| M3_120308 | cn | with_Mgb | 0.436 | 0.438 | 0.515 | 0.430 | 1.01 | -0.148 | 0.880 | 0.732 |
| M2_134021 | cn | with_Mgb | 0.420 | 0.420 | 0.447 | 0.340 | 1.23 | -0.679 | 0.910 | 0.231 |
| M7_146213 | cn | with_Mgb | 0.518 | 0.523 | 0.583 | 0.519 | 1.00 | -0.059 | 1.060 | 1.002 |
| M8_150848 | cn | with_Mgb | 0.396 | 0.397 | 0.465 | 0.313 | 1.27 | 0.320 | 0.945 | 1.264 |
| M8_161113 | cn | without_Mgb | 0.181 | 0.181 | 0.182 | 0.343 | 0.53 | 0.181 | -0.145 | 0.036 |
| M5_238314 | cn | without_Mgb | 0.322 | 0.322 | 0.328 | 0.263 | 1.23 | 0.195 | 0.135 | 0.330 |
| M14_37219 | cn | without_Mgb | 0.466 | 0.466 | 0.475 | 0.358 | 1.30 | -0.112 | 0.866 | 0.754 |

### Median widths by coverage

| Arm | Mg b coverage | Quantity | N | Sigma all | Sigma no Mg b | Sigma no carbon | Posterior half-width | Median no-Mg/all ratio | Median no-carbon/all ratio |
|---|---|---|---|---|---|---|---|---|---|
| baseline | with_Mgb | afe | 5 | 0.031 | 0.037 | 0.038 | 0.034 | 1.217 | 1.209 |
| baseline | with_Mgb | age_gyr | 5 | 0.483 | 0.488 | 0.569 | 0.446 | 1.005 | 1.104 |
| cn | with_Mgb | afe | 5 | 0.039 | 0.047 | 0.042 | 0.034 | 1.236 | 1.091 |
| cn | with_Mgb | age_gyr | 5 | 0.436 | 0.438 | 0.473 | 0.430 | 1.003 | 1.126 |
| baseline | without_Mgb | afe | 5 | 0.044 | 0.044 | 0.048 | 0.036 | 1.000 | 1.129 |
| baseline | without_Mgb | age_gyr | 5 | 0.327 | 0.327 | 0.347 | 0.301 | 1.000 | 1.081 |
| cn | without_Mgb | afe | 5 | 0.084 | 0.084 | 0.098 | 0.042 | 1.000 | 1.136 |
| cn | without_Mgb | age_gyr | 5 | 0.352 | 0.352 | 0.368 | 0.320 | 1.000 | 1.019 |

| Saved per-galaxy values | Saved medians |
|---|---|
| [Region information and tugs](information-map/regions.csv), [widths and closure](information-map/widths.csv), [combined carbon comparison](information-map/region-comparisons.csv) | [Regions](information-map/medians-regions.csv), [widths](information-map/medians-widths.csv), [combined comparison](information-map/medians-comparisons.csv) |

## Experiment 9 results

Production SFH prior and a common cosmic-time formation history. All slopes below are in Gyr per unit redshift; ages are in Gyr and abundances in dex.

| Sample | N | Prior median-age slope | Universe-age OLS slope | d(t_univ)/dz at median z | Prior / universe OLS |
| --- | ---: | ---: | ---: | ---: | ---: |
| all135 | 135 | -2.278833 | -5.172135 | -5.518885 | 0.4406 |
| test10 | 10 | -2.309617 | -5.239110 | -5.508097 | 0.4408 |

The prior-only median-age slope is about 44% of the universe-age slope. The complete [prior table](prior-slope/prior-per-galaxy.csv) contains the 135 October galaxies and the extra test-set member M5_238314, which is absent from that October selection.

| Arm | Recovered slope [95% bootstrap] | True OLS slope | Recovered / true | Median age bias, lower z | Median age bias, upper z | Age truth within 16–84 | Median alpha/Fe bias | Median Fe/H bias |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P | -5.62641 [-6.29939, -3.41142] | -5.23911 | 1.0739 | +0.57218 | +0.53700 | 10/30 | -0.01181 | +0.05219 |
| W | -6.74923 [-8.34734, -0.81977] | -5.23911 | 1.2882 | +0.22905 | +0.31801 | 14/30 | -0.01220 | +0.04326 |

These mocks do not establish flattening of the recovered slope. Production P recovers 1.074 times the true slope; the wider prior W recovers 1.288. Both 95% bootstrap intervals include the true slope. The wider prior reduces the positive age offset in both redshift halves; its slope point estimate is steeper and farther from truth.

| Item | Definition or check |
| --- | --- |
| Prior draws | 200,000 production StudentT ratio vectors: mean 0, scale 0.3, df 2; seed 20261119. The same vectors are used at every redshift. Fourteen ratios define the notebook's fifteen time nodes. No tail clipping. scipy softmax removes a common SFR normalisation to avoid overflow; 100 draws agree with the production transform to relative tolerance 1e-12. |
| Prior slope | Unweighted OLS of each galaxy's prior median mass-weighted age against catalog redshift. The universe-age OLS column uses the same redshifts; the derivative column is the tangent at their median. |
| Cosmology and bins | The [production notebook](../../notebooks/ceridwen_integrated_photometry_spectra.ipynb) uses [age_gyr and Cosmology.planck18](../../ceridwen/ceridwen/cosmology.py); identical parameters and 14-bin construction. Per-galaxy fitting bins match the stored production bins. The derivative agrees with a central finite difference to relative tolerance 1e-8. The true age curve is t_univ(z) minus a constant; recovery ratios use its OLS slope over the same ten redshifts. |
| Formation window | Constant star formation from cosmic time 2.468870095 to 3.468870095 Gyr. At median z = 0.729950011, the exact true age equals the test-set median baseline age, 4.160633248 Gyr. Baseline ages use the stored 400 equal-weight SFH draws, as in Experiment 8. |
| Fine truth | Existing [CSPBasis_afe](../../ceridwen/ceridwen/csp/csp_afe.py) and [per-bin step integration](../../ceridwen/ceridwen/csp/csp.py): 100 active bins of 0.01 Gyr with exact window boundaries, plus two empty intervals. SFH integrates to one formed solar mass before baseline logmass scaling. The exact formed-mass age is the window midpoint in lookback time. Halving active bins to 0.005 Gyr for M1 changes the spectrum by 9.42e-7 and photometry by 2.10e-7 of their respective maximum fluxes. The SSP age grid and isochrones remain unchanged. |
| Truth and observations | alpha/Fe +0.2, constant Fe/H -0.2, no C/N. Each galaxy retains its native wavelength grid, instrument, filters, masks and statistical uncertainties. Dust, dispersion, logmass and spectral fractional floor use that galaxy's weighted baseline medians. Catalog redshift; unity calibration; zero emission amplitudes. |
| Noise | Experiment 4 recipe: independent Gaussian bands then pixels, baseline model-scaled spectral floor and 5% photometry floor. Seeds 20261111, 20261112, 20261113; RNG restarts for each galaxy, so standardized noise is shared by seed on native indices. Recovery retains original statistical uncertainties and production floor rules. Every saved draw was independently reproduced exactly. |
| Recovery arms | P: unchanged production StudentT scale 0.3. W: only priors.logsfr_ratios = StudentT(mean=0.0, scale=1.0, df=2.0) through the existing experiment config. Both use production settings, plain grid, analytic linear nuisances, fast SFH basis, 500 live points, 65 inner steps, 100 deletes and logZ tolerance -5; inference seed 20261110, A100-40GB. No notebook or model source changes. |
| Age and abundance summaries | Recovery quantiles use all weighted posterior samples, with the production formed-mass age definition. Intervals are 16–84%. Bias is posterior median minus truth. Fe/H is the sampled formed-mass mean metallicity coordinate. |
| Slope and bootstrap | OLS on all 30 posterior median ages, equivalent to OLS on each galaxy's mean across three noise seeds. 10,000 cluster bootstrap draws resample ten galaxies, keeping each galaxy's three noise realizations together; seed 20261129, 95% percentile interval. Lower and upper halves contain five galaxies each, split at median catalog redshift. |
| Scope of comparison | Fine-time constant-metallicity truth is recovered with the coarser production evolving-metallicity model. Both arms share those differences; their only recovery setting difference is SFH prior scale. The bootstrap describes these ten targets and three fixed noise realizations. |
| Validation | All sixty fits pass local artifact validation and stored diagnostics. Native grids, masks, statistical errors and production photometry floors match the inputs. Stored SFH draws match the full-sample age calculation within 8.9e-15 Gyr. All sixty cells requested A100-40GB and exit zero. Modal supplied 56 A100-SXM4-40GB and four A100-SXM4-80GB allocations. All ten own apps are stopped; zero own containers, zero billed cost. |
| Artifacts | [Inputs and exact histories](prior-slope/inputs.json), [per-mock recoveries](prior-slope/per-mock.csv), [slopes](prior-slope/recovery-slopes.csv), [validation](prior-slope/artifact-checks.json), [script](prior-slope/analyse.py). Thirty immutable NPZ inputs and all sixty retrieved fits are in prior-slope/. |
| Noticed, not done | No changes to shared model/notebook code or production defaults. No figures or wiki pages. The pre-existing state-checker worktree error remains. |

| Galaxy | z | Prior age 16 / 50 / 84 | Exact mock age | Baseline age |
| --- | ---: | ---: | ---: | ---: |
| M1_210210 | 0.654200 | 1.02742 / 3.29854 / 5.03825 | 4.597337894 | 3.48668 |
| M3_117010 | 0.676600 | 1.00864 / 3.24012 / 4.95167 | 4.464036425 | 4.42204 |
| M7_146213 | 0.687500 | 0.99940 / 3.21230 / 4.91049 | 4.400462472 | 4.32716 |
| M8_150848 | 0.701128 | 0.98855 / 3.17770 / 4.85982 | 4.322139396 | 3.66283 |
| M3_120308 | 0.727900 | 0.96666 / 3.11168 / 4.76186 | 4.171938486 | 4.46606 |
| M5_238314 | 0.732000 | 0.96351 / 3.10167 / 4.74732 | 4.149355452 | 4.21940 |
| M14_37219 | 0.734678 | 0.96126 / 3.09516 / 4.73761 | 4.134663999 | 3.52217 |
| M2_134021 | 0.749300 | 0.95022 / 3.06006 / 4.68613 | 4.055262380 | 3.22927 |
| M4_107370 | 0.843600 | 0.88171 / 2.84787 / 4.37405 | 3.574528180 | 4.40188 |
| M8_161113 | 0.891105 | 0.85036 / 2.74965 / 4.22867 | 3.351390107 | 4.10187 |

Arm P.

| Galaxy | Noise seed | True age | Recovered age [16–84] | Age bias | Truth inside | alpha/Fe | alpha/Fe bias | Fe/H | Fe/H bias |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| M1_210210 | 20261111 | 4.59734 | 5.20488 [4.92670, 5.50903] | +0.60754 | no | +0.20672 | +0.00672 | -0.17316 | +0.02684 |
| M1_210210 | 20261112 | 4.59734 | 5.44410 [5.10684, 5.81651] | +0.84676 | no | +0.18566 | -0.01434 | -0.18254 | +0.01746 |
| M1_210210 | 20261113 | 4.59734 | 5.16951 [4.84077, 5.51977] | +0.57218 | no | +0.19832 | -0.00168 | -0.18704 | +0.01296 |
| M3_117010 | 20261111 | 4.46404 | 4.73806 [4.24167, 5.20340] | +0.27402 | yes | +0.07986 | -0.12014 | -0.07797 | +0.12203 |
| M3_117010 | 20261112 | 4.46404 | 4.76860 [4.22144, 5.32267] | +0.30456 | yes | +0.25572 | +0.05572 | -0.13276 | +0.06724 |
| M3_117010 | 20261113 | 4.46404 | 4.89112 [4.37305, 5.36343] | +0.42708 | yes | +0.22327 | +0.02327 | -0.13015 | +0.06985 |
| M7_146213 | 20261111 | 4.40046 | 4.81425 [4.35923, 5.31344] | +0.41379 | yes | +0.14835 | -0.05165 | -0.17521 | +0.02479 |
| M7_146213 | 20261112 | 4.40046 | 4.88667 [4.41355, 5.33892] | +0.48621 | no | +0.17666 | -0.02334 | -0.13199 | +0.06801 |
| M7_146213 | 20261113 | 4.40046 | 5.55844 [5.09385, 6.03793] | +1.15798 | no | +0.23643 | +0.03643 | -0.23641 | -0.03641 |
| M8_150848 | 20261111 | 4.32214 | 4.92027 [4.52132, 5.36103] | +0.59813 | no | +0.21244 | +0.01244 | -0.18060 | +0.01940 |
| M8_150848 | 20261112 | 4.32214 | 5.10350 [4.72415, 5.47437] | +0.78136 | no | +0.19072 | -0.00928 | -0.19711 | +0.00289 |
| M8_150848 | 20261113 | 4.32214 | 4.86287 [4.51437, 5.22616] | +0.54073 | no | +0.18353 | -0.01647 | -0.15121 | +0.04879 |
| M3_120308 | 20261111 | 4.17194 | 4.58121 [4.16649, 5.01360] | +0.40928 | yes | +0.22228 | +0.02228 | -0.14386 | +0.05614 |
| M3_120308 | 20261112 | 4.17194 | 4.80374 [4.45526, 5.17374] | +0.63180 | no | +0.16536 | -0.03464 | -0.13608 | +0.06392 |
| M3_120308 | 20261113 | 4.17194 | 4.78657 [4.41721, 5.17544] | +0.61463 | no | +0.18308 | -0.01692 | -0.16215 | +0.03785 |
| M5_238314 | 20261111 | 4.14936 | 4.96994 [4.55425, 5.36848] | +0.82058 | no | +0.22803 | +0.02803 | -0.16385 | +0.03615 |
| M5_238314 | 20261112 | 4.14936 | 4.68508 [4.38096, 5.00181] | +0.53573 | no | +0.16392 | -0.03608 | -0.15403 | +0.04597 |
| M5_238314 | 20261113 | 4.14936 | 5.31958 [4.92669, 5.66506] | +1.17022 | no | +0.18470 | -0.01530 | -0.18966 | +0.01034 |
| M14_37219 | 20261111 | 4.13466 | 5.02958 [4.50614, 5.51831] | +0.89492 | no | +0.20359 | +0.00359 | -0.12859 | +0.07141 |
| M14_37219 | 20261112 | 4.13466 | 4.39001 [3.89796, 4.86849] | +0.25535 | yes | +0.13498 | -0.06502 | -0.09302 | +0.10698 |
| M14_37219 | 20261113 | 4.13466 | 4.96224 [4.39022, 5.48898] | +0.82758 | no | +0.11312 | -0.08688 | -0.14440 | +0.05560 |
| M2_134021 | 20261111 | 4.05526 | 4.85984 [4.39862, 5.37948] | +0.80458 | no | +0.21114 | +0.01114 | -0.24621 | -0.04621 |
| M2_134021 | 20261112 | 4.05526 | 4.59226 [4.10852, 5.10822] | +0.53700 | no | +0.23091 | +0.03091 | -0.10658 | +0.09342 |
| M2_134021 | 20261113 | 4.05526 | 4.47209 [3.96288, 4.95066] | +0.41683 | yes | +0.20623 | +0.00623 | -0.12640 | +0.07360 |
| M4_107370 | 20261111 | 3.57453 | 4.42651 [4.00675, 4.82806] | +0.85198 | no | +0.20161 | +0.00161 | -0.21830 | -0.01830 |
| M4_107370 | 20261112 | 3.57453 | 4.01085 [3.55472, 4.47550] | +0.43632 | yes | +0.15419 | -0.04581 | -0.10472 | +0.09528 |
| M4_107370 | 20261113 | 3.57453 | 4.00530 [3.54320, 4.49110] | +0.43077 | yes | +0.10141 | -0.09859 | -0.10777 | +0.09223 |
| M8_161113 | 20261111 | 3.35139 | 3.76576 [3.37548, 4.15724] | +0.41437 | no | +0.15774 | -0.04226 | -0.12839 | +0.07161 |
| M8_161113 | 20261112 | 3.35139 | 3.74925 [3.33742, 4.12334] | +0.39786 | yes | +0.18341 | -0.01659 | -0.13255 | +0.06745 |
| M8_161113 | 20261113 | 3.35139 | 3.96523 [3.57352, 4.32046] | +0.61384 | no | +0.20313 | +0.00313 | -0.17692 | +0.02308 |

Arm W.

| Galaxy | Noise seed | True age | Recovered age [16–84] | Age bias | Truth inside | alpha/Fe | alpha/Fe bias | Fe/H | Fe/H bias |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| M1_210210 | 20261111 | 4.59734 | 4.80992 [4.70287, 5.16943] | +0.21258 | no | +0.20799 | +0.00799 | -0.16649 | +0.03351 |
| M1_210210 | 20261112 | 4.59734 | 5.39694 [4.74317, 5.97330] | +0.79961 | no | +0.18584 | -0.01416 | -0.18527 | +0.01473 |
| M1_210210 | 20261113 | 4.59734 | 4.82639 [4.61236, 5.35348] | +0.22905 | no | +0.19721 | -0.00279 | -0.18647 | +0.01353 |
| M3_117010 | 20261111 | 4.46404 | 4.47753 [3.78983, 5.17206] | +0.01350 | yes | +0.07335 | -0.12665 | -0.07794 | +0.12206 |
| M3_117010 | 20261112 | 4.46404 | 4.46742 [3.66904, 5.10159] | +0.00338 | yes | +0.25425 | +0.05425 | -0.12400 | +0.07600 |
| M3_117010 | 20261113 | 4.46404 | 4.54220 [3.83751, 5.15990] | +0.07817 | yes | +0.22900 | +0.02900 | -0.12605 | +0.07395 |
| M7_146213 | 20261111 | 4.40046 | 4.60916 [4.10736, 5.32164] | +0.20870 | yes | +0.14639 | -0.05361 | -0.17765 | +0.02235 |
| M7_146213 | 20261112 | 4.40046 | 4.60798 [4.08250, 5.11187] | +0.20751 | yes | +0.17396 | -0.02604 | -0.12896 | +0.07104 |
| M7_146213 | 20261113 | 4.40046 | 5.52593 [4.77291, 6.02495] | +1.12546 | no | +0.23799 | +0.03799 | -0.24658 | -0.04658 |
| M8_150848 | 20261111 | 4.32214 | 4.85787 [4.35378, 5.67610] | +0.53573 | no | +0.21253 | +0.01253 | -0.19088 | +0.00912 |
| M8_150848 | 20261112 | 4.32214 | 4.76448 [4.48038, 5.32270] | +0.44234 | no | +0.18963 | -0.01037 | -0.19470 | +0.00530 |
| M8_150848 | 20261113 | 4.32214 | 4.59472 [4.37234, 5.00161] | +0.27258 | no | +0.18597 | -0.01403 | -0.15888 | +0.04112 |
| M3_120308 | 20261111 | 4.17194 | 4.31865 [3.71421, 4.93893] | +0.14671 | yes | +0.22368 | +0.02368 | -0.14031 | +0.05969 |
| M3_120308 | 20261112 | 4.17194 | 4.54625 [4.21844, 5.07413] | +0.37431 | no | +0.16532 | -0.03468 | -0.14907 | +0.05093 |
| M3_120308 | 20261113 | 4.17194 | 4.68540 [4.19673, 5.49683] | +0.51347 | no | +0.18285 | -0.01715 | -0.16970 | +0.03030 |
| M5_238314 | 20261111 | 4.14936 | 4.93341 [4.38649, 5.52448] | +0.78406 | no | +0.22649 | +0.02649 | -0.16922 | +0.03078 |
| M5_238314 | 20261112 | 4.14936 | 4.46737 [4.26005, 4.80747] | +0.31801 | no | +0.16281 | -0.03719 | -0.16197 | +0.03803 |
| M5_238314 | 20261113 | 4.14936 | 5.34250 [4.78090, 5.79279] | +1.19315 | no | +0.18420 | -0.01580 | -0.19189 | +0.00811 |
| M14_37219 | 20261111 | 4.13466 | 5.39751 [4.42909, 6.01434] | +1.26285 | no | +0.20632 | +0.00632 | -0.15575 | +0.04425 |
| M14_37219 | 20261112 | 4.13466 | 4.03598 [3.21715, 4.69698] | -0.09869 | yes | +0.12680 | -0.07320 | -0.08278 | +0.11722 |
| M14_37219 | 20261113 | 4.13466 | 5.17389 [4.37485, 5.87475] | +1.03922 | no | +0.11021 | -0.08979 | -0.15773 | +0.04227 |
| M2_134021 | 20261111 | 4.05526 | 4.74952 [4.32051, 5.49654] | +0.69425 | no | +0.20969 | +0.00969 | -0.26618 | -0.06618 |
| M2_134021 | 20261112 | 4.05526 | 4.40446 [3.63983, 5.29819] | +0.34920 | yes | +0.23282 | +0.03282 | -0.11471 | +0.08529 |
| M2_134021 | 20261113 | 4.05526 | 4.12453 [3.34915, 4.69895] | +0.06926 | yes | +0.20483 | +0.00483 | -0.12435 | +0.07565 |
| M4_107370 | 20261111 | 3.57453 | 4.17979 [3.74008, 4.79735] | +0.60526 | no | +0.20287 | +0.00287 | -0.21879 | -0.01879 |
| M4_107370 | 20261112 | 3.57453 | 3.64120 [2.92953, 4.28840] | +0.06668 | yes | +0.14743 | -0.05257 | -0.09331 | +0.10669 |
| M4_107370 | 20261113 | 3.57453 | 3.68240 [2.85708, 5.09110] | +0.10787 | yes | +0.10800 | -0.09200 | -0.10638 | +0.09362 |
| M8_161113 | 20261111 | 3.35139 | 3.21317 [2.78543, 3.82858] | -0.13822 | yes | +0.15566 | -0.04434 | -0.10389 | +0.09611 |
| M8_161113 | 20261112 | 3.35139 | 3.15780 [2.77641, 3.91808] | -0.19359 | yes | +0.18067 | -0.01933 | -0.10930 | +0.09070 |
| M8_161113 | 20261113 | 3.35139 | 3.46390 [2.97962, 3.99753] | +0.11251 | yes | +0.20171 | +0.00171 | -0.13880 | +0.06120 |

## Experiment 10 results

All 120 new recoveries use the ten Experiment 9 galaxies and three recorded noise seeds. P9 below is the existing Experiment 9 production arm; it was read without modification. Slopes have units Gyr per unit redshift, ages and age differences are Gyr, and abundance differences are dex.

| Arm | Injected C/Fe, N/Fe | Recovery | Rest-frame vacuum window (A) | New fits |
| --- | --- | --- | --- | ---: |
| P9 | 0, 0 | Plain grid | Original coverage | 0 |
| A | 0, 0 | Plain grid | 4155.0–4438.1 | 30 |
| B1 | +0.15, +0.30 | Plain grid | Original coverage | 30 |
| B2 | +0.15, +0.30 | C and N free | Original coverage | 30 |
| B3 | +0.15, +0.30 | Plain grid | 4155.0–4438.1 | 30 |

The exact truth has a finite-sample OLS slope of -5.239110. Each interval below is a 95% galaxy-cluster bootstrap interval, not a posterior interval.

| Arm | Recovered slope [95% bootstrap] | Recovered / true | True slope inside interval | Median alpha/Fe bias |
| --- | ---: | ---: | --- | ---: |
| P9 | -5.626 [-6.299, -3.411] | 1.074 | yes | -0.012 |
| A | -3.412 [-4.311, -0.925] | 0.651 | no | +0.012 |
| B1 | -5.944 [-6.986, -3.345] | 1.135 | yes | -0.213 |
| B2 | -5.493 [-6.421, -3.859] | 1.049 | yes | -0.013 |
| B3 | -4.348 [-6.043, -2.333] | 0.830 | yes | -0.206 |

With zero injected C/N, the common window recovers 0.651 of the true slope. Full-range C/N injection gives a more negative point slope than P9; C/N freedom brings it closer to truth. The interval-membership column gives the bootstrap comparison with the exact true slope for this ten-galaxy mock design.


| Arm | Age bias, lower z | Upper z | Originally with Mg b | Originally without Mg b | Age truth inside 16–84, all / with / without |
| --- | ---: | ---: | ---: | ---: | ---: |
| P9 | +0.572 | +0.537 | +0.598 | +0.436 | 10/30 / 3/15 / 7/15 |
| A | +0.539 | +0.695 | +0.548 | +0.695 | 17/30 / 10/15 / 7/15 |
| B1 | +0.442 | +0.430 | +0.516 | +0.399 | 13/30 / 5/15 / 8/15 |
| B2 | +0.542 | +0.481 | +0.548 | +0.450 | 11/30 / 5/15 / 6/15 |
| B3 | +0.941 | +1.173 | +0.941 | +1.173 | 6/30 / 3/15 / 3/15 |

The lower and upper halves each contain five galaxies and fifteen noise realizations. The original five-with/five-without Mg b grouping stays fixed in every arm. The joint fit is age = a + b z + c g, with g = 1 originally with Mg b and g = 0 originally without. Thus c is with minus without at fixed redshift; it is distinct from a difference of the two median biases.

| Arm | a | Joint slope b | Mg b group step c [95% bootstrap] |
| --- | ---: | ---: | ---: |
| P9 | 8.790 | -5.516 | +0.031 [-0.262, +0.259] |
| A | 7.596 | -3.720 | -0.085 [-0.348, +0.174] |
| B1 | 8.752 | -5.624 | +0.089 [-0.162, +0.284] |
| B2 | 8.602 | -5.355 | +0.038 [-0.215, +0.254] |
| B3 | 8.423 | -4.400 | -0.014 [-0.386, +0.275] |

The same joint fit to exact true ages gives b = -5.241253 and c = -0.000593. The small nonzero true c comes from approximating the curved age-redshift relation by a plane, with a common formation history in both groups. Every recovered group-step 95% bootstrap interval includes zero.

| Arm | Original Mg b coverage | Mocks | Median age width | Matching P9 width | Median paired width ratio | Median paired width difference |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| P9 | all | 30 | 0.843 | 0.843 | 1.000 | +0.000 |
| P9 | with_Mgb | 15 | 0.840 | 0.840 | 1.000 | +0.000 |
| P9 | without_Mgb | 15 | 0.921 | 0.921 | 1.000 | +0.000 |
| A | all | 30 | 1.310 | 0.843 | 1.539 | +0.463 |
| A | with_Mgb | 15 | 1.303 | 0.840 | 1.580 | +0.511 |
| A | without_Mgb | 15 | 1.317 | 0.921 | 1.514 | +0.403 |
| B1 | all | 30 | 0.843 | 0.843 | 0.990 | -0.010 |
| B1 | with_Mgb | 15 | 0.837 | 0.840 | 1.045 | +0.030 |
| B1 | without_Mgb | 15 | 0.885 | 0.921 | 0.976 | -0.019 |
| B2 | all | 30 | 0.862 | 0.843 | 0.983 | -0.015 |
| B2 | with_Mgb | 15 | 0.861 | 0.840 | 0.991 | -0.008 |
| B2 | without_Mgb | 15 | 0.891 | 0.921 | 0.959 | -0.034 |
| B3 | all | 30 | 1.310 | 0.843 | 1.519 | +0.464 |
| B3 | with_Mgb | 15 | 1.316 | 0.840 | 1.642 | +0.525 |
| B3 | without_Mgb | 15 | 1.258 | 0.921 | 1.414 | +0.416 |

Age width is q84 minus q16. Ratios and differences are computed for each matching galaxy and seed before taking the median; a ratio of median widths is a different statistic.

A changes the recovered slope from P9 by +2.215. At full coverage the C/N injection changes the plain-grid slope by -0.318; freeing C/N then changes it by +0.451. In the common window the injection changes the slope from A to B3 by -0.937.

| Method or check | Recorded choice or result |
| --- | --- |
| Truth and noise | The Experiment 9 cosmic-time formation window [2.468870095056303, 3.468870095056303] Gyr, exact per-galaxy ages, grids, native masks, instrument, filters, statistical uncertainties, dust and dispersion are unchanged. Fine truth uses 102 bins, including 100 active 0.01 Gyr bins. Alpha/Fe is +0.2 and Fe/H is -0.2. The inherited truth has constant metallicity; production fitting retains metallicity evolution and 14 SFH ratio parameters. |
| C/N injection | Only B injects +0.15 and +0.30 through the existing alf responses. At zero C/N, the fine-history mean spectrum and photometry are bitwise identical to Experiment 9 for all ten galaxies. All other original mock fields are bitwise unchanged. Enhanced-spectrum noise uses the same standardized Gaussian draws, photometry first then spectrum, and the same statistical-plus-floor recipe evaluated on the enhanced mean. |
| Response resolution | Existing catalogue-dispersion response ratios and unchanged isochrones. Minimum total response sigma is 171.151–275.252 km/s across targets; none is below 100 km/s. The existing fixed-catalogue-sigma approximation is inherited. |
| Inference | Production priors, SFH fast path, 500 live points, 65 inner steps, 100 deletions and logZ tolerance -5. SFH ratios retain StudentT scale 0.3 and df 2. Inference seed 20261110; noise seeds 20261111, 20261112, 20261113. No new sampler, notebook or model changes. |
| Windows | A and B3 apply the notebook rest_range setting, inclusive 4155.0–4438.1 A on the native rest-frame vacuum grid, retaining all native mask holes. Photometry is unchanged between recovery windows. |
| Posterior summaries | All weighted raw posterior samples determine age and alpha/Fe quantiles. SFH mass fractions and ages independently match the stored derived draws. Age coverage is the exact true formed-mass-weighted age inside q16–q84. |
| Slopes and bootstrap | Unweighted OLS on thirty posterior median ages, equivalent to OLS on ten galaxy means. Same 10,000 galaxy-cluster resamples and seed 20261129 as Experiment 9, retaining all three seeds together. All resamples enter slope intervals; 9,979 full-rank resamples enter the group-step intervals, with 21 nonidentified steps excluded. |
| Real-data reference | The read-only [135-galaxy report](../chronometer-135-2026-11-10/REPORT.md) gives -1.55 and +0.97 for the two 135-galaxy arms. Its -3.77 common-window result is arm (e), 130 valid galaxies, C/N free and alpha/Fe fixed +0.25. The requested mock arms here retain free alpha/Fe; they do not duplicate that extra fixed-alpha setting. |
| Label repair | Only cfe and nfe entries were added to scripts/plot_prior_kl.py label(). Both original KeyErrors were reproduced. All seven existing test_plot_prior_kl.py tests pass; the real C/N caller also returns both abundance labels. No figures were generated. |
| Validation | All 120 retrieved raw/derived fits pass the existing validator, input/mask/uncertainty checks and SFH-age checks. Original thirty Experiment 9 mock hashes and new thirty injected mock hashes remain unchanged; all twenty raw response files retain their recorded hashes. Independent slope, bootstrap, group-step, coverage and paired-width checks pass. All twenty owned Modal apps are stopped and no owned containers remain. |
| GPU provenance | Requested A100-40GB for every fit. Actual completed-fit GPU counts: {"NVIDIA A100 80GB PCIe": 3, "NVIDIA A100-SXM4-40GB": 84, "NVIDIA A100-SXM4-80GB": 33}. All remote bootstrap and fit exits are zero. |
| Artifacts | [Per-mock results](slope-mismatch/per-mock.csv), [arm summary](slope-mismatch/summary.csv), [paired widths](slope-mismatch/width-comparison.csv), [inputs](slope-mismatch/inputs.json), [validation](slope-mismatch/artifact-checks.json), [independent checks](slope-mismatch/independent-checks.json), [Modal state](slope-mismatch/modal-state.json), [script](slope-mismatch/analyse.py). |
| Noticed, not done | The pre-existing Ceridwen state-checker worktree error remains. No figures, wiki pages, notebook or model changes. |
