---
kind: question
id: q-spectral-range
title: Rest-frame spectral range and age slopes
date: 2026-11-24
origin: new
status: open
---

## Context

### Answer

- **Age slope:** mass-weighted age against redshift, in Gyr per unit \(z\). Planck18 Universe-age slope: −5.23 over the LEGA-C 348, −11.4 over the SDSS 50.
- **SFH bins:** about half of the narrow-window SDSS slope comes from SFH bins that end at the Planck18 Universe age ([bins and prior](wiki/research/experiments/e-sfh-grid-prior.md)).
- **SDSS, wide spectrum, bins to 15 Gyr:** −11.9 ± 3.3. With Na D masked, −10.0 ± 2.9, and 1 of 50 ages above the Universe age ([wide range](wiki/research/experiments/e-sdss-wide-range.md), [Na D](wiki/research/experiments/e-sdss-nad-mask.md), [sample checks](wiki/research/experiments/e-sdss-sample-checks.md)).
- **LEGA-C, bins to 15 Gyr:** slope unchanged within errors. Ages 3.1 Gyr older, 40 of 60 above the Universe age ([15 Gyr bins](wiki/research/experiments/e-legac-15gyr-grid.md), [full spectrum](wiki/research/experiments/e-legac-full-range.md)).
- **Fake galaxies:** model spectra of known age, on real LEGA-C wavelengths and noise. On 15 Gyr bins they come out 2.3 Gyr too old. The LEGA-C window does not fix mass formed more than about 8 Gyr ago.
- **Model:** the LEGA-C window lies wholly below 4728 Å, where Park et al. 2025 state no line-list tuning ([model limits](wiki/research/experiments/e-park2025-model-limits.md)).

### Spectral range

DR3 is the current LEGA-C sample: 4,057 spectra narrow to 371 covering 4074.5–4666.1 Å and 348 fitted per `OBJECT`. The 10 Nov DR2 set (1,988 spectra, 187 quiescent, 135 fitted) only chose that window.

| Set of fits | Galaxies | Rest range (Å) |
| --- | --- | --- |
| LEGA-C DR3 | 348 | 4074.5–4666.1 |
| LEGA-C DR2 standard | 135 | per galaxy, from 3011.6–4155.0 to 4206.7–5691.2 |
| SDSS until 24 Nov | 50 | 4074.5–4666.1 |
| SDSS wide | 50 | 3604.0–7079.3 |

### Age slopes

Errors: ± bootstrap standard deviation. LEGA-C DR3: 16–84 % range.

| Fits | Age slope (Gyr per unit \(z\)) | Planck18 Universe-age slope |
| --- | --- | --- |
| LEGA-C DR3 348, window, bins to the Universe age | −4.77 (−5.26 to −4.28) | −5.23 |
| LEGA-C 60, window, bins to 15 Gyr | −4.55 ± 2.22 | −5.15 |
| SDSS 50, window, bins to the Universe age | −12.1 ± 0.9 | −11.4 |
| SDSS 50, wide, bins to 15 Gyr, Na D masked | −10.0 ± 2.9 | −11.4 |

- LEGA-C DR2: −3.26 on rest 4155.0–4438.1 Å (130 galaxies), −4.60 on 4074.5–4666.1 Å (110).

## Your words

```json
[
  {
    "date": "2026-11-24",
    "text": "bruh, bit stupid to not widen it. lega c is so narrow, jeez? does most of lega cs age come from prior then"
  },
  {
    "date": "2026-11-24",
    "text": "uhh, lega c has 300+ galaxies. okay, i didn't realise how badly controlled the spectral part of the fitting is. this has to go on the wiki"
  }
]
```

## References

- [DR3 348](results/dr3-more-galaxies-2026-11-16/REPORT.md), [DR2 windows](results/chronometer-135-2026-11-10/REPORT.md) ([ranges](results/chronometer-135-2026-11-10/per-fit.csv)), [DR2 README](data/raw/legac_dr2/README.md), [targets](results/dr2-refit-2026-10-12/targets.json), [SDSS 50](results/sdss-50-2026-11-24/t_481e53cf-detail.md), [SDSS prior](results/sdss-prior-cosmology-2026-11-24/t_ab1e0a67-detail.md).
- Roadmap: [two SFH priors, continuity and SFMS](https://wiki.eclw.org/p/p-bc6aadf5-1337-49f4-b09c-8485c7ad60df/) · [finer SFH bins](https://wiki.eclw.org/p/p-0b2aceaa-550e-41c9-878b-8987bc2f126c/) · [more SFH bins](https://wiki.eclw.org/p/p-8285edc7-06b5-4e1f-aad9-b75c63ba4200/)

## Decisions

```json
[]
```
