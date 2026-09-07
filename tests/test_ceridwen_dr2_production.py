import json
import os
from pathlib import Path

import pytest

from scripts import run_ceridwen_vast_multi_gpu as runner


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"


@pytest.fixture(scope="module")
def target_manifest():
    return runner.build_target_manifest(num_shards=2, base_seed=20260830)


def test_manifest_selects_187_unique_objects(target_manifest):
    targets = target_manifest["targets"]

    assert target_manifest["eligible_spectra"] == 194
    assert target_manifest["unique_objects"] == 187
    assert len({target["object_id"] for target in targets}) == 187
    assert [target["sn"] for target in targets] == sorted(
        (target["sn"] for target in targets), reverse=True
    )


def test_manifest_has_stable_seeds_and_balanced_shards(target_manifest):
    targets = target_manifest["targets"]

    assert [target["manifest_index"] for target in targets] == list(range(187))
    assert [target["seed"] for target in targets] == list(
        range(20260830, 20260830 + 187)
    )
    assert [target["shard_index"] for target in targets] == [
        index % 2 for index in range(187)
    ]
    assert sum(target["shard_index"] == 0 for target in targets) == 94
    assert sum(target["shard_index"] == 1 for target in targets) == 93


def test_reference_target_keeps_manifest_seed(target_manifest):
    target = next(
        target for target in target_manifest["targets"] if target["spect_id"] == "M1_210210"
    )

    assert target == {
        "manifest_index": 2,
        "object_id": 210210,
        "spect_id": "M1_210210",
        "sn": pytest.approx(62.2),
        "shard_index": 0,
        "seed": 20260832,
    }


def test_control_process_keeps_validation_off_gpu(monkeypatch, tmp_path):
    monkeypatch.delenv("JAX_PLATFORMS", raising=False)
    args = runner._parser().parse_args(
        ["--write-targets-file", str(tmp_path / "targets.json")]
    )

    assert runner._run(args) == 0
    assert os.environ["JAX_PLATFORMS"] == "cpu"


def test_monitor_pulls_only_promised_per_target_files(monkeypatch, tmp_path):
    endpoint = runner._monitor_endpoint("49277679:ssh8.vast.ai:37678:1")
    manifest = {
        "targets": [{"object_id": 233129, "spect_id": "M10_233129"}],
        "results": {"M10_233129": {"status": "complete"}},
    }
    validations = 0
    commands = []

    def validate(*_args):
        nonlocal validations
        validations += 1
        if validations == 1:
            raise FileNotFoundError

    monkeypatch.setattr(runner, "_validate_result", validate)
    monkeypatch.setattr(
        runner, "_rsync_command", lambda _endpoint, *args: commands.append(args)
    )

    assert runner._pull_completed(
        endpoint, manifest, tmp_path, runner.DEFAULT_REMOTE_RESULT_ROOT
    ) == {"M10_233129"}
    result_pull = commands[1]
    assert "--include=execution.log" in result_pull
    assert "--include=ceridwen_result.h5" in result_pull
    assert "--include=ceridwen_derived_outputs.h5" in result_pull
    assert "--include=M10_233129_executed.ipynb" in result_pull
    assert "--exclude=*" in result_pull
    assert not any(".png" in argument or ".pkl" in argument for argument in result_pull)


def test_notebook_uses_production_model_and_sampler_contract():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "drop_duplicates(\"OBJECT\", keep=\"first\")" in source
    assert "assert len(selected_passive) == 187" in source
    assert "assert phot_fit_mask.sum() == 12" in source
    assert "ClippedNormal(\n        mean=1.0, sigma=0.3, low=0.2, high=3.0" in source
    assert '"num_live": 500' in source
    assert '"num_inner_steps": 65' in source
    assert '"num_delete": 100' in source
    assert '"logZ_tol": -5.0' in source
    assert "assert sum(np.size(value) for value in joint_model.theta_init.values())" in source
    assert '"Z": "log10 absolute metallicity"' in source
    assert r"$\log_{10}(Z/Z_\odot)$" not in source
    assert "aperture_transfer" not in source


def test_notebook_embeds_figures_and_writes_analysis_ready_hdf5():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert ".savefig(" not in source
    assert 'RESULT_DIR / "' not in source or ".png" not in source
    for group in ("summary", "sfh", "photometry", "spectrum", "diagnostics"):
        assert f'create_group("{group}")' in source
    assert "plt.show()" in source
    assert "np.where(spectrum_mask, spectrum_flux, np.nan)" in source


def test_shard_runs_one_fit_per_gpu_by_default():
    args = runner._parser().parse_args(["--shard-index", "0"])

    assert args.fits_per_gpu == runner.DEFAULT_FITS_PER_GPU
    assert runner.DEFAULT_FITS_PER_GPU == 1


def test_worker_memory_fraction_splits_the_device():
    assert runner._memory_fraction(1) is None
    assert runner._memory_fraction(2) == pytest.approx(0.42)
    assert runner._memory_fraction(3) == pytest.approx(0.28)

    target = {"seed": 1, "spect_id": "M1_1", "object_id": 1, "manifest_index": 0}
    env = runner._worker_environment(target, Path("/tmp/x"), runner._memory_fraction(3))
    assert env["XLA_CLIENT_MEM_FRACTION"] == "0.28"
    assert "XLA_CLIENT_MEM_FRACTION" not in runner._worker_environment(
        target, Path("/tmp/x"), runner._memory_fraction(1)
    )


def test_concurrent_shard_records_fits_per_gpu_and_every_target(monkeypatch, tmp_path):
    executed = []

    def execute(target, result_dir, mem_fraction=None):
        executed.append((target["spect_id"], mem_fraction))
        return 0

    validations = {}

    def validate(result_dir, spect_id):
        validations[spect_id] = validations.get(spect_id, 0) + 1
        if validations[spect_id] == 1:
            raise FileNotFoundError

    monkeypatch.setattr(runner, "_visible_gpu", lambda _minimum: {"memory_mib": 8188})
    monkeypatch.setattr(runner, "_execute_target", execute)
    monkeypatch.setattr(runner, "_validate_result", validate)
    args = runner._parser().parse_args(
        [
            "--num-shards",
            "63",
            "--shard-index",
            "0",
            "--fits-per-gpu",
            "3",
            "--output-root",
            str(tmp_path),
        ]
    )

    assert runner._run(args) == 0

    manifest = json.loads((tmp_path / "shard_0_manifest.json").read_text())
    assert manifest["status"] == "complete"
    assert manifest["fits_per_gpu"] == 3
    assert sorted(spect_id for spect_id, _ in executed) == sorted(
        target["spect_id"] for target in manifest["targets"]
    )
    assert len(executed) == 3
    assert {fraction for _, fraction in executed} == {0.28}
    assert all(
        result["status"] == "complete" for result in manifest["results"].values()
    )


def test_validator_counts_only_physical_parameter_groups():
    # dust_free samples the attenuation slope; free-z / free-sigma add zred / sigma_smooth.
    sampled = ["Z", "afe", "diffuse_dust_index", "diffuse_tau_kc", "log_f_calib",
               "logmass", "logsfr_ratios", "sigma_smooth", "spectrum_scaling", "zred"]
    assert runner.physical_parameter_names(sampled) == [
        "Z", "afe", "diffuse_tau_kc", "log_f_calib", "logmass", "logsfr_ratios",
        "spectrum_scaling",
    ]


def test_notebook_defaults_to_the_continuity_sfh_prior():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert 'SFH_PRIOR = os.environ.get("CERIDWEN_SFH_PRIOR", "student")' in source
    assert 'StudentT(mean=0.0, scale=0.3, df=2.0)' in source


def test_notebook_defaults_to_a_free_dust_index():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert 'FREE_DUST_INDEX = os.environ.get("CERIDWEN_FREE_DUST_INDEX", "1") == "1"' in source
    assert 'os.environ.get("CERIDWEN_DUST_INDEX_BOUNDS", "-1.0,0.4")' in source


def test_notebook_defaults_to_the_uniform_tau_prior():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert 'TAU_PRIOR = os.environ.get("CERIDWEN_TAU_PRIOR", "uniform")' in source
    # Ceridwen's documented dust-column prior, selected by CERIDWEN_TAU_PRIOR=clipped.
    assert "ClippedNormal(mean=0.3, sigma=1.0, low=0.0, high=4.0)" in source
    assert 'attrs["tau_prior"] = TAU_PRIOR' in source
    assert 'attrs["dust_index_bounds"]' in source


def test_notebook_marks_major_absorption_features():
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    # Windows come from ceridwen's Lick/IDS catalogue, redshifted with z_catalog.
    assert (
        "from ceridwen.observation.absorption_features import "
        "absorption_feature_mask, feature_windows"
    ) in source
    assert "def mark_absorption_features(ax" in source
    assert "mark_absorption_features(axes[0])" in source
    assert "mark_absorption_features(axes[1], show_labels=False)" in source
    for name in ("CaK", "CaH", "HdA", "G4300", "HgA", "Fe4383", "Hbeta", "Mgb", "Fe5270"):
        assert f'("{name}",' in source


def test_result_roots_default_to_the_first_production_run(monkeypatch):
    monkeypatch.delenv("CERIDWEN_OUTPUT_ROOT", raising=False)
    monkeypatch.delenv("CERIDWEN_REMOTE_RESULT_ROOT", raising=False)
    args = runner._parser().parse_args([])

    assert args.output_root == PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
    assert args.remote_result_root == (
        "/workspace/cosmic-chronometers-jwst/results/rtx-5060-dr2-quiescent-full-spectrum"
    )


def test_result_roots_follow_the_environment_and_then_the_flags(monkeypatch, tmp_path):
    monkeypatch.setenv("CERIDWEN_OUTPUT_ROOT", str(tmp_path / "env-root"))
    monkeypatch.setenv("CERIDWEN_REMOTE_RESULT_ROOT", "/workspace/x/results/env-root")
    from_env = runner._parser().parse_args([])

    assert from_env.output_root == tmp_path / "env-root"
    assert from_env.remote_result_root == "/workspace/x/results/env-root"

    from_flags = runner._parser().parse_args(
        ["--output-root", str(tmp_path / "flag-root"),
         "--remote-result-root", "/workspace/x/results/flag-root"]
    )
    assert from_flags.output_root == tmp_path / "flag-root"
    assert from_flags.remote_result_root == "/workspace/x/results/flag-root"


def test_monitor_reads_and_pulls_from_the_given_remote_root(monkeypatch, tmp_path):
    endpoint = runner._monitor_endpoint("49277679:ssh8.vast.ai:37678:1")
    manifest = {
        "targets": [{"object_id": 233129, "spect_id": "M10_233129"}],
        "results": {"M10_233129": {"status": "complete"}},
    }
    remote_root = "/workspace/cosmic-chronometers-jwst/results/dr2-quiescent-new-defaults"
    commands = []
    ssh_commands = []

    def fake_ssh(command, **_kwargs):
        ssh_commands.append(command)
        return type("Completed", (), {"stdout": "{}"})()

    monkeypatch.setattr(runner, "_validate_result", lambda *_args: None)
    monkeypatch.setattr(
        runner, "_rsync_command", lambda _endpoint, *args: commands.append(args)
    )
    monkeypatch.setattr(runner.subprocess, "run", fake_ssh)

    runner._remote_manifest(endpoint, remote_root)
    assert f"{remote_root}/shard_1_manifest.json" in ssh_commands[0]

    runner._pull_completed(endpoint, manifest, tmp_path, remote_root)
    assert all(
        "rtx-5060-dr2-quiescent-full-spectrum" not in argument
        for argument in commands[0]
    )
    assert f"root@ssh8.vast.ai:{remote_root}/targets.json" in commands[0]


def test_summary_script_takes_a_result_root_and_an_output_path():
    from scripts import build_dr2_quiescent_summary as summary

    defaults = summary._parser().parse_args([])
    assert defaults.result_root == PROJECT_ROOT / "results/rtx-5060-dr2-quiescent-full-spectrum"
    assert defaults.out_path == PROJECT_ROOT / "results/dr2-quiescent-summary.csv"

    chosen = summary._parser().parse_args(
        ["--result-root", "results/dr2-quiescent-new-defaults",
         "--out-path", "results/dr2-quiescent-new-defaults-summary.csv"]
    )
    assert chosen.result_root == Path("results/dr2-quiescent-new-defaults")
    assert chosen.out_path == Path("results/dr2-quiescent-new-defaults-summary.csv")


def test_destroy_skips_the_interactive_confirmation(monkeypatch):
    """`vastai destroy` prompts and exits 0 when it aborts, so the monitor's
    teardown must not rely on the exit code alone to know it ran."""
    endpoints = [{"instance_id": 50104285}, {"instance_id": 50104286}]
    calls = []
    monkeypatch.setattr(
        runner.subprocess, "run", lambda command, **_kwargs: calls.append(command)
    )

    runner._set_instances(endpoints, "destroy")
    assert calls == [
        ["vastai", "destroy", "instance", "50104285", "-y"],
        ["vastai", "destroy", "instance", "50104286", "-y"],
    ]

    calls.clear()
    runner._set_instances(endpoints, "stop")
    assert calls == [
        ["vastai", "stop", "instance", "50104285"],
        ["vastai", "stop", "instance", "50104286"],
    ]
