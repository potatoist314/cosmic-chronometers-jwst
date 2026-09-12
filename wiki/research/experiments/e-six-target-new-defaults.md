---
kind: experiment
id: e-six-target-new-defaults
title: Combined dust and SFH changes on six targets
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Compare new_default with poly3_total on the same six targets. The polynomial and photometry are held fixed in this small comparison.

## Runs

```json
[
  {
    "id": "new-default-m4-108989",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924
  },
  {
    "id": "new-default-m5-172669",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  },
  {
    "id": "new-default-m5-173928",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970
  },
  {
    "id": "new-default-m12-185653",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923
  },
  {
    "id": "new-default-m1-206545",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877
  },
  {
    "id": "new-default-m12-98104",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007
  }
]
```

## Results

The saved headline table records parameter shifts, width ratios, evidence and residual changes for each target. [Six-target comparison](results/fit-accuracy-knobs/new-defaults-headline.csv).

[Dust-slope posteriors](results/fit-accuracy-knobs/nd-dust-index.png)

## Caveats

The combined change does not isolate dust and SFH effects. Historical adoption is not a validation grade. Repeats are linked under the compute question.

## References

- [Executed comparison](results/fit-accuracy-knobs/new-defaults.ipynb)
- [Combined and individual changes](results/fit-accuracy-knobs/new-defaults-additivity.csv)
- [Additional arms](results/fit-accuracy-knobs/new-defaults-extra-arms.csv)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
