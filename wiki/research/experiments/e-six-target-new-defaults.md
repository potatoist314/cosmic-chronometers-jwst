---
kind: experiment
id: e-six-target-new-defaults
title: Combined dust and SFH changes on six targets
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Compare new_default with poly3_total on the same six targets. The polynomial and photometry are held fixed in this small comparison.

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
    "id": "poly3-total-m5-173928",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/execution.log"
      }
    ],
    "target": "M5_173928"
  },
  {
    "id": "poly3-total-m12-185653",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/execution.log"
      }
    ],
    "target": "M12_185653"
  },
  {
    "id": "poly3-total-m1-206545",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/execution.log"
      }
    ],
    "target": "M1_206545"
  },
  {
    "id": "poly3-total-m12-98104",
    "arm": "poly3_total",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/execution.log"
      }
    ],
    "target": "M12_98104"
  },
  {
    "id": "new-default-m4-108989",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924,
    "target": "M4_108989"
  },
  {
    "id": "new-default-m5-172669",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830,
    "target": "M5_172669"
  },
  {
    "id": "new-default-m5-173928",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970,
    "target": "M5_173928"
  },
  {
    "id": "new-default-m12-185653",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923,
    "target": "M12_185653"
  },
  {
    "id": "new-default-m1-206545",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877,
    "target": "M1_206545"
  },
  {
    "id": "new-default-m12-98104",
    "arm": "new_default",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/new_default/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007,
    "target": "M12_98104"
  }
]
```

## Figures

```json
[
  {
    "path": "results/fit-accuracy-knobs/nd-sfh-histories.png",
    "view": "Comparison",
    "caption": "Six targets with both dust and SFH changes; calibration and photometry remain fixed in this comparison.",
    "target": ""
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m12-185653",
    "target": "M12_185653",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M12_185653 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m12-185653",
    "target": "M12_185653",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M12_185653 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_185653 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_185653 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m12-185653",
    "target": "M12_185653",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M12_185653 · free dust slope and continuity prior. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M12_185653 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m12-185653",
    "target": "M12_185653",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M12_185653 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m12-185653",
    "target": "M12_185653",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M12_185653 · free dust slope and continuity prior. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_185653 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_185653 · order 3, total photometry. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m12-98104",
    "target": "M12_98104",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M12_98104 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m12-98104",
    "target": "M12_98104",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M12_98104 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_98104 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_98104 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m12-98104",
    "target": "M12_98104",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M12_98104 · free dust slope and continuity prior. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M12_98104 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m12-98104",
    "target": "M12_98104",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M12_98104 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m12-98104",
    "target": "M12_98104",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M12_98104 · free dust slope and continuity prior. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_98104 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_98104 · order 3, total photometry. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m1-206545",
    "target": "M1_206545",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M1_206545 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m1-206545",
    "target": "M1_206545",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M1_206545 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M1_206545 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M1_206545 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m1-206545",
    "target": "M1_206545",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M1_206545 · free dust slope and continuity prior. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M1_206545 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m1-206545",
    "target": "M1_206545",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M1_206545 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m1-206545",
    "target": "M1_206545",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M1_206545 · free dust slope and continuity prior. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M1_206545 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M1_206545 · order 3, total photometry. Age and formed-mass fractions."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m4-108989",
    "target": "M4_108989",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M4_108989 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m4-108989",
    "target": "M4_108989",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M4_108989 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m4-108989",
    "target": "M4_108989",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M4_108989 · free dust slope and continuity prior. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m4-108989",
    "target": "M4_108989",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M4_108989 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m4-108989",
    "target": "M4_108989",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M4_108989 · free dust slope and continuity prior. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m5-172669",
    "target": "M5_172669",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M5_172669 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m5-172669",
    "target": "M5_172669",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M5_172669 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m5-172669",
    "target": "M5_172669",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M5_172669 · free dust slope and continuity prior. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m5-172669",
    "target": "M5_172669",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M5_172669 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m5-172669",
    "target": "M5_172669",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M5_172669 · free dust slope and continuity prior. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "new-default-m5-173928",
    "target": "M5_173928",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M5_173928 · free dust slope and continuity prior. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "new-default-m5-173928",
    "target": "M5_173928",
    "arm": "new_default",
    "view": "Fits",
    "caption": "M5_173928 · free dust slope and continuity prior. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_173928 · order 3, total photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_173928 · order 3, total photometry. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "new-default-m5-173928",
    "target": "M5_173928",
    "arm": "new_default",
    "view": "SFH",
    "caption": "M5_173928 · free dust slope and continuity prior. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M5_173928 · order 3, total photometry. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "new-default-m5-173928",
    "target": "M5_173928",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M5_173928 · free dust slope and continuity prior. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/new_default/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "new-default-m5-173928",
    "target": "M5_173928",
    "arm": "new_default",
    "view": "Posteriors",
    "caption": "M5_173928 · free dust slope and continuity prior. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_173928 · order 3, total photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_173928 · order 3, total photometry. Age and formed-mass fractions."
  }
]
```

## Results

The saved headline table records parameter shifts, width ratios, evidence and residual changes for each target. [Six-target comparison](results/fit-accuracy-knobs/new-defaults-headline.csv).

[Dust-slope posteriors](results/fit-accuracy-knobs/nd-dust-index.png)

## Caveats

The combined change does not isolate dust and SFH effects. Historical adoption is not a validation grade. Repeats are linked under the compute question.

## References

- [Executed comparison](results/fit-accuracy-knobs/new-defaults.ipynb)
- [Combined and individual changes](results/fit-accuracy-knobs/new-defaults-additivity.csv)
- [Additional arms](results/fit-accuracy-knobs/new-defaults-extra-arms.csv)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
