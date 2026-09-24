"""Independent Noll slope and Drude amplitude through Ceridwen."""
import ast
import json
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import pytest

jax.config.update("jax_enable_x64", True)

from sedpy_jax.attenuation_dust import kriek_conroy, noll
from ceridwen.dust.DustModel import DiffuseDust


def test_linked_law_preserves_reference():
    wave = jnp.array([1500., 2175., 3000., 5500., 10000.])
    # Captured from sedpy_jax 482429b with float64 enabled.
    np.testing.assert_allclose(kriek_conroy(wave, .4, -.7),
        [2.5561667069005694, 2.0144670426096094, 1.06359601976844,
         .4005609018130236, .12191921164784238], rtol=1e-13)


def test_zero_bump_zero_dust_and_analytic_peak_increment():
    wave = jnp.array([1500., (1e4 / 4.59), 3000., 5500.])
    tau, slope, amplitude = .4, -.7, 2.0
    base = noll(wave, tau, slope, 0.)
    bumped = noll(wave, tau, slope, Ebump=amplitude)
    expected = tau * amplitude / 4.05 * ((1e4 / 4.59) / 5500.) ** slope
    np.testing.assert_allclose(bumped[1] - base[1], expected, rtol=1e-12)
    np.testing.assert_array_equal(noll(wave, 0., slope, Ebump=amplitude), 0.)
    # After removing the power-law tilt, fixed bump amplitude is independent of slope.
    for slope in [-1., 0., .4]:
        curve = noll(wave, tau, slope, Ebump=amplitude)
        np.testing.assert_allclose(curve / (wave / 5500.) ** slope,
                                   noll(wave, tau, 0., Ebump=amplitude))


def test_diffuse_wrapper_jit_and_independent_gradients():
    dust = DiffuseDust("noll")
    wave = jnp.array([1500., (1e4 / 4.59), 3000., 5500.])

    def curve(params):
        return dust.compute_attenuation(wave, {
            "diffuse_tau_noll": .4,
            "diffuse_c_r": 0.,
            "diffuse_delta": params[0],
            "diffuse_Ebump": params[1],
        })

    params = jnp.array([-.7, 2.])
    np.testing.assert_allclose(jax.jit(curve)(params), noll(wave, .4, -.7, Ebump=2.))
    jac = jax.jit(jax.jacfwd(curve))(params)
    assert np.isfinite(jac).all()
    assert np.linalg.matrix_rank(jac) == 2
    assert set(dust.get_param_names()) == {
        "diffuse_tau_noll", "diffuse_delta", "diffuse_Ebump", "diffuse_c_r"}
    assert "diffuse_Ebump" not in DiffuseDust().get_param_names()


@pytest.mark.parametrize("birth_cloud", [False, True])
def test_notebook_csp_routes_both_parameters_into_photometric_prediction(birth_cloud):
    from ceridwen.csp import CSPBasis_afe
    from ceridwen.ssps import SSPDataAfe
    from ceridwen.model import SedModel
    from ceridwen.observation import Photometry
    from ceridwen.sampler.priors import Uniform

    wave = jnp.geomspace(1000., 30000., 512)
    ssp = SSPDataAfe(jnp.array([-2.2, -1.4]), jnp.array([-.2, .6]),
                     jnp.array([-3., -1., 0., 1.2]), wave,
                     jnp.ones((2, 2, 4, 512)) * 1e-15)
    priors = {"diffuse_delta": Uniform(low=-1., high=.4),
              "diffuse_Ebump": Uniform(low=0., high=6.)}
    path = Path(__file__).resolve().parents[1] / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
    cells = json.loads(path.read_text())["cells"]
    settings_source = next("".join(c["source"]) for c in cells
                           if c["cell_type"] == "code" and "PRIORS = {" in "".join(c["source"]))
    prior_dict = next(n.value for n in ast.parse(settings_source).body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "PRIORS" for t in n.targets))
    bump_prior = next(v for k, v in zip(prior_dict.keys, prior_dict.values)
                      if isinstance(k, ast.Constant) and k.value == "diffuse_Ebump")
    actual_prior = eval(compile(ast.Expression(bump_prior), "bump_prior", "eval"), {"Uniform": Uniform})
    assert tuple(float(v) for v in actual_prior.bounds) == (0.0, 6.0)
    priors["diffuse_Ebump"] = actual_prior
    source = next("".join(c["source"]) for c in cells
                  if c["cell_type"] == "code" and "joint_csp = CSPBasis_afe(" in "".join(c["source"]))
    assignment = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "joint_csp" for t in n.targets))
    env = dict(CSPBasis_afe=CSPBasis_afe, ssp=ssp, jnp=jnp,
               lookback_template=np.array([0., .1, 1., 5.]),
               SETTINGS={"birth_cloud_dust": birth_cloud}, PRIORS=priors)
    exec(compile(ast.Module(body=[assignment], type_ignores=[]), "notebook_csp", "exec"), env)
    env.update(joint_transforms={}, joint_priors={"dust_ratio": Uniform(low=0., high=2.)})
    birth_cloud_node = next(n for n in ast.parse(source).body if isinstance(n, ast.If)
                            and ast.unparse(n.test) == "SETTINGS['birth_cloud_dust']")
    exec(compile(ast.Module(body=[birth_cloud_node], type_ignores=[]), "birth_cloud", "exec"), env)
    if birth_cloud:
        priors["dust_ratio"] = env["joint_priors"]["dust_ratio"]
        np.testing.assert_allclose(env["joint_transforms"]["tau_pow"](
            {"dust_ratio": .5, "diffuse_tau_noll": .4}), .2)
    obs = Photometry(filters=["galex_NUV", "cfht_megacam_u_9302"],
                      flux=np.ones(2), uncertainty=np.ones(2), name="photometry")
    model = SedModel(env["joint_csp"], observations=[obs], priors=priors, transforms=env["joint_transforms"],
                     free_param_init={"dust_ratio": jnp.array([1.])} if birth_cloud else {}, zred=.6542)
    assert set(priors) <= set(model.theta_init)
    assert set(priors) <= set(model.param_names)
    theta = dict(model.theta_init, diffuse_Ebump=jnp.array([0.]))
    no_bump = np.asarray(model.predict(theta)["photometry"])
    theta["diffuse_Ebump"] = jnp.array([2.])
    bumped = np.asarray(model.predict(theta)["photometry"])
    assert np.isfinite(bumped).all()
    assert np.all(bumped < no_bump)


def test_noll_saved_notebook_keeps_parameter_names(monkeypatch):
    from scripts import regenerate_fit_notebooks as regenerate
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root / "scripts"))
    folder = root / "results/m1-210210-reference/tau-1/poly10/210210-M1_210210"
    fit = {**regenerate.stored_fit(folder), "dust_law": "noll", "scaling_prior": None}
    notebook = regenerate.compact_notebook(folder, fit)
    source = "\n".join(c.source for c in notebook.cells)
    assert 'diffuse_law="noll"' in source
    assert '"diffuse_Ebump": Uniform(low=0.0, high=6.0)' in source
    assert "diffuse_tau_kc" not in source
    for cell in notebook.cells:
        if cell.cell_type == "code":
            ast.parse(cell.source)
