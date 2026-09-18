# Astro Research Wiki

This directory contains the Ceridwen research notebook and codebase reference.
The user writes research reasoning in chat. Agents preserve those original words
and maintain execution records and factual results. The user selects the research
direction and scientific methodology.

## All pages: no agent commentary

- Apply this rule to every existing and future page: Home, results, meetings,
  papers, masking, code, guides, questions, research records and archived pages.
- Remove process narration, editorial advice, generic caveats, assessments,
  source-summary framing and agent-role labels. Do not add "why this matters"
  sections, narrate what a source says, or judge whether the user's notes are valid.
- Keep factual research content, necessary technical explanations, concrete
  limitations, citations and the user's own reasoning. State facts directly.
- Preserve original user messages, handwriting, recorded results and evidence.
  Do not strip uncertainty from a claim or turn an interpretation into a fact.
- Keep operational instructions in guides and factual execution plans in records.
  Do not add unsolicited research recommendations.

## All pages: rendered scientific notation

- Use LaTeX for scientific symbols and equations on every maintained wiki page,
  including headings, prose, tables, figure captions and research-record displays.
- Use `\(...\)` for inline math and `\[...\]` for display equations. Dollar signs
  remain literal. For example, write `\([\alpha/\mathrm{Fe}]\)`,
  `\(\sigma_\star\)`, `\(M_\odot\)` and `\(\chi^2\)`.
- Keep code identifiers, exact source excerpts, URLs and commands literal in code
  spans or blocks. Keep original quotations, handwriting, archived source files
  and immutable activity records unchanged. Format the separate display wording.
- Change notation only: preserve values, units, definitions, uncertainty and
  meaning. Do not add commentary or infer a scientific correction during conversion.
- Retain plain document titles and image alt text. Use `display_title` when a
  note's visible title needs math; keep existing heading anchors available.
- KaTeX and its fonts are served locally. `assets/math.js` renders explicit math,
  including content inserted after load; no runtime CDN is required.
- Check math syntax, phone/tablet layouts, dark mode and print when changing math
  rendering. Do not rerun fits or regenerate saved plots to change page notation.
- This is a wiki rule. Scientific equations in chat remain plain text.

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
- Before adding any figure to `wiki/analyses/<slug>/` or a wiki note, open the rendered PNG at
  the wiki column's 900 px display width and check for overlapping labels, legends or ticks,
  text clipped at axes edges, and unreadable fonts. Fix and re-render until clean; for new
  figures, then screenshot the built wiki page.
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
- Existing questions may use a factual description of the comparison instead of
  user messages. Do not attribute that description to Liu Hao.
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

### Priority resolutions and Apple Pencil

- Keep annotations and explicit priority status changes independent.
- Use `activity.py:save` for browser and chat activity. Append revisions and state
  changes under `research/activity/`; never rewrite saved originals or events.
- `research/direction.md` remains canonical for scores, titles and dependencies.
- Handwritten notes, ink previews and immutable figure backgrounds are permitted
  source records inside `research/activity/`. They are not scientific result runs.
- Preserve ink and original text. Transcribe only when requested. Never infer
  a resolution from handwriting, a saved note, or an experiment's status.
- Browser drafts stay on the originating device until saved to the Mac.
- Run `python3 -m unittest discover -s wiki/tests -p 'test_activity.py'` with the
  existing wiki checks when changing the activity or handwriting workflow.

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
- Keep sourced claims and unresolved questions separate.
- Do not perform web research unless the user requests it.
- Record uncertainty. Do not guess why the code was written.

## Structure

- Navigation has seven links: Home, Results, Model, Meetings, Papers, Masking, Code & guides.
- Model (`/wiki/model/`) renders notes with front matter `section: Literature`.
  `/wiki/literature/` remains the earlier address of the same page.
  The note is `notes/model.md`. The page contract is `research/model-page-spec.md`.
- Home shows the full priority list and planned/running work. Original direction,
  questions and dated amendments are in its collapsed research record.
- Results lists saved visual reports and benchmarks, with other experiment records
  and earlier analyses/boards below. Keep result pages focused on figures and captions.
- Meetings and Papers have their own collections. Papers links the local PDFs in
  `papers/README.md`; preserve its citations without promoting historical roles.
- List every assumption and setting on the Model page.
  Include each sample cut, preprocessing step, data source, prior, switch, mask, sampler setting
  and derived-quantity definition. Tag assumptions nobody on this project chose as `inherited`.
- Use four groups in this order: Sample and data; Stellar model, SFH and dust;
  Calibration, noise and sampler; Derived quantities and cosmology.
  Each group is one raw `<dl class="model-group">`.
  Use `<div class="model-row">` for a row without bullets.
  Use `<details class="model-row">` for a row with bullets.
- Show the setting, value, reason of at most six words, and `!` flag.
  On click, show fragment bullets labelled why, how, tested, problem, papers, source and note.
  Link every tested and problem bullet to its experiment record, note or meeting note.
- Use a reason only from a recorded decision, meeting point, experiment result or paper.
  Leave the reason empty when none is recorded. Never invent a reason.
- Use `!` only with linked evidence from this repository's results or a recorded meeting point.
  A paper that disagrees does not justify a flag. Put it in the Literature section below the groups.
- Keep the comparison figure and z~0.7 values table in the Literature section.
  Keep Jonah Powley's Prospector reference collapsed there. Include other redshifts and references.
  List each citation once.
- Update the row in the same commit when a prior, switch, mask or data source changes.
  Apply this rule to sampler settings and derived-quantity definitions.
  Keep values aligned with `notebooks/ceridwen_integrated_photometry_spectra.ipynb`.
  Do not change defaults.
- `notes/default-fit-parameters.md` and `notes/papers-quiescent-parameters.md` are obsolete stubs.
  `notes/model.md` supersedes both. Keep the stubs so old URLs work.
  Parameter references use tables and source links; they do not require teaching blocks.
  Code documentation, notebooks, guides and earlier history follow.
  Keep one search across all content.
- Preserve old URLs and anchors. `/wiki/roadmap/` serves the same content as Home;
  questions, experiments, reference, source notes, themes and log routes remain.

- `research/` holds existing and new questions, experiments and the user's direction.
- `notes/` holds the existing reference and analysis source notes.
- `build.py` and `research.py` render both corpora into `public/`, using the standard library.
- `public/` is generated output. Never edit it by hand.
- The TrueNAS server is the only host of the wiki, at `https://wiki.eclw.org/` behind the Pangolin
  login on the VPS (traefik, gerbil, newt on the NAS, nginx on the newt bridge gateway 172.16.12.1:8765).
  Pages live at the site root; `/wiki/...` links from before 2026-09-18 redirect permanently.
  `scripts/publish_wiki.py` pulls the research activity the browser saved there, sends the wiki
  sources, `scripts/serve_wiki.py` and every project file linked through `/f/`, then the NAS
  builds its own `public/`. A launchd agent on the Mac runs it after each build and every 30 minutes.
  A build on the Mac is for checking; nothing serves it. Deployment files: `scripts/truenas-wiki/`.
  The question box needs the Mac's bridge, so the NAS pages do not show it.
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
Execution plans and measured results occupy separate sections in research records.
Use literal section titles without agent-role labels. Never add these to meeting notes.
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

- Show measured benchmark results.
- Show measured performance, cost, memory and comparison conditions.
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
- Do not add uncited interpretations or `Project synthesis` commentary.
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
  <p>Factual contract with its docstring, test, README or script citation.</p>
  <p>Factual behavior in the active Ceridwen path, if the excerpt needs explanation.</p>
</div>
```

- Copy a contiguous source excerpt without edits or ellipses.
- Use 5-20 lines unless a longer contract cannot be divided safely.
- Name the class, function, test, notebook heading, or script entry point.
- Cite the nearest public docstring first. Use a test when no useful docstring
  exists. Use a maintained README or script help for operational workflows.
- Keep the documented contract separate from the wiki explanation.
- Omit uncited inferences and editorial assessments.
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
4. State evidence and unresolved questions directly, without added synthesis.
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
