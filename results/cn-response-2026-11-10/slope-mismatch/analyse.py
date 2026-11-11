#!/usr/bin/env python3
"""Experiment 10: unchanged chronometer mocks under coverage and C/N mismatch."""
from __future__ import annotations

import argparse
import contextlib
import csv
import gc
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys

os.environ.update(JAX_PLATFORMS="cpu", JAX_ENABLE_X64="1", MPLBACKEND="Agg",
                  CERIDWEN_PLOTS="0")
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BASE = OUT.parent
PREVIOUS = BASE / "prior-slope"
sys.path[:0] = [str(ROOT), str(ROOT / "ceridwen"), str(ROOT / "external/sedpy_jax")]
os.chdir(ROOT)

spec = importlib.util.spec_from_file_location("experiment9", PREVIOUS / "analyse.py")
e9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e9)
import h5py
import jax
import jax.numpy as jnp
import numpy as np
from scipy.special import softmax
from scipy.spatial import cKDTree

from ceridwen.csp import CSPBasis_afe
from ceridwen.model import SedModel
from ceridwen.broadening import Kinematics
from ceridwen.ssps.abundance_response import AlfCNResponse
from ceridwen.observation.absorption_features import absorption_feature_mask
from scripts.generate_cn_mocks import RESPONSE
from scripts.experiment import validate_result, configuration
from scripts.run_ceridwen_vast_multi_gpu import _fit_notebook

SEEDS = e9.NOISE_SEEDS
FIT_SEED = e9.FIT_SEED
BOOTSTRAP_SEED = e9.BOOTSTRAP_SEED
REST_RANGE = [4155., 4438.1]
CFE, NFE = .15, .30
sha, dump, table = e9.sha, e9.dump, e9.table


def previous_inputs():
    return json.loads((PREVIOUS / "inputs.json").read_text())


def groups():
    rows = csv.DictReader((BASE / "information-map/widths.csv").open())
    result = {r["target"]: r["coverage"] == "with_Mgb" for r in rows
              if r["arm"] == "baseline" and r["quantity"] == "age_gyr"}
    assert len(result) == 10 and sum(result.values()) == 5
    return result


def assemble(truth):
    raw = ROOT / truth["baseline_result"]
    manifest = json.loads((raw.parent.parents[2] / "manifest.json").read_text())
    cell = next(c for c in manifest["source"]["experiment"]
                if c["target"] == truth["target"] and c["arm"] == "baseline")
    settings = dict(cell["settings"], ssp_grid=manifest["source"]["grid"],
                    mock_data=None, abundance_response=None)
    os.environ.update(CERIDWEN_TARGET_ID=truth["target"],
                      CERIDWEN_MANIFEST_INDEX=str(cell["target_metadata"]["manifest_index"]),
                      CERIDWEN_RANDOM_SEED=str(FIT_SEED),
                      CERIDWEN_RESULT_DIR=str(OUT / "assembly" / truth["target"]))
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        document = _fit_notebook(json.dumps(settings), json.dumps(cell["priors"]))
        for index, notebook_cell in enumerate(document.cells[:9]):
            if notebook_cell.cell_type == "code":
                exec(compile(notebook_cell.source, f"production-cell-{index}", "exec"), ns)
    assert ns["joint_csp"].sfh_basis_fastpath
    assert float(ns["joint_priors"]["logsfr_ratios"].scale) == .3
    return ns


def predictions(ns, truth):
    """The same 102-bin truth as E9, with the existing alf response attached."""
    med = {k: np.asarray(v) for k, v in truth["median_parameters"].items()}
    times = np.asarray(truth["time_edges_gyr"])
    history = np.asarray(truth["sfh_per_bin"])
    np.testing.assert_allclose(np.sum(history * np.diff(times) * 1e9), 1., rtol=1e-14)
    mass = history * np.diff(times)
    exact_age = mass @ ((times[:-1] + times[1:]) / 2) / mass.sum()
    np.testing.assert_allclose(exact_age, truth["true_age_gyr"], atol=2e-15, rtol=0)
    response = AlfCNResponse.load(ROOT / RESPONSE, sigma_catalog=float(ns["sigma_star"]))
    transforms = {k: v for k, v in ns["joint_transforms"].items()
                  if k in ("diffuse_c_r", "tau_pow", "alpha_pow")}
    theta = dict(lookback_time=jnp.asarray(times), sfh=jnp.asarray(history),
                 logzsol=jnp.array([-.2]), afe=jnp.array([.2]),
                 diffuse_tau_noll=jnp.asarray(med["diffuse_tau_noll"]),
                 diffuse_delta=jnp.asarray(med["diffuse_delta"]))
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        csp = CSPBasis_afe(ns["ssp"], theta=theta, abundance_response=response,
                           zh_const=True, sfh_interp="step", add_dust=ns["SETTINGS"]["birth_cloud_dust"],
                           add_diffuse_dust=True, diffuse_law="noll", add_dust_emission=False,
                           add_igm=False, track_zred_age=False, cosmo=e9.COSMO, verbose=False)
        model = SedModel(csp, observations=[ns["phot_obs"], ns["spectrum_obs"]],
                         transforms=transforms,
                         free_param_init={k: jnp.asarray(med[k]) for k in
                                          ("logmass", "diffuse_Ebump", "dust_ratio") if k in med},
                         zred=truth["redshift"],
                         kinematics=Kinematics(sigma_gal=float(med["sigma_smooth"][0])),
                         broaden_photometry=False)
        zero_theta = dict(model.theta_init, cfe=jnp.array([0.]), nfe=jnp.array([0.]))
        zero = {k: np.asarray(v) for k, v in model.predict(zero_theta).items()}
        cn_theta = dict(zero_theta, cfe=jnp.array([CFE]), nfe=jnp.array([NFE]))
        cn = {k: np.asarray(v) for k, v in model.predict(cn_theta).items()}
    assert csp.sfh_basis_fastpath
    return zero, cn, dict(response.minimum_total_sigma)


def generate(first_only=False):
    source = previous_inputs()
    g = groups()
    for mock in source["mocks"]:
        assert sha(ROOT / mock["path"]) == mock["sha256"]
    manifest = dict(previous_manifest=str((PREVIOUS / "inputs.json").relative_to(ROOT)),
                    previous_manifest_sha256=sha(PREVIOUS / "inputs.json"),
                    previous_script_sha256=sha(PREVIOUS / "analyse.py"),
                    generator_sha256=sha(Path(__file__)), cfe=CFE, nfe=NFE,
                    rest_range=REST_RANGE, fit_seed=FIT_SEED, noise_seeds=SEEDS,
                    response_directory=RESPONSE, response_sha256={str(p.name): sha(p)
                        for p in sorted((ROOT / RESPONSE).glob("*.abund.krpa.s100"))},
                    truths=source["truths"], mocks=[], checks=[],
                    group_indicator="1 = originally with fitted Mg b in full range; 0 = originally without. Fixed across all arms, including common-window fits.",
                    formation_start_gyr=source["formation_start_gyr"], formation_end_gyr=source["formation_end_gyr"],
                    choices="Exact E9 times, SFH, metallicity, alpha, dust, mass, dispersion, instrument, grids, masks, filters and statistical errors. Only C/Fe +0.15 and N/Fe +0.30 change. Same standardized Gaussian draws; true model-scaled floors recomputed for the enhanced mean, as in E4/E9.")
    (OUT / "mocks").mkdir(exist_ok=True)
    (OUT / "configs/B").mkdir(parents=True, exist_ok=True)
    selected = source["truths"][:1] if first_only else source["truths"]
    for truth in selected:
        ns = assemble(truth)
        zero, cn, minimum_sigma = predictions(ns, truth)
        arms = {}
        for seed in SEEDS:
            old_record = next(m for m in source["mocks"] if m["target"] == truth["target"]
                              and m["noise_seed"] == seed)
            with np.load(ROOT / old_record["path"]) as stored:
                old = {k: np.asarray(v) for k, v in stored.items()}
            np.testing.assert_array_equal(zero["photometry"], old["mean_photometry"])
            np.testing.assert_array_equal(zero["spectrum"], old["mean_spectrum"])
            np.testing.assert_array_equal(ns["spectrum_wave"], old["spectrum_wave"])
            np.testing.assert_array_equal(ns["spectrum_mask"], old["spectrum_mask"])
            actual_group = bool(np.any(absorption_feature_mask(old["spectrum_wave"],
                                zred=truth["redshift"], features=["Mgb"]) & old["spectrum_mask"]))
            assert actual_group == g[truth["target"]]
            rest = old["spectrum_wave"] / (1 + truth["redshift"])
            common_mask = old["spectrum_mask"] & (rest >= REST_RANGE[0]) & (rest <= REST_RANGE[1])
            assert common_mask.sum() > 0
            phot_sigma = np.hypot(old["photometry_uncertainty"], .05 * np.abs(cn["photometry"]))
            floor = np.exp(truth["median_parameters"]["log_f_calib"][0])
            spec_sigma = np.hypot(old["spectrum_uncertainty"], floor * np.abs(cn["spectrum"]))
            rng = np.random.default_rng(seed)
            phot_noise = rng.standard_normal(phot_sigma.shape)
            spec_noise = rng.standard_normal(spec_sigma.shape)
            # The zero-response reconstruction must reproduce the old noise byte-for-byte.
            np.testing.assert_array_equal(old["photometry_flux"], old["mean_photometry"]
                                          + phot_noise * old["photometry_noise_sigma"])
            np.testing.assert_array_equal(old["spectrum_flux"], old["mean_spectrum"] + np.where(
                old["native_valid"], spec_noise * old["spectrum_noise_sigma"], 0.))
            new = dict(old, photometry_flux=cn["photometry"] + phot_noise * phot_sigma,
                       spectrum_flux=cn["spectrum"] + np.where(old["native_valid"], spec_noise * spec_sigma, 0.),
                       mean_photometry=cn["photometry"], mean_spectrum=cn["spectrum"],
                       photometry_noise_sigma=phot_sigma, spectrum_noise_sigma=spec_sigma,
                       cfe=np.array(CFE), nfe=np.array(NFE))
            changed = {"photometry_flux", "spectrum_flux", "mean_photometry", "mean_spectrum",
                       "photometry_noise_sigma", "spectrum_noise_sigma"}
            for key in old.keys() - changed:
                np.testing.assert_array_equal(new[key], old[key])
            path = OUT / "mocks" / f'{truth["target"]}_s{seed}.npz'
            np.savez_compressed(path, **new)
            manifest["mocks"].append(dict(target=truth["target"], noise_seed=seed,
                path=str(path.relative_to(ROOT)), sha256=sha(path),
                previous_path=old_record["path"], previous_sha256=old_record["sha256"]))
            for arm in ("B1", "B2", "B3"):
                settings = dict(mock_data=str(path.relative_to(ROOT)),
                                abundance_response=RESPONSE if arm == "B2" else None,
                                rest_range=REST_RANGE if arm == "B3" else None)
                arms[f"{arm}_s{seed}"] = dict(settings=settings)
        manifest["checks"].append(dict(target=truth["target"], zero_response_bitwise=True,
            other_mock_fields_bitwise=True, standardized_noise_exact=True,
            true_age_gyr=truth["true_age_gyr"], original_Mgb_group=g[truth["target"]],
            common_range_pixels=int(common_mask.sum()), minimum_total_sigma_kms=minimum_sigma))
        dump(OUT / f'configs/B/{truth["target"]}.json', dict(targets=[truth["target"]],
             seed=FIT_SEED, settings={}, priors={}, arms=arms))
        print(f'{truth["target"]}: zero-response and unchanged fields bitwise; '
              f'{common_mask.sum()} common-window pixels; sigma {minimum_sigma}', flush=True)
        del ns, zero, cn
        gc.collect()
        jax.clear_caches()
    for mock in source["mocks"]:
        assert sha(ROOT / mock["path"]) == mock["sha256"]
    dump(OUT / ("probe-inputs.json" if first_only else "inputs.json"), manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["probe", "generate"])
    args = parser.parse_args()
    generate(first_only=args.step == "probe")


if __name__ == "__main__":
    main()
