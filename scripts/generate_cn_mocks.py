#!/usr/bin/env python3
"""Generate recorded LEGA-C C/N injections through the production notebook model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESPONSE = "data/raw/alf/cda32111c721efe586945d7dfcb9f605a9f6a105"


def notebook_model(settings, output):
    """Run the existing notebook through model assembly, without fitting or plotting."""
    if __package__:
        from .run_ceridwen_vast_multi_gpu import _fit_notebook
    else:
        from run_ceridwen_vast_multi_gpu import _fit_notebook

    os.environ.update(CERIDWEN_TARGET_ID="M1_210210", CERIDWEN_PLOTS="0",
                      CERIDWEN_RANDOM_SEED="20261110",
                      CERIDWEN_RESULT_DIR=str(output))
    namespace = {}
    document = _fit_notebook(json.dumps(settings), None)
    for index, cell in enumerate(document.cells[:9]):
        if cell.cell_type == "code":
            exec(compile(cell.source, f"production-cell-{index}", "exec"), namespace)
    return namespace


def observations(namespace, truth, cfe, nfe, seed):
    """Gaussian draws: cgs F_nu spectra and maggies photometry, with recorded floors."""
    model = namespace["joint_model"]
    theta = {name: np.asarray(value) for name, value in truth.items()}
    theta.update(cfe=np.array([cfe]), nfe=np.array([nfe]))
    prediction = {k: np.asarray(v) for k, v in model.predict_jit(theta).items()}
    phot_stat = np.asarray(namespace["phot_error_stat"])
    spec_stat = np.asarray(namespace["native_uncertainty"])
    phot_sigma = np.hypot(phot_stat, namespace["SETTINGS"]["photometry_floor"]
                          * np.abs(prediction["photometry"]))
    spec_sigma = np.hypot(spec_stat, np.exp(float(theta["log_f_calib"][0]))
                          * np.abs(prediction["spectrum"]))
    rng = np.random.default_rng(seed)
    # The same standardized noise draw is reused across abundances for each seed.
    phot_noise = rng.standard_normal(phot_sigma.shape)
    spec_noise = rng.standard_normal(spec_sigma.shape)
    valid = np.asarray(namespace["native_valid"])
    return {
        "photometry_flux": prediction["photometry"] + phot_noise * phot_sigma,
        "photometry_uncertainty": phot_stat,
        "spectrum_flux": prediction["spectrum"] + np.where(valid, spec_noise * spec_sigma, 0.),
        "spectrum_uncertainty": spec_stat,
        "mean_photometry": prediction["photometry"], "mean_spectrum": prediction["spectrum"],
        "photometry_noise_sigma": phot_sigma, "spectrum_noise_sigma": spec_sigma,
        "spectrum_wave": np.asarray(namespace["spectrum_wave"]),
        "filter_names": np.asarray(namespace["FILTER_NAMES"]), "native_valid": valid,
        "photometry_unit": "maggies", "spectrum_unit": "erg s-1 cm-2 Hz-1",
        "wavelength_unit": "Angstrom (vacuum observed)", "target_id": "M1_210210",
        "cfe": cfe, "nfe": nfe, "noise_seed": seed,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    os.chdir(ROOT)
    if __package__:
        from .absorption_mask_analysis import truth_from_result
        from .absorption_mask_report import mass_weighted_age
    else:
        from absorption_mask_analysis import truth_from_result
        from absorption_mask_report import mass_weighted_age

    args.output.mkdir(parents=True, exist_ok=True)
    namespace = notebook_model({"abundance_response": RESPONSE}, args.output)
    truth = truth_from_result(args.source_result)
    truth.update(afe=[.2], logzsol=[-.2], sigma_smooth=[float(namespace["sigma_star"])])
    truth_age = mass_weighted_age(truth["logsfr_ratios"], namespace["lookback_template"])
    manifest = {
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "ceridwen_commit": subprocess.check_output(["git", "-C", "ceridwen", "rev-parse", "HEAD"], text=True).strip(),
        "source_result": str(args.source_result),
        "source_result_sha256": hashlib.sha256(args.source_result.read_bytes()).hexdigest(),
        "target": "M1_210210", "truth": truth, "mass_weighted_age_gyr": truth_age,
        "sigma_catalog_kms": float(namespace["sigma_star"]),
        "redshift": float(namespace["z_catalog"]),
        "settings": {"abundance_response": RESPONSE},
        "noise_seeds": [20261111, 20261112, 20261113], "fit_seed": 20261110,
        "cfe_grid": [0., .15, .3], "nfe_grid": [0., .3, .6],
        "noise": "Independent Gaussian pixels/bands; same standardized draws per seed across C/N. Statistical uncertainties from M1_210210. True model-scaled spectral floor and 5% photometry floor; recovery applies unchanged production noise rules.",
        "generator_backend": "JAX CPU x64", "mocks": [],
    }
    mask = np.asarray(namespace["spectrum_mask"])
    for cfe in manifest["cfe_grid"]:
        for nfe in manifest["nfe_grid"]:
            for seed in manifest["noise_seeds"]:
                name = f"c{cfe:.2f}_n{nfe:.2f}_s{seed}".replace(".", "p")
                values = observations(namespace, truth, cfe, nfe, seed)
                path = args.output / f"{name}.npz"
                np.savez_compressed(path, **values)
                manifest["mocks"].append({
                    "name": name, "path": str(path.relative_to(ROOT) if path.is_absolute() else path),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "cfe": cfe, "nfe": nfe, "noise_seed": seed,
                    "spectrum_statistical_sn_median": float(np.median(values["mean_spectrum"][mask] / values["spectrum_uncertainty"][mask])),
                    "spectrum_total_sn_median": float(np.median(values["mean_spectrum"][mask] / values["spectrum_noise_sigma"][mask])),
                })
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {len(manifest['mocks'])} injections; truth age {truth_age:.6f} Gyr")


if __name__ == "__main__":
    main()
