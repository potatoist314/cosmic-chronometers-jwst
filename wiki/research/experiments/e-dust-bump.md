---
kind: experiment
id: e-dust-bump
title: New fit on a 5090 with Eb bump strength as free parameter
date: 2026-09-24
origin: new
status: planned
question: q-dust-index-railing
follow_up:
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
