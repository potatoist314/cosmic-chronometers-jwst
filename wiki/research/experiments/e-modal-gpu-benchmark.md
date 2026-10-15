---
kind: experiment
id: e-modal-gpu-benchmark
title: Modal datacentre GPU speed and cost per fit
date: 2026-10-14
results_at: 2026-10-15T01:11:43+01:00
origin: new
benchmark: true
status: results-ready
question: q-compute
follow_up:
result_groups: results/gpu-bench-modal-2026-10-14
---

## Context

Relative sampling speed and cost per fit of every Modal datacentre GPU type on one build.

## Before delegation

```json
[
  {
    "date": "2026-10-14",
    "text": "do benchmarks on the modal datacentre cards overnight. current relative benchmark results are all for consumer cards. absolute speed is not so important bc of speedup changes, relative speeds between cards is the important result",
    "display_text": "Do benchmarks on the Modal datacentre cards overnight. Current relative benchmark results are all for consumer cards. Absolute speed is not so important because of speedup changes; relative speeds between cards is the important result."
  },
  {
    "date": "2026-10-14",
    "text": "spend caps are lifted, no more caps given modal credits",
    "display_text": "Spend caps are lifted; no more caps given Modal credits."
  }
]
```

## Execution plan

- Workload: M1_210210, production defaults, seed 20260832.
- Build: `ce9752c`, Ceridwen `d7c0536`, sedpy_jax `9d8aa19`, notebook blob `0455b097`; image `sha256:e1c8846c…`.
- Replicates: 4 containers \(\times\) 2 fits per card; 11 cards, 88 fits.
- Timings: queue, boot, unpack + grid, bootstrap, model + grid cell, JIT compile, sampling, post-fit cells, retrieval.
- Reference: L40S; Modal’s “suggested starting point”, 48 GB, $1.95/h GPU price; `modal-gpu` example card.
- Cost: [Modal rates](https://modal.com/pricing), 2026-10-14; GPU + 2 CPU cores + 16 GiB memory. Sampling excludes JIT; one-fit container includes setup, grid read, bootstrap, full fit stage and packing; excludes queue.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "modal-t4",
    "arm": "T4",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-BJBlUR2l8c2ARfVU1SNac9",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/t4/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/t4/containers/0-fc-01M4Y7BQP7GJNPJH2V3R4MW24M/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/t4-driver.log"
      }
    ]
  },
  {
    "id": "modal-l4",
    "arm": "L4",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-zonnXUJbFtK6Esi7rIYWe3",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/l4/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/l4/containers/0-fc-01M4Y7BRX6718VVGYM2TF0GKZJ/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/l4-driver.log"
      }
    ]
  },
  {
    "id": "modal-a10",
    "arm": "A10",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-8vUulXsy94xHyp16ucf11I",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/a10/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/a10/containers/0-fc-01M4Y7BTF443TKCVM4RMWXJ70F/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/a10-driver.log"
      }
    ]
  },
  {
    "id": "modal-l40s",
    "arm": "L40S",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-xtXSsNP08AQAkdbaBN7nOp",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/l40s/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/l40s/containers/0-fc-01M4Y7BYXX1T75NHH30V1JNGJY/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/l40s-driver.log"
      }
    ]
  },
  {
    "id": "modal-a100-40gb",
    "arm": "A100-40GB",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-wwxvAvUFXbiZujuxSHNQJG",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/a100-40gb/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/a100-40gb/containers/0-fc-01M4Y7C4R1F4FWF52EDTZV5N0P/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/a100-40gb-driver.log"
      }
    ]
  },
  {
    "id": "modal-a100-80gb",
    "arm": "A100-80GB",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-MUuEzDODJxv1sIGIMxzMxP",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/a100-80gb/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/a100-80gb/containers/0-fc-01M4Y7CBFH42S37GETX5G5GKPN/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/a100-80gb-driver.log"
      }
    ]
  },
  {
    "id": "modal-rtx-pro-6000",
    "arm": "RTX-PRO-6000",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-lXZSHmyD2EgbSFg3mV98YM",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/rtx-pro-6000/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/rtx-pro-6000/containers/0-fc-01M4Y7CHFDBQXZAD3YPV5T04GA/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/rtx-pro-6000-driver.log"
      }
    ]
  },
  {
    "id": "modal-h100",
    "arm": "H100!",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-3aqOa2bmw33xFSOVYH8URg",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/h100/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/h100/containers/0-fc-01M4Y7CNQ82Q6YHGA4WT2GWERG/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/h100-driver.log"
      }
    ]
  },
  {
    "id": "modal-h200",
    "arm": "H200",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-isXsUWiLxTyN8fziB2Yw7y",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/h200/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/h200/containers/0-fc-01M4Y7CR72Y6AF9N77CWZVC1TZ/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/h200-driver.log"
      }
    ]
  },
  {
    "id": "modal-b200",
    "arm": "B200",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-bcjAnGaDGPftU5cQfu3w9q",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/b200/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/b200/containers/0-fc-01M4Y7D5XZHWW282R8BYZKGW1N/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/b200-driver.log"
      }
    ]
  },
  {
    "id": "modal-b300",
    "arm": "B300",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-nIzUkdfA8tGXF2vsymsRvL",
    "containers": 4,
    "fits_per_container": 2,
    "code": "ce9752cbe65d2a181746e9dd954fd0d3bf92b342",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Benchmark summary",
        "path": "results/gpu-bench-modal-2026-10-14/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/b300/manifest.json"
      },
      {
        "label": "Executed notebook, container 0 fit 0",
        "path": "results/gpu-bench-modal-2026-10-14/b300/containers/0-fc-01M4Y7CYKQH0NGS72JAD8DD2SH/results/fit-0/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/b300-driver.log"
      }
    ]
  },
  {
    "id": "modal-h100-shakedown",
    "arm": "H100!",
    "status": "complete",
    "target": "M1_210210",
    "modal_app_id": "ap-xqNn4uMEyzseuRBj4DpSjp",
    "containers": 1,
    "fits_per_container": 1,
    "code": "a7e67d4d8a787cdfd8552c508903354ff970257f",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "artifacts": [
      {
        "label": "Shakedown summary",
        "path": "results/gpu-bench-modal-2026-10-14/shakedown-a7e67d4/summary.json"
      },
      {
        "label": "Run manifest",
        "path": "results/gpu-bench-modal-2026-10-14/shakedown-a7e67d4/manifest.json"
      },
      {
        "label": "Driver log",
        "path": "results/gpu-bench-modal-2026-10-14/shakedown-a7e67d4-driver.log"
      }
    ]
  },
  {
    "id": "modal-all-cards-267a7b5",
    "arm": "all 11 cards",
    "status": "failed",
    "target": "M1_210210",
    "code": "267a7b54bccd3a7fff73dadfdb153ed5ceb46745",
    "model": "Ceridwen d7c0536, sedpy_jax 9d8aa19; amist_c3k_hr_krou_afe_nebular grid sha256 6fe00c55a177; image ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c0f06db1793ad788d46fcc99493cd9d5419aca4eecacce5fc30315c34",
    "config": "results/gpu-bench-modal-2026-10-14/experiment.json",
    "data": "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
    "seed": 20260832,
    "error": "L40S container reused warm by Modal: FileExistsError: [Errno 17] File exists: '/grids' -> '/workspace/cosmic-chronometers-jwst/grid'. Launch stopped on all 11 cards; the remaining calls ended with RemoteError after app stop.",
    "artifacts": [
      {
        "label": "L40S manifest",
        "path": "results/gpu-bench-modal-2026-10-14/aborted-267a7b5/l40s/manifest.json"
      },
      {
        "label": "L40S driver log",
        "path": "results/gpu-bench-modal-2026-10-14/aborted-267a7b5/l40s-driver.log"
      }
    ]
  }
]
```

## Measurements

| GPU | Modal $/h | Sampling speed vs L40S (container range) | Sampling s | Cost/fit vs L40S | Sampling $/fit | One-fit container $/fit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [B200](results/gpu-bench-modal-2026-10-14/summary.json) | 6.47 | 3.53 (3.49–3.55) | 50.3 | 0.84 | 0.0904 | 0.2851 |
| [H200](results/gpu-bench-modal-2026-10-14/summary.json) | 4.76 | 2.96 (2.90–3.06) | 60.0 | 0.74 | 0.0793 | 0.2247 |
| [H100 (`H100!`)](results/gpu-bench-modal-2026-10-14/summary.json) | 4.17 | 2.91 (2.74–3.08) | 61.1 | 0.66 | 0.0708 | 0.1832 |
| [A100-80GB](results/gpu-bench-modal-2026-10-14/summary.json) | 2.72 | 1.91 (1.84–2.01) | 92.8 | 0.65 | 0.0701 | 0.1796 |
| [A100-40GB](results/gpu-bench-modal-2026-10-14/summary.json) | 2.32 | 1.82 (1.70–1.87) | 97.8 | 0.59 | 0.0631 | 0.1489 |
| [RTX PRO 6000](results/gpu-bench-modal-2026-10-14/summary.json) | 3.25 | 1.35 (1.28–1.39) | 131.2 | 1.11 | 0.1185 | 0.2087 |
| [B300](results/gpu-bench-modal-2026-10-14/summary.json) | 7.32 | 1.00 (1.00–1.01) | 177.2 | 3.36 | 0.3603 | 0.6329 |
| [L40S](results/gpu-bench-modal-2026-10-14/summary.json) | 2.17 | 1.00 (0.99–1.03) | 177.6 | 1.00 | 0.1072 | 0.1607 |
| [A10](results/gpu-bench-modal-2026-10-14/summary.json) | 1.32 | 0.42 (0.41–0.46) | 423.3 | 1.45 | 0.1557 | 0.1916 |
| [L4](results/gpu-bench-modal-2026-10-14/summary.json) | 1.02 | 0.39 (0.39–0.40) | 450.0 | 1.19 | 0.1277 | 0.1712 |
| [T4](results/gpu-bench-modal-2026-10-14/summary.json) | 0.81 | 0.12 (0.12–0.12) | 1470.3 | 3.10 | 0.3319 | 0.3594 |

## Results

B200 fastest: 3.53\(\times\) L40S. A100-40GB cheapest per fit: $0.0631 sampling; $0.1489 one-fit container.

B300: 1.00\(\times\) L40S, 0.28\(\times\) B200; fits use float64. [NVIDIA HGX specifications](https://www.nvidia.com/en-us/data-center/hgx/): FP64 10 TFLOPS for B300, 296 TFLOPS for B200, both 8-GPU systems.

Container spread: 1–12%. Same-path fits agree across cards to float rounding. Across paths, \(\ln Z\) spans 0.61, median \(\sigma\) 0.24; posterior medians vary by at most 0.44\(\sigma\).

Same-build RTX 5090 tie: one Vast DR2 refit, 116.39 s sampling, 1.53\(\times\) L40S.

## Caveats

- Queue waits reflect the account limit: about 10 concurrent GPU containers; hillclimb used 3–5.
- Modal specifies B300 CUDA 13.1+; the pinned CUDA 12 image completed every fit.
- B200/B300 cuBLAS warning: versions below 13.2 may free TMEM buffers multiple times; concurrent kernels can silently corrupt data.
- `A10`: 3 A10 containers, 1 A10G; A10G sampled 8% faster.
- Likelihood harness dropped: `benchmark_baked_runtime.py` fails on emission lines shared with photometry.
- Old consumer benchmark untied: different build, grid and likelihood-harness workload.
- Not measured separately: `B200+`, `A100`, upgradeable `H100`; AMD MI355X absent from GPU guide, image CUDA-only.

## References

- [Report](results/gpu-bench-modal-2026-10-14/REPORT.md) · [Summary](results/gpu-bench-modal-2026-10-14/summary.json) · [Configuration](results/gpu-bench-modal-2026-10-14/experiment.json)
- [Benchmark driver](scripts/benchmark_modal.py) · [Modal pricing](https://modal.com/pricing) · [Modal GPU guide](https://modal.com/docs/guide/gpu) · [NVIDIA HGX](https://www.nvidia.com/en-us/data-center/hgx/)
- [RTX 5090 tie fit](results/dr2-refit-2026-10-12/part-02/run/manifest.json) · [Consumer benchmark](wiki/research/experiments/e-gpu-price-benchmark.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
