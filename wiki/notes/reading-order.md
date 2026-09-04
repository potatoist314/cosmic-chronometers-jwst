---
title: Reading order
date: 2026-08-25
section: Guides
tags: [ceridwen, reading]
job: 
old: _old/guides/reading-order.html
---

1. [Repository](#stage-1-learn-the-repository)Boundaries
2. [Data](#stage-2-read-small-project-functions)Representations
3. [Notebooks](#stage-3-follow-a-data-product)Configuration
4. [Prediction](#stage-4-read-notebooks-as-orchestration)Forward model
5. [Sampling](#stage-5-trace-one-ceridwen-prediction)Saved result

<figure>
<figcaption>Each stage adds one part of the active fit.</figcaption>
</figure>

### Stage 1: Learn the repository

Read [Project map](../project-map/). Keep these boundaries in mind:

- Ceridwen is the primary model and inference path.
- `main.py` is a scaffold. It is not a scientific entry point.
- The project owns its code but does not own submodule code.
- The root project and Ceridwen use separate Python environments.

### Stage 2: Trace the input data

Read [Data pipeline](../data-pipeline/). Then trace one LEGA-C object through these forms:

1. Find the selected row in the LEGA-C catalogue.
2. Open the matching LEGA-C spectrum.
3. Find the matched COSMOS2015 photometry.
4. Trace the wavelength and flux conversions.
5. Inspect the Ceridwen `Spectrum` and `Photometry` objects.

Each step changes the data representation. The galaxy stays the same.

### Stage 3: Read the active notebooks

Read [Notebook map](../notebook-map/). Then read these notebooks:

1. Read `ceridwen_test_spectra.ipynb` for the spectral fit.
2. Read `ceridwen_integrated_photometry_spectra.ipynb` for the joint fit.

The notebooks configure the data, model, likelihood, sampler, and saved result.

### Stage 4: Trace one Ceridwen prediction

Read these pages in order:

1. [Ceridwen architecture](../ceridwen-architecture/)
2. [SSP grids to CSPs](../ceridwen-ssp-csp/)
3. [Observations and SedModel](../ceridwen-observations-model/)

1. **`model.predict(theta)`**
2. **Apply transforms**Build named parameters
3. **CSP prediction**Create model spectrum
4. **Observation projection**Match measured spaces

<figure>
<figcaption>One sampled parameter point becomes one prediction for each observation.</figcaption>
</figure>

### Stage 5: Trace nested sampling and results

Read these pages after you understand one prediction:

1. [Likelihood and sampling](../ceridwen-likelihood-sampling/)
2. [Tests as documentation](../tests-as-documentation/)
3. [Vast.ai GPU workflow](../vast-ai-gpu-workflow/)
4. [Modal GPU workflow](../modal-gpu-workflow/)

1. **`run_sampler`**
2. **Prediction and likelihood**
3. **BlackJAX NSS adapter**
4. **SamplingResult**
5. **Checkpoint and HDF5**

<figure>
<figcaption>The sampler evaluates the model and returns restartable, saved output.</figcaption>
</figure>

Use [Python patterns](../python-patterns/) when you find an unfamiliar implementation pattern.
