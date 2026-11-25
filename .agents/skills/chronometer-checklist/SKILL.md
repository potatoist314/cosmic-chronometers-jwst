---
name: chronometer-checklist
description: Use before you plan, run, check or report a cosmic-chronometer fit, a chronometer sample or an age-redshift slope. It gives Liu Hao's decisions for chronometer work and his open items. It also gives the table of masked pixels, the reason for each mask, the table of free and fixed parameters for each run, how free C and N work, and the limits of the stellar population model.
---

# Chronometer checklist

Liu Hao, 2026-11-24: "i think we need a full chronometer checklist, maybe make this a skill."

Liu Hao, 2026-11-24, on its use: "not a gate. just knowledge the model should have to ensure we are on the same page."

A chronometer fit is a Ceridwen fit of one quiescent galaxy. The age from each fit goes into a slope of age against redshift. Read this skill before you work on a fit, a sample or a slope.

The general rules for fits, physical facts and figures are in `AGENTS.md`. Read them there. To run a fit, read `.agents/skills/running-ceridwen-experiments/SKILL.md`.

## His decisions

All decisions are from his interview of 2026-11-24. Text in quotation marks is his. "Picked" shows an option that he selected from a list.

1. **Use.** The checklist is knowledge. It is not a gate.
2. **Time grid.** Picked: "Fixed grid is enough". Use a time grid for the star-formation history (SFH) that does not change with cosmology. A routine wrong-grid test is not necessary. The setting is `sfh_grid_age` in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`. A fact, not a rule: the value is 15.0 Gyr in `results/sdss-mask-nad-2026-11-24/experiment.json` and `results/legac-break-fixed-grid-2026-11-24/experiment.json`.
3. **Spectral window.** Picked: "Same within a survey", then "Each survey its own widest". Use one rest-frame window for each survey. Use the widest window that keeps the redshift range of that survey. The windows of two surveys can be different. The masks and the rules are the same in all surveys.
   "let's just do the widest range we can per survey and keep it consistent through surveys, mask bad lines or known elements the model cant accurately model (due to ssp constraints, isochrone constraints etc) but keep it very clear what is being masked"
4. **Features.** A fit includes these features where the survey permits: the 4000 Å break, Hγ and Hδ, Hβ. He did not select Mg b and the iron lines.
   "i'd very much like a wider spectra where possible... some features are really important to include"
5. **Masks.** "na d should be masked. but as said earlier, we need to be very clear on what is masked and have a valid physical justification is". Each mask is a row in the table below. The same table is on the wiki: "table in skill and on wiki". When a mask changes, change the two tables.
6. **Age.** "just use mass weighted for now and experiment with only keeping the oldest per refshift bin." Use the mass-weighted age for the slope. The experiment with the oldest galaxy of each redshift bin uses the stored fits. It needs no new GPU fit.
7. **Old ages.** Keep a galaxy that is older than the Universe. Keep a fit that is at a limit. "keep, you can flag but it doesnt seem like s huge deal". His reason: "if the error bars are wide it seems like some should land older than the universe just by scatter, but they should probably be kept to balance those which land on the young side of the error?"
8. **Sample.** "250km/s floor seems good across all surveys. but should also do a quick check of sfh from model output". For the velocity dispersion: "use published within survey."
9. **SFH check.** Picked: "Recent mass formed". A galaxy fails when more than a small fraction of its mass formed recently. Flag the galaxy. Show the slope with and without the flagged galaxies. The fraction and the time are not yet set. A check of the 50 SDSS fits of `results/sdss-mask-nad-2026-11-24` gives two facts. They are not rules. The largest posterior median of the mass formed in the last 1 Gyr is 1.4 %. 16 of the 50 galaxies have more than 5 % in the last 2 Gyr (`~/.claude/scripts/hermes-bridge/results/t_107ca68a-detail.md`).
10. **Data quality.** Picked: "No fixed floor yet". Use the quality flags of the survey. Record the S/N and the resolution of each spectrum. Examine the slope against S/N and resolution before you set a number.
11. **Checks before an H value is shown.** He selected two checks: mock recovery, and a wrong-grid test on a subset. He did not select two others: the slope by subsample, and variants of mask and range. "more testing before final output, less for now"

## Open items

These items are his, and he did not decide them. Do not decide them for him.

- How to combine surveys: "combining surveys still open."
- The resolution of the SFH: "sfh resolution still somewhat open."
- The 250 km/s floor for a survey that publishes no velocity dispersion: "i havent decided what to do without survey yet, keep opem"
- Mass-weighted age against the oldest galaxy of each redshift bin. He asked for the experiment. "not sure. mass weighted seems ok, but oldest envelope to avoid progenitor bias also seems ok."

## Masked pixels

State on 2026-11-24. The masks are in `SETTINGS` (cell 2) and cell 6 of `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, and in the `experiment.json` of each run. Rest wavelengths are vacuum. A line mask is the line centre ± 1500 km/s (`mask_lines` in `ceridwen/ceridwen/observation/spectrum.py`).

| Mask | Range | Surveys | Physical reason | Source |
|---|---|---|---|---|
| Flagged pixels | LEGA-C: `QUAL` = 1 or error = 0. SDSS: `IVAR` = 0 or BRIGHTSKY set. | LEGA-C DR3, SDSS DR17 | LEGA-C: an imperfect sky subtraction at the pixel. SDSS: very bad conditions, or sky brighter than flux + 10 × error. | LEGA-C DR3 release description (ESO), data format. SDSS DR17 SPPIXMASK, https://www.sdss4.org/dr17/algorithms/bitmasks/ |
| Telluric band | 7590 to 7660 Å observed, air (7592.09 to 7662.11 Å vacuum) | LEGA-C DR3, SDSS DR17 | O2 A band of the atmosphere of the Earth. The notebook comment gives no reason. The Model page of the wiki says "A band". | van der Wel et al. 2021, arXiv:2108.00744, §2.2.2: O2 templates use 7580 to 7710 Å. Kimeswenger et al. 2021, arXiv:2011.10845, §1: A band 7596.0 to 7713.3 Å. |
| Ca II K | 3915.08 to 3954.46 Å rest (3934.77 Å ± 1500 km/s) | SDSS DR17. LEGA-C DR3 only in the window that starts at 3850.0 Å. | His order, 2026-09-30: "i was told to mask all Ca". Papers: the grid changes Ca with [α/Fe], and in early-type galaxies "Ca tracks Fe". P25 §2.4: "Since our α-enhanced models do not track individual α abundances, one should be careful in fitting spectra including Ca indices." | `wiki/research/experiments/e-mask-all-ca.md`. P25 §2.1, §2.4. C14 §5.2. |
| Ca II H, with Hε | 3946.75 to 3993.18 Å rest (3966.6 and 3973.3 Å ± 1500 km/s) | Same as Ca II K | Ca II H: same as Ca II K. Hε (3971.20 Å) and [Ne III] 3968.65 Å are in the range. No record gives a reason to mask Hε. | Same as Ca II K. Hε: NIST ASD. [Ne III]: FSPS `emlines_info.dat`. |
| Ca I 4227 | 4206.77 to 4249.07 Å rest (4227.92 Å ± 1500 km/s) | LEGA-C DR3, SDSS DR17 | Same order as Ca II K. Jonah Powley, meeting of 2026-09-17: "Ca I can be masked because of potential IGM contamination". Papers: Ca4227 becomes much stronger with [α/Fe] in the model. P25 §2.4: "Since our α-enhanced models do not track individual α abundances, one should be careful in fitting spectra including Ca indices." | `e-mask-all-ca.md`. P25 §2.4, §3.2.3. C14 §5.2. |
| Na D | 5878.50 to 5911.01 Å rest (Lick band 5876.875 to 5909.375 Å air) | SDSS DR17. The LEGA-C windows end at 4666.1 Å. | His order, 2026-11-24: "okay, mask na d". The model has no free Na. [Na/Fe] is −0.16 to +0.43 in early-type galaxies. Interstellar gas absorbs at 5895 Å. With Na D fitted, the data are below the model in 49 of 49 SDSS galaxies. | C14 §5.2. Trager et al. 1998, arXiv:astro-ph/9712258, Table 2. `~/.claude/scripts/hermes-bridge/results/t_dcbba686-detail.md` |

P25 and C14 are defined in the next section.

- **Na D is a setting of the run.** Set `"masked_absorption_features": ["NaD"]` in `experiment.json`. The notebook default is an empty list.
- **Pixels outside the window are not fitted.** Windows in the run configs: SDSS DR17 3604.0 to 7079.3 Å. LEGA-C DR3 4074.5 to 4666.1 Å. One arm of `results/legac-break-fixed-grid-2026-11-24` starts at 3850.0 Å to include the 4000 Å break.
- **Not masked: Hβ, [O II], [O III].** Each emission line of the FSPS list gets a free flux (`emission_line_marginalisation: True`). Liu Hao, 2026-09-30: "keep o unmasked as default is fine". The LEGA-C DR2 fits before that date masked Hβ and [O III]. The current code does not.
- **No sky-line mask.** `sky_lines_air` is an empty list.
- **Wiki table:** `wiki/notes/spectral-masks.md`, built as the page `/n/spectral-masks/`.

## Free and fixed parameters

Liu Hao, 2026-11-25: "carbon very important - this free parameter stuff is equally important to be tracked as compared to masks". He said this after his question "is carbon masked or free".

State on 2026-11-25. A parameter is free when the sampler draws it. `PRIORS` (cell 2) of `notebooks/ceridwen_integrated_photometry_spectra.ipynb` gives each prior. Cells 6 and 8 remove a prior when a setting makes its parameter fixed. The settings of each fit are in `source.experiment[i].settings` of the `manifest.json` of its run.

These settings are the same in each fit of each run in the table "C and N in each run": `fix_afe` null, `metallicity_evolution` true, `birth_cloud_dust` true, `emission_line_marginalisation` true, `calibration_order` 10, `sfh_nbins` 14. Only `abundance_response` changes the free parameters between these runs.

| Parameter | State | Prior or value | Source |
|---|---|---|---|
| `cfe`, [C/Fe] | Free only when `abundance_response` is set. When it is null: fixed, solar-scaled as in the grid. | Uniform −0.3 to +0.5 dex | `PRIORS`. Cell 8: `if cn_response is None: joint_priors.pop("cfe")`. P25 §2.4. |
| `nfe`, [N/Fe] | Same as `cfe` | Uniform −0.3 to +1.0 dex | Same as `cfe` |
| `logzsol`, [Fe/H] | Free | Uniform on the grid, −2.5 to +0.5 | Cell 8, `joint_priors["logzsol"]`. `model/metallicity_axis_logzsol` in `ceridwen_result.h5`. |
| `zh_beta_unit` | Free | Uniform 0 to 1. It sets how [Fe/H] rises with formed mass. | `PRIORS`. Cell 8, `zh_from_mass`. |
| `afe`, [α/Fe] | Free | Uniform on the grid, −0.2 to +0.6. One value sets all α elements. | Cell 8, `joint_priors["afe"]`. Grid `ssp_afe` in `references/stellar-population-model.md`. |
| Na, and each α element alone | Not a parameter | Set by the grid | Summary items 2 and 3 of the next section. `PRIORS` has no entry. |
| `logsfr_ratios`, 13 values | Free | Student-t: mean 0, scale 0.3, 2 degrees of freedom. Limits −3 to 3. | `PRIORS`. Cell 8, `N_RATIOS` and `joint_bounds`. |
| `logmass` | Free | Uniform 8 to 13 | `PRIORS` |
| `diffuse_tau_noll`, `diffuse_delta`, `diffuse_Ebump` | Free | Uniform 0 to 1, −1.0 to 0.4, 0 to 6 | `PRIORS` |
| `dust_ratio` | Free | Normal: mean 1.0, sigma 0.3. Limits 0 to 2. | `PRIORS` |
| `sigma_smooth`, σ★ | Free | Normal about the catalogue σ★. Its width is the catalogue error. Limits ± 3 errors. | Cell 8, `joint_priors["sigma_smooth"]`. `sigma_clip` in `SETTINGS`. |
| `log_f_calib` | Free | Uniform ln 0.01 to ln 0.10 | `PRIORS` |
| `zred` | Fixed | Catalogue redshift | Cell 6: `PRIORS.pop("zred", None)` when `emission_line_marginalisation` is true |
| `diffuse_c_r` | Fixed | 0 | Cell 8, `joint_transforms` |
| `alpha_pow` | Fixed | −1 | Cell 8, `joint_transforms` |
| `tau_pow` | Tied | `dust_ratio` × `diffuse_tau_noll` | Cell 8, `joint_transforms` |
| Calibration polynomial, 11 coefficients | Free, not sampled | Chebyshev of order 10, and a constant. The fit solves them analytically. | `SETTINGS`: `calibration_order`, `calibration_fit_constant` |
| Emission-line fluxes | Free, not sampled | 0 or more. The calibration solve gives them. | `SETTINGS`: `emission_line_marginalisation` |

- **Do not use the `priors` block of a manifest.** It lists `cfe` and `nfe` in each fit, also when they are fixed. Read `settings.abundance_response`.
- **To check one finished fit,** read `model/param_names` in its `ceridwen_result.h5`. `cfe` and `nfe` are in the list only when they are free.
  - C and N free, 13 names and 25 values: `results/sdss-mask-nad-2026-11-24/run/fits/age15_nad/1237648704057966805-0309-51994-0145/`.
  - C and N fixed, 11 names and 23 values: `results/legac-break-fixed-grid-2026-11-24/run/fits/b_age15/104877-M14_104877/`.
- **A new run.** Add its row to the table below.

### C and N in each run

The column "Manifest folder" is the folder of `manifest.json`, below `results/`. "Free": `abundance_response` is `data/raw/alf/cda32111c721efe586945d7dfcb9f605a9f6a105` in each fit of the arm. "Fixed": it is null in each fit of the arm.

| Survey | Manifest folder | Arms | Fits in the manifest | C and N |
|---|---|---|---|---|
| SDSS DR17 | `sdss-pilot-2026-11-20/run` | `sdss` | 10 | Free |
| SDSS DR17 | `sdss-50-2026-11-24/run` | `sdss` | 50 | Free |
| SDSS DR17 | `sdss-prior-cosmology-2026-11-24/run` | `h0_50`, `h0_90` | 50 for each arm | Free |
| SDSS DR17 | `sdss-wide-range-2026-11-24/run` | `planck18`, `h0_50`, `h0_90` | 50 for each arm | Free |
| SDSS DR17 | `sdss-wide-fixed-age-2026-11-24/run` | `age15` | 50 | Free |
| SDSS DR17 | `sdss-mask-nad-2026-11-24/run` | `age15_nad` | 50 | Free |
| LEGA-C DR3 | `legac-dr3-2026-11-11/test-set/run` | `dr3_full`, `dr3_window` | 10 for each arm | Fixed |
| LEGA-C DR3 | `legac-dr3-2026-11-11/window-194/run` | `dr3_plain_w` | 194 | Fixed |
| LEGA-C DR3 | `legac-dr3-2026-11-11/window-194/run` | `dr3_cn_free_w` | 194 | Free |
| LEGA-C DR3 | `dr3-more-galaxies-2026-11-16/plain-colab/run`, `plain-modal/run` | `dr3_plain_w` | 24 and 130 | Fixed |
| LEGA-C DR3 | `dr3-more-galaxies-2026-11-16/first-10/run`, `rest-a/run`, `rest-b/run` | `dr3_cn_free_w` | 10, 73 and 73. They are 154 galaxies. 2 galaxies are in two manifests. | Free |
| LEGA-C DR3 | `legac-prior-cosmology-2026-11-24/run` | `planck18`, `h0_50`, `h0_90` | 10 for each arm | Free |
| LEGA-C DR3 | `legac-break-fixed-grid-2026-11-24/run` | `b_age15`, `c_age15_break` | 60 for each arm | Fixed |
| LEGA-C DR3 | `legac-full-range-test-2026-11-24/run` | `d_full_age15`, `e_window_age10`, `f_full_age10` | 36 for each arm | Fixed |
| LEGA-C DR3 | `legac-steps-control-2026-11-24/run-steps33-seed2`, `run-steps65` | `steps33_seed2`, `steps65` | 12 for each arm | Fixed |
| Mock | `legac-full-range-test-2026-11-24/mock/run` | 18 arms | 36 | Fixed |
| Mock | `legac-fixed-grid-mock-2026-11-24/run` | 12 arms | 24 | Fixed |

- **SDSS DR17.** C and N are free in each run.
- **LEGA-C DR3, the sample of 348 galaxies.** It has two arms. In `dr3_plain_w` C and N are fixed: 348 valid fits. In `dr3_cn_free_w` C and N are free: 347 valid fits, because M102_214235 has none. Source: `results/dr3-more-galaxies-2026-11-16/REPORT.md`.
- **Fits on the 15 Gyr grid of 2026-11-24.** The SDSS fits have C and N free. The LEGA-C fits have C and N fixed.

### How free C and N work

Liu Hao, 2026-11-25: "in skill and slides you need to explain how cn free works".

The code is the class `AlfCNResponse` in `ceridwen/ceridwen/ssps/abundance_response.py`. The line numbers below are for that file at Ceridwen commit `84dff70b`. The data are the alf files in `data/raw/alf/cda32111c721efe586945d7dfcb9f605a9f6a105/`. alf is a public fitting code (https://github.com/cconroy20/alf). The file cites Conroy & van Dokkum (2012) and Conroy et al. (2018) (lines 1-5).

1. **Why.** C and N are solar-scaled in the grid (P25 §2.4). The grid cannot change C or N alone.
2. **alf spectra.** Each alf file holds theoretical spectra of one single-age population. One column is the solar spectrum. Each other column has one element changed. C changes by +0.15 and −0.15 dex. N changes by +0.3 and −0.3 dex. Source: the header of each file ("+/- is 0.3 dex except for C which is 0.15 dex", columns `C+`, `C-`, `N+`, `N-`) and `load`, lines 66-69.
3. **Files.** The code reads 20 files: 5 ages (1, 3, 5, 9, 13 Gyr) for each of 4 metallicities ([Fe/H] −1.5, −1.0, −0.5, 0.0). It does not read the 5 files at +0.2 (lines 24-26, 55-58).
4. **Differential spectrum.** For each file, this is the changed spectrum divided by the solar spectrum, minus 1 (lines 68-69).
5. **Interpolation.** The code interpolates linearly in log age and in [Fe/H]. Below 1 Gyr it uses the 1 Gyr spectra. Above 13 Gyr it uses the 13 Gyr spectra. Below −1.5 it uses the −1.5 spectra. Above 0.0 it uses the 0.0 spectra (lines 86-89, 184-186).
6. **Weights.** For each draw of the sampler, the SFH and the metallicity history of that draw weight the alf spectra (lines 27-28, 176-206). The result is the alf spectrum of a population with that history.
7. **Amplitude.** The code multiplies the differential C spectrum by \|`cfe`\| / 0.15. It multiplies the differential N spectrum by \|`nfe`\| / 0.3. The sign of `cfe` selects the `C+` or the `C-` column. The sign of `nfe` selects the `N+` or the `N-` column. One cross term, C × N, gets the product of the two factors (lines 187-199). The scaling is linear. The code sets no limit on it (line 192).
8. **Ratio.** ratio = 1 + (sum of the scaled differential spectra) / (alf solar spectrum) (line 211). The code multiplies the Park model spectrum by the ratio: `f = f_Park × ratio`. Source: `ceridwen/ceridwen/csp/csp_afe.py:657-658` for the photometry and `:666-669` for the spectrum.
9. **What does not change.** The isochrones do not change (line 22). Outside the alf wavelengths, 3501.0 to 24997.6 Å vacuum, the ratio is 1 (lines 35, 212). With `cfe` = 0 and `nfe` = 0 the model spectrum does not change (`csp_afe.py:656-658`).
10. **Resolution.** The code broadens the alf spectra one time, to the catalogue velocity dispersion and the instrument resolution. The Park spectrum keeps the sampled `sigma_smooth` (lines 30-32). The photometry uses the ratio without broadening (line 34).
11. **Conditions.** The redshift must be fixed at the catalogue value (lines 144-145). The total dispersion must be 100 km/s or more (lines 115-116). The SFH must be the fixed-grid step basis (lines 83-84).
12. **One value for each galaxy.** One `cfe` and one `nfe` apply to all ages of the galaxy (lines 187-188).
13. **Prior against the alf step.** The upper limit of `cfe`, +0.5, is 3.3 × the 0.15 dex step. Its lower limit, −0.3, is 2 × the step. The upper limit of `nfe`, +1.0, is 3.3 × the 0.3 dex step. Its lower limit, −0.3, is 1 × the step. Above 1 step the response is a linear extrapolation (line 192).

## Stellar population model: what it contains and its limits

Liu Hao, 2026-11-24: "we need to have a comprehensive understanding of the park alpha enhanced sps / isochrone paper and the model limitations and save it in the chronoemter skill".

The full section, with each source reference, is `references/stellar-population-model.md`. Read it before you make a statement about the model. P25 is Park et al. 2025, ApJ 994:165, the published paper (`papers/spectral fitting/Alpha-MC - Self-consistent Alpha-enhanced Stellar Population Models Covering a Wide Range of Age, Metallicity, and Wavelength (ApJ 994 165, published).pdf`). D26 is Dotter et al. 2026, arXiv:2602.22012v1. C14 is Conroy, Graves & van Dokkum 2014, ApJ 780:33.

Summary:

1. The grid is α-MC: MIST v2.5 isochrones, C3K v2.3 spectra and one Kroupa IMF (P25 §2.1 to §2.3).
2. One [α/Fe] sets O, Ne, Mg, Si, S, Ar, Ca and Ti together. No α element is free alone (P25 §2.1, §2.4).
3. C and N are solar-scaled in the grid (P25 §2.4). Ceridwen adds the alf C and N response with free `cfe` and `nfe` only when `abundance_response` is set. See "Free and fixed parameters". There is no free Na.
4. The line list is "tuned to the observed high-resolution spectra of the Sun and Arcturus for 4728 Å–1 μm" (P25 §2.2). The paper states nothing for shorter wavelengths. The LEGA-C window 4074.5 to 4666.1 Å is fully below 4728 Å. See "Blue of 4728 Å" below.
5. `logzsol` is [Fe/H], not total metallicity (`ceridwen/docs/afe.md:47-51`).
6. The age axis has 107 nodes with a step of 0.05 dex (P25 §2.3). One step is 12.2 % in age. Four nodes are older than 13.8 Gyr.
7. `SedModel` refuses an SFH node more than 0.5 % older than the Universe at the galaxy redshift (`ceridwen/ceridwen/model/model.py:232`).
8. The model has no post-AGB stars, no white dwarfs and no full horizontal branch (D26 §2.7, §3.4).
9. The spectra are 1D, plane-parallel and LTE (P25 §2.4). Opacity tables are missing at the metal-rich corner (P25 §2.1).
10. P25 shows no comparison with observed galaxy spectra (P25 §1). C2 4668 is much weaker than in models made from observed stars (P25 §3.3.2).
11. P25 §2.4 names five caveats: initial versus surface abundances, one [α/Fe] for all α elements, LTE, constant microturbulence, and single-star evolution. On Ca: "Since our α-enhanced models do not track individual α abundances, one should be careful in fitting spectra including Ca indices." The isochrones "are based on the evolution of single stars".

### Blue of 4728 Å

Liu Hao, 2026-11-24: "okay take the published one. no tuning below 4728 is concerning"

- **Tuning.** P25 §2.2: "The latest atomic and molecular line list has been provided by R. Kurucz, and it has been tuned to the observed high-resolution spectra of the Sun and Arcturus for 4728 Å–1 μm, as described in P. A. Cargile et al. (2020)." The v1 text is the same.
- **Accuracy.** No source read gives a measured accuracy of C3K v2.3 at 3600 to 4728 Å. Cargile et al. 2020 §2.1.2 gives no wavelength range for the tuning and tests 5150 to 5350 Å.

Published tests of other synthetic spectra in the blue:

| Source | Spectra tested | Finding | Size |
|---|---|---|---|
| Knowles et al. 2019, MNRAS 486, 1814 | Conroy ATLAS12 + SYNTHE before the tuning, Coelho 2014, and ATLAS9 + ASSET, against MILES stars | "C2 4668 is systematically underestimated by the models compared to observations". | ATLAS9 + ASSET cool giants, rms about Theory = Obs (Table 7): HδA 2.86 Å, HγA 2.54 Å, C2 4668 4.03 Å. Mgb 0.77 Å, Fe5270 1.08 Å. |
| C14 | Synthetic responses, used differentially, against SDSS early-type stacks | Systematics at 4500 and 4675 Å, "probably due to features that are not well-captured in our synthetic spectral library". | Median absolute residual 0.1 % in the red. 0.16 % at low σ to 0.25 % at high σ in the blue. |
| Coelho 2014, arXiv:1404.3243 | ATLAS9 and MARCS + SYNTHE, against MILES fluxes | "features below 4200 Å corresponding to missing opacities". | Within ∼5 % for T_eff ≥ 4750 K. "∼ 50% at the coolest interval". |
| Bertone et al. 2008, A&A 485, 823 | ATLAS9 + SYNTHE, against Vega, the Sun, Arcturus and ELODIE stars | "increasingly poor match performances of synthetic models when fitting the observed SEDs at shorter wavelengths". | Residual scatter 0.7 %, 4.5 % and 8.8 % for Vega, the Sun and Arcturus at R = 100 000. |

Our fits, 50 SDSS galaxies (`results/sdss-mask-nad-2026-11-24`), median of fits, blue of 4728 Å against red:

- χ² per pixel is 1.21 against 1.07. Blue is higher in 36 of 50 fits.
- Scatter above the catalogue noise is 2.8 % against 1.0 % of the model flux.
- The largest band offset is at 4600 to 4728 Å, the C2 4668 band. The mean is −0.48σ at 4600 to 4700 Å and −0.87σ at 4666.1 to 4728 Å. χ² per pixel is 1.72 and 1.82.
- The LEGA-C window 4074.5 to 4666.1 Å is fully below 4728 Å.

Source: `~/.claude/scripts/hermes-bridge/results/t_fe81f500-detail.md`, sections 4 and 5.

The residual test cannot show:

- **Smooth or broadband misfit.** The order-10 calibration polynomial removes it. In LEGA-C it removes a 100 Å band mean by construction.
- **Misfit that the free parameters absorb.** A wrong line strength can move age, [Fe/H], [α/Fe], C, N, σ or dust. The residual then stays small.
- **Absolute accuracy.** χ² per pixel grows with S/N. It also assumes that the catalogue noise is correct.
- **Masked features.** Ca II H and K, Hε, Ca4227 and Na D have no fitted pixel.

### Absorption features, rest 3600 to 7100 Å

Copied from section 4 of the references file.

Last column: the feature has a basis for a mask if (a) it depends on an abundance that the model cannot set and a cited paper measures that abundance away from the model value, or (b) a cited paper reports non-stellar absorption in the band. This test is the worker's, not from a paper.

Measured in massive early-type galaxies (C14 abstract, §5.2, §8): [Fe/H] changes by < 0.1 dex over the sample. Mg and O go from ≈ 0.0 at low σ to ≈ 0.25 at high σ. Si and Ti rise less. "Ca tracks Fe rather than O". [C/Fe] and [N/Fe] are above 0.2 at high σ. [Na/Fe] goes from −0.16 to +0.43. At z ~ 0.7 the patterns are "strikingly similar to those at z ~ 0" (B23 abstract).

| Feature | Model behaviour when [α/Fe] rises at fixed [Fe/H] (P25 §3.2.3, Figs. 10-12) | Depends on | Evidence for massive ellipticals | Basis for a mask |
|---|---|---|---|---|
| H8 to H16, Hδ, Hγ | Produced. Hγ_A and Hδ_A get weaker. More sensitive than Hβ. | Age, [Fe/H], [α/Fe] | Not stated in the sources read. | None found |
| Hβ | Produced. At [Fe/H] = 0: no clear change above 1 Gyr. Weaker at log age 8.5 to 9. | Age, [Fe/H] | Not stated. | None found |
| Hα | Produced. P25 does not discuss it. | Not stated | Not stated. | None found |
| Ca II H and K | Deeper (P25 §3.2.1, Fig. 5). | Ca, tied to [α/Fe] | Ca follows Fe, not Mg (C14). | Yes, (a) |
| 4000 Å break | Produced (D4000, Bruzual 1983). Size of change: not stated in text. | Not stated | Not stated. | None found |
| CN1, CN2 | Weaker. | C, N, O | [C/Fe], [N/Fe] > 0.2 at high σ (C14 §5.2, Fig. 13). | Yes, (a), unless the C/N response is on |
| G4300 | Weaker. | C | Same as CN. | Yes, (a), unless the C/N response is on |
| Ca4227 | Much stronger. Also stronger at fixed [Z/H]. | Ca, tied to [α/Fe] | Ca follows Fe (C14). | Yes, (a) |
| Fe4383 | Weaker above 1 Gyr. Also carbon-sensitive. | Fe, C | [Fe/H] is free. C as for CN. | Fe: none. C: as CN |
| Fe4531 | Stronger. | Ti, tied to [α/Fe] | Ti rises less than Mg (C14 abstract). | Partly, (a) |
| Fe4668 (C2 4668) | "Dramatically decreases" above 1 Gyr. | C | Theoretical spectra are weaker than MILES stars (Knowles et al. 2019, cited in P25 §3.3.2). [C/Fe] > 0.2 (C14). | Yes, (a) |
| Fe5015 | Stronger. Weaker at fixed [Z/H]. | Ti, Fe | Ti rises less than Mg (C14). | Partly, (a) |
| Mg b | Most sensitive index to [α/Fe]. Stronger also at fixed [Z/H]. | Mg, tied to [α/Fe] | Mg ≈ O. Ca, Ti and Si do not follow Mg (C14). | Mg can be set. The other α elements then move with it. |
| Fe5270, Fe5335 | Weaker above 1 Gyr. | Fe | [Fe/H] is free. | None found |
| Na D | Weaker. "Behaves as Fe-sensitive lines". | Na, not free | [Na/Fe] −0.16 to +0.43. The 5895 Å line is "well-known to be affected by" the interstellar medium (C14 §5.2). | Yes, (a) and (b) |
| TiO1, TiO2 | Stronger. Isochrone and spectrum contribute about equally. Very sensitive to temperature. | Ti, O, T_eff of M stars | Ti rises less than Mg (C14). IMF dependence stated only for young ages (P25 §3.2.3). | Partly, (a) |

State of each feature in the current fits (`t_0c96cd9b-detail.md:111`, `:121`, `:227-272`): Ca II K, Ca II H, Hε and Ca4227 have no fitted pixel, because the `emission_lines` list masks 3934.77, 3966.6, 3973.3 and 4227.92 Å ± 1500 km/s. All other features above are fitted in the wide range. In the narrow window the fitted features are Hδ, CN, G4300, Hγ, Fe4383, Ca4455, Fe4531 and 0.36 of Fe4668.
