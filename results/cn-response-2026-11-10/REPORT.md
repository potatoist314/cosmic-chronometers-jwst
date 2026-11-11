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
