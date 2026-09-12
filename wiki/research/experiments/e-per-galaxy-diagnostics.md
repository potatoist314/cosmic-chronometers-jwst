---
kind: experiment
id: e-per-galaxy-diagnostics
title: Per-galaxy residuals and GPU refit checks
date: 2026-09-06
origin: existing
status: recorded
question: q-population-results
related_questions: q-compute
source_notes: per-galaxy-fit-diagnostics,per-galaxy-diagnostics-gallery
result_groups: results/rtx-5060-per-galaxy-diagnostics-verification
---

## Context

Audit stored residuals and assembly histories for the baseline sample, then refit two targets using their recorded seeds.

## Runs

```json
[
  {
    "id": "m2-139662",
    "arm": "verification",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_139662",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/ceridwen_result.h5"
      }
    ],
    "seed": 20260949,
    "config": "results/rtx-5060-per-galaxy-diagnostics-verification/shard_1_manifest.json",
    "data": "results/rtx-5060-per-galaxy-diagnostics-verification/targets.json",
    "target": "M2_139662"
  },
  {
    "id": "m1-210210",
    "arm": "verification",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/ceridwen_result.h5"
      }
    ],
    "seed": 20260832,
    "config": "results/rtx-5060-per-galaxy-diagnostics-verification/shard_0_manifest.json",
    "data": "results/rtx-5060-per-galaxy-diagnostics-verification/targets.json",
    "target": "M1_210210"
  },
  {
    "id": "baseline-m2-139662",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M2_139662",
        "path": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/ceridwen_result.h5"
      }
    ],
    "seed": 20260949,
    "config": "results/rtx-5060-dr2-quiescent-full-spectrum/shard_1_manifest.json",
    "code": "0cc76d3b86a6889f497474c6a3ad04eb627a12fd",
    "model": "Ceridwen afe37fea1055901497154cfd0e27ce91fa47bfbd",
    "data": "results/rtx-5060-dr2-quiescent-full-spectrum/targets.json",
    "target": "M2_139662"
  },
  {
    "id": "baseline-m1-210210",
    "arm": "baseline",
    "status": "complete",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "Saved posterior",
        "path": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/ceridwen_result.h5"
      }
    ],
    "seed": 20260832,
    "config": "results/rtx-5060-dr2-quiescent-full-spectrum/shard_0_manifest.json",
    "code": "0cc76d3b86a6889f497474c6a3ad04eb627a12fd",
    "model": "Ceridwen afe37fea1055901497154cfd0e27ce91fa47bfbd",
    "data": "results/rtx-5060-dr2-quiescent-full-spectrum/targets.json",
    "target": "M1_210210"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "baseline-m1-210210",
    "target": "M1_210210",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M1_210210 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "baseline-m1-210210",
    "target": "M1_210210",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M1_210210 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "verification",
    "view": "Fits",
    "caption": "M1_210210 · verification refit. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "verification",
    "view": "Fits",
    "caption": "M1_210210 · verification refit. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 26,
    "output": 3,
    "run": "baseline-m1-210210",
    "target": "M1_210210",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M1_210210 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "verification",
    "view": "SFH",
    "caption": "M1_210210 · verification refit. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 26,
    "output": 0,
    "run": "baseline-m1-210210",
    "target": "M1_210210",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M1_210210 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "baseline-m1-210210",
    "target": "M1_210210",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M1_210210 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "verification",
    "view": "Posteriors",
    "caption": "M1_210210 · verification refit. Physical-parameter posterior."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "verification",
    "view": "Posteriors",
    "caption": "M1_210210 · verification refit. Age and formed-mass fractions."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "baseline-m2-139662",
    "target": "M2_139662",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M2_139662 · baseline. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "baseline-m2-139662",
    "target": "M2_139662",
    "arm": "baseline",
    "view": "Fits",
    "caption": "M2_139662 · baseline. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 25,
    "output": 0,
    "run": "m2-139662",
    "target": "M2_139662",
    "arm": "verification",
    "view": "Fits",
    "caption": "M2_139662 · verification refit. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 23,
    "output": 1,
    "run": "m2-139662",
    "target": "M2_139662",
    "arm": "verification",
    "view": "Fits",
    "caption": "M2_139662 · verification refit. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 26,
    "output": 3,
    "run": "baseline-m2-139662",
    "target": "M2_139662",
    "arm": "baseline",
    "view": "SFH",
    "caption": "M2_139662 · baseline. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 29,
    "output": 3,
    "run": "m2-139662",
    "target": "M2_139662",
    "arm": "verification",
    "view": "SFH",
    "caption": "M2_139662 · verification refit. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 26,
    "output": 0,
    "run": "baseline-m2-139662",
    "target": "M2_139662",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M2_139662 · baseline. Physical-parameter posterior."
  },
  {
    "notebook": "results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "baseline-m2-139662",
    "target": "M2_139662",
    "arm": "baseline",
    "view": "Posteriors",
    "caption": "M2_139662 · baseline. Age and formed-mass fractions."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 29,
    "output": 0,
    "run": "m2-139662",
    "target": "M2_139662",
    "arm": "verification",
    "view": "Posteriors",
    "caption": "M2_139662 · verification refit. Physical-parameter posterior."
  },
  {
    "notebook": "results/rtx-5060-per-galaxy-diagnostics-verification/139662-M2_139662/M2_139662_executed.ipynb",
    "cell": 29,
    "output": 1,
    "run": "m2-139662",
    "target": "M2_139662",
    "arm": "verification",
    "view": "Posteriors",
    "caption": "M2_139662 · verification refit. Age and formed-mass fractions."
  }
]
```

## Results

The source report gives median photometric chi2/N = 7.04 and spectral chi2/N = 1.120. The refit table records a 0.44 Gyr age change for M1_210210 and a smaller change for M2_139662. [All target diagnostics](results/per-galaxy-diagnostics.csv) · [GPU refit comparison](results/rtx-5060-per-galaxy-diagnostics-verification/refit_vs_production.csv).

## Caveats

Matching a seed does not reproduce the model implementation. The original report attributes the refit discrepancy to forward-model changes; use its recorded checks rather than treating these as pure seed repeats.

## References

- [Executed diagnostics](notebooks/ceridwen_per_galaxy_diagnostics.ipynb)
- [Audit report](reports/astro-chisq-sf-plots-2026-09-06.md)
- [GPU comparison](results/rtx-5060-per-galaxy-diagnostics-verification/refit_vs_production.csv)
- [per-galaxy-fit-diagnostics · source note](wiki/notes/per-galaxy-fit-diagnostics.md)
- [per-galaxy-diagnostics-gallery · source note](wiki/notes/per-galaxy-diagnostics-gallery.md)
