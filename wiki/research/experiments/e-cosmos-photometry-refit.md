---
kind: experiment
id: e-cosmos-photometry-refit
title: M1_210210 refit with COSMOS2020 Classic and COSMOS2025 photometry
date: 2026-09-21
results_at: 2026-09-21T22:36:55+01:00
origin: new
status: results-ready
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
[
  {
    "id": "cosmos2020-classic-seed20260832",
    "arm": "cosmos2020_classic",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/cosmos-photometry-refit/cosmos2020_classic/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/cosmos-photometry-refit/cosmos2020_classic/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/cosmos-photometry-refit/cosmos2020_classic/210210-M1_210210/execution.log"
      }
    ],
    "code": "00fd111",
    "model": "Ceridwen 5f2c316",
    "config": "results/cosmos-photometry-refit/vast_run_2026-09-21T211545+0000.json",
    "data": "results/cosmos-photometry-refit/cells.json",
    "seed": 20260832
  },
  {
    "id": "cosmos2025-seed20260832",
    "arm": "cosmos2025",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/cosmos-photometry-refit/cosmos2025/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/cosmos-photometry-refit/cosmos2025/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/cosmos-photometry-refit/cosmos2025/210210-M1_210210/execution.log"
      }
    ],
    "code": "066f614",
    "model": "Ceridwen 5f2c316",
    "config": "results/cosmos-photometry-refit/vast_run_2026-09-21T211545+0000.json",
    "data": "results/cosmos-photometry-refit/cells.json",
    "seed": 20260832
  }
]
```

## Figures

```json
[
  {
    "path": "wiki/analyses/cosmos-photometry-refit/spectrum-cosmos2015-M1_210210.png",
    "view": "Fits",
    "target": "M1_210210",
    "caption": "COSMOS2015 reference, 12 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges"
  },
  {
    "path": "wiki/analyses/cosmos-photometry-refit/spectrum-cosmos2020_classic-M1_210210.png",
    "view": "Fits",
    "target": "M1_210210",
    "caption": "COSMOS2020 Classic, 30 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges"
  },
  {
    "path": "wiki/analyses/cosmos-photometry-refit/spectrum-cosmos2025-M1_210210.png",
    "view": "Fits",
    "target": "M1_210210",
    "caption": "COSMOS2025, 28 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges"
  },
  {
    "path": "results/cosmos-photometry-refit/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "Physical-parameter posteriors with \\(1\\sigma\\) contours for the COSMOS2015 reference, COSMOS2020 Classic and COSMOS2025 fits of M1_210210."
  },
  {
    "path": "results/cosmos-photometry-refit/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "Star-formation history with 16–84% band and cumulative mass fraction for the COSMOS2015 reference, COSMOS2020 Classic and COSMOS2025 fits of M1_210210."
  }
]
```

## Measurements

| Quantity | COSMOS2015 | COSMOS2020 Classic | COSMOS2025 |
| --- | --- | --- | --- |
| Photometry | COSMOS2015 `cosmos_total` | COSMOS2020 Classic | COSMOS2025 |
| Bands | 12 | 30 | 28 |
| Photometric \(\chi^2\) | 55.0 | 146.5 | 144.8 |
| Spectral \(\chi^2\), catalogue uncertainties | 10772.1 | 10880.6 | 10869.6 |
| Spectral \(\chi^2\) at the reference fit's floor | 3655.0 | 3694.0 | 3684.3 |
| \(\ln Z\) | 231153.16 ± 0.35 | 231476.73 ± 0.24 | 231426.50 ± 0.28 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.650 ± 0.013 | 11.654 ± 0.011 | 11.597 ± 0.012 |
| \([\mathrm{Fe}/\mathrm{H}]\) | -0.159 ± 0.022 | -0.209 ± 0.024 | -0.201 ± 0.025 |
| \([\alpha/\mathrm{Fe}]\) | +0.060 ± 0.010 | +0.052 ± 0.010 | +0.051 ± 0.009 |
| \(\tau_{\mathrm{dust}}\) | 0.405 ± 0.013 | 0.407 ± 0.013 | 0.356 ± 0.013 |
| \(\delta_{\mathrm{dust}}\) | -0.987 ± 0.014 | -0.994 ± 0.007 | -0.994 ± 0.007 |
| \(t_{\mathrm{MW}}\) [Gyr] | 5.19 ± 0.12 | 5.12 ± 0.11 | 5.18 ± 0.13 |
| \(t_{20}\) [Gyr] | 3.77 ± 0.13 | 3.69 ± 0.11 | 3.75 ± 0.14 |
| \(t_{50}\) [Gyr] | 5.32 ± 0.17 | 5.25 ± 0.16 | 5.31 ± 0.17 |
| \(t_{80}\) [Gyr] | 6.67 ± 0.07 | 6.64 ± 0.07 | 6.66 ± 0.07 |
| \(f_{\mathrm{calib}}\) [%] | 2.52 ± 0.05 | 2.53 ± 0.05 | 2.54 ± 0.05 |
| \(z\) | 0.654219 ± 0.000015 | 0.654219 ± 0.000013 | 0.654220 ± 0.000015 |
| \(\sigma_\star\) [km/s] | 263.4 ± 3.1 | 267.1 ± 2.9 | 266.6 ± 3.2 |
| ESS | 4923 | 5499 | 5828 |
| Likelihood calls | 10 455 667 | 10 494 423 | 10 788 158 |
| Sampler wall time [s] | 1502 | 1025 | 1064 |
| Vast instance, spend | 51331110, $0.086 | 51958216, $0.180 for both |  |

Values are posterior median ± half the 16–84% width. All fits use seed 20260832 and 3523 spectral pixels.

## Results

- Order: COSMOS2015 reference / COSMOS2020 Classic / COSMOS2025; values are posterior median ± half the 16–84% width.
- \(\log_{10}(M_\star/M_\odot)\): 11.650 ± 0.013 / 11.654 ± 0.011 / 11.597 ± 0.012.
- \(\tau_{\mathrm{dust}}\): 0.405 ± 0.013 / 0.407 ± 0.013 / 0.356 ± 0.013.
- \([\mathrm{Fe}/\mathrm{H}]\): −0.159 ± 0.022 / −0.209 ± 0.024 / −0.201 ± 0.025.
- \([\alpha/\mathrm{Fe}]\): +0.060 ± 0.010 / +0.052 ± 0.010 / +0.051 ± 0.009.
- \(\delta_{\mathrm{dust}}\): −0.987 ± 0.014 / −0.994 ± 0.007 / −0.994 ± 0.007; the prior lower bound is −1.0.
- \(t_{\mathrm{MW}}\) [Gyr]: 5.19 ± 0.12 / 5.12 ± 0.11 / 5.18 ± 0.13.
- \(t_{50}\) [Gyr]: 5.32 ± 0.17 / 5.25 ± 0.16 / 5.31 ± 0.17.
- \(\sigma_\star\) [km/s]: 263.4 ± 3.1 / 267.1 ± 2.9 / 266.6 ± 3.2.
- \(z\): 0.65422 in all three fits; \(f_{\mathrm{calib}}\): 2.52 / 2.53 / 2.54%.
- Photometric \(\chi^2\) / bands: 55.0 / 12, 146.5 / 30, 144.8 / 28.
- Spectral \(\chi^2\) with catalogue uncertainties: 10772 / 10881 / 10870 over 3523 pixels.
- Largest photometric pull in both refits: \(u^*\), about −6 for Classic and −7 for COSMOS2025; the model is above the data.

## Caveats

- \(\ln Z\) values are not comparable between fits: the photometric data differ, with 12, 30 and 28 bands.
- `cosmos2020_classic`: the sampler finished on the GPU; the notebook then stopped in the photometry figure on both attempts.
- `xerr` was negative for `hsc_i`: its `sedpy_jax` `red_edge` lies below `wave_eff`. Fixed in commit `066f614`.
- The executed notebook and `ceridwen_derived_outputs.h5` were regenerated on CPU from the stored posterior with `scripts/regenerate_fit_notebooks.py`; the sampler was not re-run.
- `cosmos2025`: attempt 1 was stopped by hand after 4 minutes so attempt 2 used the fixed notebook; same seed.
- COSMOS2025 has no zero-point offsets because none are published; its Milky Way extinction uses COSMOS2020 Classic \(E(B-V)=0.015\).
- The photometry figure inside the executed notebooks was laid out for 12 bands; labels overlap with 30 or 28 bands. It is not shown here.
- One galaxy. The 5% error floor sets the photometric uncertainty in most bands.
- Liu Hao raised the price cap to $0.21/h for this rental only on 2026-09-21; the rule stays $0.11/h.

## References

- [cosmos-photometry-comparison](wiki/notes/cosmos-photometry-comparison.md)
- [cosmos-photometry-refit](wiki/notes/cosmos-photometry-refit.md)
- [e-m1-210210-reference](wiki/research/experiments/e-m1-210210-reference.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
