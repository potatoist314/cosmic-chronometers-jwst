---
kind: experiment
id: e-dust-slope
title: Free and wider dust-slope priors
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Free the attenuation slope on [-1, 0.4], then test a wider lower bound. All other settings follow the documented poly3_total reference.

## Runs

```json
[
  {
    "id": "dust-free-m4-108989",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924
  },
  {
    "id": "dust-free-m5-172669",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  },
  {
    "id": "dust-free-m5-173928",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970
  },
  {
    "id": "dust-free-m12-185653",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923
  },
  {
    "id": "dust-free-m1-206545",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877
  },
  {
    "id": "dust-free-m12-98104",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007
  },
  {
    "id": "dust-wide-m4-108989",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924
  },
  {
    "id": "dust-wide-m5-172669",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  },
  {
    "id": "dust-wide-m5-173928",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970
  },
  {
    "id": "dust-wide-m12-185653",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923
  },
  {
    "id": "dust-wide-m1-206545",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877
  },
  {
    "id": "dust-wide-m12-98104",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007
  }
]
```

## Results

| Arm | Median delta spectral chi2 | Median delta photometric chi2 | Median delta ln Z |
| --- | ---: | ---: | ---: |
| dust_free | -1.92 | -10.65 | 8.18 |

[Verdict table](results/fit-accuracy-knobs/verdict.csv) · [Per-target comparisons](results/fit-accuracy-knobs/before-after.csv). Spectral chi2 uses common pixels at a fixed 3% calibration floor.

## Caveats

Several slopes follow the lower boundary when it moves. Better fit quality does not identify the physical cause of the mismatch.

## References

- [Executed comparison](results/fit-accuracy-knobs/analysis.ipynb)
- [Saved arm settings](results/fit-accuracy-knobs/arms.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
