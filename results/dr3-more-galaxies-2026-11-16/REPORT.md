# More LEGA-C DR3 passive galaxies for the chronometer slope

2026-11-17. Tables: `age-redshift-slopes.csv`, `slope-differences.csv`, `fit-quality.csv`, `railing.csv`,
`photometry-by-cosmos2015-class.csv`, `fits.csv`. Code: `analysis.ipynb`.

## Sample

- Unchanged: quality flags, NUVrJ quiescent, [O II] EW < 5 Å, no 3σ [O II] or [O III], window 4074.5–4666.1 Å rest.
- Chain: 4057 → 2571 quality → 1222 NUVrJ quiescent → 931 [O II] EW → 581 no 3σ lines → 523 fittable photometry → 371 covers window → 348 one per OBJECT.
- Gained 154, combined 348.

| Change | Gained |
|---|---|
| COSMOS2015 clean cut → fittable photometry | 134 |
| NaN σ★ error → prior width 0.0388 σ★ (median fractional error of the 194) | 14 |
| Both of the above | 4 |
| One spectrum per OBJECT picked after the window cut | 2 |

- Fits: same two arms and seed as the 194 (`dr3_cn_free_w`, `dr3_plain_w`). Plain 154 of 154 valid. C/N-free 153 of 154.
- M102_214235 (σ★ 82.9 km/s, S/N 7) has no C/N-free fit: the alf response needs total σ ≥ 100 km/s; this spectrum has 97.3.

## Slope and H

Slope in Gyr per unit z. H in km/s/Mpc. Brackets are the 16–84% bootstrap range. Median z is 0.728 for every row.

| Arm | Sample | N | Slope | z_eff | H(z_eff) | Planck18 H(z_eff) | H(median z) |
|---|---|---|---|---|---|---|---|
| C/N-free | 194 | 194 | −5.154 (−5.782, −4.534) | 0.775 | 106.9 (95.3, 121.5) | 105.4 | 109.8 (97.9, 124.8) |
| C/N-free | gained | 153 | −4.761 (−5.473, −4.029) | 0.772 | 115.9 (100.8, 136.9) | 105.3 | 118.8 (103.4, 140.4) |
| C/N-free | combined | 347 | −5.011 (−5.481, −4.533) | 0.774 | 110.0 (100.6, 121.6) | 105.4 | 112.9 (103.2, 124.8) |
| plain | 194 | 194 | −5.043 (−5.702, −4.388) | 0.775 | 109.2 (96.6, 125.6) | 105.4 | 112.2 (99.2, 128.9) |
| plain | gained | 154 | −4.309 (−5.001, −3.569) | 0.772 | 128.0 (110.3, 154.6) | 105.3 | 131.3 (113.2, 158.6) |
| plain | combined | 348 | −4.766 (−5.258, −4.281) | 0.774 | 115.7 (104.8, 128.8) | 105.4 | 118.7 (107.6, 132.2) |

- Gained minus 194 slope: C/N-free +0.39 ± 0.95 (0.4σ); plain +0.73 ± 0.97 (0.8σ).
- H(z_eff) 16–84% width, 194 → combined: C/N-free 26.2 → 21.0; plain 28.9 → 23.9.
- Residual age scatter, 194 / gained / combined: C/N-free 0.805 / 0.759 / 0.783 Gyr; plain 0.875 / 0.743 / 0.818 Gyr.

## Fit quality, gained against the 194

Medians; KS p in brackets.

| Quantity | C/N-free 194 | C/N-free gained | plain 194 | plain gained |
|---|---|---|---|---|
| χ² per pixel, catalogue errors | 1.885 | 1.899 (0.06) | 1.887 | 1.895 (0.09) |
| χ² per pixel, 3% floor | 1.245 | 1.277 (0.75) | 1.251 | 1.284 (0.76) |
| Photometry χ² per band | 1.070 | 1.210 (0.83) | 1.095 | 1.229 (0.65) |
| (fitted σ − σ★) / σ★ error | −0.959 | −1.011 (0.91) | −0.898 | −0.847 (0.92) |
| Age (Gyr) | 4.879 | 4.802 (0.40) | 4.879 | 4.824 (0.68) |
| [α/Fe] | 0.160 | 0.141 (0.47) | 0.131 | 0.139 (0.45) |
| [Fe/H] | −0.325 | −0.336 (0.48) | −0.317 | −0.324 (0.83) |
| [C/Fe] | −0.034 | −0.037 (0.95) | | |
| [N/Fe] | 0.238 | 0.353 (0.05) | | |

Posterior median within 5% of a prior bound, 194 / gained:

| Arm | [α/Fe] | [Fe/H] | [C/Fe] | [N/Fe] | log f_calib | σ beyond 2.5 errors | χ² per pixel (3% floor) > 3 |
|---|---|---|---|---|---|---|---|
| C/N-free | 3 / 0 | 3 / 0 | 4 / 1 | 4 / 1 | 19 / 7 | 1 / 0 | 7 / 1 |
| plain | 5 / 1 | 3 / 0 | | | 20 / 8 | 0 / 0 | 7 / 1 |

## What differs in the gained galaxies

**[O II].** Median [O II] EW 0.33 Å against 0.68 Å (KS p 0.025); median |EW / error| 0.87 against 1.34 (KS p 0.037).
Both [O II] cuts apply to every gained galaxy. The gained galaxies have the weaker [O II].
NUV−r, r−J, HδA, [O III] EW, S/N, z and σ★ match the 194 (KS p 0.13 to 0.96, `gained-vs-194.csv`).

**COSMOS2015 flags.** Column meanings from VizieR J/ApJS/224/24 (Laigle et al. 2016):

- `Area` (FLAG_HJMCC): 0 = UltraVISTA area, ≥1 = out of UltraVISTA.
- `Sat` (FLAG_PETER): 0 = good area, ≥1 = saturated objects and bad areas, masked in the optical broad bands.
- `Cfl` (FLAG_COSMOS): 1 = the 2 deg² COSMOS area.
- `Flag` (FLAG_SHALLOW): "Shallow flag". The VizieR and IRSA column tables give no value meanings.

The old cut kept `Area = 0, Sat = 0, Cfl = 1, Flag = 0`. Of the 138 gained galaxies with a flag, 124 have only `Flag = 1` and 14 have `Sat ≥ 1` or `Area ≥ 1`.
The fits use COSMOS2025 or COSMOS2020 Classic photometry, not COSMOS2015.

Fitted photometry, C/N-free arm (plain arm in `photometry-by-cosmos2015-class.csv`; its median χ² per band agrees within 0.05):

| Photometry | Class | Fits | Median χ² per band | χ² per band > 2 | Median largest pull |
|---|---|---|---|---|---|
| COSMOS2025 | 194 | 99 | 1.66 | 25 | 3.10 |
| COSMOS2025 | gained, shallow only | 74 | 1.65 | 16 | 2.88 |
| COSMOS2025 | gained, saturation or bad area | 10 | 1.96 | 5 | 3.56 |
| COSMOS2020 Classic | 194 | 95 | 0.51 | 2 | 1.76 |
| COSMOS2020 Classic | gained, shallow only | 49 | 0.50 | 1 | 1.72 |
| COSMOS2020 Classic | gained, saturation or bad area | 4 | 0.61 | 1 | 1.93 |

Slope with and without the flagged galaxies:

| Arm | Sample | N | Slope | H(z_eff) |
|---|---|---|---|---|
| C/N-free | gained, shallow only | 123 | −5.274 (−6.046, −4.449) | 104.7 (91.4, 124.2) |
| C/N-free | gained, saturation or bad area | 14 | −4.729 (−6.857, −2.603) | 114.5 (79.0, 208.0) |
| C/N-free | combined without saturation or bad area | 333 | −5.091 (−5.583, −4.608) | 108.3 (98.8, 119.7) |
| C/N-free | combined without any COSMOS2015 flag | 210 | −4.932 (−5.541, −4.355) | 111.7 (99.5, 126.6) |
| plain | gained, shallow only | 124 | −4.776 (−5.538, −3.952) | 115.7 (99.8, 139.8) |
| plain | gained, saturation or bad area | 14 | −4.275 (−6.231, −2.367) | 126.6 (86.9, 228.8) |
| plain | combined without saturation or bad area | 334 | −4.840 (−5.342, −4.321) | 114.0 (103.3, 127.6) |
| plain | combined without any COSMOS2015 flag | 210 | −4.806 (−5.446, −4.184) | 114.7 (101.2, 131.7) |

**The 16 gained galaxies without a COSMOS2015 flag** (14 NaN σ★ error, 2 other spectrum; z 0.66–0.88) have a flat slope:
C/N-free −1.04 (−3.07, +1.08), plain −0.48 (−2.93, +1.99); 1.9σ and 1.8σ from the 194. Median age 4.49 Gyr.

**[N/Fe].** Median 0.35 against 0.24 (KS p 0.048).

## Noticed, not done

- 58 passive spectra (581 → 523) have no fittable photometry under the rule of `scripts/cosmos_photometry.py`.
- The primary-sample flag and the redshift range stay in the quality cut.
- M102_214235 has no C/N-free fit; the combined C/N-free sample is 347, the plain one 348.
- 16 gained galaxies have no HST F814W cutout; their fit notebooks (both arms) have no local figures.
