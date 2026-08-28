# Agent Wiki Index

Human entry point: `index.html` (updated 2026-08-26)

Reader pages use responsive HTML, CSS, and inline SVG schematics. They do not
require JavaScript or external diagram assets.

Technical pages contain one or two source-backed teaching blocks. Each block
pairs an exact code excerpt with source documentation and a plain explanation.

## Synthesis

- `overview.html` — Explains the Ceridwen-first codebase flow and reading path.

## Learning guides

- `guides/reading-order.html` — Gives an ordered path through the active Ceridwen workflow.
- `guides/python-patterns.html` — Python and JAX patterns used here.
- `guides/vast-ai-gpu-workflow.html` — Explains compact-image Vast setup, SFH-basis benchmark choices, production sampling, and saved results.
- `guides/modal-gpu-workflow.html` — Explains Modal inputs, detached A100 runs, bounded kernel traces, and persistent outputs.

## Codebase

- `codebase/project-map.html` — Explains repository boundaries, entry points, and environments.
- `codebase/project-modules.html` — Explains active support scripts and retained legacy modules.
- `codebase/data-pipeline.html` — Traces LEGA-C data into Ceridwen observations.
- `codebase/ceridwen-architecture.html` — Explains the packages and complete call graph.
- `codebase/ceridwen-ssp-csp.html` — Explains SSP grids, SFH weights, and spectra.
- `codebase/ceridwen-observations-model.html` — Explains data projections and parameters.
- `codebase/ceridwen-likelihood-sampling.html` — Explains likelihoods, samplers, checkpoints, and HDF5 results.
- `codebase/tests-as-documentation.html` — Explains tests that define important contracts.

## Notebooks

- `notebooks/notebook-map.html` — Explains fitting notebooks, saved outputs, aligned posterior rows, and two joint corner plots.

## Sources

The wiki does not contain literature source pages. The current pages document live code.

## Concepts

`guides/python-patterns.html` currently explains the code concepts.

## Methods

The codebase pages explain the Ceridwen methods beside their implementations.

## Datasets

`codebase/data-pipeline.html` explains the datasets.

## Analyses

- `analyses/ceridwen-gpu-benchmarks.html` — Compares measured speed, cost, memory, hardware behaviour, and the RTX 5060 SFH fast path across twenty GPU types.
