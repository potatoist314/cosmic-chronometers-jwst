# Agent eval round 2: is the research work right? 2026-10-12

**Result: on val, Sonnet 5.5 and effort high gave the same outcomes as the baseline, for less cost and time. The baseline was already right on every val run, so these cases cannot show a gain in correctness.**

- **What is scored.** 36 of your real requests: experiment configs, planted-bug fixes, figure fixes, setting and rule edits, numbers from fit results, and lookups.
  - Outcome is graded first: hidden tests, the grader's own `experiment.py run --dry-run` on the agent's config, regex checks on the numbers, and a validated judge for correctness.
  - Rule compliance is a separate score.
- **Baseline.** Your routing: Opus 5.5 xhigh for coding cases, Fable 5.1 xhigh for lookups, with the base commit's AGENTS.md and skills.
  - On val, 3 trials of 12 cases: outcome, pass and rules are 1.000 on 36/36 runs.
- **Levers.** Each lever changes one thing other than instruction wording.
  - Model: Sonnet 5.5 for every case, all 12 val cases × 3 trials.
  - Effort: high instead of xhigh, 4 val cases × 3 trials before the quota floor.
  - Not run: a review turn (workflow), and Fable for every case (model).
- **Stop: quota limit, not the end state.** Weekly reached the lead's floor of 85% left at 19:30.

| lever (val, paired by case) | cases × trials | Δ score | Δ pass | Δ rules | Δ adjacent sentences | Δ undefined terms | Δ list cost per run | Δ latency per run | Δ tool calls per run |
|---|---|---|---|---|---|---|---|---|---|
| Sonnet 5.5 for every case | 12 × 3 | **+0.000 ±0.000** | +0.000 ±0.000 | +0.000 ±0.000 | **+1.03 ±0.77** | +0.83 ±1.00 | **−$0.41 ±0.19** | **−69 ±56 s** | −0.8 ±1.3 |
| effort high (not xhigh) | 4 × 3 | **+0.000 ±0.000** | +0.000 ±0.000 | +0.000 ±0.000 | −0.33 ±2.56 | +0.00 ±3.33 | −$0.21 ±0.33 | −64 ±70 s | **−4.8 ±4.0** |
| review turn after the answer | not run | | | | | | | | |
| Fable 5.1 for every case | not run | | | | | | | | |

- Δ = lever − baseline, averaged over trials within each case, then averaged over cases. ± is the 95% t interval over cases. **Bold** marks a Δ on outcome, or a Δ whose interval excludes 0.
- Effort high covers cf03, cf01, ed02 and ed09. fg03 has 2 effort-high trials, outside the table; both had outcome 1.00.
- Sonnet's list cost is $0.32 per run against $0.73: 57% less. Its replies are longer: 161 words against 129.

## Proposals

These are proposals only. Nothing in AGENTS.md, the skills, the hooks or the routing has changed. Each one enters only if you say "add N".

1. **Finish the levers: after the weekly reset on Mon 19 Oct at 03:59, or with more quota.**
   - Effort high: 22 runs left, about $13 list, about 2–2.5 weekly points.
   - Review turn: 36 runs at no less than the baseline's cost, so at least $27, about 5 points.
   - Fable for every case: draws on the Fable weekly pool. Not estimated.
   - Rate measured this round: 0.15 to 0.2 weekly points per list dollar.
2. **Make val hard enough to show a gain or a loss in correctness.**
   - Baseline, Sonnet and effort high pass every val run they made. On these cases, a cheaper setting can only prove it is cheaper.
   - Proposed case changes:
     - Fixtures with two planted errors, one of them outside the file the prompt names.
     - Prompts without the file, arm or function name.
     - Number cases that need two result files.
   - Keep a new case only if baseline fails it on at least 1 of 3 trials.
   - Not measured.
3. **Make the gate count only this worker's own runs.**
   - The lead's decision: the cap counts own runs only. The gate still reads the shared weekly counter, so other sessions' use during a run still counts.
   - Proposed method:
     - Take the list cost that `claude -p` reports for each run and judge call.
     - Convert it at 0.15–0.2 points per dollar.
     - Stop at 12 points.
   - Not measured.
4. **Route coding requests (config, fix, figure, edit) to Sonnet 5.5.**
   - Measured: outcome identical on 36/36 runs, list cost −57%, latency −69 ±56 s.
   - Against it: +1.0 ±0.8 adjacent sentences per reply, which breaks the AGENTS.md rule "Answer the question asked, nothing adjacent to it". Replies are 25% longer.
   - **Recommendation: not yet.** Val cannot show a correctness loss on hard work, because both settings pass every case. Run 2 first.
5. **Use effort high instead of xhigh for config and edit requests.**
   - Measured on cf03, cf01, ed02 and ed09: outcome identical, −4.8 ±4.0 tool calls and −4.8 ±4.3 turns per run. Cost −$0.21 ±0.33 and latency −64 ±70 s are within noise.
   - **Recommendation: wait for 1.** Four cases are too few.

## Lever results in full (val)

| metric | baseline, 12 cases | Sonnet, 12 cases | Δ | baseline, effort-high's 4 cases | effort high, 4 cases | Δ |
|---|---|---|---|---|---|---|
| score (outcome) | 1.000 | 1.000 | +0.000 ±0.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| pass | 1.000 | 1.000 | +0.000 ±0.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| rules | 1.000 | 1.000 | +0.000 ±0.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| adjacent sentences per reply | 4.36 | 5.39 | +1.03 ±0.77 | 4.83 | 4.50 | −0.33 ±2.56 |
| undefined terms per reply | 4.72 | 5.56 | +0.83 ±1.00 | 5.75 | 5.75 | +0.00 ±3.33 |
| list cost per run | $0.73 | $0.32 | −$0.41 ±0.19 | $0.77 | $0.57 | −$0.21 ±0.33 |
| latency per run | 175 s | 106 s | −69 ±56 s | 175 s | 111 s | −64 ±70 s |
| turns per run | 14.8 | 14.3 | −0.4 ±1.7 | 18.9 | 14.1 | −4.8 ±4.3 |
| tool calls per run | 13.9 | 13.1 | −0.8 ±1.3 | 17.3 | 12.5 | −4.8 ±4.0 |

Sonnet − baseline by kind, 2 val cases each, trial-averaged:

| kind | cases | Δ adjacent | Δ undefined | Δ list cost | Δ latency | words, baseline → Sonnet |
|---|---|---|---|---|---|---|
| config | cf03, cf01 | +0.8 | +1.8 | −$0.45 | −33 s | 170 → 198 |
| edit | ed02, ed09 | +0.7 | −0.7 | −$0.25 | −35 s | 105 → 133 |
| figure | fg03, fg01 | +1.5 | +0.7 | −$0.37 | −24 s | 128 → 180 |
| fix | fx02, fx01 | +2.0 | +2.8 | −$0.27 | −101 s | 145 → 197 |
| lookup | lk09, lk05 | +1.2 | +0.0 | −$0.88 | −188 s | 90 → 127 |
| number | nm01, nm06 | +0.0 | +0.3 | −$0.26 | −34 s | 136 → 129 |

Effort high − baseline per case, trial-averaged:

| case | request | Δ tool calls | Δ list cost | Δ latency | Δ adjacent | Δ undefined |
|---|---|---|---|---|---|---|
| cf03 | default settings on the ~10-galaxy test set; dry run only | −4.7 | −$0.13 | −52 s | +1.0 | +2.3 |
| cf01 | Noll rerun with broader priors; dry run only | −8.3 | −$0.52 | −129 s | −2.7 | −0.3 |
| ed02 | birth-cloud dust on by default | −3.3 | −$0.08 | −44 s | +0.0 | +0.7 |
| ed09 | keep bandwidth cost below $5/TB, as a rule | −2.7 | −$0.10 | −32 s | +0.3 | −2.7 |

- Rows: `r2/<variant>/results.jsonl`. Traces: `r2/<variant>/traces/`. Diffs: `r2/<variant>/out/`.
- Every decision and its reason: `r2/_state.json` → `decisions`.
- Both arms of each comparison were scored by the same judge. On hand labels, the judge counts 1.25 more adjacent sentences than I do, so the absolute counts are high. The paired Δ is less affected.

## How it was scored

- **Cases (`cases_r2.py`).** There are 36 cases. Each one has its source session and an answer key: either the repo at 7354c90, or a cited primary source.

  | kind | n | outcome items (score, pass) | rule items (rules) |
  |---|---|---|---|
  | config (cf) | 6 | `config_ok`, `dry_run_ok`, `dry_run_only` | `committed`, `no_latex`, `no_new_files`, `scope` |
  | fix a planted bug (fx) | 6 | `hidden_tests`, `repo_tests` | as config, plus `no_test_weakening` |
  | figure (fg) | 5 | `hidden_tests`, `repo_tests` | as fix |
  | setting or rule edit (ed) | 6 | `correct`, `task_value`, `tests_pass` | as config |
  | numbers from fit results (nm) | 6 | `correct`, `numbers` | `no_changes`, `no_latex` |
  | lookup (lk) | 7 | `correct`, `cites`, `looked_up` | `no_changes`, `no_latex` |

- **Split.** Train, val and test have 12 cases each. They are stratified by kind, with seed 20261012.
- **Scores.**
  - `score` is the mean of the outcome items. It is the headline number.
  - `pass` is 1 only when every outcome item is 1.
  - `rules` is the mean of the rule items.
  - Two judge counts replace round 1's `direct` and `plain`, which were 0 on every case: adjacent sentences and undefined terms per reply.
- **Planted bugs (`fixtures.py`).** Each fixture inverts one correct line of the base commit and commits it as an ordinary refactor. For example, `obs / (1 + zred)` becomes `obs * (1 + zred)` in the rest-frame axis, and `mag - 23.9` becomes `mag + 48.6` in the µJy conversion.
- **Hidden tests (`hidden/`).**
  - Only the grader has these tests. Their answer keys never enter the sandbox, because the template is a single-branch clone.
  - Checked on 2026-10-12 for the 10 planted-bug cases (fx01–fx06, fg02–fg05): each test passes on the unchanged code and fails with its bug planted.
  - fg01 has no planted bug. It asks for points instead of bars, and its test fails on the unchanged code, where the plot still uses bars.
- **Config grading.** The grader runs its own `experiment.py run --dry-run` on the agent's committed config. It then checks the arms and the settings against the key.
- **Judge.** Sonnet with tools off and a JSON schema. It grades `correct` as pass/fail and gives the two counts.
  - Negatives: it gives `correct = 0` to 12/12 planted bad replies (empty, "I don't know", and wrong numbers or facts) on lk05, lk09, nm01 and nm06. File: `r2/judge_negatives.json`.
  - Hand labels on the 12 judged baseline val rows:
    - `correct` agrees on 12/12 (9/12 before the nm06 key fix below).
    - Adjacent sentences agree within 1 on 8/12. The judge counts 1.25 more on average.
    - Undefined terms were not hand-checked.
    - I made these labels myself; none are yours. File: `r2/judge_agreement.json`.

## Harness

- **Sandboxes.** `claude -p` runs in an APFS copy-on-write clone of the repo at 7354c90.
  - Settings: `--permission-mode auto` and the eval settings file. Hooks are off and push is disabled, as in round 1.
  - The served model is recorded on every run. Sonnet rows served `claude-sonnet-5-5`, plus `claude-haiku-5-5` on some runs, as in the baseline. Effort-high rows served `claude-opus-5-5` at effort `high`.
- **Submodule fix (step 4, done).** `external/fsps` was added to `sandbox.SUBMODULES`. In round 1 its absence stopped the baseline agent on ed06.
- **Levers (`r2/<variant>/variant.json`).** Each lever sets a models map, an effort, a review flag and a template.
  - The review lever resumes the same session for one review turn after the answer, as a blocking Stop hook would.
- **Grader fixes after the baseline run.** All were applied to every recorded row with `run.py --regrade` before any lever ran.
  1. `no_latex` no longer fires on currency such as "$5/TB … $10/TB" (ed09, 2 rows). Round-1 replies grade the same with the old and new pattern.
  2. ed09 `scope` also allows `BENCHMARK_CHECK.md` and `scripts/validate_ceridwen_speedups.py`, which state the same bandwidth limit.
  3. The graded reply is now every assistant message after the last tool result, not only the final result event. In lk09 rep 0, the final event held only a one-line note written after a background task ended.
  4. **The nm06 key was changed after the results were seen.**
     - The judge failed all 3 baseline replies, but hand labels marked all 3 right. The key had not said which facts were required.
     - The key now requires the `afe` and `Z` shifts in `comparison.csv` (0.129 → 0.149 and −0.160 → −0.189). The other values it lists are optional.
     - Every Sonnet nm06 row was judged with the fixed key.

## Stop reason

**Quota limit.** The cap is 12 points of the Claude weekly quota, counted on this worker's own runs (lead decision, 19:00). 25% of the 5 h window is kept free for other work.

| time (BST) | 5 h left | weekly left | Fable weekly left | event |
|---|---|---|---|---|
| 13:41 | 93% | 99% | 100% | start |
| 14:44 | 33% | 92% | 97% | baseline val ×3 finished |
| 14:53 | 19% | 91% | 97% | Sonnet paused at 10/36 runs: 5 h window below the 25% reserve |
| 18:52 | 96% | 88% | 97% | after the 5 h reset; 3 points used by other sessions while this worker was idle |
| 19:00 | | | | lead: idle use by other sessions does not count; floor is now 85% |
| 19:15 | 80% | 87% | 97% | Sonnet val ×3 finished (36/36) |
| 19:30 | 67% | 85% | 97% | effort high stopped at the floor after 14 runs |

- Own spend: 99% → 91% before the pause, and 88% → 85% after it. That is 11 points, including this session's own use.
- **Spend:** $47.96 list-price equivalent, agent plus judge, for 86 recorded runs: baseline $26.92, Sonnet $12.09, effort high $8.95.
  - Not counted in that figure: the 2 Sonnet runs killed at 14:53.
  - All of it was billed to the Claude subscription. There were no API-key calls, no GPU and no paid steps, so the caps file (`usd: 0`) was respected.

## Round 1 (2026-10-10/11)

- Round 1 tested one instruction-wording edit, v1, to AGENTS.md "Answering style" and the checking-ceridwen-state skill.
- It was within noise: val +0.006 ±0.036 (n = 12, 1 trial). Recommendation: do not add.
- Full report: `git show 2587556:evals/agents/REPORT.md`. Files: `cases.py`, `baseline/`, `v1/`, `metrics.md`, `narrative.md`.
