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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
    ]
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
