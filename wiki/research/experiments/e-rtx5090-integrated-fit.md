---
kind: experiment
id: e-rtx5090-integrated-fit
title: Archived RTX 5090 integrated fit
date: 2026-08-27
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results
result_groups: archive/results/rtx-5090-integrated-fit
---

## Context

M1_210210, 11 fitted photometric bands and 3523 spectral pixels; grid schema 2.1. NSS uses 300 live points, 40 inner steps and 25 deletions.

## Runs

```json
[
  {
    "id": "rtx5090-integrated-fit",
    "arm": "saved run",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed notebook",
        "path": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb"
      }
    ],
    "target": "M1_210210"
  }
]
```

## Figures

```json
[
  {
    "notebook": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "rtx5090-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Fits",
    "caption": "M1_210210 · saved run. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "rtx5090-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Fits",
    "caption": "M1_210210 · saved run. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb",
    "cell": 26,
    "output": 3,
    "run": "rtx5090-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "SFH",
    "caption": "M1_210210 · saved run. Saved SFH and posterior interval."
  },
  {
    "notebook": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb",
    "cell": 26,
    "output": 0,
    "run": "rtx5090-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Posteriors",
    "caption": "M1_210210 · saved run. Physical-parameter posterior."
  },
  {
    "notebook": "archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "rtx5090-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Posteriors",
    "caption": "M1_210210 · saved run. Age and formed-mass fractions."
  }
]
```

## Results

The saved timing is 1307.5 seconds sampling and 1386.14 seconds notebook execution. The saved log evidence is 230637.429 +/- 0.443.

## Caveats

These are different workloads and model versions. No cross-GPU speed ranking or inference about current production performance is made.

## References

- [Executed notebook](archive/results/rtx-5090-integrated-fit/ceridwen_integrated_photometry_spectra_executed.ipynb)
- [Saved timing](archive/results/rtx-5090-integrated-fit/fit_timing.json)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
