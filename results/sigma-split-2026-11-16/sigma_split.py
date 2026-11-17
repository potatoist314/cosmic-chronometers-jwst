"""Sigma-star and mass split of the age-redshift line, and progenitor-bias tests, on the 194 window fits.

Existing fits only. Run from the repository root:
    ceridwen/.venv/bin/python results/sigma-split-2026-11-16/sigma_split.py
Inputs (read only):
    results/legac-dr3-2026-11-11/window-194-fits.csv and the fit folders it names (ages, fitted SFH, sigma_star)
    results/mock-chronometer-window-2026-11-13/per-mock.csv, mocks/*.npz, and the mock fit folders
    results/mock-chronometer-cn-free-2026-11-16/per-mock.csv
    data/raw/legac_dr3/legac_DR3.fits, data/raw/cosmos2020/cosmos2020_classic_legac_dr3_1arcsec.fits,
    data/raw/cosmos2015/cosmos2015_legac_dr3_photometry_1arcsec.fits
    results/oldest-envelope-2026-11-11/envelope.py (binned upper-envelope estimator)
Outputs: the CSV tables beside this script.
"""

import importlib.util
import sys
import warnings
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM, Planck18
from astropy.table import Table
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.chronometer import (  # noqa: E402
    GYR_INV_TO_KM_S_MPC,
    binned_difference_hubble,
    effective_redshift,
    fit_age_plane,
)

_spec = importlib.util.spec_from_file_location('envelope', ROOT / 'results/oldest-envelope-2026-11-11/envelope.py')
envelope = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(envelope)

DRAWS, SEED = 10000, 20261110  # galaxy bootstrap of results/carbon-mask-window-2026-11-13 and mocks.py
TOY_SEED, TOY_REALISATIONS = 20261117, 2000
ARMS = ('plain', 'cn_free')
FITS = ROOT / 'results/legac-dr3-2026-11-11/window-194-fits.csv'
MOCKS = ROOT / 'results/mock-chronometer-window-2026-11-13'
MOCKS_CN = ROOT / 'results/mock-chronometer-cn-free-2026-11-16'
# Tacchella et al. 2022 (ApJ 926, 134), Sect. 1 and Table 1: a galaxy is quiescent when sSFR < 1 / (20 t_H(z)).
QUIESCENT_D = 1 / 20
STAR_FORMING_D = 1 / 3  # same source: star-forming when sSFR > 1 / (3 t_H(z))
# LEGA-C DR3 release description (data/raw/legac_dr3/ESO_DR3_release_description.pdf): "The K-band limit ranges
# from K < 21.08 at z = 0.6 to K < 20.36 at z = 1.0". Interpolated here linearly in log10(1 + z).
K_LIMIT = ((0.6, 21.08), (1.0, 20.36))
# Loose cosmology bound for cosmic-time intervals: the grid corners of src.chronometer.effective_redshift.
LOOSE = ((60.0, 0.25), (75.0, 0.40))
MARGINS = np.arange(-2.5, 2.51, 0.25)  # Gyr
TIMES = ('l50', 'l90', 'lquench', 'lleave')  # lookback: 50% formed, 90% formed, sSFR t_H < 1/20, sSFR t_H < 1/3
YOUNGEST = (0.1, 0.2, 0.3, 0.5)


# ---------------------------------------------------------------- per-galaxy table

def sfh_times(edges, fractions, universe_age, threshold=None):
    """Per posterior draw, lookback times [Gyr]: 50% of the formed mass in place, 90% in place, quenching.

    Bins run young to old with constant SFR. Quenching: the old edge of the unbroken run of youngest bins with
    sSFR * t_H < threshold (default 1/20), where sSFR is SFR over the mass formed up to the bin centre and t_H
    the cosmic age there.
    """
    threshold = QUIESCENT_D if threshold is None else threshold
    widths = np.diff(edges)
    total = fractions.sum(axis=1, keepdims=True)
    fractions = fractions / total
    younger = np.concatenate([np.zeros((len(fractions), 1)), np.cumsum(fractions, axis=1)], axis=1)
    l50 = np.array([np.interp(0.5, y, edges) for y in younger])
    l90 = np.array([np.interp(0.1, y, edges) for y in younger])
    formed = 1 - younger[:, 1:] + 0.5 * fractions
    cosmic = universe_age - 0.5 * (edges[:-1] + edges[1:])
    with np.errstate(invalid='ignore', divide='ignore'):
        passive = fractions / widths * cosmic / formed < threshold
    return l50, l90, edges[np.argmin(passive, axis=1)]


def fit_times(path):
    with h5py.File(ROOT / path / 'ceridwen_derived_outputs.h5') as h:
        edges = h['sfh/lookback_time_gyr'][:]
        fractions = h['sfh/mass_fraction_draws'][:]
        times = sfh_times(edges, fractions, edges[-1])
        leave = sfh_times(edges, fractions, edges[-1], STAR_FORMING_D)[2]
        names = [n.decode() if isinstance(n, bytes) else n for n in h['summary/parameter'][:]]
        return dict(universe_age=edges[-1], l50=np.median(times[0]), l90=np.median(times[1]),
                    lquench=np.median(times[2]), lleave=np.median(leave),
                    logmass=h['summary/q50'][names.index('logmass')],
                    sigma_star=h.attrs['sigma_star_kms'], sigma_star_err=h.attrs['sigma_star_err'],
                    sn=h.attrs['catalogue_sn'])


def k_limit(z):
    (z0, k0), (z1, k1) = K_LIMIT
    x, x0, x1 = (np.log10(1 + v) for v in (z, z0, z1))
    return k0 + (k1 - k0) * (x - x0) / (x1 - x0)


def per_galaxy():
    fits = pd.read_csv(FITS)
    fits = fits[fits.release == 'dr3']
    rows = None
    for arm in ARMS:
        f = fits[fits.arm == arm].reset_index(drop=True)  # file order: reproduces the saved bootstrap ranges
        t = pd.DataFrame([fit_times(p) for p in f.path])
        if rows is None:
            rows = pd.DataFrame(dict(target=f.target, object_id=f.object_id, z=f.z, sigma_star=t.sigma_star,
                                     sigma_star_err=t.sigma_star_err, sn=t.sn, universe_age=t.universe_age))
        assert (rows.target == f.target).all()
        rows[f'age_{arm}'] = f.age_gyr_q50
        rows[f'logmass_{arm}'] = t.logmass
        for name in TIMES:
            rows[f'{name}_{arm}'] = t[name]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        c20 = Table.read(ROOT / 'data/raw/cosmos2020/cosmos2020_classic_legac_dr3_1arcsec.fits')
        c15 = Table.read(ROOT / 'data/raw/cosmos2015/cosmos2015_legac_dr3_photometry_1arcsec.fits')
    mass = pd.DataFrame(dict(object_id=np.array(c20['OBJECT'], dtype=np.int64),
                             logmass_cosmos2020=np.array(c20['loglpMassmed'], dtype=float)))
    flux = pd.DataFrame(dict(object_id=np.array(c15['OBJECT'], dtype=np.int64),
                             ks_flux=np.array(c15['FKsap3'], dtype=float)))
    rows = rows.merge(mass.dropna().drop_duplicates('object_id'), on='object_id', how='left')
    rows = rows.merge(flux.dropna().drop_duplicates('object_id'), on='object_id', how='left')
    rows['ks_ap3'] = 23.9 - 2.5 * np.log10(rows.pop('ks_flux'))  # 3" aperture flux in uJy, AB
    rows['k_limit'] = k_limit(rows.z)
    rows['log_sigma_star'] = np.log10(rows.sigma_star)
    return rows


# ---------------------------------------------------------------- estimators on (draws, N) arrays

def line(z, y, w=None):
    """Least-squares slope and its ordinary standard error along the last axis; w is a 0/1 membership."""
    w = np.ones_like(z) if w is None else w
    n = w.sum(-1, keepdims=True)
    zc = z - (w * z).sum(-1, keepdims=True) / n
    yc = y - (w * y).sum(-1, keepdims=True) / n
    szz = (w * zc**2).sum(-1)
    slope = (w * zc * yc).sum(-1) / szz
    rss = (w * (yc - slope[..., None] * zc)**2).sum(-1)
    return slope, np.sqrt(rss / (n[..., 0] - 2) / szz)


def common_slope(z, y, masks):
    """One slope with a separate intercept per bin (src.chronometer.fit_common_age_slope, batched)."""
    num = den = 0
    for w in masks:
        n = w.sum(-1, keepdims=True)
        zc = z - (w * z).sum(-1, keepdims=True) / n
        num = num + (w * zc * y).sum(-1)
        den = den + (w * zc**2).sum(-1)
    return num / den


def hubble(z_eff, slope):
    """src.chronometer.hubble_from_age_slope on arrays; NaN where the slope is not negative."""
    slope = np.asarray(slope, dtype=float)
    return np.where(slope < 0, -GYR_INV_TO_KM_S_MPC / ((1 + z_eff) * np.where(slope < 0, slope, -1.0)), np.nan)


def spread(values):
    """Point estimate (row 0) and the 16, 50, 84% quantiles of the bootstrap draws (rows 1:)."""
    q = np.nanquantile(values[1:], [0.16, 0.5, 0.84])
    return dict(value=values[0], q16=q[0], q50=q[1], q84=q[2])


def slope_row(z_eff, slope, reference=None, planck=None):
    """Table fields for one slope estimator: slope, H(z_eff), paired difference from the reference estimator."""
    s = spread(slope)
    row = dict(z_eff=z_eff, slope=s['value'], slope_q16=s['q16'], slope_q84=s['q84'],
               H=float(hubble(z_eff, s['value'])), H_q16=float(hubble(z_eff, s['q16'])),
               H_q84=float(hubble(z_eff, s['q84'])), H_planck18=Planck18.H(z_eff).value)
    if planck is not None:
        row['slope_planck18_same_estimator'] = planck
    if reference is not None:
        d = spread(slope - reference)
        row.update(diff=d['value'], diff_q16=d['q16'], diff_q84=d['q84'],
                   diff_over_error=d['value'] / (0.5 * (d['q84'] - d['q16'])))
    return row


def bootstrap_indices(n):
    """Row 0 is the sample itself; rows 1: are the galaxy resamples of the saved line fits."""
    return np.vstack([np.arange(n), np.random.default_rng(SEED).integers(0, n, size=(DRAWS, n))])


def z_eff_of(z):
    return effective_redshift(z)['z_eff']


def planck_age(z):
    return Planck18.age(z).to_value('Gyr')


# ---------------------------------------------------------------- step 2: split estimators

def bin_masks(x, k):
    """Membership of k equal-count bins of x (fixed thresholds: the sample quantiles)."""
    code = np.searchsorted(np.quantile(x, np.arange(1, k) / k), x, side='right')
    return [code == i for i in range(k)], code


def weighted_hubble(z, y, masks, idx):
    """Per bin H(z_eff of the bin) from the bin's slope, combined with inverse-variance weights."""
    z_effs = np.array([z_eff_of(z[m]) for m in masks])
    h, weight = [], []
    for m, z_eff in zip(masks, z_effs):
        slope, error = line(z[idx], y[idx], m[idx].astype(float))
        value = hubble(z_eff, slope)
        h.append(value)
        weight.append((value * error / np.abs(slope))**-2)
    h, weight = np.array(h), np.array(weight)
    return (weight * h).sum(0) / weight.sum(0), float((weight[:, 0] * z_effs).sum() / weight[:, 0].sum())


def hubble_row(z_eff, values, reference, planck):
    """Table fields for an estimator that returns H directly; reference is the plain-line H on the same draws."""
    s, d = spread(values), spread(values - reference)
    return dict(z_eff=z_eff, H=s['value'], H_q16=s['q16'], H_q84=s['q84'], H_planck18=Planck18.H(z_eff).value,
                H_planck18_same_estimator=planck, H_diff=d['value'], H_diff_q16=d['q16'], H_diff_q84=d['q84'],
                H_diff_over_error=d['value'] / (0.5 * (d['q84'] - d['q16'])),
                draws_not_finite=float(np.mean(~np.isfinite(values[1:]))))


def scatter(residual, parameters):
    return float(np.std(residual, ddof=parameters))


def split_tables(g):
    planes, bins = [], []
    for arm in ARMS:
        covariates = dict(log_sigma_star=g.log_sigma_star.values, logmass_cosmos2020=g.logmass_cosmos2020.values,
                          logmass_fitted=g[f'logmass_{arm}'].values)
        for name, x in covariates.items():
            keep = np.isfinite(x)
            z, y, x = g.z.values[keep], g[f'age_{arm}'].values[keep], x[keep]
            idx = bootstrap_indices(len(z))
            z_eff, tu = z_eff_of(z), planck_age(z)
            plain, _ = line(z[idx], y[idx])
            b, c = fit_age_plane(z[idx], y[idx], x[idx])
            fit = np.polyfit(z, y, 1)
            a = np.mean(y - b[0] * z - c[0] * x)
            cs = spread(c)
            planes.append(dict(
                arm=arm, covariate=name, galaxies=len(z), corr_z_covariate=np.corrcoef(z, x)[0, 1],
                corr_age_covariate=np.corrcoef(y, x)[0, 1], plain_slope=plain[0],
                plain_q16=spread(plain)['q16'], plain_q84=spread(plain)['q84'],
                **slope_row(z_eff, b, plain, float(fit_age_plane(z, tu, x)[0])),
                coefficient=cs['value'], coefficient_q16=cs['q16'], coefficient_q84=cs['q84'],
                coefficient_draws_above_zero=float(np.mean(c[1:] > 0)),
                scatter_plain=scatter(y - np.polyval(fit, z), 2), scatter_plane=scatter(y - a - b[0] * z - c[0] * x, 3)))
            for k, scheme in ((2, 'halves'), (3, 'thirds')):
                masks, _ = bin_masks(x, k)
                for i, m in enumerate(masks):
                    slope, _ = line(z[idx], y[idx], m[idx].astype(float))
                    bins.append(dict(arm=arm, covariate=name, scheme=scheme, bin=str(i + 1), galaxies=int(m.sum()),
                                     covariate_min=x[m].min(), covariate_median=np.median(x[m]),
                                     covariate_max=x[m].max(), z_median=np.median(z[m]),
                                     **slope_row(z_eff_of(z[m]), slope, plain, np.polyfit(z[m], tu[m], 1)[0])))
                weights = [m[idx].astype(float) for m in masks]
                common = common_slope(z[idx], y[idx], weights)
                bins.append(dict(arm=arm, covariate=name, scheme=scheme, bin='common slope', galaxies=len(z),
                                 z_median=np.median(z),
                                 **slope_row(z_eff, common, plain, float(common_slope(z, tu, masks)))))
                h, z_w = weighted_hubble(z, y, masks, idx)
                h_planck = weighted_hubble(z, tu, masks, np.arange(len(z))[None, :])[0][0]
                row = hubble_row(z_w, h, hubble(z_eff, plain), h_planck)
                bins.append(dict(arm=arm, covariate=name, scheme=scheme, bin='weighted H', galaxies=len(z),
                                 z_median=np.median(z), **row))
    return pd.DataFrame(planes), pd.DataFrame(bins)


def binned_draws(z, y, groups, edges, idx):
    """binned_difference_hubble on every row of idx. Returns H per row and the smallest cell count per row."""
    n_bins = len(edges) - 1
    _, code = np.unique(groups, return_inverse=True)
    cell = code * n_bins + np.clip(np.searchsorted(edges, z, side='right') - 1, 0, n_bins - 1)
    n_cells = (code.max() + 1) * n_bins
    h, smallest = np.full(len(idx), np.nan), np.zeros(len(idx), dtype=int)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for i, draw in enumerate(idx):
            smallest[i] = np.bincount(cell[draw], minlength=n_cells).min()
            try:
                h[i] = binned_difference_hubble(z[draw], y[draw], groups[draw], edges)['hubble']
            except ValueError:  # an empty cell, a zero MAD or a zero age difference
                pass
    return h, smallest


def binned_tables(g):
    """The literature scheme: four redshift bins, median ages, i-th against (i+2)-th point, weighted mean."""
    rows, pairs = [], []
    for arm in ARMS:
        groupings = dict(none=np.zeros(len(g)), log_sigma_star=g.log_sigma_star.values,
                         logmass_cosmos2020=g.logmass_cosmos2020.values, logmass_fitted=g[f'logmass_{arm}'].values)
        for name, x in groupings.items():
            keep = np.isfinite(x)
            z, y, x = g.z.values[keep], g[f'age_{arm}'].values[keep], x[keep]
            groups = np.zeros(len(z), dtype=int) if name == 'none' else bin_masks(x, 2)[1]
            idx = bootstrap_indices(len(z))
            plain_h = hubble(z_eff_of(z), line(z[idx], y[idx])[0])
            for binning, edges in (('equal width', np.linspace(z.min(), z.max(), 5)),
                                   ('equal count', np.quantile(z, np.linspace(0, 1, 5)))):
                point = binned_difference_hubble(z, y, groups, edges)
                planck = binned_difference_hubble(z, planck_age(z), groups, edges)
                h, smallest = binned_draws(z, y, groups, edges, idx)
                full = np.where(smallest >= 3, h, np.nan)
                rows.append(dict(arm=arm, split=name, redshift_bins=binning, galaxies=len(z),
                                 smallest_cell=int(point['counts'].min()), formal_error=point['error'],
                                 **hubble_row(point['z_eff'], h, plain_h, planck['hubble']),
                                 draws_with_cell_below_3=float(np.mean(smallest[1:] < 3)),
                                 H_q16_cells_3_or_more=np.nanquantile(full[1:], 0.16),
                                 H_q84_cells_3_or_more=np.nanquantile(full[1:], 0.84)))
                for i in range(len(point['pair_hubble'])):
                    step = (len(edges) - 1) // 2
                    group, low = divmod(i, len(edges) - 1 - step)
                    counts = point['counts'].reshape(-1, len(edges) - 1)[group]
                    pairs.append(dict(arm=arm, split=name, redshift_bins=binning, group=group + 1,
                                      bins=f'{low + 1} and {low + 1 + step}', galaxies=int(counts[low] + counts[low + step]),
                                      z_eff=point['pair_z_eff'][i], H=point['pair_hubble'][i],
                                      H_error=point['pair_error'][i], H_planck18=planck['pair_hubble'][i]))
    return pd.DataFrame(rows), pd.DataFrame(pairs)


# ---------------------------------------------------------------- selection check

def correlations(x, y, control=None):
    """Pearson r of x and y on every bootstrap row; with control, the partial correlation at fixed control."""
    def r(a, b):
        a, b = a - a.mean(-1, keepdims=True), b - b.mean(-1, keepdims=True)
        return (a * b).sum(-1) / np.sqrt((a**2).sum(-1) * (b**2).sum(-1))
    idx = bootstrap_indices(len(x))
    rxy = r(x[idx], y[idx])
    if control is None:
        return rxy
    rxc, ryc = r(x[idx], control[idx]), r(y[idx], control[idx])
    return (rxy - rxc * ryc) / np.sqrt((1 - rxc**2) * (1 - ryc**2))


def selection_tables(g):
    parent = Table.read(ROOT / 'data/raw/legac_dr3/legac_DR3.fits')
    pz = np.array(parent['Z'], dtype=float)
    ps = np.array(parent['SIGMA_STARS_PRIME'], dtype=float)
    primary = (np.array(parent['FLAG_PRIMARY']) == 1) & (pz >= 0.6) & (pz <= 1.0) & np.isfinite(ps) & (ps > 0)
    columns = dict(log_sigma_star='log_sigma_star', logmass_cosmos2020='logmass_cosmos2020',
                   logmass_fitted='logmass_plain', ks_ap3='ks_ap3', sn='sn', mag_brighter_than_k_limit='margin')
    g = g.assign(margin=g.k_limit - g.ks_ap3)
    complete = g[g.ks_ap3 < K_LIMIT[1][1]]
    cases = [('194', g, name, None) for name in columns]
    cases += [('194', g, 'log_sigma_star', c) for c in ('logmass_cosmos2020', 'logmass_fitted', 'ks_ap3', 'sn')]
    cases += [(f'194 with Ks < {K_LIMIT[1][1]}', complete, name, None) for name in ('log_sigma_star', 'ks_ap3')]
    mass_limit = g[g.ks_ap3 >= K_LIMIT[1][1]].logmass_cosmos2020.max()  # no fainter galaxy above this mass
    cases.append((f'194 with COSMOS2020 log mass > {mass_limit:.2f}', g[g.logmass_cosmos2020 > mass_limit],
                  'log_sigma_star', None))
    rows = []
    for sample, frame, name, control in cases:
        cols = [columns[name]] + ([columns[control]] if control else [])
        f = frame[np.isfinite(frame[cols]).all(axis=1)]
        z, x = f.z.values, f[columns[name]].values
        s = spread(correlations(z, x, f[columns[control]].values if control else None))
        rho = spearmanr(z, x)
        rows.append(dict(sample=sample, quantity=name, held_fixed=control or '', galaxies=len(f), pearson=s['value'],
                         pearson_q16=s['q16'], pearson_q84=s['q84'],
                         spearman=np.nan if control else rho.statistic, spearman_p=np.nan if control else rho.pvalue))
    s = spread(correlations(pz[primary], np.log10(ps[primary])))
    rho = spearmanr(pz[primary], ps[primary])
    rows.append(dict(sample='LEGA-C DR3 primary, 0.6 <= z <= 1.0, sigma_star measured', quantity='log_sigma_star',
                     held_fixed='', galaxies=int(primary.sum()), pearson=s['value'], pearson_q16=s['q16'],
                     pearson_q84=s['q84'], spearman=rho.statistic, spearman_p=rho.pvalue))
    thirds = []
    for i, m in enumerate(bin_masks(g.z.values, 3)[0]):
        f = g[m]
        thirds.append(dict(z_third=i + 1, galaxies=len(f), z_min=f.z.min(), z_max=f.z.max(),
                           sigma_star_median=f.sigma_star.median(), sigma_star_q16=f.sigma_star.quantile(0.16),
                           sigma_star_q84=f.sigma_star.quantile(0.84), logmass_cosmos2020_median=f.logmass_cosmos2020.median(),
                           ks_ap3_median=f.ks_ap3.median(), ks_ap3_faintest=f.ks_ap3.max(),
                           k_limit_median=f.k_limit.median(), mag_brighter_than_k_limit_median=f.margin.median(),
                           fainter_than_20p36=int((f.ks_ap3 >= K_LIMIT[1][1]).sum()), sn_median=f.sn.median()))
    return pd.DataFrame(rows), pd.DataFrame(thirds)


# ---------------------------------------------------------------- step 3: the split on the mocks

def mock_split_table(g, planes):
    """Mocks have one formation epoch, so the true coefficient of any covariate is zero. Each mock takes the
    sigma_star and masses of its real galaxy. Injected rows add coefficient * (covariate - mean), the coefficient
    being the one fitted to the real galaxies, to the true and the recovered ages."""
    rows = []
    for arm, folder in (('plain', MOCKS), ('cn_free', MOCKS_CN)):
        mocks = pd.read_csv(folder / 'per-mock.csv')
        real = g.set_index('target').loc[mocks.target]
        z, truth, recovered = mocks.z.values, mocks.true_age_gyr.values, mocks.age_q50.values
        for name, column in (('log_sigma_star', 'log_sigma_star'), ('logmass_cosmos2020', 'logmass_cosmos2020'),
                             ('logmass_fitted', f'logmass_{arm}')):
            x = real[column].values
            keep = np.isfinite(x)
            zk, tk, rk, xk = z[keep], truth[keep], recovered[keep], x[keep]
            idx = bootstrap_indices(len(zk))
            z_eff = z_eff_of(zk)
            true_slope = line(zk[idx], tk[idx])[0]
            coefficient = float(planes[(planes.arm == arm) & (planes.covariate == name)].coefficient.iloc[0])
            shift = coefficient * (xk - xk.mean())
            for ages, y in (('recovered', rk), ('recovered + injected relation', rk + shift)):
                plain = line(zk[idx], y[idx])[0]
                b, c = fit_age_plane(zk[idx], y[idx], xk[idx])
                estimates = {'plain line': plain, 'line + covariate term': b}
                for k, scheme in ((2, 'halves'), (3, 'thirds')):
                    masks = [m[idx].astype(float) for m in bin_masks(xk, k)[0]]
                    estimates[f'{scheme}, common slope'] = common_slope(zk[idx], y[idx], masks)
                for estimator, slope in estimates.items():
                    s, d, e = spread(slope), spread(slope - plain), spread(slope - true_slope)
                    w = spread(plain)
                    rows.append(dict(
                        mocks=arm, galaxies=len(zk), covariate=name, ages=ages, estimator=estimator,
                        true_slope=true_slope[0], slope=s['value'], slope_q16=s['q16'], slope_q84=s['q84'],
                        minus_truth=e['value'], minus_truth_q16=e['q16'], minus_truth_q84=e['q84'],
                        minus_plain=d['value'], minus_plain_q16=d['q16'], minus_plain_q84=d['q84'],
                        width_over_plain=(s['q84'] - s['q16']) / (w['q84'] - w['q16']),
                        H=float(hubble(z_eff, s['value'])), H_truth=float(hubble(z_eff, true_slope[0])),
                        coefficient=spread(c)['value'] if estimator == 'line + covariate term' else np.nan,
                        coefficient_q16=spread(c)['q16'] if estimator == 'line + covariate term' else np.nan,
                        coefficient_q84=spread(c)['q84'] if estimator == 'line + covariate term' else np.nan,
                        injected_coefficient=coefficient if 'injected' in ages else 0.0))
    return pd.DataFrame(rows)


def mock_binned_table(g, planes):
    """The literature scheme on the mocks: H against the same scheme on the true ages."""
    rows = []
    for arm, folder in (('plain', MOCKS), ('cn_free', MOCKS_CN)):
        mocks = pd.read_csv(folder / 'per-mock.csv')
        x = g.set_index('target').loc[mocks.target].log_sigma_star.values
        z, truth, recovered = mocks.z.values, mocks.true_age_gyr.values, mocks.age_q50.values
        idx = bootstrap_indices(len(z))
        coefficient = float(planes[(planes.arm == arm) & (planes.covariate == 'log_sigma_star')].coefficient.iloc[0])
        shift = coefficient * (x - x.mean())
        edges = np.linspace(z.min(), z.max(), 5)
        for split, groups in (('none', np.zeros(len(z), dtype=int)), ('log_sigma_star', bin_masks(x, 2)[1])):
            for ages, y, t in (('recovered', recovered, truth), ('recovered + injected relation', recovered + shift,
                                                                 truth + shift)):
                h, smallest = binned_draws(z, y, groups, edges, idx)
                true_h = binned_difference_hubble(z, truth, groups, edges)
                s = spread(h)
                rows.append(dict(mocks=arm, galaxies=len(z), split=split, ages=ages,
                                 smallest_cell=int(true_h['counts'].min()), z_eff=true_h['z_eff'], H=s['value'],
                                 H_q16=s['q16'], H_q84=s['q84'], H_same_scheme_true_ages=true_h['hubble'],
                                 H_same_scheme_true_ages_with_relation=binned_difference_hubble(z, t, groups, edges)['hubble'],
                                 H_true_cosmology=Planck18.H(true_h['z_eff']).value,
                                 draws_not_finite=float(np.mean(~np.isfinite(h[1:]))),
                                 draws_with_cell_below_3=float(np.mean(smallest[1:] < 3))))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- progenitor bias: tests on the fits

def mock_frame(g):
    """Per mock: true and recovered age and SFH lookback times, and the sigma_star of its real galaxy."""
    mocks = pd.read_csv(MOCKS / 'per-mock.csv')
    rows = []
    for target, path in zip(mocks.target, mocks.path):
        with np.load(MOCKS / 'mocks' / f'{target}.npz') as m:
            edges = m['time_edges_gyr']
            mass = (m['sfh_per_bin'] * np.diff(edges))[None, :]
        true = sfh_times(edges, mass, edges[-1])
        row = dict(l50_true=true[0][0], l90_true=true[1][0], lquench_true=true[2][0],
                   lleave_true=sfh_times(edges, mass, edges[-1], STAR_FORMING_D)[2][0])
        fit = fit_times(path)
        row.update({name: fit[name] for name in TIMES}, universe_age=fit['universe_age'])
        rows.append(row)
    frame = pd.concat([mocks[['target', 'shape', 'z', 'true_age_gyr', 'age_q50']], pd.DataFrame(rows)], axis=1)
    frame['log_sigma_star'] = g.set_index('target').loc[frame.target].log_sigma_star.values
    return frame.rename(columns=dict(age_q50='age'))


def samples_of(g, mocks):
    """(arm, sample, frame with z, age and the lookback times). The halves split at the median sigma_star."""
    out = []
    for arm in ARMS:
        f = g.rename(columns={f'age_{arm}': 'age', **{f'{name}_{arm}': name for name in TIMES}})
        high = bin_masks(f.log_sigma_star.values, 2)[1] == 1
        out += [(arm, 'all', f), (arm, 'sigma_star low half', f[~high]), (arm, 'sigma_star high half', f[high])]
    high = bin_masks(mocks.log_sigma_star.values, 2)[1] == 1
    out += [('mock', 'all', mocks), ('mock', 'sigma_star low half', mocks[~high]),
            ('mock', 'sigma_star high half', mocks[high])]
    return out


COSMOLOGIES = (('Planck18', Planck18),) + tuple(
    (f'H0 {h0:.0f}, Omega_m {om:.2f}', FlatLambdaCDM(h0, om)) for h0, om in LOOSE)
MARKERS = (('l90', '90% of the mass formed'), ('lleave', 'sSFR t_H below 1/3'), ('lquench', 'sSFR t_H below 1/20'))


def fixed_population_table(samples, z_top, offsets):
    """Keep a galaxy when its marker time is earlier than the cosmic age at z_top by the margin:
    lookback >= t(z) - t(z_top) + margin. margin_true adds the median (recovered - true) lookback of the mocks.
    The sigma_term columns fit age = a + b z + c log sigma_star to the kept galaxies; diff is from the plain line
    of the full sample."""
    rows = []
    for arm, sample, f in samples:
        z, y, x = f.z.values, f.age.values, f.log_sigma_star.values
        idx = bootstrap_indices(len(z))
        plain = line(z[idx], y[idx])[0]
        plane = fit_age_plane(z[idx], y[idx], x[idx])[0]
        thirds = bin_masks(z, 3)[1]
        for cosmology_name, cosmology in COSMOLOGIES:
            if cosmology_name != 'Planck18' and sample != 'all':
                continue
            interval = (cosmology.age(z) - cosmology.age(z_top)).to_value('Gyr')
            for marker, description in MARKERS:
                for margin in MARGINS:
                    keep = f[marker].values >= interval + margin
                    if keep.sum() < 30:
                        continue
                    slope = line(z[idx], y[idx], keep[idx].astype(float))[0]
                    row = dict(
                        arm=arm, sample=sample, cosmology=cosmology_name, marker=description, margin=margin,
                        margin_true=margin - offsets[marker], galaxies=int(keep.sum()),
                        kept_low_z_third=int(keep[thirds == 0].sum()), kept_mid_z_third=int(keep[thirds == 1].sum()),
                        kept_high_z_third=int(keep[thirds == 2].sum()),
                        **slope_row(z_eff_of(z[keep]), slope, plain,
                                    np.polyfit(z[keep], planck_age(z[keep]), 1)[0]))
                    if sample == 'all' and cosmology_name == 'Planck18':
                        both = fit_age_plane(z[idx], y[idx], x[idx], keep[idx].astype(float))[0]
                        s, d, e = spread(both), spread(both - plain), spread(both - plane)
                        row.update(
                            sigma_term_slope=s['value'], sigma_term_slope_q16=s['q16'], sigma_term_slope_q84=s['q84'],
                            sigma_term_H=float(hubble(row['z_eff'], s['value'])),
                            sigma_term_H_q16=float(hubble(row['z_eff'], s['q16'])),
                            sigma_term_H_q84=float(hubble(row['z_eff'], s['q84'])),
                            sigma_term_diff=d['value'], sigma_term_diff_q16=d['q16'], sigma_term_diff_q84=d['q84'],
                            sigma_term_minus_full_sample_sigma_term=e['value'],
                            sigma_term_minus_full_sample_sigma_term_q16=e['q16'],
                            sigma_term_minus_full_sample_sigma_term_q84=e['q84'])
                    rows.append(row)
    return pd.DataFrame(rows)


def youngest_keep(z, y, fraction, k):
    """Rows sorted by redshift, and False where a galaxy is in the youngest `fraction` of its k redshift
    neighbours. The rank uses the age residual from the row's own line, so the trend inside a window does not
    set it."""
    order = np.argsort(z, axis=-1, kind='stable')
    z, y = np.take_along_axis(z, order, axis=-1), np.take_along_axis(y, order, axis=-1)
    residual = y - line(z, y)[0][:, None] * z
    n = z.shape[-1]
    starts = np.clip(np.arange(n) - k // 2, 0, n - k)
    keep = np.empty(z.shape, dtype=bool)
    for lo in range(0, len(z), 500):
        r = residual[lo:lo + 500]
        keep[lo:lo + 500] = (sliding_window_view(r, k, axis=-1)[:, starts, :] < r[:, :, None]).mean(-1) >= fraction
    return z, y, keep


def envelope_slope(z, y, kind, p):
    zp, yp, _ = envelope.binned(z, y, np.zeros_like(y), 4, kind, p)
    return envelope.ols_slope(zp, yp)


def young_cut_estimates(z, y):
    """Slopes on (draws, N) arrays for the youngest-fraction cuts and the upper envelope."""
    k = z.shape[-1] // 5
    out = {}
    for fraction in YOUNGEST:
        zs, ys, keep = youngest_keep(z, y, fraction, k)
        out[f'drop the youngest {fraction:.0%} of {k} redshift neighbours'] = line(zs, ys, keep.astype(float))[0]
    out['oldest half of 4 redshift bins, medians'] = envelope_slope(z, y, 'oldest_fraction', 0.5)
    out['75% age quantile of 4 redshift bins'] = envelope_slope(z, y, 'bin_quantile', 0.75)
    return out


def young_cut_table(samples):
    rows = []
    for arm, sample, f in samples:
        z, y = f.z.values, f.age.values
        idx = bootstrap_indices(len(z))
        plain = line(z[idx], y[idx])[0]
        z_eff = z_eff_of(z)
        planck = young_cut_estimates(z[None, :], planck_age(z)[None, :])
        rows.append(dict(arm=arm, sample=sample, estimator='plain line', galaxies=len(z),
                         **slope_row(z_eff, plain, plain, np.polyfit(z, planck_age(z), 1)[0])))
        for estimator, slope in young_cut_estimates(z[idx], y[idx]).items():
            rows.append(dict(arm=arm, sample=sample, estimator=estimator, galaxies=len(z),
                             **slope_row(z_eff, slope, plain, float(planck[estimator][0]))))
    return pd.DataFrame(rows)


def moments(z_code, residual):
    """Per redshift third, on (draws, N) arrays: scatter, skewness, and the lower and upper half-widths."""
    out = {}
    for i in range(3):
        r = np.where(z_code == i, residual, np.nan)
        centred = r - np.nanmean(r, axis=-1, keepdims=True)
        q16, q50, q84 = np.nanquantile(r, [0.16, 0.5, 0.84], axis=-1)
        out[i] = dict(scatter=np.sqrt(np.nanmean(centred**2, axis=-1)),
                      skewness=np.nanmean(centred**3, axis=-1) / np.nanmean(centred**2, axis=-1)**1.5,
                      lower_half_width=q50 - q16, upper_half_width=q84 - q50)
    return out


def moments_table(samples):
    """Age residuals from the sample's own line. A young tail that grows toward low z gives a larger scatter,
    a more negative skewness and a larger lower half-width in the low-z third."""
    rows = []
    for arm, sample, f in samples:
        z, y = f.z.values, f.age.values
        idx = bootstrap_indices(len(z))
        zb, yb = z[idx], y[idx]
        slope = line(zb, yb)[0]
        residual = yb - yb.mean(-1, keepdims=True) - slope[:, None] * (zb - zb.mean(-1, keepdims=True))
        code = bin_masks(z, 3)[1]
        m = moments(code[idx], residual)
        for statistic in m[0]:
            row = dict(arm=arm, sample=sample, statistic=statistic, galaxies=len(z))
            for i, name in enumerate(('low_z', 'mid_z', 'high_z')):
                s = spread(m[i][statistic])
                row.update({name: s['value'], f'{name}_q16': s['q16'], f'{name}_q84': s['q84']})
            d = m[0][statistic] - m[2][statistic]
            s = spread(d)
            row.update(low_minus_high=s['value'], low_minus_high_q16=s['q16'], low_minus_high_q84=s['q84'],
                       draws_above_zero=float(np.mean(d[1:] > 0)))
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- progenitor bias: toy population

TOY_LATE_FRACTION = (0.1, 0.2, 0.4)  # late fraction at the lowest redshift; zero at the highest
TOY_DELAY = (0.5, 1.0, 2.0, 3.0)  # Gyr by which a late member forms later
TOY_MARGIN = (0.0, 0.5, 1.0)  # Gyr, true margin of the fixed-population cut


def toy_estimates(z, x, low, age, lookback, late, interval, offsets):
    """Slopes of every estimator on (realisations, N) arrays, and the fractions the fixed-population cut keeps."""
    slopes, kept = {'plain line': line(z, age)[0]}, {}
    slopes['true late members removed'] = line(z, age, (~late).astype(float))[0]
    for marker, description in MARKERS[:2]:
        for margin in TOY_MARGIN:
            keep = lookback[marker] >= interval + offsets[marker] + margin
            name = f'fixed population, {description}, true margin {margin:.1f} Gyr'
            slopes[name] = line(z, age, keep.astype(float))[0]
            kept[name] = ((keep & late).sum() / max(late.sum(), 1), (keep & ~late).sum() / (~late).sum())
    slopes.update(young_cut_estimates(z, age))
    slopes['line + log sigma_star term'] = fit_age_plane(z, age, x)[0]
    slopes['sigma_star halves, common slope'] = common_slope(z, age, [low.astype(float), (~low).astype(float)])
    code = np.broadcast_to(bin_masks(z[0], 3)[1], z.shape)
    residual = age - age.mean(-1, keepdims=True) - slopes['plain line'][:, None] * (z - z.mean(-1, keepdims=True))
    m = moments(code, residual)
    return slopes, kept, {name: m[0][name] - m[2][name] for name in m[0]}


def toy_tables(mocks, real_scatter, observed):
    """A base population with one formation epoch and a redshift-independent Gaussian scatter of formation time,
    plus late members: probability late_fraction * (z_top - z) / (z_top - z_min), formed `delay` Gyr later (age and
    every SFH lookback time shifted together). Recovered values add each mock's own (recovered - true) error.
    `observed` is moments_table of the real fits: the moment rows give the fraction of realisations at or below
    the observed low-z minus high-z value."""
    observed = {arm: observed[(observed.arm == arm) & (observed['sample'] == 'all')].set_index('statistic')
                .low_minus_high for arm in ARMS}
    rng = np.random.default_rng(TOY_SEED)
    z1, x1 = mocks.z.values, mocks.log_sigma_star.values
    n = len(z1)
    truth = np.polyfit(z1, mocks.true_age_gyr, 1)[0]
    mock_scatter = scatter(mocks.age - np.polyval(np.polyfit(z1, mocks.age, 1), z1), 2)
    sigma_int = np.sqrt(real_scatter**2 - mock_scatter**2)
    shape = (TOY_REALISATIONS, n)
    z, x = np.broadcast_to(z1, shape), np.broadcast_to(x1, shape)
    low1 = bin_masks(x1, 2)[1] == 0
    low = np.broadcast_to(low1, shape)
    interval = planck_age(z1) - planck_age(z1.max())
    offsets = {marker: float(np.median(mocks[marker] - mocks[f'{marker}_true'])) for marker, _ in MARKERS}
    delta = rng.normal(0, sigma_int, shape)
    u = rng.random(shape)
    ramp = (z1.max() - z1) / (z1.max() - z1.min())
    base_age = mocks.true_age_gyr.values + delta
    age_error = (mocks.age - mocks.true_age_gyr).values
    base_lookback = {m: mocks[f'{m}_true'].values + delta for m, _ in MARKERS[:2]}
    errors = {m: (mocks[m] - mocks[f'{m}_true']).values for m, _ in MARKERS[:2]}
    none = np.zeros(shape, dtype=bool)
    base, _, base_moments = toy_estimates(z, x, low, base_age + age_error,
                                          {m: base_lookback[m] + errors[m] for m in errors}, none, interval, offsets)
    rows, moment_rows = [], []
    for members in ('any sigma_star', 'low sigma_star half only'):
        for fraction in TOY_LATE_FRACTION:
            probability = fraction * ramp * (2 * low1 if members != 'any sigma_star' else 1)
            late = u < probability
            for delay in TOY_DELAY:
                shift = delay * late
                slopes, kept, moment = toy_estimates(
                    z, x, low, base_age - shift + age_error,
                    {m: base_lookback[m] - shift + errors[m] for m in errors}, late, interval, offsets)
                cell = dict(late_members=members, late_fraction_at_z_min=fraction, delay_gyr=delay,
                            sigma_int_gyr=sigma_int, true_slope=truth,
                            late_galaxies_mean=late.sum(-1).mean(),
                            late_formed_90_after_z_top=float(((base_lookback['l90'] - shift < interval) & late).sum()
                                                             / late.sum()),
                            plain_bias_expected=delay * fraction / (z1.max() - z1.min()))
                for estimator, slope in slopes.items():
                    d, t = slope - base[estimator], slope - truth
                    b = base[estimator] - truth
                    rows.append(dict(
                        **cell, estimator=estimator, bias_from_late_members=d.mean(),
                        bias_from_late_members_q16=np.quantile(d, 0.16), bias_from_late_members_q84=np.quantile(d, 0.84),
                        without_late_members_minus_truth=b.mean(), slope_minus_truth=t.mean(),
                        slope_minus_truth_q16=np.quantile(t, 0.16), slope_minus_truth_q84=np.quantile(t, 0.84),
                        late_members_kept=kept[estimator][0] if estimator in kept else np.nan,
                        base_members_kept=kept[estimator][1] if estimator in kept else np.nan))
                for statistic, value in moment.items():
                    d = value - base_moments[statistic]
                    moment_rows.append(dict(
                        **cell, statistic=f'{statistic}, low-z third minus high-z third', value=value.mean(),
                        value_q16=np.quantile(value, 0.16), value_q84=np.quantile(value, 0.84),
                        without_late_members=base_moments[statistic].mean(), change_from_late_members=d.mean(),
                        change_q16=np.quantile(d, 0.16), change_q84=np.quantile(d, 0.84),
                        **{f'observed_{arm}': observed[arm][statistic] for arm in ARMS},
                        **{f'realisations_at_or_below_observed_{arm}': float(np.mean(value <= observed[arm][statistic]))
                           for arm in ARMS},
                        **{f'without_late_members_at_or_below_observed_{arm}':
                           float(np.mean(base_moments[statistic] <= observed[arm][statistic])) for arm in ARMS}))
    return pd.DataFrame(rows), pd.DataFrame(moment_rows)


# ---------------------------------------------------------------- summary tables

def headline_table(planes, bins):
    """Step 4: the plain line, the line with a log sigma_star term, and the cross-checks, at the full-sample z_eff."""
    fields = ['galaxies', 'z_eff', 'slope', 'slope_q16', 'slope_q84', 'H', 'H_q16', 'H_q84', 'H_planck18',
              'diff', 'diff_q16', 'diff_q84', 'diff_over_error']
    rows = []
    for arm in ARMS:
        p = planes[planes.arm == arm].set_index('covariate')
        b = bins[(bins.arm == arm) & (bins.bin == 'common slope')].set_index(['covariate', 'scheme'])
        s = p.loc['log_sigma_star']
        rows.append(dict(arm=arm, estimator='plain line', role='reference', galaxies=s.galaxies, z_eff=s.z_eff,
                         slope=s.plain_slope, slope_q16=s.plain_q16, slope_q84=s.plain_q84,
                         H=float(hubble(s.z_eff, s.plain_slope)), H_q16=float(hubble(s.z_eff, s.plain_q16)),
                         H_q84=float(hubble(s.z_eff, s.plain_q84)), H_planck18=s.H_planck18))
        for estimator, role, r in (
                ('line + log sigma_star term', 'headline', s),
                ('sigma_star thirds, common slope', 'cross-check', b.loc[('log_sigma_star', 'thirds')]),
                ('sigma_star halves, common slope', 'cross-check', b.loc[('log_sigma_star', 'halves')]),
                ('line + COSMOS2020 log mass term', 'cross-check', p.loc['logmass_cosmos2020'])):
            rows.append(dict(arm=arm, estimator=estimator, role=role, **{name: r[name] for name in fields}))
    return pd.DataFrame(rows)


def budget_table(planes, fixed, toy, n_mocks):
    """Progenitor-bias terms: shift of the slope and of H at the full-sample z_eff,
    H(reference slope + shift) - H(reference slope). The cut is the fixed-population cut on the time when 90% of
    the mass had formed, at the margin whose bias-corrected value is nearest zero."""
    rows = []

    def add(term, arm, line_name, galaxies_removed, z_eff, reference, shift, q16, q84, source):
        h0 = float(hubble(z_eff, reference))
        h = sorted(float(hubble(z_eff, reference + d)) - h0 for d in (q16, q84))
        rows.append(dict(term=term, arm=arm, line=line_name, galaxies_removed=galaxies_removed,
                         reference_slope=reference, slope_shift=shift, slope_shift_q16=q16, slope_shift_q84=q84,
                         H_reference=h0, H_shift=float(hubble(z_eff, reference + shift)) - h0, H_shift_q16=h[0],
                         H_shift_q84=h[1], H_shift_percent=100 * (float(hubble(z_eff, reference + shift)) / h0 - 1),
                         source=source))

    marker = MARKERS[0][1]
    cut = 'galaxies that formed 90% of their mass after the cosmic age at z_top removed'
    for arm in ARMS:
        p = planes[(planes.arm == arm) & (planes.covariate == 'log_sigma_star')].iloc[0]
        add('log sigma_star term', arm, 'plain line', 0, p.z_eff, p.plain_slope, p['diff'], p.diff_q16, p.diff_q84,
            'split-plane.csv')
        f = fixed[(fixed.arm == arm) & (fixed['sample'] == 'all') & (fixed.marker == marker)]
        c = f[f.cosmology == 'Planck18']
        r = c.iloc[c.margin_true.abs().argmin()]
        removed = int(p.galaxies - r.galaxies)
        add(cut, arm, 'plain line', removed, p.z_eff, p.plain_slope, r['diff'], r.diff_q16, r.diff_q84,
            'progenitor-fixed-population.csv')
        add(cut, arm, 'line + log sigma_star term', removed, p.z_eff, p.slope,
            r.sigma_term_minus_full_sample_sigma_term, r.sigma_term_minus_full_sample_sigma_term_q16,
            r.sigma_term_minus_full_sample_sigma_term_q84, 'progenitor-fixed-population.csv')
        for name, _ in COSMOLOGIES[1:]:
            q = f[(f.cosmology == name) & np.isclose(f.margin, r.margin)].iloc[0]
            add(f'{cut}; cosmic-time interval from {name}', arm, 'plain line', int(p.galaxies - q.galaxies), p.z_eff,
                p.plain_slope, q['diff'], q.diff_q16, q.diff_q84, 'progenitor-fixed-population.csv')
    m = fixed[(fixed.arm == 'mock') & (fixed['sample'] == 'all') & (fixed.marker == marker)
              & (fixed.cosmology == 'Planck18') & np.isclose(fixed.margin, r.margin)].iloc[0]
    z_eff = planes.z_eff.iloc[0]
    add('the same cut on the mocks (one formation epoch)', 'mock', 'plain line', int(n_mocks - m.galaxies),
        z_eff, m.slope - m['diff'], m['diff'], m.diff_q16, m.diff_q84, 'progenitor-fixed-population.csv')
    t = toy[toy.late_members == 'any sigma_star']
    first = t[(t.late_fraction_at_z_min == TOY_LATE_FRACTION[0]) & (t.delay_gyr == TOY_DELAY[0])].set_index('estimator')
    fp = f'fixed population, {marker}, true margin 0.0 Gyr'
    truth = first.true_slope.iloc[0]
    own = first.without_late_members_minus_truth
    add('the same cut on the toy population without late members', 'toy', 'plain line', np.nan, z_eff,
        truth + own['plain line'], own[fp] - own['plain line'], np.nan, np.nan, 'progenitor-toy.csv')
    for fraction, delay in ((0.2, 1.0), (0.2, 2.0), (0.2, 3.0)):
        cell = t[(t.late_fraction_at_z_min == fraction) & (t.delay_gyr == delay)].set_index('estimator')
        for estimator, line_name in (('plain line', 'plain line'), (fp, 'plain line after the cut'),
                                     ('line + log sigma_star term', 'line + log sigma_star term')):
            e = cell.loc[estimator]
            add(f'toy late members: {fraction:.0%} at z_min, formed {delay:g} Gyr later '
                f'({e.late_formed_90_after_z_top:.0%} of them formed 90% after z_top)', 'toy', line_name, np.nan,
                z_eff, truth, e.bias_from_late_members, e.bias_from_late_members_q16, e.bias_from_late_members_q84,
                'progenitor-toy.csv')
    return pd.DataFrame(rows)


def main():
    g = per_galaxy()
    planes, bins = split_tables(g)
    binned, pairs = binned_tables(g)
    selection, by_redshift = selection_tables(g)
    mocks = mock_frame(g)
    samples = samples_of(g, mocks)
    offsets = {marker: float(np.median(mocks[marker] - mocks[f'{marker}_true'])) for marker, _ in MARKERS}
    fixed = fixed_population_table(samples, g.z.max(), offsets)
    observed = moments_table(samples)
    real_scatter = planes[(planes.arm == 'plain') & (planes.covariate == 'log_sigma_star')].scatter_plain.iloc[0]
    toy, toy_moments = toy_tables(mocks, real_scatter, observed)
    tables = {
        'per-galaxy': g, 'headline': headline_table(planes, bins), 'split-plane': planes, 'split-bins': bins,
        'binned-difference': binned, 'binned-difference-pairs': pairs, 'selection-check': selection,
        'selection-by-redshift': by_redshift, 'mock-split': mock_split_table(g, planes),
        'mock-binned': mock_binned_table(g, planes), 'mock-sfh-times': mocks,
        'progenitor-fixed-population': fixed, 'progenitor-youngest-cut': young_cut_table(samples),
        'progenitor-moments': observed, 'progenitor-toy': toy, 'progenitor-toy-moments': toy_moments,
        'progenitor-budget': budget_table(planes, fixed, toy, len(mocks)),
    }
    for name, table in tables.items():
        table.to_csv(OUT / f'{name}.csv', index=False, float_format='%.6g')


if __name__ == '__main__':
    with np.errstate(invalid='ignore', divide='ignore'):  # 0 / 0 where an estimator equals its reference
        main()
