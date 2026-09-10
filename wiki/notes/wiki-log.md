---
title: Wiki log
date: 2026-09-04
section: Archive
tags: [log]
job: 
status: obsolete
source: wiki/log.md
---

<details>
<summary>[2026-08-20] setup | Wiki initialized</summary>

- Pages: [[index]], [[overview]]
- Change: Added the Codex workflow and empty knowledge structure.

</details>

<details>
<summary>[2026-08-20] codebase | Initial autonomous code map</summary>

- Pages: [[guides/reading-order]], [[codebase/project-map]], [[notebooks/notebook-map]]
- Change: Documented project modules, data flow, Ceridwen internals, and tests.

</details>

<details>
<summary>[2026-08-21] format | Human wiki moved to HTML</summary>

- Pages: `index.html`, `overview.html`, `guides/`, `codebase/`, `notebooks/`
- Change: Replaced reader-facing Markdown with styled, linked HTML pages.

</details>

<details>
<summary>[2026-08-21] codebase | Source-first reading examples</summary>

- Pages: all reader-facing guides, codebase pages, and the notebook map
- Change: Added 29 exact source excerpts with locators and reading explanations.

</details>

<details>
<summary>[2026-08-24] codebase | Notebook workspace cleanup</summary>

- Pages: `notebooks/notebook-map.html`, `guides/reading-order.html`, `codebase/project-modules.html`
- Change: Removed retired notebooks from the live map and separated practice material.

</details>

<details>
<summary>[2026-08-24] format | Minimal wiki style</summary>

- Pages: all reader pages, `assets/wiki.css`, `AGENTS.md`
- Change: Removed repeated prompts, exercises, decorative cards, and redundant navigation.

</details>

<details>
<summary>[2026-08-24] codebase | Vast.ai GPU workflow</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.html`, `index.md`
- Change: Added cloud-GPU setup, data transfer, validation, and notebook execution.

</details>

<details>
<summary>[2026-08-24] codebase | Ceridwen notebook names</summary>

- Pages: `notebooks/notebook-map.html`, `guides/reading-order.html`, `guides/vast-ai-gpu-workflow.html`
- Change: Retired notebooks 05-06 and removed numeric prefixes from active notebooks.

</details>

<details>
<summary>[2026-08-24] codebase | Shared Ceridwen kernel</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`
- Change: Documented shared CPU/GPU kernel resolution and bounded CPU trials.

</details>

<details>
<summary>[2026-08-25] codebase | Ceridwen nested-sampling notebooks</summary>

- Pages: `notebooks/notebook-map.html`, `codebase/ceridwen-likelihood-sampling.html`, `index.md`
- Change: Replaced active notebook NUTS paths with weighted BlackJAX nested sampling.

</details>

<details>
<summary>[2026-08-25] codebase | Vast.ai CUDA library isolation</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented JAX isolation from Vast's inherited system CUDA library path.

</details>

<details>
<summary>[2026-08-25] codebase | Integrated-fit sampler settings</summary>

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Set the production joint fit to 300 live points, 25 deletions, and 40 inner steps.

</details>

<details>
<summary>[2026-08-25] codebase | Modal GPU workflow</summary>

- Pages: `guides/modal-gpu-workflow.html`, `index.html`, `index.md`
- Change: Added persistent inputs, batch execution, and interactive Jupyter Sandbox controls.

</details>

<details>
<summary>[2026-08-25] codebase | Modal GPU quick-run validation</summary>

- Pages: `guides/modal-gpu-workflow.html`, `index.md`
- Change: Fixed Modal Volume workspace paths, disabled JAX preallocation, and recorded the successful A100 quick batch.

</details>

<details>
<summary>[2026-08-25] codebase | Ceridwen v0.2.2 workflow</summary>

- Pages: Ceridwen codebase pages, notebook map, Vast.ai guide, Modal guide
- Change: Documented the published schema-2.1 grid, pinned per-pixel resolution support, upstream sampler settings, checkpoints, and reloadable HDF5 results.

</details>

<details>
<summary>[2026-08-25] format | STE rewrite</summary>

- Pages: all reader pages, `index.md`, `AGENTS.md`
- Change: Rewrote the wiki in controlled, plain English while preserving facts, qualifiers, code excerpts, and source locators.

</details>

<details>
<summary>[2026-08-25] codebase | Modal v0.2.2 GPU validation</summary>

- Pages: `guides/modal-gpu-workflow.html`
- Change: Set an explicit remote project root and validated the published schema-2.1 grid in an A100 quick run.

</details>

<details>
<summary>[2026-08-25] codebase | Vast A100 recommendation</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Replaced the RTX recommendation with an A100 40 GB and recorded the tested Croatia host.

</details>

<details>
<summary>[2026-08-25] scope | Ceridwen primary focus</summary>

- Pages: `index.html`, `overview.html`, `guides/reading-order.html`, `guides/python-patterns.html`, `codebase/project-map.html`, `codebase/project-modules.html`, `codebase/data-pipeline.html`, `notebooks/notebook-map.html`, `index.md`, `AGENTS.md`
- Change: Made Ceridwen the primary workflow and marked earlier inference branches as inactive history.

</details>

<details>
<summary>[2026-08-25] format | Native workflow diagrams</summary>

- Pages: all reader pages, `assets/wiki.css`, `index.md`, `AGENTS.md`
- Change: Replaced text diagrams and added responsive schematics for the Ceridwen learning path.

</details>

<details>
<summary>[2026-08-25] format | Source-backed teaching blocks</summary>

- Pages: technical reader pages, `index.md`, `AGENTS.md`
- Change: Paired exact code excerpts with source documentation and plain explanations.

</details>

<details>
<summary>[2026-08-25] codebase | Compact spectral likelihood modes</summary>

- Pages: `notebooks/notebook-map.html`, `codebase/data-pipeline.html`, `codebase/ceridwen-likelihood-sampling.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Documented compact full-spectrum and LEGA-C feature-band fits with Modal controls.

</details>

<details>
<summary>[2026-08-25] codebase | Complete Ceridwen fit outputs</summary>

- Pages: `notebooks/notebook-map.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Documented detached Modal runs, persistent timing, posterior predictions, and star-formation histories.

</details>

<details>
<summary>[2026-08-25] codebase | Detached Modal function calls</summary>

- Pages: `guides/modal-gpu-workflow.html`, `index.md`
- Change: Made batch notebook execution independent of local-entrypoint cancellation and recorded interrupted timing states.

</details>

<details>
<summary>[2026-08-26] codebase | Feature-spectrum posterior report</summary>

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented HDF5 posterior tables, parameter marginals, corner plots, and derived mass-weighted age.

</details>

<details>
<summary>[2026-08-26] query | Ceridwen A100 benchmark runs</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.html`, `index.md`
- Change: Converted the Vast.ai and Modal A100 timings into a readable comparison with workload and completion-status caveats.

</details>

<details>
<summary>[2026-08-26] query | Concise A100 benchmark table</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Replaced the benchmark analysis with hardware and sampler figures for all retained runs.

</details>

<details>
<summary>[2026-08-26] query | Omit unrecorded wiki metrics</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Removed unrecorded metrics and excluded JIT compilation from throughput figures.

</details>

<details>
<summary>[2026-08-26] query | Matched V100 benchmark checkpoint</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.html`, `index.md`
- Change: Recorded matched A100–V100 throughput, JAX peak memory, and the bounded bottleneck inference.

</details>

<details>
<summary>[2026-08-26] query | Hardware-first GPU benchmark table</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Combined GPU specifications and post-JIT throughput in one workload-labelled table.

</details>

<details>
<summary>[2026-08-26] codebase | Public wiki deployment</summary>

- Pages: `.github/workflows/pages.yml`
- Change: Published reader-facing wiki files through GitHub Pages.

</details>

<details>
<summary>[2026-08-26] codebase | Reproducible Vast GPU benchmark</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Documented the fixed 5,000-call benchmark, fingerprints, outputs, and comparison command.

</details>

<details>
<summary>[2026-08-26] query | V100 allocator memory verification</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Recorded two fresh-process JAX peaks, 100 ms NVML traces, and allocator-profile evidence.

</details>

<details>
<summary>[2026-08-26] query | Concise GPU comparison</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Reduced the benchmark introduction to one matched hardware and throughput table.

</details>

<details>
<summary>[2026-08-26] query | FP32 GPU comparison</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Added peak FP32 throughput and made it a required GPU comparison field.

</details>

<details>
<summary>[2026-08-26] query | Relevant GPU compute paths</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Added FP32 and FP64 core counts, tensor paths, L2 cache, and dense hardware peaks.

</details>

<details>
<summary>[2026-08-26] query | Benchmark schema fields</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Added the Ceridwen grid schema to each benchmark row and future benchmark rules.

</details>

<details>
<summary>[2026-08-26] query | Concise memory benchmark</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Restored retained timings and reduced the V100 memory section without removing measurements.

</details>

<details>
<summary>[2026-08-26] query | Plain memory terms</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`
- Change: Replaced tool labels with plain memory terms and defined each measurement source.

</details>

<details>
<summary>[2026-08-26] codebase | Modal A100 kernel trace</summary>

- Pages: `guides/modal-gpu-workflow.html`, `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Documented the fixed post-JIT trace, saved XProf files, and reduction-dominated GPU timing.

</details>

<details>
<summary>[2026-08-26] query | Matched Vast GPU benchmark</summary>

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Added matched RTX 3090, RTX 4090, and H100 speed, cost, and memory results.

</details>

<details>
<summary>[2026-08-26] query | Merged GPU benchmark page</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.html`, `index.md`, `guides/modal-gpu-workflow.html`
- Change: Renamed the A100 benchmark page, grouped every GPU type into one hardware, run, and memory table, and added sourced RTX 3090, RTX 4090, and H100 specifications.

</details>

<details>
<summary>[2026-08-26] query | Measurement-only GPU benchmark page</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `AGENTS.md`, `index.md`
- Change: Removed the GPU hardware section, added an FP32 peak column and a calls/s against FP32 peak chart, and reduced the memory and kernel-trace results to short notes.

</details>

<details>
<summary>[2026-08-26] query | Precision charts on the GPU benchmark page</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `AGENTS.md`
- Change: Replaced the single chart with eight panels for CUDA FP32, CUDA FP64, and the tensor precisions, removed the speed-and-cost list, and reduced the source excerpt to the sampler settings.

</details>

<details>
<summary>[2026-08-26] query | Grouped benchmark rows by GPU</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Grouped the measured-run rows by GPU model, fastest group first, and noted the new order.

</details>

<details>
<summary>[2026-08-26] query | Predicted and measured Vast GPU rates</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added RTX 3060, RTX 3080 Ti, and RTX 4070 Super speed, cost, transfer-price, prediction, and memory results.

</details>

<details>
<summary>[2026-08-26] query | Reader-facing benchmark results</summary>

- Pages: `AGENTS.md`, `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Removed prediction and workflow bookkeeping from the benchmark page and made measured reader-facing results the wiki rule.

</details>

<details>
<summary>[2026-08-26] codebase | Four-GPU Vast fit launcher</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented one independent joint Ceridwen fit per GPU, isolated outputs, and partial-checkpoint recovery.

</details>

<details>
<summary>[2026-08-26] query | Log-log GPU benchmark charts</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Rebuilt the six speed panels on log axes with a none band, cased dot marks, and collision-free labels.

</details>

<details>
<summary>[2026-08-26] query | GPU benchmark cost column</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Moved the cost column to one million calls and added marked price estimates for the Vast A100 and V100 runs.

</details>

<details>
<summary>[2026-08-26] codebase | Four-GPU production sampler profile</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Recorded the 300-live-point BlackJAX NSS profile with 40 slice steps, 25 deletions, and `logZ_tol=-3`.

</details>

<details>
<summary>[2026-08-27] codebase | Eight-GB Vast benchmark</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented on-demand JAX allocation, 8 GB benchmark support, and schema-v1 comparison compatibility.

</details>

<details>
<summary>[2026-08-27] codebase | Joint posterior corner plots</summary>

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented aligned posterior rows and both stable corner-plot filenames.

</details>

<details>
<summary>[2026-08-27] codebase | Compact Vast benchmark image</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Set the CUDA 12.6.3 base image as the default for current and future Vast benchmarks.

</details>

<details>
<summary>[2026-08-27] query | Eight-GB allocator benchmark</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added matched RTX 3070 results for on-demand and 50% pooled JAX allocation.

</details>

<details>
<summary>[2026-08-27] query | Blackwell RTX 50-series benchmarks</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added measured RTX 5060 Ti, RTX 5070, RTX 5070 Ti, and RTX 5080 speed, cost, and memory results.

</details>

<details>
<summary>[2026-08-27] query | RTX 5090 complete-fit benchmark</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added the complete RTX 5090 fit rate, actual cost, sampler settings, and observed sampling memory.

</details>

<details>
<summary>[2026-08-27] query | Additional Blackwell GPU benchmarks</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added B200, RTX 5060, and RTX PRO 4000, 4500, 5000, and 6000 speed, cost, and memory results.

</details>

<details>
<summary>[2026-08-28] query | Ampere and Ada GPU sweep</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added seventeen measured runs, marked earlier comparison fingerprints, and retained all prior benchmark rows.

</details>

<details>
<summary>[2026-08-28] query | RTX 5060 fast-basis convergence test</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Added paired converged speeds and recorded the failed posterior and evidence equivalence gate.

</details>

<details>
<summary>[2026-08-28] codebase | Separate paired-fit notebooks</summary>

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented independent executed baseline and fast-path reports with complete saved plots.

</details>

<details>
<summary>[2026-08-28] codebase | Interactive active-codebase map</summary>

- Pages: `codebase/active-codebase-map.html`, `index.html`, `index.md`, `AGENTS.md`
- Change: Added a validated Archify map of the active Ceridwen project and allowed self-contained JavaScript for interactive diagrams.

</details>

<details>
<summary>[2026-08-28] codebase | Benchmark artifact relocation</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/modal-gpu-workflow.html`, `index.md`
- Change: Updated benchmark evidence paths after moving non-scientific runs out of `results/`.

</details>

<details>
<summary>[2026-08-28] codebase | Readable result directory names</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Updated the RTX 5090 evidence path after shortening result directory names.

</details>

<details>
<summary>[2026-08-28] codebase | Smoothed posterior density plots</summary>

- Pages: `notebooks/notebook-map.html`, `index.md`
- Change: Documented the shared blue density style and HDF5-only result plot regeneration.

</details>

<details>
<summary>[2026-08-28] codebase | Stellar-index likelihood mode</summary>

- Pages: `codebase/ceridwen-observations-model.html`, `codebase/data-pipeline.html`, `notebooks/notebook-map.html`, `guides/modal-gpu-workflow.html`, `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Documented the separate stellar-index observation, selectable integrated-fit likelihoods, outputs, and cloud controls.

</details>

<details>
<summary>[2026-08-30] codebase | DR2 quiescent production run</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `codebase/data-pipeline.html`, `codebase/ceridwen-ssp-csp.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented 187 unique targets, automatic SFH contraction, strict NSS settings, fitted spectrum scaling, embedded figures, two RTX 5060 shards, and local cap-aware result validation and cleanup.

</details>

<details>
<summary>[2026-09-01] analysis | Ceridwen differential ages</summary>

- Pages: `overview.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Documented the Borghi-style binning, posterior bootstrap, unstable negative result, saved aggregate result, and cosmology-dependence boundary.

</details>

<details>
<summary>[2026-09-01] analysis | Ceridwen chronometer audit</summary>

- Pages: `overview.html`, `notebooks/notebook-map.html`, `index.md`
- Change: Added controlled Borghi cohorts, unbinned slopes, formation-time drift, selection sensitivity, influence, and fit diagnostics.

</details>

<details>
<summary>[2026-09-01] codebase | Static smoothing collapsed into one convolution</summary>

- Pages: `codebase/ceridwen-observations-model.html`, `index.md`
- Change: Documented the quadrature-combined LOSVD and instrumental convolution, the baked interpolation indices and Fourier taper, the input-floored resampling grid, lazy `_H`, and the measured cost and width-accuracy comparison.

</details>

<details>
<summary>[2026-09-01] codebase | Combined static smoother made the installed default</summary>

- Pages: `codebase/ceridwen-observations-model.html`
- Change: Recorded that the superproject pins the ceridwen commit with `_smoothing.py`, that `.gitmodules` points at the project copy of ceridwen, and that the bootstrap reinstalls ceridwen and checks the import.

</details>

<details>
<summary>[2026-09-01] lint | Fixed-grid SFH basis accepted</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`
- Change: Removed the equivalence-gate caveat and the "keep the baseline basis" synthesis. Seed-to-seed scatter of the baseline exceeds the gate thresholds, so the fixed-grid basis is accepted as the default. Removed the gate script and the variation-notebook builder.

</details>

<details>
<summary>[2026-09-01] analysis | Likelihood kernel A/B and per-GPU concurrency</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `codebase/ceridwen-likelihood-sampling.html`
- Change: Recorded the same-boot RTX 5060 Ti comparison (kernel-count reductions verified bit-identical but GPU-neutral; banded smoother rejected), the 66 percent boot-to-boot variance caveat, linear scaling to three concurrent fits per GPU, and the NumPy sedpy filter construction cutting per-fit setup to about 27 s.

</details>

<details>
<summary>[2026-09-01] codebase | Speed-up defaults for every run</summary>

- Pages: `guides/vast-ai-gpu-workflow.html`, `guides/modal-gpu-workflow.html`, `codebase/ceridwen-observations-model.html`, `analyses/ceridwen-gpu-benchmarks.html`, `index.md`
- Change: Recorded the sedpy_jax fork as the `external/sedpy_jax` submodule that the bootstrap and Modal image install from the tree, the `fits_per_gpu` manifest field, and the same-boot RTX 4060 Ti measurement in which three concurrent production fits gave no aggregate gain over one, so the shard runner keeps one fit per GPU by default.

</details>

<details>
<summary>[2026-09-02] analysis | N=2 concurrency and JAX allocator levels on 8 GB</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/vast-ai-gpu-workflow.html`
- Change: Recorded the same-boot RTX 3070 measurement of one, two, and three concurrent production fits (0.96 to 0.97 of one fit in aggregate, default stays one fit per GPU), the 0.8 to 1.0 GiB JAX working set against the 75 percent preallocated pool, the 0.14 fraction and preallocation-off levels at full speed, the 0.10 fraction autotuning failure, and the one-iteration sampler shift that a smaller pool causes.

</details>

<details>
<summary>[2026-09-02] analysis | Blackwell concurrency on 8, 12, and 16 GB</summary>

- Pages: `analyses/ceridwen-gpu-benchmarks.html`, `guides/vast-ai-gpu-workflow.html`, `index.md`
- Change: Recorded the same-boot RTX 5060, RTX 5070, and RTX 5060 Ti 16 GB measurements of one, two, and three concurrent production fits (0.99 to 1.03 of one fit in aggregate, default stays one fit per GPU), the 1,005 MiB JAX working set per fit against the whole-GPU peaks, the identical 1,157,000-call M5_172669 fit across all Blackwell levels, and the single-fit cost per card.

</details>

<details>
<summary>[2026-09-02] analysis | Absorption-line pixel mask (draft)</summary>

- Pages: `analyses/absorption-line-mask.html`, `index.md`
- Change: Opened a draft analysis of feature-only and continuum-down-weighted spectral likelihoods: the S/N-squared weight budget of the current joint likelihood for three DR2 targets, a Fisher forecast per parameter, the feature catalogue and modes added to ceridwen on branch `absorption-mask`, and the mock and real-target experiment design. Result sections are filled once the Vast runs finish.

</details>

<details>
<summary>[2026-09-02] analysis | Absorption-line pixel mask: results</summary>

- Pages: `analyses/absorption-line-mask.html`
- Change: Filled the draft with the 45-fit grid (36 mocks with 0, 3 and 6 percent continuum tilts at two S/N scales; M5_172669, M9_232005 and M11_214430 in three pixel modes). Feature-only and continuum-down-weighted likelihoods carry the same tilt-induced bias as the full spectrum and are 1.1 to 1.6 times wider; on the real targets they move the posteriors by up to 22 sigma. Recommended default: off. Result figures under `analyses/absorption-mask/`. Page stays a draft pending Liu Hao's decision on the default, line list and window.

</details>

<details>
<summary>[2026-09-03] analysis | DR2 quiescent sample figure set (layout B)</summary>

- Pages: `analyses/dr2-quiescent-sample.html`, `index.md`
- Change: Published the final 187-galaxy figure set in the chosen layout B (single age–redshift panel with Ceridwen−Borghi residual strip): headline, three formation-timescale plots, 1D distributions, and fit-quality panel, all rendered from `results/dr2-quiescent-summary.csv` into `analyses/dr2-quiescent-sample/` (PNG + PDF). Superseded embedded chronometer figures backed up under `analyses/_old/`.

</details>

<details>
<summary>[2026-09-04] analysis | Ceridwen results board</summary>

- Pages: `analyses/ceridwen-results.html`, `index.html`, `index.md`
- Change: New single landing page for every Ceridwen analysis output (DR2 final set, Borghi comparison, summary CSV, absorption mask, calibration polynomial, GPU benchmarks, chronometer notebook) with inline figures, artifact links, a push-state/open-decision table, and a Results entry in the index route and sections.

</details>

<details>
<summary>[2026-09-04] analysis | Results board repair: full audit, true push states</summary>

- Pages: `analyses/ceridwen-results.html`
- Change: Inlined the omitted dt-mass/dt-alpha, all four absorption-mask, and all five calibration plots; added a directory-level related-fit-runs section and a PDF/CSV/notebook/script artifact list; split the calibration row into pushed tilt-origin branch verdict (`85c1e4a`) vs untracked local dir; stated the board's own unpushed state. GitHub search confirms plain-HTML/no-framework dashboards are the common pattern, matching this wiki's existing shell.

</details>

<details>
<summary>[2026-09-04] analysis | Hostable checkpoint animation</summary>

- Pages: `analyses/ceridwen-results.html`, `analyses/checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html`, `index.md`
- Change: Added the self-contained viewer inside the published wiki root, preserved its accepted scientific payload, and fitted its controls, legend, axes, and plots into portrait and landscape mobile viewports.

</details>

<details>
<summary>[2026-09-04] analysis | Ceridwen common results board repair & Tailscale hosting</summary>

- Pages: `analyses/ceridwen-results.html`, `scripts/serve_wiki.py`, `tests/test_ceridwen_results_board.py`
- Change: Rebuilt the Ceridwen results board from the validated 79-item audit manifest; corrected calibration science (DR2 spectra are brighter than production photometry; corrected photometry eliminates M4 tilt; M5 retains dust-degeneracy tilt from 0.3-mag optical-NIR model mismatch); inlined all 19 PNG plots with accessible fallback text; linked all 79 deliverables (PDFs, CSVs, notebooks, scripts, directories); launched persistent loopback launchd service (`com.liuhao.astro-wiki`) on port 8765 exposed via Tailscale Serve over HTTPS tailnet URL (`https://liu-haos-macbook-pro.tail5c940d.ts.net/wiki/analyses/ceridwen-results.html`).

</details>

<details>
<summary>[2026-09-04] format | Wiki rebuilt as a lab notebook</summary>

- Pages: `notes/*.md`, `build.py`, `tests/run_tests.py`, `public/`
- Change: Converted every HTML page to a Markdown note, added a stdlib

generator with search and RSS, and added a per-note question box that resumes
the worker session recorded on the note.

</details>
