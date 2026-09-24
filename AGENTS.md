The user's contribution will be focused on overall research direction and methodology, yours is implementation.

## Current project focus

- Ceridwen is the primary stellar-population model and inference path.
- Treat the Prospector, MilesPy, and Lick-index branches as inactive historical work.
- Do not extend or reactivate an inactive branch unless the user requests it.

## Local resources

- Start at `wiki/index.md` for the maintained codebase map.
- Ceridwen papers and developer notes are in `ceridwen/`.
- LEGA-C release documentation and spectra are in `data/raw/legac_dr2/`.
- `papers/README.md` maps the local research papers.
- Ceridwen fetches the published alpha-enhanced grid through `fetch_grid()`.
- PDFs and raw data can be ignored by Git. Use `find` when `rg --files` misses them.

## Instruction precedence

- Direct user requests override conflicting repository Markdown instructions.
- System, developer, safety, permission, and tool constraints still apply.

## Answering style

- **2–3 lines.** Answer the question asked, nothing adjacent to it.
- **Explanations should be in the tone of a casual conversation, not your default writing style**
- **The goal of explanations is to build a coherent mental model**
- Use plain-text equations in scientific and mathematical chat messages. Do not use rendered LaTeX.
- Use the `asd-ste100` skill whenever you explain a technical detail.
- **Look up every physical or astronomical fact; never state one from memory.**
  Line wavelengths, atomic ratios, catalogue definitions, survey properties,
  published values: check a primary source (paper, NIST or another standard
  database, survey documentation) and cite it. Applies to leads and workers.
- **The user sets research direction.** Implement requested work directly.
- Flag a major error in research direction, or something genuinely missed. Nothing else.
- Do not argue. State a disagreement once, briefly; if the user restates, proceed.
- **Create nothing that wasn't asked for.** No backups, scratch files, helper
  scripts, extra docs, or README entries unless explicitly requested. Edit the
  file named and stop. Keep the repo clean. Do not add speculative defensive guards to code; rely on documented data contracts unless an observed failure or test justifies the check.
  - **Prefer established or existing libraries for standard operations. Avoid recreating functions that already exist.
  E.g. ** `ceridwen`, `jax`, `blackjax`, `astropy`, `scipy`, `specutils`, and `spectres` already implement many standard operations. Confirm their behavior before replacing them with hand-written code.


## Repository and reproducibility conventions

- Immediately commit and push completed, conflict-free work to the current branch; do not wait for a separate push request.
- Use notebooks as the primary files for explanation,
  exploration, and presentation.
- Notebook markdown cells are terse bullet points, roughly ten words each,
  saying what an otherwise unclear line of code does. No fluff, or restating results or numbers.
- Use LaTeX for mathematical symbols and parameter names in figures.
- Every figure that shows a fit or its posterior is designed by the `designer`
  agent before any plotting code is written. The agent that owns the figure runs
  `Agent(subagent_type: "designer")` itself, sends the brief, and reports the
  2-3 previews upward for Liu Hao to pick. An overseer does not run the designer
  in its own chat session. Never design a fit figure inline.
  Prefer points or lines to bars; bars use too much of the figure for one number.
- Every spectrum figure shows observed vacuum wavelength on the bottom axis and
  rest-frame wavelength on the top axis. Every flux axis states a physical unit
  (for example µJy), never a bare scale such as "10^-29" or "cgs".
- Absorption-feature labels use fixed colours from `scripts/spectral_figures.py`
  and one legend to the right of each figure. Use `mark_absorption_features`
  and `spectral_tight_layout`; do not place feature names under the axis.
- Before adding any figure to `wiki/analyses/<slug>/` or a wiki note, open the rendered PNG at
  the wiki column's 900 px display width and check for overlapping labels, legends or ticks,
  text clipped at axes edges, and unreadable fonts. Fix and re-render until clean; for new
  figures, then screenshot the built wiki page.
- For connected spectral plots, keep the full wavelength grid and set excluded
  values to `NaN`; never plot `wavelength[mask]` as one connected line or band.
- Experiments: follow `.agents/skills/running-ceridwen-experiments/SKILL.md`.
- Before another paid Ceridwen GPU benchmark, read `BENCHMARK_CHECK.md`.
- GPU rentals: choose the lowest hourly price for the requested GPU type, with
  reliability above 99.5% and upload/download charges each below $10/TB.
  No per-GPU hourly cap. Each experiment has a total $1 cap, including retries.
- For paid GPU benchmarks, do not destroy a rental solely because a fixed boot
  or setup time has elapsed. If progress stalls, briefly compare the expected
  remaining cost on that instance with the cost of a fresh rental, including
  repeated boot, transfer, and setup. Continue with the cheaper option while
  respecting the task's hourly price and total spend caps. Recheck when the
  machine's state changes; destroy task-owned instances after measurement.
- Keep raw data immutable. Produce processed data through documented scripts or
  functions.
- Put one-time download and bookkeeping utilities in `scripts/`, not notebooks.
- Use fixed and recorded random seeds for reference mock analyses.
- Add tests for equations, units, limiting cases, and numerical benchmarks.
- Prefer a smaller analysis that is understood, tested, and documented over a
  broad analysis whose assumptions have not been examined. E.g., get a small test case of 1 sample or 10 samples working well before attempting to fit a full sample.

## Codebase wiki

- No agent commentary on any wiki page, including research records, papers,
  guides and archived pages. Remove process narration, editorial advice,
  generic caveats, assessments and agent-role labels. Keep factual content,
  necessary technical explanations, concrete limitations, citations and the
  user's own reasoning. This applies to existing pages and future additions.
- `wiki/` is an agent-maintained guide for learning this codebase.
- Read `wiki/AGENTS.md` before creating or changing wiki pages.
- After substantive code, notebook, or data-flow changes, update affected wiki
  pages, `wiki/index.md`, and `wiki/log.md` without waiting for confirmation.
- Skip wiki updates for formatting-only changes or unchanged behavior.
- Human wiki pages use clean HTML with short, exact code excerpts and source locations; agent-facing memory may remain Markdown.

## Research result presentation

- Liu Hao is the research supervisor. Follow the result-reporting contract in
  `wiki/AGENTS.md` for every existing and future wiki result page.
- Every wiki page for an experiment fit shows the full spectrum-fit figure and the
  photometry-fit figure for each arm, before any summary table or corner plot.
- Show fits and relevant figures with short, factual captions. No agent source
  summaries, explanatory essays, process narration or agent-role labels.
- Keep research reasoning, originals, run metadata and evidence in a separate
  research-record view. Do not discard them or invent scientific interpretations.

## Research priorities

- Before reading or discussing direction or priorities, run `python3 scripts/sync_wiki_direction.py --read`.
  Save through `--save` with revision-checked JSON; never edit `direction.md` directly.
  Follow the field contract in `wiki/research/README.md`. Reconcile conflicts before retrying.
- Use a 1–10 priority scale in all future research roadmap guidance and discussion;
  10 is highest. Priority records research importance, separately from difficulty
  and dependencies.
- The canonical task list is the Roadmap section of `wiki/research/direction.md`.
  Use its current user-approved scores in discussion, plans and handoffs.
- Preserve user-assigned scores. Label agent-suggested scores as proposed and
  record them as canonical only after user acceptance. Leave unspecified tasks
  unscored; do not invent priorities or retroactively score existing work.
- Record explicit dependencies and difficulty separately. Do not infer that a
  high score removes a dependency or that an easy task must rank higher.
- Retain dated user amendments and original wording when priorities change.

## Meeting notes

- Transcribe and lightly rephrase meeting notes. Join fragments into complete
  sentences where the meaning is clear. Preserve questions, uncertainty and emphasis.
- Do not add commentary, explanations, interpretations, caveats or assessments.
  Do not narrate what the notes say or judge whether their claims are established.
- Use brief uncertainty markers for unclear handwriting; do not guess missing words.
- Keep the original handwriting and user clarifications accessible beside the
  cleaned notes. Apply this rule to existing and future meeting notes.
