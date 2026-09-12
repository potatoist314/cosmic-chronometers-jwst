---
kind: experiment
id: e-age-assembly-relations
title: Age–redshift and assembly-history comparisons
date: 2026-09-07
origin: existing
status: recorded
question: q-population-results
related_questions:
source_notes: dr2-quiescent-sample,dr2-new-defaults,ceridwen-results
result_groups: results/figures
---

## Context

Reanalyse the baseline and revised population fits against redshift, mass, alpha/Fe and the matched Borghi catalogue. No additional sampling.

## Results

Both saved runs have weak full-sample age–redshift trends. The existing figures include velocity-dispersion and oldest-fraction selections, plus assembly-history comparisons.

[Old and revised age–redshift](wiki/analyses/dr2-new-defaults/headline-age-redshift-old-vs-new.png) · [Oldest-fraction comparison](wiki/analyses/dr2-new-defaults/headline-age-redshift-oldest30.png) · [Assembly interval against alpha/Fe](wiki/analyses/dr2-quiescent-sample/dt-vs-alpha.png)

## Caveats

Ceridwen mass-weighted ages and Borghi SSP-equivalent ages are different quantities. A flat mixed-population trend alone does not diagnose fit failure. Assembly-history structure depends on the SFH time resolution.

## References

- [Baseline population notebook](results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer.ipynb)
- [Revised population notebook](results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb)
- [Oldest-fraction table](results/dr2-quiescent-new-defaults/age_redshift_oldest30.csv)
- [dr2-quiescent-sample · source note](wiki/notes/dr2-quiescent-sample.md)
- [dr2-new-defaults · source note](wiki/notes/dr2-new-defaults.md)
- [ceridwen-results · source note](wiki/notes/ceridwen-results.md)
