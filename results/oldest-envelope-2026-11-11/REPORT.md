# Oldest-galaxy age–redshift slope on the common-window fits

Liu Hao, 2026-11-11 11:08: "which prior, the age prior? galaxies themselves error can be overcome by sampling the oldest galaxies only to remove progenitor bias. i see smaller subset messes with slope -> what about legac dr3 data? would that be compatible? i don't even know if it contains the extra redshift wavelengths, or if the extra dr3 data can be compared apples to apples e.g. would it be calibrated in a different way"

Recorded question, 11:09: "What I'd do, in order: 1. Oldest-galaxy slope on the existing window fits (no new fits). 2. Download DR3 and refit the 10 test galaxies from both releases on the common window, to measure the DR2-to-DR3 shift. 3. If that's clean, refit the full DR3 quiescent sample. Shall I start 1 and 2?"

Liu Hao, 11:13: "yeah do all 3"

This record is item 1. No new fits, no GPU.

## Setup

- Inputs (read only): `results/chronometer-135-2026-11-10/per-fit.csv`; LEGA-C DR2 catalogue `data/raw/legac_dr2/legaCdr2.fits.gz`, column `SIGMA_STARS_PRIME` ("observed stellar velocity dispersion", ESO DR2 release description).
- Arms: the common-window fits (e), (h) on 4155.0–4438.1 Å and (i), (j) on 4074.5–4666.1 Å, rest vacuum; settings in `results/chronometer-135-2026-11-10/REPORT.md`.
- Age: posterior median mass-weighted age; δa = posterior 84th minus 50th percentile (edge estimator only).
- Samples: "own valid" (130, 130, 110, 110 fits); "same 108", the galaxies valid in all four arms; "same 108, σ★ > 215", 41 of them. `envelope-slopes.csv` also has "own valid, σ★ > 215" (55 for (e), (h); 41 for (i), (j)) and "same galaxies, σ★ > 215".
- Bootstrap: 10000 resamples of galaxies, seed 20261110, as `results/chronometer-135-2026-11-10`. Each draw recomputes the bins, the selection and the slope. Same draws for all estimators of a sample; "envelope minus all galaxies" uses the paired draws.
- Slope through the binned points: unweighted least squares (Borghi et al. 2022b, Sect. 3.1, do not weight by age errors).
- Bins: equal-count bins in z (`numpy.array_split` sizes), 2 to 6 bins (Borghi et al. 2022b, Sect. 3.1: "from two up to six redshift intervals"; equally populated bins are one of their checks).
- Planck18 line: least-squares slope of the Planck18 age of the universe (ceridwen `age_gyr`, the fit cosmology) at the sample's redshifts. "Same estimator on t_univ(z)": the estimator applied to t_univ(z_i) of the same galaxies (coeval, zero scatter).
- H = -977.79 / ((1 + z_med) · slope) km/s/Mpc, as `results/chronometer-135-2026-11-10/REPORT.md` (Jimenez & Loeb 2002, eq. 2); z_med is the sample median redshift. A slope ≥ 0 gives no H.
- Defaults fixed in `envelope.py` before the run: oldest half with 4 bins, 75th percentile with 4 bins, τ = 0.7, edge with 4 bins.
- The all-galaxy slopes, Planck18 lines and H values reproduce `results/chronometer-135-2026-11-10/REPORT.md` (own valid: -3.77, -3.26, -4.60, -5.37; same 108: -4.66, -3.90, -4.62, -5.39).

## Definitions

| estimator | used here | source |
|---|---|---|
| upper cut-off | Compare the upper cut-off of the age distributions of passively evolving galaxies at two redshifts. | Jimenez & Loeb 2002, ApJ 573, 37, Sect. 1 |
| oldest fraction f | In each bin, the k = max(1, round(f·n)) oldest of the n galaxies; point: their median age at their median z. f = 0.5, 1/3, 0.25, 0.2. f = 0.5 is "only the D4000n values above the median D4000n in each redshift bin, and then estimate the median", applied to age. | Moresco et al. 2012a, JCAP 08 (2012) 006, App. A.1 |
| bin percentile q | Age percentile q of each bin (numpy linear interpolation) at the bin median z. q = 0.75, 0.84, 0.90. Moresco et al. 2012a use the 75th upper percentile "as a proxy of the upper-envelope". | Moresco et al. 2012a, App. A.1 |
| quantile regression τ | Linear quantile regression of age on z over all galaxies (linear program, scipy HiGHS). τ = 0.7, 0.8, 0.9. Reference method for the red envelope: "quantile regression when including 30% of the points"; the result "converges quickly after choosing more than 10% of the points". τ = 0.7 is read here as 30 % of galaxies above the line. | Jimenez, Moresco, Verde & Wandelt 2023, arXiv:2306.11425, Sect. 2.3 |
| edge, ΔlnP = 0.5 | In each bin, P(t \| a_i) = 1 for t > a_i + δa_i, otherwise ln P = -x², x = (a_i + δa_i - t) / (√2 δa_i). The edge is where the ln of the product over the bin "drops by 0.5 from its maximum". Point at the bin median z. | Jimenez, Verde, Treu & Stern 2003, ApJ 593, 622, Sect. 3.4; followed by Stern et al. 2010, JCAP 02 (2010) 008, Sect. 5 |
| σ★ > 215 km/s | Higher-σ★ subsample. Borghi et al. 2022b split their 140 LEGA-C galaxies at the median σ★ = 215 km/s and take the median age per bin of each subsample. Moresco et al. 2022 list "a cut in stellar mass, or, equivalently, in stellar velocity dispersion σ★" as a selection criterion. | Borghi, Moresco & Cimatti 2022b, ApJL 928, L4, Sect. 2; Moresco et al. 2022, Living Rev. Relativ. 25, 6, Sect. 3.1.2 |

- Progenitor bias: Moresco et al. 2022, Sect. 3.1.4, state that the upper envelope of the age–z distribution "by definition, could not be biased by the progenitor bias effect", and that the progenitor bias "flattens the age − z relations".

## Defaults: slope (Gyr/z), bootstrap 16–84, [galaxies that set each point]

For quantile regression, [ ] is the number of galaxies above the fitted line. For the edge, it is the number with a_i + δa_i above the edge.

| arm | sample | N | z med | all galaxies | oldest half, 4 bins | 75th percentile, 4 bins | quantile regression, τ = 0.7 | edge, ΔlnP = 0.5, 4 bins | Planck18 line |
|---|---|---|---|---|---|---|---|---|---|
| (e) as (c), 4155.0–4438.1 Å | own valid | 130 | 0.728 | -3.77 (-4.42 to -3.09) | -4.77 (-5.61 to -4.01) [16–17] | -4.99 (-5.45 to -4.02) [32–33] | -5.01 (-5.36 to -4.09) [38] | -4.24 (-5.00 to -3.29) [3–6] | -5.19 |
| (h) baseline, 4155.0–4438.1 Å | own valid | 130 | 0.728 | -3.26 (-3.90 to -2.61) | -4.56 (-5.13 to -3.37) [16–17] | -4.92 (-5.24 to -3.50) [32–33] | -4.20 (-4.53 to -3.88) [38] | -2.97 (-4.75 to -2.03) [2–7] | -5.19 |
| (i) baseline, 4074.5–4666.1 Å | own valid | 110 | 0.725 | -4.60 (-5.54 to -3.58) | -3.82 (-5.77 to -3.35) [14] | -4.19 (-5.78 to -3.25) [27–28] | -5.09 (-5.68 to -3.97) [32] | -5.34 (-7.55 to -4.08) [2–3] | -5.31 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | 110 | 0.725 | -5.37 (-6.27 to -4.37) | -5.12 (-6.71 to -4.82) [14] | -5.61 (-6.88 to -4.61) [27–28] | -6.11 (-6.81 to -5.46) [32] | -3.74 (-6.01 to -2.54) [1–9] | -5.31 |
| (e) as (c), 4155.0–4438.1 Å | same 108 | 108 | 0.714 | -4.66 (-5.62 to -3.68) | -5.10 (-6.43 to -3.79) [14] | -5.52 (-6.55 to -3.68) [27] | -5.32 (-6.27 to -4.66) [32] | -4.45 (-5.25 to -3.23) [1–6] | -5.31 |
| (h) baseline, 4155.0–4438.1 Å | same 108 | 108 | 0.714 | -3.90 (-4.89 to -2.90) | -3.90 (-5.27 to -2.90) [14] | -4.39 (-5.62 to -3.08) [27] | -4.16 (-4.86 to -3.03) [31] | -3.26 (-4.52 to -2.05) [1–6] | -5.31 |
| (i) baseline, 4074.5–4666.1 Å | same 108 | 108 | 0.714 | -4.62 (-5.58 to -3.60) | -4.03 (-5.66 to -3.26) [14] | -4.73 (-5.96 to -3.44) [27] | -5.06 (-5.66 to -4.01) [31] | -5.32 (-7.47 to -4.04) [2–3] | -5.31 |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | 108 | 0.714 | -5.39 (-6.32 to -4.41) | -5.13 (-6.55 to -4.75) [14] | -6.03 (-6.97 to -4.82) [27] | -5.96 (-6.81 to -5.47) [32] | -3.68 (-5.87 to -2.52) [1–9] | -5.31 |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | 41 | 0.703 | -5.31 (-6.94 to -3.67) | -4.11 (-6.88 to -2.97) [5–6] | -3.74 (-5.76 to -2.87) [10–11] | -5.48 (-5.79 to -3.40) [11] | -3.54 (-4.62 to -2.79) [2–6] | -5.30 |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | 41 | 0.703 | -4.26 (-5.88 to -2.62) | -3.72 (-5.87 to -2.58) [5–6] | -3.99 (-5.13 to -2.59) [10–11] | -3.40 (-4.37 to -2.90) [12] | -2.20 (-4.27 to -1.35) [1–4] | -5.30 |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | 41 | 0.703 | -5.46 (-6.80 to -4.04) | -5.62 (-7.46 to -3.56) [5–6] | -5.49 (-6.97 to -3.66) [10–11] | -5.66 (-6.64 to -4.68) [12] | -4.44 (-7.42 to -2.95) [1–2] | -5.30 |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | 41 | 0.703 | -6.22 (-7.54 to -4.76) | -5.69 (-7.75 to -2.33) [5–6] | -5.98 (-7.22 to -2.75) [10–11] | -6.02 (-6.90 to -4.90) [11] | -2.97 (-6.80 to -2.12) [1–3] | -5.30 |

## Defaults: envelope slope minus all-galaxy slope (Gyr/z), paired bootstrap median and 16–84

| arm | sample | oldest half, 4 bins | 75th percentile, 4 bins | quantile regression, τ = 0.7 | edge, ΔlnP = 0.5, 4 bins |
|---|---|---|---|---|---|
| (e) as (c), 4155.0–4438.1 Å | own valid | -0.98 (-1.90 to -0.18) | -0.94 (-1.73 to -0.21) | -0.99 (-1.60 to -0.38) | -0.34 (-1.35 to 0.59) |
| (h) baseline, 4155.0–4438.1 Å | own valid | -0.98 (-1.86 to -0.16) | -1.14 (-1.91 to -0.34) | -0.90 (-1.46 to -0.34) | 0.15 (-1.44 to 1.29) |
| (i) baseline, 4074.5–4666.1 Å | own valid | 0.02 (-1.23 to 1.16) | 0.01 (-1.17 to 1.14) | -0.30 (-1.14 to 0.59) | -1.04 (-3.03 to 0.68) |
| (j) C/N free, 4074.5–4666.1 Å | own valid | -0.34 (-1.54 to 0.68) | -0.42 (-1.56 to 0.70) | -0.75 (-1.50 to 0.02) | 1.35 (-0.90 to 2.88) |
| (e) as (c), 4155.0–4438.1 Å | same 108 | -0.45 (-1.78 to 0.78) | -0.47 (-1.81 to 0.85) | -0.72 (-1.57 to 0.19) | 0.42 (-0.82 to 1.63) |
| (h) baseline, 4155.0–4438.1 Å | same 108 | -0.18 (-1.31 to 0.97) | -0.47 (-1.61 to 0.72) | -0.17 (-1.03 to 0.76) | 0.68 (-0.75 to 1.98) |
| (i) baseline, 4074.5–4666.1 Å | same 108 | 0.13 (-1.04 to 1.19) | -0.12 (-1.28 to 0.99) | -0.27 (-1.12 to 0.62) | -0.86 (-2.91 to 0.79) |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | -0.22 (-1.36 to 0.75) | -0.53 (-1.61 to 0.56) | -0.71 (-1.47 to 0.05) | 1.47 (-0.78 to 2.96) |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | 0.57 (-1.58 to 2.51) | 0.99 (-0.68 to 2.82) | 0.26 (-1.10 to 1.85) | 1.51 (-0.13 to 3.32) |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | 0.23 (-1.72 to 2.18) | 0.35 (-1.32 to 2.14) | 0.46 (-0.89 to 2.00) | 1.58 (-0.20 to 3.41) |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | -0.14 (-2.06 to 1.66) | 0.07 (-1.69 to 1.80) | -0.23 (-1.45 to 1.19) | 0.25 (-2.14 to 2.56) |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | 0.46 (-1.63 to 3.04) | 0.72 (-1.29 to 2.94) | 0.28 (-0.89 to 1.61) | 2.27 (-0.42 to 4.34) |

## Defaults: H (km/s/Mpc), central and (from the 16–84 slopes)

| arm | sample | all galaxies | oldest half, 4 bins | 75th percentile, 4 bins | quantile regression, τ = 0.7 | edge, ΔlnP = 0.5, 4 bins | Planck18 line |
|---|---|---|---|---|---|---|---|
| (e) as (c), 4155.0–4438.1 Å | own valid | 150 (128–183) | 119 (101–141) | 113 (104–141) | 113 (106–138) | 134 (113–172) | 109 |
| (h) baseline, 4155.0–4438.1 Å | own valid | 174 (145–217) | 124 (110–168) | 115 (108–162) | 135 (125–146) | 191 (119–279) | 109 |
| (i) baseline, 4074.5–4666.1 Å | own valid | 123 (102–158) | 148 (98–169) | 135 (98–175) | 111 (100–143) | 106 (75–139) | 107 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | 106 (90–130) | 111 (85–118) | 101 (82–123) | 93 (83–104) | 152 (94–224) | 107 |
| (e) as (c), 4155.0–4438.1 Å | same 108 | 122 (102–155) | 112 (89–151) | 103 (87–155) | 107 (91–122) | 128 (109–176) | 107 |
| (h) baseline, 4155.0–4438.1 Å | same 108 | 146 (117–197) | 146 (108–197) | 130 (102–185) | 137 (117–188) | 175 (126–278) | 107 |
| (i) baseline, 4074.5–4666.1 Å | same 108 | 123 (102–159) | 141 (101–175) | 121 (96–166) | 113 (101–142) | 107 (76–141) | 107 |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | 106 (90–129) | 111 (87–120) | 95 (82–118) | 96 (84–104) | 155 (97–227) | 107 |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | 108 (83–156) | 140 (83–193) | 153 (100–200) | 105 (99–169) | 162 (124–206) | 108 |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | 135 (98–219) | 154 (98–222) | 144 (112–222) | 169 (131–198) | 261 (134–425) | 108 |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | 105 (84–142) | 102 (77–161) | 104 (82–157) | 101 (86–123) | 129 (77–194) | 108 |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | 92 (76–121) | 101 (74–247) | 96 (79–208) | 95 (83–117) | 193 (84–271) | 108 |

## Stability across choices

Each row: all choices of one estimator family (oldest fraction: 4 fractions × 5 bin counts; bin percentile: 3 × 5; quantile regression: 3 τ; edge: 5 bin counts). "Planck18 line inside 16–84": choices whose bootstrap 16–84 contains the Planck18 line. "Steeper" / "shallower": choices whose paired 84th percentile is below zero / 16th percentile is above zero.

| arm | sample | estimator | choices | slope, min to max (median) | Planck18 line inside 16–84 | steeper than all galaxies | shallower than all galaxies | galaxies per point | same estimator on t_univ(z) |
|---|---|---|---|---|---|---|---|---|---|
| (e) as (c), 4155.0–4438.1 Å | own valid | oldest fraction | 20 | -8.28 to -3.68 (-4.43) | 10 | 9 | 0 | 4–33 | -5.92 to -5.36 |
| (e) as (c), 4155.0–4438.1 Å | own valid | bin percentile | 15 | -5.63 to -3.13 (-4.39) | 6 | 5 | 0 | 21–65 | -6.01 to -2.69 |
| (e) as (c), 4155.0–4438.1 Å | own valid | quantile regression | 3 | -5.01 to -4.32 (-4.52) | 2 | 2 | 0 | 12–38 | -5.22 to -5.10 |
| (e) as (c), 4155.0–4438.1 Å | own valid | edge | 5 | -4.24 to -2.89 (-3.98) | 0 | 0 | 0 | 1–6 | – |
| (h) baseline, 4155.0–4438.1 Å | own valid | oldest fraction | 20 | -7.96 to -3.56 (-4.17) | 8 | 15 | 0 | 4–33 | -5.92 to -5.36 |
| (h) baseline, 4155.0–4438.1 Å | own valid | bin percentile | 15 | -4.97 to -2.31 (-4.19) | 4 | 9 | 0 | 21–65 | -6.01 to -2.69 |
| (h) baseline, 4155.0–4438.1 Å | own valid | quantile regression | 3 | -4.66 to -4.20 (-4.21) | 0 | 3 | 0 | 12–38 | -5.22 to -5.10 |
| (h) baseline, 4155.0–4438.1 Å | own valid | edge | 5 | -3.56 to -1.70 (-2.97) | 0 | 0 | 0 | 1–7 | – |
| (i) baseline, 4074.5–4666.1 Å | own valid | oldest fraction | 20 | -9.45 to -3.04 (-4.94) | 20 | 1 | 0 | 4–28 | -5.93 to -5.55 |
| (i) baseline, 4074.5–4666.1 Å | own valid | bin percentile | 15 | -7.71 to -3.80 (-5.31) | 15 | 1 | 0 | 18–55 | -9.92 to -3.83 |
| (i) baseline, 4074.5–4666.1 Å | own valid | quantile regression | 3 | -7.77 to -4.94 (-5.09) | 3 | 1 | 0 | 10–32 | -5.37 to -5.32 |
| (i) baseline, 4074.5–4666.1 Å | own valid | edge | 5 | -7.01 to -5.34 (-6.44) | 5 | 1 | 0 | 2–4 | – |
| (j) C/N free, 4074.5–4666.1 Å | own valid | oldest fraction | 20 | -8.59 to -2.78 (-5.72) | 19 | 1 | 0 | 4–28 | -5.93 to -5.55 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | bin percentile | 15 | -7.71 to -4.31 (-6.31) | 13 | 2 | 0 | 18–55 | -9.92 to -3.83 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | quantile regression | 3 | -6.52 to -5.25 (-6.11) | 2 | 0 | 0 | 10–32 | -5.37 to -5.32 |
| (j) C/N free, 4074.5–4666.1 Å | own valid | edge | 5 | -7.21 to -3.74 (-4.05) | 4 | 1 | 0 | 1–10 | – |
| (e) as (c), 4155.0–4438.1 Å | same 108 | oldest fraction | 20 | -7.11 to -3.64 (-4.42) | 18 | 0 | 0 | 4–27 | -5.93 to -5.55 |
| (e) as (c), 4155.0–4438.1 Å | same 108 | bin percentile | 15 | -6.13 to -3.48 (-5.20) | 15 | 0 | 0 | 18–54 | -9.98 to -3.86 |
| (e) as (c), 4155.0–4438.1 Å | same 108 | quantile regression | 3 | -5.48 to -4.29 (-5.32) | 2 | 0 | 0 | 10–32 | -5.39 to -5.33 |
| (e) as (c), 4155.0–4438.1 Å | same 108 | edge | 5 | -5.35 to -4.25 (-4.45) | 3 | 0 | 0 | 1–6 | – |
| (h) baseline, 4155.0–4438.1 Å | same 108 | oldest fraction | 20 | -5.29 to -2.73 (-3.87) | 10 | 0 | 0 | 4–27 | -5.93 to -5.55 |
| (h) baseline, 4155.0–4438.1 Å | same 108 | bin percentile | 15 | -4.98 to -2.33 (-4.05) | 15 | 0 | 0 | 18–54 | -9.98 to -3.86 |
| (h) baseline, 4155.0–4438.1 Å | same 108 | quantile regression | 3 | -4.66 to -3.50 (-4.16) | 0 | 0 | 0 | 9–31 | -5.39 to -5.33 |
| (h) baseline, 4155.0–4438.1 Å | same 108 | edge | 5 | -3.87 to -2.89 (-3.46) | 1 | 0 | 0 | 1–7 | – |
| (i) baseline, 4074.5–4666.1 Å | same 108 | oldest fraction | 20 | -8.58 to -3.04 (-5.07) | 20 | 0 | 0 | 4–27 | -5.93 to -5.55 |
| (i) baseline, 4074.5–4666.1 Å | same 108 | bin percentile | 15 | -6.80 to -4.11 (-5.30) | 15 | 0 | 0 | 18–54 | -9.98 to -3.86 |
| (i) baseline, 4074.5–4666.1 Å | same 108 | quantile regression | 3 | -7.77 to -4.94 (-5.06) | 3 | 1 | 0 | 10–31 | -5.39 to -5.33 |
| (i) baseline, 4074.5–4666.1 Å | same 108 | edge | 5 | -7.50 to -5.32 (-5.98) | 5 | 1 | 0 | 2–5 | – |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | oldest fraction | 20 | -8.82 to -2.78 (-5.80) | 19 | 1 | 0 | 4–27 | -5.93 to -5.55 |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | bin percentile | 15 | -7.76 to -4.39 (-6.40) | 14 | 1 | 0 | 18–54 | -9.98 to -3.86 |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | quantile regression | 3 | -6.52 to -5.66 (-5.96) | 2 | 0 | 0 | 10–32 | -5.39 to -5.33 |
| (j) C/N free, 4074.5–4666.1 Å | same 108 | edge | 5 | -7.26 to -3.36 (-3.98) | 4 | 0 | 0 | 1–9 | – |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | oldest fraction | 20 | -8.50 to -3.19 (-3.85) | 16 | 0 | 0 | 1–11 | -5.93 to -5.51 |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | bin percentile | 15 | -7.93 to -3.13 (-3.74) | 12 | 0 | 0 | 6–21 | -9.41 to -4.00 |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | quantile regression | 3 | -5.48 to -3.95 (-4.14) | 2 | 0 | 0 | 3–11 | -5.40 to -5.37 |
| (e) as (c), 4155.0–4438.1 Å | same 108, σ★ > 215 | edge | 5 | -4.91 to -3.17 (-3.54) | 2 | 0 | 0 | 1–8 | – |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | oldest fraction | 20 | -8.47 to -1.33 (-3.69) | 11 | 0 | 0 | 1–11 | -5.93 to -5.51 |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | bin percentile | 15 | -7.97 to -2.74 (-3.99) | 6 | 0 | 0 | 6–21 | -9.41 to -4.00 |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | quantile regression | 3 | -3.91 to -1.13 (-3.40) | 0 | 0 | 0 | 3–12 | -5.40 to -5.37 |
| (h) baseline, 4155.0–4438.1 Å | same 108, σ★ > 215 | edge | 5 | -2.75 to -1.74 (-2.20) | 1 | 0 | 0 | 1–6 | – |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | oldest fraction | 20 | -9.82 to -4.23 (-6.24) | 20 | 0 | 0 | 1–11 | -5.93 to -5.51 |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | bin percentile | 15 | -9.93 to -4.43 (-5.75) | 15 | 0 | 0 | 6–21 | -9.41 to -4.00 |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | quantile regression | 3 | -6.30 to -5.66 (-6.30) | 3 | 0 | 0 | 3–12 | -5.40 to -5.37 |
| (i) baseline, 4074.5–4666.1 Å | same 108, σ★ > 215 | edge | 5 | -10.67 to -4.44 (-5.97) | 5 | 0 | 0 | 1–3 | – |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | oldest fraction | 20 | -9.00 to -2.34 (-5.72) | 20 | 0 | 0 | 1–11 | -5.93 to -5.51 |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | bin percentile | 15 | -9.45 to -2.37 (-5.69) | 15 | 0 | 0 | 6–21 | -9.41 to -4.00 |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | quantile regression | 3 | -6.02 to -2.41 (-5.64) | 3 | 0 | 0 | 3–11 | -5.40 to -5.37 |
| (j) C/N free, 4074.5–4666.1 Å | same 108, σ★ > 215 | edge | 5 | -7.70 to -2.97 (-3.67) | 5 | 0 | 0 | 1–5 | – |

- Same estimator on t_univ(z): the bin percentile at the bin median z gives -9.98 to -2.69 Gyr/z for coeval, zero-scatter ages; the oldest fraction gives -5.93 to -5.24; quantile regression -5.40 to -5.10.
- Bootstrap: in 13 % of all rows of `envelope-slopes.csv` the bootstrap median differs from the central slope by more than half the 16–84 width (median absolute difference 0.30 Gyr/z).

## Grid, own valid fits: oldest fraction, central slope (Gyr/z)

| f | bins | per point, (e) (h) | per point, (i) (j) | (e) | (h) | (i) | (j) | t_univ, (e) (h) | t_univ, (i) (j) |
|---|---|---|---|---|---|---|---|---|---|
| 0.50 | 2 | 33 | 28 | -8.28 | -6.68 | -4.67 | -7.57 | -5.70 | -5.71 |
| 0.50 | 3 | 22 | 18–19 | -6.15 | -4.71 | -9.45 | -8.59 | -5.52 | -5.72 |
| 0.50 | 4 | 16–17 | 14 | -4.77 | -4.56 | -3.82 | -5.12 | -5.49 | -5.69 |
| 0.50 | 5 | 13 | 11 | -4.48 | -4.10 | -4.70 | -5.58 | -5.36 | -5.57 |
| 0.50 | 6 | 11 | 9–10 | -4.91 | -4.65 | -4.60 | -5.61 | -5.37 | -5.55 |
| 0.33 | 2 | 22 | 18 | -7.77 | -7.96 | -7.15 | -4.49 | -5.87 | -5.85 |
| 0.33 | 3 | 14–15 | 12 | -5.42 | -4.68 | -4.96 | -6.63 | -5.64 | -5.88 |
| 0.33 | 4 | 11 | 9 | -4.27 | -3.91 | -4.83 | -5.46 | -5.52 | -5.76 |
| 0.33 | 5 | 9 | 7 | -4.22 | -3.92 | -4.19 | -5.52 | -5.45 | -5.61 |
| 0.33 | 6 | 7 | 6 | -4.40 | -3.83 | -5.71 | -6.31 | -5.39 | -5.57 |
| 0.25 | 2 | 16 | 14 | -7.08 | -4.26 | -4.15 | -2.78 | -5.92 | -5.91 |
| 0.25 | 3 | 11 | 9 | -3.83 | -4.39 | -5.46 | -5.84 | -5.73 | -5.88 |
| 0.25 | 4 | 8 | 7 | -3.92 | -3.98 | -4.98 | -5.01 | -5.55 | -5.81 |
| 0.25 | 5 | 7 | 6 | -4.38 | -3.75 | -4.92 | -5.87 | -5.48 | -5.65 |
| 0.25 | 6 | 5–6 | 5 | -4.27 | -3.67 | -6.21 | -6.63 | -5.39 | -5.58 |
| 0.20 | 2 | 13 | 11 | -6.21 | -6.21 | -3.04 | -2.86 | -5.92 | -5.93 |
| 0.20 | 3 | 9 | 7 | -3.68 | -4.24 | -7.04 | -6.43 | -5.73 | -5.91 |
| 0.20 | 4 | 6–7 | 5–6 | -3.89 | -3.79 | -4.91 | -4.71 | -5.56 | -5.86 |
| 0.20 | 5 | 5 | 4 | -4.13 | -3.56 | -5.94 | -6.19 | -5.51 | -5.73 |
| 0.20 | 6 | 4 | 4 | -4.45 | -4.02 | -6.78 | -6.72 | -5.40 | -5.59 |

## Grid, own valid fits: bin percentile, central slope (Gyr/z)

| q | bins | per point, (e) (h) | per point, (i) (j) | (e) | (h) | (i) | (j) | t_univ, (e) (h) | t_univ, (i) (j) |
|---|---|---|---|---|---|---|---|---|---|
| 0.75 | 2 | 65 | 55 | -3.71 | -3.02 | -3.80 | -6.31 | -2.69 | -5.30 |
| 0.75 | 3 | 43–44 | 36–37 | -5.63 | -4.51 | -7.09 | -7.71 | -6.01 | -3.83 |
| 0.75 | 4 | 32–33 | 27–28 | -4.99 | -4.92 | -4.19 | -5.61 | -5.35 | -5.38 |
| 0.75 | 5 | 26 | 22 | -4.63 | -4.46 | -4.96 | -6.16 | -5.56 | -6.09 |
| 0.75 | 6 | 21–22 | 18–19 | -4.30 | -4.19 | -4.74 | -5.86 | -4.64 | -5.82 |
| 0.84 | 2 | 65 | 55 | -3.19 | -2.89 | -5.69 | -4.31 | -4.40 | -7.59 |
| 0.84 | 3 | 43–44 | 36–37 | -5.13 | -4.76 | -6.98 | -7.66 | -5.71 | -5.10 |
| 0.84 | 4 | 32–33 | 27–28 | -4.93 | -4.37 | -5.18 | -5.67 | -5.17 | -5.13 |
| 0.84 | 5 | 26 | 22 | -4.36 | -4.02 | -4.68 | -6.36 | -5.10 | -5.85 |
| 0.84 | 6 | 21–22 | 18–19 | -3.90 | -3.47 | -5.31 | -6.63 | -4.57 | -5.72 |
| 0.90 | 2 | 65 | 55 | -3.13 | -2.31 | -4.73 | -4.68 | -4.60 | -9.92 |
| 0.90 | 3 | 43–44 | 36–37 | -4.39 | -4.97 | -7.71 | -7.20 | -4.99 | -4.95 |
| 0.90 | 4 | 32–33 | 27–28 | -4.49 | -4.56 | -5.46 | -4.99 | -5.13 | -4.53 |
| 0.90 | 5 | 26 | 22 | -4.49 | -3.85 | -5.63 | -6.95 | -5.01 | -5.40 |
| 0.90 | 6 | 21–22 | 18–19 | -3.95 | -3.45 | -6.56 | -7.17 | -4.57 | -5.75 |

## Own valid fits: quantile regression and edge, slope (Gyr/z), bootstrap 16–84, [galaxies]

| estimator | τ or bins | (e) | (h) | (i) | (j) |
|---|---|---|---|---|---|
| edge | 2 bins | -2.89 (-4.47 to -2.45) [4–6] | -1.70 (-3.59 to -1.19) [4] | -5.93 (-8.48 to -3.97) [2–3] | -7.21 (-8.52 to -5.54) [4–9] |
| edge | 3 bins | -4.16 (-4.88 to -3.24) [2–6] | -3.22 (-4.38 to -2.37) [4] | -6.57 (-8.29 to -3.75) [2–4] | -3.75 (-6.40 to -3.23) [1–10] |
| edge | 4 bins | -4.24 (-5.00 to -3.29) [3–6] | -2.97 (-4.75 to -2.03) [2–7] | -5.34 (-7.55 to -4.08) [2–3] | -3.74 (-6.01 to -2.54) [1–9] |
| edge | 5 bins | -3.98 (-4.88 to -3.37) [1–6] | -2.88 (-4.64 to -2.21) [1–7] | -6.44 (-7.63 to -4.12) [2] | -5.03 (-7.49 to -2.86) [1–6] |
| edge | 6 bins | -3.94 (-4.82 to -3.58) [1–6] | -3.56 (-4.45 to -2.95) [1–6] | -7.01 (-7.76 to -5.12) [2–4] | -4.05 (-7.65 to -3.40) [1–9] |
| quantile regression | τ = 0.7 | -5.01 (-5.36 to -4.09) [38] | -4.20 (-4.53 to -3.88) [38] | -5.09 (-5.68 to -3.97) [32] | -6.11 (-6.81 to -5.46) [32] |
| quantile regression | τ = 0.8 | -4.52 (-5.36 to -4.19) [25] | -4.21 (-4.76 to -3.40) [25] | -4.94 (-6.64 to -4.53) [21] | -5.25 (-6.98 to -5.09) [21] |
| quantile regression | τ = 0.9 | -4.32 (-4.94 to -3.81) [12] | -4.66 (-5.11 to -3.65) [12] | -7.77 (-7.94 to -4.76) [10] | -6.52 (-7.17 to -3.75) [10] |

## Numbers in brief

- Own valid fits, defaults (oldest half, 75th percentile, τ = 0.7, edge): (e) -4.77, -4.99, -5.01, -4.24, all galaxies -3.77; (h) -4.56, -4.92, -4.20, -2.97, all -3.26; (i) -3.82, -4.19, -5.09, -5.34, all -4.60; (j) -5.12, -5.61, -6.11, -3.74, all -5.37. Planck18 line -5.19 ((e), (h)), -5.31 ((i), (j)).
- Own valid fits, all 43 choices: central slope (e) -8.28 to -2.89, (h) -7.96 to -1.70, (i) -9.45 to -3.04, (j) -8.59 to -2.78 Gyr/z.
- Envelope steeper than the all-galaxy slope (paired 84th < 0), own valid fits: (e) 16, (h) 27, (i) 4, (j) 4 of 43 choices. Same 108: (e) 0, (h) 0, (i) 2, (j) 2. Shallower (paired 16th > 0): none.
- Planck18 line inside the 16–84, own valid fits: (e) 18, (h) 12, (i) 43, (j) 38 of 43 choices.
- Envelope 16–84 half-width, defaults, own valid fits: 0.32–1.73 Gyr/z; all-galaxy: 0.64–0.98.
- Galaxies that set each point: oldest fraction 1–33, edge 1–10.

## Files

- `envelope.py`: writes both CSV files; every table above is read from `envelope-slopes.csv`. Run with `PYTHONPATH=external/sedpy_jax ceridwen/.venv/bin/python results/oldest-envelope-2026-11-11/envelope.py`. Quantile-regression bootstraps run in 8 worker processes.
- `envelope-slopes.csv`: one row per arm, sample, estimator and choice: slope, bootstrap 16/50/84, galaxies per point, all-galaxy slope, paired difference, Planck18 line, same estimator on t_univ(z), H.
- `envelope-points.csv`: every binned point of the central fits, with the number of galaxies that set it.

## Noticed, not done

- Arms (a)–(d), (f), (g), (k)–(m): not common-window fits; not analysed.
- Lower-σ★ subsample (Borghi et al. 2022b use both) and a stellar-mass cut (Moresco et al. 2022, log M > 10.6–11): not done. The Ceridwen `logmass` differs between arms.
- Constant-width z bins (Borghi et al. 2022b baseline, Δz ≈ 0.075, alternate points): not done; equal-count bins only.
- Items 2 and 3 of the approved list (DR3 download and refits): separate tasks.
