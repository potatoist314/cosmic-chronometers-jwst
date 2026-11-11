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
from scipy.linalg import lstsq
from scipy.stats import linregress
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


def make_row(arm, target, seed, truth, ageq, afe, path, reference, with_mgb):
    q16, q50, q84 = map(float, ageq)
    width = q84 - q16
    pwidth = float(reference["age_q84"]) - float(reference["age_q16"])
    return dict(arm=arm, target=target, noise_seed=seed, redshift=truth["redshift"],
        original_with_Mgb=with_mgb, true_age_gyr=truth["true_age_gyr"],
        age_q16=q16, age_q50=q50, age_q84=q84,
        age_bias_gyr=q50 - truth["true_age_gyr"],
        age_truth_inside=q16 <= truth["true_age_gyr"] <= q84,
        age_width_16_84_gyr=width, P_age_width_16_84_gyr=pwidth,
        width_ratio_to_P=width / pwidth, width_difference_from_P_gyr=width - pwidth,
        afe_q50=afe, afe_bias=afe - .2, result_path=path)


def summarize():
    inputs = json.loads((OUT / "inputs.json").read_text())
    old_inputs = previous_inputs()
    assert sha(PREVIOUS / "inputs.json") == inputs["previous_manifest_sha256"]
    assert sha(PREVIOUS / "analyse.py") == inputs["previous_script_sha256"]
    for item in old_inputs["mocks"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for item in inputs["mocks"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for name, digest in inputs["response_sha256"].items():
        assert sha(ROOT / RESPONSE / name) == digest
    references = {(r["target"], int(r["noise_seed"])): r for r in
                  csv.DictReader((PREVIOUS / "per-mock.csv").open()) if r["arm"] == "P"}
    assert len(references) == 30
    truths = {t["target"]: t for t in inputs["truths"]}
    original_groups = {t["target"]: t["original_Mgb_group"] for t in inputs["checks"]}
    rows, checks = [], []
    for (target, seed), reference in references.items():
        rows.append(make_row("P9", target, seed, truths[target],
                    [reference[f"age_q{q}"] for q in (16, 50, 84)],
                    float(reference["afe_q50"]), reference["result_path"], reference, original_groups[target]))
    for part, arms in (("A", ("A",)), ("B", ("B1", "B2", "B3"))):
        for target, truth in truths.items():
            run = OUT / "runs" / part / target
            manifest = json.loads((run / "manifest.json").read_text())
            assert set(manifest["completed_cells"]) == {
                f"{arm}_s{seed}/{target}" for arm in arms for seed in SEEDS}
            for arm in arms:
                for seed in SEEDS:
                    directory, = (run / "fits" / f"{arm}_s{seed}").iterdir()
                    validate_result(directory)
                    raw = directory / "ceridwen_result.h5"
                    fit = e9.load_result_h5(raw)
                    assert ({"cfe", "nfe"} <= set(fit.samples)) if arm == "B2" else not (
                        {"cfe", "nfe"} & set(fit.samples))
                    assert np.asarray(fit.samples["logsfr_ratios"]).shape[1:] == (14,)
                    mock_record = next(m for m in (old_inputs["mocks"] if part == "A" else inputs["mocks"])
                                       if m["target"] == target and m["noise_seed"] == seed)
                    with np.load(ROOT / mock_record["path"]) as data, h5py.File(
                            directory / "ceridwen_derived_outputs.h5", "r") as stored:
                        times = np.asarray(stored["sfh/lookback_time_gyr"])
                        assert int(stored.attrs["random_seed"]) == FIT_SEED
                        np.testing.assert_allclose(float(stored.attrs["redshift"]), truth["redshift"],
                                                   atol=1e-10, rtol=0)
                        mask = data["spectrum_mask"].copy()
                        if arm in ("A", "B3"):
                            rest = data["spectrum_wave"] / (1 + truth["redshift"])
                            mask &= (rest >= REST_RANGE[0]) & (rest <= REST_RANGE[1])
                        np.testing.assert_array_equal(stored["spectrum/mask"], mask)
                        assert np.all(np.isnan(np.asarray(stored["spectrum/pull"])[~mask]))
                        np.testing.assert_array_equal(stored["spectrum/wavelength"], data["spectrum_wave"])
                        np.testing.assert_array_equal(stored["spectrum/observed"], data["spectrum_flux"])
                        np.testing.assert_array_equal(stored["photometry/observed"], data["photometry_flux"])
                        np.testing.assert_array_equal(stored["spectrum/uncertainty"], np.where(
                            data["native_valid"], data["spectrum_uncertainty"], 1.))
                        np.testing.assert_allclose(stored["photometry/uncertainty"], np.hypot(
                            data["photometry_uncertainty"], .05 * np.abs(data["photometry_flux"])), rtol=1e-14)
                        stored_fractions = np.asarray(stored["sfh/mass_fraction_draws"])
                        stored_ages = np.asarray(stored["sfh/mass_weighted_age_gyr"])
                    ratios = np.asarray(fit.samples["logsfr_ratios"])
                    sfr = softmax(np.c_[np.zeros(len(ratios)), -np.cumsum(ratios, axis=1)]
                                  * np.log(10.), axis=1)
                    mass = .5 * (sfr[:, :-1] + sfr[:, 1:]) * np.diff(times)
                    fractions = mass / mass.sum(axis=1)[:, None]
                    ages = fractions @ (.5 * (times[:-1] + times[1:]))
                    distance, index = cKDTree(fractions).query(stored_fractions)
                    assert distance.max() < 1e-11
                    np.testing.assert_allclose(ages[index], stored_ages, atol=1e-11, rtol=0)
                    ageq = e9.weighted_quantiles(ages, fit.log_weights, quantiles=[.16, .5, .84])
                    afe = e9.weighted_quantiles(np.asarray(fit.samples["afe"]).ravel(),
                                              fit.log_weights, quantiles=[.5])[0]
                    rows.append(make_row(arm, target, seed, truth, ageq, afe,
                                         str(raw.relative_to(ROOT)), references[(target, seed)], original_groups[target]))
                    cell = next(c for c in manifest["source"]["experiment"]
                                if c["arm"] == f"{arm}_s{seed}" and c["target"] == target)
                    assert cell["settings"]["rest_range"] == (REST_RANGE if arm in ("A", "B3") else None)
                    assert bool(cell["settings"]["abundance_response"]) == (arm == "B2")
                    assert cell["settings"]["fix_afe"] is None
                    prior = eval(cell["priors"]["logsfr_ratios"], {"StudentT": e9.StudentT})
                    assert float(prior.scale) == .3
                    checks.append(dict(arm=arm, target=target, noise_seed=seed,
                        validation=True, spectrum_pixels=int(mask.sum()),
                        raw_sha256=sha(raw), derived_sha256=sha(raw.with_name("ceridwen_derived_outputs.h5")),
                        source_commit=manifest["source"]["commit"],
                        stored_fraction_max_distance=float(distance.max()),
                        stored_age_max_error_gyr=float(np.max(np.abs(ages[index] - stored_ages)))))
            print(f"{part}/{target}: {len(arms) * len(SEEDS)} fits validated", flush=True)
    assert len(rows) == 150 and len(checks) == 120
    table(OUT / "per-mock.csv", rows)
    summarize_rows(rows)
    dump(OUT / "artifact-checks.json", dict(fits=checks, fits_validated=120,
        original_mock_hashes_unchanged=True, reference_P_csv_sha256=sha(PREVIOUS / "per-mock.csv"),
        injected_mock_hashes_unchanged=True, raw_response_hashes_unchanged=True,
        prior_script_unchanged=True, prior_manifest_unchanged=True))


def summarize_rows(rows):
    g = {r["target"]: r["original_with_Mgb"] for r in rows}
    truths = {t["target"]: t for t in previous_inputs()["truths"]}
    names = sorted(truths)
    z = np.array([truths[n]["redshift"] for n in names])
    true = np.array([truths[n]["true_age_gyr"] for n in names])
    group = np.array([g[n] for n in names], float)
    design = np.c_[np.ones(len(names)), z, group]
    true_coefficients, _, rank, _ = np.linalg.lstsq(design, true, rcond=None)
    assert rank == 3
    true_slope = float(np.polyfit(z, true, 1)[0])
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, len(names), (10000, len(names)))
    boot_z = z[indices]
    dz = boot_z - boot_z.mean(axis=1)[:, None]
    ranks = np.array([np.linalg.matrix_rank(design[i]) for i in indices])
    summaries, widths = [], []
    for arm in ("P9", "A", "B1", "B2", "B3"):
        selected = [r for r in rows if r["arm"] == arm]
        assert len(selected) == 30
        age = np.array([[next(float(r["age_q50"]) for r in selected
                              if r["target"] == n and int(r["noise_seed"]) == seed)
                         for seed in SEEDS] for n in names])
        mean_age = age.mean(axis=1)
        slope = float(np.polyfit(z, mean_age, 1)[0])
        boot_y = mean_age[indices]
        boot_slopes = np.sum(dz * (boot_y - boot_y.mean(axis=1)[:, None]), axis=1) / np.sum(dz**2, axis=1)
        q = np.quantile(boot_slopes, [.025, .975])
        coefficients = np.linalg.lstsq(design, mean_age, rcond=None)[0]
        # Twenty-one of these fixed bootstrap draws omit an estimable group contrast.
        step_boot = np.array([np.linalg.lstsq(design[i], mean_age[i], rcond=None)[0]
                              for i in indices[ranks == 3]])
        stepq = np.quantile(step_boot[:, 2], [.025, .975])
        summary = dict(arm=arm, galaxies=10, mocks=30, recovered_age_slope=slope,
            slope_bootstrap_q025=float(q[0]), slope_bootstrap_q975=float(q[1]),
            true_age_slope=true_slope, slope_ratio=slope / true_slope,
            median_age_bias_lower_z=float(np.median([float(r["age_bias_gyr"]) for r in selected
                                                     if float(r["redshift"]) < np.median(z)])),
            median_age_bias_upper_z=float(np.median([float(r["age_bias_gyr"]) for r in selected
                                                     if float(r["redshift"]) > np.median(z)])),
            median_age_bias_with_Mgb=float(np.median([float(r["age_bias_gyr"]) for r in selected if g[r["target"]]])),
            median_age_bias_without_Mgb=float(np.median([float(r["age_bias_gyr"]) for r in selected if not g[r["target"]]])),
            joint_intercept=float(coefficients[0]), joint_slope=float(coefficients[1]),
            Mgb_group_step=float(coefficients[2]), step_bootstrap_q025=float(stepq[0]),
            step_bootstrap_q975=float(stepq[1]), step_bootstrap_valid=int(np.sum(ranks == 3)),
            true_joint_slope=float(true_coefficients[1]), true_group_step=float(true_coefficients[2]),
            age_truth_inside=sum(r["age_truth_inside"] for r in selected),
            age_truth_inside_with_Mgb=sum(r["age_truth_inside"] for r in selected if g[r["target"]]),
            age_truth_inside_without_Mgb=sum(r["age_truth_inside"] for r in selected if not g[r["target"]]),
            median_afe_bias=float(np.median([float(r["afe_bias"]) for r in selected])))
        summaries.append(summary)
        for label, subgroup in (("all", selected),
                ("with_Mgb", [r for r in selected if g[r["target"]]]),
                ("without_Mgb", [r for r in selected if not g[r["target"]]])):
            widths.append(dict(arm=arm, original_coverage=label, mocks=len(subgroup),
                median_age_width_16_84_gyr=float(np.median([float(r["age_width_16_84_gyr"]) for r in subgroup])),
                median_P_width_16_84_gyr=float(np.median([float(r["P_age_width_16_84_gyr"]) for r in subgroup])),
                median_paired_width_ratio=float(np.median([float(r["width_ratio_to_P"]) for r in subgroup])),
                median_paired_width_difference_gyr=float(np.median([float(r["width_difference_from_P_gyr"]) for r in subgroup]))))
    table(OUT / "summary.csv", summaries)
    table(OUT / "width-comparison.csv", widths)
    dump(OUT / "bootstrap-method.json", dict(seed=BOOTSTRAP_SEED, draws=10000,
        interval="95% percentile", clusters="Ten galaxies, keeping all three noise realizations together.",
        estimator="Unweighted OLS on all 30 posterior median ages, equivalent to OLS on ten galaxy means.",
        step="age = a + b*z + c*g; g=1 originally with Mg b, 0 originally without, fixed across all arms.",
        step_bootstrap_valid=int(np.sum(ranks == 3)), step_bootstrap_nonidentified=int(np.sum(ranks != 3)),
        step_bootstrap_rule="Only full-rank three-column fits enter step intervals; all 10000 draws enter slope intervals.",
        true_group_step_gyr=float(true_coefficients[2]),
        true_step_note="The common cosmic-time history has no physical group offset; this tiny fitted linear step comes from curvature of age_universe(z)."))
    print(json.dumps(summaries), flush=True)


def report():
    """Append only the requested Experiment 10 section after validation."""
    summary = list(csv.DictReader((OUT / "summary.csv").open()))
    widths = list(csv.DictReader((OUT / "width-comparison.csv").open()))
    checks = json.loads((OUT / "artifact-checks.json").read_text())
    independent = json.loads((OUT / "independent-checks.json").read_text())
    modal = json.loads((OUT / "modal-state.json").read_text())
    assert checks["fits_validated"] == 120 and independent["passed"]
    assert not modal["own_containers"]
    assert all(app["state"] == "stopped" for app in modal["own_apps"])
    by_arm = {r["arm"]: r for r in summary}
    assert set(by_arm) == {"P9", "A", "B1", "B2", "B3"}
    f = lambda r, key, places=3: f'{float(r[key]):.{places}f}'
    signed = lambda r, key: f'{float(r[key]):+.3f}'
    interval = lambda r, key: (f'{float(r[key]):+.3f} '
        f'[{float(r["slope_bootstrap_q025"]):+.3f}, {float(r["slope_bootstrap_q975"]):+.3f}]')
    true_slope = float(summary[0]["true_age_slope"])
    text = ["\n## Experiment 10 results\n",
        "All 120 new recoveries use the ten Experiment 9 galaxies and three recorded noise seeds. "
        "P9 below is the existing Experiment 9 production arm; it was read without modification. "
        "Slopes have units Gyr per unit redshift, ages and age differences are Gyr, and abundance differences are dex.\n",
        "| Arm | Injected C/Fe, N/Fe | Recovery | Rest-frame vacuum window (A) | New fits |",
        "| --- | --- | --- | --- | ---: |",
        "| P9 | 0, 0 | Plain grid | Original coverage | 0 |",
        "| A | 0, 0 | Plain grid | 4155.0–4438.1 | 30 |",
        "| B1 | +0.15, +0.30 | Plain grid | Original coverage | 30 |",
        "| B2 | +0.15, +0.30 | C and N free | Original coverage | 30 |",
        "| B3 | +0.15, +0.30 | Plain grid | 4155.0–4438.1 | 30 |\n",
        f"The exact truth has a finite-sample OLS slope of {true_slope:+.6f}. "
        "Each interval below is a 95% galaxy-cluster bootstrap interval, not a posterior interval.\n",
        "| Arm | Recovered slope [95% bootstrap] | Recovered / true | True slope inside interval | Median alpha/Fe bias |",
        "| --- | ---: | ---: | --- | ---: |"]
    for r in summary:
        inside = float(r["slope_bootstrap_q025"]) <= true_slope <= float(r["slope_bootstrap_q975"])
        text.append(f'| {r["arm"]} | {interval(r, "recovered_age_slope")} | '
                    f'{f(r, "slope_ratio")} | {"yes" if inside else "no"} | {signed(r, "median_afe_bias")} |')
    text += [f'\nWith zero injected C/N, the common window recovers {float(by_arm["A"]["slope_ratio"]):.3f} '
        'of the true slope. Full-range C/N injection gives a more negative point slope than P9; '
        'C/N freedom brings it closer to truth. The interval-membership column gives the bootstrap '
        'comparison with the exact true slope for this ten-galaxy mock design.\n']
    text += ["\n| Arm | Age bias, lower z | Upper z | Originally with Mg b | Originally without Mg b | Age truth inside 16–84, all / with / without |",
        "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in summary:
        text.append(f'| {r["arm"]} | {signed(r, "median_age_bias_lower_z")} | '
            f'{signed(r, "median_age_bias_upper_z")} | {signed(r, "median_age_bias_with_Mgb")} | '
            f'{signed(r, "median_age_bias_without_Mgb")} | {r["age_truth_inside"]}/30 / '
            f'{r["age_truth_inside_with_Mgb"]}/15 / {r["age_truth_inside_without_Mgb"]}/15 |')
    text += ["\nThe lower and upper halves each contain five galaxies and fifteen noise realizations. "
        "The original five-with/five-without Mg b grouping stays fixed in every arm. "
        "The joint fit is age = a + b z + c g, with g = 1 originally with Mg b and g = 0 originally without. "
        "Thus c is with minus without at fixed redshift; it is distinct from a difference of the two median biases.\n",
        "| Arm | a | Joint slope b | Mg b group step c [95% bootstrap] |",
        "| --- | ---: | ---: | ---: |"]
    for r in summary:
        text.append(f'| {r["arm"]} | {f(r, "joint_intercept")} | {signed(r, "joint_slope")} | '
            f'{signed(r, "Mgb_group_step")} [{signed(r, "step_bootstrap_q025")}, '
            f'{signed(r, "step_bootstrap_q975")}] |')
    text += [f'\nThe same joint fit to exact true ages gives b = {float(summary[0]["true_joint_slope"]):+.6f} '
        f'and c = {float(summary[0]["true_group_step"]):+.6f}. The small nonzero true c comes from '
        "approximating the curved age-redshift relation by a plane, with a common formation history in both groups. "
        "Every recovered group-step 95% bootstrap interval includes zero.\n",
        "| Arm | Original Mg b coverage | Mocks | Median age width | Matching P9 width | Median paired width ratio | Median paired width difference |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in widths:
        text.append(f'| {r["arm"]} | {r["original_coverage"]} | {r["mocks"]} | '
            f'{f(r, "median_age_width_16_84_gyr")} | {f(r, "median_P_width_16_84_gyr")} | '
            f'{f(r, "median_paired_width_ratio")} | {signed(r, "median_paired_width_difference_gyr")} |')
    text += ["\nAge width is q84 minus q16. Ratios and differences are computed for each matching "
        "galaxy and seed before taking the median; a ratio of median widths is a different statistic.\n",
        f'A changes the recovered slope from P9 by '
        f'{float(by_arm["A"]["recovered_age_slope"]) - float(by_arm["P9"]["recovered_age_slope"]):+.3f}. '
        f'At full coverage the C/N injection changes the plain-grid slope by '
        f'{float(by_arm["B1"]["recovered_age_slope"]) - float(by_arm["P9"]["recovered_age_slope"]):+.3f}; '
        f'freeing C/N then changes it by '
        f'{float(by_arm["B2"]["recovered_age_slope"]) - float(by_arm["B1"]["recovered_age_slope"]):+.3f}. '
        f'In the common window the injection changes the slope from A to B3 by '
        f'{float(by_arm["B3"]["recovered_age_slope"]) - float(by_arm["A"]["recovered_age_slope"]):+.3f}.\n',
        "| Method or check | Recorded choice or result |",
        "| --- | --- |",
        "| Truth and noise | The Experiment 9 cosmic-time formation window [2.468870095056303, 3.468870095056303] Gyr, exact per-galaxy ages, grids, native masks, instrument, filters, statistical uncertainties, dust and dispersion are unchanged. Fine truth uses 102 bins, including 100 active 0.01 Gyr bins. Alpha/Fe is +0.2 and Fe/H is -0.2. The inherited truth has constant metallicity; production fitting retains metallicity evolution and 14 SFH ratio parameters. |",
        "| C/N injection | Only B injects +0.15 and +0.30 through the existing alf responses. At zero C/N, the fine-history mean spectrum and photometry are bitwise identical to Experiment 9 for all ten galaxies. All other original mock fields are bitwise unchanged. Enhanced-spectrum noise uses the same standardized Gaussian draws, photometry first then spectrum, and the same statistical-plus-floor recipe evaluated on the enhanced mean. |",
        "| Response resolution | Existing catalogue-dispersion response ratios and unchanged isochrones. Minimum total response sigma is 171.151–275.252 km/s across targets; none is below 100 km/s. The existing fixed-catalogue-sigma approximation is inherited. |",
        "| Inference | Production priors, SFH fast path, 500 live points, 65 inner steps, 100 deletions and logZ tolerance -5. SFH ratios retain StudentT scale 0.3 and df 2. Inference seed 20261110; noise seeds 20261111, 20261112, 20261113. No new sampler, notebook or model changes. |",
        "| Windows | A and B3 apply the notebook rest_range setting, inclusive 4155.0–4438.1 A on the native rest-frame vacuum grid, retaining all native mask holes. Photometry is unchanged between recovery windows. |",
        "| Posterior summaries | All weighted raw posterior samples determine age and alpha/Fe quantiles. SFH mass fractions and ages independently match the stored derived draws. Age coverage is the exact true formed-mass-weighted age inside q16–q84. |",
        "| Slopes and bootstrap | Unweighted OLS on thirty posterior median ages, equivalent to OLS on ten galaxy means. Same 10,000 galaxy-cluster resamples and seed 20261129 as Experiment 9, retaining all three seeds together. All resamples enter slope intervals; 9,979 full-rank resamples enter the group-step intervals, with 21 nonidentified steps excluded. |",
        "| Real-data reference | The read-only [135-galaxy report](../chronometer-135-2026-11-10/REPORT.md) gives -1.55 and +0.97 for the two 135-galaxy arms. Its -3.77 common-window result is arm (e), 130 valid galaxies, C/N free and alpha/Fe fixed +0.25. The requested mock arms here retain free alpha/Fe; they do not duplicate that extra fixed-alpha setting. |",
        "| Label repair | Only cfe and nfe entries were added to scripts/plot_prior_kl.py label(). Both original KeyErrors were reproduced. All seven existing test_plot_prior_kl.py tests pass; the real C/N caller also returns both abundance labels. No figures were generated. |",
        "| Validation | All 120 retrieved raw/derived fits pass the existing validator, input/mask/uncertainty checks and SFH-age checks. Original thirty Experiment 9 mock hashes and new thirty injected mock hashes remain unchanged; all 25 raw response files retain their recorded hashes. Independent slope, bootstrap, group-step, coverage and paired-width checks pass. All twenty owned Modal apps are stopped and no owned containers remain. |",
        f'| GPU provenance | Requested A100-40GB for every fit. Actual completed-fit GPU counts: {json.dumps(independent["actual_gpu_counts"], sort_keys=True)}. All remote bootstrap and fit exits are zero. |',
        "| Artifacts | [Per-mock results](slope-mismatch/per-mock.csv), [arm summary](slope-mismatch/summary.csv), [paired widths](slope-mismatch/width-comparison.csv), [inputs](slope-mismatch/inputs.json), [validation](slope-mismatch/artifact-checks.json), [independent checks](slope-mismatch/independent-checks.json), [Modal state](slope-mismatch/modal-state.json), [script](slope-mismatch/analyse.py). |",
        "| Noticed, not done | The pre-existing Ceridwen state-checker worktree error remains. No figures, wiki pages, notebook or model changes. |\n"]
    path = BASE / "REPORT.md"
    original = path.read_text()
    assert "## Experiment 10 results" not in original
    path.write_text(original + "\n".join(text))


def verify():
    """Check the saved tables using independent least-squares calculations."""
    rows = list(csv.DictReader((OUT / "per-mock.csv").open()))
    summaries = list(csv.DictReader((OUT / "summary.csv").open()))
    widths = list(csv.DictReader((OUT / "width-comparison.csv").open()))
    inputs = json.loads((OUT / "inputs.json").read_text())
    sources = json.loads((OUT / "source-checks.json").read_text())
    for name, digest in sources["sha256"].items():
        if "chronometer-135" not in name:  # Its owner may update this read-only reference.
            assert sha(ROOT / name) == digest, name
    names = sorted({r["target"] for r in rows})
    arms = [r["arm"] for r in summaries]
    assert arms == ["P9", "A", "B1", "B2", "B3"]
    z = np.array([next(float(r["redshift"]) for r in rows if r["target"] == n) for n in names])
    truth = np.array([next(float(r["true_age_gyr"]) for r in rows if r["target"] == n) for n in names])
    g = np.array([next(r["original_with_Mgb"] == "True" for r in rows if r["target"] == n)
                  for n in names], float)
    assert g.sum() == 5
    means = np.array([[np.mean([float(r["age_q50"]) for r in rows
                               if r["target"] == n and r["arm"] == arm])
                       for arm in arms] for n in names])
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, 10, (10000, 10))
    slopes, steps = [], []
    for index in indices:
        coefficients = lstsq(np.c_[np.ones(10), z[index]], means[index], lapack_driver="gelsy")[0]
        slopes.append(coefficients[1])
        coefficients, _, rank, _ = lstsq(np.c_[np.ones(10), z[index], g[index]],
                                        means[index], lapack_driver="gelsd")
        if rank == 3:
            steps.append(coefficients[2])
    slope_intervals = np.quantile(slopes, [.025, .975], axis=0)
    step_intervals = np.quantile(steps, [.025, .975], axis=0)
    assert len(steps) == 9979
    coefficient_errors, interval_errors = [], []
    for j, summary in enumerate(summaries):
        selected = [r for r in rows if r["arm"] == summary["arm"]]
        assert len(selected) == 30
        zz = np.array([float(r["redshift"]) for r in selected])
        yy = np.array([float(r["age_q50"]) for r in selected])
        gg = np.array([r["original_with_Mgb"] == "True" for r in selected], float)
        coefficients = lstsq(np.c_[np.ones(30), zz, gg], yy, lapack_driver="gelsy")[0]
        slope = linregress(zz, yy).slope
        np.testing.assert_allclose(slope, float(summary["recovered_age_slope"]), rtol=0, atol=1e-11)
        np.testing.assert_allclose(linregress(z, truth).slope, float(summary["true_age_slope"]),
                                   rtol=0, atol=1e-11)
        coefficient_errors.append(float(np.max(np.abs(coefficients - [float(summary[k]) for k in
                                  ("joint_intercept", "joint_slope", "Mgb_group_step")]))))
        np.testing.assert_allclose(coefficients, [float(summary[k]) for k in
                                  ("joint_intercept", "joint_slope", "Mgb_group_step")], rtol=0, atol=1e-10)
        for actual, keys in ((slope_intervals[:, j], ("slope_bootstrap_q025", "slope_bootstrap_q975")),
                             (step_intervals[:, j], ("step_bootstrap_q025", "step_bootstrap_q975"))):
            expected = np.array([float(summary[k]) for k in keys])
            interval_errors.append(float(np.max(np.abs(actual - expected))))
            np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-9)
        for r in selected:
            age, lo, hi, true = (float(r[k]) for k in ("age_q50", "age_q16", "age_q84", "true_age_gyr"))
            np.testing.assert_allclose(age - true, float(r["age_bias_gyr"]), rtol=0, atol=1e-14)
            np.testing.assert_allclose(hi - lo, float(r["age_width_16_84_gyr"]), rtol=0, atol=1e-14)
            assert (lo <= true <= hi) == (r["age_truth_inside"] == "True")
        assert sum(r["age_truth_inside"] == "True" for r in selected) == int(summary["age_truth_inside"])
        for key, selector in (
                ("median_age_bias_lower_z", lambda r: float(r["redshift"]) < np.median(z)),
                ("median_age_bias_upper_z", lambda r: float(r["redshift"]) > np.median(z)),
                ("median_age_bias_with_Mgb", lambda r: r["original_with_Mgb"] == "True"),
                ("median_age_bias_without_Mgb", lambda r: r["original_with_Mgb"] == "False")):
            subgroup = [r for r in selected if selector(r)]
            assert len(subgroup) == 15
            np.testing.assert_allclose(np.median([float(r["age_bias_gyr"]) for r in subgroup]),
                                       float(summary[key]), rtol=0, atol=1e-14)
        np.testing.assert_allclose(np.median([float(r["afe_bias"]) for r in selected]),
                                   float(summary["median_afe_bias"]), rtol=0, atol=1e-14)
        for suffix, flag in (("with_Mgb", "True"), ("without_Mgb", "False")):
            assert sum(r["age_truth_inside"] == "True" for r in selected if
                       r["original_with_Mgb"] == flag) == int(summary[f"age_truth_inside_{suffix}"])
        for label, selector in (("all", lambda r: True),
                ("with_Mgb", lambda r: r["original_with_Mgb"] == "True"),
                ("without_Mgb", lambda r: r["original_with_Mgb"] == "False")):
            subgroup = [r for r in selected if selector(r)]
            w, = [w for w in widths if w["arm"] == summary["arm"] and w["original_coverage"] == label]
            assert len(subgroup) == int(w["mocks"]) == (30 if label == "all" else 15)
            for outkey, inkey in (("median_age_width_16_84_gyr", "age_width_16_84_gyr"),
                    ("median_P_width_16_84_gyr", "P_age_width_16_84_gyr"),
                    ("median_paired_width_ratio", "width_ratio_to_P"),
                    ("median_paired_width_difference_gyr", "width_difference_from_P_gyr")):
                np.testing.assert_allclose(np.median([float(r[inkey]) for r in subgroup]), float(w[outkey]),
                                           rtol=0, atol=1e-14)
    assert all(float(r["width_ratio_to_P"]) == 1 and float(r["width_difference_from_P_gyr"]) == 0
               for r in rows if r["arm"] == "P9")
    gpu_names, exits, notebooks, images = {}, [], 0, 0
    for part in ("A", "B"):
        for manifest_path in (OUT / "runs" / part).glob("*/manifest.json"):
            manifest = json.loads(manifest_path.read_text())
            assert manifest["source"]["commit"] == (
                "c2f7fc149940741231d14241ac21f8af5f303255" if part == "A" else
                "4fe9d26803977e276fe157f551452dc4316295d5")
            for attempt in manifest["attempts"]:
                assert attempt["status"] == "complete"
                for cell in attempt["cells"].values():
                    assert cell["exit"] == {"bootstrap": 0, "fit": 0}
                    exits.append(cell["exit"])
                    name = cell["gpu_name"]
                    gpu_names[name] = gpu_names.get(name, 0) + 1
            for path in (manifest_path.parent / "fits").glob("*/*/*_executed.ipynb"):
                notebooks += 1
                document = json.loads(path.read_text())
                images += sum(any(key.startswith("image/") for key in output.get("data", {}))
                              for cell in document["cells"] for output in cell.get("outputs", []))
    assert len(exits) == notebooks == 120 and images == 0
    assert not list(OUT.rglob("*.png"))
    for record in previous_inputs()["mocks"] + inputs["mocks"]:
        assert sha(ROOT / record["path"]) == record["sha256"]
    for name, digest in inputs["response_sha256"].items():
        assert sha(ROOT / RESPONSE / name) == digest
    dump(OUT / "independent-checks.json", dict(passed=True, fits=120, reference_rows=30,
        independent_slopes="SciPy linregress on all thirty ages per arm",
        independent_bootstrap="SciPy QR and SVD least squares, same fixed galaxy clusters",
        maximum_coefficient_difference=float(max(coefficient_errors)),
        maximum_interval_difference=float(max(interval_errors)),
        identified_step_bootstraps=len(steps), posterior_coverage_and_paired_widths_verified=True,
        executed_notebooks=notebooks, embedded_images=images, png_files=0,
        requested_gpu="A100-40GB", actual_gpu_counts=gpu_names,
        remote_bootstrap_and_fit_exits_all_zero=True, mock_hashes_unchanged=True,
        raw_response_hashes_unchanged=True, frozen_reference_hashes_unchanged=True,
        read_only_real_report_initial_sha256=sources["sha256"]["results/chronometer-135-2026-11-10/REPORT.md"],
        read_only_real_report_final_sha256=sha(ROOT / "results/chronometer-135-2026-11-10/REPORT.md")))
    print(json.dumps(dict(passed=True, actual_gpu_counts=gpu_names)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["probe", "generate", "summarize", "verify", "report"])
    args = parser.parse_args()
    if args.step == "summarize":
        summarize()
    elif args.step == "report":
        report()
    elif args.step == "verify":
        verify()
    else:
        generate(first_only=args.step == "probe")


if __name__ == "__main__":
    main()
