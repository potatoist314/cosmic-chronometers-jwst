"""Fast KL diagnostics: exact df=2 Student-t quantile, vectorised noise floor.

The KL table of the stored M1_210210 eline_off posterior must match the
pre-change output bit for bit (the closed form only removes TFP round-off),
and the SFH noise floor must match within Monte Carlo noise (seed scatter
sigma ~1.5e-4; same-seed old-vs-new delta 3.5e-4).
"""
import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import plot_prior_kl as pkl  # noqa: E402
import per_galaxy_diagnostics as pgd  # noqa: E402

RESULT_DIR = PROJECT_ROOT / "results/emission-line-marginalisation/eline_off/210210-M1_210210"
SEED = 20260832
# kl_table of the stored fit from the code before the change (scripts/plot_prior_kl.py
# at project 559377b): parameter -> (bits, err).
KL_BEFORE = {
    "Z": (5.096406292663635, 0.013900341652690607),
    "afe": (4.255320349301022, 0.012977707687738427),
    "diffuse_dust_index": (5.903017320555649, 0.022457876131450227),
    "diffuse_tau_kc": (4.308767605165043, 0.014195554697966628),
    "log_f_calib": (4.62408511522886, 0.014286586478789776),
    "logmass": (6.803120276022747, 0.01334665249210687),
    "sigma_smooth": (1.4917925367638456, 0.01583102839831929),
    "zred": (11.527375613544454, 0.01423817877183886),
    "log_sfr_bin[0]": (5.238358075851573, 0.016498599948599146),
    "log_sfr_bin[1]": (1.3885852611068832, 0.010230042605435918),
    "log_sfr_bin[2]": (1.6759716127726194, 0.008840489863015444),
    "log_sfr_bin[3]": (1.594783114054159, 0.009110966815068733),
    "log_sfr_bin[4]": (3.6378856794746834, 0.01773879976494186),
    "log_sfr_bin[5]": (4.7023125576198455, 0.01695981427294946),
    "log_sfr_bin[6]": (4.86114534738099, 0.01437944358220511),
}
FLOOR_BEFORE = 0.008849  # log_sfr_noise_floor of the stored fit, same code

needs_fit = pytest.mark.skipif(
    not (RESULT_DIR / "ceridwen_result.h5").exists(),
    reason="needs the stored M1_210210 eline_off fit",
)


def test_student_t_df2_matches_scipy():
    from scipy.stats import t

    rng = np.random.default_rng(1)
    p = np.concatenate([np.linspace(1e-12, 1 - 1e-12, 20001), rng.uniform(0, 1, 20000)])
    for loc, scale in ((0.0, 1.0), (0.3, 2.5), (-1.0, 0.3)):
        got = pkl.student_t_quantile_df2(p, loc=loc, scale=scale)
        want = t.ppf(p, 2, loc=loc, scale=scale)
        scaled = np.abs(got - want) / np.maximum(np.abs(want), 1.0)
        assert scaled.max() < 1e-10, (loc, scale, scaled.max())


def test_student_t_df2_edges():
    edge = pkl.student_t_quantile_df2(np.array([0.0, 0.5, 1.0]), loc=1.0, scale=2.0)
    assert np.isneginf(edge[0]) and edge[1] == 1.0 and np.isposinf(edge[2])


def test_student_t_df2_matches_tfp():
    prior = pgd.parse_prior("StudentT(mean=0.0, scale=0.3, df=2.0)")
    u = np.linspace(1e-6, 1 - 1e-6, 2001).reshape(-1, 1)
    got = np.asarray(pkl._prior_quantile(prior, u), dtype=float)
    want = np.asarray(prior.unit_transform(u), dtype=float)
    np.testing.assert_allclose(got, want, rtol=1e-6, atol=1e-8)


def test_other_df_falls_back_to_tfp():
    prior = pgd.parse_prior("StudentT(mean=0.0, scale=0.3, df=5.0)")
    u = np.linspace(1e-3, 1 - 1e-3, 11).reshape(-1, 1)
    got = np.asarray(pkl._prior_quantile(prior, u), dtype=float)
    want = np.asarray(prior.unit_transform(u), dtype=float)
    np.testing.assert_allclose(got, want, rtol=1e-12, atol=0.0)


@needs_fit
def test_kl_table_matches_pre_change_output():
    galaxy = pgd.load_galaxy(RESULT_DIR)
    table = pkl.kl_table(galaxy)
    assert sorted(table.index) == sorted(KL_BEFORE)
    for name, (bits, err) in KL_BEFORE.items():
        # Measured delta is 0.0; 1e-9 is far below the bootstrap err (~1e-2).
        assert table.loc[name, "bits"] == pytest.approx(bits, abs=1e-9)
        assert table.loc[name, "err"] == pytest.approx(err, abs=1e-9)


@needs_fit
def test_noise_floor_within_monte_carlo_noise():
    galaxy = pgd.load_galaxy(RESULT_DIR)
    floor = pkl.log_sfr_noise_floor(galaxy, seed=SEED)
    assert abs(floor - FLOOR_BEFORE) <= 5e-4


@needs_fit
def test_noise_floor_few_repeats_is_finite():
    galaxy = pgd.load_galaxy(RESULT_DIR)
    floor = pkl.log_sfr_noise_floor(galaxy, seed=SEED, repeats=3)
    assert np.isfinite(floor) and floor > 0
