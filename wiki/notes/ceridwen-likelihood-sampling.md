---
title: Ceridwen: likelihood and sampling
date: 2026-09-06
section: Codebase
theme: Model and code reference
tags: [ceridwen, blackjax, nested-sampling]
job:
old: _old/codebase/ceridwen-likelihood-sampling.html
---

This layer converts predictions into posterior density values. An external algorithm then explores these values.

<details>
<summary>Per-observation likelihood</summary>

A diagonal Gaussian compares four aligned arrays:

- **Data**`y`
- **Prediction**`mu`
- **Uncertainty**`sigma`
- **Mask**Boolean selection

</details>

<figure>
<figcaption>All four arrays align with the same observation coordinates.</figcaption>
</figure>

<details>
<summary>Details</summary>

The compiled kernel calculates aligned arrays before it applies the boolean mask. A false mask value removes a datum from the final sum. It does not shorten the arrays.

The spectra-only notebook therefore compacts the observation before model construction. Full mode has 3,523 likelihood pixels. Feature mode has 1,924. Each compact array also has two masked endpoints that preserve the native smoothing boundaries.

`notebooks/ceridwen_test_spectra.ipynb` · “Build the native-resolution spectrum” · `compact_indices` and `compact_likelihood_mask`

An optional `DiagonalNoiseModel` modifies the variance. It can add model-scaled fractional calibration error. It can also add data-scaled fractional error or additive jitter (`ceridwen/ceridwen/likelihood/noise_model.py:210-280`). Lines 283-365 contain the calculation. Both active fitting notebooks use `log_f_calib` for model-scaled spectral calibration uncertainty.

`ceridwen/ceridwen/likelihood/noise_model.py:324-350`

</details>

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

<details>
<summary>Details</summary>

Each enabled term adds a squared uncertainty to `var`. A model prediction, observed data, or absolute jitter can set the term's scale.

</details>


<details>
<summary>Calibration matrix</summary>

`ceridwen/ceridwen/likelihood/calibration.py:262-275 · _gram, normal_matrix`

```python
    def _gram(self, weights) -> Array:
        """``D^T D`` from the Chebyshev moments ``M_j = sum_i w_i T_j(x_i)``.

        ``T_m T_n = (T_{m+n} + T_{|m-n|}) / 2`` turns the ``(n_pix, k, k)``
        reduction into one ``(n_pix, 2k + 1)`` matvec, linear in the order.
        """
        moments = weights @ self.moment_basis
        return 0.5 * (moments[self.pair_plus] + moments[self.pair_minus])

    def normal_matrix(self, mu, sigma, mask) -> Array:
        """``D^T D + Sigma_p^{-1}`` -- the posterior precision of the coefficients."""
        normal = self._gram(self._weights(mu, sigma, mask))
        precision = self._precision()
        return normal if precision is None else normal + precision
```

</details>

<details>
<summary>Multiple observations</summary>

`MultiObservationLikelihood` stores matching tuples of observation keys and likelihood objects (`likelihood/likelihood.py:793-837`). Its call loops through these static pairs and sums their log-likelihoods (`lines 840-872`).

For the joint notebook:

- **Photometry likelihood**One scalar
- **Spectrum likelihood**One scalar

</details>

<figure>
<figcaption>Each observation keeps its own units before scalar likelihood values are added.</figcaption>
</figure>

<details>
<summary>Details</summary>

Different observation types can retain different units. Each residual is divided by an uncertainty with the same units. The code then adds the scalar log-likelihoods.

`ceridwen/ceridwen/likelihood/likelihood.py:866-872 · MultiObservationLikelihood.__call__`

</details>

```
lnl_total = jnp.zeros(())
aux: dict[str, LikelihoodOutput] = {}
for key, lhood in zip(self.keys, self.likelihoods):
    lnl_i, aux_i = lhood(y[key], mu[key], sigma_obs[key], mask[key], params)
    lnl_total    = lnl_total + lnl_i
    aux[key]     = aux_i
return lnl_total, aux`
```

<details>
<summary>Details</summary>

The method docstring returns the sum and a diagnostic object for each observation (`ceridwen/ceridwen/likelihood/likelihood.py:848-865`).

The same key selects the data, prediction, uncertainty, and mask. Each observation type returns one scalar contribution. The function sums these contributions.

</details>

<details>
<summary>Prior</summary>

`SedModel.ln_prior` loops through the registered priors. It sums `prior.logpdf` for each free parameter (`model/model.py:408-447`). A parameter that is absent from the prior dictionary contributes zero.

</details>

<details>
<summary>Sampler boundary</summary>

`run_sampler` extracts static observation arrays. It then creates two JIT functions:

- `loglike_fn(theta)` predicts the data and sums the data likelihoods.
- `logprior_fn(theta)` calls `model.ln_prior`.

It sends both functions and `model.theta_init` to a `SamplerAdapter` (`sampler/runner.py:275-366`). Separate functions support both MCMC and nested sampling.

`ceridwen/ceridwen/sampler/runner.py:335-366`

</details>

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

<details>
<summary>Details</summary>

The code captures the data once outside the compiled closures. The adapter receives two functions and an initial parameter tree. It does not require the Ceridwen observation classes.

</details>

<details>
<summary>Inactive NUTS implementation</summary>

The package includes this adapter, but the project does not use it. All current Ceridwen fits use BlackJAX nested sampling.

`BlackJAXNUTSAdapter` performs these steps:

1. It flattens the parameter dictionary (`sampler/nuts.py:308-324`).
2. It maps bounded parameters to unconstrained coordinates.
3. It adds the transformation Jacobian to the posterior (`lines 395-422`).
4. It adapts the step size and mass matrix during warmup (`lines 426-468`).
5. It runs compiled NUTS chains from line 470.
6. It reconstructs named posterior arrays in `SamplingResult`.

The unconstrained transformation prevents hard uniform boundaries from becoming geometric walls for Hamiltonian trajectories.

</details>

<details>
<summary>Nested-sampling path</summary>

`BlackJAXNestedSamplerAdapter` requires a proper prior for every free parameter. It draws the initial live ensemble directly from these priors (`sampler/nested.py:156-190`). It then runs the BlackJAX nested slice sampler with separate likelihood and prior functions.

The defaults use 500 live points and five inner steps for each dimension. Each iteration deletes one-fifth of the live points. The default `logZ_tol` is `-5` (`sampler/nested.py:144-172` and `350-359`).

`BlackJAXNestedSamplerAdapter` defaults to `slice_kernel='lanes'` (Dance et al., 2025, arXiv:2503.17405). `lane_update` runs each replaced particle’s slice chain as one lane in one `lax.while_loop`. Each round evaluates one batch of `num_delete` candidates: one left edge, right edge or shrink proposal per running lane. `'carry'` retains the BlackJAX kernel with `stepping_out_carry`, testing each new edge once. `'stock'` selects unchanged `blackjax.nss`.

A candidate with prior below the slice level is outside the slice regardless of likelihood. Each round, a lane advances past up to `free_moves=8` such candidates and stored results outside the slice without a likelihood call. One pass computes each lane’s next `free_moves + lookahead` candidates, assuming earlier candidates are outside, and evaluates their priors as one batch. Finished lanes’ batch slots evaluate running lanes’ next candidates, up to `lookahead - 1 = 3` per lane. Results are stored per lane and reused when slice step, `t` and position match bitwise. A stored result inside the slice also triggers evaluation of that lane’s next candidate in the same round. The batch remains `num_delete`: on CPU, a row’s log-likelihood bits depend on batch size.

CPU samples, evidence and call counts are bitwise equal to `blackjax.nss` (`tests/test_nss_diagnostics.py`). On RTX 5090, lanes and carry differ only through float32 rounding in `_T @ spectrum`, the photometry product. M1_210210 sampling: carry 253.2 s, lanes 108.7 s. With the rules above, iterations 20 and 140 take 156 and 245 rounds, versus 376 and 427 without them (`ceridwen a60f1f8`). On the same RTX 5090 rental, sampling falls from 180.4 s to 108.0 s and `BlackJAXNestedSamplerAdapter.run` from 183.1 s to 111.2 s. Dead points and samples remain bitwise equal (`results/speedups-swarm-sampler-2026-10-01/session2`).

`ceridwen/ceridwen/sampler/nested.py:330-337 · lane_update`

```python
            # Move past candidates below the prior level (outside the slice
            # whatever their likelihood) and stored ones outside the slice,
            # up to free_moves of them, within the slice step.
            free = (~(logprior >= level) | (hit & ~found_inside)) & ~ends
            m = jnp.argmin(free & (jnp.arange(depth) < free_moves), axis=1)
            at = lambda tree: jax.tree.map(lambda v: v[lanes, m], tree)  # noqa: E731
            s, now_t, now_x, now_hit, now_found, now_inside = at(
                (states, t, x, hit, found, found_inside))
```

`ceridwen/ceridwen/sampler/nested.py:819-829 · _logical_likelihood_calls`

```python
    @staticmethod
    def _logical_likelihood_calls(info):
        """Per-particle evaluations for the pinned stepping-out slice kernel.

        Each expansion loop evaluates its terminating condition once more
        than its body runs. The two endpoints therefore add two calls per
        slice. This counts logical evaluations, not redundant GPU lanes in
        a vectorized while loop.
        """
        return jnp.sum(info.update_info.num_expansions
                       + info.update_info.num_shrink + 2)
```

1. **Draw from priors**Initial live points
2. **Evaluate likelihood**Score every point
3. **Replace points**Apply likelihood constraint
4. **Accumulate dead points**Evidence and weights
5. **Build SamplingResult**Posterior output

</details>

<figure>
<figcaption>BlackJAX NSS turns prior draws into weighted posterior samples and evidence.</figcaption>
</figure>

<details>
<summary>Details</summary>

`ceridwen/ceridwen/sampler/nested.py:883-892 · BlackJAXNestedSamplerAdapter.run`

</details>

```
rng_key, prior_key = jax.random.split(rng_key)
particles = self._sample_prior(theta_init, prior_key)

# ── Build NSS kernel ──────────────────────────────────────────────
# loglike_fn / logprior_fn operate on a SINGLE particle (un-batched).
# The NSS step_fn vmaps internally over the live-point ensemble.
nested_sampler = self._build_nested_sampler(
    loglike_fn, logprior_fn, num_inner_steps, num_delete)
init_fn = jax.jit(nested_sampler.init)
step_fn = jax.jit(nested_sampler.step)
```

<details>
<summary>Details</summary>

The adapter docstring requires a proper prior for every free parameter and defines live-point sampling (`ceridwen/ceridwen/sampler/nested.py:88-142`).

`anesthetic` calculates evidence and importance weights for the completed dead points (`sampler/nested.py:502-529`). Normalize or resample these weights before you calculate posterior percentiles, predictive draws, or derived SFHs.

</details>

<details>
<summary>Checkpoints</summary>

The nested adapter can write an atomic partial posterior every 20 minutes. Each checkpoint contains finalized positions, likelihoods, birth likelihoods, evidence, and the number of dead points (`sampler/nested.py:226-315`, `438-501`).

</details>

<details>
<summary>Result</summary>

`SamplingResult` stores named posterior samples, log likelihoods, available evidence, diagnostics, timings, and backend-specific raw output (`sampler/runner.py:69-128`). The inactive NUTS adapter returns equal-weight samples without Bayesian evidence. Nested sampling returns weighted dead points, evidence, and evidence uncertainty. The active notebooks convert these points to deterministic equal-weight posterior draws before they calculate later summaries.

The active notebooks write the final result with `write_result_h5`. They load it again with `load_result_h5`. They then check the parameter names and likelihood shape (`fit.py:369-621`).

</details>

<details>
<summary>High-level `fitSED`</summary>

`fitSED` creates default diagonal likelihoods and a sampler adapter. It calls `run_sampler`. It then writes HDF5 and a text log (`fit.py:148-282`). The project notebooks use the lower-level route because they customize the likelihoods.

</details>
