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
    loglike, _ = _make_log_functions(model, namespace["joint_likelihood"])
    values = np.asarray(jax.jit(jax.vmap(loglike))(_draws(model)))
    np.testing.assert_array_equal(values, [float.fromhex(value) for value in BASELINE])


def test_stellar_model_variance_is_close_to_the_line_dependent_variance():
    """Fractional noise at the stellar model mu versus at mu + sum f_k L_k.

    Per draw: the joint marginal with sigma^2 = sigma_obs^2 + (f_calib mu)^2 (the
    implementation), and again with the posterior-mean line fluxes (f >= 0) added
    to mu in that variance term.  A constant offset leaves the posterior unchanged; its spread
    over the posterior draws is what can move it.
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
    assert {"Ba-beta 4861", "[O III] 4959", "[O III] 5007"} <= set(lines.names)
    assert np.any(np.abs(np.asarray(spectrum.wavelength)[mask] - 4862.76 * (1 + namespace["z_catalog"])) < 3)

    def marginal(theta):
        mu = model.predict(theta)["spectrum"]
        f_calib = jnp.exp(theta["log_f_calib"][0])
        columns = lines.columns(theta)

        def lnz(sigma):
            mu_cal, _, _, extra = calibration.calibrate_with_lines(y, mu, sigma, mask, columns,
                                                                   lines.pairs, lines.ridge)
            gauss, _ = lnlike_diag_gaussian(y, mu_cal, 1 / sigma ** 2, 0.5 * jnp.log(2 * jnp.pi * sigma ** 2), mask)
            return gauss + extra

        sigma = jnp.sqrt(sigma_obs ** 2 + (f_calib * mu) ** 2)
        stellar = lnz(sigma)
        # line fluxes: mean of 128 truncated (f >= 0) posterior draws at this theta
        fluxes = jnp.mean(calibration.posterior_draws_with_lines(
            y, jnp.tile(mu, (128, 1)), jnp.tile(sigma, (128, 1)), jnp.tile(columns, (128, 1, 1)), mask,
            jax.random.PRNGKey(0), sweeps=300, ridge=lines.ridge)[1], axis=0)
        with_lines = lnz(jnp.sqrt(sigma_obs ** 2 + (f_calib * (mu + columns @ fluxes)) ** 2))
        # rest-frame equivalent width [A] against the stellar model at the line centre
        opz = 1 + theta["zred"][0]
        centre = jnp.asarray(lines.wave_rest) * opz
        f_lambda = jnp.interp(centre, jnp.asarray(spectrum.wavelength), mu) * 2.99792458e18 / centre ** 2
        return with_lines - stellar, fluxes / f_lambda / opz

    delta, ew = (np.asarray(value) for value in jax.jit(jax.vmap(marginal))(_draws(model)))
    print(f"\ndelta lnL: mean {delta.mean():.3f}, sd over draws {delta.std():.3f}, "
          f"max |delta| {np.abs(delta).max():.3f}; |EW| median {np.median(np.abs(ew)):.3f} A, "
          f"max {np.abs(ew).max():.3f} A over {len(lines.names)} lines")
    assert delta.std() < 0.25
    assert np.abs(delta).max() < 1.0


def test_loglikelihood_is_finite_across_the_redshift_prior():
    """Lines are selected at the catalogue z; at the prior edges some leave the
    unmasked pixels and their columns shrink, but the likelihood stays finite."""
    import jax
    import jax.numpy as jnp
    import numpy as np

    namespace = _build(True)
    model = namespace["joint_model"]
    from benchmark_ceridwen_vast import _make_log_functions

    loglike, _ = _make_log_functions(model, namespace["joint_likelihood"])
    draws = _draws(model)
    offsets = np.linspace(-namespace["SETTINGS"]["zred_half_width"], namespace["SETTINGS"]["zred_half_width"], 20)
    draws["zred"] = jnp.asarray(namespace["z_catalog"] + offsets).reshape(draws["zred"].shape)
    values = np.asarray(jax.jit(jax.vmap(loglike))(draws))
    assert np.all(np.isfinite(values))
