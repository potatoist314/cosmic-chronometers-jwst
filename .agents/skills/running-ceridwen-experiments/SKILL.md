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

## Production defaults

The production defaults are `SETTINGS` and `PRIORS` in
`notebooks/ceridwen_integrated_photometry_spectra.ipynb`. An `experiment.json` that
omits a key runs with the notebook value. `python3 scripts/ceridwen_state.py` prints
each value with the records that tested it (skill `checking-ceridwen-state`).

Liu Hao, 2026-09-30, on the nebular grid with line marginalisation and the Ca II K,
Ca II H and Ca I mask: "this seems like a good default". On [O II], Hβ and [O III]:
"keep o unmasked as default is fine". On `diffuse_Ebump`: "for bump, keep prior (0, 6)".
On metallicity evolution: "the metallicity-evolution slope (ZH beta, the zevo arm of
wiki/research/experiments/e-dust-bump.md) should be part of the production default".
On this section: "make sure all the defaults are well saved in apporpriate skillsl, wiki etc".

The M1_210210 configs of 2026-09-29 and 2026-09-30 under `results/` set
`diffuse_Ebump` to `Uniform(low=0.0, high=12.0)`; their records state it. The notebook
default is `Uniform(low=0.0, high=6.0)`.

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
   Use the GPU type requested by the user. Offers must have reliability above
   99.5%, falling back to above 96% only if no offers pass all filters. Both
   bandwidth rates must be below $10/TB. The total $1 cap covers all arms and
   retries; `--spend-cap` can reduce it.
   The runner ranks offers by the latest row for each host in `scripts/vast_hosts.csv`:
   `good`, then no row, then `poor`. It rents a `poor` host only when no other offer
   passes the filters. In the same group, it rents the lowest cost per fit. It gets
   the cost per fit from the `calls/s` value of the host. A host without a `calls/s`
   value gets the median value for the GPU type, so among such hosts the lowest
   hourly price wins.

   Missing registered grids download locally before rental. The command uploads
   pinned source and checked grids, runs the full notebook with figure
   construction skipped on the box (CERIDWEN_PLOTS=0; figures render nothing
   under Agg), downloads each arm-target result, destroys its rental, and then
   rebuilds the standard figures locally while keeping the GPU-computed
   derived outputs.
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
5. **Record hosts.** List the hosts that started an instance:
   ```bash
   python3 -c "import json; [print(a['offer']['host_id'], a['offer']['gpu_name'], a['status'], a.get('error', '')) for a in json.load(open('results/<slug>/run/manifest.json'))['attempts'] if a.get('instance_id')]"
   ```
   Add one row for each host to the end of `scripts/vast_hosts.csv`, with the
   columns `host_id,outcome,gpu,date,run,reason`. The latest row sets the outcome.
   - Write `good` when the fit finished on the host.
   - Write `poor` when the host failed. Examples: the boot stalled, the instance
     became unavailable, or the host closed SSH.
   - Do not add a row for an offer that did not start an instance.
   - Do not add a row for a failure that our code or inputs caused.
   - Do not add a row when the records do not show the cause.
6. **Finish.** Report success or partial failure, the local result path, and any
   diagnostic failure in 2–3 lines. Link the existing executed notebook and result
   file. Commit and push task-owned configuration, code and new host rows as
   required by `AGENTS.md`.
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

### Standard figures for a result page

Liu Hao, 2026-09-29: "i just want my usual corner plots, sfh against time etc in
accordance with the standard wiki". Put these figures on the page, in this order.
Do not design a different figure.

| Order | Figure | Wiki file | Source |
| --- | --- | --- | --- |
| 1 | Spectrum fit: fitted LEGA-C pixels, posterior median, 16-84% band, pulls | `spectrum-<arm>-<target>.png` | `cell14_2.png` |
| 2 | Photometry fit: band fluxes, model medians, median continuum, pulls | `photometry-<arm>-<target>.png` | `cell14_1.png` |
| 3 | SFH of one fit: normalized SFR against lookback time, median, 16-84% band | `sfh-<arm>-<target>.png` | `cell20_7.png` |
| 4 | SFH of all arms on the same axes, and the mass fraction younger | `sfh-<target>.png` | `analysis.ipynb` |
| 5 | Corner of the physical parameters of one fit | `corner-<arm>-<target>.png` | `cell20_5.png` |
| 6 | Corner of all arms on the same axes, 1σ contours | `corner-<target>.png` | `analysis.ipynb` |

Show figures 1 and 2 for each arm before figure 3. Figures 4 and 6 are only for a
comparison of fits. The rules are in `wiki/AGENTS.md`, "Result reporting", and in
`AGENTS.md`, "Repository and reproducibility conventions". Read them.

The commands are from the M1_210210 KC13-bump page of 2026-09-29:
`wiki/notes/m1-210210-kcbump.md`, with figures in `wiki/analyses/m1-210210-kcbump/`.

1. **Get the figures of each fit.** The production notebook made them during the fit
   with `scripts/spectral_figures.py`. Do not run the fit again. This command writes
   each saved image of the executed notebook to `<dir>/cell<cell>_<count>.png`:
   ```bash
   ceridwen/.venv/bin/python - \
     results/<slug>/run/fits/<arm>/<object>-<target>/<target>_executed.ipynb <dir> <<'EOF'
   import base64, sys
   import nbformat
   nb = nbformat.read(sys.argv[1], as_version=4)
   k = 0
   for i, c in enumerate(nb.cells):
       for o in c.get("outputs", []):
           if "image/png" in o.get("data", {}):
               open(f"{sys.argv[2]}/cell{i:02d}_{k}.png", "wb").write(base64.b64decode(o["data"]["image/png"]))
               k += 1
   EOF
   ```
   Cell 14 is the notebook section "Output fit". Cell 20 is "Corners and SFH". Open
   each image before you copy it. A different notebook version can change the names.
2. **Make the comparison figures.** Copy `results/m1-210210-kcbump-2026-09-29/analysis.ipynb`
   to `results/<slug>/analysis.ipynb`. In code cell 1, set `RESULTS`, `TARGET`, `FIT_DIRS`,
   `COLOURS`, `NAMES` and `REF`. The baseline arm has the colour `#222222`. Then run:
   ```bash
   PYTHONPATH="$PWD/external/sedpy_jax" ceridwen/.venv/bin/python - <<'EOF'
   import nbformat
   from nbclient import NotebookClient
   p = "results/<slug>/analysis.ipynb"
   nb = nbformat.read(p, as_version=4)
   try:
       NotebookClient(nb, timeout=None, kernel_name="python3",
                      resources={"metadata": {"path": "results/<slug>"}}).execute()
   finally:
       nbformat.write(nb, p)
   EOF
   ```
   The notebook reads the saved results of each arm. It writes `sfh-<target>.png`,
   `corner-<target>.png` and `comparison.csv` to `results/<slug>/`.
3. **Copy the figures to the wiki.**
   ```bash
   D=wiki/analyses/<slug> && mkdir -p $D
   cp <dir>/cell14_2.png $D/spectrum-<arm>-<target>.png
   cp <dir>/cell14_1.png $D/photometry-<arm>-<target>.png
   cp <dir>/cell20_7.png $D/sfh-<arm>-<target>.png
   cp <dir>/cell20_5.png $D/corner-<arm>-<target>.png
   cp results/<slug>/sfh-<target>.png results/<slug>/corner-<target>.png $D/
   ```
   For an arm that has figures on a different wiki page, use those files.
4. **Check each figure at 900 px.** Run
   `sips --resampleWidth 900 <file> --out <dir>/<name>_900.png`. Then open the output.
5. **Write the page.** Use the `editing-the-wiki` skill. Use the structure of
   `wiki/notes/m1-210210-kcbump.md`.
6. **Put the page on the wiki Results page.** Liu Hao, 2026-09-29: "i don't see it in
   results. always put this stuff in results". Link the page from the research record
   of the experiment in `wiki/research/experiments/`. The example is
   `wiki/research/experiments/e-dust-bump.md`:
   ```yaml
   source_notes: m1-210210-kcbump
   result_groups: results/m1-210210-kcbump-2026-09-29
   ```
   `source_notes` is the slug of the note. `result_groups` is the result directory.
   For the other fields, read `wiki/research/README.md`. Then run:
   ```bash
   python3 wiki/build.py
   python3 wiki/tests/run_tests.py
   python3 -m unittest discover -s wiki/tests -p 'test_research.py'
   ```
   Commit and push the record. Then check the live Results page:
   ```bash
   ssh truenas 'curl -s http://127.0.0.1:8765/results/' < /dev/null | grep <record id>
   ```
   If there is no output, wait 10 seconds and do the check again. If there is no
   output after 60 seconds, the record is not on the page. Find the cause.

The executed notebook has more images. Add one only when the request names it.

| Image | Notebook section | Figure |
| --- | --- | --- |
| `cell04_0.png` | Data and target | HST ACS F814W cutout with the 3 arcsec aperture |
| `cell16_3.png` | Spectrum fit | Spectrum fit on all valid native pixels, excluded pixels in grey |
| `cell18_4.png` | Calibration polynomial | Calibration polynomial, median and 16-84% band |
| `cell20_6.png` | Corners and SFH | Corner of the dust parameters against the SFH mass fractions |
| `cell22_8.png` | Prior-to-posterior KL | KL divergence from prior to posterior for each parameter, in bits |

An old executed notebook can lack `cell20_6.png`. Make it from the saved posterior:
`ceridwen/.venv/bin/python scripts/add_dust_sfh_corner.py <result dir> --png <file>`.
