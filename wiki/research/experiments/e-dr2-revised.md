---
kind: experiment
id: e-dr2-revised
title: Revised DR2 population fit and baseline comparison
date: 2026-09-07
origin: existing
status: recorded
question: q-population-results
related_questions: q-fitting-choices
source_notes: dr2-new-defaults,per-galaxy-fit-diagnostics
result_groups: results/dr2-quiescent-new-defaults
---

## Context

The revised 187-target run uses order-3 calibration, cosmos_total photometry, a free dust slope and a StudentT SFH prior. The saved tau prior is Uniform(0, 2).

## Runs

```json
[
  {
    "id": "m12-101089",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_101089",
        "path": "results/dr2-quiescent-new-defaults/101089-M12_101089/M12_101089_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/101089-M12_101089/ceridwen_result.h5"
      }
    ],
    "seed": 20260995,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-101830",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_101830",
        "path": "results/dr2-quiescent-new-defaults/101830-M12_101830/M12_101830_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/101830-M12_101830/ceridwen_result.h5"
      }
    ],
    "seed": 20260983,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-102456",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_102456",
        "path": "results/dr2-quiescent-new-defaults/102456-M12_102456/M12_102456_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/102456-M12_102456/ceridwen_result.h5"
      }
    ],
    "seed": 20260863,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-102968",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_102968",
        "path": "results/dr2-quiescent-new-defaults/102968-M14_102968/M14_102968_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/102968-M14_102968/ceridwen_result.h5"
      }
    ],
    "seed": 20260991,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-103366",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_103366",
        "path": "results/dr2-quiescent-new-defaults/103366-M14_103366/M14_103366_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/103366-M14_103366/ceridwen_result.h5"
      }
    ],
    "seed": 20260963,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-104877",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_104877",
        "path": "results/dr2-quiescent-new-defaults/104877-M14_104877/M14_104877_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/104877-M14_104877/ceridwen_result.h5"
      }
    ],
    "seed": 20261016,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-105474",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_105474",
        "path": "results/dr2-quiescent-new-defaults/105474-M4_105474/M4_105474_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/105474-M4_105474/ceridwen_result.h5"
      }
    ],
    "seed": 20260850,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-107362",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_107362",
        "path": "results/dr2-quiescent-new-defaults/107362-M3_107362/M3_107362_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/107362-M3_107362/ceridwen_result.h5"
      }
    ],
    "seed": 20260915,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-107370",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_107370",
        "path": "results/dr2-quiescent-new-defaults/107370-M4_107370/M4_107370_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/107370-M4_107370/ceridwen_result.h5"
      }
    ],
    "seed": 20260947,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-107643",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_107643",
        "path": "results/dr2-quiescent-new-defaults/107643-M4_107643/M4_107643_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/107643-M4_107643/ceridwen_result.h5"
      }
    ],
    "seed": 20260928,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-108989",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_108989",
        "path": "results/dr2-quiescent-new-defaults/108989-M4_108989/M4_108989_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/108989-M4_108989/ceridwen_result.h5"
      }
    ],
    "seed": 20260924,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-109352",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_109352",
        "path": "results/dr2-quiescent-new-defaults/109352-M3_109352/M3_109352_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/109352-M3_109352/ceridwen_result.h5"
      }
    ],
    "seed": 20260914,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-109713",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_109713",
        "path": "results/dr2-quiescent-new-defaults/109713-M3_109713/M3_109713_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/109713-M3_109713/ceridwen_result.h5"
      }
    ],
    "seed": 20260911,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-109843",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_109843",
        "path": "results/dr2-quiescent-new-defaults/109843-M3_109843/M3_109843_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/109843-M3_109843/ceridwen_result.h5"
      }
    ],
    "seed": 20260972,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-111390",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_111390",
        "path": "results/dr2-quiescent-new-defaults/111390-M3_111390/M3_111390_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/111390-M3_111390/ceridwen_result.h5"
      }
    ],
    "seed": 20260873,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-112534",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_112534",
        "path": "results/dr2-quiescent-new-defaults/112534-M4_112534/M4_112534_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/112534-M4_112534/ceridwen_result.h5"
      }
    ],
    "seed": 20261009,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-113852",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_113852",
        "path": "results/dr2-quiescent-new-defaults/113852-M7_113852/M7_113852_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/113852-M7_113852/ceridwen_result.h5"
      }
    ],
    "seed": 20260848,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-117010",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_117010",
        "path": "results/dr2-quiescent-new-defaults/117010-M3_117010/M3_117010_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/117010-M3_117010/ceridwen_result.h5"
      }
    ],
    "seed": 20260944,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-117400",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_117400",
        "path": "results/dr2-quiescent-new-defaults/117400-M4_117400/M4_117400_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/117400-M4_117400/ceridwen_result.h5"
      }
    ],
    "seed": 20260856,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-117694",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_117694",
        "path": "results/dr2-quiescent-new-defaults/117694-M3_117694/M3_117694_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/117694-M3_117694/ceridwen_result.h5"
      }
    ],
    "seed": 20260912,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-119474",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_119474",
        "path": "results/dr2-quiescent-new-defaults/119474-M3_119474/M3_119474_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/119474-M3_119474/ceridwen_result.h5"
      }
    ],
    "seed": 20260860,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-119802",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_119802",
        "path": "results/dr2-quiescent-new-defaults/119802-M3_119802/M3_119802_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/119802-M3_119802/ceridwen_result.h5"
      }
    ],
    "seed": 20260905,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-119809",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_119809",
        "path": "results/dr2-quiescent-new-defaults/119809-M3_119809/M3_119809_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/119809-M3_119809/ceridwen_result.h5"
      }
    ],
    "seed": 20261011,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-120308",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_120308",
        "path": "results/dr2-quiescent-new-defaults/120308-M3_120308/M3_120308_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/120308-M3_120308/ceridwen_result.h5"
      }
    ],
    "seed": 20260891,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-120372",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_120372",
        "path": "results/dr2-quiescent-new-defaults/120372-M7_120372/M7_120372_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/120372-M7_120372/ceridwen_result.h5"
      }
    ],
    "seed": 20260939,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-120488",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_120488",
        "path": "results/dr2-quiescent-new-defaults/120488-M7_120488/M7_120488_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/120488-M7_120488/ceridwen_result.h5"
      }
    ],
    "seed": 20260967,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m3-120540",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M3_120540",
        "path": "results/dr2-quiescent-new-defaults/120540-M3_120540/M3_120540_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/120540-M3_120540/ceridwen_result.h5"
      }
    ],
    "seed": 20260958,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-120758",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_120758",
        "path": "results/dr2-quiescent-new-defaults/120758-M7_120758/M7_120758_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/120758-M7_120758/ceridwen_result.h5"
      }
    ],
    "seed": 20260989,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-121482",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_121482",
        "path": "results/dr2-quiescent-new-defaults/121482-M7_121482/M7_121482_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/121482-M7_121482/ceridwen_result.h5"
      }
    ],
    "seed": 20261001,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-122025",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_122025",
        "path": "results/dr2-quiescent-new-defaults/122025-M7_122025/M7_122025_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/122025-M7_122025/ceridwen_result.h5"
      }
    ],
    "seed": 20260965,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-122242",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_122242",
        "path": "results/dr2-quiescent-new-defaults/122242-M7_122242/M7_122242_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/122242-M7_122242/ceridwen_result.h5"
      }
    ],
    "seed": 20260903,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-123161",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_123161",
        "path": "results/dr2-quiescent-new-defaults/123161-M4_123161/M4_123161_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/123161-M4_123161/ceridwen_result.h5"
      }
    ],
    "seed": 20260929,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-124231",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_124231",
        "path": "results/dr2-quiescent-new-defaults/124231-M4_124231/M4_124231_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/124231-M4_124231/ceridwen_result.h5"
      }
    ],
    "seed": 20260867,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-124875",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_124875",
        "path": "results/dr2-quiescent-new-defaults/124875-M7_124875/M7_124875_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/124875-M7_124875/ceridwen_result.h5"
      }
    ],
    "seed": 20260876,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-125213",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_125213",
        "path": "results/dr2-quiescent-new-defaults/125213-M4_125213/M4_125213_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/125213-M4_125213/ceridwen_result.h5"
      }
    ],
    "seed": 20260897,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-126153",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_126153",
        "path": "results/dr2-quiescent-new-defaults/126153-M1_126153/M1_126153_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/126153-M1_126153/ceridwen_result.h5"
      }
    ],
    "seed": 20260987,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-126578",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_126578",
        "path": "results/dr2-quiescent-new-defaults/126578-M1_126578/M1_126578_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/126578-M1_126578/ceridwen_result.h5"
      }
    ],
    "seed": 20260957,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-127946",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_127946",
        "path": "results/dr2-quiescent-new-defaults/127946-M5_127946/M5_127946_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/127946-M5_127946/ceridwen_result.h5"
      }
    ],
    "seed": 20261010,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-128311",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_128311",
        "path": "results/dr2-quiescent-new-defaults/128311-M5_128311/M5_128311_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/128311-M5_128311/ceridwen_result.h5"
      }
    ],
    "seed": 20260902,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-129596",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_129596",
        "path": "results/dr2-quiescent-new-defaults/129596-M2_129596/M2_129596_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/129596-M2_129596/ceridwen_result.h5"
      }
    ],
    "seed": 20260943,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-130005",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_130005",
        "path": "results/dr2-quiescent-new-defaults/130005-M2_130005/M2_130005_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/130005-M2_130005/ceridwen_result.h5"
      }
    ],
    "seed": 20260945,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-130052",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_130052",
        "path": "results/dr2-quiescent-new-defaults/130052-M1_130052/M1_130052_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/130052-M1_130052/ceridwen_result.h5"
      }
    ],
    "seed": 20260839,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-133240",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_133240",
        "path": "results/dr2-quiescent-new-defaults/133240-M1_133240/M1_133240_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/133240-M1_133240/ceridwen_result.h5"
      }
    ],
    "seed": 20260982,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-133501",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_133501",
        "path": "results/dr2-quiescent-new-defaults/133501-M2_133501/M2_133501_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/133501-M2_133501/ceridwen_result.h5"
      }
    ],
    "seed": 20260834,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-134021",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_134021",
        "path": "results/dr2-quiescent-new-defaults/134021-M2_134021/M2_134021_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/134021-M2_134021/ceridwen_result.h5"
      }
    ],
    "seed": 20260904,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-134391",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_134391",
        "path": "results/dr2-quiescent-new-defaults/134391-M2_134391/M2_134391_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/134391-M2_134391/ceridwen_result.h5"
      }
    ],
    "seed": 20260838,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-139423",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_139423",
        "path": "results/dr2-quiescent-new-defaults/139423-M1_139423/M1_139423_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/139423-M1_139423/ceridwen_result.h5"
      }
    ],
    "seed": 20260896,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-139662",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_139662",
        "path": "results/dr2-quiescent-new-defaults/139662-M2_139662/M2_139662_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/139662-M2_139662/ceridwen_result.h5"
      }
    ],
    "seed": 20260949,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-143127",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_143127",
        "path": "results/dr2-quiescent-new-defaults/143127-M7_143127/M7_143127_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/143127-M7_143127/ceridwen_result.h5"
      }
    ],
    "seed": 20260980,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-145276",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_145276",
        "path": "results/dr2-quiescent-new-defaults/145276-M8_145276/M8_145276_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/145276-M8_145276/ceridwen_result.h5"
      }
    ],
    "seed": 20260950,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-146213",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_146213",
        "path": "results/dr2-quiescent-new-defaults/146213-M7_146213/M7_146213_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/146213-M7_146213/ceridwen_result.h5"
      }
    ],
    "seed": 20260936,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-147270",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_147270",
        "path": "results/dr2-quiescent-new-defaults/147270-M7_147270/M7_147270_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/147270-M7_147270/ceridwen_result.h5"
      }
    ],
    "seed": 20260930,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-147539",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_147539",
        "path": "results/dr2-quiescent-new-defaults/147539-M8_147539/M8_147539_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/147539-M8_147539/ceridwen_result.h5"
      }
    ],
    "seed": 20260884,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-147849",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_147849",
        "path": "results/dr2-quiescent-new-defaults/147849-M7_147849/M7_147849_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/147849-M7_147849/ceridwen_result.h5"
      }
    ],
    "seed": 20260886,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-148698",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_148698",
        "path": "results/dr2-quiescent-new-defaults/148698-M8_148698/M8_148698_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/148698-M8_148698/ceridwen_result.h5"
      }
    ],
    "seed": 20260871,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-150848",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_150848",
        "path": "results/dr2-quiescent-new-defaults/150848-M8_150848/M8_150848_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/150848-M8_150848/ceridwen_result.h5"
      }
    ],
    "seed": 20260844,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-152125",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_152125",
        "path": "results/dr2-quiescent-new-defaults/152125-M7_152125/M7_152125_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/152125-M7_152125/ceridwen_result.h5"
      }
    ],
    "seed": 20260954,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-156118",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_156118",
        "path": "results/dr2-quiescent-new-defaults/156118-M8_156118/M8_156118_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/156118-M8_156118/ceridwen_result.h5"
      }
    ],
    "seed": 20260985,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-160400",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_160400",
        "path": "results/dr2-quiescent-new-defaults/160400-M8_160400/M8_160400_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/160400-M8_160400/ceridwen_result.h5"
      }
    ],
    "seed": 20260840,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-161113",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_161113",
        "path": "results/dr2-quiescent-new-defaults/161113-M8_161113/M8_161113_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/161113-M8_161113/ceridwen_result.h5"
      }
    ],
    "seed": 20260975,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-161346",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_161346",
        "path": "results/dr2-quiescent-new-defaults/161346-M8_161346/M8_161346_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/161346-M8_161346/ceridwen_result.h5"
      }
    ],
    "seed": 20260845,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-162149",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_162149",
        "path": "results/dr2-quiescent-new-defaults/162149-M8_162149/M8_162149_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/162149-M8_162149/ceridwen_result.h5"
      }
    ],
    "seed": 20260846,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m7-162587",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M7_162587",
        "path": "results/dr2-quiescent-new-defaults/162587-M7_162587/M7_162587_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/162587-M7_162587/ceridwen_result.h5"
      }
    ],
    "seed": 20260974,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m8-163989",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M8_163989",
        "path": "results/dr2-quiescent-new-defaults/163989-M8_163989/M8_163989_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/163989-M8_163989/ceridwen_result.h5"
      }
    ],
    "seed": 20260941,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-165871",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_165871",
        "path": "results/dr2-quiescent-new-defaults/165871-M5_165871/M5_165871_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/165871-M5_165871/ceridwen_result.h5"
      }
    ],
    "seed": 20260907,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m6-166634",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M6_166634",
        "path": "results/dr2-quiescent-new-defaults/166634-M6_166634/M6_166634_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/166634-M6_166634/ceridwen_result.h5"
      }
    ],
    "seed": 20261000,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-167056",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_167056",
        "path": "results/dr2-quiescent-new-defaults/167056-M5_167056/M5_167056_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/167056-M5_167056/ceridwen_result.h5"
      }
    ],
    "seed": 20260997,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-172669",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_172669",
        "path": "results/dr2-quiescent-new-defaults/172669-M5_172669/M5_172669_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/172669-M5_172669/ceridwen_result.h5"
      }
    ],
    "seed": 20260830,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-173928",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_173928",
        "path": "results/dr2-quiescent-new-defaults/173928-M5_173928/M5_173928_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/173928-M5_173928/ceridwen_result.h5"
      }
    ],
    "seed": 20260970,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-180774",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_180774",
        "path": "results/dr2-quiescent-new-defaults/180774-M12_180774/M12_180774_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/180774-M12_180774/ceridwen_result.h5"
      }
    ],
    "seed": 20260921,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-181421",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_181421",
        "path": "results/dr2-quiescent-new-defaults/181421-M12_181421/M12_181421_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/181421-M12_181421/ceridwen_result.h5"
      }
    ],
    "seed": 20260984,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-181945",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_181945",
        "path": "results/dr2-quiescent-new-defaults/181945-M12_181945/M12_181945_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/181945-M12_181945/ceridwen_result.h5"
      }
    ],
    "seed": 20260833,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-182890",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_182890",
        "path": "results/dr2-quiescent-new-defaults/182890-M12_182890/M12_182890_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/182890-M12_182890/ceridwen_result.h5"
      }
    ],
    "seed": 20260952,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-184916",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_184916",
        "path": "results/dr2-quiescent-new-defaults/184916-M12_184916/M12_184916_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/184916-M12_184916/ceridwen_result.h5"
      }
    ],
    "seed": 20260885,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-185631",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185631",
        "path": "results/dr2-quiescent-new-defaults/185631-M12_185631/M12_185631_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/185631-M12_185631/ceridwen_result.h5"
      }
    ],
    "seed": 20261012,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-185653",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_185653",
        "path": "results/dr2-quiescent-new-defaults/185653-M12_185653/M12_185653_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/185653-M12_185653/ceridwen_result.h5"
      }
    ],
    "seed": 20260923,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-189698",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_189698",
        "path": "results/dr2-quiescent-new-defaults/189698-M10_189698/M10_189698_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/189698-M10_189698/ceridwen_result.h5"
      }
    ],
    "seed": 20261002,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-191718",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_191718",
        "path": "results/dr2-quiescent-new-defaults/191718-M10_191718/M10_191718_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/191718-M10_191718/ceridwen_result.h5"
      }
    ],
    "seed": 20261005,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-197591",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_197591",
        "path": "results/dr2-quiescent-new-defaults/197591-M10_197591/M10_197591_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/197591-M10_197591/ceridwen_result.h5"
      }
    ],
    "seed": 20260913,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-201233",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_201233",
        "path": "results/dr2-quiescent-new-defaults/201233-M10_201233/M10_201233_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/201233-M10_201233/ceridwen_result.h5"
      }
    ],
    "seed": 20260994,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-205715",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_205715",
        "path": "results/dr2-quiescent-new-defaults/205715-M5_205715/M5_205715_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/205715-M5_205715/ceridwen_result.h5"
      }
    ],
    "seed": 20260870,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-205742",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_205742",
        "path": "results/dr2-quiescent-new-defaults/205742-M1_205742/M1_205742_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/205742-M1_205742/ceridwen_result.h5"
      }
    ],
    "seed": 20260842,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-205765",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_205765",
        "path": "results/dr2-quiescent-new-defaults/205765-M5_205765/M5_205765_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/205765-M5_205765/ceridwen_result.h5"
      }
    ],
    "seed": 20260964,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-206501",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206501",
        "path": "results/dr2-quiescent-new-defaults/206501-M1_206501/M1_206501_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/206501-M1_206501/ceridwen_result.h5"
      }
    ],
    "seed": 20260883,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-206545",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206545",
        "path": "results/dr2-quiescent-new-defaults/206545-M1_206545/M1_206545_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/206545-M1_206545/ceridwen_result.h5"
      }
    ],
    "seed": 20260877,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-206669",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_206669",
        "path": "results/dr2-quiescent-new-defaults/206669-M2_206669/M2_206669_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/206669-M2_206669/ceridwen_result.h5"
      }
    ],
    "seed": 20260861,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-206771",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_206771",
        "path": "results/dr2-quiescent-new-defaults/206771-M5_206771/M5_206771_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/206771-M5_206771/ceridwen_result.h5"
      }
    ],
    "seed": 20260978,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-206858",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_206858",
        "path": "results/dr2-quiescent-new-defaults/206858-M1_206858/M1_206858_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/206858-M1_206858/ceridwen_result.h5"
      }
    ],
    "seed": 20260869,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-208364",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_208364",
        "path": "results/dr2-quiescent-new-defaults/208364-M2_208364/M2_208364_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/208364-M2_208364/ceridwen_result.h5"
      }
    ],
    "seed": 20260906,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-208622",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_208622",
        "path": "results/dr2-quiescent-new-defaults/208622-M1_208622/M1_208622_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/208622-M1_208622/ceridwen_result.h5"
      }
    ],
    "seed": 20260946,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-210210",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/dr2-quiescent-new-defaults/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/210210-M1_210210/ceridwen_result.h5"
      }
    ],
    "seed": 20260832,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-210940",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_210940",
        "path": "results/dr2-quiescent-new-defaults/210940-M2_210940/M2_210940_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/210940-M2_210940/ceridwen_result.h5"
      }
    ],
    "seed": 20260966,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m1-211157",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_211157",
        "path": "results/dr2-quiescent-new-defaults/211157-M1_211157/M1_211157_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/211157-M1_211157/ceridwen_result.h5"
      }
    ],
    "seed": 20260862,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-211347",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_211347",
        "path": "results/dr2-quiescent-new-defaults/211347-M5_211347/M5_211347_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/211347-M5_211347/ceridwen_result.h5"
      }
    ],
    "seed": 20260888,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-211767",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_211767",
        "path": "results/dr2-quiescent-new-defaults/211767-M5_211767/M5_211767_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/211767-M5_211767/ceridwen_result.h5"
      }
    ],
    "seed": 20260895,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-212391",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_212391",
        "path": "results/dr2-quiescent-new-defaults/212391-M9_212391/M9_212391_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/212391-M9_212391/ceridwen_result.h5"
      }
    ],
    "seed": 20260933,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-212718",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_212718",
        "path": "results/dr2-quiescent-new-defaults/212718-M11_212718/M11_212718_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/212718-M11_212718/ceridwen_result.h5"
      }
    ],
    "seed": 20260981,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-213004",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_213004",
        "path": "results/dr2-quiescent-new-defaults/213004-M11_213004/M11_213004_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/213004-M11_213004/ceridwen_result.h5"
      }
    ],
    "seed": 20260849,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-213587",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_213587",
        "path": "results/dr2-quiescent-new-defaults/213587-M9_213587/M9_213587_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/213587-M9_213587/ceridwen_result.h5"
      }
    ],
    "seed": 20260899,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-213772",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_213772",
        "path": "results/dr2-quiescent-new-defaults/213772-M10_213772/M10_213772_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/213772-M10_213772/ceridwen_result.h5"
      }
    ],
    "seed": 20260843,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-214296",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_214296",
        "path": "results/dr2-quiescent-new-defaults/214296-M11_214296/M11_214296_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/214296-M11_214296/ceridwen_result.h5"
      }
    ],
    "seed": 20260937,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-214430",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_214430",
        "path": "results/dr2-quiescent-new-defaults/214430-M11_214430/M11_214430_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/214430-M11_214430/ceridwen_result.h5"
      }
    ],
    "seed": 20260956,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-214899",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_214899",
        "path": "results/dr2-quiescent-new-defaults/214899-M9_214899/M9_214899_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/214899-M9_214899/ceridwen_result.h5"
      }
    ],
    "seed": 20260942,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-215519",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_215519",
        "path": "results/dr2-quiescent-new-defaults/215519-M10_215519/M10_215519_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/215519-M10_215519/ceridwen_result.h5"
      }
    ],
    "seed": 20260948,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-215585",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_215585",
        "path": "results/dr2-quiescent-new-defaults/215585-M11_215585/M11_215585_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/215585-M11_215585/ceridwen_result.h5"
      }
    ],
    "seed": 20260859,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-216730",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_216730",
        "path": "results/dr2-quiescent-new-defaults/216730-M10_216730/M10_216730_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/216730-M10_216730/ceridwen_result.h5"
      }
    ],
    "seed": 20260853,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-216899",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_216899",
        "path": "results/dr2-quiescent-new-defaults/216899-M11_216899/M11_216899_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/216899-M11_216899/ceridwen_result.h5"
      }
    ],
    "seed": 20260926,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-217020",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_217020",
        "path": "results/dr2-quiescent-new-defaults/217020-M10_217020/M10_217020_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/217020-M10_217020/ceridwen_result.h5"
      }
    ],
    "seed": 20260973,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-217564",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_217564",
        "path": "results/dr2-quiescent-new-defaults/217564-M11_217564/M11_217564_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/217564-M11_217564/ceridwen_result.h5"
      }
    ],
    "seed": 20261015,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-218207",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_218207",
        "path": "results/dr2-quiescent-new-defaults/218207-M11_218207/M11_218207_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/218207-M11_218207/ceridwen_result.h5"
      }
    ],
    "seed": 20260852,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-218701",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_218701",
        "path": "results/dr2-quiescent-new-defaults/218701-M9_218701/M9_218701_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/218701-M9_218701/ceridwen_result.h5"
      }
    ],
    "seed": 20260880,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-221163",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_221163",
        "path": "results/dr2-quiescent-new-defaults/221163-M11_221163/M11_221163_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/221163-M11_221163/ceridwen_result.h5"
      }
    ],
    "seed": 20260868,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-225431",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_225431",
        "path": "results/dr2-quiescent-new-defaults/225431-M9_225431/M9_225431_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/225431-M9_225431/ceridwen_result.h5"
      }
    ],
    "seed": 20260931,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-225441",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_225441",
        "path": "results/dr2-quiescent-new-defaults/225441-M10_225441/M10_225441_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/225441-M10_225441/ceridwen_result.h5"
      }
    ],
    "seed": 20260894,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-225678",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_225678",
        "path": "results/dr2-quiescent-new-defaults/225678-M9_225678/M9_225678_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/225678-M9_225678/ceridwen_result.h5"
      }
    ],
    "seed": 20260979,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-226316",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_226316",
        "path": "results/dr2-quiescent-new-defaults/226316-M9_226316/M9_226316_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/226316-M9_226316/ceridwen_result.h5"
      }
    ],
    "seed": 20260836,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-226721",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_226721",
        "path": "results/dr2-quiescent-new-defaults/226721-M11_226721/M11_226721_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/226721-M11_226721/ceridwen_result.h5"
      }
    ],
    "seed": 20260889,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-227516",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_227516",
        "path": "results/dr2-quiescent-new-defaults/227516-M10_227516/M10_227516_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/227516-M10_227516/ceridwen_result.h5"
      }
    ],
    "seed": 20260887,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-227630",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_227630",
        "path": "results/dr2-quiescent-new-defaults/227630-M9_227630/M9_227630_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/227630-M9_227630/ceridwen_result.h5"
      }
    ],
    "seed": 20260940,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-227672",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_227672",
        "path": "results/dr2-quiescent-new-defaults/227672-M10_227672/M10_227672_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/227672-M10_227672/ceridwen_result.h5"
      }
    ],
    "seed": 20260934,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-228215",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_228215",
        "path": "results/dr2-quiescent-new-defaults/228215-M10_228215/M10_228215_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/228215-M10_228215/ceridwen_result.h5"
      }
    ],
    "seed": 20260851,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-228380",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_228380",
        "path": "results/dr2-quiescent-new-defaults/228380-M10_228380/M10_228380_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/228380-M10_228380/ceridwen_result.h5"
      }
    ],
    "seed": 20260855,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-228717",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_228717",
        "path": "results/dr2-quiescent-new-defaults/228717-M10_228717/M10_228717_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/228717-M10_228717/ceridwen_result.h5"
      }
    ],
    "seed": 20260962,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-229551",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_229551",
        "path": "results/dr2-quiescent-new-defaults/229551-M11_229551/M11_229551_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/229551-M11_229551/ceridwen_result.h5"
      }
    ],
    "seed": 20260872,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-229883",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_229883",
        "path": "results/dr2-quiescent-new-defaults/229883-M9_229883/M9_229883_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/229883-M9_229883/ceridwen_result.h5"
      }
    ],
    "seed": 20260919,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-230747",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_230747",
        "path": "results/dr2-quiescent-new-defaults/230747-M13_230747/M13_230747_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/230747-M13_230747/ceridwen_result.h5"
      }
    ],
    "seed": 20260917,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-230983",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_230983",
        "path": "results/dr2-quiescent-new-defaults/230983-M10_230983/M10_230983_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/230983-M10_230983/ceridwen_result.h5"
      }
    ],
    "seed": 20260922,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-231276",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_231276",
        "path": "results/dr2-quiescent-new-defaults/231276-M9_231276/M9_231276_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/231276-M9_231276/ceridwen_result.h5"
      }
    ],
    "seed": 20260847,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-231544",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_231544",
        "path": "results/dr2-quiescent-new-defaults/231544-M10_231544/M10_231544_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/231544-M10_231544/ceridwen_result.h5"
      }
    ],
    "seed": 20260901,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-231554",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_231554",
        "path": "results/dr2-quiescent-new-defaults/231554-M13_231554/M13_231554_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/231554-M13_231554/ceridwen_result.h5"
      }
    ],
    "seed": 20260986,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-232005",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_232005",
        "path": "results/dr2-quiescent-new-defaults/232005-M9_232005/M9_232005_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/232005-M9_232005/ceridwen_result.h5"
      }
    ],
    "seed": 20260893,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-232627",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_232627",
        "path": "results/dr2-quiescent-new-defaults/232627-M13_232627/M13_232627_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/232627-M13_232627/ceridwen_result.h5"
      }
    ],
    "seed": 20260854,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-232890",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_232890",
        "path": "results/dr2-quiescent-new-defaults/232890-M9_232890/M9_232890_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/232890-M9_232890/ceridwen_result.h5"
      }
    ],
    "seed": 20260976,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-232962",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_232962",
        "path": "results/dr2-quiescent-new-defaults/232962-M11_232962/M11_232962_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/232962-M11_232962/ceridwen_result.h5"
      }
    ],
    "seed": 20260878,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m10-233129",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M10_233129",
        "path": "results/dr2-quiescent-new-defaults/233129-M10_233129/M10_233129_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/233129-M10_233129/ceridwen_result.h5"
      }
    ],
    "seed": 20260831,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m9-233169",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M9_233169",
        "path": "results/dr2-quiescent-new-defaults/233169-M9_233169/M9_233169_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/233169-M9_233169/ceridwen_result.h5"
      }
    ],
    "seed": 20260837,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m6-233902",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M6_233902",
        "path": "results/dr2-quiescent-new-defaults/233902-M6_233902/M6_233902_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/233902-M6_233902/ceridwen_result.h5"
      }
    ],
    "seed": 20260938,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-236682",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_236682",
        "path": "results/dr2-quiescent-new-defaults/236682-M5_236682/M5_236682_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/236682-M5_236682/ceridwen_result.h5"
      }
    ],
    "seed": 20260875,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-236994",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_236994",
        "path": "results/dr2-quiescent-new-defaults/236994-M5_236994/M5_236994_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/236994-M5_236994/ceridwen_result.h5"
      }
    ],
    "seed": 20260874,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m6-237437",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M6_237437",
        "path": "results/dr2-quiescent-new-defaults/237437-M6_237437/M6_237437_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/237437-M6_237437/ceridwen_result.h5"
      }
    ],
    "seed": 20260908,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m6-237641",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M6_237641",
        "path": "results/dr2-quiescent-new-defaults/237641-M6_237641/M6_237641_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/237641-M6_237641/ceridwen_result.h5"
      }
    ],
    "seed": 20260935,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-238314",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_238314",
        "path": "results/dr2-quiescent-new-defaults/238314-M5_238314/M5_238314_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/238314-M5_238314/ceridwen_result.h5"
      }
    ],
    "seed": 20260865,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-238580",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_238580",
        "path": "results/dr2-quiescent-new-defaults/238580-M5_238580/M5_238580_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/238580-M5_238580/ceridwen_result.h5"
      }
    ],
    "seed": 20260910,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m6-240899",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M6_240899",
        "path": "results/dr2-quiescent-new-defaults/240899-M6_240899/M6_240899_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/240899-M6_240899/ceridwen_result.h5"
      }
    ],
    "seed": 20260955,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m5-241189",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M5_241189",
        "path": "results/dr2-quiescent-new-defaults/241189-M5_241189/M5_241189_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/241189-M5_241189/ceridwen_result.h5"
      }
    ],
    "seed": 20260892,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-243871",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_243871",
        "path": "results/dr2-quiescent-new-defaults/243871-M13_243871/M13_243871_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/243871-M13_243871/ceridwen_result.h5"
      }
    ],
    "seed": 20260920,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-244239",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_244239",
        "path": "results/dr2-quiescent-new-defaults/244239-M13_244239/M13_244239_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/244239-M13_244239/ceridwen_result.h5"
      }
    ],
    "seed": 20260909,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-244680",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_244680",
        "path": "results/dr2-quiescent-new-defaults/244680-M13_244680/M13_244680_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/244680-M13_244680/ceridwen_result.h5"
      }
    ],
    "seed": 20261014,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-244738",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_244738",
        "path": "results/dr2-quiescent-new-defaults/244738-M11_244738/M11_244738_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/244738-M11_244738/ceridwen_result.h5"
      }
    ],
    "seed": 20260890,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-245252",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_245252",
        "path": "results/dr2-quiescent-new-defaults/245252-M11_245252/M11_245252_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/245252-M11_245252/ceridwen_result.h5"
      }
    ],
    "seed": 20260841,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-245621",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_245621",
        "path": "results/dr2-quiescent-new-defaults/245621-M11_245621/M11_245621_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/245621-M11_245621/ceridwen_result.h5"
      }
    ],
    "seed": 20260951,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-245763",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_245763",
        "path": "results/dr2-quiescent-new-defaults/245763-M13_245763/M13_245763_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/245763-M13_245763/ceridwen_result.h5"
      }
    ],
    "seed": 20260992,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-245864",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_245864",
        "path": "results/dr2-quiescent-new-defaults/245864-M11_245864/M11_245864_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/245864-M11_245864/ceridwen_result.h5"
      }
    ],
    "seed": 20260969,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-246149",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_246149",
        "path": "results/dr2-quiescent-new-defaults/246149-M13_246149/M13_246149_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/246149-M13_246149/ceridwen_result.h5"
      }
    ],
    "seed": 20260900,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-248217",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_248217",
        "path": "results/dr2-quiescent-new-defaults/248217-M13_248217/M13_248217_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/248217-M13_248217/ceridwen_result.h5"
      }
    ],
    "seed": 20260881,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-248829",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_248829",
        "path": "results/dr2-quiescent-new-defaults/248829-M11_248829/M11_248829_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/248829-M11_248829/ceridwen_result.h5"
      }
    ],
    "seed": 20260932,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-250391",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_250391",
        "path": "results/dr2-quiescent-new-defaults/250391-M11_250391/M11_250391_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/250391-M11_250391/ceridwen_result.h5"
      }
    ],
    "seed": 20260858,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-253688",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_253688",
        "path": "results/dr2-quiescent-new-defaults/253688-M13_253688/M13_253688_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/253688-M13_253688/ceridwen_result.h5"
      }
    ],
    "seed": 20261013,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-254350",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_254350",
        "path": "results/dr2-quiescent-new-defaults/254350-M13_254350/M13_254350_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/254350-M13_254350/ceridwen_result.h5"
      }
    ],
    "seed": 20260968,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-255047",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_255047",
        "path": "results/dr2-quiescent-new-defaults/255047-M13_255047/M13_255047_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/255047-M13_255047/ceridwen_result.h5"
      }
    ],
    "seed": 20260993,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m11-257455",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M11_257455",
        "path": "results/dr2-quiescent-new-defaults/257455-M11_257455/M11_257455_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/257455-M11_257455/ceridwen_result.h5"
      }
    ],
    "seed": 20260857,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-258753",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_258753",
        "path": "results/dr2-quiescent-new-defaults/258753-M13_258753/M13_258753_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/258753-M13_258753/ceridwen_result.h5"
      }
    ],
    "seed": 20260996,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m13-259737",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M13_259737",
        "path": "results/dr2-quiescent-new-defaults/259737-M13_259737/M13_259737_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/259737-M13_259737/ceridwen_result.h5"
      }
    ],
    "seed": 20260961,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-27068",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_27068",
        "path": "results/dr2-quiescent-new-defaults/27068-M14_27068/M14_27068_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/27068-M14_27068/ceridwen_result.h5"
      }
    ],
    "seed": 20260925,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-31835",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_31835",
        "path": "results/dr2-quiescent-new-defaults/31835-M14_31835/M14_31835_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/31835-M14_31835/ceridwen_result.h5"
      }
    ],
    "seed": 20260898,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-36550",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_36550",
        "path": "results/dr2-quiescent-new-defaults/36550-M14_36550/M14_36550_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/36550-M14_36550/ceridwen_result.h5"
      }
    ],
    "seed": 20260998,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-37023",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_37023",
        "path": "results/dr2-quiescent-new-defaults/37023-M14_37023/M14_37023_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/37023-M14_37023/ceridwen_result.h5"
      }
    ],
    "seed": 20260927,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-37219",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_37219",
        "path": "results/dr2-quiescent-new-defaults/37219-M14_37219/M14_37219_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/37219-M14_37219/ceridwen_result.h5"
      }
    ],
    "seed": 20260959,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-37723",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_37723",
        "path": "results/dr2-quiescent-new-defaults/37723-M14_37723/M14_37723_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/37723-M14_37723/ceridwen_result.h5"
      }
    ],
    "seed": 20260916,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-37843",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_37843",
        "path": "results/dr2-quiescent-new-defaults/37843-M14_37843/M14_37843_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/37843-M14_37843/ceridwen_result.h5"
      }
    ],
    "seed": 20261008,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-38646",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_38646",
        "path": "results/dr2-quiescent-new-defaults/38646-M14_38646/M14_38646_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/38646-M14_38646/ceridwen_result.h5"
      }
    ],
    "seed": 20260990,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-38648",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_38648",
        "path": "results/dr2-quiescent-new-defaults/38648-M14_38648/M14_38648_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/38648-M14_38648/ceridwen_result.h5"
      }
    ],
    "seed": 20260835,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-38771",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_38771",
        "path": "results/dr2-quiescent-new-defaults/38771-M14_38771/M14_38771_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/38771-M14_38771/ceridwen_result.h5"
      }
    ],
    "seed": 20260977,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m14-39865",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M14_39865",
        "path": "results/dr2-quiescent-new-defaults/39865-M14_39865/M14_39865_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/39865-M14_39865/ceridwen_result.h5"
      }
    ],
    "seed": 20261006,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-77632",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_77632",
        "path": "results/dr2-quiescent-new-defaults/77632-M15_77632/M15_77632_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/77632-M15_77632/ceridwen_result.h5"
      }
    ],
    "seed": 20260866,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-77745",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_77745",
        "path": "results/dr2-quiescent-new-defaults/77745-M15_77745/M15_77745_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/77745-M15_77745/ceridwen_result.h5"
      }
    ],
    "seed": 20260879,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m4-84337",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M4_84337",
        "path": "results/dr2-quiescent-new-defaults/84337-M4_84337/M4_84337_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/84337-M4_84337/ceridwen_result.h5"
      }
    ],
    "seed": 20260960,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-87207",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_87207",
        "path": "results/dr2-quiescent-new-defaults/87207-M15_87207/M15_87207_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/87207-M15_87207/ceridwen_result.h5"
      }
    ],
    "seed": 20260999,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-88032",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_88032",
        "path": "results/dr2-quiescent-new-defaults/88032-M15_88032/M15_88032_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/88032-M15_88032/ceridwen_result.h5"
      }
    ],
    "seed": 20260918,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-89072",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_89072",
        "path": "results/dr2-quiescent-new-defaults/89072-M15_89072/M15_89072_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/89072-M15_89072/ceridwen_result.h5"
      }
    ],
    "seed": 20261003,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m15-89153",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M15_89153",
        "path": "results/dr2-quiescent-new-defaults/89153-M15_89153/M15_89153_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/89153-M15_89153/ceridwen_result.h5"
      }
    ],
    "seed": 20260988,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-91529",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_91529",
        "path": "results/dr2-quiescent-new-defaults/91529-M12_91529/M12_91529_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/91529-M12_91529/ceridwen_result.h5"
      }
    ],
    "seed": 20260864,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-92132",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_92132",
        "path": "results/dr2-quiescent-new-defaults/92132-M12_92132/M12_92132_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/92132-M12_92132/ceridwen_result.h5"
      }
    ],
    "seed": 20260953,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-93943",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_93943",
        "path": "results/dr2-quiescent-new-defaults/93943-M2_93943/M2_93943_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/93943-M2_93943/ceridwen_result.h5"
      }
    ],
    "seed": 20260971,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-94494",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_94494",
        "path": "results/dr2-quiescent-new-defaults/94494-M2_94494/M2_94494_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/94494-M2_94494/ceridwen_result.h5"
      }
    ],
    "seed": 20260882,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m2-97310",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_97310",
        "path": "results/dr2-quiescent-new-defaults/97310-M2_97310/M2_97310_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/97310-M2_97310/ceridwen_result.h5"
      }
    ],
    "seed": 20261004,
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  },
  {
    "id": "m12-98104",
    "arm": "revised",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M12_98104",
        "path": "results/dr2-quiescent-new-defaults/98104-M12_98104/M12_98104_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/dr2-quiescent-new-defaults/98104-M12_98104/ceridwen_result.h5"
      }
    ],
    "seed": 20261007,
    "config": "results/dr2-quiescent-new-defaults/shard_1_manifest.json",
    "code": "eb6ebc6",
    "data": "results/dr2-quiescent-new-defaults/targets.json"
  }
]
```

## Results

Matched-row median shifts are age +1.229 Gyr, log Z -0.167 dex, alpha/Fe -0.056 dex and tau +0.169. The saved median delta ln Z is +254.28. [Baseline CSV](results/dr2-quiescent-summary.csv) · [Revised CSV](results/dr2-quiescent-new-defaults-summary.csv).

[Parameter comparison](wiki/analyses/dr2-new-defaults/old-vs-new-parameters.png)

## Caveats

The old source summary incorrectly calls calibration and photometry unchanged: the baseline executed notebooks and diagnostic note show aperture photometry and no polynomial. This is not an isolated dust/SFH test, and evidence is not a same-data comparison.

The source seed-noise section treats dimensionless half-width ratios as absolute errors and scales them by sqrt(187). Its significance column is unsupported. A weak age-shift/dust-slope correlation also does not establish which change caused the shift.

These saved fits did not use the later tau <= 0.2 sensitivity setting.

## References

- [Executed comparison](results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb)
- [Revised run manifest](results/dr2-quiescent-new-defaults/shard_0_manifest.json)
- [Dust-slope quantiles](results/dr2-quiescent-new-defaults/dust_index_posteriors.csv)
- [Baseline executed notebook](results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/M9_229883_executed.ipynb)
- [Saved revised model](results/dr2-quiescent-new-defaults/229883-M9_229883/ceridwen_result.h5)
- [dr2-new-defaults · source note](wiki/notes/dr2-new-defaults.md)
- [per-galaxy-fit-diagnostics · source note](wiki/notes/per-galaxy-fit-diagnostics.md)
