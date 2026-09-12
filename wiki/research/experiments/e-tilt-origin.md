---
kind: experiment
id: e-tilt-origin
title: Photometry corrections and residual spectral tilt
date: 2026-09-04
origin: existing
status: recorded
question: q-fitting-choices
related_questions:
source_notes: ceridwen-results
result_groups: tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02,archive/results/calibration-polynomial-2026-09-02
---

## Context

Earlier calibration work compares aperture/total photometry, attenuation choices and spectral polynomials for M4_108989 and M5_172669.

## Figures

```json
[
  {
    "path": "tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/photometry-residuals.png",
    "view": "Fits",
    "caption": "Photometric residuals across the saved aperture, calibration and attenuation settings.",
    "target": ""
  },
  {
    "path": "tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/sfh-histories.png",
    "view": "SFH",
    "caption": "Saved SFH comparisons across the two targets and recorded settings.",
    "target": ""
  },
  {
    "path": "tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/posteriors.png",
    "view": "Posteriors",
    "caption": "Parameter posteriors across the recorded comparisons; these changes do not isolate one physical cause.",
    "target": ""
  },
  {
    "path": "tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/polynomial-vectors.png",
    "view": "Comparison",
    "caption": "Corrected photometry removes the strong tilt in one target; the other retains a substantial tilt.",
    "target": ""
  }
]
```

## Results

Corrected photometry removes the strong tilt in one tested target; a substantial tilt remains in the other. [All 46 comparison rows](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv) and [In-band flux checks](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/ibands.csv) preserve the individual settings.

## Caveats

The source board attributes the remaining tilt to dust/model mismatch. This comparison alone does not establish that mechanism. Evidence remains at its existing worktree path.

## References

- [Executed tilt analysis](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/analysis.ipynb)
- [Comparison rows](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv)
- [Earlier calibration rows](archive/results/calibration-polynomial-2026-09-02/arms.csv)
- [Ceridwen results · source note](wiki/notes/ceridwen-results.md)
