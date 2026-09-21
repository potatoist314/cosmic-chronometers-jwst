#!/usr/bin/env python3
"""Plot the fit-input photometry of M1_210210 from each COSMOS catalogue.

Top panel: rest-frame UV on a linear flux axis, with the catalogue error and the
error after the 5% floor. Below: the full SED on log axes, then the flux ratio
and the error ratio to COSMOS2015 per filter, with the sample medians.

Inputs:  results/cosmos-photometry-comparison/bands.csv and ratios.csv
         (from scripts/compare_cosmos_photometry.py)
Output:  wiki/analyses/cosmos-photometry-comparison/cosmos-photometry-M1_210210.png

Usage: ``ceridwen/.venv/bin/python scripts/plot_cosmos_photometry_comparison.py``
(``scripts/spectral_figures.py`` imports ceridwen, which the root uv env lacks.)
"""
from pathlib import Path
import sys

import matplotlib as mpl
import numpy as np
import pandas as pd

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import ScaledTranslation

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
# The import applies FIT_FIGURE_RCPARAMS, the style of the fit-notebook figures.
from spectral_figures import mark_rest_wavelength_axis, set_plain_log_ticks  # noqa: E402

OUT = ROOT / "wiki" / "analyses" / "cosmos-photometry-comparison"
DATA = ROOT / "results" / "cosmos-photometry-comparison"
GALAXY, ZRED, FLOOR = "M1_210210", 0.6542, 0.05

# tab:red is the model and tab:purple the LEGA-C range in the fit figures.
COLOR = {"cosmos2015": "tab:blue", "classic": "tab:orange", "cosmos2025": "tab:green"}
GREY, LABEL_PT = "0.6", mpl.rcParams["font.size"] - 1.5
NAME = {"cosmos2015": "COSMOS2015 (present fit)", "classic": "COSMOS2020 Classic",
        "cosmos2025": "COSMOS2025"}
ORDER = ["cosmos2015", "classic", "cosmos2025"]
SHIFT_PT = {"cosmos2015": -4.5, "classic": 0.0, "cosmos2025": 4.5}   # catalogue offset in x

FIT = ["u*", "B", "V", "r+", "i+", "z++", "Y", "J", "H", "Ks", "ch1", "ch2"]
SPACE = ["F814W", "F115W", "F150W", "F277W", "F444W"]
UV_EDGE = 0.3 * (1 + ZRED)            # rest-frame 0.3 um, observed um

TEX = {"u*": r"$u^{*}$", "B": r"$B$", "V": r"$V$", "r+": r"$r^{+}$", "i+": r"$i^{+}$",
       "z++": r"$z^{++}$", "Y": r"$Y$", "J": r"$J$", "H": r"$H$", "Ks": r"$K_s$",
       "u": r"$u$", "g": r"$g$", "r": r"$r$", "i": r"$i$", "z": r"$z$", "y": r"$y$"}


def load():
    bands = pd.read_csv(DATA / "bands.csv")
    bands = bands[(bands.spect_id == GALAXY) & bands.total_flux_ujy.notna()].copy()
    bands["um"] = bands.wavelength_angstrom / 1e4
    bands["floored"] = np.hypot(bands.total_error_ujy, FLOOR * bands.total_flux_ujy)
    ratios = pd.read_csv(DATA / "ratios.csv")
    ratios = ratios[ratios.catalogue.isin(["classic", "cosmos2025"])].copy()
    ratios["um"] = ratios.wavelength_angstrom / 1e4
    sample = (ratios.groupby(["catalogue", "band", "um"]).flux_ratio
              .quantile([0.16, 0.5, 0.84]).unstack().reset_index())
    n = ratios.dropna(subset=["flux_ratio"]).groupby("catalogue").spect_id.nunique()
    galaxy = ratios[(ratios.spect_id == GALAXY) & ratios.flux_ratio.notna()]
    return bands, galaxy, sample, n


def axes_in(fig, left, bottom, width, height):
    w, h = fig.get_size_inches()
    return fig.add_axes([left / w, bottom / h, width / w, height / h])


def shifted(ax, cat):
    """Data transform moved sideways by the catalogue's offset in points."""
    return ax.transData + ScaledTranslation(SHIFT_PT[cat] / 72, 0, ax.figure.dpi_scale_trans)


def draw_flux(ax, bands, errors):
    for cat in ORDER:
        trans = shifted(ax, cat)
        for _, row in bands[bands.catalogue == cat].iterrows():
            if errors:
                for err, lw in ((row.floored, 0.8), (row.total_error_ujy, 2.4)):
                    ax.errorbar(row.um, row.total_flux_ujy, yerr=err, fmt="none",
                                ecolor=COLOR[cat], elinewidth=lw, capsize=0,
                                zorder=3 + ORDER.index(cat), transform=trans)
            ax.plot(row.um, row.total_flux_ujy, "o", color=COLOR[cat],
                    zorder=3.5 + ORDER.index(cat), transform=trans)


def label_bands(ax, bands, names, *, side, extra=None, anchor=None):
    """One label per band, above the highest or below the lowest mark.

    ``extra`` moves a label by (dx, dy) points and joins it to its marks with a
    thin leader; ``anchor`` moves the leader's foot sideways onto the marks.
    """
    extra, anchor = extra or {}, anchor or {}
    for band in names:
        rows = bands[bands.band == band]
        if rows.empty:
            continue
        up = side(band) > 0
        hi = (rows.total_flux_ujy + rows.floored).max()
        lo = (rows.total_flux_ujy - rows.floored).min()
        dx, dy = extra.get(band, (0, 0))
        foot = ax.transData + ScaledTranslation(anchor.get(band, 0) / 72, 0,
                                                ax.figure.dpi_scale_trans)
        leader = (dict(arrowstyle="-", lw=0.6, color=GREY, shrinkA=1.5, shrinkB=4.5)
                  if band in extra else None)
        ax.annotate(TEX.get(band, band), (rows.um.iloc[0], hi if up else lo), xycoords=foot,
                    xytext=(dx, (6 + dy) if up else -(6 + dy)), textcoords="offset points",
                    ha="center", va="bottom" if up else "top", arrowprops=leader,
                    fontsize=LABEL_PT, zorder=8)


def draw_ratio(ax, galaxy, column, sample=None):
    ax.axhline(1, color="0.5", lw=0.8, zorder=1)
    for cat in ("classic", "cosmos2025"):
        trans = shifted(ax, cat)
        if sample is not None:
            rows = sample[sample.catalogue == cat]
            ax.vlines(rows.um, rows[0.16], rows[0.84], color=COLOR[cat], lw=3, alpha=0.25,
                      zorder=2, capstyle="butt", transform=trans)
            ax.plot(rows.um, rows[0.5], "_", ms=6, mew=1.3, color=COLOR[cat], alpha=0.8,
                    zorder=2.5, transform=trans)
        rows = galaxy[galaxy.catalogue == cat]
        ax.plot(rows.um, rows[column], "o", color=COLOR[cat], zorder=4, transform=trans)


def style_x(ax, lo, hi, ticks, *, labels=True):
    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    set_plain_log_ticks(ax.xaxis, [t for t in ticks if lo <= t <= hi])
    if not labels:
        ax.tick_params(axis="x", labelbottom=False)


def rest_axis(ax, ticks, label):
    top = mark_rest_wavelength_axis(ax, ZRED, label=label)
    lo, hi = (v / (1 + ZRED) for v in ax.get_xlim())
    set_plain_log_ticks(top.xaxis, [t for t in ticks if lo <= t <= hi])
    return top


def legend_handles(*, sample_n=None):
    gap = Line2D([], [], ls="none")
    catalogues = [(Line2D([], [], ls="none", marker="o", color=COLOR[c]), NAME[c]) for c in ORDER]
    catalogues.append((gap, "COSMOS2020 Farmer: no photometry"))
    errors = [(Line2D([], [], color="0.35", lw=2.4), r"catalogue error $\sigma$"),
              (Line2D([], [], color="0.35", lw=0.8), r"$\sqrt{\sigma^2 + (0.05\,F_\nu)^2}$"),
              (Patch(fc=GREY, alpha=0.2, lw=0), r"$\pm 5\%$ error floor")]
    if sample_n is not None:
        errors.append((Line2D([], [], color=COLOR["classic"], lw=3, alpha=0.35,
                              marker="_", ms=6, mew=1.3, mec=COLOR["classic"]),
                       "sample median, 16–84%\n"
                       rf"($N = {sample_n['classic']}$, ${sample_n['cosmos2025']}$)"))
    return catalogues, errors


OBS_TICKS = [0.25, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 3, 4, 5]
REST_TICKS = [0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 1, 1.5, 2, 3]
OBS_LABEL = r"observed vacuum wavelength [$\mu$m]"
REST_LABEL = r"rest-frame vacuum wavelength [$\mu$m]"
FLUX_LABEL = r"$F_\nu$ [$\mu$Jy]"


def plot(bands, galaxy, sample, n):
    fig = plt.figure(figsize=(8, 9.25))
    left, width = 0.72, 7.1
    ax_err = axes_in(fig, left, 0.55, width, 1.0)
    ax_rat = axes_in(fig, left, 1.67, width, 1.3)
    ax_all = axes_in(fig, left, 3.09, width, 1.9)
    ax_uv = axes_in(fig, left, 6.0, width, 2.7)

    uv = bands[bands.um < UV_EDGE + 0.02]
    draw_flux(ax_uv, uv, errors=True)
    style_x(ax_uv, 0.22, 0.51, OBS_TICKS + [0.35, 0.45])
    ax_uv.set_ylim(-0.12, 3.25)
    ax_uv.axhline(0, color="0.5", lw=0.8, zorder=1)
    ax_uv.set_ylabel(FLUX_LABEL)
    ax_uv.set_xlabel(OBS_LABEL)
    rest_axis(ax_uv, REST_TICKS + [0.14, 0.16, 0.18, 0.22, 0.28], REST_LABEL)
    label_bands(ax_uv, uv, ["NUV", "u", "u*", "IB427", "B", "IB464"], side=lambda b: 1)
    g = uv[uv.band.isin(["g", "IA484"])]
    ax_uv.annotate(r"$g$, IA484", (g.um.iloc[0], (g.total_flux_ujy + g.floored).max()),
                   xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                   fontsize=LABEL_PT)

    draw_flux(ax_all, bands, errors=False)
    ax_all.set_yscale("log")
    ax_all.set_ylim(0.025, 900)
    set_plain_log_ticks(ax_all.yaxis, [0.1, 1, 10, 100])
    ax_all.set_ylabel(FLUX_LABEL)
    ax_all.axvspan(0.22, 0.51, color=GREY, alpha=0.2, lw=0, zorder=0)
    added = [b for b in bands.band.unique() if b not in FIT and bands[bands.band == b].um.iloc[0] > 0.51]
    # Foot of each leader sits on the band's own marks (catalogue offsets in SHIFT_PT).
    anchor = {"i+": -2.25, "z++": -2.25, "i": 2.25, "z": 2.25, "y": 2.25,
              **{b: SHIFT_PT["cosmos2025"] for b in SPACE}}
    label_bands(ax_all, bands, FIT, side=lambda b: 1, anchor=anchor,
                extra={"i+": (-5, 7), "z++": (-3, 14), "Y": (5, 7)})
    label_bands(ax_all, bands, added, side=lambda b: -1, anchor=anchor,
                extra={"i": (-6, 7), "z": (2, 7), "y": (2, 7),
                       "F814W": (0, 20), "F115W": (0, 20)})

    draw_ratio(ax_rat, galaxy, "flux_ratio", sample)
    ax_rat.axhspan(1 - FLOOR, 1 + FLOOR, color=GREY, alpha=0.2, lw=0, zorder=0)
    ax_rat.set_ylim(0.5, 1.2)
    ax_rat.set_yticks([0.6, 0.8, 1.0])
    ax_rat.set_ylabel(r"$F_\nu\,/\,F_{\nu,\,2015}$")

    draw_ratio(ax_err, galaxy, "error_ratio")
    ax_err.set_yscale("log")
    ax_err.set_ylim(0.15, 3)
    set_plain_log_ticks(ax_err.yaxis, [0.2, 0.5, 1, 2])
    ax_err.set_ylabel(r"$\sigma\,/\,\sigma_{2015}$")
    ax_err.set_xlabel(OBS_LABEL)

    for ax in (ax_all, ax_rat, ax_err):
        style_x(ax, 0.2, 5.4, OBS_TICKS, labels=ax is ax_err)
    rest_axis(ax_all, [0.15] + REST_TICKS, REST_LABEL)

    catalogues, errors = legend_handles(sample_n=n)
    entries = catalogues + errors
    ax_uv.legend([h for h, _ in entries], [t for _, t in entries], loc="upper left", frameon=False,
                 title=rf"{GALAXY}, $z = {ZRED}$", alignment="left")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"cosmos-photometry-{GALAXY}.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    plot(*load())
