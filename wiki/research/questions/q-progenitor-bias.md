---
kind: question
id: q-progenitor-bias
title: Progenitor bias in the cosmic chronometer
date: 2026-11-16
origin: new
status: open
---

## Context

Galaxies that quench after the high-\(z\) end is observed join the passive sample at low \(z\). That end reads younger, the age–\(z\) line flattens and \(H\) reads high. Only the passive cuts act on this now (NUVrJ, \([\mathrm{O\,II}]\) EW, 3σ lines). Agreement with Planck18 does not test it: the slope is the measurement.

Each fit's SFH gives a quenching time. Galaxies quenched before \(z=1.0\) form one population seen at different times. Borghi+2022a's Lick-index ages assume a single burst.

Median age 16–84% half-width 0.50 Gyr, against 2.05 Gyr from \(z=1.0\) to 0.6 (Planck18). Mock fits put 27% of mass in bins older than any true star. Late quenchers could look earlier.

### Answer

In progress on the 194 fits: slope as the quenching-time cut tightens, slope without the youngest galaxies at each \(z\), toy mock with late quenchers.

## Your words

```json
[
  {
    "date": "2026-11-16",
    "text": "and i'm still not sure how progenitor bias is handled, if at all",
    "display_text": "And I'm still not sure how progenitor bias is handled, if at all.",
    "source_ref": "session 44a318fe-f8bc-458f-a1fc-c4c5cd719664"
  },
  {
    "date": "2026-11-16",
    "text": "ah, if we have sfh, then we can distinguish later quenching galaxies! is that what you mean?",
    "display_text": "Ah, if we have SFH, then we can distinguish later-quenching galaxies! Is that what you mean?",
    "source_ref": "session 44a318fe-f8bc-458f-a1fc-c4c5cd719664"
  }
]
```

## References

- Chronometer result: [q-afe-age-chronometer](wiki/research/questions/q-afe-age-chronometer.md).
- Passive selection: [selection-counts.csv](results/legac-dr3-2026-11-11/selection-counts.csv), rows NUVrJ quiescent, [O II] EW below 5 Å, no 3σ [O II], [O III].
- Age half-width: [window-194-fits.csv](results/legac-dr3-2026-11-11/window-194-fits.csv), `age_gyr_q16`, `age_gyr_q84`; 0.50 Gyr for plain and C/N free.
- 2.05 Gyr: astropy `Planck18.age`, 5.85 Gyr at \(z=1.0\), 7.90 Gyr at \(z=0.6\).
- Older-bin mass: [age-offset.csv](results/mock-chronometer-window-2026-11-13/age-offset.csv), row `all`, `mass_older` 0.27, median of 194 mocks.
- [Borghi+2022a](papers/chronometer/Toward%20a%20Better%20Understanding%20of%20Cosmic%20Chronometers%20-%20Stellar%20Population%20Properties%20of%20Passive%20Galaxies%20at%20Intermediate%20Redshift.pdf), Sect. 3.1 and Sect. 4 (iii): single-burst SFH, \(t_\mathrm{form}=t_\mathrm{peak}=t_\mathrm{quench}\).

## Decisions

```json
[]
```
