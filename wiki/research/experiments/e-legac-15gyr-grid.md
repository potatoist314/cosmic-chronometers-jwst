---
kind: experiment
id: e-legac-15gyr-grid
title: LEGA-C 60 on 15 Gyr SFH bins
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
result_groups: results/legac-break-fixed-grid-2026-11-24, results/legac-steps-control-2026-11-24, results/legac-fixed-grid-mock-2026-11-24
---

## Context

60 LEGA-C DR3 galaxies, \(z\) 0.603–0.999 (median 0.810), rest 4074.5–4666.1 Å. Their standard SFH bins end at the Planck18 Universe age, 5.85–7.89 Gyr here. Test 1: end the bins at 15 Gyr, as on SDSS, so cosmology no longer enters the fit. Test 2: add the 4000 Å break (rest from 3850.0 Å).

Planck18 Universe-age slope over these redshifts: −5.15 Gyr per unit \(z\). Universe age at \(z\) 0.810: 6.71 Gyr.

## Measurements

| SFH bins end at | Age slope (Gyr per unit \(z\)) | Ages above the Planck18 Universe age |
| --- | --- | --- |
| Planck18 Universe age | −4.92 ± 0.91 | 0 of 60 |
| 15 Gyr | −4.55 ± 2.22 | 40 of 60 |
| 15 Gyr, 4000 Å break added | −4.98 ± 2.15 | 33 of 60 |

- Median age 4.58 → 7.81 Gyr. Age takes up 0.64 of the fractional change in bin length.
- Scatter of ages about the line: 0.90 → 2.11 Gyr. Uncertainty on one galaxy's age: 0.50 → 1.33 Gyr.
- The break lowers ages by 0.36 Gyr at all \(z\) and [α/Fe] by 0.10 dex. 15 of 60 fits then sit at the lower [α/Fe] limit (3 without).

**Sampler.** The 15 Gyr fits used 33 inner steps of the nested sampler, the Planck18 fits 65. Test: refit 12 of the galaxies.

| 12 galaxies | Uncertainty on one galaxy's age, Gyr | Scatter of ages about the line, Gyr |
| --- | --- | --- |
| 15 Gyr bins, 33 steps | 1.34 | 1.88 |
| 15 Gyr bins, 33 steps, second random seed | 1.27 | 1.79 |
| 15 Gyr bins, 65 steps | 1.38 | 1.93 |
| Planck18 bins, 65 steps | 0.50 | 0.88 |

- 33 → 65 steps moves ages by −0.07 of their uncertainty (largest 0.48). A second seed moves them +0.03. The sampler does not cause the wider ages.

**Fake galaxies.** A fake galaxy is a spectrum made by the fit's own model from a known star-formation history. It takes the wavelengths, noise and masks of a real LEGA-C galaxy.

12 fakes: one 0.5 Gyr burst with true age 3, 4.5 or 6 Gyr. Two hosts, at \(z\) 0.648 and 0.852 (Universe age 7.61 and 6.50 Gyr), two noise draws each.

| 12 fake galaxies | Planck18 bins | 15 Gyr bins |
| --- | --- | --- |
| Fitted minus true age, mean, Gyr | +0.03 | +2.29 |
| Uncertainty on one galaxy's age, Gyr | 0.52 | 1.36 |
| Fitted age gap between true 3 and 6 Gyr, Gyr | 1.30 | 2.53 |
| Mass fraction put in bins older than the Universe (true: 0) | 0 | 0.19–0.61 |

- χ² per pixel is the same on both (median change +0.0002). One SFH gives the same model flux on both sets of bins: no bug.
- The prior alone gives 6.47 Gyr on 15 Gyr bins, and 3.25 and 2.78 Gyr on the two hosts' Planck18 bins.
- Real galaxies: the age rise follows the mass the Planck18 fit put in its oldest bin (rank correlation +0.89). Age order is kept (0.88).

## Results

- 15 Gyr bins leave the LEGA-C slope within errors: −4.55 ± 2.22 against Planck18 −5.15. They raise ages 3.11 Gyr and widen the uncertainty on each age 2.7 times.
- Not the sampler, not a bug: fake galaxies come out 2.29 Gyr too old with the same χ².
- Rest 4074.5–4666.1 Å does not fix how much mass formed more than about 8 Gyr ago. The bins and the prior set it.

## References

- [LEGA-C 60 fits](results/legac-break-fixed-grid-2026-11-24/t_5775081a-detail.md) · [Sampler steps](results/legac-steps-control-2026-11-24/table.md) · [Fake galaxies](results/legac-fixed-grid-mock-2026-11-24/REPORT.md)
- Roadmap: [two SFH priors, continuity and SFMS](https://wiki.eclw.org/p/p-bc6aadf5-1337-49f4-b09c-8485c7ad60df/) · [finer SFH bins](https://wiki.eclw.org/p/p-0b2aceaa-550e-41c9-878b-8987bc2f126c/) · [more SFH bins](https://wiki.eclw.org/p/p-8285edc7-06b5-4e1f-aad9-b75c63ba4200/)

## Before delegation

```json
[
  {
    "date": "2026-11-24",
    "text": "Could it be the updated sampler settings?"
  }
]
```

## Your interpretation

```json
[
  {
    "date": "2026-11-24",
    "text": "median age is 7.8gyr in a 7 gyr universe? uhh..."
  },
  {
    "date": "2026-11-24",
    "text": "I don't understand the fake galaxy, so that is something you've cooked up."
  },
  {
    "date": "2026-11-24",
    "text": "Okay, bins and prior can be controlled. Very good. I was going to ask for a prior, wasn't I? Have I mentioned this?"
  }
]
```
