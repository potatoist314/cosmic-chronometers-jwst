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
    "caption": "M11_214430 · observed · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M11_214430 · observed · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M11_214430 · observed · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M11_214430 · observed · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M11_214430 · observed · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M11_214430 · observed · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M11_214430 · observed · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M11_214430 · observed · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M11_214430 · observed · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_all/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-all",
    "target": "M11_214430 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-features",
    "target": "M11_214430 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M11_214430_features_downweight/M11_214430_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m11-214430-features-downweight",
    "target": "M11_214430 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M11_214430 · observed · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 0.25 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.00_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p00-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.00 · S/N scale 1.00 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 0.25 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.03_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p03-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.03 · S/N scale 1.00 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr0.25_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr0p25-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 0.25 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed1_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed1-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 1 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-all",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-features",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/mock_tilt0.06_snr1.00_seed2_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "mock-tilt0p06-snr1p00-seed2-features-downweight",
    "target": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M1_210210 · mock tilt 0.06 · S/N scale 1.00 · seed 2 · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M5_172669 · observed · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M5_172669 · observed · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M5_172669 · observed · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M5_172669 · observed · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M5_172669 · observed · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M5_172669 · observed · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M5_172669 · observed · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M5_172669 · observed · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M5_172669 · observed · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_all/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-all",
    "target": "M5_172669 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-features",
    "target": "M5_172669 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M5_172669_features_downweight/M5_172669_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m5-172669-features-downweight",
    "target": "M5_172669 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M5_172669 · observed · continuum downweighted. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M9_232005 · observed · full spectrum. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Fits",
    "caption": "M9_232005 · observed · full spectrum. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M9_232005 · observed · feature windows. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Fits",
    "caption": "M9_232005 · observed · feature windows. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M9_232005 · observed · continuum downweighted. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 23,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Fits",
    "caption": "M9_232005 · observed · continuum downweighted. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "SFH",
    "caption": "M9_232005 · observed · full spectrum. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "SFH",
    "caption": "M9_232005 · observed · feature windows. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 3,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "SFH",
    "caption": "M9_232005 · observed · continuum downweighted. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · full spectrum. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_all/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-all",
    "target": "M9_232005 · observed",
    "arm": "all",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · full spectrum. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · feature windows. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-features",
    "target": "M9_232005 · observed",
    "arm": "features",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · feature windows. Age and formed-mass fractions."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 0,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · continuum downweighted. Physical-parameter posterior."
  },
  {
    "notebook": "results/absorption-mask/real_M9_232005_features_downweight/M9_232005_executed.ipynb",
    "cell": 27,
    "output": 1,
    "run": "real-m9-232005-features-downweight",
    "target": "M9_232005 · observed",
    "arm": "features_downweight",
    "view": "Posteriors",
    "caption": "M9_232005 · observed · continuum downweighted. Age and formed-mass fractions."
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
