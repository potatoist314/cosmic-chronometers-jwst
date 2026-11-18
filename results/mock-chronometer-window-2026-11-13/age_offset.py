#!/usr/bin/env python3
"""Why the 194 mock fits return ages older than the truth. Existing fits only; the likelihood runs on the CPU.

    ceridwen/.venv/bin/python results/mock-chronometer-window-2026-11-13/age_offset.py per-mock
    ceridwen/.venv/bin/python results/mock-chronometer-window-2026-11-13/age_offset.py summarize

Per mock: the posterior mass in each SFH bin against the true formation window, the part of the offset that
the fit's own bins give with the true SFH put into them (binning) and the part that is left, the age of the SFH
prior alone, and the production likelihood of the exact truth and of the best fits at fixed age.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import json
import multiprocessing
import sys

import h5py
import jax
import jax.numpy as jnp
from jax.flatten_util import ravel_pytree
import nbformat
import numpy as np
from scipy.optimize import minimize
from scipy.stats import linregress

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import mocks
from mocks import OUT, ROOT, weighted_quantiles

from ceridwen.likelihood.likelihood import observation_data
from ceridwen.sampler.priors import StudentT

EARLIER = ROOT / "results/cn-response-2026-11-10/prior-slope"  # Experiment 9: prior scale 0.3 (P) and 1.0 (W)
PRIOR_SEED = 20261116
PER_MOCK, SUMMARY = OUT / "age-offset-per-mock.csv", OUT / "age-offset.csv"
LIKELIHOOD = ("lnl_truth lnl_posterior_q50 lnl_posterior_max lnl_check_max_abs lnl_free age_free_gyr lnl_true_age "
              "lnl_posterior_age lnl_mirror_age lnl_no_older age_no_older_gyr").split()
FIELDS = ("target shape z universe_age_gyr true_age_gyr age_q16 age_q50 age_q84 age_bias_gyr age_mean_bias_gyr "
          "binned_truth_bias_gyr age_bias_minus_binned_truth_gyr older_bins mass_older truth_mass_older older_gap_gyr "
          "term_older_gyr term_younger_gyr term_overlap_gyr age_bias_other_bins_gyr age_bias_at_zero_older_gyr mass_last "
          "ratio13_q50 ratio14_q16 ratio14_q50 ratio14_q84 prior_age_q16 prior_age_q50 prior_age_q84").split() + LIKELIHOOD


def masses(ratios, edges):
    """Formed-mass fraction of each fit bin. Ceridwen 2.0 fits (one ratio fewer than bins): one SFR per bin.
    Earlier fits (one ratio per bin): the bin SFR is the mean of its two node values."""
    log_sfr = np.concatenate([np.zeros((len(ratios), 1)), -np.cumsum(ratios, axis=1)], axis=1)
    sfr = 10.0 ** (log_sfr - log_sfr.max(axis=1, keepdims=True))
    mass = (sfr if sfr.shape[1] == len(edges) - 1 else 0.5 * (sfr[:, :-1] + sfr[:, 1:])) * np.diff(edges)
    return mass / mass.sum(axis=1, keepdims=True)


def posterior(result, mock):
    """Posterior mass by fit bin against the true formation window of the mock."""
    with h5py.File(result, "r") as stored:
        ratios = stored["samples/logsfr_ratios"][:]
        log_weights, lnl = stored["samples/log_weights"][:], stored["samples/log_likelihoods"][:]
        edges = stored["model/sfh_times_yr"][:] / 1e9
    weights = np.exp(log_weights - log_weights.max())
    weights /= weights.sum()
    mass, mid = masses(ratios, edges), 0.5 * (edges[:-1] + edges[1:])
    age = mass @ mid
    times, fine = mock["time_edges_gyr"], mock["sfh_per_bin"] * np.diff(mock["time_edges_gyr"])
    fine = fine / fine.sum()
    true_age = float(fine @ (0.5 * (times[:-1] + times[1:])))
    truth_mass = np.diff(np.interp(edges, times, np.concatenate([[0.0], np.cumsum(fine)])))
    # Fit bins wholly older or wholly younger than every true star; the others overlap the true window.
    older = edges[:-1] >= times[1:][fine > 0].max() - 1e-9
    younger = edges[1:] <= times[:-1][fine > 0].min() + 1e-9
    mean_mass, shift = weights @ mass, mid - true_age
    quantile = lambda values: weighted_quantiles(values, log_weights, (0.16, 0.5, 0.84))
    # Binning: the bin-midpoint age of the true SFH put into the fit bins, against the true age.
    binned_truth_bias = float(truth_mass @ mid) - true_age
    # Across the posterior samples: weighted least squares of age on the mass in the older bins, read at zero mass.
    sample_older = mass[:, older].sum(axis=1)
    centred = sample_older - weights @ sample_older
    slope = (weights @ (centred * age)) / (weights @ centred**2)
    row = dict(true_age_gyr=true_age, **dict(zip(("age_q16", "age_q50", "age_q84"), quantile(age))),
               age_bias_gyr=quantile(age)[1] - true_age,
               age_mean_bias_gyr=float(weights @ age) - true_age, binned_truth_bias_gyr=binned_truth_bias,
               age_bias_minus_binned_truth_gyr=quantile(age)[1] - true_age - binned_truth_bias, older_bins=int(older.sum()),
               mass_older=float(mean_mass[older].sum()), truth_mass_older=float(truth_mass[older].sum()),
               older_gap_gyr=float(edges[:-1][older].min() - times[1:][fine > 0].max()),
               term_older_gyr=float(mean_mass[older] @ shift[older]),
               term_younger_gyr=float(mean_mass[younger] @ shift[younger]),
               term_overlap_gyr=float(mean_mass[~older & ~younger] @ shift[~older & ~younger]),
               # Mean age of the posterior-mean mass outside the older bins.
               age_bias_other_bins_gyr=float(mean_mass[~older] @ mid[~older] / mean_mass[~older].sum()) - true_age,
               age_bias_at_zero_older_gyr=float(weights @ age - slope * (weights @ sample_older)) - true_age,
               mass_last=float(mean_mass[-1]),
               ratio13_q50=quantile(ratios[:, 12])[1],
               # Ceridwen 2.0 fits have 13 ratios: no ratio 14.
               **dict(zip(("ratio14_q16", "ratio14_q50", "ratio14_q84"),
                          quantile(ratios[:, 13]) if ratios.shape[1] > 13 else [float("nan")] * 3)))
    return row, dict(ratios=ratios, weights=weights, lnl=lnl, edges=edges, age=age, older=older, mass=mass,
                     log_weights=log_weights)


def prior_ages(edges, n_ratios):
    """Mass-weighted age of the SFH prior alone, as prior_only() of Experiment 9, on these bin edges."""
    if not hasattr(prior_ages, "draws"):
        prior_ages.draws = np.asarray(StudentT(mean=0.0, scale=0.3, df=2.0).sample(
            jax.random.PRNGKey(PRIOR_SEED), (200000, 14)))
    return np.quantile(masses(prior_ages.draws[:, :n_ratios], edges) @ (0.5 * (edges[:-1] + edges[1:])), [0.16, 0.5, 0.84])


def likelihood(row, truth, mock, fit):
    """Production ln L (calibration and emission lines marginalised) of the truth and of fits at fixed age."""
    ns, _ = mocks.assemble(row, mock_data=truth["mock"])
    cell = nbformat.read(ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb", as_version=4).cells[10].source
    exec(cell[cell.index("calibration_polynomial = "):cell.index("model_parameter_block_text")], ns)
    model, joint = ns["joint_model"], ns["joint_likelihood"]
    data = {key: observation_data(model.obs_dict[key]) for key in joint.keys}
    names = sorted(model.theta_init)  # ravel_pytree order
    with h5py.File(ROOT / row_path(row) / "ceridwen_result.h5", "r") as stored:
        samples = np.concatenate([stored["samples"][name][:].reshape(len(fit["lnl"]), -1) for name in names], axis=1)
    _, unravel = ravel_pytree({name: jnp.asarray(model.theta_init[name], dtype=float) for name in names})
    lnl = lambda x: joint.loglike(data, model.predict(unravel(x)), unravel(x), None)
    order = np.argsort(fit["lnl"])
    # The local CPU likelihood against the stored values of the GPU fit.
    check = max(abs(float(lnl(jnp.asarray(samples[index]))) - fit["lnl"][index]) for index in order[[-1, -100, -1000]])
    assert check < 0.2
    # The exact truth: noise-free mock fluxes as the prediction, with the truth's floor and dispersion.
    exact = {"photometry": jnp.asarray(mock["mean_photometry"]),
             "spectrum": jnp.asarray(mock["mean_spectrum"] / truth["truth"]["calibration_constant"])}
    lnl_truth = float(joint.loglike(data, exact, {k: jnp.array([truth["truth"][k]]) for k in ("log_f_calib", "sigma_smooth")}, None))

    dt, mid, older = jnp.asarray(np.diff(fit["edges"])), jnp.asarray(0.5 * (fit["edges"][:-1] + fit["edges"][1:])), jnp.asarray(fit["older"])

    def bin_mass(x):
        log_sfr = jnp.concatenate([jnp.zeros(1), -jnp.cumsum(unravel(x)["logsfr_ratios"])])
        sfr = 10.0 ** (log_sfr - log_sfr.max())
        mass = (sfr if sfr.shape[0] == dt.shape[0] else 0.5 * (sfr[:-1] + sfr[1:])) * dt
        return mass / mass.sum()

    age = lambda x: bin_mass(x) @ mid
    mass_older = lambda x: jnp.sum(jnp.where(older, bin_mass(x), 0.0))
    bounds = []
    for name in names:  # uniform and clipped priors: their limits; the unbounded StudentT ratios: +-5 dex
        prior = model.priors[name].params
        bounds += [(-5.0, 5.0) if name == "logsfr_ratios" else (float(prior["low"]), float(prior["high"]))] * int(np.size(model.theta_init[name]))
    true_age, posterior_age = float(fit["true_age"]), float(fit["age_q50"])
    mirror_age = 2 * true_age - posterior_age  # as far from the truth as the posterior median, on the other side
    solve = lambda function, start, steps: minimize(
        lambda x: tuple(np.asarray(v, dtype=float) for v in function(jnp.asarray(x))), start, jac=True,
        method="L-BFGS-B", bounds=bounds, options=dict(maxiter=steps, maxfun=4 * steps, ftol=1e-15, gtol=1e-6))
    fixed_age = jax.jit(jax.value_and_grad(lambda x, target, width: -lnl(x) + 0.5 * ((age(x) - target) / width) ** 2))
    fixed_older = jax.jit(jax.value_and_grad(lambda x, target, width: -lnl(x) + 0.5 * ((mass_older(x) - target) / width) ** 2))

    def best(objective, target, width, values):
        """Maximum ln L with one quantity held at target: a quadratic penalty, tightened in three stages."""
        near = np.argsort(np.abs(values - target))[:200]  # the samples nearest the constraint
        runs = []
        for x in (samples[near[np.argmax(fit["lnl"][near])]], samples[near[0]], samples[order[-1]], samples[order[-30]]):
            for scale, steps in ((20.0, 500), (4.0, 500), (1.0, 5000)):
                run = solve(lambda z: objective(z, target, scale * width), x, steps)
                x = run.x
            runs.append(run)
        return jnp.asarray(min(runs, key=lambda run: run.fun).x)

    fixed = {"true_age": best(fixed_age, true_age, 0.005, fit["age"]),
             "posterior_age": best(fixed_age, posterior_age, 0.005, fit["age"]),
             "mirror_age": best(fixed_age, mirror_age, 0.005, fit["age"]),
             "no_older": best(fixed_older, 0.0, 0.002, fit["mass"][:, fit["older"]].sum(axis=1))}
    # A constrained fit that misses its constraint gives no value (NaN).
    met = {"true_age": abs(float(age(fixed["true_age"])) - true_age) < 0.02,
           "posterior_age": abs(float(age(fixed["posterior_age"])) - posterior_age) < 0.02,
           "mirror_age": abs(float(age(fixed["mirror_age"])) - mirror_age) < 0.02,
           "no_older": float(mass_older(fixed["no_older"])) < 0.01}
    held = lambda name, function=lnl: float(function(fixed[name])) if met[name] else float("nan")
    # Unconstrained maximum: from the best samples and from each constrained solution.
    runs = [solve(lambda z: fixed_age(z, 0.0, 1e30), start, 5000)
            for start in [samples[order[-1]], samples[order[-30]], *map(np.asarray, fixed.values())]]
    free = jnp.asarray(min(runs, key=lambda run: run.fun).x)
    return dict(lnl_truth=lnl_truth, lnl_posterior_q50=weighted_quantiles(fit["lnl"], fit["log_weights"], (0.5,))[0],
                lnl_posterior_max=float(fit["lnl"].max()), lnl_check_max_abs=check, lnl_free=float(lnl(free)), age_free_gyr=float(age(free)),
                lnl_true_age=held("true_age"), lnl_posterior_age=held("posterior_age"), lnl_mirror_age=held("mirror_age"),
                lnl_no_older=held("no_older"), age_no_older_gyr=held("no_older", age))


def row_path(row):
    if not hasattr(row_path, "paths"):
        row_path.paths = {r["target"]: r["path"] for r in csv.DictReader((OUT / "per-mock.csv").open())}
    return row_path.paths[row["target"]]


def one(job):
    row, stored = job
    truth = json.loads((OUT / "truths" / f'{row["target"]}.json').read_text())
    mock = dict(np.load(ROOT / truth["mock"]))
    stats, fit = posterior(ROOT / row_path(row) / "ceridwen_result.h5", mock)
    np.testing.assert_allclose(stats["true_age_gyr"], truth["true_age_gyr"], atol=1e-9)
    prior = prior_ages(fit["edges"], fit["ratios"].shape[1])
    out = dict(target=row["target"], shape=row["shape"], z=row["z"], universe_age_gyr=truth["universe_age_gyr"], **stats,
               prior_age_q16=prior[0], prior_age_q50=prior[1], prior_age_q84=prior[2],
               **(stored or likelihood(row, truth, mock, dict(fit, true_age=stats["true_age_gyr"], age_q50=stats["age_q50"]))))
    return {name: out[name] for name in FIELDS}


def per_mock(workers):
    """One row per mock. The likelihood columns of a mock already in the table are kept, not run again."""
    stored = ({r["target"]: {k: float(r[k]) for k in LIKELIHOOD} for r in csv.DictReader(PER_MOCK.open())}
              if PER_MOCK.exists() else {})
    jobs = [(r, stored.get(r["target"])) for r in mocks.read_design()]
    with ProcessPoolExecutor(workers, multiprocessing.get_context("spawn")) as pool:
        rows = []
        for result in pool.map(one, jobs):
            rows.append(result)
            mocks.table(PER_MOCK, rows)
            print(len(rows), len(jobs), result["target"], flush=True)


def summarize():
    rows = [{k: (v if k in ("target", "shape") else float(v)) for k, v in r.items()} for r in csv.DictReader(PER_MOCK.open())]
    assert len(rows) == 194
    median = lambda group, name: float(np.median([r[name] for r in group]))
    difference = lambda group, a, b: (lambda d: d[np.isfinite(d)])(np.array([r[a] - r[b] for r in group]))
    out = []
    binning = lambda low, high: [r for r in rows if low <= r["binned_truth_bias_gyr"] < high]
    for name, group in ([("all", rows)] + [(s, [r for r in rows if r["shape"] == s]) for s in mocks.SHAPES]
                        # Mocks sorted by the offset that the fit bins give with the true SFH put into them.
                        + [("binning_under_0.1_gyr", binning(-np.inf, 0.1)), ("binning_0.1_to_0.3_gyr", binning(0.1, 0.3)),
                           ("binning_over_0.3_gyr", binning(0.3, np.inf))]):
        flat = difference(group, "lnl_posterior_age", "lnl_true_age")
        # Offset against the binning term over the mocks: a slope of 1 if the binning term added to the offset.
        line = linregress([r["binned_truth_bias_gyr"] for r in group], [r["age_bias_gyr"] for r in group])
        out.append(dict(
            sample=name, prior_scale=0.3, mocks=len(group), age_bias_gyr=median(group, "age_bias_gyr"),
            binned_truth_bias_gyr=median(group, "binned_truth_bias_gyr"),
            age_bias_minus_binned_truth_gyr=median(group, "age_bias_minus_binned_truth_gyr"),
            offset_slope_on_binned_truth=float(line.slope), offset_slope_error=float(line.stderr),
            offset_binned_truth_r=float(line.rvalue),
            mass_older=median(group, "mass_older"), truth_mass_older_max=max(r["truth_mass_older"] for r in group),
            older_gap_gyr=median(group, "older_gap_gyr"), term_older_gyr=median(group, "term_older_gyr"),
            term_younger_gyr=median(group, "term_younger_gyr"), term_overlap_gyr=median(group, "term_overlap_gyr"),
            age_bias_other_bins_gyr=median(group, "age_bias_other_bins_gyr"),
            age_bias_at_zero_older_gyr=median(group, "age_bias_at_zero_older_gyr"),
            prior_age_minus_truth_gyr=float(np.median(difference(group, "prior_age_q50", "true_age_gyr"))),
            ratio14_q16=median(group, "ratio14_q16"), ratio14_q50=median(group, "ratio14_q50"),
            ratio14_q84=median(group, "ratio14_q84"),
            lnl_truth_minus_posterior_q50=float(np.median(difference(group, "lnl_truth", "lnl_posterior_q50"))),
            truth_at_or_above_posterior_q50=int(np.sum(difference(group, "lnl_truth", "lnl_posterior_q50") >= 0)),
            fixed_age_fits=len(flat),
            lnl_posterior_age_minus_true_age_q16=float(np.quantile(flat, 0.16)),
            lnl_posterior_age_minus_true_age_q50=float(np.median(flat)),
            lnl_posterior_age_minus_true_age_q84=float(np.quantile(flat, 0.84)),
            lnl_true_age_minus_mirror_age=float(np.median(difference(group, "lnl_true_age", "lnl_mirror_age"))),
            mirror_age_fits=len(difference(group, "lnl_true_age", "lnl_mirror_age")),
            lnl_free_minus_true_age=float(np.median(difference(group, "lnl_free", "lnl_true_age"))),
            true_age_within_half_lnl_of_best=int(np.sum(difference(group, "lnl_free", "lnl_true_age") < 0.5)),
            true_age_inside_posterior_68=int(np.sum([r["age_q16"] <= r["true_age_gyr"] <= r["age_q84"] for r in group])),
            lnl_free_minus_no_older=float(np.median(difference(group, "lnl_free", "lnl_no_older"))),
            age_bias_no_older_gyr=float(np.median(difference(group, "age_no_older_gyr", "true_age_gyr")))))
    # Experiment 9: the same 30 mocks fitted with the production prior scale (P) and a wider one (W).
    earlier = list(csv.DictReader((EARLIER / "per-mock.csv").open()))
    for arm, scale in (("P", 0.3), ("W", 1.0)):
        group = [posterior(ROOT / r["result_path"], np.load(EARLIER / "mocks" / f'{r["target"]}_s{r["noise_seed"]}.npz'))[0]
                 for r in earlier if r["arm"] == arm]
        out.append(dict(dict.fromkeys(out[0]), sample=f"experiment9_{arm}", prior_scale=scale, mocks=len(group),
                        true_age_inside_posterior_68=int(np.sum([r["age_q16"] <= r["true_age_gyr"] <= r["age_q84"] for r in group])),
                        truth_mass_older_max=max(r["truth_mass_older"] for r in group),
                        **{name: median(group, name) for name in (
                            "age_bias_gyr", "binned_truth_bias_gyr", "age_bias_minus_binned_truth_gyr", "mass_older",
                            "older_gap_gyr", "term_older_gyr", "term_younger_gyr", "term_overlap_gyr",
                            "age_bias_other_bins_gyr", "age_bias_at_zero_older_gyr", "ratio14_q16", "ratio14_q50",
                            "ratio14_q84")}))
    mocks.table(SUMMARY, out)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["per-mock", "summarize"])
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    summarize() if args.step == "summarize" else per_mock(args.workers)
