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
2. **Configure.** Write `experiment.json` in the experiment's result directory.
   Use the production notebook's `SETTINGS` and `PRIORS` keys. Do not edit its
   defaults to configure an experiment. Example:
   ```json
   {
     "targets": ["M1_210210"],
     "seed": 20260832,
     "settings": {},
     "priors": {},
     "arms": {
       "baseline": {},
       "wide_dust": {"priors": {"diffuse_tau_kc": "Uniform(low=0.0, high=2.0)"}}
     }
   }
   ```
   Each arm merges its changes into the shared settings and priors. Nested
   settings merge too. Priors are Python expression strings. `settings.ssp_grid`
   accepts a registered name or a local `.h5` path relative to this JSON file.
   The exact seed applies to every fit. New model code must be committed before
   running; the command uses committed HEAD and pinned submodules.
3. **Check.** Use `--dry-run` to check the configuration and local inputs without
   rentals or network access. It requires cached grids. Show the targets, changes,
   baseline and cap if those choices still need the user's approval. Existing
   authorization covers execution; do not ask for the same approval again.
4. **Run.** Use this command for new experiment fits:
   ```bash
   python3 scripts/experiment.py run results/<slug>/experiment.json \
     --gpu "RTX 5090" --output results/<slug>/run
   ```
   Use the GPU type requested by the user. The runner selects the lowest hourly
   price above 99.5% reliability, falling back to above 96% only if no offers
   pass all filters. Both bandwidth rates must be below $10/TB. The total $1
   cap covers all arms and retries; `--spend-cap` can reduce it.

   Missing registered grids download locally before rental. The command uploads
   pinned source and checked grids, runs the full notebook including existing
   post-fit plots, downloads each arm-target result, and destroys its rental.
   Results are under `run/fits/<arm>/<object>-<target>/`: executed notebook,
   `ceridwen_result.h5`, derived outputs and logs. The run directory also holds
   the manifest, stage logs and available charges. Repeat the same command and
   `--output` to resume its source, configuration, completed fits and budget.
   Do not manually rent replacements. The historical arm-specific runners remain
   for their existing runs.
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

Local SSH errors stop before rental. Use an execution environment authorized to run
SSH; waiting for the GPU cannot fix a local user-ID error. The shared upload
includes HST cutouts and the emission-line table. A nonzero remote stage exit
saves its log, destroys the owned rental and stops. Diagnose the log before
repeating the command; do not rent a replacement for the same code or input error.
