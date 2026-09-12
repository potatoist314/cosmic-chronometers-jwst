---
kind: experiment
id: e-four-gpu-fits
title: Four-target RTX 4070 SUPER campaign
date: 2026-08-26
origin: existing
status: recorded
question: q-compute
related_questions:
source_notes: ceridwen-results,vast-ai-gpu-workflow
result_groups: results/rtx-4070-super-four-galaxy-fits
---

## Context

Four independently seeded full-profile fits, one target per RTX 4070 SUPER worker.

## Runs

```json
[
  {
    "id": "m1-210210",
    "arm": "full",
    "status": "complete",
    "seed": 20260812,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210/m1_210210_executed.ipynb"
      }
    ],
    "target": "M1_210210"
  },
  {
    "id": "m12-181945",
    "arm": "full",
    "status": "complete",
    "seed": 20260813,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_1_m12_181945/m12_181945_executed.ipynb"
      }
    ],
    "target": "M12_181945"
  },
  {
    "id": "m2-133501",
    "arm": "full",
    "status": "complete",
    "seed": 20260814,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_2_m2_133501/m2_133501_executed.ipynb"
      }
    ],
    "target": "M2_133501"
  },
  {
    "id": "m14-38648",
    "arm": "full",
    "status": "complete",
    "seed": 20260815,
    "config": "results/rtx-4070-super-four-galaxy-fits/run_manifest.json",
    "artifacts": [
      {
        "label": "Executed fit",
        "path": "results/rtx-4070-super-four-galaxy-fits/gpu_3_m14_38648/m14_38648_executed.ipynb"
      }
    ],
    "target": "M14_38648"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_1_m12_181945/m12_181945_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "m12-181945",
    "target": "M12_181945",
    "arm": "full",
    "view": "Fits",
    "caption": "M12_181945 · full. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_1_m12_181945/m12_181945_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "m12-181945",
    "target": "M12_181945",
    "arm": "full",
    "view": "Fits",
    "caption": "M12_181945 · full. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_1_m12_181945/m12_181945_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "m12-181945",
    "target": "M12_181945",
    "arm": "full",
    "view": "SFH",
    "caption": "M12_181945 · full. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_3_m14_38648/m14_38648_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "m14-38648",
    "target": "M14_38648",
    "arm": "full",
    "view": "Fits",
    "caption": "M14_38648 · full. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_3_m14_38648/m14_38648_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "m14-38648",
    "target": "M14_38648",
    "arm": "full",
    "view": "Fits",
    "caption": "M14_38648 · full. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_3_m14_38648/m14_38648_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "m14-38648",
    "target": "M14_38648",
    "arm": "full",
    "view": "SFH",
    "caption": "M14_38648 · full. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210/m1_210210_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "full",
    "view": "Fits",
    "caption": "M1_210210 · full. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210/m1_210210_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "full",
    "view": "Fits",
    "caption": "M1_210210 · full. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210/m1_210210_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "m1-210210",
    "target": "M1_210210",
    "arm": "full",
    "view": "SFH",
    "caption": "M1_210210 · full. Saved SFH and posterior interval."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_2_m2_133501/m2_133501_executed.ipynb",
    "cell": 24,
    "output": 0,
    "run": "m2-133501",
    "target": "M2_133501",
    "arm": "full",
    "view": "Fits",
    "caption": "M2_133501 · full. Spectrum and residuals on the saved wavelength grid."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_2_m2_133501/m2_133501_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "m2-133501",
    "target": "M2_133501",
    "arm": "full",
    "view": "Fits",
    "caption": "M2_133501 · full. Photometry and residuals; bands and uncertainty model are those of this run."
  },
  {
    "notebook": "results/rtx-4070-super-four-galaxy-fits/gpu_2_m2_133501/m2_133501_executed.ipynb",
    "cell": 26,
    "output": 1,
    "run": "m2-133501",
    "target": "M2_133501",
    "arm": "full",
    "view": "SFH",
    "caption": "M2_133501 · full. Saved SFH and posterior interval."
  }
]
```

## Results

The manifest records all four workers complete. Their executed notebooks retain the fitted spectra and posterior outputs.

## Caveats

This early campaign uses its recorded full-profile settings. It is not a matched speed comparison with later DR2 campaigns.

## References

- [Campaign manifest](results/rtx-4070-super-four-galaxy-fits/run_manifest.json)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
- [vast-ai-gpu-workflow · source note](wiki/notes/vast-ai-gpu-workflow.md)
