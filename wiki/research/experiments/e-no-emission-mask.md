---
kind: experiment
id: e-no-emission-mask
title: M1_210210 fit without the emission-line mask
date: 2026-09-21
origin: new
status: planned
question: q-fitting-choices
follow_up:
---

## Context

The production fit masks ±1500 km/s around rest-frame 3726.0, 3728.8 ([O II]), 4861.3 (H-beta), 4958.9 and 5006.8 ([O III]) Å: about 190 Å, covering the H-beta age feature and Fe5015. The DR2 quiescent sample is selected on |EW/sigma_EW| < 3 for [O II] and [O III].

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "but without the mask this could offer better fitting / parameter constraints, no?",
    "display_text": "But without the mask this could offer better fitting / parameter constraints, no?"
  },
  {
    "date": "2026-09-21",
    "text": "yes, put a worker on the fit",
    "display_text": "Yes, put a worker on the fit."
  }
]
```

## Execution plan


- Comparison: fit M1_210210 without an emission-line mask against the stored masked fit, using the same seed.
- Baseline: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`, not re-run; calibration order 10; `tau_dust` Uniform(0, 1); free `zred` and `sigma_star`; seed 20260832; ceridwen `c540bc7`; config `results/m1-210210-reference/tau-1/vast_run_2026-09-17T175951+0000.json`.
- Data: LEGA-C DR2 spectrum M1_210210; joint fit with COSMOS2015 `cosmos_total` photometry, 12 bands.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`; grid `amist_c3k_hr_krou_afe`; ceridwen `b419fd1` (`c540bc7` plus per-iteration progress logging in `sampler/nested.py`, no sampling change); Student-t SFH prior; free dust index; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `SETTINGS['emission_lines'] = []` only; telluric mask 7590–7660 Å air kept; arm `no_emission_mask` of `scripts/calibration_arms_vast.py` sets `CERIDWEN_SETTINGS_OVERRIDE={"emission_lines": []}`; `scripts/run_ceridwen_vast_multi_gpu.py` merges it into `SETTINGS` in the executed copy; template default unchanged.
- Analysis: `results/no-emission-mask/analysis.ipynb`; shift of each sampled parameter in units of the baseline posterior half-width; posterior-width change; KL bits from the prior for both arms; derived mass-weighted age included; comparison figure designed by the designer agent.
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%, bandwidth under $5/TB; `results/no-emission-mask/no_emission_mask/210210-M1_210210/` with the executed notebook (fit, SFH, corner, KL figure); a wiki note.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "no-emission-mask-m1-210210",
    "arm": "no_emission_mask",
    "status": "planned"
  }
]
```

## Figures

```json
[]
```

## Measurements

## Results

## Caveats

## References

- [Masked baseline fit](results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb)
- [Baseline run configuration](results/m1-210210-reference/tau-1/vast_run_2026-09-17T175951+0000.json)
- [M1_210210 reference fit · note](wiki/notes/m1-210210-reference.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
