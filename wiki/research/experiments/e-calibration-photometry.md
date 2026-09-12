---
kind: experiment
id: e-calibration-photometry
title: Calibration polynomial and photometry aperture
date: 2026-09-05
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: calibration-polynomial-dr2
result_groups: results/calibration-polynomial-dr2
---

## Context

Six DR2 targets: baseline = order 0 with cosmos_ap3; poly3 = order 3 with cosmos_ap3; poly3_total = order 3 with cosmos_total.

## Runs

```json
[
  {
    "id": "baseline-m4-108989",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/execution.log"
      }
    ],
    "target": "M4_108989"
  },
  {
    "id": "baseline-m5-172669",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/execution.log"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "baseline-m5-173928",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/execution.log"
      }
    ],
    "target": "M5_173928"
  },
  {
    "id": "baseline-m12-185653",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/execution.log"
      }
    ],
    "target": "M12_185653"
  },
  {
    "id": "baseline-m1-206545",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/execution.log"
      }
    ],
    "target": "M1_206545"
  },
  {
    "id": "baseline-m12-98104",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/execution.log"
      }
    ],
    "target": "M12_98104"
  },
  {
    "id": "poly3-m4-108989",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/execution.log"
      }
    ],
    "target": "M4_108989"
  },
  {
    "id": "poly3-m5-172669",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/execution.log"
      }
    ],
    "target": "M5_172669"
  },
  {
    "id": "poly3-m5-173928",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/execution.log"
      }
    ],
    "target": "M5_173928"
  },
  {
    "id": "poly3-m12-185653",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/execution.log"
      }
    ],
    "target": "M12_185653"
  },
  {
    "id": "poly3-m1-206545",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/execution.log"
      }
    ],
    "target": "M1_206545"
  },
  {
    "id": "poly3-m12-98104",
    "arm": "poly3",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/execution.log"
      }
    ],
    "target": "M12_98104"
  },
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
  }
]
```

## Figures

```json
[
  {
    "path": "wiki/analyses/calibration-polynomial-dr2/parameters-before-after.png",
    "view": "Comparison",
    "caption": "Six targets, three calibration/photometry settings. Changing aperture to total photometry changes the fitted data.",
    "target": ""
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m12-185653",
    "target": "M12_185653",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M12_185653 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m12-185653",
    "target": "M12_185653",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M12_185653 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m12-185653",
    "target": "M12_185653",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M12_185653 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m12-185653",
    "target": "M12_185653",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M12_185653 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m12-185653",
    "target": "M12_185653",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M12_185653 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m12-185653",
    "target": "M12_185653",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M12_185653 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m12-185653",
    "target": "M12_185653",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M12_185653 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m12-185653",
    "target": "M12_185653",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M12_185653 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m12-185653",
    "target": "M12_185653",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M12_185653 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m12-185653",
    "target": "M12_185653",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M12_185653 · order 3, aperture photometry. Age and formed-mass fractions."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m12-98104",
    "target": "M12_98104",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M12_98104 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m12-98104",
    "target": "M12_98104",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M12_98104 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m12-98104",
    "target": "M12_98104",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M12_98104 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m12-98104",
    "target": "M12_98104",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M12_98104 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m12-98104",
    "target": "M12_98104",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M12_98104 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m12-98104",
    "target": "M12_98104",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M12_98104 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m12-98104",
    "target": "M12_98104",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M12_98104 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m12-98104",
    "target": "M12_98104",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M12_98104 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m12-98104",
    "target": "M12_98104",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M12_98104 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m12-98104",
    "target": "M12_98104",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M12_98104 · order 3, aperture photometry. Age and formed-mass fractions."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m1-206545",
    "target": "M1_206545",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M1_206545 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m1-206545",
    "target": "M1_206545",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M1_206545 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m1-206545",
    "target": "M1_206545",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M1_206545 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m1-206545",
    "target": "M1_206545",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M1_206545 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m1-206545",
    "target": "M1_206545",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M1_206545 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m1-206545",
    "target": "M1_206545",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M1_206545 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m1-206545",
    "target": "M1_206545",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M1_206545 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m1-206545",
    "target": "M1_206545",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M1_206545 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m1-206545",
    "target": "M1_206545",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M1_206545 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m1-206545",
    "target": "M1_206545",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M1_206545 · order 3, aperture photometry. Age and formed-mass fractions."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m4-108989",
    "target": "M4_108989",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M4_108989 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m4-108989",
    "target": "M4_108989",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M4_108989 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m4-108989",
    "target": "M4_108989",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M4_108989 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m4-108989",
    "target": "M4_108989",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M4_108989 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m4-108989",
    "target": "M4_108989",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M4_108989 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m4-108989",
    "target": "M4_108989",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M4_108989 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m4-108989",
    "target": "M4_108989",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M4_108989 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m4-108989",
    "target": "M4_108989",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M4_108989 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m4-108989",
    "target": "M4_108989",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M4_108989 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m4-108989",
    "target": "M4_108989",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M4_108989 · order 3, aperture photometry. Age and formed-mass fractions."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m5-172669",
    "target": "M5_172669",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M5_172669 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m5-172669",
    "target": "M5_172669",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M5_172669 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m5-172669",
    "target": "M5_172669",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M5_172669 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m5-172669",
    "target": "M5_172669",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M5_172669 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m5-172669",
    "target": "M5_172669",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M5_172669 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m5-172669",
    "target": "M5_172669",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M5_172669 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m5-172669",
    "target": "M5_172669",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M5_172669 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m5-172669",
    "target": "M5_172669",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M5_172669 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m5-172669",
    "target": "M5_172669",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m5-172669",
    "target": "M5_172669",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M5_172669 · order 3, aperture photometry. Age and formed-mass fractions."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "baseline-m5-173928",
    "target": "M5_173928",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M5_173928 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "baseline-m5-173928",
    "target": "M5_173928",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M5_173928 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-m5-173928",
    "target": "M5_173928",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M5_173928 · order 3, aperture photometry. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-m5-173928",
    "target": "M5_173928",
    "arm": "poly3",
    "view": "Fits",
    "caption": "M5_173928 · order 3, aperture photometry. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "baseline-m5-173928",
    "target": "M5_173928",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M5_173928 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-m5-173928",
    "target": "M5_173928",
    "arm": "poly3",
    "view": "SFH",
    "caption": "M5_173928 · order 3, aperture photometry. Saved SFH and posterior interval."
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
    "notebook": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "baseline-m5-173928",
    "target": "M5_173928",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M5_173928 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/baseline/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "baseline-m5-173928",
    "target": "M5_173928",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M5_173928 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-m5-173928",
    "target": "M5_173928",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M5_173928 · order 3, aperture photometry. Physical-parameter posterior."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-m5-173928",
    "target": "M5_173928",
    "arm": "poly3",
    "view": "Posteriors",
    "caption": "M5_173928 · order 3, aperture photometry. Age and formed-mass fractions."
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

The poly3_total arm has the smallest photometric chi2 in each target. Adding the polynomial alone leaves substantial photometric residuals. [Arms table](results/calibration-polynomial-dr2/arms.csv) records all three settings.

[Parameter comparison](results/calibration-polynomial-dr2/parameters-before-after.png) · [Calibration vectors](results/calibration-polynomial-dr2/polynomial-vectors.png)

## Caveats

The photometry changes between poly3 and poly3_total. Their evidence values are not a comparison on identical observed data. Lower chi2 does not establish unbiased parameters.

## References

- [Executed comparison](results/calibration-polynomial-dr2/analysis.ipynb)
- [Run manifest](results/calibration-polynomial-dr2/arms_manifest.json)
- [Resolved cells](results/calibration-polynomial-dr2/cells.json)
- [Calibration polynomial dr2 · source note](wiki/notes/calibration-polynomial-dr2.md)
