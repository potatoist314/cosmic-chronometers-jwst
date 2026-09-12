---
kind: experiment
id: e-calibration-tilt-mock
title: Calibration recovery on the tilted mock
date: 2026-09-05
origin: existing
status: recorded
question: q-mock-recovery
related_questions: q-fitting-choices
source_notes: calibration-polynomial-dr2
result_groups: results/calibration-polynomial-dr2
---

## Context

The same 4% tilted mock is fitted without a calibration polynomial and with order 3.

## Runs

```json
[
  {
    "id": "mock-tilt4-baseline-m5-172669",
    "arm": "mock_tilt4_baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/execution.log"
      }
    ]
  },
  {
    "id": "mock-tilt4-poly3-m5-172669",
    "arm": "mock_tilt4_poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/execution.log"
      }
    ]
  }
]
```

## Results

The saved comparison reports dust recovery within the posterior interval with the polynomial. The no-polynomial arm overestimates dust. [Mock comparison](results/calibration-polynomial-dr2/mock-tilt.png).

## Caveats

This is one injected population and one tilt configuration. It does not establish general posterior coverage.

## References

- [Executed comparison](results/calibration-polynomial-dr2/analysis.ipynb)
- [Resolved mock cells](results/calibration-polynomial-dr2/cells.json)
- [Calibration polynomial dr2 · source note](wiki/notes/calibration-polynomial-dr2.md)
