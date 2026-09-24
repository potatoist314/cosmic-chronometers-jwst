---
kind: experiment
id: e-birth-cloud-dust
title: M1_210210 fit with birth-cloud dust (dust1) on, and with the dust index down to −3
date: 2026-09-23
results_at: 2026-09-24T12:09:29+00:00
origin: new
status: results-ready
question: q-birth-cloud-dust
follow_up:
---

## Context

Sandro Tacchella, Slack, 23 Sep 2026: "did you switch on dust1 (birth cloud dust)?" `wiki/notes/model.md` lists birth-cloud dust as off. The fit uses diffuse Kriek & Conroy (2013) dust only (\(\tau_{\mathrm{dust}}\), \(\delta_{\mathrm{dust}}\)); \(\delta_{\mathrm{dust}}\) sits at its prior edge of \(-1\).

## Before delegation

```json
[
  {
    "date": "2026-09-23",
    "text": "Can you try a fit with the both cloud does turned on?",
    "display_text": "Can you try a fit with the birth cloud dust turned on?",
    "source_ref": "Spoken on his watch, transcribed"
  }
]
```

## Execution plan

- Comparison: three fits of M1_210210 on one instance, same seed: `dust1_off` (current defaults), `dust1_on` and `dust_index_m3`.
- Baseline: arm `dust1_off`; the stored reference `results/m1-210210-reference/tau-1/poly10/210210-M1_210210` predates the polynomial-constant normalisation and `baked_runtime` defaults.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2015 `cosmos_total` photometry, 12 bands; seed 20260832.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at current defaults; grid `amist_c3k_hr_krou_afe`; ceridwen `6fc7539`; calibration order 10 with fitted constant; emission-line marginalisation off; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `SETTINGS["birth_cloud_dust"]` False → True. On: Ceridwen `Dust` power law, `add_dust=True`, on SSP ages up to 10 Myr (bin edge \(10^{-1.97}\) Gyr), added to the diffuse Kriek & Conroy screen.
- Birth-cloud law: \(\tau_{\mathrm{bc}}(\lambda) = r_{\mathrm{dust}}\,\tau_{\mathrm{dust}}\,(\lambda/5500\,\text{Å})^{-1}\); \(r_{\mathrm{dust}}\) ~ ClippedNormal(1, 0.3) on [0, 2]; index fixed at \(-1\). Prospector `dust1 = dust_ratio × dust2`.
- Arm `dust_index_m3`: birth-cloud dust off; \(\delta_{\mathrm{dust}}\) prior Uniform(\(-1\), 0.4) → Uniform(\(-3\), 0.4), set through `CERIDWEN_PRIORS_OVERRIDE` in the executed copy; the notebook default stays Uniform(\(-1\), 0.4).
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%, bandwidth under $5/TB; spend cap $0.25; `results/birth-cloud-dust/<arm>/210210-M1_210210/` with the executed notebooks; a wiki note.

## Amendments

```json
[
  {
    "date": "2026-09-23",
    "text": "also try a fit of -3 and see if it converges (-3 on dust)",
    "source_ref": "Sandro Tacchella's check: could you run the fit with allowing even steeper slopes, all the way down to -3 to see if it will converge?"
  },
  {
    "date": "2026-09-24",
    "text": "get a muse worker to run the dust cloud experiment on the cheapest 5090, bypassing the normal cost limit",
    "source_ref": "Task instruction; total task ceiling $5"
  }
]
```

## Runs

```json
[
  {
    "id": "dust1-off-seed20260832",
    "arm": "dust1_off",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/birth-cloud-dust/dust1_off/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/birth-cloud-dust/dust1_off/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/birth-cloud-dust/dust1_off/210210-M1_210210/execution.log"
      }
    ],
    "code": "232aab1",
    "model": "Ceridwen 1fae781",
    "config": "results/birth-cloud-dust/vast_run_2026-09-23T221813+0000.json",
    "data": "results/birth-cloud-dust/cells.json",
    "seed": 20260832
  },
  {
    "id": "dust1-on-seed20260832",
    "arm": "dust1_on",
    "status": "failed",
    "error": "spend cap $0.32 reached after 10 NSS iterations; instance destroyed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "execution.log",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/execution.log"
      }
    ],
    "code": "232aab1",
    "model": "Ceridwen 1fae781",
    "config": "results/birth-cloud-dust/vast_run_2026-09-23T221813+0000.json",
    "data": "results/birth-cloud-dust/cells.json",
    "seed": 20260832
  },
  {
    "id": "dust1-on-5090-remote",
    "arm": "dust1_on",
    "status": "failed",
    "error": "attempt 1 finished 27700 draws but the box validator expected 6 physical groups; dust_ratio makes 7; attempt-2 identical rerun terminated (SIGTERM) after the HDF5 was verified; remote manifest failed, returncode -15",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "execution.log",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/execution.log"
      },
      {
        "label": "ns_progress.jsonl",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/ns_progress.jsonl"
      },
      {
        "label": "arms.log",
        "path": "results/birth-cloud-dust/arms.log"
      }
    ],
    "code": "3d24700",
    "model": "Ceridwen 1fae781",
    "config": "results/birth-cloud-dust/vast_run_2026-09-24T120929+0000.json",
    "data": "results/birth-cloud-dust/cells.json",
    "seed": 20260832
  },
  {
    "id": "dust1-on-5090-recovery",
    "arm": "dust1_on",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/birth-cloud-dust/dust1_on/210210-M1_210210/ceridwen_derived_outputs.h5"
      }
    ],
    "code": "3d24700",
    "model": "Ceridwen 1fae781",
    "config": "results/birth-cloud-dust/vast_run_2026-09-24T120929+0000.json",
    "data": "results/birth-cloud-dust/cells.json",
    "seed": 20260832
  },
  {
    "id": "dust-index-m3-5090",
    "arm": "dust_index_m3",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "execution.log",
        "path": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/execution.log"
      }
    ],
    "code": "3d24700",
    "model": "Ceridwen 1fae781",
    "config": "results/birth-cloud-dust/vast_run_2026-09-24T120929+0000.json",
    "data": "results/birth-cloud-dust/cells.json",
    "seed": 20260832
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/birth-cloud-dust/dust1_off/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "dust1-off-seed20260832",
    "target": "M1_210210",
    "arm": "dust1_off",
    "view": "Fits",
    "caption": "M1_210210 · birth-cloud dust off. Spectrum over fitted pixels; joint posterior median and 16–84% band; lower-panel pull at fitted noise floor."
  },
  {
    "notebook": "results/birth-cloud-dust/dust1_off/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "dust1-off-seed20260832",
    "target": "M1_210210",
    "arm": "dust1_off",
    "view": "Fits",
    "caption": "M1_210210 · birth-cloud dust off. Observed 28-band fluxes with per-band posterior medians (16–84%); lower-panel per-band pulls."
  },
  {
    "notebook": "results/birth-cloud-dust/dust1_on/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "dust1-on-5090-recovery",
    "target": "M1_210210",
    "arm": "dust1_on",
    "view": "Fits",
    "caption": "M1_210210 · birth-cloud dust on. Spectrum over fitted pixels; joint posterior median and 16–84% band; lower-panel pull at fitted noise floor."
  },
  {
    "notebook": "results/birth-cloud-dust/dust1_on/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "dust1-on-5090-recovery",
    "target": "M1_210210",
    "arm": "dust1_on",
    "view": "Fits",
    "caption": "M1_210210 · birth-cloud dust on. Observed 28-band fluxes with per-band posterior medians (16–84%); lower-panel per-band pulls."
  },
  {
    "notebook": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "dust-index-m3-5090",
    "target": "M1_210210",
    "arm": "dust_index_m3",
    "view": "Fits",
    "caption": "M1_210210 · dust index prior down to −3. Spectrum over fitted pixels; joint posterior median and 16–84% band; lower-panel pull at fitted noise floor."
  },
  {
    "notebook": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "dust-index-m3-5090",
    "target": "M1_210210",
    "arm": "dust_index_m3",
    "view": "Fits",
    "caption": "M1_210210 · dust index prior down to −3. Observed 28-band fluxes with per-band posterior medians (16–84%); lower-panel per-band pulls."
  },
  {
    "path": "results/birth-cloud-dust/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "M1_210210. Star-formation history with 16–84% band and cumulative mass fraction for the off, on and m3 arms."
  },
  {
    "path": "results/birth-cloud-dust/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "M1_210210. Physical-parameter posteriors with 1-sigma contours for the off, on and m3 arms."
  }
]
```

## Measurements

## Results

- Order: `dust1_off` / `dust1_on` / `dust_index_m3`; values are posterior median ± half the 16–84% width from `results/birth-cloud-dust/comparison.csv`. Same seed 20260832, spectrum, 28 COSMOS2025 bands and NSS settings in all three.
- \(\ln Z\): 231432.39 ± 0.22 / 231446.95 ± 0.24 / 231501.86 ± 0.40. ESS: 4560 / 4930 / 4267.
- Spectral \(\chi^2\) with catalogue uncertainties: 10855.5 / 10840.9 / 10725.3 over 3523 pixels; at the `dust1_off` floor: 3357.2 / 3353.0 / 3321.8.
- Photometric \(\chi^2\) / 28 bands: 146.8 / 118.2 / 48.0. CFHT \(u^*\) pull: −7.38 / −6.31 / +0.06.
- \(\delta_{\mathrm{dust}}\): −0.994 ± 0.007 / −0.992 ± 0.009 / −2.361 ± 0.151; the off/on prior lower bound is −1, m3 uses Uniform(−3, 0.4).
- \(r_{\mathrm{dust}}\) (`dust_ratio`, on): 1.375 ± 0.221.
- \(\log_{10}(M_\star/M_\odot)\): 11.587 ± 0.011 / 11.585 ± 0.010 / 11.538 ± 0.012.
- \([\mathrm{Fe}/\mathrm{H}]\): −0.181 ± 0.021 / −0.184 ± 0.020 / −0.117 ± 0.023.
- \([\alpha/\mathrm{Fe}]\): +0.050 ± 0.010 / +0.054 ± 0.011 / +0.069 ± 0.009.
- \(\tau_{\mathrm{dust}}\): 0.353 ± 0.011 / 0.332 ± 0.011 / 0.141 ± 0.016.
- \(t_{\mathrm{MW}}\) [Gyr]: 5.07 ± 0.12 / 5.14 ± 0.12 / 5.14 ± 0.13.
- Checks: `dust_index_m3` done on attempt 1, sampler wall 340.1 s. Both arms pass full validation with `diagnostics.passed` true. `results/birth-cloud-dust/analysis.ipynb` executed locally; outputs `comparison.csv`, `sfh-M1_210210.png`, `corner-M1_210210.png`.
- Compute: on-demand RTX 5090 offer 47794369 at $0.7347/h (host 43746, reliability 0.997). Instance 52400715 spent $0.9962 and was destroyed; no instances left. Run file `results/birth-cloud-dust/vast_run_2026-09-24T120929+0000.json`.

## Caveats

- The box ran the branch default photometry, COSMOS2025, 28 bands; the default changed from COSMOS2015 after the execution plan.
- `dust1_on` stopped after 10 NSS iterations and `dust_index_m3` did not start: the driver's account-credit spend reached the $0.32 run cap at 22:18 UTC.
- Instances 52298088, 52298461, 52299165 destroyed; the account showed no instances after the run.
- `dust1_on` remote status is `failed`: attempt 1 finished 27700 draws but the box validator expected 6 physical groups; `dust_ratio` makes 7. The identical attempt-2 rerun was terminated (SIGTERM, returncode −15) after the HDF5 was verified.
- `dust1_on` recovery is a separate local run: the HDF5 reloaded with finite weights and \(\ln Z\) 231446.95 ± 0.24, and the post-fit cells were regenerated on CPU with the corrected validator; full validation passed.
- `dust1_on` `ns_progress.jsonl` mixes three segments: the 23 September partial prefix (10 lines), the completed attempt (272 lines) and the terminated rerun prefix (20 lines).
- Offer selection used the worktree-local `--only-5090` patch on branch `birth-cloud-5090`; the box ran `absorption-mask` at `3d24700`, whose fit path is unchanged since `b0c2ca4`.

## References

- [e-m1-210210-reference](wiki/research/experiments/e-m1-210210-reference.md)
- [e-cosmos-photometry-refit](wiki/research/experiments/e-cosmos-photometry-refit.md)
- [model](wiki/notes/model.md)
- [e-dust-slope](wiki/research/experiments/e-dust-slope.md)
- Roadmap task `p-03df19b8-1627-4f43-a51d-1601bbadaf7a`, [direction](wiki/research/direction.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
