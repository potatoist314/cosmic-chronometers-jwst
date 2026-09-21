---
kind: experiment
id: e-runtime-z-sigma-speed
title: Wall time per fit with free z and sigma_star
date: 2026-09-21
results_at: 2026-09-21T13:08:26+01:00
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
- GPU benchmark: Vast.ai RTX 5060 Ti, one process and boot, fixed/current/baked arms. M1_210210, order-10 joint likelihood, JAX 0.10.2 x64, `jit(vmap)`, 100/500 particles, 30 interleaved rounds, 20 timed calls per round, medians, seed 20260921. Ceridwen `6707c05`, project `52b0373`. On demand at $0.1269/h; price cap raised from $0.11/h to $0.13/h for this rental only.

## Amendments

```json
[
  {
    "date": "2026-09-21",
    "text": "i approve the speedup changes, go forward with the test, make it default if it works",
    "display_text": "I approve the speedup changes; go forward with the test and make it default if it works."
  },
  {
    "date": "2026-09-21",
    "text": "go"
  }
]
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
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed GPU tables",
        "path": "results/runtime-z-sigma-speed/gpu-benchmark.ipynb"
      },
      {
        "label": "timing-gpu.json",
        "path": "results/runtime-z-sigma-speed/timing-gpu.json"
      },
      {
        "label": "benchmark-gpu.log",
        "path": "results/runtime-z-sigma-speed/benchmark-gpu.log"
      },
      {
        "label": "Vast rental record",
        "path": "results/runtime-z-sigma-speed/vast_run_2026-09-21T115913+0000.json"
      }
    ],
    "code": "52b0373",
    "model": "Ceridwen 6707c05",
    "config": "results/runtime-z-sigma-speed/timing-gpu.json",
    "data": "results/runtime-z-sigma-speed/benchmark-gpu.log",
    "seed": 20260921
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
| GPU device | RTX 5060 Ti, jax 0.10.2 x64, Vast instance 51906463, one boot; 30 interleaved rounds of 20 calls per arm |
| GPU \(\mu\mathrm{s}\) per call, 100 particles, fixed / current / baked | 18.5 / 45.4 / 31.3 (1.45x, rounds 1.445 to 1.456) |
| GPU \(\mu\mathrm{s}\) per call, 500 particles, fixed / current / baked | 16.3 / 45.9 / 30.0 (1.53x, rounds 1.528 to 1.535) |
| GPU max \(|\Delta\ln L|\), baked against current, 500 prior draws | 3.7e-9 (relative 1.0e-13) |
| Rental | $0.1269/h on demand, $0.0315 spent, instance destroyed |
| GPU fits, fixed / free, different boots | 468 s, 8.42M calls, 56 \(\mu\mathrm{s}\) / 1502 s, 10.46M calls, 144 \(\mu\mathrm{s}\) |

[Executed profile](results/runtime-z-sigma-speed/analysis.ipynb) · [Timing](results/runtime-z-sigma-speed/timing.csv) · [Parts](results/runtime-z-sigma-speed/parts.csv) · [GPU tables](results/runtime-z-sigma-speed/gpu-benchmark.ipynb) · [GPU timing](results/runtime-z-sigma-speed/timing-gpu.json)

## Results

CPU cost with both parameters free fell from 267 to 160 \(\mu\mathrm{s}\) per call; fixed parameters cost 114 \(\mu\mathrm{s}\). The free/fixed ratio fell from 2.33x to 1.40x. Smoothing fell from 104 to 62 \(\mu\mathrm{s}\), and redshift interpolation from 89 to 16 \(\mu\mathrm{s}\).

Maximum absolute log-likelihood difference over 100 prior draws was 2.8e-9, with relative difference 2e-14. Prediction tests use 1e-9 relative tolerance. The `ceridwen` suite recorded 184 passed and 26 skipped.

GPU fixed/current/baked costs: 18.5/45.4/31.3 \(\mu\mathrm{s}\)/call at 100 particles, 16.3/45.9/30.0 at 500. Speed-ups: 1.45x/1.53x. Across 500 draws, maximum |ΔlnL| was 3.7e-9, relative 1.0e-13, within tolerance. `Spectrum(baked_runtime=True)` became default in `5f2c316`, with notebook settings enabled. \(z\) and \(\sigma_\star\) remain free, with unchanged priors.

## Caveats

- No full fit rerun under the baked path. Wall time per fit remains unmeasured.
- GPU boot-to-boot variance reaches 66%.
- CPU free/fixed ratios fell from 2.33x to 1.40x. GPU ratios at 500 particles fell from 2.81x to 1.84x.
- The remaining CPU 1.40x cost includes the 18432-point instrument FFT and the 8192-point LOSVD FFT.
- Baked free GPU cost remains 1.84x fixed cost. Sampled \(\sigma_\star\) needs a second FFT.
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
