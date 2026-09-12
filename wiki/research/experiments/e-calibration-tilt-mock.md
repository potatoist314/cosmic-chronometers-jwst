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
    ],
    "target": "M5_172669"
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
    ],
    "target": "M5_172669"
  }
]
```

## Figures

```json
[
  {
    "path": "results/calibration-polynomial-dr2/mock-tilt.png",
    "view": "Comparison",
    "caption": "Same 4% tilted mock, with and without order-3 calibration. The polynomial recovers the injected dust within its interval.",
    "target": ""
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt4-baseline-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_baseline",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, no polynomial. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt4-baseline-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_baseline",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, no polynomial. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, order 3. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, order 3. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mock-tilt4-baseline-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_baseline",
    "view": "SFH",
    "caption": "M5_172669 · 4% tilt, no polynomial. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "SFH",
    "caption": "M5_172669 · 4% tilt, order 3. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mock-tilt4-baseline-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_baseline",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, no polynomial. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mock-tilt4-baseline-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_baseline",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, no polynomial. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, order 3. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/mock_tilt4_poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mock-tilt4-poly3-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, order 3. Age and formed-mass fractions."
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
