---
name: chronometer-checklist
description: Use before you plan, run, check or report a cosmic-chronometer fit, a chronometer sample or an age-redshift slope. It gives Liu Hao's decisions for chronometer work and his open items. It also gives the table of masked pixels, the reason for each mask, and the limits of the stellar population model.
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
| Ca II K | 3915.08 to 3954.46 Å rest (3934.77 Å ± 1500 km/s) | SDSS DR17. LEGA-C DR3 only in the window that starts at 3850.0 Å. | His order, 2026-09-30: "i was told to mask all Ca". Papers: the grid changes Ca with [α/Fe], and in early-type galaxies "Ca tracks Fe". | `wiki/research/experiments/e-mask-all-ca.md`. P25 §2.1. C14 §5.2. |
| Ca II H, with Hε | 3946.75 to 3993.18 Å rest (3966.6 and 3973.3 Å ± 1500 km/s) | Same as Ca II K | Ca II H: same as Ca II K. Hε (3971.20 Å) and [Ne III] 3968.65 Å are in the range. No record gives a reason to mask Hε. | Same as Ca II K. Hε: NIST ASD. [Ne III]: FSPS `emlines_info.dat`. |
| Ca I 4227 | 4206.77 to 4249.07 Å rest (4227.92 Å ± 1500 km/s) | LEGA-C DR3, SDSS DR17 | Same order as Ca II K. Jonah Powley, meeting of 2026-09-17: "Ca I can be masked because of potential IGM contamination". Papers: Ca4227 becomes much stronger with [α/Fe] in the model. | `e-mask-all-ca.md`. P25 §3.2.3. C14 §5.2. |
| Na D | 5878.50 to 5911.01 Å rest (Lick band 5876.875 to 5909.375 Å air) | SDSS DR17. The LEGA-C windows end at 4666.1 Å. | His order, 2026-11-24: "okay, mask na d". The model has no free Na. [Na/Fe] is −0.16 to +0.43 in early-type galaxies. Interstellar gas absorbs at 5895 Å. With Na D fitted, the data are below the model in 49 of 49 SDSS galaxies. | C14 §5.2. Trager et al. 1998, arXiv:astro-ph/9712258, Table 2. `~/.claude/scripts/hermes-bridge/results/t_dcbba686-detail.md` |

P25 and C14 are defined in the next section.

- **Na D is a setting of the run.** Set `"masked_absorption_features": ["NaD"]` in `experiment.json`. The notebook default is an empty list.
- **Pixels outside the window are not fitted.** Windows in the run configs: SDSS DR17 3604.0 to 7079.3 Å. LEGA-C DR3 4074.5 to 4666.1 Å. One arm of `results/legac-break-fixed-grid-2026-11-24` starts at 3850.0 Å to include the 4000 Å break.
- **Not masked: Hβ, [O II], [O III].** Each emission line of the FSPS list gets a free flux (`emission_line_marginalisation: True`). Liu Hao, 2026-09-30: "keep o unmasked as default is fine". The LEGA-C DR2 fits before that date masked Hβ and [O III]. The current code does not.
- **No sky-line mask.** `sky_lines_air` is an empty list.
- **Wiki table:** `wiki/notes/spectral-masks.md`, built as the page `/n/spectral-masks/`.

## Stellar population model: what it contains and its limits

Liu Hao, 2026-11-24: "we need to have a comprehensive understanding of the park alpha enhanced sps / isochrone paper and the model limitations and save it in the chronoemter skill".

The full section, with each source reference, is `references/stellar-population-model.md`. Read it before you make a statement about the model. P25 is Park et al. 2025, ApJ 994:165, arXiv:2410.21375v1. D26 is Dotter et al. 2026, arXiv:2602.22012v1. C14 is Conroy, Graves & van Dokkum 2014, ApJ 780:33.

Summary:

1. The grid is α-MC: MIST isochrones, C3K v2.3 spectra and one Kroupa IMF (P25 §2.1 to §2.3).
2. One [α/Fe] sets O, Ne, Mg, Si, S, Ar, Ca and Ti together. No α element is free alone (P25 §2.1, §2.4).
3. C and N are solar-scaled in the grid (P25 §2.4). Ceridwen adds the alf C and N response with free `cfe` and `nfe`. There is no free Na.
4. The line list is tuned for 4728 Å to 1 µm only (P25 §2.2). The LEGA-C window 4074.5 to 4666.1 Å is fully below 4728 Å.
5. `logzsol` is [Fe/H], not total metallicity (`ceridwen/docs/afe.md:47-51`).
6. The age axis has 107 nodes with a step of 0.05 dex (P25 §2.3). One step is 12.2 % in age. Four nodes are older than 13.8 Gyr.
7. `SedModel` refuses an SFH node more than 0.5 % older than the Universe at the galaxy redshift (`ceridwen/ceridwen/model/model.py:232`).
8. The model has no post-AGB stars, no white dwarfs and no full horizontal branch (P25 §3.1 and D26 §2.7, §3.4).
9. The spectra are 1D, plane-parallel and LTE (P25 §2.4). Opacity tables are missing at the metal-rich corner (P25 §2.1).
10. P25 shows no comparison with observed galaxy spectra (P25 §1). C2 4668 is much weaker than in models made from observed stars (P25 §3.3.2).

### Absorption features, rest 3600 to 7100 Å

Copied from section 4 of the references file.

Last column: the feature has a basis for a mask if (a) it depends on an abundance that the model cannot set and a cited paper measures that abundance away from the model value, or (b) a cited paper reports non-stellar absorption in the band. This test is the worker's, not from a paper.

Measured in massive early-type galaxies (C14 abstract, §5.2, §8): [Fe/H] changes by < 0.1 dex over the sample. Mg and O go from ≈ 0.0 at low σ to ≈ 0.25 at high σ. Si and Ti rise less. "Ca tracks Fe rather than O". [C/Fe] and [N/Fe] are above 0.2 at high σ. [Na/Fe] goes from −0.16 to +0.43. At z ~ 0.7 the patterns are "strikingly similar to those at z ~ 0" (B23 abstract).

| Feature | Model behaviour when [α/Fe] rises at fixed [Fe/H] (P25 §3.2.3, Figs. 9-11) | Depends on | Evidence for massive ellipticals | Basis for a mask |
|---|---|---|---|---|
| H8 to H16, Hδ, Hγ | Produced. Hγ_A and Hδ_A get weaker. More sensitive than Hβ. | Age, [Fe/H], [α/Fe] | Not stated in the sources read. | None found |
| Hβ | Produced. At [Fe/H] = 0: no clear change above 1 Gyr. Weaker at log age 8.5 to 9. | Age, [Fe/H] | Not stated. | None found |
| Hα | Produced. P25 does not discuss it. | Not stated | Not stated. | None found |
| Ca II H and K | Deeper (P25 §3.2.1, Fig. 4). | Ca, tied to [α/Fe] | Ca follows Fe, not Mg (C14). | Yes, (a) |
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
