---
kind: experiment
id: e-afe-fixed-zero
title: M1_210210 fit with afe fixed at 0.0 on the current grid
date: 2026-09-23
results_at:
origin: new
status: planned
question: q-dust-index-railing
follow_up:
---

## Context

Sandro Tacchella's check: do the old MIST models (not alpha-enhanced) show the same dust-index railing and weak UV? The current grid `amist_c3k_hr_krou_afe` is the alpha-MC set of Park et al. (2025).

Its \([\alpha/\mathrm{Fe}] = 0.0\) plane keeps the same MIST isochrone family, C3K-HR library, Kroupa IMF, wavelength grid, and age and metallicity nodes. The comparison fits \([\alpha/\mathrm{Fe}]\) sampled versus fixed at 0.0.

## Before delegation

```json
[
  {
    "date": "2026-09-23",
    "text": "i want you to make preparations for testing older non alpha enhanced MIST models with the current alpha enhanced model to see how it varies. ideally everything is identical for the SSP/isochrone except",
    "display_text": "I want preparations for testing older non alpha-enhanced MIST models against the current alpha-enhanced model, to see how it varies. Ideally everything is identical for the SSP/isochrone except (message cut off here)."
  },
  {
    "date": "2026-09-23",
    "text": "why are grids being built? do non alpha scaled grids not exist?",
    "display_text": "Why are grids being built? Do non alpha-scaled grids not exist?"
  }
]
```

## Execution plan

- Comparison: two fits of M1_210210, same seed: `afe_sampled` (current defaults) and `afe_fixed_0`.
- Baseline: arm `afe_sampled`; reference `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2025 photometry with Classic fallback; seed 20260812.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at current defaults; grid `amist_c3k_hr_krou_afe`; calibration order 10 with fitted constant; BlackJAX NSS `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `SETTINGS["fix_afe"]` None → 0.0. At None, \([\alpha/\mathrm{Fe}]\) keeps its Uniform grid prior; at 0.0 it is set by transform and leaves the prior set.
- Outputs: executed notebooks under `results/afe-fixed-zero/<arm>/210210-M1_210210/`; spectrum-fit and photometry-fit figures per arm.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "afe-sampled-m1-210210",
    "arm": "afe_sampled",
    "status": "planned"
  },
  {
    "id": "afe-fixed-0-m1-210210",
    "arm": "afe_fixed_0",
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

Preparation only; no fit has run. `scripts/check_afe0_likelihood.py` reuses notebook cells 2, 4, 6, 8 and the cell-10 likelihood setup verbatim with `fix_afe=0.0` and evaluates the joint photometry+spectrum log-likelihood once at theta_init on CPU: 206218.544531, finite. The parameter block confirms \([\alpha/\mathrm{Fe}]\) fixed at 0 and absent from the priors.

## Caveats

The corner-plot cell of the notebook names \([\alpha/\mathrm{Fe}]\) directly, so the executed `afe_fixed_0` copy needs that panel skipped or dropped. The \([\alpha/\mathrm{Fe}] = 0.0\) plane replaces a MIST+MILES Kroupa control grid.

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [model](wiki/notes/model.md)
- Notebook `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, cells 2 (`fix_afe`), 8 (model)
- Check `scripts/check_afe0_likelihood.py`
- Park et al. (2025), ApJ 994, 165, arXiv:2410.21375: `papers/spectral fitting/Alpha-MC - Self-consistent Alpha-enhanced Stellar Population Models Covering a Wide Range of Age, Metallicity, and Wavelength.pdf`
- Grid registry `ceridwen/ceridwen/ssps/grid_fetch.py` (`amist_c3k_hr_krou_afe`); build `ceridwen/scripts_afe/build_afe_hr_grid.py`
- Roadmap task `p-1b7c64b9-ce3b-4c29-890e-d0f30c458412`, [direction](wiki/research/direction.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
