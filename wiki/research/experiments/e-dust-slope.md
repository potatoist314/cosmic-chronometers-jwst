---
kind: experiment
id: e-dust-slope
title: Free and wider dust-slope priors
date: 2026-09-06
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: fit-accuracy-knobs
result_groups: results/fit-accuracy-knobs
features: diffuse_dust_index
finding: slope freed on [-1, 0.4] (dust_free arm): median delta photometric chi2 -10.65, ln Z +8.18
---

## Context

Free the attenuation slope on [-1, 0.4], then test a wider lower bound. All other settings follow the documented poly3_total reference.

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
    "id": "dust-free-m4-108989",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924,
    "target": "M4_108989"
  },
  {
    "id": "dust-free-m5-172669",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830,
    "target": "M5_172669"
  },
  {
    "id": "dust-free-m5-173928",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970,
    "target": "M5_173928"
  },
  {
    "id": "dust-free-m12-185653",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923,
    "target": "M12_185653"
  },
  {
    "id": "dust-free-m1-206545",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877,
    "target": "M1_206545"
  },
  {
    "id": "dust-free-m12-98104",
    "arm": "dust_free",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/execution.log"
      }
    ],
    "seed": 20261007,
    "target": "M12_98104"
  },
  {
    "id": "dust-wide-m4-108989",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/execution.log"
      }
    ],
    "seed": 20260924,
    "target": "M4_108989"
  },
  {
    "id": "dust-wide-m5-172669",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/execution.log"
      }
    ],
    "seed": 20260830,
    "target": "M5_172669"
  },
  {
    "id": "dust-wide-m5-173928",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/execution.log"
      }
    ],
    "seed": 20260970,
    "target": "M5_173928"
  },
  {
    "id": "dust-wide-m12-185653",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/execution.log"
      }
    ],
    "seed": 20260923,
    "target": "M12_185653"
  },
  {
    "id": "dust-wide-m1-206545",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/execution.log"
      }
    ],
    "seed": 20260877,
    "target": "M1_206545"
  },
  {
    "id": "dust-wide-m12-98104",
    "arm": "dust_wide",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/execution.log"
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
    "path": "results/fit-accuracy-knobs/nd-dust-index.png",
    "view": "Comparison",
    "caption": "Dust-slope posteriors for the combined revised settings; several approach the lower prior bound.",
    "target": ""
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m12-185653",
    "target": "M12_185653",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M12_185653 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m12-185653",
    "target": "M12_185653",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M12_185653 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m12-185653",
    "target": "M12_185653",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M12_185653 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m12-185653",
    "target": "M12_185653",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M12_185653 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_185653 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_185653 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m12-185653",
    "target": "M12_185653",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M12_185653 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m12-185653",
    "target": "M12_185653",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M12_185653 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M12_185653 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m12-185653",
    "target": "M12_185653",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M12_185653 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m12-185653",
    "target": "M12_185653",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M12_185653 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m12-185653",
    "target": "M12_185653",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M12_185653 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m12-185653",
    "target": "M12_185653",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M12_185653 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_185653 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/185653-M12_185653/M12_185653_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m12-185653",
    "target": "M12_185653",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_185653 · Ages · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m12-98104",
    "target": "M12_98104",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M12_98104 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m12-98104",
    "target": "M12_98104",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M12_98104 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m12-98104",
    "target": "M12_98104",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M12_98104 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m12-98104",
    "target": "M12_98104",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M12_98104 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_98104 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M12_98104 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m12-98104",
    "target": "M12_98104",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M12_98104 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m12-98104",
    "target": "M12_98104",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M12_98104 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M12_98104 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m12-98104",
    "target": "M12_98104",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M12_98104 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m12-98104",
    "target": "M12_98104",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M12_98104 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m12-98104",
    "target": "M12_98104",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M12_98104 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m12-98104",
    "target": "M12_98104",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M12_98104 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_98104 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/98104-M12_98104/M12_98104_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m12-98104",
    "target": "M12_98104",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M12_98104 · Ages · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m1-206545",
    "target": "M1_206545",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M1_206545 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m1-206545",
    "target": "M1_206545",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M1_206545 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m1-206545",
    "target": "M1_206545",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M1_206545 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m1-206545",
    "target": "M1_206545",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M1_206545 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M1_206545 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M1_206545 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m1-206545",
    "target": "M1_206545",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M1_206545 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m1-206545",
    "target": "M1_206545",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M1_206545 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M1_206545 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m1-206545",
    "target": "M1_206545",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M1_206545 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m1-206545",
    "target": "M1_206545",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M1_206545 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m1-206545",
    "target": "M1_206545",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M1_206545 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m1-206545",
    "target": "M1_206545",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M1_206545 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M1_206545 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/206545-M1_206545/M1_206545_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m1-206545",
    "target": "M1_206545",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M1_206545 · Ages · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m4-108989",
    "target": "M4_108989",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M4_108989 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m4-108989",
    "target": "M4_108989",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M4_108989 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m4-108989",
    "target": "M4_108989",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M4_108989 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m4-108989",
    "target": "M4_108989",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M4_108989 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M4_108989 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M4_108989 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m4-108989",
    "target": "M4_108989",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M4_108989 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m4-108989",
    "target": "M4_108989",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M4_108989 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M4_108989 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m4-108989",
    "target": "M4_108989",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M4_108989 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m4-108989",
    "target": "M4_108989",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M4_108989 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m4-108989",
    "target": "M4_108989",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M4_108989 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m4-108989",
    "target": "M4_108989",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M4_108989 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M4_108989 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/108989-M4_108989/M4_108989_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m4-108989",
    "target": "M4_108989",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M4_108989 · Ages · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m5-172669",
    "target": "M5_172669",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M5_172669 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m5-172669",
    "target": "M5_172669",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m5-172669",
    "target": "M5_172669",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M5_172669 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m5-172669",
    "target": "M5_172669",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_172669 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m5-172669",
    "target": "M5_172669",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M5_172669 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m5-172669",
    "target": "M5_172669",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M5_172669 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M5_172669 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m5-172669",
    "target": "M5_172669",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M5_172669 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m5-172669",
    "target": "M5_172669",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M5_172669 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m5-172669",
    "target": "M5_172669",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M5_172669 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m5-172669",
    "target": "M5_172669",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M5_172669 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_172669 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/172669-M5_172669/M5_172669_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m5-172669",
    "target": "M5_172669",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_172669 · Ages · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-free-m5-173928",
    "target": "M5_173928",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M5_173928 · Spectrum · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-free-m5-173928",
    "target": "M5_173928",
    "arm": "dust_free",
    "view": "Fits",
    "caption": "M5_173928 · Photometry · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "dust-wide-m5-173928",
    "target": "M5_173928",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M5_173928 · Spectrum · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "dust-wide-m5-173928",
    "target": "M5_173928",
    "arm": "dust_wide",
    "view": "Fits",
    "caption": "M5_173928 · Photometry · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_173928 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Fits",
    "caption": "M5_173928 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-free-m5-173928",
    "target": "M5_173928",
    "arm": "dust_free",
    "view": "SFH",
    "caption": "M5_173928 · SFH · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "dust-wide-m5-173928",
    "target": "M5_173928",
    "arm": "dust_wide",
    "view": "SFH",
    "caption": "M5_173928 · SFH · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "SFH",
    "caption": "M5_173928 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-free-m5-173928",
    "target": "M5_173928",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M5_173928 · Posteriors · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_free/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-free-m5-173928",
    "target": "M5_173928",
    "arm": "dust_free",
    "view": "Posteriors",
    "caption": "M5_173928 · Ages · dust_free: dust index free U(-1, 0.4); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "dust-wide-m5-173928",
    "target": "M5_173928",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M5_173928 · Posteriors · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/fit-accuracy-knobs/dust_wide/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "dust-wide-m5-173928",
    "target": "M5_173928",
    "arm": "dust_wide",
    "view": "Posteriors",
    "caption": "M5_173928 · Ages · dust_wide: dust-index prior U(-2, 0.5), SFH StudentT(0, 0.3, 2); otherwise as poly3_total."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_173928 · Photometry · poly3_total, reference."
  },
  {
    "notebook": "results/calibration-polynomial-dr2/poly3_total/173928-M5_173928/M5_173928_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "poly3-total-m5-173928",
    "target": "M5_173928",
    "arm": "poly3_total",
    "view": "Posteriors",
    "caption": "M5_173928 · Ages · poly3_total, reference."
  }
]
```

## Results

| Arm | Median delta spectral \(\chi^2\) | Median delta photometric \(\chi^2\) | Median delta \(\ln Z\) |
| --- | ---: | ---: | ---: |
| dust_free | -1.92 | -10.65 | 8.18 |

[Verdict table](results/fit-accuracy-knobs/verdict.csv) · [Per-target comparisons](results/fit-accuracy-knobs/before-after.csv). Spectral \(\chi^2\) uses common pixels at a fixed 3% calibration floor.

## Caveats

Several slopes follow the lower boundary when it moves.

## References

- [Executed comparison](results/fit-accuracy-knobs/analysis.ipynb)
- [Saved arm settings](results/fit-accuracy-knobs/arms.csv)
- [Attempt history](results/fit-accuracy-knobs/arms_manifest.json)
- [Fit accuracy knobs · source note](wiki/notes/fit-accuracy-knobs.md)
