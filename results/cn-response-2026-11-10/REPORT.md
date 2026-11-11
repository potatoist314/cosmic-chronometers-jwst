# C/N responses and injection recovery

Experiment 3: all 78 fits retrieved and independently validated. Experiment 4: 27 injections generated and checked; plain-grid recovery is running.

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

The exact outputs are in `validation/baseline-existing-tests.log` and `validation/current-existing-tests.log`; `validation/cross-pin-checks.txt` records the comparison. Focused response/fast-path tests: 35 passed. The wider selected suite: 106 passed, these two pre-existing failures. Existing wiki test failures are recorded in `validation.json`.

## Noticed, not done

Ca offsets; experiments 1, 2 and the full-sample chronometer experiment 5 (owned by the lead/other worker); pre-existing production/wiki test faults. The existing model-page photometry row still says 12 bands. Visual wiki check: Not tested. On the M1, `freespace` opened no new Safari window and macOS denied Apple Events (`-1743`). Live NAS text readback passed. No new figures or wiki result pages.
