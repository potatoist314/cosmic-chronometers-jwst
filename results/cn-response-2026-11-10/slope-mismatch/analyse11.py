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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["prepare", "check"])
    args = parser.parse_args()
    if args.step == "prepare":
        prepare()
    else:
        check_readers()


if __name__ == "__main__":
    main()
