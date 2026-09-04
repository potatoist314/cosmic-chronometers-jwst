---
title: Ceridwen architecture
date: 2026-08-25
section: Codebase
tags: [ceridwen]
job: 
old: _old/codebase/ceridwen-architecture.html
---

Ceridwen is a JAX-native stellar-population forward model and Bayesian fitting package. The package root exports `SSPData`, `CSPBasis`, `SedModel`, configurable cosmology, and `fitSED` (`ceridwen/ceridwen/__init__.py:31-89`).

### Package map

**Physical model**

`ssps/`, `csp/`, dust, nebular, IGM, and cosmology.

**Measured space**

`observation/` stores data and projects model spectra.

**Inference**

`model/`, `likelihood/`, `sampler/`, and `fit.py`.

<figure>
<figcaption>Three package layers connect physical spectra to sampled results.</figcaption>
</figure>

- The `ssps/` package loads, generates, checks, and fetches SSP grids.
- The `csp/` package combines SSP spectra into a galaxy spectrum.
- The `dust/`, `neb/`, and `igm.py` modules provide optional physical components.
- The `observation/` package stores measured data and projects models into data space.
- The `model/` package manages parameters, transforms, priors, and predictions.
- The `likelihood/` package defines noise models and compares data with models.
- The `sampler/` package defines priors and adapters. The active project path uses BlackJAX nested sampling.
- `cosmology.py` calculates differentiable distances, ages, and flux factors.
- `fit.py` controls high-level fits and saves results.

The package `__init__.py` files show the intended public interface. Read these files before you inspect the implementation modules.

### End-to-end call graph

- **SSPData and CSPBasis**Grid and physical model
- **Observations**Prepared data projections
- **Priors and transforms**Parameter definition

1. **SedModel**Named parameters
2. **Prediction**CSP and projections
3. **Likelihood and prior**Two scalar functions
4. **BlackJAX NSS**Adapter run
5. **Saved result**Checkpoints and HDF5

<figure>
<figcaption>Static components form a model before nested sampling evaluates changing parameters.</figcaption>
</figure>

### Fit paths

`fitSED` provides the high-level route. It creates default diagonal likelihoods and selects a sampler adapter. It runs the sampler, writes HDF5, and logs the configuration and timings (`ceridwen/ceridwen/fit.py:67-282`).

`run_sampler` provides the lower-level route. The notebooks use this route to create custom `MultiObservationLikelihood` and `DiagonalNoiseModel` objects (`ceridwen/ceridwen/sampler/runner.py:275-366`).

### Static versus sampled state

**Static structure**

Grid axes, observation types, projection matrices, physics switches, and likelihood layout.

**Sampled state**

Free parameters, derived parameters, predictions, likelihood values, and prior values.

<figure>
<figcaption>JAX compiles the fixed structure and evaluates new sampled values.</figcaption>
</figure>

These values stay static after model construction:

- The SSP grid axes and flux cube stay static.
- The SFH grid length and observation types stay static.
- The filter curves, pixel wavelengths, and projection matrices stay static.
- The enabled physics components and likelihood structure stay static.

These values change at each sampler step:

- The free parameter arrays in `theta` change.
- The transforms calculate new derived parameter values.
- The spectrum, projected predictions, likelihood, and prior values change.

The static structure lets JAX compile one numerical graph. A change to shapes, observation types, or dictionary keys usually requires a new trace.

### Examples

`ceridwen/ceridwen/__init__.py:40-42`

```
from .ssps import SSPData
from .csp import CSPBasis
from .model import SedModel`
```

The package root exports the three construction layers. Start with these names. Then follow each relative import to the module that defines the name.

`ceridwen/ceridwen/model/model.py:337-342 · SedModel.apply_transforms`

```
if not self.transforms:
    return free_theta
model_theta = dict(free_theta)
for derived_param, fn in self.transforms.items():
    model_theta[derived_param] = fn(free_theta)
return model_theta`
```

**Documented contract:** The method docstring says the result keeps free parameters and adds every derived value (`ceridwen/ceridwen/model/model.py:313-336`).

**Why it matters:** Each transform adds a derived value to a copy. The free sampler parameters remain in the copy. The transform calculates keys such as `sfh` before the CSP receives the dictionary.

`ceridwen/ceridwen/model/model.py:395-401 · SedModel.predict`

```
if self._zred_fixed is not None and "zred" not in model_theta:
    if model_theta is theta:          # apply_transforms may not copy
        model_theta = dict(model_theta)
    model_theta["zred"] = self._zred_fixed
# Mass scaling is handled inside csp.predict() — the spectrum is
# scaled once before projection, rather than per-observation.
return self.csp.predict(model_theta, self.observations)`
```

**Documented contract:** The method docstring returns one prediction array for each observation name (`ceridwen/ceridwen/model/model.py:348-383`).

**Why it matters:** `SedModel` first completes the parameter bookkeeping. It then sends the physical prediction and observation projection to the CSP.
