---
title: Python patterns
date: 2026-08-25
section: Guides
tags: [python, jax]
job: 
old: _old/guides/python-patterns.html
---

### Function

A function converts inputs into outputs. First, read its signature. Then find its `return` statements. After that, inspect the intermediate lines.

- `ceridwen/ceridwen/model/model.py:313-342`, `apply_transforms(theta)` returns a parameter dictionary.
- `ceridwen/ceridwen/model/model.py:348-401`, `predict(theta)` returns a dict.
- `ceridwen/ceridwen/sampler/runner.py:275-366`, `run_sampler(...)` returns a `SamplingResult`.

These return values follow the active Ceridwen prediction and sampling path.

### Dataclass

A dataclass defines a data record. It can store results without implementing the algorithm that produced them.

- `ceridwen/ceridwen/sampler/runner.py:69-128`: `SamplingResult` stores output.

The field names define the object’s data contract. Search for class construction to find the producing algorithm.

`ceridwen/ceridwen/sampler/runner.py:69-76 · SamplingResult`

```
@dataclass
class SamplingResult:
    """
    Universal container for the output of any Ceridwen sampling run.

    All fields are backend-agnostic.  The sampler-specific raw output
    (e.g. a BlackJAX ``dead`` pytree) is preserved in ``raw`` for
    downstream processing.`
```

**Documented contract:** The class docstring defines backend-independent samples, evidence, weights, diagnostics, and raw output (`ceridwen/ceridwen/sampler/runner.py:69-116`).

**Why it matters:** All Ceridwen samplers return this container. Lines 118-128 define the posterior, evidence, diagnostics, timing, and raw-output fields.

### Closure

A closure is an inner function that retains variables from its outer function. `Spectrum.setup_for_model` stores a projection closure in `_predict_fn` (`ceridwen/ceridwen/observation/spectrum.py:663-667`).

`ceridwen/ceridwen/observation/spectrum.py:663-667`

```
_L = _apply_losvd
self._predict_fn = (
    lambda spec, _A=_apply_instr, _L=_L:
        _A(_L(spec[_idx]))
)`
```

The lambda retains the prepared smoothing operation and pixel selection. Later predictions supply only the model spectrum.

### Class and inheritance

Inheritance defines a specialized form of another class. `Photometry`, `Spectrum`, and `Lines` inherit storage and masking from `Observation`. Each class implements its own projection:

- Base contract: `ceridwen/ceridwen/observation/base.py:25-89`.
- Abstract-style `predict`: `base.py:291-319`.
- Photometry implementation: `photometry.py:245-267`.
- Spectrum implementation: `spectrum.py:686-750`.

Compare the same method in the parent class and each child class.

- **Photometry**Filter projection
- **Spectrum**Resolution and pixels
- **Lines**Line measurements

<figure>
<figcaption>Each observation type shares one contract and defines its own projection.</figcaption>
</figure>

### Composition

Composition means that one object contains other objects. `SedModel` contains a CSP, observations, priors, and transforms. It does not inherit their code (`ceridwen/ceridwen/model/model.py:141-167`). Ceridwen uses this design to combine different observation types.

### Adapter

An adapter gives different external libraries a common interface. `SamplerAdapter.run(...)` defines the protocol. The sampler classes implement this protocol. The active project path uses the nested-sampling class (`ceridwen/ceridwen/sampler/runner.py:215-268`).

`run_sampler` uses the protocol. It does not use the internal BlackJAX API (`runner.py:275-366`).

### Decorator

A decorator changes function execution but keeps the function callable.

- `@jax.jit` compiles a numerical function: `runner.py:349-363`.
- `@classmethod` passes the class as `cls`: `ssp_data.py:508-566`.
- `@property` exposes a method like an attribute: `base.py:234-259`.

Read the decorator before you read the function. The decorator changes execution.

The JAX example below shows how `@jax.jit` changes a likelihood function.

### Module exports

An `__init__.py` file defines public names. For example, `ceridwen/ceridwen/ssps/__init__.py:7-18` exports grid containers and fetch helpers. Start with that file. Then open the module that defines each name.

### JAX static versus traced values

This distinction explains much of the Ceridwen structure:

- **Static Python values**Shapes, keys, and observation types
- **Traced JAX arrays**Sampled numerical parameters

<figure>
<figcaption>Python fixes the computation shape before JAX evaluates sampled values.</figcaption>
</figure>

- Static Python values define shapes, object types, and observation lists.
- Traced JAX arrays contain parameter values that change during sampling.
- JAX resolves static branches once during compilation.
- Python cannot use a traced numerical value to select a branch.

Examples:

- Observation setup precomputes matrices before JIT: `ceridwen/ceridwen/model/model.py:219-240`.
- The observation loop becomes compiled operations: `ceridwen/ceridwen/csp/csp_afe.py:1114-1134`.
- `theta` arrays remain differentiable inside prediction: `ceridwen/ceridwen/model/model.py:348-401`.

`ceridwen/ceridwen/sampler/runner.py:348-358 · run_sampler.loglike_fn`

```
# ── Log-likelihood: sum over observations, no prior ───────────────────
@jax.jit
def loglike_fn(theta: dict[str, Array]) -> Array:
    predictions = model.predict(theta)
    lnl = jnp.zeros(())
    for key, lhood in zip(_keys, _likelihoods):
        y_k, sig_k, mask_k = _static_data[key]
        mu_k    = predictions[key]
        lnl_k, _ = lhood(y_k, mu_k, sig_k, mask_k, params=theta)
        lnl = lnl + lnl_k
    return lnl`
```

**Documented contract:** The parent docstring says this compiled function sums observation likelihoods without a prior term (`ceridwen/ceridwen/sampler/runner.py:275-310`).

**Why it matters:** `theta` contains traced numerical data. The code creates `_keys` and `_likelihoods` outside this function. JAX therefore sees a fixed loop structure. A different observation list usually requires new compilation.
