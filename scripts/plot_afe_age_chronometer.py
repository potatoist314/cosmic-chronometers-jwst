"""Chronometer figures and table of the wiki page q-afe-age-chronometer.

Age against redshift for the LEGA-C DR3 window-194 galaxies (plain, C/N free and carbon-mask arms),
and the mock chronometer on the same window from every valid mock fit present. Re-run as more mocks finish.

Usage: ``ceridwen/.venv/bin/python scripts/plot_afe_age_chronometer.py``
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import h5py
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patheffects
from matplotlib.colors import to_rgb

ROOT = Path(__file__).resolve().parents[1]
DR3 = ROOT / "results/legac-dr3-2026-11-11"
MASK = ROOT / "results/carbon-mask-window-2026-11-13"
MOCK = ROOT / "results/mock-chronometer-window-2026-11-13"
OUT = ROOT / "wiki/analyses/afe-age-chronometer"

spec = importlib.util.spec_from_file_location("mocks", MOCK / "mocks.py")
mocks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mocks)  # line_fit, read_design, TRUE_AFE of the mock experiment

from ceridwen.cosmology import age_gyr, resolve_cosmology  # noqa: E402
from scripts.experiment import validate_result  # noqa: E402

COSMO = resolve_cosmology(None)  # Planck18, as the slope analyses
AGE = "mass-weighted age [Gyr]"


def real_ages():
    """Per-galaxy summary quantiles of the three DR3 window arms."""
    reference = pd.read_csv(DR3 / "window-194-fits.csv").query("release == 'dr3'")
    fits = pd.concat([reference, pd.read_csv(MASK / "window-194-mask-fits.csv")], ignore_index=True)
    return fits[fits.valid][["arm", "target", "z", "age_gyr_q16", "age_gyr_q50", "age_gyr_q84", "afe_q50"]]


def mock_ages():
    """Truth and recovered quantiles of every mock fit that passes validate_result."""
    rows = []
    for row in mocks.read_design():
        found = list((MOCK / "runs").glob(f'*/fits/mock_w/{row["object_id"]}-{row["target"]}'))
        if not found:
            continue
        try:
            validate_result(found[0])
        except Exception:
            continue
        truth = json.loads((MOCK / "truths" / f'{row["target"]}.json').read_text())
        with h5py.File(found[0] / "ceridwen_derived_outputs.h5") as stored:
            names = stored["summary/parameter"].asstr()[:]
            q = {k: dict(zip(names, stored[f"summary/{k}"][:])) for k in ("q16", "q50", "q84")}
        rows.append(dict(target=row["target"], shape=row["shape"], z=row["z"], true_age_gyr=truth["true_age_gyr"],
                         age_q16=float(q["q16"][AGE]), age_q50=float(q["q50"][AGE]), age_q84=float(q["q84"][AGE]),
                         afe_q50=float(q["q50"]["afe"])))
    return pd.DataFrame(rows)


def hubble(slope, z):
    """H = −1 / ((1 + z) dt/dz) in km/s/Mpc (Jimenez & Loeb 2002, eq. 2), as the window slope analyses."""
    import astropy.units as u

    return -(1 / u.Gyr).to_value(u.km / u.s / u.Mpc) / ((1 + z) * slope)


def table(mock):
    """Markdown rows: slope, H and median [α/Fe] per arm, the Planck18 line, and the mock truth and recovery."""
    slopes = pd.read_csv(MASK / "age-redshift-slopes.csv").query("group == 'all'").set_index("arm")
    span = lambda a, b, c: f"{a:.2f} ({b:.2f} to {c:.2f})"
    rows = []
    for arm, label in (("plain", "Plain"), ("cn_free", "C/N free"), ("mask", "Carbon mask")):
        s = slopes.loc[arm]
        rows.append((f"{label}, \\(N={s.galaxies}\\)", span(s.slope_gyr_per_z, s.bootstrap_q16, s.bootstrap_q84),
                     f"{s.H_kms_mpc:.0f} ({s.H_from_q16:.0f} to {s.H_from_q84:.0f})", f"{s.median_afe:+.2f}"))
    s = slopes.loc["plain"]
    rows.append(("Planck18", f"{s.planck18_line_slope:.2f}", f"{hubble(s.planck18_line_slope, s.z_median):.0f}", ""))
    z, z_med = mock.z.to_numpy(), float(mock.z.median())
    true, fit = mocks.line_fit(z, mock.true_age_gyr.to_numpy()), mocks.line_fit(z, mock.age_q50.to_numpy())
    rows.append((f"Mock truth, \\(N={len(mock)}\\)", f"{true['slope']:.2f}", f"{hubble(true['slope'], z_med):.0f}", f"{mocks.TRUE_AFE:+.2f}"))
    rows.append((f"Mock recovered, \\(N={len(mock)}\\)", span(fit["slope"], fit["q16"], fit["q84"]),
                 f"{hubble(fit['slope'], z_med):.0f} ({hubble(fit['q16'], z_med):.0f} to {hubble(fit['q84'], z_med):.0f})",
                 f"{mock.afe_q50.median():+.2f}"))
    return rows


# Figure style and layout: designer pick B (figure 1) and C (figure 2), 2026-11-14.
PAPER, INK, INK2, INK3 = "#fafaf8", "#1c2024", "#4b535b", "#7d858d"  # wiki --paper, --ink, --ink-2, --ink-3
ARMS = {"plain": ("Plain", "#2d5f9a"), "cn_free": ("C/N free", "#b5832a"), "mask": ("Carbon mask", "#a83c3c")}
SHAPES = {"tophat1": "Constant, 1 Gyr", "short": "Constant, 0.5 Gyr", "exp": "Exponential", "twoburst": "Two bursts"}
WIDTH = 7.6  # in; wiki figures display at most 760 px wide
DASH = (0, (4, 2.5))
AGE_LABEL = "Mass-weighted age (Gyr)"
REDSHIFT = "Redshift $z$"
SLOPE = "Age slope (Gyr per unit $z$)"
STYLE = {
    "font.family": "Charter", "font.size": 9.5,
    "mathtext.fontset": "custom", "mathtext.rm": "Charter", "mathtext.it": "Charter:italic",
    "mathtext.bf": "Charter:bold", "mathtext.fallback": "stix",
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
    "axes.edgecolor": INK3, "axes.linewidth": 0.7, "axes.labelcolor": INK2, "axes.labelsize": 10.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": INK3, "ytick.color": INK3, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5, "xtick.major.size": 3, "ytick.major.size": 3,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "lines.solid_capstyle": "round", "lines.dash_capstyle": "butt",
}


def _num(value):
    return f"{value:.2f}".replace("-", "−")


def _tint(colour, keep):
    """Colour mixed into the paper; keep = 1 is the colour itself."""
    return tuple(keep * c + (1 - keep) * p for c, p in zip(to_rgb(colour), to_rgb(PAPER)))


def _ages(ax, z, q16, q50, q84, colour, size=9):
    """Per-galaxy posterior median (dot) and 16-84% range (bar)."""
    ax.vlines(z, q16, q84, color=_tint(colour, 0.32), lw=0.7, zorder=1)
    ax.scatter(z, q50, s=size, color=_tint(colour, 0.75), lw=0, zorder=2)


def _fit_line(ax, zmin, zmax, slope, z0, y0, colour):
    x = np.array([zmin, zmax])
    ax.plot(x, y0 + slope * (x - z0), color=colour, lw=1.9,
            path_effects=[patheffects.withStroke(linewidth=4.5, foreground=PAPER)], zorder=4)


def _ref_line(ax, zmin, zmax, slope, z0, y0):
    """Ink dashed reference drawn over the fit."""
    x = np.array([zmin, zmax])
    ax.plot(x, y0 + slope * (x - z0), color=INK, lw=1.25, ls=DASH, zorder=5)


def _key(ax, rows, top=0.94, step=0.095, right=0.97):
    """Labels with a line swatch before each, flush with the panel's right edge. rows: (text, colour, dashed)."""
    texts = [ax.text(0, top - i * step, text, transform=ax.transAxes, ha="left", va="center", color=INK,
                     fontsize=9.5) for i, (text, _, _) in enumerate(rows)]
    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()
    inverse = ax.transAxes.inverted()
    widest = max(np.diff(inverse.transform(t.get_window_extent(renderer)), axis=0)[0, 0] for t in texts)
    gap = 0.009 / ax.get_position().width
    x0 = right - widest
    for t, (_, colour, dashed) in zip(texts, rows):
        t.set_x(x0)
        y = t.get_position()[1]
        ax.plot([x0 - 5 * gap, x0 - gap], [y, y], transform=ax.transAxes, color=colour,
                lw=1.25 if dashed else 1.9, ls=DASH if dashed else "-", clip_on=False)


def _slope_strip(ax, rows, reference, ref_label, xlim):
    """Dot and 16-84% whisker per row against a vertical ink dashed reference.
    rows: (label, colour, slope, q16, q84, filled); filled rows carry their number."""
    n = len(rows)
    ax.plot([reference, reference], [n - 0.4, -0.55], color=INK, lw=1.25, ls=DASH, zorder=1)
    ax.text(reference, -0.65, ref_label, ha="center", va="bottom", color=INK, fontsize=9.5)
    for i, (label, colour, mid, lo, hi, filled) in enumerate(rows):
        ax.plot([lo, hi], [i, i], color=colour, lw=2.2 if filled else 1.3, zorder=2)
        ax.scatter([mid], [i], s=46 if filled else 30, color=colour if filled else PAPER, edgecolor=colour,
                   lw=1.4, zorder=3)
        if filled:
            ax.text(hi + 0.012 * (xlim[1] - xlim[0]) * WIDTH / ax.figure.get_figwidth() / ax.get_position().width,
                    i, _num(mid), ha="left", va="center", color=INK, fontsize=9.5)
    ax.set_yticks(range(n), [r[0] for r in rows])
    ax.tick_params(axis="y", length=0, labelcolor=INK, labelsize=10)
    ax.set_ylim(n - 0.4, -0.95)
    ax.set_xlim(*xlim)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(SLOPE)


def age_redshift_figure(real):
    """Slope of each arm against Planck18, then one age panel per arm; the Planck18 slope pivots on the arm's mean."""
    fit = pd.read_csv(MASK / "age-redshift-slopes.csv").query("group == 'all'").set_index("arm")
    ref = fit.planck18_line_slope.iloc[0]
    with plt.rc_context(STYLE):
        fig = plt.figure(figsize=(WIDTH, 5.6), layout="constrained")
        fig.get_layout_engine().set(w_pad=0.15)  # margin left of the strip's row labels
        grid = fig.add_gridspec(2, 2)
        strip = fig.add_subplot(grid[0, 0])
        first = fig.add_subplot(grid[0, 1])
        axes = [first, fig.add_subplot(grid[1, 0], sharex=first, sharey=first),
                fig.add_subplot(grid[1, 1], sharex=first, sharey=first)]
        rows = [(name, colour, fit.slope_gyr_per_z[arm], fit.bootstrap_q16[arm], fit.bootstrap_q84[arm], True)
                for arm, (name, colour) in ARMS.items()]
        _slope_strip(strip, rows, ref, f"Planck18 {_num(ref)}", (-6.2, -3.0))
        for ax, (arm, (name, colour)) in zip(axes, ARMS.items()):
            g = real[real.arm == arm]
            assert np.isclose(mocks.line_fit(g.z.to_numpy(), g.age_gyr_q50.to_numpy())["slope"], fit.slope_gyr_per_z[arm])
            _ages(ax, g.z, g.age_gyr_q16, g.age_gyr_q50, g.age_gyr_q84, colour)
            z0, y0 = g.z.mean(), g.age_gyr_q50.mean()  # the least-squares line passes through the mean
            _fit_line(ax, g.z.min(), g.z.max(), fit.slope_gyr_per_z[arm], z0, y0, colour)
            _ref_line(ax, g.z.min(), g.z.max(), ref, z0, y0)
            ax.text(0.97, 0.95, name, transform=ax.transAxes, ha="right", va="top", color=INK, fontsize=10.5)
            ax.set_xlim(0.58, 1.02)
            ax.set_xticks([0.6, 0.7, 0.8, 0.9, 1.0])
            ax.set_ylim(0, 8.6)
            ax.set_yticks([0, 2, 4, 6, 8])
            ax.set_xlabel(REDSHIFT)
            ax.set_ylabel(AGE_LABEL)
        axes[2].set_ylabel("")
        _key(axes[0], [("Planck18 slope", INK, True)], top=0.07)
    return fig


def mock_figure(mock):
    """Recovered ages against the true-age line, beside the recovered slope for all mocks and per SFH shape."""
    colour = ARMS["plain"][1]
    z = mock.z.to_numpy()
    true, rec = mocks.line_fit(z, mock.true_age_gyr.to_numpy()), mocks.line_fit(z, mock.age_q50.to_numpy())
    with plt.rc_context(STYLE):
        fig, (ax, strip) = plt.subplots(1, 2, figsize=(WIDTH, 3.6), width_ratios=[1.6, 1], layout="constrained")
        _ages(ax, mock.z, mock.age_q16, mock.age_q50, mock.age_q84, colour, size=12)
        zmin, zmax = mock.z.min(), mock.z.max()
        _fit_line(ax, zmin, zmax, rec["slope"], mock.z.mean(), mock.age_q50.mean(), colour)
        _ref_line(ax, zmin, zmax, true["slope"], mock.z.mean(), mock.true_age_gyr.mean())
        span = zmax - zmin
        ax.set_xlim(zmin - 0.05 * span, zmax + 0.05 * span)
        ax.set_ylim(np.floor(min(mock.age_q16.min(), mock.true_age_gyr.min()) - 0.2), np.ceil(mock.age_q84.max() + 0.9))
        ax.set_ylabel(AGE_LABEL)
        ax.set_xlabel(REDSHIFT)
        _key(ax, [("Recovered", colour, False), ("True", INK, True)])
        rows = [("All mocks", colour, rec["slope"], rec["q16"], rec["q84"], True)]
        for shape, name in SHAPES.items():
            g = mock[mock["shape"] == shape]
            s = mocks.line_fit(g.z.to_numpy(), g.age_q50.to_numpy())
            rows.append((name, colour, s["slope"], s["q16"], s["q84"], False))
        ends = [v for r in rows for v in r[3:5]] + [true["slope"]]
        _slope_strip(strip, rows, true["slope"], f"True {_num(true['slope'])}",
                     (np.floor(min(ends) * 2) / 2 - 0.2, np.ceil(max(ends) * 2) / 2 + 0.6))
    return fig


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mock = mock_ages()
    for name, fig in (("age-redshift-dr3", age_redshift_figure(real_ages())), ("mock-chronometer", mock_figure(mock))):
        fig.savefig(OUT / f"{name}.png", dpi=200)
        plt.close(fig)
    print(f"{len(mock)} valid mock fits")
    for row in table(mock):
        print("| " + " | ".join([row[0], *(cell.replace("-", "−") for cell in row[1:])]) + " |")


if __name__ == "__main__":
    main()
