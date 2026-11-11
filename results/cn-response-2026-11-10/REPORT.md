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
