---
name: checking-ceridwen-state
description: Use before you discuss, propose or run a Ceridwen experiment. One command prints each current fit setting and prior, its comment, the experiments that changed it, and the experiments that are planned, running or recent.
---

# Check the Ceridwen state

Liu Hao, 2026-09-30: "marginalisation is already implemented to some extent. you
should be aware of that. hm. there should be a skill that tracks the running
progress/state of the experiment and settings".

A lead discussed emission-line marginalisation as a new feature. It was already
`SETTINGS["emission_line_marginalisation"]`, with the record
`wiki/research/experiments/e-emission-line-marginalisation.md`.

Before you discuss, propose or run a Ceridwen experiment, run this command from the
project root. It reads local files only. It rents nothing.

```bash
python3 scripts/ceridwen_state.py
```

The command reads the live sources. Do not copy its output into a file. Run it again.
The examples below are from the run of 2026-09-30.

## The five blocks of the output

1. **`SETTINGS`.** Each entry of `SETTINGS` in
   `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: the value, then the
   comment from the notebook. An option that is off is in this list.
   ```
   emission_line_marginalisation = False
       True: FSPS lines get free fluxes >= 0 in the calibration solve, shared with the photometry; z fixed; lines leave the mask
   metallicity_evolution = False
       True: Z rises with formed mass, Gallazzi+26 Table 1; Z is then log10 of the formed-mass-weighted metallicity
       e-dust-bump ran zevo=true
   ```
   The line `e-dust-bump ran zevo=true` shows that an `experiment.json` changed the
   entry. `e-dust-bump` is the record. `zevo` is the arm. `true` is the value.
2. **`PRIORS`.** The same for each entry of `PRIORS`.
3. **`FIXED IN THE CSPBasis_afe CALL`.** The options that the notebook sets in code
   and not in `SETTINGS`. The dust law is here, with the laws that `sedpy_jax` has.
   ```
   diffuse_law = 'noll'
       registered laws (external/sedpy_jax/sedpy_jax/attenuation_dust.py): smc, lmc, kriek_conroy, powerlaw, calzetti, drude, noll, chevallard, cardelli, conroy
   ```
4. **`EXPERIMENT RECORDS`.** Each record in `wiki/research/experiments/` that is
   planned or running, or that has results from the last 14 days. Each record shows
   the id, status, date, question, title, arms and result directories.
   ```
   e-dust-bump  results-ready  2026-09-30  q-dust-index-railing
       New fit on a 5090 with Eb bump strength as free parameter
       arms: default14 3 failed, 1 complete; dust_index_m3 1 complete; wide 1 failed, 1 complete; zevo 1 failed, 1 complete
       results/m1-210210-kcbump-2026-09-29  $0.76 invoiced
   ```
   `python3 scripts/ceridwen_state.py --days 3` shows results from the last 3 days.
5. **`RUN DIRECTORIES IN NO RECORD`.** Each result directory with an
   `experiment.json` and a run manifest that no record lists in `result_groups`.
   A quick fit is here.
   ```
   results/speedup-ablations-2026-09-30  $0.23 invoiced
       results/speedup-ablations-2026-09-30/run  3/3 fits complete, last attempt complete, manifest written 2026-09-30 11:53
       sampler: inner46={"num_inner_steps": 46}, inner23={"num_inner_steps": 23}, delete250={"num_delete": 250}
   ```

## Limits of the output

- A `ran` line exists only for a run that has an `experiment.json`. These are the
  runs of `scripts/experiment.py`. An entry without a `ran` line can have a record.
  Find the record with the key:
  ```bash
  grep -l emission_line_marginalisation wiki/research/experiments/*.md
  ```
  On 2026-09-30 this printed `wiki/research/experiments/e-emission-line-marginalisation.md`.
- The output does not give the result of an experiment. Read the section Results of
  the record before you speak about the result.
- `$ invoiced` is the sum of the `charges.json` files that `scripts/experiment.py`
  saved. A directory without `charges.json` shows no amount. Its record gives the cost.
- A line `NOT A CURRENT KEY` shows an `experiment.json` key that the notebook does
  not have now.

## Related rules

- For priorities and direction, read `AGENTS.md`, section "Research priorities".
- To run a fit, use the `running-ceridwen-experiments` skill.
- For the fields of a record, read `wiki/research/README.md`.
