---
title: Tests as documentation
date: 2026-08-25
section: Codebase
tags: [tests]
job: 
old: _old/codebase/tests-as-documentation.html
---

Tests show which behavior the maintainers treat as a contract. Each test places its inputs and expected outputs together. This structure can make tests easier to read than long implementation files.

The root Astro project currently has no project-owned `tests/` directory. Ceridwen contains focused unit tests, misuse tests, regression tests, and grid-dependent tests.

- **Construction tests**Shapes and parameter modes
- **Projection tests**Units and limiting cases
- **Sampler tests**Checkpoints and output
- **Regression tests**Preserved physical behavior

<figure>
<figcaption>Each test family records a different Ceridwen contract.</figcaption>
</figure>

### Test map

#### Constructing a CSP

Read `ceridwen/tests/test_csp_construction.py` with `ceridwen/ceridwen/csp/csp.py:544-732`.

The test demonstrates these behaviors:

- The `lookback_time=` argument provides a shortcut.
- Node-based and per-bin SFHs use different shapes.
- Metallicity can be constant or time-varying.
- Missing structures and one-node grids cause errors.

#### Predictive observations

Read `ceridwen/tests/test_observation_predictive.py` with `observation/base.py:189-202` and `observation/spectrum.py:368-437`.

The test shows that a spectrum without flux can retain its wavelength grid. It can also prepare a projection and generate model values.

#### SSP provenance

Read `ceridwen/tests/test_ssp_provenance.py` with `ssps/ssp_data.py`.

The test covers HDF5 metadata round trips and strict schema-2.x loading. It also checks required resolution curves and prohibited FSPS parameters. It checks automatic transfer of isochrone data into the CSP.

#### Redshift-dependent ages

Read `ceridwen/tests/test_zred_age_tracking.py` with `csp/csp.py:1817-1842`.

These tests check that the oldest SFH bin tracks the age of the universe. They check that the spectrum changes and gradients pass through redshift. They also check that the fixed-redshift path stays unchanged.

#### Observation projection and noise

- `test_spectrum_fixes.py` checks LSF input resolution, FWHM and sigma conventions, calibration, and line masking.
- `test_lines_static.py` checks the static line-projection matrix and JIT behavior.
- `test_line_projection_continuum.py` checks continuum-subtracted nebular lines.
- `test_upper_limit_likelihood.py` checks detections, upper limits, and gradients.
- `test_losvd_no_lyman_spike.py` checks a boundary regression in FFT smoothing.

#### v0.2.2 contracts

- `test_spectrum_scaling.py` checks analytic spectrum scaling and fixed-scaling behavior.
- `test_cosmology_configurable.py` checks configurable cosmology, distances, ages, and gradients.
- `test_ns_checkpoint.py` checks periodic snapshots, disabled checkpoints, and checkpoint loading.

#### Physical invariants and misuse

`ceridwen/tests/regression/test_misuse.py` checks shared units across SSP weight calculations and finite zero-SFR behavior. It also checks emission-line scaling semantics and unknown parameter keys. `tests/csp/test_lookback_flip_invariant.py` checks that time-order conventions do not change the physics silently.

### Examples

`ceridwen/tests/test_csp_construction.py:48-61 · test_shortcut_matches_full_theta_structure`

```
def test_shortcut_matches_full_theta_structure(ssp):
    lb = jnp.linspace(0.0, 12.0, 6)
    via_theta = CSPBasis(
        ssp, theta={"lookback_time": lb, "sfh": jnp.ones(6),
                    "Z": jnp.array([-1.85])}, **KW)
    via_shortcut = CSPBasis(ssp, lookback_time=lb, **KW)

    np.testing.assert_allclose(np.asarray(via_shortcut.sfh_times),
                               np.asarray(via_theta.sfh_times))
    assert via_shortcut.n_time == via_theta.n_time == 6
    assert via_shortcut.sfh_per_bin is False
    assert via_shortcut.zh_is_scalar is True          # zh_const -> 'Z' mode
    # Neutral initial Z must lie inside the grid: no clamp messages.
    assert via_shortcut.check_param_ranges(warn=False) == []`
```

**Documented contract:** The test requires both construction routes to produce the same time grid and parameter modes (`ceridwen/tests/test_csp_construction.py:48-61`).

**Why it matters:** Two construction routes receive equivalent inputs. Each assertion checks one part of that equivalence. These parts are the grid, node count, SFH representation, metallicity mode, and range validity.

`ceridwen/tests/test_observation_predictive.py:35-47 · test_fluxless_spectrum_setup_and_predict`

```
def test_fluxless_spectrum_setup_and_predict():
    wave_obs = np.linspace(4000.0, 8000.0, 50)
    spec = Spectrum(wavelength=wave_obs, name="predictive")

    wave_model = np.linspace(1000.0, 20000.0, 500)   # rest frame
    zred = 0.1
    spec.setup_for_model(wave_model, zred=zred)

    # A flat unit model spectrum must project to ~1 on every pixel
    # (pure linear interpolation of a constant).
    pred = spec.predict(jnp.ones(wave_model.size), wave_model)
    assert pred.shape == (wave_obs.size,)
    np.testing.assert_allclose(np.asarray(pred), 1.0, rtol=1e-6)`
```

**Documented contract:** The test requires a fluxless Spectrum to project a constant model without changing its value (`ceridwen/tests/test_observation_predictive.py:35-47`).

**Why it matters:** The constant spectrum is a limiting case with a known answer. The test checks the output shape and the numerical invariant.
