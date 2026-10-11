# Agent eval: AGENTS.md and skills hill-climb, 2026-10-10/11

**Result: the one proposed edit (v1) did not measurably change scores. I recommend not adding it.**

| variant | val score | test score | train score |
|---|---|---|---|
| baseline (AGENTS.md and skills at 7354c90) | 0.683 ±0.081 (n=12, 1 trial) | 0.608 ±0.118 (n=9 of 12, 1 trial) | 0.649 ±0.107 (n=9 of 12, 1 trial) |
| v1 | 0.689 ±0.083 (n=12, 1 trial) | 0.561 ±0.185 (n=5 of 12, 1 trial) | not run |
| v1 − baseline, paired by case | **+0.006 ±0.036** (n=12) | **−0.043 ±0.276** (n=5) | |

- `score` is the mean of a case's rubric items (0 to 1). ± is the 95% t interval over cases.
- Guardrails on val: `correct` and `pass` are 12/12 at baseline and 11/12 with v1. The one loss (st05) is a borderline judge call. The judge's reason says the formula "actually agrees" with the key, but it failed the reply for not naming the key's notebook and grid file.
- Per-case detail and traces: `report.html` and `trajectory/scores.tsv`. Running summary: `narrative.md`. Every decision and its reason: `_state.json` → `decisions`.

## Proposed edits

These are proposals only. The branch's own AGENTS.md and skills are unchanged. Each one enters only if you say "add N". Edits 1 and 2 were measured together as v1. Exact diff: `v1/change.patch`. Full files after the change: `v1/levers/`.

1. **AGENTS.md, "Answering style": add four sub-bullets under "2–3 lines."**
   - They require the answer in the first sentence.
   - They give a test for each sentence, with a list of what counts as adjacent: history, fitted results when asked about a setting, runs, priors or options the question did not name, related files, comparisons with upstream, runtime and cost, next steps.
   - They forbid reporting your own process.
   - They require leading with the current state.
   - Rule it serves: AGENTS.md "Answer the question asked, nothing adjacent to it."; memory/data-not-commentary.md.
   - Measured delta (with 2): val **+0.006 ±0.036** (n=12, 1 trial); test **−0.043 ±0.276** (n=5, 1 trial).
   - Recommendation: **do not add**.
2. **`.agents/skills/checking-ceridwen-state/SKILL.md`: add one bullet.** "The output is for you, not for the reply. Answer from the entry the question names. Leave its `built`, `changed`, other `tested` and `ran` lines, `open` questions and findings out of the reply unless the question asks for them."
   - Rule it serves: same as 1.
   - Measured delta: same run as 1.
   - Recommendation: **do not add**.

Why the null result is real and not a wiring fault:

- The variant AGENTS.md reached the agents. Both variants run `scripts/sync_wiki_direction.py --read` on st06, and only AGENTS.md states that rule. The v1 skill text appears in the v1 traces.
- The behaviour v1 targeted did not move on the 17 cases both variants ran:
  - Mean reply length: 186 words at baseline, 201 with v1. The paired geometric-mean word ratio is 0.99.
  - `direct`: 0/17 in both.
  - Replies that open with a process line ("I have the sources now. Writing the answer."): 5/26 at baseline, 4/17 with v1.

## Stop reason

**Quota.** The runs stopped at 09:20 BST.

- The shared claude 5 h window fell below the merge swarm's 25% reserve at about 08:40. It was at 7% at 09:20.
- It resets at 12:50, after the 11:00 stop time the lead set at 03:30. That decision moved the original 08:00 stop to 11:00 and raised the weekly floor from 30% to 40%.
- Weekly was at 50% at the stop, above the 40% floor.

Completed: val 12/12 for both variants. Test: baseline 9/12, v1 5/12. Train: baseline 9/12 and v1 not run. Baseline ed02 and ed04 hit the old push-deny harness fault; ed03 was never run.

## How it was measured

- **Cases (`cases.py`):** 36 of your own Astro-project requests, each with its source session and an answer key from the repo at 7354c90 or a cited primary source. There are 9 each of status, explain, lookup and edit.
- **Split:** train/val/test 12/12/12, stratified by kind, seed 20261010. The analyzer that wrote v1 read only train traces. Val and test are held out from it.
- **Runner (`run.py`, `sandbox.py`):** `claude -p` runs in a copy-on-write clone of the repo at 7354c90 with the variant's AGENTS.md, CLAUDE.md and skills.
  - Settings: `--permission-mode auto` (your default), effort xhigh. Edit cases use Opus; other cases use Fable.
  - The Claude Code Bash sandbox blocks network access and writes outside the clone.
  - Push is disabled twice: the remote push URL is `DISABLED`, and git `pushInsteadOf` maps every URL form to a non-existent local path. The agent-messaging, Vast, herdr, codex and bridge commands are denied, and hooks are off.
  - Checked: on ed06 the agent's `git commit && git push` committed, and the push failed with "Please make sure you have the correct access rights".
- **Grading (`grade.py`, `rubric.md`):** each item cites the written rule it checks (AGENTS.md, your global CLAUDE.md, memory files, `bd` notes).
  - Deterministic items: line count, no LaTeX, scope, new files, committed, end-state value, tests, dry run only, lookup and citation.
  - Judge items (Sonnet, tools off, JSON schema): `correct`, `direct`, `no_commentary`, `plain`, `mental_model`, `sourced`, `in_scope`.
- **Judge checks (`metrics.md`):**
  - It fails 12/12 planted empty, "I don't know" and wrong replies on `correct`.
  - It agrees with hand labels on 52/60 items: `correct` 13/13, `direct` 11/13, `no_commentary` 10/13, `plain` 11/12, `mental_model` 4/4, `in_scope` 1/1, `sourced` 2/4.
- **Spend:** $62.81 list-price equivalent over 51 runs (4 pilot, 30 baseline, 17 v1), as reported by `claude -p`. All of it was billed to the Claude subscription. There were no API-key calls, no GPU and no paid steps, so the caps file (`usd: 0`) was respected.
- **Failures and harness faults:**
  - 4 baseline attempts are in `baseline/errors.jsonl`:
    - st02 and ex08: the judge timed out at an empty 5 h window. Both were re-run.
    - ed02 and ed04: a compound commit-and-push was denied by the old `Bash(git push:*)` rule, which was then replaced by the git-level block.
  - One grader bug was fixed after the runs. `dry_run_only` counted `experiment.py run --help` as a launch. It was recomputed from the traces for both variants (ed06 only).
  - The sandbox lacks the `external/fsps` submodule. The v1 agent on ed06 restored the file it needed from the main checkout with read-only `git show`. The baseline agent stopped and reported the missing file.

## Before and after (val)

- **lk08, "what's illustris? … more concise and self contained":** 176 → 131 words, `no_commentary` 0 → 1. Both open with an analogy ("Think of a cube of the universe about 106 Mpc on a side …" / "Picture a cube of universe about 100 Mpc on a side …"). Both add the Leja et al. continuity-prior link that the question did not ask for.
- **ed06, Noll rerun with broader priors, dry run only:** 239 → 182 words, `lines` 0 → 1.
  - Baseline opens: "I've set up the run, but the dry run didn't finish."
  - v1 opens: "I've set up the M1_210210 rerun with wider Noll priors and the dry run passes. Nothing was launched."
  - Both then add the 2026-09-29/30 fit results unasked.
- **ex02, "chebyshev polynomial … marginalised analytically":** 204 → 232 words, `no_commentary` 1 → 0. v1 drops the analogy and leads with the formula. It is longer and cites a docstring path mid-explanation.

## What I'd try next

1. **Make `direct` and `plain` finer.** Both are 0 in every val and test case in both variants. A pass/fail item stuck at 0 cannot show a change. Grade the number of adjacent sentences and undefined terms per reply instead, and re-check it against hand labels.
2. **Add `external/fsps` to `sandbox.SUBMODULES`**, so the dry-run cases (ed05, ed06) start from the same state as your checkout.
3. **Use 3 trials on val** before judging a rule change. At 1 trial the paired noise is ±0.036 on val.
4. **Lever ideas still open:**
   - Undefined jargon (`plain`: 0 on val and test, 1/9 on baseline train).
   - The process-line opening, about 1 reply in 5 in both variants. The v1 rule "nothing before it" did not stop it.
