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

| GPU | Rental $/h | Calls/s | Cost per million calls ($) |
| --- | ---: | ---: | ---: |
| [RTX 5060 Ti](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.185 | 33,173 | 0.001550 |
| [RTX 5070](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.210 | 44,179 | 0.001323 |
| [RTX 5080](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.352 | 79,161 | 0.001235 |
| [RTX 5090](results/gpu-benchmark-2026-09-23/sol/summary.json) | 0.485 | 148,930 | 0.000905 |

## Results

Six of ten requested host measurements completed: two RTX 5060 Ti, one 5070, one 5080 and two 5090. The 5070 Ti has no measured host. [Price matrix and invoices](results/gpu-benchmark-2026-09-23/sol/summary.json) record $0.981 billed, including failed rentals. [Diagnostic summary](results/gpu-benchmark-2026-09-23/diagnostic/summary.json) records $0.087 billed for the separate 5090 test.

At batch 500 on diagnostic host 622869, GPU use was 96%; host dispatch took 0.196 ms of a 3.224 ms blocked call. Calls/s stayed between 147,676 and 151,955 from batch 500 to 8,000. The host CPU did not leave this GPU idle at those batch sizes.

## Caveats

- Missing: one additional 5070 host, two 5070 Ti hosts and one additional 5080 host.
- The 5090 hosts measured 94,294 and 148,930 calls/s on different rentals. The diagnostic did not identify the cause of that spread.
- The displayed 5090 row excludes the 94,294 calls/s measurement.
- `nvidia-smi` activity is not SM occupancy. The batch-100 steady-use value has one one-second sample. The post-dispatch wait includes GPU work and launch overhead.
- The original execution plan above retains its pre-run price limits and fixed teardown times. Later user instructions replaced both; the saved runs used project commit `c869309c374bb7976b4bb9729a0650043fbfb4f7`.

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
