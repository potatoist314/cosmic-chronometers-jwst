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

## Figures

```json
[
  {
    "path": "wiki/analyses/dr2-quiescent-sample/stacked-pull.png",
    "view": "Comparison",
    "caption": "187 revised fits, stacked on native pixels. Median mean pull squared is 1.149; the null expectation is 1.",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-quiescent-sample/M11_216899-spectrum.png",
    "view": "Comparison",
    "caption": "M11_216899: revised fit; contributes 79% of summed pull² in the 3672 Å rest-frame bin (about 6234 Å observed).",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-quiescent-sample/M12_184916-spectrum.png",
    "view": "Comparison",
    "caption": "M12_184916: revised fit; contributes 86% of summed pull² in the 5566 Å rest-frame bin (about 9348 Å observed).",
    "target": ""
  },
  {
    "path": "wiki/analyses/dr2-quiescent-sample/stacked-pull-by-feature.png",
    "view": "Comparison",
    "caption": "Feature pulls with galaxy-bootstrap errors; coherent Ca, Balmer, Mg and Fe residuals remain across stacking recipes.",
    "target": ""
  }
]
```

## Results

The recorded median per-galaxy reduced chi2 is 1.086; median stacked mean pull squared is 1.149. Ca, Balmer, Mg and Fe windows show coherent residuals across the recipes. [Source table and method](wiki/notes/stacked-chi2-and-median-pull.md).

[Native-pixel stack](wiki/analyses/dr2-quiescent-sample/stacked-pull.png) · [Feature pulls](wiki/analyses/dr2-quiescent-sample/stacked-pull-by-feature.png)

## Caveats

The older interpolated stack and its extra error scaling were superseded. The archived Q&A still discusses that earlier version. Bootstrap uncertainty accounts for galaxy-to-galaxy variation; interpret low-coverage wavelength bins separately.

## References

- [Stacking implementation](scripts/plot_dr2_stacked_pull.py)
- [Revised input table](results/dr2-quiescent-new-defaults-summary.csv)
- [stacked-chi2-and-median-pull · source note](wiki/notes/stacked-chi2-and-median-pull.md)
- [M11_216899 executed fit](results/dr2-quiescent-new-defaults/216899-M11_216899/M11_216899_executed.ipynb) — spectrum: cell 26, output 0 (zero-based).
- [M12_184916 executed fit](results/dr2-quiescent-new-defaults/184916-M12_184916/M12_184916_executed.ipynb) — spectrum: cell 26, output 0 (zero-based).
