---
kind: experiment
id: e-cn-mask
title: Exclude CN and C4668 regions
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
---

## Context

Exclude rest-frame 4142–4177 and 4634–4720 Angstrom windows. All other settings follow the documented poly3_total reference.

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
    "id": "mask-cn-m4-108989",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924,
    "target": "M4_108989"
  },
  {
    "id": "mask-cn-m5-172669",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830,
    "target": "M5_172669"
  },
  {
    "id": "mask-cn-m5-173928",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970,
    "target": "M5_173928"
  },
  {
    "id": "mask-cn-m12-185653",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923,
    "target": "M12_185653"
  },
  {
    "id": "mask-cn-m1-206545",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877,
    "target": "M1_206545"
  },
  {
    "id": "mask-cn-m12-98104",
    "arm": "mask_cn",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/execution.log"
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m12-185653",
    "target": "M12_185653",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M12_185653 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m12-185653",
    "target": "M12_185653",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M12_185653 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m12-185653",
    "target": "M12_185653",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M12_185653 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m12-185653",
    "target": "M12_185653",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M12_185653 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m12-185653",
    "target": "M12_185653",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M12_185653 · CN regions omitted. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m12-98104",
    "target": "M12_98104",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M12_98104 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m12-98104",
    "target": "M12_98104",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M12_98104 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m12-98104",
    "target": "M12_98104",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M12_98104 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m12-98104",
    "target": "M12_98104",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M12_98104 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m12-98104",
    "target": "M12_98104",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M12_98104 · CN regions omitted. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m1-206545",
    "target": "M1_206545",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M1_206545 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m1-206545",
    "target": "M1_206545",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M1_206545 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m1-206545",
    "target": "M1_206545",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M1_206545 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m1-206545",
    "target": "M1_206545",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M1_206545 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m1-206545",
    "target": "M1_206545",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M1_206545 · CN regions omitted. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m4-108989",
    "target": "M4_108989",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M4_108989 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m4-108989",
    "target": "M4_108989",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M4_108989 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m4-108989",
    "target": "M4_108989",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M4_108989 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m4-108989",
    "target": "M4_108989",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M4_108989 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m4-108989",
    "target": "M4_108989",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M4_108989 · CN regions omitted. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m5-172669",
    "target": "M5_172669",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M5_172669 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m5-172669",
    "target": "M5_172669",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M5_172669 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m5-172669",
    "target": "M5_172669",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M5_172669 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m5-172669",
    "target": "M5_172669",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M5_172669 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m5-172669",
    "target": "M5_172669",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M5_172669 · CN regions omitted. Age and formed-mass fractions."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mask-cn-m5-173928",
    "target": "M5_173928",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M5_173928 · CN regions omitted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "mask-cn-m5-173928",
    "target": "M5_173928",
    "arm": "mask_cn",
    "view": "Fits",
    "caption": "M5_173928 · CN regions omitted. Photometry and residuals; bands and uncertainty model are those of this run."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "mask-cn-m5-173928",
    "target": "M5_173928",
    "arm": "mask_cn",
    "view": "SFH",
    "caption": "M5_173928 · CN regions omitted. Saved SFH and posterior interval."
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
    "notebook": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "mask-cn-m5-173928",
    "target": "M5_173928",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M5_173928 · CN regions omitted. Physical-parameter posterior."
  },
  {
    "notebook": "results/fit-accuracy-knobs/mask_cn/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "mask-cn-m5-173928",
    "target": "M5_173928",
    "arm": "mask_cn",
    "view": "Posteriors",
    "caption": "M5_173928 · CN regions omitted. Age and formed-mass fractions."
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

| Arm | Median delta spectral chi2 | Median delta photometric chi2 | Median delta ln Z |
| --- | ---: | ---: | ---: |
| mask_cn | -13.82 | -2.24 | not comparable |

[Verdict table](results/fit-accuracy-knobs/verdict.csv) · [Per-target comparisons](results/fit-accuracy-knobs/before-after.csv). Spectral chi2 uses common pixels at a fixed 3% calibration floor.

## Caveats

Removing spectral pixels changes the data. Parameter movement is a sensitivity result, not a validation criterion.

## References

- [Executed comparison](results/fit-accuracy-knobs/analysis.ipynb)
- [Saved arm settings](results/fit-accuracy-knobs/arms.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
