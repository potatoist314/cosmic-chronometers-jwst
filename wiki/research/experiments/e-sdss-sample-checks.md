---
kind: experiment
id: e-sdss-sample-checks
title: SDSS 50 sample checks on the age slope
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
---

## Context

50 SDSS fits: Na D masked, rest 3604.0–7079.3 Å, SFH bins ending at 15 Gyr. Age slope −10.0 ± 2.9 Gyr per unit \(z\), Planck18 Universe age −11.4. Test: which galaxy properties besides age change with \(z\) here? No new fits: stored posteriors and SDSS catalogues only.

Slopes in Gyr per unit \(z\), ± bootstrap standard deviation.

## Measurements

| Fit, galaxy properties | Galaxies | Age slope |
| --- | --- | --- |
| Age against \(z\) only | 50 | −10.0 ± 2.9 |
| Velocity dispersion and stellar mass also in the line | 50 | −12.5 ± 2.4 |
| Same velocity-dispersion mix in every \(z\) bin | 36 | −9.7 ± 3.6 |
| Galaxies with over 5 % of their mass formed in the last 2 Gyr removed | 34 | −7.0 ± 3.0 |

- Recent star formation: no galaxy formed more than 1.4 % of its mass in the last 1 Gyr. 16 formed over 5 % in the last 2 Gyr, more of them at higher \(z\). A constant rate over 15 Gyr gives 13.3 %.

**What else changes with \(z\).** Medians in the lowest and highest of four \(z\) bins.

| Quantity | \(z\) 0.05–0.12 | \(z\) 0.24–0.30 |
| --- | --- | --- |
| Median signal-to-noise per pixel, r band | 50 | 24 |
| Fibre radius / galaxy half-light radius | 0.30 | 0.66 |
| Share of the galaxy's r-band light inside the fibre | 0.25 | 0.44 |

- All three track \(z\). With 50 galaxies, the fit cannot separate their effect on age from a \(z\) trend.
- The telluric mask cuts into a TiO or Na D band only at \(z \ge 0.214\) (16 galaxies). Two spectra start at rest 3693 and 4030 Å instead of 3604 Å.

## Results

- Velocity dispersion and mass do not explain the slope (−12.5 ± 2.4 with both in the line).
- Without the 16 galaxies that formed over 5 % of their mass in the last 2 Gyr, the slope is −7.0 ± 3.0.
- S/N, fibre coverage and fibre light share track \(z\). This sample cannot separate their effect from a \(z\) trend.

## References

- [Na D-masked fits](results/sdss-mask-nad-2026-11-24/experiment.json) · [SDSS 50 fits](results/sdss-50-2026-11-24/t_481e53cf-detail.md)

## Before delegation

```json
[
  {
    "date": "2026-11-24",
    "text": "is anything unaddressed for sdss"
  }
]
```
