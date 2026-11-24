---
kind: question
id: q-spectral-range
title: Rest-frame spectral range and age slopes
date: 2026-11-24
origin: new
status: open
---

## Context

LEGA-C DR2 holds 1,988 spectra of 1,922 galaxies (`data/raw/legac_dr2/legaCdr2.fits.gz`): 609 NUVrJ quiescent spectra, 187 clean quiescent galaxies (180 fittable, 135 fitted in Oct, `targets.json`). DR3 holds 4,081 spectra of 3,741 galaxies (`data/raw/legac_dr3/legac_DR3.fits`): 302 clean quiescent, 194 window-fitted (`selection-counts.csv`), 333 clean under relaxed cuts (`estimators.csv`).

Standard DR2 fits span 3011.6–4155.0 Å blue to 4206.7–5691.2 Å red (`per-fit.csv`, median 3701.3–5110.4 Å). The 50 SDSS spectra cover 4029.9–7079.4 Å in common (2923.5–8718.8 Å full range, `data/processed/sdss_dr17/`), yet inherit 4074.5–4666.1 Å.

| Fit set | \(N\) | \(z\) | Rest range (Å) | Features / coverage | Age slope (Gyr/\(z\)) | \(t_U\) slope (Gyr/\(z\)) |
| --- | --- | --- | --- | --- | --- | --- |
| LEGA-C DR2 full, plain (a) | 135 | 0.603–0.987 | 3011.6–4155.0 to 4206.7–5691.2 | Mg b in 61/135 | −1.55 (−2.23 to −0.88) | −5.17 |
| LEGA-C DR2 full, C/N free (b) | 135 | 0.603–0.987 | 3011.6–4155.0 to 4206.7–5691.2 | Mg b in 61/135 | +0.97 (+0.20 to +1.75) | −5.17 |
| LEGA-C DR2 strict window, plain (h) | 130 | 0.603–0.987 | 4155.0–4438.1 | 129/135 cover: \(\mathrm{H}\gamma_A\), Ca4227, G4300, Fe4383 | −3.26 (−3.91 to −2.62) | −5.19 |
| LEGA-C DR2 strict window, C/N free, \([\alpha/\mathrm{Fe}]=+0.25\) (e) | 130 | 0.603–0.987 | 4155.0–4438.1 | 129/135 cover: same 4 features | −3.77 (−4.42 to −3.09) | −5.19 |
| LEGA-C DR2 window, plain (i) | 110 | 0.603–0.984 | 4074.5–4666.1 | 110/135 cover: \(\mathrm{H}\delta_A\), \(\mathrm{H}\gamma_A\), Ca4227, Ca4455, CN4150, G4300, Fe4383, Fe4531 | −4.60 (−5.56 to −3.60) | −5.31 |
| LEGA-C DR2 window, C/N free (j) | 110 | 0.603–0.984 | 4074.5–4666.1 | 110/135 cover: same 8 features | −5.37 (−6.29 to −4.41) | −5.31 |
| LEGA-C DR3 window, C/N free | 194 | 0.603–0.999 | 4074.5–4666.1 | Same 8 features (plain −5.04) | −5.15 (−5.78 to −4.53) | −5.23 |
| SDSS DR17, C/N free | 50 | 0.054–0.300 | 4074.5–4666.1 | Same 8 features; 539–546 of 2901–3844 valid px | −12.1 \(\pm\) 0.9 | −11.4 |

Cosmology enters the SFH prior only through the 14 bin edges, ending at \(t_U\). Prior-only median age equals \(0.43\,t_U\). Per galaxy, SDSS ages shift at \(\mathrm{d}\ln\mathrm{age}/\mathrm{d}\ln t_U = 0.79\).

| SDSS 50 SFH-grid cosmology (4074.5–4666.1 Å) | \(t_U\) slope (Gyr/\(z\)) | Age slope (Gyr/\(z\)) | Median age/\(t_U\) |
| --- | --- | --- | --- |
| Planck18 (\(H_0 = 67.66\)) | −11.4 | −12.1 \(\pm\) 0.9 | 0.732 |
| \(H_0 = 50\) | −15.4 | −15.9 \(\pm\) 1.1 | 0.695 |
| \(H_0 = 90\) | −8.6 | −11.5 \(\pm\) 0.9 | 0.768 |
| One common SFH grid (fixed \(t_U\)) | 0 | −6.2 \(\pm\) 1.0 | — |
| Prior only (Planck18) | −11.4 | −5.0 | 0.431 |

## Your words

```json
[
  {
    "date": "2026-11-24",
    "text": "uhh, lega c has 300+ galaxies. okay, i didn't realise how badly controlled the spectral part of the fitting is. this has to go on the wiki"
  }
]
```

## References

- [DR2 chronometer & rest-frame windows](results/chronometer-135-2026-11-10/REPORT.md) ([per-fit ranges](results/chronometer-135-2026-11-10/per-fit.csv)), [DR2 targets](results/dr2-refit-2026-10-12/targets.json), [DR3 selection & fits](results/legac-dr3-2026-11-11/REPORT.md) ([counts](results/legac-dr3-2026-11-11/selection-counts.csv)), [DR3 extended sample](results/sigma-split-2026-11-16/more-galaxies-2026-11-17/estimators.csv), [SDSS 50 fits](results/sdss-50-2026-11-24/t_481e53cf-detail.md), [SDSS SFH-grid cosmology](results/sdss-prior-cosmology-2026-11-24/t_ab1e0a67-detail.md).

## Decisions

```json
[]
```
