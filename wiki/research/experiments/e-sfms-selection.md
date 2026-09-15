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

Compare SFR100 and formed mass from the baseline and revised runs with the recorded Whitaker and Leja curves at \(z=0.73\).

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

The revised run has smaller quiescent fractions under both curves. [Old and revised SFR100 comparison](wiki/analyses/sfms-quiescent/sfms-quiescent.png).

## Caveats

The plotted mass is formed mass. The literature curves use a different stellar-mass convention.

Evidence paths were rewritten on 2026-09-15: `results/rtx-5060-dr2-quiescent-full-spectrum` and `results/dr2-quiescent-summary.csv` moved to `archive/results/dr2-quiescent-no-polynomial/` (no calibration polynomial; superseded by `results/dr2-quiescent-new-defaults`).

## References

- [Plot implementation](scripts/plot_sfms_quiescent.py)
- [Baseline SFR100 table](archive/results/dr2-quiescent-no-polynomial/dr2-quiescent-summary.csv)
- [Revised SFR100 table](results/dr2-quiescent-new-defaults-summary.csv)
- [sfms-quiescent · source note](wiki/notes/sfms-quiescent.md)
