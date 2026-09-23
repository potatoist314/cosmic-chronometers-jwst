---
kind: experiment
id: e-emission-line-marginalisation
title: Emission-line marginalisation test on M1_210210
date: 2026-09-23
results_at:
origin: new
status: planned
question: q-emission-lines
follow_up:
---

## Context

Compare the current default fit with the emission-line marginalisation option on M1_210210.

## Before delegation

```json
[
  {"date": "2026-09-23", "text": "just do a eline test right now, with higher spend"}
]
```

## Execution plan

- Comparison: two arms on M1_210210 with seed 20260832 on one instance.
- Baseline: `eline_off`, current notebook defaults, including COSMOS2025 photometry, Chebyshev order 10, constant prior 0.3, and baked runtime.
- Controlled change: `eline_on` sets `SETTINGS["emission_line_marginalisation"]` to `True`.
- Model: project branch `absorption-mask`; Ceridwen fork `1fae781`. The option uses 23 FSPS lines with nonnegative flat-prior fluxes, ties [O III] 4959/5007, excludes FSPS [O II] 3867, fixes redshift to the catalogue value, and adds lines to photometry.
- Hardware: one Vast.ai RTX 5060 or 5060 Ti at up to $0.20/h, reliability above 99.5%, total cap $0.50.
- Outputs: executed notebooks, spectrum and photometry fit figures for both arms, line fluxes with errors, parameter shifts, Hbeta-region residuals, runtime, likelihood calls, and cost.

## Amendments

```json
[]
```

## Runs

```json
[]
```

## Figures

```json
[]
```

## Measurements

## Results

## Caveats

## References

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
