---
kind: experiment
id: e-quiescent-speedups
title: Ten-galaxy production-defaults fits on the combined speedups
date: 2026-10-01
results_at: 2026-10-01T11:37:35+00:00
origin: existing
status: recorded
question: q-compute
result_groups: results/quiescent-test-set-speedups-2026-10-01
---

## Context

Ten galaxies from the existing quiescent-test-set were fitted using production defaults with combined speedups.

## Before delegation

```json
[
  {
    "date": "2026-10-01",
    "text": "get muse to run this new speedup with all the default settings (ask me if you're unfamiliar) on the test set of around 10 varied galaxies",
    "display_text": "Get muse to run this new speedup with all the default settings (ask me if you're unfamiliar) on the test set of around 10 varied galaxies."
  },
  {
    "date": "2026-10-01",
    "text": "put the results on the wiki for me to view",
    "display_text": "Put the results on the wiki for me to view."
  }
]
```

## Runs

```json
[
  {
    "id": "qss-prod-run-53684057-m1-210210",
    "arm": "fit",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m8-150848",
    "arm": "fit",
    "status": "complete",
    "target": "M8_150848",
    "artifacts": [
      {
        "label": "Executed fit · M8_150848",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m5-238314",
    "arm": "fit",
    "status": "complete",
    "target": "M5_238314",
    "artifacts": [
      {
        "label": "Executed fit · M5_238314",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/M5_238314_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m3-120308",
    "arm": "fit",
    "status": "complete",
    "target": "M3_120308",
    "artifacts": [
      {
        "label": "Executed fit · M3_120308",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m2-134021",
    "arm": "fit",
    "status": "complete",
    "target": "M2_134021",
    "artifacts": [
      {
        "label": "Executed fit · M2_134021",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m7-146213",
    "arm": "fit",
    "status": "complete",
    "target": "M7_146213",
    "artifacts": [
      {
        "label": "Executed fit · M7_146213",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m3-117010",
    "arm": "fit",
    "status": "complete",
    "target": "M3_117010",
    "artifacts": [
      {
        "label": "Executed fit · M3_117010",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m4-107370",
    "arm": "fit",
    "status": "complete",
    "target": "M4_107370",
    "artifacts": [
      {
        "label": "Executed fit · M4_107370",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m14-37219",
    "arm": "fit",
    "status": "complete",
    "target": "M14_37219",
    "artifacts": [
      {
        "label": "Executed fit · M14_37219",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  },
  {
    "id": "qss-prod-run-53684057-m8-161113",
    "arm": "fit",
    "status": "complete",
    "target": "M8_161113",
    "artifacts": [
      {
        "label": "Executed fit · M8_161113",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/execution.log"
      }
    ],
    "code": "a6fba80",
    "model": "Ceridwen 2d5edc9; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json",
    "seed": 20260832,
    "data": "results/quiescent-test-set-speedups-2026-10-01/run/manifest.json"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "Fits",
    "caption": "M1_210210 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "Fits",
    "caption": "M1_210210 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "SFH",
    "caption": "M1_210210 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M1_210210 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_150848 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_150848 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "SFH",
    "caption": "M8_150848 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M8_150848 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "Fits",
    "caption": "M5_238314 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "Fits",
    "caption": "M5_238314 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "SFH",
    "caption": "M5_238314 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M5_238314 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_120308 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_120308 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "SFH",
    "caption": "M3_120308 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M3_120308 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "Fits",
    "caption": "M2_134021 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "Fits",
    "caption": "M2_134021 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "SFH",
    "caption": "M2_134021 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M2_134021 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "Fits",
    "caption": "M7_146213 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "Fits",
    "caption": "M7_146213 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "SFH",
    "caption": "M7_146213 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M7_146213 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_117010 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_117010 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "SFH",
    "caption": "M3_117010 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M3_117010 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "Fits",
    "caption": "M4_107370 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "Fits",
    "caption": "M4_107370 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "SFH",
    "caption": "M4_107370 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M4_107370 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "Fits",
    "caption": "M14_37219 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "Fits",
    "caption": "M14_37219 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "SFH",
    "caption": "M14_37219 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M14_37219 — Posteriors, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "qss-prod-run-53684057-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_161113 — Spectrum, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "qss-prod-run-53684057-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_161113 — Photometry, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "qss-prod-run-53684057-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "SFH",
    "caption": "M8_161113 — SFH, using production defaults with combined speedups."
  },
  {
    "notebook": "results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "qss-prod-run-53684057-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "Posteriors",
    "caption": "M8_161113 — Posteriors, using production defaults with combined speedups."
  }
]
```

## Measurements

| Metric | Value | Source |
| --- | --- | --- |
| Sampling wall, median of 10 | 84.6 s | `ceridwen_result.h5` `samples.attrs[wall_time_s]` per target |
| Sampling wall, range | 67.6–96.1 s | `ceridwen_result.h5` `samples.attrs[wall_time_s]` per target |
| Invoice total | $0.237 ($0.224 GPU + $0.013 disk) | `results/quiescent-test-set-speedups-2026-10-01/run/charges.json` |

## Results

- Completed 2026-10-01 on Vast.ai RTX 5090 instance 53684057; destroyed.
- All ten cells complete. `validate_result` passes on all ten.
- Each executed notebook holds 9 PNG outputs.
- Saved figures per target: spectrum (cell 14, output 2), photometry (cell 14, output 0), physical corner (cell 20, output 0), SFH (cell 20, output 3).
- Sampling wall time: median 84.6 s; range 67.6–96.1 s.
- Compute: $0.237 invoiced ($0.224 GPU + $0.013 disk).

## Caveats

This run has one arm, fit, and no matched before/after comparison.

## References

- [q-compute](wiki/research/questions/q-compute.md)
- Run metadata: `results/quiescent-test-set-speedups-2026-10-01/run/manifest.json`, `results/quiescent-test-set-speedups-2026-10-01/run/charges.json`, `results/quiescent-test-set-speedups-2026-10-01/run-driver.log`; per-target notebooks and HDF5 under `results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/`.
