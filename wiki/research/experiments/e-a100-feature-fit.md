---
kind: experiment
id: e-a100-feature-fit
title: Archived A100 feature-spectrum fit
date: 2026-08-25
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results
result_groups: archive/results/a100-feature-spectrum
---

## Context

Feature-spectrum full-profile run recorded by the Modal timing file.

## Runs

```json
[
  {
    "id": "a100-feature-fit",
    "arm": "saved run",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed notebook",
        "path": "archive/results/a100-feature-spectrum/ceridwen_test_spectra.executed.ipynb"
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
    "notebook": "archive/results/a100-feature-spectrum/ceridwen_test_spectra.executed.ipynb",
    "cell": 25,
    "output": 1,
    "run": "a100-feature-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "Fits",
    "caption": "M1_210210 · saved run. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "archive/results/a100-feature-spectrum/ceridwen_test_spectra.executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "a100-feature-fit",
    "target": "M1_210210",
    "arm": "saved run",
    "view": "SFH",
    "caption": "M1_210210 · saved run. Saved SFH and posterior interval."
  }
]
```

## Results

The timing record marks the notebook completed, with 10948.46 seconds wall time. This includes notebook execution, not only post-JIT sampling.

## Caveats

These are different workloads and model versions. No cross-GPU speed ranking or inference about current production performance is made.

## References

- [Executed notebook](archive/results/a100-feature-spectrum/ceridwen_test_spectra.executed.ipynb)
- [Saved timing](archive/results/a100-feature-spectrum/modal_execution_timing.json)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
