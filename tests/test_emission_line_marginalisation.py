"""Emission-line marginalisation option of the fit notebook, on M1_210210.

Builds the notebook's model and likelihood (cells 2, 4, 6, 8 and the
likelihood lines of cell 10) on CPU and evaluates them at 20 posterior draws
of the reference fit.  Skips when the local grid, data or $SPS_HOME is absent.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# The notebook sets JAX_ENABLE_X64 before its imports; ceridwen imported without it keeps
# float32 module constants and shifts lnL by ~6e-5.
os.environ["JAX_ENABLE_X64"] = "1"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
REFERENCE = PROJECT_ROOT / "results/m1-210210-reference/tau-1/poly10/210210-M1_210210/ceridwen_result.h5"
SPS_HOME = PROJECT_ROOT / "external/fsps"
# Posterior rows (weighted draw, seed 20260922) and their joint log-likelihood from the
# code before the option existed (ceridwen 5f2c316, project dfa01ba), on this Mac's CPU.
DRAWS = [23073, 23886, 24301, 24532, 24534, 24551, 24698, 24862, 24990, 25377,
         25545, 25660, 25986, 26338, 26459, 26478, 26729, 26752, 28072, 28929]
BASELINE = [
    "0x1.c38d08ab1212cp+17", "0x1.c38c516aa2931p+17", "0x1.c38facfad7ce0p+17",
    "0x1.c38fb5f4412a9p+17", "0x1.c38f69243e3d5p+17", "0x1.c38f1c125d3cbp+17",
    "0x1.c39013beb9aeep+17", "0x1.c38b5d3729bbfp+17", "0x1.c3908f3d7743ap+17",
    "0x1.c38e073bfc202p+17", "0x1.c390055742a52p+17", "0x1.c39168dbeba74p+17",
    "0x1.c39126a3244fdp+17", "0x1.c390a81a6de26p+17", "0x1.c39168ab5e4c0p+17",
    "0x1.c392804c5a0a6p+17", "0x1.c390a910fc0eep+17", "0x1.c3925db0e83d0p+17",
    "0x1.c393454f2ae25p+17", "0x1.c390fdc3e2883p+17",
]

pytestmark = pytest.mark.skipif(
    not (REFERENCE.exists() and (Path.home() / ".ceridwen/grids/amist_c3k_hr_krou_afe.h5").exists()
         and (SPS_HOME / "data/emlines_info.dat").exists()),
    reason="needs the M1_210210 reference fit, the HR alpha grid and FSPS emlines_info.dat",
)


def _build(emission_line_marginalisation):
    import jax

    jax.config.update("jax_enable_x64", True)
    os.environ.update(MPLBACKEND="Agg", CERIDWEN_TARGET_ID="M1_210210", JAX_PLATFORMS="cpu",
                      CERIDWEN_RESULT_DIR=tempfile.mkdtemp(), SPS_HOME=str(SPS_HOME))
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    cells = ["".join(cell["source"]) for cell in json.loads(NOTEBOOK.read_text())["cells"]]
    namespace = {"display": lambda *args, **kwargs: None}
    cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)
    try:
        exec(cells[2], namespace)
        namespace["SETTINGS"]["emission_line_marginalisation"] = emission_line_marginalisation
        for index in (4, 6, 8):
            exec(cells[index], namespace)
        likelihood_lines = cells[10].split("calibration_polynomial =")[1].split("model_parameter_block_text")[0]
        exec("calibration_polynomial =" + likelihood_lines, namespace)
    finally:
        os.chdir(cwd)
    namespace["plt"].close("all")
    return namespace


def _draws(model):
    import jax.numpy as jnp
    import numpy as np
    from ceridwen.fit import load_result_h5

    samples = load_result_h5(REFERENCE).samples
    return {name: jnp.asarray(np.asarray(samples[name])[DRAWS]).reshape((len(DRAWS), *np.shape(template)))
            for name, template in model.theta_init.items()}


def _sampler_loglike(namespace):
    """The log-likelihood run_sampler hands to the sampler."""
    import jax
    from types import SimpleNamespace
    from ceridwen.sampler.runner import run_sampler

    capture = SimpleNamespace(run=lambda loglike, logprior, theta, key: loglike)
    return run_sampler(namespace["joint_model"], namespace["joint_likelihood"], capture,
                       jax.random.PRNGKey(0))


def test_default_is_off():
    cells = ["".join(cell["source"]) for cell in json.loads(NOTEBOOK.read_text())["cells"]]
    assert '"emission_line_marginalisation": False,' in cells[2]


def test_option_off_reproduces_the_previous_loglikelihood_bit_for_bit():
    import jax
    import numpy as np

    namespace = _build(False)
    from benchmark_ceridwen_vast import _make_log_functions  # scripts/ is on sys.path after _build
    assert namespace["emission_line_columns"] is None
    model = namespace["joint_model"]
    assert "zred" in model.param_names
    expected = [float.fromhex(value) for value in BASELINE]
    for loglike in (_make_log_functions(model, namespace["joint_likelihood"])[0], _sampler_loglike(namespace)):
        np.testing.assert_array_equal(np.asarray(jax.jit(jax.vmap(loglike))(_draws(model))), expected)


def test_option_on_fixes_redshift_ties_oxygen_and_shares_photometry():
    import jax
    import numpy as np

    namespace = _build(True)
    model = namespace["joint_model"]
    lines = namespace["emission_line_columns"]
    assert "zred" not in model.param_names and lines.zred_key is None
    assert lines.photometry_key == "photometry"
    assert "[O III] 5007 (+[O III] 4959)" in lines.free_names
    assert "[Ne III] 3869 (+[Ne III] 3968)" in lines.free_names
    assert "[O II] 3726" not in lines.names          # below the spectrum; never tied
    values = np.asarray(jax.jit(jax.vmap(_sampler_loglike(namespace)))(_draws(model)))
    assert np.all(np.isfinite(values))


def test_tied_ratio_holds_in_posterior_draws():
    import jax
    import jax.numpy as jnp
    import numpy as np

    namespace = _build(True)
    model = namespace["joint_model"]
    lines = namespace["emission_line_columns"]
    spectrum = model.obs_dict["spectrum"]
    theta = {name: value[0] for name, value in _draws(model).items()}
    mu = model.predict(theta)
    sigma = jnp.sqrt(spectrum.uncertainty ** 2 + (jnp.exp(theta["log_f_calib"][0]) * mu["spectrum"]) ** 2)
    n = 200
    _, fluxes, _ = namespace["calibration_polynomial"].posterior_draws_with_lines(
        spectrum.flux, jnp.tile(mu["spectrum"], (n, 1)), jnp.tile(sigma, (n, 1)),
        jnp.tile(lines.columns(theta), (n, 1, 1)), spectrum.mask, jax.random.PRNGKey(3),
        sweeps=100, ridge=lines.ridge,
        photometry=(lines.band_matrix, namespace["phot_flux"], jnp.tile(mu["photometry"], (n, 1)),
                    jnp.tile(namespace["phot_uncertainty"], (n, 1)), namespace["phot_fit_mask"]))
    raw = np.asarray(fluxes) @ lines.tie.T                  # flux of every FSPS line per draw
    names = list(lines.names)
    assert np.all(raw >= 0)
    np.testing.assert_allclose(raw[:, names.index("[O III] 5007")], 3.010 * raw[:, names.index("[O III] 4959")],
                               rtol=1e-12)
    np.testing.assert_allclose(raw[:, names.index("[Ne III] 3869")], 3.318 * raw[:, names.index("[Ne III] 3968")],
                               rtol=1e-12)


def test_band_matrix_matches_the_narrow_line_formula_and_changes_bands_slightly():
    """One unit-flux line at lambda_0 adds lambda_0 T(lambda_0) / (c int T / lambda dlambda)
    in F_nu to an AB band.  With the posterior-mean fluxes of M1_210210 the bands
    change by well under their 5 % error floor."""
    import jax
    import jax.numpy as jnp
    import numpy as np

    namespace = _build(True)
    lines = namespace["emission_line_columns"]
    phot = namespace["phot_obs"]
    from dataclasses import replace

    raw_band = replace(lines, tie=None).with_photometry(phot, "photometry").band_matrix  # one column per line
    np.testing.assert_allclose(raw_band @ lines.tie, lines.band_matrix, rtol=1e-12)
    # narrow-line limit (1 km/s): the delta-function formula below
    raw_band = replace(lines, tie=None, sigma_gas_kms=1.0,
                       sigma_inst_kms=np.ones_like(lines.sigma_inst_kms)).with_photometry(phot, "photometry").band_matrix
    centre = lines.wave_rest * (1 + lines.zred)
    for b, curve in enumerate(phot.filterset.filters):
        lam, trans = np.asarray(curve.wavelength, float), np.asarray(curve.transmission, float)
        expected = (centre * np.interp(centre, lam, trans, left=0, right=0)
                    / (2.99792458e18 * np.trapezoid(trans / lam, lam)) / 3631e-23)
        np.testing.assert_allclose(raw_band[b], expected, rtol=2e-3, atol=1e-4 * np.abs(expected).max())

    model = namespace["joint_model"]
    draws = _draws(model)
    spectrum = model.obs_dict["spectrum"]
    mu = jax.vmap(model.predict)(draws)
    sigma = jnp.sqrt(spectrum.uncertainty ** 2 + (jnp.exp(draws["log_f_calib"]) * mu["spectrum"]) ** 2)
    _, fluxes, _ = namespace["calibration_polynomial"].posterior_draws_with_lines(
        spectrum.flux, mu["spectrum"], sigma, jax.vmap(lines.columns)(draws), spectrum.mask,
        jax.random.PRNGKey(4), sweeps=300, ridge=lines.ridge,
        photometry=(lines.band_matrix, namespace["phot_flux"], mu["photometry"],
                    jnp.broadcast_to(namespace["phot_uncertainty"], mu["photometry"].shape),
                    namespace["phot_fit_mask"]))
    change = np.asarray(fluxes) @ lines.band_matrix.T / np.asarray(mu["photometry"])
    names = namespace["FILTER_LABELS"]
    print("\nband change from lines, median over draws [%]: "
          + ", ".join(f"{n} {v:.3f}" for n, v in zip(names, 100 * np.median(change, axis=0))))
    assert np.all(change >= 0)
    assert np.max(change) < 0.01


def test_stellar_model_variance_is_close_to_the_line_dependent_variance():
    """Fractional noise at the stellar model mu versus at mu + sum f_k L_k.

    Per draw: the joint marginal (spectrum and photometry sharing the fluxes) with
    sigma^2 = sigma_obs^2 + (f_calib mu)^2 (the implementation), and again with the
    posterior-mean line fluxes (f >= 0) added to mu in that variance term.  A constant
    offset leaves the posterior unchanged; its spread over the draws is what can move it.
    """
    import jax
    import jax.numpy as jnp
    import numpy as np
    from ceridwen.likelihood import lnlike_diag_gaussian

    namespace = _build(True)
    model = namespace["joint_model"]
    lines = namespace["emission_line_columns"]
    calibration = namespace["calibration_polynomial"]
    spectrum = model.obs_dict["spectrum"]
    y, sigma_obs, mask = spectrum.flux, spectrum.uncertainty, spectrum.mask
    y_p, sigma_p, mask_p = namespace["phot_flux"], namespace["phot_uncertainty"], namespace["phot_fit_mask"]
    band = jnp.asarray(lines.band_matrix)
    assert np.any(np.abs(np.asarray(spectrum.wavelength)[mask] - 4862.76 * (1 + namespace["z_catalog"])) < 3)

    def marginal(theta):
        prediction = model.predict(theta)
        mu, mu_p = prediction["spectrum"], prediction["photometry"]
        f_calib = jnp.exp(theta["log_f_calib"][0])
        columns = lines.columns(theta)
        phot = (band, y_p, mu_p, sigma_p, mask_p)

        def lnz(sigma):
            mu_cal, _, f_hat, extra = calibration.calibrate_with_lines(
                y, mu, sigma, mask, columns, lines.pairs, lines.ridge, phot)
            gauss, _ = lnlike_diag_gaussian(y, mu_cal, 1 / sigma ** 2, 0.5 * jnp.log(2 * jnp.pi * sigma ** 2), mask)
            gauss_p, _ = lnlike_diag_gaussian(y_p, mu_p + band @ f_hat, 1 / sigma_p ** 2,
                                              0.5 * jnp.log(2 * jnp.pi * sigma_p ** 2), mask_p)
            return gauss + gauss_p + extra

        sigma = jnp.sqrt(sigma_obs ** 2 + (f_calib * mu) ** 2)
        stellar = lnz(sigma)
        n = 128
        fluxes = jnp.mean(calibration.posterior_draws_with_lines(
            y, jnp.tile(mu, (n, 1)), jnp.tile(sigma, (n, 1)), jnp.tile(columns, (n, 1, 1)), mask,
            jax.random.PRNGKey(0), sweeps=300, ridge=lines.ridge,
            photometry=(band, y_p, jnp.tile(mu_p, (n, 1)), jnp.tile(sigma_p, (n, 1)), mask_p))[1], axis=0)
        with_lines = lnz(jnp.sqrt(sigma_obs ** 2 + (f_calib * (mu + columns @ fluxes)) ** 2))
        return with_lines - stellar, stellar

    delta, stellar = (np.asarray(value) for value in jax.jit(jax.vmap(marginal))(_draws(model)))
    # the mu-only variance is what the sampler evaluates
    np.testing.assert_allclose(stellar, np.asarray(jax.jit(jax.vmap(_sampler_loglike(namespace)))(_draws(model))),
                               rtol=1e-12)
    print(f"\ndelta lnL: mean {delta.mean():.3f}, sd over draws {delta.std():.3f}, "
          f"max |delta| {np.abs(delta).max():.3f}")
    assert delta.std() < 0.25
    assert np.abs(delta).max() < 1.0
