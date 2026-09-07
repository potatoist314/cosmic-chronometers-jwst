"""Shared absorption-feature marking used by every wavelength-axis figure."""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest
from ceridwen.observation.absorption_features import feature_windows

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from spectral_figures import (  # noqa: E402
    FEATURE_XLABEL_PAD,
    MARKED_FEATURES,
    mark_absorption_features,
)

FEATURE_NAMES = [name for name, _ in MARKED_FEATURES]


def shaded_windows(ax):
    """Data-space (lower, upper) of every axvspan drawn on ``ax``, in draw order."""
    return [
        (float(patch.get_x()), float(patch.get_x() + patch.get_width()))
        for patch in ax.patches
    ]


def text_rows(ax):
    """Rendered name boxes grouped by row, keyed on the row's baseline y."""
    renderer = ax.figure.canvas.get_renderer()
    rows = {}
    for text in ax.texts:
        box = text.get_window_extent(renderer)
        rows.setdefault(round(box.y1, 1), []).append((box, text.get_text()))
    return rows


def make_axis(width=12.0, xlim=(6000.0, 8800.0)):
    fig, ax = plt.subplots(figsize=(width, 4.0))
    ax.set_xlim(*xlim)
    return fig, ax


def test_catalogue_covers_the_nine_marked_features():
    assert FEATURE_NAMES == [
        "CaK", "CaH", "HdA", "G4300", "HgA", "Fe4383", "Hbeta", "Mgb", "Fe5270"
    ]


@pytest.mark.parametrize("zred", [0.0, 0.6, 0.8])
def test_window_edges_follow_the_redshifted_catalogue(zred):
    fig, ax = make_axis(xlim=(3000.0, 12000.0))
    mark_absorption_features(ax, zred, show_labels=False)

    expected = feature_windows(FEATURE_NAMES, zred=zred)
    np.testing.assert_allclose(shaded_windows(ax), expected)
    plt.close(fig)


def test_window_kms_widens_the_line_windows():
    fig, ax = make_axis(xlim=(3000.0, 12000.0))
    mark_absorption_features(ax, 0.0, show_labels=False, window_kms=2000.0)

    expected = feature_windows(FEATURE_NAMES, zred=0.0, window_kms=2000.0)
    np.testing.assert_allclose(shaded_windows(ax), expected)
    # CaK and CaH are line centres, so only they widen.
    narrow = feature_windows(FEATURE_NAMES, zred=0.0, window_kms=1000.0)
    widths = expected[:, 1] - expected[:, 0]
    assert (widths[:2] > 1.9 * (narrow[:, 1] - narrow[:, 0])[:2]).all()
    plt.close(fig)


def test_labels_appear_only_on_the_panel_that_asked_for_them():
    fig, axes = plt.subplots(2, 1, figsize=(12.0, 6.0), sharex=True)
    for ax in axes:
        ax.set_xlim(6000.0, 8800.0)
    mark_absorption_features(axes[0], 0.6, show_labels=False)
    mark_absorption_features(axes[1], 0.6)

    fig.canvas.draw()

    assert len(axes[0].texts) == 0
    assert len(axes[1].texts) == len(MARKED_FEATURES)
    assert [text.get_text() for text in axes[1].texts] == [
        label for _, label in MARKED_FEATURES
    ]
    renderer = fig.canvas.get_renderer()
    axis_bottom = axes[1].get_window_extent().y0
    for text in axes[1].texts:
        assert text.get_window_extent(renderer).y1 < axis_bottom
        assert text.get_clip_on() is False
        assert text.get_transform() is not axes[1].transData
    assert len(shaded_windows(axes[0])) == len(shaded_windows(axes[1]))
    plt.close(fig)


def test_names_drop_a_row_only_when_the_text_would_overlap():
    fig, ax = make_axis(width=12.0)
    mark_absorption_features(ax, 0.6)
    fig.canvas.draw()

    rows = text_rows(ax)
    second_row = min(rows)
    assert len(rows) == 2
    assert [text for _, text in rows[second_row]] == [r"Ca H+H$\epsilon$"]
    plt.close(fig)

    fig, ax = make_axis(width=24.0)
    mark_absorption_features(ax, 0.6)
    fig.canvas.draw()

    assert len(text_rows(ax)) == 1
    plt.close(fig)


def test_narrow_panels_use_as_many_rows_as_the_names_need():
    # A stacked-pull panel is a third of a figure wide, so two rows are not enough.
    fig, ax = make_axis(width=3.5, xlim=(3200.0, 5600.0))
    mark_absorption_features(ax, 0.0, xlabel=r"Rest wavelength [$\mathrm{\AA}$]")
    fig.canvas.draw()

    rows = text_rows(ax)
    assert len(rows) >= 3
    for row in rows.values():
        row.sort(key=lambda pair: pair[0].x0)
        for (left, _), (right, _) in zip(row, row[1:]):
            assert right.x0 > left.x1
    assert ax.xaxis.labelpad > FEATURE_XLABEL_PAD
    plt.close(fig)


def test_windows_outside_the_axis_are_skipped_and_limits_restored():
    fig, ax = make_axis(xlim=(3000.0, 3500.0))
    mark_absorption_features(ax, 0.0)

    assert len(ax.patches) == 0
    assert len(ax.texts) == 0
    assert ax.get_xlim() == (3000.0, 3500.0)
    plt.close(fig)


def test_partly_visible_windows_are_drawn_whole():
    fig, ax = make_axis(xlim=(6000.0, 8800.0))
    mark_absorption_features(ax, 0.7, show_labels=False)

    windows = feature_windows(FEATURE_NAMES, zred=0.7)
    visible = [
        (float(lower), float(upper))
        for lower, upper in windows
        if upper >= 6000.0 and lower <= 8800.0
    ]
    np.testing.assert_allclose(shaded_windows(ax), visible)
    assert ax.get_xlim() == (6000.0, 8800.0)
    plt.close(fig)


def test_xlabel_argument_leaves_room_for_the_names():
    fig, ax = make_axis()
    mark_absorption_features(ax, 0.6, xlabel="observed vacuum wavelength [angstrom]")
    fig.canvas.draw()

    assert ax.get_xlabel() == "observed vacuum wavelength [angstrom]"
    assert ax.xaxis.labelpad >= FEATURE_XLABEL_PAD
    # The label clears the lowest name whatever the panel height.
    renderer = fig.canvas.get_renderer()
    label_top = ax.xaxis.label.get_window_extent(renderer).y1
    assert label_top < min(
        text.get_window_extent(renderer).y0 for text in ax.texts
    )
    plt.close(fig)


def test_short_panels_still_put_the_label_below_the_names():
    # Rows are placed as a fraction of the axis, so a short axis needs more pad.
    fig, axes = plt.subplots(3, 1, figsize=(6.0, 9.0))
    for ax in axes:
        ax.set_xlim(6000.0, 8800.0)
    mark_absorption_features(axes[2], 0.6, xlabel="observed [angstrom]")
    fig.canvas.draw()

    renderer = fig.canvas.get_renderer()
    label_top = axes[2].xaxis.label.get_window_extent(renderer).y1
    assert label_top < min(
        text.get_window_extent(renderer).y0 for text in axes[2].texts
    )
    plt.close(fig)

    fig, ax = make_axis()
    ax.set_xlabel("kept by the caller")
    mark_absorption_features(ax, 0.6)

    assert ax.get_xlabel() == "kept by the caller"
    plt.close(fig)


def test_log_axes_keep_their_scale_and_limits():
    fig, ax = make_axis(xlim=(3000.0, 90000.0))
    ax.set_xscale("log")
    mark_absorption_features(ax, 0.7, show_labels=False)

    assert ax.get_xscale() == "log"
    assert ax.get_xlim() == (3000.0, 90000.0)
    assert len(shaded_windows(ax)) == len(MARKED_FEATURES)
    plt.close(fig)
