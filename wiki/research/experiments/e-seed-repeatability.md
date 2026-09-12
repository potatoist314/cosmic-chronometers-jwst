---
kind: experiment
id: e-seed-repeatability
title: Repeatability under the reference and revised settings
date: 2026-09-06
origin: existing
status: recorded
question: q-compute
related_questions: q-fitting-choices
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Independent NSS seed repeats on two targets, for poly3_total and new_default. The reference and revised repeats use their own posterior half-widths.

## Runs

```json
[
  {
    "id": "poly3-total-m4-108989",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/execution.log"
      }
    ],
    "target": "M4_108989"
  },
  {
    "id": "poly3-total-m5-172669",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/execution.log"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "new-default-rep1-m4-108989",
    "arm": "new_default_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20261924,
    "target": "M4_108989"
  },
  {
    "id": "new-default-rep1-m5-172669",
    "arm": "new_default_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20261830,
    "target": "M5_172669"
  },
  {
    "id": "new-default-rep2-m4-108989",
    "arm": "new_default_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20262924,
    "target": "M4_108989"
  },
  {
    "id": "new-default-rep2-m5-172669",
    "arm": "new_default_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20262830,
    "target": "M5_172669"
  },
  {
    "id": "seed-rep1-m4-108989",
    "arm": "seed_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20261924,
    "target": "M4_108989"
  },
  {
    "id": "seed-rep1-m5-172669",
    "arm": "seed_rep1",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20261830,
    "target": "M5_172669"
  },
  {
    "id": "seed-rep2-m4-108989",
    "arm": "seed_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20262924,
    "target": "M4_108989"
  },
  {
    "id": "seed-rep2-m5-172669",
    "arm": "seed_rep2",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20262830,
    "target": "M5_172669"
  },
  {
    "id": "seed-rep3-m4-108989",
    "arm": "seed_rep3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20263924,
    "target": "M4_108989"
  },
  {
    "id": "seed-rep3-m5-172669",
    "arm": "seed_rep3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20263830,
    "target": "M5_172669"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep1",
    "view": "Fits",
    "caption": "M4_108989 · new default rep1 · seed 20261924. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep1",
    "view": "Fits",
    "caption": "M4_108989 · new default rep1 · seed 20261924. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep2",
    "view": "Fits",
    "caption": "M4_108989 · new default rep2 · seed 20262924. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep2",
    "view": "Fits",
    "caption": "M4_108989 · new default rep2 · seed 20262924. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M4_108989 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M4_108989 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep1",
    "view": "Fits",
    "caption": "M4_108989 · seed rep1 · seed 20261924. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep1",
    "view": "Fits",
    "caption": "M4_108989 · seed rep1 · seed 20261924. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep2",
    "view": "Fits",
    "caption": "M4_108989 · seed rep2 · seed 20262924. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep2",
    "view": "Fits",
    "caption": "M4_108989 · seed rep2 · seed 20262924. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep3-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep3",
    "view": "Fits",
    "caption": "M4_108989 · seed rep3 · seed 20263924. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep3-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep3",
    "view": "Fits",
    "caption": "M4_108989 · seed rep3 · seed 20263924. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep1",
    "view": "SFH",
    "caption": "M4_108989 · new default rep1 · seed 20261924. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep2",
    "view": "SFH",
    "caption": "M4_108989 · new default rep2 · seed 20262924. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M4_108989 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep1",
    "view": "SFH",
    "caption": "M4_108989 · seed rep1 · seed 20261924. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep2",
    "view": "SFH",
    "caption": "M4_108989 · seed rep2 · seed 20262924. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep3-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep3",
    "view": "SFH",
    "caption": "M4_108989 · seed rep3 · seed 20263924. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep1",
    "view": "Posteriors",
    "caption": "M4_108989 · new default rep1 · seed 20261924. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep1",
    "view": "Posteriors",
    "caption": "M4_108989 · new default rep1 · seed 20261924. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep2",
    "view": "Posteriors",
    "caption": "M4_108989 · new default rep2 · seed 20262924. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "new_default_rep2",
    "view": "Posteriors",
    "caption": "M4_108989 · new default rep2 · seed 20262924. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M4_108989 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M4_108989 · order 3, total photometry. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep1",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep1 · seed 20261924. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep1-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep1",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep1 · seed 20261924. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep2",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep2 · seed 20262924. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep2-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep2",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep2 · seed 20262924. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep3-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep3",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep3 · seed 20263924. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep3-m4-108989",
    "target": "M4_108989",
    "arm": "seed_rep3",
    "view": "Posteriors",
    "caption": "M4_108989 · seed rep3 · seed 20263924. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep1",
    "view": "Fits",
    "caption": "M5_172669 · new default rep1 · seed 20261830. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep1",
    "view": "Fits",
    "caption": "M5_172669 · new default rep1 · seed 20261830. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep2",
    "view": "Fits",
    "caption": "M5_172669 · new default rep2 · seed 20262830. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep2",
    "view": "Fits",
    "caption": "M5_172669 · new default rep2 · seed 20262830. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_172669 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_172669 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep1",
    "view": "Fits",
    "caption": "M5_172669 · seed rep1 · seed 20261830. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep1",
    "view": "Fits",
    "caption": "M5_172669 · seed rep1 · seed 20261830. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep2",
    "view": "Fits",
    "caption": "M5_172669 · seed rep2 · seed 20262830. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep2",
    "view": "Fits",
    "caption": "M5_172669 · seed rep2 · seed 20262830. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "seed-rep3-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep3",
    "view": "Fits",
    "caption": "M5_172669 · seed rep3 · seed 20263830. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "seed-rep3-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep3",
    "view": "Fits",
    "caption": "M5_172669 · seed rep3 · seed 20263830. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep1",
    "view": "SFH",
    "caption": "M5_172669 · new default rep1 · seed 20261830. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep2",
    "view": "SFH",
    "caption": "M5_172669 · new default rep2 · seed 20262830. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M5_172669 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep1",
    "view": "SFH",
    "caption": "M5_172669 · seed rep1 · seed 20261830. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep2",
    "view": "SFH",
    "caption": "M5_172669 · seed rep2 · seed 20262830. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "seed-rep3-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep3",
    "view": "SFH",
    "caption": "M5_172669 · seed rep3 · seed 20263830. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep1",
    "view": "Posteriors",
    "caption": "M5_172669 · new default rep1 · seed 20261830. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep1",
    "view": "Posteriors",
    "caption": "M5_172669 · new default rep1 · seed 20261830. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep2",
    "view": "Posteriors",
    "caption": "M5_172669 · new default rep2 · seed 20262830. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "new_default_rep2",
    "view": "Posteriors",
    "caption": "M5_172669 · new default rep2 · seed 20262830. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_172669 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_172669 · order 3, total photometry. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep1",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep1 · seed 20261830. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep1/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep1-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep1",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep1 · seed 20261830. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep2",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep2 · seed 20262830. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep2/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep2-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep2",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep2 · seed 20262830. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "seed-rep3-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep3",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep3 · seed 20263830. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/seed_rep3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "seed-rep3-m5-172669",
    "target": "M5_172669",
    "arm": "seed_rep3",
    "view": "Posteriors",
    "caption": "M5_172669 · seed rep3 · seed 20263830. Age and formed-mass fractions."
  }
]
```

## Results

Maximum age shifts are 1.197 reference half-widths and 0.336 revised half-widths. Maximum absolute evidence shifts are 1.986 and 3.133. [Seed-floor table](results/fit-accuracy-knobs/seed-floors.csv).

## Caveats

The parameter floors are dimensionless, not Gyr or dex. They come from two targets. They cannot be treated as universal absolute errors or divided by sqrt(187) to establish population significance.

## References

- [Executed comparison](results/fit-accuracy-knobs/new-defaults.ipynb)
- [Seed-floor table](results/fit-accuracy-knobs/seed-floors.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
