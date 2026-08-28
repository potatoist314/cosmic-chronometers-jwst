#!/bin/zsh

set -u
setopt pipe_fail

target_agent="w2:p4"
owner_agent="w2:p1"
state_dir="/Users/liuhao/.cache/codex/herdr-claude-gpu-bench"
label_prefix="ceridwen-bench-"
reset_wait_seconds=18600
poll_seconds=60
nonworking_poll_limit=2
nonworking_polls=0
guard_pid=0

usage() {
  print -u2 "Usage: $0 [--target-agent ID] [--owner-agent ID] [--state-dir DIR]"
  print -u2 "          [--label-prefix PREFIX] [--poll-seconds N] [--reset-seconds N]"
}

parse_args() {
  while (( $# > 0 )); do
    case "$1" in
      --target-agent)
        target_agent="$2"
        shift 2
        ;;
      --owner-agent)
        owner_agent="$2"
        shift 2
        ;;
      --state-dir)
        state_dir="$2"
        shift 2
        ;;
      --label-prefix)
        label_prefix="$2"
        shift 2
        ;;
      --poll-seconds)
        poll_seconds="$2"
        shift 2
        ;;
      --reset-seconds)
        reset_wait_seconds="$2"
        shift 2
        ;;
      -h|--help)
        usage
        return 1
        ;;
      *)
        print -u2 "Unknown argument: $1"
        usage
        return 2
        ;;
    esac
  done

  if [[ -z "$label_prefix" ]]; then
    print -u2 "The Vast.ai label prefix must not be empty."
    return 2
  fi
  if [[ "$poll_seconds" != <-> || "$reset_wait_seconds" != <-> ]]; then
    print -u2 "Poll and reset intervals must be non-negative integers."
    return 2
  fi
}

set_state_paths() {
  initial_prompt="$state_dir/initial-prompt.txt"
  resume_prompt="$state_dir/resume-prompt.txt"
  started_file="$state_dir/watchdog.started"
  complete_file="$state_dir/complete"
  limit_log="$state_dir/usage-limit-destroyed.tsv"
  limit_latch="$state_dir/usage-limit.active"
}

utc_now() {
  date -u +'%Y-%m-%dT%H:%M:%SZ'
}

agent_state() {
  herdr agent get "$1" 2>/dev/null \
    | jq -r '.result.agent.agent_status // "missing"' 2>/dev/null
}

benchmark_instances() {
  local payload
  payload="$(vastai show instances --raw 2>/dev/null)" || return 1
  print -r -- "$payload" \
    | jq --arg prefix "$label_prefix" \
      '[.[] | select((.label // "") | startswith($prefix))]' 2>/dev/null
}

benchmark_instance_count() {
  benchmark_instances | jq 'length' 2>/dev/null
}

claude_usage_limit_detected() {
  local snapshot
  snapshot="$(herdr agent read "$target_agent" --source visible 2>/dev/null)" || return 1
  print -r -- "$snapshot" \
    | tr '\n' ' ' \
    | grep -Eiq \
      "you.?ve hit your (session |usage |weekly )?limit|usage limit (reached|exceeded)|maximum usage reached|/upgrade to increase[[:space:]]+your usage limit"
}

activate_limit_latch() {
  local reason="$1"
  if [[ ! -e "$limit_latch" ]]; then
    print $(( $(date +%s) + reset_wait_seconds )) > "$limit_latch"
    print "$(utc_now) LIMIT: $reason"
  fi
}

expire_limit_latch_if_due() {
  local deadline now
  [[ -e "$limit_latch" ]] || return 0
  deadline="$(<"$limit_latch")"
  now="$(date +%s)"

  if [[ "$deadline" == <-> ]] && (( now < deadline )); then
    return 0
  fi

  rm -f "$limit_latch"
  print "$(utc_now) RESET: the usage-limit cleanup latch expired."
}

destroy_benchmark_instances() {
  local rows id label
  rows="$(benchmark_instances \
    | jq -r '.[] | [.id, .label] | @tsv' 2>/dev/null)" || {
    print "$(utc_now) ERROR: Vast.ai instance state is unavailable during cleanup."
    return 1
  }

  if [[ -z "$rows" ]]; then
    print "$(utc_now) LIMIT: no matching benchmark instance is active."
    return 0
  fi

  while IFS=$'\t' read -r id label; do
    if vastai destroy instance "$id" -y --raw >/dev/null 2>&1; then
      print -r -- "$(utc_now)\t$id\t$label" >> "$limit_log"
      print "$(utc_now) DESTROY: removed benchmark instance $id with label $label."
    else
      print "$(utc_now) ERROR: failed to remove benchmark instance $id with label $label."
    fi
  done <<< "$rows"
}

usage_limit_guard_once() {
  local instance_count instance_status target_state

  expire_limit_latch_if_due

  if claude_usage_limit_detected; then
    activate_limit_latch "Claude reached a usage limit."
  fi

  instance_count="$(benchmark_instance_count)"
  instance_status=$?
  if (( instance_status != 0 )); then
    print "$(utc_now) ERROR: Vast.ai instance state is unavailable during the limit check."
    return 1
  fi

  if (( instance_count > 0 )); then
    target_state="$(agent_state "$target_agent")"
    if [[ "$target_state" == "working" ]]; then
      nonworking_polls=0
    else
      (( nonworking_polls += 1 ))
      if (( nonworking_polls >= nonworking_poll_limit )); then
        activate_limit_latch \
          "Claude was $target_state for $nonworking_polls checks while a benchmark rental was active."
      fi
    fi
  else
    nonworking_polls=0
  fi

  if [[ -e "$limit_latch" ]] && (( instance_count > 0 )); then
    destroy_benchmark_instances
  fi
}

usage_limit_guard() {
  while true; do
    usage_limit_guard_once
    sleep "$poll_seconds"
  done
}

controller_step() {
  local owner_state instance_count instance_status target_state prompt_file prompt_status

  if [[ -e "$complete_file" ]]; then
    print "$(utc_now) COMPLETE: Claude finished the benchmark queue."
    return 10
  fi

  owner_state="$(agent_state "$owner_agent")"
  instance_count="$(benchmark_instance_count)"
  instance_status=$?

  if [[ "$owner_state" == "working" || "$owner_state" == "blocked" ]]; then
    print "$(utc_now) WAIT: the existing Astro benchmark owner is $owner_state."
    return 0
  fi

  if (( instance_status != 0 )); then
    print "$(utc_now) WAIT: Vast.ai instance state is unavailable."
    return 0
  fi

  if (( instance_count != 0 )); then
    print "$(utc_now) WAIT: $instance_count existing benchmark instance is active."
    return 0
  fi

  if [[ -e "$limit_latch" ]]; then
    print "$(utc_now) WAIT: the Claude usage-limit latch is active."
    return 0
  fi

  target_state="$(agent_state "$target_agent")"
  if [[ "$target_state" == "working" ]]; then
    print "$(utc_now) WAIT: Claude is working."
    return 0
  fi
  if [[ "$target_state" == "blocked" ]]; then
    print "$(utc_now) BLOCKED: Claude requires user input. The watchdog sent no input."
    return 20
  fi
  if [[ "$target_state" != "idle" && "$target_state" != "done" ]]; then
    print "$(utc_now) WAIT: Claude state is $target_state."
    return 20
  fi

  if [[ -e "$started_file" ]]; then
    prompt_file="$resume_prompt"
    print "$(utc_now) PROMPT: resume after the usage-reset wait."
  else
    prompt_file="$initial_prompt"
    print "$(utc_now) PROMPT: start the Claude-owned benchmark queue."
    date -u +'%Y-%m-%dT%H:%M:%SZ' > "$started_file"
  fi

  if [[ ! -s "$prompt_file" ]]; then
    print "$(utc_now) ERROR: prompt file is missing or empty: $prompt_file"
    return 20
  fi

  herdr agent prompt "$target_agent" "$(<"$prompt_file")" \
    --wait --until working --timeout 10000
  prompt_status=$?

  if [[ -e "$complete_file" ]]; then
    print "$(utc_now) COMPLETE: Claude finished the benchmark queue."
    return 10
  fi

  target_state="$(agent_state "$target_agent")"
  if [[ "$target_state" == "working" ]]; then
    print "$(utc_now) WAIT: the prompt timed out while Claude was working."
    return 0
  fi
  if [[ "$target_state" == "blocked" ]]; then
    print "$(utc_now) BLOCKED: Claude requires user input. The watchdog sent no input."
    return 20
  fi

  if claude_usage_limit_detected; then
    activate_limit_latch "Claude reached a usage limit after a prompt."
    return 0
  fi

  print "$(utc_now) WAIT: Claude settled with status $prompt_status."
  print "$(utc_now) WAIT: the next unknown-state retry is in 600 seconds."
  return 20
}

main() {
  local step_status sleep_seconds
  parse_args "$@" || return $?
  set_state_paths
  mkdir -p "$state_dir"

  usage_limit_guard_once
  usage_limit_guard &
  guard_pid=$!

  stop_watchdog() {
    if (( guard_pid > 0 )); then
      kill "$guard_pid" 2>/dev/null
    fi
    return 130
  }

  trap 'if (( guard_pid > 0 )); then kill "$guard_pid" 2>/dev/null; fi' EXIT
  trap 'stop_watchdog; exit 130' INT TERM

  while true; do
    controller_step
    step_status=$?
    case "$step_status" in
      10)
        return 0
        ;;
      20)
        sleep_seconds=600
        ;;
      *)
        sleep_seconds="$poll_seconds"
        ;;
    esac
    sleep "$sleep_seconds"
  done
}

set_state_paths
if [[ "${WATCHDOG_TEST_SOURCE_ONLY:-0}" != "1" ]]; then
  main "$@"
fi
