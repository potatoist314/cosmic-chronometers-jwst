---
title: COSMOS2020 and COSMOS2025 photometry against COSMOS2015
date: 2026-09-21
section: Analyses
theme: Sample and data
tags: [dr2-quiescent-sample, ceridwen, photometry, cosmos2020, cosmos2025]
figures: [cosmos-photometry-M1_210210.png]
---

Sample
: 187 fitted DR2 quiescent galaxies; M1_210210, \(z=0.6542\)
Present fit input
: COSMOS2015 `cosmos_total`, Laigle et al. (2016), 12 bands
COSMOS2020
: Weaver et al. (2022); VizieR `J/ApJS/258/11`, Classic and Farmer
COSMOS2025
: Shuntov et al. (2025), COSMOS-Web DR1; VizieR `J/A+A/704/A339/phot`
Match
: nearest source within \(1''\)
Download
: `scripts/download_cosmos2020_cosmos2025_legac_dr2_photometry.py`
Tables
: `scripts/compare_cosmos_photometry.py`
Plot
: `scripts/plot_cosmos_photometry_comparison.py` → `wiki/analyses/cosmos-photometry-comparison/`

<figure>
<img src="figures/cosmos-photometry-comparison/cosmos-photometry-M1_210210.png" alt="M1_210210 total fluxes from COSMOS2015, COSMOS2020 Classic and COSMOS2025 against observed and rest-frame wavelength, with flux-ratio and error-ratio panels">
<figcaption><code>cosmos-photometry-M1_210210.png</code> · M1_210210 total fluxes from COSMOS2015, COSMOS2020 Classic and COSMOS2025: rest-frame UV (linear), full SED (log), \(F/F_{2015}\) with sample median and 16–84% range, \(\sigma/\sigma_{2015}\); grey band \(\pm5\%\) error floor; COSMOS2020 Farmer has no photometry, model did not converge</figcaption>
</figure>

## Match of the 187 fitted galaxies

| catalogue | matched | median separation [arcsec] | maximum separation [arcsec] |
| --- | --- | --- | --- |
| COSMOS2015 | 187 | 0.048 | 0.711 |
| COSMOS2020 Classic | 186; none for M1_139423 | 0.120 | 0.386 |
| COSMOS2020 Farmer | 165; 145 with `FModel == 0` | 0.128 | 0.384 |
| COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 0.123 | 0.290 |

<details open>
<summary>M1_210210 per band</summary>

| band | \(\lambda_\mathrm{obs}\) [\(\mu\)m] | `sedpy_jax` filter | COSMOS2015 [\(\mu\)Jy] | Classic [\(\mu\)Jy] | COSMOS2025 [\(\mu\)Jy] | \(F/F_{2015}\) Classic | \(\sigma/\sigma_{2015}\) Classic | \(F/F_{2015}\) 2025 | \(\sigma/\sigma_{2015}\) 2025 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NUV | 0.231 | `galex_NUV` |  | 0.056 ± 0.075 |  |  |  |  |  |
| u | 0.371 | none |  | 0.415 ± 0.018 |  |  |  |  |  |
| u* | 0.386 | `cfht_megacam_us_9301` | 0.531 ± 0.049 | 0.440 ± 0.010 | 0.355 ± 0.046 | 0.83 | 0.21 | 0.67 | 0.95 |
| IB427 | 0.427 | `subaru_suprimecam_ia427` |  | 0.719 ± 0.094 | 0.608 ± 0.188 |  |  |  |  |
| B | 0.449 | `subaru_suprimecam_B` | 1.393 ± 0.050 | 1.319 ± 0.019 |  | 0.95 | 0.39 |  |  |
| IB464 | 0.464 | `subaru_suprimecam_ia464` |  | 1.192 ± 0.151 |  |  |  |  |  |
| g | 0.485 | `hsc_g` |  | 2.492 ± 0.027 | 2.475 ± 0.033 |  |  |  |  |
| IA484 | 0.485 | `subaru_suprimecam_ia484` |  | 2.543 ± 0.059 | 2.350 ± 0.078 |  |  |  |  |
| V | 0.549 | `subaru_suprimecam_V` | 5.798 ± 0.129 | 5.554 ± 0.055 |  | 0.96 | 0.43 |  |  |
| r | 0.622 | `hsc_r` |  | 11.08 ± 0.05 | 11.59 ± 0.05 |  |  |  |  |
| r+ | 0.630 | `subaru_suprimecam_rp` | 12.79 ± 0.15 | 12.17 ± 0.04 |  | 0.95 | 0.25 |  |  |
| i+ | 0.769 | `subaru_suprimecam_ip` | 35.39 ± 0.20 | 33.32 ± 0.05 |  | 0.94 | 0.23 |  |  |
| i | 0.770 | `hsc_i` |  | 33.66 ± 0.08 | 35.70 ± 0.09 |  |  |  |  |
| F814W | 0.806 | `acs_wfc_f814w` |  |  | 35.75 ± 0.12 |  |  |  |  |
| z | 0.889 | `hsc_z` |  | 49.71 ± 0.12 | 51.33 ± 0.12 |  |  |  |  |
| z++ | 0.905 | `subaru_suprimecam_zp` | 55.53 ± 0.10 | 53.37 ± 0.07 |  | 0.96 | 0.65 |  |  |
| y | 0.976 | `hsc_y` |  | 61.20 ± 0.15 | 65.19 ± 0.19 |  |  |  |  |
| Y | 1.022 | `vista_vircam_Y` | 68.55 ± 0.11 | 66.11 ± 0.04 | 66.84 ± 0.23 | 0.96 | 0.39 | 0.97 | 2.04 |
| F115W | 1.154 | `jwst_f115w` |  |  | 73.98 ± 0.18 |  |  |  |  |
| J | 1.252 | `vista_vircam_J` | 95.93 ± 0.17 | 92.81 ± 0.05 | 87.49 ± 0.19 | 0.97 | 0.32 | 0.91 | 1.14 |
| F150W | 1.501 | `jwst_f150w` |  |  | 106.3 ± 0.1 |  |  |  |  |
| H | 1.647 | `vista_vircam_H` | 137.3 ± 0.2 | 134.5 ± 0.1 | 123.1 ± 0.2 | 0.98 | 0.32 | 0.90 | 0.86 |
| Ks | 2.156 | `vista_vircam_Ks` | 173.1 ± 0.2 | 171.1 ± 0.1 | 164.5 ± 0.3 | 0.99 | 0.50 | 0.95 | 1.18 |
| F277W | 2.762 | `jwst_f277w` |  |  | 173.8 ± 0.1 |  |  |  |  |
| ch1 | 3.569 | `spitzer_irac_ch1` | 146.2 ± 0.7 | 150.4 ± 0.4 | 120.9 ± 0.6 | 1.03 | 0.62 | 0.83 | 0.96 |
| F444W | 4.404 | `jwst_f444w` |  |  | 92.99 ± 0.07 |  |  |  |  |
| ch2 | 4.507 | `spitzer_irac_ch2` | 100.6 ± 0.3 | 103.4 ± 0.2 | 78.38 ± 0.32 | 1.03 | 0.50 | 0.78 | 0.93 |

</details>

<details>
<summary>Total-flux corrections</summary>

| catalogue | flux used | aperture-to-total | Milky Way extinction | zero-point offset |
| --- | --- | --- | --- | --- |
| COSMOS2015 | \(3''\) aperture | Per-object `Offset`; IRAC already total | \(E(B-V)\,F\), Laigle et al. (2016) Table 3 | Laigle et al. (2016) Table 3 \(s_f\), subtracted |
| COSMOS2020 Classic | \(2''\) aperture | Per-object `totaloff2`; IRAC (IRACLEAN) and GALEX already total | Not in catalogue; applied with the same \(F\) | Weaver et al. (2022) Table 3, LePhare/Classic column, added |
| COSMOS2020 Farmer | Total model flux | None | Not in catalogue; applied with the same \(F\) | Weaver et al. (2022) Table 3, LePhare/Farmer column, added |
| COSMOS2025 | Total SE++ model flux, calibrated error `e_Flux-c-mod` | None | No \(E(B-V)\) column; value taken from COSMOS2020 Classic | None tabulated in Shuntov et al. (2025); none applied |

</details>

<details>
<summary>Sample flux and error ratios against COSMOS2015</summary>

| band | catalogue | N | median \(F/F_{2015}\) | 16–84% | median \(\sigma/\sigma_{2015}\) |
| --- | --- | --- | --- | --- | --- |
| u* | Classic | 186 | 0.85 | 0.72–0.99 | 0.21 |
| u* | Farmer | 138 | 0.75 | 0.52–0.91 | 0.13 |
| B | Classic | 186 | 0.92 | 0.85–0.98 | 0.43 |
| V | Classic | 186 | 0.95 | 0.89–0.98 | 0.45 |
| r+ | Classic | 186 | 0.95 | 0.92–0.98 | 0.29 |
| i+ | Classic | 186 | 0.95 | 0.93–0.98 | 0.31 |
| z++ | Classic | 186 | 0.97 | 0.95–1.00 | 0.65 |
| Y | Classic | 186 | 0.97 | 0.95–1.00 | 0.40 |
| Y | Farmer | 140 | 0.96 | 0.79–1.01 | 0.13 |
| J | Classic | 186 | 0.97 | 0.96–1.00 | 0.33 |
| J | Farmer | 140 | 0.97 | 0.79–1.01 | 0.11 |
| H | Classic | 186 | 0.99 | 0.97–1.01 | 0.32 |
| H | Farmer | 140 | 0.99 | 0.82–1.03 | 0.10 |
| Ks | Classic | 186 | 0.99 | 0.97–1.02 | 0.48 |
| Ks | Farmer | 141 | 1.00 | 0.82–1.03 | 0.14 |
| ch1 | Classic | 185 | 1.07 | 1.03–1.11 | 0.46 |
| ch1 | Farmer | 131 | 1.08 | 0.73–1.17 | 0.06 |
| ch2 | Classic | 181 | 1.08 | 1.02–1.13 | 0.47 |
| ch2 | Farmer | 140 | 1.08 | 0.87–1.16 | 0.10 |
| u* | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 0.72 | 0.54–0.96 | 0.87 |
| Y | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 1.07 | 0.99–1.16 | 1.20 |
| J | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 1.00 | 0.93–1.10 | 0.71 |
| H | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 0.99 | 0.92–1.08 | 0.56 |
| Ks | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 1.04 | 0.97–1.14 | 0.78 |
| ch1 | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 0.90 | 0.81–1.01 | 1.45 |
| ch2 | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 0.88 | 0.81–0.96 | 1.15 |

</details>

<details>
<summary>Rest-frame UV signal-to-noise across the sample</summary>

| band | catalogue | N | median \(F/\sigma\) |
| --- | --- | --- | --- |
| u | Classic | 186 | 12.2 |
| u | Farmer | 138 | 20.6 |
| u* | COSMOS2015 | 187 | 5.4 |
| u* | Classic | 186 | 21.0 |
| u* | Farmer | 138 | 24.9 |
| IB427 | Classic | 186 | 3.8 |
| IB427 | Farmer | 142 | 11.1 |
| B | COSMOS2015 | 187 | 14.0 |
| B | Classic | 186 | 29.6 |
| u* | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 4.7 |
| IB427 | COSMOS2025 | 122; COSMOS-Web footprint, 0.54 deg\(^2\) | 1.5 |
| NUV | Classic | 72 | 1.0 |
| NUV | Farmer | 57 | 1.0 |

</details>

<details open>
<summary>Fit notebook changes</summary>

- In `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: new `CERIDWEN_PHOTOMETRY` value per catalogue beside `cosmos_total`; `BANDS` map and input file per catalogue.
- Total-flux recipes above replace `Offset`, `COSMOS2015_SF` and `COSMOS2015_EXTINCTION`.
- COSMOS2020 fluxes from magnitude columns; VizieR rounds flux columns to \(0.01\,\mu\mathrm{Jy}\).
- Replace `Area`/`Sat`/`Cfl`/`Flag` cuts with `FlagCOMBINED == 0` (Classic), `FModel == 0` (Farmer), `warn-flag == 0` (COSMOS2025).
- CFHT \(u\) (\(0.371\,\mu\mathrm{m}\)) has no curve in `sedpy_jax`; `cfht_megacam_us_9301` is the \(u^*\) curve. Every other band has a curve.
- Coverage: Classic 186 of 187; Farmer 165 matched, 145 with a converged model; COSMOS2025 122 of 187.
- M1_210210 catalogue errors exceed 5% only in COSMOS2015 \(u^*\); Classic NUV, IB427, IB464; COSMOS2025 \(u^*\), IB427.
- The 5% floor sets the M1_210210 error in every other band.

</details>
