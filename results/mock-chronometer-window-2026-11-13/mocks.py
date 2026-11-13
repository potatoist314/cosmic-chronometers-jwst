#!/usr/bin/env python3
"""Mock chronometer on the common rest-frame window: one mock on each real LEGA-C DR3 window-194 galaxy.

Recipe of results/cn-response-2026-11-10/prior-slope/analyse.py (Experiment 9), with four SFH shapes
at one cosmic formation epoch and flux levels matched to the real photometry and spectrum.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import functools
import gc
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

os.environ.update(JAX_PLATFORMS="cpu", JAX_ENABLE_X64="1", MPLBACKEND="Agg", CERIDWEN_PLOTS="0")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
REAL = ROOT / "results/legac-dr3-2026-11-11/window-194"
EARLIER = ROOT / "results/cn-response-2026-11-10/prior-slope/inputs.json"
sys.path[:0] = [str(ROOT), str(ROOT / "ceridwen"), str(ROOT / "external/sedpy_jax")]
os.chdir(ROOT)

import jax
import jax.numpy as jnp
import numpy as np

from ceridwen import Cosmology
from ceridwen.broadening import Kinematics
from ceridwen.cosmology import age_gyr
from ceridwen.csp import CSPBasis_afe
from ceridwen.fit import load_result_h5
from ceridwen.model import SedModel
from ceridwen.ssps import SSPDataAfe
from scripts.absorption_mask_report import weighted_quantiles
from scripts.run_ceridwen_vast_multi_gpu import _fit_notebook

COSMO = Cosmology.planck18()
ARM = "dr3_plain_w"  # the real plain arm: data_source legac_dr3, rest_range [4074.5, 4666.1]
FIT_SEED = 20260832  # inference seed of the real window-194 run
NOISE_SEED = 20261113  # each mock: default_rng([NOISE_SEED, object_id])
BOOTSTRAP_SEED = 20261110  # as the real window-194 slopes
SHAPES = ("tophat1", "short", "exp", "twoburst")
TRUE_FEH, TRUE_AFE, STEP = -0.2, 0.2, 0.01  # as Experiment 9; fine bins of 0.01 Gyr
# Experiment 9 formation window: its midpoint is the mass-weighted formation time of every shape here.
FORMATION = sum(json.loads(EARLIER.read_text())[k] for k in ("formation_start_gyr", "formation_end_gyr")) / 2

SSPDataAfe.load = functools.lru_cache(maxsize=None)(SSPDataAfe.load)  # one grid read for all galaxies


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=1, allow_nan=False) + "\n")


def table(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def shape_history(shape):
    """Cosmic-time bin edges [Gyr] and formed-mass fractions; mass-weighted mean time FORMATION."""
    def flat(low, high):
        edges = np.linspace(low, high, round((high - low) / STEP) + 1)
        return edges, np.full(len(edges) - 1, 1.0 / (len(edges) - 1))

    if shape == "tophat1":  # Experiment 9: constant SFR for 1 Gyr
        pieces = [(1.0, *flat(-0.5, 0.5))]
    elif shape == "short":  # constant SFR for 0.5 Gyr, about one SSP age cell (0.33 to 0.58 Gyr wide at 2.8 to 5.0 Gyr)
        pieces = [(1.0, *flat(-0.25, 0.25))]
    elif shape == "exp":  # SFR proportional to exp(-t / 1 Gyr) for 2 Gyr
        edges = np.linspace(0.0, 2.0, round(2.0 / STEP) + 1)
        mass = -np.diff(np.exp(-edges))
        mass /= mass.sum()
        pieces = [(1.0, edges - mass @ (0.5 * (edges[:-1] + edges[1:])), mass)]
    elif shape == "twoburst":  # 80% of the mass in 0.5 Gyr, then 20% in 0.5 Gyr, 2 Gyr later
        pieces = [(0.8, *flat(-0.65, -0.15)), (0.2, *flat(1.35, 1.85))]
    edges = [FORMATION + e for _, e, _ in pieces]
    masses = [f * m for f, _, m in pieces]
    mean = sum(m @ (0.5 * (e[:-1] + e[1:])) for e, m in zip(edges, masses))
    np.testing.assert_allclose(mean, FORMATION, atol=1e-13, rtol=0)
    return edges, masses


def lookback_history(shape, universe_age):
    """Lookback bin edges [Gyr] and SFR per formed solar mass [1/yr] in each bin, youngest first."""
    times, history = [0.0], []
    for edges, masses in reversed(list(zip(*shape_history(shape)))):
        lookback = universe_age - edges[::-1]
        assert times[-1] < lookback[0] and lookback[-1] < universe_age
        history += [0.0, *(masses[::-1] / np.diff(lookback) / 1e9)]
        times += lookback.tolist()
    times, history = np.array(times + [universe_age]), np.array(history + [0.0])
    masses = history * np.diff(times) * 1e9
    np.testing.assert_allclose(masses.sum(), 1.0, rtol=1e-12)
    return times, history, float(masses @ (0.5 * (times[:-1] + times[1:])))


def design():
    """z-ordered galaxies, shapes cycled so each shape covers the z range; every fifth group of four is the subset."""
    cells = {c["target"]: c for c in json.loads((REAL / "run/manifest.json").read_text())["source"]["experiment"]
             if c["arm"] == ARM}
    real = {r["target"]: r for r in csv.DictReader((REAL.parent / "window-194-fits.csv").open())
            if r["arm"] == "plain" and r["release"] == "dr3"}
    assert set(cells) == set(real) and len(cells) == 194 and all(r["valid"] == "True" for r in real.values())
    rows = []
    for rank, target in enumerate(sorted(cells, key=lambda t: (float(real[t]["z"]), t))):
        meta = cells[target]["target_metadata"]
        rows.append(dict(rank=rank, target=target, object_id=meta["object_id"], manifest_index=meta["manifest_index"],
                         z=float(real[target]["z"]), catalogue_sn=meta["sn"],
                         shape=SHAPES[(rank + rank // 4) % 4], subset=(rank // 4) % 5 == 0 and rank // 4 < 50,
                         real_age_q50=float(real[target]["age_gyr_q50"]), real_fit=real[target]["path"]))
    table(OUT / "design.csv", rows)
    subset = [r for r in rows if r["subset"]]
    print(f"{len(rows)} mocks; subset {len(subset)}: " + ", ".join(
        f"{s} {sum(r['shape'] == s for r in subset)}/{sum(r['shape'] == s for r in rows)}" for s in SHAPES))


def read_design():
    rows = list(csv.DictReader((OUT / "design.csv").open()))
    for row in rows:
        row.update(rank=int(row["rank"]), z=float(row["z"]), subset=row["subset"] == "True",
                   object_id=int(row["object_id"]), manifest_index=int(row["manifest_index"]))
    return rows


def assemble(row, mock_data=None, cells=9):
    """Production notebook through model assembly, with the settings of the real plain arm."""
    cell = next(c for c in json.loads((REAL / "run/manifest.json").read_text())["source"]["experiment"]
                if c["arm"] == ARM and c["target"] == row["target"])
    grid = json.loads((REAL / "run/manifest.json").read_text())["source"]["grid"]
    settings = dict(cell["settings"], ssp_grid=grid, mock_data=mock_data)
    ns = {}
    with (tempfile.TemporaryDirectory() as scratch, contextlib.redirect_stdout(io.StringIO()),
          contextlib.redirect_stderr(io.StringIO())):
        os.environ.update(CERIDWEN_TARGET_ID=row["target"], CERIDWEN_MANIFEST_INDEX=str(row["manifest_index"]),
                          CERIDWEN_RANDOM_SEED=str(FIT_SEED), CERIDWEN_RESULT_DIR=scratch)
        for index, source in enumerate(_fit_notebook(json.dumps(settings), None).cells[:cells]):
            if source.cell_type == "code":
                exec(compile(source.source, f"production-cell-{index}", "exec"), ns)
    return ns, settings


def real_medians(row):
    fit = load_result_h5(ROOT / row["real_fit"] / "ceridwen_result.h5")
    medians = {}
    for name, values in fit.samples.items():
        flat = np.asarray(values).reshape(len(fit.log_weights), -1)
        medians[name] = np.array([weighted_quantiles(flat[:, k], fit.log_weights)[2] for k in range(flat.shape[1])])
    return medians


def truth_prediction(ns, medians, shape):
    """Fine-time constant-metallicity truth through CSPBasis_afe, as Experiment 9."""
    times, history, exact_age = lookback_history(shape, float(ns["universe_age"]))
    np.testing.assert_allclose(exact_age, float(ns["universe_age"]) - FORMATION, atol=1e-12, rtol=0)
    transforms = {k: v for k, v in ns["joint_transforms"].items() if k in ("diffuse_c_r", "tau_pow", "alpha_pow")}
    theta = {"lookback_time": jnp.asarray(times), "sfh": jnp.asarray(history),
             "logzsol": jnp.array([TRUE_FEH]), "afe": jnp.array([TRUE_AFE]),
             "diffuse_tau_noll": jnp.asarray(medians["diffuse_tau_noll"]),
             "diffuse_delta": jnp.asarray(medians["diffuse_delta"])}
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        csp = CSPBasis_afe(ns["ssp"], theta=theta, zh_const=True, sfh_interp="step",
                           add_dust=ns["SETTINGS"]["birth_cloud_dust"], add_diffuse_dust=True, diffuse_law="noll",
                           add_dust_emission=False, add_igm=False, track_zred_age=False, cosmo=COSMO, verbose=False)
        free = {k: jnp.asarray(medians[k]) for k in ("logmass", "diffuse_Ebump", "dust_ratio")}
        model = SedModel(csp, observations=[ns["phot_obs"], ns["spectrum_obs"]], transforms=transforms,
                         free_param_init=free, zred=float(ns["z_catalog"]),
                         kinematics=Kinematics(sigma_gal=float(medians["sigma_smooth"][0])), broaden_photometry=False)
        weights = np.asarray(csp.calculate_ssp_weights(model.apply_transforms(model.theta_init)))
        prediction = {k: np.asarray(v) for k, v in model.predict(model.theta_init).items()}
    np.testing.assert_allclose(weights.sum(), 1.0, rtol=1e-7)
    assert all(np.all(np.isfinite(v)) for v in prediction.values())
    # Step integration puts each SFH slice on the SSP of its age cell: the age that the spectrum has.
    ssp_age = float(weights.sum(axis=0) @ 10 ** np.asarray(ns["ssp"].ssp_lg_age_gyr))
    return prediction, exact_age, ssp_age, times, history


def generate(rows):
    (OUT / "mocks").mkdir(exist_ok=True)
    (OUT / "truths").mkdir(exist_ok=True)
    for row in rows:
        path = OUT / "mocks" / f'{row["target"]}.npz'
        if path.exists() and (OUT / "truths" / f'{row["target"]}.json').exists():
            continue
        ns, _ = assemble(row)
        assert ns["joint_csp"].sfh_basis_fastpath and int(ns["OBJECT_ID"]) == row["object_id"]
        np.testing.assert_allclose(float(ns["z_catalog"]), row["z"], atol=1e-12, rtol=0)
        medians = real_medians(row)
        prediction, exact_age, ssp_age, times, history = truth_prediction(ns, medians, row["shape"])
        mask, valid = np.asarray(ns["spectrum_mask"]), np.asarray(ns["native_valid"])
        real_phot, real_spec = np.asarray(ns["phot_flux"]), np.asarray(ns["native_flux"])
        phot_stat, spec_stat = np.asarray(ns["phot_error_stat"]), np.asarray(ns["native_uncertainty"])
        # Real flux levels, so the real statistical uncertainties give the real S/N: formed mass from the
        # photometry (the notebook's logmass start), then one calibration constant on the window spectrum.
        bands = np.asarray(ns["phot_fit_mask"]) & (real_phot > 0)
        mass_shift = float(np.median(np.log10(real_phot[bands] / prediction["photometry"][bands])))
        photometry = prediction["photometry"] * 10**mass_shift
        model_spectrum = prediction["spectrum"] * 10**mass_shift
        calibration = float(np.median(real_spec[mask]) / np.median(model_spectrum[mask]))
        spectrum = calibration * model_spectrum
        phot_sigma = np.hypot(phot_stat, ns["SETTINGS"]["photometry_floor"] * np.abs(photometry))
        # The fit's floor is f_calib * |uncalibrated model|.
        spec_sigma = np.hypot(spec_stat, np.exp(medians["log_f_calib"][0]) * np.abs(model_spectrum))
        rng = np.random.default_rng([NOISE_SEED, row["object_id"]])
        photo = photometry + rng.standard_normal(phot_sigma.shape) * phot_sigma
        spec = spectrum + np.where(valid, rng.standard_normal(spec_sigma.shape) * spec_sigma, 0.0)
        np.savez_compressed(
            path, photometry_flux=photo, photometry_uncertainty=phot_stat, spectrum_flux=spec,
            spectrum_uncertainty=spec_stat, native_valid=valid, mean_photometry=photometry, mean_spectrum=spectrum,
            photometry_noise_sigma=phot_sigma, spectrum_noise_sigma=spec_sigma,
            spectrum_wave=np.asarray(ns["spectrum_wave"]), filter_names=np.asarray(ns["FILTER_NAMES"]),
            spectrum_mask=mask, target_id=row["target"], true_age_gyr=exact_age, shape=row["shape"],
            noise_seed=[NOISE_SEED, row["object_id"]], time_edges_gyr=times, sfh_per_bin=history,
            photometry_unit="maggies", spectrum_unit="erg s-1 cm-2 Hz-1", wavelength_unit="Angstrom (vacuum observed)")
        rest = np.asarray(ns["spectrum_wave"])[mask] / (1.0 + row["z"])
        dump(OUT / "truths" / f'{row["target"]}.json', dict(
            target=row["target"], object_id=row["object_id"], rank=row["rank"], redshift=row["z"], shape=row["shape"],
            subset=row["subset"], true_age_gyr=exact_age, ssp_weight_age_gyr=ssp_age,
            universe_age_gyr=float(ns["universe_age"]),
            real_fit=row["real_fit"], real_fit_sha256=sha(ROOT / row["real_fit"] / "ceridwen_result.h5"),
            real_medians={k: v.tolist() for k, v in medians.items()},
            truth=dict(logzsol=TRUE_FEH, afe=TRUE_AFE, logmass=float(medians["logmass"][0]) + mass_shift,
                       calibration_constant=calibration,
                       **{k: float(medians[k][0]) for k in ("diffuse_tau_noll", "diffuse_delta", "diffuse_Ebump",
                                                             "dust_ratio", "sigma_smooth", "log_f_calib")}),
            logmass_shift_from_real_fit=mass_shift, photometry_source=ns["SETTINGS"]["photometry"],
            bands=int(len(photometry)), fitted_pixels=int(mask.sum()),
            fitted_rest_range=[float(rest.min()), float(rest.max())],
            sn_real=float(np.median(real_spec[mask] / spec_stat[mask])),
            sn_mock_statistical=float(np.median(spectrum[mask] / spec_stat[mask])),
            sn_mock_total=float(np.median(spectrum[mask] / spec_sigma[mask])),
            real_over_mock_spectrum_rms=float(np.std(real_spec[mask] / spectrum[mask])),
            truth_bins=len(history), spectrum_mask_sha256=hashlib.sha256(mask.tobytes()).hexdigest(),
            mock=str(path.relative_to(ROOT)), mock_sha256=sha(path)))
        print(f'{row["rank"]:3d} {row["target"]} {row["shape"]}: z {row["z"]:.4f}, true age {exact_age:.4f} Gyr, '
              f'S/N real {np.median(real_spec[mask] / spec_stat[mask]):.1f}, calibration {calibration:.3f}', flush=True)
        del ns, prediction
        gc.collect()
        jax.clear_caches()


def inputs():
    """One record of the design, seeds and every mock hash, and the experiment configuration of the subset and the rest."""
    rows = read_design()
    truths = [json.loads((OUT / "truths" / f'{r["target"]}.json').read_text()) for r in rows
              if (OUT / "truths" / f'{r["target"]}.json').exists()]
    for truth in truths:
        assert sha(ROOT / truth["mock"]) == truth["mock_sha256"]
    dump(OUT / "inputs.json", dict(
        source_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        ceridwen_commit=subprocess.check_output(["git", "-C", "ceridwen", "rev-parse", "HEAD"], text=True).strip(),
        formation_time_gyr=FORMATION, shapes={s: dict(
            cosmic_time_edges_gyr=[[float(e[0]), float(e[-1])] for e in shape_history(s)[0]],
            mass_fractions=[float(m.sum()) for m in shape_history(s)[1]]) for s in SHAPES},
        fine_bin_gyr=STEP, noise_seed=NOISE_SEED, fit_seed=FIT_SEED, cosmology=COSMO.to_dict(),
        noise="Independent Gaussian photometry then spectral draws, default_rng([noise_seed, object_id]); spectral floor f_calib * |uncalibrated model| with the real fit's median f_calib, 5% photometric floor; real statistical uncertainties and native validity.",
        choices="Constant truth [Fe/H]=-0.2, [alpha/Fe]=+0.2, no C/N; catalogue redshift; dust, dispersion and log_f_calib: weighted medians of the real dr3_plain_w fit; formed mass from the real photometry; one calibration constant matches the median real window flux; emission zero.",
        mocks=[{k: t[k] for k in ("target", "shape", "subset", "mock", "mock_sha256")} for t in truths]))
    for name, chosen in (("subset", [r for r in rows if r["subset"]]), ("rest", [r for r in rows if not r["subset"]])):
        dump(OUT / f"experiment-{name}.json", dict(
            targets=[r["target"] for r in chosen], seed=FIT_SEED, settings={"data_source": "legac_dr3"}, priors={},
            arms={"mock_w": {"settings": {"rest_range": [4074.5, 4666.1],
                                          "mock_data": str((OUT / "mocks").relative_to(ROOT)) + "/{target}.npz"}}}))
    print(f"{len(truths)} of {len(rows)} mocks recorded")


def check(rows):
    """Each mock through the production reader: loaded arrays, fitted mask and noise scale."""
    results = []
    for row in rows:
        truth = json.loads((OUT / "truths" / f'{row["target"]}.json').read_text())
        data = np.load(ROOT / truth["mock"])
        ns, _ = assemble(row, mock_data=truth["mock"], cells=7)
        mask = np.asarray(ns["spectrum_mask"])
        np.testing.assert_array_equal(mask, data["spectrum_mask"])
        np.testing.assert_array_equal(np.asarray(ns["spectrum_obs"].flux)[mask], data["spectrum_flux"][mask])
        np.testing.assert_array_equal(np.asarray(ns["spectrum_obs"].uncertainty)[mask], data["spectrum_uncertainty"][mask])
        np.testing.assert_array_equal(np.asarray(ns["phot_flux"]), data["photometry_flux"])
        np.testing.assert_array_equal(list(ns["FILTER_NAMES"]), list(data["filter_names"]))
        rest = np.asarray(ns["spectrum_wave"])[mask] / (1.0 + row["z"])
        assert 4074.5 <= rest.min() and rest.max() <= 4666.1
        pull = ((data["spectrum_flux"] - data["mean_spectrum"]) / data["spectrum_noise_sigma"])[mask]
        phot_pull = (data["photometry_flux"] - data["mean_photometry"]) / data["photometry_noise_sigma"]
        times, history, age = lookback_history(row["shape"], float(age_gyr(row["z"], COSMO)))
        np.testing.assert_allclose(age, float(data["true_age_gyr"]), atol=1e-12, rtol=0)
        results.append(dict(target=row["target"], shape=row["shape"], z=row["z"], fitted_pixels=int(mask.sum()),
                            spectrum_pull_mean=float(pull.mean()), spectrum_pull_std=float(pull.std()),
                            photometry_pull_std=float(phot_pull.std()), sn_real=truth["sn_real"],
                            sn_mock_statistical=truth["sn_mock_statistical"],
                            calibration_constant=truth["truth"]["calibration_constant"],
                            logmass_shift=truth["logmass_shift_from_real_fit"], true_age_gyr=age))
        del ns
        gc.collect()
        jax.clear_caches()
    return results


def line_fit(z, y):
    """Least squares and the galaxy bootstrap of results/legac-dr3-2026-11-11/analysis.ipynb, with a 95% interval added."""
    from scipy.stats import linregress

    fit = linregress(z, y)
    indices = np.random.default_rng(BOOTSTRAP_SEED).integers(0, len(z), size=(10000, len(z)))
    zc = z[indices] - z[indices].mean(axis=1, keepdims=True)
    draws = np.sum(zc * y[indices], axis=1) / np.sum(zc**2, axis=1)
    q = np.quantile(draws, [0.025, 0.16, 0.84, 0.975]).tolist()
    return dict(slope=float(fit.slope), q025=q[0], q16=q[1], q84=q[2], q975=q[3],
                scatter=float(np.std(y - fit.intercept - fit.slope * z, ddof=2)))


def summarize():
    """Per-mock recoveries, age-redshift slopes against truth, and age bias in redshift and S/N thirds."""
    import h5py
    from scripts.experiment import validate_result

    rows = []
    for row in read_design():
        found = list((OUT / "runs").glob(f'*/fits/mock_w/{row["object_id"]}-{row["target"]}'))
        if not found:
            continue
        directory, = found
        validate_result(directory)
        truth = json.loads((OUT / "truths" / f'{row["target"]}.json').read_text())
        assert sha(ROOT / truth["mock"]) == truth["mock_sha256"]
        data = np.load(ROOT / truth["mock"])
        with h5py.File(directory / "ceridwen_derived_outputs.h5") as stored:
            assert int(stored.attrs["random_seed"]) == FIT_SEED and float(stored.attrs["redshift"]) == row["z"]
            mask = np.asarray(stored["spectrum/mask"])
            np.testing.assert_array_equal(mask, data["spectrum_mask"])
            np.testing.assert_array_equal(np.asarray(stored["spectrum/observed"])[mask], data["spectrum_flux"][mask])
            np.testing.assert_array_equal(np.asarray(stored["photometry/observed"]), data["photometry_flux"])
            names = stored["summary/parameter"].asstr()[:]
            q = {k: dict(zip(names, stored[f"summary/{k}"][:])) for k in ("q16", "q50", "q84")}
        age = [float(q[k]["mass-weighted age [Gyr]"]) for k in q]  # the estimator of the real window-194 table
        rows.append(dict(rank=row["rank"], target=row["target"], shape=row["shape"], subset=row["subset"], z=row["z"],
                         sn=truth["sn_mock_statistical"], true_age_gyr=truth["true_age_gyr"],
                         ssp_weight_age_gyr=truth["ssp_weight_age_gyr"], age_q16=age[0],
                         age_q50=age[1], age_q84=age[2], age_bias_gyr=age[1] - truth["true_age_gyr"],
                         age_truth_inside=age[0] <= truth["true_age_gyr"] <= age[2],
                         afe_q50=float(q["q50"]["afe"]), afe_bias=float(q["q50"]["afe"]) - TRUE_AFE,
                         feh_q50=float(q["q50"]["logzsol"]), feh_bias=float(q["q50"]["logzsol"]) - TRUE_FEH,
                         path=str(directory.relative_to(ROOT))))
    table(OUT / "per-mock.csv", rows)
    column = lambda chosen, name: np.array([r[name] for r in chosen], dtype=float)
    slopes = []
    for group in ("all", *SHAPES):
        chosen = [r for r in rows if group in ("all", r["shape"])]
        if len(chosen) < 5:
            continue
        z, age, true, bias = (column(chosen, n) for n in ("z", "age_q50", "true_age_gyr", "age_bias_gyr"))
        fit, exact = line_fit(z, age), line_fit(z, true)
        slopes.append(dict(group=group, mocks=len(chosen), true_slope=exact["slope"], recovered_slope=fit["slope"],
                           slope_q16=fit["q16"], slope_q84=fit["q84"], slope_q025=fit["q025"], slope_q975=fit["q975"],
                           recovered_over_true=fit["slope"] / exact["slope"], residual_scatter_gyr=fit["scatter"],
                           median_age_bias_gyr=float(np.median(bias)), mean_age_bias_gyr=float(bias.mean()),
                           age_truth_inside=int(sum(r["age_truth_inside"] for r in chosen)),
                           median_afe_bias=float(np.median(column(chosen, "afe_bias"))),
                           median_feh_bias=float(np.median(column(chosen, "feh_bias")))))
    table(OUT / "slopes.csv", slopes)
    thirds = []
    for name in ("z", "sn"):
        ordered = sorted(rows, key=lambda r: r[name])
        for index, chosen in enumerate(np.array_split(np.arange(len(ordered)), 3)):
            chosen = [ordered[i] for i in chosen]
            bias = column(chosen, "age_bias_gyr")
            thirds.append(dict(quantity=name, third=("low", "middle", "high")[index], mocks=len(chosen),
                               low=chosen[0][name], high=chosen[-1][name], median=float(np.median(column(chosen, name))),
                               median_age_bias_gyr=float(np.median(bias)), mean_age_bias_gyr=float(bias.mean()),
                               standard_error_gyr=float(bias.std(ddof=1) / np.sqrt(len(bias))),
                               age_truth_inside=int(sum(r["age_truth_inside"] for r in chosen))))
    table(OUT / "age-bias-thirds.csv", thirds)
    for r in slopes:
        print(f'{r["group"]:9s} N {r["mocks"]:3d}: slope {r["recovered_slope"]:+.3f} [{r["slope_q16"]:+.3f}, {r["slope_q84"]:+.3f}] '
              f'(95% {r["slope_q025"]:+.3f}, {r["slope_q975"]:+.3f}), truth {r["true_slope"]:+.3f}, ratio {r["recovered_over_true"]:.3f}, '
              f'median bias {r["median_age_bias_gyr"]:+.3f} Gyr, scatter {r["residual_scatter_gyr"]:.3f}, inside {r["age_truth_inside"]}')
    for r in thirds:
        print(f'{r["quantity"]:2s} {r["third"]:6s} {r["low"]:.3f}-{r["high"]:.3f}: bias median {r["median_age_bias_gyr"]:+.3f}, '
              f'mean {r["mean_age_bias_gyr"]:+.3f} +/- {r["standard_error_gyr"]:.3f} Gyr, N {r["mocks"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["design", "generate", "inputs", "check", "summarize"])
    parser.add_argument("--subset", action="store_true", help="the 40-mock subset only")
    parser.add_argument("--shard", default="0/1", help="i/n: every n-th mock, starting at i")
    args = parser.parse_args()
    if args.step == "design":
        return design()
    if args.step == "inputs":
        return inputs()
    if args.step == "summarize":
        return summarize()
    index, count = map(int, args.shard.split("/"))
    rows = [r for r in read_design() if r["subset"] or not args.subset][index::count]
    if args.step == "generate":
        generate(rows)
    else:
        results = check(rows)
        table(OUT / "reader-checks.csv", results)
        print(f"{len(results)} mocks pass the reader check")


if __name__ == "__main__":
    main()
