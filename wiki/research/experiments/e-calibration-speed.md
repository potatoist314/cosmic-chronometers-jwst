---
kind: experiment
id: e-calibration-speed
title: Calibration reduction: matched production benchmark
date: 2026-09-07
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results
result_groups: results/rtx-5060-production-speedup
---

## Context

Compare the original and reduced calibration calculation on RTX 5060, grid schema 2.1, with fixed targets, seeds and NSS settings. Existing float32 forward-model assembly is retained.

## Runs

```json
[
  {
    "id": "m1-210210-20260906-baseline",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-baseline/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-baseline/timing.json"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m1-210210-20260906-reduce",
    "arm": "reduce",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-reduce/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-reduce/timing.json"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m1-210210-20260906-rejected-installation",
    "arm": "rejected installation",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-rejected-installation/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260906-rejected-installation/timing.json"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m1-210210-20260907-baseline",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260907-baseline/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260907-baseline/timing.json"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m1-210210-20260907-reduce",
    "arm": "reduce",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260907-reduce/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M1_210210-20260907-reduce/timing.json"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m5-172669-20260906-baseline",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260906-baseline/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260906-baseline/timing.json"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "m5-172669-20260906-reduce",
    "arm": "reduce",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260906-reduce/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260906-reduce/timing.json"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "m5-172669-20260907-baseline",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260907-baseline/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260907-baseline/timing.json"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "m5-172669-20260907-reduce",
    "arm": "reduce",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260907-reduce/analysis.ipynb"
      },
      {
        "label": "Timing",
        "path": "results/rtx-5060-production-speedup/M5_172669-20260907-reduce/timing.json"
      }
    ],
    "target": "M5_172669"
  }
]
```

## Measurements

| Quantity | Measurement |
| --- | --- |
| Workload | Four matched target/seed pairs, RTX 5060, grid schema 2.1 |
| Median full-fit speedup | 1.181x |
| Median time reduction | 15.35% |
| Posterior samples | Equivalent in the recorded comparisons |
| Timing interval | Data loading through HDF5 save; plotting excluded |

[Executed comparison](results/rtx-5060-production-speedup/comparison.ipynb) · [Measurements](results/rtx-5060-production-speedup/comparison.json)

## Results

Across four matched target/seed pairs, median full-fit speedup is 1.181x, or 15.35% less time. Posterior samples are equivalent and the recorded numerical gates pass. [Comparison metrics and numerical checks](results/rtx-5060-production-speedup/comparison.json).

## Caveats

Timing covers data loading through HDF5 save and excludes plotting. Comparisons must use matching compilation paths. The saved rejected-installation attempt is retained as provenance and is not a benchmark pair.

## References

- [Executed comparison](results/rtx-5060-production-speedup/comparison.ipynb)
- [Saved comparison](results/rtx-5060-production-speedup/comparison.json)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
