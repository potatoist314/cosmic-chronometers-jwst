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

## Results

Corrected photometry removes the strong tilt in one tested target; a substantial tilt remains in the other. [All 46 comparison rows](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv) and [In-band flux checks](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/ibands.csv) preserve the individual settings.

## Caveats

The source board attributes the remaining tilt to dust/model mismatch. This comparison alone does not establish that mechanism. Evidence remains at its existing worktree path.

## References

- [Executed tilt analysis](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/analysis.ipynb)
- [Comparison rows](tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv)
- [Earlier calibration rows](archive/results/calibration-polynomial-2026-09-02/arms.csv)
- [Ceridwen results · source note](wiki/notes/ceridwen-results.md)
