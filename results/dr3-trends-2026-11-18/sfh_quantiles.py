"""Mass-assembly times t20, t50, t80 and t_sf = t80 - t20 over the LEGA-C DR3 passive window fits.

t_X is the cosmic time [Gyr] when X% of the formed stellar mass was in place. t_sf = t80 - t20 is the
star-formation timescale of Liu Hao's note (Freenotes, "sandro meeting 2", p. 10, 2026-09-15), which also
says to plot t_sf against [alpha/Fe].

Existing fits only. Run from the repository root, after trends.py:
    ceridwen/.venv/bin/python results/dr3-trends-2026-11-18/sfh_quantiles.py
Inputs (read only): per-galaxy.csv beside this script and the fit folders it names; the two mock folders that
trends.py reads. Each quantile is computed per posterior draw, then summarised per galaxy (median, 16-84%).
Outputs beside this script:
    sfh-quantiles.csv     one row per bin, slope or mock summary; columns t20, t50, t80, tsf with 16-84%
    fig-t20-t50-t80.png   quick-look figure
"""

import importlib.util
from pathlib import Path

import h5py
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from astropy.cosmology import Planck18  # noqa: E402

OUT = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('trends', OUT / 'trends.py')
trends = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(trends)

FRACTIONS = {'t20': 0.2, 't50': 0.5, 't80': 0.8}  # fraction of the formed mass in place
Q = ['t20', 't50', 't80', 'tsf']
TERCILES = ['low', 'mid', 'high']
BIN_DRAWS = 1000  # bootstrap draws for bin medians, as trends.binned
COLOR = {'t20': 'tab:blue', 't50': 'k', 't80': 'tab:red', 'tsf': 'tab:purple'}
SYMBOL = {'t20': r'$t_{20}$', 't50': r'$t_{50}$', 't80': r'$t_{80}$', 'tsf': r'$t_{\rm sf}=t_{80}-t_{20}$'}


# ---------------------------------------------------------------- per-fit quantiles

def quantile_draws(edges, mass, universe_age):
    """Per draw: cosmic time [Gyr] with 20, 50, 80% of the formed mass in place, and t_sf = t80 - t20."""
    v = {k: universe_age - trends.lookback_quantile(edges, mass, 1 - f) for k, f in FRACTIONS.items()}
    v['tsf'] = v['t80'] - v['t20']
    return v


def fit_quantiles(path):
    """Per-galaxy median and 16-84% of each quantile; also the fit's cosmic age at z_obs."""
    with h5py.File(trends.ROOT / path / 'ceridwen_derived_outputs.h5') as h:
        edges = h['sfh/lookback_time_gyr'][:]
        fractions = h['sfh/mass_fraction_draws'][:]
    row = dict(universe_age=edges[-1])
    for k, v in quantile_draws(edges, fractions, edges[-1]).items():
        row.update({k: np.median(v), f'{k}_q16': np.quantile(v, 0.16), f'{k}_q84': np.quantile(v, 0.84)})
    return row


def galaxies():
    g = pd.read_csv(OUT / 'per-galaxy.csv')
    q = pd.DataFrame([fit_quantiles(p) for p in g.path]).drop(columns='universe_age')
    return pd.concat([g.drop(columns=['t50']).reset_index(drop=True), q], axis=1)


def mocks(g):
    """trends.mock_table plus recovered and true t20, t50, t80, t_sf for every mock."""
    m, _ = trends.mock_table(g)
    rows = []
    for folder, arm in ((trends.MOCKS, 'plain'), (trends.MOCKS_CN, 'cn_free')):
        for r in pd.read_csv(folder / 'per-mock.csv').itertuples():
            fit = fit_quantiles(r.path.strip())
            d = np.load(trends.MOCKS / 'mocks' / f'{r.target}.npz')
            true = quantile_draws(d['time_edges_gyr'], (d['sfh_per_bin'] * np.diff(d['time_edges_gyr']))[None],
                                  fit['universe_age'])
            rows.append(dict(mock_arm=arm, target=r.target, **{k: fit[k] for k in Q},
                             **{f'true_{k}': float(v[0]) for k, v in true.items()}))
    return m.drop(columns=['t50', 'true_t50']).merge(pd.DataFrame(rows), on=['mock_arm', 'target'])


# ---------------------------------------------------------------- tables

def median_row(grp):
    """Bin median of each quantile and bootstrap 16-84% of that median."""
    idx = trends.boot_idx(len(grp), draws=BIN_DRAWS)
    row = {}
    for k in Q:
        row.update(zip((k, f'{k}_q16', f'{k}_q84'), trends.summary(np.median(grp[k].values[idx], axis=1))))
    return row


def bin_table(g):
    rows = []
    for arm in ('cn_free', 'plain'):
        d = g[(g.arm == arm) & g.main]
        for by in ('sigma_star', 'logmass_cosmos2020'):
            s = d[d[by].notna()]
            for b, grp in s.groupby(pd.qcut(s[by], 3, labels=TERCILES), observed=True):
                rows.append(dict(table=f'{by} tercile', arm=arm, bin=b, N=len(grp), x=by, x_low=grp[by].min(),
                                 x_high=grp[by].max(), x_median=grp[by].median(), z_median=grp.z.median(),
                                 universe_age_median=grp.universe_age.median(), **median_row(grp)))
        for b, tercile in d.groupby(pd.qcut(d.sigma_star, 3, labels=TERCILES), observed=True):
            for h, grp in tercile.groupby(pd.qcut(tercile.z, 2, labels=['low z', 'high z']), observed=True):
                rows.append(dict(table='z half at fixed sigma_star', arm=arm, bin=f'sigma_star {b}, {h}', N=len(grp),
                                 x='z', x_low=grp.z.min(), x_high=grp.z.max(), x_median=grp.z.median(),
                                 z_median=grp.z.median(), universe_age_median=grp.universe_age.median(),
                                 **median_row(grp)))
    return rows


def trend_rows(d, x, label, **extra):
    """trends.trend for every quantile: slope at fixed z, z coefficient at fixed x, Spearman rho."""
    t = {k: trends.trend(d, k, x) for k in Q}
    out = []
    for stat, name in (('slope', f'slope vs {label} at fixed z'), ('control_slope', f'dt/dz at fixed {label}'),
                       ('rho', f'Spearman rho vs {label}')):
        row = dict(table=name, N=t['t50']['N'], x=x, **extra)
        for k in Q:
            row.update({k: t[k][stat], f'{k}_q16': t[k][f'{stat}_q16'], f'{k}_q84': t[k][f'{stat}_q84']})
        out.append(row)
    return out


def slope_table(g, m):
    rows = []
    for arm in ('cn_free', 'plain'):
        d = g[(g.arm == arm) & g.main]
        rows += trend_rows(d, 'log_sigma_star', 'log sigma_star', arm=arm)
        rows += trend_rows(d, 'afe_q50', '[alpha/Fe]', arm=arm)
    for arm in ('plain', 'cn_free'):
        rows += [r for r in trend_rows(m[m.mock_arm == arm], 'log_sigma_star', 'log sigma_star', arm=f'mock {arm}')
                 if r['table'].startswith('slope')]
    return rows


def mock_rows(m):
    rows = []
    for arm in ('plain', 'cn_free'):
        mk = m[m.mock_arm == arm]
        for shape, grp in list(mk.groupby('shape')) + [('all', mk)]:
            true = dict(table='mock truth', arm=f'mock {arm}', bin=shape, N=len(grp))
            rec = dict(table='mock recovered', arm=f'mock {arm}', bin=shape, N=len(grp))
            for k in Q:  # 16-84% across mocks: the recovery scatter of one galaxy
                true.update({k: grp[f'true_{k}'].median(), f'{k}_q16': grp[f'true_{k}'].quantile(0.16),
                             f'{k}_q84': grp[f'true_{k}'].quantile(0.84)})
                rec.update({k: grp[k].median(), f'{k}_q16': grp[k].quantile(0.16), f'{k}_q84': grp[k].quantile(0.84)})
            rows += [true, rec]
        idx = trends.boot_idx(len(mk))
        row = dict(table='mock response d(recovered)/d(true)', arm=f'mock {arm}', N=len(mk))
        for k in Q:
            Y, X = mk[k].values[idx], mk[f'true_{k}'].values[idx]
            b = trends.ols(Y, [X - X.mean(axis=1, keepdims=True)])[:, 1]
            row.update(zip((k, f'{k}_q16', f'{k}_q84'), trends.summary(b)))
        rows.append(row)
    return rows


# ---------------------------------------------------------------- figure (quick look only)

def twin_z(ax):
    sec = ax.secondary_yaxis('right', functions=(trends.time_to_z, trends.z_to_time))
    sec.set_ylabel(r'$z$')
    sec.set_yticks([1, 1.5, 2, 3, 5])


def errbar(ax, x, r, k, **kw):
    ax.errorbar(x, r[k], [r[k] - r[f'{k}_q16'], r[f'{k}_q84'] - r[k]], color=COLOR[k], capsize=2, **kw)


def figure(t, g):
    plt.rcParams.update({'font.size': 10})
    fig, axes = plt.subplots(2, 4, figsize=(17, 8.6), constrained_layout=True)
    sty = {'cn_free': dict(marker='o', ms=5, lw=1.5, ls='-'),
           'plain': dict(marker='s', ms=3.5, lw=1, ls='--', mfc='white', alpha=0.8)}

    for ax, by, xlabel, fmt in ((axes[0, 0], 'sigma_star', trends.LABEL['log_sigma_star'], np.log10),
                                (axes[0, 1], 'logmass_cosmos2020', trends.LABEL['logmass_cosmos2020'], None)):
        for arm in ('cn_free', 'plain'):
            r = t[(t.table == f'{by} tercile') & (t.arm == arm)]
            x = fmt(r.x_median) if fmt else r.x_median
            for k in ('t20', 't50', 't80'):
                errbar(ax, x + (0.005 if arm == 'plain' else 0), r, k, **sty[arm],
                       label=f'{SYMBOL[k]}, ' + ('C/N-free' if arm == 'cn_free' else 'plain'))
        ax.set_xlabel(xlabel)
        ax.set_ylabel('cosmic time [Gyr]')
        ax.set_title('tercile medians, bootstrap 16–84%', fontsize=9)
    axes[0, 0].sharey(axes[0, 1])
    axes[0, 0].legend(fontsize=7, ncol=2, loc='upper right')
    twin_z(axes[0, 1])

    ax = axes[0, 2]
    d = g[(g.arm == 'cn_free') & g.main]
    ax.scatter(d.afe_q50, d.tsf, s=6, color='0.6', lw=0, alpha=0.6, label='C/N-free fits')
    for arm, s in (('cn_free', sty['cn_free']), ('plain', sty['plain'])):
        dd = g[(g.arm == arm) & g.main]
        xb, yb, lo, hi = trends.binned(dd.afe_q50.values, dd.tsf.values, 5)
        ax.errorbar(xb, yb, [yb - lo, hi - yb], color=COLOR['tsf'], capsize=2, **s,
                    label=('C/N-free' if arm == 'cn_free' else 'plain') + ', quintile median')
    rho = t[(t.table == 'Spearman rho vs [alpha/Fe]') & (t.arm == 'cn_free')].iloc[0]
    ax.text(0.03, 0.97, rf'$\rho={rho.tsf:.2f}$ [{rho.tsf_q16:.2f}, {rho.tsf_q84:.2f}]', transform=ax.transAxes,
            va='top', fontsize=8)
    ax.set_xlabel(trends.LABEL['afe_q50'])
    ax.set_ylabel(r'$t_{\rm sf}=t_{80}-t_{20}$ [Gyr]')
    ax.set_title(r'$t_{\rm sf}$ against $[\alpha/\mathrm{Fe}]$', fontsize=9)
    ax.legend(fontsize=7, loc='upper right')

    ax = axes[0, 3]
    for arm, s in (('plain', dict(marker='o', ms=5)), ('cn_free', dict(marker='D', ms=4, mfc='white'))):
        tr = t[(t.table == 'mock truth') & (t.arm == f'mock {arm}') & (t.bin != 'all')]
        rc = t[(t.table == 'mock recovered') & (t.arm == f'mock {arm}') & (t.bin != 'all')]
        for k in ('t20', 't50', 't80'):
            ax.errorbar(tr[k].values, rc[k].values, [rc[k] - rc[f'{k}_q16'], rc[f'{k}_q84'] - rc[k]],
                        color=COLOR[k], ls='none', capsize=2, **s,
                        label=f'{SYMBOL[k]}, {"194 plain" if arm == "plain" else "40 C/N-free"} mocks')
    lim = [0, 5.5]
    ax.plot(lim, lim, color='0.5', lw=0.8, ls=':', label='recovered = true')
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel('true [Gyr, cosmic time]')
    ax.set_ylabel('recovered [Gyr, cosmic time]')
    ax.set_title('mocks: median per SFH shape, 16–84% of mocks', fontsize=9)
    ax.legend(fontsize=7, loc='upper left', ncol=1)
    twin_z(ax)

    zgrid = np.linspace(0.55, 1.05, 50)
    for i, b in enumerate(TERCILES):
        ax = axes[1, i]
        ax.plot(zgrid, Planck18.age(zgrid).value, color='0.6', lw=1, label='age of the Universe at $z_{\\rm obs}$')
        sig = t[(t.table == 'sigma_star tercile') & (t.arm == 'cn_free') & (t.bin == b)].iloc[0]
        for arm in ('cn_free', 'plain'):
            r = t[(t.table == 'z half at fixed sigma_star') & (t.arm == arm) & t.bin.astype(str).str.startswith(f'sigma_star {b},')]
            for k in ('t20', 't50', 't80'):
                errbar(ax, r.x_median + (0.004 if arm == 'plain' else 0), r, k, **sty[arm],
                       label=f'{SYMBOL[k]}, ' + ('C/N-free' if arm == 'cn_free' else 'plain'))
        ax.set_xlabel(r'$z_{\rm obs}$ (median of each half)')
        ax.set_title(rf'$\sigma_\star$ {b} tercile, {sig.x_low:.0f}–{sig.x_high:.0f} km s$^{{-1}}$', fontsize=9)
        ax.set_ylim(0, 8)
        if i:
            ax.sharey(axes[1, 0])
            ax.tick_params(labelleft=False)
        else:
            ax.set_ylabel('cosmic time [Gyr]')
    axes[1, 0].legend(fontsize=7, loc='lower right')
    twin_z(axes[1, 2])

    ax = axes[1, 3]
    sets = (('cn_free', 'k', 'o', 'C/N-free fits (333)'), ('plain', '0.5', 's', 'plain fits (334)'),
            ('mock plain', 'tab:orange', 'D', 'plain mocks (194)'), ('mock cn_free', 'tab:red', 'D', 'C/N-free mocks (40)'))
    for j, (arm, color, marker, label) in enumerate(sets):
        r = t[(t.table == 'slope vs log sigma_star at fixed z') & (t.arm == arm)].iloc[0]
        x = np.arange(len(Q)) + (j - 1.5) * 0.15
        v = np.array([r[k] for k in Q])
        lo, hi = np.array([r[f'{k}_q16'] for k in Q]), np.array([r[f'{k}_q84'] for k in Q])
        ax.errorbar(x, v, [v - lo, hi - v], color=color, marker=marker, ls='none', ms=5, capsize=2, label=label)
    ax.axhline(0, color='0.6', lw=0.8)
    ax.set_xticks(range(len(Q)), [SYMBOL[k] if k != 'tsf' else r'$t_{\rm sf}$' for k in Q])
    ax.set_ylabel(r'$\mathrm{d}t/\mathrm{d}\log_{10}\sigma_\star$ at fixed $z$ [Gyr dex$^{-1}$]')
    ax.set_title('slopes, bootstrap 16–84%; mock truth has no trend', fontsize=9)
    ax.legend(fontsize=7, loc='lower left')
    fig.savefig(OUT / 'fig-t20-t50-t80.png', dpi=140)
    plt.close(fig)


def main():
    g = galaxies()
    m = mocks(g)
    t = pd.DataFrame(bin_table(g) + slope_table(g, m) + mock_rows(m))
    lead = ['table', 'arm', 'bin', 'N', 'x', 'x_low', 'x_high', 'x_median', 'z_median', 'universe_age_median']
    t = t[lead + [c for k in Q for c in (k, f'{k}_q16', f'{k}_q84')]]
    t.to_csv(OUT / 'sfh-quantiles.csv', index=False)
    figure(t, g)


if __name__ == '__main__':
    main()
