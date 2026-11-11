"""Age-redshift slope of the oldest galaxies (upper age envelope) on the chronometer-135 fits.

Run: PYTHONPATH=external/sedpy_jax ceridwen/.venv/bin/python results/oldest-envelope-2026-11-11/envelope.py
Inputs (read only): results/chronometer-135-2026-11-10/per-fit.csv, data/raw/legac_dr2/legaCdr2.fits.gz.
"""

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.table import Table
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/oldest-envelope-2026-11-11'
ARMS = ('e_cn_afe0p25_common', 'h_baseline_common', 'i_baseline_w110', 'j_cn_free_w110')  # the common-window fits
SIGMA_SPLIT = 215.0  # km/s, Borghi et al. 2022b (ApJL 928, L4), Sect. 2: median sigma_* of their 140 galaxies
DRAWS, SEED = 10000, 20261110  # same galaxy-bootstrap convention as results/chronometer-135-2026-11-10
H_UNIT = (1 / u.Gyr).to_value(u.km / u.s / u.Mpc)

# Choice grid. Defaults are fixed here, before any result: Moresco et al. 2012a (JCAP 08, 006), App. A.1,
# median of the values above the bin median; four bins as in Borghi et al. 2022b; tau 0.7 as in
# Jimenez et al. 2023 (arXiv:2306.11425), Sect. 2.3; Delta lnP = 0.5 as in Jimenez et al. 2003 (ApJ 593, 622), Sect. 3.4.
BINS = (2, 3, 4, 5, 6)  # Borghi et al. 2022b, Sect. 3.1: "from two up to six redshift intervals"
FRACTIONS = (0.5, 1 / 3, 0.25, 0.2)
QUANTILES = (0.75, 0.84, 0.90)
TAUS = (0.7, 0.8, 0.9)
DEFAULT = {'oldest_fraction': (0.5, 4), 'bin_quantile': (0.75, 4), 'quantile_regression': (0.7, None),
           'edge_dlnP_0p5': (None, 4)}


def ols_slope(x, y):
    """Least-squares slope along the last axis."""
    xc = x - x.mean(axis=-1, keepdims=True)
    return np.sum(xc * y, axis=-1) / np.sum(xc**2, axis=-1)


def edge(a, d):
    """Jimenez et al. 2003, Sect. 3.4: ln P(t) = -sum over a_i + d_i > t of x_i^2, x_i = (a_i + d_i - t) / (sqrt(2) d_i);
    the edge is where ln P drops by 0.5 from its maximum (0). a, d: (draws, n). Bisection on the monotone sum."""
    lo, hi = (a - 10 * d).min(axis=1), (a + d).max(axis=1)
    for _ in range(80):
        t = 0.5 * (lo + hi)
        x = np.clip(a + d - t[:, None], 0, None) / (np.sqrt(2) * d)
        above = np.sum(x**2, axis=1) > 0.5
        lo, hi = np.where(above, t, lo), np.where(above, hi, t)
    t = 0.5 * (lo + hi)
    return t, np.sum(a + d > t[:, None], axis=1)


def binned(z, y, d, nbins, kind, p):
    """Points of one binned estimator. z, y, d: (draws, N). Equal-count bins in z (np.array_split sizes).
    Returns point z, point age, galaxies that set each point: (draws, nbins)."""
    order = np.argsort(z, axis=1, kind='stable')
    z, y, d = (np.take_along_axis(v, order, axis=1) for v in (z, y, d))
    zp, yp, n_set = [], [], []
    for chunk in np.array_split(np.arange(z.shape[1]), nbins):
        zb, yb, db = z[:, chunk], y[:, chunk], d[:, chunk]
        n = len(chunk)
        if kind == 'oldest_fraction':  # median age and median z of the k oldest galaxies of the bin
            k = max(1, int(np.floor(p * n + 0.5)))
            top = np.argsort(yb, axis=1, kind='stable')[:, -k:]
            zp.append(np.median(np.take_along_axis(zb, top, axis=1), axis=1))
            yp.append(np.median(np.take_along_axis(yb, top, axis=1), axis=1))
            n_set.append(np.full(len(z), k))
        elif kind == 'bin_quantile':  # age quantile of the bin (numpy linear interpolation) at the bin median z
            zp.append(np.median(zb, axis=1))
            yp.append(np.quantile(yb, p, axis=1))
            n_set.append(np.full(len(z), n))
        else:  # edge_dlnP_0p5, at the bin median z; galaxies with a_i + d_i above the edge set it
            t, m = edge(yb, db)
            zp.append(np.median(zb, axis=1))
            yp.append(t)
            n_set.append(m)
    return np.stack(zp, 1), np.stack(yp, 1), np.stack(n_set, 1)


def quantreg(z, y, tau):
    """Linear quantile regression (Koenker & Bassett 1978) as a linear program, scipy HiGHS. Returns slope, galaxies above."""
    n = len(z)
    zc = z - z.mean()
    c = np.r_[0.0, 0.0, np.full(n, tau), np.full(n, 1 - tau)]
    a_eq = np.c_[np.ones(n), zc, np.eye(n), -np.eye(n)]
    x = linprog(c, A_eq=a_eq, b_eq=y, bounds=[(None, None)] * 2 + [(0, None)] * (2 * n), method='highs').x
    return x[1], int(np.sum(y > x[0] + x[1] * zc + 1e-9))


def quantreg_draws(args):
    z, y, tau = args
    return np.array([quantreg(zi, yi, tau)[0] for zi, yi in zip(z, y)])


def hubble(slope, z):
    # Jimenez & Loeb 2002 eq. 2 with dt/dz = d(age)/dz, as results/chronometer-135-2026-11-10/REPORT.md
    return -H_UNIT / ((1 + z) * slope) if slope < 0 else np.nan


def main():
    import sys
    sys.path.insert(0, str(ROOT / 'ceridwen'))
    from ceridwen.cosmology import age_gyr, resolve_cosmology
    cosmo = resolve_cosmology(None)  # Planck18, the fit cosmology

    fits = pd.read_csv(ROOT / 'results/chronometer-135-2026-11-10/per-fit.csv')
    fits = fits[fits.arm.isin(ARMS) & fits.valid.astype(bool)]
    cat = Table.read(ROOT / 'data/raw/legac_dr2/legaCdr2.fits.gz')
    sigma = pd.Series(np.asarray(cat['SIGMA_STARS_PRIME'], float), index=np.asarray(cat['SPECT_ID']).astype(str))
    fits['sigma_star'] = fits.target.map(sigma)
    assert fits.sigma_star.notna().all() and (fits.seed == 20260832).all()
    same = sorted(set.intersection(*(set(fits.target[fits.arm == a]) for a in ARMS)))

    samples = []
    for arm in ARMS:
        own = fits[fits.arm == arm].sort_values('target')
        for name, frame in (('own valid', own), ('same galaxies', own[own.target.isin(same)])):
            samples.append((arm, name, frame))
            samples.append((arm, f'{name}, sigma* > 215', frame[frame.sigma_star > SIGMA_SPLIT]))

    rows, points, qr_jobs = [], [], []
    for arm, name, s in samples:
        z0, y0 = s.z.to_numpy(), s.age_gyr_q50.to_numpy()
        d0 = (s.age_gyr_q84 - s.age_gyr_q50).to_numpy()
        tu0 = np.asarray(age_gyr(z0, cosmo))
        n = len(z0)
        ix = np.random.default_rng(SEED).integers(0, n, size=(DRAWS, n))
        z, y, d = z0[ix], y0[ix], d0[ix]
        all_draws = ols_slope(z, y)
        base = dict(arm=arm, sample=name, galaxies=n, z_min=z0.min(), z_max=z0.max(), z_median=float(np.median(z0)),
                    sigma_star_median=float(np.median(s.sigma_star)), all_slope=float(ols_slope(z0, y0)),
                    all_q16=np.quantile(all_draws, 0.16), all_q84=np.quantile(all_draws, 0.84),
                    planck18_line_slope=float(ols_slope(z0, tu0)), _all_draws=all_draws)
        grid = [('oldest_fraction', p, b) for p in FRACTIONS for b in BINS] + \
               [('bin_quantile', p, b) for p in QUANTILES for b in BINS] + [('edge_dlnP_0p5', None, b) for b in BINS]
        for kind, p, b in grid:
            zp, yp, ns = binned(z0[None], y0[None], d0[None], b, kind, p)
            draws = ols_slope(*binned(z, y, d, b, kind, p)[:2])
            zt, yt, _ = binned(z0[None], tu0[None], d0[None], b, kind, p) if kind != 'edge_dlnP_0p5' else (zp, None, None)
            p18 = float(ols_slope(zt, yt)[0]) if yt is not None else np.nan
            rows.append(base | dict(estimator=kind, param=p, bins=b, slope=float(ols_slope(zp, yp)[0]),
                                    draws=draws, planck18_same_estimator=p18,
                                    per_point_min=int(ns.min()), per_point_max=int(ns.max())))
            points += [dict(arm=arm, sample=name, estimator=kind, param=p, bins=b, bin=k + 1, z_point=zp[0, k],
                            age_point=yp[0, k], galaxies_setting_point=int(ns[0, k])) for k in range(b)]
        for tau in TAUS:
            slope, above = quantreg(z0, y0, tau)
            slope_t = quantreg(z0, tu0, tau)[0]
            rows.append(base | dict(estimator='quantile_regression', param=tau, bins=np.nan, slope=slope, draws=None,
                                    planck18_same_estimator=slope_t, per_point_min=above, per_point_max=above))
            qr_jobs.append((len(rows) - 1, (z, y, tau)))

    with ProcessPoolExecutor(max_workers=8) as pool:
        for (i, _), draws in zip(qr_jobs, pool.map(quantreg_draws, [job for _, job in qr_jobs])):
            rows[i]['draws'] = draws

    out = []
    for r in rows:
        draws, all_draws = r.pop('draws'), r.pop('_all_draws')
        diff = draws - all_draws
        q16, q50, q84 = np.quantile(draws, [0.16, 0.5, 0.84])
        p, b = r['param'], r['bins']
        default = DEFAULT[r['estimator']] == (None if r['estimator'] == 'edge_dlnP_0p5' else p,
                                             None if r['estimator'] == 'quantile_regression' else b)
        out.append(r | dict(q16=q16, q50=q50, q84=q84, diff_vs_all_q16=np.quantile(diff, 0.16),
                            diff_vs_all_q50=np.quantile(diff, 0.5), diff_vs_all_q84=np.quantile(diff, 0.84),
                            planck18_line_in_16_84=bool(q16 <= r['planck18_line_slope'] <= q84),
                            H_kms_mpc=hubble(r['slope'], r['z_median']), H_from_q16=hubble(q16, r['z_median']),
                            H_from_q84=hubble(q84, r['z_median']),
                            H_planck18_line=hubble(r['planck18_line_slope'], r['z_median']), default=default))
    table = pd.DataFrame(out)
    order = ['arm', 'sample', 'galaxies', 'z_min', 'z_max', 'z_median', 'sigma_star_median', 'estimator', 'param', 'bins',
             'default', 'slope', 'q16', 'q50', 'q84', 'per_point_min', 'per_point_max', 'all_slope', 'all_q16', 'all_q84',
             'diff_vs_all_q16', 'diff_vs_all_q50', 'diff_vs_all_q84', 'planck18_line_slope', 'planck18_same_estimator',
             'planck18_line_in_16_84', 'H_kms_mpc', 'H_from_q16', 'H_from_q84', 'H_planck18_line']
    table[order].to_csv(OUT / 'envelope-slopes.csv', index=False)
    pd.DataFrame(points).to_csv(OUT / 'envelope-points.csv', index=False)
    print(table.groupby(['arm', 'sample']).galaxies.first())


if __name__ == '__main__':
    main()
