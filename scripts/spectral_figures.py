"""Shared absorption-feature marking for every figure with a wavelength axis.

Production labelling standard: grey Lick/IDS windows with dotted edges on
every wavelength panel, and the feature names in one horizontal row hanging
below the bottom panel's x axis, outside the plotting area.  A name drops to
the next line only when its rendered text would overlap the name to its left,
so a wide panel keeps one row and a narrow one grows as many as it needs.

Import it with the project's shared-module pattern::

    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
    from spectral_figures import mark_absorption_features

Multi-panel ``sharex`` figures call it with ``show_labels=False`` on the upper
panels and ``show_labels=True`` on the bottom panel only.
"""

from __future__ import annotations

from matplotlib.transforms import offset_copy

from ceridwen.observation.absorption_features import feature_windows

# Major stellar absorption features (Lick/IDS names in ceridwen's catalogue);
# bands span the Lick bandpass, lines span +-window_kms around the centre.
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
# Fewest points of x-label padding; more when the name rows need it.
FEATURE_XLABEL_PAD = 30
# Points below the axis for the first name row, and between rows.  Points, not
# axes fractions: a fraction moves with the panel height, which tight_layout
# then changes again in response to the label pad measured from it.
ROW_ONE_PT, ROW_SPACING_PT = 22.0, 9.0


def mark_absorption_features(
    ax, zred, *, show_labels=True, window_kms=1000.0, xlabel=None
):
    """Shade the Lick windows of MARKED_FEATURES on ax; names below the axis.

    ``zred`` redshifts the rest-frame catalogue onto the axis; a rest-frame
    axis passes ``zred=0.0``.  ``xlabel`` sets the axis title with enough pad
    to clear the names; a caller that keeps its own label adds the pad itself.
    """
    windows = feature_windows(
        [name for name, _ in MARKED_FEATURES], zred=zred, window_kms=window_kms
    )
    x_limits = ax.get_xlim()
    labels = []
    for (_, label), (lower, upper) in zip(MARKED_FEATURES, windows, strict=True):
        if upper < x_limits[0] or lower > x_limits[1]:
            continue
        ax.axvspan(
            lower, upper, facecolor="0.2", alpha=0.10, linewidth=0, zorder=0.5
        )
        for edge in (lower, upper):
            ax.axvline(edge, color="0.3", lw=0.6, linestyle=":", zorder=1)
        if show_labels:
            labels.append(
                ax.text(
                    0.5 * (lower + upper),
                    0.0,
                    label,
                    color="0.2",
                    fontsize=7,
                    ha="center",
                    va="top",
                    transform=_row_transform(ax, 0),
                    clip_on=False,
                )
            )
    ax.set_xlim(x_limits)
    # One row below the axis; a name drops to the first row it fits on, so a
    # narrow panel grows a third and fourth row instead of overlapping names.
    renderer = ax.figure.canvas.get_renderer()
    row_right_edge = []
    for text in labels:
        box = text.get_window_extent(renderer)
        row = next(
            (n for n, edge in enumerate(row_right_edge) if box.x0 > edge + 3),
            len(row_right_edge),
        )
        if row == len(row_right_edge):
            row_right_edge.append(box.x1)
        else:
            row_right_edge[row] = box.x1
        text.set_transform(_row_transform(ax, row))
    if xlabel is not None:
        ax.set_xlabel(
            xlabel, labelpad=_label_pad(ax, labels, len(row_right_edge), renderer)
        )


def _row_transform(ax, row):
    """Axis x in data units, y a fixed number of points below the axis."""
    return offset_copy(
        ax.get_xaxis_transform(),
        fig=ax.figure,
        units="points",
        y=-(ROW_ONE_PT + ROW_SPACING_PT * row),
    )


def _label_pad(ax, labels, n_rows, renderer):
    """Points of x-label pad that clear the name rows on this axis.

    Matplotlib measures ``labelpad`` down from the tick labels, so subtract
    how far the tick labels already hang below the axis.
    """
    if not labels:
        return FEATURE_XLABEL_PAD
    scale = 72.0 / ax.figure.dpi
    ticks = [text.get_window_extent(renderer) for text in ax.get_xticklabels()]
    axis_bottom = ax.get_window_extent().y0
    tick_drop = scale * (axis_bottom - min(box.y0 for box in ticks)) if ticks else 0.0
    name_height = scale * max(
        box.y1 - box.y0
        for box in (text.get_window_extent(renderer) for text in labels)
    )
    lowest = ROW_ONE_PT + ROW_SPACING_PT * (n_rows - 1) + name_height
    return max(FEATURE_XLABEL_PAD, lowest - tick_drop + 4.0)


__all__ = ["FEATURE_XLABEL_PAD", "MARKED_FEATURES", "mark_absorption_features"]
