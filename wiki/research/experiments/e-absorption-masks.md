---
kind: experiment
id: e-absorption-masks
title: Full spectrum, feature windows and continuum downweighting
date: 2026-09-02
origin: existing
status: recorded
question: q-fitting-choices
related_questions: q-mock-recovery
source_notes: absorption-line-mask,ceridwen-results
result_groups: results/absorption-mask
---

## Context

Compare three pixel-weighting modes across real targets and a grid of mock tilts, noise scales and seeds.

## Runs

```json
[
  {
    "id": "mock-tilt0p00-snr0p25-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr0p25-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr0p25-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p00-snr0p25-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2002,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2010,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2005,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2013,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2008,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed1-all",
    "arm": "all",
    "status": "complete",
    "seed": 1016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed1-features",
    "arm": "features",
    "status": "complete",
    "seed": 1016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 1016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed2-all",
    "arm": "all",
    "status": "complete",
    "seed": 2016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed2-features",
    "arm": "features",
    "status": "complete",
    "seed": 2016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 2016,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2"
  },
  {
    "id": "real-m11-214430-all",
    "arm": "all",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M11_214430_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb"
      }
    ],
    "target": "M11_214430 · observed"
  },
  {
    "id": "real-m11-214430-features",
    "arm": "features",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M11_214430_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb"
      }
    ],
    "target": "M11_214430 · observed"
  },
  {
    "id": "real-m11-214430-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M11_214430_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb"
      }
    ],
    "target": "M11_214430 · observed"
  },
  {
    "id": "real-m5-172669-all",
    "arm": "all",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M5_172669_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb"
      }
    ],
    "target": "M5_172669 · observed"
  },
  {
    "id": "real-m5-172669-features",
    "arm": "features",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M5_172669_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb"
      }
    ],
    "target": "M5_172669 · observed"
  },
  {
    "id": "real-m5-172669-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M5_172669_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb"
      }
    ],
    "target": "M5_172669 · observed"
  },
  {
    "id": "real-m9-232005-all",
    "arm": "all",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M9_232005_all/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb"
      }
    ],
    "target": "M9_232005 · observed"
  },
  {
    "id": "real-m9-232005-features",
    "arm": "features",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M9_232005_features/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb"
      }
    ],
    "target": "M9_232005 · observed"
  },
  {
    "id": "real-m9-232005-features-downweight",
    "arm": "features_downweight",
    "status": "complete",
    "seed": 0,
    "artifacts": [
      {
        "label": "Saved posterior",
        "path": "results/absorption-mask/real_M9_232005_features_downweight/ceridwen_result.h5"
      },
      {
        "label": "Executed fit",
        "path": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb"
      }
    ],
    "target": "M9_232005 · observed"
  }
]
```

## Figures

```json
[
  {
    "path": "wiki/analyses/absorption-mask/mock_bias_vs_tilt.png",
    "view": "Comparison",
    "caption": "All three weighting modes retain tilt sensitivity in these mocks.",
    "target": ""
  },
  {
    "path": "wiki/analyses/absorption-mask/real_targets_posteriors.png",
    "view": "Comparison",
    "caption": "Real-target posterior shifts across weighting modes; the full-spectrum fit is the reference, not known truth.",
    "target": ""
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M11_214430 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M11_214430 · observed · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M11_214430 · observed · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M11_214430 · observed · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M11_214430 · observed · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M11_214430 · observed · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M11_214430 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M11_214430 · observed · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M11_214430 · observed · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 0.25 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 1 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · \\(\\mathrm{S/N}\\) scale 1.00 · seed 2 · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M5_172669 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M5_172669 · observed · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M5_172669 · observed · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M5_172669 · observed · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M5_172669 · observed · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M5_172669 · observed · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M5_172669 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M5_172669 · observed · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M5_172669 · observed · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · Ages · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M9_232005 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M9_232005 · observed · Photometry · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M9_232005 · observed · Spectrum · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M9_232005 · observed · Photometry · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M9_232005 · observed · Spectrum · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M9_232005 · observed · Photometry · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M9_232005 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M9_232005 · observed · SFH · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M9_232005 · observed · SFH · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Spectrum · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Ages · full spectrum, reference."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Posteriors · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Ages · feature windows only; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Posteriors · continuum downweighted; otherwise as full spectrum."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · Ages · continuum downweighted; otherwise as full spectrum."
  }
]
```

## Results

The saved summary contains 45 fits. Feature selection retains tilt sensitivity in the mocks and produces large real-target shifts. [All cells](results/absorption-mask/summary.csv).

[Mock bias versus tilt](wiki/analyses/absorption-mask/mock_bias_vs_tilt.png) · [Real-target posteriors](wiki/analyses/absorption-mask/real_targets_posteriors.png)

## Caveats

Real-target shifts are relative to the full-spectrum posterior, not known truth. Coverage estimates from the small mock grid are conditional on its injections.

## References

- [Summary with injected truth](results/absorption-mask/summary.csv)
- [Fisher diagnostic](results/absorption-mask/fisher_M5_172669.json)
- [Absorption line mask · source note](wiki/notes/absorption-line-mask.md)
- [Ceridwen results · source note](wiki/notes/ceridwen-results.md)
