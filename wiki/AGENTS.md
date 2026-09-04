# Astro Research Wiki

This directory contains an LLM-maintained guide to the Astro project codebase.
Codex maintains the guide so the user can learn to read the code. The user
selects the research direction and scientific methodology.

## Current scope

- Make Ceridwen the primary path in navigation, explanations, and examples.
- Treat Prospector, MilesPy, and Lick-index work as inactive history.
- Keep historical facts only when they explain retained code or data.
- Do not present an inactive method as a current analysis option.

## Boundaries

- During wiki-only work, treat project code, notebooks, `papers/`, `data/raw/`,
  submodules, and user-designated sources as read-only evidence.
- Store only generated knowledge pages inside `wiki/`.
- Never copy, rename, edit, or delete evidence during wiki work.
- Never treat a wiki summary as stronger evidence than its raw source.
- Keep sourced claims, project inferences, and unresolved questions separate.
- Do not perform web research unless the user requests it.
- Record uncertainty. Do not guess why the code was written.

## Structure

- `notes/` holds the source of truth: one Markdown note for each entry.
- `build.py` renders `notes/` into `public/`. It is standard library only.
- `public/` is generated output. Never edit it by hand.
- `tests/run_tests.py` fails the build when the generator writes prose.
- `_old/` keeps every pre-notebook HTML page. Do not delete it without asking.
- `assets/fonts/` holds the self-hosted faces. The site loads no CDN.
- `analyses/<slug>/` holds the plots. `build.py` copies them to `public/figures/`.
- `index.md` is the compact agent catalog of notes.
- `log.md` is an append-only record of wiki operations.

Each note starts with YAML frontmatter:

```yaml
---
title: Stacked chi-squared and median pull
date: 2026-09-04
section: Analyses
tags: [dr2-quiescent-sample, ceridwen]
job: t_ee8ca17a
status: obsolete   # optional
---
```

- `section` must be one of Analyses, Guides, Notebooks, Codebase, Paper drafts, Archive.
- `job` is the Hermes card whose worker produced the note. Leave it empty when
  no card produced it. It drives the per-note question box, so never guess it.
- `status: obsolete` marks a note that stays readable but no longer applies.

### The one rule that overrides the rest

A note shows only Liu Hao's own content: title, date, figures, numbers,
commands, and his text. Write no summary, no dek, no caption of your own, no
"related" list, and no explanation. `tests/run_tests.py` fails the build when a
text node outside a note body is longer than four words, or ends a sentence.

Run `python3 wiki/tests/run_tests.py` after every change. Run
`python3 wiki/tests/run_tests.py --plant` to see the audit catch one planted
sentence.

### Question box

Each note that records a resumable `job` shows a question box. The question
goes to `bridge.py ask`, which resumes that exact worker session read-only. The
answer is appended to the note under `## Thread`. A note whose session cannot
be resumed shows nothing at all. Do not add a fallback worker or a notice.

## Page conventions

- Write terse and factual prose. Remove filler, scene-setting, conclusions, and
  repeated explanations.
- Do not use promotional text or rhetorical questions.
- Do not use prompts such as “Read it.”
- Use literal navigation labels. Prefer short lists to cards and callouts.
- Add a reading exercise only when the user requests one.
- Omit a measurement when the source did not record it. Do not add placeholder
  fields such as `not measured` or `not recorded`.
- When a benchmark includes JIT compilation, calculate throughput from later
  iterations only.
- Include the published dense tensor-core FP32 (TF32) peak for every GPU comparison.
- Include the Ceridwen grid schema in every benchmark row.

### Reader-facing benchmark pages

- Write benchmark pages for a reader who wants the result and its meaning.
- Show measured performance, cost, memory, comparison conditions, and useful interpretation.
- Do not show planning estimates, predicted-versus-measured checks, comparison
  fingerprints, commit hashes, runner hashes, instance IDs, transfer prices,
  commands, agent workflow, or status history unless the user asks for them.
- Keep reproducibility bookkeeping in scripts and machine-readable result files.
- Do not include source-code excerpts on benchmark result pages. Put code teaching
  in codebase pages or guides.
- Keep evidence to one short data-source note when it helps the reader.

### Diagram conventions

- Use a diagram when it makes a flow, branch, hierarchy, or comparison easier
  to understand than prose.
- Use semantic HTML and shared classes from `assets/wiki.css` for sequences,
  lanes, and labelled nodes.
- Use inline SVG only for connectors that HTML and CSS cannot show clearly.
- Keep all diagram labels in HTML so they reflow at narrow widths.
- Give every diagram a short caption. Give meaningful SVG elements a
  `<title>` and `<desc>`.
- Pair colour with text, position, or line style. Do not use colour alone.
- Use links only when a diagram is part of navigation.
- Do not use Mermaid, external scripts, external assets, or generated plot images.
- Self-contained JavaScript is allowed when it materially improves a
  user-requested interactive diagram.
- A validated Archify viewer may use its own self-contained HTML, CSS, inline
  SVG, and JavaScript instead of the normal wiki page shell and teaching blocks.
- Check diagrams at 360, 736, and 1024 pixels. Check dark mode and print.

Each generated HTML page must include:

```html
<meta name="wiki-type" content="codebase">
<meta name="wiki-status" content="current">
<meta name="wiki-updated" content="YYYY-MM-DD">
```

- Record source pages and inspected paths in visible `Evidence` sections when
  this information helps a reader check the explanation.
- Cite raw files with a page, section, figure, table, or row locator.
- Cite code with `path:line` and name the relevant class or function.
- Cite notebooks by filename, heading, and function or variable name.
- Label uncited interpretation explicitly as `Project synthesis`.
- Record conflicting claims together. Do not select one without explanation.
- Link the first meaningful mention of another wiki page.
- Revise an existing page instead of creating a near-duplicate.
- Keep summaries concise. Preserve uncertainty and scope.

Code pages must show short and exact source snippets. Include a file and line
locator for each snippet. Explain each snippet in plain language. Use only
sections that improve understanding.

### Source-backed teaching blocks

Technical pages must contain one or two source-backed teaching blocks. This
rule applies to codebase pages, notebook pages, Python guides, and GPU workflow
guides. Operational command examples do not count toward this limit.

Each teaching block must contain these parts in this order:

```html
<div class="source-example">
  <p class="source-locator"><code>path/to/file.py:10-20 · symbol_name</code></p>
  <pre class="python"><code>exact source excerpt</code></pre>
  <p><strong>Documented contract:</strong> Cited docstring, test, README, or script behavior.</p>
  <p><strong>Why it matters:</strong> Plain explanation for the active Ceridwen path.</p>
</div>
```

- Copy a contiguous source excerpt without edits or ellipses.
- Use 5-20 lines unless a longer contract cannot be divided safely.
- Name the class, function, test, notebook heading, or script entry point.
- Cite the nearest public docstring first. Use a test when no useful docstring
  exists. Use a maintained README or script help for operational workflows.
- Keep the documented contract separate from the wiki explanation.
- Label an uncited inference as `Project synthesis`.
- Recheck every excerpt and locator against the live source before completion.
- An analysis page may carry a bare source excerpt with a locator and no
  contract paragraphs.

## Autonomous codebase workflow

1. Read `index.md`, `overview.html`, and the relevant existing pages.
2. Inspect the live working tree. Do not use stale notebook outputs as current evidence.
3. Work from public entry points toward internal implementation details.
4. Explain one execution path at a time with exact source locators.
5. Update existing pages when behavior changes. Do not create duplicate summaries.
6. Update `index.md`. Append one `codebase` entry to `log.md`.
7. Check changed links, locators, contradictions, and duplicate pages.

The maintained codebase and notebooks are an authorized source corpus. Process
coherent groups without requesting approval for each file. Exclude virtual
environments, caches, generated outputs, and raw data payloads.

## Query workflow

1. Read `index.md`. Then read only the pages that are relevant to the question.
2. Consult raw sources when the wiki lacks evidence or precision.
3. Answer with links to wiki pages and exact raw-source locators.
4. Distinguish established evidence from project synthesis.
5. Add durable code explanations when they improve an existing page.
6. Create a new analysis page only when the user requests it.
7. Update `index.md` and append a `query` entry when pages change.

## Lint workflow

Check for broken links, orphan pages, missing source locators, duplicate pages,
contradictions, stale or superseded claims, and important unresolved concepts.
Report proposed repairs before you change scientific meaning. After the user
approves the repairs, update the affected pages. Append one `lint` entry to
`log.md`.

## Log format

Append entries without rewriting prior history:

```markdown
## [YYYY-MM-DD] ingest | Source title

- Pages: `sources/example.html`, `concepts/example.html`
- Change: One concise description.
```
