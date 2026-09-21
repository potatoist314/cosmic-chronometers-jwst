---
kind: experiment
id: e-weak-emission-literature
title: Where the idea of faint emission in quiescent galaxies comes from, and whether the literature establishes it
date: 2026-09-21
origin: new
status: planned
question: q-sample-selection
related_questions: q-fitting-choices, q-emission-lines
follow_up:
---

## Context

Literature check on 2026-09-21: weak emission in quiescent galaxies, power sources, \(\mathrm{H}\beta/[\mathrm{O\,III}]\), \(\mathrm{H}\beta\) infill and age, results at \(z=0.6\text{–}0.9\), and Ceridwen emission selection and masking. Six citations checked against available papers; Gonzalez (1993) checked indirectly; no fit run, no data downloaded, no compute rented.

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "where did you get this notion of emission too weak to detect from - is this established in the literature? what's your source for this?"
  },
  {
    "date": "2026-09-21",
    "text": "tell me more about faint emission from quiescent galaxies"
  }
]
```

## Execution plan

- Comparison: cited claims against paper PDFs.
- Data: arXiv PDFs; `data/raw/legac_dr2/legaCdr2.fits.gz` for the 187 fitted galaxies in `results/dr2-quiescent-new-defaults-summary.csv`.
- Claim labels: PDF, not read, derived, textbook or repo.
- Output: wiki note `weak-emission-quiescent`.

## Amendments

```json
[]
```

## Runs

```json
[]
```

## Figures

```json
[]
```

## Measurements

## Results

- Yan+2006: emission detected at \(\geq3\sigma\) in 52.2% of SDSS red galaxies. Sarzi+2006: 75% of 48 E/S0 galaxies, at an EW limit of \(0.1\,\mathrm{\AA}\). [PDF]
- Maseda+2021: 59% of UVJ-quiescent galaxies at \(z\approx0.85\) above \(\mathrm{EW}([\mathrm{O\,II}])=1.5\,\mathrm{\AA}\). Below-limit stack: \([\mathrm{O\,II}]\) \(0.59\pm0.052\,\mathrm{\AA}\), \([\mathrm{O\,III}]\) \(0.24\pm0.037\,\mathrm{\AA}\), \(\mathrm{H}\beta<0.39\,\mathrm{\AA}\) (\(3\sigma\)), \([\mathrm{Ne\,III}]<0.063\,\mathrm{\AA}\). [PDF]
- \(\mathrm{EW}(\mathrm{H}\beta_{\rm em})/\mathrm{EW}([\mathrm{O\,III}]\,5007)\): Gonzalez (1993), approximately 0.7 via Trager+2000a [not read]; Trager+2000a, median 0.60, range 0.33–1.25 [PDF]; Kuntschner+2006, median 0.67, range 0.3–2.3 [PDF].
- Trager+2000a: \(\mathrm{H}\beta\) infill lowers the absorption index and raises the SSP age; \(0.02\,\mathrm{\AA}\) corresponds to approximately 3% in age. [PDF]
- Fitted sample: \([\mathrm{O\,II}]\) EW missing in 174 of 187 galaxies; \([\mathrm{O\,III}]\,5007\) missing in 167; both missing in 154. Missing EW passes the emission selection. [repo]
- Catalogue Balmer emission at \(|\mathrm{EW}/\sigma_{\mathrm{EW}}|\geq3\): \(\mathrm{H}\beta\), 2 galaxies; \(\mathrm{H}\gamma\), 7; \(\mathrm{H}\delta\), 13. [repo]
- The \(\mathrm{H}\beta\) mask spans \(4837\text{–}4886\,\mathrm{\AA}\), covering the Lick \(\mathrm{H}\beta\) band at \(4847.875\text{–}4876.625\,\mathrm{\AA}\) [derived]. \(\mathrm{H}\gamma\) and \(\mathrm{H}\delta\) are not masked [repo].

## Caveats

- Gonzalez (1993) thesis not read.
- Derived values are arithmetic on cited numbers.
- Case B ratios not checked in a paper.
- No diagnostic-diagram line ratios found for quiescent galaxies at \(z=0.6\text{–}0.9\) in the papers read.

## References

- [weak-emission-quiescent](wiki/notes/weak-emission-quiescent.md)
- [model](wiki/notes/model.md)
- `scripts/absorption_mask_analysis.py:71-75`

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
