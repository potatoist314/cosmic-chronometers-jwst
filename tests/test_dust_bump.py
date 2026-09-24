"""Independent Kriek-Conroy slope and Drude amplitude through Ceridwen."""
import ast
import json
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np

jax.config.update("jax_enable_x64", True)

from sedpy_jax.attenuation_dust import kriek_conroy, kriek_conroy_free_bump
from ceridwen.dust.DustModel import DiffuseDust


def test_linked_law_preserves_reference_and_matches_independent_amplitude():
    wave = jnp.array([1500., 2175., 3000., 5500., 10000.])
    # Captured from sedpy_jax 482429b with float64 enabled.
    np.testing.assert_allclose(kriek_conroy(wave, .4, -.7),
        [2.5561667069005694, 2.0144670426096094, 1.06359601976844,
         .4005609018130236, .12191921164784238], rtol=1e-13)
    for slope in [-1.0, -0.7, 0.0, 0.4]:
        np.testing.assert_array_equal(
            kriek_conroy(wave, .4, slope),
            kriek_conroy_free_bump(wave, .4, slope, .85 - 1.9 * slope))


def test_zero_bump_zero_dust_and_analytic_peak_increment():
    wave = jnp.array([1500., 2175., 3000., 5500.])
    tau, slope, amplitude = .4, -.7, 2.0
    base = kriek_conroy_free_bump(wave, tau, slope, 0.)
    bumped = kriek_conroy_free_bump(wave, tau, slope, amplitude)
    expected = tau * amplitude / 4.05 * (2175. / 5500.) ** slope
    np.testing.assert_allclose(bumped[1] - base[1], expected, rtol=1e-12)
    np.testing.assert_array_equal(kriek_conroy_free_bump(wave, 0., slope, amplitude), 0.)
    # After removing the power-law tilt, fixed bump amplitude is independent of slope.
    for slope in [-1., 0., .4]:
        curve = kriek_conroy_free_bump(wave, tau, slope, amplitude)
        np.testing.assert_allclose(curve / (wave / 5500.) ** slope,
                                   kriek_conroy_free_bump(wave, tau, 0., amplitude))


def test_diffuse_wrapper_jit_and_independent_gradients():
    dust = DiffuseDust("kriek_conroy_free_bump")
    wave = jnp.array([1500., 2175., 3000., 5500.])

    def curve(params):
        return dust.compute_attenuation(wave, {
            "diffuse_tau_kc": .4,
            "diffuse_dust_index": params[0],
            "diffuse_bump_strength": params[1],
        })

    params = jnp.array([-.7, 2.])
    np.testing.assert_allclose(jax.jit(curve)(params), kriek_conroy_free_bump(wave, .4, -.7, 2.))
    jac = jax.jit(jax.jacfwd(curve))(params)
    assert np.isfinite(jac).all()
    assert np.linalg.matrix_rank(jac) == 2
    assert set(dust.get_param_names()) == {
        "diffuse_tau_kc", "diffuse_dust_index", "diffuse_bump_strength"}
    assert "diffuse_bump_strength" not in DiffuseDust().get_param_names()


def test_notebook_csp_routes_both_parameters_into_photometric_prediction():
    from ceridwen.csp import CSPBasis_afe
    from ceridwen.ssps import SSPDataAfe
    from ceridwen.model import SedModel
    from ceridwen.observation import Photometry
    from ceridwen.sampler.priors import Uniform

    wave = jnp.geomspace(1000., 30000., 512)
    ssp = SSPDataAfe(jnp.array([-2.2, -1.4]), jnp.array([-.2, .6]),
                     jnp.array([-3., -1., 0., 1.2]), wave,
                     jnp.ones((2, 2, 4, 512)) * 1e-15)
    priors = {"diffuse_dust_index": Uniform(low=-1., high=.4),
              "diffuse_bump_strength": Uniform(low=0., high=4.)}  # test bounds only
    path = Path(__file__).resolve().parents[1] / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
    cells = json.loads(path.read_text())["cells"]
    source = next("".join(c["source"]) for c in cells
                  if c["cell_type"] == "code" and "joint_csp = CSPBasis_afe(" in "".join(c["source"]))
    assignment = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "joint_csp" for t in n.targets))
    env = dict(CSPBasis_afe=CSPBasis_afe, ssp=ssp, jnp=jnp,
               lookback_template=np.array([0., .1, 1., 5.]),
               SETTINGS={"birth_cloud_dust": False}, PRIORS=priors)
    exec(compile(ast.Module(body=[assignment], type_ignores=[]), "notebook_csp", "exec"), env)
    obs = Photometry(filters=["galex_NUV", "cfht_megacam_u_9302"],
                      flux=np.ones(2), uncertainty=np.ones(2), name="photometry")
    model = SedModel(env["joint_csp"], observations=[obs], priors=priors, zred=.6542)
    assert set(priors) <= set(model.theta_init)
    assert set(priors) <= set(model.param_names)
    theta = dict(model.theta_init, diffuse_bump_strength=jnp.array([0.]))
    no_bump = np.asarray(model.predict(theta)["photometry"])
    theta["diffuse_bump_strength"] = jnp.array([2.])
    bumped = np.asarray(model.predict(theta)["photometry"])
    assert np.isfinite(bumped).all()
    assert np.all(bumped < no_bump)
