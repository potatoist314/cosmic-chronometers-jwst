---
kind: experiment
id: e-seed-repeatability
title: Repeatability under the reference and revised settings
date: 2026-09-06
origin: existing
status: recorded
question: q-compute
related_questions: q-fitting-choices
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Independent NSS seed repeats on two targets, for poly3_total and new_default. The reference and revised repeats use their own posterior half-widths.

## Runs

```json
[
  {
    "id": "new-default-rep1-m4-108989",
    "arm": "new_default_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20261924
  },
  {
    "id": "new-default-rep1-m5-172669",
    "arm": "new_default_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20261830
  },
  {
    "id": "new-default-rep2-m4-108989",
    "arm": "new_default_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20262924
  },
  {
    "id": "new-default-rep2-m5-172669",
    "arm": "new_default_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20262830
  },
  {
    "id": "seed-rep1-m4-108989",
    "arm": "seed_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20261924
  },
  {
    "id": "seed-rep1-m5-172669",
    "arm": "seed_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20261830
  },
  {
    "id": "seed-rep2-m4-108989",
    "arm": "seed_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20262924
  },
  {
    "id": "seed-rep2-m5-172669",
    "arm": "seed_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20262830
  },
  {
    "id": "seed-rep3-m4-108989",
    "arm": "seed_rep3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20263924
  },
  {
    "id": "seed-rep3-m5-172669",
    "arm": "seed_rep3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20263830
  }
]
```

## Results

Maximum age shifts are 1.197 reference half-widths and 0.336 revised half-widths. Maximum absolute evidence shifts are 1.986 and 3.133. [Seed-floor table](results/fit-accuracy-knobs/seed-floors.csv).

## Caveats

The parameter floors are dimensionless, not Gyr or dex. They come from two targets. They cannot be treated as universal absolute errors or divided by sqrt(187) to establish population significance.

## References

- [Executed comparison](results/fit-accuracy-knobs/new-defaults.ipynb)
- [Seed-floor table](results/fit-accuracy-knobs/seed-floors.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
