#!/usr/bin/env python3
"""Experiment 9: production SFH prior, fine-time mocks, and chronometer recovery."""
from __future__ import annotations

import argparse
import contextlib
import csv
import gc
import hashlib
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
sys.path[:0] = [str(ROOT), str(ROOT / "ceridwen"), str(ROOT / "external/sedpy_jax")]
os.chdir(ROOT)

import h5py
import jax
import jax.numpy as jnp
import numpy as np
from scipy.special import softmax
from scipy.spatial import cKDTree

from ceridwen import Cosmology
from ceridwen.broadening import Kinematics
from ceridwen.cosmology import age_gyr
from ceridwen.csp import CSPBasis_afe
from ceridwen.fit import load_result_h5
from ceridwen.model import SedModel, logsfr_ratios_to_sfh
from ceridwen.sampler.priors import StudentT
from scripts.absorption_mask_report import weighted_quantiles
from scripts.run_ceridwen_vast_multi_gpu import _fit_notebook

COSMO = Cosmology.planck18()
NOISE_SEEDS = [20261111, 20261112, 20261113]
FIT_SEED = 20261110
PRIOR_SEED = 20261119
BOOTSTRAP_SEED = 20261129


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def table(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def targets():
    return json.loads((ROOT / "results/quiescent-test-set/targets.json").read_text())["targets"]


def baseline_rows():
    names = {t["spect_id"] for t in targets()}
    return [r for r in csv.DictReader((BASE / "exp3-per-galaxy.csv").open())
            if r["group"] == "legac" and r["arm"] == "baseline" and r["target"] in names]


def bins(universe_age):
    return np.array([0., 10**7.4772 / 1e9]
                    + (10**np.linspace(8., np.log10(universe_age * .85e9), 12) / 1e9).tolist()
                    + [universe_age])


def prior_only():
    """Common StudentT draws reduce Monte Carlo scatter between redshifts."""
    ratios = np.asarray(StudentT(mean=0., scale=.3, df=2.).sample(
        jax.random.PRNGKey(PRIOR_SEED), (200000, 14)))
    # The library's x64 transform can overflow on the unbounded StudentT tail.
    # Softmax removes only a common SFR normalisation, which cancels in the age.
    log_sfr = np.c_[np.zeros(len(ratios)), -np.cumsum(ratios, axis=1)] * np.log(10.)
    sfr = softmax(log_sfr, axis=1)
    small = ratios[:100]
    tcheck = bins(float(age_gyr(.7, COSMO)))
    reference = np.asarray(jax.vmap(lambda x: logsfr_ratios_to_sfh(x, tcheck * 1e9))(small))
    stable = sfr[:100] / np.sum(.5 * (sfr[:100, :-1] + sfr[:100, 1:])
                                * np.diff(tcheck)[None, :] * 1e9, axis=1)[:, None]
    np.testing.assert_allclose(stable, reference, rtol=1e-12, atol=1e-25)
    test_names = {t["spect_id"] for t in targets()}
    manifest = json.loads((ROOT / "results/dr2-refit-2026-10-12/targets.json").read_text())
    sources = [(t["spect_id"], ROOT / "results/dr2-refit-2026-10-12" / t["folder"]
                / "ceridwen_derived_outputs.h5", True) for t in manifest["targets"]]
    parent_names = {t[0] for t in sources}
    # The test-set galaxy M5_238314 is absent from the October 135 selection.
    sources += [(r["target"], (BASE / r["result_path"]).with_name("ceridwen_derived_outputs.h5"), False)
                for r in baseline_rows() if r["target"] not in parent_names]
    rows = []
    for target_name, derived, parent_member in sources:
        with h5py.File(derived, "r") as stored:
            z = float(stored.attrs["redshift"])
            native_bins = np.asarray(stored["sfh/lookback_time_gyr"])
        tuniv = float(age_gyr(z, COSMO))
        times = bins(tuniv)
        np.testing.assert_allclose(times, native_bins, rtol=0, atol=1e-12)
        masses = .5 * (sfr[:, :-1] + sfr[:, 1:]) * np.diff(times)
        ages = (masses @ (.5 * (times[:-1] + times[1:]))) / masses.sum(axis=1)
        quantiles = np.quantile(ages, [.16, .5, .84])
        rows.append(dict(target=target_name, redshift=z, october_135=parent_member,
                         test_set=target_name in test_names, universe_age_gyr=tuniv,
                         prior_age_q16=quantiles[0], prior_age_q50=quantiles[1], prior_age_q84=quantiles[2],
                         dt_univ_dz=float(jax.grad(lambda zz: age_gyr(zz, COSMO))(z))))
    table(OUT / "prior-per-galaxy.csv", rows)
    summaries = []
    for name, selected in (("all135", [r for r in rows if r["october_135"]]),
                           ("test10", [r for r in rows if r["test_set"]])):
        z = np.array([r["redshift"] for r in selected])
        summaries.append(dict(sample=name, galaxies=len(z), median_redshift=float(np.median(z)),
                              prior_median_age_slope=float(np.polyfit(z, [r["prior_age_q50"] for r in selected], 1)[0]),
                              universe_age_ols_slope=float(np.polyfit(z, [r["universe_age_gyr"] for r in selected], 1)[0]),
                              dt_univ_dz_at_median=float(jax.grad(lambda zz: age_gyr(zz, COSMO))(np.median(z)))))
    table(OUT / "prior-slopes.csv", summaries)
    dump(OUT / "prior-method.json", dict(draws=len(ratios), seed=PRIOR_SEED, scale=.3, df=2.,
         ratios=14, common_draws_across_redshifts=True, cosmology=COSMO.to_dict(),
         stable_transform_reference_max_relative_error=float(np.max(np.abs(stable / reference - 1))),
         estimator="Unweighted OLS of each galaxy's prior median mass-weighted age against catalog redshift.",
         stable_transform="scipy softmax of cumulative log SFR; common scaling cancels; no truncation of StudentT tails."))
    print(json.dumps(summaries), flush=True)


def assemble(row):
    raw = BASE / row["result_path"]
    manifest = json.loads((raw.parent.parents[2] / "manifest.json").read_text())
    cell = next(c for c in manifest["source"]["experiment"]
                if c["target"] == row["target"] and c["arm"] == "baseline")
    settings = dict(cell["settings"], ssp_grid=manifest["source"]["grid"], mock_data=None,
                    abundance_response=None)
    os.environ.update(CERIDWEN_TARGET_ID=row["target"],
                      CERIDWEN_MANIFEST_INDEX=str(cell["target_metadata"]["manifest_index"]),
                      CERIDWEN_RANDOM_SEED=str(FIT_SEED),
                      CERIDWEN_RESULT_DIR=str(OUT / "assembly" / row["target"]))
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        doc = _fit_notebook(json.dumps(settings), json.dumps({
            "logsfr_ratios": "StudentT(mean=0.0, scale=1.0, df=2.0)"}))
        for index, cell in enumerate(doc.cells[:9]):
            if cell.cell_type == "code":
                exec(compile(cell.source, f"production-cell-{index}", "exec"), ns)
    assert ns["joint_csp"].sfh_basis_fastpath
    assert float(ns["joint_priors"]["logsfr_ratios"].scale) == 1.
    np.testing.assert_allclose(ns["lookback_template"], bins(float(ns["universe_age"])), atol=0, rtol=0)
    fit = load_result_h5(raw)
    medians = {}
    for name, values in fit.samples.items():
        flat = np.asarray(values).reshape(len(fit.log_weights), -1)
        medians[name] = np.array([weighted_quantiles(flat[:, k], fit.log_weights)[2]
                                 for k in range(flat.shape[1])])
    return ns, medians, raw


def truth_prediction(ns, medians, formation_middle, step=.01):
    tuniv = float(ns["universe_age"])
    younger = tuniv - formation_middle - .5
    older = younger + 1.
    assert 0 < younger < older < tuniv
    active_edges = np.linspace(younger, older, round(1 / step) + 1)
    times = np.r_[0., active_edges, tuniv]
    # CSP spectra are per formed mass: integrate to one Msun before logmass.
    history = np.r_[0., np.ones(len(active_edges) - 1), 0.] / 1e9
    np.testing.assert_allclose(np.sum(history * np.diff(times) * 1e9), 1., rtol=1e-14)
    masses = history * np.diff(times)
    exact_age = float(masses @ (.5 * (times[:-1] + times[1:])) / masses.sum())
    np.testing.assert_allclose(exact_age, tuniv - formation_middle, atol=2e-15, rtol=0)
    transforms = {k: v for k, v in ns["joint_transforms"].items()
                  if k in ("diffuse_c_r", "tau_pow", "alpha_pow")}
    theta = {"lookback_time": jnp.asarray(times), "sfh": jnp.asarray(history),
             "logzsol": jnp.array([-.2]), "afe": jnp.array([.2]),
             "diffuse_tau_noll": jnp.asarray(medians["diffuse_tau_noll"]),
             "diffuse_delta": jnp.asarray(medians["diffuse_delta"])}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        csp = CSPBasis_afe(ns["ssp"], theta=theta, zh_const=True, sfh_interp="step",
                           add_dust=ns["SETTINGS"]["birth_cloud_dust"], add_diffuse_dust=True,
                           diffuse_law="noll", add_dust_emission=False, add_igm=False,
                           track_zred_age=False, cosmo=COSMO, verbose=False)
        free = {k: jnp.asarray(medians[k]) for k in
                ("logmass", "diffuse_Ebump", "dust_ratio") if k in medians}
        model = SedModel(csp, observations=[ns["phot_obs"], ns["spectrum_obs"]],
                         transforms=transforms, free_param_init=free,
                         zred=float(ns["z_catalog"]),
                         kinematics=Kinematics(sigma_gal=float(medians["sigma_smooth"][0])),
                         broaden_photometry=False)
        weights = csp.calculate_ssp_weights(model.apply_transforms(model.theta_init))
        np.testing.assert_allclose(np.sum(weights), 1., rtol=1e-7)
        prediction = {k: np.asarray(v) for k, v in model.predict(model.theta_init).items()}
    for value in prediction.values():
        assert np.all(np.isfinite(value))
    return prediction, exact_age, times, history


def generate(first_only=False):
    rows = baseline_rows()
    ages, redshifts = [], []
    for row in rows:
        with h5py.File((BASE / row["result_path"]).with_name("ceridwen_derived_outputs.h5"), "r") as stored:
            ages.append(float(np.median(stored["sfh/mass_weighted_age_gyr"])))
            redshifts.append(float(stored.attrs["redshift"]))
    zmed, baseline_age = float(np.median(redshifts)), float(np.median(ages))
    formation_middle = float(age_gyr(zmed, COSMO)) - baseline_age
    manifest = dict(source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                    ceridwen_commit=subprocess.check_output(["git", "-C", "ceridwen", "rev-parse", "HEAD"], text=True).strip(),
                    median_redshift=zmed, median_baseline_age_gyr=baseline_age,
                    formation_start_gyr=formation_middle - .5, formation_end_gyr=formation_middle + .5,
                    fine_active_bin_gyr=.01, noise_seeds=NOISE_SEEDS, fit_seed=FIT_SEED,
                    cosmology=COSMO.to_dict(), truths=[], mocks=[],
                    noise="Experiment 4: independent Gaussian photometry then spectral draws; model-scaled baseline spectral floor, 5% photometric floor; retain original statistical uncertainties and native validity.",
                    choices="Constant truth [Fe/H]=-0.2; [alpha/Fe]=+0.2; no C/N; catalog redshift; baseline median logmass, dust, dispersion and log_f_calib; calibration unity, emission zero. Truth SFH normalised to one formed Msun before logmass scaling. Production evolving-metallicity recovery unchanged.")
    (OUT / "mocks").mkdir(exist_ok=True)
    for row in rows[:1] if first_only else rows:
        ns, medians, raw = assemble(row)
        prediction, exact_age, times, history = truth_prediction(ns, medians, formation_middle)
        convergence = None
        if row == rows[0]:
            half, age2, _, _ = truth_prediction(ns, medians, formation_middle, .005)
            convergence = {k: float(np.max(np.abs(half[k] - prediction[k])) / np.max(np.abs(prediction[k])))
                           for k in prediction}
            assert max(convergence.values()) < 2e-6
            np.testing.assert_allclose(age2, exact_age, atol=2e-15, rtol=0)
        truth = dict(target=row["target"], redshift=float(ns["z_catalog"]),
                     true_age_gyr=exact_age, baseline_age_gyr=ages[rows.index(row)],
                     baseline_result=str(raw.relative_to(ROOT)), baseline_sha256=sha(raw),
                     baseline_derived_sha256=sha(raw.with_name("ceridwen_derived_outputs.h5")),
                     median_parameters={k: v.tolist() for k, v in medians.items()},
                     time_edges_gyr=times.tolist(), sfh_per_bin=history.tolist(),
                     refinement_relative_max_error=convergence,
                     recovery_sfh_bins=int(ns["N_RATIOS"]), recovery_fastpath=bool(ns["joint_csp"].sfh_basis_fastpath),
                     widened_prior_config_verified=True,
                     spectrum_mask_sha256=hashlib.sha256(np.asarray(ns["spectrum_mask"]).tobytes()).hexdigest())
        manifest["truths"].append(truth)
        phot_stat = np.asarray(ns["phot_error_stat"])
        spec_stat = np.asarray(ns["native_uncertainty"])
        phot_sigma = np.hypot(phot_stat, ns["SETTINGS"]["photometry_floor"] * np.abs(prediction["photometry"]))
        spec_sigma = np.hypot(spec_stat, np.exp(medians["log_f_calib"][0]) * np.abs(prediction["spectrum"]))
        valid = np.asarray(ns["native_valid"])
        arms = {}
        for seed in NOISE_SEEDS:
            rng = np.random.default_rng(seed)
            photo = prediction["photometry"] + rng.standard_normal(phot_sigma.shape) * phot_sigma
            spec = prediction["spectrum"] + np.where(valid, rng.standard_normal(spec_sigma.shape) * spec_sigma, 0.)
            path = OUT / "mocks" / f'{row["target"]}_s{seed}.npz'
            np.savez_compressed(path, photometry_flux=photo, photometry_uncertainty=phot_stat,
                                spectrum_flux=spec, spectrum_uncertainty=spec_stat, native_valid=valid,
                                mean_photometry=prediction["photometry"], mean_spectrum=prediction["spectrum"],
                                photometry_noise_sigma=phot_sigma, spectrum_noise_sigma=spec_sigma,
                                spectrum_wave=np.asarray(ns["spectrum_wave"]),
                                filter_names=np.asarray(ns["FILTER_NAMES"]),
                                spectrum_mask=np.asarray(ns["spectrum_mask"]), target_id=row["target"],
                                true_age_gyr=exact_age, noise_seed=seed,
                                time_edges_gyr=times, sfh_per_bin=history,
                                photometry_unit="maggies", spectrum_unit="erg s-1 cm-2 Hz-1",
                                wavelength_unit="Angstrom (vacuum observed)")
            relative = str(path.relative_to(ROOT))
            manifest["mocks"].append(dict(target=row["target"], noise_seed=seed, path=relative, sha256=sha(path)))
            for arm in ("P", "W"):
                arms[f"{arm}_s{seed}"] = {"settings": {"mock_data": relative}}
                if arm == "W":
                    arms[f"{arm}_s{seed}"]["priors"] = {"logsfr_ratios": "StudentT(mean=0.0, scale=1.0, df=2.0)"}
        dump(OUT / f'{row["target"]}.json', dict(targets=[row["target"]], seed=FIT_SEED,
             settings={"abundance_response": None}, priors={}, arms=arms))
        print(f'{row["target"]}: true age {exact_age:.9f} Gyr; {len(times)-1} truth bins; refinement {convergence}', flush=True)
        del ns, prediction
        gc.collect()
        jax.clear_caches()
    dump(OUT / ("probe-inputs.json" if first_only else "inputs.json"), manifest)


def summarize():
    from scripts.experiment import validate_result

    inputs = json.loads((OUT / "inputs.json").read_text())
    truths = {t["target"]: t for t in inputs["truths"]}
    for mock in inputs["mocks"]:
        assert sha(ROOT / mock["path"]) == mock["sha256"]
    for truth in truths.values():
        raw = ROOT / truth["baseline_result"]
        assert sha(raw) == truth["baseline_sha256"]
        assert sha(raw.with_name("ceridwen_derived_outputs.h5")) == truth["baseline_derived_sha256"]
    rows, checks = [], []
    for target, truth in truths.items():
        run = OUT / "runs" / target
        manifest = json.loads((run / "manifest.json").read_text())
        assert set(manifest["completed_cells"]) == {
            f"{arm}_s{seed}/{target}" for arm in ("P", "W") for seed in NOISE_SEEDS}
        for arm in ("P", "W"):
            for seed in NOISE_SEEDS:
                directory, = (run / "fits" / f"{arm}_s{seed}").iterdir()
                validate_result(directory)
                raw = directory / "ceridwen_result.h5"
                fit = load_result_h5(raw)
                assert not ({"cfe", "nfe"} & set(fit.samples))
                assert np.asarray(fit.samples["logsfr_ratios"]).shape[1:] == (14,)
                with h5py.File(directory / "ceridwen_derived_outputs.h5", "r") as stored:
                    times = np.asarray(stored["sfh/lookback_time_gyr"])
                    assert int(stored.attrs["random_seed"]) == FIT_SEED
                    assert np.isclose(float(stored.attrs["redshift"]), truth["redshift"], atol=1e-10, rtol=0)
                    assert hashlib.sha256(np.asarray(stored["spectrum/mask"]).tobytes()).hexdigest() == truth["spectrum_mask_sha256"]
                    data = np.load(OUT / "mocks" / f"{target}_s{seed}.npz")
                    np.testing.assert_array_equal(stored["spectrum/wavelength"], data["spectrum_wave"])
                    # Production replaces invalid-pixel uncertainties with 1; those pixels remain excluded.
                    np.testing.assert_array_equal(stored["spectrum/uncertainty"], np.where(
                        data["native_valid"], data["spectrum_uncertainty"], 1.))
                    np.testing.assert_allclose(stored["photometry/uncertainty"], np.hypot(
                        data["photometry_uncertainty"], .05 * np.abs(data["photometry_flux"])), rtol=1e-14)
                    with h5py.File((ROOT / truth["baseline_result"]).with_name("ceridwen_derived_outputs.h5"), "r") as baseline:
                        np.testing.assert_array_equal(stored["photometry/mask"], baseline["photometry/mask"])
                        np.testing.assert_array_equal(baseline["spectrum/wavelength"], data["spectrum_wave"])
                        np.testing.assert_array_equal(baseline["spectrum/mask"], data["spectrum_mask"])
                        np.testing.assert_array_equal(baseline["spectrum/uncertainty"], np.where(
                            data["native_valid"], data["spectrum_uncertainty"], 1.))
                    for group, name in (("spectrum", "spectrum_flux"), ("photometry", "photometry_flux")):
                        np.testing.assert_array_equal(np.asarray(stored[f"{group}/observed"]), data[name])
                    derived_age = np.quantile(np.asarray(stored["sfh/mass_weighted_age_gyr"]), [.16, .5, .84])
                    stored_ages = np.asarray(stored["sfh/mass_weighted_age_gyr"])
                    stored_fractions = np.asarray(stored["sfh/mass_fraction_draws"])
                # All weighted posterior samples, with the production mass-age definition.
                ratios = np.asarray(fit.samples["logsfr_ratios"])
                sfr = softmax(np.c_[np.zeros(len(ratios)), -np.cumsum(ratios, axis=1)] * np.log(10.), axis=1)
                masses = .5 * (sfr[:, :-1] + sfr[:, 1:]) * np.diff(times)
                ages = masses @ (.5 * (times[:-1] + times[1:])) / masses.sum(axis=1)
                fractions = masses / masses.sum(axis=1)[:, None]
                distances, indices = cKDTree(fractions).query(stored_fractions)
                assert np.max(distances) < 1e-11
                np.testing.assert_allclose(ages[indices], stored_ages, atol=1e-11, rtol=0)
                ageq = weighted_quantiles(ages, fit.log_weights, quantiles=[.16, .5, .84])
                row = dict(arm=arm, target=target, noise_seed=seed, redshift=truth["redshift"],
                           true_age_gyr=truth["true_age_gyr"], age_q16=ageq[0], age_q50=ageq[1],
                           age_q84=ageq[2], age_bias_gyr=ageq[1] - truth["true_age_gyr"],
                           age_truth_inside=ageq[0] <= truth["true_age_gyr"] <= ageq[2])
                for param, true in (("afe", .2), ("logzsol", -.2)):
                    q = weighted_quantiles(np.asarray(fit.samples[param]).ravel(), fit.log_weights,
                                           quantiles=[.16, .5, .84])
                    row.update({f"{param}_q50": q[1], f"{param}_bias": q[1] - true})
                row.update(result_path=str(raw.relative_to(ROOT)))
                rows.append(row)
                cell = next(c for c in manifest["source"]["experiment"]
                            if c["arm"] == f"{arm}_s{seed}" and c["target"] == target)
                expected_scale = ".3" if arm == "P" else "1.0"
                expected = StudentT(mean=0., scale=float(expected_scale), df=2.)
                # Expressions are frozen in the runner's source manifest.
                resolved = eval(cell["priors"]["logsfr_ratios"], {"StudentT": StudentT})
                assert float(resolved.scale) == float(expected.scale)
                checks.append(dict(arm=arm, target=target, noise_seed=seed, validation=True,
                                   raw_sha256=sha(raw), derived_sha256=sha(raw.with_name("ceridwen_derived_outputs.h5")),
                                   source_commit=manifest["source"]["commit"],
                                   stored_sfh_fraction_max_distance=float(np.max(distances)),
                                   stored_age_max_error_gyr=float(np.max(np.abs(ages[indices] - stored_ages))),
                                   age_quantiles_400_equal_draws=derived_age.tolist(),
                                   age_quantiles_all_weighted=ageq))
    assert len(rows) == 60
    table(OUT / "per-mock.csv", rows)
    summaries = []
    for arm in ("P", "W"):
        selected = [r for r in rows if r["arm"] == arm]
        names = sorted(truths)
        z = np.array([truths[n]["redshift"] for n in names])
        true = np.array([truths[n]["true_age_gyr"] for n in names])
        age = np.array([[next(r["age_q50"] for r in selected
                             if r["target"] == n and r["noise_seed"] == seed)
                         for seed in NOISE_SEEDS] for n in names])
        mean_age = age.mean(axis=1)
        slope = float(np.polyfit(z, mean_age, 1)[0])
        true_slope = float(np.polyfit(z, true, 1)[0])
        rng = np.random.default_rng(BOOTSTRAP_SEED)
        indices = rng.integers(0, len(names), (10000, len(names)))
        bootz, booty = z[indices], mean_age[indices]
        dz, dy = bootz - bootz.mean(axis=1)[:, None], booty - booty.mean(axis=1)[:, None]
        boot = np.sum(dz * dy, axis=1) / np.sum(dz**2, axis=1)
        q = np.quantile(boot, [.025, .975])
        summaries.append(dict(arm=arm, galaxies=len(names), mocks=len(selected),
             true_age_slope=true_slope, recovered_age_slope=slope, slope_bootstrap_q025=q[0],
             slope_bootstrap_q975=q[1], slope_ratio=slope / true_slope,
             dt_univ_dz_at_median=float(jax.grad(lambda zz: age_gyr(zz, COSMO))(np.median(z))),
             median_age_bias_lower_z=float(np.median([r["age_bias_gyr"] for r in selected if r["redshift"] < np.median(z)])),
             median_age_bias_upper_z=float(np.median([r["age_bias_gyr"] for r in selected if r["redshift"] > np.median(z)])),
             age_truth_inside=sum(r["age_truth_inside"] for r in selected),
             median_afe_bias=float(np.median([r["afe_bias"] for r in selected])),
             median_feh_bias=float(np.median([r["logzsol_bias"] for r in selected]))))
    table(OUT / "recovery-slopes.csv", summaries)
    dump(OUT / "artifact-checks.json", dict(fits=checks, input_hashes_unchanged=True,
         baseline_hashes_unchanged=True, bootstrap_seed=BOOTSTRAP_SEED, bootstrap_draws=10000,
         bootstrap="95% percentile interval; resample the ten galaxies as clusters, keeping each galaxy's three noise recoveries together. OLS on all 30 ages equals OLS on each galaxy's mean of its three posterior medians."))
    print(json.dumps(summaries), flush=True)


def report():
    """Append the requested section only after every recovery is validated."""
    prior = list(csv.DictReader((OUT / "prior-slopes.csv").open()))
    all_prior = {r["target"]: r for r in csv.DictReader((OUT / "prior-per-galaxy.csv").open())}
    recoveries = list(csv.DictReader((OUT / "per-mock.csv").open()))
    slopes = list(csv.DictReader((OUT / "recovery-slopes.csv").open()))
    inputs = json.loads((OUT / "inputs.json").read_text())
    checks = json.loads((OUT / "artifact-checks.json").read_text())
    assert len(checks["fits"]) == 60 and all(r["validation"] for r in checks["fits"])
    lines = ["\n## Experiment 9 results\n",
             "Production SFH prior and a common cosmic-time formation history. "
             "All slopes below are in Gyr per unit redshift; ages are in Gyr and abundances in dex.\n",
             "| Sample | N | Prior median-age slope | Universe-age OLS slope | d(t_univ)/dz at median z | Prior / universe OLS |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in prior:
        ratio = float(r["prior_median_age_slope"]) / float(r["universe_age_ols_slope"])
        lines.append(f'| {r["sample"]} | {r["galaxies"]} | {float(r["prior_median_age_slope"]):.6f} | '
                     f'{float(r["universe_age_ols_slope"]):.6f} | {float(r["dt_univ_dz_at_median"]):.6f} | {ratio:.4f} |')
    lines += ["", "The prior-only median-age slope is about 44% of the universe-age slope. "
              "The complete [prior table](prior-slope/prior-per-galaxy.csv) contains the 135 October galaxies "
              "and the extra test-set member M5_238314, which is absent from that October selection.\n",
              "| Arm | Recovered slope [95% bootstrap] | True OLS slope | Recovered / true | Median age bias, lower z | Median age bias, upper z | Age truth within 16–84 | Median alpha/Fe bias | Median Fe/H bias |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for r in slopes:
        lines.append(f'| {r["arm"]} | {float(r["recovered_age_slope"]):.5f} '
                     f'[{float(r["slope_bootstrap_q025"]):.5f}, {float(r["slope_bootstrap_q975"]):.5f}] | '
                     f'{float(r["true_age_slope"]):.5f} | {float(r["slope_ratio"]):.4f} | '
                     f'{float(r["median_age_bias_lower_z"]):+.5f} | {float(r["median_age_bias_upper_z"]):+.5f} | '
                     f'{r["age_truth_inside"]}/30 | {float(r["median_afe_bias"]):+.5f} | {float(r["median_feh_bias"]):+.5f} |')
    by_arm = {r["arm"]: r for r in slopes}
    p, w = by_arm["P"], by_arm["W"]
    assert all(float(r["slope_bootstrap_q025"]) < float(r["true_age_slope"])
               < float(r["slope_bootstrap_q975"]) for r in slopes)
    lines += ["", f'These mocks do not establish flattening of the recovered slope. '
              f'Production P recovers {float(p["slope_ratio"]):.3f} times the true slope; '
              f'the wider prior W recovers {float(w["slope_ratio"]):.3f}. '
              'Both 95% bootstrap intervals include the true slope. '
              'The wider prior reduces the positive age offset in both redshift halves; '
              'its slope point estimate is steeper and farther from truth.\n',
              "| Item | Definition or check |", "| --- | --- |",
              "| Prior draws | 200,000 production StudentT ratio vectors: mean 0, scale 0.3, df 2; seed 20261119. The same vectors are used at every redshift. Fourteen ratios define the notebook's fifteen time nodes. No tail clipping. scipy softmax removes a common SFR normalisation to avoid overflow; 100 draws agree with the production transform to relative tolerance 1e-12. |",
              "| Prior slope | Unweighted OLS of each galaxy's prior median mass-weighted age against catalog redshift. The universe-age OLS column uses the same redshifts; the derivative column is the tangent at their median. |",
              "| Cosmology and bins | The [production notebook](../../notebooks/ceridwen_integrated_photometry_spectra.ipynb) uses [age_gyr and Cosmology.planck18](../../ceridwen/ceridwen/cosmology.py); identical parameters and 14-bin construction. Per-galaxy fitting bins match the stored production bins. The derivative agrees with a central finite difference to relative tolerance 1e-8. The true age curve is t_univ(z) minus a constant; recovery ratios use its OLS slope over the same ten redshifts. |",
              f'| Formation window | Constant star formation from cosmic time {inputs["formation_start_gyr"]:.9f} to {inputs["formation_end_gyr"]:.9f} Gyr. At median z = {inputs["median_redshift"]:.9f}, the exact true age equals the test-set median baseline age, {inputs["median_baseline_age_gyr"]:.9f} Gyr. Baseline ages use the stored 400 equal-weight SFH draws, as in Experiment 8. |',
              "| Fine truth | Existing [CSPBasis_afe](../../ceridwen/ceridwen/csp/csp_afe.py) and [per-bin step integration](../../ceridwen/ceridwen/csp/csp.py): 100 active bins of 0.01 Gyr with exact window boundaries, plus two empty intervals. SFH integrates to one formed solar mass before baseline logmass scaling. The exact formed-mass age is the window midpoint in lookback time. Halving active bins to 0.005 Gyr for M1 changes the spectrum by 9.42e-7 and photometry by 2.10e-7 of their respective maximum fluxes. The SSP age grid and isochrones remain unchanged. |",
              "| Truth and observations | alpha/Fe +0.2, constant Fe/H -0.2, no C/N. Each galaxy retains its native wavelength grid, instrument, filters, masks and statistical uncertainties. Dust, dispersion, logmass and spectral fractional floor use that galaxy's weighted baseline medians. Catalog redshift; unity calibration; zero emission amplitudes. |",
              "| Noise | Experiment 4 recipe: independent Gaussian bands then pixels, baseline model-scaled spectral floor and 5% photometry floor. Seeds 20261111, 20261112, 20261113; RNG restarts for each galaxy, so standardized noise is shared by seed on native indices. Recovery retains original statistical uncertainties and production floor rules. Every saved draw was independently reproduced exactly. |",
              "| Recovery arms | P: unchanged production StudentT scale 0.3. W: only priors.logsfr_ratios = StudentT(mean=0.0, scale=1.0, df=2.0) through the existing experiment config. Both use production settings, plain grid, analytic linear nuisances, fast SFH basis, 500 live points, 65 inner steps, 100 deletes and logZ tolerance -5; inference seed 20261110, A100-40GB. No notebook or model source changes. |",
              "| Age and abundance summaries | Recovery quantiles use all weighted posterior samples, with the production formed-mass age definition. Intervals are 16–84%. Bias is posterior median minus truth. Fe/H is the sampled formed-mass mean metallicity coordinate. |",
              "| Slope and bootstrap | OLS on all 30 posterior median ages, equivalent to OLS on each galaxy's mean across three noise seeds. 10,000 cluster bootstrap draws resample ten galaxies, keeping each galaxy's three noise realizations together; seed 20261129, 95% percentile interval. Lower and upper halves contain five galaxies each, split at median catalog redshift. |",
              "| Scope of comparison | Fine-time constant-metallicity truth is recovered with the coarser production evolving-metallicity model. Both arms share those differences; their only recovery setting difference is SFH prior scale. The bootstrap describes these ten targets and three fixed noise realizations. |",
              "| Validation | All sixty fits pass local artifact validation and stored diagnostics. Native grids, masks, statistical errors and production photometry floors match the inputs. Stored SFH draws match the full-sample age calculation within 8.9e-15 Gyr. All sixty cells requested A100-40GB and exit zero. Modal supplied 56 A100-SXM4-40GB and four A100-SXM4-80GB allocations. All ten own apps are stopped; zero own containers, zero billed cost. |",
              "| Artifacts | [Inputs and exact histories](prior-slope/inputs.json), [per-mock recoveries](prior-slope/per-mock.csv), [slopes](prior-slope/recovery-slopes.csv), [validation](prior-slope/artifact-checks.json), [script](prior-slope/analyse.py). Thirty immutable NPZ inputs and all sixty retrieved fits are in prior-slope/. |",
              "| Noticed, not done | No changes to shared model/notebook code or production defaults. No figures or wiki pages. The pre-existing state-checker worktree error remains. |", "",
              "| Galaxy | z | Prior age 16 / 50 / 84 | Exact mock age | Baseline age |",
              "| --- | ---: | ---: | ---: | ---: |"]
    for t in sorted(inputs["truths"], key=lambda t: t["redshift"]):
        r = all_prior[t["target"]]
        lines.append(f'| {t["target"]} | {t["redshift"]:.6f} | {float(r["prior_age_q16"]):.5f} / '
                     f'{float(r["prior_age_q50"]):.5f} / {float(r["prior_age_q84"]):.5f} | '
                     f'{t["true_age_gyr"]:.9f} | {t["baseline_age_gyr"]:.5f} |')
    for arm in ("P", "W"):
        lines += ["", f"Arm {arm}.\n", "| Galaxy | Noise seed | True age | Recovered age [16–84] | Age bias | Truth inside | alpha/Fe | alpha/Fe bias | Fe/H | Fe/H bias |",
                  "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |"]
        for r in sorted((r for r in recoveries if r["arm"] == arm), key=lambda r: (float(r["redshift"]), r["noise_seed"])):
            lines.append(f'| {r["target"]} | {r["noise_seed"]} | {float(r["true_age_gyr"]):.5f} | '
                         f'{float(r["age_q50"]):.5f} [{float(r["age_q16"]):.5f}, {float(r["age_q84"]):.5f}] | '
                         f'{float(r["age_bias_gyr"]):+.5f} | {"yes" if r["age_truth_inside"] == "True" else "no"} | '
                         f'{float(r["afe_q50"]):+.5f} | {float(r["afe_bias"]):+.5f} | '
                         f'{float(r["logzsol_q50"]):+.5f} | {float(r["logzsol_bias"]):+.5f} |')
    path = BASE / "REPORT.md"
    old = path.read_text()
    assert "## Experiment 9 results" not in old
    path.write_text(old + "\n".join(lines) + "\n")
    print("Appended Experiment 9 results.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["prior", "probe", "generate", "summarize", "report"])
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.step == "report":
        report()
    elif args.step == "summarize":
        summarize()
    elif args.step == "prior":
        prior_only()
    else:
        generate(args.step == "probe")


if __name__ == "__main__":
    main()
