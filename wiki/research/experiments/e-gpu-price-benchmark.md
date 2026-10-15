---
kind: experiment
id: e-gpu-price-benchmark
title: GPU likelihood rental cost
date: 2026-09-23
results_at: 2026-09-23T22:22:58+01:00
origin: new
benchmark: true
status: stopped
question: q-compute
follow_up:
result_groups: results/gpu-benchmark-2026-09-23
source_notes: gpu-benchmark-2026-09-23-failures
---

## Context

Speed ratios of RTX 5060 Ti, 5070, 5070 Ti, 5080 and 5090 (and 5060 if offered) on the current code, and the hourly price cap per card that keeps cost per likelihood call equal across cards.

## Before delegation

```json
[
  {
    "date": "2026-09-23",
    "text": "how much faster are 5070ti, 5080, 5090 than 5060 - then assign a price times that multiple for each of them, to maintain same efficiency across different models",
    "display_text": "How much faster are 5070 Ti, 5080, 5090 than 5060? Then assign a price times that multiple for each of them, to maintain same efficiency across different models."
  },
  {
    "date": "2026-09-23",
    "text": "sure, i could use more up to date measurements. be careful with unreliable machines that have issues like loading the images and such - they have a tendency to inflate cost too much",
    "display_text": "Sure, I could use more up to date measurements. Be careful with unreliable machines that have issues like loading the images and such; they have a tendency to inflate cost too much."
  }
]
```

## Execution plan

- Comparison: steady-state likelihood calls/s per card, two rentals on different hosts each; price cap per card is $0.11/h times its mean speed ratio to the RTX 5060 Ti.
- Workload: `scripts/benchmark_baked_runtime.py` on M1_210210 at production defaults (order-10 calibration polynomial, free z and sigma_star, baked_runtime on), 500 particles, 5 interleaved rounds of 10 timed vmapped calls after JIT warm-up, seed 20260921; calls/s is 1e6 over the median free_baked microseconds per call. `scripts/benchmark_ceridwen_vast.py run` (5000 fixed NSS calls) runs beside it for comparison with the August numbers.
- Code: branch `absorption-mask` at `b55ff78`, ceridwen `7f18311`; clean committed trees on every box.
- Hosts: verified offers, reliability above 0.995, at or under the provisional cap (5060/5060 Ti $0.11, 5070 $0.14, 5070 Ti $0.20, 5080 $0.25, 5090 $0.40/h); destroy if not running with ssh up within 8 minutes or prepare unfinished within 15 minutes; never retry a host; total spend cap $1.50.
- Outputs: raw JSON per rental under `results/gpu-benchmark-2026-09-23/`, `summary.json` and `table.md` with ratios and caps, total cost including failed rentals.

## Amendments

```json
[
  {
    "date": "2026-09-23",
    "text": "don't be so trigger happy in destroying instances - probably more expensive to give up partway through and reset. change the rule to do a super short approximation on if its cheaper to destroy and start new versus let it keep going, and pick the cheaper. dont strictly follow destroy within xx minutes"
  },
  {
    "date": "2026-09-23",
    "text": "it boggles the mind how it can vary so much. something must be wrong"
  }
]
```

## Runs

```json
[
  {
    "id": "rtx-5060-ti-host-87213",
    "arm": "RTX 5060 Ti",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 87213,
    "instance_id": 52261203,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5060-ti-host-87213.json"
      }
    ]
  },
  {
    "id": "rtx-5060-ti-host-92578",
    "arm": "RTX 5060 Ti",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 92578,
    "instance_id": 52263839,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5060-ti-host-92578.json"
      }
    ]
  },
  {
    "id": "rtx-5070-host-511119",
    "arm": "RTX 5070",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 511119,
    "instance_id": 52292035,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5070-host-511119.json"
      }
    ]
  },
  {
    "id": "rtx-5080-host-616858",
    "arm": "RTX 5080",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 616858,
    "instance_id": 52282106,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5080-host-616858.json"
      }
    ]
  },
  {
    "id": "rtx-5090-host-213578",
    "arm": "RTX 5090",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 213578,
    "instance_id": 52289523,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5090-host-213578.json"
      }
    ]
  },
  {
    "id": "rtx-5090-host-406325",
    "arm": "RTX 5090",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 406325,
    "instance_id": 52295242,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/sol/manifest.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Raw timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/sol/timing-rtx-5090-host-406325.json"
      }
    ]
  },
  {
    "id": "rtx-5090-host-622869-diagnostic",
    "arm": "RTX 5090 batch scaling",
    "status": "complete",
    "target": "M1_210210",
    "host_id": 622869,
    "instance_id": 52299029,
    "code": "c869309c374bb7976b4bb9729a0650043fbfb4f7",
    "model": "Ceridwen 1fae781; amist_c3k_hr_krou_afe grid",
    "config": "results/gpu-benchmark-2026-09-23/diagnostic/summary.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260921,
    "artifacts": [
      {
        "label": "Batch timing JSON",
        "path": "results/gpu-benchmark-2026-09-23/diagnostic/batches.json"
      },
      {
        "label": "One-second GPU log",
        "path": "results/gpu-benchmark-2026-09-23/diagnostic/nvidia-smi.csv"
      },
      {
        "label": "Hardware record",
        "path": "results/gpu-benchmark-2026-09-23/diagnostic/hardware.txt"
      }
    ]
  }
]
```

## Figures

```json
[]
```

## Measurements

| GPU | Rental $/h | Calls/s | Estimated sampler cost/fit ($) |
| --- | ---: | ---: | ---: |
| [RTX 5060 Ti](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.185 | 33,173 | 0.051 |
| [RTX 5070](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.210 | 44,179 | 0.044 |
| [RTX 5080](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.352 | 79,161 | 0.041 |
| [RTX 5090](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.485 | 148,930 | 0.030 |

### Speed relative to RTX 5090

| GPU | 23 Sep · likelihood calls/s | 30 Sep · 30 later sampler steps | 14 Oct · sampling |
| --- | ---: | ---: | ---: |
| RTX 3090 |  | [0.26](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/rtx-3090/run/out/solo30/summary.json) |  |
| RTX 4090 |  | [0.65](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/rtx-4090/run/out/solo30/summary.json) |  |
| RTX 5060 Ti | [0.22](results/gpu-benchmark-2026-09-23/sol/summary.json) | [0.28](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/rtx-5060-ti/run/out/solo30/summary.json) |  |
| RTX 5070 | [0.30](results/gpu-benchmark-2026-09-23/sol/summary.json) |  |  |
| RTX 5080 | [0.53](results/gpu-benchmark-2026-09-23/sol/summary.json) |  |  |
| RTX 5090 | [1.00](results/gpu-benchmark-2026-09-23/sol/summary.json) | [1.00](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/rtx-5090/run/out/solo30/summary.json) | [1.00](results/gpu-bench-modal-2026-10-14/REPORT.md) |
| Tesla V100 |  | [0.25](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/tesla-v100/run/out/solo30/summary.json) |  |
| T4 |  |  | [0.08 (0.08–0.08)](results/gpu-bench-modal-2026-10-14/summary.json) |
| L4 |  |  | [0.26 (0.26–0.26)](results/gpu-bench-modal-2026-10-14/summary.json) |
| A10 |  |  | [0.27 (0.27–0.30)](results/gpu-bench-modal-2026-10-14/summary.json) |
| L40S |  |  | [0.66 (0.65–0.68)](results/gpu-bench-modal-2026-10-14/summary.json) |
| A100 SXM4 (40 GB) |  | [0.91](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types/a100-sxm4/run/out/solo30/summary.json) | [1.19 (1.12–1.23)](results/gpu-bench-modal-2026-10-14/summary.json) |
| A100 SXM4 (80 GB) |  |  | [1.25 (1.21–1.32)](results/gpu-bench-modal-2026-10-14/summary.json) |
| RTX PRO 6000 |  |  | [0.89 (0.84–0.91)](results/gpu-bench-modal-2026-10-14/summary.json) |
| H100 |  |  | [1.90 (1.79–2.02)](results/gpu-bench-modal-2026-10-14/summary.json) |
| H200 |  |  | [1.94 (1.90–2.00)](results/gpu-bench-modal-2026-10-14/summary.json) |
| B200 |  |  | [2.31 (2.29–2.32)](results/gpu-bench-modal-2026-10-14/summary.json) |
| B300 |  |  | [0.66 (0.65–0.66)](results/gpu-bench-modal-2026-10-14/summary.json) |

- The 23 Sep, 30 Sep and 14 Oct columns differ in builds and workloads. Comparisons apply only within each column.
- The table shows relative sampling speeds from 14 Oct eight-fit median sampling times. Speed ranges use four container mean sampling times.
- The [14 Oct RTX 5090 anchor](results/gpu-bench-modal-2026-10-14/REPORT.md) is a single same-build fit on one Vast host. Sampling took 116.39 s.

## Results

Six of ten requested host measurements completed: two RTX 5060 Ti, one 5070, one 5080 and two 5090. The 5070 Ti has no measured host. [Price matrix and invoices](results/gpu-benchmark-2026-09-23/sol/summary.json) record $0.981 billed, including failed rentals. [Diagnostic summary](results/gpu-benchmark-2026-09-23/diagnostic/summary.json) records $0.087 billed for the separate 5090 test.

At batch 500 on diagnostic host 622869, GPU use was 96%; host dispatch took 0.196 ms of a 3.224 ms blocked call. Calls/s stayed between 147,676 and 151,955 from batch 500 to 8,000. The host CPU did not leave this GPU idle at those batch sizes.

The estimate uses three converged RTX 5060 Ti M1_210210 sampler times: 1,025 s and 1,064 s for [COSMOS2020 Classic and COSMOS2025](wiki/research/experiments/e-cosmos-photometry-refit.md), and 891.5 s for [emission off](wiki/research/experiments/e-emission-line-marginalisation.md). Their mean is 993.5 s.

Estimated time per card = 993.5 s × 33,173 / measured calls/s. Cost/fit = estimated time × rental $/h / 3,600. Setup, transfer, and postprocessing are excluded.

## Caveats

- Missing: one additional 5070 host, two 5070 Ti hosts and one additional 5080 host.
- The 5090 hosts measured 94,294 and 148,930 calls/s on different rentals. The diagnostic did not identify the cause of that spread.
- The displayed 5090 row excludes the 94,294 calls/s measurement.
- `nvidia-smi` activity is not SM occupancy. The batch-100 steady-use value has one one-second sample. The post-dispatch wait includes GPU work and launch overhead.
- The original execution plan above retains its pre-run price limits and fixed teardown times. Later user instructions replaced both; the saved runs used project commit `c869309c374bb7976b4bb9729a0650043fbfb4f7`.
- Since the 10 Oct 2026 Ceridwen upstream merge, `scripts/benchmark_baked_runtime.py` has no `baked_runtime` switch; its arms are fixed and free \(\sigma_\star\), without the speed-up fields.

## References

- [Price summary](results/gpu-benchmark-2026-09-23/sol/summary.json) · [Attempt manifest](results/gpu-benchmark-2026-09-23/sol/manifest.json)
- [Diagnostic timing](results/gpu-benchmark-2026-09-23/diagnostic/batches.json) · [One-second GPU log](results/gpu-benchmark-2026-09-23/diagnostic/nvidia-smi.csv) · [Hardware record](results/gpu-benchmark-2026-09-23/diagnostic/hardware.txt)
- [Failures and fixes](wiki/notes/gpu-benchmark-2026-09-23-failures.md) · [Benchmark method](scripts/benchmark_baked_runtime.py)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
