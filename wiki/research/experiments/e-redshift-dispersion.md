---
kind: experiment
id: e-redshift-dispersion
title: Free redshift and velocity dispersion
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: redshift-sigma-wiggle
result_groups: results/redshift-sigma-wiggle
---

## Context

Compare zsig with poly3_total for four targets, using the documented free-z spectrum fork.

## Runs

```json
[
  {
    "id": "zsig-m5-172669",
    "arm": "zsig",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/redshift-sigma-wiggle/zsig/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/redshift-sigma-wiggle/zsig/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/redshift-sigma-wiggle/zsig/172669-M5_172669/execution.log"
      }
    ]
  },
  {
    "id": "zsig-m5-173928",
    "arm": "zsig",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/redshift-sigma-wiggle/zsig/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/redshift-sigma-wiggle/zsig/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/redshift-sigma-wiggle/zsig/173928-M5_173928/execution.log"
      }
    ]
  },
  {
    "id": "zsig-m12-185653",
    "arm": "zsig",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/redshift-sigma-wiggle/zsig/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/redshift-sigma-wiggle/zsig/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/redshift-sigma-wiggle/zsig/185653-M12_185653/execution.log"
      }
    ]
  },
  {
    "id": "zsig-m1-206545",
    "arm": "zsig",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/redshift-sigma-wiggle/zsig/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/redshift-sigma-wiggle/zsig/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/redshift-sigma-wiggle/zsig/206545-M1_206545/execution.log"
      }
    ]
  }
]
```

## Results

The source comparison finds small age shifts, while M5_173928 reaches the dispersion upper bound. [Per-target shifts](results/redshift-sigma-wiggle/delta-vs-poly3_total.csv).

## Caveats

The free-z implementation was an experimental fork. Do not infer current production behaviour from this historical run.

## References

- [Executed comparison](results/redshift-sigma-wiggle/analysis.ipynb)
- [Fitted nuisances](results/redshift-sigma-wiggle/zsig-vs-poly3_total.csv)
- [Redshift sigma wiggle · source note](wiki/notes/redshift-sigma-wiggle.md)
