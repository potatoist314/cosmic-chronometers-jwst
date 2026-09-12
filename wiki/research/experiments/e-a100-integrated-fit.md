---
kind: experiment
id: e-a100-integrated-fit
title: Archived A100 integrated fit
date: 2026-09-04
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results
result_groups: archive/results/a100-integrated-fit-notebook
---

## Context

Early joint photometry/spectrum run retained in the common results board.

## Runs

```json
[
  {
    "id": "a100-integrated-fit",
    "arm": "saved run",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed notebook",
        "path": "archive/results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb"
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
    "notebook": "archive/results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb",
    "cell": 25,
    "output": 0,
    "run": "a100-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Fits",
    "caption": "M1_210210 · saved run. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "archive/results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb",
    "cell": 23,
    "output": 0,
    "run": "a100-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Fits",
    "caption": "M1_210210 · saved run. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "archive/results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb",
    "cell": 27,
    "output": 1,
    "run": "a100-integrated-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "SFH",
    "caption": "M1_210210 · saved run. Saved SFH and posterior interval."
  }
]
```

## Results

The saved notebook contains fitted outputs and a converged NSS trace. Its run settings and results remain in the notebook.

## Caveats

These are different workloads and model versions. No cross-GPU speed ranking or inference about current production performance is made.

## References

- [Executed notebook](archive/results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
