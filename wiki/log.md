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

## [2026-08-26] query | Ceridwen A100 benchmark runs

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.html`, `index.md`
- Change: Converted the Vast.ai and Modal A100 timings into a readable comparison with workload and completion-status caveats.

## [2026-08-26] query | Concise A100 benchmark table

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `index.md`
- Change: Replaced the benchmark analysis with hardware and sampler figures for all retained runs.

## [2026-08-26] query | Omit unrecorded wiki metrics

- Pages: `analyses/ceridwen-a100-benchmarks.html`, `AGENTS.md`
- Change: Removed unrecorded metrics and excluded JIT compilation from throughput figures.
