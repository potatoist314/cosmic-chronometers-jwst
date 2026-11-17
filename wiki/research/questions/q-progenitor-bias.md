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

- **Handled now:** passive cuts only. Published chronometers split by \(\sigma_\star\) or mass and difference narrow \(z\) slices; Moresco+2012 bound it at 6–10 km/s/Mpc for \(z\) 0.6–0.9.
- **Late formers:** 5 of 194 (4 C/N free) formed 90% of their mass after \(z=1.0\), all in the low-\(\sigma_\star\) half. Without them \(H\) is 5 (4) km/s/Mpc lower on the \(\log\sigma_\star\) line.
- **No growing young tail:** age scatter at fixed \(z\) does not grow toward low \(z\); dropping the youngest 10–50% at each \(z\) moves the slope by −0.10 to +0.30, inside its range.

| Line, \(H(z_\mathrm{eff}=0.775)\) (km/s/Mpc, 16–84%) | Plain | C/N free |
| --- | --- | --- |
| Age against \(z\) | 109 (97 to 126) | 107 (95 to 122) |
| Late formers removed | 99 (89 to 112) | 99 (89 to 111) |
| With \(\log\sigma_\star\) term | 95 (86 to 106) | 94 (86 to 103) |
| With \(\log\sigma_\star\) term, late formers removed | 90 (82 to 99) | 90 (82 to 98) |
| Planck18 | 105.4 | 105.4 |

| Toy: late members formed later by | Plain line | Late formers removed | \(\log\sigma_\star\) term |
| --- | --- | --- | --- |
| 1 Gyr | +0.51 | +0.34 | +0.51 |
| 2 Gyr | +1.02 | +0.33 | +1.02 |
| 3 Gyr | +1.53 | +0.12 | +1.54 |

Toy slope bias (Gyr per unit \(z\)): late members rise from none at \(z=1.0\) to 20% at the lowest \(z\). With no late members the cut shifts the slope by −0.12.

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
- Velocity-dispersion term: [q-sigma-term](wiki/research/questions/q-sigma-term.md).
- Passive selection: [selection-counts.csv](results/legac-dr3-2026-11-11/selection-counts.csv), rows NUVrJ quiescent, [O II] EW below 5 Å, no 3σ [O II], [O III].
- Age half-width: [window-194-fits.csv](results/legac-dr3-2026-11-11/window-194-fits.csv), `age_gyr_q16`, `age_gyr_q84`; 0.50 Gyr for plain and C/N free.
- 2.05 Gyr: astropy `Planck18.age`, 5.85 Gyr at \(z=1.0\), 7.90 Gyr at \(z=0.6\).
- Older-bin mass: [age-offset.csv](results/mock-chronometer-window-2026-11-13/age-offset.csv), row `all`, `mass_older` 0.27, median of 194 mocks.
- Tables: [progenitor-budget.csv](results/sigma-split-2026-11-16/progenitor-budget.csv), [progenitor-fixed-population.csv](results/sigma-split-2026-11-16/progenitor-fixed-population.csv), [progenitor-moments.csv](results/sigma-split-2026-11-16/progenitor-moments.csv), [progenitor-youngest-cut.csv](results/sigma-split-2026-11-16/progenitor-youngest-cut.csv), [progenitor-toy.csv](results/sigma-split-2026-11-16/progenitor-toy.csv); script [sigma_split.py](results/sigma-split-2026-11-16/sigma_split.py).
- Late formers: fitted lookback time of 90% of the mass formed under Planck18 \(t(z)-t(z=1.0)-0.75\) Gyr; mocks recover that lookback time 0.67 Gyr short ([mock-sfh-times.csv](results/sigma-split-2026-11-16/mock-sfh-times.csv)). Rows `margin` −0.75. Intervals from \(H_0\) 60–75, \(\Omega_m\) 0.25–0.40 remove 2–6 galaxies.
- Scatter of age about the line, low-\(z\) third minus high-\(z\) third: −0.12 (−0.25 to +0.01) Gyr plain, +0.01 (−0.13 to +0.14) C/N free.
- Published chronometers, with sections: [literature.csv](results/sigma-split-2026-11-16/literature.csv); Moresco+2012 App. A.1, Table 6.
- [Borghi+2022a](papers/chronometer/Toward%20a%20Better%20Understanding%20of%20Cosmic%20Chronometers%20-%20Stellar%20Population%20Properties%20of%20Passive%20Galaxies%20at%20Intermediate%20Redshift.pdf), Sect. 3.1 and Sect. 4 (iii): single-burst SFH, \(t_\mathrm{form}=t_\mathrm{peak}=t_\mathrm{quench}\).

## Decisions

```json
[]
```
