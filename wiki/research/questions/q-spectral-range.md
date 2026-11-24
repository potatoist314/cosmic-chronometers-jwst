---
kind: question
id: q-spectral-range
title: Rest-frame spectral range and age slopes
date: 2026-11-24
origin: new
status: open
---

## Context

DR3 is the current LEGA-C sample: 4,057 spectra narrow to 371 covering 4074.5–4666.1 Å and 348 fitted per `OBJECT`. The 10 Nov DR2 set (1,988 spectra, 187 quiescent, 135 fitted) only chose that window.

Standard DR2 fits span 3011.6–4155.0 to 4206.7–5691.2 Å (`per-fit.csv`, `a_baseline`). SDSS 50 fits inherit 4074.5–4666.1 Å despite wider spectra.

| Set of fits | Galaxies | Rest range (Å) | Age slope (Gyr/\(z\)) |
| --- | --- | --- | --- |
| LEGA-C DR3 current, C/N free | 347 | 4074.5–4666.1 | −5.011 (−5.481, −4.533) |
| LEGA-C DR3 current, plain | 348 | 4074.5–4666.1 | −4.766 (−5.258, −4.281) |
| LEGA-C DR2 strict window (h / e) | 130 (129/135 cover) | 4155.0–4438.1 | −3.26 plain, −3.77 arm (e) |
| LEGA-C DR2 chosen window (i / j) | 110 | 4074.5–4666.1 | −4.60 plain, −5.37 C/N free |
| SDSS DR17, C/N free | 50 | 4074.5–4666.1 | −12.1 \(\pm\) 0.9 |

Cosmology enters only through SFH bin edges to \(t_U\). Prior-only age is \(0.43\,t_U\), and SDSS follows \(\mathrm{d}\ln\mathrm{age}/\mathrm{d}\ln t_U = 0.79\).

| SDSS 50 SFH-grid cosmology (4074.5–4666.1 Å) | \(t_U\) slope (Gyr/\(z\)) | Age slope (Gyr/\(z\)) | Median age/\(t_U\) |
| --- | --- | --- | --- |
| Planck18 (\(H_0 = 67.66\)) | −11.4 | −12.1 \(\pm\) 0.9 | 0.732 |
| \(H_0 = 50\) | −15.4 | −15.9 \(\pm\) 1.1 | 0.695 |
| \(H_0 = 90\) | −8.6 | −11.5 \(\pm\) 0.9 | 0.768 |
| One common SFH grid | — | −6.2 \(\pm\) 1.0 | — |
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

- [DR3 348](results/dr3-more-galaxies-2026-11-16/REPORT.md), [DR2 windows](results/chronometer-135-2026-11-10/REPORT.md) ([ranges](results/chronometer-135-2026-11-10/per-fit.csv)), [DR2 README](data/raw/legac_dr2/README.md), [targets](results/dr2-refit-2026-10-12/targets.json), [SDSS 50](results/sdss-50-2026-11-24/t_481e53cf-detail.md), [SDSS prior](results/sdss-prior-cosmology-2026-11-24/t_ab1e0a67-detail.md).

## Decisions

```json
[]
```
