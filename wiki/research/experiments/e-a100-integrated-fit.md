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
    ]
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
