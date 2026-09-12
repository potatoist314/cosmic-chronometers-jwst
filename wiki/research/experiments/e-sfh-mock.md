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
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Fits",
    "caption": "M5_172669 · 4% tilt, continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "SFH",
    "caption": "M5_172669 · 4% tilt, continuity prior. Saved SFH and posterior interval."
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
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mock_tilt4_sfh_cont/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mock-tilt4-sfh-cont-m5-172669",
    "target": "M5_172669",
    "arm": "mock_tilt4_sfh_cont",
    "view": "Posteriors",
    "caption": "M5_172669 · 4% tilt, continuity prior. Age and formed-mass fractions."
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
