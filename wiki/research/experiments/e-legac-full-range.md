---
kind: experiment
id: e-legac-full-range
title: LEGA-C 36 on the full spectrum and on 10 Gyr SFH bins
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
result_groups: results/legac-full-range-test-2026-11-24
---

## Context

On 15 Gyr SFH bins the LEGA-C window leaves ages loose ([15 Gyr bins](wiki/research/experiments/e-legac-15gyr-grid.md)). Two tests on 36 of those galaxies, 9 per 0.1 in \(z\), \(z\) 0.608–0.999 (median 0.810):

- More spectrum: fit every valid pixel, rest 3364.1–5361.8 Å at the extremes. Median 3604 pixels, against 1541 in the window (4074.5–4666.1 Å).
- Shorter bins: end the SFH bins at 10 Gyr instead of 15 Gyr, the same for every galaxy.

Planck18 Universe-age slope over these redshifts: −5.12 Gyr per unit \(z\). Universe age at \(z\) 0.810: 6.71 Gyr.

## Measurements

| Real galaxies: spectrum, SFH bins end at | Age slope (Gyr per unit \(z\)) | Median age, Gyr |
| --- | --- | --- |
| Window, 15 Gyr | −2.36 ± 2.96 | 8.01 |
| Full spectrum, 15 Gyr | −4.74 ± 1.97 | 4.77 |
| Window, 10 Gyr | −1.74 ± 1.84 | 6.10 |
| Full spectrum, 10 Gyr | −3.25 ± 1.41 | 4.44 |

| Real galaxies: spectrum, SFH bins end at | Uncertainty on one galaxy's age, Gyr | Ages above the Planck18 Universe age |
| --- | --- | --- |
| Window, 15 Gyr | 1.34 | 27 of 36 |
| Full spectrum, 15 Gyr | 0.92 | 6 of 36 |
| Window, 10 Gyr | 0.80 | 10 of 36 |
| Full spectrum, 10 Gyr | 0.61 | 2 of 36 |

- Full spectrum: 15 fits put [α/Fe] at its lower prior limit (median −0.09, window +0.13). 18 put a nuisance parameter at its upper limit. 29 of 36 have some parameter at a limit (window: 18).

**Fake galaxies**, the 12 of [15 Gyr bins](wiki/research/experiments/e-legac-15gyr-grid.md): model spectra of known age on real LEGA-C wavelengths and noise. On Planck18 bins the true 3 Gyr gap comes out as 1.30 Gyr, mean error +0.03.

| Fake galaxies: spectrum, SFH bins end at | Fitted age gap between true 3 and 6 Gyr, Gyr | Fitted minus true age, mean, Gyr |
| --- | --- | --- |
| Window, 15 Gyr | 2.53 | +2.29 |
| Full spectrum, 15 Gyr | 2.64 | +2.34 |
| Window, 10 Gyr | 1.73 | +1.03 |
| Full spectrum, 10 Gyr | 1.91 | +1.12 |

## Results

- Full spectrum, real galaxies: ages fall 2.56 Gyr (median) and the slope moves to −4.74 ± 1.97. Fake galaxies do not show this fall (+0.05 Gyr). Their 2.3 Gyr excess stays.
- Real full-spectrum fits with [α/Fe] or the nuisance parameter at a limit: ages fall 3.12 Gyr (26 fits). The other 10 fall 1.85 Gyr.
- 10 Gyr bins: narrower ages, but the fit shrinks a true 3 Gyr gap to 1.73 Gyr.

## References

- [Full range and 10 Gyr fits](results/legac-full-range-test-2026-11-24/summary.md) · [Per fit](results/legac-full-range-test-2026-11-24/per-fit.csv) · [Galaxy list](results/legac-full-range-test-2026-11-24/subset36.csv)
