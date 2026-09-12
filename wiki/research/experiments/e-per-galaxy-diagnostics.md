---
kind: experiment
id: e-per-galaxy-diagnostics
title: Per-galaxy residuals and GPU refit checks
date: 2026-09-06
origin: existing
status: recorded
question: q-population-results
related_questions: q-compute
source_notes: per-galaxy-fit-diagnostics,per-galaxy-diagnostics-gallery
result_groups: results/rtx-5060-per-galaxy-diagnostics-verification
---

## Context

Audit stored residuals and assembly histories for the baseline sample, then refit two targets using their recorded seeds.

## Runs

```json
[
  {
    "id": "m2-139662",
    "arm": "verification",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_139662",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/ceridwen_result.h5"
      }
    ],
    "seed": 20260949,
    "config": "results/rtx-5060-per-galaxy-diagnostics-verification/shard_1_manifest.json",
    "data": "results/rtx-5060-per-galaxy-diagnostics-verification/targets.json"
  },
  {
    "id": "m1-210210",
    "arm": "verification",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/ceridwen_result.h5"
      }
    ],
    "seed": 20260832,
    "config": "results/rtx-5060-per-galaxy-diagnostics-verification/shard_0_manifest.json",
    "data": "results/rtx-5060-per-galaxy-diagnostics-verification/targets.json"
  }
]
```

## Results

The source report gives median photometric chi2/N = 7.04 and spectral chi2/N = 1.120. The refit table records a 0.44 Gyr age change for M1_210210 and a smaller change for M2_139662. [All target diagnostics](results/per-galaxy-diagnostics.csv) · [GPU refit comparison](results/rtx-5060-per-galaxy-diagnostics-verification/refit_vs_production.csv).

## Caveats

Matching a seed does not reproduce the model implementation. The original report attributes the refit discrepancy to forward-model changes; use its recorded checks rather than treating these as pure seed repeats.

## References

- [Executed diagnostics](notebooks/ceridwen_per_galaxy_diagnostics.ipynb)
- [Audit report](reports/astro-chisq-sf-plots-2026-09-06.md)
- [GPU comparison](results/rtx-5060-per-galaxy-diagnostics-verification/refit_vs_production.csv)
- [per-galaxy-fit-diagnostics · source note](wiki/notes/per-galaxy-fit-diagnostics.md)
- [per-galaxy-diagnostics-gallery · source note](wiki/notes/per-galaxy-diagnostics-gallery.md)
