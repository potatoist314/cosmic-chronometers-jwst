---
kind: experiment
id: e-cn-mask
title: Exclude CN and C4668 regions
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Exclude rest-frame 4142–4177 and 4634–4720 Angstrom windows. All other settings follow the documented poly3_total reference.

## Runs

```json
[
  {
    "id": "mask-cn-m4-108989",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924
  },
  {
    "id": "mask-cn-m5-172669",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  },
  {
    "id": "mask-cn-m5-173928",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970
  },
  {
    "id": "mask-cn-m12-185653",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923
  },
  {
    "id": "mask-cn-m1-206545",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877
  },
  {
    "id": "mask-cn-m12-98104",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007
  }
]
```

## Results

| Arm | Median delta spectral chi2 | Median delta photometric chi2 | Median delta ln Z |
| --- | ---: | ---: | ---: |
| mask_cn | -13.82 | -2.24 | not comparable |

[Verdict table](results/fit-accuracy-knobs/verdict.csv) · [Per-target comparisons](results/fit-accuracy-knobs/before-after.csv). Spectral chi2 uses common pixels at a fixed 3% calibration floor.

## Caveats

Removing spectral pixels changes the data. Parameter movement is a sensitivity result, not a validation criterion.

## References

- [Executed comparison](results/fit-accuracy-knobs/analysis.ipynb)
- [Saved arm settings](results/fit-accuracy-knobs/arms.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
