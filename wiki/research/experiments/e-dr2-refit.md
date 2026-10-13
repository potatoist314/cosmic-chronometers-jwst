---
kind: experiment
id: e-dr2-refit
title: Refit larger DR2 sample with newer settings
date: 2026-10-12
results_at: 2026-10-13T02:30:00+01:00
origin: new
status: results-ready
question: q-population-results
source_notes: dr2-refit-sample
result_groups: results/dr2-refit-2026-10-12
finding: 135 fitted; age 4.04 Gyr; USD 5.65 billed
---

## Context

Refit the September sample of 187 LEGA-C DR2 quiescent targets with October production defaults. Compare the fitted galaxies with their September results and the Borghi+22 catalogue.

## Before delegation

```json
[
  {
    "date": "2026-10-12",
    "text": "overnight you can do the big run on the full lega c sample set with the new default settings and try and extract useful parameters for the sample size (e.g. sfh t50, t80 t20 against age), age against redshift and such. not sure how much this will take but put spend cap at say 10 bucks",
    "display_text": "Overnight, do the big run on the full LEGA-C sample with the new default settings. Extract useful parameters for the sample (e.g. SFH t50, t80, t20 against age), age against redshift and such. Not sure how long this will take; put the spend cap at about 10 dollars."
  },
  {
    "date": "2026-10-12",
    "text": "big sample set is about 180+ galaxies. find a good way to present the data for the morning",
    "display_text": "The big sample is about 180+ galaxies. Find a good way to present the data for the morning."
  }
]
```

## Execution plan

- Sample: check production photometry; exclude 7 refused targets, leaving 180 fittable.
- Settings: absorption-mask `f273855`, Ceridwen `d7c0536`, SFH-basis fast path; nebular grid, COSMOS2025/2020 photometry, Ceridwen filters, 14 SFH bins, metallicity evolution, Noll and birth-cloud dust, free emission lines, absorption masks, calibration order 10; seed 20260832.
- Runner and lanes: `python3 scripts/experiment.py run <part>/experiment.json --gpu "RTX 5090"`; USD 1 per output directory, USD 10 task cap; 11 shards of 17 started; after photometry checks, remaining 179 re-dealt into `part-01..09`.
- Lane continuation: use already-booted instances; pass them to `part-10..16` before the runner cap; no re-rent after failed boot, upload or lane loss.
- Order: `fit_order` seed 20261013; seeded random order, then from 22:59 UTC stratify the remaining pool by \(z\) tertile × September \(\log M\) tertile.
- Stop rule: 12 Oct steer to stop near USD 0.30 credit and keep the fitted set unbiased in \(z\) and mass; actual stop at USD 0.55–0.70.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "shard-00-m5-172669",
    "arm": "fit",
    "status": "complete",
    "target": "M5_172669",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/172669-M5_172669/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/172669-M5_172669/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/172669-M5_172669/execution.log"
      }
    ],
    "code": "7033ef1",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/shard-00/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m10-233129",
    "arm": "fit",
    "status": "complete",
    "target": "M10_233129",
    "artifacts": [
      {
        "label": "Executed fit · M10_233129",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/233129-M10_233129/M10_233129_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/233129-M10_233129/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/233129-M10_233129/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/233129-M10_233129/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m1-210210",
    "arm": "fit",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/210210-M1_210210/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m12-181945",
    "arm": "fit",
    "status": "complete",
    "target": "M12_181945",
    "artifacts": [
      {
        "label": "Executed fit · M12_181945",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/181945-M12_181945/M12_181945_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/181945-M12_181945/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/181945-M12_181945/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/181945-M12_181945/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m2-133501",
    "arm": "fit",
    "status": "complete",
    "target": "M2_133501",
    "artifacts": [
      {
        "label": "Executed fit · M2_133501",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/133501-M2_133501/M2_133501_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/133501-M2_133501/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/133501-M2_133501/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/133501-M2_133501/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m14-38648",
    "arm": "fit",
    "status": "complete",
    "target": "M14_38648",
    "artifacts": [
      {
        "label": "Executed fit · M14_38648",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/38648-M14_38648/M14_38648_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/38648-M14_38648/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/38648-M14_38648/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/38648-M14_38648/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m9-233169",
    "arm": "fit",
    "status": "complete",
    "target": "M9_233169",
    "artifacts": [
      {
        "label": "Executed fit · M9_233169",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/233169-M9_233169/M9_233169_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/233169-M9_233169/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/233169-M9_233169/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/233169-M9_233169/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m2-134391",
    "arm": "fit",
    "status": "complete",
    "target": "M2_134391",
    "artifacts": [
      {
        "label": "Executed fit · M2_134391",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/134391-M2_134391/M2_134391_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/134391-M2_134391/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/134391-M2_134391/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/134391-M2_134391/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m8-160400",
    "arm": "fit",
    "status": "complete",
    "target": "M8_160400",
    "artifacts": [
      {
        "label": "Executed fit · M8_160400",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/160400-M8_160400/M8_160400_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/160400-M8_160400/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/160400-M8_160400/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/160400-M8_160400/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m1-205742",
    "arm": "fit",
    "status": "complete",
    "target": "M1_205742",
    "artifacts": [
      {
        "label": "Executed fit · M1_205742",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205742-M1_205742/M1_205742_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205742-M1_205742/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205742-M1_205742/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205742-M1_205742/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m10-213772",
    "arm": "fit",
    "status": "complete",
    "target": "M10_213772",
    "artifacts": [
      {
        "label": "Executed fit · M10_213772",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/213772-M10_213772/M10_213772_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/213772-M10_213772/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/213772-M10_213772/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/213772-M10_213772/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m8-150848",
    "arm": "fit",
    "status": "complete",
    "target": "M8_150848",
    "artifacts": [
      {
        "label": "Executed fit · M8_150848",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/150848-M8_150848/M8_150848_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/150848-M8_150848/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/150848-M8_150848/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/150848-M8_150848/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m8-161346",
    "arm": "fit",
    "status": "complete",
    "target": "M8_161346",
    "artifacts": [
      {
        "label": "Executed fit · M8_161346",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/161346-M8_161346/M8_161346_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/161346-M8_161346/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/161346-M8_161346/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/161346-M8_161346/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m8-162149",
    "arm": "fit",
    "status": "complete",
    "target": "M8_162149",
    "artifacts": [
      {
        "label": "Executed fit · M8_162149",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/162149-M8_162149/M8_162149_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/162149-M8_162149/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/162149-M8_162149/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/162149-M8_162149/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m7-113852",
    "arm": "fit",
    "status": "complete",
    "target": "M7_113852",
    "artifacts": [
      {
        "label": "Executed fit · M7_113852",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/113852-M7_113852/M7_113852_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/113852-M7_113852/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/113852-M7_113852/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/113852-M7_113852/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m4-105474",
    "arm": "fit",
    "status": "complete",
    "target": "M4_105474",
    "artifacts": [
      {
        "label": "Executed fit · M4_105474",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/105474-M4_105474/M4_105474_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/105474-M4_105474/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/105474-M4_105474/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/105474-M4_105474/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m10-228215",
    "arm": "fit",
    "status": "complete",
    "target": "M10_228215",
    "artifacts": [
      {
        "label": "Executed fit · M10_228215",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/228215-M10_228215/M10_228215_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/228215-M10_228215/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/228215-M10_228215/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/228215-M10_228215/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m11-218207",
    "arm": "fit",
    "status": "complete",
    "target": "M11_218207",
    "artifacts": [
      {
        "label": "Executed fit · M11_218207",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/218207-M11_218207/M11_218207_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/218207-M11_218207/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/218207-M11_218207/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/218207-M11_218207/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m10-216730",
    "arm": "fit",
    "status": "complete",
    "target": "M10_216730",
    "artifacts": [
      {
        "label": "Executed fit · M10_216730",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/216730-M10_216730/M10_216730_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/216730-M10_216730/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/216730-M10_216730/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/216730-M10_216730/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m13-232627",
    "arm": "fit",
    "status": "complete",
    "target": "M13_232627",
    "artifacts": [
      {
        "label": "Executed fit · M13_232627",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232627-M13_232627/M13_232627_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232627-M13_232627/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232627-M13_232627/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232627-M13_232627/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m10-228380",
    "arm": "fit",
    "status": "complete",
    "target": "M10_228380",
    "artifacts": [
      {
        "label": "Executed fit · M10_228380",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/228380-M10_228380/M10_228380_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/228380-M10_228380/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/228380-M10_228380/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/228380-M10_228380/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m4-117400",
    "arm": "fit",
    "status": "complete",
    "target": "M4_117400",
    "artifacts": [
      {
        "label": "Executed fit · M4_117400",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/117400-M4_117400/M4_117400_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/117400-M4_117400/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/117400-M4_117400/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/117400-M4_117400/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m11-257455",
    "arm": "fit",
    "status": "complete",
    "target": "M11_257455",
    "artifacts": [
      {
        "label": "Executed fit · M11_257455",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/257455-M11_257455/M11_257455_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/257455-M11_257455/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/257455-M11_257455/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/257455-M11_257455/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m11-215585",
    "arm": "fit",
    "status": "complete",
    "target": "M11_215585",
    "artifacts": [
      {
        "label": "Executed fit · M11_215585",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/215585-M11_215585/M11_215585_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/215585-M11_215585/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/215585-M11_215585/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/215585-M11_215585/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m3-119474",
    "arm": "fit",
    "status": "complete",
    "target": "M3_119474",
    "artifacts": [
      {
        "label": "Executed fit · M3_119474",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/119474-M3_119474/M3_119474_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/119474-M3_119474/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/119474-M3_119474/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/119474-M3_119474/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m2-206669",
    "arm": "fit",
    "status": "complete",
    "target": "M2_206669",
    "artifacts": [
      {
        "label": "Executed fit · M2_206669",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/206669-M2_206669/M2_206669_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/206669-M2_206669/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/206669-M2_206669/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/206669-M2_206669/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m1-211157",
    "arm": "fit",
    "status": "complete",
    "target": "M1_211157",
    "artifacts": [
      {
        "label": "Executed fit · M1_211157",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/211157-M1_211157/M1_211157_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/211157-M1_211157/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/211157-M1_211157/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/211157-M1_211157/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m12-102456",
    "arm": "fit",
    "status": "complete",
    "target": "M12_102456",
    "artifacts": [
      {
        "label": "Executed fit · M12_102456",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/102456-M12_102456/M12_102456_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/102456-M12_102456/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/102456-M12_102456/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/102456-M12_102456/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m11-221163",
    "arm": "fit",
    "status": "complete",
    "target": "M11_221163",
    "artifacts": [
      {
        "label": "Executed fit · M11_221163",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/221163-M11_221163/M11_221163_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/221163-M11_221163/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/221163-M11_221163/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/221163-M11_221163/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m1-206858",
    "arm": "fit",
    "status": "complete",
    "target": "M1_206858",
    "artifacts": [
      {
        "label": "Executed fit · M1_206858",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/206858-M1_206858/M1_206858_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/206858-M1_206858/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/206858-M1_206858/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/206858-M1_206858/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m5-205715",
    "arm": "fit",
    "status": "complete",
    "target": "M5_205715",
    "artifacts": [
      {
        "label": "Executed fit · M5_205715",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/205715-M5_205715/M5_205715_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/205715-M5_205715/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/205715-M5_205715/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/205715-M5_205715/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m8-148698",
    "arm": "fit",
    "status": "complete",
    "target": "M8_148698",
    "artifacts": [
      {
        "label": "Executed fit · M8_148698",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/148698-M8_148698/M8_148698_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/148698-M8_148698/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/148698-M8_148698/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/148698-M8_148698/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m11-229551",
    "arm": "fit",
    "status": "complete",
    "target": "M11_229551",
    "artifacts": [
      {
        "label": "Executed fit · M11_229551",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/229551-M11_229551/M11_229551_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/229551-M11_229551/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/229551-M11_229551/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/229551-M11_229551/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m5-236682",
    "arm": "fit",
    "status": "complete",
    "target": "M5_236682",
    "artifacts": [
      {
        "label": "Executed fit · M5_236682",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/236682-M5_236682/M5_236682_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/236682-M5_236682/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/236682-M5_236682/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/236682-M5_236682/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m1-206545",
    "arm": "fit",
    "status": "complete",
    "target": "M1_206545",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/206545-M1_206545/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/206545-M1_206545/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/206545-M1_206545/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m11-232962",
    "arm": "fit",
    "status": "complete",
    "target": "M11_232962",
    "artifacts": [
      {
        "label": "Executed fit · M11_232962",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/232962-M11_232962/M11_232962_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/232962-M11_232962/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/232962-M11_232962/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/232962-M11_232962/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m15-77745",
    "arm": "fit",
    "status": "complete",
    "target": "M15_77745",
    "artifacts": [
      {
        "label": "Executed fit · M15_77745",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/77745-M15_77745/M15_77745_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/77745-M15_77745/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/77745-M15_77745/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/77745-M15_77745/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m9-218701",
    "arm": "fit",
    "status": "complete",
    "target": "M9_218701",
    "artifacts": [
      {
        "label": "Executed fit · M9_218701",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/218701-M9_218701/M9_218701_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/218701-M9_218701/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/218701-M9_218701/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/218701-M9_218701/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m13-248217",
    "arm": "fit",
    "status": "complete",
    "target": "M13_248217",
    "artifacts": [
      {
        "label": "Executed fit · M13_248217",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/248217-M13_248217/M13_248217_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/248217-M13_248217/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/248217-M13_248217/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/248217-M13_248217/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m8-147539",
    "arm": "fit",
    "status": "complete",
    "target": "M8_147539",
    "artifacts": [
      {
        "label": "Executed fit · M8_147539",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/147539-M8_147539/M8_147539_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/147539-M8_147539/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/147539-M8_147539/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/147539-M8_147539/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m12-184916",
    "arm": "fit",
    "status": "complete",
    "target": "M12_184916",
    "artifacts": [
      {
        "label": "Executed fit · M12_184916",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/184916-M12_184916/M12_184916_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/184916-M12_184916/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/184916-M12_184916/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/184916-M12_184916/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m7-147849",
    "arm": "fit",
    "status": "complete",
    "target": "M7_147849",
    "artifacts": [
      {
        "label": "Executed fit · M7_147849",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/147849-M7_147849/M7_147849_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/147849-M7_147849/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/147849-M7_147849/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/147849-M7_147849/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m10-227516",
    "arm": "fit",
    "status": "complete",
    "target": "M10_227516",
    "artifacts": [
      {
        "label": "Executed fit · M10_227516",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/227516-M10_227516/M10_227516_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/227516-M10_227516/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/227516-M10_227516/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/227516-M10_227516/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m5-211347",
    "arm": "fit",
    "status": "complete",
    "target": "M5_211347",
    "artifacts": [
      {
        "label": "Executed fit · M5_211347",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/211347-M5_211347/M5_211347_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/211347-M5_211347/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/211347-M5_211347/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/211347-M5_211347/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m3-120308",
    "arm": "fit",
    "status": "complete",
    "target": "M3_120308",
    "artifacts": [
      {
        "label": "Executed fit · M3_120308",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/120308-M3_120308/M3_120308_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/120308-M3_120308/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/120308-M3_120308/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/120308-M3_120308/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m9-232005",
    "arm": "fit",
    "status": "complete",
    "target": "M9_232005",
    "artifacts": [
      {
        "label": "Executed fit · M9_232005",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232005-M9_232005/M9_232005_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232005-M9_232005/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232005-M9_232005/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/232005-M9_232005/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m10-225441",
    "arm": "fit",
    "status": "complete",
    "target": "M10_225441",
    "artifacts": [
      {
        "label": "Executed fit · M10_225441",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/225441-M10_225441/M10_225441_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/225441-M10_225441/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/225441-M10_225441/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/225441-M10_225441/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m1-139423",
    "arm": "fit",
    "status": "complete",
    "target": "M1_139423",
    "artifacts": [
      {
        "label": "Executed fit · M1_139423",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/139423-M1_139423/M1_139423_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/139423-M1_139423/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/139423-M1_139423/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/139423-M1_139423/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m14-31835",
    "arm": "fit",
    "status": "complete",
    "target": "M14_31835",
    "artifacts": [
      {
        "label": "Executed fit · M14_31835",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/31835-M14_31835/M14_31835_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/31835-M14_31835/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/31835-M14_31835/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/31835-M14_31835/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m9-213587",
    "arm": "fit",
    "status": "complete",
    "target": "M9_213587",
    "artifacts": [
      {
        "label": "Executed fit · M9_213587",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/213587-M9_213587/M9_213587_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/213587-M9_213587/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/213587-M9_213587/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/213587-M9_213587/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m13-246149",
    "arm": "fit",
    "status": "complete",
    "target": "M13_246149",
    "artifacts": [
      {
        "label": "Executed fit · M13_246149",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/246149-M13_246149/M13_246149_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/246149-M13_246149/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/246149-M13_246149/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/246149-M13_246149/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m10-231544",
    "arm": "fit",
    "status": "complete",
    "target": "M10_231544",
    "artifacts": [
      {
        "label": "Executed fit · M10_231544",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/231544-M10_231544/M10_231544_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/231544-M10_231544/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/231544-M10_231544/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/231544-M10_231544/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m5-128311",
    "arm": "fit",
    "status": "complete",
    "target": "M5_128311",
    "artifacts": [
      {
        "label": "Executed fit · M5_128311",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/128311-M5_128311/M5_128311_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/128311-M5_128311/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/128311-M5_128311/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/128311-M5_128311/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m7-122242",
    "arm": "fit",
    "status": "complete",
    "target": "M7_122242",
    "artifacts": [
      {
        "label": "Executed fit · M7_122242",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/122242-M7_122242/M7_122242_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/122242-M7_122242/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/122242-M7_122242/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/122242-M7_122242/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m2-134021",
    "arm": "fit",
    "status": "complete",
    "target": "M2_134021",
    "artifacts": [
      {
        "label": "Executed fit · M2_134021",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/134021-M2_134021/M2_134021_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/134021-M2_134021/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/134021-M2_134021/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/134021-M2_134021/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m3-119802",
    "arm": "fit",
    "status": "complete",
    "target": "M3_119802",
    "artifacts": [
      {
        "label": "Executed fit · M3_119802",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119802-M3_119802/M3_119802_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119802-M3_119802/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119802-M3_119802/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119802-M3_119802/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m5-165871",
    "arm": "fit",
    "status": "complete",
    "target": "M5_165871",
    "artifacts": [
      {
        "label": "Executed fit · M5_165871",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/165871-M5_165871/M5_165871_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/165871-M5_165871/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/165871-M5_165871/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/165871-M5_165871/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m6-237437",
    "arm": "fit",
    "status": "complete",
    "target": "M6_237437",
    "artifacts": [
      {
        "label": "Executed fit · M6_237437",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/237437-M6_237437/M6_237437_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/237437-M6_237437/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/237437-M6_237437/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/237437-M6_237437/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m13-244239",
    "arm": "fit",
    "status": "complete",
    "target": "M13_244239",
    "artifacts": [
      {
        "label": "Executed fit · M13_244239",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/244239-M13_244239/M13_244239_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/244239-M13_244239/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/244239-M13_244239/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/244239-M13_244239/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m5-238580",
    "arm": "fit",
    "status": "complete",
    "target": "M5_238580",
    "artifacts": [
      {
        "label": "Executed fit · M5_238580",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/238580-M5_238580/M5_238580_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/238580-M5_238580/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/238580-M5_238580/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/238580-M5_238580/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m3-109713",
    "arm": "fit",
    "status": "complete",
    "target": "M3_109713",
    "artifacts": [
      {
        "label": "Executed fit · M3_109713",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/109713-M3_109713/M3_109713_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/109713-M3_109713/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/109713-M3_109713/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/109713-M3_109713/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m3-117694",
    "arm": "fit",
    "status": "complete",
    "target": "M3_117694",
    "artifacts": [
      {
        "label": "Executed fit · M3_117694",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/117694-M3_117694/M3_117694_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/117694-M3_117694/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/117694-M3_117694/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/117694-M3_117694/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m13-230747",
    "arm": "fit",
    "status": "complete",
    "target": "M13_230747",
    "artifacts": [
      {
        "label": "Executed fit · M13_230747",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/230747-M13_230747/M13_230747_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/230747-M13_230747/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/230747-M13_230747/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/230747-M13_230747/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m15-88032",
    "arm": "fit",
    "status": "complete",
    "target": "M15_88032",
    "artifacts": [
      {
        "label": "Executed fit · M15_88032",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/88032-M15_88032/M15_88032_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/88032-M15_88032/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/88032-M15_88032/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/88032-M15_88032/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m9-229883",
    "arm": "fit",
    "status": "complete",
    "target": "M9_229883",
    "artifacts": [
      {
        "label": "Executed fit · M9_229883",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/229883-M9_229883/M9_229883_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/229883-M9_229883/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/229883-M9_229883/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/229883-M9_229883/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m13-243871",
    "arm": "fit",
    "status": "complete",
    "target": "M13_243871",
    "artifacts": [
      {
        "label": "Executed fit · M13_243871",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/243871-M13_243871/M13_243871_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/243871-M13_243871/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/243871-M13_243871/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/243871-M13_243871/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m12-180774",
    "arm": "fit",
    "status": "complete",
    "target": "M12_180774",
    "artifacts": [
      {
        "label": "Executed fit · M12_180774",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/180774-M12_180774/M12_180774_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/180774-M12_180774/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/180774-M12_180774/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/180774-M12_180774/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m12-185653",
    "arm": "fit",
    "status": "complete",
    "target": "M12_185653",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185653-M12_185653/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185653-M12_185653/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185653-M12_185653/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m14-27068",
    "arm": "fit",
    "status": "complete",
    "target": "M14_27068",
    "artifacts": [
      {
        "label": "Executed fit · M14_27068",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/27068-M14_27068/M14_27068_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/27068-M14_27068/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/27068-M14_27068/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/27068-M14_27068/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m11-216899",
    "arm": "fit",
    "status": "complete",
    "target": "M11_216899",
    "artifacts": [
      {
        "label": "Executed fit · M11_216899",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/216899-M11_216899/M11_216899_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/216899-M11_216899/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/216899-M11_216899/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/216899-M11_216899/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m14-37023",
    "arm": "fit",
    "status": "complete",
    "target": "M14_37023",
    "artifacts": [
      {
        "label": "Executed fit · M14_37023",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/37023-M14_37023/M14_37023_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/37023-M14_37023/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/37023-M14_37023/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/37023-M14_37023/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m4-107643",
    "arm": "fit",
    "status": "complete",
    "target": "M4_107643",
    "artifacts": [
      {
        "label": "Executed fit · M4_107643",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/107643-M4_107643/M4_107643_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/107643-M4_107643/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/107643-M4_107643/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/107643-M4_107643/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m4-123161",
    "arm": "fit",
    "status": "complete",
    "target": "M4_123161",
    "artifacts": [
      {
        "label": "Executed fit · M4_123161",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/123161-M4_123161/M4_123161_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/123161-M4_123161/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/123161-M4_123161/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/123161-M4_123161/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m7-147270",
    "arm": "fit",
    "status": "complete",
    "target": "M7_147270",
    "artifacts": [
      {
        "label": "Executed fit · M7_147270",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/147270-M7_147270/M7_147270_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/147270-M7_147270/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/147270-M7_147270/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/147270-M7_147270/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m9-212391",
    "arm": "fit",
    "status": "complete",
    "target": "M9_212391",
    "artifacts": [
      {
        "label": "Executed fit · M9_212391",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/212391-M9_212391/M9_212391_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/212391-M9_212391/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/212391-M9_212391/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/212391-M9_212391/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m6-237641",
    "arm": "fit",
    "status": "complete",
    "target": "M6_237641",
    "artifacts": [
      {
        "label": "Executed fit · M6_237641",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/237641-M6_237641/M6_237641_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/237641-M6_237641/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/237641-M6_237641/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/237641-M6_237641/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m7-146213",
    "arm": "fit",
    "status": "complete",
    "target": "M7_146213",
    "artifacts": [
      {
        "label": "Executed fit · M7_146213",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/146213-M7_146213/M7_146213_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/146213-M7_146213/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/146213-M7_146213/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/146213-M7_146213/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m11-214296",
    "arm": "fit",
    "status": "complete",
    "target": "M11_214296",
    "artifacts": [
      {
        "label": "Executed fit · M11_214296",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/214296-M11_214296/M11_214296_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/214296-M11_214296/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/214296-M11_214296/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/214296-M11_214296/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m6-233902",
    "arm": "fit",
    "status": "complete",
    "target": "M6_233902",
    "artifacts": [
      {
        "label": "Executed fit · M6_233902",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/233902-M6_233902/M6_233902_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/233902-M6_233902/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/233902-M6_233902/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/233902-M6_233902/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m7-120372",
    "arm": "fit",
    "status": "complete",
    "target": "M7_120372",
    "artifacts": [
      {
        "label": "Executed fit · M7_120372",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/120372-M7_120372/M7_120372_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/120372-M7_120372/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/120372-M7_120372/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/120372-M7_120372/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m9-227630",
    "arm": "fit",
    "status": "complete",
    "target": "M9_227630",
    "artifacts": [
      {
        "label": "Executed fit · M9_227630",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/227630-M9_227630/M9_227630_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/227630-M9_227630/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/227630-M9_227630/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/227630-M9_227630/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m2-129596",
    "arm": "fit",
    "status": "complete",
    "target": "M2_129596",
    "artifacts": [
      {
        "label": "Executed fit · M2_129596",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/129596-M2_129596/M2_129596_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/129596-M2_129596/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/129596-M2_129596/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/129596-M2_129596/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m3-117010",
    "arm": "fit",
    "status": "complete",
    "target": "M3_117010",
    "artifacts": [
      {
        "label": "Executed fit · M3_117010",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/117010-M3_117010/M3_117010_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/117010-M3_117010/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/117010-M3_117010/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/117010-M3_117010/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m2-130005",
    "arm": "fit",
    "status": "complete",
    "target": "M2_130005",
    "artifacts": [
      {
        "label": "Executed fit · M2_130005",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/130005-M2_130005/M2_130005_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/130005-M2_130005/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/130005-M2_130005/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/130005-M2_130005/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m1-208622",
    "arm": "fit",
    "status": "complete",
    "target": "M1_208622",
    "artifacts": [
      {
        "label": "Executed fit · M1_208622",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/208622-M1_208622/M1_208622_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/208622-M1_208622/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/208622-M1_208622/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/208622-M1_208622/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m4-107370",
    "arm": "fit",
    "status": "complete",
    "target": "M4_107370",
    "artifacts": [
      {
        "label": "Executed fit · M4_107370",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/107370-M4_107370/M4_107370_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/107370-M4_107370/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/107370-M4_107370/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/107370-M4_107370/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m10-215519",
    "arm": "fit",
    "status": "complete",
    "target": "M10_215519",
    "artifacts": [
      {
        "label": "Executed fit · M10_215519",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/215519-M10_215519/M10_215519_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/215519-M10_215519/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/215519-M10_215519/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/215519-M10_215519/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m12-92132",
    "arm": "fit",
    "status": "complete",
    "target": "M12_92132",
    "artifacts": [
      {
        "label": "Executed fit · M12_92132",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/92132-M12_92132/M12_92132_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/92132-M12_92132/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/92132-M12_92132/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/92132-M12_92132/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m7-152125",
    "arm": "fit",
    "status": "complete",
    "target": "M7_152125",
    "artifacts": [
      {
        "label": "Executed fit · M7_152125",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/152125-M7_152125/M7_152125_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/152125-M7_152125/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/152125-M7_152125/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/152125-M7_152125/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m6-240899",
    "arm": "fit",
    "status": "complete",
    "target": "M6_240899",
    "artifacts": [
      {
        "label": "Executed fit · M6_240899",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/240899-M6_240899/M6_240899_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/240899-M6_240899/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/240899-M6_240899/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/240899-M6_240899/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m11-214430",
    "arm": "fit",
    "status": "complete",
    "target": "M11_214430",
    "artifacts": [
      {
        "label": "Executed fit · M11_214430",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/214430-M11_214430/M11_214430_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/214430-M11_214430/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/214430-M11_214430/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/214430-M11_214430/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m1-126578",
    "arm": "fit",
    "status": "complete",
    "target": "M1_126578",
    "artifacts": [
      {
        "label": "Executed fit · M1_126578",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/126578-M1_126578/M1_126578_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/126578-M1_126578/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/126578-M1_126578/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/126578-M1_126578/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m14-37219",
    "arm": "fit",
    "status": "complete",
    "target": "M14_37219",
    "artifacts": [
      {
        "label": "Executed fit · M14_37219",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/37219-M14_37219/M14_37219_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/37219-M14_37219/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/37219-M14_37219/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/37219-M14_37219/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m4-84337",
    "arm": "fit",
    "status": "complete",
    "target": "M4_84337",
    "artifacts": [
      {
        "label": "Executed fit · M4_84337",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/84337-M4_84337/M4_84337_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/84337-M4_84337/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/84337-M4_84337/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/84337-M4_84337/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m13-259737",
    "arm": "fit",
    "status": "complete",
    "target": "M13_259737",
    "artifacts": [
      {
        "label": "Executed fit · M13_259737",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/259737-M13_259737/M13_259737_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/259737-M13_259737/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/259737-M13_259737/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/259737-M13_259737/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m14-103366",
    "arm": "fit",
    "status": "complete",
    "target": "M14_103366",
    "artifacts": [
      {
        "label": "Executed fit · M14_103366",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/103366-M14_103366/M14_103366_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/103366-M14_103366/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/103366-M14_103366/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/103366-M14_103366/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m5-205765",
    "arm": "fit",
    "status": "complete",
    "target": "M5_205765",
    "artifacts": [
      {
        "label": "Executed fit · M5_205765",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205765-M5_205765/M5_205765_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205765-M5_205765/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205765-M5_205765/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/205765-M5_205765/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m7-122025",
    "arm": "fit",
    "status": "complete",
    "target": "M7_122025",
    "artifacts": [
      {
        "label": "Executed fit · M7_122025",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/122025-M7_122025/M7_122025_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/122025-M7_122025/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/122025-M7_122025/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/122025-M7_122025/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m2-210940",
    "arm": "fit",
    "status": "complete",
    "target": "M2_210940",
    "artifacts": [
      {
        "label": "Executed fit · M2_210940",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/210940-M2_210940/M2_210940_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/210940-M2_210940/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/210940-M2_210940/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/210940-M2_210940/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m7-120488",
    "arm": "fit",
    "status": "complete",
    "target": "M7_120488",
    "artifacts": [
      {
        "label": "Executed fit · M7_120488",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/120488-M7_120488/M7_120488_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/120488-M7_120488/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/120488-M7_120488/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/120488-M7_120488/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m11-245864",
    "arm": "fit",
    "status": "complete",
    "target": "M11_245864",
    "artifacts": [
      {
        "label": "Executed fit · M11_245864",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/245864-M11_245864/M11_245864_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/245864-M11_245864/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/245864-M11_245864/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/245864-M11_245864/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m3-109843",
    "arm": "fit",
    "status": "complete",
    "target": "M3_109843",
    "artifacts": [
      {
        "label": "Executed fit · M3_109843",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/109843-M3_109843/M3_109843_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/109843-M3_109843/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/109843-M3_109843/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/109843-M3_109843/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m10-217020",
    "arm": "fit",
    "status": "complete",
    "target": "M10_217020",
    "artifacts": [
      {
        "label": "Executed fit · M10_217020",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/217020-M10_217020/M10_217020_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/217020-M10_217020/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/217020-M10_217020/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/217020-M10_217020/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m7-162587",
    "arm": "fit",
    "status": "complete",
    "target": "M7_162587",
    "artifacts": [
      {
        "label": "Executed fit · M7_162587",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/162587-M7_162587/M7_162587_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/162587-M7_162587/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/162587-M7_162587/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/162587-M7_162587/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m8-161113",
    "arm": "fit",
    "status": "complete",
    "target": "M8_161113",
    "artifacts": [
      {
        "label": "Executed fit · M8_161113",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/161113-M8_161113/M8_161113_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/161113-M8_161113/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/161113-M8_161113/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/161113-M8_161113/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m9-232890",
    "arm": "fit",
    "status": "complete",
    "target": "M9_232890",
    "artifacts": [
      {
        "label": "Executed fit · M9_232890",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/232890-M9_232890/M9_232890_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/232890-M9_232890/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/232890-M9_232890/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/232890-M9_232890/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m11-212718",
    "arm": "fit",
    "status": "complete",
    "target": "M11_212718",
    "artifacts": [
      {
        "label": "Executed fit · M11_212718",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/212718-M11_212718/M11_212718_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/212718-M11_212718/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/212718-M11_212718/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/212718-M11_212718/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m1-133240",
    "arm": "fit",
    "status": "complete",
    "target": "M1_133240",
    "artifacts": [
      {
        "label": "Executed fit · M1_133240",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/133240-M1_133240/M1_133240_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/133240-M1_133240/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/133240-M1_133240/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/133240-M1_133240/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m12-101830",
    "arm": "fit",
    "status": "complete",
    "target": "M12_101830",
    "artifacts": [
      {
        "label": "Executed fit · M12_101830",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/101830-M12_101830/M12_101830_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/101830-M12_101830/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/101830-M12_101830/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/101830-M12_101830/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m12-181421",
    "arm": "fit",
    "status": "complete",
    "target": "M12_181421",
    "artifacts": [
      {
        "label": "Executed fit · M12_181421",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/181421-M12_181421/M12_181421_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/181421-M12_181421/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/181421-M12_181421/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/181421-M12_181421/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m8-156118",
    "arm": "fit",
    "status": "complete",
    "target": "M8_156118",
    "artifacts": [
      {
        "label": "Executed fit · M8_156118",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/156118-M8_156118/M8_156118_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/156118-M8_156118/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/156118-M8_156118/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/156118-M8_156118/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m1-126153",
    "arm": "fit",
    "status": "complete",
    "target": "M1_126153",
    "artifacts": [
      {
        "label": "Executed fit · M1_126153",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/126153-M1_126153/M1_126153_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/126153-M1_126153/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/126153-M1_126153/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/126153-M1_126153/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m7-120758",
    "arm": "fit",
    "status": "complete",
    "target": "M7_120758",
    "artifacts": [
      {
        "label": "Executed fit · M7_120758",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/120758-M7_120758/M7_120758_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/120758-M7_120758/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/120758-M7_120758/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/120758-M7_120758/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m14-38646",
    "arm": "fit",
    "status": "complete",
    "target": "M14_38646",
    "artifacts": [
      {
        "label": "Executed fit · M14_38646",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/38646-M14_38646/M14_38646_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/38646-M14_38646/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/38646-M14_38646/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/38646-M14_38646/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m14-102968",
    "arm": "fit",
    "status": "complete",
    "target": "M14_102968",
    "artifacts": [
      {
        "label": "Executed fit · M14_102968",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/102968-M14_102968/M14_102968_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/102968-M14_102968/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/102968-M14_102968/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/102968-M14_102968/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m13-245763",
    "arm": "fit",
    "status": "complete",
    "target": "M13_245763",
    "artifacts": [
      {
        "label": "Executed fit · M13_245763",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/245763-M13_245763/M13_245763_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/245763-M13_245763/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/245763-M13_245763/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/245763-M13_245763/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m13-255047",
    "arm": "fit",
    "status": "complete",
    "target": "M13_255047",
    "artifacts": [
      {
        "label": "Executed fit · M13_255047",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/255047-M13_255047/M13_255047_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/255047-M13_255047/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/255047-M13_255047/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/255047-M13_255047/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-14-m10-201233",
    "arm": "fit",
    "status": "complete",
    "target": "M10_201233",
    "artifacts": [
      {
        "label": "Executed fit · M10_201233",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/201233-M10_201233/M10_201233_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/201233-M10_201233/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/201233-M10_201233/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-14/run/fits/fit/201233-M10_201233/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-14/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m12-101089",
    "arm": "fit",
    "status": "complete",
    "target": "M12_101089",
    "artifacts": [
      {
        "label": "Executed fit · M12_101089",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/101089-M12_101089/M12_101089_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/101089-M12_101089/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/101089-M12_101089/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/101089-M12_101089/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-12-m13-258753",
    "arm": "fit",
    "status": "complete",
    "target": "M13_258753",
    "artifacts": [
      {
        "label": "Executed fit · M13_258753",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/258753-M13_258753/M13_258753_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/258753-M13_258753/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/258753-M13_258753/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-12/run/fits/fit/258753-M13_258753/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-12/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m5-167056",
    "arm": "fit",
    "status": "complete",
    "target": "M5_167056",
    "artifacts": [
      {
        "label": "Executed fit · M5_167056",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/167056-M5_167056/M5_167056_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/167056-M5_167056/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/167056-M5_167056/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/167056-M5_167056/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m15-87207",
    "arm": "fit",
    "status": "complete",
    "target": "M15_87207",
    "artifacts": [
      {
        "label": "Executed fit · M15_87207",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/87207-M15_87207/M15_87207_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/87207-M15_87207/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/87207-M15_87207/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/87207-M15_87207/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m6-166634",
    "arm": "fit",
    "status": "complete",
    "target": "M6_166634",
    "artifacts": [
      {
        "label": "Executed fit · M6_166634",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/166634-M6_166634/M6_166634_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/166634-M6_166634/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/166634-M6_166634/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/166634-M6_166634/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m7-121482",
    "arm": "fit",
    "status": "complete",
    "target": "M7_121482",
    "artifacts": [
      {
        "label": "Executed fit · M7_121482",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/121482-M7_121482/M7_121482_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/121482-M7_121482/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/121482-M7_121482/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/121482-M7_121482/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m10-189698",
    "arm": "fit",
    "status": "complete",
    "target": "M10_189698",
    "artifacts": [
      {
        "label": "Executed fit · M10_189698",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/189698-M10_189698/M10_189698_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/189698-M10_189698/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/189698-M10_189698/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/189698-M10_189698/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-04-m15-89072",
    "arm": "fit",
    "status": "complete",
    "target": "M15_89072",
    "artifacts": [
      {
        "label": "Executed fit · M15_89072",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/89072-M15_89072/M15_89072_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/89072-M15_89072/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/89072-M15_89072/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-04/run/fits/fit/89072-M15_89072/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-04/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m2-97310",
    "arm": "fit",
    "status": "complete",
    "target": "M2_97310",
    "artifacts": [
      {
        "label": "Executed fit · M2_97310",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/97310-M2_97310/M2_97310_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/97310-M2_97310/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/97310-M2_97310/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/97310-M2_97310/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m14-37843",
    "arm": "fit",
    "status": "complete",
    "target": "M14_37843",
    "artifacts": [
      {
        "label": "Executed fit · M14_37843",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/37843-M14_37843/M14_37843_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/37843-M14_37843/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/37843-M14_37843/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/37843-M14_37843/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-01-m4-112534",
    "arm": "fit",
    "status": "complete",
    "target": "M4_112534",
    "artifacts": [
      {
        "label": "Executed fit · M4_112534",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/112534-M4_112534/M4_112534_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/112534-M4_112534/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/112534-M4_112534/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-01/run/fits/fit/112534-M4_112534/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-01/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-02-m5-127946",
    "arm": "fit",
    "status": "complete",
    "target": "M5_127946",
    "artifacts": [
      {
        "label": "Executed fit · M5_127946",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/127946-M5_127946/M5_127946_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/127946-M5_127946/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/127946-M5_127946/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-02/run/fits/fit/127946-M5_127946/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-02/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-03-m3-119809",
    "arm": "fit",
    "status": "complete",
    "target": "M3_119809",
    "artifacts": [
      {
        "label": "Executed fit · M3_119809",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119809-M3_119809/M3_119809_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119809-M3_119809/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119809-M3_119809/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-03/run/fits/fit/119809-M3_119809/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-03/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-15-m12-185631",
    "arm": "fit",
    "status": "complete",
    "target": "M12_185631",
    "artifacts": [
      {
        "label": "Executed fit · M12_185631",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185631-M12_185631/M12_185631_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185631-M12_185631/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185631-M12_185631/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-15/run/fits/fit/185631-M12_185631/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-15/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-05-m13-253688",
    "arm": "fit",
    "status": "complete",
    "target": "M13_253688",
    "artifacts": [
      {
        "label": "Executed fit · M13_253688",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/253688-M13_253688/M13_253688_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/253688-M13_253688/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/253688-M13_253688/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-05/run/fits/fit/253688-M13_253688/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-05/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-16-m11-217564",
    "arm": "fit",
    "status": "complete",
    "target": "M11_217564",
    "artifacts": [
      {
        "label": "Executed fit · M11_217564",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/217564-M11_217564/M11_217564_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/217564-M11_217564/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/217564-M11_217564/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-16/run/fits/fit/217564-M11_217564/execution.log"
      }
    ],
    "code": "85d3acb",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-16/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "part-13-m14-104877",
    "arm": "fit",
    "status": "complete",
    "target": "M14_104877",
    "artifacts": [
      {
        "label": "Executed fit · M14_104877",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/104877-M14_104877/M14_104877_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/104877-M14_104877/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/104877-M14_104877/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/part-13/run/fits/fit/104877-M14_104877/execution.log"
      }
    ],
    "code": "a9550ce",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/part-13/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  },
  {
    "id": "shard-00-m11-245252",
    "arm": "fit",
    "status": "failed",
    "error": "ValueError: M11_245252: classic FlagCOMBINED = 1 (production photometry refuses it)",
    "target": "M11_245252",
    "artifacts": [
      {
        "label": "Executed fit · M11_245252",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/245252-M11_245252/M11_245252_executed.ipynb"
      },
      {
        "label": "execution.log",
        "path": "results/dr2-refit-2026-10-12/shard-00/run/fits/fit/245252-M11_245252/execution.log"
      }
    ],
    "code": "7033ef1",
    "model": "Ceridwen d7c0536; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/dr2-refit-2026-10-12/shard-00/experiment.json",
    "seed": 20260832,
    "data": "results/dr2-refit-2026-10-12/targets.json"
  }
]
```

## Figures

```json
[
  {
    "path": "wiki/analyses/dr2-refit-sample/formation-times-vs-age.png",
    "view": "Comparison",
    "caption": "Per-galaxy posterior medians of \\(t_{80}\\), \\(t_{50}\\) and \\(t_{20}\\) against mass-weighted age, with 16–84 intervals, running medians in 10 equal-count bins and a 1:1 line; median \\(t_{80}-\\mathrm{age}\\): 1.46 Gyr, median \\(\\mathrm{age}-t_{20}\\): 1.38 Gyr.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/headline-age-redshift.png",
    "view": "Comparison",
    "caption": "Mass-weighted age against redshift with binned medians, split at \\(\\sigma_\\star=215\\ \\mathrm{km\\,s^{-1}}\\) (80 low, 55 high; age–\\(z\\) Spearman −0.17), above Ceridwen minus Borghi+22 ages for the 48 overlap galaxies.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/borghi2022-age-vs-z.png",
    "view": "Comparison",
    "caption": "Ceridwen and re-binned Borghi+22 catalogue ages (\\(N=140\\)) in \\(\\Delta z=0.075\\) bins over 0.6–0.9, split at \\(215\\ \\mathrm{km\\,s^{-1}}\\); bin medians span 3.56–4.66 and 2.15–3.69 Gyr respectively, with mean offset +1.21 Gyr and offsets 0.23–2.17 Gyr.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/old-vs-new.png",
    "view": "Comparison",
    "caption": "October refit against the September run reference arm for the same 135 galaxies, with intervals on both axes and a 1:1 line: median shifts in age, \\(t_{50}\\), \\(\\Delta t\\), \\(\\log M_\\star\\), \\([\\mathrm{Fe}/\\mathrm{H}]\\), \\([\\alpha/\\mathrm{Fe}]\\) and \\(\\tau\\) are −0.60 Gyr, −0.82 Gyr, +0.27 Gyr, −0.02, −0.09, −0.01 and +0.06 respectively; dust parameters use different laws, Noll in October and Kriek &amp; Conroy in September.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/dt-vs-formation-epoch.png",
    "view": "Comparison",
    "caption": "\\(\\Delta t=t_{80}-t_{20}\\) against \\(t_{50}\\), \\(z_{\\mathrm{form}}\\) and \\(z_{\\mathrm{obs}}\\), with running medians; median \\(\\Delta t\\): 2.74 Gyr, Spearman with \\(t_{50}\\): −0.34.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/dt-vs-mass.png",
    "view": "Comparison",
    "caption": "\\(\\Delta t\\) against \\(\\log M_\\star\\), with running medians; Spearman −0.29.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/dt-vs-alpha.png",
    "view": "Comparison",
    "caption": "\\(\\Delta t\\) against \\([\\alpha/\\mathrm{Fe}]\\), with running medians; Spearman 0.32.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/distributions-1d.png",
    "view": "Comparison",
    "caption": "Distributions for 135 galaxies per panel; sample medians: \\(z\\) 0.73, \\(\\log M_\\star\\) 11.28, age 4.04 Gyr, \\([\\mathrm{Fe}/\\mathrm{H}]\\) −0.29, \\([\\alpha/\\mathrm{Fe}]\\) −0.03, \\(\\tau_{\\mathrm{diffuse}}\\) (Noll) 0.49, \\(t_{50}\\) 3.97 Gyr and \\(\\Delta t\\) 2.74 Gyr.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-refit-sample/fit-quality.png",
    "view": "Comparison",
    "caption": "Likelihood calls, \\(\\ln Z\\), joint \\(\\chi^2/\\nu\\) and spectrum versus photometry \\(\\chi^2/\\nu\\); all 135 diagnostics passed, calls span 4.1–7.9 M, joint \\(\\chi^2/\\nu\\) median 1.09 and maximum 2.54 (253688), sampler wall time median 109 s.",
    "target": ""
  }
]
```

## Results

- Fitted 135; 45 unreached. All fits passed diagnostics; joint \(\chi^2/\nu\) median 1.09, maximum 2.54 (`253688`); likelihood calls 4.1–7.9 M; median sampler time 109 s.
- Fitted versus unfitted KS \(p\): \(z\) 0.43, September \(\log M\) 0.78, S/N 0.85; fitted/all medians: \(z\) 0.728/0.729, \(\log M\) 11.35/11.34, S/N 21.5/21.3.
- Across per-galaxy posterior medians, median [16th, 84th percentile]: age 4.04 [3.42, 4.77] Gyr; \(t_{20}\) 2.55 [1.98, 3.56], \(t_{50}\) 3.97 [3.21, 4.94], \(t_{80}\) 5.49 [4.84, 6.21], \(\Delta t\) 2.74 [2.24, 3.15] Gyr.
- Same summaries: \(\log M_\star\) 11.28 [11.02, 11.58]; \([\mathrm{Fe}/\mathrm{H}]\) −0.29 [−0.56, −0.12]; \([\alpha/\mathrm{Fe}]\) −0.03 [−0.19, 0.13]; \(\tau_{\rm diffuse}\) 0.49 [0.36, 0.66].
- October − September paired differences, median [16th, 84th]: age −0.60 [−1.27, +0.14], \(t_{20}\) −0.64 [−1.56, +0.24], \(t_{50}\) −0.82 [−1.49, +0.19], \(t_{80}\) −0.45 [−1.02, +0.24], \(\Delta t\) +0.27 [−0.23, +0.84] Gyr.
- Borghi+22 overlap: 48 galaxies; mean binned age offset +1.21 Gyr, range 0.23–2.17 Gyr. Spearman \(\Delta t\) versus \(t_{50}\), \(\log M\), \([\alpha/\mathrm{Fe}]\): −0.34, −0.29, 0.32.
- Billed USD 5.65 over 13 instances; final credit USD 0.52; 0 instances left. Per-target spectrum, photometry, SFH and corner figures came from executed notebooks and were rebuilt locally on CPU.

## Caveats

- Production photometry refused `M11_245252`, `M11_226721`, `M11_244738`, `M5_241189`, `M2_208364`, `M10_228717`, `M15_89153`: outside COSMOS2025, COSMOS2020 Classic `FlagCOMBINED = 1`; `M11_245252` failed in `shard-00` before the full check.
- First 65 fits started from heads of S/N-ordered slices: median S/N 29.2 versus 21.25 for all 180; KS \(p=0.01\) in \(z\) and \(\log M\); stratification began at 22:59 UTC.
- Lost lanes: bid `55630268` reclaimed, bid `55630494` outbid, `55623415` interrupted when its controlling process stopped; in-flight fits lost, targets returned to the pool; no lane re-rented.
- The 45 unreached targets are listed under `unfitted` in `targets.json`; stopping credit was USD 0.55–0.70 versus the USD 0.30 steer.
- September and October changed multiple settings; \(\tau\) uses different dust laws.
- Joint \(\chi^2/\nu\) reached 2.54; `216899` had joint \(\chi^2/\nu=1.73\) and photometry \(\chi^2/\nu=17.7\).

## References

- [DR2 quiescent refit, October defaults](wiki/notes/dr2-refit-sample.md)
- [DR2 quiescent sample](wiki/notes/dr2-quiescent-sample.md)
- [September research record](wiki/research/experiments/e-dr2-revised.md)
- [Target selection and fit order](results/dr2-refit-2026-10-12/targets.json)
- [Refit summary](results/dr2-refit-2026-10-12/dr2-refit-summary.csv)
- Run manifests: `results/dr2-refit-2026-10-12/<part>/run/manifest.json`
