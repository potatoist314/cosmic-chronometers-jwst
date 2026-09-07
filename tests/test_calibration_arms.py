"""Cell construction for the fit-accuracy arms in ``scripts/calibration_arms_vast.py``."""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

os.environ.setdefault("CERIDWEN_ARMS_RESULTS", "results/fit-accuracy-knobs")
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def arms():
    spec = importlib.util.spec_from_file_location(
        "calibration_arms_vast", ROOT / "scripts/calibration_arms_vast.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


STAGE1 = ["floor20", "emis_wide", "no_irac", "dust_free", "sfh_cont", "mask_cn"]
NEW_DEFAULT_ARMS = ["tau_cn", "dust_wide"]


def test_new_default_arm_pins_both_flipped_defaults(arms):
    # Equal to the production notebook with no env after the two 2026-09-06 flips.
    assert arms.ARMS["new_default"] == {
        "CERIDWEN_CALIBRATION_ORDER": "3", "CERIDWEN_PHOTOMETRY": "cosmos_total",
        "CERIDWEN_SFH_PRIOR": "student", "CERIDWEN_FREE_DUST_INDEX": "1",
    }
    for name in NEW_DEFAULT_ARMS:
        extra = {k: v for k, v in arms.ARMS[name].items() if arms.ARMS["new_default"].get(k) != v}
        assert len(extra) == 1, (name, extra)
        assert set(arms.ARMS["new_default"]) <= set(arms.ARMS[name])
    assert arms.ARMS["tau_cn"]["CERIDWEN_TAU_PRIOR"] == "clipped"
    assert arms.ARMS["dust_wide"]["CERIDWEN_DUST_INDEX_BOUNDS"] == "-2.0,0.5"
    assert arms.MOCK_ARMS["mock_tilt4_new_default"]["CERIDWEN_SFH_PRIOR"] == "student"
    assert arms.MOCK_ARMS["mock_tilt4_new_default"]["CERIDWEN_FREE_DUST_INDEX"] == "1"
    assert arms.MOCK_ARMS["mock_tilt4_new_default"]["CERIDWEN_CALIBRATION_ORDER"] == "3"


def test_new_default_seed_repeats_carry_the_new_default_env(arms):
    cells = arms.build_cells(arms.DEFAULT_TARGETS, ["new_default", "new_default_rep1", "new_default_rep2"], [])
    by_arm = {}
    for cell in cells:
        by_arm.setdefault(cell["arm"], []).append(cell)
    assert len(by_arm["new_default"]) == 6
    production = {c["target"]: c["seed"] for c in by_arm["new_default"]}
    for arm in ("new_default_rep1", "new_default_rep2"):
        assert sorted(c["target"] for c in by_arm[arm]) == ["M4_108989", "M5_172669"]
        for cell in by_arm[arm]:
            assert cell["env"] == arms.ARMS["new_default"]
            assert cell["seed"] != production[cell["target"]]
    # Same shifted seeds as the poly3_total repeats, so the two floors are paired.
    assert arms.SEED_REP_BASE["new_default_rep1"] == arms.SEED_REP_BASE["seed_rep1"]
    assert arms.SEED_REP_BASE["new_default_rep2"] == arms.SEED_REP_BASE["seed_rep2"]


def test_stage1_arms_differ_from_poly3_total_by_one_switch(arms):
    for name in STAGE1:
        extra = {k: v for k, v in arms.ARMS[name].items() if arms.ARMS["poly3_total"].get(k) != v}
        assert len(extra) == 1, (name, extra)
        # An arm may override a reference key (sfh_cont flips the prior) but never drops one.
        assert set(arms.ARMS["poly3_total"]) <= set(arms.ARMS[name])


def test_seed_repeats_only_run_on_two_targets_with_new_seeds(arms):
    cells = arms.build_cells(arms.DEFAULT_TARGETS, ["poly3_total", "seed_rep1", "seed_rep2"], [])
    by_arm = {}
    for cell in cells:
        by_arm.setdefault(cell["arm"], []).append(cell)
    assert len(by_arm["poly3_total"]) == 6
    assert sorted(c["target"] for c in by_arm["seed_rep1"]) == ["M4_108989", "M5_172669"]
    production = {c["target"]: c["seed"] for c in by_arm["poly3_total"]}
    for arm in ("seed_rep1", "seed_rep2"):
        for cell in by_arm[arm]:
            assert cell["base_seed"] != arms.DEFAULT_BASE_SEED
            assert cell["seed"] != production[cell["target"]]
            assert cell["env"] == arms.ARMS["poly3_total"]
    seeds = {(c["arm"], c["target"]): c["seed"] for c in cells}
    assert seeds[("seed_rep1", "M4_108989")] != seeds[("seed_rep2", "M4_108989")]
    assert all("base_seed" not in c for c in by_arm["poly3_total"])


def test_seed_forwarded_to_runner_command(arms):
    cell = dict(name="seed_rep1/M4_108989", arm="seed_rep1", target="M4_108989",
                object_id="1", seed=1, env={}, base_seed=12345)
    command = arms.runner_command(cell, Path("/tmp/out"))
    assert command[command.index("--base-seed") + 1] == "12345"
    plain = arms.runner_command({**cell, "base_seed": None}, Path("/tmp/out"))
    assert "--base-seed" not in plain


def test_mock_arms_are_selected_by_name(arms):
    cells = arms.build_cells(["M4_108989"], [], ["mock_tilt4_sfh_cont"])
    assert [c["arm"] for c in cells] == ["mock_tilt4_sfh_cont"]
    assert cells[0]["env"]["CERIDWEN_SFH_PRIOR"] == "student"
    assert cells[0]["env"]["CERIDWEN_CALIBRATION_ORDER"] == "3"


def test_reference_arm_pins_the_uniform_sfh_prior_after_the_default_flip(arms):
    # Production default became the StudentT continuity prior on 2026-09-06; the
    # stored poly3_total / seed_rep fits were made with the uniform prior, so the
    # reference arm must say so explicitly to stay reproducible.
    for name in ("poly3_total", "seed_rep1", "floor20", "no_irac", "dust_free", "mask_cn"):
        assert arms.ARMS[name]["CERIDWEN_SFH_PRIOR"] == "uniform"
    assert arms.ARMS["sfh_cont"]["CERIDWEN_SFH_PRIOR"] == "student"


def test_reference_arm_pins_the_fixed_dust_index_after_the_default_flip(arms):
    # Production default freed the Kriek and Conroy index (Uniform -1.0, 0.4) on
    # 2026-09-06; the stored poly3_total / seed_rep fits fixed it at -0.7, so the
    # reference arm must say so explicitly to stay reproducible.
    for name in ("poly3_total", "seed_rep1", "floor20", "no_irac", "sfh_cont", "mask_cn"):
        assert arms.ARMS[name]["CERIDWEN_FREE_DUST_INDEX"] == "0"
    assert arms.ARMS["dust_free"]["CERIDWEN_FREE_DUST_INDEX"] == "1"


def _offer(**overrides):
    base = dict(gpu_name="RTX 5060", dph_total=0.09, reliability2=0.997, gpu_ram=8151,
                cuda_max_good=12.8, inet_down_cost=0.0, host_id=1)
    base.update(overrides)
    return base


def test_offer_rule_accepts_only_cheap_reliable_5060s(arms):
    """Liu Hao's rule (2026-09-07): RTX 5060 or 5060 Ti, under $0.10/h, above 99.5% reliable."""
    assert arms.offer_qualifies(_offer())
    assert arms.offer_qualifies(_offer(gpu_name="RTX 5060 Ti", gpu_ram=16311))
    assert not arms.offer_qualifies(_offer(dph_total=0.10))
    assert not arms.offer_qualifies(_offer(dph_total=0.149))
    assert not arms.offer_qualifies(_offer(reliability2=0.995))
    assert not arms.offer_qualifies(_offer(gpu_name="RTX 5070"))
    assert not arms.offer_qualifies(_offer(gpu_name="RTX 4090", dph_total=0.05))


def test_offer_rule_constants_match_the_rule(arms):
    assert arms.MAX_DPH_USD == 0.10
    assert arms.MIN_RELIABILITY == 0.995
    assert set(arms.GPU_NAMES) == {"RTX 5060", "RTX 5060 Ti"}
