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

- **Common rest-frame window (4074.5–4666.1 Å):** \([\alpha/\mathrm{Fe}]\) +0.21, slope −4.60.
- **Full spectrum:** \([\alpha/\mathrm{Fe}]\) +0.01, slope −2.09. Rest-frame coverage changes with redshift.
- **Mocks recover a known slope:** true −5.24 gives −5.63.

### Common window against full spectrum

| Fit | Slope (Gyr per unit \(z\), 16–84%) | Median \([\alpha/\mathrm{Fe}]\) |
| --- | --- | --- |
| Normal model, full spectrum, \(N=108\) | −2.09 (−3.13 to −0.99) | +0.01 |
| Normal model, common window, \(N=110\) | −4.60 (−5.56 to −3.60) | +0.21 |
| Carbon and nitrogen free, common window, \(N=110\) | −5.37 (−6.29 to −4.41) | +0.14 |

Expected slope −5.31.

### Window extensions (change from the common window)

| Window (Å) | Adds | \(\Delta[\alpha/\mathrm{Fe}]\) | \(\Delta\)age (Gyr) | Slope change (16–84%) |
| --- | --- | --- | --- | --- |
| 3742.9–4666.1 | H10, H9, H8 | −0.18 | +0.01 | +0.47 (−0.27 to +1.27) |
| 4074.5–4893.0 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\) | −0.12 | +0.01 | +0.28 (−0.34 to +0.90) |
| 4074.5–5207.9 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\), Fe5015, Mg b | −0.16 | −0.96 | +2.15 (+0.45 to +3.78) |

Age moves only when Fe5015 and Mg b come in.

### Mock check

True −5.24 gives −5.63 full spectrum, −4.54 on the window.

## References

- Detail: [chronometer fits](results/chronometer-135-2026-11-10/REPORT.md), [carbon, nitrogen and mocks](results/cn-response-2026-11-10/REPORT.md), [oldest galaxies](results/oldest-envelope-2026-11-11/REPORT.md).
