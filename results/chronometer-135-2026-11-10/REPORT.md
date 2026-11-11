# Chronometer test on the 135 LEGA-C DR2 quiescent galaxies

Liu Hao, 2026-11-10 23:55: "sure, run all of them, i'm most interested in the effects of C and N and the result on the chronometer test, but do all of them"

Arms (a)–(e) are from the overseer-astronomy brief. Arms (f) and (g) (answer to the checkpoint) and (h)–(j) (section "Rest-frame windows") are from its follow-ups, under Liu Hao, 2026-11-10: "you can research and run experiments overnight, i'll sleep soon".

## Setup

| arm | settings (notebook keys; rest are production defaults) | fits run here | reused |
|---|---|---|---|
| (a) | none | 0 | 135 October refits, `results/dr2-refit-2026-10-12` |
| (b) | `abundance_response`: alf C/N responses (`data/raw/alf/cda32111…`) | 135 | – |
| (c) | as (b), `fix_afe` 0.25 | 135 | – |
| (d) | `masked_absorption_features` CN4150, G4300, Fe4383, C4668 | 74 | 61, `results/carbon-mask-2026-11-08` |
| (e) | as (c), `rest_range` [4155.0, 4438.1] | 135 (130 valid) | – |
| (f) | as (b), `rest_range` [0.0, 5144.0] | 61 (Mg b group) | 74 from (b) |
| (g) | `rest_range` [0.0, 5144.0] | 61 (Mg b group) | 74 from (a) |

- Fit seed 20260832 in every fit (checked in each derived-output file). Modal A100-40GB through `scripts/experiment.py`, revision 99c179ba.
- Modal cost estimates: (b) $19.29, (d) $7.21, (c) $17.43, (f) $8.53, (g) $5.77, (e) $13.63; total $71.86. Billed cost after credits was $0.00 before each launch and after the last run.
- Age is the posterior median mass-weighted age from `ceridwen_derived_outputs.h5`. [Fe/H] is `logzsol`. [C/Fe] and [N/Fe] are weighted medians of the nested-sampling samples.
- Mg b group (October coverage): the October fit has fitted pixels in the Mg b bandpass (`feature_windows(['Mgb'])`). 61 galaxies in the Mg b group, 74 in the no-Mg b group, in every arm. These are the same 61 galaxies as the carbon-mask reuse.
- Arms (e), (f), (g), (h), (i) and (j) fit zero Mg b bandpass pixels in every galaxy. The 61 cut fits of (f) and (g) and all fits of (e), (h), (i), (j) also fit zero pixels in the Mg b pseudo-continua. Two reused no-Mg b-group fits in (f) and (g), M12_181945 and M6_240899, keep 26 and 28 pixels of the blue pseudo-continuum.
- Mg b cut for (f), (g): Trager et al. 1998, ApJS 116, 1, Table 2, Mg b: bandpass 5160.125–5192.625 Å, pseudo-continua 5142.625–5161.375 and 5191.375–5206.375 Å (air). In vacuum (`air2vac`) the full window is 5144.058–5207.825 Å. `rest_range` [0.0, 5144.0] Å. All 61 cut fits have zero fitted pixels in the window.
- Common range for (e): the widest interval that lies inside the fitted rest range of at least 129 of the 135 October fits (95 percent) is 4155.0–4438.1 Å (rest vacuum). Six galaxies do not fully cover it: M11_212718, M12_181421, M7_120758, M10_189698, M2_97310, M5_127946.
- Bootstrap: 10000 resamples of galaxies, seed 20261110. Each draw refits the line (and the step model).
- Samples: "all 135" uses every fit of an arm. (e) has 130 valid fits, so its rows use 130 galaxies. "Common 130" uses the 130 galaxies valid in all seven arms.

## Pin difference

| arm | Astro / Ceridwen pins (fits) |
|---|---|
| (a) | 7033ef13/d7c0536f: 1; 85d3acbf/d7c0536f: 63; a9550ce2/d7c0536f: 71 |
| (b) | 99c179ba/13791e0e: 135 |
| (c) | 99c179ba/13791e0e: 135 |
| (d) | 33a06784/a0b1f6ed: 61; 99c179ba/13791e0e: 74 |
| (e) | 99c179ba/13791e0e: 130 |
| (f) | 99c179ba/13791e0e: 135 |
| (g) | 85d3acbf/d7c0536f: 37; 99c179ba/13791e0e: 61; a9550ce2/d7c0536f: 37 |

- The production `SETTINGS`/`PRIORS` cell is identical at a9550ce2, 85d3acbf and 7033ef13. At 99c179ba it only adds keys: `data_source` "legac_dr2", `mock_data` None, `abundance_response` None, `sky_lines_air` [], `rest_range` None, `photometry_excluded` [], `spectrum_floor_anchor` "model", `masked_absorption_features` [], and priors `cfe`, `nfe` (sampled only with `abundance_response`).
- results/cn-response-2026-11-10: with those keys off, predictions are bitwise equal between Ceridwen a0b1f6e and 13791e0.
- Pin check: the same-pin baseline of `results/carbon-mask-2026-11-08/check` (33a06784/a0b1f6ed) against the October refit, 10 galaxies: mean Δage +0.037 Gyr (range -0.052 to +0.149), mean Δ[α/Fe] -0.0010, mean Δ[Fe/H] -0.0027.

## Failed validations

| arm | fits | valid | failed |
|---|---|---|---|
| (a) | 135 | 135 | 0 |
| (b) | 135 | 135 | 0 |
| (c) | 135 | 135 | 0 |
| (d) | 135 | 135 | 0 |
| (e) | 135 | 130 | 5 |
| (f) | 135 | 135 | 0 |
| (g) | 135 | 135 | 0 |

- (e): M1_126578 (z 0.750), M13_245763 (z 0.754), M10_189698 (z 0.926), M5_127946 (z 0.939), M2_97310 (z 0.943) stop on the GPU with `ValueError: attempt to get argmax of an empty sequence` (`ceridwen/ceridwen/likelihood/emission_lines.py:374`). No emission line has fitted pixels in 4155.0–4438.1 Å for these galaxies: for the first two, Hγ and [O III] 4363 fall in the masked telluric band; the other three spectra end below rest 4341 Å. Not rerun; the error is deterministic.
- (b): the local figure rebuild of `scripts/experiment.py` failed for 47 C/N fits and wrote the failed notebook over the GPU notebook. `recover.py` re-executed those notebooks on CPU from the saved samples (sampler not rerun, result and derived files byte-identical); receipt in `cn-free/run/recovery.json`. For (c), (e) and (f) the driver was stopped when the rebuild started. All counts above are after this.

## Age–redshift slope

d t_univ/dz is the straight-line slope of the Planck18 age of the universe (ceridwen `age_gyr`, the fit cosmology) at the same redshifts. Its tangent at z = 0.728 is -5.52 Gyr/z.

### All galaxies of each arm

| arm | group | N | z med | slope (Gyr/z) | bootstrap 16–84 | scatter (Gyr) | d t_univ/dz, line | H (km/s/Mpc) | H from 16–84 |
|---|---|---|---|---|---|---|---|---|---|
| (a) baseline | all | 135 | 0.728 | -1.55 | -2.23 to -0.88 | 0.82 | -5.17 | 365 | 254–644 |
| (b) C/N free | all | 135 | 0.728 | +0.97 | +0.20 to +1.75 | 0.99 | -5.17 | – | none (slope > 0) |
| (c) C/N free, [α/Fe] = +0.25 | all | 135 | 0.728 | +1.18 | +0.42 to +1.95 | 1.04 | -5.17 | – | none (slope > 0) |
| (d) carbon mask | all | 135 | 0.728 | -2.72 | -3.40 to -2.04 | 0.82 | -5.17 | 208 | 166–278 |
| (e) as (c), 4155.0–4438.1 Å | all | 130 | 0.728 | -3.77 | -4.42 to -3.09 | 0.80 | -5.19 | 150 | 128–183 |
| (f) as (b), Mg b cut | all | 135 | 0.728 | -0.42 | -1.14 to +0.30 | 0.94 | -5.17 | 1359 | 494–∞ |
| (g) baseline, Mg b cut | all | 135 | 0.728 | -1.11 | -1.78 to -0.47 | 0.81 | -5.17 | 509 | 318–1211 |
| (a) baseline | Mg b group (October coverage) | 61 | 0.682 | -2.77 | -5.07 to -0.45 | 0.86 | -5.82 | 210 | 115–1306 |
| (b) C/N free | Mg b group (October coverage) | 61 | 0.682 | -2.76 | -5.35 to +0.26 | 1.00 | -5.82 | 211 | 109–∞ |
| (c) C/N free, [α/Fe] = +0.25 | Mg b group (October coverage) | 61 | 0.682 | -3.40 | -6.07 to -0.25 | 1.02 | -5.82 | 171 | 96–2335 |
| (d) carbon mask | Mg b group (October coverage) | 61 | 0.682 | -4.76 | -7.22 to -2.35 | 0.89 | -5.82 | 122 | 80–248 |
| (e) as (c), 4155.0–4438.1 Å | Mg b group (October coverage) | 60 | 0.681 | -4.68 | -7.30 to -2.15 | 0.86 | -5.82 | 124 | 80–270 |
| (f) as (b), Mg b cut | Mg b group (October coverage) | 61 | 0.682 | -7.13 | -9.29 to -4.75 | 0.92 | -5.82 | 81 | 63–122 |
| (g) baseline, Mg b cut | Mg b group (October coverage) | 61 | 0.682 | -3.45 | -5.92 to -1.20 | 0.84 | -5.82 | 168 | 98–486 |
| (a) baseline | no-Mg b group | 74 | 0.822 | -1.35 | -2.28 to -0.47 | 0.79 | -4.97 | 396 | 236–1130 |
| (b) C/N free | no-Mg b group | 74 | 0.822 | -2.07 | -3.06 to -1.14 | 0.86 | -4.97 | 260 | 175–469 |
| (c) C/N free, [α/Fe] = +0.25 | no-Mg b group | 74 | 0.822 | -1.72 | -2.76 to -0.73 | 0.93 | -4.97 | 312 | 194–731 |
| (d) carbon mask | no-Mg b group | 74 | 0.822 | -2.70 | -3.66 to -1.79 | 0.78 | -4.97 | 198 | 147–300 |
| (e) as (c), 4155.0–4438.1 Å | no-Mg b group | 70 | 0.809 | -4.42 | -5.41 to -3.42 | 0.75 | -4.98 | 122 | 100–158 |
| (f) as (b), Mg b cut | no-Mg b group | 74 | 0.822 | -2.07 | -3.06 to -1.14 | 0.86 | -4.97 | 260 | 175–469 |
| (g) baseline, Mg b cut | no-Mg b group | 74 | 0.822 | -1.35 | -2.28 to -0.47 | 0.79 | -4.97 | 396 | 236–1130 |

### Common 130 (same galaxies in every arm)

| arm | group | N | z med | slope (Gyr/z) | bootstrap 16–84 | scatter (Gyr) | d t_univ/dz, line | H (km/s/Mpc) | H from 16–84 |
|---|---|---|---|---|---|---|---|---|---|
| (a) baseline | all | 130 | 0.728 | -1.34 | -2.03 to -0.64 | 0.82 | -5.19 | 424 | 279–887 |
| (b) C/N free | all | 130 | 0.728 | +1.36 | +0.61 to +2.16 | 0.99 | -5.19 | – | none (slope > 0) |
| (c) C/N free, [α/Fe] = +0.25 | all | 130 | 0.728 | +1.56 | +0.78 to +2.37 | 1.04 | -5.19 | – | none (slope > 0) |
| (d) carbon mask | all | 130 | 0.728 | -2.44 | -3.14 to -1.73 | 0.82 | -5.19 | 232 | 180–326 |
| (e) as (c), 4155.0–4438.1 Å | all | 130 | 0.728 | -3.77 | -4.42 to -3.09 | 0.80 | -5.19 | 150 | 128–183 |
| (f) as (b), Mg b cut | all | 130 | 0.728 | -0.08 | -0.79 to +0.66 | 0.94 | -5.19 | 7243 | 712–∞ |
| (g) baseline, Mg b cut | all | 130 | 0.728 | -0.89 | -1.57 to -0.22 | 0.81 | -5.19 | 633 | 360–2597 |
| (a) baseline | Mg b group (October coverage) | 60 | 0.681 | -3.24 | -5.64 to -0.94 | 0.86 | -5.82 | 180 | 103–621 |
| (b) C/N free | Mg b group (October coverage) | 60 | 0.681 | -3.54 | -6.11 to -0.73 | 0.99 | -5.82 | 164 | 95–794 |
| (c) C/N free, [α/Fe] = +0.25 | Mg b group (October coverage) | 60 | 0.681 | -4.18 | -6.83 to -1.24 | 1.02 | -5.82 | 139 | 85–467 |
| (d) carbon mask | Mg b group (October coverage) | 60 | 0.681 | -5.26 | -7.87 to -2.91 | 0.89 | -5.82 | 111 | 74–200 |
| (e) as (c), 4155.0–4438.1 Å | Mg b group (October coverage) | 60 | 0.681 | -4.68 | -7.30 to -2.15 | 0.86 | -5.82 | 124 | 80–270 |
| (f) as (b), Mg b cut | Mg b group (October coverage) | 60 | 0.681 | -7.89 | -10.01 to -5.72 | 0.91 | -5.82 | 74 | 58–102 |
| (g) baseline, Mg b cut | Mg b group (October coverage) | 60 | 0.681 | -4.06 | -6.66 to -1.79 | 0.83 | -5.82 | 143 | 87–325 |
| (a) baseline | no-Mg b group | 70 | 0.809 | -0.92 | -1.90 to -0.01 | 0.79 | -4.98 | 585 | 285–48958 |
| (b) C/N free | no-Mg b group | 70 | 0.809 | -1.50 | -2.51 to -0.55 | 0.86 | -4.98 | 360 | 215–987 |
| (c) C/N free, [α/Fe] = +0.25 | no-Mg b group | 70 | 0.809 | -1.14 | -2.21 to -0.12 | 0.93 | -4.98 | 473 | 245–4366 |
| (d) carbon mask | no-Mg b group | 70 | 0.809 | -2.18 | -3.16 to -1.25 | 0.77 | -4.98 | 248 | 171–432 |
| (e) as (c), 4155.0–4438.1 Å | no-Mg b group | 70 | 0.809 | -4.42 | -5.41 to -3.42 | 0.75 | -4.98 | 122 | 100–158 |
| (f) as (b), Mg b cut | no-Mg b group | 70 | 0.809 | -1.50 | -2.51 to -0.55 | 0.86 | -4.98 | 360 | 215–987 |
| (g) baseline, Mg b cut | no-Mg b group | 70 | 0.809 | -0.92 | -1.90 to -0.01 | 0.79 | -4.98 | 585 | 285–48958 |

## ρ([α/Fe], z) and medians

Spearman ρ. (c) and (e) fix [α/Fe] at +0.25.

| arm | group | N | ρ([α/Fe], z) | median [α/Fe] | median age (Gyr) | median [Fe/H] | median [C/Fe] | median [N/Fe] |
|---|---|---|---|---|---|---|---|---|
| (a) baseline | all | 135 | -0.47 (p 0.000) | -0.03 | 4.04 | -0.29 | – | – |
| (a) baseline | Mg b group (October coverage) | 61 | -0.23 (p 0.075) | +0.08 | 4.23 | -0.24 | – | – |
| (a) baseline | no-Mg b group | 74 | -0.15 (p 0.207) | -0.16 | 3.84 | -0.33 | – | – |
| (b) C/N free | all | 135 | -0.24 (p 0.006) | +0.12 | 4.44 | -0.42 | -0.02 | +0.30 |
| (b) C/N free | Mg b group (October coverage) | 61 | -0.27 (p 0.034) | +0.21 | 3.73 | -0.28 | +0.12 | +0.12 |
| (b) C/N free | no-Mg b group | 74 | +0.37 (p 0.001) | -0.05 | 4.70 | -0.57 | -0.14 | +0.45 |
| (c) C/N free, [α/Fe] = +0.25 | all | 135 | fixed | +0.25 | 4.38 | -0.52 | +0.11 | +0.38 |
| (c) C/N free, [α/Fe] = +0.25 | Mg b group (October coverage) | 61 | fixed | +0.25 | 3.68 | -0.29 | +0.13 | +0.18 |
| (c) C/N free, [α/Fe] = +0.25 | no-Mg b group | 74 | fixed | +0.25 | 4.64 | -0.63 | +0.07 | +0.60 |
| (d) carbon mask | all | 135 | -0.56 (p 0.000) | +0.09 | 4.39 | -0.37 | – | – |
| (d) carbon mask | Mg b group (October coverage) | 61 | -0.39 (p 0.002) | +0.20 | 4.66 | -0.37 | – | – |
| (d) carbon mask | no-Mg b group | 74 | -0.26 (p 0.027) | -0.11 | 4.27 | -0.38 | – | – |
| (e) as (c), 4155.0–4438.1 Å | all | 130 | fixed | +0.25 | 4.93 | -0.43 | -0.05 | +0.38 |
| (e) as (c), 4155.0–4438.1 Å | Mg b group (October coverage) | 60 | fixed | +0.25 | 4.99 | -0.42 | -0.07 | +0.35 |
| (e) as (c), 4155.0–4438.1 Å | no-Mg b group | 70 | fixed | +0.25 | 4.81 | -0.44 | -0.04 | +0.43 |
| (f) as (b), Mg b cut | all | 135 | +0.22 (p 0.011) | -0.08 | 4.64 | -0.42 | -0.13 | +0.32 |
| (f) as (b), Mg b cut | Mg b group (October coverage) | 61 | +0.10 (p 0.428) | -0.09 | 4.52 | -0.29 | -0.11 | +0.21 |
| (f) as (b), Mg b cut | no-Mg b group | 74 | +0.37 (p 0.001) | -0.05 | 4.70 | -0.57 | -0.14 | +0.45 |
| (g) baseline, Mg b cut | all | 135 | -0.29 (p 0.001) | -0.10 | 3.93 | -0.30 | – | – |
| (g) baseline, Mg b cut | Mg b group (October coverage) | 61 | -0.09 (p 0.482) | -0.06 | 4.06 | -0.26 | – | – |
| (g) baseline, Mg b cut | no-Mg b group | 74 | -0.15 (p 0.207) | -0.16 | 3.84 | -0.33 | – | – |

## Mg b offset and step model

- Offset: median residual of the Mg b group minus median residual of the no-Mg b group, about one straight line in z.
- Step model: age = a + b·z + c·[Mg b group], least squares; b is the joint slope, c the step.
- Brackets: bootstrap 16–84.

| arm | sample | N | Mg b offset (Gyr) | joint slope (Gyr/z) | step (Gyr) | H from joint slope |
|---|---|---|---|---|---|---|
| (a) baseline | all 135 (e: 130) | 135 | +0.27 (+0.08 to +0.36) | -1.58 (-2.43 to -0.74) | -0.01 (-0.19 to +0.17) | 358 |
| (b) C/N free | all 135 (e: 130) | 135 | -0.86 (-0.95 to -0.54) | -2.18 (-3.10 to -1.27) | -0.99 (-1.19 to -0.79) | 260 |
| (c) C/N free, [α/Fe] = +0.25 | all 135 (e: 130) | 135 | -0.85 (-0.96 to -0.62) | -1.99 (-2.97 to -1.02) | -0.99 (-1.22 to -0.77) | 284 |
| (d) carbon mask | all 135 (e: 130) | 135 | +0.11 (-0.06 to +0.20) | -3.03 (-3.93 to -2.16) | -0.10 (-0.29 to +0.09) | 186 |
| (e) as (c), 4155.0–4438.1 Å | all 135 (e: 130) | 130 | -0.17 (-0.29 to -0.04) | -4.46 (-5.38 to -3.55) | -0.21 (-0.41 to -0.02) | 127 |
| (f) as (b), Mg b cut | all 135 (e: 130) | 135 | -0.21 (-0.38 to -0.00) | -2.88 (-3.80 to -1.98) | -0.77 (-0.98 to -0.57) | 196 |
| (g) baseline, Mg b cut | all 135 (e: 130) | 135 | +0.09 (-0.11 to +0.19) | -1.69 (-2.54 to -0.86) | -0.18 (-0.37 to -0.00) | 335 |
| (a) baseline | common 130 | 130 | +0.28 (+0.07 to +0.36) | -1.31 (-2.17 to -0.45) | +0.01 (-0.17 to +0.19) | 433 |
| (b) C/N free | common 130 | 130 | -0.83 (-0.94 to -0.55) | -1.84 (-2.78 to -0.93) | -0.99 (-1.19 to -0.79) | 308 |
| (c) C/N free, [α/Fe] = +0.25 | common 130 | 130 | -0.82 (-0.96 to -0.63) | -1.65 (-2.64 to -0.67) | -0.99 (-1.21 to -0.77) | 344 |
| (d) carbon mask | common 130 | 130 | +0.10 (-0.05 to +0.19) | -2.69 (-3.60 to -1.81) | -0.08 (-0.27 to +0.10) | 210 |
| (e) as (c), 4155.0–4438.1 Å | common 130 | 130 | -0.17 (-0.29 to -0.04) | -4.46 (-5.38 to -3.55) | -0.21 (-0.41 to -0.02) | 127 |
| (f) as (b), Mg b cut | common 130 | 130 | -0.21 (-0.39 to -0.01) | -2.56 (-3.52 to -1.64) | -0.76 (-0.97 to -0.56) | 221 |
| (g) baseline, Mg b cut | common 130 | 130 | +0.05 (-0.12 to +0.17) | -1.44 (-2.31 to -0.60) | -0.17 (-0.35 to +0.01) | 392 |

## Paired age differences against z

Per galaxy, newer arm minus older arm, on galaxies valid in both. Slope of Δage on z with bootstrap 16–84. Per-galaxy values: `paired-age-differences-per-galaxy.csv`.

| pair | group | N | median Δage (Gyr) | Δage 16–84 | fraction older | dΔage/dz (Gyr/z) | ρ(Δage, z) |
|---|---|---|---|---|---|---|---|
| (b) − (a) | all | 135 | +0.31 | -0.54 to +1.00 | 0.70 | +2.53 (+2.01 to +3.06) | +0.36 (p 0.000) |
| (b) − (a) | Mg b group (October coverage) | 61 | -0.15 | -0.92 to +0.48 | 0.44 | +0.01 (-2.19 to +2.60) | +0.01 (p 0.944) |
| (b) − (a) | no-Mg b group | 74 | +0.52 | +0.09 to +1.15 | 0.92 | -0.71 (-1.40 to -0.04) | -0.12 (p 0.295) |
| (c) − (a) | all | 135 | +0.20 | -0.61 to +0.90 | 0.64 | +2.73 (+2.21 to +3.26) | +0.40 (p 0.000) |
| (c) − (a) | Mg b group (October coverage) | 61 | -0.18 | -1.02 to +0.35 | 0.38 | -0.64 (-2.77 to +1.91) | -0.06 (p 0.673) |
| (c) − (a) | no-Mg b group | 74 | +0.50 | +0.02 to +1.13 | 0.85 | -0.37 (-1.12 to +0.39) | +0.01 (p 0.920) |
| (d) − (a) | all | 135 | +0.25 | -0.05 to +0.68 | 0.79 | -1.17 (-1.43 to -0.91) | -0.28 (p 0.001) |
| (d) − (a) | Mg b group (October coverage) | 61 | +0.32 | +0.07 to +0.71 | 0.85 | -1.99 (-3.07 to -1.02) | -0.23 (p 0.074) |
| (d) − (a) | no-Mg b group | 74 | +0.14 | -0.07 to +0.60 | 0.74 | -1.35 (-1.71 to -0.99) | -0.37 (p 0.001) |
| (e) − (a) | all | 130 | +0.72 | -0.16 to +1.51 | 0.79 | -2.43 (-3.10 to -1.74) | -0.25 (p 0.005) |
| (e) − (a) | Mg b group (October coverage) | 60 | +0.69 | +0.03 to +1.60 | 0.85 | -1.44 (-3.44 to +0.63) | -0.11 (p 0.399) |
| (e) − (a) | no-Mg b group | 70 | +0.73 | -0.31 to +1.46 | 0.74 | -3.50 (-4.63 to -2.38) | -0.42 (p 0.000) |
| (f) − (a) | all | 135 | +0.45 | -0.23 to +1.09 | 0.76 | +1.13 (+0.65 to +1.62) | +0.12 (p 0.165) |
| (f) − (a) | Mg b group (October coverage) | 61 | +0.21 | -0.80 to +0.85 | 0.56 | -4.37 (-6.21 to -2.36) | -0.25 (p 0.048) |
| (f) − (a) | no-Mg b group | 74 | +0.52 | +0.09 to +1.15 | 0.92 | -0.71 (-1.40 to -0.04) | -0.12 (p 0.295) |
| (g) − (a) | all | 135 | +0.00 | -0.21 to +0.00 | 0.16 | +0.44 (+0.28 to +0.59) | +0.17 (p 0.049) |
| (g) − (a) | Mg b group (October coverage) | 61 | -0.09 | -0.50 to +0.13 | 0.34 | -0.69 (-1.57 to +0.01) | -0.12 (p 0.347) |
| (g) − (a) | no-Mg b group | 74 | +0.00 | +0.00 to +0.00 | 0.00 | +0.00 (+0.00 to +0.00) | – |
| (c) − (b) | all | 135 | -0.04 | -0.24 to +0.07 | 0.37 | +0.20 (+0.03 to +0.38) | +0.07 (p 0.443) |
| (c) − (b) | Mg b group (October coverage) | 61 | -0.04 | -0.24 to +0.10 | 0.34 | -0.64 (-1.06 to -0.19) | -0.17 (p 0.185) |
| (c) − (b) | no-Mg b group | 74 | -0.03 | -0.24 to +0.07 | 0.39 | +0.35 (+0.11 to +0.59) | +0.21 (p 0.066) |
| (e) − (c) | all | 130 | +0.47 | -0.72 to +1.56 | 0.68 | -5.32 (-5.98 to -4.67) | -0.53 (p 0.000) |
| (e) − (c) | Mg b group (October coverage) | 60 | +1.08 | +0.40 to +2.01 | 0.88 | -0.50 (-3.40 to +1.99) | -0.06 (p 0.666) |
| (e) − (c) | no-Mg b group | 70 | +0.01 | -0.89 to +0.78 | 0.50 | -3.28 (-4.22 to -2.35) | -0.39 (p 0.001) |
| (f) − (b) | all | 135 | +0.00 | +0.00 to +0.36 | 0.32 | -1.39 (-1.70 to -1.10) | -0.44 (p 0.000) |
| (f) − (b) | Mg b group (October coverage) | 61 | +0.15 | -0.22 to +0.93 | 0.70 | -4.38 (-5.81 to -3.18) | -0.46 (p 0.000) |
| (f) − (b) | no-Mg b group | 74 | +0.00 | +0.00 to +0.00 | 0.00 | +0.00 (+0.00 to +0.00) | – |

## Mg b cut, paired changes for the 61 Mg b galaxies

| pair | quantity | N | median Δ | Δ 16–84 | fraction > 0 |
|---|---|---|---|---|---|
| (f) - (b) | [α/Fe] | 61 | -0.22 | -0.39 to -0.07 | 0.03 |
| (f) - (b) | age (Gyr) | 61 | +0.15 | -0.22 to +0.93 | 0.70 |
| (f) - (b) | [C/Fe] | 61 | -0.12 | -0.29 to -0.00 | 0.16 |
| (f) - (b) | [N/Fe] | 61 | +0.01 | -0.09 to +0.22 | 0.64 |
| (g) - (a) | [α/Fe] | 61 | -0.11 | -0.20 to -0.02 | 0.05 |
| (g) - (a) | age (Gyr) | 61 | -0.09 | -0.50 to +0.13 | 0.34 |

The plain grid of (a) and (g) has no [C/Fe] or [N/Fe] parameter.

Per galaxy, sorted by z:

| target | z | Δ[α/Fe] f−b | Δage f−b (Gyr) | Δ[C/Fe] f−b | Δ[N/Fe] f−b | Δ[α/Fe] g−a | Δage g−a (Gyr) |
|---|---|---|---|---|---|---|---|
| M8_160400 | 0.603 | -0.32 | +0.75 | -0.24 | +0.04 | -0.16 | -0.20 |
| M7_122242 | 0.603 | -0.32 | +0.43 | -0.25 | +0.01 | -0.10 | +0.14 |
| M5_172669 | 0.604 | -0.33 | +0.74 | -0.17 | +0.24 | -0.25 | -0.11 |
| M1_211157 | 0.607 | -0.39 | +1.25 | -0.35 | +0.17 | -0.12 | -0.08 |
| M9_233169 | 0.610 | -0.29 | +1.10 | -0.15 | +0.01 | -0.13 | -0.06 |
| M10_228215 | 0.611 | -0.15 | +0.48 | -0.10 | +0.13 | -0.16 | +0.07 |
| M13_248217 | 0.611 | -0.16 | +0.25 | -0.12 | +0.22 | -0.06 | -0.41 |
| M9_232005 | 0.611 | -0.11 | +0.04 | -0.08 | +0.15 | -0.08 | -0.46 |
| M10_228380 | 0.611 | -0.12 | +1.29 | -0.12 | +0.22 | -0.06 | -0.23 |
| M10_215519 | 0.615 | -0.53 | +0.45 | -0.34 | -0.11 | -0.27 | -0.26 |
| M10_233129 | 0.619 | -0.31 | +0.79 | -0.32 | +0.27 | -0.13 | +0.00 |
| M13_232627 | 0.621 | -0.26 | -0.24 | -0.08 | -0.11 | -0.28 | -0.25 |
| M1_208622 | 0.648 | -0.33 | +0.35 | -0.16 | -0.13 | -0.14 | +0.39 |
| M1_210210 | 0.654 | -0.27 | +0.36 | -0.19 | -0.03 | -0.10 | +0.13 |
| M10_231544 | 0.655 | -0.34 | +0.46 | -0.15 | +0.04 | -0.22 | -0.43 |
| M8_161346 | 0.657 | -0.08 | +0.09 | -0.03 | -0.01 | -0.05 | +0.14 |
| M11_257455 | 0.666 | -0.25 | +0.20 | -0.20 | -0.06 | -0.11 | +0.20 |
| M2_206669 | 0.672 | -0.45 | +0.25 | -0.22 | +0.01 | -0.18 | -1.09 |
| M14_103366 | 0.674 | -0.22 | +0.09 | -0.10 | +0.13 | -0.19 | -0.21 |
| M14_38648 | 0.674 | -0.46 | +2.11 | -0.36 | +0.23 | -0.08 | -0.02 |
| M7_113852 | 0.675 | -0.56 | +1.57 | -0.48 | +0.20 | -0.11 | +0.29 |
| M8_148698 | 0.676 | -0.36 | +0.85 | -0.26 | -0.00 | -0.11 | -0.11 |
| M7_147849 | 0.677 | -0.25 | -0.68 | -0.13 | +0.01 | -0.10 | +0.23 |
| M14_31835 | 0.677 | -0.36 | +1.26 | -0.30 | +0.25 | -0.15 | -0.05 |
| M12_185653 | 0.678 | -0.08 | +0.08 | -0.15 | +0.49 | -0.02 | -0.35 |
| M12_102456 | 0.678 | -0.03 | +0.15 | -0.02 | +0.00 | -0.02 | +0.03 |
| M14_27068 | 0.678 | -0.01 | +0.12 | -0.00 | -0.00 | -0.01 | +0.03 |
| M12_184916 | 0.679 | -0.31 | -0.54 | -0.24 | +0.06 | +0.00 | -0.79 |
| M3_119809 | 0.680 | -0.01 | +0.36 | +0.04 | +0.01 | +0.00 | -0.10 |
| M3_119474 | 0.681 | -0.48 | +1.05 | -0.24 | -0.28 | -0.25 | +0.94 |
| M3_119802 | 0.682 | -0.37 | +1.13 | -0.36 | +0.09 | -0.00 | +0.27 |
| M1_126153 | 0.682 | -0.17 | +0.09 | -0.03 | -0.07 | -0.14 | -0.06 |
| M10_225441 | 0.682 | -0.14 | -0.02 | -0.09 | -0.01 | -0.09 | -0.09 |
| M3_117694 | 0.683 | -0.44 | +0.72 | -0.27 | -0.14 | -0.24 | +0.48 |
| M2_134391 | 0.683 | -0.40 | +1.58 | -0.30 | +0.06 | -0.16 | +0.52 |
| M7_146213 | 0.688 | -0.47 | +0.82 | -0.43 | +0.26 | -0.11 | -0.50 |
| M2_210940 | 0.695 | -0.22 | -0.87 | +0.05 | -0.33 | -0.20 | -0.44 |
| M9_218701 | 0.695 | -0.19 | -0.45 | -0.11 | +0.31 | -0.12 | -1.05 |
| M2_129596 | 0.696 | -0.19 | -0.22 | -0.07 | -0.15 | -0.11 | -0.14 |
| M8_147539 | 0.696 | -0.12 | -0.17 | -0.03 | +0.09 | -0.15 | -0.67 |
| M11_245864 | 0.698 | -0.04 | +0.05 | +0.00 | -0.01 | -0.04 | +0.10 |
| M13_230747 | 0.698 | -0.39 | +0.48 | -0.28 | +0.11 | -0.17 | -0.20 |
| M10_213772 | 0.700 | -0.33 | -0.13 | -0.09 | -0.50 | -0.14 | -0.50 |
| M8_150848 | 0.701 | -0.14 | +0.06 | +0.00 | +0.02 | -0.19 | -0.13 |
| M13_259737 | 0.703 | +0.16 | -0.59 | -0.01 | +0.22 | +0.19 | -0.90 |
| M5_165871 | 0.703 | +0.00 | -0.85 | +0.05 | +0.01 | -0.06 | -0.77 |
| M8_162149 | 0.703 | -0.00 | -0.03 | +0.01 | +0.01 | -0.01 | +0.05 |
| M1_206858 | 0.725 | -0.16 | +0.37 | -0.12 | +0.31 | -0.01 | -0.44 |
| M9_212391 | 0.726 | -0.13 | -0.21 | -0.01 | +0.01 | -0.14 | -0.52 |
| M1_205742 | 0.727 | -0.49 | +1.76 | -0.39 | +0.02 | -0.03 | +0.10 |
| M3_120308 | 0.728 | -0.23 | +0.33 | -0.21 | +0.33 | -0.09 | -0.84 |
| M9_229883 | 0.728 | -0.06 | +0.12 | -0.06 | -0.01 | -0.00 | -0.01 |
| M2_133501 | 0.729 | -0.18 | +0.02 | -0.11 | +0.09 | -0.07 | -0.01 |
| M9_227630 | 0.730 | -0.03 | +0.15 | -0.04 | +0.01 | -0.01 | +0.10 |
| M5_238580 | 0.730 | -0.01 | -0.14 | +0.01 | -0.02 | -0.02 | -0.07 |
| M13_243871 | 0.733 | -0.15 | -0.54 | +0.00 | +0.00 | -0.28 | -0.72 |
| M4_107643 | 0.734 | -0.25 | -0.18 | -0.14 | -0.28 | -0.21 | -0.22 |
| M2_134021 | 0.749 | -0.20 | +0.36 | -0.14 | +0.55 | -0.23 | -0.38 |
| M1_139423 | 0.749 | -0.09 | -0.34 | +0.05 | -0.17 | -0.06 | -0.07 |
| M1_126578 | 0.750 | -0.09 | -0.04 | +0.01 | -0.02 | -0.21 | +0.04 |
| M2_130005 | 0.834 | -0.09 | +0.09 | -0.02 | -0.08 | -0.00 | +0.12 |

## (e): fitted pixels in 4155.0–4438.1 Å

Median 667, range 513–785 (130 valid fits). The October fits have median 3604 fitted pixels. Per galaxy (z), sorted by z:

|  |  |  |  |
|---|---|---|---|
| M8_160400 (0.603): 644 | M7_122242 (0.603): 644 | M5_172669 (0.604): 643 | M1_211157 (0.607): 644 |
| M9_233169 (0.610): 647 | M10_228215 (0.611): 646 | M13_248217 (0.611): 647 | M9_232005 (0.611): 644 |
| M10_228380 (0.611): 646 | M10_215519 (0.615): 647 | M10_233129 (0.619): 650 | M13_232627 (0.621): 651 |
| M1_208622 (0.648): 661 | M1_210210 (0.654): 663 | M10_231544 (0.655): 664 | M8_161346 (0.657): 663 |
| M11_257455 (0.666): 669 | M4_117400 (0.669): 667 | M2_206669 (0.672): 670 | M4_105474 (0.673): 666 |
| M14_103366 (0.674): 665 | M14_38648 (0.674): 671 | M7_113852 (0.675): 666 | M8_148698 (0.676): 673 |
| M3_117010 (0.677): 661 | M7_147849 (0.677): 669 | M14_31835 (0.677): 673 | M12_185653 (0.678): 672 |
| M12_102456 (0.678): 660 | M12_180774 (0.678): 668 | M14_27068 (0.678): 674 | M12_184916 (0.679): 674 |
| M12_181945 (0.680): 674 | M11_214296 (0.680): 674 | M3_119809 (0.680): 674 | M3_119474 (0.681): 669 |
| M11_218207 (0.682): 675 | M3_119802 (0.682): 666 | M1_126153 (0.682): 675 | M10_225441 (0.682): 674 |
| M3_117694 (0.683): 668 | M2_134391 (0.683): 676 | M7_146213 (0.688): 672 | M2_210940 (0.695): 680 |
| M9_218701 (0.695): 680 | M2_129596 (0.696): 680 | M11_229551 (0.696): 681 | M8_147539 (0.696): 680 |
| M5_211347 (0.697): 678 | M11_221163 (0.698): 680 | M11_232962 (0.698): 680 | M11_216899 (0.698): 680 |
| M11_245864 (0.698): 681 | M13_230747 (0.698): 679 | M10_213772 (0.700): 682 | M8_150848 (0.701): 681 |
| M13_259737 (0.703): 683 | M5_165871 (0.703): 682 | M8_162149 (0.703): 684 | M3_109843 (0.724): 589 |
| M1_206858 (0.725): 587 | M9_212391 (0.726): 575 | M1_205742 (0.727): 576 | M3_109713 (0.728): 576 |
| M3_120308 (0.728): 575 | M9_229883 (0.728): 576 | M1_133240 (0.728): 576 | M1_206545 (0.728): 577 |
| M5_205765 (0.729): 577 | M2_133501 (0.729): 576 | M6_233902 (0.729): 572 | M9_227630 (0.730): 575 |
| M5_128311 (0.730): 578 | M5_238580 (0.730): 577 | M13_243871 (0.733): 577 | M6_237437 (0.734): 578 |
| M5_236682 (0.734): 579 | M4_107643 (0.734): 574 | M13_246149 (0.735): 578 | M14_37219 (0.735): 578 |
| M14_37023 (0.735): 580 | M13_244239 (0.738): 579 | M6_240899 (0.739): 580 | M5_205715 (0.747): 581 |
| M12_92132 (0.748): 583 | M7_122025 (0.748): 578 | M11_215585 (0.749): 585 | M2_134021 (0.749): 585 |
| M1_139423 (0.749): 581 | M1_126578 (0.750): failed | M13_245763 (0.754): failed | M9_232890 (0.766): 592 |
| M10_227516 (0.779): 596 | M7_162587 (0.787): 597 | M7_152125 (0.787): 577 | M4_123161 (0.799): 683 |
| M10_201233 (0.818): 637 | M15_77745 (0.826): 615 | M8_156118 (0.830): 632 | M15_87207 (0.833): 656 |
| M2_130005 (0.834): 667 | M15_89072 (0.837): 677 | M13_253688 (0.837): 681 | M4_84337 (0.839): 660 |
| M15_88032 (0.839): 704 | M4_107370 (0.844): 736 | M7_147270 (0.847): 733 | M12_101089 (0.851): 736 |
| M6_166634 (0.853): 742 | M6_237641 (0.858): 745 | M13_255047 (0.864): 742 | M11_212718 (0.890): 513 |
| M11_217564 (0.890): 758 | M9_213587 (0.890): 733 | M11_214430 (0.891): 759 | M8_161113 (0.891): 748 |
| M5_167056 (0.893): 738 | M10_217020 (0.893): 755 | M10_216730 (0.894): 754 | M13_258753 (0.910): 750 |
| M12_185631 (0.925): 758 | M10_189698 (0.926): failed | M7_120488 (0.933): 762 | M7_121482 (0.936): 768 |
| M7_120758 (0.937): 605 | M5_127946 (0.939): failed | M14_102968 (0.939): 768 | M7_120372 (0.942): 755 |
| M2_97310 (0.943): failed | M14_104877 (0.954): 772 | M12_181421 (0.958): 609 | M14_38646 (0.969): 785 |
| M14_37843 (0.969): 780 | M4_112534 (0.984): 775 | M12_101830 (0.987): 782 |  |

## Conversion to H

- Relation: H(z) = −1/(1+z) · dz/dt. Jimenez & Loeb 2002, ApJ 573, 37, eq. 2 (arXiv:astro-ph/0106145).
- Assumption (same paper, §1 and §3): the galaxies are passively evolving and formed at the same time. Both samples have been passively evolving for a time much longer than the age difference between the two redshifts. The paper compares the upper cut-off of the age distributions at the two redshifts.
- Here dt/dz is the fitted age slope, so H = −977.79 / ((1+z_med) · slope) km/s/Mpc (977.79 km/s/Mpc = 1/Gyr, astropy). A slope ≥ 0 gives no H.
- Planck18 H at z = 0.728: 102.5 km/s/Mpc. The Planck18 tangent d t_univ/dz gives the same value. The straight line through t_univ at the 135 redshifts gives 109.4 km/s/Mpc.

## What the sample can and cannot constrain

- Redshift range 0.603–0.987, median 0.728. Mg b group median z 0.682, no-Mg b group 0.822.
- The fitted age slope of all galaxies changes with the fit setup from +1.18 Gyr/z ((c)) to -3.77 Gyr/z ((e), 130 galaxies). Its bootstrap 16–84 half-width is 0.65–0.78 Gyr/z.
- The Planck18 line over the same redshifts is -5.17 Gyr/z. No arm's 16–84 interval for all galaxies reaches it.
- The galaxy-to-galaxy scatter about the line is 0.80–1.04 Gyr.
- With C and N free, the Mg b group sits below the no-Mg b group at fixed z: offset -0.86 Gyr in (b) and -0.85 Gyr in (c); step -0.99 and -0.99 Gyr. The step 16–84 interval includes zero in (a), (d).
- The bootstrap 16–84 half-width of the step is 0.18–0.22 Gyr. That is the precision of the Mg b-coverage age step in each setup.
- It does not constrain H(z). The slope changes with the setup by more than its bootstrap width, and it is positive in (b) and (c). Where it is negative, the central H is 150–1359 km/s/Mpc across arms; Planck18 gives 102.5.
- The test here fits a line to the posterior median mass-weighted ages of all galaxies. It does not use the upper cut-off of the age distribution, and it does not test the same-formation-time assumption.

## Files

- `analysis.ipynb`: all tables above. Run with `ceridwen/.venv/bin/python` and `PYTHONPATH=external/sedpy_jax`.
- `per-fit.csv`, `validation.csv`, `age-redshift-slopes.csv`, `paired-age-differences.csv`, `paired-age-differences-per-galaxy.csv`, `mgb-cut-paired.csv`, `mgb-cut-paired-per-galaxy.csv`, `common-range-pixels.csv`, `pin-check.csv`.
- `<arm>/experiment.json`, `<arm>/run-driver.log`, `<arm>/run/manifest.json`, `<arm>/run/fits/<arm>/<object>-<target>/`.
- `recover.py`: notebook restore after the failed local rebuild (see Failed validations).

## Noticed, not done

- `scripts/plot_prior_kl.py` `label()` has no entry for `cfe` or `nfe`. The local figure rebuild of `scripts/experiment.py` then stops with `KeyError: 'cfe'` and writes the failed notebook over the GPU notebook, so `validate_result` fails. No standard figures were rebuilt for (b), (c), (e), (f), (j).
- `EmissionLineColumns` (`ceridwen/ceridwen/likelihood/emission_lines.py:374`) raises when no emission line has fitted pixels (5 fits of (e), the same 5 of (h)).
- `scripts/ceridwen_state.py` stops on a missing worktree.
- `cn-afe0p25-common/run/.modal/0/*.tar.gz` and `baseline-common/run/.modal/0/*.tar.gz` (557 MB and 505 MB of retrieval archives, left by the two runs with failed fits) are left in place and not committed.

## Rest-frame windows: arms (h), (i), (j)

overseer-astronomy follow-up, under Liu Hao, 2026-11-10: "you can research and run experiments overnight, i'll sleep soon". Arm (e) is the only arm in which every galaxy is fitted on the same rest-frame pixels. These arms separate the window from the other settings and test a wider window.

### Candidate common windows

The widest rest window (vacuum Å) that lies inside the October fitted rest range of each of N galaxies. Edges are rounded inward to 0.1 Å. Features: catalogue entries of `ceridwen/observation/absorption_features.py` (Lick bandpass, or line centre ±1000 km/s) that lie wholly inside the window. Forecast slope σ = 0.8 Gyr / (rms z · √N).

| required N | galaxies | window (Å) | width (Å) | features inside | z range | rms z | forecast σ (Gyr/z) | Mg b group |
|---|---|---|---|---|---|---|---|---|
| 135 | 135 | 4155.0–4206.6 | 51.6 | – | 0.603–0.987 | 0.101 | 0.68 | 61 |
| 129 | 129 | 4155.0–4438.1 | 283.1 | HgA Ca4227 G4300 Fe4383 | 0.603–0.987 | 0.096 | 0.74 | 61 |
| 120 | 120 | 4131.3–4573.8 | 442.5 | HgA Ca4227 Ca4455 CN4150 G4300 Fe4383 Fe4531 | 0.603–0.987 | 0.085 | 0.86 | 60 |
| 110 | 110 | 4074.5–4666.1 | 591.6 | HdA HgA Ca4227 Ca4455 CN4150 G4300 Fe4383 Fe4531 | 0.603–0.984 | 0.076 | 1.00 | 56 |
| 100 | 100 | 4103.4–4892.4 | 789.0 | HgA Hbeta Ca4227 Ca4455 CN4150 G4300 C4668 Fe4383 Fe4531 | 0.603–0.894 | 0.066 | 1.21 | 59 |
| 90 | 90 | 4033.4–4947.4 | 914.0 | HdA HgA Hbeta Ca4227 Ca4455 CN4150 G4300 C4668 Fe4383 Fe4531 | 0.603–0.894 | 0.064 | 1.32 | 53 |
| 80 | 80 | 4028.9–5014.7 | 985.8 | HdA HgA Hbeta Ca4227 Ca4455 CN4150 G4300 C4668 Fe4383 Fe4531 | 0.603–0.894 | 0.062 | 1.45 | 52 |

Choice: 110 galaxies on 4074.5–4666.1 Å, the widest window with forecast σ ≤ 1.2 Gyr/z (1.00; the next, 100 galaxies, gives 1.21).

### Arms

| arm | settings | galaxies | Modal cost estimate |
|---|---|---|---|
| (h) | `rest_range` [4155.0, 4438.1] (plain grid, [α/Fe] free) | 135 | $8.94 |
| (i) | `rest_range` [4074.5, 4666.1] (plain grid, [α/Fe] free) | 110 | $8.89 |
| (j) | as (i), `abundance_response` alf C/N | 110 | $13.23 |

- Seed 20260832, revision 99c179ba / Ceridwen 13791e0e, Modal A100-40GB. Billed cost after credits $0.00 before launch.
- Standard figures: rebuilt locally for (i). None for (h): the driver rebuilds only when every fit passes. None for (j): the driver was stopped at the rebuild (`KeyError: 'cfe'`, see "Noticed, not done"); its GPU notebooks and derived outputs are unchanged and all 110 validate.
- Samples: "own valid" is each new arm on its own valid fits. "w110" is the 108 galaxies of the window sample that are valid in (a), (b), (e), (h), (i) and (j).

### Failed validations

| arm | fits | valid | failed |
|---|---|---|---|
| (h) | 135 | 130 | 5 |
| (i) | 110 | 110 | 0 |
| (j) | 110 | 110 | 0 |

- (h): M1_126578 (z 0.750), M13_245763 (z 0.754), M10_189698 (z 0.926), M5_127946 (z 0.939), M2_97310 (z 0.943): `ValueError: attempt to get argmax of an empty sequence`
- (h) fails on the same galaxies as (e), with the same error (first "Failed validations" section). Not rerun.

### Age–redshift slope

#### New arms, own valid fits

| arm | group | N | z med | slope (Gyr/z) | bootstrap 16–84 | scatter (Gyr) | d t_univ/dz, line | H (km/s/Mpc) | H from 16–84 |
|---|---|---|---|---|---|---|---|---|---|
| (h) baseline, 4155.0–4438.1 Å | all | 130 | 0.728 | -3.26 | -3.91 to -2.62 | 0.81 | -5.19 | 174 | 145–216 |
| (i) baseline, 4074.5–4666.1 Å | all | 110 | 0.725 | -4.60 | -5.56 to -3.60 | 0.91 | -5.31 | 123 | 102–158 |
| (j) C/N free, 4074.5–4666.1 Å | all | 110 | 0.725 | -5.37 | -6.29 to -4.41 | 0.86 | -5.31 | 106 | 90–129 |
| (h) baseline, 4155.0–4438.1 Å | Mg b group (October coverage) | 60 | 0.681 | -3.43 | -5.84 to -0.93 | 0.85 | -5.82 | 170 | 99–627 |
| (i) baseline, 4074.5–4666.1 Å | Mg b group (October coverage) | 56 | 0.683 | -6.18 | -8.66 to -3.79 | 0.89 | -5.79 | 94 | 67–153 |
| (j) C/N free, 4074.5–4666.1 Å | Mg b group (October coverage) | 56 | 0.683 | -7.26 | -9.40 to -5.19 | 0.85 | -5.79 | 80 | 62–112 |
| (h) baseline, 4155.0–4438.1 Å | no-Mg b group | 70 | 0.809 | -3.98 | -4.96 to -3.04 | 0.77 | -4.98 | 136 | 109–178 |
| (i) baseline, 4074.5–4666.1 Å | no-Mg b group | 54 | 0.747 | -5.10 | -6.75 to -3.46 | 0.94 | -5.08 | 110 | 83–162 |
| (j) C/N free, 4074.5–4666.1 Å | no-Mg b group | 54 | 0.747 | -5.20 | -6.74 to -3.59 | 0.89 | -5.08 | 108 | 83–156 |

#### Same 108 galaxies (w110)

| arm | group | N | z med | slope (Gyr/z) | bootstrap 16–84 | scatter (Gyr) | d t_univ/dz, line | H (km/s/Mpc) | H from 16–84 |
|---|---|---|---|---|---|---|---|---|---|
| (a) baseline | all | 108 | 0.714 | -2.09 | -3.13 to -0.99 | 0.82 | -5.31 | 273 | 182–574 |
| (b) C/N free | all | 108 | 0.714 | -0.31 | -1.42 to +0.92 | 1.01 | -5.31 | 1818 | 402–∞ |
| (e) as (c), 4155.0–4438.1 Å | all | 108 | 0.714 | -4.66 | -5.61 to -3.68 | 0.80 | -5.31 | 122 | 102–155 |
| (h) baseline, 4155.0–4438.1 Å | all | 108 | 0.714 | -3.90 | -4.87 to -2.90 | 0.82 | -5.31 | 146 | 117–197 |
| (i) baseline, 4074.5–4666.1 Å | all | 108 | 0.714 | -4.62 | -5.61 to -3.61 | 0.92 | -5.31 | 123 | 102–158 |
| (j) C/N free, 4074.5–4666.1 Å | all | 108 | 0.714 | -5.39 | -6.30 to -4.42 | 0.87 | -5.31 | 106 | 90–129 |
| (a) baseline | Mg b group (October coverage) | 55 | 0.682 | -3.17 | -5.35 to -0.98 | 0.79 | -5.79 | 183 | 109–594 |
| (b) C/N free | Mg b group (October coverage) | 55 | 0.682 | -5.10 | -7.37 to -2.46 | 0.95 | -5.79 | 114 | 79–236 |
| (e) as (c), 4155.0–4438.1 Å | Mg b group (October coverage) | 55 | 0.682 | -6.86 | -8.79 to -5.07 | 0.78 | -5.79 | 85 | 66–115 |
| (h) baseline, 4155.0–4438.1 Å | Mg b group (October coverage) | 55 | 0.682 | -5.15 | -7.07 to -3.23 | 0.78 | -5.79 | 113 | 82–180 |
| (i) baseline, 4074.5–4666.1 Å | Mg b group (October coverage) | 55 | 0.682 | -6.37 | -8.95 to -3.91 | 0.90 | -5.79 | 91 | 65–149 |
| (j) C/N free, 4074.5–4666.1 Å | Mg b group (October coverage) | 55 | 0.682 | -7.63 | -9.88 to -5.50 | 0.85 | -5.79 | 76 | 59–106 |
| (a) baseline | no-Mg b group | 53 | 0.747 | -2.15 | -3.65 to -0.59 | 0.87 | -5.09 | 261 | 153–945 |
| (b) C/N free | no-Mg b group | 53 | 0.747 | -4.10 | -5.58 to -2.60 | 0.88 | -5.09 | 137 | 100–215 |
| (e) as (c), 4155.0–4438.1 Å | no-Mg b group | 53 | 0.747 | -5.10 | -6.73 to -3.57 | 0.82 | -5.09 | 110 | 83–157 |
| (h) baseline, 4155.0–4438.1 Å | no-Mg b group | 53 | 0.747 | -4.59 | -6.27 to -3.07 | 0.86 | -5.09 | 122 | 89–183 |
| (i) baseline, 4074.5–4666.1 Å | no-Mg b group | 53 | 0.747 | -5.08 | -6.74 to -3.50 | 0.95 | -5.09 | 110 | 83–160 |
| (j) C/N free, 4074.5–4666.1 Å | no-Mg b group | 53 | 0.747 | -5.19 | -6.75 to -3.62 | 0.90 | -5.09 | 108 | 83–155 |

### ρ([α/Fe], z) and medians

| arm | sample | group | N | ρ([α/Fe], z) | median [α/Fe] | median age (Gyr) | median [Fe/H] | median [C/Fe] | median [N/Fe] |
|---|---|---|---|---|---|---|---|---|---|
| (h) baseline, 4155.0–4438.1 Å | own valid | all | 130 | -0.27 (p 0.002) | +0.25 | 4.77 | -0.39 | – | – |
| (h) baseline, 4155.0–4438.1 Å | own valid | Mg b group (October coverage) | 60 | -0.22 (p 0.085) | +0.28 | 4.83 | -0.39 | – | – |
| (h) baseline, 4155.0–4438.1 Å | own valid | no-Mg b group | 70 | -0.26 (p 0.032) | +0.23 | 4.68 | -0.42 | – | – |
| (i) baseline, 4074.5–4666.1 Å | own valid | all | 110 | -0.11 (p 0.239) | +0.21 | 5.00 | -0.50 | – | – |
| (i) baseline, 4074.5–4666.1 Å | own valid | Mg b group (October coverage) | 56 | -0.18 (p 0.191) | +0.22 | 5.02 | -0.47 | – | – |
| (i) baseline, 4074.5–4666.1 Å | own valid | no-Mg b group | 54 | -0.03 (p 0.827) | +0.20 | 4.91 | -0.53 | – | – |
| (j) C/N free, 4074.5–4666.1 Å | own valid | all | 110 | -0.04 (p 0.684) | +0.14 | 5.10 | -0.50 | -0.13 | +0.23 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | Mg b group (October coverage) | 56 | -0.16 (p 0.242) | +0.14 | 5.29 | -0.48 | -0.14 | +0.18 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | no-Mg b group | 54 | +0.01 (p 0.915) | +0.14 | 5.01 | -0.52 | -0.12 | +0.30 |
| (a) baseline | w110 | all | 108 | -0.42 (p 0.000) | +0.01 | 4.01 | -0.25 | – | – |
| (a) baseline | w110 | Mg b group (October coverage) | 55 | -0.30 (p 0.027) | +0.09 | 4.21 | -0.24 | – | – |
| (a) baseline | w110 | no-Mg b group | 53 | -0.14 (p 0.333) | -0.15 | 3.82 | -0.29 | – | – |
| (b) C/N free | w110 | all | 108 | -0.45 (p 0.000) | +0.07 | 4.29 | -0.39 | -0.02 | +0.25 |
| (b) C/N free | w110 | Mg b group (October coverage) | 55 | -0.22 (p 0.113) | +0.21 | 3.73 | -0.29 | +0.09 | +0.14 |
| (b) C/N free | w110 | no-Mg b group | 53 | -0.00 (p 0.989) | -0.14 | 4.64 | -0.43 | -0.16 | +0.33 |
| (e) as (c), 4155.0–4438.1 Å | w110 | all | 108 | fixed | +0.25 | 5.04 | -0.44 | -0.06 | +0.34 |
| (e) as (c), 4155.0–4438.1 Å | w110 | Mg b group (October coverage) | 55 | fixed | +0.25 | 4.98 | -0.44 | -0.08 | +0.33 |
| (e) as (c), 4155.0–4438.1 Å | w110 | no-Mg b group | 53 | fixed | +0.25 | 5.06 | -0.44 | -0.04 | +0.36 |
| (h) baseline, 4155.0–4438.1 Å | w110 | all | 108 | -0.21 (p 0.032) | +0.26 | 4.82 | -0.39 | – | – |
| (h) baseline, 4155.0–4438.1 Å | w110 | Mg b group (October coverage) | 55 | -0.25 (p 0.069) | +0.28 | 4.82 | -0.39 | – | – |
| (h) baseline, 4155.0–4438.1 Å | w110 | no-Mg b group | 53 | -0.08 (p 0.569) | +0.24 | 4.82 | -0.42 | – | – |
| (i) baseline, 4074.5–4666.1 Å | w110 | all | 108 | -0.09 (p 0.367) | +0.21 | 5.00 | -0.50 | – | – |
| (i) baseline, 4074.5–4666.1 Å | w110 | Mg b group (October coverage) | 55 | -0.14 (p 0.324) | +0.22 | 5.04 | -0.47 | – | – |
| (i) baseline, 4074.5–4666.1 Å | w110 | no-Mg b group | 53 | -0.02 (p 0.884) | +0.20 | 4.91 | -0.53 | – | – |
| (j) C/N free, 4074.5–4666.1 Å | w110 | all | 108 | -0.02 (p 0.857) | +0.15 | 5.10 | -0.50 | -0.13 | +0.23 |
| (j) C/N free, 4074.5–4666.1 Å | w110 | Mg b group (October coverage) | 55 | -0.12 (p 0.378) | +0.15 | 5.24 | -0.49 | -0.14 | +0.17 |
| (j) C/N free, 4074.5–4666.1 Å | w110 | no-Mg b group | 53 | +0.02 (p 0.897) | +0.14 | 4.99 | -0.51 | -0.13 | +0.31 |

### Mg b offset and step model

Mg b group by October coverage. (e), (h), (i) and (j) fit no Mg b pixels; (a) and (b) fit them in the Mg b group.

| arm | sample | N | Mg b offset (Gyr) | joint slope (Gyr/z) | step (Gyr) | H from joint slope |
|---|---|---|---|---|---|---|
| (h) baseline, 4155.0–4438.1 Å | own valid | 130 | -0.15 (-0.22 to -0.02) | -3.89 (-4.79 to -3.00) | -0.19 (-0.39 to +0.00) | 146 |
| (i) baseline, 4074.5–4666.1 Å | own valid | 110 | -0.25 (-0.39 to -0.06) | -5.38 (-6.71 to -4.03) | -0.21 (-0.44 to +0.02) | 105 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | 110 | -0.03 (-0.24 to +0.16) | -5.73 (-6.98 to -4.46) | -0.10 (-0.31 to +0.11) | 99 |
| (a) baseline | w110 | 108 | +0.23 (+0.06 to +0.43) | -2.40 (-3.64 to -1.13) | -0.08 (-0.26 to +0.10) | 237 |
| (b) C/N free | w110 | 108 | -0.94 (-1.04 to -0.64) | -4.35 (-5.61 to -3.06) | -1.08 (-1.28 to -0.87) | 131 |
| (e) as (c), 4155.0–4438.1 Å | w110 | 108 | -0.19 (-0.38 to -0.12) | -5.55 (-6.85 to -4.26) | -0.24 (-0.44 to -0.04) | 103 |
| (h) baseline, 4155.0–4438.1 Å | w110 | 108 | -0.19 (-0.31 to -0.08) | -4.73 (-6.03 to -3.45) | -0.22 (-0.42 to -0.03) | 120 |
| (i) baseline, 4074.5–4666.1 Å | w110 | 108 | -0.26 (-0.40 to -0.05) | -5.41 (-6.77 to -4.04) | -0.21 (-0.45 to +0.02) | 106 |
| (j) C/N free, 4074.5–4666.1 Å | w110 | 108 | -0.05 (-0.26 to +0.14) | -5.80 (-7.07 to -4.49) | -0.11 (-0.34 to +0.11) | 98 |

### Paired age differences against z

| pair | group | N | median Δage (Gyr) | Δage 16–84 | fraction older | dΔage/dz (Gyr/z) | ρ(Δage, z) |
|---|---|---|---|---|---|---|---|
| (h) − (a) | all | 130 | +0.56 | -0.24 to +1.41 | 0.72 | -1.92 (-2.53 to -1.31) | -0.21 (p 0.015) |
| (h) − (a) | Mg b group (October coverage) | 60 | +0.59 | -0.11 to +1.26 | 0.78 | -0.19 (-1.96 to +1.70) | -0.04 (p 0.790) |
| (h) − (a) | no-Mg b group | 70 | +0.52 | -0.35 to +1.42 | 0.67 | -3.05 (-4.12 to -2.03) | -0.38 (p 0.001) |
| (e) − (h) | all | 130 | +0.16 | -0.05 to +0.40 | 0.78 | -0.51 (-0.72 to -0.28) | -0.21 (p 0.014) |
| (e) − (h) | Mg b group (October coverage) | 60 | +0.16 | -0.04 to +0.50 | 0.82 | -1.25 (-1.87 to -0.68) | -0.26 (p 0.042) |
| (e) − (h) | no-Mg b group | 70 | +0.16 | -0.08 to +0.38 | 0.76 | -0.44 (-0.71 to -0.17) | -0.17 (p 0.167) |
| (i) − (a) | all | 110 | +0.84 | -0.01 to +1.54 | 0.83 | -2.59 (-3.52 to -1.69) | -0.22 (p 0.022) |
| (i) − (a) | Mg b group (October coverage) | 56 | +0.90 | +0.14 to +1.55 | 0.89 | -3.55 (-5.23 to -2.00) | -0.24 (p 0.071) |
| (i) − (a) | no-Mg b group | 54 | +0.84 | -0.28 to +1.50 | 0.76 | -2.88 (-4.47 to -1.36) | -0.26 (p 0.058) |
| (j) − (b) | all | 110 | +0.67 | -0.33 to +1.64 | 0.77 | -5.15 (-6.18 to -4.21) | -0.45 (p 0.000) |
| (j) − (b) | Mg b group (October coverage) | 56 | +1.15 | +0.61 to +2.21 | 0.93 | -3.06 (-6.12 to -0.47) | -0.22 (p 0.102) |
| (j) − (b) | no-Mg b group | 54 | +0.17 | -0.53 to +0.82 | 0.61 | -1.04 (-2.26 to +0.26) | -0.16 (p 0.255) |
| (j) − (i) | all | 110 | +0.16 | -0.07 to +0.45 | 0.70 | -0.77 (-1.07 to -0.45) | -0.23 (p 0.017) |
| (j) − (i) | Mg b group (October coverage) | 56 | +0.25 | -0.00 to +0.51 | 0.80 | -1.08 (-1.73 to -0.37) | -0.20 (p 0.139) |
| (j) − (i) | no-Mg b group | 54 | +0.09 | -0.16 to +0.34 | 0.59 | -0.10 (-0.53 to +0.41) | +0.01 (p 0.967) |
| (i) − (h) | all | 108 | +0.22 | -0.25 to +0.63 | 0.65 | -0.72 (-1.21 to -0.23) | -0.16 (p 0.102) |
| (i) − (h) | Mg b group (October coverage) | 55 | +0.26 | -0.20 to +0.57 | 0.75 | -1.22 (-2.47 to -0.12) | -0.17 (p 0.203) |
| (i) − (h) | no-Mg b group | 53 | +0.06 | -0.29 to +0.68 | 0.55 | -0.49 (-1.20 to +0.33) | -0.08 (p 0.572) |

### Posterior age width and the prior

- Width: posterior 84th minus 16th percentile of the mass-weighted age, per galaxy. Ratio: window arm over arm (a), same galaxy; median and 16–84 of the ratios.
- Prior: production SFH prior median and 16–84 mass-weighted age at each galaxy's redshift, from `results/cn-response-2026-11-10/prior-slope/prior-per-galaxy.csv` (experiment 9). The prior median age decreases monotonically with z over these galaxies, so ρ(age, prior median age) = −ρ(age, z).
- Prior slope: straight-line slope of the prior median age on z over the same galaxies.

| arm | sample | N | width ratio to (a) | median width (Gyr) | posterior / prior width | ρ(age, prior median age) | prior slope (Gyr/z) |
|---|---|---|---|---|---|---|---|
| (a) baseline | own valid | 135 | 1.00 (1.00 to 1.00) | 0.75 | 0.20 | +0.17 (p 0.055) | -2.28 |
| (a) baseline | w110 | 108 | 1.00 (1.00 to 1.00) | 0.78 | 0.20 | +0.15 (p 0.116) | -2.34 |
| (e) as (c), 4155.0–4438.1 Å | own valid | 130 | 1.62 (1.20 to 2.18) | 1.17 | 0.31 | +0.48 (p 0.000) | -2.28 |
| (e) as (c), 4155.0–4438.1 Å | w110 | 108 | 1.58 (1.19 to 2.23) | 1.17 | 0.31 | +0.41 (p 0.000) | -2.34 |
| (h) baseline, 4155.0–4438.1 Å | own valid | 130 | 1.55 (1.20 to 2.13) | 1.15 | 0.31 | +0.45 (p 0.000) | -2.28 |
| (h) baseline, 4155.0–4438.1 Å | w110 | 108 | 1.52 (1.20 to 2.20) | 1.16 | 0.31 | +0.35 (p 0.000) | -2.34 |
| (i) baseline, 4074.5–4666.1 Å | own valid | 110 | 1.29 (0.98 to 1.78) | 0.97 | 0.26 | +0.33 (p 0.000) | -2.34 |
| (i) baseline, 4074.5–4666.1 Å | w110 | 108 | 1.29 (0.98 to 1.78) | 0.95 | 0.26 | +0.33 (p 0.000) | -2.34 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | 110 | 1.27 (1.02 to 1.77) | 0.98 | 0.26 | +0.39 (p 0.000) | -2.34 |
| (j) C/N free, 4074.5–4666.1 Å | w110 | 108 | 1.27 (1.02 to 1.77) | 0.98 | 0.26 | +0.39 (p 0.000) | -2.34 |

### Numbers in brief

- Same 108 galaxies, all-galaxy slope (Gyr/z): (a) -2.09, (b) -0.31, (e) -4.66, (h) -3.90, (i) -4.62, (j) -5.39. Planck18 line -5.31; prior median-age line -2.34.
- Same galaxies, joint slope with the Mg b step: (a) -2.40, (b) -4.35, (e) -5.55, (h) -4.73, (i) -5.41, (j) -5.80.
- Median age-width ratio to (a) on the same galaxies: (e) 1.58, (h) 1.52, (i) 1.29, (j) 1.27. ρ(age, prior median age): (a) +0.15, (e) +0.41, (h) +0.35, (i) +0.33, (j) +0.39.
- Posterior / prior age width on the same galaxies: (a) 0.20, (e) 0.31, (h) 0.31, (i) 0.26, (j) 0.26. The prior median age falls with z, so a true age–z trend also gives ρ(age, prior median age) > 0. The window-arm slopes (-3.90 to -5.39) are steeper than the prior median-age line (-2.34).

### Files

- `common-windows.csv`, `age-width-prior.csv`; new rows in `per-fit.csv`, `validation.csv`, `age-redshift-slopes.csv` (samples `own_valid`, `w110`), `paired-age-differences.csv`, `paired-age-differences-per-galaxy.csv`.
- `baseline-common/`, `baseline-w110/`, `cn-free-w110/`: `experiment.json`, `run-driver.log`, `run/`.

## Window extensions: arms (k), (l), (m)

overseer-astronomy follow-up, under Liu Hao, 2026-11-10: "you can research and run experiments overnight, i'll sleep soon". On the 108 galaxies of the window sample, (i) gives slope -4.62 Gyr/z, median [α/Fe] +0.22 / +0.20 (Mg b group / no-Mg b group) and ρ([α/Fe], z) -0.09. The full-range fits (a) of the same galaxies give -2.09, +0.09 / -0.15 and -0.42. These arms extend the (i) window blue or red, with baseline settings, on the window-sample galaxies that fully cover the extended window.

### Windows

| arm | window (Å) | galaxies | Mg b group | z range | features added | fitted pixels added, median | Modal cost estimate |
|---|---|---|---|---|---|---|---|
| (k) | 3742.9–4666.1 | 60 | 7 | 0.654–0.984 | H10, H9, H8, CaK, CaH | 730 | $5.19 |
| (l) | 4074.5–4893.0 | 96 | 56 | 0.603–0.894 | Hbeta, C4668 | 636 | $7.87 |
| (m) | 4074.5–5207.9 | 46 | 46 | 0.603–0.750 | Hbeta, C4668, Fe5015, Mgb | 1496 | $4.49 |

- Edges: Lick definitions of Trager et al. 1998, Table 2 (air), converted to vacuum with `ceridwen.observation.filters.air2vac`. R1 and R2 are rounded up to 0.1 Å. "Covers": the October fitted rest range contains the window.
- (k): B = 3742.9 Å, the bluest limit that at least 60 of the 110 cover (60th smallest October first fitted pixel, 3742.84 Å, rounded up to 0.1 Å).
- (l): R1 = 4893.0 Å, just above the Hβ red pseudo-continuum (4891.625 Å air = 4892.99 Å vacuum). It contains the C4668 and Hβ bandpasses and their pseudo-continua, and stops below the Fe5015 blue pseudo-continuum (4946.500 Å air = 4947.88 Å) and bandpass (4977.750 Å air = 4979.14 Å).
- (m): R2 = 5207.9 Å, just above the Mg b red pseudo-continuum (5206.375 Å air = 5207.82 Å vacuum).
- Features added: catalogue windows (Lick bandpass, or line centre ±1000 km/s) wholly inside the arm's window and not wholly inside 4074.5–4666.1 Å. C4668 crosses the (i) red edge.
- (k) and (l) fit zero Mg b bandpass pixels in every galaxy. (m) fits the Mg b bandpass in all 46 of its valid fits (median 90 pixels; median 175 in bandpass plus pseudo-continua).
- CaK and CaH have no fitted pixels: the production `emission_lines` setting masks ±1500 km/s around 3934.77 Å (Ca II K) and 3966.6 and 3973.3 Å (Ca II H), rest vacuum; this contains the catalogue windows, 3921.7–3947.9 Å and 3956.4–3982.8 Å.
- Seed 20260832, revision 99c179ba / Ceridwen 13791e0e, Modal A100-40GB, `rest_range` only. Billed cost after credits $0.00 before launch.

### Failed validations

| arm | fits | valid | failed |
|---|---|---|---|
| (k) | 60 | 60 | 0 |
| (l) | 96 | 96 | 0 |
| (m) | 46 | 46 | 0 |

- none

### Paired change against (i), same galaxies

Extension arm minus (i), posterior medians per galaxy; median and 16–84 across galaxies. dΔage/dz: straight-line slope with galaxy-bootstrap 16–84. (m): every galaxy is in the Mg b group, so only the "all" row is shown.

| arm | group | N | Δ[α/Fe] | Δage (Gyr) | Δ[Fe/H] | dΔage/dz (Gyr/z) | ρ(Δage, z) |
|---|---|---|---|---|---|---|---|
| (k) | all | 60 | -0.18 (-0.32 to -0.07) | +0.01 (-0.38 to +0.39) | +0.02 (-0.06 to +0.10) | +0.47 (-0.27 to +1.27) | +0.06 (p 0.624) |
| (k) | Mg b group (October coverage) | 7 | -0.19 (-0.24 to -0.16) | +0.24 (-0.23 to +0.51) | -0.04 (-0.06 to +0.04) | +19.00 (+12.99 to +24.60) | +0.75 (p 0.052) |
| (k) | no-Mg b group | 53 | -0.18 (-0.34 to -0.06) | +0.01 (-0.38 to +0.34) | +0.02 (-0.06 to +0.13) | +0.62 (-0.23 to +1.52) | +0.07 (p 0.594) |
| (l) | all | 96 | -0.12 (-0.26 to -0.04) | +0.01 (-0.34 to +0.33) | +0.01 (-0.07 to +0.09) | +0.28 (-0.34 to +0.90) | -0.01 (p 0.940) |
| (l) | Mg b group (October coverage) | 56 | -0.14 (-0.25 to -0.04) | -0.03 (-0.35 to +0.38) | +0.01 (-0.07 to +0.09) | -0.43 (-1.55 to +0.73) | -0.12 (p 0.380) |
| (l) | no-Mg b group | 40 | -0.11 (-0.28 to -0.04) | +0.06 (-0.32 to +0.27) | +0.02 (-0.07 to +0.09) | +0.55 (-0.27 to +1.38) | +0.11 (p 0.489) |
| (m) | all | 46 | -0.16 (-0.29 to -0.00) | -0.96 (-1.37 to -0.29) | +0.21 (+0.09 to +0.29) | +2.15 (+0.45 to +3.78) | +0.13 (p 0.377) |

### Age–redshift slope on each arm's galaxies

(a), (i) and the extension arm on the galaxies valid in all three. Same bootstrap draws for the three arms.

| galaxies | group | N | z med | arm | slope (Gyr/z) | bootstrap 16–84 | scatter (Gyr) | d t_univ/dz, line | H (km/s/Mpc) | ρ([α/Fe], z) | median [α/Fe] | median age (Gyr) | median [Fe/H] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (k) galaxies | all | 60 | 0.735 | (a) baseline | -1.47 | -2.90 to +0.02 | 0.88 | -5.13 | 382 | -0.27 (p 0.040) | -0.10 | 3.80 | -0.29 |
| (k) galaxies | all | 60 | 0.735 | (i) baseline, 4074.5–4666.1 Å | -4.59 | -5.92 to -3.23 | 0.91 | -5.13 | 123 | -0.09 (p 0.484) | +0.21 | 4.91 | -0.51 |
| (k) galaxies | all | 60 | 0.735 | (k) baseline, blue extension | -4.12 | -5.44 to -2.73 | 0.86 | -5.13 | 137 | -0.15 (p 0.263) | +0.01 | 4.88 | -0.47 |
| (k) galaxies | Mg b group (October coverage) | 7 | 0.678 | (a) baseline | +34.98 | +12.92 to +63.25 | 0.91 | -5.86 | – | -0.46 (p 0.294) | +0.05 | 3.57 | -0.18 |
| (k) galaxies | Mg b group (October coverage) | 7 | 0.678 | (i) baseline, 4074.5–4666.1 Å | -0.21 | -8.71 to +11.12 | 0.63 | -5.86 | 2830 | +0.57 (p 0.180) | +0.23 | 5.15 | -0.45 |
| (k) galaxies | Mg b group (October coverage) | 7 | 0.678 | (k) baseline, blue extension | +18.80 | +10.21 to +29.43 | 0.47 | -5.86 | – | +0.18 (p 0.702) | +0.06 | 5.00 | -0.48 |
| (k) galaxies | no-Mg b group | 53 | 0.747 | (a) baseline | -2.29 | -3.80 to -0.76 | 0.85 | -5.08 | 244 | -0.15 (p 0.282) | -0.15 | 3.82 | -0.29 |
| (k) galaxies | no-Mg b group | 53 | 0.747 | (i) baseline, 4074.5–4666.1 Å | -5.14 | -6.80 to -3.54 | 0.94 | -5.08 | 109 | -0.04 (p 0.753) | +0.20 | 4.91 | -0.53 |
| (k) galaxies | no-Mg b group | 53 | 0.747 | (k) baseline, blue extension | -4.52 | -6.07 to -2.95 | 0.89 | -5.08 | 124 | -0.09 (p 0.531) | -0.02 | 4.86 | -0.45 |
| (l) galaxies | all | 96 | 0.698 | (a) baseline | -2.39 | -3.95 to -0.67 | 0.86 | -5.46 | 241 | -0.35 (p 0.000) | +0.04 | 4.02 | -0.25 |
| (l) galaxies | all | 96 | 0.698 | (i) baseline, 4074.5–4666.1 Å | -4.87 | -6.25 to -3.35 | 0.96 | -5.46 | 118 | -0.02 (p 0.859) | +0.22 | 5.05 | -0.49 |
| (l) galaxies | all | 96 | 0.698 | (l) baseline, red to Hβ | -4.59 | -5.93 to -3.10 | 0.92 | -5.46 | 125 | -0.11 (p 0.292) | +0.10 | 5.03 | -0.50 |
| (l) galaxies | Mg b group (October coverage) | 56 | 0.683 | (a) baseline | -2.63 | -4.81 to -0.44 | 0.79 | -5.79 | 221 | -0.30 (p 0.027) | +0.09 | 4.22 | -0.24 |
| (l) galaxies | Mg b group (October coverage) | 56 | 0.683 | (i) baseline, 4074.5–4666.1 Å | -6.18 | -8.66 to -3.79 | 0.89 | -5.79 | 94 | -0.18 (p 0.191) | +0.22 | 5.02 | -0.47 |
| (l) galaxies | Mg b group (October coverage) | 56 | 0.683 | (l) baseline, red to Hβ | -6.61 | -8.60 to -4.71 | 0.82 | -5.79 | 88 | -0.16 (p 0.224) | +0.08 | 5.05 | -0.47 |
| (l) galaxies | no-Mg b group | 40 | 0.735 | (a) baseline | -2.66 | -5.13 to +0.11 | 0.96 | -5.24 | 212 | -0.14 (p 0.377) | -0.13 | 3.80 | -0.28 |
| (l) galaxies | no-Mg b group | 40 | 0.735 | (i) baseline, 4074.5–4666.1 Å | -5.62 | -8.25 to -2.89 | 1.06 | -5.24 | 100 | +0.16 (p 0.326) | +0.21 | 5.08 | -0.53 |
| (l) galaxies | no-Mg b group | 40 | 0.735 | (l) baseline, red to Hβ | -5.07 | -7.63 to -2.37 | 1.05 | -5.24 | 111 | -0.10 (p 0.532) | +0.11 | 5.03 | -0.51 |
| (m) galaxies | all | 46 | 0.682 | (a) baseline | -4.44 | -7.09 to -1.57 | 0.79 | -5.92 | 131 | -0.18 (p 0.225) | +0.10 | 4.23 | -0.24 |
| (m) galaxies | all | 46 | 0.682 | (i) baseline, 4074.5–4666.1 Å | -9.38 | -12.11 to -6.50 | 0.92 | -5.92 | 62 | -0.24 (p 0.115) | +0.22 | 5.00 | -0.46 |
| (m) galaxies | all | 46 | 0.682 | (m) baseline, red past Mg b | -7.23 | -9.91 to -4.43 | 0.84 | -5.92 | 80 | -0.27 (p 0.065) | +0.06 | 4.08 | -0.26 |

### Band pulls of the added features

Band pull: sum of the stored fitted pulls (observed − posterior median) / effective uncertainty over the fitted pixels in the feature window, divided by √(number of those pixels); negative: data below the model. The metric of `results/cn-response-2026-11-10` (residual stack). Median and 16–84 across galaxies; galaxies with no fitted pixel in the window are left out.

| arm | feature | fit | galaxies with fitted pixels | median band pull (16–84) | median fitted pixels |
|---|---|---|---|---|---|
| (k) | H10 | own fit | 60 | -0.40 (-1.68 to +0.43) | 73 |
| (k) | H9 | own fit | 60 | +0.80 (-0.30 to +2.02) | 74 |
| (k) | H8 | own fit | 60 | +0.70 (-0.57 to +1.88) | 75 |
| (k) | CaK | own fit | 0 | – | – |
| (k) | CaH | own fit | 0 | – | – |
| (k) | H10 | (a), same galaxies | 60 | -2.34 (-3.54 to -0.69) | 73 |
| (k) | H9 | (a), same galaxies | 60 | +0.31 (-0.94 to +1.38) | 74 |
| (k) | H8 | (a), same galaxies | 60 | +1.47 (+0.25 to +3.09) | 75 |
| (k) | CaK | (a), same galaxies | 0 | – | – |
| (k) | CaH | (a), same galaxies | 0 | – | – |
| (l) | Hbeta | own fit | 96 | +0.02 (-0.70 to +1.35) | 81 |
| (l) | C4668 | own fit | 96 | -2.58 (-3.76 to -0.79) | 244 |
| (l) | Hbeta | (a), same galaxies | 96 | +0.64 (-0.70 to +2.22) | 81 |
| (l) | C4668 | (a), same galaxies | 96 | -3.82 (-6.64 to -2.02) | 244 |
| (m) | Hbeta | own fit | 46 | +0.21 (-1.25 to +1.66) | 80 |
| (m) | C4668 | own fit | 46 | -4.72 (-7.32 to -2.68) | 240 |
| (m) | Fe5015 | own fit | 46 | -0.05 (-2.24 to +1.72) | 208 |
| (m) | Mgb | own fit | 46 | -2.20 (-3.75 to -0.85) | 90 |
| (m) | Hbeta | (a), same galaxies | 46 | +0.90 (-0.55 to +2.47) | 80 |
| (m) | C4668 | (a), same galaxies | 46 | -5.39 (-8.11 to -3.37) | 240 |
| (m) | Fe5015 | (a), same galaxies | 46 | -0.65 (-3.21 to +1.41) | 208 |
| (m) | Mgb | (a), same galaxies | 46 | -3.80 (-5.66 to -1.61) | 90 |

### Window ladder

Each arm on its own valid fits.

| arm | window (Å) | N | median [α/Fe] | slope (Gyr/z) | bootstrap 16–84 | d t_univ/dz, line |
|---|---|---|---|---|---|---|
| (a) baseline | October fitted range | 135 | -0.03 | -1.55 | -2.23 to -0.88 | -5.17 |
| (h) baseline, 4155.0–4438.1 Å | 4155.0–4438.1 | 130 | +0.25 | -3.26 | -3.91 to -2.62 | -5.19 |
| (i) baseline, 4074.5–4666.1 Å | 4074.5–4666.1 | 110 | +0.21 | -4.60 | -5.56 to -3.60 | -5.31 |
| (k) baseline, blue extension | 3742.9–4666.1 | 60 | +0.01 | -4.12 | -5.44 to -2.73 | -5.13 |
| (l) baseline, red to Hβ | 4074.5–4893.0 | 96 | +0.10 | -4.59 | -5.93 to -3.10 | -5.46 |
| (m) baseline, red past Mg b | 4074.5–5207.9 | 46 | +0.06 | -7.23 | -9.91 to -4.43 | -5.92 |

### Numbers in brief

- (k) (3742.9–4666.1 Å, 60 galaxies): Δ[α/Fe] -0.18, Δage +0.01 Gyr against (i). Slope -4.12; (i) -4.59, (a) -1.47, Planck18 line -5.13. ρ([α/Fe], z) -0.15; (i) -0.09, (a) -0.27.
- (l) (4074.5–4893.0 Å, 96 galaxies): Δ[α/Fe] -0.12, Δage +0.01 Gyr against (i). Slope -4.59; (i) -4.87, (a) -2.39, Planck18 line -5.46. ρ([α/Fe], z) -0.11; (i) -0.02, (a) -0.35.
- (m) (4074.5–5207.9 Å, 46 galaxies): Δ[α/Fe] -0.16, Δage -0.96 Gyr against (i). Slope -7.23; (i) -9.38, (a) -4.44, Planck18 line -5.92. ρ([α/Fe], z) -0.27; (i) -0.24, (a) -0.18.
- Slope minus the (i) slope, same galaxies: (k) +0.47, (l) +0.28, (m) +2.15 Gyr/z; (a) minus (i): +3.12 on the (k) galaxies, +2.48 on the (l) galaxies, +4.95 on the (m) galaxies.

### Files

- `window-extension-paired.csv`, `window-extension-paired-per-galaxy.csv`, `window-extension-band-pulls.csv`, `window-extension-band-pulls-per-galaxy.csv`, `window-ladder.csv`; new rows in `per-fit.csv`, `validation.csv`, `age-redshift-slopes.csv` (samples `own_valid` and `<arm>_galaxies`).
- `baseline-blue/`, `baseline-red-hb/`, `baseline-red-mgb/`: `experiment.json`, `run-driver.log`, `run/`.
