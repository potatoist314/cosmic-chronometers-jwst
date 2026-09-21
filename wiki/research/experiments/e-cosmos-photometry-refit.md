---
kind: experiment
id: e-cosmos-photometry-refit
title: M1_210210 refit with COSMOS2020 Classic and COSMOS2025 photometry
date: 2026-09-21
origin: new
status: planned
question: q-cosmos-photometry
follow_up:
---

## Context

The Ceridwen fits use COSMOS2015 `cosmos_total` photometry, 12 bands. COSMOS2020 Classic and COSMOS2025 were matched to the 187 fitted galaxies on 2026-09-21; `cosmos-photometry-comparison` holds the per-band comparison for M1_210210. No fit with either catalogue exists.

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "High research priority (10) - incorporate COSMOS 2020/2025 photometry as a replacement for 2015 and see what changes in the fit"
  },
  {
    "date": "2026-09-21",
    "text": "yes, download new catalogs and match and compare"
  },
  {
    "date": "2026-09-21",
    "text": "COSMOS2020 Classic (Recommended), COSMOS2025 (COSMOS-Web), no zero point or extinction for JWST?"
  },
  {
    "date": "2026-09-21",
    "text": "All bands (Recommended)"
  }
]
```

## Execution plan

- Comparison: two refits of M1_210210, one per photometry catalogue, against the stored COSMOS2015 reference fit, using the same seed.
- Baseline: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`; COSMOS2015 `cosmos_total`, 12 bands; seed 20260832.
- Data: LEGA-C DR2 spectrum M1_210210, unchanged; photometry from `data/raw/cosmos2020/` and `data/raw/cosmos2025/` through `scripts/cosmos_photometry.py`.
- Arm `cosmos2020_classic`: Weaver et al. (2022) recipe; 2″ aperture flux with per-object `totaloff2`; IRAC and GALEX already total; Milky Way extinction from per-object \(E(B-V)\); Weaver Table 3 LePhare/Classic zero-point offsets; `FlagCOMBINED == 0`; 30 bands; CFHT u skipped because no `sedpy_jax` curve exists.
- Arm `cosmos2025`: total SE++ model flux; calibrated error `e_Flux-c-mod`; Milky Way extinction from the COSMOS2020 Classic match’s per-object \(E(B-V)\); no zero-point offsets, none published in Shuntov et al. (2025); `warn-flag == 0`; 28 bands including HST F814W and JWST F115W, F150W, F277W, F444W.
- Both arms: every catalogue band with a `sedpy_jax` curve (Liu Hao, 2026-09-21: “All bands”); extinction factors from Laigle et al. (2016) Table 3 \(F\), interpolated in log wavelength for other bands; 5% error floor.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at current defaults; grid `amist_c3k_hr_krou_afe`; ceridwen `5f2c316`; calibration order 10; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `SETTINGS["photometry"]`, arms `cosmos2020_classic` and `cosmos2025` of `scripts/calibration_arms_vast.py`; the notebook default stays `cosmos_total`.
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%, bandwidth under $5/TB; both fits on the same instance; `results/cosmos-photometry-refit/<arm>/210210-M1_210210/` with the executed notebooks; a wiki note.

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

- [cosmos-photometry-comparison](wiki/notes/cosmos-photometry-comparison.md)
- [e-m1-210210-reference](wiki/research/experiments/e-m1-210210-reference.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
