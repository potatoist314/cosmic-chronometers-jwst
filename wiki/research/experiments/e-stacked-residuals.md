---
kind: experiment
id: e-stacked-residuals
title: Native-pixel residual stacks and feature pulls
date: 2026-09-10
origin: existing
status: recorded
question: q-population-results
related_questions: q-fitting-choices
source_notes: stacked-chi2-and-median-pull
result_groups: results/dr2-quiescent-new-defaults
---

## Context

Stack fitted native pixels from the revised 187-target run in rest-frame bins. Compare five stacking recipes and bootstrap over galaxies.

## Results

The recorded median per-galaxy reduced chi2 is 1.086; median stacked mean pull squared is 1.149. Ca, Balmer, Mg and Fe windows show coherent residuals across the recipes. [Source table and method](wiki/notes/stacked-chi2-and-median-pull.md).

[Native-pixel stack](wiki/analyses/dr2-quiescent-sample/stacked-pull.png) · [Feature pulls](wiki/analyses/dr2-quiescent-sample/stacked-pull-by-feature.png)

## Caveats

The older interpolated stack and its extra error scaling were superseded. The archived Q&A still discusses that earlier version. Bootstrap uncertainty accounts for galaxy-to-galaxy variation; interpret low-coverage wavelength bins separately.

## References

- [Stacking implementation](scripts/plot_dr2_stacked_pull.py)
- [Revised input table](results/dr2-quiescent-new-defaults-summary.csv)
- [stacked-chi2-and-median-pull · source note](wiki/notes/stacked-chi2-and-median-pull.md)
