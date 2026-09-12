---
kind: experiment
id: e-sfh-prior
title: Continuity versus uniform SFH prior
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions: q-mock-recovery
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Compare StudentT(0, 0.3, df=2) SFH ratios with Uniform(-3, 3). All other settings follow the documented poly3_total reference.

## Runs

```json
[
  {
    "id": "sfh-cont-m4-108989",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/sfh_cont/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924
  },
  {
    "id": "sfh-cont-m5-172669",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/sfh_cont/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  },
  {
    "id": "sfh-cont-m5-173928",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/sfh_cont/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970
  },
  {
    "id": "sfh-cont-m12-185653",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/sfh_cont/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923
  },
  {
    "id": "sfh-cont-m1-206545",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/sfh_cont/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877
  },
  {
    "id": "sfh-cont-m12-98104",
    "arm": "sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/sfh_cont/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/sfh_cont/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/sfh_cont/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007
  }
]
```

## Results

| Arm | Median delta spectral chi2 | Median delta photometric chi2 | Median delta ln Z |
| --- | ---: | ---: | ---: |
| sfh_cont | 2.79 | -0.79 | -4.46 |

[Verdict table](results/fit-accuracy-knobs/verdict.csv) · [Per-target comparisons](results/fit-accuracy-knobs/before-after.csv). Spectral chi2 uses common pixels at a fixed 3% calibration floor.

## Caveats

Wider posterior intervals alone do not demonstrate better accuracy. Recovery on the existing mock is reported separately.

## References

- [Executed comparison](results/fit-accuracy-knobs/analysis.ipynb)
- [Saved arm settings](results/fit-accuracy-knobs/arms.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
