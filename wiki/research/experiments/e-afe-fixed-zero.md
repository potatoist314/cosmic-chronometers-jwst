---
kind: experiment
id: e-afe-fixed-zero
title: M1_210210 old-MIST comparison: MILES control grid and afe fixed at 0.0
date: 2026-09-23
results_at:
origin: new
status: planned
question: q-dust-index-railing
follow_up:
---

## Context

Sandro Tacchella's check: do the old MIST models (not alpha-enhanced) show the same dust-index railing and weak UV? The current grid `amist_c3k_hr_krou_afe` is the alpha-MC set of Park et al. (2025).

Its \([\alpha/\mathrm{Fe}] = 0.0\) plane keeps the same MIST isochrone family, C3K-HR library, Kroupa IMF, wavelength grid, and age and metallicity nodes. It is the cheap control.

The old-MIST arm cannot use C3K-HR: FSPS 3.2 ships only downsampled C3K (11,149 points, R at most 3000) or MILES, with 12 metallicity nodes at \(Z_\odot = 0.0142\), while the high-resolution spectra exist only in the Park FITS. The kept control is MIST v1.2 with MILES and the Kroupa IMF, matching the age nodes only.

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

- Comparison: three fits of M1_210210, same seed: `afe_sampled` (current defaults), `afe_fixed_0`, and `old_mist_miles`.
- Baseline: arm `afe_sampled`; reference `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2025 photometry with Classic fallback; seed 20260812.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at current defaults; grid `amist_c3k_hr_krou_afe`; calibration order 10 with fitted constant; BlackJAX NSS `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled changes: `SETTINGS["fix_afe"]` None → 0.0 for `afe_fixed_0`; `SETTINGS["ssp_grid"]` to the local `mist_miles_krou_afe1.h5` for `old_mist_miles`. Single-plane grids fix \([\alpha/\mathrm{Fe}]\) at their plane.
- Outputs: executed notebooks under `results/afe-fixed-zero/<arm>/210210-M1_210210/`; spectrum-fit and photometry-fit figures per arm.

## Amendments

```json
[
  {
    "date": "2026-09-23",
    "text": "old models",
    "display_text": "Old models.",
    "source_ref": "Correction: compare against the old non-alpha MIST models (MIST v1.2 in FSPS), not only the alpha-MC [alpha/Fe]=0 plane"
  }
]
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
  },
  {
    "id": "old-mist-miles-m1-210210",
    "arm": "old_mist_miles",
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

Preparation only; no fit has run. `scripts/check_mist_comparison.py` reuses notebook cells 2, 4, 6, 8 and the cell-10 likelihood setup verbatim and evaluates one joint log-likelihood at theta_init on CPU per option: default 206338.683449 (sampled), `fix_afe=0.0` 206218.544531, MILES control 205223.121219, all finite. The control grid is `mist_miles_krou_afe1.h5` (MIST v1.2, MILES, Kroupa, single \([\alpha/\mathrm{Fe}]\) plane), built by `scripts/build_mist_miles_krou_afe1.py`.

## Caveats

The corner-plot cell of the notebook names \([\alpha/\mathrm{Fe}]\) directly, so executed fixed-alpha copies need that panel skipped or dropped.

The MILES control also differs in wavelength grid (5,994 points) and resolution. Its shape also disables the CSP SFH fastpath, which needs a (5, 13, 107) grid.

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [model](wiki/notes/model.md)
- Notebook `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, cells 2 (`fix_afe`, `ssp_grid`), 8 (model)
- Check `scripts/check_mist_comparison.py`; control build `scripts/build_mist_miles_krou_afe1.py`
- Park et al. (2025), ApJ 994, 165, arXiv:2410.21375: `papers/spectral fitting/Alpha-MC - Self-consistent Alpha-enhanced Stellar Population Models Covering a Wide Range of Age, Metallicity, and Wavelength.pdf`
- Grid registry `ceridwen/ceridwen/ssps/grid_fetch.py` (`amist_c3k_hr_krou_afe`); build `ceridwen/scripts_afe/build_afe_hr_grid.py`
- FSPS 3.2 (`external/fsps/README.md`): MIST added in v3.0 (`doc/REVISION_HISTORY`); isochrone and library are independent compile switches (`doc/MANUAL.pdf` §2.1.1, `src/sps_vars.f90`); no alpha support in `src/`; shipped C3K is downsampled (`SPECTRA/C3K/readme.md`, `nspec=11149`); MIST \(Z_\odot = 0.0142\) over 12 nodes (`doc/MANUAL.pdf` Table 1)
- Roadmap task `p-1b7c64b9-ce3b-4c29-890e-d0f30c458412`, [direction](wiki/research/direction.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
