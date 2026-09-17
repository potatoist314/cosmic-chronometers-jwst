---
kind: experiment
id: e-calibration-order
title: Higher-order calibration polynomials
date: 2026-09-15
origin: new
status: results-ready
question: q-fitting-choices
follow_up:
result_groups: results/calibration-order
---

## Context

Roadmap item `calibration-polynomial` (priority 9): polynomial modes must not be shorter than 100 \(\text{\AA}\); the empirical rule is order \(\approx\) wavelength range / 100. Every DR2 fit uses Chebyshev order 3 with coefficient prior \(\operatorname{Normal}(0,0.1)\), integrated out at each likelihood call. The fitted observed-frame spans of the six reference targets are 2416–2473 \(\text{\AA}\), so order 3 has a shortest bend of about 800 \(\text{\AA}\).

## Before delegation

```json
[
  {
    "date": "2026-09-15",
    "text": "Read and understand the codebase. After that, let's try experimenting with higher order calibration polynomials."
  },
  {
    "date": "2026-09-15",
    "text": "25 is too much, try 5 and 10 first. which galaxies will you run and which arms? 5060ti also works if it is under 10 cents an hour and >99.5%, both 8gb and 16gb variants (vram doesn't make a difference)",
    "display_text": "25 is too much, try 5 and 10 first. Which galaxies will you run and which arms? A 5060 Ti also works if it is under 10 cents an hour and >99.5%, both 8 GB and 16 GB variants (VRAM doesn't make a difference)."
  },
  {
    "date": "2026-09-15",
    "text": "what's mock tilt 4? 6+2 -> how did it become 14?",
    "display_text": "What's mock tilt 4? 6+2, how did it become 14?"
  },
  {
    "date": "2026-09-15",
    "text": "is photometry same for mock tilt galaxo",
    "display_text": "Is the photometry the same for the mock tilt galaxy?"
  },
  {
    "date": "2026-09-15",
    "text": "how would you rate the importance of these mock tilts",
    "display_text": "How would you rate the importance of these mock tilts?"
  },
  {
    "date": "2026-09-15",
    "text": "remove the 4% tilt arms, don't add anything else either",
    "display_text": "Remove the 4% tilt arms; don't add anything else either."
  },
  {
    "date": "2026-09-15",
    "text": "remove from the project not just the plan",
    "display_text": "Remove from the project, not just the plan."
  }
]
```

## Execution plan

- Comparison: Chebyshev order 5 and order 10 against the stored order-3 `new_default` fits.
- Baseline: `results/fit-accuracy-knobs/new_default/` (order 3, cosmos_total, StudentT SFH prior, free dust index, seed rule base 20260830). Not rerun.
- Data: the six reference targets M12_98104, M5_173928, M12_185653, M4_108989, M1_206545, M5_172669 (`DEFAULT_TARGETS` in `scripts/calibration_arms_vast.py`); LEGA-C DR2 spectra with cosmos_total photometry.
- Model: production notebook `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, aMIST/C3K alpha-enhanced grid, BlackJAX NSS (num_live 500, num_inner_steps 65, num_delete 100, logZ_tol −5).
- Controlled change: `CERIDWEN_CALIBRATION_ORDER` 5 or 10; arms `poly5`, `poly10` = `new_default` plus the order. Prior width 0.1 unchanged.
- No mock arms. The tilt-4 mock arms were removed from the driver on 2026-09-15.
- Hardware: one Vast.ai RTX 5060 or 5060 Ti (8 or 16 GB), under $0.10/h, reliability above 99.5%; results in `results/calibration-order/<arm>/<object>-<target>/`.
- Analysis: `results/calibration-order/analysis.ipynb`. Per arm and target: polynomial shape \(P(\lambda)\) with feature marks, shortest mode length = span / order against 100 \(\text{\AA}\), coefficient magnitudes \(|a_n|\) against n, Occam term, photometric \(\chi^2\), raw spectral \(\chi^2\), dchi2_basew, \(\ln Z\), wall time; \(\tau_{\mathrm{dust}}\), \(t_{50}\) and mass-weighted age against the order-3 baseline; corner plots and SFH per fit.
- Requested outputs: `arms.csv`, figures, the executed notebook, a wiki note.
- 2026-09-15, after the order 5 and 10 fits: the stored order-3 baseline used \(\tau_{\mathrm{dust}} \sim \operatorname{Uniform}(0, 2)\) (prior narrowed to \(\operatorname{Uniform}(0, 0.2)\) in ceridwen c053f85 on 2026-09-07), so the `new_default` arm was rerun with the current prior into `results/calibration-order/new_default/` on the same Vast box and boot (instance 51132758, ceridwen 56505a6); the analysis notebook compares against that rerun.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "poly5-m12-98104",
    "arm": "poly5",
    "status": "complete",
    "target": "M12_98104",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20261007,
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-order/poly5/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/98104-M12_98104/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m12-98104",
    "arm": "poly10",
    "status": "complete",
    "target": "M12_98104",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20261007,
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-order/poly10/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/98104-M12_98104/execution.log"
      }
    ]
  },
  {
    "id": "poly5-m5-173928",
    "arm": "poly5",
    "status": "complete",
    "target": "M5_173928",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260970,
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-order/poly5/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/173928-M5_173928/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m5-173928",
    "arm": "poly10",
    "status": "complete",
    "target": "M5_173928",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260970,
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-order/poly10/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/173928-M5_173928/execution.log"
      }
    ]
  },
  {
    "id": "poly5-m12-185653",
    "arm": "poly5",
    "status": "complete",
    "target": "M12_185653",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260923,
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-order/poly5/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/185653-M12_185653/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m12-185653",
    "arm": "poly10",
    "status": "complete",
    "target": "M12_185653",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260923,
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-order/poly10/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/185653-M12_185653/execution.log"
      }
    ]
  },
  {
    "id": "poly5-m4-108989",
    "arm": "poly5",
    "status": "complete",
    "target": "M4_108989",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260924,
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-order/poly5/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/108989-M4_108989/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m4-108989",
    "arm": "poly10",
    "status": "complete",
    "target": "M4_108989",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260924,
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-order/poly10/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/108989-M4_108989/execution.log"
      }
    ]
  },
  {
    "id": "poly5-m1-206545",
    "arm": "poly5",
    "status": "complete",
    "target": "M1_206545",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260877,
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-order/poly5/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/206545-M1_206545/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m1-206545",
    "arm": "poly10",
    "status": "complete",
    "target": "M1_206545",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260877,
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-order/poly10/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/206545-M1_206545/execution.log"
      }
    ]
  },
  {
    "id": "poly5-m5-172669",
    "arm": "poly5",
    "status": "complete",
    "target": "M5_172669",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260830,
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-order/poly5/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly5/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly5/172669-M5_172669/execution.log"
      }
    ]
  },
  {
    "id": "poly10-m5-172669",
    "arm": "poly10",
    "status": "complete",
    "target": "M5_172669",
    "code": "4e82a1e",
    "model": "Ceridwen 30cc016 (working tree uploaded at launch)",
    "config": "results/calibration-order/vast_run_2026-09-15T194806+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260830,
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-order/poly10/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/poly10/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/poly10/172669-M5_172669/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m12-98104",
    "arm": "new_default",
    "status": "complete",
    "target": "M12_98104",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20261007,
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-order/new_default/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/98104-M12_98104/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m5-173928",
    "arm": "new_default",
    "status": "complete",
    "target": "M5_173928",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260970,
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/calibration-order/new_default/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/173928-M5_173928/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/173928-M5_173928/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m12-185653",
    "arm": "new_default",
    "status": "complete",
    "target": "M12_185653",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260923,
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/calibration-order/new_default/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/185653-M12_185653/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m4-108989",
    "arm": "new_default",
    "status": "complete",
    "target": "M4_108989",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260924,
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/calibration-order/new_default/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/108989-M4_108989/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/108989-M4_108989/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m1-206545",
    "arm": "new_default",
    "status": "complete",
    "target": "M1_206545",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260877,
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/calibration-order/new_default/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/206545-M1_206545/execution.log"
      }
    ]
  },
  {
    "id": "new-default-m5-172669",
    "arm": "new_default",
    "status": "complete",
    "target": "M5_172669",
    "code": "fc7380d",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-order/vast_run_2026-09-15T211257+0000.json",
    "data": "results/calibration-order/cells.json",
    "seed": 20260830,
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/calibration-order/new_default/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-order/new_default/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-order/new_default/172669-M5_172669/execution.log"
      }
    ]
  }
]
```

## Figures

```json
[
  {
    "path": "results/calibration-order/parameters-by-order.png",
    "view": "Comparison",
    "caption": "Posterior median and 16–84 range of mass, t50, dust, dust index, mass-weighted age and calibration noise floor for the six galaxies at orders 3, 5 and 10.",
    "target": ""
  },
  {
    "path": "results/calibration-order/polynomial-vectors.png",
    "view": "Comparison",
    "caption": "Calibration polynomial P(λ) by order and its difference from the order-3 median; dotted across masked pixels.",
    "target": ""
  },
  {
    "path": "results/calibration-order/coefficients.png",
    "view": "Comparison",
    "caption": "Posterior |a_n| against n per galaxy and order; dashed line is the prior width 0.1.",
    "target": ""
  },
  {
    "path": "results/calibration-order/sfh-histories.png",
    "view": "SFH",
    "caption": "Star-formation history and cumulative mass fraction for the six galaxies at orders 3, 5 and 10.",
    "target": ""
  },
  {
    "path": "results/calibration-order/fit-M12_98104.png",
    "view": "Fits",
    "caption": "M12_98104 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M12_98104"
  },
  {
    "path": "results/calibration-order/chi2-M12_98104.png",
    "view": "Fits",
    "caption": "M12_98104 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M12_98104"
  },
  {
    "path": "results/calibration-order/corner-M12_98104.png",
    "view": "Posteriors",
    "caption": "M12_98104 · posterior corner at orders 3, 5 and 10.",
    "target": "M12_98104"
  },
  {
    "path": "results/calibration-order/fit-M5_173928.png",
    "view": "Fits",
    "caption": "M5_173928 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M5_173928"
  },
  {
    "path": "results/calibration-order/chi2-M5_173928.png",
    "view": "Fits",
    "caption": "M5_173928 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M5_173928"
  },
  {
    "path": "results/calibration-order/corner-M5_173928.png",
    "view": "Posteriors",
    "caption": "M5_173928 · posterior corner at orders 3, 5 and 10.",
    "target": "M5_173928"
  },
  {
    "path": "results/calibration-order/fit-M4_108989.png",
    "view": "Fits",
    "caption": "M4_108989 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M4_108989"
  },
  {
    "path": "results/calibration-order/chi2-M4_108989.png",
    "view": "Fits",
    "caption": "M4_108989 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M4_108989"
  },
  {
    "path": "results/calibration-order/corner-M4_108989.png",
    "view": "Posteriors",
    "caption": "M4_108989 · posterior corner at orders 3, 5 and 10.",
    "target": "M4_108989"
  },
  {
    "path": "results/calibration-order/fit-M12_185653.png",
    "view": "Fits",
    "caption": "M12_185653 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M12_185653"
  },
  {
    "path": "results/calibration-order/chi2-M12_185653.png",
    "view": "Fits",
    "caption": "M12_185653 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M12_185653"
  },
  {
    "path": "results/calibration-order/corner-M12_185653.png",
    "view": "Posteriors",
    "caption": "M12_185653 · posterior corner at orders 3, 5 and 10.",
    "target": "M12_185653"
  },
  {
    "path": "results/calibration-order/fit-M1_206545.png",
    "view": "Fits",
    "caption": "M1_206545 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M1_206545"
  },
  {
    "path": "results/calibration-order/chi2-M1_206545.png",
    "view": "Fits",
    "caption": "M1_206545 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M1_206545"
  },
  {
    "path": "results/calibration-order/corner-M1_206545.png",
    "view": "Posteriors",
    "caption": "M1_206545 · posterior corner at orders 3, 5 and 10.",
    "target": "M1_206545"
  },
  {
    "path": "results/calibration-order/fit-M5_172669.png",
    "view": "Fits",
    "caption": "M5_172669 · spectrum and photometry with the order 3, 5 and 10 posterior medians.",
    "target": "M5_172669"
  },
  {
    "path": "results/calibration-order/chi2-M5_172669.png",
    "view": "Fits",
    "caption": "M5_172669 · pulls at the order-3 f_calib and cumulative raw χ² along the spectrum by order.",
    "target": "M5_172669"
  },
  {
    "path": "results/calibration-order/corner-M5_172669.png",
    "view": "Posteriors",
    "caption": "M5_172669 · posterior corner at orders 3, 5 and 10.",
    "target": "M5_172669"
  }
]
```

## Measurements

| Quantity | Measurement |
| --- | --- |
| Hardware | NVIDIA GeForce RTX 5060, Vast instance 51132758, one boot for all 18 fits |
| Sampler | BlackJAX NSS, num_live 500, num_inner_steps 65, num_delete 100 |
| \(\Delta \ln Z\), order 10 − 3 | +20, +555, +284, +29, +305, +427 (M12_98104, M5_173928, M4_108989, M12_185653, M1_206545, M5_172669) |
| \(\Delta \ln Z\), order 5 − 3 | +4, +224, +263, +23, −2, +82 (same order) |
| \(t_{50}\) order 3 / 10 [Gyr] | 4.05 / 4.07; 5.02 / 5.51; 4.84 / 5.15; 4.79 / 4.67; 5.10 / 6.07; 2.00 / 2.29 |
| \([\mathrm{Fe}/\mathrm{H}]\) order 3 / 10 | −0.58 / −0.38; −0.69 / −1.04; −0.14 / −0.28; −0.38 / −0.22; −0.23 / −0.42; +0.05 / −0.18 |
| \([\alpha/\mathrm{Fe}]\) order 3 / 10 | +0.12 / +0.06; −0.17 / −0.17; −0.19 / −0.18; +0.22 / +0.04; −0.20 / −0.12; +0.02 / +0.04 |
| \(t_{\mathrm{MW}}\) order 3 / 10 [Gyr] | 3.91 / 3.91; 4.76 / 5.50; 4.69 / 4.99; 4.70 / 4.60; 5.08 / 6.07; 2.21 / 2.72 |
| \(\tau_{\mathrm{dust}}\) median, all arms | 0.180–0.199 (prior upper bound 0.2) |
| Shortest mode at order 10 | 242–247 \(\text{\AA}\) observed, 125–154 \(\text{\AA}\) rest frame |
| Sampler wall time order 3 / 5 / 10 | 365–571 s / 406–643 s / 691–1033 s |

[Executed comparison](results/calibration-order/analysis.ipynb) · [Per-arm table](results/calibration-order/arms.csv) · [Change against order 3](results/calibration-order/before-after.csv)

## Results

The stored order-3 `new_default` fits in `results/fit-accuracy-knobs/new_default` used \(\tau_{\mathrm{dust}} \sim \mathrm{Uniform}(0, 2)\). The poly5/poly10 fits used the current \(\mathrm{Uniform}(0, 0.2)\) prior (ceridwen c053f85, 2026-09-07). The order-3 rerun in `results/calibration-order/new_default` used the current prior on the same Vast box and boot as orders 5 and 10. All values below use that rerun. Sources are `results/calibration-order/arms.csv` and `before-after.csv` from `analysis.ipynb`.

Values follow the galaxy order M12_98104, M5_173928, M4_108989, M12_185653, M1_206545, M5_172669. For order 10 minus order 3, \(\Delta\ln Z\) is +20, +555, +284, +29, +305, +427. The \(\ln Z\) errors are 0.2–0.4. For order 5 minus order 3, \(\Delta\ln Z\) is +4, +224, +263, +23, −2, +82.

At the order-3 \(f_{\mathrm{calib}}\), raw spectral \(\chi^2\) differences (`dchi2_refw`, order 10 minus 3) are −80, −1028, −577, −113, −529, −803. Photometric \(\chi^2\) values for order 3 / 10 are 25/15, 31/68, 17/21, 11/10, 64/46, 13/11.

The order 3 → 10 \(t_{50}\) values in Gyr are 4.05±0.53 → 4.07±0.55, 5.02±0.24 → 5.51±0.00, 4.84±0.21 → 5.15±0.16, 4.79±0.51 → 4.67±0.50, 5.10±0.06 → 6.07±0.01, 2.00±0.11 → 2.29±0.20. Shifts in units of the order-3 half-width are 0.0, 2.0, 1.5, −0.2, 17.3, 2.8. At order 10, \(\log_{10} M_*\) increases by 0.016–0.062 dex for five galaxies. The change for M12_185653 is −0.010 dex.

The \(\tau_{\mathrm{dust}}\) medians are 0.180–0.199 at every order, with a prior upper bound of 0.2. Dust index medians are −0.82 to −0.99 at every order for five galaxies. For M12_185653, they are −0.10, 0.05, 0.06.

The polynomial ratio \(P_{\max}/P_{\min}\) is 1.10–1.41 at order 3 and 1.14–1.68 at order 10. M5_173928 has an order-10 ratio of 1.68. The \(\max|a_n|\) values are 0.025–0.110, below the prior width 0.1 except for M1_206545 (0.107–0.110).

At the median model, the Occam term spans 0.10–0.33 nats at order 3 and 0.37–1.20 nats at order 10. The shortest mode at order 10 spans 242–247 \(\text{\AA}\) observed and 125–154 \(\text{\AA}\) rest. Every galaxy meets the 100 \(\text{\AA}\) observed-frame rule up to order 24.

Sampler wall times for order 3 / 5 / 10 are 365–571 s / 406–643 s / 691–1033 s. Order 10 takes 1.7–2.0x the order-3 time on the same boot. Order 3 used the new Chebyshev-moment arithmetic, while orders 5 and 10 used the old arithmetic (see the calibration-speedup note).

## Caveats

Each galaxy and order has one seed. At every order, \(\tau_{\mathrm{dust}}\) is at its prior edge and the dust index is at its lower bound in five of six galaxies. For M5_173928 and M1_206545, the order-10 \(t_{50}\) half-widths are 0.00–0.01 Gyr, with all mass in the oldest SFH bin.

Stored spectral \(\chi^2\) uses each fit’s own \(f_{\mathrm{calib}}\) and is not compared across arms. Orders 5 and 10 used ceridwen 30cc016, with the working tree uploaded at launch before the speed-up commit. Order 3 used 56505a6, which evaluates the same likelihood.

## References

- [Calibration polynomial dr2 · source note](wiki/notes/calibration-polynomial-dr2.md)
- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
- [Reference fits · new_default](results/fit-accuracy-knobs/new-defaults.ipynb)
- [Calibration polynomial order · note](wiki/notes/calibration-order.md)
- [Calibration polynomial speed-up · note](wiki/notes/calibration-speedup.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[
  {
    "date": "2026-09-17",
    "text": "order 10 has speedups implmented and should be the default for future fits.",
    "display_text": "Order 10 has speed-ups implemented and should be the default for future fits."
  }
]
```
