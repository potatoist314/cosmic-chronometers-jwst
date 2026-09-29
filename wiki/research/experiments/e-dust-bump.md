---
kind: experiment
id: e-dust-bump
title: New fit on a 5090 with Eb bump strength as free parameter
date: 2026-09-24
origin: new
results_at: 2026-09-29T21:19:50+01:00
status: results-ready
question: q-dust-index-railing
follow_up:
source_notes: m1-210210-kcbump
result_groups: results/m1-210210-kcbump-2026-09-29
---

## Context

M1_210210 is the fixed reference galaxy (LEGA-C DR2, \(z = 0.6542\)). In the
birth-cloud experiment the linked-bump fits rail the dust slope at the \(-1\)
prior edge with weak UV, while the slope-to-\(-3\) arm fits the UV bands far
better.

Freeing the 2175 A bump amplitude \(E_b\) independently of the slope is the
follow-up. Preparation started against `kriek_conroy_free_bump`; the Noll-law
implementation landed as `0588f9b` before the run.

## Before delegation

```json
[
  {
    "date": "2026-09-24",
    "text": "read and understand the experiment/fitting skills, then can you run a new fit on a 5090 with the new change (Eb bump strength as free parameter)",
    "display_text": "Read and understand the experiment/fitting skills, then run a new fit on a 5090 with the new change (Eb bump strength as a free parameter)."
  }
]
```

## Execution plan

- Comparison: one fit of M1_210210 at HEAD production defaults against the stored `dust1_on` fit with the linked bump, same seed.
- Baseline: run `dust1-on-5090-recovery`, `results/birth-cloud-dust/dust1_on/210210-M1_210210`; code `3d24700`; birth-cloud dust on via override; linked Kriek & Conroy bump; \(\ln Z\) 231446.95 ± 0.24; seed 20260832.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2025 photometry, 28 bands; seed 20260832.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at HEAD; grid `amist_c3k_hr_krou_afe`; ceridwen `1fae781`; calibration order 10 with fitted constant; emission-line marginalisation off; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: diffuse dust law Kriek & Conroy (linked bump) → Noll with independent slope and bump. Notebook `PRIORS`: `diffuse_tau_noll` Uniform(0, 1), `diffuse_delta` Uniform(-1, 0.4), `diffuse_Ebump` Uniform(0, 6); `diffuse_law="noll"` unconditionally.
- Birth-cloud dust is on in both fits (notebook default now, override in the baseline). Arm `free_bump` of `results/dust-bump/experiment.json` pins no overrides, so the run uses the production defaults; the linked-law side is the stored baseline fit only.
- Hardware and outputs: one Vast.ai RTX 5090, cheapest above 99.5% reliability, bandwidth under $10/TB; spend cap $1; `results/dust-bump/run/fits/free_bump/210210-M1_210210/` with the executed notebook; a wiki note. Scouted 2026-09-24: 20 of 49 offers pass the strict tier, cheapest $0.4852/h on-demand.
- Run command: `python3 scripts/experiment.py run results/dust-bump/experiment.json --gpu "RTX 5090" --output results/dust-bump/run`.

## Amendments

```json
[
  {
    "date": "2026-09-24",
    "text": "pause - there will be a change to implementation of free bump parameter."
  },
  {
    "date": "2026-09-24",
    "text": "make preparations - once the change lands it should just be an immediate one line to run the experiment",
    "display_text": "Make preparations: once the change lands it should just be an immediate one line to run the experiment."
  },
  {
    "date": "2026-09-29",
    "text": "okay, run that test",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-29",
    "text": "oh i mean this is a fresh run - spend cap applies for fresh"
  },
  {
    "date": "2026-09-29",
    "text": "show me the plots on the wiki",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-29",
    "text": "include the previous steep dust law fit for comparison, i want to see how sfh changes",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-29",
    "text": "i just want my usual corner plots, sfh against time etc in accordance with the standard wiki",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-29",
    "text": "i don't see it in results. always put this stuff in results",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Runs

```json
[
  {
    "id": "default14-run1",
    "arm": "default14",
    "status": "failed",
    "error": "driver stopped by KeyboardInterrupt at 16:03 and 16:24 UTC; instances 53382374 and 53384393 destroyed; 41 lines in ns_progress.jsonl; no result file",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "driver.log",
        "path": "results/m1-210210-kcbump-2026-09-29/driver.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-kcbump-2026-09-29/run/manifest.json"
      },
      {
        "label": "execution.log",
        "path": "results/m1-210210-kcbump-2026-09-29/run/fits/default14/210210-M1_210210/execution.log"
      }
    ],
    "code": "da0d1d5",
    "model": "Ceridwen 1fae781; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe",
    "config": "results/m1-210210-kcbump-2026-09-29/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-kcbump-2026-09-29/run/manifest.json"
  },
  {
    "id": "default14-run2",
    "arm": "default14",
    "status": "failed",
    "error": "driver stopped by KeyboardInterrupt at 16:49 UTC; instance 53388474 destroyed; next attempt on instance 53389781 lost name resolution for console.vast.ai at 17:06 UTC; destroy call failed, instance kept billing ($0.552) until destroyed later; no result file retrieved",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "driver.log",
        "path": "results/m1-210210-kcbump-2026-09-29/driver.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-kcbump-2026-09-29/run2/manifest.json"
      },
      {
        "label": "charges.json",
        "path": "results/m1-210210-kcbump-2026-09-29/run2/charges.json"
      }
    ],
    "code": "71c6622",
    "model": "Ceridwen 37f04b0; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe",
    "config": "results/m1-210210-kcbump-2026-09-29/run2/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-kcbump-2026-09-29/run2/manifest.json"
  },
  {
    "id": "default14-run3-remote",
    "arm": "default14",
    "status": "failed",
    "error": "stage fit-0 exited 1, KeyError 'diffuse_Ebump' in the prior-KL plot cell after the sampler finished; ceridwen_result.h5 retrieved; instance 53410690 destroyed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "fit-0 log",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/53410690-fit-0.log"
      },
      {
        "label": "execution.log",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/execution.log"
      },
      {
        "label": "ns_progress.jsonl",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/ns_progress.jsonl"
      }
    ],
    "code": "d522c76",
    "model": "Ceridwen 37f04b0; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe",
    "config": "results/m1-210210-kcbump-2026-09-29/run3/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-kcbump-2026-09-29/run3/manifest.json"
  },
  {
    "id": "default14-run3-recovery",
    "arm": "default14",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "Executed analysis",
        "path": "results/m1-210210-kcbump-2026-09-29/analysis.ipynb"
      }
    ],
    "code": "787f9b9",
    "model": "Ceridwen 37f04b0; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe",
    "config": "results/m1-210210-kcbump-2026-09-29/run3/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-kcbump-2026-09-29/run3/manifest.json"
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
    "notebook": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "default14-run3-recovery",
    "target": "M1_210210",
    "arm": "default14",
    "view": "Fits",
    "caption": "M1_210210 · kcbump. Spectrum over fitted pixels; joint posterior median and 16–84% band; lower-panel pull at fitted noise floor."
  },
  {
    "notebook": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "default14-run3-recovery",
    "target": "M1_210210",
    "arm": "default14",
    "view": "Fits",
    "caption": "M1_210210 · kcbump. Observed 28-band fluxes with per-band posterior medians (16–84%); lower-panel per-band pulls."
  },
  {
    "notebook": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "dust-index-m3-5090",
    "target": "M1_210210",
    "arm": "dust_index_m3",
    "view": "Fits",
    "caption": "M1_210210 · m3. Spectrum over fitted pixels; joint posterior median and 16–84% band; lower-panel pull at fitted noise floor."
  },
  {
    "notebook": "results/birth-cloud-dust/dust_index_m3/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "dust-index-m3-5090",
    "target": "M1_210210",
    "arm": "dust_index_m3",
    "view": "Fits",
    "caption": "M1_210210 · m3. Observed 28-band fluxes with per-band posterior medians (16–84%); lower-panel per-band pulls."
  },
  {
    "notebook": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "default14-run3-recovery",
    "target": "M1_210210",
    "arm": "default14",
    "view": "SFH",
    "caption": "M1_210210 · kcbump. Normalized SFR against lookback time; median and 16–84% band."
  },
  {
    "path": "results/m1-210210-kcbump-2026-09-29/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "M1_210210 · kcbump / m3. SFR per formed mass [yr⁻¹] against lookback time with 16–84% bands; right-panel cumulative mass fraction."
  },
  {
    "notebook": "results/m1-210210-kcbump-2026-09-29/run3/fits/default14/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "default14-run3-recovery",
    "target": "M1_210210",
    "arm": "default14",
    "view": "Posteriors",
    "caption": "M1_210210 · kcbump. Physical-parameter posteriors for log M*, [Fe/H], [α/Fe], τ_dust, f_calib, Δv_z, σ*, t_MW."
  },
  {
    "path": "results/m1-210210-kcbump-2026-09-29/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "M1_210210 · kcbump / m3. Physical-parameter posteriors with 1-sigma contours for log M*, [Fe/H], [α/Fe], τ_dust, δ_dust, E_bump, t_MW; m3 E_bump is tied to 0.85 − 1.9 δ_dust."
  }
]
```

## Measurements

## Results

- Order: `kcbump` / `m3`; values are posterior median [16, 84] from `results/m1-210210-kcbump-2026-09-29/comparison.csv`.
- \(\ln Z\): 231476.11 ± 0.22 / 231501.86 ± 0.40. ESS: 4635 / 4267. Sampler wall: 318.7 s / 274.6 s.
- Spectral \(\chi^2\) with catalogue uncertainties: 10768.3 / 10725.3 over 3523 pixels; at the `kcbump` floor: 3440.7 / 3427.5.
- Photometric \(\chi^2\) / 28 bands: 89.4 / 48.0. CFHT \(u^*\) pull: −4.32 / +0.06.
- \(\delta_{\mathrm{dust}}\): −0.987 [−0.997, −0.967] / −2.361 [−2.515, −2.212]; the `kcbump` prior lower bound is −1, `m3` uses Uniform(−3, 0.4).
- \(E_{\mathrm{bump}}\): 5.86 [5.63, 5.96] / 5.34 [5.05, 5.63]; the `kcbump` prior upper bound is 6, `m3` is tied to \(0.85 - 1.9\delta_{\mathrm{dust}}\).
- \(\tau_{\mathrm{dust}}\): 0.323 [0.313, 0.334] / 0.143 [0.127, 0.158].
- \(\tau_{\mathrm{bc}}/\tau_{\mathrm{dust}}\) (`kcbump`): 1.21 [0.98, 1.44].
- \(\log_{10}(M_\star/M_\odot)\): 11.544 [11.529, 11.559] / 11.538 [11.526, 11.551].
- \([\mathrm{Fe}/\mathrm{H}]\): −0.142 [−0.163, −0.122] / −0.117 [−0.141, −0.096].
- \([\alpha/\mathrm{Fe}]\): 0.050 [0.040, 0.060] / 0.069 [0.059, 0.078].
- \(t_{\mathrm{MW}}\) [Gyr]: 4.44 [4.21, 4.66] / 5.14 [5.02, 5.28].
- \(t_{20}, t_{50}, t_{80}\) [Gyr]: 3.14, 4.20, 5.84 / 3.72, 5.27, 6.65.
- \(\sigma_\star\) [km/s]: 265.8 [262.6, 268.9] / 262.5 [259.6, 265.5].
- Checks: `run3` remote stage `fit-0` exited 1 at the prior-KL plot cell with `KeyError 'diffuse_Ebump'`, after the sampler finished and `ceridwen_result.h5` was saved; 264 lines in `ns_progress.jsonl`. Commit `787f9b9` added the three Noll labels to `scripts/plot_prior_kl.py`; post-fit cells re-run locally on CPU from the stored HDF5 with `sedpy_jax 9d8aa19`.
- Validation: `scripts.experiment.validate_result` passes: finite weights and evidence, derived groups, `diagnostics.passed` true, no notebook errors. `results/m1-210210-kcbump-2026-09-29/analysis.ipynb` writes `comparison.csv`, `sfh-M1_210210.png`, `corner-M1_210210.png`.
- Compute: `run3` on RTX 5090 instance 53410690 at $0.458/h; $0.088 billed, instance destroyed. Earlier attempts: `run` $0.118 (instances 53382374, 53384393), `run2` $0.555 (instances 53388474, 53389781).

## Caveats

- `kcbump` \(\delta_{\mathrm{dust}}\) median −0.987 is at its −1 prior bound; \(E_{\mathrm{bump}}\) median 5.86 is at its 6 prior bound.
- `m3` \(E_{\mathrm{bump}}\) is not a free parameter.
- The arms differ in dust law and bump, \(\delta_{\mathrm{dust}}\) prior, birth-cloud dust, SFH bins, ceridwen commit and seed.
- Stored spectral \(\chi^2\) uses each fit's own \(f_{\mathrm{calib}}\); the comparison uses the `kcbump` floor.
- The execution plan named baseline `dust1_on`, seed 20260832, ceridwen `1fae781` and output `results/dust-bump/run`; `run3` used seed 20260927, ceridwen `37f04b0`, `sedpy_jax 9d8aa19` and 14 SFH bins. The comparison arm is `dust_index_m3` per the 2026-09-29 amendment.
- One galaxy.

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [e-birth-cloud-dust](wiki/research/experiments/e-birth-cloud-dust.md)
- Roadmap task `dust-index-railing-weak-uv`, [direction](wiki/research/direction.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
