#!/usr/bin/env python3
"""SFH prior alone (no data) on the 194 mock fits' own bin edges: production node ratios against bin ratios.

    JAX_PLATFORMS=cpu ceridwen/.venv/bin/python results/upstream-2-0-check-2026-11-17/prior_test.py

node14: production. 14 ratios ~ StudentT(0, 0.3, 2) give 15 node SFRs (logsfr_ratios_to_sfh); the step fast
        path uses each bin's node mean (ceridwen/ceridwen/csp/csp_afe.py:437).
bin13:  Leja+2019 Eq. 4 / ceridwen 2.0.0. 13 ratios of adjacent bin SFRs ~ StudentT(0, 0.3, 2) give 14 bin SFRs.

prior-test.csv: per prior, the Jacobian of bin mass fractions on the ratios, the implied log10 ratio of adjacent
bin SFRs, and the mass-weighted age and mass in bins older than any true star (medians over the 194 mocks).
prior-test-per-mock.csv: the same per mock. prior-test-bins.csv: prior mean mass fraction per bin.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import h5py
import jax
import jax.numpy as jnp
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MOCK = ROOT / "results/mock-chronometer-window-2026-11-13"
sys.path.insert(0, str(MOCK))
from age_offset import PRIOR_SEED, masses  # node14 masses as the age-offset analysis computed them

from ceridwen.model import logsfr_ratios_to_sfh
from ceridwen.sampler.priors import StudentT

SEED = 20261117  # bin13 draws; node14 reuses PRIOR_SEED of age_offset.py
DRAWS = 200000
PRIOR = StudentT(mean=0.0, scale=0.3, df=2.0)


def bin_masses(ratios, edges):
    """Formed-mass fraction of each bin from ratios of adjacent BIN SFRs (ceridwen 2.0 / Prospector)."""
    log_sfr = np.concatenate([np.zeros((len(ratios), 1)), -np.cumsum(ratios, axis=1)], axis=1)
    mass = 10.0 ** (log_sfr - log_sfr.max(axis=1, keepdims=True)) * np.diff(edges)
    return mass / mass.sum(axis=1, keepdims=True)


def jacobian_ratio(edges_yr, ratios, per_bin):
    """Singular values of d(bin mass fractions)/d(ratios) at each draw, over the largest."""
    dt = jnp.diff(jnp.asarray(edges_yr))

    def fractions(r):
        if per_bin:
            mass = 10.0 ** jnp.concatenate([jnp.zeros(1), -jnp.cumsum(r)]) * dt
        else:
            node = logsfr_ratios_to_sfh(r, sfh_times_yr=edges_yr)   # what the notebook's sfh transform returns
            mass = 0.5 * (node[:-1] + node[1:]) * dt                # csp_afe.py:437
        return mass / jnp.sum(mass)

    sv = jax.vmap(lambda r: jnp.linalg.svd(jax.jacfwd(fractions)(r), compute_uv=False))(jnp.asarray(ratios))
    return np.asarray(sv / sv[:, :1])


def main():
    design = list(csv.DictReader((MOCK / "per-mock.csv").open()))
    stored = {r["target"]: r for r in csv.DictReader((MOCK / "age-offset-per-mock.csv").open())}
    node = np.asarray(PRIOR.sample(jax.random.PRNGKey(PRIOR_SEED), (DRAWS, 14)))
    binr = np.asarray(PRIOR.sample(jax.random.PRNGKey(SEED), (DRAWS, 13)))
    rows, per_bin = [], {"node14": [], "bin13": []}
    for row in design:
        with h5py.File(ROOT / row["path"] / "ceridwen_result.h5", "r") as f:
            edges = f["model/sfh_times_yr"][:] / 1e9
        truth = json.loads((MOCK / "truths" / f'{row["target"]}.json').read_text())
        mock = np.load(ROOT / truth["mock"])
        times, fine = mock["time_edges_gyr"], mock["sfh_per_bin"] * np.diff(mock["time_edges_gyr"])
        older = edges[:-1] >= times[1:][fine > 0].max() - 1e-9   # as age_offset.posterior
        mid = 0.5 * (edges[:-1] + edges[1:])
        out = dict(target=row["target"], shape=row["shape"], z=float(row["z"]), true_age_gyr=float(row["true_age_gyr"]),
                   older_bins=int(older.sum()), posterior_mass_older=float(stored[row["target"]]["mass_older"]),
                   posterior_age_q50=float(row["age_q50"]))
        for name, mass in (("node14", masses(node, edges)), ("bin13", bin_masses(binr, edges))):
            age = mass @ mid
            q = np.quantile(age, [0.16, 0.5, 0.84])
            out.update({f"{name}_age_q16": q[0], f"{name}_age_q50": q[1], f"{name}_age_q84": q[2],
                        f"{name}_age_mean": float(age.mean()),
                        f"{name}_mass_older_mean": float(mass[:, older].sum(axis=1).mean()),
                        f"{name}_mass_older_q50": float(np.median(mass[:, older].sum(axis=1)))})
            per_bin[name].append(mass.mean(axis=0))
        # node14 reproduces the age-offset table's prior ages (same seed, same map)
        np.testing.assert_allclose(out["node14_age_q50"], float(stored[row["target"]]["prior_age_q50"]), rtol=1e-12)
        rows.append(out)
    with (OUT / "prior-test-per-mock.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # Implied prior on log10 ratios of adjacent BIN SFRs (the quantity Leja+2019 Eq. 4 constrains), z-median edges.
    ref = sorted(design, key=lambda r: float(r["z"]))[len(design) // 2]
    with h5py.File(ROOT / ref["path"] / "ceridwen_result.h5", "r") as f:
        ref_edges_yr = f["model/sfh_times_yr"][:]
    # In log space: heavy-tailed draws underflow a linear SFR.
    ln_node = np.log(10.0) * np.concatenate([np.zeros((DRAWS, 1)), -np.cumsum(node, axis=1)], axis=1)
    ln_bin = np.logaddexp(ln_node[:, :-1], ln_node[:, 1:])          # bin SFR = node mean, up to a constant
    implied = {"node14": (ln_bin[:, :-1] - ln_bin[:, 1:]) / np.log(10.0), "bin13": binr}
    cond = {"node14": jacobian_ratio(ref_edges_yr, node[:2000], per_bin=False),
            "bin13": jacobian_ratio(ref_edges_yr, binr[:2000], per_bin=True)}

    median = lambda key: float(np.median([r[key] for r in rows]))
    summary = []
    for name, n in (("node14", 14), ("bin13", 13)):
        r = implied[name]
        summary.append(dict(
            prior=name, ratios=n, bins=14,
            # Jacobian (14 bin fractions x n ratios): rank, and the smallest singular value over the largest
            jacobian_smin_over_smax_max=float(cond[name][:, -1].max()),
            jacobian_smin_over_smax_median=float(np.median(cond[name][:, -1])),
            bin_ratio_q16=float(np.quantile(r, 0.16)), bin_ratio_q50=float(np.quantile(r, 0.5)),
            bin_ratio_q84=float(np.quantile(r, 0.84)),
            bin_ratio_frac_abs_gt_1dex=float(np.mean(np.abs(r) > 1.0)),
            age_q50_minus_truth_gyr=float(np.median([r_[f"{name}_age_q50"] - r_["true_age_gyr"] for r_ in rows])),
            age_mean_gyr=median(f"{name}_age_mean"),
            age_q16_gyr=median(f"{name}_age_q16"), age_q50_gyr=median(f"{name}_age_q50"), age_q84_gyr=median(f"{name}_age_q84"),
            mass_older_mean=median(f"{name}_mass_older_mean"), mass_older_q50=median(f"{name}_mass_older_q50"),
            posterior_mass_older=median("posterior_mass_older"), mocks=len(rows)))
    with (OUT / "prior-test.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)

    # Prior mean mass fraction by bin index (0 = youngest), median over the 194 mocks' edges.
    with (OUT / "prior-test-bins.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bin", "node14_mass_mean", "bin13_mass_mean", "z_median_edges_lo_gyr", "z_median_edges_hi_gyr"])
        a, b = np.median(per_bin["node14"], axis=0), np.median(per_bin["bin13"], axis=0)
        for k in range(14):
            w.writerow([k, a[k], b[k], ref_edges_yr[k] / 1e9, ref_edges_yr[k + 1] / 1e9])
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
