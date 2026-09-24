---
name: running-ceridwen-experiments
description: Use when Liu Hao asks to change a fit setting or a prior of the Ceridwen fit, run the fit on Vast.ai, pull the results and put them on the wiki.
---

# Run one Ceridwen experiment

Written from the M1_210210 order-10 run of 2026-09-17
(`wiki/research/experiments/e-m1-210210-reference.md`).
Rules are in `AGENTS.md` and `wiki/research/README.md`. Read them. Do not copy them here.

## Steps

1. **Record.** Copy `wiki/research/templates/experiment.md` to
   `wiki/research/experiments/e-<slug>.md`, status `planned`. Put his chat text
   in **Before delegation** unchanged. Write the **Execution plan** as in
   `e-m1-210210-reference.md`: comparison, baseline, data, model, controlled change,
   hardware and outputs. Commit.
2. **Change the fit.** Edit `SETTINGS` or `PRIORS` in cell 2 of
   `notebooks/ceridwen_integrated_photometry_spectra.ipynb`. Commit and push:
   the Vast box clones `absorption-mask`.
3. **Show the plan and wait.** One table: target, changed setting (old → new),
   baseline result directory, seed, spend cap. Do not rent before he says OK.
4. **Run.** Default target M1_210210, seed 20260832. Baseline:
   `results/m1-210210-reference/tau-1/poly10/210210-M1_210210` (production defaults, 2026-09-17).
   ```
   CERIDWEN_ARMS_RESULTS=results/<slug> python scripts/calibration_arms_vast.py run \
     --arms <arm> --targets M1_210210 --interruptible --spend-cap 1
   ```
   The total experiment cap is $1 including retries. The driver rents one RTX 5060, 5060 Ti, 5070, 5080 or 5090 at the lowest
   hourly price, with reliability above 99.5% and bandwidth below $10/TB, clones the branch, uploads `ceridwen/` and
   `data/raw`, bootstraps CUDA, runs the notebook, polls every 2 min, pulls, destroys.
   Output: `results/<slug>/<arm>/<object>-<target>/` with `M1_210210_executed.ipynb`,
   `ceridwen_result.h5`, `execution.log`; `results/<slug>/vast_run_<timestamp>.json`
   with the instance id and the spend. The M1_210210 fit took 26 min and $0.086.
5. **Evaluate.** Write `results/<slug>/analysis.ipynb` (start from
   `results/m1-210210-reference/analysis.ipynb`). Run it locally with
   `JAX_PLATFORMS=cpu ceridwen/.venv/bin/python`. Outputs beside it:
   `fit-<target>.png`, `sfh-<target>.png`, `corner-<target>.png`, `comparison.csv`.
   `scripts/plot_prior_kl.py` writes the KL-from-prior chart and table.
6. **Wiki.** Copy the PNGs to `wiki/analyses/<slug>/`. Write `wiki/notes/<slug>.md`
   with the frontmatter and sections of `wiki/notes/m1-210210-reference.md`. In the
   record fill Runs, Figures, Measurements, Results, Caveats; status `results-ready`.
   Add one line to `wiki/index.md` and one entry to `wiki/log.md`. Then
   `python3 wiki/build.py` and `python3 wiki/tests/run_tests.py`.
7. **Finish.** Commit and push. Reply with the measurement table and the paths.
   Status `reviewed` only after his interpretation is in the record.
