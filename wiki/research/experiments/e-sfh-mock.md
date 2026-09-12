---
kind: experiment
id: e-sfh-mock
title: SFH-prior recovery on the tilted mock
date: 2026-09-06
origin: existing
status: recorded
question: q-mock-recovery
related_questions: q-fitting-choices
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Compare mock_tilt4_poly3 and mock_tilt4_sfh_cont on the same saved injected population.

## Runs

```json
[
  {
    "id": "mock-tilt4-sfh-cont-m5-172669",
    "arm": "mock_tilt4_sfh_cont",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830
  }
]
```

## Results

Age recovery changes from 0.637 to 1.816 posterior half-widths from truth. Dust changes from 0.711 to 1.534. [Mock-pull rows](results/fit-accuracy-knobs/mock-pulls.csv).

## Caveats

The injected SFH favours the reference setup. This single case does not rank population-wide accuracy. mock-new-defaults.csv contains these same two arms; it is not evidence that the combined new-default mock ran.

## References

- [Executed analysis](results/fit-accuracy-knobs/analysis.ipynb)
- [Mock recovery](results/fit-accuracy-knobs/mock-pulls.csv)
- [Later mock table](results/fit-accuracy-knobs/mock-new-defaults.csv)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
