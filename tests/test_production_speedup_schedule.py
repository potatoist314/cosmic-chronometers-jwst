"""An execution schedule must preserve the BlackJAX transition itself."""
import sys
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
import pytest

jax.config.update('jax_enable_x64', True)

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_ceridwen_speedups import build_algorithm, FitExperiment, calibration_normal_dot


def test_reference_fit_keeps_original_arithmetic_with_optimized_package(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from ceridwen.likelihood import PolynomialCalibration
    monkeypatch.setattr(PolynomialCalibration, 'normal_matrix', PolynomialCalibration.normal_matrix)
    FitExperiment(tmp_path, 'baseline').attach(SimpleNamespace())
    assert PolynomialCalibration.normal_matrix is calibration_normal_dot


def test_candidate_fit_rejects_stale_installed_package(monkeypatch, tmp_path):
    from types import SimpleNamespace
    from ceridwen.likelihood import PolynomialCalibration
    monkeypatch.setattr(PolynomialCalibration, 'normal_matrix', calibration_normal_dot)
    with pytest.raises(AssertionError, match='installed Ceridwen package lacks the candidate'):
        FitExperiment(tmp_path, 'reduce').attach(SimpleNamespace())


def test_fixed_redshift_notebook_uses_supported_spectrum_arguments():
    import ast
    import json
    from ceridwen.observation import Spectrum

    path = Path(__file__).resolve().parents[1]/'notebooks/ceridwen_integrated_photometry_spectra.ipynb'
    notebook = json.loads(path.read_text())
    calls = []
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        for node in ast.walk(ast.parse(''.join(cell['source']))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Spectrum':
                for keyword in node.keywords:
                    if keyword.arg is None:
                        args = eval(compile(ast.Expression(keyword.value), str(path), 'eval'),
                                    {'FREE_ZRED_KMS': 0.})
                        Spectrum(wavelength=jnp.array([4000., 4100.]), **args)
                        assert args == {}
                        calls.append(args)
    assert len(calls) == 1


@pytest.mark.parametrize('batch', [10, 5, 2])
def test_grouped_chains_preserve_keys_and_complete_state(batch):
    def likelihood(p):
        return -.5 * jnp.sum(p['x'] ** 2)

    def prior(p):
        return jnp.where(jnp.all(jnp.abs(p['x']) < 10), 0., -jnp.inf)

    baseline = build_algorithm(likelihood, prior, 3, 10)
    trial = build_algorithm(likelihood, prior, 3, 10, f'group{batch}')
    state = baseline.init({'x': jax.random.normal(jax.random.PRNGKey(1), (20, 2))})
    step_baseline, step_trial = jax.jit(baseline.step), jax.jit(trial.step)
    for seed in [2, 3, 4]:
        key = jax.random.PRNGKey(seed)
        reference = step_baseline(key, state)
        actual = step_trial(key, state)
        assert jax.tree.structure(reference) == jax.tree.structure(actual)
        for a, b in zip(jax.tree.leaves(reference), jax.tree.leaves(actual)):
            np.testing.assert_array_equal(np.asarray(a), np.asarray(b))
        state = reference[0]
