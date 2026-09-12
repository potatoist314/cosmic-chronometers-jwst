---
kind: experiment
id: e-sfms-selection
title: Inferred SFR100 against the star-forming sequence
date: 2026-09-07
origin: existing
status: recorded
question: q-sample-selection
related_questions: q-population-results
source_notes: sfms-quiescent
result_groups:
---

## Context

Compare SFR100 and formed mass from the baseline and revised runs with the recorded Whitaker and Leja curves at z = 0.73.

## Figures

```json
[
  {
    "path": "wiki/analyses/sfms-quiescent/sfms-quiescent.png",
    "view": "Comparison",
    "caption": "Baseline and revised SFR100. The plotted formed mass differs from the literature mass convention; the IMF offset alone does not resolve this.",
    "target": ""
  }
]
```

## Results

The source reports smaller quiescent fractions for the revised run under both curves. [Old and revised SFR100 comparison](wiki/analyses/sfms-quiescent/sfms-quiescent.png).

## Caveats

The plotted mass is formed mass. The literature comparison uses a different stellar-mass convention; the IMF offset alone does not resolve that mismatch. These fractions therefore do not directly validate or overturn the catalogue selection.

## References

- [Plot implementation](scripts/plot_sfms_quiescent.py)
- [Baseline SFR100 table](results/dr2-quiescent-summary.csv)
- [Revised SFR100 table](results/dr2-quiescent-new-defaults-summary.csv)
- [sfms-quiescent · source note](wiki/notes/sfms-quiescent.md)
