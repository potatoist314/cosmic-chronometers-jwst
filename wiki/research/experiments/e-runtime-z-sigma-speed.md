---
kind: experiment
id: e-runtime-z-sigma-speed
title: Wall time per fit with free z and sigma_star
date: 2026-09-21
origin: new
status: results-ready
question: q-compute
follow_up:
result_groups: results/runtime-z-sigma-speed
---

## Context

For `M1_210210`, order-10 GPU fits with fixed and free \(z\) and \(\sigma_\star\) took 468 s and 1502 s: likelihood calls rose 24%, from 8.42M to 10.46M, and cost per call rose from 56 to 144 \(\mu\mathrm{s}\) across different boots. Order 10 costs about 10% more per call than order 3. Free \(\sigma_\star\) uses two chained smoothers with repeated interpolation searches and taper construction; free \(z\) adds a `jnp.interp` search on the observed grid.

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "the new fits seem to take quite long? i remember wall time being around 7 minutes per fit, but i think it's gone up. how come, and can it be brought back then",
    "display_text": "The new fits seem to take quite long? I remember wall time being around 7 minutes per fit, but I think it's gone up. How come, and can it be brought back then?"
  }
]
```

## Execution plan

- Profile: `results/runtime-z-sigma-speed/analysis.ipynb`; Apple CPU, `jax` 0.11.1 x64, `jit(vmap)` over 100 prior draws, seed 20260921, order-10 joint likelihood, fastest median of eight interleaved rounds.
- Code: `ceridwen` commit `6707c05`, `Spectrum(baked_runtime=True)`; exact redshift lookup indices, precomputed smoothing interpolation and instrument taper, instrument FFT padding reduced from 32768 to 18432 for `M1_210210`.
- Tests: `ceridwen/tests/test_baked_runtime.py`; predictions and marginalised order-10 likelihood at 25 sampled points across three instrument routes; lookup interpolation at nodes, one ulp either side and outside the grid.
- Planned GPU benchmark: same-boot old/new comparison on one Vast.ai RTX 5060-class instance under $0.11/h, after Liu Hao approves.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "cpu-profile",
    "arm": "cpu-profile",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed profile",
        "path": "results/runtime-z-sigma-speed/analysis.ipynb"
      },
      {
        "label": "timing.csv",
        "path": "results/runtime-z-sigma-speed/timing.csv"
      },
      {
        "label": "parts.csv",
        "path": "results/runtime-z-sigma-speed/parts.csv"
      }
    ],
    "code": "1186d7d",
    "model": "Ceridwen 6707c05",
    "config": "results/runtime-z-sigma-speed/timing.csv",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921
  },
  {
    "id": "gpu-same-boot-old-vs-new",
    "arm": "timing",
    "status": "planned"
  }
]
```

## Figures

```json
[]
```

## Measurements

| Quantity | Measurement |
| --- | --- |
| Device | Apple CPU, jax 0.11.1 x64; `jax.jit(jax.vmap(loglike))` over 100 prior draws, order-10 joint M1_210210 likelihood |
| Pixels | 10992 model, 3904 after trimming, 6166 observed |
| \(\mu\mathrm{s}\) per call, fixed \(z\), \(\sigma_\star\) | 114 |
| \(\mu\mathrm{s}\) per call, free \(\sigma_\star\), current / baked | 192 / 163 |
| \(\mu\mathrm{s}\) per call, free \(z\), current / baked | 198 / 125 |
| \(\mu\mathrm{s}\) per call, free \(z\) and \(\sigma_\star\), current / baked with 2n pad / baked | 267 / 206 / 160 |
| Smoothing alone, one static Gaussian / chain current / chain baked | 20 / 104 / 62 \(\mu\mathrm{s}\) |
| Redshift stretch alone, `jnp.interp` / lookup table | 89 / 16 \(\mu\mathrm{s}\) |
| FFT pair alone, length 8192 / 32768 / 18432 | 17 / 67 / 34 \(\mu\mathrm{s}\) |
| Max \(|\Delta\ln L|\), baked against current, 100 prior draws | 2.8e-9 (relative 2e-14) |
| GPU fits, fixed / free, different boots | 468 s, 8.42M calls, 56 \(\mu\mathrm{s}\) / 1502 s, 10.46M calls, 144 \(\mu\mathrm{s}\) |

[Executed profile](results/runtime-z-sigma-speed/analysis.ipynb) · [Timing](results/runtime-z-sigma-speed/timing.csv) · [Parts](results/runtime-z-sigma-speed/parts.csv)

## Results

CPU cost with both parameters free fell from 267 to 160 \(\mu\mathrm{s}\) per call; fixed parameters cost 114 \(\mu\mathrm{s}\). The free/fixed ratio fell from 2.33x to 1.40x. Smoothing fell from 104 to 62 \(\mu\mathrm{s}\), and redshift interpolation from 89 to 16 \(\mu\mathrm{s}\).

Maximum absolute log-likelihood difference over 100 prior draws was 2.8e-9, with relative difference 2e-14. Prediction tests use 1e-9 relative tolerance. The `ceridwen` suite recorded 184 passed and 26 skipped.

## Caveats

- No GPU benchmark yet; CPU ratios are a guide. GPU boot-to-boot variance reaches 66%.
- `baked_runtime` defaults to `False`; fit defaults remain unchanged, with \(z\) and \(\sigma_\star\) free.
- The remaining 1.40x cost includes both the 18432-point instrument FFT and the 8192-point LOSVD FFT.
- `test_from_fsps_records_provenance` requires FSPS, which is not installed.

## References

- [Fixed fit log](results/m1-210210-reference/tau-0p2/poly10/210210-M1_210210/execution.log)
- [Free fit log](results/m1-210210-reference/tau-1/poly10/210210-M1_210210/execution.log)
- [Order timing](results/calibration-speedup/timing.csv)
- [Model note](wiki/notes/model.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
