# Research records

The user writes in chat or on the wiki. Research records retain the original text,
handwriting, linked evidence and explicit priority status changes.
Existing and new Ceridwen experiments share this structure. Historical reasoning
is not reconstructed. Existing notebooks, results and source-note URLs stay in place.

## No agent commentary

The no-commentary rule in `../AGENTS.md` applies to all pages, including these
research records. Use direct factual descriptions, measured results, concrete
limitations and literal section titles. Remove editorial advice, generic caveats,
source-summary framing, process narration and agent-role labels. Keep original
user wording, evidence and recorded results. Preserve necessary uncertainty.

## Result pages

Liu Hao is the research supervisor. The governing contract is in `../AGENTS.md`.
Present fits and relevant figures with short, factual captions. Do not display
source summaries, essays, process narration or agent-role labels on result pages.
Keep the full research record at the experiment's `record/` subpage.

**Figures** contains a JSON array. Each item has `caption` and `view` (`Fits`,
`SFH`, `Posteriors` or `Comparison`), and optionally `target`, `arm` and `run`.
Use `path` for an existing image, or `notebook`, `cell` and `output` for a saved
PNG notebook output (zero-based indices). A notebook figure's `run` must identify
its recorded run, and that run must link the notebook. Copy the run's explicit
`target` and `arm` into the figure. Do not match targets by a dropdown position.
Use **Measurements** only for a compact benchmark table, with units and a source.

Inspect the saved output and its code before recording its indices. Do not choose
images by an index shared across notebook versions. The builder extracts the
existing bytes; it never executes code, changes plots or generates captions.
For comparisons, include the reference arm under the same target. Caption changed
settings and material caveats. Keep failed attempts in the underlying record.

The default report opens Fits, or the first available view for non-fit analyses.
A target selector keeps every saved target available. SFH, posterior and comparison
views retain the selected target. Population figures apply to all targets.
Do not publish a result state without figures or a measured benchmark table.

## Before delegation

### Meeting notes

Transcribe and lightly rephrase meeting notes. Join fragments into complete
sentences where the meaning is clear. Preserve questions, uncertainty and emphasis.
Do not add commentary, explanations, interpretations, caveats or assessments.
Do not narrate what the notes say or judge whether their claims are established.
Use brief uncertainty markers for unclear handwriting; do not guess missing words.
Keep original handwriting and user clarifications accessible beside the cleaned
notes. Apply this rule to existing and future meeting notes.

### Roadmap priorities

All future research roadmap guidance and discussion uses **1–10**, with **10
highest**. Priority measures research importance, not difficulty. Check the
current roadmap before proposing work or preparing an experiment handoff.

`direction.md` holds one canonical **Roadmap** section containing a fenced JSON
array. Each task has a stable `id`, a short `title`, a `source` evidence link,
and an integer `priority` from 1 to 10, or `null` for unscored work. Optional
`details` and `effort` retain user-specified context and difficulty. Optional
`depends_on` lists other task IDs. Dependencies do not change the priority score.

Home and the legacy `/wiki/roadmap/` render this same array in descending priority
order. Ties retain source order. Unscored tasks appear at the end of the full
roadmap. A task's title links to its supporting meeting note or other evidence.

Preserve user-assigned priorities. Label suggested scores as **proposed** in
discussion; do not save them as canonical until the user accepts them. Do not
assign scores to historical or unspecified work. Append the user's dated changes
under **Amendments**, retaining the original wording. **References** links the
meeting notes; the original scientific direction remains under **Your words**.

### Priority history and handwriting

- Open a priority from Home to view its source and dated history.
- **Mark resolved** and **Reopen** change only that priority's state. Neither
  requires notes. Saving an annotation never changes a priority or question state.
- Home keeps active priorities and an expandable **Resolved** list. Scores,
  dependencies, original task IDs and the legacy roadmap anchors are retained.
- **Write notes** opens the writing sheet beside the question. **Annotate figure**
  opens an existing result figure and attaches the sheet to a priority or question.
- Pencil input writes. Scribble back and forth over existing ink to erase the
  covered area. Undo restores the erased ink. Figure backgrounds remain intact.
- One finger scrolls the notebook. Pencil contact stops scrolling; touches present
  during writing remain ignored until lifted. Mouse drawing is available on desktop.
- Blank sheets appear automatically near the bottom, up to 30 sheets per note.
  Save the current note before selecting **New note** to continue beyond that limit.
  The sheet selector jumps within the same continuous notebook.
- **Save annotation** saves the text, evidence links, strokes and PNG previews.
  The background is an immutable copy of the displayed figure, with its source
  record. Notebook outputs are copied without executing the notebook.
- Browser IndexedDB retains local drafts shortly after each stroke or text edit. A draft
  belongs to that browser and device. Active ink renders once per display frame over
  cached finished strokes; finger scrolling and Pencil palm handling are independent. Server saves require the Mac and Tailscale
  connection. The interface distinguishes draft storage, saving and publication.
- **Revise note** appends another version. Earlier text and ink remain readable.
  **New note** starts a separate entry after the current draft is saved.
- Transcribe only on request. Keep original handwriting beside the transcription.
  Do not interpret handwriting as a resolution or invent a scientific conclusion.

Canonical activity lives under `activity/<priority|question>/<id>/<event-id>/`.
Each immutable directory contains `event.json`, the retry request, sheet previews,
and any original figure backgrounds. Events have ordered sequence numbers and
UTC save timestamps. A resolution records the sequence it followed. Later notes
and reopening do not rewrite the record at that point. The roadmap's title,
priority and dependencies remain exclusively in `direction.md`.

`wiki/activity.py:save` is the shared browser and chat write interface. Load the
current records with `research.load`, then call `activity.save(research_root,
project_root, records, kind, id, payload, origin="chat")` for a chat update. Use a
unique request `id`, `action: "note"`, original `text`, optional `evidence` links,
and optional `supersedes` event ID. Retain known message references in `source_ref`.
For an explicit priority status change, use `action: "state"`, `state: "resolved"`
or `"open"`, and the current `expected_state`. Reuse the request ID only for an
identical retry. Rebuild after a chat save and commit only the requested records.

The server exposes GET/POST `/wiki/api/activity/<kind>/<id>`, GET
`/wiki/api/catalog`, GET `/wiki/api/figure/<experiment>:<index>`, and GET
`/wiki/api/publication`. POST requests require the same origin and JSON bodies
of at most 24 MiB. Note saves accept up to 30 sheets, each with dimensions,
original `[x, y, pressure]` points, pen size/colour and a PNG preview. Stroke
records accept an optional `tool` (`pen` or `eraser`); omitted means `pen`.
Scribble erasures retain their original points with `gesture: "scribble"`; their
covered rectangle erases ink with a 12-unit margin. Legacy eraser paths remain
readable. Eraser sizes are 12, 24 and 48 sheet units. Pen sizes remain 2, 4 and 7.
Operations replay in order on a separate ink layer; later pen strokes remain
visible over earlier erased areas. Interior blank sheets retain their positions. API writes
and chat writes share the process lock and atomic event publication. Builds use
a separate publication lock and run after saved events. A failed build leaves
the saved record available through the API and retains the previous site.

### Experiment record

1. Read the current questions and related experiments.
2. Create or reuse one question under `questions/<id>.md`.
3. Copy `templates/experiment.md` to `experiments/<id>.md`.
4. Capture the relevant user messages in **Before delegation**, in their original
   order. Retain original text and optionally add a lightly edited display.
5. Record an explicit **Execution plan**: comparison, baseline, data, model,
   controlled changes, analysis and requested outputs. This section is the agent's
   work and stays separate from the user's original wording.
6. Include the experiment ID and source path in the delegated task. Existing
   authorization in the conversation is sufficient; do not ask for it again.

Record a hypothesis or prediction only when the user supplies one. Exploratory
work is valid. Ask about missing research decisions only when execution depends
on them. Do not turn an agent's suggested explanation into the user's reasoning.

## Messages

Each user-authored section contains one JSON array inside a `json` fence. `text`
always retains the original. Optional `display_text` contains a light edit:

```json
[
  {"date": "2026-09-12", "text": "i think this might help", "display_text": "I think this might help."}
]
```

The example above describes the format; never use it as an actual message.
Use a JSON serializer so escaping does not change the decoded text.
Both strings render as plain text, not Markdown or HTML. Edited wording is
labelled and the original remains expandable. Without `display_text`, display
the original. Keep excerpts contiguous and separate thoughts separate.

Light edits may fix spelling, punctuation and small phrasing issues. Preserve
uncertainty, emphasis, qualifications, numbers and the difference between a question,
a suggestion and a decision. Do not add explanations or strengthen claims. Leave
ambiguous wording unchanged when editing would require guessing. The renderer
never generates edits; the recording agent checks each edit against the original.

Optional `source` is a known chat URL or an existing project-relative source
file. Optional `source_ref` is a known session/message identifier. Omit unavailable
references. Do not fabricate IDs, URLs or timestamps. `date` is the message date,
not an invented execution timestamp.

Append later changes to **Amendments**. Append the user's response to the results
to **Your interpretation** and their stated next action to **Next decision**.
Keep the original brief intact. Corrections remain dated additions unless the
user explicitly requests another treatment. Use the same light-edit rule for later
messages. Never synthesise missing reasoning. An agent's answer is not a user message.

## Runs and results

**Runs** contains a fenced JSON array. Every attempted run records:

- `id`: stable run ID, unique within this experiment; each retry gets another ID.
- `arm`: the comparison arm; multiple repeats can share an arm.
- `status`: `planned`, `running`, `complete` or `failed`.
- `config`: existing project-relative file or URL of the saved resolved configuration.
- `code`: exact code version; record a saved patch reference if the tree was dirty.
- `model`: SSP grid and model/dependency versions actually used.
- `data`: existing file or URL specifying the input sample and processing version.
- `seed`: recorded integer seed; batch configurations must record the per-target rule.
- `artifacts`: array of `{"label": "Executed analysis", "path": "results/.../analysis.ipynb"}`.
- `error`: required for failed runs; keep the failed attempt and its logs.

A planned run can contain only `id`, `arm` and `status`. Add evidence as it exists.
Completed runs require an executed notebook link. Keep the notebook, its saved
outputs, data products and configuration in their established result directory.
Read the configuration from the actual run; never substitute today's defaults.
Do not overwrite a completed run's configuration with a later attempt.

**Results** is factual Markdown written by the agent: measured quantities with
units, comparison conditions, figures, checks and unresolved discrepancies.
Every quantitative claim needs its source table, notebook cell or saved output.
Separate sampler/implementation checks from scientific conclusions. Do not label
a configuration more accurate merely because it changes a parameter or fits better.
Do not add an agent synthesis of the user's reasoning.

Evidence links and images are project-relative, with spaces URL-encoded, or
explicit http(s) URLs. The builder verifies local files and renders links through
the existing `/wiki/f/` route. It does not copy or upload result directories.

## States and links

- Question: `open`, `paused`, `answered`. `answered` requires the user's decision.
- Experiment: `planned`, `running`, `results-ready`, `reviewed`, `stopped`, `recorded`.
- `results-ready`: completed evidence and agent-reported results are available.
- `reviewed`: the user's interpretation is recorded. It is not a validation grade.
- `stopped`: work has stopped, including inconclusive or unsuccessful experiments.
- `question`: the existing parent question ID.
- `follow_up`: optional comma-separated experiment IDs, created only when there is
  a real follow-up brief. Preserve the user's next decision even if no follow-up exists.

The question index groups experiments by question. Experiment pages keep run
status separate from interpretation status. Home shows the full priority list and
planned/running experiments, with direction, questions and amendments in a collapsed
research record. Results lists entries with saved figures or benchmark measurements;
other experiment records and earlier analyses remain accessible below. Existing
results do not create a retrospective review backlog. Old URLs remain available.

## Existing research

- Set `origin: existing` for records organised from saved evidence. Omitted origin
  means `new`. Existing experiments use `status: recorded`, not `reviewed`.
- Require **Context** and **References**, including at least one source link.
  Describe the documented comparison in Context, not a fabricated Execution plan.
- Existing questions can omit **Your words**. Existing experiments can omit
  **Before delegation**, unrecorded run metadata and historical user interpretation.
  Empty sections are hidden. Do not invent dates, seeds, failures or code versions.
- `recorded` requires factual **Results**. It cannot contain a running run.
  Record later follow-up work as a new experiment with the normal requirements.
- Use **Caveats** for limitations, incompatible comparisons and unresolved source
  conflicts. Historical adoption labels belong to source history, not review status.
- Add `source_notes: slug-one, slug-two` for existing note backlinks. Each slug
  must exist. Links to `wiki/notes/<slug>.md` open the rendered note.
- Each experiment has one `question`. Optional `related_questions` lists other
  question IDs. Show the same record under each, without duplicating results.
- `result_groups` lists existing project-relative result directories represented
  by the entry. This supports the coverage audit; it does not move or copy files.
- For existing records, `date` is the dated source report or documented completion
  date. Retain actual per-run dates in their source manifests. Importing a record
  does not make an old result current or validate an earlier interpretation.
- Prefer saved configurations over current defaults. Check summaries against
  tables and notebooks. Record source contradictions together, with a locator.
- Keep inactive Prospector, MilesPy and Lick branches in source history.

## Build and check

```sh
python3 wiki/build.py
```

```sh
python3 wiki/tests/run_tests.py
```

```sh
python3 -m unittest discover -s wiki/tests -p 'test_research.py'
```

The builder accepts `--research DIR`. By default it reads the `research/`
directory beside `--notes`. Test builds should isolate both source directories.
Templates are not rendered. Research messages are exempt from the legacy
50-word body limit and are never shortened by the builder.
