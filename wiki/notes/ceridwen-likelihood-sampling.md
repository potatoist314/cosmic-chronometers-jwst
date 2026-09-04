---
title: Ceridwen: likelihood and sampling
date: 2026-09-01
section: Codebase
tags: [ceridwen, blackjax, nested-sampling]
job: 
old: _old/codebase/ceridwen-likelihood-sampling.html
---

This layer converts predictions into posterior density values. An external algorithm then explores these values.

### Per-observation likelihood

A diagonal Gaussian compares four aligned arrays:

- **Data**`y`
- **Prediction**`mu`
- **Uncertainty**`sigma`
- **Mask**Boolean selection

<figure>
<figcaption>All four arrays align with the same observation coordinates.</figcaption>
</figure>

The compiled kernel calculates aligned arrays before it applies the boolean mask. A false mask value removes a datum from the final sum. It does not shorten the arrays.

The spectra-only notebook therefore compacts the observation before model construction. Full mode has 3,523 likelihood pixels. Feature mode has 1,924. Each compact array also has two masked endpoints that preserve the native smoothing boundaries.

`notebooks/ceridwen_test_spectra.ipynb` · “Build the native-resolution spectrum” · `compact_indices` and `compact_likelihood_mask`

An optional `DiagonalNoiseModel` modifies the variance. It can add model-scaled fractional calibration error. It can also add data-scaled fractional error or additive jitter (`ceridwen/ceridwen/likelihood/noise_model.py:210-280`). Lines 283-365 contain the calculation. Both active fitting notebooks use `log_f_calib` for model-scaled spectral calibration uncertainty.

`ceridwen/ceridwen/likelihood/noise_model.py:324-350`

```
# Start with observational variance.
var: Array = sigma_obs ** 2

# Model-anchored fractional calibration error: sigma = f_calib * |mu|.
# Gradient flows through mu -> var -> inv_var -> lnl cleanly.
if self.use_fractional:
    f_calib = jnp.exp(params["log_f_calib"])
    var = var + (f_calib * jnp.abs(mu)) ** 2

# Data-anchored fractional systematic floor: sigma = f_data * |y|.
# Scales with the *observed* flux, so the variance does not depend on
# theta (no Eddington-type bias).  The natural form for pure zero-point
# uncertainties.  Requires the observed data to be passed explicitly.
if self.use_data_fractional:
    if data is None:
        raise ValueError(
            "DiagonalNoiseModel(use_data_fractional=True) requires the "
            "observed data array; call compute(..., data=y)."
        )
    f_data = jnp.exp(params["log_f_data"])
    var = var + (f_data * jnp.abs(data)) ** 2

# Additive noise floor (jitter).
# Parameterised as log_jitter so sampling is unconstrained.
if self.use_jitter:
    jitter = jnp.exp(params["log_jitter"])
    var = var + jitter ** 2`
```

Each enabled term adds a squared uncertainty to `var`. A model prediction, observed data, or absolute jitter can set the term's scale.

### Multiple observations

`MultiObservationLikelihood` stores matching tuples of observation keys and likelihood objects (`likelihood/likelihood.py:793-837`). Its call loops through these static pairs and sums their log-likelihoods (`lines 840-872`).

For the joint notebook:

- **Photometry likelihood**One scalar
- **Spectrum likelihood**One scalar

<figure>
<figcaption>Each observation keeps its own units before scalar likelihood values are added.</figcaption>
</figure>

Different observation types can retain different units. Each residual is divided by an uncertainty with the same units. The code then adds the scalar log-likelihoods.

`ceridwen/ceridwen/likelihood/likelihood.py:866-872 · MultiObservationLikelihood.__call__`

```
lnl_total = jnp.zeros(())
aux: dict[str, LikelihoodOutput] = {}
for key, lhood in zip(self.keys, self.likelihoods):
    lnl_i, aux_i = lhood(y[key], mu[key], sigma_obs[key], mask[key], params)
    lnl_total    = lnl_total + lnl_i
    aux[key]     = aux_i
return lnl_total, aux`
```

**Documented contract:** The method docstring returns the sum and a diagnostic object for each observation (`ceridwen/ceridwen/likelihood/likelihood.py:848-865`).

**Why it matters:** The same key selects the data, prediction, uncertainty, and mask. Each observation type returns one scalar contribution. The function sums these contributions.

### Prior

`SedModel.ln_prior` loops through the registered priors. It sums `prior.logpdf` for each free parameter (`model/model.py:408-447`). A parameter that is absent from the prior dictionary contributes zero. The model configuration must select this behavior intentionally.

### Sampler boundary

`run_sampler` extracts static observation arrays. It then creates two JIT functions:

- `loglike_fn(theta)` predicts the data and sums the data likelihoods.
- `logprior_fn(theta)` calls `model.ln_prior`.

It sends both functions and `model.theta_init` to a `SamplerAdapter` (`sampler/runner.py:275-366`). Separate functions support both MCMC and nested sampling.

`ceridwen/ceridwen/sampler/runner.py:335-366`

```
# ── Static data extracted once, before trace ──────────────────────────
_obs_dict    = model.obs_dict
_keys        = tuple(likelihood.keys)
_likelihoods = tuple(likelihood.likelihoods)
_static_data = {
    key: (
        _obs_dict[key].flux,
        _obs_dict[key].uncertainty,
        _obs_dict[key].mask,
    )
    for key in _keys
}

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
    return lnl

# ── Log-prior ─────────────────────────────────────────────────────────
@jax.jit
def logprior_fn(theta: dict[str, Array]) -> Array:
    return model.ln_prior(theta)

# ── Delegate ──────────────────────────────────────────────────────────
return adapter.run(loglike_fn, logprior_fn, model.theta_init, rng_key)`
```

The code captures the data once outside the compiled closures. The adapter receives two functions and an initial parameter tree. It does not require the Ceridwen observation classes.

### Inactive NUTS implementation

The package includes this adapter, but the project does not use it. All current Ceridwen fits use BlackJAX nested sampling.

`BlackJAXNUTSAdapter` performs these steps:

1. It flattens the parameter dictionary (`sampler/nuts.py:308-324`).
2. It maps bounded parameters to unconstrained coordinates.
3. It adds the transformation Jacobian to the posterior (`lines 395-422`).
4. It adapts the step size and mass matrix during warmup (`lines 426-468`).
5. It runs compiled NUTS chains from line 470.
6. It reconstructs named posterior arrays in `SamplingResult`.

The unconstrained transformation prevents hard uniform boundaries from becoming geometric walls for Hamiltonian trajectories.

### Nested-sampling path

`BlackJAXNestedSamplerAdapter` requires a proper prior for every free parameter. It draws the initial live ensemble directly from these priors (`sampler/nested.py:156-190`). It then runs the BlackJAX nested slice sampler with separate likelihood and prior functions.

The defaults use 500 live points and five inner steps for each dimension. Each iteration deletes one-fifth of the live points. The default `logZ_tol` is `-5` (`sampler/nested.py:144-172` and `350-359`).

The run loop reads `logZ` and `logZ_live` from the device once per iteration and reuses the two floats for the stop condition, the verbose line, the progress bar, and the checkpoint tag. Each read is a blocking device transfer, and earlier revisions performed up to seven of them per iteration.

1. **Draw from priors**Initial live points
2. **Evaluate likelihood**Score every point
3. **Replace points**Apply likelihood constraint
4. **Accumulate dead points**Evidence and weights
5. **Build SamplingResult**Posterior output

<figure>
<figcaption>BlackJAX NSS turns prior draws into weighted posterior samples and evidence.</figcaption>
</figure>

`ceridwen/ceridwen/sampler/nested.py:369-382 · BlackJAXNestedSamplerAdapter.run`

```
rng_key, prior_key = jax.random.split(rng_key)
particles = self._sample_prior(theta_init, prior_key)

# ── Build NSS kernel ──────────────────────────────────────────────
# loglike_fn / logprior_fn operate on a SINGLE particle (un-batched).
# The NSS step_fn vmaps internally over the live-point ensemble.
nested_sampler = blackjax.nss(
    logprior_fn      = logprior_fn,
    loglikelihood_fn = loglike_fn,
    num_delete       = num_delete,
    num_inner_steps  = num_inner_steps,
)
init_fn = jax.jit(nested_sampler.init)
step_fn = jax.jit(nested_sampler.step)`
```

**Documented contract:** The adapter docstring requires a proper prior for every free parameter and defines live-point sampling (`ceridwen/ceridwen/sampler/nested.py:88-142`).

**Why it matters:** `anesthetic` calculates evidence and importance weights for the completed dead points (`sampler/nested.py:502-529`). Normalize or resample these weights before you calculate posterior percentiles, predictive draws, or derived SFHs.

### Checkpoints

The nested adapter can write an atomic partial posterior every 20 minutes. Each checkpoint contains finalized positions, likelihoods, birth likelihoods, evidence, and the number of dead points (`sampler/nested.py:226-315`, `438-501`).

### Result

`SamplingResult` stores named posterior samples, log likelihoods, available evidence, diagnostics, timings, and backend-specific raw output (`sampler/runner.py:69-128`). The inactive NUTS adapter returns equal-weight samples without Bayesian evidence. Nested sampling returns weighted dead points, evidence, and evidence uncertainty. The active notebooks convert these points to deterministic equal-weight posterior draws before they calculate later summaries.

The active notebooks write the final result with `write_result_h5`. They load it again with `load_result_h5`. They then check the parameter names and likelihood shape (`fit.py:369-621`).

### High-level `fitSED`

`fitSED` creates default diagonal likelihoods and a sampler adapter. It calls `run_sampler`. It then writes HDF5 and a text log (`fit.py:148-282`). The project notebooks use the lower-level route because they customize the likelihoods.
