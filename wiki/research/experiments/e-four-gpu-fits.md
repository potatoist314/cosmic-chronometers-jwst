---
kind: experiment
id: e-four-gpu-fits
title: Four-target RTX 4070 SUPER campaign
date: 2026-08-26
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results,vast-ai-gpu-workflow
result_groups: results/rtx-4070-super-four-galaxy-fits
---

## Context

Four independently seeded full-profile fits, one target per RTX 4070 SUPER worker.

## Runs

```json
[
  {
    "id": "m1-210210",
    "arm": "full",
    "status": "complete",
    "seed": 20260812,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210/m1_210210_executed.ipynb"
      }
    ]
  },
  {
    "id": "m12-181945",
    "arm": "full",
    "status": "complete",
    "seed": 20260813,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_1_m12_181945/m12_181945_executed.ipynb"
      }
    ]
  },
  {
    "id": "m2-133501",
    "arm": "full",
    "status": "complete",
    "seed": 20260814,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_2_m2_133501/m2_133501_executed.ipynb"
      }
    ]
  },
  {
    "id": "m14-38648",
    "arm": "full",
    "status": "complete",
    "seed": 20260815,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_3_m14_38648/m14_38648_executed.ipynb"
      }
    ]
  }
]
```

## Results

The manifest records all four workers complete. Their executed notebooks retain the fitted spectra and posterior outputs.

## Caveats

This early campaign uses its recorded full-profile settings. It is not a matched speed comparison with later DR2 campaigns.

## References

- [Campaign manifest](results/rtx-4070-super-four-galaxy-fits/run_manifest.json)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
- [vast-ai-gpu-workflow · source note](wiki/notes/vast-ai-gpu-workflow.md)
