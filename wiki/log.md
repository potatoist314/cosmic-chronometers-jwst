# Wiki Log

## [2026-08-20] setup | Wiki initialized

- Pages: [[index]], [[overview]]
- Change: Added the Codex workflow and empty knowledge structure.

## [2026-08-20] codebase | Initial autonomous code map

- Pages: [[guides/reading-order]], [[codebase/project-map]], [[notebooks/notebook-map]]
- Change: Documented project modules, data flow, Ceridwen internals, and tests.

## [2026-08-21] format | Human wiki moved to HTML

- Pages: `index.html`, `overview.html`, `guides/`, `codebase/`, `notebooks/`
- Change: Replaced reader-facing Markdown with styled, linked HTML pages.

## [2026-08-21] codebase | Source-first reading examples

- Pages: all reader-facing guides, codebase pages, and the notebook map
- Change: Added 29 exact source excerpts with locators and reading explanations.

## [2026-08-24] codebase | Notebook workspace cleanup

- Pages: `notebooks/notebook-map.html`, `guides/reading-order.html`, `codebase/project-modules.html`
- Change: Removed retired notebooks from the live map and separated practice material.

## [2026-08-24] format | Minimal wiki style

- Pages: all reader pages, `assets/wiki.css`, `AGENTS.md`
- Change: Removed repeated prompts, exercises, decorative cards, and redundant navigation.

## [2026-08-24] codebase | Vast.ai GPU workflow

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.html`, `index.md`
- Change: Added cloud-GPU setup, data transfer, validation, and notebook execution.

## [2026-08-24] codebase | Ceridwen notebook names

- Pages: `notebooks/notebook-map.html`, `guides/reading-order.html`, `guides/vast-ai-gpu-workflow.html`
- Change: Retired notebooks 05-06 and removed numeric prefixes from active notebooks.

## [2026-08-24] codebase | Shared Ceridwen kernel

- Pages: `guides/vast-ai-gpu-workflow.html`
- Change: Documented shared CPU/GPU kernel resolution and bounded CPU trials.

## [2026-08-25] codebase | Ceridwen nested-sampling notebooks

- Pages: `notebooks/notebook-map.html`, `codebase/ceridwen-likelihood-sampling.html`, `index.md`
- Change: Replaced active notebook NUTS paths with weighted BlackJAX nested sampling.

## [2026-08-25] codebase | Vast.ai CUDA library isolation

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented JAX isolation from Vast's inherited system CUDA library path.

## [2026-08-25] codebase | Integrated-fit sampler settings

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Set the production joint fit to 300 live points, 25 deletions, and 40 inner steps.

## [2026-08-25] codebase | Modal GPU workflow

- Pages: `guides/modal-gpu-workflow.html`, `index.html`, `index.md`
- Change: Added persistent inputs, batch execution, and interactive Jupyter Sandbox controls.

## [2026-08-25] codebase | Modal GPU quick-run validation

- Pages: `guides/modal-gpu-workflow.html`, `index.md`
- Change: Fixed Modal Volume workspace paths, disabled JAX preallocation, and recorded the successful A100 quick batch.

## [2026-08-25] codebase | Ceridwen v0.2.2 workflow

- Pages: Ceridwen codebase pages, notebook map, Vast.ai guide, Modal guide
- Change: Documented the published schema-2.1 grid, pinned per-pixel resolution support, upstream sampler settings, checkpoints, and reloadable HDF5 results.

## [2026-08-25] format | STE rewrite

- Pages: all reader pages, `index.md`, `AGENTS.md`
- Change: Rewrote the wiki in controlled, plain English while preserving facts, qualifiers, code excerpts, and source locators.

## [2026-08-25] codebase | Modal v0.2.2 GPU validation

- Pages: `guides/modal-gpu-workflow.html`
- Change: Set an explicit remote project root and validated the published schema-2.1 grid in an A100 quick run.

## [2026-08-25] codebase | Vast A100 recommendation

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Replaced the RTX recommendation with an A100 40 GB and recorded the tested Croatia host.

## [2026-08-25] scope | Ceridwen primary focus

- Pages: `index.html`, `overview.html`, `guides/reading-order.html`, `guides/python-patterns.html`, `codebase/project-map.html`, `codebase/project-modules.html`, `codebase/data-pipeline.html`, `notebooks/notebook-map.html`, `index.md`, `AGENTS.md`
- Change: Made Ceridwen the primary workflow and marked earlier inference branches as inactive history.

## [2026-08-25] format | Native workflow diagrams

- Pages: all reader pages, `assets/wiki.css`, `index.md`, `AGENTS.md`
- Change: Replaced text diagrams and added responsive schematics for the Ceridwen learning path.

## [2026-08-25] format | Source-backed teaching blocks

- Pages: technical reader pages, `index.md`, `AGENTS.md`
- Change: Paired exact code excerpts with source documentation and plain explanations.

## [2026-08-25] codebase | Compact spectral likelihood modes

- Pages: `notebooks/notebook-map.html`, `codebase/data-pipeline.html`, `codebase/ceridwen-likelihood-sampling.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Documented compact full-spectrum and LEGA-C feature-band fits with Modal controls.

## [2026-08-25] codebase | Complete Ceridwen fit outputs

- Pages: `notebooks/notebook-map.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Documented detached Modal runs, persistent timing, posterior predictions, and star-formation histories.

## [2026-08-25] codebase | Detached Modal function calls

- Pages: `guides/modal-gpu-workflow.html`, `index.md`
- Change: Made batch notebook execution independent of local-entrypoint cancellation and recorded interrupted timing states.

## [2026-08-26] codebase | Feature-spectrum posterior report

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented HDF5 posterior tables, parameter marginals, corner plots, and derived mass-weighted age.

## [2026-08-26] query | Ceridwen A100 benchmark runs

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.html`, `index.md`
- Change: Converted the Vast.ai and Modal A100 timings into a readable comparison with workload and completion-status caveats.

## [2026-08-26] query | Concise A100 benchmark table

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Replaced the benchmark analysis with hardware and sampler figures for all retained runs.

## [2026-08-26] query | Omit unrecorded wiki metrics

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Removed unrecorded metrics and excluded JIT compilation from throughput figures.

## [2026-08-26] query | Matched V100 benchmark checkpoint

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.html`, `index.md`
- Change: Recorded matched A100–V100 throughput, JAX peak memory, and the bounded bottleneck inference.

## [2026-08-26] query | Hardware-first GPU benchmark table

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Combined GPU specifications and post-JIT throughput in one workload-labelled table.

## [2026-08-26] codebase | Public wiki deployment

- Pages: `.github/workflows/pages.yml`
- Change: Published reader-facing wiki files through GitHub Pages.

## [2026-08-26] codebase | Reproducible Vast GPU benchmark

- Pages: `guides/vast-ai-gpu-workflow.html`, `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Documented the fixed 5,000-call benchmark, fingerprints, outputs, and comparison command.

## [2026-08-26] query | V100 allocator memory verification

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Recorded two fresh-process JAX peaks, 100 ms NVML traces, and allocator-profile evidence.

## [2026-08-26] query | Concise GPU comparison

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Reduced the benchmark introduction to one matched hardware and throughput table.

## [2026-08-26] query | FP32 GPU comparison

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Added peak FP32 throughput and made it a required GPU comparison field.

## [2026-08-26] query | Relevant GPU compute paths

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Added FP32 and FP64 core counts, tensor paths, L2 cache, and dense hardware peaks.

## [2026-08-26] query | Benchmark schema fields

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Added the Ceridwen grid schema to each benchmark row and future benchmark rules.

## [2026-08-26] query | Concise memory benchmark

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Restored retained timings and reduced the V100 memory section without removing measurements.

## [2026-08-26] query | Plain memory terms

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Replaced tool labels with plain memory terms and defined each measurement source.

## [2026-08-26] codebase | Modal A100 kernel trace

- Pages: `guides/modal-gpu-workflow.html`, `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Documented the fixed post-JIT trace, saved XProf files, and reduction-dominated GPU timing.

## [2026-08-26] query | Matched Vast GPU benchmark

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Added matched RTX 3090, RTX 4090, and H100 speed, cost, and memory results.

## [2026-08-26] query | Merged GPU benchmark page

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.html`, `index.md`, `guides/modal-gpu-workflow.html`
- Change: Renamed the A100 benchmark page, grouped every GPU type into one hardware, run, and memory table, and added sourced RTX 3090, RTX 4090, and H100 specifications.

## [2026-08-26] query | Measurement-only GPU benchmark page

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `AGENTS.md`, `index.md`
- Change: Removed the GPU hardware section, added an FP32 peak column and a calls/s against FP32 peak chart, and reduced the memory and kernel-trace results to short notes.

## [2026-08-26] query | Precision charts on the GPU benchmark page

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `AGENTS.md`
- Change: Replaced the single chart with eight panels for CUDA FP32, CUDA FP64, and the tensor precisions, removed the speed-and-cost list, and reduced the source excerpt to the sampler settings.

## [2026-08-26] query | Grouped benchmark rows by GPU

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Grouped the measured-run rows by GPU model, fastest group first, and noted the new order.

## [2026-08-26] query | Predicted and measured Vast GPU rates

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added RTX 3060, RTX 3080 Ti, and RTX 4070 Super speed, cost, transfer-price, prediction, and memory results.

## [2026-08-26] query | Reader-facing benchmark results

- Pages: `AGENTS.md`, `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Removed prediction and workflow bookkeeping from the benchmark page and made measured reader-facing results the wiki rule.

## [2026-08-26] codebase | Four-GPU Vast fit launcher

- Pages: `guides/vast-ai-gpu-workflow.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented one independent joint Ceridwen fit per GPU, isolated outputs, and partial-checkpoint recovery.

## [2026-08-26] query | Log-log GPU benchmark charts

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Rebuilt the six speed panels on log axes with a none band, cased dot marks, and collision-free labels.

## [2026-08-26] query | GPU benchmark cost column

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Moved the cost column to one million calls and added marked price estimates for the Vast A100 and V100 runs.

## [2026-08-26] codebase | Four-GPU production sampler profile

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Recorded the 300-live-point BlackJAX NSS profile with 40 slice steps, 25 deletions, and `logZ_tol=-3`.

## [2026-08-27] codebase | Eight-GB Vast benchmark

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented on-demand JAX allocation, 8 GB benchmark support, and schema-v1 comparison compatibility.

## [2026-08-27] codebase | Joint posterior corner plots

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented aligned posterior rows and both stable corner-plot filenames.

## [2026-08-27] codebase | Compact Vast benchmark image

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Set the CUDA 12.6.3 base image as the default for current and future Vast benchmarks.

## [2026-08-27] query | Eight-GB allocator benchmark

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added matched RTX 3070 results for on-demand and 50% pooled JAX allocation.

## [2026-08-27] query | Blackwell RTX 50-series benchmarks

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added measured RTX 5060 Ti, RTX 5070, RTX 5070 Ti, and RTX 5080 speed, cost, and memory results.

## [2026-08-27] query | RTX 5090 complete-fit benchmark

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added the complete RTX 5090 fit rate, actual cost, sampler settings, and observed sampling memory.

## [2026-08-27] query | Additional Blackwell GPU benchmarks

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added B200, RTX 5060, and RTX PRO 4000, 4500, 5000, and 6000 speed, cost, and memory results.

## [2026-08-28] query | Ampere and Ada GPU sweep

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added seventeen measured runs, marked earlier comparison fingerprints, and retained all prior benchmark rows.

## [2026-08-28] query | RTX 5060 fast-basis convergence test

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added paired converged speeds and recorded the failed posterior and evidence equivalence gate.

## [2026-08-28] codebase | Separate paired-fit notebooks

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented independent executed baseline and fast-path reports with complete saved plots.

## [2026-08-28] codebase | Interactive active-codebase map

- Pages: `codebase/active-codebase-map.html`, `index.html`, `index.md`, `AGENTS.md`
- Change: Added a validated Archify map of the active Ceridwen project and allowed self-contained JavaScript for interactive diagrams.

## [2026-08-28] codebase | Benchmark artifact relocation

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Updated benchmark evidence paths after moving non-scientific runs out of `results/`.

## [2026-08-28] codebase | Readable result directory names

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Updated the RTX 5090 evidence path after shortening result directory names.

## [2026-08-28] codebase | Smoothed posterior density plots

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented the shared blue density style and HDF5-only result plot regeneration.

## [2026-08-28] codebase | Stellar-index likelihood mode

- Pages: `codebase/ceridwen-observations-model.html`, `codebase/data-pipeline.html`, `notebooks/notebook-map.html`, `guides/modal-gpu-workflow.html`, `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented the separate stellar-index observation, selectable integrated-fit likelihoods, outputs, and cloud controls.

## [2026-08-30] codebase | DR2 quiescent production run

- Pages: `guides/vast-ai-gpu-workflow.html`, `codebase/data-pipeline.html`, `codebase/ceridwen-ssp-csp.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented 187 unique targets, automatic SFH contraction, strict NSS settings, fitted spectrum scaling, embedded figures, two RTX 5060 shards, and local cap-aware result validation and cleanup.

## [2026-09-01] analysis | Ceridwen differential ages

- Pages: `overview.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented the Borghi-style binning, posterior bootstrap, unstable negative result, saved aggregate result, and cosmology-dependence boundary.

## [2026-09-01] analysis | Ceridwen chronometer audit

- Pages: `overview.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Added controlled Borghi cohorts, unbinned slopes, formation-time drift, selection sensitivity, influence, and fit diagnostics.

## [2026-09-01] codebase | Static smoothing collapsed into one convolution

- Pages: `codebase/ceridwen-observations-model.html`, `index.md`
- Change: Documented the quadrature-combined LOSVD and instrumental convolution, the baked interpolation indices and Fourier taper, the input-floored resampling grid, lazy `_H`, and the measured cost and width-accuracy comparison.

## [2026-09-01] codebase | Combined static smoother made the installed default

- Pages: `codebase/ceridwen-observations-model.html`
- Change: Recorded that the superproject pins the ceridwen commit with `_smoothing.py`, that `.gitmodules` points at the project copy of ceridwen, and that the bootstrap reinstalls ceridwen and checks the import.

## [2026-09-01] lint | Fixed-grid SFH basis accepted

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Removed the equivalence-gate caveat and the "keep the baseline basis" synthesis. Seed-to-seed scatter of the baseline exceeds the gate thresholds, so the fixed-grid basis is accepted as the default. Removed the gate script and the variation-notebook builder.

## [2026-09-01] analysis | Likelihood kernel A/B and per-GPU concurrency

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `codebase/ceridwen-likelihood-sampling.html`
- Change: Recorded the same-boot RTX 5060 Ti comparison (kernel-count reductions verified bit-identical but GPU-neutral; banded smoother rejected), the 66 percent boot-to-boot variance caveat, linear scaling to three concurrent fits per GPU, and the NumPy sedpy filter construction cutting per-fit setup to about 27 s.

## [2026-09-01] codebase | Speed-up defaults for every run

- Pages: `guides/vast-ai-gpu-workflow.html`, `guides/modal-gpu-workflow.html`, `codebase/ceridwen-observations-model.html`, `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Recorded the sedpy_jax fork as the `external/sedpy_jax` submodule that the bootstrap and Modal image install from the tree, the `fits_per_gpu` manifest field, and the same-boot RTX 4060 Ti measurement in which three concurrent production fits gave no aggregate gain over one, so the shard runner keeps one fit per GPU by default.

## [2026-09-02] analysis | N=2 concurrency and JAX allocator levels on 8 GB

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/vast-ai-gpu-workflow.html`
- Change: Recorded the same-boot RTX 3070 measurement of one, two, and three concurrent production fits (0.96 to 0.97 of one fit in aggregate, default stays one fit per GPU), the 0.8 to 1.0 GiB JAX working set against the 75 percent preallocated pool, the 0.14 fraction and preallocation-off levels at full speed, the 0.10 fraction autotuning failure, and the one-iteration sampler shift that a smaller pool causes.

## [2026-09-02] analysis | Blackwell concurrency on 8, 12, and 16 GB

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Recorded the same-boot RTX 5060, RTX 5070, and RTX 5060 Ti 16 GB measurements of one, two, and three concurrent production fits (0.99 to 1.03 of one fit in aggregate, default stays one fit per GPU), the 1,005 MiB JAX working set per fit against the whole-GPU peaks, the identical 1,157,000-call M5_172669 fit across all Blackwell levels, and the single-fit cost per card.

## [2026-09-02] analysis | Absorption-line pixel mask (draft)

- Pages: `analyses/absorption-line-mask.html`, `index.md`
- Change: Opened a draft analysis of feature-only and continuum-down-weighted spectral likelihoods: the S/N-squared weight budget of the current joint likelihood for three DR2 targets, a Fisher forecast per parameter, the feature catalogue and modes added to ceridwen on branch `absorption-mask`, and the mock and real-target experiment design. Result sections are filled once the Vast runs finish.

## [2026-09-02] analysis | Absorption-line pixel mask: results

- Pages: `analyses/absorption-line-mask.html`
- Change: Filled the draft with the 45-fit grid (36 mocks with 0, 3 and 6 percent continuum tilts at two S/N scales; M5_172669, M9_232005 and M11_214430 in three pixel modes). Feature-only and continuum-down-weighted likelihoods carry the same tilt-induced bias as the full spectrum and are 1.1 to 1.6 times wider; on the real targets they move the posteriors by up to 22 sigma. Recommended default: off. Result figures under `analyses/absorption-mask/`. Page stays a draft pending Liu Hao's decision on the default, line list and window.

## [2026-09-03] analysis | DR2 quiescent sample figure set (layout B)

- Pages: `analyses/dr2-quiescent-sample.html`, `index.md`
- Change: Published the final 187-galaxy figure set in the chosen layout B (single age–redshift panel with Ceridwen−Borghi residual strip): headline, three formation-timescale plots, 1D distributions, and fit-quality panel, all rendered from `results/dr2-quiescent-summary.csv` into `analyses/dr2-quiescent-sample/` (PNG + PDF). Superseded embedded chronometer figures backed up under `analyses/_old/`.

## [2026-09-04] analysis | Ceridwen results board

- Pages: `analyses/ceridwen-results.html`, `index.html`, `index.md`
- Change: New single landing page for every Ceridwen analysis output (DR2 final set, Borghi comparison, summary CSV, absorption mask, calibration polynomial, GPU benchmarks, chronometer notebook) with inline figures, artifact links, a push-state/open-decision table, and a Results entry in the index route and sections.

## [2026-09-04] analysis | Results board repair: full audit, true push states

- Pages: `analyses/ceridwen-results.html`
- Change: Inlined the omitted dt-mass/dt-alpha, all four absorption-mask, and all five calibration plots; added a directory-level related-fit-runs section and a PDF/CSV/notebook/script artifact list; split the calibration row into pushed tilt-origin branch verdict (`85c1e4a`) vs untracked local dir; stated the board's own unpushed state. GitHub search confirms plain-HTML/no-framework dashboards are the common pattern, matching this wiki's existing shell.

## [2026-09-04] analysis | Hostable checkpoint animation

- Pages: `analyses/ceridwen-results.html`, `analyses/checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html`, `index.md`
- Change: Added the self-contained viewer inside the published wiki root, preserved its accepted scientific payload, and fitted its controls, legend, axes, and plots into portrait and landscape mobile viewports.

## [2026-09-04] analysis | Ceridwen common results board repair & Tailscale hosting

- Pages: `analyses/ceridwen-results.html`, `scripts/serve_wiki.py`, `tests/test_ceridwen_results_board.py`
- Change: Rebuilt the Ceridwen results board from the validated 79-item audit manifest; corrected calibration science (DR2 spectra are brighter than production photometry; corrected photometry eliminates M4 tilt; M5 retains dust-degeneracy tilt from 0.3-mag optical-NIR model mismatch); inlined all 19 PNG plots with accessible fallback text; linked all 79 deliverables (PDFs, CSVs, notebooks, scripts, directories); launched persistent loopback launchd service (`com.liuhao.astro-wiki`) on port 8765 exposed via Tailscale Serve over HTTPS tailnet URL (`https://liu-haos-macbook-pro.tail5c940d.ts.net/wiki/analyses/ceridwen-results.html`).

## [2026-09-04] format | Wiki rebuilt as a lab notebook

- Pages: `notes/*.md`, `build.py`, `tests/run_tests.py`, `public/`
- Change: Converted every HTML page to a Markdown note, added a stdlib
  generator with search and RSS, and added a per-note question box that resumes
  the worker session recorded on the note.

## [2026-09-05] analysis | Per-galaxy chi-squared and star-formation-timescale diagnostics

- Pages: `notes/per-galaxy-fit-diagnostics.md`, `notes/per-galaxy-diagnostics-gallery.md`, `analyses/per-galaxy-diagnostics/`, `index.md`
- Change: Added per-galaxy photometric chi-squared, spectral chi-squared and t10-t90 figures for all 187 DR2 fits (`scripts/per_galaxy_diagnostics.py`, executed `notebooks/ceridwen_per_galaxy_diagnostics.ipynb`), with the model parameter block generated from the model object, checks of the stored chi-squared against the sampler's masks and sigma, sample-wide flags, and the RTX 5060 verification run.


## [2026-09-05] analysis | Calibration polynomial in the DR2 pipeline

- Pages: `notes/calibration-polynomial-dr2.md`, `analyses/calibration-polynomial-dr2/`
- Change: Added the marginalised Chebyshev calibration polynomial to the
  Ceridwen spectrum likelihood and to the integrated notebook
  (`CERIDWEN_CALIBRATION_ORDER`, `CERIDWEN_PHOTOMETRY`), with the physical
  explanation, the six-galaxy before/after comparison on one RTX 5060, the
  tilted-mock check and the sibling-card χ² acceptance figures.

## [2026-09-06] format | Calibration and per-galaxy notes cut to figures

- Pages: `notes/calibration-polynomial-dr2.md`, `notes/per-galaxy-fit-diagnostics.md`,
  `notes/per-galaxy-diagnostics-gallery.md`, `_old/`, `scripts/per_galaxy_diagnostics.py`
- Change: Replaced the three prose notes with a `Model settings` block generated
  from the result files, the figures with one sentence under each, and a
  collapsed `Details` block for tables, run records and commands. The gallery
  now carries one labelled section per galaxy with its three figures in a fixed
  order. Originals kept in `_old/`.

## [2026-09-06] edit | Calibration note: acceptance test removed

- Pages: `notes/calibration-polynomial-dr2.md`, `analyses/calibration-polynomial-dr2/`
- Change: Dropped the spectral-χ² acceptance test and the sibling-card χ²
  figures after Liu Hao's decision that the photometry carries the continuum.
  The photometric χ² per galaxy is the continuum metric. `acceptance.csv` is
  now `before-after.csv`.

## [2026-09-06] codebase | Spectral interpolation

- Pages: `notes/ceridwen-observations-model.md`, `index.md`
- Change: Replaced the obsolete dense-interpolation description with the exact weighted-gather code and refreshed source locations.
- Evidence: `results/rtx-5060-observation-speedups/comparison.ipynb`; 11.26–11.48 times faster unsmoothed interpolation on RTX 5060, no useful joint-fit gain.

## [2026-09-06] analysis | Free redshift and velocity dispersion

- Pages: `notes/redshift-sigma-wiggle.md`, `analyses/redshift-sigma-wiggle/`, `index.md`
- Change: New note. Arm `zsig` frees zred (prior 100 km/s) and sigma_smooth
  (prior 20 percent of DR2 sigma, bounds 0.5 to 1.5) on top of poly3_total for
  four DR2 galaxies.
- Evidence: `results/redshift-sigma-wiggle/analysis.ipynb`. Delta v within
  20 km/s of z_cat on all four. sigma_smooth off DR2 by 2.9 to 3.9 sigma on
  two galaxies and pinned at the 1.5 sigma_cat bound on M5_173928. Physical
  parameters stable. Delta ln Z +4 to +73. Wall time 3 to 4 times poly3_total.

## [2026-09-06] edit | zsig arm removed

- Pages: `notes/redshift-sigma-wiggle.md`
- Change: The `zsig` arm is gone from `scripts/calibration_arms_vast.py`. Production
  keeps z and sigma_star fixed at the DR2 values. The four fits stay in
  `results/redshift-sigma-wiggle/` as a record.
- Evidence: sigma_smooth absorbs template mismatch, not kinematics. Delta v
  within 20 km/s moved no physical parameter by more than 1.3 sigma.

## [2026-09-06] cleanup | Obsolete Ceridwen benchmarks removed

- Removed the old benchmark runs and three performance comparison directories.
- Removed their active wiki tables, timing claims, and links.
- Retained scientific fits, raw data, and reusable benchmark code.

## [2026-09-06] codebase | Production calibration and NSS measurements

- Pages: `notes/ceridwen-likelihood-sampling.md`, `index.md`
- Change: Documented the calibration Gram reduction, synchronized NSS step
  timing, and logical likelihood counts including initialization and slice work.
- Evidence: `ceridwen/ceridwen/likelihood/calibration.py`,
  `ceridwen/ceridwen/sampler/nested.py`,
  `results/rtx-5060-production-speedup/comparison.ipynb`.

## [2026-09-06] analysis | Fit-accuracy knobs, stage 0 and stage 1 setup

- Pages: `notes/fit-accuracy-knobs.md`, `index.md`
- Change: Stage 0 diagnostics on the six poly3_total fits (chi2 map at fixed f_calib, prior rails, Lick and Borghi+22 residuals). Six env switches in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, seven stage-1 arms plus seed repeats in `scripts/calibration_arms_vast.py`, verdict rule recorded before the fits.

## [2026-09-06] decision | Continuity SFH prior is the production default

- Pages: `notes/fit-accuracy-knobs.md`
- Change: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` defaults `CERIDWEN_SFH_PRIOR` to `student` (StudentT 0, 0.3, df 2 on logsfr_ratios). `scripts/calibration_arms_vast.py` pins `uniform` on the `poly3_total` reference so the stored fits stay reproducible. Tests cover both.

## [2026-09-06] decision | Free dust index is the production default

- Pages: `notes/fit-accuracy-knobs.md`
- Change: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` defaults `CERIDWEN_FREE_DUST_INDEX` to `1`, so the Kriek and Conroy index is sampled with Uniform(-1.0, 0.4), Ceridwen's documented default. The fixed -0.7 was an undocumented LLM choice. `scripts/calibration_arms_vast.py` pins the fixed index on the `poly3_total` reference. Tests cover both.

## [2026-09-06] analysis | Fit-accuracy knobs, stage 1 results

- Pages: `notes/fit-accuracy-knobs.md`, `analyses/fit-accuracy-knobs/`
- Change: 43 RTX 5060 fits landed ($0.665, 3.99 GPU-hours). Seed floor from six repeats: age 1.20, log Z 0.49, [alpha/Fe] 0.96, tau_dust 0.32, log M 0.49 half-widths, with the seed-to-seed ln Z spread reaching 2.0. `dust_free` adopted: the Kriek and Conroy index refuses the fixed -0.7, photometric chi2 and ln Z improve in every galaxy. `no_irac` exposed a second solution branch on M5_173928 (age 4.50 to 3.01 Gyr, log Z -2.23 to -1.49) held apart by two IRAC bands. `floor20`, `mask_cn` and `emis_wide` rejected. `sfh_cont` costs 0.7-6.8 in ln Z and widens the age error bars three to six times on the galaxies whose uniform-prior ages were implausibly tight.
- Evidence: `results/fit-accuracy-knobs/analysis.ipynb`, `verdict.csv`, `before-after.csv`, `sfh-prior-compare.csv`, `arms.csv`.

## [2026-09-06] analysis | New defaults against the original production model

- Pages: `notes/fit-accuracy-knobs.md`, `analyses/fit-accuracy-knobs/`
- Change: 22 RTX 5060 fits (2026-09-06 22:17 to 2026-09-07 01:45 UTC, about $0.36 own cost; the runner's $1.63 counter double-counted a concurrent run). `new_default` (StudentT continuity prior plus free dust index) against `poly3_total`: tau_dust moves past the old seed floor in six of six galaxies, ln Z rises in five of six on identical data. The three galaxies whose index pins to -1.0 get older by 4 to 7 half-widths and lose dust; the three with an interior index keep their age and gain dust. New-model seed floor from four repeats: age 0.34, log Z 0.54, [alpha/Fe] 0.23, tau_dust 0.07, log M 0.29, index 0.15 half-widths, ln Z spread 3.1. `tau_cn` rejected, no effect. `dust_wide` rejected: three galaxies follow the wall to -2.0 with ln Z up 24 to 31, M4_108989 flips bimodal and its Borghi [Z/H] goes from -1.7 to +3.3 sigma. Lick and Borghi agreement unchanged. `mock_tilt4_new_default` aborted, the stored truth has no dust index. Recommendation: tight index prior or fixed value, decide after the DR2-wide refit.
- Evidence: `results/fit-accuracy-knobs/new-defaults.ipynb`, `new-defaults-headline.csv`, `seed-floors.csv`, `new-defaults-extra-arms.csv`, `dust-index.csv`, `lick-new-defaults.csv`, `borghi-new-defaults.csv`.

## [2026-09-07] analysis | DR2 quiescent refit with the new production defaults

- Pages: `notes/dr2-new-defaults.md`, `analyses/dr2-new-defaults/`
- Change: all 187 LEGA-C DR2 quiescent galaxies refit at `998b6e1` with no env overrides, same manifest and seeds as the first production run, written to `results/dr2-quiescent-new-defaults`. 187/187 pass diagnostics. Sample medians, new minus old: age +1.23 Gyr, log Z -0.17, [alpha/Fe] -0.056, tau_dust +0.17, log M +0.19; against the two runs' combined seed floors those are 13.5, 3.1, 0.8, 7.1 and 4.6 times the noise on a median of 187, so [alpha/Fe] is the only parameter that does not move. Median ln Z rises 254 and every galaxy prefers the new model against a 3.7 combined seed spread. The free dust index is bimodal: 99/187 rail at the -1.0 prior floor, a second group sits between 0.0 and 0.4, 66 medians lie above the old fixed -0.7, and the age shift does not track the index (railed 1.34 Gyr, rest 1.16 Gyr). Mean age offset from Borghi+22 over the 68 overlapping galaxies grows from +0.21 to +1.89 Gyr and the age-redshift relation stays flat in both runs. Two RTX 5060 Ti boxes, 12.5 hours, $4.05. Fixed the monitor's teardown: `vastai destroy` prompts and exits 0 when it aborts, so it reported destroying instances that kept running.
- Evidence: `results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb`, `results/dr2-quiescent-new-defaults-summary.csv`, `results/dr2-quiescent-new-defaults/dust_index_posteriors.csv`.

## [2026-09-07] change | Absorption-feature windows on the fit figure

- Pages: `notes/notebook-map.md`
- Change: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` marks nine major stellar absorption features (Ca K, Ca H, Hδ, G4300, Hγ, Fe4383, Hβ, Mg b, Fe5270) on both panels of the native-spectrum fit figure. Windows come from `ceridwen.observation.absorption_features.feature_windows` at the catalogue redshift: Lick bandpasses for bands, ±1000 km/s for line centres. Grey fill with dotted edges and rotated labels along the bottom of the flux panel. Test `test_notebook_marks_major_absorption_features` pins the helper and the feature list.

## [2026-09-07] analysis | Oldest-30% age-redshift cut on the DR2 refit

- Pages: `notes/dr2-new-defaults.md`, `analyses/dr2-new-defaults/`
- Change: `ceridwen_new_defaults_comparison.ipynb` gains a second age-redshift figure that keeps the oldest 30% of each σ-z bin (Ceridwen and Borghi+22 alike), beside the unchanged full-median figure. Both runs stay flat; the new defaults sit 1 to 2 Gyr above Borghi+22 under the same cut. High-σ bins hold 3 to 4 galaxies, so the cut there is one galaxy.
- Evidence: `results/dr2-quiescent-new-defaults/age_redshift_oldest30.csv`, `figures/headline-age-redshift-oldest30.png`.

## [2026-09-07] change | Absorption-feature labels on every spectral plot

- Pages: `notes/notebook-map.md`, `notes/per-galaxy-fit-diagnostics.md`, `notes/stacked-chi2-and-median-pull.md`
- Change: the fit-figure marking is now the production standard for every plot with a wavelength axis, in one shared module `scripts/spectral_figures.py`. Grey Lick/IDS windows with dotted edges on every wavelength panel; feature names in one horizontal row hanging below the bottom panel's x axis, outside the plotting area, dropping to the next row only where the rendered text would overlap. Rows are placed in points below the axis and the x-label pad is measured from them, so a short or narrow panel keeps the label clear of the names. Callers updated: the joint template notebook, `scripts/per_galaxy_diagnostics.py`, `scripts/plot_dr2_stacked_pull.py`, `notebooks/ceridwen_test_spectra.ipynb` and the five analysis notebooks in `results/`. Photometric SED panels in observed μm and non-wavelength plots (corner, SFH, histograms) stay bare.
- Evidence: `tests/test_spectral_figures.py` (13 tests), `wiki/analyses/dr2-quiescent-sample/stacked-pull.png`, `wiki/analyses/per-galaxy-diagnostics/M1_210210-spectral_chi2.png`.

## [2026-09-07] analysis | Quiescent sample on the star-forming sequence

- Pages: `notes/sfms-quiescent.md`, `analyses/sfms-quiescent/`
- Change: 2x2 log SFR100 against log formed mass for the old and new runs against Whitaker+14 and Leja+22 at z = 0.73, with the +-0.3 dex band and the +0.6 starburst and -1.0 quiescent lines. SFR100 averages the youngest 100 Myr per posterior draw; new columns `sfr100_q16/q50/q84` in both summary CSVs. Median offsets: old -1.65/-1.49 dex, new -1.06/-0.89 dex (Whitaker/Leja); q50 below the quiescent line: old 82%/76%, new 54%/42%.
- Evidence: `scripts/plot_sfms_quiescent.py`, `scripts/build_dr2_quiescent_summary.py:sfr100_draws`, `tests/test_sfr100.py`, `wiki/analyses/sfms-quiescent/sfms-quiescent.png`.

## [2026-09-07] change | Dust against young-SFH corner in the joint notebook

- Pages: `notes/notebook-map.md`
- Change: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` gains a third corner plot showing the dust parameters against the three youngest formed-mass fractions (0-0.03, 0.03-0.1, 0.1-0.3 Gyr) with per-pair Spearman rank correlations, reusing the existing corner style and quick-profile ranges. The dust index joins the plot only when `FREE_DUST_INDEX` is set. Verified by executing the new block against real draws from both DR2 runs.

## [2026-09-09] change | Galaxy image and photometric aperture in the joint notebook

- Pages: `notes/notebook-map.md`, `notes/data-pipeline.md`
- Change: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` gains one early cell that draws the HST ACS F814W cutout of the target with an asinh stretch, arcsecond offset axes, north up and east left, and a 1.5-arcsecond-radius circle for the COSMOS2015 3-arcsecond aperture. `scripts/download_hst_cutouts.py` fetched all 187 cutouts from the IRSA `acs_mosaic_2.0` table into `data/raw/hst_f814w/`, with no misses. `scripts/backfill_hst_cutout_cell.py` inserted the cell and its output into the 187 executed notebooks under `results/dr2-quiescent-new-defaults/` without repeating a fit.
- Evidence: `reports/astro-hst-cutouts-2026-09-09.md`, `tests/test_ceridwen_dr2_production.py` (20 tests). The drawn radius measures 1.49993 to 1.49998 arcseconds through the WCS on three galaxies, and `_validate_result()` passes on the same three.

## [2026-09-10] change | Stacked pull: true rebinning, five recipes, per-feature figure

- Pages: `notes/stacked-chi2-and-median-pull.md`
- Change: `scripts/plot_dr2_stacked_pull.py` no longer interpolates onto the rest-frame grid and no longer multiplies sigma by `sqrt(dlambda_new / dlambda_native)`. That step claimed a noise average that interpolation never performs, so mean pull² sat near 0.16 and the null line at 1 carried no meaning. Every fitted native pixel now goes into the bin that contains it. Mean pull² per native pixel is 1.149 on `results/dr2-quiescent-new-defaults` (187 galaxies) against a per-galaxy reduced χ² of 1.086. The script gained five stacking recipes (mean, median, inverse-variance weighted, sigma-clipped mean, biweight location from Beers, Flynn & Gebhardt 1990), a bootstrap over galaxies for the 1σ width, and a per-feature figure comparing each absorption window with the continuum between the windows. Absorption windows are marked on every rest-frame panel.
- Evidence: `reports/astro-stacked-pull-2026-09-10/` (three figures and `run.log`), `tests/test_stacked_pull.py` (17 tests, all pass). The regression test fixes mean pull² against bin width, which the old scaling failed. Every feature window sits 5σ to 16σ from zero and far from the continuum level of −0.022. The Hβ window holds no fitted pixel because the fits mask rest-frame Hβ and [O III].

## [2026-09-10] change | Theme hub, archive folder, scripts index

- Pages: [[themes]], [[index]], all 30 themed notes
- Change: Notes gained `theme:` frontmatter; `wiki/themes.md` board added; front page became the theme hub; date feed moved to `log/`; inactive scripts/notebooks/results moved into `archive/`; `scripts/README.md` added.

## [2026-09-11] change | Theme board grouped by experiment

- Pages: [[themes]]
- Change: Grouped board rows under experiment headings linked once to their note; removed note and experiment columns; added change column; rewrote results in plain words; stacked layout on narrow screens.

## [2026-09-12] change | Prospective research notebook

- Pages: Research overview, Questions, Experiments, Reference and Earlier work.
- Change: Added stable question/experiment records, verbatim user messages, separate
  agent execution plans and measured results, linked runs, status filtering and search.
- Workflow: Chat remains the writing surface. User amendments, interpretation and
  decisions retain their original wording. Reviewed status requires a recorded user
  interpretation. New research is exempt from the legacy 50-word body cap.
- Preservation: All 31 existing notes and earlier board routes remain accessible;
  historical reasoning and saved results were not reconstructed or migrated.
- Evidence: `research/README.md`, `research.py`, `tests/test_research.py` and
  `tests/run_tests.py`; isolated browser checks covered filtering, search, run
  metadata and links, dark desktop rendering and 360-pixel mobile light rendering.


## 2026-09-12 · codebase · Existing research integration and light editing

- Integrated 28 experiments under five research questions, including all analysis
  notes, current result groups and archived Ceridwen campaigns.
- Added existing-record provenance, Recorded status, cross-question links and
  source-note backlinks. Historical evidence does not require invented briefs.
- Allowed light display edits while retaining original messages. Updated agent
  instructions and templates to preserve meaning, uncertainty and attribution.
- Kept saved results in place. Recorded seed-floor units and the full-sample
  calibration/photometry mismatch as caveats beside the affected results.
- Evidence: `research/`, `research.py`, `tests/test_research.py` and source links
  in each record. Raw notebooks, fits and source notes remain unchanged.
- Validation: both wiki test suites passed; 70 local routes and the private site
  returned HTTP 200. All 546 linked run notebooks have outputs and no error cells.
  Browser checks covered original wording, Recorded filtering, search, expanded
  run records and layouts at 360, 736 and 1024 pixels without horizontal overflow.


## 2026-09-12 · codebase · Supervisor-style result reporting

- Made figure-first reporting the governing rule in wiki and root instructions.
- Replaced default experiment summaries with inline fits, diagnostic figures and
  short captions. Retained full records at each experiment's `record/` subpage.
- Added target and view selectors, reference-arm comparisons and deferred image
  loading. All 28 experiments have figures or a measured benchmark table.
- Figure references identify the saved notebook cell/output or existing image.
  Extracted images are generated assets; original notebooks and plots are unchanged.
- Validation: target/arm mismatches and missing figures stop publication. Tests
  verify exact image extraction, preserved reasoning and absence of agent summary
  sections from the visual result page.
- Validation completed: both wiki test suites passed; 58 result/record routes
  and the private site returned HTTP 200. All 2,693 image assets resolve. Browser
  checks covered desktop and 360-pixel layouts, loaded images and target retention
  across Fits, SFH, Posteriors and Comparison views, without horizontal overflow.


## 2026-09-12 · codebase · Absorption-feature colours and side legend

- Replaced grey windows and below-axis names with fixed feature colours and one
  right-side legend. Shared layout reserves a separate column for the legend.
- Updated active notebook templates, diagnostic and stacked-residual plotting.
- Re-rendered affected saved figures from existing results; no fits were rerun.
- Recorded the default in root and wiki instructions and the notebook map.
- Refreshed 189 spectral diagnostics, the example notebook image and wiki copy,
  and both stacked wavelength figures (PNG/PDF). All 189 diagnostics reproduce
  their recorded likelihood and chi-squared values to absolute tolerance 1e-6.
- Validation: plotting/production/diagnostics/stacking tests and both wiki suites
  passed. Existing numerical inputs and unrelated notebook outputs are unchanged.


## 2026-09-12 · codebase · Spectra behind the stacked-pull spikes

- Added M11_216899 and M12_184916 spectrum-and-pull images directly below the
  stack on the result page and its linked source note.
- Images are unchanged PNG outputs from the revised-run notebooks, cell 26,
  output 0; notebook links remain available beside the source figures and in
  the research record.
- Captions identify the 3672 Å and 5566 Å bins and each galaxy's contribution.
  Existing plots and numerical results are unchanged; no fits were rerun.


## 2026-09-12 · query · Approved quiescent mock truth

- Added `research/experiments/e-quiescent-mock.md` under mock recovery, with
  status planned and the six approved intrinsic parameter values.
- Preserved the original user messages and approval, the plain-English physical
  explanation, and the Bevacqua/Nersesian references.
- Recorded the planned 1%, 5%, and 10% noise cases. Observing parameters and the
  noise prescription remain undecided; no fits were run.
- Validation: both wiki suites passed. The rendered record, approved values,
  original approval and navigation links were checked; the private route returns 200.

## [2026-09-14] ingest | JWST handwritten masking notes

- Pages: `notes/jwst-image-masking.md`, `index.md`.
- Change: Added a readable masking workflow, observing context and page-by-page transcription of `masking/masking.pdf`.
- Preserved colour annotations, ambiguous shorthand and the original PDF link. No image masking or scientific experiment was performed.

## [2026-09-14] query | Separate masking category

- Added a Masking sidebar category and `/wiki/masking/` listing.
- Moved the JWST note out of Reference into Masking, retaining its existing URL and content.

## [2026-09-15] ingest | MJ Park and Sandro meeting and research roadmap

- Added the corrected meeting notes, the original reviewed transcription and an unchanged copy of the eight-page handwritten PDF.
- Added `/wiki/roadmap/`, a Research sidebar link and current priorities on the overview, all rendered from the Roadmap in `research/direction.md`.
- Recorded the approved 10, 9, 8, 7, 6, 5, 3, 3 priorities, the metallicity dependency and the unscored remaining tasks.
- Retained dated clarifications and the standing 1–10 convention in the root and wiki instructions and research README.
- Validation: the wiki audit and 31 research tests passed; 33 notes built. Scores, dependencies, link anchors and the PDF were checked locally and through the private wiki URL; desktop and 360-pixel layouts were reviewed.

## [2026-09-15] ingest | Quiescent-galaxy parameter literature

- Added 8 PDFs under `papers/quiescent populations`, its README, 8 rows in `papers/README.md`, and `wiki/notes/papers-quiescent-parameters.md`.
- The note tabulates mass, age, metallicity and [α/Fe] references from nine papers, LEGA-C quiescent galaxies, z~0 anchors and the 187-galaxy Ceridwen DR2 medians.
- The comparison lists numbers only and links the metallicity roadmap item.

## [2026-09-15] query | Six-section navigation and faithful meeting notes

- Replaced the grouped sidebar with Home, Results, Meetings, Papers, Masking and Code & guides; removed the personal/DR2 byline.
- Home renders the full priority list and planned/running work, with original direction, questions and amendments collapsed below. The Roadmap URL remains an alias with its task and amendment anchors.
- Results links all saved reports and retains other experiment records and earlier analyses/boards. Code & guides retains earlier documentation and note history.
- Papers links the catalogued local PDFs and includes them in search. Older catalog paths resolve by their unique filename after the chronometer folder move.
- Removed agent commentary from the Park/Sandro meeting notes. Retained the handwriting, user clarifications, uncertainty markers and previous anchors; direct links open collapsed records.
- Saved the transcription-only rule in root and wiki AGENTS.md and the research README: light rephrasing and complete sentences are allowed; added commentary is not.
- Validation: 32 research tests and the wiki audit passed; 34 notes built. All 34 notes, 29 experiments and 22 PDF links were checked, with all six sections served locally and on the private wiki. Desktop and 360-pixel layouts, search and original-clarification links were reviewed. The audit/build used the installed Command Line Tools via DEVELOPER_DIR after the default Xcode shim required licence acceptance.

## [2026-09-15] query | No commentary across the wiki

- Extended the standing no-commentary rule to every page, including research records, papers, masking, code and earlier analyses.
- Removed agent-role labels, source-summary framing, editorial recommendations and generic verdicts. Retained factual explanations, comparison conditions and concrete limitations.
- Preserved note images, research figure references, run metadata and original user messages. Kept old section anchors.
- Removed the DR2 comparison's unsupported seed-significance commentary and corrected its settings description to match the existing research record.
- Validation: 32 research tests and the wiki audit passed; 34 notes built. Checked 120 HTML pages and 11 local/private-site routes. Note images, code excerpts, figure/run arrays, original messages and previous anchors were retained.

## [2026-09-15] revise | Literature route and commentary lint

- Pages: [[papers-quiescent-parameters]] (section Literature, own page `/wiki/literature/`, four tables expanded, linked from Home and Papers); `wiki/tests/run_tests.py`, `wiki/tests/test_research.py`.
- Change: `wiki/build.py` `commentary_faults()` stops the build on agent-commentary labels: Why it matters, Documented contract, Project synthesis, verdict lines, Decisions for Liu Hao.

## [2026-09-15] revise | Literature page by parameter with figure

- Pages: [[papers-quiescent-parameters]]; `scripts/plot_literature_values.py`, `wiki/analyses/papers-quiescent-parameters/literature-vs-ceridwen.{png,pdf}`.
- Change: Reordered `wiki/notes/papers-quiescent-parameters.md`: comparison table, one table per parameter (mass, velocity dispersion, age, metallicity, alpha), other redshifts, sample definition. Added a figure from `scripts/plot_literature_values.py`.

## [2026-09-15] codebase | Priority history and handwriting

- Pages: Home, priority details, research questions and result figures.
- Change: Added explicit resolve/reopen controls, immutable activity history, Apple Pencil writing sheets, figure backgrounds and recoverable local drafts.

## [2026-09-15] codebase | Current default priors

- Pages: `notes/default-fit-parameters.md`, Code & guides, `index.md`.
- Change: Expanded the current notebook's 14 sampled values, priors and physical meanings above the code links, followed by fixed settings and three marginalised calibration coefficients. The canonical note supplies both views; rows stack on narrow screens.
- Sources: Current joint-fit notebook configuration and priors, grid axes and metadata, SFH transform, attenuation, noise and calibration implementations. Fitting defaults unchanged.
- Validation: Wiki audit and 35-note build passed; 33 of 34 research tests passed, including both new tests. The unchanged corpus check reports the unrelated `results/calibration-order` directory missing from `result_groups`. Page and all eight source/reference links returned HTTP 200; private site served the update. Safari layouts checked at 360, 736 and 1024 CSS pixels.

## [2026-09-15] code | Partial erasing and continuous notes

- Change: Added visible Pen/Eraser controls, partial ink erasing, finger scrolling, automatic blank sheets and bounded canvas rendering. Saved records retain ordered ink/eraser paths, figure backgrounds and interior blank sheets.
- Files: `assets/activity.js`, `assets/activity.css`, `activity.py`, `tests/test_activity.py`, `research/README.md`, `index.md`.
- Validation: All 12 activity tests, the wiki audit and the 35-note build passed. Safari checks covered partial erasing, Undo/Redo, figure preservation, sheet boundaries, draft recovery, compact layout and the 30-sheet limit. The research suite passed 33 of 34 tests; its corpus check reports the unrelated `results/calibration-speedup` directory missing from `result_groups`.

## [2026-09-15] code | Scribble erasing and handwriting latency

- Change: Cached finished ink, limited drawing to affected sheets once per display frame, removed repeated canvas resets and deep undo copies, and deferred draft writes until pauses between strokes. Height-only layout changes preserve the active stroke. Removed Pen/Eraser controls. Repeated scribbles over ink erase their covered area; original gesture points remain in saved revisions.
- Validation: Runtime tests cover 128 samples with 500 finished strokes, eraser rendering, cross-sheet input, immutable undo snapshots and scribble recognition over existing ink. Saved browser previews preserve ink, erased areas and figure pixels.
- Validation status: All 13 activity tests and eight ink runtime tests pass. Publication is blocked by stale research paths after the concurrent archive move; iPad gesture and latency verification remain pending.

## [2026-09-15] codebase | Rendered scientific notation

- Change: Added locally served KaTeX and fonts to the shared page shell; converted scientific notation in maintained notes, tables, captions and research displays. Saved the standing rule in `AGENTS.md`.
- Preservation: Original wording and source excerpts stay literal; figure files, parameter values and definitions were not changed by this notation update. Previous heading links remain available.
- Validation: Eight math tests passed, including compilation of authored expressions with the vendored renderer. Browser checks covered 360, 736 and 1024 CSS pixels, light/dark themes, print and inserted captions. The complete unit run passed 53 of 54 tests; the remaining corpus check reports the unrelated `results/calibration-speedup` directory missing from `result_groups`.
- Build: An initial 35-note build passed. The later audit and rebuild were blocked when a concurrent archive move removed paths under `results/rtx-5060-dr2-quiescent-full-spectrum`; the saved public site was retained.
- Completion: After the archive references were updated, the full wiki audit and 35-note build passed. All 137 shared pages include math support; seven private-site routes and assets returned HTTP 200. The final unit run passed 54 of 55 tests, with only the same unrelated calibration-speedup corpus failure.

## [2026-09-15] change | Archived the no-polynomial DR2 run

- Change: Archived the DR2 run without a calibration polynomial, superseded by results/dr2-quiescent-new-defaults.
- Files: Moved results/rtx-5060-dr2-quiescent-full-spectrum/ and results/dr2-quiescent-summary.csv to archive/results/dr2-quiescent-no-polynomial/ with a README; repointed scripts, tests, notebooks, wiki notes and research-record evidence paths to the new run or archive; regenerated DR2 sample figures from the new run and updated numbers in notes/dr2-quiescent-sample.md.
- Validation: Figures checked at 900 px; wiki build and tests pass; 36 pytest cases pass.

## [2026-09-15] revise | [Fe/H] as the displayed metallicity

- Pages: [[dr2-quiescent-sample]], [[dr2-new-defaults]], [[absorption-line-mask]], [[fit-accuracy-knobs]], [[redshift-sigma-wiggle]], [[calibration-polynomial-dr2]], [[papers-quiescent-parameters]]
- Change: Every figure, table and summary CSV now shows [Fe/H] = grid Z + 1.7328283 instead of log Z. The 545 executed per-target notebooks had their corner figures redrawn from saved posteriors and their summary rows relabelled without re-running any fit (`scripts/relabel_feh_notebooks.py`). Analysis notebooks were re-executed from saved outputs; shifts and half-widths are unchanged.

## [2026-09-15] result | Calibration polynomial order 3, 5, 10

- Pages: [[calibration-order]], [[calibration-polynomial-dr2]], [[themes]]
- Change: New note and executed analysis for Chebyshev order 3, 5 and 10 on the six reference galaxies. The stored order-3 baseline used the old \(\tau_{\mathrm{dust}}\) prior, so the order-3 arm was rerun with the current prior on the same Vast boot as the other arms. Experiment record `e-calibration-order` at results-ready with 18 complete runs.
- Files: results/calibration-order/, wiki/analyses/calibration-order/, wiki/notes/calibration-order.md, wiki/research/experiments/e-calibration-order.md.
- Validation: all 18 result files carry the same dust prior bounds; figures checked at 900 px; wiki build and tests pass.

## [2026-09-15] change | Calibration polynomial speed-up

- Pages: [[calibration-speedup]], [[ceridwen-likelihood-sampling]], [[themes]]
- Change: `PolynomialCalibration` forms the Gram matrix from Chebyshev moments and takes the coefficients and log-determinant from one Cholesky factor (ceridwen 56505a6); same likelihood value, linear instead of quadratic cost in the order. New note with the same-boot RTX 5060 timing and the order-10 refit of M12_98104.
- Files: ceridwen/ceridwen/likelihood/calibration.py, ceridwen/tests/test_polynomial_calibration.py, scripts/benchmark_calibration_order.py, results/calibration-speedup/, wiki/analyses/calibration-speedup/, wiki/research/experiments/e-calibration-speedup.md.
- Validation: Gram and calibrate tests at orders 1 to 24; summed log-likelihoods identical old vs new; figures checked at 900 px; wiki build and tests pass.


## [2026-09-15] fix | Wiki server accepts a whole page load at once

- Pages: every served page; `scripts/serve_wiki.py`
- Change: `WikiServer` sets the listen backlog to 128 (Python's default is 5). Safari opens one HTTP/1.0 connection per script, stylesheet and font, plus a speculative preconnect for every subresource it remembers, before the HTML arrives; the kernel reset the overflow, a reset `<script defer>` failed silently and the page showed raw TeX.
- Validation: 20 and 60 simultaneous connections to port 8765 all served (13–15 of 20 were reset before); fresh Safari windows on `/wiki/code/`, `/wiki/literature/`, `/wiki/n/default-fit-parameters/` and the Tailscale URL fetched all four scripts and the KaTeX fonts and rendered headings, prose, tables and captions; 420 px layout and dark mode checked; `wiki/tests/test_math.py` passes.

## [2026-09-17] lint | Every modelling decision on the literature page

- Pages: [[papers-quiescent-parameters]], [[default-fit-parameters]], index.md, AGENTS.md
- Change: The literature page now lists every prior, sample cut, preprocessing step, model and calibration setting, sampler setting and derived-quantity definition from the production notebook, one table per stage, with a short Decided column filled only from recorded decisions and each citation once in a collapsed References block. The per-paper tables are merged into the physical-parameters table. `notes/default-fit-parameters.md` is obsolete and superseded by it. A `figures/` path on a note with a `source:` field now resolves to the site figure folder; the note page had shown a broken figure since 2026-09-10.
- Files: wiki/build.py, wiki/tests/test_research.py.
- Validation: every value re-read from notebook cells 2 to 30, the executed poly5 notebook's selection counts and the DR2 summary CSV; wiki build passes; the two test suites pass apart from two failures that predate this change (bridge question box, calibration analyses unlinked); note page, literature landing and code landing checked in Safari with KaTeX font fetches in the server log; 400 px layout checked.

## [2026-09-17] add | Student group meeting and Jonah Powley meeting notes

- Pages: [[meeting-2026-09-17-student-group]], [[meeting-2026-09-17-jonah-powley]], index.md
- Change: Two meeting notes from one nine-page handwritten PDF: the Thursday student group meeting (pages 1–3) and the meeting with Jonah Powley on Prospector fits of quiescent galaxies (pages 4–9). Each page has the cleaned notes, the original page-by-page transcription and a link to the unchanged PDF under reports/. The split between the two meetings at page 4 is a reading of the notes, not marked in them.
- Files: reports/meeting-2026-09-17-student-group-jonah-powley.pdf.
- Validation: wiki build passes (39 notes); the two test suites pass apart from the two failures that predate this change (bridge question box, calibration analyses unlinked); both note pages and the Meetings landing checked in Safari with KaTeX font fetches in the server log; the PDF link answers 200.

## [2026-09-17] add | Jonah Powley's Prospector priors on the literature page

- Pages: [[papers-quiescent-parameters]], [[meeting-2026-09-17-jonah-powley]], index.md, AGENTS.md
- Change: A reference table above the stage tables lists Jonah Powley's Prospector dust attenuation, dust emission and AGN torus priors beside the Ceridwen production settings, with his original code in a collapsed block. The meeting note links to it and records that \(f_{\mathrm{AGN}}\) and \(\tau_{\mathrm{AGN}}\) are sampled uniformly in \(\log_{10}\). No rows list SFH, mass, metallicity or redshift priors, which are absent from the excerpt.
- Files: wiki/tests/test_research.py (literature landing table count 7 to 8).
- Validation: wiki build passes (39 notes); the two test suites pass apart from the two failures that predate this change; every prior re-read against the pasted code; note page, Literature landing and the meeting-note link checked in Safari with KaTeX font fetches in the server log.

## [2026-09-17] change | Wiki also served from the TrueNAS server

- Pages: AGENTS.md
- Change: The built wiki is mirrored to the TrueNAS server and served on the tailnet at `https://truenas-scale.tail5c940d.ts.net:8765/wiki/`, so it stays reachable when the Mac is off. `scripts/publish_wiki.py` copies `wiki/public/` and every project file linked through `/wiki/f/`. The launchd agent `com.liuhao.astro-wiki-publish` runs it after each build and every 30 minutes; it copies nothing if nothing has changed. An nginx container on the NAS serves the pages and files. It forwards requests for `/wiki/ask`, `/wiki/api/` and files it does not hold to the Mac's server, so the question box and activity saves require the Mac to be awake. The Mac service on port 8765 and its URL are unchanged.
- Files: scripts/publish_wiki.py, scripts/truenas-wiki/nginx.conf, scripts/truenas-wiki/docker-compose.yml.
- Validation: wiki build passes (40 notes); the two test suites pass apart from the two failures that predate this change (bridge question box, calibration analyses unlinked); Home, a note with maths and a priority page with its activity panel checked in Safari through the NAS URL, with KaTeX font fetches in the NAS nginx log; 1986 linked paths mirrored and an rsync dry run finds nothing left to copy; linked `.h5`, `.ipynb`, `.csv` and `.png` files and the 13.9 MB meeting PDF served from the NAS disk; `/wiki/api/publication` answers through the NAS; a POST with a foreign Origin gets 403 at the NAS; the NAS LAN address refuses connections on port 8765; a rebuild started a publication 34 s after the build ended; a run with nothing new takes 0.35 s.

## [2026-09-17] revise | Calibration polynomial order 10 as the default

- Pages: [[calibration-order]], [[model]], research record `e-calibration-order`, question `q-fitting-choices`
- Change: Production notebook default `CERIDWEN_CALIBRATION_ORDER` changed from 3 to 10 on Liu Hao’s decision; calibration-order note gained a table of \([\mathrm{Fe}/\mathrm{H}]\), \([\alpha/\mathrm{Fe}]\), and age by order; decision recorded in the `e-calibration-order` research record.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, tests/test_ceridwen_dr2_production.py.

## [2026-09-17] change | Model page: every assumption and setting on one page

- Pages: `/wiki/model/`, `/wiki/literature/`, [[notes/model]], [[notes/papers-quiescent-parameters]], [[notes/default-fit-parameters]], [[notes/meeting-2026-09-17-jonah-powley]], [[research/model-page-spec]], [[index]].
- Change: Liu Hao asked for one page showing every assumption and setting at a glance. The Literature page became Model. The navigation entry is Model. The new route is `/wiki/model/`. `/wiki/literature/` still serves the same page. Renamed `notes/papers-quiescent-parameters.md` to `notes/model.md`. Left an obsolete stub at the old slug. The figure directory is `wiki/analyses/model/`. Four groups contain rows with a value, short reason, inherited tag and `!` flag. Bullets open on click and link to experiment records. Four flags appear at build time: tau_dust prior, dust slope prior, [alpha/Fe] prior and f_calib prior. Moved literature values, Jonah Powley's Prospector table and references to a Literature section below. Added the upkeep rule to `AGENTS.md` and the spec to `research/model-page-spec.md`.
- Files: `wiki/notes/model.md`, `wiki/notes/papers-quiescent-parameters.md`, `wiki/notes/default-fit-parameters.md`, `wiki/notes/meeting-2026-09-17-jonah-powley.md`, `wiki/research/model-page-spec.md`, `wiki/research.py`, `wiki/build.py`, `wiki/tests/run_tests.py`, `wiki/tests/test_research.py`, `scripts/plot_literature_values.py`, `wiki/AGENTS.md`, `wiki/index.md`.
- Validation: The wiki build passes with 40 notes. Both test suites pass apart from two failures that predate this change: bridge question box and calibration analyses unlinked. `/wiki/model/`, `/wiki/literature/`, `/wiki/n/model/`, `/wiki/n/papers-quiescent-parameters/` and `/wiki/n/default-fit-parameters/` return 200. Checked the page at 1280 px and 400 px with all rows open in a windowless headless renderer. KaTeX rendered. Re-read ten values against the fitting notebook.

## [2026-09-17] revise | tau_dust prior Uniform(0, 1)

- Pages: [[model]], research direction roadmap task tau-dust-railing.
- Change: Changed the production notebook's uniform tau_dust prior from Uniform(0, 0.2) to Uniform(0, 1) on Liu Hao's instruction. Updated the Model page row. Removed its '!' flag because no fit under the new prior exists yet. Three flags remain. Kept earlier railing results as tested bullets. Corrected the tested bullet: the tau_cn comparison was against Uniform(0, 2). Added the unscored roadmap task tau-dust-railing to check for railing. Appended Liu Hao's words under Amendments.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, wiki/notes/model.md, wiki/research/direction.md, wiki/research/model-page-spec.md, wiki/tests/test_research.py.
- Validation: wiki build passes (40 notes); both wiki test suites pass apart from the two failures that predate this change; tests/test_ceridwen_dr2_production.py passes (22); /wiki/p/tau-dust-railing/ built; Model row checked at 1280 px in a windowless headless renderer.

## [2026-09-17] decision | Science skills, workflows and the agent wiki submission format as a priority

- Pages: Home, research/direction.md
- Change: Roadmap task `science-skills-wiki-format` added at priority 10 on Liu Hao's instruction, with his original wording under Amendments.
- Validation: wiki build passes; the task shows on Home at 10/10 and its priority page opens.

## [2026-09-17] revise | Redshift and sigma_star sampled by default

- Pages: [[model]], [[redshift-sigma-wiggle]], research direction Amendments.
- Change: On Liu Hao's instruction the production notebook samples redshift, Uniform(z_cat - 0.1, z_cat + 0.1), and sigma_star, Normal(DR2, error) clipped at 3 errors, in every full-spectrum fit. Removed the switches CERIDWEN_FREE_ZRED_KMS and CERIDWEN_FREE_SIGMA. Sampled parameters rise from 14 to 16; NSS inner steps stay 65. Cherry-picked the fork's free-z-spectrum commit 354f5e9 onto the pinned ceridwen branch as c540bc7. Result attribute free_zred_kms replaced by zred_half_width. Updated the Model rows for redshift, sigma_star, resolution and the nested sampler. No fit has run under these defaults. Wording by Claude; codex quota exhausted until 19 Sep.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, ceridwen (submodule), tests/test_ceridwen_dr2_production.py, tests/test_production_speedup_schedule.py, scripts/validate_ceridwen_speedups.py, scripts/relabel_feh_notebooks.py, wiki/notes/model.md, wiki/notes/redshift-sigma-wiggle.md, wiki/research/direction.md.

## [2026-09-17] decision | Trend plots against stellar mass and the mock spectra test suite as priorities

- Pages: Home, research/direction.md
- Change: Roadmap tasks `alpha-fe-t50-vs-mass` at priority 8 and `mock-spectra-test-suite` at priority 6 added on Liu Hao's instruction, in his wording, with the originals under Amendments. Codex quota exhausted until 19 Sep, so no Codex pass.
- Validation: wiki build passes; both tasks show on Home at 8/10 and 6/10 and their priority pages open.

## [2026-09-17] decision | Local elliptical galaxies as relative ground truth as a priority

- Pages: Home, research/direction.md
- Change: Roadmap task `local-ellipticals-ground-truth` added at priority 9 on Liu Hao's instruction, in his wording, with the original under Amendments. Codex quota exhausted until 19 Sep, so no Codex pass.
- Validation: wiki build passes; the task shows on Home at 9/10 and its priority page opens.

## [2026-09-17] decision | Rising SFH continuity prior as a priority; Turner et al. (2025) added to papers

- Pages: Home, Papers, research/direction.md
- Change: Roadmap task `rising-sfh-continuity-prior` added at priority 8 on Liu Hao's instruction, with his original wording under Amendments. He wrote "turner 2015"; the paper with the rising continuity prior is Turner et al. (2025), MNRAS 537:1826-1848, arXiv:2410.05377, citation confirmed from the PDF and Crossref. PDF downloaded to papers/spectral fitting/ and listed in papers/README.md. Codex quota exhausted until 19 Sep, so no Codex pass.
- Files: papers/README.md, wiki/research/direction.md.
- Validation: wiki build passes; the task shows on Home at 8/10, its priority page opens and the Papers page links the PDF.

## [2026-09-17] decision | Conroy dust index railing and weak UV as a priority

- Pages: Home, research/direction.md
- Change: Roadmap task `dust-index-railing-weak-uv` added at priority 9 on Liu Hao's instruction, in his wording, with the original under Amendments. Codex quota exhausted until 19 Sep, so no Codex pass.
- Validation: wiki build passes; the task shows on Home at 9/10 and its priority page opens.

## [2026-09-17] analysis | M1_210210 reference fit and prior KL divergence

- Pages: notes/m1-210210-reference.md, research/experiments/e-m1-210210-reference.md
- Change: Two order-10 fits of M1_210210 on Vast (tau_dust Uniform(0, 0.2) at 55ff5f4; production defaults at cc983ce with tau_dust Uniform(0, 1) and sampled z, sigma_star) beside the stored order-3 fit: parameter table, fit, SFH and corner figures. Per-parameter KL divergence from the prior in bits from `scripts/plot_prior_kl.py`, figure and table written straight to `wiki/analyses/m1-210210-reference/` on Liu Hao's instruction. Codex quota exhausted until 19 Sep, so the note text and captions had no Codex pass.
- Files: scripts/plot_prior_kl.py, scripts/per_galaxy_diagnostics.py (`prior_unit_values`, `marginal_kl_bits`), tests/test_per_galaxy_diagnostics.py, results/m1-210210-reference/, wiki/analyses/m1-210210-reference/.
- Validation: four figures checked at 900 px; the first fit figure had the legend on the data and the polynomial panel scaled by unfitted pixels, both fixed; KL tests pass.

## [2026-09-17] revise | Dust corner plot uses every SFH bin by default

- Pages: [[notebook-map]]
- Change: On Liu Hao's instruction the production notebook's dust corner plots the dust parameters against every formed-mass fraction, not the three youngest. `N_YOUNG_BINS` removed; the Spearman printout covers every bin. No fit has run under this default. Wording by Claude; Codex quota exhausted until 19 Sep.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, wiki/notes/notebook-map.md.

## [2026-09-17] revise | Dust against every SFH bin added to the existing executed notebooks

- Pages: [[notebook-map]]
- Change: On Liu Hao's instruction every existing executed notebook got one added cell, tagged `dust-sfh-all-bins`, with the dust parameters against every formed-mass fraction and the per-pair Spearman lines. `scripts/add_dust_sfh_corner.py` builds it from `ceridwen_result.h5` with the notebook's own seed and bin edges. No fit was run. 556 of 558 notebooks done; 551 rebuilt draws match the saved `sfh/mass_fraction_draws`; 5 have no `ceridwen_derived_outputs.h5` and use the notebook's seed and the LEGA-C DR2 catalogue redshift. 2 have no `ceridwen_result.h5` and are unchanged: results/fit-accuracy-knobs/mock_tilt4_new_default/172669-M5_172669 and archive/results/a100-feature-spectrum. 163 of the changed notebooks are tracked in git; the rest are untracked on disk. Wording by Claude; Codex quota exhausted until 19 Sep.
- Files: scripts/add_dust_sfh_corner.py, results/ and archive/results/ executed notebooks, wiki/notes/notebook-map.md.
- Validation: nbformat validation passes on every changed notebook; each has one tagged cell; tracked diffs are insertions only; figures from every batch viewed, no overlaps or clipping.

## [2026-09-17] revise | Sampler progress moved to a file and absorption labels on existing figures

- Pages: [[notebook-map]]
- Change: On Liu Hao's instruction the template sampler cell runs with `verbose=False` and the sampler writes one JSON line per iteration to `RESULT_DIR/ns_progress.jsonl`, with dead points per second and likelihood calls per second. The cell keeps the settings line, one rate summary and the result summary. `scripts/relabel_executed_figures.py` redrew the fit and posterior-predictive spectrum figures of existing executed notebooks from `ceridwen_derived_outputs.h5` with absorption labels, in the same cell and output slot, and removed sampler progress lines that `execution.log` also holds. No fit was run. 530 of 558 notebooks relabelled; 21 already carried labels; 7 have no `ceridwen_derived_outputs.h5` and are unchanged. 137 changed notebooks are tracked in git. 393 are untracked on disk, so their previous PNGs exist nowhere else; the same h5 can redraw them. Five analysis notebooks were re-executed on CPU with `spectral_tight_layout`, so the feature legend no longer overlaps the axes: calibration-polynomial-dr2/analysis, fit-accuracy-knobs/analysis, fit-accuracy-knobs/new-defaults, redshift-sigma-wiggle/analysis, dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison. `plot_windows` in `scripts/absorption_mask_report.py` uses the shared marking; `feature_windows_M5_172669.png` regenerated. Wording by Claude; Codex quota exhausted until 19 Sep.
- Files: ceridwen/ceridwen/sampler/nested.py (submodule b419fd1), both template notebooks, scripts/relabel_executed_figures.py, scripts/per_galaxy_diagnostics.py, scripts/absorption_mask_report.py, scripts/run_ceridwen_vast_multi_gpu.py, tests/test_relabel_executed_figures.py, tests/test_per_galaxy_diagnostics.py, tests/test_ceridwen_dr2_production.py, wiki/analyses/absorption-mask/, wiki/notes/notebook-map.md.
- Validation: M13_232627 redraw compared with the original figure; 4038 valid and 3526 fitted pixels match the notebook printout and the mask gaps match. Tracked diffs touch only the sampler, predictive and fit cells. A quick local template run gives a two-block sampler cell and a five-line `ns_progress.jsonl`. Figures checked at 900 px. Tests for the touched files pass.

## [2026-09-18] infra | Notebook served from the TrueNAS box only

- Pages: none
- Change: On Liu Hao's instruction the wiki moved entirely to the TrueNAS server and the Mac no longer serves it. The Mac's launchd agent `com.liuhao.astro-wiki` and the `/wiki` route of the Mac's Tailscale Serve are removed. On the NAS, `scripts/truenas-wiki/docker-compose.yml` runs nginx for the pages and files and a `python:3.12-alpine` service running `scripts/serve_wiki.py` for `/wiki/api/`; nginx proxies the API to it on loopback and no longer falls back to the Mac. `serve_wiki.py` finds the project root from its own location. `scripts/publish_wiki.py` now pulls `wiki/research/activity/` from the NAS, sends the wiki sources, the server, the word counter and every linked file, and has the NAS build its own `public/`; it also brings the nginx access log to `~/Library/Logs/astro-wiki/nas-access.log` for the Review Inbox. The question box is not shown on the NAS pages: it resumes agent sessions that live on the Mac. Wording by Claude; Codex quota exhausted until 19 Sep.
- Files: scripts/serve_wiki.py, scripts/publish_wiki.py, scripts/truenas-wiki/nginx.conf, scripts/truenas-wiki/docker-compose.yml, tests/test_ceridwen_results_board.py, wiki/AGENTS.md, scripts/README.md.
- Validation: the NAS build lists the same 2995 files as the Mac build with equal PNG sizes; pages, `/wiki/f/` files and the activity API answer 200 through the tailnet URL; a POST with a foreign Origin gets 403 and a same-origin POST reaches the server; a repeated publish with nothing changed finishes in 7 s without a rebuild; 127.0.0.1:8765 on the Mac refuses.

## [2026-09-18] wiki | Tick box resolves a priority from Home

- Pages: [[index]]
- Change: Each priority row carries a tick box under its score; ticking resolves the task and unticking a row in the resolved table reopens it, and the row moves between the two tables without a reload. A failed save unticks the box and shows the server's message above the table.
- Files: wiki/research.py, wiki/assets/activity.js, wiki/assets/activity.css, wiki/tests/test_research.py, wiki/tests/test_activity.py.
- Validation: tick, untick, 409 and 404 paths driven in a headless browser against a scratch copy of the server; rows move and boxes follow the catalog state; screenshots at 1200 and 400 px; wiki tests pass except two failures present before this change (Hermes bridge session for the question-box fixture, three unlinked analysis notes).

## [2026-09-18] infra | Notebook at https://wiki.eclw.org/ behind Pangolin

- Pages: [[index]]
- Change: The notebook is published as https://wiki.eclw.org/ through Pangolin on the VPS: traefik and gerbil there, newt on the NAS, nginx listening on the newt bridge gateway 172.16.12.1:8765. Pages moved from `/wiki/` to the site root; old `/wiki/...` links redirect permanently and project files sit under `/f/`. Saves are accepted only from the wiki.eclw.org origin. The Tailscale Serve mapping stays until the Pangolin route is verified.
- Files: wiki/build.py, wiki/activity.py, scripts/serve_wiki.py, scripts/publish_wiki.py, scripts/truenas-wiki/nginx.conf, scripts/truenas-wiki/docker-compose.yml, wiki/tests/test_activity.py, wiki/tests/test_research.py, tests/test_ceridwen_results_board.py, wiki/AGENTS.md.
- Validation: from a container on the newt bridge, `/`, `/n/model/`, `/f/wiki/log.md`, `/api/catalog` and `/style.css` answer 200, `/wiki/` and `/wiki/n/model/` answer 301 to the root paths, a POST from the wiki.eclw.org origin reaches the server and one from a foreign origin gets 403; the same through the Tailscale route. Unit suite passes except the unlinked-analysis-notes failure present before this change.

## [2026-09-18] notebooks | Compact fit notebook and regenerated executed copies

- Pages: [[notes/notebook-map]], [[notes/model]], [[notes/default-fit-parameters]], [[notes/calibration-polynomial-dr2]], [[notes/fit-accuracy-knobs]], [[notes/absorption-line-mask]], [[notes/redshift-sigma-wiggle]]
- Change: On Liu Hao's instruction `notebooks/ceridwen_integrated_photometry_spectra.ipynb` shrank from 33 to 21 cells and from about 2100 to 923 code lines. Every setting and prior is a literal in two dictionaries at the top, `SETTINGS` and `PRIORS`; a parameter is sampled when its key is in `PRIORS`. The environment switches `CERIDWEN_FIT_MODE`, `SPECTRUM_PIXELS`, `FEATURE_*`, `MOCK_*`, `TAU_PRIOR`, `SFH_PRIOR`, `FREE_DUST_INDEX`, `PHOT_DROP`, `MASK_REST_WINDOWS`, `CALIBRATION_ORDER`, `CALIBRATION_PRIOR`, `PHOTOMETRY` and the branches they guarded are gone, with the settings prints, data-shape asserts, the data-only figure, the coefficient table, the age-mass corner and the interpretation cells. Kept: HST cutout, parameter block, sampler summary, KL and ESS table, photometry and spectrum figures, calibration polynomial figure, quantile table, physical and dust corners, SFH plot, both h5 files. The result h5 loses the switch-record attributes and gains `zred_half_width` and `sigma_star_err`. New `scripts/regenerate_fit_notebooks.py` re-executes the compact notebook for a stored fit on the CPU with the posterior reloaded through `load_result_h5`, setting target, seed, calibration order, tau bounds and the fixed or sampled z and sigma from the h5; all 189 executed notebooks were regenerated this way without a sampler run. Wording by Claude; Codex quota exhausted until 19 Sep.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, scripts/regenerate_fit_notebooks.py, scripts/validate_ceridwen_speedups.py, scripts/calibration_arms_vast.py, scripts/absorption_mask_grid.py, tests/test_ceridwen_dr2_production.py, results/dr2-quiescent-new-defaults/*/, results/m1-210210-reference/*/poly10/*/, wiki/research/experiments/e-dr2-revised.md.
- Validation: quick-profile smoke run on the CPU completes with the listed outputs; regenerated derived h5 for the three M1_210210 fits match the previous ones to float noise (draw indices identical, calibration coefficient summaries shift by about 1e-4 from CPU versus GPU predictions); 33 tests pass in the three notebook test files; the DR2 summary CSV rebuilt from the regenerated h5 differs from the current one by at most 2.4e-3 relative in the chi2 columns and 1e-13 elsewhere; the figure records of e-dr2-revised remapped to the compact cell numbers, with the dropped age-mass corner replaced by the dust corner.

## [2026-09-20] code | Notebook layout and saving

- Change: Full-screen writing sheet with a compact header and collapsible Notebook options. Done saves before closing. New note saves the current draft and opens a blank notebook. Save errors retain the open editor; local and server save states are distinct. Undo and Redo reflect the available history.
- Validation: Browser checks cover saved history and notebook options. Twelve ink runtime tests and 13 activity tests pass. The 41-note build passes. The broader wiki audit retains its unrelated question-box failure; the research suite retains its corpus coverage failure.

## [2026-09-20] ops | Restore the public wiki route

- Fault: DNS reached the VPS, but Pangolin contained no wiki resource. The NAS served the site correctly; the public gateway returned 404 and no valid wiki certificate.
- Change: Restored the Astro wiki resource at `wiki.eclw.org`, with HTTPS and SSO, through christscam to `http://172.16.12.1:8765`.
- Validation: HTTPS certificate verification passes. Unauthenticated requests redirect to Pangolin login. The signed-in browser loads Home, the metallicity priority, and the full-screen notebook.

## [2026-09-20] notebooks | KL bar chart appended to the fit notebook

- Pages: [[notes/notebook-map]], [[research/experiments/e-m1-210210-reference]]
- Change: On Liu Hao's instruction the fit notebook ends with a bar chart of D_KL(posterior || prior) in bits for every sampled scalar parameter, sorted from most to least constrained, parameters on the x axis. The cell imports `kl_table` from `scripts/plot_prior_kl.py` and `load_galaxy` from `scripts/per_galaxy_diagnostics.py`; `matplotlib.use("Agg")` moved into that script's `main()` so the notebook keeps its inline backend. Only the tau-1 order-10 M1_210210 notebook was regenerated, on the CPU from the stored posterior; the other 188 executed notebooks are unchanged. The 2026-09-20 amendment supersedes the 2026-09-17 message that KL could stay outside the notebook. Wording by Claude, notebook-map sentence by Codex.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, scripts/plot_prior_kl.py, results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb.
- Validation: the regenerated notebook has 23 cells and no error outputs; the KL figure was inspected at full size with 16 rotated labels, none overlapping or clipped; 24 notebook tests pass.

## [2026-09-21] notebooks | KL figure uses points, not bars, with a noise-floor band and a 1-bit line

- Pages: [[notes/notebook-map]], [[research/experiments/e-m1-210210-reference]]
- Change: Liu Hao rejected the bars ("takes up too much visual space, use points instead"). The last cell of the fit notebook now draws one point per parameter with its bootstrap error bar, labels rotated 40 degrees, no grid, top and right spines removed; layout chosen by Liu Hao from three designer previews. Only the tau-1 order-10 M1_210210 notebook was regenerated, on the CPU from the stored posterior. Amendment recorded with his original text. Later the same day two reference marks were added on a log axis: a grey band at the estimator noise floor, measured in the cell from 200 prior-only draws with the posterior weights (95th percentile 0.009 bits), and a dashed line at 1 bit, a stated convention for a factor-two narrowing of the prior, not a standard. Liu Hao picked the log-axis treatment from two designer variants.
- Files: notebooks/ceridwen_integrated_photometry_spectra.ipynb, results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb.
- Validation: the regenerated notebook has 23 cells and no error outputs; the figure was inspected at full size, 16 labels, none overlapping or clipped, no stray tick marks on the top or right edges.

## [2026-09-21] query | Rising continuity SFH prior in the literature

- Pages: [[notes/sfh-continuity-prior-variants]], [[research/questions/q-rising-continuity-prior]], [[notes/model]]
- Change: New literature note with the continuity prior (Leja 2019), the rising variants (de Graaff, Turner 2025, Wang 2023), the Dirichlet, bursty and UniverseMachine-centred variants, code locators in bd-j/prospector and jakobhelton/jwst_program_id_08544, and the most likely source of Jonah Powley's rising prior. New question record holds Liu Hao's 2026-09-21 question. Model page SFH prior row links the note. Web research requested by Liu Hao. Note prose by Codex.
- Validation: wiki build passes with 42 notes; both test suites pass apart from the two failures that predate this change (bridge question box, calibration analyses unlinked); all 188 LaTeX expressions in the note parse in the bundled KaTeX 0.18.7; the built note has 8 collapsed blocks and one table, and the question page shows the original question text.

## [2026-09-21] ingest | External comparison samples for fit outputs

- Pages: [[notes/external-comparison-samples]], [[research/questions/q-external-validation]], [[research/experiments/e-literature-ground-truth]]
- Change: Literature review requested by Liu Hao. The note tables local early-type samples, direct measurements (dynamical and lensing masses, resolved stars, cluster spectra) and z 0.4-0.8 samples, with method, catalogue access and the definition differences against Ceridwen, and lists three first comparisons. Values read from the arXiv PDFs; unverified values and catalogue locations are omitted. No catalogue data fetched, no fit run. Note and record wording by Codex gpt-6-astra from a fact sheet; log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] ingest | Weak emission in quiescent galaxies

- Pages: [[notes/weak-emission-quiescent]], [[research/experiments/e-weak-emission-literature]]
- Change: Six citations on faint emission and H-beta infill checked against the arXiv PDFs; Gonzalez 1993 (thesis) not read. The note tables incidence, power source, the H-beta to [O III] ratio, infill and age, z 0.6-0.9 results, and the emission selection and mask of the 187 fitted galaxies read from the local DR2 catalogue. Every row carries a check mark: PDF, not read, derived, textbook or repo. The record keeps the question as relayed in the task brief, not verbatim. Note and record wording by Codex gpt-6-astra from a fact sheet; log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] roadmap | Emission lines: model, mask or ignore, priority 9

- Pages: [[research/direction]], [[research/questions/q-emission-lines]], [[research/experiments/e-weak-emission-literature]]
- Change: Liu Hao's 2026-09-21 message appended to Amendments; roadmap task `emission-lines-model-mask-ignore` at his priority 9, linked to the new question `q-emission-lines`, which holds his words, the three options, the DR2 catalogue facts and the evidence links. No decision recorded. `ceridwen.neb.NebularModel` exists and is unused in the production fit. His question on circularity and his request to add the explanation are appended to Amendments; the five-point explanation and a Balmer recount on the 117 fitted galaxies covering all three lines (H-beta 2, H-gamma 5, H-delta 10) are in the item details and the question; Case B ratios marked unverified. Question wording by Codex gpt-6-astra from a fact sheet; log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] roadmap | NebularModel covers young-star ionisation only

- Pages: [[research/direction]], [[research/questions/q-emission-lines]]
- Change: Liu Hao's two 2026-09-21 messages appended to Amendments. The priority-9 item and the question state that `NebularModel` applies emission only to SSPs inside the CLOUDY cube age range (`NebularGridModel.py:355-380`), that the local MIST cubes span 0.5-20 Myr, and what the "model" option therefore requires. The Byler et al. 2017 attribution is marked unverified. No decision recorded. Wording by Codex gpt-6-astra from a fact sheet; cube-age line and log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] experiment | Wall time with free z and sigma_star

- Pages: [[research/experiments/e-runtime-z-sigma-speed]]
- Change: Liu Hao's 2026-09-21 message recorded. CPU profile of the M1_210210 likelihood with fixed and free z and sigma_star, the `Spectrum(baked_runtime=True)` path (ceridwen 6707c05, default off) and its equality test. Same-boot GPU benchmark planned, not run. Record wording by Codex gpt-6-astra from a fact sheet; tables and log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] experiment | M1_210210 without the emission-line mask

- Pages: [[notes/no-emission-mask]], [[research/experiments/e-no-emission-mask]]
- Change: One no-mask fit of M1_210210 on Vast.ai against the stored masked fit, same seed; arm `no_emission_mask` sets `CERIDWEN_SETTINGS_OVERRIDE` and the runner merges it into `SETTINGS` in the executed copy. Record holds Figures, Measurements, Results and Caveats at status results-ready; overlaid corner picked by Liu Hao from designer previews. Wording by Codex gpt-6-astra from a fact sheet; tables generated from the saved CSVs.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] infrastructure | Wiki edits go live in seconds

- Pages: `research_figures.py`, `research.py`, `build.py`, `scripts/publish_wiki.py`, `tests/test_research.py`, [[AGENTS]]
- Change: wiki/research_figures.py caches notebook PNGs by notebook version and hardlinks them into builds. NAS build time fell from 79.9 s to 3.4 s, Mac from 28.7 s to 3.7 s. research.py joins section text once and checks evidence paths with os.path. The watcher sends files whose size or time changed over one shared SSH connection. Partial publication takes 5.7 s, an unchanged check 0.3 s. On 2026-09-21, NAS nginx showed a note edit 8.7 s after saving and its revert after 9.4 s, previously about 106 s. Tests compare cold and cached outputs byte for byte and check cache replacement after notebook edits. Wording by Codex gpt-6-astra from a fact sheet; entry assembled by Claude.
- Validation: `wiki/tests/run_tests.py`, `python3 -m unittest discover -s wiki/tests`, a timed save measured at the NAS.

## [2026-09-21] roadmap | Priority-9 emission-line item cut to one sentence

- Pages: [[research/direction]], [[research/questions/q-emission-lines]]
- Change: On Liu Hao's feedback the roadmap item holds one sentence and its link to `q-emission-lines`. All evidence moved to the question as one-fact bullets in full words under five headings; code locators, paths and column names moved to its References. Every fact and unverified mark kept. Wording by Codex gpt-6-astra from a fact sheet; two bullets and the log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] infrastructure | Publish-time length check

- Pages: `build.py`, `length-baseline.txt`, `tests/test_length.py`
- Change: wiki/build.py runs check_lengths() before output: standard-library-only, no model call, whitespace-split words. Roadmap titles plus details exceeding 30 words or wiki/{notes,research} paragraphs exceeding 60 (excluding README/templates/activity) print '<path>: <task id or line>: N words (cap M)' and raise SystemExit. wiki/length-baseline.txt records 3 roadmap items and 46 paragraphs that exceed caps; they pass until growth. Wording by Codex gpt-6-astra from a fact sheet; entry assembled by Claude. Liu Hao accepted the check on 2026-09-21: "a cheap check would be good."
- Validation: `python3 wiki/build.py`, `wiki/tests/test_length.py`, `python3 -m unittest discover -s wiki/tests`, `wiki/tests/run_tests.py`.

## [2026-09-21] experiment | baked_runtime GPU benchmark and default

- Pages: [[research/experiments/e-runtime-z-sigma-speed]], [[notes/model]]
- Change: same-boot RTX 5060 Ti benchmark recorded (run, measurements, Liu Hao's two approvals under Amendments). `Spectrum(baked_runtime=True)` is the ceridwen default (5f2c316) and a `SETTINGS` entry of the fit notebook. Speed lines added to the Redshift and \(\sigma_\star\) rows of the model page. Wording by Codex gpt-6-astra from a fact sheet; tables and log entry by Claude.
- Validation: wiki build, `wiki/tests/run_tests.py` and `test_research.py`.

## [2026-09-21] infrastructure | Check-in pages

- Pages: `research/checkins/2026-09-21.md`, `checkins.py`, `research.py`, `index.md`.
- Change: Added `wiki/checkins.py`. `python3 wiki/checkins.py <date> --since <date>` drafts experiments with status `results-ready` or `reviewed`, dated since the previous check-in and absent from earlier check-ins.
- Each experiment shows its title, first figure with the record caption, and at most three rows from its first Measurements table, matching labels in Results text or, otherwise, each row’s first number.
- Sources also accept sections of hand-written items in fenced JSON: `text`, `points`, `link`, and one of `figure` (`<experiment>:<index>`), `image`, or code from a notebook cell. `## Your words` preserves the messages in a collapsed Research record.
- The first page contains Liu Hao’s Done and Questions items. `research.py`’s `write_pages` calls `checkins.write_pages`; `wiki/build.py` is unchanged.
- Validation: `python3 wiki/build.py`, `wiki/tests/run_tests.py`, `test_research.py`; page checked at 1440 and 900 px.
