---
kind: experiment
id: e-calibration-speedup
title: Linear-in-order calibration polynomial arithmetic
date: 2026-09-15
origin: new
status: results-ready
question: q-compute
related_questions: q-fitting-choices
follow_up:
result_groups: results/calibration-speedup
---

## Context

The higher-order run (`e-calibration-order`) measured 66, 77 and 135 \(\mu\mathrm{s}\) per likelihood call at Chebyshev orders 3, 5 and 10 on one RTX 5060 Ti (M12_98104), about 58 \(\mu\mathrm{s}\) + 0.77 \(\mu\mathrm{s}\) \(\times\) \(\mathrm{order}^2\). The quadratic term is the `(n_pix, k, k)` Gram reduction in `PolynomialCalibration.normal_matrix`, followed by an LU solve and a separate slogdet of the same matrix. The replacement forms the Gram matrix from \(2k+1\) Chebyshev moments, \(N_{mn}=\tfrac12(M_{m+n}+M_{|m-n|})\), and takes \(\hat a\) and \(\ln|N|\) from one Cholesky factorisation. The likelihood value is unchanged.

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

- Code: `ceridwen/ceridwen/likelihood/calibration.py` at ceridwen commit 56505a6 (parent 46a9175): moment basis `chebvander(x, 2k)`, static index arrays \(m+n\) and \(|m-n|\), `jax.scipy.linalg.cho_solve`, \(\ln|N|=2\sum\log\operatorname{diag}L\).
- Tests: `ceridwen/tests/test_polynomial_calibration.py` — Gram matrix and gradient against the explicit \(D^\mathsf{T}D+\Sigma_p^{-1}\) at orders 1, 3, 7, 10, 24 (1e-10); `calibrate` against explicit `solve` + `slogdet` at orders 10 and 24 (1e-9).
- Timing: `scripts/benchmark_calibration_order.py` on one Vast.ai RTX 5060 / 5060 Ti (cap $0.11/h, reliability above 99.5%, inbound bandwidth under $5/TB). Same process and boot: old arithmetic (frozen `calibration_normal_reduce` + LU solve + slogdet) and new, orders 3, 5, 10, 24, 100 and 500 particles, `jax.jit(jax.vmap(loglike))`, median of 20 timed calls after one compile, joint M1_210210 likelihood (`build_joint_workload`).
- Refit: `poly10` M12_98104 with the new code through `scripts/calibration_arms_vast.py run --arms poly10 --targets M12_98104 --keep-instance`, `CERIDWEN_ARMS_RESULTS=results/calibration-speedup`; same NSS settings and seed rule as `e-calibration-order`. Compare \(\ln Z\), \(\tau_{\mathrm{dust}}\), \(t_{50}\) and wall time with `results/calibration-order/poly10/98104-M12_98104` (different boot).
- Analysis: `results/calibration-speedup/analysis.ipynb` — \(\mu\mathrm{s}\) per call by order and variant, speed-up ratio, refit fit/SFH/corner outputs, \(\ln Z\) and parameter deltas.

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
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed comparison",
        "path": "results/calibration-speedup/analysis.ipynb"
      },
      {
        "label": "timing-gpu.json",
        "path": "results/calibration-speedup/timing-gpu.json"
      },
      {
        "label": "benchmark.log",
        "path": "results/calibration-speedup/benchmark.log"
      },
      {
        "label": "timing.csv",
        "path": "results/calibration-speedup/timing.csv"
      }
    ],
    "code": "4e82a1e",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-speedup/timing-gpu.json",
    "data": "results/calibration-speedup/benchmark.log",
    "seed": 20260915
  },
  {
    "id": "poly10-m12-98104-new-arithmetic",
    "arm": "poly10",
    "status": "complete",
    "target": "M12_98104",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/calibration-speedup/poly10/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/calibration-speedup/poly10/98104-M12_98104/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/calibration-speedup/poly10/98104-M12_98104/execution.log"
      }
    ],
    "code": "4e82a1e",
    "model": "Ceridwen 56505a6",
    "config": "results/calibration-speedup/vast_run_2026-09-15T201420+0000.json",
    "data": "results/calibration-speedup/cells.json",
    "seed": 20261007
  }
]
```

## Figures

```json
[
  {
    "path": "results/calibration-speedup/timing-by-order.png",
    "view": "Comparison",
    "caption": "Microseconds per likelihood call against Chebyshev order, old and new arithmetic, 100 and 500 particles, one RTX 5060.",
    "target": ""
  },
  {
    "path": "results/calibration-speedup/fit-M12_98104.png",
    "view": "Fits",
    "caption": "M12_98104 · order 10. Spectrum and photometry with the old-code and new-code posterior medians.",
    "target": "M12_98104"
  },
  {
    "path": "results/calibration-speedup/sfh-M12_98104.png",
    "view": "SFH",
    "caption": "M12_98104 · order 10. Star-formation history and cumulative mass fraction, old and new code.",
    "target": "M12_98104"
  },
  {
    "path": "results/calibration-speedup/corner-M12_98104.png",
    "view": "Posteriors",
    "caption": "M12_98104 · order 10. Physical-parameter posterior, old and new code.",
    "target": "M12_98104"
  }
]
```

## Measurements

| Quantity | Measurement |
| --- | --- |
| Device | NVIDIA GeForce RTX 5060, jax 0.10.2, Vast instance 51132758 |
| Benchmark workload | Joint M1_210210 likelihood, 3523 spectral pixels, `jax.jit(jax.vmap(loglike))`, median of 20 calls |
| \(\mu\mathrm{s}\) per call, 100 particles, old / new | order 3: 16.7 / 16.4; order 5: 18.5 / 16.7; order 10: 35.9 / 17.1; order 24: 131.4 / 21.4 |
| \(\mu\mathrm{s}\) per call, 500 particles, old / new | order 3: 8.4 / 7.6; order 5: 10.5 / 7.7; order 10: 19.5 / 8.3; order 24: 76.2 / 9.9 |
| Summed log-likelihood, old vs new | identical at every order and particle count |
| Refit M12_98104 order 10, \(\ln Z\) old / new | 249687.64 ± 0.27 / 249688.02 ± 0.28 |
| Refit likelihood calls old / new | 5 347 784 / 5 315 506 |
| Refit sampler wall time old / new | 723 s / 393 s (1.84x) |
| Refit \(\tau_{\mathrm{dust}}\) old / new | 0.192 ± 0.009 / 0.192 ± 0.009 |
| Refit \(t_{50}\) old / new | 4.07 ± 0.55 / 4.01 ± 0.46 Gyr |

[Executed comparison](results/calibration-speedup/analysis.ipynb) · [Timing](results/calibration-speedup/timing.csv) · [Refit table](results/calibration-speedup/refit.csv)

## Results

The new arithmetic costs the same as the old at order 3, 2.1x to 2.4x less at order 10 and 6.1x to 7.7x less at order 24; an order-24 call costs 1.3x an order-3 call. The order-10 refit of M12_98104 on the same boot reproduces \(\ln Z\) within the sampler error and every parameter median within its interval, in 393 s instead of 723 s.

## Caveats

Benchmark cost per call (17 \(\mu\mathrm{s}\) at order 10) is below the sampler's cost per logical call (74 \(\mu\mathrm{s}\)); only the old/new ratio transfers. The refit is one target and one seed. The benchmark target M1_210210 is not one of the six reference galaxies.

## References

- [Calibration polynomial speed-up · wiki note](wiki/notes/calibration-speedup.md)

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
