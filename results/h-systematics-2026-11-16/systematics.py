"""Shifts of the chronometer H under variations that already have fits. No new fits.

Run from the repository root:
    ceridwen/.venv/bin/python results/h-systematics-2026-11-16/systematics.py

Baseline: 194 LEGA-C DR3 galaxies, rest 4074.5-4666.1 A, C/N-free fit, least-squares
line of mass-weighted age against z, H at the effective redshift of that line.

Each variant j is compared with a fit c on the same bootstrap resamples:
    dH = (H_j(z_j) - H_P18(z_j)) - (H_c(z_c) - H_P18(z_c))
z_j is the redshift at which the same estimator on Planck18 ages equals dt/dz, so a
subset or estimator with another effective redshift is compared at its own redshift
(the model correction of Jiao+2023 Eq. 11). Same galaxies and estimator: dH = H_j - H_c.
"""

from __future__ import annotations

import json
import sys
import warnings
from functools import lru_cache
from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.cosmology import Planck18
from astropy.table import Table
from scipy.optimize import brentq
from scipy.stats import median_abs_deviation

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from chronometer import (  # noqa: E402
    GYR_INV_TO_KM_S_MPC,
    effective_redshift,
    fit_common_age_slope,
    hubble_from_age_difference,
    hubble_uncertainty_from_age_errors,
    inverse_variance_combine,
)

SEED, DRAWS = 20261110, 10000  # as results/carbon-mask-window-2026-11-13
MOCK_PRIOR_SEED = 20261129  # as results/cn-response-2026-11-10/prior-slope/analyse.py
COST_PER_FIT = 0.10
Z_GRID = np.linspace(0.4, 1.2, 4001)
H_GRID = Planck18.H(Z_GRID).value


def planck_age(z):
    return Planck18.age(z).to_value(u.Gyr)


def planck_h(z):
    return np.interp(z, Z_GRID, H_GRID)


@lru_cache(maxsize=None)
def resample(n, seed=SEED):
    """Bootstrap indices and the matching count of each galaxy in each draw."""
    indices = np.random.default_rng(seed).integers(0, n, size=(DRAWS, n))
    counts = np.zeros((DRAWS, n))
    np.add.at(counts, (np.arange(DRAWS)[:, None], indices), 1.0)
    return indices, counts


def coefficient(design, y, weights, column):
    """Weighted least-squares coefficient, one per row of weights."""
    p = design.shape[1]
    a = (weights @ (design[:, :, None] * design[:, None, :]).reshape(len(y), -1)).reshape(-1, p, p)
    b = weights @ (design * y[:, None])
    return np.linalg.solve(a, b[:, :, None])[:, column, 0]


def hubble(z_eff, slope):
    """H from dt/dz; a slope that is not negative has no finite H."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(slope < 0, -GYR_INV_TO_KM_S_MPC / ((1 + z_eff) * slope), np.inf)


def line(z, age, counts=None, design=None, column=1, keep=None):
    """Slope estimate and its bootstrap draws; element 0 is the estimate on the data."""
    keep = np.ones(len(z), bool) if keep is None else np.asarray(keep)
    design = np.column_stack((np.ones_like(z), z)) if design is None else design
    weights = keep[None, :].astype(float)
    if counts is not None:
        weights = np.vstack((weights, counts * keep))
    slope = coefficient(design, age, weights, column)
    ref = coefficient(design, planck_age(z), weights[:1], column)[0]
    z_eff = brentq(
        lambda x: -(1 / ((1 + x) * Planck18.H(x))).to_value(u.Gyr) - ref,
        z[keep].min(), z[keep].max(), xtol=1e-10,
    )
    h = hubble(z_eff, slope)
    return dict(n=int(keep.sum()), z_eff=z_eff, slope=slope, ref=ref, h=h, excess=h - planck_h(z_eff))


def bin_labels(z, sigma, n_z, z_bins, n_sigma):
    edges = (
        np.linspace(z.min(), z.max(), n_z + 1)
        if z_bins == "fixed"
        else np.quantile(z, np.linspace(0, 1, n_z + 1))
    )
    z_bin = np.clip(np.searchsorted(edges, z, side="right") - 1, 0, n_z - 1)
    sigma_bin = (sigma > np.median(sigma)).astype(int) if n_sigma == 2 else np.zeros(len(z), int)
    return sigma_bin * n_z + z_bin


def binned_h(z, age, labels, n_z, n_sigma, centre):
    """H from bin i and bin i + n_z/2 inside each sigma-star bin, inverse-variance mean.

    Borghi+2022b Sect. 3; Jiao+2023 Sect. 5.1-5.2 (median age, error MAD / sqrt(N)).
    """
    stat = np.median if centre == "median" else np.mean
    bins = []
    for label in range(n_z * n_sigma):
        a = age[labels == label]
        error = median_abs_deviation(a) if centre == "median" else np.std(a, ddof=1)
        bins.append((stat(z[labels == label]), stat(a), error / np.sqrt(len(a))))
    h, errors, z_eff = [], [], []
    for s in range(n_sigma):
        for i in range(n_z // 2):
            low, high = bins[s * n_z + i], bins[s * n_z + i + n_z // 2]
            pair_z, pair_h = hubble_from_age_difference(low[0], high[0], low[1], high[1])
            errors.append(hubble_uncertainty_from_age_errors(pair_h, high[1] - low[1], low[2], high[2]))
            h.append(pair_h)
            z_eff.append(pair_z)
    value, error = inverse_variance_combine(np.array(h), np.array(errors))
    weight = np.array(errors) ** -2
    return value, error, float(np.sum(weight * z_eff) / weight.sum())


def binned(z, age, sigma, indices, n_z, z_bins, n_sigma, centre):
    """Binned H and its bootstrap draws; bin edges stay those of the data."""
    labels = bin_labels(z, sigma, n_z, z_bins, n_sigma)
    value, error, z_eff = binned_h(z, age, labels, n_z, n_sigma, centre)
    h, excess = np.full(DRAWS + 1, np.nan), np.full(DRAWS + 1, np.nan)
    h[0], excess[0] = value, value - planck_h(z_eff)
    for draw, i in enumerate(indices, start=1):
        try:  # a draw with an empty or one-galaxy bin has no H
            h[draw], _, draw_z = binned_h(z[i], age[i], labels[i], n_z, n_sigma, centre)
            excess[draw] = h[draw] - planck_h(draw_z)
        except ValueError:
            pass
    nan = np.full(DRAWS + 1, np.nan)
    return dict(n=len(z), z_eff=z_eff, slope=nan, ref=np.nan, h=h, excess=excess, error=error)


def interval(draws):
    return np.nanquantile(draws, [0.16, 0.84, 0.025, 0.975, 0.5], method="nearest")


def shift(term, variant, compared_with, var, cmp, in_total=True, note=""):
    with np.errstate(invalid="ignore"):
        d_slope = (var["slope"] - var["ref"]) - (cmp["slope"] - cmp["ref"])
        d_h = var["excess"] - cmp["excess"]
    s, h = interval(d_slope[1:]), interval(d_h[1:])
    pct = 100 / cmp["h"][0]
    return dict(
        term=term, variant=variant, compared_with=compared_with, n=var["n"], n_compared=cmp["n"],
        slope=var["slope"][0], slope_compared=cmp["slope"][0],
        dslope=d_slope[0], dslope_q16=s[0], dslope_q84=s[1], dslope_q025=s[2], dslope_q975=s[3],
        z_eff=var["z_eff"], H=var["h"][0], H_compared=cmp["h"][0],
        dH=d_h[0], dH_q16=h[0], dH_q84=h[1], dH_q025=h[2], dH_q975=h[3], dH_bootstrap_median=h[4],
        dH_pct=pct * d_h[0], dH_pct_q16=pct * h[0], dH_pct_q84=pct * h[1],
        resolved_95=bool(h[2] > 0 or h[3] < 0), in_total=in_total, note=note,
    )


def selection_columns(targets):
    """NUVrJ margin, [O II] EW and sigma-star of the targets from the DR3 catalogue."""
    table = Table.read(ROOT / "data/raw/legac_dr3/legac_DR3.fits")
    cat = table[[n for n in table.colnames if len(table[n].shape) <= 1]].to_pandas()
    if isinstance(cat.SPECT_ID.iloc[0], bytes):
        cat["SPECT_ID"] = cat.SPECT_ID.str.decode("ascii")
    cat["SPECT_ID"] = cat.SPECT_ID.str.strip()
    phot = Table.read(ROOT / "data/raw/cosmos2015/cosmos2015_legac_dr3_photometry_1arcsec.fits").to_pandas()
    cat = cat.reset_index().merge(
        phot[["LEGAC_INDEX", "NUVMag", "RMag", "JMag"]], left_on="index", right_on="LEGAC_INDEX", how="left"
    )
    nuv_r, r_j = cat.NUVMag - cat.RMag, cat.RMag - cat.JMag
    cat["nuvrj_margin"] = np.minimum(nuv_r - (3 * r_j + 1), nuv_r - 3.1)
    return cat.set_index("SPECT_ID").loc[targets, ["nuvrj_margin", "OII_3727_EW", "SIGMA_STARS_PRIME"]]


def main():
    warnings.simplefilter("ignore", RuntimeWarning)
    rows = []

    # ---- the 194 galaxies -------------------------------------------------------
    fits = pd.read_csv(ROOT / "results/legac-dr3-2026-11-11/window-194-fits.csv")
    dr3 = fits[fits.release == "dr3"]
    base = dr3[dr3.arm == "cn_free"].set_index("target")
    names, z = base.index.to_numpy(), base.z.to_numpy()
    ages = {
        "cn_free": base.age_gyr_q50.to_numpy(),
        "plain": dr3[dr3.arm == "plain"].set_index("target").age_gyr_q50.loc[names].to_numpy(),
        "mask": pd.read_csv(ROOT / "results/carbon-mask-window-2026-11-13/window-194-mask-fits.csv")
        .set_index("target").age_gyr_q50.loc[names].to_numpy(),
    }
    age = ages["cn_free"]
    indices, counts = resample(len(z))
    baseline = line(z, age, counts)
    assert np.isclose(baseline["z_eff"], effective_redshift(z)["z_eff"], atol=1e-8)
    h0 = baseline["h"][0]
    stat = interval(baseline["h"][1:])

    # A. abundance treatment
    for arm, label in (("plain", "plain"), ("mask", "carbon mask")):
        rows.append(shift("abundance treatment", f"{label} fit", "C/N-free fit, same 194",
                          line(z, ages[arm], counts), baseline))

    # B. wavelength window: DR2 spectra, plain fit, against the common window
    per_fit = pd.read_csv(ROOT / "results/chronometer-135-2026-11-10/per-fit.csv")
    per_fit = per_fit[per_fit.valid]
    common = per_fit[per_fit.arm == "i_baseline_w110"].set_index("target")
    for arm, label in (
        ("k_baseline_blue", "3743-4666 A (adds H10, H9, H8)"),
        ("l_baseline_red_hb", "4075-4893 A (adds C2 4668, Hbeta)"),
        ("m_baseline_red_mgb", "4075-5208 A (adds C2 4668, Hbeta, Fe5015, Mg b)"),
    ):
        wide = per_fit[per_fit.arm == arm].set_index("target")
        both = wide.index.intersection(common.index)
        zc, c = common.z.loc[both].to_numpy(), resample(len(both))[1]
        rows.append(shift("wavelength window", label, "4075-4666 A, same DR2 galaxies, plain fit",
                          line(zc, wide.age_gyr_q50.loc[both].to_numpy(), c),
                          line(zc, common.age_gyr_q50.loc[both].to_numpy(), c),
                          note="DR2 spectra; percent shift applied to the baseline H"))

    # C. DR2 against DR3 spectra of the same objects
    for arm, label in (("cn_free", "C/N-free"), ("plain", "plain")):
        old = fits[(fits.release == "dr2") & (fits.arm == arm)].set_index("target")
        new = dr3[dr3.arm == arm].set_index("target").loc[old.index]
        c = resample(len(old))[1]
        rows.append(shift("spectra release", f"DR2 spectra, {label} fit", "DR3 spectra, same 73 objects, same fit",
                          line(old.z.to_numpy(), old.age_gyr_q50.to_numpy(), c),
                          line(new.z.to_numpy(), new.age_gyr_q50.to_numpy(), c),
                          note="percent shift applied to the baseline H"))

    # D. photometry catalogue
    targets = pd.DataFrame(json.load(open(ROOT / "results/legac-dr3-2026-11-11/targets.json"))["targets"])
    targets = targets.set_index("spect_id").loc[names]
    catalogue = targets.photometry.to_numpy()
    is_2025 = catalogue == "cosmos2025"
    intercepts = np.column_stack((z, is_2025, ~is_2025)).astype(float)
    grouped = line(z, age, counts, design=intercepts, column=0)
    assert np.isclose(grouped["slope"][0], fit_common_age_slope(z, age, catalogue)[0])
    rows.append(shift("photometry catalogue", "one slope, one intercept per catalogue", "baseline line, 194",
                      grouped, baseline))
    split = {True: line(z, age, counts, keep=is_2025), False: line(z, age, counts, keep=~is_2025)}
    rows.append(shift("photometry catalogue", "COSMOS2025 galaxies only", "baseline line, 194", split[True], baseline))
    rows.append(shift("photometry catalogue", "COSMOS2020 Classic galaxies only", "baseline line, 194",
                      split[False], baseline))
    rows.append(shift("photometry catalogue", "COSMOS2025 galaxies", "COSMOS2020 Classic galaxies",
                      split[True], split[False], in_total=False,
                      note="different galaxies; no object was fitted with both catalogues"))

    # E. estimator
    select = selection_columns(names)
    sigma = select.SIGMA_STARS_PRIME.to_numpy()
    with_sigma = np.column_stack((np.ones_like(z), z, np.log10(sigma)))
    rows.append(shift("estimator", "line with a log sigma-star term", "baseline line, 194",
                      line(z, age, counts, design=with_sigma), baseline))
    for n_z, z_bins, n_sigma, centre in (
        (4, "fixed", 2, "median"), (4, "quantile", 2, "median"), (2, "fixed", 2, "median"),
        (6, "fixed", 2, "median"), (4, "fixed", 1, "median"), (4, "quantile", 1, "median"),
        (2, "fixed", 1, "median"), (6, "fixed", 1, "median"), (4, "fixed", 2, "mean"),
    ):
        result = binned(z, age, sigma, indices, n_z, z_bins, n_sigma, centre)
        rows.append(shift("estimator", f"binned differences: {n_z} {z_bins} z bins x {n_sigma} sigma-star, {centre}",
                          "baseline line, 194", result, baseline,
                          note=f"error from the bin errors {result['error']:.1f} km/s/Mpc; "
                               "the bootstrap of this estimator is not centred on its estimate (dH_bootstrap_median)"))
    q10, q25, q75, q90 = np.quantile(z, [0.10, 0.25, 0.75, 0.90])
    for label, keep in (
        (f"z <= {q90:.3f} (lowest 90%)", z <= q90), (f"z >= {q10:.3f} (highest 90%)", z >= q10),
        (f"{q10:.3f} <= z <= {q90:.3f}", (z >= q10) & (z <= q90)),
        (f"z <= {q75:.3f} (lowest 75%)", z <= q75), (f"z >= {q25:.3f} (highest 75%)", z >= q25),
    ):
        rows.append(shift("estimator", f"line, {label}", "baseline line, 194", line(z, age, counts, keep=keep), baseline))
    masks = np.array([name.split("_")[0] for name in names])
    jack = pd.DataFrame([
        dict(mask=m, galaxies=int((masks == m).sum()),
             dH=line(z, age, keep=masks != m)["excess"][0] - baseline["excess"][0])
        for m in pd.unique(masks)
    ])
    g = len(jack)
    jack_se = np.sqrt((g - 1) / g * np.sum((jack.dH - jack.dH.mean()) ** 2))
    worst = jack.loc[jack.dH.abs().idxmax()]
    rows.append(dict(term="estimator", variant=f"line, leave one mask out ({g} masks)", compared_with="baseline line, 194",
                     n=len(z) - int(worst.galaxies), n_compared=len(z), H_compared=h0, dH=worst.dH,
                     dH_pct=100 * worst.dH / h0, resolved_95=False, in_total=False,
                     note=f"largest single shift, mask {worst['mask']}; jackknife standard error {jack_se:.1f} km/s/Mpc; "
                          "all masks are in COSMOS"))

    # F. selection inside the 194
    sn, margin, oii = targets.sn.to_numpy(), select.nuvrj_margin.to_numpy(), select.OII_3727_EW.to_numpy()
    cuts = []
    for fraction in (0.10, 0.25, 1 / 3):
        cuts.append((f"S/N > {np.quantile(sn, fraction):.1f} (drops lowest {100 * fraction:.0f}%)",
                     sn > np.quantile(sn, fraction)))
    for fraction in (0.10, 0.25, 1 / 3):
        cuts.append((f"NUVrJ margin > {np.quantile(margin, fraction):.2f} mag (drops lowest {100 * fraction:.0f}%)",
                     margin > np.quantile(margin, fraction)))
    for fraction in (0.90, 0.75):
        limit = np.nanquantile(oii, fraction)
        cuts.append((f"[O II] EW < {limit:.2f} A or not measured", ~(oii >= limit)))
    for label, keep in cuts:
        rows.append(shift("selection", label, "baseline line, 194", line(z, age, counts, keep=keep), baseline))

    # G. SFH prior scale: Experiment 9 mocks, full spectrum, plain fit
    mocks = pd.read_csv(ROOT / "results/cn-response-2026-11-10/prior-slope/per-mock.csv")
    galaxy = mocks.groupby(["arm", "target"], sort=True)[["redshift", "age_q50"]].mean()
    zp, c = galaxy.loc["P"].redshift.to_numpy(), resample(galaxy.loc["P"].shape[0], MOCK_PRIOR_SEED)[1]
    rows.append(shift("SFH prior scale", "StudentT scale 1.0, mocks", "scale 0.3 (production), same 10 mock galaxies x 3 seeds",
                      line(zp, galaxy.loc["W"].age_q50.to_numpy(), c), line(zp, galaxy.loc["P"].age_q50.to_numpy(), c),
                      note="mocks, full spectrum, plain fit; percent shift applied to the baseline H"))

    # H. method bias from mocks: truth against recovered
    for folder, label in (
        ("mock-chronometer-window-2026-11-13", "plain fit, 194 mocks"),
        ("mock-chronometer-cn-free-2026-11-16", "C/N-free fit, 40 mocks"),
    ):
        mock = pd.read_csv(ROOT / "results" / folder / "per-mock.csv")
        zm, c = mock.z.to_numpy(), resample(len(mock))[1]
        truth, recovered = line(zm, mock.true_age_gyr.to_numpy(), c), line(zm, mock.age_q50.to_numpy(), c)
        row = shift("method bias (mocks)", f"true ages, {label}", "recovered ages, same mocks", truth, recovered,
                    note="percent shift applied to the baseline H")
        ratio = recovered["slope"] / truth["slope"]
        q = interval(ratio[1:])
        row["note"] += f"; recovered/true slope {ratio[0]:.3f} ({q[0]:.3f} to {q[1]:.3f})"
        rows.append(row)

    shifts = pd.DataFrame(rows)
    for column in ("dH", "dH_q16", "dH_q84"):
        shifts[column.replace("dH", "dH_at_baseline")] = shifts[column] / shifts.H_compared * h0
    shifts.to_csv(OUT / "shifts.csv", index=False)
    jack.to_csv(OUT / "jackknife-masks.csv", index=False)

    # ---- budget --------------------------------------------------------------------
    what = {
        "abundance treatment": "plain grid and carbon mask against C/N free, same 194 fits",
        "wavelength window": "three wider windows against the common window, DR2 spectra, plain fit (60, 96, 46 galaxies)",
        "spectra release": "DR2 against DR3 spectra of the same 73 objects",
        "photometry catalogue": "per-catalogue intercepts; each catalogue's galaxies alone (99, 95)",
        "estimator": "log sigma-star term; nine binned-difference schemes; five z ranges",
        "selection": "S/N, NUVrJ margin and [O II] EW cuts inside the 194",
        "SFH prior scale": "StudentT scale 1.0 against 0.3 on 30 mocks",
        "method bias (mocks)": "true against recovered slope: 194 plain mocks, 40 C/N-free mocks",
    }
    used = shifts[shifts.in_total]
    budget = used.groupby("term", sort=False).apply(lambda t: pd.Series(dict(
        what_varied=what[t.name], variants=len(t), resolved_95=int(t.resolved_95.sum()),
        dH_median=t.dH_at_baseline.median(), dH_min=t.dH_at_baseline.min(), dH_max=t.dH_at_baseline.max(),
        dH_pct_median=100 * t.dH_at_baseline.median() / h0,
        dH_uncertainty=((t.dH_at_baseline_q84 - t.dH_at_baseline_q16) / 2).median(),
        how_combined="median over the variants (Jiao+2023 Eq. 11)",
    ))).reset_index()
    gained = pd.read_csv(ROOT / "results/dr3-more-galaxies-2026-11-16/fits.csv")
    budget.loc[len(budget)] = dict(
        term="154 gained galaxies", what_varied="not available",
        how_combined=f"fits.csv has {int(gained.valid.sum())} valid rows of {len(gained)} and no slope table")
    budget.to_csv(OUT / "budget.csv", index=False)

    def total(rows_used, label):
        median = rows_used.groupby("term").dH_at_baseline.median()
        upper, lower = np.sqrt((median[median > 0] ** 2).sum()), np.sqrt((median[median < 0] ** 2).sum())
        rms = np.sqrt((rows_used.dH_at_baseline ** 2).mean())
        return dict(
            terms_included=label, terms=len(median), H_variants=len(rows_used),
            jiao_upper=upper, jiao_lower=lower, jiao_upper_pct=100 * upper / h0, jiao_lower_pct=100 * lower / h0,
            borghi_std=rms, borghi_std_pct=100 * rms / h0,
        )

    no_mask = used[used.variant != "carbon mask fit"]
    totals = pd.DataFrame([
        total(used, "all existing variations"),
        total(no_mask, "without the carbon-mask fit"),
    ])
    totals.insert(0, "status", "provisional, incomplete: no SPS model, stellar library, IMF, metallicity, SFH or dust term")
    totals.to_csv(OUT / "totals.csv", index=False)

    # ---- side by side with the published budgets ----------------------------------
    ours = totals.iloc[1]
    comparison = pd.DataFrame([
        dict(work="This work, existing fits only (incomplete; without the carbon-mask fit)", z=baseline["z_eff"], H=h0,
             stat_plus=stat[1] - h0, stat_minus=h0 - stat[0], syst_plus=ours.jiao_upper, syst_minus=ours.jiao_lower,
             syst_std=ours.borghi_std, terms="abundance, window, spectra release, photometry catalogue, estimator, "
             "selection, SFH prior (mocks), method bias (mocks)",
             how="syst_plus/minus: median per term, quadrature, each sign apart; syst_std: rms of all variants about the baseline",
             source="shifts.csv, totals.csv"),
        dict(work="Borghi+2022b", z=0.75, H=98.8, stat_plus=24.8, stat_minus=24.8, syst_std=22.7,
             terms="Lick index set (about 1/3), binning (1/4), SPS model (1/4), SFH (1/6)",
             how="standard deviation of 15 H(z) values about the baseline; added to stat in quadrature: 33.6",
             source="Sect. 3.1, Eq. 2"),
        dict(work="Jiao+2023", z=0.80, H=113.1, stat_plus=15.1, stat_minus=15.1, syst_plus=29.1, syst_minus=11.3,
             terms="binning scheme, quality flags, SFH (double power law, 7.9%)",
             how="median shift per source after the model correction (Eq. 11); quadrature, upper and lower apart",
             source="Sect. 5.2, Eq. 11"),
        dict(work="Tomasetti+2023", z=1.26, H=135.0, stat_plus=60.0, stat_minus=60.0, syst_plus=27.0, syst_minus=27.0,
             terms="SFH (double power law) 27; binning 2.4",
             how="mean difference between equivalent binnings; quadrature with stat: 65",
             source="Sect. 4.3.1, Table 4"),
        dict(work="Moresco+2020, best case", terms="IMF 0.5%, SPS model 5.1%, metallicity 1.9%",
             how="quadrature: 5.5% of H; each term fully correlated in z (Eq. 9)", source="Eq. 10"),
        dict(work="Moresco+2020, worst case", terms="SFH 2.5%, IMF 0.5%, SPS model 10.8%, metallicity 9.8%",
             how="quadrature: 14.8% of H", source="Eq. 11"),
    ])
    for sign in ("plus", "minus"):
        comparison[f"syst_{sign}_pct"] = 100 * comparison[f"syst_{sign}"] / comparison.H
    comparison["syst_std_pct"] = 100 * comparison.syst_std / comparison.H
    comparison.to_csv(OUT / "budget-comparison.csv", index=False)

    # ---- terms with no variation yet ------------------------------------------------
    paired = shifts[shifts.term == "abundance treatment"]
    width = ((paired.dH_pct_q84 - paired.dH_pct_q16) / 2).to_numpy()  # 1 sigma on a paired shift, 194 galaxies
    grids = "~/.ceridwen/grids"
    missing = pd.DataFrame([
        dict(term="SPS model / isochrones", literature="Moresco+2020 Table 4: 8.9% mean (4.5% without the most discordant model)",
             vary="ssp_grid = mist_bpass_v2 against the default grid at fix_afe = 0.0", new_arms=2,
             exists_today=f"yes: {grids}/mist_bpass_v2.h5 and registry key mist_bpass_v2; no Padova, PARSEC or BaSTI grid",
             note="BPASS grid has no [alpha/Fe] axis; the fix_afe = 0.0 arm is the control for the next two rows too"),
        dict(term="stellar library", literature="Moresco+2020 Table 4: 6.6% mean",
             vary="ssp_grid = mist_miles_krou_afe1 (MILES) against the default grid (C3K) at fix_afe = 0.0", new_arms=1,
             exists_today=f"yes: {grids}/mist_miles_krou_afe1.h5",
             note="also changes the isochrones (MIST against aMIST v2.5); [alpha/Fe] = 0 plane only"),
        dict(term="IMF", literature="Moresco+2020 Table 4: 0.4% mean",
             vary="ssp_grid = mist_miles_chab (Chabrier) against mist_miles_krou_afe1 (Kroupa)", new_arms=1,
             exists_today="yes: registry key mist_miles_chab (67 MB download); no Salpeter grid",
             note="same isochrones and library in both arms"),
        dict(term="metallicity evolution", literature="Moresco+2020 Table 4: 9.0% for a 10% metallicity error, 4.2% for 5%",
             vary="metallicity_evolution = False against True", new_arms=1,
             exists_today="yes: notebook setting", note=""),
        dict(term="SFH bin number", literature="Borghi+2022b: SFH 1/6 of 22.7; Jiao+2023: SFH 7.9%; Tomasetti+2023: 27 of 135",
             vary="sfh_nbins = 8 against 14", new_arms=1, exists_today="yes: notebook setting", note=""),
        dict(term="SFH prior on the real data", literature="as above",
             vary="logsfr_ratios StudentT scale 1.0 against 0.3", new_arms=1,
             exists_today="yes: priors override, as Experiment 9 arm W", note="existing evidence is 30 mocks only"),
        dict(term="dust law", literature="not a term in the four papers",
             vary="birth_cloud_dust = False against True", new_arms=1, exists_today="yes: notebook setting",
             note="the attenuation slope diffuse_delta is already free"),
    ])
    for n in (40, 194):
        missing[f"cost_usd_{n}_galaxies"] = missing.new_arms * n * COST_PER_FIT
        missing[f"shift_1sigma_pct_{n}_galaxies"] = "{:.1f} to {:.1f}".format(*sorted(width * np.sqrt(194 / n)))
    missing.to_csv(OUT / "missing-terms.csv", index=False)

    pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 70)
    slope_q = interval(baseline["slope"][1:])
    print(f"baseline: slope {baseline['slope'][0]:.3f} ({slope_q[0]:.3f} to {slope_q[1]:.3f}), "
          f"z_eff {baseline['z_eff']:.4f}, H {h0:.1f} ({stat[0]:.1f} to {stat[1]:.1f})")
    print(shifts[["term", "variant", "n", "slope", "dslope", "dslope_q16", "dslope_q84", "H", "dH", "dH_q16", "dH_q84",
                  "dH_bootstrap_median", "dH_pct", "resolved_95"]].round(2).to_string())
    print(budget.drop(columns=["what_varied", "how_combined"]).round(2).to_string())
    print(totals.drop(columns="status").round(1).to_string())
    print(missing[["term", "new_arms", "cost_usd_40_galaxies", "cost_usd_194_galaxies",
                   "shift_1sigma_pct_40_galaxies", "shift_1sigma_pct_194_galaxies"]].to_string())


if __name__ == "__main__":
    main()
