# Astro Research Wiki

This directory is an LLM-maintained guide to the Astro project codebase.
Codex writes and maintains it autonomously so the user can learn to read the
code; the user still chooses research direction and scientific methodology.

## Boundaries

- Treat project code, notebooks, `papers/`, `data/raw/`, submodules, and
  user-designated sources as read-only evidence during wiki-only work.
- Store only generated knowledge pages inside `wiki/`.
- Never copy, rename, edit, or delete evidence during wiki work.
- Never treat a wiki summary as stronger evidence than its raw source.
- Separate sourced claims, project inferences, and unresolved questions.
- Do not perform web research unless the user requests it.
- Record uncertainty instead of guessing why code was written.

## Structure

- `index.html` is the human-facing entry point.
- `index.md` is the compact agent catalog of every reader page.
- `overview.html` holds the current cross-source synthesis.
- `log.md` is an append-only history of wiki operations.
- `guides/` holds ordered learning and code-reading paths.
- `codebase/` explains architecture, modules, tests, and execution flows.
- `notebooks/` explains notebook roles and their relationship to modules.
- `sources/` holds one evidence-focused page per ingested source.
- `concepts/` holds scientific ideas synthesized across sources.
- `methods/` holds models, measurements, and analysis procedures.
- `datasets/` holds provenance, selection, columns, and limitations.
- `analyses/` holds user-requested comparisons and derived arguments.

Create category directories only when their first page is needed. Human-facing
pages use short, lowercase, hyphenated `.html` filenames and normal relative
HTML links. Agent-only schema, catalog, log, and persistent-memory files may
remain Markdown. Keep shared presentation rules in `assets/wiki.css`.

## Page conventions

- Write terse, factual prose. Remove filler, scene-setting, conclusions, and
  repeated explanations.
- Do not use promotional copy, rhetorical questions, or prompts such as
  “Read it.”
- Keep navigation labels literal. Prefer short lists over cards and callouts.
- Add a reading exercise only when the user requests one.

Each generated HTML page must include:

```html
<meta name="wiki-type" content="codebase">
<meta name="wiki-status" content="current">
<meta name="wiki-updated" content="YYYY-MM-DD">
```

- Record source pages and inspected paths in visible `Evidence` sections when
  they help a reader verify the explanation.
- Cite raw files with a page, section, figure, table, or row locator.
- Cite code with `path:line` and name the relevant class or function.
- Cite notebooks by filename, heading, and function or variable name.
- Label uncited interpretation explicitly as `Project synthesis`.
- Record conflicting claims together; do not silently choose one.
- Link the first meaningful mention of another wiki page.
- Prefer revising an existing page over creating a near-duplicate.
- Keep summaries concise and preserve uncertainty and scope.

Code pages must show short, exact source snippets with file and line locators,
then explain each snippet in plain language. Use only sections that improve
understanding.

## Autonomous codebase workflow

1. Read `index.md`, `overview.html`, and relevant existing pages.
2. Inspect the live working tree; do not rely on stale notebook outputs.
3. Work from public entry points toward internal implementation details.
4. Explain one execution path at a time with exact source locators.
5. Update existing pages when behavior changes; avoid duplicate summaries.
6. Update `index.md`; append one `codebase` entry to `log.md`.
7. Check changed links, locators, contradictions, and duplicate pages.

The maintained codebase and notebooks are a standing authorized source corpus.
Process coherent groups autonomously without requesting per-file approval.
Exclude virtual environments, caches, generated outputs, and raw data payloads.

## Query workflow

1. Read `index.md`, then only the pages relevant to the question.
2. Consult raw sources when the wiki lacks evidence or precision.
3. Answer with links to wiki pages and exact raw-source locators.
4. Distinguish established evidence from project synthesis.
5. Add durable code explanations to the wiki autonomously when they improve an
   existing page; create a new analysis page only when the user requests it.
6. Update `index.md` and append a `query` entry when pages change.

## Lint workflow

Check for broken links, orphan pages, missing source locators, duplicate pages,
contradictions, stale or superseded claims, and important unresolved concepts.
Report proposed repairs before changing scientific meaning. After approved
repairs, update affected pages and append one `lint` entry to `log.md`.

## Log format

Append entries without rewriting prior history:

```markdown
## [YYYY-MM-DD] ingest | Source title

- Pages: `sources/example.html`, `concepts/example.html`
- Change: One concise description.
```
