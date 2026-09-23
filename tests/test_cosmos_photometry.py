"""COSMOS2025 default photometry: footprint fallback and the refit recipe."""
from __future__ import annotations

import pytest

from scripts import cosmos_photometry as phot
from scripts import run_ceridwen_vast_multi_gpu as runner

INSIDE = "M1_210210"  # in the COSMOS2025 footprint (the refit galaxy)
OUTSIDE = "M10_233129"  # outside it; in COSMOS2020 Classic with FlagCOMBINED == 0


@pytest.fixture(scope="module")
def tables():
    return phot.read_matches()


def test_cosmos2025_is_the_default_with_classic_fallback():
    assert phot.DEFAULT_PHOTOMETRY == "cosmos2025"
    assert phot.FALLBACK_PHOTOMETRY == "cosmos2020_classic"


def test_resolve_keeps_cosmos2025_inside_its_footprint(tables):
    assert phot.resolve_photometry("cosmos2025", INSIDE, tables) == "cosmos2025"


def test_resolve_falls_back_to_classic_outside_its_footprint(tables):
    assert OUTSIDE not in tables["cosmos2025"]
    assert phot.resolve_photometry("cosmos2025", OUTSIDE, tables) == "cosmos2020_classic"


def test_resolve_leaves_explicit_sources_unchanged(tables):
    for source in ("cosmos_total", "cosmos2020_classic"):
        assert phot.resolve_photometry(source, INSIDE, tables) == source
        assert phot.resolve_photometry(source, OUTSIDE, tables) == source


def test_fit_photometry_matches_the_refit_band_counts():
    """Same recipe as e-cosmos-photometry-refit: 28 COSMOS2025 and 30 Classic bands on M1_210210."""
    _expected = {"cosmos2025": ("cosmos2025", 28), "cosmos2020_classic": ("classic", 30)}
    for source, (catalogue, n_bands) in _expected.items():
        bands = phot.fit_photometry(source, INSIDE)
        assert len(bands) == n_bands
        assert set(bands["catalogue"]) == {catalogue}
        assert bands["filter_in_sedpy_jax"].all()


def test_fit_photometry_falls_back_outside_the_footprint():
    bands = phot.fit_photometry("cosmos2025", OUTSIDE)
    assert len(bands) > 0
    assert set(bands["catalogue"]) == {"classic"}


def test_footprint_covers_122_of_the_187_dr2_galaxies(tables):
    manifest = runner.build_target_manifest(num_shards=1, base_seed=runner.DEFAULT_BASE_SEED)
    targets = [target["spect_id"] for target in manifest["targets"]]
    assert len(targets) == 187
    inside = [spect_id for spect_id in targets if spect_id in tables["cosmos2025"]]
    assert len(inside) == 122
    uncovered = [s for s in targets if s not in tables["cosmos2025"] and s not in tables["classic"]]
    assert uncovered == []
