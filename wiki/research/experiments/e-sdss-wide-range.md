---
kind: experiment
id: e-sdss-wide-range
title: SDSS 50 on a wide spectrum and 15 Gyr SFH bins
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
result_groups: results/sdss-wide-range-2026-11-24, results/sdss-wide-fixed-age-2026-11-24
---

## Context

The SDSS fits had used rest 4074.5–4666.1 Å, the LEGA-C window, though SDSS spectra reach much further. 50 galaxies, \(z\) 0.054–0.300.

- Test 1: fit rest 3604.0–7079.3 Å, 2738 pixels instead of 544.
- Test 2: end the SFH bins at 15 Gyr for every galaxy, so cosmology no longer enters the fit.

Planck18 Universe-age slope over these redshifts: −11.4 Gyr per unit \(z\).

## Measurements

| Rest 3604.0–7079.3 Å: SFH bins end at | Age slope (Gyr per unit \(z\)) | Ages above the Planck18 Universe age |
| --- | --- | --- |
| Planck18 Universe age at each \(z\) | −16.7 ± 2.7 | none possible: ages stop at 0.925 of it |
| 15 Gyr | −11.9 ± 3.3 | 11 of 50 |

- Bins to the Universe age: 12 of 50 fits put more than 90 % of their mass in the oldest bin. Their ages sit at the largest possible value. Age still follows 0.66 of a change in the bins (narrow window 0.79).
- 15 Gyr bins: \(H_0\) from the slope 65.6 (50.9 to 91.4) km/s/Mpc. Scatter of ages about the line: 1.60 Gyr. Uncertainty on one galaxy's age: 0.84 Gyr.
- Worst-fitted bands, χ² per pixel over all 50: Na D 3.28, Fe4668 1.90, Mg b 1.36. All pixels: 1.14.

**Ages above the Universe age, 15 Gyr bins.** Test: is 11 of 50 more than scatter gives?

| Count | Expected | Seen |
| --- | --- | --- |
| Above the Universe age, from the 1.60 Gyr scatter | 11.8 | 11 |
| Above it, from the fits' own age uncertainties | 4.7 | 11 |
| More than 2 Gyr above / below the line | equal | 6 / 5 |

- The scatter beyond the fits' uncertainties follows velocity dispersion (r +0.47) and stellar mass (+0.54), not S/N (+0.01).
- Slope without the 11: −10.4 ± 2.9. That cut pulls slopes toward the Planck18 −11.4. In 20,000 simulated sets of 50 ages (scatter 1.60 Gyr), true −4.0 becomes −7.3 and true −20.0 becomes −16.2.
- Without the 5 fits at the 15 Gyr limit: −8.9 ± 3.3. Ages clipped at the Universe age: −12.0 ± 2.8.

**Oldest galaxies per redshift bin.** 4, 6 or 8 bins of equal count. Keep the oldest 1, 10, 25 or 50 % of each: 12 choices.

| Sample | All galaxies | Oldest per bin, 12 choices |
| --- | --- | --- |
| SDSS, 50, 15 Gyr bins | −11.91 | −13.56 to −7.27 |
| LEGA-C DR3, 348, bins to the Universe age | −4.77 | −5.20 to −4.40 |

- Planck18 Universe-age slope at the kept redshifts: −11.28 to −11.68 (SDSS), −5.26 to −5.38 (LEGA-C).
- On SDSS the choice moves the slope by 6.3 Gyr per unit \(z\), more than its bootstrap error (3.4 to 4.6).

## Results

- Wide range, 15 Gyr bins: slope −11.9 ± 3.3 against −11.4 for Planck18. 11 of 50 ages lie above the Universe age, as many as the scatter predicts.
- Keeping only the oldest per redshift bin does not pin the SDSS slope at \(N = 50\).

## References

- [Wide range](results/sdss-wide-range-2026-11-24/t_0c96cd9b-detail.md) · [15 Gyr bins, configuration](results/sdss-wide-fixed-age-2026-11-24/experiment.json) · [LEGA-C DR3 348](results/dr3-more-galaxies-2026-11-16/REPORT.md)

## Your interpretation

```json
[
  {
    "date": "2026-11-24",
    "text": "ugh. step 1 seems good."
  },
  {
    "date": "2026-11-24",
    "text": "older than universe doesn't seem like a bad sign? if the error bars are wide it seems like some should land older than the universe just by scatter, but they should probably be kept to balance those which land on the young side of the error?"
  }
]
```

## Before delegation

```json
[
  {
    "date": "2026-11-24",
    "text": "just use mass weighted for now and experiment with only keeping the oldest per refshift bin. i think this doesnt need extra gpu compute"
  }
]
```
