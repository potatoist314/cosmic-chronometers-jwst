# Astro Research Wiki

This directory contains the Ceridwen research notebook and codebase reference.
The user writes research reasoning in chat. Agents preserve those original words
and maintain execution records and factual results. The user selects the research
direction and scientific methodology.

## Result reporting: Liu Hao is the supervisor

- Result pages report the work to Liu Hao as the research supervisor.
- Show spectral and photometric fits first, with short, factual captions. Keep SFH,
  posterior and comparison figures available alongside them.
- Do not add agent source summaries, explanatory essays, process narration or
  agent-role labels to result pages. Do not teach standard astronomy terms.
- Captions identify the comparison, report the relevant observation and flag
  material problems. Preserve uncertainty. Never invent scientific interpretations.
- Use existing plots or saved notebook images. Do not rerun analyses to populate
  the wiki. Keep every target accessible and aligned across comparison arms.
- Use compact measured tables for benchmarks when plots add nothing.
- Keep before-delegation thoughts, original wording, run metadata and evidence in
  the underlying research record, accessible separately from the visual report.
- Absorption features use the shared fixed colours and one right-side legend
  from `scripts/spectral_figures.py`. Finish these figures with
  `spectral_tight_layout`; do not put feature names beneath the axis.
- Apply this contract to existing and future result pages, templates and rendering.
  Tests must reject summary sections or agent-role labels on result pages.

## Research workflow

- Read `research/README.md` before recording or delegating a scientific experiment.
- Organise questions and experiments under `research/`, with stable IDs and grouped runs.
- Retain original chat messages. Allow light editing of displayed spelling, punctuation
  and phrasing, without changing meaning, uncertainty, emphasis or qualifications.
- Preserve ambiguous wording. Never invent a prediction, explanation or interpretation.
- Keep edited display separate from original text, with the original expandable.
- Attribute agent execution plans and factual results separately from user reasoning.
- Append later amendments and decisions with their dates. Existing chat authorization
  remains sufficient. Do not request repeated permission.
- `reviewed` requires the user's interpretation. It is not a scientific validation grade.
- Integrate existing Ceridwen results as full entries with source references and caveats.
  Use `origin: existing` and `status: recorded`. Do not reconstruct historical briefs,
  invent metadata, rerun fits, or move existing evidence.
- Existing questions may use source-derived context instead of user messages. Label
  this context as an agent source summary. Do not attribute it to Liu Hao.
- Research entries are exempt from the legacy word and caption limits.
- Run `python3 wiki/tests/run_tests.py` and
  `python3 -m unittest discover -s wiki/tests -p 'test_research.py'` after changes.

## Current scope

### Meeting notes

- Transcribe and lightly rephrase meeting notes. Join fragments into complete
  sentences where the meaning is clear. Preserve questions, uncertainty and emphasis.
- Do not add commentary, explanations, interpretations, caveats or assessments.
  Do not narrate what the notes say or judge whether their claims are established.
- Use brief uncertainty markers for unclear handwriting; do not guess missing words.
- Keep original handwriting and user clarifications accessible beside the cleaned
  notes. Apply this rule to existing and future meeting notes.

### Research priorities

- Use the same 1–10 scale for all future roadmap guidance and discussion, with
  10 highest. Read the canonical Roadmap in `research/direction.md` first.
- Show priority, difficulty and dependencies separately. Keep unspecified tasks
  unscored. Only user-approved scores belong in the canonical roadmap; identify
  agent suggestions as proposed until accepted.
- Preserve dated amendments and original user wording. Render Home and the legacy
  roadmap route from the same task list; never maintain separate copies of scores.
- Keep corrected meeting notes alongside their original transcription and source.

### Active research

- Make Ceridwen the primary path in navigation, explanations, and examples.
- Treat Prospector, MilesPy, and Lick-index work as inactive history.
- Keep historical facts only when they explain retained code or data.
- Do not present an inactive method as a current analysis option.

## Boundaries

- During wiki-only work, treat project code, notebooks, `papers/`, `data/raw/`,
  submodules, and user-designated sources as read-only evidence.
- Store only generated knowledge pages inside `wiki/`.
- Never rename, edit, or delete evidence during wiki work. The builder may extract
  unchanged saved notebook images into generated `public/` assets.
- Never treat a wiki summary as stronger evidence than its raw source.
- Keep sourced claims, project inferences, and unresolved questions separate.
- Do not perform web research unless the user requests it.
- Record uncertainty. Do not guess why the code was written.

## Structure

- Navigation has six links: Home, Results, Meetings, Papers, Masking, Code & guides.
- Home shows the full priority list and planned/running work. Original direction,
  questions and dated amendments are in its collapsed research record.
- Results lists saved visual reports and benchmarks, with other experiment records
  and earlier analyses/boards below. Keep result pages focused on figures and captions.
- Meetings and Papers have their own collections. Papers links the local PDFs in
  `papers/README.md`; preserve its citations without promoting historical roles.
- Code & guides groups code documentation, notebooks and guides, with earlier
  documentation and note history below. Keep one search across all content.
- Preserve old URLs and anchors. `/wiki/roadmap/` serves the same content as Home;
  questions, experiments, reference, source notes, themes and log routes remain.

- `research/` holds existing and new questions, experiments and the user's direction.
- `notes/` holds the existing reference and analysis source notes.
- `build.py` and `research.py` render both corpora into `public/`, using the standard library.
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
theme: Population results
status: obsolete   # optional
---
```

- `section` must be one of Analyses, Meetings, Masking, Guides, Notebooks, Codebase, Paper drafts, Archive.
- Meeting notes use `section: Meetings` and appear at `/wiki/meetings/`.
- Masking notes appear under the separate Masking sidebar category at `/wiki/masking/`.
- `job` is the Hermes card whose worker produced the note. Leave it empty when
  no card produced it. It drives the per-note question box, so never guess it.
- `status: obsolete` marks a note that stays readable but no longer applies.
- `theme` is required unless `status: obsolete`. Use one of the seven names in `THEMES` in `wiki/build.py`. Values: Single-fit accuracy, Validation on mocks, Sample and data, Population results, Compute, Model and code reference, Background reading.
- `superseded_by` is optional and names the slug of the note replacing this one. The build stops if that slug is not a note. The replaced note keeps its page and shows a banner.
- In `wiki/themes.md`, write one purpose line under each `## Theme` heading, then one `### Experiment` block per experiment. Add an optional `note: <slug>` line and an `arm | change | status | result` table with one row per arm. Use adopted, dropped, inconclusive, or planned for status. State what the arm does differently in change and what happened in result. Keep each to one clause with no full stop, plain words, no galaxy IDs or symbols. The build stops on an unknown status, a sentence in change or result, or a note slug that is not a note.
- `themes/` retains the earlier theme hub. `log/` is the existing date-ordered note feed.

### Authorship and generated text

User reasoning may have a lightly edited display, with the original text retained.
Agent source summaries, execution plans and measured results are labelled separately
in research records. Never add these to meeting notes.
The renderer never rewrites text or generates scientific interpretations. Existing
note routes and evidence remain accessible. Navigation uses short labels.

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
