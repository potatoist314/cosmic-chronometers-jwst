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


def test_new_default_seed_repeats_carry_the_new_default_env(arms):
    cells = arms.build_cells(arms.DEFAULT_TARGETS, ["new_default", "new_default_rep1", "new_default_rep2"])
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
    cells = arms.build_cells(arms.DEFAULT_TARGETS, ["poly3_total", "seed_rep1", "seed_rep2"])
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


def test_calibration_order_arms_change_only_the_order(arms):
    for name, order in (("poly5", "5"), ("poly10", "10")):
        extra = {k: v for k, v in arms.ARMS[name].items() if arms.ARMS["new_default"].get(k) != v}
        assert extra == {"CERIDWEN_CALIBRATION_ORDER": order}, (name, extra)
        assert set(arms.ARMS["new_default"]) <= set(arms.ARMS[name])
    cells = arms.build_cells(arms.DEFAULT_TARGETS, ["poly5", "poly10"])
    assert len(cells) == 12
    assert all("base_seed" not in c for c in cells)


def test_no_mock_arms(arms):
    # Removed 2026-09-15; every cell is a real DR2 target from the manifest.
    assert not hasattr(arms, "MOCK_ARMS")
    assert not any(a.startswith("mock") for a in arms.ARMS)


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


def test_offer_rule_accepts_reliable_cards_under_loose_guards(arms):
    """Liu Hao's rule (2026-09-23): 5060/5060 Ti/5070/5080/5090 above 99.5% reliable; $0.80/h and $25/TB are loose disaster guards."""
    assert arms.offer_qualifies(_offer())
    assert arms.offer_qualifies(_offer(gpu_name="RTX 5060 Ti", gpu_ram=16311))
    assert arms.offer_qualifies(_offer(gpu_name="RTX 5070"))
    assert arms.offer_qualifies(_offer(gpu_name="RTX 5080", dph_total=0.35))
    assert arms.offer_qualifies(_offer(gpu_name="RTX 5090", dph_total=0.57))
    assert not arms.offer_qualifies(_offer(dph_total=0.80))
    assert not arms.offer_qualifies(_offer(reliability2=0.995))
    assert not arms.offer_qualifies(_offer(gpu_name="RTX 5070 Ti"))
    assert not arms.offer_qualifies(_offer(gpu_name="RTX 4090", dph_total=0.05))


def test_interruptible_offers_are_judged_on_the_bid(arms):
    """2026-09-15: interruptible is fine under two hours; bid = min_bid + margin, under the guard."""
    dear_on_demand = _offer(dph_total=0.90, min_bid=0.09)
    assert arms.offer_price(dear_on_demand, interruptible=True) == 0.095
    assert arms.offer_qualifies(dear_on_demand, interruptible=True)
    assert not arms.offer_qualifies(dear_on_demand)
    assert not arms.offer_qualifies(_offer(dph_total=0.90, min_bid=0.80), interruptible=True)
    assert not arms.offer_qualifies(_offer(min_bid=0.05, reliability2=0.99), interruptible=True)
    assert arms.offer_qualifies(_offer(inet_down_cost=0.013))  # $13/TB passes the loose $25/TB guard
    assert not arms.offer_qualifies(_offer(inet_down_cost=0.025))


def test_offer_ranking_prefers_lower_cost_per_work_over_lower_hourly(arms):
    ti = _offer(gpu_name="RTX 5060 Ti", dph_total=0.10,
                inet_down_cost=0.001)  # (0.10 + 0.006) / 1.00 = 0.106
    faster = _offer(gpu_name="RTX 5080", dph_total=0.20,
                    inet_down_cost=0.001)  # (0.20 + 0.006) / 2.39 = 0.0862
    ranked = sorted([ti, faster], key=arms._vast.fit_offer_cost_per_work)
    assert [entry["gpu_name"] for entry in ranked] == ["RTX 5080", "RTX 5060 Ti"]


def test_offer_rule_constants_match_the_rule(arms):
    assert arms.MAX_DPH_USD == 0.80
    assert arms.MIN_RELIABILITY == 0.995
    assert set(arms.GPU_NAMES) == {"RTX 5060", "RTX 5060 Ti", "RTX 5070", "RTX 5080", "RTX 5090"}


def test_parser_requires_explicit_arms(arms):
    # Nineteen arms is never the intended run; the caller must name them.
    with pytest.raises(SystemExit) as exc:
        arms.main(["plan", "--targets", "M5_172669"])
    assert exc.value.code == 2


def test_5090_query_narrows_the_gpu_and_keeps_reliability_bandwidth(arms):
    query = arms.offer_query_5090(arms._vast)
    assert "gpu_name=RTX_5090" in query
    assert "reliability>0.995" in query
    assert "inet_down_cost<0.005" in query
    assert "dph<" not in query  # the hourly ceiling is bypassed at the search


def _offer_5090(**overrides):
    base = dict(gpu_name="RTX 5090", dph_total=1.20, gpu_ram=32768)
    base.update(overrides)
    return _offer(**base)


def test_5090_rule_bypasses_only_the_hourly_ceiling(arms):
    sweep = arms._vast
    assert arms.offer_qualifies_5090(sweep, _offer_5090())
    assert arms.offer_qualifies_5090(sweep, _offer_5090(dph_total=2.50))
    assert not arms.offer_qualifies_5090(sweep, _offer_5090(gpu_name="RTX 5080", dph_total=0.20))
    assert not arms.offer_qualifies_5090(sweep, _offer_5090(reliability2=0.995))
    assert not arms.offer_qualifies_5090(sweep, _offer_5090(inet_down_cost=0.005))
    assert arms.offer_qualifies_5090(sweep, _offer_5090(inet_down_cost=0.0049))
    assert not arms.offer_qualifies_5090(
        sweep, {k: v for k, v in _offer_5090().items() if k != "inet_down_cost"})


def test_5090_selection_ranks_by_hourly_price(arms):
    import types

    seen = {}
    # Lower hourly price but higher total cost (bandwidth): hourly ranking keeps it first.
    cheap_hourly = _offer_5090(id=1, dph_total=0.60, inet_down_cost=0.004, host_id=11)
    cheap_total = _offer_5090(id=2, dph_total=0.61, inet_down_cost=0.0, host_id=12)
    dear = _offer_5090(id=3, dph_total=1.50, inet_down_cost=0.0, host_id=13)
    other_gpu = _offer(id=4, gpu_name="RTX 5080", dph_total=0.20, host_id=14)
    flaky = _offer_5090(id=5, dph_total=0.55, reliability2=0.99, host_id=15)

    def fake_vastai_json(argv):
        seen["query"] = argv[2]
        return [cheap_hourly, cheap_total, dear, other_gpu, flaky]

    sweep = types.SimpleNamespace(
        FIT_MIN_RELIABILITY=arms._vast.FIT_MIN_RELIABILITY,
        MAX_INET_COST_USD_PER_TB=arms._vast.MAX_INET_COST_USD_PER_TB,
        _vastai_json=fake_vastai_json,
        fit_offer_cost_per_work=arms._vast.fit_offer_cost_per_work,
    )
    ranked = arms.offers_rtx_5060(sweep, set(), False, True)
    assert [o["id"] for o in ranked] == [1, 2, 3]
    assert "gpu_name=RTX_5090" in seen["query"]
    # Cost-per-work ranking would put id 2 first; hourly keeps id 1 first.
    by_work = sorted([cheap_hourly, cheap_total],
                     key=lambda o: arms._vast.fit_offer_cost_per_work(o))
    assert [o["id"] for o in by_work] == [2, 1]


@pytest.fixture(scope="module")
def multi():
    spec = importlib.util.spec_from_file_location(
        "run_ceridwen_vast_multi_gpu", ROOT / "scripts/run_ceridwen_vast_multi_gpu.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _eline_cell(arms, arm="eline_on"):
    return dict(name=f"{arm}/M1_210210", arm=arm, target="M1_210210",
                object_id=210210, seed=20260832, env=arms.ARMS[arm])


def test_remote_env_requests_a_sampler_only_run(arms):
    env = arms.remote_env(_eline_cell(arms))
    assert env["CERIDWEN_SAMPLER_ONLY"] == "1"
    # The arm switches ride along unchanged.
    assert env["CERIDWEN_SETTINGS_OVERRIDE"] == '{"emission_line_marginalisation": true}'
    assert env["SPS_HOME"] == "/workspace/cosmic-chronometers-jwst/external/fsps"


def test_regenerate_command_carries_the_arm_switches(arms):
    cell = _eline_cell(arms)
    command = arms.regenerate_command(cell, Path("results/x/210210-M1_210210"))
    assert command[command.index("--settings-override") + 1] == cell["env"]["CERIDWEN_SETTINGS_OVERRIDE"]
    assert command[-1] == "results/x/210210-M1_210210"
    plain = arms.regenerate_command(_eline_cell(arms, "eline_off"), Path("results/x/210210-M1_210210"))
    assert "--settings-override" not in plain and "--priors-override" not in plain


def test_regen_python_defaults_to_the_checkout_venv(arms, monkeypatch):
    monkeypatch.delenv("CERIDWEN_REGEN_PYTHON", raising=False)
    assert arms.regen_python() == str(arms.PROJECT_ROOT / "ceridwen/.venv/bin/python")
    assert arms.regenerate_command(_eline_cell(arms), Path("results/x"))[0] == arms.regen_python()


def test_regen_python_override_selects_another_interpreter(arms, monkeypatch):
    # A worktree without ceridwen/.venv reuses an existing environment (2026-09-24).
    monkeypatch.setenv("CERIDWEN_REGEN_PYTHON", "/elsewhere/bin/python")
    command = arms.regenerate_command(_eline_cell(arms), Path("results/x/210210-M1_210210"))
    assert command[0] == "/elsewhere/bin/python"
    assert command[command.index("--settings-override") + 1] == '{"emission_line_marginalisation": true}'


def test_sampler_only_follows_the_env(multi, monkeypatch):
    monkeypatch.delenv("CERIDWEN_SAMPLER_ONLY", raising=False)
    assert multi.sampler_only() is False
    monkeypatch.setenv("CERIDWEN_SAMPLER_ONLY", "1")
    assert multi.sampler_only() is True


def test_truncate_to_sampler_keeps_the_prefix(multi):
    import nbformat

    document = nbformat.read(ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb", as_version=4)
    kept = multi.truncate_to_sampler(document)
    code = [c for c in kept if c.cell_type == "code"]
    assert len(kept) == 11
    assert multi.SAMPLER_CELL_MARKER in code[-1].source
    assert "ceridwen_derived_outputs.h5" not in "\n".join(c.source for c in code)


def test_truncate_to_sampler_needs_the_marker(multi):
    import nbformat

    document = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("a = 1")])
    with pytest.raises(ValueError, match="run_sampler"):
        multi.truncate_to_sampler(document)


RESULT_H5 = ROOT / "results/emission-line-marginalisation/eline_off/210210-M1_210210/ceridwen_result.h5"
needs_result = pytest.mark.skipif(not RESULT_H5.exists(), reason="needs the stored eline_off fit")


@needs_result
def test_sampler_validation_passes_without_derived_outputs(multi, tmp_path):
    import shutil

    result_dir = tmp_path / "210210-M1_210210"
    result_dir.mkdir()
    shutil.copy(RESULT_H5, result_dir / "ceridwen_result.h5")
    multi._validate_sampler_result(result_dir, "M1_210210")
    with pytest.raises((FileNotFoundError, KeyError, OSError, RuntimeError, ValueError)):
        multi._validate_result(result_dir, "M1_210210")


def _manifest_tree(monkeypatch, tmp_path, arms, statuses):
    import json

    monkeypatch.setattr(arms, "PROJECT_ROOT", tmp_path)
    root = tmp_path / arms.RESULTS
    root.mkdir(parents=True)
    (root / "arms_manifest.json").write_text(json.dumps(statuses))
    return root


def test_regenerate_skips_cells_that_are_not_done(arms, tmp_path, monkeypatch):
    cell = _eline_cell(arms)
    _manifest_tree(monkeypatch, tmp_path, arms, {cell["name"]: {"status": "failed"}})

    def fail(*args, **kwargs):
        raise AssertionError("no subprocess for a failed cell")

    monkeypatch.setattr(arms.subprocess, "run", fail)
    assert arms._regenerate([cell], arms._log("test")) == {}


def test_regenerate_runs_and_validates_done_cells(arms, tmp_path, monkeypatch):
    import types

    cell = _eline_cell(arms)
    root = _manifest_tree(monkeypatch, tmp_path, arms, {cell["name"]: {"status": "done"}})
    calls = {}

    def fake_run(command, **kwargs):
        calls["command"] = command
        return types.SimpleNamespace(returncode=0)

    def fake_validate(result_dir, target):
        calls["validated"] = (str(result_dir), target)

    monkeypatch.setattr(arms.subprocess, "run", fake_run)
    monkeypatch.setattr(arms, "_load", lambda name, filename: types.SimpleNamespace(_validate_result=fake_validate))
    out = arms._regenerate([cell], arms._log("test"))
    assert out[cell["name"]]["status"] == "ok"
    command = calls["command"]
    assert command[command.index("--settings-override") + 1] == cell["env"]["CERIDWEN_SETTINGS_OVERRIDE"]
    assert command[-1] == str(root / "eline_on" / "210210-M1_210210")
    assert calls["validated"] == (str(root / "eline_on" / "210210-M1_210210"), "M1_210210")
