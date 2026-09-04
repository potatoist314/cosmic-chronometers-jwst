---
title: Ceridwen project overview
date: 2026-09-01
section: Guides
tags: [ceridwen, overview]
job: 
old: _old/overview.html
---

Ceridwen is the project’s primary stellar-population inference path. The active notebooks fit LEGA-C spectra and photometry. The longer-term goal is age-based cosmology with massive quiescent galaxies.

### Project flow

- **LEGA-C spectra**Flux and uncertainty
- **COSMOS photometry**Matched broadband flux
- **SSP grid**Population spectra

1. **Observations**Spectrum and Photometry
2. **SedModel**Forward prediction
3. **BlackJAX NSS**Posterior search
4. **Saved output**Checkpoints and HDF5

<figure>
<figcaption>Measured data and an SSP grid become a saved Ceridwen result.</figcaption>
</figure>

The current workflow has these boundaries:

- Ceridwen infers stellar-population parameters from spectra and photometry.
- BlackJAX nested sampling explores the configured posterior.
- Earlier inference branches remain only as historical code and records.
- A downstream notebook now audits Borghi-style differential ages, exact-object age-source changes, selection sensitivity, and population drift. Its Ceridwen age ceiling inherits an assumed cosmology, so it is not an independent chronometer measurement.

### Ceridwen flow

1. **SSPData**Stellar grid
2. **CSPBasis**Composite spectrum
3. **Observations**Data projection
4. **SedModel**Parameters
5. **Likelihood**Fit score
6. **SamplingResult**Posterior output

<figure>
<figcaption>Ceridwen builds a prediction, scores it, and stores the sampled posterior.</figcaption>
</figure>

- The SSP grid supplies spectra for a range of ages and compositions.
- The CSP combines the spectra with an SFH and a metallicity history.
- Each observation projects one model spectrum into measured data space.
- `SedModel` manages parameters, transforms, priors, and predictions.
- The likelihood compares each prediction with the data.
- An adapter runs the sampler.

### Ceridwen exports

`ceridwen/ceridwen/__init__.py:40-42`

```
from .ssps import SSPData
from .csp import CSPBasis
from .model import SedModel`
```

The package exports `SSPData`, `CSPBasis`, and `SedModel` in forward-model order.

### Reading order

First, read [Reading order](../reading-order/). Then read [Project map](../project-map/). For the current Ceridwen work, continue with [Ceridwen architecture](../ceridwen-architecture/). Consult [Python patterns](../python-patterns/) when you find an unfamiliar Python pattern.
