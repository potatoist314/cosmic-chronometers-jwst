# Chronometer test on the 135 LEGA-C DR2 quiescent galaxies

Liu Hao, 2026-11-10 23:55: "sure, run all of them, i'm most interested in the effects of C and N and the result on the chronometer test, but do all of them"

Arms (a)–(e) are from the overseer-astronomy brief; (f) and (g) are from its answer to the checkpoint.

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
- Mg b group: the October fit has fitted pixels in the Mg b bandpass (`feature_windows(['Mgb'])`). 61 galaxies with, 74 without. These are the same 61 galaxies as the carbon-mask reuse.
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
| (a) baseline | with Mg b | 61 | 0.682 | -2.77 | -5.07 to -0.45 | 0.86 | -5.82 | 210 | 115–1306 |
| (b) C/N free | with Mg b | 61 | 0.682 | -2.76 | -5.35 to +0.26 | 1.00 | -5.82 | 211 | 109–∞ |
| (c) C/N free, [α/Fe] = +0.25 | with Mg b | 61 | 0.682 | -3.40 | -6.07 to -0.25 | 1.02 | -5.82 | 171 | 96–2335 |
| (d) carbon mask | with Mg b | 61 | 0.682 | -4.76 | -7.22 to -2.35 | 0.89 | -5.82 | 122 | 80–248 |
| (e) as (c), 4155.0–4438.1 Å | with Mg b | 60 | 0.681 | -4.68 | -7.30 to -2.15 | 0.86 | -5.82 | 124 | 80–270 |
| (f) as (b), Mg b cut | with Mg b | 61 | 0.682 | -7.13 | -9.29 to -4.75 | 0.92 | -5.82 | 81 | 63–122 |
| (g) baseline, Mg b cut | with Mg b | 61 | 0.682 | -3.45 | -5.92 to -1.20 | 0.84 | -5.82 | 168 | 98–486 |
| (a) baseline | without Mg b | 74 | 0.822 | -1.35 | -2.28 to -0.47 | 0.79 | -4.97 | 396 | 236–1130 |
| (b) C/N free | without Mg b | 74 | 0.822 | -2.07 | -3.06 to -1.14 | 0.86 | -4.97 | 260 | 175–469 |
| (c) C/N free, [α/Fe] = +0.25 | without Mg b | 74 | 0.822 | -1.72 | -2.76 to -0.73 | 0.93 | -4.97 | 312 | 194–731 |
| (d) carbon mask | without Mg b | 74 | 0.822 | -2.70 | -3.66 to -1.79 | 0.78 | -4.97 | 198 | 147–300 |
| (e) as (c), 4155.0–4438.1 Å | without Mg b | 70 | 0.809 | -4.42 | -5.41 to -3.42 | 0.75 | -4.98 | 122 | 100–158 |
| (f) as (b), Mg b cut | without Mg b | 74 | 0.822 | -2.07 | -3.06 to -1.14 | 0.86 | -4.97 | 260 | 175–469 |
| (g) baseline, Mg b cut | without Mg b | 74 | 0.822 | -1.35 | -2.28 to -0.47 | 0.79 | -4.97 | 396 | 236–1130 |

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
| (a) baseline | with Mg b | 60 | 0.681 | -3.24 | -5.64 to -0.94 | 0.86 | -5.82 | 180 | 103–621 |
| (b) C/N free | with Mg b | 60 | 0.681 | -3.54 | -6.11 to -0.73 | 0.99 | -5.82 | 164 | 95–794 |
| (c) C/N free, [α/Fe] = +0.25 | with Mg b | 60 | 0.681 | -4.18 | -6.83 to -1.24 | 1.02 | -5.82 | 139 | 85–467 |
| (d) carbon mask | with Mg b | 60 | 0.681 | -5.26 | -7.87 to -2.91 | 0.89 | -5.82 | 111 | 74–200 |
| (e) as (c), 4155.0–4438.1 Å | with Mg b | 60 | 0.681 | -4.68 | -7.30 to -2.15 | 0.86 | -5.82 | 124 | 80–270 |
| (f) as (b), Mg b cut | with Mg b | 60 | 0.681 | -7.89 | -10.01 to -5.72 | 0.91 | -5.82 | 74 | 58–102 |
| (g) baseline, Mg b cut | with Mg b | 60 | 0.681 | -4.06 | -6.66 to -1.79 | 0.83 | -5.82 | 143 | 87–325 |
| (a) baseline | without Mg b | 70 | 0.809 | -0.92 | -1.90 to -0.01 | 0.79 | -4.98 | 585 | 285–48958 |
| (b) C/N free | without Mg b | 70 | 0.809 | -1.50 | -2.51 to -0.55 | 0.86 | -4.98 | 360 | 215–987 |
| (c) C/N free, [α/Fe] = +0.25 | without Mg b | 70 | 0.809 | -1.14 | -2.21 to -0.12 | 0.93 | -4.98 | 473 | 245–4366 |
| (d) carbon mask | without Mg b | 70 | 0.809 | -2.18 | -3.16 to -1.25 | 0.77 | -4.98 | 248 | 171–432 |
| (e) as (c), 4155.0–4438.1 Å | without Mg b | 70 | 0.809 | -4.42 | -5.41 to -3.42 | 0.75 | -4.98 | 122 | 100–158 |
| (f) as (b), Mg b cut | without Mg b | 70 | 0.809 | -1.50 | -2.51 to -0.55 | 0.86 | -4.98 | 360 | 215–987 |
| (g) baseline, Mg b cut | without Mg b | 70 | 0.809 | -0.92 | -1.90 to -0.01 | 0.79 | -4.98 | 585 | 285–48958 |

## ρ([α/Fe], z) and medians

Spearman ρ. (c) and (e) fix [α/Fe] at +0.25.

| arm | group | N | ρ([α/Fe], z) | median [α/Fe] | median age (Gyr) | median [Fe/H] | median [C/Fe] | median [N/Fe] |
|---|---|---|---|---|---|---|---|---|
| (a) baseline | all | 135 | -0.47 (p 0.000) | -0.03 | 4.04 | -0.29 | – | – |
| (a) baseline | with Mg b | 61 | -0.23 (p 0.075) | +0.08 | 4.23 | -0.24 | – | – |
| (a) baseline | without Mg b | 74 | -0.15 (p 0.207) | -0.16 | 3.84 | -0.33 | – | – |
| (b) C/N free | all | 135 | -0.24 (p 0.006) | +0.12 | 4.44 | -0.42 | -0.02 | +0.30 |
| (b) C/N free | with Mg b | 61 | -0.27 (p 0.034) | +0.21 | 3.73 | -0.28 | +0.12 | +0.12 |
| (b) C/N free | without Mg b | 74 | +0.37 (p 0.001) | -0.05 | 4.70 | -0.57 | -0.14 | +0.45 |
| (c) C/N free, [α/Fe] = +0.25 | all | 135 | fixed | +0.25 | 4.38 | -0.52 | +0.11 | +0.38 |
| (c) C/N free, [α/Fe] = +0.25 | with Mg b | 61 | fixed | +0.25 | 3.68 | -0.29 | +0.13 | +0.18 |
| (c) C/N free, [α/Fe] = +0.25 | without Mg b | 74 | fixed | +0.25 | 4.64 | -0.63 | +0.07 | +0.60 |
| (d) carbon mask | all | 135 | -0.56 (p 0.000) | +0.09 | 4.39 | -0.37 | – | – |
| (d) carbon mask | with Mg b | 61 | -0.39 (p 0.002) | +0.20 | 4.66 | -0.37 | – | – |
| (d) carbon mask | without Mg b | 74 | -0.26 (p 0.027) | -0.11 | 4.27 | -0.38 | – | – |
| (e) as (c), 4155.0–4438.1 Å | all | 130 | fixed | +0.25 | 4.93 | -0.43 | -0.05 | +0.38 |
| (e) as (c), 4155.0–4438.1 Å | with Mg b | 60 | fixed | +0.25 | 4.99 | -0.42 | -0.07 | +0.35 |
| (e) as (c), 4155.0–4438.1 Å | without Mg b | 70 | fixed | +0.25 | 4.81 | -0.44 | -0.04 | +0.43 |
| (f) as (b), Mg b cut | all | 135 | +0.22 (p 0.011) | -0.08 | 4.64 | -0.42 | -0.13 | +0.32 |
| (f) as (b), Mg b cut | with Mg b | 61 | +0.10 (p 0.428) | -0.09 | 4.52 | -0.29 | -0.11 | +0.21 |
| (f) as (b), Mg b cut | without Mg b | 74 | +0.37 (p 0.001) | -0.05 | 4.70 | -0.57 | -0.14 | +0.45 |
| (g) baseline, Mg b cut | all | 135 | -0.29 (p 0.001) | -0.10 | 3.93 | -0.30 | – | – |
| (g) baseline, Mg b cut | with Mg b | 61 | -0.09 (p 0.482) | -0.06 | 4.06 | -0.26 | – | – |
| (g) baseline, Mg b cut | without Mg b | 74 | -0.15 (p 0.207) | -0.16 | 3.84 | -0.33 | – | – |

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
| (b) − (a) | with Mg b | 61 | -0.15 | -0.92 to +0.48 | 0.44 | +0.01 (-2.19 to +2.60) | +0.01 (p 0.944) |
| (b) − (a) | without Mg b | 74 | +0.52 | +0.09 to +1.15 | 0.92 | -0.71 (-1.40 to -0.04) | -0.12 (p 0.295) |
| (c) − (a) | all | 135 | +0.20 | -0.61 to +0.90 | 0.64 | +2.73 (+2.21 to +3.26) | +0.40 (p 0.000) |
| (c) − (a) | with Mg b | 61 | -0.18 | -1.02 to +0.35 | 0.38 | -0.64 (-2.77 to +1.91) | -0.06 (p 0.673) |
| (c) − (a) | without Mg b | 74 | +0.50 | +0.02 to +1.13 | 0.85 | -0.37 (-1.12 to +0.39) | +0.01 (p 0.920) |
| (d) − (a) | all | 135 | +0.25 | -0.05 to +0.68 | 0.79 | -1.17 (-1.43 to -0.91) | -0.28 (p 0.001) |
| (d) − (a) | with Mg b | 61 | +0.32 | +0.07 to +0.71 | 0.85 | -1.99 (-3.07 to -1.02) | -0.23 (p 0.074) |
| (d) − (a) | without Mg b | 74 | +0.14 | -0.07 to +0.60 | 0.74 | -1.35 (-1.71 to -0.99) | -0.37 (p 0.001) |
| (e) − (a) | all | 130 | +0.72 | -0.16 to +1.51 | 0.79 | -2.43 (-3.10 to -1.74) | -0.25 (p 0.005) |
| (e) − (a) | with Mg b | 60 | +0.69 | +0.03 to +1.60 | 0.85 | -1.44 (-3.44 to +0.63) | -0.11 (p 0.399) |
| (e) − (a) | without Mg b | 70 | +0.73 | -0.31 to +1.46 | 0.74 | -3.50 (-4.63 to -2.38) | -0.42 (p 0.000) |
| (f) − (a) | all | 135 | +0.45 | -0.23 to +1.09 | 0.76 | +1.13 (+0.65 to +1.62) | +0.12 (p 0.165) |
| (f) − (a) | with Mg b | 61 | +0.21 | -0.80 to +0.85 | 0.56 | -4.37 (-6.21 to -2.36) | -0.25 (p 0.048) |
| (f) − (a) | without Mg b | 74 | +0.52 | +0.09 to +1.15 | 0.92 | -0.71 (-1.40 to -0.04) | -0.12 (p 0.295) |
| (g) − (a) | all | 135 | +0.00 | -0.21 to +0.00 | 0.16 | +0.44 (+0.28 to +0.59) | +0.17 (p 0.049) |
| (g) − (a) | with Mg b | 61 | -0.09 | -0.50 to +0.13 | 0.34 | -0.69 (-1.57 to +0.01) | -0.12 (p 0.347) |
| (g) − (a) | without Mg b | 74 | +0.00 | +0.00 to +0.00 | 0.00 | +0.00 (+0.00 to +0.00) | – |
| (c) − (b) | all | 135 | -0.04 | -0.24 to +0.07 | 0.37 | +0.20 (+0.03 to +0.38) | +0.07 (p 0.443) |
| (c) − (b) | with Mg b | 61 | -0.04 | -0.24 to +0.10 | 0.34 | -0.64 (-1.06 to -0.19) | -0.17 (p 0.185) |
| (c) − (b) | without Mg b | 74 | -0.03 | -0.24 to +0.07 | 0.39 | +0.35 (+0.11 to +0.59) | +0.21 (p 0.066) |
| (e) − (c) | all | 130 | +0.47 | -0.72 to +1.56 | 0.68 | -5.32 (-5.98 to -4.67) | -0.53 (p 0.000) |
| (e) − (c) | with Mg b | 60 | +1.08 | +0.40 to +2.01 | 0.88 | -0.50 (-3.40 to +1.99) | -0.06 (p 0.666) |
| (e) − (c) | without Mg b | 70 | +0.01 | -0.89 to +0.78 | 0.50 | -3.28 (-4.22 to -2.35) | -0.39 (p 0.001) |
| (f) − (b) | all | 135 | +0.00 | +0.00 to +0.36 | 0.32 | -1.39 (-1.70 to -1.10) | -0.44 (p 0.000) |
| (f) − (b) | with Mg b | 61 | +0.15 | -0.22 to +0.93 | 0.70 | -4.38 (-5.81 to -3.18) | -0.46 (p 0.000) |
| (f) − (b) | without Mg b | 74 | +0.00 | +0.00 to +0.00 | 0.00 | +0.00 (+0.00 to +0.00) | – |

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

- `scripts/plot_prior_kl.py` `label()` has no entry for `cfe` or `nfe`. The local figure rebuild of `scripts/experiment.py` then stops with `KeyError: 'cfe'` and writes the failed notebook over the GPU notebook, so `validate_result` fails. No standard figures were rebuilt for (b), (c), (e), (f).
- `EmissionLineColumns` (`ceridwen/ceridwen/likelihood/emission_lines.py:374`) raises when no emission line has fitted pixels (5 fits of (e)).
- `scripts/ceridwen_state.py` stops on a missing worktree.
- `cn-afe0p25-common/run/.modal/0/*.tar.gz` (550 MB of retrieval archives) are left in place and not committed.
