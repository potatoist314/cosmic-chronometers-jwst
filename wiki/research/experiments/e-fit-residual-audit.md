---
kind: experiment
id: e-fit-residual-audit
title: Residuals and prior boundaries in the six calibration fits
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Reanalyse the six poly3_total fits without new sampling. Compare spectral chi2 at a fixed 3% calibration floor, photometric pulls and prior-boundary occupancy.

## Figures

```json
[
  {
    "path": "wiki/analyses/fit-accuracy-knobs/stage0_chi2_map.png",
    "view": "Comparison",
    "caption": "Six poly3_total fits at a common 3% spectral calibration floor; optical and IRAC residuals remain.",
    "target": ""
  },
  {
    "path": "wiki/analyses/fit-accuracy-knobs/stage0_prior_rails.png",
    "view": "Comparison",
    "caption": "Posterior occupancy near prior boundaries; several parameters approach their bounds.",
    "target": ""
  }
]
```

## Results

The saved tables show optical/IRAC residuals and several parameters near their bounds. The CN and C4668 residuals motivated later mask tests. [Stage 0 table](results/fit-accuracy-knobs/stage0_summary.csv).

[Residual figure](wiki/analyses/fit-accuracy-knobs/stage0_chi2_map.png)

## Caveats

Catalogue absorption indices use the catalogue spectra. Borghi SSP-equivalent ages and Ceridwen mass-weighted ages are different quantities.

## References

- [Executed diagnostics](results/fit-accuracy-knobs/stage0_diagnostics.ipynb)
- [Diagnostic table](results/fit-accuracy-knobs/stage0_summary.csv)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
