---
kind: experiment
id: e-sdss-nad-mask
title: SDSS 50 with Na D masked
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
result_groups: results/sdss-mask-nad-2026-11-24
---

## Context

Na D was the worst-fitted band of the wide SDSS fits (χ² per pixel 3.28). The model has no free sodium abundance. Test: remove the Na D band and refit. Same 50 galaxies, rest 3604.0–7079.3 Å, SFH bins ending at 15 Gyr.

- Band: Lick Na D passband 5876.875–5909.375 Å, air (Trager et al. 1998, ApJS 116, 1, Table 2). In vacuum: 5878.50–5911.01 Å. 1142 pixels over the 50 fits.
- Before the mask, the data are deeper than the model at Na D in 49 of 49 galaxies. Extra absorption: 0.89 Å, 2.8 % of the model flux.

## Measurements

| Quantity | Na D fitted | Na D masked |
| --- | --- | --- |
| Age slope, Gyr per unit \(z\) (Planck18 Universe age −11.4) | −11.9 ± 3.3 | −10.0 ± 2.9 |
| Scatter of ages about the line, Gyr | 1.60 | 1.32 |
| Ages above the Planck18 Universe age | 11 | 1 |
| Fits with more than 90 % of their mass in the oldest bin | 5 | 0 |

- All 49 galaxies that lose pixels get younger: median −1.09 Gyr. [Fe/H] changes by −0.09 dex, [α/Fe] by +0.09.
- \(H_0\) from the slope: 77.5 (60.1 to 108.8) km/s/Mpc. Unmasked: 65.6.

**Median age per redshift bin, Na D masked.**

| \(z\) (galaxies) | Planck18 Universe age, Gyr | Median fitted age, Gyr |
| --- | --- | --- |
| 0.05–0.12 (15) | 12.78 | 9.86 |
| 0.12–0.18 (14) | 11.78 | 9.77 |
| 0.18–0.24 (9) | 11.17 | 9.19 |
| 0.24–0.30 (12) | 10.69 | 8.10 |

## Results

- The model's Na D is too weak in every galaxy, and fitting it pushed ages older. Masked, ages fall 1.09 Gyr. Only 1 of 50 stays above the Universe age.
- Slope −10.0 ± 2.9 against Planck18 −11.4.

## References

- [Configuration](results/sdss-mask-nad-2026-11-24/experiment.json) · [Wide-range fits](results/sdss-wide-range-2026-11-24/t_0c96cd9b-detail.md)

## Before delegation

```json
[
  {
    "date": "2026-11-24",
    "text": "okay, mask na d"
  }
]
```
