---
kind: question
id: q-afe-age-chronometer
title: Low alpha/Fe, Mg b and the chronometer age slope
date: 2026-11-10
origin: existing
status: open
---

## Context

### Answer

- **LEGA-C DR3, common window, 194 galaxies:** slope −5.04 plain, −5.15 C/N free, −4.26 carbon mask; same line fit to Planck18 ages −5.23.
- **Carbon mask:** median \([\alpha/\mathrm{Fe}]\) +0.23 against +0.13 plain; slope 1.5σ shallower than the same line fit to Planck18 ages.
- **Mocks on the same window:** true slope −5.23 gives −5.12 (194 mocks).
- **Carried forward:** C/N free. Liu Hao, 2026-11-16: “sure cn free seems good to carry on”.

A mock is a synthetic spectrum and photometry with a known age, made at a real galaxy's redshift, S/N and window and fitted with the plain arm.

<figure>
<img src="wiki/analyses/afe-age-chronometer/age-redshift-dr3.png" alt="Mass-weighted age against redshift, 194 LEGA-C DR3 galaxies, three arms, with fitted lines and the same line fit to Planck18 ages">
<figcaption>LEGA-C DR3, rest frame 4074.5–4666.1 Å. C/N free: \([\mathrm{C}/\mathrm{Fe}]\), \([\mathrm{N}/\mathrm{Fe}]\) free (<a href="wiki/notes/model.md#cn-responses">alf responses</a>). Carbon mask: CN4150, G4300, Fe4383, C4668 masked. Otherwise as plain. Dashed: same line fit to Planck18 ages, through each arm's mean.</figcaption>
</figure>

<figure>
<img src="wiki/analyses/afe-age-chronometer/mock-chronometer.png" alt="True and recovered mass-weighted age against redshift for the mocks on the common window">
<figcaption>Mocks: plain arm; four SFH shapes, one formation epoch; \([\alpha/\mathrm{Fe}]=+0.2\), \([\mathrm{Fe}/\mathrm{H}]=-0.2\); fluxes matched to each galaxy.</figcaption>
</figure>

| Fit | Slope (Gyr per unit \(z\), 16–84%) | \(H(z_\mathrm{eff})\) (km/s/Mpc) | Median \([\alpha/\mathrm{Fe}]\) |
| --- | --- | --- | --- |
| Plain, \(N=194\) | −5.04 (−5.70 to −4.39) | 109 (97 to 126) | +0.13 |
| [C/N free](wiki/notes/model.md#cn-responses), \(N=194\) | −5.15 (−5.78 to −4.53) | 107 (95 to 122) | +0.16 |
| Carbon mask, \(N=194\) | −4.26 (−4.90 to −3.62) | 129 (112 to 152) | +0.23 |
| Planck18 at \(z_\mathrm{eff}=0.775\), \(H_0=67.66\) | −5.23 | 105.4 |  |
| Mock truth, \(N=194\) | −5.23 | 105 | +0.20 |
| Mock recovered, \(N=194\) | −5.12 (−5.36 to −4.88) | 108 (103 to 113) | +0.21 |
| Mock C/N free, \(N=40\), true −5.35 | −5.04 (−5.47 to −4.57) |  | +0.20 |

Age against \(z\) is curved, so a straight-line slope equals \(\mathrm{d}t/\mathrm{d}z\) at \(z_\mathrm{eff}=0.775\), not at the median \(z=0.728\); \(z_\mathrm{eff}\) is 0.774–0.775 for \(H_0\) 60–75, \(\Omega_m\) 0.25–0.40.

<details>
<summary>LEGA-C DR2, 2026-11-10</summary>

| Fit | Slope (Gyr per unit \(z\), 16–84%) | Median \([\alpha/\mathrm{Fe}]\) |
| --- | --- | --- |
| Normal model, full spectrum, \(N=108\) | −2.09 (−3.13 to −0.99) | +0.01 |
| Normal model, common window, \(N=110\) | −4.60 (−5.56 to −3.60) | +0.21 |
| Carbon and nitrogen free, common window, \(N=110\) | −5.37 (−6.29 to −4.41) | +0.14 |

Expected slope −5.31. Mocks: true −5.24 gives −5.63 full spectrum, −4.54 on the window.

| Window (Å) | Adds | \(\Delta[\alpha/\mathrm{Fe}]\) | \(\Delta\)age (Gyr) | Slope change (16–84%) |
| --- | --- | --- | --- | --- |
| 3742.9–4666.1 | H10, H9, H8 | −0.18 | +0.01 | +0.47 (−0.27 to +1.27) |
| 4074.5–4893.0 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\) | −0.12 | +0.01 | +0.28 (−0.34 to +0.90) |
| 4074.5–5207.9 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\), Fe5015, Mg b | −0.16 | −0.96 | +2.15 (+0.45 to +3.78) |

Window extensions change from the common window. Age moves only when Fe5015 and Mg b come in.

</details>

## Your words

```json
[
  {
    "date": "2026-11-10",
    "text": "fundamentally i'm not getting the alpha/fe i expect from my fits, it's too low because Mg b is not being predicted correctly, but i can't seem to do much about it because that's just how the full spectrum fitting is and if i keep masking arbitrary bands there may as well be no benefit to doing full spectrum fitting. and somewhere along the way this is messing with age so i'm not seeing the overall hubble constant age results i want from the cosmic chronometer"
  },
  {
    "date": "2026-11-14",
    "text": "cool,  good methodology,  but not well presented or visible"
  },
  {
    "date": "2026-11-16",
    "text": "yes, the standard seems good"
  }
]
```

## References

- Detail: [DR3 window fits](results/legac-dr3-2026-11-11/REPORT.md), [carbon mask on the window](results/carbon-mask-window-2026-11-13/age-redshift-slopes.csv), [mock chronometer](results/mock-chronometer-window-2026-11-13/mocks.py), [C/N-free mocks](results/mock-chronometer-cn-free-2026-11-16/slopes.csv) ([paired with plain](results/mock-chronometer-cn-free-2026-11-16/paired-slopes.csv)), [DR2 chronometer fits](results/chronometer-135-2026-11-10/REPORT.md), [carbon, nitrogen and mocks](results/cn-response-2026-11-10/REPORT.md), [oldest galaxies](results/oldest-envelope-2026-11-11/REPORT.md).
- Figures and table: `scripts/plot_afe_age_chronometer.py`; \(z_\mathrm{eff}\): `effective_redshift` in `src/chronometer.py`.
