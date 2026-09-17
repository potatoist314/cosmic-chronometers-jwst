---
kind: experiment
id: e-m1-210210-reference
title: M1_210210 reference fit at calibration order 10
date: 2026-09-17
origin: new
status: planned
question: q-fitting-choices
follow_up:
---

## Context

M1_210210 was chosen on 17 Sep 2026 for fitting under roadmap item strong-spectrum: LEGA-C DR2, \(z = 0.6542\), \(\sigma_\star = 260\,\mathrm{km/s}\), catalogue S/N 62.2, ranking third by S/N among 187 quiescent galaxies. It has Dn4000 1.817, HdeltaA 0.418 and Fe4383 3.455, and belongs to the Borghi et al. 2022 overlap. The production fit at `results/dr2-quiescent-new-defaults/210210-M1_210210` used Chebyshev calibration order 3; order 10 became the default on 17 Sep 2026, and no order-10 fit exists for this galaxy.

## Before delegation

```json
[
  {
    "date": "2026-09-17",
    "text": "i want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectoy.",
    "display_text": "I want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectory."
  },
  {
    "date": "2026-09-17",
    "text": "order 10 has speedups implmented and should be the default for future fits.",
    "display_text": "Order 10 has speed-ups implemented and should be the default for future fits."
  }
]
```

## Execution plan

- Comparison: fit order 10 against the stored order-3 production fit of M1_210210, using the same seed.
- Baseline: `results/dr2-quiescent-new-defaults/210210-M1_210210`; order 3; seed 20260832.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2015 `cosmos_total` photometry, 12 bands.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`; grid `amist_c3k_hr_krou_afe`; ceridwen `56505a6`; Student-t SFH prior; free dust index; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `CERIDWEN_CALIBRATION_ORDER=10`, arm `poly10` of `scripts/calibration_arms_vast.py`.
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%; `results/m1-210210-reference/poly10/210210-M1_210210/` with the executed notebook; a wiki note.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "poly10-seed20260832",
    "arm": "poly10",
    "status": "planned"
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

- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
- [Calibration polynomial order · note](wiki/notes/calibration-order.md)
- [Order-3 production fit](results/dr2-quiescent-new-defaults/210210-M1_210210/M1_210210_executed.ipynb)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
