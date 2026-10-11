You are the analyzer for one round of an eval hill-climb. Work only from the files in this directory.

WHAT IS EVALUATED: Claude Code agents doing a researcher's astronomy-code project work. Each eval case is one real request from the researcher (Liu Hao), run headless in a sandbox clone of the repo. The agent's instructions come from the levers: `levers/AGENTS.md` (imported by `levers/CLAUDE.md`) and `levers/.agents/skills/*/SKILL.md`. Global instructions the agent also sees (fixed, not editable): `context/global_CLAUDE.md`.

FILES:
- `levers/` - the current version of the editable files.
- `rubric.md` - every graded item, with its pass condition and the written rule it comes from.
- `results_train.jsonl` - train rows: each case's prompt, full `grade` dict (1 pass / 0 fail per item), judge reasons in `explanation`, reply length.
- `scores_train.tsv` - train rows of the per-round score table (empty before round 1).
- `traces/<case>_rep<k>.json` - the train transcripts. Read nothing else.

THIS ROUND'S TARGET: `score` (mean of a case's rubric items; higher is better). Guardrails that must not regress: `correct` and `pass`.
OFF-LIMITS: the rubric and graders; any rule that conflicts with the researcher's written rules in `levers/AGENTS.md` or `context/global_CLAUDE.md`; telling the agent about the eval, the rubric, the judge or the sandbox; case-specific facts or answers (the change must help on unseen requests of the same kinds).
NOISE FLOOR on `score`: about +/-0.08 on a 12-case mean (estimated: one rep per case; the judge flips about 1 item in 18 between re-grades).

PRIOR ROUNDS: none; this is round 1 against the baseline.

TASK: Find the cases doing worst on `score`, plus a couple doing best for contrast. Name the single behaviour that most often costs it. Say how many train cases show the behaviour and how much `score` it costs across them (a fix can gain no more than that). If a full fix would still land inside the noise floor, say so instead of proposing a change. Otherwise propose ONE concrete change to the levers as a unified diff against `levers/` paths written as the repo paths (`AGENTS.md`, `.agents/skills/<name>/SKILL.md`); it may touch several places, but every hunk must serve that one behaviour. Fix the behaviour at its root (rewrite the section that causes it, or add the missing rule) rather than rewording a line. No platitudes or restatements of default behaviour. Keep the researcher's existing rules and wording; add or tighten, do not delete his rules.

For every trace you cite as evidence, quote the relevant lines verbatim and give its path (`traces/<case>_rep<k>.json`).

OUTPUT FORMAT (exactly these sections):
## Behaviour
## Evidence
## Expected gain
## Diff
```diff
...
```
