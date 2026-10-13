---
kind: question
id: q-afe-mgb-weighting
title: Mg b weighting in alpha-abundance fits
date: 2026-10-13
origin: new
status: open
---

## Context

### Full-spectrum and index fits

- Full-spectrum median \([\alpha/\mathrm{Fe}]\): +0.087, about +0.09, for 60 galaxies with Mg b in the fitted range ([REPORT.md](results/afe-feh-investigation-2026-10-13/REPORT.md), §2).
- Mg b + Fe4383 fits on Ceridwen's own grid use the two-index approach of Bevacqua+23. Conditional scans retain fitted SFH and iron history.
- For 18 clean galaxies, the index median is +0.345, about +0.35, against a full-spectrum median of +0.097. The median paired shift is +0.203 dex, about +0.20. Its galaxy-bootstrap 95% interval is +0.156 to +0.327 dex, about +0.16 to +0.33 ([INDEX-TEST.md](results/afe-feh-investigation-2026-10-13/INDEX-TEST.md), opening table).
- Method alone produces the missing roughly 0.2 dex within the same grid. Which pixels determine \([\alpha/\mathrm{Fe}]\) explains this shift. A line-strength zero point alone cannot explain it.

### Line residuals

Negative residuals mean the model is too weak ([REPORT.md](results/afe-feh-investigation-2026-10-13/REPORT.md), §1).

| Feature | Residual | Pull | Galaxies |
| --- | --- | --- | --- |
| Mg b | −1.44% | −3.28 | 61 |
| \(\mathrm{C}_2\) 4668 | −1.27% | −3.62 | 117 |
| CN4150 | −1.01% | −1.59 | 133 |

- Raising \([\alpha/\mathrm{Fe}]\) on the lockstep grid deepens Mg b but weakens carbon-sensitive bands. The full-spectrum compromise settles low.
- More oxygen binding more carbon into CO is a proposed mechanism ([Park et al. 2025](papers/spectral%20fitting/Alpha-MC%20-%20Self-consistent%20Alpha-enhanced%20Stellar%20Population%20Models%20Covering%20a%20Wide%20Range%20of%20Age,%20Metallicity,%20and%20Wavelength.pdf), §3.2.3). C/N remain solar-scaled (§2.4).

### Coverage and pixel weights

- \([\alpha/\mathrm{Fe}]\) versus redshift has \(\rho=-0.47\) as Mg b leaves the LEGA-C window above \(z\approx0.72\). Borghi+22 gives \(\rho=-0.01\) for the same 48 galaxies ([REPORT.md](results/afe-feh-investigation-2026-10-13/REPORT.md), §2).
- Pixel weights come only from noise: `noise_floor=0`. Fitted fractional \(f_{\mathrm{calib}}\) has median 3.8%, with the same fraction at every pixel. There are no special Mg b or carbon-feature weights ([noise_model.py](ceridwen/ceridwen/likelihood/noise_model.py#L163-L181), lines 163–181, and saved October posteriors).

### Parked step — priority 10

- Mask CN4150, G4300, Fe4383 and \(\mathrm{C}_2\) 4668 so Mg b carries more weight in \([\alpha/\mathrm{Fe}]\). Park et al. 2025 §3.2.3 identifies these carbon-sensitive indices as weakening with increasing \([\alpha/\mathrm{Fe}]\).
- Refit about 60 galaxies whose spectra cover Mg b. First check: short local fits on about 10.
- Rest-frame UV below \(4000\,\mathrm{\AA}\) also prefers the lowest \([\alpha/\mathrm{Fe}]\), so masking may not lift it all the way ([REPORT.md](results/afe-feh-investigation-2026-10-13/REPORT.md), §2).

## Your words

```json
[
  {
    "date": "2026-10-13",
    "text": "i trust the mg line much more than the carbon lines so it seems bad they have equal weight"
  },
  {
    "date": "2026-10-13",
    "text": "park that thought and put findings in the wiki as a research roadmap priority 10"
  }
]
```

## References

- [REPORT.md](results/afe-feh-investigation-2026-10-13/REPORT.md), §§1–2.
- [INDEX-TEST.md](results/afe-feh-investigation-2026-10-13/INDEX-TEST.md), opening table and conditional two-index scans.
- [Park et al. 2025](papers/spectral%20fitting/Alpha-MC%20-%20Self-consistent%20Alpha-enhanced%20Stellar%20Population%20Models%20Covering%20a%20Wide%20Range%20of%20Age,%20Metallicity,%20and%20Wavelength.pdf), §§2.4 and 3.2.3.
- [noise_model.py](ceridwen/ceridwen/likelihood/noise_model.py#L163-L181), lines 163–181. Fractional-noise median: weighted posterior medians of `samples/log_f_calib` across the 135 saved [October fits](results/dr2-refit-2026-10-12/dr2-refit-summary.csv). The saved spectrum observations have `noise_floor=0`.

## Decisions

```json
[]
```
