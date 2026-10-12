---
kind: experiment
id: e-ceridwen-upstream-merge
title: Ceridwen upstream merge: CPU equivalence, speed and GPU check
date: 2026-10-10
origin: existing
status: recorded
question: q-compute
result_groups: results/ceridwen-upstream-merge-2026-10-10
finding: Production CPU likelihoods were bitwise equal at 21 points for all 10 targets; CPU batch time fell from 203.6 ms to 159.8 ms.
---

## Context

Ceridwen `729fba6` merged upstream `cc8ac9d` (1.0.12) into local `speedups` `2d5edc9`, with local speed work and fixes ported. Comparisons covered CPU tests, likelihood equivalence and speed against `2d5edc9`, and GPU fits against the 1 Oct reference in `results/quiescent-test-set-speedups-2026-10-01`.

## Runs

```json
[
  {
    "id": "merge-run-55330097-m1-210210",
    "arm": "fit",
    "status": "failed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Bootstrap log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run/55330097-bootstrap.log"
      }
    ],
    "code": "b891d1a",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run/manifest.json",
    "error": "bootstrap grid probe refused the nebular grid; fixed in 4ca0b64"
  },
  {
    "id": "merge-run2-55330634-m1-210210",
    "arm": "fit",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-2/fits/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-2/fits/fit/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-2/fits/fit/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-2/fits/fit/210210-M1_210210/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-2/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-2/manifest.json"
  },
  {
    "id": "merge-ten-55332978-m1-210210",
    "arm": "fit",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m8-150848",
    "arm": "fit",
    "status": "complete",
    "target": "M8_150848",
    "artifacts": [
      {
        "label": "Executed fit · M8_150848",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/M8_150848_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m5-238314",
    "arm": "fit",
    "status": "complete",
    "target": "M5_238314",
    "artifacts": [
      {
        "label": "Executed fit · M5_238314",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/M5_238314_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m3-120308",
    "arm": "fit",
    "status": "complete",
    "target": "M3_120308",
    "artifacts": [
      {
        "label": "Executed fit · M3_120308",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/M3_120308_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m2-134021",
    "arm": "fit",
    "status": "complete",
    "target": "M2_134021",
    "artifacts": [
      {
        "label": "Executed fit · M2_134021",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/M2_134021_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m7-146213",
    "arm": "fit",
    "status": "complete",
    "target": "M7_146213",
    "artifacts": [
      {
        "label": "Executed fit · M7_146213",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/M7_146213_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m3-117010",
    "arm": "fit",
    "status": "complete",
    "target": "M3_117010",
    "artifacts": [
      {
        "label": "Executed fit · M3_117010",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/M3_117010_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m4-107370",
    "arm": "fit",
    "status": "complete",
    "target": "M4_107370",
    "artifacts": [
      {
        "label": "Executed fit · M4_107370",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/M4_107370_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m14-37219",
    "arm": "fit",
    "status": "complete",
    "target": "M14_37219",
    "artifacts": [
      {
        "label": "Executed fit · M14_37219",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/M14_37219_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  },
  {
    "id": "merge-ten-55335713-m8-161113",
    "arm": "fit",
    "status": "complete",
    "target": "M8_161113",
    "artifacts": [
      {
        "label": "Executed fit · M8_161113",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/M8_161113_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/execution.log"
      }
    ],
    "code": "4ca0b64",
    "model": "Ceridwen 729fba6; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json",
    "seed": 20260832,
    "data": "results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55332978-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55332978-m1-210210",
    "target": "M1_210210",
    "arm": "fit",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_150848 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/150848-M8_150848/M8_150848_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m8-150848",
    "target": "M8_150848",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_150848 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "Fits",
    "caption": "M5_238314 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/238314-M5_238314/M5_238314_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m5-238314",
    "target": "M5_238314",
    "arm": "fit",
    "view": "Fits",
    "caption": "M5_238314 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_120308 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/120308-M3_120308/M3_120308_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m3-120308",
    "target": "M3_120308",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_120308 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "Fits",
    "caption": "M2_134021 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/134021-M2_134021/M2_134021_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m2-134021",
    "target": "M2_134021",
    "arm": "fit",
    "view": "Fits",
    "caption": "M2_134021 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "Fits",
    "caption": "M7_146213 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/146213-M7_146213/M7_146213_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m7-146213",
    "target": "M7_146213",
    "arm": "fit",
    "view": "Fits",
    "caption": "M7_146213 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_117010 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/117010-M3_117010/M3_117010_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m3-117010",
    "target": "M3_117010",
    "arm": "fit",
    "view": "Fits",
    "caption": "M3_117010 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "Fits",
    "caption": "M4_107370 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/107370-M4_107370/M4_107370_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m4-107370",
    "target": "M4_107370",
    "arm": "fit",
    "view": "Fits",
    "caption": "M4_107370 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "Fits",
    "caption": "M14_37219 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/37219-M14_37219/M14_37219_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m14-37219",
    "target": "M14_37219",
    "arm": "fit",
    "view": "Fits",
    "caption": "M14_37219 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "merge-ten-55335713-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_161113 · Spectrum · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  },
  {
    "notebook": "results/ceridwen-upstream-merge-2026-10-10/run-ten/fits/fit/161113-M8_161113/M8_161113_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "merge-ten-55335713-m8-161113",
    "target": "M8_161113",
    "arm": "fit",
    "view": "Fits",
    "caption": "M8_161113 · Photometry · ceridwen 729fba6 (upstream merge); reference: 1 Oct e-quiescent-speedups (ceridwen 2d5edc9); baked_runtime removed."
  }
]
```

## Measurements

| Config | Targets | Verdict | Max \(\lvert\Delta\ln L\rvert\) |
| --- | --- | --- | --- |
| production | 10/10 | bitwise | 0 |
| elines_off | 10/10 | bitwise | 0 |
| zevo_off | 10/10 | bitwise | 0 |
| afe_grid | 10/10 | bitwise | 0 |
| cal_order0 | 10/10 | bitwise | 0 |
| free_z | 10/10 | differs | 17.9 |
| baked_off | 0/10 | setting removed | |

| CPU production lnL, M1_210210, batch 128 | 2d5edc9 | 729fba6 | Ratio |
| --- | --- | --- | --- |
| ms per batch | 203.6 | 159.8 | 0.785 |

## Results

- `729fba6` had no merge-only CPU test failures. It shared upstream `cc8ac9d`’s 31 failures: missing FSPS, a pre-schema-2.0 grid file, and numerical tolerance.
- CPU float64 likelihoods were bitwise equal at 21 points per target for all 10 targets in `production`, `elines_off`, `zevo_off`, `afe_grid`, and `cal_order0`: \(\max|\Delta\ln L|=0\). The `Z`–`logzsol` mapping used a shift of 1.7328282715969863.
- For `M1_210210`, production CPU likelihood batches of 128 took 159.8 ms on `729fba6` versus 203.6 ms on `2d5edc9`; the time ratio was 0.785.
- All 11 RTX 5090 results passed `scripts.experiment.validate_result`. Total billed cost was $0.423.
- Two merged `M1_210210` fits on hosts `43746` and `568360` had bitwise-equal dead points: 16,700 samples and 5,375,929 likelihood calls. Log likelihoods differed by at most \(3.0\times10^{-7}\).
- For `M1_210210`, 1 Oct → merged: \(\ln Z\), \(236003.520\pm0.213\) → \(236003.678\pm0.362\); \([\mathrm{Fe}/\mathrm{H}]\), \(-0.120\;[-0.151,-0.091]\) → \(-0.121\;[-0.153,-0.091]\); `sigma_smooth`, 260.3 → 260.5 km/s. Every summary median shifted by at most 0.45 of its 1 Oct half-width.
- Across ten galaxies, the largest median shift per galaxy was 0.15–0.53 reference half-widths. \(|\Delta\ln Z|\) was 0.04–0.93 against nested-sampling error estimates of 0.13–0.36. Per-fit wall time was 1.07–1.31 times the 1 Oct time.

## Caveats

- `free_z`, outside production, differed by up to \(|\Delta\ln L|=17.9\). Upstream re-projects photometry at sampled redshift and uses its `SpectralProjector`.
- `baked_off` was unavailable after removal of `baked_runtime`. On `2d5edc9`, `baked_off` matched production within \(5.8\times10^{-11}\) in \(\ln L\).
- Merged dead points differed from the 1 Oct fit, which had 16,900 samples. GPU likelihoods were not compared point by point; CPU equality covered only 21 points per target.
- Wall times came from different hosts, not a same-boot comparison.
- 11 Oct `REPORT.md` decisions: keep local chain projector; production reads ceridwen's filter library; retain upstream base-grid refusal, cap base-grid `logzsol` prior at +0.25; production nebular grid has no refused cells. Pin `d7c0536`: comments only. Undecided: Noll bump, photometry broadening, polynomial marginal, `blackjax` floor, stale parent tests.

## References

- [Merge report](results/ceridwen-upstream-merge-2026-10-10/REPORT.md) · [Commit ledger](results/ceridwen-upstream-merge-2026-10-10/LEDGER.md)
- Run metadata: `results/ceridwen-upstream-merge-2026-10-10/run-2/manifest.json`, `results/ceridwen-upstream-merge-2026-10-10/run-ten/manifest.json`, `results/ceridwen-upstream-merge-2026-10-10/run-ten/charges.json`, `results/ceridwen-upstream-merge-2026-10-10/run-ten-driver.log`
- [1 Oct reference record](wiki/research/experiments/e-quiescent-speedups.md)
