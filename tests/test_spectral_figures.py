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
    FEATURE_COLORS,
    spectral_tight_layout,
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


def test_colours_are_unique_and_do_not_depend_on_visible_features():
    assert len(set(FEATURE_COLORS.values())) == len(MARKED_FEATURES)
    fig, ax = make_axis(xlim=(4800, 5000))
    mark_absorption_features(ax, 0)
    np.testing.assert_allclose(ax.lines[0].get_color(), FEATURE_COLORS["Hbeta"])
    assert [t.get_text() for t in fig.legends[0].get_texts()] == [r"H$\beta$"]
    assert not ax.texts
    plt.close(fig)


def test_one_legend_covers_all_panels_without_replacing_data_legend():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot([4000, 4500], [1, 2], label="Observed")
    data_legend = axes[0].legend()
    axes[0].set_xlim(3900, 4200)
    axes[1].set_xlim(4800, 5400)
    mark_absorption_features(axes[0], 0)
    mark_absorption_features(axes[1], 0)
    spectral_tight_layout(fig)
    assert len(fig.legends) == 1
    assert axes[0].get_legend() is data_legend
    assert not axes[0].texts and not axes[1].texts
    assert [t.get_text() for t in fig.legends[0].get_texts()] == [
        label for name, label in MARKED_FEATURES
        if name in {"CaK", "CaH", "HdA", "Hbeta", "Mgb", "Fe5270"}
    ]
    plt.close(fig)


def test_unlabelled_panels_are_coloured_without_requesting_a_legend():
    fig, ax = make_axis()
    mark_absorption_features(ax, 0.6, show_labels=False)
    assert not fig.legends and not ax.texts
    assert len(ax.patches) == len(MARKED_FEATURES)
    for patch, (name, _) in zip(ax.patches, MARKED_FEATURES, strict=True):
        np.testing.assert_allclose(patch.get_facecolor()[:3], FEATURE_COLORS[name][:3])
    plt.close(fig)


@pytest.mark.parametrize("width,nrows", [(3.5, 1), (10, 2), (9, 5)])
def test_side_legend_clears_axes_and_is_inside_export(width, nrows):
    fig, axes = plt.subplots(nrows, 1, figsize=(width, max(4, nrows * 2)), squeeze=False)
    for ax in axes.flat:
        ax.set_xlim(3200, 5600)
        mark_absorption_features(ax, 0, show_labels=ax is axes[-1, 0], xlabel="Wavelength")
    spectral_tight_layout(fig)
    fig.canvas.draw()
    size = fig.get_size_inches().copy()
    spectral_tight_layout(fig)
    np.testing.assert_allclose(fig.get_size_inches(), size)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    box = fig.legends[0].get_window_extent(renderer)
    assert box.x1 <= fig.bbox.x1 and box.y0 >= 0 and box.y1 <= fig.bbox.y1
    for ax in axes.flat:
        assert ax.get_tightbbox(renderer).x1 < box.x0
        assert ax.xaxis.labelpad == FEATURE_XLABEL_PAD
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


def test_xlabel_uses_normal_padding_and_existing_title_is_preserved():
    fig, ax = make_axis()
    mark_absorption_features(ax, 0.6, xlabel="Observed wavelength")
    assert ax.get_xlabel() == "Observed wavelength"
    assert ax.xaxis.labelpad == FEATURE_XLABEL_PAD
    mark_absorption_features(ax, 0.6, show_labels=False)
    assert ax.get_xlabel() == "Observed wavelength"
    plt.close(fig)


def test_log_axes_keep_their_scale_and_limits():
    fig, ax = make_axis(xlim=(3000.0, 90000.0))
    ax.set_xscale("log")
    mark_absorption_features(ax, 0.7, show_labels=False)

    assert ax.get_xscale() == "log"
    assert ax.get_xlim() == (3000.0, 90000.0)
    assert len(shaded_windows(ax)) == len(MARKED_FEATURES)
    plt.close(fig)
