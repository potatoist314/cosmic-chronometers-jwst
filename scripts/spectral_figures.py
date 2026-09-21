"""Consistent absorption-feature colours and one legend beside each figure.

Call ``mark_absorption_features`` on each wavelength panel, with
``show_labels=True`` on one panel, then ``spectral_tight_layout(fig)``.
The layout helper reserves a right-hand legend column without narrowing the
original figure. Feature windows come from the existing Ceridwen catalogue.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

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


__all__ = ["FEATURE_XLABEL_PAD", "FEATURE_COLORS", "MARKED_FEATURES",
           "mark_absorption_features", "mark_rest_wavelength_axis", "set_plain_log_ticks",
           "spectral_tight_layout"]
