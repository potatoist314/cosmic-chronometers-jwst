---
name: running-ceridwen-experiments
description: Configure and run Ceridwen fits on Vast.ai, retrieve results, and verify local artifacts. Add analysis or wiki reports only when requested.
---

# Run one Ceridwen experiment

## Default scope: fit and retrieve

A request to run or try a fit means configure, run, retrieve, validate, and report.
Prioritise a working fit and reliable local results. Do not create an experiment
write-up, separate analysis notebook, extra plots, wiki page, or prose-review task
unless the user requests that deliverable. Existing notebook plots still run.
Do not delay launch or retrieval for documentation or a documentation-only commit.

Read `AGENTS.md`. For a quick fit, the configuration, pinned source, seed, manifest,
stage logs, and result files are the reproducibility record. Keep only a short
Beads status with the output path and any blocker. Read `wiki/research/README.md`
only if research records or wiki publication are part of the request.

New runs use the compact dependency image pinned in `scripts/vast.py`, selected
input files, and cached grids. Do not replace it with a generic CUDA image.
Use `--image` only for an explicitly requested override. Saved runs keep their image.

## Steps

1. **Configure.** Write `experiment.json` in the experiment's result directory.
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
       "wide_dust": {"priors": {"diffuse_tau_noll": "Uniform(low=0.0, high=2.0)"}}
     }
   }
   ```
   Each arm merges its changes into the shared settings and priors. Nested
   settings merge too. Priors are Python expression strings. `settings.ssp_grid`
   accepts a registered name or a local `.h5` path relative to this JSON file.
   The exact seed applies to every fit. New model code must be committed before
   running; the command uses committed HEAD and pinned submodules.
2. **Check.** Use `--dry-run` to check the configuration and local inputs without
   rentals or network access. It requires cached grids. Show the targets, changes,
   baseline and cap if those choices still need the user's approval. Existing
   authorization covers execution; do not ask for the same approval again.
3. **Run.** Use this command for new experiment fits:
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
4. **Verify retrieval.** Check every requested arm and target in the local
   manifest against `run/fits/`. Run `scripts.experiment.validate_result` locally
   on each result directory using `ceridwen/.venv/bin/python`. It opens the result
   HDF5, checks finite weights and evidence, checks derived groups and diagnostics,
   and checks the executed notebook for errors. Confirm the logs were retrieved.
   A remote success message or an existing filename is not enough.

   If retrieval or validation fails, preserve the partial files and logs. Diagnose
   whether the fit, post-processing, or transfer failed. Recover available outputs
   before considering another paid fit. Resume through the runner with the same
   configuration and output directory, within the remaining cap. Do not delete
   completed results or blindly rerun the sampler to repair missing plots.
5. **Finish.** Report success or partial failure, the local result path, and any
   diagnostic failure in 2–3 lines. Link the existing executed notebook and result
   file. Commit and push task-owned configuration or code as required by `AGENTS.md`.
   Once local results are verified, the quick-fit task is complete.

## Analysis and publication: only when requested

If the user asks for analysis, comparisons, new figures, or a wiki report, produce
only those requested outputs after retrieval. Follow `wiki/research/README.md` and
the relevant plotting or wiki skill for that work. An explicit request for a full
experiment record still includes the record. Do not infer that request from
“experiment”, “try”, or “run a fit”. Documentation must not delay result retrieval.

Local SSH errors stop before rental. Use an execution environment authorized to run
SSH; waiting for the GPU cannot fix a local user-ID error. The shared upload
includes HST cutouts and the emission-line table. A nonzero remote stage exit
saves its log, destroys the owned rental and stops. Diagnose the log before
repeating the command; do not rent a replacement for the same code or input error.
