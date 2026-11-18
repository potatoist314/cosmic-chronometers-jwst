"""Trends of SFH timing, [alpha/Fe], [Fe/H], [C/Fe], [N/Fe] and dust over the LEGA-C DR3 passive window fits.

Existing fits only. Run from the repository root:
    ceridwen/.venv/bin/python results/dr3-trends-2026-11-18/trends.py
Inputs (read only):
    results/dr3-more-galaxies-2026-11-16/fits.csv and the fit folders it names (194 + 154, arms cn_free and plain)
    results/sigma-split-2026-11-16/more-galaxies-2026-11-17/per-galaxy.csv (COSMOS2020 Classic mass)
    results/mock-chronometer-window-2026-11-13/ (194 plain-arm mocks: per-mock.csv, mocks/*.npz, fits)
    results/mock-chronometer-cn-free-2026-11-16/ (40 C/N-free mocks of the same galaxies: per-mock.csv, fits)
Outputs beside this script:
    per-galaxy.csv    posterior summaries per galaxy and arm
    trends.csv        real trends: Spearman rho, slope at fixed z, z coefficient, bootstrap 16-84%, N
    mock-null.csv     the same trends on the mocks (constant truth, one formation epoch: any trend is spurious)
    mock-recovery.csv true and recovered values per mock arm and SFH shape
    parameters.csv    posterior width / prior width, scatter of medians against mock scatter, railed counts, KDE peaks
    terciles.csv      medians in sigma_star and COSMOS2020 mass terciles
    outliers.csv      galaxies > 3 robust sigma from the linear sigma_star + z relation
    stacked-sfh.csv   normalised SFR against cosmic time, by sigma_star and COSMOS2020 mass terciles, and mocks
    fig-*.png         quick-look figures
Main sample: cn_free arm, valid fits, without the 14 COSMOS2015 saturation or bad-area galaxies (333).
"""

import importlib.util
from pathlib import Path

import h5py
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from astropy import units as u  # noqa: E402
from astropy.cosmology import Planck18, z_at_value  # noqa: E402
from scipy.stats import gaussian_kde, rankdata  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
MORE = ROOT / 'results/dr3-more-galaxies-2026-11-16'
SPLIT = ROOT / 'results/sigma-split-2026-11-16'
MOCKS = ROOT / 'results/mock-chronometer-window-2026-11-13'
MOCKS_CN = ROOT / 'results/mock-chronometer-cn-free-2026-11-16'

_spec = importlib.util.spec_from_file_location('sigma_split', SPLIT / 'sigma_split.py')
sigma_split = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sigma_split)

DRAWS, SEED = 10000, 20261118
# Prior bounds from the fit parameter block (ceridwen_derived_outputs.h5 attrs['parameter_block']).
PRIORS = {'afe': (-0.2, 0.6), 'feh': (-2.5, 0.5), 'cfe': (-0.3, 0.5), 'nfe': (-0.3, 1.0), 'tau': (0.0, 1.0)}
UNIFORM_68 = 0.68  # 16-84% range of a uniform prior, as a fraction of its full range
MOCK_TRUTH = {'afe': 0.2, 'feh': -0.2, 'cfe': 0.0, 'nfe': 0.0}  # mocks.py: constant truth for every mock
TGRID = np.arange(0.01, 8.0, 0.02)  # cosmic time grid for stacked SFHs [Gyr]

TRENDS = [
    ('age', 'log_sigma_star'), ('age', 'logmass_q50'), ('age', 'logmass_cosmos2020'), ('log_age', 'log_sigma_star'),
    ('log_age', 'logmass_cosmos2020'),
    ('t50', 'log_sigma_star'), ('t50', 'logmass_q50'), ('t50', 'logmass_cosmos2020'), ('z50', 'log_sigma_star'),
    ('t90', 'log_sigma_star'), ('t90', 'logmass_cosmos2020'), ('tquench', 'log_sigma_star'),
    ('dt_q50', 'log_sigma_star'), ('late', 'log_sigma_star'),
    ('afe_q50', 'log_sigma_star'), ('afe_q50', 'logmass_q50'), ('afe_q50', 'logmass_cosmos2020'),
    ('afe_q50', 'dt_q50'), ('afe_q50', 't50'), ('afe_q50', 'sn'),
    ('feh_q50', 'logmass_q50'), ('feh_q50', 'logmass_cosmos2020'), ('feh_q50', 'log_sigma_star'), ('feh_q50', 'afe_q50'),
    ('cfe_q50', 'log_sigma_star'), ('cfe_q50', 'logmass_cosmos2020'),
    ('nfe_q50', 'log_sigma_star'), ('nfe_q50', 'logmass_cosmos2020'),
    ('tau_q50', 'log_sigma_star'), ('tau_q50', 'logmass_cosmos2020'),
]
MOCK_ONLY = [('age_bias', 'log_sigma_star'), ('t50_bias', 'log_sigma_star'), ('dt_q50', 'true_dt'), ('late', 'true_late')]
OUTLIER_COLUMNS = ['age', 't50', 'afe_q50', 'feh_q50', 'cfe_q50', 'nfe_q50']
TERCILE_COLUMNS = ['age', 't50', 'z50', 't90', 'tquench', 'late', 'afe_q50', 'feh_q50', 'cfe_q50', 'nfe_q50', 'tau_q50']


# ---------------------------------------------------------------- per-fit summaries

def lookback_quantile(edges, fractions, younger_fraction):
    """Per draw, lookback [Gyr] at which `younger_fraction` of the formed mass is younger (sigma_split.sfh_times)."""
    fractions = fractions / fractions.sum(axis=1, keepdims=True)
    younger = np.concatenate([np.zeros((len(fractions), 1)), np.cumsum(fractions, axis=1)], axis=1)
    return np.array([np.interp(younger_fraction, y, edges) for y in younger])


def fit_row(path):
    """Posterior summaries of one fit: SFH times (lookback), fitted mass, dust; SFH density per bin [1/Gyr]."""
    with h5py.File(ROOT / path / 'ceridwen_derived_outputs.h5') as h:
        edges = h['sfh/lookback_time_gyr'][:]
        fractions = h['sfh/mass_fraction_draws'][:]
        names = [n.decode() if isinstance(n, bytes) else n for n in h['summary/parameter'][:]]
        q = {k: h[f'summary/{k}'][:] for k in ('q16', 'q50', 'q84')}
    l50, l90, lquench = sigma_split.sfh_times(edges, fractions, edges[-1])
    l10 = lookback_quantile(edges, fractions, 0.9)
    row = dict(universe_age=edges[-1])
    for name, v in (('l10', l10), ('l50', l50), ('l90', l90), ('lquench', lquench), ('dt', l10 - l90),
                    ('late', l50 - l90)):
        row.update({f'{name}_q16': np.quantile(v, 0.16), f'{name}_q50': np.median(v),
                    f'{name}_q84': np.quantile(v, 0.84)})
    for key, name in (('logmass', 'logmass'), ('tau', 'diffuse_tau_noll')):
        i = names.index(name)
        row.update({f'{key}_q16': q['q16'][i], f'{key}_q50': q['q50'][i], f'{key}_q84': q['q84'][i]})
    mean_fraction = (fractions / fractions.sum(axis=1, keepdims=True)).mean(axis=0)
    return row, edges, mean_fraction / np.diff(edges)


def formation_redshift(cosmic_gyr):
    """Redshift at a cosmic time [Gyr] in Planck18, the fits' cosmology (parameter block)."""
    t = np.clip(cosmic_gyr, 0.05, None)
    return np.array([float(z_at_value(Planck18.age, v * u.Gyr)) for v in t])


def add_times(d):
    for name in ('l10', 'l50', 'l90', 'lquench'):
        d[f't{name[1:]}'] = d.universe_age - d[f'{name}_q50']  # cosmic time [Gyr]
    d['late'] = d.late_q50  # t90 - t50 [Gyr]
    d['log_age'] = np.log10(d.age)
    d['z50'] = formation_redshift(d.t50.values)
    return d


def per_galaxy():
    fits = pd.read_csv(MORE / 'fits.csv')
    fits = fits[fits.valid].reset_index(drop=True)
    mass = pd.read_csv(SPLIT / 'more-galaxies-2026-11-17/per-galaxy.csv')[['target', 'logmass_cosmos2020']]
    rows, sfhs = [], {}
    for r in fits.itertuples():
        row, edges, density = fit_row(r.path)
        rows.append(dict(arm=r.arm, target=r.target, **row))
        sfhs[(r.arm, r.target)] = (edges, density)
    g = fits.merge(pd.DataFrame(rows), on=['arm', 'target']).merge(mass, on='target', how='left')
    g['log_sigma_star'] = np.log10(g.sigma_star)
    g['age'] = g.age_gyr_q50
    g = add_times(g)
    g['z90'] = formation_redshift(g.t90.values)
    g['main'] = g.cosmos2015 != 'saturation or bad area'
    return g, sfhs


def true_sfh(target):
    """True lookback l10, l50, l90 [Gyr] and SFH density of one mock (mocks/<target>.npz)."""
    d = np.load(MOCKS / 'mocks' / f'{target}.npz')
    edges = d['time_edges_gyr']
    mass = (d['sfh_per_bin'] * np.diff(edges))[None]
    times = [float(lookback_quantile(edges, mass, f)[0]) for f in (0.9, 0.5, 0.1)]
    return times, edges, mass[0] / mass.sum() / np.diff(edges)


def mock_table(real):
    """One row per mock with the real galaxy's sigma_star and COSMOS2020 mass; recovered and true SFH times."""
    rows, sfhs = [], {}
    for folder, arm in ((MOCKS, 'plain'), (MOCKS_CN, 'cn_free')):
        for r in pd.read_csv(folder / 'per-mock.csv').itertuples():
            fit, edges, density = fit_row(r.path.strip())
            (l10, l50, l90), true_edges, true_density = true_sfh(r.target)
            sfhs[(arm, r.target)] = (edges, density)
            sfhs[('truth', r.target)] = (true_edges, true_density)
            row = dict(mock_arm=arm, target=r.target, shape=r.shape, z=r.z, sn=r.sn, age=r.age_q50,
                       true_age=r.true_age_gyr, afe_q50=r.afe_q50, feh_q50=r.feh_q50,
                       true_l10=l10, true_l50=l50, true_l90=l90, **fit)
            if arm == 'cn_free':
                row.update(cfe_q50=r.cfe_q50, nfe_q50=r.nfe_q50)
            rows.append(row)
    m = pd.DataFrame(rows)
    ref = real[real.arm == 'plain'].set_index('target')
    for c in ('sigma_star', 'log_sigma_star', 'logmass_cosmos2020'):
        m[c] = m.target.map(ref[c])
    m = add_times(m)
    for name in ('l10', 'l50', 'l90'):
        m[f'true_t{name[1:]}'] = m.universe_age - m[f'true_{name}']
    m['true_dt'] = m.true_l10 - m.true_l90
    m['true_late'] = m.true_l50 - m.true_l90
    m['age_bias'] = m.age - m.true_age
    m['t50_bias'] = m.t50 - m.true_t50
    return m, sfhs


# ---------------------------------------------------------------- statistics

def boot_idx(n, seed=SEED, draws=None):
    return np.vstack([np.arange(n), np.random.default_rng(seed).integers(0, n, size=(draws or DRAWS, n))])


def spearman(x, y):
    """Spearman rho along the last axis."""
    rx, ry = rankdata(x, axis=-1), rankdata(y, axis=-1)
    rx, ry = rx - rx.mean(-1, keepdims=True), ry - ry.mean(-1, keepdims=True)
    return (rx * ry).sum(-1) / np.sqrt((rx**2).sum(-1) * (ry**2).sum(-1))


def ols(y, columns):
    """Least-squares coefficients (intercept first) on every bootstrap row: y (draws, N), columns list of same."""
    X = np.stack([np.ones_like(y)] + list(columns), axis=-1)
    XtX = np.einsum('dni,dnj->dij', X, X)
    Xty = np.einsum('dni,dn->di', X, y)
    return np.linalg.solve(XtX, Xty[..., None])[..., 0]


def summary(values):
    q = np.quantile(values[1:], [0.16, 0.84])
    return values[0], q[0], q[1]


def trend(d, y, x, control='z'):
    """N, Spearman rho, partial rho at fixed control, slope dy/dx at fixed control, control coefficient."""
    d = d[d[[y, x, control]].notna().all(axis=1)]
    idx = boot_idx(len(d))
    Y, X, C = d[y].values[idx], d[x].values[idx], d[control].values[idx]
    X0, C0 = X - d[x].mean(), C - d[control].mean()
    by, bx = ols(Y, [C0]), ols(X0, [C0])
    R, RX = Y - by[:, :1] - by[:, 1:] * C0, X0 - bx[:, :1] - bx[:, 1:] * C0  # residuals at fixed control
    b = ols(Y, [X0, C0])
    row = dict(y=y, x=x, control=control, N=len(d))
    for name, v in (('rho', spearman(X, Y)), ('partial_rho', spearman(RX, R)), ('slope', b[:, 1]),
                    ('control_slope', b[:, 2])):
        row.update(zip((name, f'{name}_q16', f'{name}_q84'), summary(v)))
    return row


def binned(x, y, nbins):
    """Median x, median y and bootstrap 16-84% of the median y in quantile bins of x."""
    keep = np.isfinite(x) & np.isfinite(y)
    x, y = x[keep], y[keep]
    edges = np.quantile(x, np.linspace(0, 1, nbins + 1))
    out = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = (x >= lo) & (x <= hi)
        boot = np.median(y[s][boot_idx(s.sum(), draws=1000)[1:]], axis=1)
        out.append((np.median(x[s]), np.median(y[s]), *np.quantile(boot, [0.16, 0.84])))
    return np.array(out).T


def kde_peaks(v):
    """Local maxima above 10% of the peak in a Gaussian KDE (Scott bandwidth)."""
    v = v[np.isfinite(v)]
    grid = np.linspace(v.min(), v.max(), 512)
    p = gaussian_kde(v)(grid)
    return int(((p[1:-1] > p[:-2]) & (p[1:-1] > p[2:]) & (p[1:-1] > 0.1 * p.max())).sum())


# ---------------------------------------------------------------- tables

def trend_table(g):
    rows = []
    for arm in ('cn_free', 'plain'):
        d = g[(g.arm == arm) & g.main]
        for y, x in TRENDS:
            if d[y].notna().any():
                rows.append(dict(arm=arm, sample='main', **trend(d, y, x)))
    targets = set(pd.read_csv(MOCKS_CN / 'per-mock.csv').target)
    for arm in ('cn_free', 'plain'):
        d = g[(g.arm == arm) & g.target.isin(targets)]
        for y in ('afe_q50', 'feh_q50', 'cfe_q50', 'nfe_q50'):
            if d[y].notna().any():
                rows.append(dict(arm=arm, sample='40 C/N-free mock targets', **trend(d, y, 'log_sigma_star')))
    return pd.DataFrame(rows)


def mock_null_table(m):
    rows = []
    for arm in ('plain', 'cn_free'):
        d = m[m.mock_arm == arm]
        for y, x in TRENDS + MOCK_ONLY:
            if y in d and x in d and d[y].notna().any():
                rows.append(dict(mock_arm=arm, **trend(d, y, x)))
    sub = set(m[m.mock_arm == 'cn_free'].target)
    d = m[(m.mock_arm == 'plain') & m.target.isin(sub)]
    for y in ('afe_q50', 'feh_q50'):
        rows.append(dict(mock_arm='plain, 40 C/N-free mock targets', **trend(d, y, 'log_sigma_star')))
    return pd.DataFrame(rows)


def recovery_table(m):
    cols = ['true_age', 'age', 'age_bias', 'true_t10', 't10', 'true_t50', 't50', 'true_t90', 't90',
            'true_dt', 'dt_q50', 'afe_q50', 'feh_q50', 'cfe_q50', 'nfe_q50', 'tau_q50']
    med = m.groupby(['mock_arm', 'shape'])[cols].median()
    med.insert(0, 'N', m.groupby(['mock_arm', 'shape']).size())
    allshapes = m.groupby('mock_arm')[cols].median()
    allshapes.insert(0, 'N', m.groupby('mock_arm').size())
    allshapes.index = pd.MultiIndex.from_tuples([(a, 'all') for a in allshapes.index], names=['mock_arm', 'shape'])
    return pd.concat([med, allshapes]).reset_index()


def parameter_table(g, m):
    rows = []
    d = g[(g.arm == 'cn_free') & g.main]
    for name in ('afe', 'feh', 'cfe', 'nfe', 'tau', 'age', 't50', 't90', 'dt'):
        col = {'age': 'age', 't50': 't50', 't90': 't90'}.get(name, f'{name}_q50')
        mock = m[m.mock_arm == 'cn_free'][col] if name in ('cfe', 'nfe') else m[m.mock_arm == 'plain'][col]
        row = dict(parameter=name, N=d[col].notna().sum(), median=d[col].median(), std_of_medians=d[col].std(),
                   mock_std=mock.std(), mock_N=mock.notna().sum(), kde_peaks=kde_peaks(d[col].values),
                   mock_kde_peaks=kde_peaks(mock.values))
        if name in PRIORS:
            lo, hi = PRIORS[name]
            half = (d[f'{name}_q84'] - d[f'{name}_q16']) / 2
            prior_half = UNIFORM_68 * (hi - lo) / 2
            row.update(prior_low=lo, prior_high=hi, posterior_half_width=half.median(), prior_half_width=prior_half,
                       width_ratio=(half / prior_half).median(), frac_width_ratio_above_half=(half / prior_half > 0.5).mean(),
                       n_railed=int(d[f'{name}_railed'].sum()) if f'{name}_railed' in d else np.nan)
        if name in MOCK_TRUTH:  # mocks share one truth, so their scatter is the recovery scatter
            row['mock_truth'] = MOCK_TRUTH[name]
            row['intrinsic_std_estimate'] = np.sqrt(max(row['std_of_medians']**2 - row['mock_std']**2, 0))
        rows.append(row)
    return pd.DataFrame(rows)


def tercile_table(g):
    """Medians of the main C/N-free sample in terciles of sigma_star and of COSMOS2020 mass."""
    d = g[(g.arm == 'cn_free') & g.main]
    out = []
    for by in ('sigma_star', 'logmass_cosmos2020'):
        s = d[d[by].notna()]
        groups = s.groupby(pd.qcut(s[by], 3, labels=['low', 'mid', 'high']), observed=True)
        t = groups[TERCILE_COLUMNS].median()
        t.insert(0, 'N', groups.size())
        t.insert(1, 'low_edge', groups[by].min())
        t.insert(2, 'high_edge', groups[by].max())
        t.insert(3, 'median_z', groups.z.median())
        out.append(t.reset_index(names='tercile').assign(by=by))
    out = pd.concat(out)
    return out[['by'] + [c for c in out.columns if c != 'by']]


def outlier_table(g):
    """Main C/N-free galaxies more than 3 robust sigma (1.4826 MAD) from the linear sigma_star + z relation."""
    d = g[(g.arm == 'cn_free') & g.main].reset_index(drop=True)
    X = np.column_stack([np.ones(len(d)), d.log_sigma_star, d.z])
    rows = []
    for y in OUTLIER_COLUMNS:
        resid = d[y] - X @ np.linalg.lstsq(X, d[y], rcond=None)[0]
        scale = 1.4826 * np.median(np.abs(resid - np.median(resid)))
        for i in np.flatnonzero(np.abs(resid) > 3 * scale):
            r = d.loc[i]
            rows.append(dict(quantity=y, target=r.target, value=r[y], robust_sigma_from_relation=resid[i] / scale,
                             sigma_star=r.sigma_star, z=r.z, sn=r.sn, railed=r[f'{y[:-4]}_railed'] if y.endswith('_q50') else np.nan))
    return pd.DataFrame(rows)


def sfh_on_grid(universe_age, edges, density):
    """Step SFH density [1/Gyr] at cosmic times TGRID; NaN after the observed epoch."""
    lookback = universe_age - TGRID
    i = np.searchsorted(edges, lookback, side='right') - 1
    out = density[np.clip(i, 0, len(density) - 1)]
    return np.where((lookback >= 0) & (lookback <= edges[-1]), out, np.nan)


def stack(curves):
    """Median curve and bootstrap 16-84% of the median, where at least half of the galaxies are observed."""
    curves = np.array(curves)
    boot = np.nanmedian(curves[boot_idx(len(curves), draws=300)[1:]], axis=1)
    med = np.nanmedian(curves, axis=0)
    lo, hi = np.nanquantile(boot, [0.16, 0.84], axis=0)
    covered = np.isfinite(curves).mean(axis=0) >= 0.5
    return [np.where(covered, v, np.nan) for v in (med, lo, hi)]


def stacked_table(g, sfhs, m, mock_sfhs):
    d = g[(g.arm == 'cn_free') & g.main].copy()
    cols = {}
    for by, label in (('sigma_star', 'sigma'), ('logmass_cosmos2020', 'mass')):
        s = d[d[by].notna()].copy()
        s['bin'] = pd.qcut(s[by], 3, labels=['low', 'mid', 'high'])
        for b, grp in s.groupby('bin', observed=True):
            curves = [sfh_on_grid(r.universe_age, *sfhs[('cn_free', r.target)]) for r in grp.itertuples()]
            med, lo, hi = stack(curves)
            key = f'{label}_{b}'
            cols.update({key: med, f'{key}_q16': lo, f'{key}_q84': hi})
            cols[f'{key}_range'] = np.full_like(TGRID, np.nan)
            cols[f'{key}_range'][:2] = grp[by].min(), grp[by].max()
    p = m[m.mock_arm == 'plain']
    for src, label in (('plain', 'mock_recovered'), ('truth', 'mock_truth')):
        curves = [sfh_on_grid(r.universe_age, *mock_sfhs[(src, r.target)]) for r in p.itertuples()]
        med, lo, hi = stack(curves)
        cols.update({label: med, f'{label}_q16': lo, f'{label}_q84': hi})
    return pd.DataFrame({'cosmic_time_gyr': TGRID, **cols})


# ---------------------------------------------------------------- figures (quick look only)

LABEL = {'log_sigma_star': r'$\log_{10}\,\sigma_\star\ [\mathrm{km\,s^{-1}}]$',
         'logmass_cosmos2020': r'$\log_{10}\,M_\star^{\rm COSMOS2020}\ [M_\odot]$',
         't50': r'$t_{50}$ [Gyr, cosmic time]', 't90': r'$t_{90}$ [Gyr, cosmic time]',
         'afe_q50': r'$[\alpha/\mathrm{Fe}]$', 'feh_q50': r'$[\mathrm{Fe/H}]$',
         'cfe_q50': r'$[\mathrm{C/Fe}]$', 'nfe_q50': r'$[\mathrm{N/Fe}]$'}
_ZGRID = np.linspace(0.3, 20, 4000)
_TGRID_Z = Planck18.age(_ZGRID).value


def time_to_z(t):
    return np.interp(t, _TGRID_Z[::-1], _ZGRID[::-1])


def z_to_time(z):
    return np.interp(z, _ZGRID, _TGRID_Z)


def panel(ax, d, m_plain, m_cn, plain, y, x, truth=None, prior=None, nbins=6):
    sc = ax.scatter(d[x], d[y], c=d.z, s=7, cmap='viridis', vmin=0.6, vmax=1.0, alpha=0.6, lw=0)
    xb, yb, lo, hi = binned(d[x].values, d[y].values, nbins)
    ax.errorbar(xb, yb, [yb - lo, hi - yb], color='k', marker='o', ms=5, lw=1.5, capsize=2,
                label=r'C/N-free fits, median', zorder=5)
    if plain is not None and plain[y].notna().any():
        xb, yb, lo, hi = binned(plain[x].values, plain[y].values, nbins)
        ax.plot(xb, yb, color='0.45', ls='--', marker='s', ms=3, lw=1, label='plain arm, median', zorder=4)
    for mk, color, label, n in ((m_plain, 'tab:orange', 'plain mocks (194), median', nbins),
                                (m_cn, 'tab:red', 'C/N-free mocks (40), median', 3)):
        if mk is not None and y in mk and mk[y].notna().any():
            xb, yb, lo, hi = binned(mk[x].values, mk[y].values, n)
            ax.errorbar(xb, yb, [yb - lo, hi - yb], color=color, marker='D', ms=4, lw=1.2, capsize=2,
                        label=label, zorder=6)
    if truth is not None:
        ax.axhline(truth, color='tab:orange', ls=':', lw=1.2, label='mock truth')
    if prior is not None:
        for v in prior:
            ax.axhline(v, color='0.6', lw=0.8, ls='-.')
    ax.set_xlabel(LABEL[x])
    ax.set_ylabel(LABEL[y])
    return sc


def figures(g, m, stacked):
    d = g[(g.arm == 'cn_free') & g.main]
    plain = g[(g.arm == 'plain') & g.main]
    mp, mc = m[m.mock_arm == 'plain'], m[m.mock_arm == 'cn_free']
    plt.rcParams.update({'font.size': 10})

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
    for ax, y in zip(axes, ('t50', 't90')):
        sc = panel(ax, d, mp, None, plain, y, 'log_sigma_star')
        xb, yb, lo, hi = binned(mp.log_sigma_star.values, mp[f'true_{y}'].values, 6)
        ax.plot(xb, yb, color='tab:orange', ls=':', lw=1.2, label='mock truth (one epoch)')
        sec = ax.secondary_yaxis('right', functions=(time_to_z, z_to_time))
        sec.set_ylabel(r'$z$')
        sec.set_yticks([1, 1.5, 2, 3, 5, 10])
    axes[0].legend(fontsize=7, loc='upper right')
    fig.colorbar(sc, ax=axes, label=r'$z_{\rm obs}$')
    fig.savefig(OUT / 'fig-formation-sigma.png', dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True, constrained_layout=True)
    colors = {'low': 'tab:blue', 'mid': 'tab:green', 'high': 'tab:red'}
    for ax, label, unit in ((axes[0], 'sigma', r'\sigma_\star'), (axes[1], 'mass', r'\log M_\star')):
        for b, color in colors.items():
            key = f'{label}_{b}'
            lo_v, hi_v = stacked[f'{key}_range'][:2]
            text = (f'${lo_v:.0f}<{unit}<{hi_v:.0f}$' if label == 'sigma' else f'${lo_v:.2f}<{unit}<{hi_v:.2f}$')
            ax.plot(stacked.cosmic_time_gyr, stacked[key], color=color, lw=1.6, label=text)
            ax.fill_between(stacked.cosmic_time_gyr, stacked[f'{key}_q16'], stacked[f'{key}_q84'], color=color,
                            alpha=0.2, lw=0)
        ax.plot(stacked.cosmic_time_gyr, stacked.mock_recovered, color='0.3', ls='--', lw=1.2,
                label='plain mocks, recovered')
        ax.plot(stacked.cosmic_time_gyr, stacked.mock_truth, color='0.3', ls=':', lw=1.2, label='plain mocks, truth')
        ax.set_xlabel('cosmic time [Gyr]')
        ax.set_xlim(0, 7.5)
        ax.set_yscale('log')
        ax.set_ylim(0.01, 5)
        sec = ax.secondary_xaxis('top', functions=(time_to_z, z_to_time))
        sec.set_xlabel(r'$z$')
        sec.set_xticks([0.7, 1, 1.5, 2, 3, 5])
        ax.legend(fontsize=7, loc='lower left')
    axes[0].set_ylabel(r'median SFR / $M_{\rm formed}$ [Gyr$^{-1}$]')
    axes[0].set_title(r'C/N-free fits, $\sigma_\star$ terciles [km s$^{-1}$]', fontsize=9)
    axes[1].set_title(r'C/N-free fits, COSMOS2020 mass terciles [$M_\odot$]', fontsize=9)
    fig.savefig(OUT / 'fig-stacked-sfh.png', dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
    panel(axes[0], d, mp, mc, plain, 'afe_q50', 'log_sigma_star', truth=MOCK_TRUTH['afe'], prior=PRIORS['afe'])
    sc = panel(axes[1], d, mp, mc, plain, 'feh_q50', 'logmass_cosmos2020', truth=MOCK_TRUTH['feh'])
    axes[1].set_ylim(-1.2, 0.5)
    axes[0].legend(fontsize=7, loc='upper right')
    fig.colorbar(sc, ax=axes, label=r'$z_{\rm obs}$')
    fig.savefig(OUT / 'fig-afe-feh.png', dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), constrained_layout=True)
    panel(axes[0], d, None, mc, None, 'cfe_q50', 'log_sigma_star', truth=MOCK_TRUTH['cfe'], prior=PRIORS['cfe'])
    sc = panel(axes[1], d, None, mc, None, 'nfe_q50', 'log_sigma_star', truth=MOCK_TRUTH['nfe'], prior=PRIORS['nfe'])
    axes[1].legend(fontsize=7, loc='upper left')
    fig.colorbar(sc, ax=axes, label=r'$z_{\rm obs}$')
    fig.savefig(OUT / 'fig-cn-sigma.png', dpi=150)
    plt.close(fig)


def main():
    g, sfhs = per_galaxy()
    m, mock_sfhs = mock_table(g)
    g.to_csv(OUT / 'per-galaxy.csv', index=False)
    trend_table(g).to_csv(OUT / 'trends.csv', index=False)
    mock_null_table(m).to_csv(OUT / 'mock-null.csv', index=False)
    recovery_table(m).to_csv(OUT / 'mock-recovery.csv', index=False)
    parameter_table(g, m).to_csv(OUT / 'parameters.csv', index=False)
    tercile_table(g).to_csv(OUT / 'terciles.csv', index=False)
    outlier_table(g).to_csv(OUT / 'outliers.csv', index=False)
    stacked = stacked_table(g, sfhs, m, mock_sfhs)
    stacked.to_csv(OUT / 'stacked-sfh.csv', index=False)
    figures(g, m, stacked)


if __name__ == '__main__':
    main()
