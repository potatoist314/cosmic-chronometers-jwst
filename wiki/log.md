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

## [2026-09-02] analysis | Calibration polynomial in the spectrum likelihood

- Pages: `analyses/ceridwen-calibration-polynomial.html`, `index.md`
- Change: Added a draft analysis page explaining Prospector's spectrophotometric calibration vector, recording that `Spectrum.fit_polynomial_calibration` was never on the sampled path, documenting the profiled Chebyshev `PolynomialCalibration` on branch `calibration-polynomial`, and reporting the mock and DR2 fits with and without it.

## [2026-09-03] analysis | Origin of the LEGA-C spectrum versus photometry tilt

- Pages: `analyses/ceridwen-calibration-polynomial.html`, `index.md`
- Change: Added the follow-up that settles where the 25 percent tilt comes from: quoted the DR2 release description and the three LEGA-C papers (spectra flux-calibrated by a 5th-order polynomial onto FAST templates of the UltraVISTA total SED, colour gradients uncorrected, no published throughput trend), compared each spectrum with four photometric SEDs in the five intermediate bands inside its range, and reported 46 further fits (error floor 0.02 to 0.15, COSMOS2015 3-arcsecond versus Laigle total versus UltraVISTA photometry, photometry-only, spectrum-only, free dust slope, Calzetti, photometric dust prior, bands left out). Hypotheses (a) calibration and (b) aperture gradient are excluded; the production photometry mixed 3-arcsecond apertures with total IRAC fluxes and skipped the offsets, which explains the whole tilt of the 4.6 Gyr galaxy and the normalisation of both; the 1.7 Gyr galaxy's residual tilt is the dust–polynomial degeneracy driven by a 0.3 mag optical–NIR mismatch of the model family at its line-based solution. Recommended default: corrected total photometry, all twelve bands, order-3 polynomial with `spectrum_scaling` kept.
