from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "scripts" / "watch_claude_vast_benchmarks.zsh"


def _write_executable(path: Path, body: str) -> None:
    path.write_text(body)
    path.chmod(0o755)


@pytest.fixture
def fake_commands(tmp_path: Path) -> tuple[dict[str, str], Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    call_log = tmp_path / "calls.log"

    _write_executable(
        bin_dir / "herdr",
        """#!/bin/zsh
if [[ \"$1 $2\" == \"agent read\" ]]; then
  print -r -- \"${FAKE_HERDR_SNAPSHOT:-}\"
elif [[ \"$1 $2\" == \"agent get\" ]]; then
  print -r -- \"{\\\"result\\\":{\\\"agent\\\":{\\\"agent_status\\\":\\\"${FAKE_HERDR_STATE:-idle}\\\"}}}\"
elif [[ \"$1 $2\" == \"agent prompt\" ]]; then
  print -r -- \"prompt $*\" >> \"$FAKE_CALL_LOG\"
fi
""",
    )
    _write_executable(
        bin_dir / "vastai",
        """#!/bin/zsh
if [[ \"$1 $2\" == \"show instances\" ]]; then
  if [[ \"${FAKE_VAST_FAIL:-0}\" == \"1\" ]]; then
    exit 1
  fi
  print -r -- \"${FAKE_VAST_INSTANCES:-[]}\"
elif [[ \"$1 $2\" == \"destroy instance\" ]]; then
  print -r -- \"destroy $3\" >> \"$FAKE_CALL_LOG\"
fi
""",
    )

    environment = os.environ.copy()
    environment.update(
        {
            "PATH": f"{bin_dir}:{environment['PATH']}",
            "FAKE_CALL_LOG": str(call_log),
        }
    )
    return environment, call_log


def _source_and_run(command: str, environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "zsh",
            "-c",
            f'WATCHDOG_TEST_SOURCE_ONLY=1; source "$1"; {command}',
            "watchdog-test",
            str(SCRIPT),
        ],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    "message",
    [
        "You've hit your session limit · resets 8:10am (Europe/London)",
        "You've hit your usage limit",
        "Usage limit reached",
        "Maximum usage reached",
        "/upgrade to increase\nyour usage limit",
    ],
)
def test_usage_limit_messages_are_detected(
    fake_commands: tuple[dict[str, str], Path], message: str
) -> None:
    environment, _ = fake_commands
    environment["FAKE_HERDR_SNAPSHOT"] = message

    result = _source_and_run("claude_usage_limit_detected", environment)

    assert result.returncode == 0, result.stderr


def test_normal_idle_message_is_not_a_limit(
    fake_commands: tuple[dict[str, str], Path],
) -> None:
    environment, _ = fake_commands
    environment["FAKE_HERDR_SNAPSHOT"] = "Ready for the next benchmark."

    result = _source_and_run("claude_usage_limit_detected", environment)

    assert result.returncode != 0


def test_vast_failure_is_not_mistaken_for_zero_instances(
    fake_commands: tuple[dict[str, str], Path],
) -> None:
    environment, _ = fake_commands
    environment["FAKE_VAST_FAIL"] = "1"

    result = _source_and_run("benchmark_instance_count", environment)

    assert result.returncode != 0


def test_destroy_is_restricted_to_configured_label_prefix(
    fake_commands: tuple[dict[str, str], Path], tmp_path: Path
) -> None:
    environment, call_log = fake_commands
    environment["FAKE_VAST_INSTANCES"] = json.dumps(
        [
            {"id": 101, "label": "ceridwen-bench-a10"},
            {"id": 202, "label": "ceridwen-sfh-fastpath-nss-rtx5060"},
        ]
    )
    state_dir = tmp_path / "state"
    state_dir.mkdir()

    result = _source_and_run(
        f'state_dir="{state_dir}"; set_state_paths; destroy_benchmark_instances',
        environment,
    )

    assert result.returncode == 0, result.stderr
    assert call_log.read_text().splitlines() == ["destroy 101"]


def test_two_nonworking_polls_destroy_a_matching_rental(
    fake_commands: tuple[dict[str, str], Path], tmp_path: Path
) -> None:
    environment, call_log = fake_commands
    environment["FAKE_HERDR_STATE"] = "idle"
    environment["FAKE_HERDR_SNAPSHOT"] = "Unknown provider message"
    environment["FAKE_VAST_INSTANCES"] = json.dumps(
        [{"id": 303, "label": "ceridwen-bench-rtx4080"}]
    )
    state_dir = tmp_path / "state"
    state_dir.mkdir()

    result = _source_and_run(
        f'state_dir="{state_dir}"; reset_wait_seconds=100; set_state_paths; '
        "usage_limit_guard_once; usage_limit_guard_once",
        environment,
    )

    assert result.returncode == 0, result.stderr
    assert call_log.read_text().splitlines() == ["destroy 303"]
    assert (state_dir / "usage-limit.active").exists()
    assert "Claude was idle for 2 checks" in result.stdout


def test_active_latch_prevents_resume_prompt(
    fake_commands: tuple[dict[str, str], Path], tmp_path: Path
) -> None:
    environment, call_log = fake_commands
    environment["FAKE_HERDR_STATE"] = "idle"
    environment["FAKE_VAST_INSTANCES"] = "[]"
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "usage-limit.active").write_text("9999999999\n")

    result = _source_and_run(
        f'state_dir="{state_dir}"; set_state_paths; controller_step', environment
    )

    assert result.returncode == 0, result.stderr
    assert "usage-limit latch is active" in result.stdout
    assert not call_log.exists()


def test_sigint_stops_the_watchdog_cleanly(
    fake_commands: tuple[dict[str, str], Path], tmp_path: Path
) -> None:
    environment, _ = fake_commands
    environment["FAKE_VAST_INSTANCES"] = "[]"
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "usage-limit.active").write_text("9999999999\n")
    process = subprocess.Popen(
        [
            "zsh",
            str(SCRIPT),
            "--state-dir",
            str(state_dir),
            "--poll-seconds",
            "60",
        ],
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(0.2)

    process.send_signal(signal.SIGINT)
    stdout, stderr = process.communicate(timeout=5)

    assert process.returncode in {130, -signal.SIGINT}, (stdout, stderr)
    assert "parameter not set" not in stderr
