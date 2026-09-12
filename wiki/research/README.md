# Research records

The user writes in chat. Agents maintain these records and the linked evidence.
This workflow applies to new research. Existing analyses remain in Earlier work;
their reasoning is not reconstructed.

## Before delegation

1. Read the current questions and related experiments.
2. Create or reuse one question under `questions/<id>.md`.
3. Copy `templates/experiment.md` to `experiments/<id>.md`.
4. Paste the relevant user messages into **Before delegation**, verbatim and in
   their original order. Preserve spelling, punctuation, whitespace and uncertainty.
5. Record an explicit **Execution plan**: comparison, baseline, data, model,
   controlled changes, analysis and requested outputs. This section is the agent's
   work and is labelled accordingly on the page.
6. Include the experiment ID and source path in the delegated task. Existing
   authorization in the conversation is sufficient; do not ask for it again.

Record a hypothesis or prediction only when the user supplies one. Exploratory
work is valid. Ask about missing research decisions only when execution depends
on them. Do not turn an agent's suggested explanation into the user's reasoning.

## Messages

Each user-authored section contains one JSON array inside a `json` fence:

```json
[
  {"date": "2026-09-12", "text": "The user's exact words, including\nline breaks."}
]
```

The example above describes the format; never use it as an actual message.
Use a JSON serializer so escaping does not change the decoded text. Messages are
rendered as plain text, not interpreted as Markdown or HTML. Keep relevant
excerpts contiguous; do not stitch fragments into a new sentence.

Optional `source` is a known chat URL or an existing project-relative source
file. Optional `source_ref` is a known session/message identifier. Omit unavailable
references. Do not fabricate IDs, URLs or timestamps. `date` is the message date,
not an invented execution timestamp.

Append later changes to **Amendments**. Append the user's response to the results
to **Your interpretation** and their stated next action to **Next decision**.
Keep the original brief intact. Corrections remain dated additions unless the
user explicitly requests another treatment. Never paraphrase, synthesise or
silently improve these messages. An agent's answer is not a user message.

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
- Experiment: `planned`, `running`, `results-ready`, `reviewed`, `stopped`.
- `results-ready`: completed evidence and agent-reported results are available.
- `reviewed`: the user's interpretation is recorded. It is not a validation grade.
- `stopped`: work has stopped, including inconclusive or unsuccessful experiments.
- `question`: the existing parent question ID.
- `follow_up`: optional comma-separated experiment IDs, created only when there is
  a real follow-up brief. Preserve the user's next decision even if no follow-up exists.

The question index groups experiments by question. Experiment pages keep run
status separate from interpretation status. The homepage shows active questions,
ongoing experiments and results awaiting interpretation. No historical run is
promoted into this workflow automatically.

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
