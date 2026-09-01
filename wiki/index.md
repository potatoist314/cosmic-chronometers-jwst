# Agent Wiki Index

Human entry point: `index.html` (updated 2026-09-01)

Reader pages use responsive HTML, CSS, and inline SVG schematics. The Archify
map uses self-contained JavaScript; no page loads external diagram assets.

Technical pages contain one or two source-backed teaching blocks. Each block
pairs an exact code excerpt with source documentation and a plain explanation.

## Synthesis

- `overview.html` — Explains the Ceridwen-first flow, chronometer boundary, and reading path.

## Learning guides

- `guides/reading-order.html` — Gives an ordered path through the active Ceridwen workflow.
- `guides/python-patterns.html` — Python and JAX patterns used here.
- `guides/vast-ai-gpu-workflow.html` — Explains reliable RTX 5060 selection, deterministic DR2 shards, production sampling, and result transfer.
- `guides/modal-gpu-workflow.html` — Explains Modal inputs, selectable spectroscopy modes, detached runs, Jupyter, and benchmark storage.

## Codebase

- `codebase/active-codebase-map.html` — Interactively maps the active data, notebook, Ceridwen, sampling, GPU, test, and result paths.
- `codebase/project-map.html` — Explains repository boundaries, entry points, and environments.
- `codebase/project-modules.html` — Explains active support scripts and retained legacy modules.
- `codebase/data-pipeline.html` — Traces LEGA-C spectra or published stellar indices and COSMOS2015 photometry into Ceridwen.
- `codebase/ceridwen-architecture.html` — Explains the packages and complete call graph.
- `codebase/ceridwen-ssp-csp.html` — Explains SSP grids, SFH weights, automatic fixed-grid contraction, and spectra.
- `codebase/ceridwen-observations-model.html` — Explains photometry, spectra, emission lines, stellar indices, and model parameters.
- `codebase/ceridwen-likelihood-sampling.html` — Explains likelihoods, samplers, checkpoints, and HDF5 results.
- `codebase/tests-as-documentation.html` — Explains tests that define important contracts.

## Notebooks

- `notebooks/notebook-map.html` — Explains fitting modes, embedded outputs, posterior reports, and the Ceridwen differential-age analysis.

## Sources

The wiki does not contain literature source pages. The current pages document live code.

## Concepts

`guides/python-patterns.html` currently explains the code concepts.

## Methods

The codebase pages explain the Ceridwen methods beside their implementations.

## Datasets

`codebase/data-pipeline.html` explains the datasets.

## Analyses

- `analyses/ceridwen-gpu-benchmarks.html` — Compares speed, cost, memory, and hardware behaviour across forty-six measured GPU runs stored under `benchmarks/`.
