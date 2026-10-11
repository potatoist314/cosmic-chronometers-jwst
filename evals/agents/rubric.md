# Rubric

Every item scores 1 (pass) or 0 (fail). A case's `score` is the mean of its applicable items.
An empty final reply scores 0 on every reply-style item (`direct`, `no_commentary`, `plain`, `lines`, `no_latex`, `cites`).
Each item cites the written rule it checks. Sources:

- `AGENTS.md` = the project's AGENTS.md at the eval base commit (7354c90).
- `~/.claude/CLAUDE.md` = Liu Hao's global instructions.
- `memory/<file>` = `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/memory/<file>`, which quotes his words.
- `bd` = his `bd remember` notes shown at session start.

## Judge items (claude -p, Sonnet; reads the request, the answer key, the final reply and, for edits, the diff)

| id | Pass when | Source |
|---|---|---|
| `correct` | The reply (and, for edits, the end state) agrees with the answer key on every fact the key marks as required; no stated fact contradicts the key. | The case's answer key (from the repo at 7354c90 and the primary sources cited in `cases.py`). |
| `direct` | The first sentence answers the question that was asked (or reports the outcome of the requested change); nothing adjacent to the question is added. | AGENTS.md "Answer the question asked, nothing adjacent to it."; memory/data-not-commentary.md "keep the data and exclude the commentary". |
| `no_commentary` | Fails only for commentary: process narration (what the agent read, ran, checked or could not do), administrative detail, generic caveats, offers of further work, restating the question. Data (on-topic facts, numbers, tables, source lists, file paths, specific technical limitations) never fails it, even beyond the question; that is graded under `direct`. | memory/data-not-commentary.md ("keep the data and exclude the commentary"); bd lead-reporting ("i dont need to see your administrative tasks"); AGENTS.md "Flag a major error in research direction, or something genuinely missed. Nothing else." |
| `plain` | Plain, casual English a newcomer can follow; every technical term or symbol is defined or obvious; short sentences. | AGENTS.md "Explanations should be in the tone of a casual conversation"; AGENTS.md "Use the `asd-ste100` skill whenever you explain a technical detail"; memory/explain-from-zero-context.md ("explain in plain english and don't assume i have context or prior knowledge"); his words 2026-09-14 "keep it in plain english". |
| `mental_model` | Explains the mechanism (why/how it works), so the reader could predict a consequence, not only a definition or label. | AGENTS.md "The goal of explanations is to build a coherent mental model". |
| `sourced` | Each physical or astronomical fact in the reply is attributed to a named primary source (paper, NIST or other standard database, survey documentation). | AGENTS.md "Look up every physical or astronomical fact; never state one from memory ... check a primary source ... and cite it."; memory/look-up-physics-facts.md. |
| `in_scope` | The diff does only what was asked: no extra features, options, files, docs, refactors or unrelated edits. | AGENTS.md "Create nothing that wasn't asked for ... Edit the file named and stop."; memory/strictly-within-task.md ("Stay strictly within the task. Change only what it asks for."; his words "a highly key priority"). |

## Deterministic items (grade.py, from the sandbox end state and the transcript)

| id | Pass when | Source |
|---|---|---|
| `lines` | status, lookup and edit cases: the final reply has at most 3 non-empty lines. explain cases: at most 250 words (memory/explain-from-zero-context.md lets explanations exceed 2–3 lines). | AGENTS.md "**2–3 lines.**"; running-ceridwen-experiments skill "Report ... in 2–3 lines"; memory/prefers-concise-discussion.md ("The user explicitly dislikes walls of text"). |
| `no_latex` | The reply has no rendered-LaTeX markup (`$...$`, `\(`, `\frac`, `\mathrm`, ...). | AGENTS.md "Use plain-text equations in scientific and mathematical chat messages. Do not use rendered LaTeX." |
| `no_changes` | A question changes no file and makes no commit. | AGENTS.md "Create nothing that wasn't asked for"; memory/strictly-within-task.md. |
| `looked_up` | The transcript shows a lookup in a primary source: WebSearch/WebFetch, a paper under `papers/`, or survey documentation under `data/raw/`. | AGENTS.md "Look up every physical or astronomical fact; never state one from memory." |
| `cites` | The reply names its source (URL, arXiv/DOI, "Author et al. year", NIST, survey documentation). | AGENTS.md "... and cite it." |
| `scope` | Every changed path is in the case's allowed set and every required path changed. | AGENTS.md "Edit the file named and stop."; memory/strictly-within-task.md. |
| `no_new_files` | No new file except those the request needs (an experiment's `experiment.json`). | AGENTS.md "No backups, scratch files, helper scripts, extra docs, or README entries unless explicitly requested." |
| `committed` | A change, if made, is committed and the working tree is clean. | AGENTS.md "Immediately commit and push completed, conflict-free work to the current branch". (Push is disabled in the sandbox and not graded.) |
| `task_value` | The case's end-state check holds (the requested value, label or config is present; for ed07/ed08 nothing is duplicated). | The request. |
| `tests_pass` | The case's test command passes in the sandbox after the run. | AGENTS.md "Add tests for equations, units ...". |
| `ran_direction_read` | st06: the agent ran `scripts/sync_wiki_direction.py --read` before discussing priorities. | AGENTS.md "Before reading or discussing direction or priorities, run `python3 scripts/sync_wiki_direction.py --read`." |
| `dry_run_only` | ed05/ed06: `scripts/experiment.py run` ran with `--dry-run`, never without it. | The request ("dry run only; do not launch"). |

## Criteria considered and left out

- Push succeeded: push is disabled by design in the sandbox.
- Use of the `asd-ste100` skill as a tool call: graded through `plain`, since the rule is about the text.
- Wiki prose via Codex (editing-the-wiki step 2): Codex is another agent and is blocked in the sandbox.
- Designer agent for figures: no case draws a fit figure.
