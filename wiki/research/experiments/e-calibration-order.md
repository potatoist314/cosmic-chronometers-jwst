---
kind: experiment
id: e-calibration-order
title: Higher-order calibration polynomials
date: 2026-09-15
origin: new
status: running
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
    "status": "planned",
    "target": "M12_98104"
  },
  {
    "id": "poly10-m12-98104",
    "arm": "poly10",
    "status": "planned",
    "target": "M12_98104"
  },
  {
    "id": "poly5-m5-173928",
    "arm": "poly5",
    "status": "planned",
    "target": "M5_173928"
  },
  {
    "id": "poly10-m5-173928",
    "arm": "poly10",
    "status": "planned",
    "target": "M5_173928"
  },
  {
    "id": "poly5-m12-185653",
    "arm": "poly5",
    "status": "planned",
    "target": "M12_185653"
  },
  {
    "id": "poly10-m12-185653",
    "arm": "poly10",
    "status": "planned",
    "target": "M12_185653"
  },
  {
    "id": "poly5-m4-108989",
    "arm": "poly5",
    "status": "planned",
    "target": "M4_108989"
  },
  {
    "id": "poly10-m4-108989",
    "arm": "poly10",
    "status": "planned",
    "target": "M4_108989"
  },
  {
    "id": "poly5-m1-206545",
    "arm": "poly5",
    "status": "planned",
    "target": "M1_206545"
  },
  {
    "id": "poly10-m1-206545",
    "arm": "poly10",
    "status": "planned",
    "target": "M1_206545"
  },
  {
    "id": "poly5-m5-172669",
    "arm": "poly5",
    "status": "planned",
    "target": "M5_172669"
  },
  {
    "id": "poly10-m5-172669",
    "arm": "poly10",
    "status": "planned",
    "target": "M5_172669"
  }
]
```

## Figures

```json
[]
```

## Measurements

## Results

## Caveats

## References

- [Calibration polynomial dr2 · source note](wiki/notes/calibration-polynomial-dr2.md)
- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
- [Reference fits · new_default](results/fit-accuracy-knobs/new-defaults.ipynb)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
