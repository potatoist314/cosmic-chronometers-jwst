#!/usr/bin/env python3
"""Experiment 11: the 4074.5–4666.1 A mock chronometer window."""
from __future__ import annotations

import argparse
import csv
import datetime
import importlib.util
import json
from pathlib import Path
import subprocess

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BASE = OUT.parent
spec = importlib.util.spec_from_file_location("experiment10", OUT / "analyse.py")
e10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e10)
e9 = e10.e9
sha, dump, table = e10.sha, e10.dump, e10.table
SEEDS, FIT_SEED, BOOTSTRAP_SEED = e10.SEEDS, e10.FIT_SEED, e10.BOOTSTRAP_SEED
REST_RANGE = [4074.5, 4666.1]
NEW_ARMS = ("C1", "C2", "C3")
ALL_ARMS = ("P9", "A", "B1", "B2", "B3", *NEW_ARMS)
INFERENCE_REVISION = "e0b0086e9f99bf9c930b5739ff6e8221c0ac1015"


def prepare():
    old = e10.previous_inputs()
    injected = json.loads((OUT / "inputs.json").read_text())
    original_groups = {r["target"]: r["original_Mgb_group"] for r in injected["checks"]}
    for record in old["mocks"] + injected["mocks"]:
        assert sha(ROOT / record["path"]) == record["sha256"]
    (OUT / "configs/C").mkdir(exist_ok=True)
    coverage = []
    for truth in old["truths"]:
        target = truth["target"]
        arms = {}
        per_seed = []
        for seed in SEEDS:
            plain, = [r for r in old["mocks"] if r["target"] == target and r["noise_seed"] == seed]
            enhanced, = [r for r in injected["mocks"] if r["target"] == target and r["noise_seed"] == seed]
            with np.load(ROOT / plain["path"]) as data, np.load(ROOT / enhanced["path"]) as extra:
                np.testing.assert_array_equal(data["spectrum_wave"], extra["spectrum_wave"])
                np.testing.assert_array_equal(data["spectrum_mask"], extra["spectrum_mask"])
                rest = data["spectrum_wave"] / (1 + truth["redshift"])
                available = rest[data["spectrum_mask"]]
                mask = data["spectrum_mask"] & (rest >= REST_RANGE[0]) & (rest <= REST_RANGE[1])
                per_seed.append(dict(target=target, redshift=truth["redshift"],
                    original_with_Mgb=original_groups[target],
                    original_fitted_pixels=int(data["spectrum_mask"].sum()),
                    window_fitted_pixels=int(mask.sum()),
                    available_rest_min=float(available.min()), available_rest_max=float(available.max()),
                    kept_rest_min=float(rest[mask].min()), kept_rest_max=float(rest[mask].max()),
                    fully_covered=bool(available.min() <= REST_RANGE[0] and available.max() >= REST_RANGE[1]),
                    missing_blue_angstrom=max(0., float(available.min()) - REST_RANGE[0]),
                    missing_red_angstrom=max(0., REST_RANGE[1] - float(available.max()))))
            for arm in NEW_ARMS:
                arms[f"{arm}_s{seed}"] = dict(settings=dict(
                    mock_data=plain["path"] if arm == "C1" else enhanced["path"],
                    abundance_response=e10.RESPONSE if arm == "C3" else None))
        assert per_seed[0] == per_seed[1] == per_seed[2]
        coverage.append(per_seed[0])
        dump(OUT / f"configs/C/{target}.json", dict(targets=[target], seed=FIT_SEED,
             settings=dict(rest_range=REST_RANGE), priors={}, arms=arms))
        print(f'{target}: {coverage[-1]["window_fitted_pixels"]} fitted pixels; '
              f'{"full" if coverage[-1]["fully_covered"] else "PARTIAL"} coverage', flush=True)
    table(OUT / "experiment11-window-coverage.csv", coverage)
    dump(OUT / "experiment11-inputs.json", dict(
        created=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        rest_range=REST_RANGE, arms=list(NEW_ARMS), inference_seed=FIT_SEED,
        noise_seeds=list(SEEDS), bootstrap_seed=BOOTSTRAP_SEED,
        coverage_definition="Full coverage means the original fitted rest-frame pixel centers span both window limits. Internal mask holes remain excluded.",
        partial_coverage_rule="Keep every target, including partial spans; never extrapolate or fill gaps.",
        previous_manifest_sha256=sha(e10.PREVIOUS / "inputs.json"),
        injected_manifest_sha256=sha(OUT / "inputs.json"),
        reference_rows_sha256=sha(OUT / "per-mock.csv"),
        reference_script_sha256=sha(OUT / "analyse.py"),
        previous_report_sha256=sha(BASE / "REPORT.md"),
        notebook_sha256=sha(ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"),
        preparation_script_sha256=sha(Path(__file__)),
        parent_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        truths=old["truths"], original_mocks=old["mocks"], injected_mocks=injected["mocks"],
        response_sha256=injected["response_sha256"], coverage=coverage))


def check_readers():
    from scripts.experiment import preflight
    source = preflight(OUT / "configs/C/M1_210210.json", "HEAD", commands=("git",))
    assert len(source["experiment"]) == 9
    checks = []
    for target, arm in (("M1_210210", "C1"), ("M1_210210", "C3"), ("M8_161113", "C3")):
        if target != "M1_210210":
            source = preflight(OUT / f"configs/C/{target}.json", "HEAD", commands=("git",))
        cell, = [c for c in source["experiment"] if c["arm"] == f"{arm}_s{SEEDS[0]}"]
        settings = dict(cell["settings"], ssp_grid=source["grid"])
        e10.os.environ.update(CERIDWEN_TARGET_ID=target,
            CERIDWEN_MANIFEST_INDEX=str(cell["target_metadata"]["manifest_index"]),
            CERIDWEN_RANDOM_SEED=str(FIT_SEED),
            CERIDWEN_RESULT_DIR=str(OUT / "assembly11" / f"{arm}-{target}"))
        ns = {}
        with e10.contextlib.redirect_stdout(e10.io.StringIO()), e10.contextlib.redirect_stderr(e10.io.StringIO()):
            document = e10._fit_notebook(json.dumps(settings), json.dumps(cell["priors"]))
            for index, notebook_cell in enumerate(document.cells[:9]):
                if notebook_cell.cell_type == "code":
                    exec(compile(notebook_cell.source, f"production-cell-{index}", "exec"), ns)
        assert ns["joint_csp"].sfh_basis_fastpath
        assert float(ns["joint_priors"]["logsfr_ratios"].scale) == .3
        cn = {"cfe", "nfe"} <= set(ns["joint_priors"])
        assert cn == (arm == "C3")
        with np.load(ROOT / settings["mock_data"]) as data:
            z = next(t["redshift"] for t in e10.previous_inputs()["truths"] if t["target"] == target)
            rest = data["spectrum_wave"] / (1 + z)
            expected = data["spectrum_mask"] & (rest >= REST_RANGE[0]) & (rest <= REST_RANGE[1])
            np.testing.assert_array_equal(ns["spectrum_mask"], expected)
            np.testing.assert_array_equal(ns["spectrum_wave"], data["spectrum_wave"])
        checks.append(dict(target=target, arm=arm, fitted_pixels=int(expected.sum()),
                           mask_exact=True, fast_path=True, free_CN=cn, sfh_prior_scale=.3))
        print(checks[-1], flush=True)
        del ns
        e10.gc.collect()
        e10.jax.clear_caches()
    dump(OUT / "experiment11-reader-checks.json", dict(checks=checks, no_sampling=True, no_figures=True))


def read_rows(path):
    rows = list(csv.DictReader(path.open()))
    for row in rows:
        for name in row:
            if name in ("arm", "target", "result_path"):
                continue
            if name in ("original_with_Mgb", "age_truth_inside"):
                row[name] = row[name] == "True"
            elif name == "noise_seed":
                row[name] = int(row[name])
            else:
                row[name] = float(row[name])
    return rows


def summarize():
    inputs = json.loads((OUT / "experiment11-inputs.json").read_text())
    assert sha(e10.PREVIOUS / "inputs.json") == inputs["previous_manifest_sha256"]
    assert sha(OUT / "inputs.json") == inputs["injected_manifest_sha256"]
    assert sha(OUT / "per-mock.csv") == inputs["reference_rows_sha256"]
    assert sha(OUT / "analyse.py") == inputs["reference_script_sha256"]
    assert sha(ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb") == inputs["notebook_sha256"]
    for item in inputs["original_mocks"] + inputs["injected_mocks"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    for name, digest in inputs["response_sha256"].items():
        assert sha(ROOT / e10.RESPONSE / name) == digest
    rows = read_rows(OUT / "per-mock.csv")
    assert len(rows) == 150
    reference = {(r["target"], r["noise_seed"]): r for r in rows if r["arm"] == "P9"}
    coverage = {r["target"]: r for r in inputs["coverage"]}
    checks = []
    for truth in inputs["truths"]:
        target = truth["target"]
        run = OUT / "runs/C" / target
        manifest = json.loads((run / "manifest.json").read_text())
        assert manifest["source"]["commit"] == INFERENCE_REVISION
        assert set(manifest["completed_cells"]) == {
            f"{arm}_s{seed}/{target}" for arm in NEW_ARMS for seed in SEEDS}
        for arm in NEW_ARMS:
            for seed in SEEDS:
                directory, = (run / "fits" / f"{arm}_s{seed}").iterdir()
                e10.validate_result(directory)
                raw = directory / "ceridwen_result.h5"
                fit = e9.load_result_h5(raw)
                assert ({"cfe", "nfe"} <= set(fit.samples)) if arm == "C3" else not (
                    {"cfe", "nfe"} & set(fit.samples))
                assert np.asarray(fit.samples["logsfr_ratios"]).shape[1:] == (14,)
                mock_record, = [m for m in inputs["original_mocks" if arm == "C1" else "injected_mocks"]
                                if m["target"] == target and m["noise_seed"] == seed]
                with np.load(ROOT / mock_record["path"]) as data, e10.h5py.File(
                        directory / "ceridwen_derived_outputs.h5", "r") as stored:
                    times = np.asarray(stored["sfh/lookback_time_gyr"])
                    assert int(stored.attrs["random_seed"]) == FIT_SEED
                    np.testing.assert_allclose(float(stored.attrs["redshift"]), truth["redshift"],
                                               atol=1e-10, rtol=0)
                    rest = data["spectrum_wave"] / (1 + truth["redshift"])
                    mask = data["spectrum_mask"] & (rest >= REST_RANGE[0]) & (rest <= REST_RANGE[1])
                    assert int(mask.sum()) == coverage[target]["window_fitted_pixels"]
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
                sfr = e10.softmax(np.c_[np.zeros(len(ratios)), -np.cumsum(ratios, axis=1)] * np.log(10.), axis=1)
                mass = .5 * (sfr[:, :-1] + sfr[:, 1:]) * np.diff(times)
                fractions = mass / mass.sum(axis=1)[:, None]
                ages = fractions @ (.5 * (times[:-1] + times[1:]))
                distance, index = e10.cKDTree(fractions).query(stored_fractions)
                assert distance.max() < 1e-11
                np.testing.assert_allclose(ages[index], stored_ages, atol=1e-11, rtol=0)
                ageq = e9.weighted_quantiles(ages, fit.log_weights, quantiles=[.16, .5, .84])
                afe = e9.weighted_quantiles(np.asarray(fit.samples["afe"]).ravel(),
                                          fit.log_weights, quantiles=[.5])[0]
                rows.append(e10.make_row(arm, target, seed, truth, ageq, afe,
                    str(raw.relative_to(ROOT)), reference[(target, seed)], coverage[target]["original_with_Mgb"]))
                cell, = [c for c in manifest["source"]["experiment"] if c["arm"] == f"{arm}_s{seed}"]
                assert cell["settings"]["rest_range"] == REST_RANGE
                assert cell["settings"]["mock_data"] == mock_record["path"]
                assert bool(cell["settings"]["abundance_response"]) == (arm == "C3")
                assert cell["settings"]["fix_afe"] is None
                assert cell["settings"]["masked_absorption_features"] == []
                assert cell["settings"]["sampler"] == dict(num_live=500, num_inner_steps=65,
                                                          num_delete=100, logZ_tol=-5.)
                assert cell["priors"]["logsfr_ratios"] == "StudentT(mean=0.0, scale=0.3, df=2.0)"
                checks.append(dict(arm=arm, target=target, noise_seed=seed, validation=True,
                    fitted_pixels=int(mask.sum()), fully_covered=coverage[target]["fully_covered"],
                    raw_sha256=sha(raw), derived_sha256=sha(raw.with_name("ceridwen_derived_outputs.h5")),
                    stored_fraction_max_distance=float(distance.max()),
                    stored_age_max_error_gyr=float(np.max(np.abs(ages[index] - stored_ages)))))
        print(f"{target}: 9 fits validated", flush=True)
    assert len(rows) == 240 and len(checks) == 90
    table(OUT / "experiment11-per-mock.csv", rows)
    old_error = summarize_rows(rows, inputs)
    dump(OUT / "experiment11-artifact-checks.json", dict(fits_validated=90, reference_rows=150,
        fits=checks, all_sixty_mock_hashes_unchanged=True, raw_response_hashes_unchanged=True,
        response_files=len(inputs["response_sha256"]), reference_rows_sha256=sha(OUT / "per-mock.csv"),
        inference_revision=INFERENCE_REVISION, old_summary_max_difference=old_error))


def summarize_rows(rows, inputs):
    truths = {t["target"]: t for t in inputs["truths"]}
    groups = {r["target"]: r["original_with_Mgb"] for r in inputs["coverage"]}
    names = sorted(truths)
    z = np.array([truths[n]["redshift"] for n in names])
    true = np.array([truths[n]["true_age_gyr"] for n in names])
    g = np.array([groups[n] for n in names], float)
    x = np.c_[np.ones(10), z, g]
    true_coeff = np.linalg.lstsq(x, true, rcond=None)[0]
    true_slope = float(np.polyfit(z, true, 1)[0])
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, 10, (10000, 10))
    dz = z[indices] - z[indices].mean(axis=1)[:, None]
    full_rank = np.array([np.linalg.matrix_rank(x[i]) == 3 for i in indices])
    assert full_rank.sum() == 9979
    summaries, widths = [], []
    for arm in ALL_ARMS:
        selected = [r for r in rows if r["arm"] == arm]
        assert len(selected) == 30
        assert all(r["original_with_Mgb"] == groups[r["target"]] for r in selected)
        mean_age = np.array([np.mean([r["age_q50"] for r in selected if r["target"] == n]) for n in names])
        slopes = np.sum(dz * (mean_age[indices] - mean_age[indices].mean(axis=1)[:, None]), axis=1) / np.sum(dz**2, axis=1)
        q = np.quantile(slopes, [.025, .975])
        coefficients = np.linalg.lstsq(x, mean_age, rcond=None)[0]
        step_samples = np.array([np.linalg.lstsq(x[i], mean_age[i], rcond=None)[0][2]
                                 for i in indices[full_rank]])
        stepq = np.quantile(step_samples, [.025, .975])
        slope = float(np.polyfit(z, mean_age, 1)[0])
        med = lambda subset, field: float(np.median([r[field] for r in subset]))
        low = [r for r in selected if r["redshift"] < np.median(z)]
        high = [r for r in selected if r["redshift"] > np.median(z)]
        with_mgb = [r for r in selected if groups[r["target"]]]
        without_mgb = [r for r in selected if not groups[r["target"]]]
        assert all(len(a) == 15 for a in (low, high, with_mgb, without_mgb))
        summaries.append(dict(arm=arm, galaxies=10, mocks=30, recovered_age_slope=slope,
            slope_bootstrap_q025=float(q[0]), slope_bootstrap_q975=float(q[1]),
            true_age_slope=true_slope, slope_ratio=slope / true_slope,
            median_age_bias_lower_z=med(low, "age_bias_gyr"), median_age_bias_upper_z=med(high, "age_bias_gyr"),
            median_age_bias_with_Mgb=med(with_mgb, "age_bias_gyr"), median_age_bias_without_Mgb=med(without_mgb, "age_bias_gyr"),
            joint_intercept=float(coefficients[0]), joint_slope=float(coefficients[1]), Mgb_group_step=float(coefficients[2]),
            step_bootstrap_q025=float(stepq[0]), step_bootstrap_q975=float(stepq[1]), step_bootstrap_valid=int(full_rank.sum()),
            true_joint_slope=float(true_coeff[1]), true_group_step=float(true_coeff[2]),
            age_truth_inside=sum(r["age_truth_inside"] for r in selected),
            age_truth_inside_with_Mgb=sum(r["age_truth_inside"] for r in with_mgb),
            age_truth_inside_without_Mgb=sum(r["age_truth_inside"] for r in without_mgb), median_afe_bias=med(selected, "afe_bias")))
        for label, subgroup in (("all", selected), ("with_Mgb", with_mgb), ("without_Mgb", without_mgb)):
            widths.append(dict(arm=arm, original_coverage=label, mocks=len(subgroup),
                median_age_width_16_84_gyr=med(subgroup, "age_width_16_84_gyr"),
                median_P_width_16_84_gyr=med(subgroup, "P_age_width_16_84_gyr"),
                median_paired_width_ratio=med(subgroup, "width_ratio_to_P"),
                median_paired_width_difference_gyr=med(subgroup, "width_difference_from_P_gyr")))
    old_summary = {r["arm"]: r for r in csv.DictReader((OUT / "summary.csv").open())}
    errors = []
    for row in summaries[:5]:
        for key, value in row.items():
            if key != "arm":
                error = abs(value - float(old_summary[row["arm"]][key]))
                assert error < 1e-12
                errors.append(error)
    table(OUT / "experiment11-summary.csv", summaries)
    table(OUT / "experiment11-width-comparison.csv", widths)
    dump(OUT / "experiment11-bootstrap-method.json", dict(seed=BOOTSTRAP_SEED, draws=10000,
        interval="95% percentile", clusters="Ten galaxies including the partial-coverage target; retain all three seeds together.",
        estimator="Unweighted OLS on thirty posterior median ages, equivalent to ten galaxy means.",
        step="age = a + b*z + c*g; g=1 originally with Mg b, 0 originally without; fixed across all arms.",
        step_bootstrap_valid=int(full_rank.sum()), step_bootstrap_nonidentified=int((~full_rank).sum()),
        rule="All draws enter slope intervals; only full-rank joint fits enter step intervals."))
    print(json.dumps(summaries), flush=True)
    return max(errors)


def verify():
    inputs = json.loads((OUT / "experiment11-inputs.json").read_text())
    rows = read_rows(OUT / "experiment11-per-mock.csv")
    summaries = list(csv.DictReader((OUT / "experiment11-summary.csv").open()))
    widths = list(csv.DictReader((OUT / "experiment11-width-comparison.csv").open()))
    assert [r["arm"] for r in summaries] == list(ALL_ARMS)
    assert len(rows) == 240 and len(widths) == 24
    truths = {t["target"]: t for t in inputs["truths"]}
    coverage = {r["target"]: r for r in inputs["coverage"]}
    names = sorted(truths)
    z = np.array([truths[n]["redshift"] for n in names])
    true = np.array([truths[n]["true_age_gyr"] for n in names])
    group = np.array([coverage[n]["original_with_Mgb"] for n in names], float)
    means = np.array([[np.mean([r["age_q50"] for r in rows if r["target"] == n and r["arm"] == arm])
                       for arm in ALL_ARMS] for n in names])
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, 10, (10000, 10))
    slopes, steps = [], []
    for index in indices:
        slopes.append(e10.lstsq(np.c_[np.ones(10), z[index]], means[index], lapack_driver="gelsy")[0][1])
        coefficients, _, rank, _ = e10.lstsq(np.c_[np.ones(10), z[index], group[index]],
                                             means[index], lapack_driver="gelsd")
        if rank == 3:
            steps.append(coefficients[2])
    assert len(steps) == 9979
    slopeq, stepq = np.quantile(slopes, [.025, .975], axis=0), np.quantile(steps, [.025, .975], axis=0)
    errors = []
    reference = {(r["target"], r["noise_seed"]): r for r in rows if r["arm"] == "P9"}
    for j, summary in enumerate(summaries):
        selected = [r for r in rows if r["arm"] == summary["arm"]]
        assert len(selected) == 30
        zz = np.array([r["redshift"] for r in selected])
        yy = np.array([r["age_q50"] for r in selected])
        gg = np.array([r["original_with_Mgb"] for r in selected], float)
        np.testing.assert_allclose(e10.linregress(zz, yy).slope, float(summary["recovered_age_slope"]), atol=1e-11, rtol=0)
        np.testing.assert_allclose(e10.linregress(z, true).slope, float(summary["true_age_slope"]), atol=1e-11, rtol=0)
        coefficients = e10.lstsq(np.c_[np.ones(30), zz, gg], yy, lapack_driver="gelsy")[0]
        np.testing.assert_allclose(coefficients, [float(summary[k]) for k in
            ("joint_intercept", "joint_slope", "Mgb_group_step")], atol=1e-10, rtol=0)
        for actual, keys in ((slopeq[:, j], ("slope_bootstrap_q025", "slope_bootstrap_q975")),
                             (stepq[:, j], ("step_bootstrap_q025", "step_bootstrap_q975"))):
            expected = np.array([float(summary[k]) for k in keys])
            errors.append(float(np.max(np.abs(actual - expected))))
            np.testing.assert_allclose(actual, expected, atol=1e-9, rtol=0)
        for r in selected:
            assert r["redshift"] == truths[r["target"]]["redshift"]
            assert r["true_age_gyr"] == truths[r["target"]]["true_age_gyr"]
            assert r["age_q16"] <= r["age_q50"] <= r["age_q84"]
            assert r["age_truth_inside"] == (r["age_q16"] <= r["true_age_gyr"] <= r["age_q84"])
            p = reference[(r["target"], r["noise_seed"])]
            pw = p["age_q84"] - p["age_q16"]
            for actual, expected in ((r["age_bias_gyr"], r["age_q50"] - r["true_age_gyr"]),
                    (r["afe_bias"], r["afe_q50"] - .2),
                    (r["age_width_16_84_gyr"], r["age_q84"] - r["age_q16"]),
                    (r["P_age_width_16_84_gyr"], pw),
                    (r["width_ratio_to_P"], r["age_width_16_84_gyr"] / pw),
                    (r["width_difference_from_P_gyr"], r["age_width_16_84_gyr"] - pw)):
                np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-14)
        for key, subset in (
                ("median_age_bias_lower_z", [r for r in selected if r["redshift"] < np.median(z)]),
                ("median_age_bias_upper_z", [r for r in selected if r["redshift"] > np.median(z)]),
                ("median_age_bias_with_Mgb", [r for r in selected if r["original_with_Mgb"]]),
                ("median_age_bias_without_Mgb", [r for r in selected if not r["original_with_Mgb"]])):
            assert len(subset) == 15
            np.testing.assert_allclose(np.quantile([r["age_bias_gyr"] for r in subset], .5), float(summary[key]), atol=1e-14, rtol=0)
        np.testing.assert_allclose(np.median([r["afe_bias"] for r in selected]), float(summary["median_afe_bias"]), atol=1e-14, rtol=0)
        assert sum(r["age_truth_inside"] for r in selected) == int(summary["age_truth_inside"])
        for label, subset in (("all", selected),
                ("with_Mgb", [r for r in selected if r["original_with_Mgb"]]),
                ("without_Mgb", [r for r in selected if not r["original_with_Mgb"]])):
            w, = [w for w in widths if w["arm"] == summary["arm"] and w["original_coverage"] == label]
            assert len(subset) == int(w["mocks"])
            if label != "all":
                assert sum(r["age_truth_inside"] for r in subset) == int(summary[f"age_truth_inside_{label}"])
            for outkey, inkey in (("median_age_width_16_84_gyr", "age_width_16_84_gyr"),
                    ("median_P_width_16_84_gyr", "P_age_width_16_84_gyr"),
                    ("median_paired_width_ratio", "width_ratio_to_P"),
                    ("median_paired_width_difference_gyr", "width_difference_from_P_gyr")):
                np.testing.assert_allclose(np.median([r[inkey] for r in subset]), float(w[outkey]), atol=1e-14, rtol=0)
    coverage_csv = {r["target"]: r for r in csv.DictReader((OUT / "experiment11-window-coverage.csv").open())}
    for target, c in coverage.items():
        mock, = [r for r in inputs["original_mocks"] if r["target"] == target and r["noise_seed"] == SEEDS[0]]
        with np.load(ROOT / mock["path"]) as data:
            rest = data["spectrum_wave"] / (1 + truths[target]["redshift"])
            assert np.all(np.diff(rest) > 0)
            lo = np.searchsorted(rest, REST_RANGE[0], side="left")
            hi = np.searchsorted(rest, REST_RANGE[1], side="right")
            assert int(data["spectrum_mask"][lo:hi].sum()) == c["window_fitted_pixels"] == int(coverage_csv[target]["window_fitted_pixels"])
            available = rest[data["spectrum_mask"]]
            assert (float(available.min()) <= REST_RANGE[0] and float(available.max()) >= REST_RANGE[1]) == c["fully_covered"]
            assert (coverage_csv[target]["fully_covered"] == "True") == c["fully_covered"]
    for record in inputs["original_mocks"] + inputs["injected_mocks"]:
        assert sha(ROOT / record["path"]) == record["sha256"]
    for name, digest in inputs["response_sha256"].items():
        assert sha(ROOT / e10.RESPONSE / name) == digest
    assert sha(OUT / "per-mock.csv") == inputs["reference_rows_sha256"]
    preparation = subprocess.check_output(["git", "show", "37dda4cfb999ee0cd92c6337969b91d79e49ebfb:" + str((OUT / "analyse11.py").relative_to(ROOT))])
    assert e10.hashlib.sha256(preparation).hexdigest() == inputs["preparation_script_sha256"]
    gpu_counts, exits, notebooks, images = {}, 0, 0, 0
    for path in (OUT / "runs/C").glob("*/manifest.json"):
        manifest = json.loads(path.read_text())
        assert manifest["source"]["commit"] == INFERENCE_REVISION
        for attempt in manifest["attempts"]:
            assert attempt["status"] == "complete"
            for cell in attempt["cells"].values():
                assert cell["exit"] == {"bootstrap": 0, "fit": 0}
                exits += 1
                gpu_counts[cell["gpu_name"]] = gpu_counts.get(cell["gpu_name"], 0) + 1
        for notebook in (path.parent / "fits").glob("*/*/*_executed.ipynb"):
            document = json.loads(notebook.read_text())
            notebooks += 1
            images += sum(any(k.startswith("image/") for k in out.get("data", {}))
                          for cell in document["cells"] for out in cell.get("outputs", []))
    assert exits == notebooks == 90 and images == 0
    assert not list(OUT.rglob("*.png"))
    dump(OUT / "experiment11-independent-checks.json", dict(passed=True, fits=90, reference_rows=150,
        independent_slopes="SciPy linregress on thirty ages per arm", independent_bootstrap="SciPy QR and SVD on the same galaxy clusters",
        maximum_interval_difference=max(errors), identified_step_bootstraps=len(steps),
        coverage_counts_independently_verified=True, partial_targets=[n for n in names if not coverage[n]["fully_covered"]],
        original_reference_rows_unchanged=True, all_sixty_mock_hashes_unchanged=True,
        response_files=len(inputs["response_sha256"]), response_hashes_unchanged=True,
        executed_notebooks=notebooks, embedded_images=images, png_files=0,
        requested_gpu="A100-40GB", actual_gpu_counts=gpu_counts, remote_exits_all_zero=True))
    print(json.dumps(dict(passed=True, actual_gpu_counts=gpu_counts)), flush=True)


def report():
    inputs = json.loads((OUT / "experiment11-inputs.json").read_text())
    validation = json.loads((OUT / "experiment11-artifact-checks.json").read_text())
    independent = json.loads((OUT / "experiment11-independent-checks.json").read_text())
    modal = json.loads((OUT / "experiment11-modal-state.json").read_text())
    assert validation["fits_validated"] == 90 and independent["passed"]
    assert not modal["own_containers"] and all(a["state"] == "stopped" for a in modal["own_apps"])
    summaries = list(csv.DictReader((OUT / "experiment11-summary.csv").open()))
    widths = list(csv.DictReader((OUT / "experiment11-width-comparison.csv").open()))
    f = lambda r, k: f'{float(r[k]):.3f}'
    signed = lambda r, k: f'{float(r[k]):+.3f}'
    true_slope = float(summaries[0]["true_age_slope"])
    text = ["\n## Experiment 11 results\n",
        "Ninety new recoveries use the existing thirty Experiment 9 mocks and thirty C/N-injected "
        "Experiment 10 mocks without changing either set. Each new arm has ten galaxies and three "
        "noise seeds. C1, C2 and C3 use rest_range = [4074.5, 4666.1] A; all other settings are production values.\n",
        "| Galaxy | Fitted pixels kept | Original fitted rest span (A) | Kept rest span (A) | Coverage |",
        "| --- | ---: | --- | --- | --- |"]
    for r in inputs["coverage"]:
        flag = "full" if r["fully_covered"] else f'PARTIAL: red end missing {r["missing_red_angstrom"]:.3f} A'
        text.append(f'| {r["target"]} | {r["window_fitted_pixels"]} | '
            f'{r["available_rest_min"]:.3f}–{r["available_rest_max"]:.3f} | '
            f'{r["kept_rest_min"]:.3f}–{r["kept_rest_max"]:.3f} | {flag} |')
    text += ["\nWavelengths are rest-frame vacuum values. Full coverage means that the first and last "
        "originally fitted pixel centers bracket both requested limits. Interior quality and emission-line "
        "mask holes remain excluded. M8_161113 is retained in every arm and every bootstrap resample "
        "in which that galaxy is selected; its nine new fits use 1490 pixels. No gaps are filled.\n",
        "| Arm | Injected C/Fe, N/Fe | Recovery | Rest-frame window (A) | New fits in Experiment 11 |",
        "| --- | --- | --- | --- | ---: |",
        "| P9 | 0, 0 | Plain grid | Original coverage | 0 |",
        "| A | 0, 0 | Plain grid | 4155.0–4438.1 | 0 |",
        "| B1 | +0.15, +0.30 | Plain grid | Original coverage | 0 |",
        "| B2 | +0.15, +0.30 | C/N free | Original coverage | 0 |",
        "| B3 | +0.15, +0.30 | Plain grid | 4155.0–4438.1 | 0 |",
        "| C1 | 0, 0 | Plain grid | 4074.5–4666.1 | 30 |",
        "| C2 | +0.15, +0.30 | Plain grid | 4074.5–4666.1 | 30 |",
        "| C3 | +0.15, +0.30 | C/N free | 4074.5–4666.1 | 30 |\n",
        f"The exact true finite-sample slope is {true_slope:+.6f} Gyr per unit redshift. "
        "Slope and step intervals are 95% galaxy-cluster bootstrap intervals. Age intervals are "
        "posterior q16–q84; age differences and widths are Gyr, abundance biases are dex.\n",
        "| Arm | Recovered slope [95% bootstrap] | Recovered / true | True slope inside interval | Median alpha/Fe bias |",
        "| --- | ---: | ---: | --- | ---: |"]
    for r in summaries:
        inside = float(r["slope_bootstrap_q025"]) <= true_slope <= float(r["slope_bootstrap_q975"])
        text.append(f'| {r["arm"]} | {signed(r, "recovered_age_slope")} '
            f'[{signed(r, "slope_bootstrap_q025")}, {signed(r, "slope_bootstrap_q975")}] | '
            f'{f(r, "slope_ratio")} | {"yes" if inside else "no"} | {signed(r, "median_afe_bias")} |')
    c3, = [r for r in summaries if r["arm"] == "C3"]
    c3_inside = float(c3["slope_bootstrap_q025"]) <= true_slope <= float(c3["slope_bootstrap_q975"])
    text += [f'\nC3 recovers {float(c3["slope_ratio"]):.3f} of the true slope in this mock design. '
        f'Its 95% bootstrap interval {"includes" if c3_inside else "excludes"} the exact true slope. '
        f'Its median alpha/Fe bias is {float(c3["median_afe_bias"]):+.3f} dex.\n']
    text += ["\n| Arm | Age bias, lower z | Upper z | Originally with Mg b | Originally without Mg b | Age truth inside 16–84, all / with / without |",
        "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in summaries:
        text.append(f'| {r["arm"]} | {signed(r, "median_age_bias_lower_z")} | '
            f'{signed(r, "median_age_bias_upper_z")} | {signed(r, "median_age_bias_with_Mgb")} | '
            f'{signed(r, "median_age_bias_without_Mgb")} | {r["age_truth_inside"]}/30 / '
            f'{r["age_truth_inside_with_Mgb"]}/15 / {r["age_truth_inside_without_Mgb"]}/15 |')
    text += ["\nThe redshift halves each contain five galaxies and fifteen mocks. Original Mg b "
        "coverage defines the same five-with/five-without groups as Experiment 10, fixed across all windows. "
        "The joint fit is age = a + b z + c g, with g = 1 originally with Mg b and 0 originally without. "
        "Its c is the with-minus-without step at fixed redshift.\n",
        "| Arm | a | Joint slope b | Mg b group step c [95% bootstrap] |",
        "| --- | ---: | ---: | ---: |"]
    for r in summaries:
        text.append(f'| {r["arm"]} | {f(r, "joint_intercept")} | {signed(r, "joint_slope")} | '
            f'{signed(r, "Mgb_group_step")} [{signed(r, "step_bootstrap_q025")}, {signed(r, "step_bootstrap_q975")}] |')
    text += [f'\nThe joint fit to exact true ages gives b = {float(summaries[0]["true_joint_slope"]):+.6f}, '
        f'c = {float(summaries[0]["true_group_step"]):+.6f}; the small fitted true step comes from '
        'approximating the curved age-redshift relation by a plane.\n',
        "| Arm | Original Mg b coverage | Mocks | Median age width | Matching P9 width | Median paired width ratio | Median paired width difference |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |"]
    for r in widths:
        text.append(f'| {r["arm"]} | {r["original_coverage"]} | {r["mocks"]} | '
            f'{f(r, "median_age_width_16_84_gyr")} | {f(r, "median_P_width_16_84_gyr")} | '
            f'{f(r, "median_paired_width_ratio")} | {signed(r, "median_paired_width_difference_gyr")} |')
    text += ["\nWidths are q84 minus q16. Each width ratio and difference uses the matching "
        "P9 galaxy and noise seed before the median is taken.\n",
        "| Method or check | Recorded choice or result |",
        "| --- | --- |",
        "| Inputs | All sixty NPZ hashes match their Experiment 9/10 records. No mocks were regenerated. The same 1 Gyr cosmic-time formation window, exact true ages, 102-bin fine truth, dust, dispersion, filters, instrumental response and noise realizations are reused. |",
        "| Inference | Existing committed production model, SFH fast path, fourteen SFH ratio parameters, StudentT scale 0.3 and df 2, metallicity evolution, 500 live points, 65 inner steps, 100 deletions, logZ tolerance -5. Inference seed 20261110; noise seeds 20261111–20261113. Alpha/Fe remains free. The only recovery changes are rest_range and enabling the existing C/N response in C3. |",
        "| Response and truth approximations | The fine truth has constant Fe/H; production fitting retains metallicity evolution. C2/C3 reuse the existing injected response spectra and photometry, including the fixed-catalogue-dispersion response approximation and unchanged isochrones recorded in Experiment 10. All 25 raw response files retain their hashes. The Experiment 10 prose count was corrected from twenty to 25; its code already checked all 25. |",
        "| Coverage | The inclusive cut is applied on the native rest-frame vacuum pixel centers. Original quality/emission masks and photometry are retained. The partial target is kept without padding or extrapolation. Reader checks cover plain/C/N-free models and the partial target; their masks match the NPZ-based cut exactly. |",
        "| Summaries | All weighted raw posterior samples determine age and alpha/Fe quantiles. Derived SFH mass fractions and ages match independent reconstruction from raw samples. The five previous arm summaries reproduce their original values; their source CSV is unchanged. |",
        "| Bootstrap | Same 10,000 galaxy-cluster resamples and seed 20261129 as Experiment 10. Keep all three noise realizations together. OLS on thirty posterior median ages equals OLS on ten galaxy means. All 10,000 draws enter slope intervals; 9,979 full-rank joint fits enter step intervals, with 21 nonidentified steps omitted. |",
        f'| Validation | All 90 new raw/derived fits pass the existing validator and input, mask, uncertainty and SFH-age checks. Independent SciPy slope, joint-step, bootstrap, age-coverage, pixel-count and paired-width calculations pass. All {len(modal["own_apps"])} owned Experiment 11 Modal apps are stopped; no owned containers remain. |',
        f'| GPU provenance | Requested A100-40GB. Actual completed-fit counts: {json.dumps(independent["actual_gpu_counts"], sort_keys=True)}. Remote bootstrap and fit exits are zero. All 90 executed notebooks contain no images; no figures or wiki pages were created. |',
        "| Artifacts | [Per-mock comparison](slope-mismatch/experiment11-per-mock.csv), [eight-arm summary](slope-mismatch/experiment11-summary.csv), [paired widths](slope-mismatch/experiment11-width-comparison.csv), [window coverage](slope-mismatch/experiment11-window-coverage.csv), [frozen inputs](slope-mismatch/experiment11-inputs.json), [validation](slope-mismatch/experiment11-artifact-checks.json), [independent checks](slope-mismatch/experiment11-independent-checks.json), [Modal state](slope-mismatch/experiment11-modal-state.json), [script](slope-mismatch/analyse11.py). |",
        "| Noticed, not done | The pre-existing state-checker worktree error remains. The real-galaxy job's folder was read only; its fits and analysis remain with that job. |\n"]
    path = BASE / "REPORT.md"
    assert sha(path) == inputs["previous_report_sha256"]
    original = path.read_text()
    assert "## Experiment 11 results" not in original
    path.write_text(original + "\n".join(text))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["prepare", "check", "summarize", "verify", "report"])
    args = parser.parse_args()
    if args.step == "prepare":
        prepare()
    elif args.step == "check":
        check_readers()
    elif args.step == "verify":
        verify()
    elif args.step == "report":
        report()
    else:
        summarize()


if __name__ == "__main__":
    main()
