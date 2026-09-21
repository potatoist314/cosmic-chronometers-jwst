"""Consistent absorption-feature colours and one legend beside each figure.

Call ``mark_absorption_features`` on each wavelength panel, with
``show_labels=True`` on one panel, then ``spectral_tight_layout(fig)``.
The layout helper reserves a right-hand legend column without narrowing the
original figure. Feature windows come from the existing Ceridwen catalogue.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, FuncFormatter, MultipleLocator, NullLocator

from ceridwen.observation.absorption_features import feature_windows

MARKED_FEATURES = [
    ("CaK", "Ca K"),
    ("CaH", r"Ca H+H$\epsilon$"),
    ("HdA", r"H$\delta$"),
    ("G4300", "G"),
    ("HgA", r"H$\gamma$"),
    ("Fe4383", "Fe4383"),
    ("Hbeta", r"H$\beta$"),
    ("Mgb", r"Mg $b$"),
    ("Fe5270", "Fe5270"),
]
# Keep a feature's colour fixed even when other features are outside the axes.
FEATURE_COLORS = dict(zip(
    (name for name, _ in MARKED_FEATURES),
    (mpl.colormaps["tab10"](i) for i in (0, 1, 2, 3, 4, 5, 6, 8, 9)),
    strict=True,
))
FEATURE_XLABEL_PAD = mpl.rcParams["axes.labelpad"]
_LEGEND_GID = "absorption-feature-legend"
_WINDOW_PREFIX = "absorption-feature:"


def mark_absorption_features(
    ax, zred, *, show_labels=True, window_kms=1000.0, xlabel=None
):
    """Colour visible catalogue windows; list their names beside the figure.

    ``zred=0`` marks a rest-frame axis. ``show_labels=False`` colours an upper
    panel without requesting a legend. One legend covers all marked panels.
    Existing data legends and axis limits are preserved.
    """
    windows = feature_windows(
        [name for name, _ in MARKED_FEATURES], zred=zred, window_kms=window_kms
    )
    x_limits = ax.get_xlim()
    for (name, _), (lower, upper) in zip(MARKED_FEATURES, windows, strict=True):
        if upper < min(x_limits) or lower > max(x_limits):
            continue
        color = FEATURE_COLORS[name]
        patch = ax.axvspan(
            lower, upper, facecolor=color, alpha=0.10, linewidth=0, zorder=0.5
        )
        patch.set_gid(_WINDOW_PREFIX + name)
        for edge in (lower, upper):
            ax.axvline(edge, color=color, lw=0.7, linestyle=":", zorder=1)
    ax.set_xlim(x_limits)
    if xlabel is not None:
        ax.set_xlabel(xlabel, labelpad=FEATURE_XLABEL_PAD)
    figure = ax.figure
    existing = next((leg for leg in figure.legends if leg.get_gid() == _LEGEND_GID), None)
    if show_labels or existing is not None:
        visible = {
            patch.get_gid()[len(_WINDOW_PREFIX):]
            for axis in figure.axes for patch in axis.patches
            if (patch.get_gid() or "").startswith(_WINDOW_PREFIX)
        }
        if existing is not None:
            existing.remove()
        if visible:
            handles = [Line2D([], [], color=FEATURE_COLORS[name], lw=2, label=label)
                       for name, label in MARKED_FEATURES if name in visible]
            legend = figure.legend(handles=handles, loc="center right", frameon=False,
                                   fontsize=8, title="Absorption features", title_fontsize=8)
            legend.set_gid(_LEGEND_GID)


def mark_rest_wavelength_axis(
    ax, zred, *, label=r"rest-frame vacuum wavelength [$\mathrm{\AA}$]", title=None
):
    """Top x axis in rest-frame wavelength, lambda_rest = lambda_obs / (1 + z).

    The top axis is the bottom axis's twin: same tick size, same label form.
    The observed-frame ticks leave the top spine. With ``title`` the header is
    one row: title flush left, axis label flush right, on one baseline. Without
    it an existing centred title stays above the centred axis label. Call before
    ``spectral_tight_layout``.
    """
    top = ax.secondary_xaxis(
        "top", functions=(lambda obs: obs / (1 + zred), lambda rest: rest * (1 + zred))
    )
    ax.tick_params(axis="x", which="both", top=False)
    if title is None:
        top.set_xlabel(label)
        return top
    top.set_xlabel(label, loc="right")
    fig = ax.figure
    fig.draw_without_rendering()                       # places the top label
    renderer = fig.canvas.get_renderer()
    baseline = top.xaxis.label.get_position()[1]       # display px
    axes_top = ax.get_window_extent(renderer).y1
    pad = (baseline - axes_top) * 72 / fig.dpi
    ax.set_title(title, loc="left", y=1.0, pad=pad)
    fig.draw_without_rendering()
    title_box = ax.title.get_window_extent(renderer)
    label_box = top.xaxis.label.get_window_extent(renderer)
    if title_box.x1 > label_box.x0:
        # The row is too narrow for both: stack the title above the label.
        ax.set_title(title, loc="left", y=1.0, pad=pad + (label_box.height + 2) * 72 / fig.dpi)
    return top


def set_plain_log_ticks(axis, ticks):
    """Log axis with plain decimal tick labels (0.4, 1, 2), no minor ticks."""
    axis.set_major_locator(FixedLocator(list(ticks)))
    axis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    axis.set_minor_locator(NullLocator())


def spectral_tight_layout(fig=None, *, rect=(0, 0, 1, 1), **kwargs):
    """Apply tight layout, with a separate column for the feature legend.

    Figures without feature labels use normal tight layout. Repeated calls do
    not increase figure dimensions again. Existing top/bottom margins remain.
    """
    fig = plt.gcf() if fig is None else fig
    legend = next((leg for leg in fig.legends if leg.get_gid() == _LEGEND_GID), None)
    if legend is None:
        fig.tight_layout(rect=rect, **kwargs)
        return
    box = legend.get_window_extent(fig.canvas.get_renderer())
    column = box.width / fig.dpi + 0.35
    height = box.height / fig.dpi + 0.4
    if not hasattr(fig, "_absorption_base_size"):
        fig._absorption_base_size = tuple(fig.get_size_inches())
    width, original_height = fig._absorption_base_size
    fig.set_size_inches(width + column, max(original_height, height))
    right = min(rect[2], 1 - column / fig.get_figwidth())
    legend.set_bbox_to_anchor((1 - 0.05 / fig.get_figwidth(), (rect[1] + rect[3]) / 2))
    fig.tight_layout(rect=(rect[0], rect[1], right, rect[3]), **kwargs)


_PHOT_INK, _PHOT_MODEL, _PHOT_LEADER, _PHOT_RANGE = "#1f2a33", "#d62728", "#9aa3ab", "#9467bd"


def _spread_labels(positions, minimum, low, high):
    """Nearest positions to sorted ``positions`` with ``minimum`` spacing, inside [low, high]."""
    steps = minimum * np.arange(len(positions))
    blocks = []
    for value in positions - steps:
        blocks.append([value, 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            mean, count = blocks.pop()
            total = blocks[-1][1] + count
            blocks[-1] = [(blocks[-1][0] * blocks[-1][1] + mean * count) / total, total]
    spread = np.concatenate([[mean] * count for mean, count in blocks])
    spread = np.maximum.accumulate(np.maximum(spread, low)) + steps
    return np.minimum(spread, high - steps[::-1])


def _draw_label_rail(rail, wave, labels, spacing, fan):
    """Rotated band names on ``rail``, with leaders to the true wavelength on both edges."""
    fig = rail.figure
    low, high = np.log10(rail.get_xlim())
    width_in = rail.get_position().width * fig.get_figwidth()
    dex_per_in = (high - low) / width_in
    spots = 10 ** _spread_labels(
        np.log10(wave), spacing * dex_per_in, low + 0.08 * dex_per_in, high - 0.08 * dex_per_in
    )
    texts = [
        rail.text(spot, 1 - fan - 0.03, label, rotation=90, ha="center", va="top",
                  fontsize=7.5, color=_PHOT_INK)
        for spot, label in zip(spots, labels, strict=True)
    ]
    fig.draw_without_rendering()
    to_rail = rail.transData.inverted()
    for true, spot, text in zip(wave, spots, texts, strict=True):
        box = text.get_window_extent()
        bottom = to_rail.transform((0, box.y0))[1] - 0.025
        style = dict(color=_PHOT_LEADER, lw=0.55, solid_capstyle="butt", clip_on=False)
        rail.plot([true, spot, spot], [1, 1 - fan, 1 - fan - 0.005], **style)
        rail.plot([spot, spot, true], [bottom, fan, 0], **style)


def plot_photometry_fit(
    labels, wave_eff, flux, uncertainty, model_q16, model_q50, model_q84, *,
    redshift, data_label, spectral_range=None, continuum=None, mask=None,
):
    """Photometry fit with a pull panel; band names sit on a rail between the panels.

    Fluxes in microjansky, wavelengths in observed angstrom. ``spectral_range`` is the
    (min, max) of the fitted spectral pixels, ``continuum`` a (wavelength, flux) pair,
    ``mask`` False for a band outside the fit. Returns ``(fig, (ax_flux, ax_pull))``.
    """
    order = np.argsort(wave_eff)
    wave = np.asarray(wave_eff, dtype=float)[order] * 1e-4
    flux, sigma, q16, q50, q84 = (
        np.asarray(values, dtype=float)[order]
        for values in (flux, uncertainty, model_q16, model_q50, model_q84)
    )
    labels = [labels[index] for index in order]
    fitted = np.ones(len(wave), dtype=bool) if mask is None else np.asarray(mask, dtype=bool)[order]
    pull = (flux - q50) / sigma

    width, rail_in, right, top_in, bottom_in = 9.0, 0.95, 0.765, 0.62, 0.55
    height = top_in + 3.5 + rail_in + 1.45 + bottom_in
    fig = plt.figure(figsize=(width, height))
    grid = fig.add_gridspec(
        3, 1, height_ratios=[3.5, rail_in, 1.45], hspace=0,
        left=0.085, right=right, top=1 - top_in / height, bottom=bottom_in / height,
    )
    ax = fig.add_subplot(grid[0])
    rail = fig.add_subplot(grid[1], sharex=ax)
    ax_pull = fig.add_subplot(grid[2], sharex=ax)

    x_low, x_high = wave.min() * 0.84, wave.max() * 1.22
    floor = 0.6 * min(np.min(np.maximum(flux - sigma, 0.35 * flux)), q16.min())
    for panel in (ax, ax_pull):
        if spectral_range is not None:
            panel.axvspan(spectral_range[0] * 1e-4, spectral_range[1] * 1e-4,
                          facecolor=_PHOT_RANGE, alpha=0.10, lw=0, zorder=0)
        panel.tick_params(direction="in", which="both", right=True, labelsize=9)

    if continuum is not None:
        ax.plot(np.asarray(continuum[0]) * 1e-4, continuum[1], color="0.6", lw=0.8, zorder=1)
    ax.errorbar(
        wave, q50, yerr=[q50 - q16, q84 - q50], fmt="s", ms=7.5, mfc="none", mec=_PHOT_MODEL,
        mew=1.1, ecolor=_PHOT_MODEL, elinewidth=1.0, zorder=2,
    )
    lower = np.minimum(sigma, flux - floor * 1.02)
    for pick, face in ((fitted, _PHOT_INK), (~fitted, "white")):
        if pick.any():
            ax.errorbar(wave[pick], flux[pick], yerr=[lower[pick], sigma[pick]], fmt="o", ms=4.2,
                        color=_PHOT_INK, mfc=face, elinewidth=0.9, zorder=3)
            ax_pull.plot(wave[pick], pull[pick], "o", ms=4.5, color=_PHOT_INK, mfc=face, zorder=3)

    ax.set(xscale="log", yscale="log", xlim=(x_low, x_high), ylim=(floor, flux.max() * 2.2))
    ax.set_ylabel(r"$F_\nu$ [$\mu$Jy]", fontsize=10)
    set_plain_log_ticks(ax.yaxis, [tick for tick in (0.01, 0.1, 1, 10, 100, 1000) if tick > floor])
    ax.tick_params(which="both", bottom=False, labelbottom=False)
    ax_pull.axhline(0, color="0.5", lw=0.8, zorder=1)
    ax_pull.set_ylim(min(-3.5, pull.min() * 1.18), max(3.5, pull.max() * 1.3))
    ax_pull.yaxis.set_major_locator(MultipleLocator(3))
    ax_pull.set_xlabel(r"observed vacuum wavelength [$\mu$m]", fontsize=10)
    ax_pull.set_ylabel(r"$(F_\mathrm{obs}-F_\mathrm{model})\,/\,\sigma$", fontsize=10)
    ax_pull.tick_params(which="both", top=False)
    set_plain_log_ticks(
        ax_pull.xaxis, [tick for tick in (0.1, 0.2, 0.4, 0.6, 1, 2, 4, 8) if x_low < tick < x_high]
    )
    top = mark_rest_wavelength_axis(ax, redshift, label=r"rest-frame vacuum wavelength [$\mu$m]")
    set_plain_log_ticks(
        top.xaxis,
        [tick for tick in (0.1, 0.15, 0.25, 0.4, 0.6, 1, 1.5, 2.5, 4)
         if x_low < tick * (1 + redshift) < x_high],
    )
    top.tick_params(direction="in", labelsize=9)
    top.xaxis.label.set_fontsize(10)

    rail.set(ylim=(0, 1))
    rail.axis("off")
    _draw_label_rail(rail, wave, labels, spacing=0.142, fan=0.24 / rail_in)

    handles = [
        Line2D([], [], marker="o", ms=4.2, color=_PHOT_INK, lw=0.9,
               label=f"observed total flux,\n{data_label}"),
        Line2D([], [], marker="s", ms=7.5, mfc="none", mec=_PHOT_MODEL, mew=1.1,
               color=_PHOT_MODEL, lw=1.0, label="Ceridwen median,\n16–84% range"),
    ]
    if not fitted.all():
        handles.insert(1, Line2D([], [], marker="o", ms=4.2, color=_PHOT_INK, mfc="white", lw=0.9,
                                 label="band outside the fit"))
    if continuum is not None:
        handles.append(Line2D([], [], color="0.6", lw=0.8, label="median continuum"))
    if spectral_range is not None:
        handles.append(Patch(facecolor=_PHOT_RANGE, alpha=0.18, lw=0, label="LEGA-C spectral range"))
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(right + 0.012, 1 - top_in / height),
               frameon=False, fontsize=8.5, handlelength=1.4, borderaxespad=0, labelspacing=0.9)
    return fig, (ax, ax_pull)


__all__ = ["FEATURE_XLABEL_PAD", "FEATURE_COLORS", "MARKED_FEATURES",
           "mark_absorption_features", "mark_rest_wavelength_axis", "plot_photometry_fit",
           "set_plain_log_ticks", "spectral_tight_layout"]
