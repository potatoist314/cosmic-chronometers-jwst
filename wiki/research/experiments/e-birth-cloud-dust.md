---
kind: experiment
id: e-birth-cloud-dust
title: M1_210210 fit with birth-cloud dust (dust1) on, and with the dust index down to −3
date: 2026-09-23
results_at:
origin: new
status: planned
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
  }
]
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
