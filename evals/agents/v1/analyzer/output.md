## Behaviour
Every reply carries most of what the agent found or did, not only the answer. After answering, the agent adds history ("what it was before"), fit results and priors from runs the question did not name, related options and files, comparisons with upstream, runtime and cost, and its own process (what it checked, which tests passed, what it did not trace). AGENTS.md says "Answer the question asked, nothing adjacent to it," but it never says what counts as adjacent. The agents research widely, and the `checking-ceridwen-state` output hands them history, tests and open questions for each entry. Nothing tells them to leave that material out of the reply.

Scores in the 11 train rows (the file has 11, not 12):
- **Worst:** st07 0.43, ex08 0.50, lk07 0.50, ed02 0.56, st02 0.57.
- **Best:** ex03 0.75, st08 0.71.
- **Item failures:** `direct` fails in 10 of 11 cases, and in 9 of those the judge's reason is "adds adjacent material". `no_commentary` fails in 8 of 11. `lines` fails in 5. Even the two best cases lose `direct` to small add-ons.

## Evidence
- **`traces/st07_rep0.json` (line 155), the worst case.** The answer is buried under the old reason, a citation detour and test history:
  > "The worry is mainly Hβ: a bit of emission sitting in the absorption trough makes the line look shallower, and the fit reads that as an older population (Trager+2000a, cited in `wiki/notes/weak-emission-quiescent.md`, puts 0.02 Å of infill at roughly 3% in age). Even your \"no emission\" sample cut lets blank catalogue EWs through…"
  
  > "The M1_210210 no-mask test moved nothing by more than about 1.7 half-widths, with a small positive residual left at [O III], which is what pushed things toward marginalising rather than masking."
  
  Judge: "The first sentence defends emission masking in general rather than saying that production notebooks no longer mask emission lines". The current state came last, which also cost `correct`.
- **`traces/ex08_rep0.json` (line 159).** The reply is 445 words, so `lines` failed. It ends with status, results, cost and a caveat:
  > "Where it differs from upstream: upstream's eline_marginal.py sat outside the fork's calibration…"
  
  > "Status: on by default since 30 Sep with the nebular grid and Ca mask. On M1_210210, turning it on moved mass-weighted age by -0.41 Gyr, cut the RMS pull … and cost about 2.3x the fit wall time. One caveat: the flat prior shifts ln Z by a constant per line…"
- **`traces/st02_rep0.json` (line 217).** It answers the question and then adds the history and the fit results:
  > "So it is enabled, and more than that it is decoupled: the old Kriek & Conroy law tied the bump to the slope via E_b = 0.85 − 1.9 δ … the Ca-masked and nebular arms landed around E_b ≈ 2–3.5 with δ ≈ −0.2"
- **`traces/lk07_rep0.json` (line 303).** The third bullet is adjacent:
  > "**In production it mostly washes out.** With `emission_line_marginalisation` on, each line in the spectrum gets a free flux >= 0, so LIER-like lines from old stars would be absorbed by the free amplitudes…"
- **`traces/lk06_rep0.json` (line 286).** It opens with process narration and adds production-prior remarks:
  > "Done looking things up. Here is the answer."
  
  > "So the production U(0, 6) prior has room, and the 8 to 10.5 values the M1_210210 wide arms found are off the chart."
- **`traces/lk01_rep0.json` (line 92).** It ends with process narration:
  > "I did not trace which Cloudy label produced the entry."
- **`traces/ed02_rep0.json` (line 128).** It reports administrative detail:
  > "Tests: the production test file has 31 passing and 8 failing, both with and without this change, so the change didn't break anything. `tests/test_dust_bump.py` couldn't run at all…"
- **`traces/ed04_rep0.json` (line 70).** It reports its own checks:
  > "The file now matches commit d4bc517 exactly and parses cleanly. I didn't re-run the plot."
- **Contrast, `traces/st08_rep0.json` (line 25), score 0.71.** It answers in the first clause and loses `direct` only to one added sentence:
  > "You run it with `python3 scripts/experiment.py run results/<slug>/experiment.json --gpu \"<GPU type>\"`."
- **Contrast, `traces/ex01_rep0.json` (line 74).** It loses `direct` to one tangent:
  > "There is also a separate static per-pixel `calibration=` array you can hand the likelihood…"

## Expected gain
All 11 train cases show the behaviour; each fails `direct` or `no_commentary`, and most fail both. The most a full fix could recover on the 11-case mean:

| Item | Cases failing | Ceiling on the mean |
|---|---|---|
| `direct` | 10 | +0.110 |
| `no_commentary` | 8 | +0.084 |
| `lines` (padding drives these) | 5 | +0.048 |
| **Total** | | **about +0.24** |

That is well above the ±0.08 noise floor. Some `direct` failures are close calls by the judge, so I expect about +0.08 to +0.12.

- **Guardrail on `correct`:** the last hunk bullet keeps every needed fact and puts the current state first. That should protect `correct` (st07's miss came from leading with the old reason).
- **Out of scope:** `plain` (jargon, about 0.10) is a separate behaviour and is left for a later round. The `committed` failures happened because the sandbox denied the commit, so this change does not touch them.

## Diff
```diff
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -23,6 +23,20 @@
 ## Answering style
 
 - **2–3 lines.** Answer the question asked, nothing adjacent to it.
+  - The first sentence is the answer (for a change: what changed). Nothing before it:
+    no note on what you looked up, no background, no analogy.
+  - Research wide, reply narrow. Before you send, test each sentence against the
+    literal question. Delete it unless it states part of the answer or its source.
+    Adjacent, so deleted: how the value got this way or what it was before; fitted
+    results when the question asks about a setting; runs, priors or options the
+    question did not name; related scripts, files or switches; comparisons with
+    upstream or other codes; runtime and cost; what to try next.
+  - No report of your own process: what you read, ran, checked or could not check,
+    tests that passed, "parses cleanly", "did not re-run". For a change, report the
+    change and whether it is committed and pushed. Add a check only if it failed, in
+    one clause.
+  - Keep every fact the question needs, with its source. If the thing asked about
+    has changed, its current state is the answer; lead with it, not with the old reason.
 - **Explanations should be in the tone of a casual conversation, not your default writing style**
 - **The goal of explanations is to build a coherent mental model**
 - Use plain-text equations in scientific and mathematical chat messages. Do not use rendered LaTeX.
--- a/.agents/skills/checking-ceridwen-state/SKILL.md
+++ b/.agents/skills/checking-ceridwen-state/SKILL.md
@@ -93,5 +93,9 @@
   saved. A directory without `charges.json` shows no amount. Its record gives the cost.
 - The command does not print `abandoned`. A record that stopped shows `stopped`. A
   branch shows the date of its last commit.
+- The output is for you, not for the reply. Answer from the entry the question names.
+  Leave its `built`, `changed`, other `tested` and `ran` lines, `open` questions and
+  findings out of the reply unless the question asks for them. `AGENTS.md`,
+  "Answering style", says what is adjacent.
 
 ## Related rules
```