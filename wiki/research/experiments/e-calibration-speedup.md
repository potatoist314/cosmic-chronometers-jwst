---
kind: experiment
id: e-calibration-speedup
title: Linear-in-order calibration polynomial arithmetic
date: 2026-09-15
origin: new
status: planned
question: q-compute
related_questions: q-fitting-choices
follow_up:
---

## Context

The higher-order run (`e-calibration-order`) measured 66, 77 and 135 µs per likelihood call at Chebyshev orders 3, 5 and 10 on one RTX 5060 Ti (M12_98104), about 58 µs + 0.77 µs × order². The quadratic term is the `(n_pix, k, k)` Gram reduction in `PolynomialCalibration.normal_matrix`, followed by an LU solve and a separate slogdet of the same matrix. The replacement forms the Gram matrix from 2k + 1 Chebyshev moments, `N_mn = ½ (M_{m+n} + M_{|m−n|})`, and takes â and ln|N| from one Cholesky factorisation. The likelihood value is unchanged.

## Before delegation

```json
[
  {
    "date": "2026-09-15",
    "text": "i didn't realise the calibration polynomial slowed things down so much. you can't evaluate a fixed polynomial from the start for the galaxy?",
    "display_text": "I didn't realise the calibration polynomial slowed things down so much. You can't evaluate a fixed polynomial from the start for the galaxy?"
  },
  {
    "date": "2026-09-15",
    "text": "can you look into whether you can optimise the calibration polynomial calculations?",
    "display_text": "Can you look into whether you can optimise the calibration polynomial calculations?"
  }
]
```

## Execution plan

- Code: `ceridwen/ceridwen/likelihood/calibration.py` at ceridwen commit 56505a6 (parent 46a9175): moment basis `chebvander(x, 2k)`, static index arrays m+n and |m−n|, `jax.scipy.linalg.cho_solve`, ln|N| = 2 Σ log diag L.
- Tests: `ceridwen/tests/test_polynomial_calibration.py` — Gram matrix and gradient against the explicit `DᵀD + Σ_p⁻¹` at orders 1, 3, 7, 10, 24 (1e-10); `calibrate` against explicit `solve` + `slogdet` at orders 10 and 24 (1e-9).
- Timing: `scripts/benchmark_calibration_order.py` on one Vast.ai RTX 5060 / 5060 Ti (cap $0.11/h, reliability above 99.5%, inbound bandwidth under $5/TB). Same process and boot: old arithmetic (frozen `calibration_normal_reduce` + LU solve + slogdet) and new, orders 3, 5, 10, 24, 100 and 500 particles, `jax.jit(jax.vmap(loglike))`, median of 20 timed calls after one compile, joint M1_210210 likelihood (`build_joint_workload`).
- Refit: `poly10` M12_98104 with the new code through `scripts/calibration_arms_vast.py run --arms poly10 --targets M12_98104 --keep-instance`, `CERIDWEN_ARMS_RESULTS=results/calibration-speedup`; same NSS settings and seed rule as `e-calibration-order`. Compare lnZ, τ_dust, t50 and wall time with `results/calibration-order/poly10/98104-M12_98104` (different boot).
- Analysis: `results/calibration-speedup/analysis.ipynb` — µs per call by order and variant, speed-up ratio, refit fit/SFH/corner outputs, lnZ and parameter deltas.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "timing-old-vs-new",
    "arm": "timing",
    "status": "planned"
  },
  {
    "id": "poly10-m12-98104-new-arithmetic",
    "arm": "poly10",
    "status": "planned",
    "target": "M12_98104"
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

- [Higher-order calibration polynomials](wiki/research/experiments/e-calibration-order.md)
- [Calibration reduction: matched production benchmark](wiki/research/experiments/e-calibration-speed.md)
- [Ceridwen likelihood and sampling](wiki/notes/ceridwen-likelihood-sampling.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
