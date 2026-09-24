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
    """COSMOS2025 retains 28 bands; the added u response enables Classic's 31st."""
    _expected = {"cosmos2025": ("cosmos2025", 28), "cosmos2020_classic": ("classic", 31)}
    for source, (catalogue, n_bands) in _expected.items():
        bands = phot.fit_photometry(source, INSIDE)
        assert len(bands) == n_bands
        assert set(bands["catalogue"]) == {catalogue}
        assert bands["filter_in_sedpy_jax"].all()


def test_fit_photometry_falls_back_outside_the_footprint():
    bands = phot.fit_photometry("cosmos2025", OUTSIDE)
    assert len(bands) > 0
    assert set(bands["catalogue"]) == {"classic"}


def test_uv_supplement_preserves_baseline_and_keeps_nondetection():
    import numpy as np
    import pandas as pd

    baseline = phot.fit_photometry("cosmos2025", INSIDE)
    augmented = phot.fit_photometry("cosmos2025_uv", INSIDE)
    pd.testing.assert_frame_equal(
        augmented[augmented.catalogue == "cosmos2025"].reset_index(drop=True), baseline
    )
    uv = augmented[augmented.catalogue == "classic"].set_index("band")
    assert set(uv.index) == {"NUV", "u"}
    np.testing.assert_allclose(uv.loc["NUV", ["total_flux_ujy", "total_error_ujy"]].astype(float),
                               [0.056442473, 0.075039941], rtol=1e-6)
    np.testing.assert_allclose(uv.loc["u", ["total_flux_ujy", "total_error_ujy"]].astype(float),
                               [0.414527252, 0.017638869], rtol=1e-6)
    assert augmented.band.is_unique


def test_uv_supplement_fallback_has_no_duplicates():
    import pandas as pd

    pd.testing.assert_frame_equal(phot.fit_photometry("cosmos2025_uv", OUTSIDE),
                                  phot.fit_photometry("cosmos2020_classic", OUTSIDE))


def test_uv_filters_project_flat_fnu_and_keep_gaussian_flux_likelihood():
    import numpy as np
    from ceridwen.observation.photometry import Photometry

    bands = phot.fit_photometry("cosmos2025_uv", INSIDE)
    uv = bands[bands.catalogue == "classic"]
    scale = 1e-6 / 3631.0
    flux = uv.total_flux_ujy.to_numpy() * scale
    sigma = np.hypot(uv.total_error_ujy.to_numpy() * scale, 0.05 * abs(flux))
    obs = Photometry(filters=list(uv.sedpy_filter), flux=flux, uncertainty=sigma,
                     mask=np.ones(2, dtype=bool), name="photometry")
    wave = np.linspace(1000.0, 5000.0, 20001)
    # A flat spectrum at the AB reference flux projects to one maggie.
    np.testing.assert_allclose(obs.get_maggies(wave, np.full_like(wave, 3631e-23)),
                               np.ones(2), rtol=3e-3)
    assert obs.upper_limit is None
    assert obs.chi_sq(flux + sigma) == pytest.approx(2.0, rel=1e-5)
    assert obs.chi_sq(flux - sigma) == pytest.approx(2.0, rel=1e-5)


def test_footprint_covers_122_of_the_187_dr2_galaxies(tables):
    manifest = runner.build_target_manifest(num_shards=1, base_seed=runner.DEFAULT_BASE_SEED)
    targets = [target["spect_id"] for target in manifest["targets"]]
    assert len(targets) == 187
    inside = [spect_id for spect_id in targets if spect_id in tables["cosmos2025"]]
    assert len(inside) == 122
    uncovered = [s for s in targets if s not in tables["cosmos2025"] and s not in tables["classic"]]
    assert uncovered == []
