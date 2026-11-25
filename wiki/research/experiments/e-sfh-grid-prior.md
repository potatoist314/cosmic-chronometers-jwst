---
kind: experiment
id: e-sfh-grid-prior
title: How much of the fitted age comes from the SFH bins and prior
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
result_groups: results/sdss-prior-cosmology-2026-11-24, results/legac-prior-cosmology-2026-11-24, results/sdss-50-2026-11-24
---

## Context

Each fit splits the star-formation history (SFH) into 14 time bins. The bins run from now back to the Planck18 Universe age at the galaxy's redshift, \(t_U\). A continuity prior (Student-t, scale 0.3) favours similar star-formation rates in neighbouring bins. Cosmology enters a fit only through these bin edges.

- Test 1: refit with SFH bins built for other Hubble constants.
- Test 2: refit with one set of bins for every galaxy.

If the spectrum fixed the age, the age would not move.

Slopes in Gyr per unit \(z\), ± bootstrap standard deviation.

## Measurements

| SDSS 50, rest 4074.5–4666.1 Å: SFH bins end at | Age slope | Slope of the bin end against \(z\) |
| --- | --- | --- |
| Planck18 \(t_U\) (\(H_0 = 67.66\)) | −12.1 ± 0.9 | −11.4 |
| \(t_U\) for \(H_0 = 50\) | −15.9 ± 1.1 | −15.4 |
| \(t_U\) for \(H_0 = 90\) | −11.5 ± 0.9 | −8.6 |
| 13.50 Gyr for every galaxy | −6.2 ± 1.0 | 0 |

- About half of the narrow-window SDSS slope follows the bins. With one set of bins the slope halves.

**Response of the age to the bins.** 1: the bins alone set the age. 0: the spectrum sets it.

| Quantity | SDSS, 50 | LEGA-C, 10 |
| --- | --- | --- |
| Fractional age change per fractional change of \(t_U\) | 0.79 (0.70–0.88) | 0.69 (0.51–0.87) |
| Median age as a fraction of \(t_U\) | 0.73 | 0.64 |
| Same, prior alone (no data) | 0.43 | 0.43 |

- LEGA-C prior alone: response 1.01. SDSS prior alone: slope −5.0.
- LEGA-C fits use about 40 % of the pixels each spectrum has (1391–1563 of 3451–3807).

**Age against metallicity.** An older age can trade against a lower [Fe/H]. Test: is that what leaves the age loose? Uncertainty on one galaxy's age: half the 16–84 % range of its posterior.

| Quantity | SDSS, 50 | LEGA-C DR3, 348 |
| --- | --- | --- |
| Uncertainty on one galaxy's age, fit (prior alone), Gyr | 1.02 (3.04) | 0.51 (1.89) |
| [Fe/H] uncertainty, dex (prior alone 1.02) | 0.10 | 0.08 |
| Correlation of age and [Fe/H] within one fit, median | −0.56 | −0.52 |

- The correlation is negative in all 498 fits. Knowing [Fe/H] exactly would shrink the SDSS age uncertainty only to 0.83 of its value.
- [Fe/H] moves −0.21 dex per unit ln age. The 3/2 law gives −0.27 (Trager et al. 2000, AJ 119, 1645).

## Results

- Ages follow the SFH bins: 0.79 of a bin change on SDSS, 0.69 on LEGA-C.
- Metallicity does not leave ages loose. The fits measure [Fe/H] to 0.1 dex, and fixing it would narrow the age by only 17 %.

## References

- [SDSS bins and prior](results/sdss-prior-cosmology-2026-11-24/t_ab1e0a67-detail.md) · [LEGA-C bins and prior](results/legac-prior-cosmology-2026-11-24/t_93f88c29-detail.md) · [SDSS 50 fits](results/sdss-50-2026-11-24/t_481e53cf-detail.md) · [LEGA-C DR3 348](results/dr3-more-galaxies-2026-11-16/REPORT.md)

## Before delegation

```json
[
  {
    "date": "2026-11-24",
    "text": "bruh, bit stupid to not widen it. lega c is so narrow, jeez? does most of lega cs age come from prior then"
  },
  {
    "date": "2026-11-24",
    "text": "so it seems like we don't strongly constrain age metallicity? is that right?"
  }
]
```
