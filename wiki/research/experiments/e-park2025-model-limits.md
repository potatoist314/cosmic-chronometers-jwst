---
kind: experiment
id: e-park2025-model-limits
title: Stellar model limits in Park et al. 2025
date: 2026-11-24
origin: existing
status: recorded
question: q-spectral-range
---

## Context

The fits use the α-enhanced stellar population models of Park et al. 2025 (ApJ 994:165). Check: do the fitted windows fall inside the wavelengths and elements the authors tuned or tested? The published paper and the arXiv draft give the same line-list text.

Line list: "tuned to the observed high-resolution spectra of the Sun and Arcturus for 4728 Å–1 μm" (§2.2). The paper states nothing below 4728 Å.

## Measurements

| Spectrum | Rest range, Å | Inside the tuned range |
| --- | --- | --- |
| Tuned line list | 4728–10000 | — |
| LEGA-C window | 4074.5–4666.1 | none of it |
| SDSS wide range | 3604.0–7079.3 | from 4728 Å |

- 327 of the 348 LEGA-C DR3 spectra reach rest 4728 Å. 128 reach the red edge of Mg b (5194.07 Å).

**SDSS wide fits, either side of 4728 Å.** Test: does the fit get worse where the authors did not tune the line list?

| 50 SDSS galaxies | Blue of 4728 Å | Red of 4728 Å |
| --- | --- | --- |
| χ² per pixel, median | 1.21 | 1.07 |
| Scatter above the catalogue noise | 2.8 % | 1.0 % |

- The largest offset is at 4600–4728 Å, the C2 4668 band. The authors find their C2 4668 much weaker than in models from observed stars (§3.3.2).

**Elements.**

- One [α/Fe] moves O, Ne, Mg, Si, S, Ar, Ca and Ti together. Authors: Ca is close to solar in ellipticals, so "one should be careful in fitting spectra including Ca indices".
- The models keep C and N solar-scaled. Ceridwen adds free C and N through alf responses (3501.0–24997.6 Å).
- The models neither enhance Na nor leave it free: see [Na D masked](wiki/research/experiments/e-sdss-nad-mask.md).
- Old SSP ages are 1.2–1.5 Gyr apart near 10–14 Gyr. The grid runs to 19.95 Gyr.

## Results

- The whole LEGA-C window lies below 4728 Å, where the authors state no line-list tuning.
- On SDSS the fit is worse blue of 4728 Å: χ² per pixel 1.21 against 1.07.

## References

- [Park et al. 2025, ApJ 994:165](https://doi.org/10.3847/1538-4357/ae0cba) · [Local papers](papers/README.md) · [SDSS wide-range fits](results/sdss-wide-range-2026-11-24/t_0c96cd9b-detail.md)

## Your interpretation

```json
[
  {
    "date": "2026-11-24",
    "text": "okay take the published one. no tuning below 4728 is concerning"
  }
]
```
