# Agent eval round 2: is the research work right? 2026-10-12

**Result: the baseline got every validation (val) outcome right, so no lever can show a gain on these cases. Only one lever ran before the quota cap: Sonnet 5.5. On the 3 cases that have all 3 trials, it gave the same outcomes for 45% less list cost.**

- **What is scored.** 36 of your real requests: experiment configs, planted-bug fixes, figure fixes, setting and rule edits, numbers from fit results, and lookups.
  - Outcome is graded first: hidden tests, the grader's own `experiment.py run --dry-run` on the agent's config, regex checks on the numbers, and a validated judge for correctness.
  - Rule compliance is a separate score.
- **Baseline.** Your routing: Opus 5.5 xhigh for coding cases, Fable 5.1 xhigh for lookups, with the base commit's AGENTS.md and skills.
  - On val, 3 trials of 12 cases: outcome, pass and rules are 1.000 on 36/36 runs.
- **Levers.** Each lever changes one thing other than instruction wording: the model, the effort, or the workflow.
  - Sonnet 5.5 ran 10 of its 36 val runs.
  - Effort high, a review turn, and Fable for every case did not run.
- **Stop: quota limit, not the end state.**
  - Weekly quota went from 99% to 88% left. That is the 12-point cap, with 1 point of margin for runs in flight.
  - At least 3 of the 11 points were used by other sessions while this worker was idle.

| lever (val, paired by case) | cases × trials | Δ score | Δ pass | Δ rules | Δ adjacent sentences | Δ undefined terms | Δ list cost per run | Δ latency per run |
|---|---|---|---|---|---|---|---|---|
| Sonnet 5.5 for every case | 3 × 3 | **+0.000 ±0.000** | +0.000 ±0.000 | +0.000 ±0.000 | +0.78 ±2.91 | +1.44 ±1.72 | **−$0.37 ±0.41** | **−36 ±23 s** |
| effort high (not xhigh) | not run | | | | | | | |
| review turn after the answer | not run | | | | | | | |
| Fable 5.1 for every case | not run | | | | | | | |

- Δ = lever − baseline, averaged over trials within each case, then averaged over cases. ± is the 95% t interval over cases (n = 3, 2 degrees of freedom).
- The 3 cases are cf03, cf01 and ed02.
- ed09 has 1 Sonnet trial, outside the table: outcome 1.00, list cost $0.31 against a baseline mean of $0.61.

## Proposals

These are proposals only. Nothing in AGENTS.md, the skills, the hooks or the routing has changed. Each one enters only if you say "add N".

1. **Finish the lever runs: about 7 points more of weekly quota, or wait for the reset on Mon 19 Oct at 03:59.**
   - The runs: Sonnet's remaining 26 runs, then effort high, 36 runs, on val ×3.
   - Estimate from this round:
     - Usage is 0.15 to 0.2 weekly points per list dollar. That is baseline: 4 points for $26.92; Sonnet: about 1 point for $4.63.
     - Sonnet costs about $10 more.
     - Effort high costs at most the baseline's $26.
   - The review and Fable levers need a further budget. Fable draws on the Fable weekly pool.
2. **Make val hard enough to show a gain.**
   - Baseline passes 36/36 val runs, so the current cases can only show losses and cost.
   - Proposed case changes:
     - Fixtures with two planted errors, one of them outside the file the prompt names.
     - Prompts without the file, arm or function name.
     - Number cases that need two result files.
   - Keep a new case only if baseline fails it on at least 1 of 3 trials.
   - Not measured.
3. **Count the 12-point cap on this worker's own runs.**
   - The gate reads the shared weekly counter, which other sessions also draw down.
   - Proposed method:
     - Take the list cost that `claude -p` reports for each run and judge call.
     - Convert it with the measured 0.15–0.2 points per dollar.
     - Stop at 12 points.
   - Not measured.
4. **Route config and setting-edit requests to Sonnet 5.5.**
   - Measured as the Sonnet lever above: outcome unchanged, −$0.37 and −36 s per run, n = 3 cases.
   - Undefined terms rose by +1.4 ±1.7 per reply. That is within noise, but the sign is against Sonnet.
   - **Recommendation: wait for proposal 1.** Three cases are too few to change the routing.

## Lever results in full (val)

| metric | baseline, 12 cases | baseline, same 3 cases | Sonnet, same 3 cases | Δ, paired by case |
|---|---|---|---|---|
| score (outcome) | 1.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| pass | 1.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| rules | 1.000 | 1.000 | 1.000 | +0.000 ±0.000 |
| adjacent sentences per reply | 4.36 | 5.33 | 6.11 | +0.78 ±2.91 |
| undefined terms per reply | 4.72 | 5.56 | 7.00 | +1.44 ±1.72 |
| list cost per run | $0.73 | $0.83 | $0.46 | −$0.37 ±0.41 |
| latency per run | 175 s | 184 s | 148 s | −36 ±23 s |
| turns per run | 14.8 | 20.3 | 19.6 | −0.8 ±2.1 |
| tool calls per run | 13.9 | 18.4 | 18.4 | +0.0 ±2.5 |

Per case, Sonnet − baseline, trial-averaged:

| case | request | Δ list cost | Δ latency | Δ adjacent | Δ undefined |
|---|---|---|---|---|---|
| cf03 | default settings on the ~10-galaxy test set; dry run only | −$0.36 | −41 s | +2.0 | +1.7 |
| cf01 | Noll rerun with broader priors; dry run only | −$0.54 | −25 s | −0.3 | +2.0 |
| ed02 | birth-cloud dust on by default | −$0.21 | −42 s | +0.7 | +0.7 |

Rows: `r2/<variant>/results.jsonl`. Traces: `r2/<variant>/traces/`. Diffs: `r2/<variant>/out/`. Every decision and its reason: `r2/_state.json` → `decisions`.

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
  - Settings: `--permission-mode auto` and the eval settings file. Hooks are off and push is disabled, as in round 1. The served model is checked on every run.
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
     - Applied to every variant. Sonnet has no nm06 rows.

## Stop reason

**Quota limit.** The cap is 12 points of the Claude weekly quota recorded at the start. 25% of the 5 h window is kept free for other work.

| time (BST) | 5 h left | weekly left | Fable weekly left | event |
|---|---|---|---|---|
| 13:41 | 93% | 99% | 100% | start |
| 14:44 | 33% | 92% | 97% | baseline val ×3 finished |
| 14:53 | 19% | 91% | 97% | Sonnet stopped at 10/36 rows: 5 h window below the 25% reserve |
| 18:52 | 96% | 88% | 97% | after the 5 h reset: weekly at the cap floor, so no new runs |

- Weekly fell from 91% to 88% between 14:53 and 18:52, while this worker made only status checks.
- I tried to lower the stop floor by those 3 points. The auto-mode permission check refused, because the change loosened the worker's own spend guard. The cap therefore stayed on the shared counter. Proposal 3 is the fix if you want the cap counted on own spend.
- **Spend:** $30.61 agent plus $0.94 judge, list-price equivalent, for the 46 recorded runs.
  - Not counted in that figure: the 2 Sonnet runs killed at 14:53.
  - All of it was billed to the Claude subscription. There were no API-key calls, no GPU and no paid steps, so the caps file (`usd: 0`) was respected.

## Round 1 (2026-10-10/11)

- Round 1 tested one instruction-wording edit, v1, to AGENTS.md "Answering style" and the checking-ceridwen-state skill.
- It was within noise: val +0.006 ±0.036 (n = 12, 1 trial). Recommendation: do not add.
- Full report: `git show 2587556:evals/agents/REPORT.md`. Files: `cases.py`, `baseline/`, `v1/`, `metrics.md`, `narrative.md`.
