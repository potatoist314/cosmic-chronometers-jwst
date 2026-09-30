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
features: logsfr_ratios
finding: tilted mock, mock_tilt4_poly3 to mock_tilt4_sfh_cont: age 0.637 to 1.816 posterior half-widths from truth; dust 0.711 to 1.534
---

## Context

Compare mock_tilt4_poly3 and mock_tilt4_sfh_cont on the same saved injected population.

## Runs

```json
[
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
    ],
    "target": "M5_172669"
  },
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
    "seed": 20260830,
    "target": "M5_172669"
  }
]
```

## Figures

```json
[
  {
    "path": "results/fit-accuracy-knobs/mock-sfh-prior.png",
    "view": "Comparison",
    "caption": "Same injected SFH: the continuity-prior fit lies further from the injected age. This is one reference-like mock.",
    "target": ""
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Fits",
    "caption": "M5_172669 · Spectrum · mock_tilt4_poly3, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · mock_tilt4_poly3, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Fits",
    "caption": "M5_172669 · Spectrum · mock_tilt4_sfh_cont: SFH prior StudentT(0, 0.3, 2); otherwise as mock_tilt4_poly3."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · mock_tilt4_sfh_cont: SFH prior StudentT(0, 0.3, 2); otherwise as mock_tilt4_poly3."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "SFH",
    "caption": "M5_172669 · SFH · mock_tilt4_poly3, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "SFH",
    "caption": "M5_172669 · SFH · mock_tilt4_sfh_cont: SFH prior StudentT(0, 0.3, 2); otherwise as mock_tilt4_poly3."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · Posteriors · mock_tilt4_poly3, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · Ages · mock_tilt4_poly3, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Posteriors",
    "caption": "M5_172669 · Posteriors · mock_tilt4_sfh_cont: SFH prior StudentT(0, 0.3, 2); otherwise as mock_tilt4_poly3."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Posteriors",
    "caption": "M5_172669 · Ages · mock_tilt4_sfh_cont: SFH prior StudentT(0, 0.3, 2); otherwise as mock_tilt4_poly3."
  }
]
```

## Results

Age recovery changes from 0.637 to 1.816 posterior half-widths from truth. Dust changes from 0.711 to 1.534. [Mock-pull rows](results/fit-accuracy-knobs/mock-pulls.csv).

## Caveats

One injected SFH. mock-new-defaults.csv contains mock_tilt4_poly3 and mock_tilt4_sfh_cont, with no combined new-default arm.

## References

- [Executed analysis](results/fit-accuracy-knobs/analysis.ipynb)
- [Mock recovery](results/fit-accuracy-knobs/mock-pulls.csv)
- [Later mock table](results/fit-accuracy-knobs/mock-new-defaults.csv)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
