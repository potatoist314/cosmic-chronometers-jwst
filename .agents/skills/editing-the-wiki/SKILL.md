---
name: editing-the-wiki
description: Use when you add or change text, a roadmap item, a caption or a figure on the Astro wiki (wiki/notes/, wiki/research/, wiki/analyses/).
---

# Edit one wiki page

Written from the priority-9 roadmap edit of 2026-09-21 (commit `05c8f1a`).
The version before that commit put every fact of the item into one paragraph of
`details` in `wiki/research/direction.md`. Liu Hao's words about it:
"jesus christ, this is BAD word vomit."
Rules are in `AGENTS.md`, `~/.claude/CLAUDE.md`, `wiki/AGENTS.md` and
`wiki/research/README.md`. Read them. Do not copy them here.

## Steps

1. **Read.** In `wiki/AGENTS.md`: "All pages: no agent commentary", "Result reporting"
   and "Page conventions". In `AGENTS.md`: "Repository and reproducibility conventions"
   and "Research result presentation". In `~/.claude/CLAUDE.md`: "Design work goes
   through the designer agent". For the roadmap or a record: `wiki/research/README.md`.
   Before reading direction or priorities, run `python3 scripts/sync_wiki_direction.py --read`.
   Save changes to `direction.md` through `--save` and its revision-checked JSON
   contract in `wiki/research/README.md`, never by direct file edits.
2. **Write the prose with Codex.** Put the facts and their source paths in a fact sheet. Then:
   ```
   codex exec -m gpt-6-astra -c model_reasoning_effort="low" -s read-only \
     -C "/Users/liuhao/Downloads/Astro project" -o <scratchpad>/<name>.md "<prompt>"
   ```
   His words (2026-09-10): "nothing i hate more than bloated ai slop wiki pages. get
   astra on light or medium effort to do any prose writing".
3. **Edit.** Change the source file in `wiki/notes/`, `wiki/research/` or
   `wiki/analyses/<slug>/`. Do not edit `wiki/public/`. Add one line to `wiki/index.md`
   for a new page. Append one entry to `wiki/log.md`.
4. **Check.**
   ```
   python3 wiki/build.py
   python3 wiki/tests/run_tests.py
   python3 -m unittest discover -s wiki/tests -p 'test_research.py'
   ```
   The build runs the length check. His words (2026-09-21): "a cheap check would be good."
   The check uses no model. It rejects a roadmap item of more than 30 words. It rejects
   a paragraph of more than 60 words. Make the text shorter. Do not bypass the check.
5. **Finish.** Commit only your paths. The pre-commit hook `scripts/wiki_prose_check.py` sends new wiki prose to Opus. On a fail, apply its rewrites and commit again. Only Liu Hao uses `SKIP_PROSE_CHECK=1`. Push to `absorption-mask`. The launchd agent
   `com.liuhao.astro-wiki-publish` publishes the change to `https://wiki.eclw.org/`.
