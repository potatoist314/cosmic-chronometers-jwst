
 The user's contribution will be focused on overall research direction and methodology, yours is implementation.

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
- **The user sets research direction.** Implement requested work directly.
- Flag a major error in research direction, or something genuinely missed. Nothing else.
- Do not argue. State a disagreement once, briefly; if the user restates, proceed.
- **Create nothing that wasn't asked for.** No backups, scratch files, helper
  scripts, extra docs, or README entries unless explicitly requested. Edit the
  file named and stop. Keep the repo clean. Do not add speculative defensive guards to code; rely on documented data contracts unless an observed failure or test justifies the check.
  - **Prefer established or existing libraries for standard operations. Avoid recreating functions that already exist.
  E.g. ** `milespy`,`astropy`, `scipy`, `specutils`, `spectres` and the other installed packages already implement many standard operations. Confirm their behavior before replacing them with hand-written code.


## Repository and reproducibility conventions

- Immediately commit and push completed, conflict-free work to the current branch; do not wait for a separate push request.
- Use notebooks as the primary files for explanation,
  exploration, and presentation.
- Every new result directory must include its executed analysis `.ipynb` with saved fit, SFH/age-history, and corner-plot outputs.
- Notebook markdown cells are terse bullet points, roughly ten words each,
  saying what an otherwise unclear line of code does. No fluff, or restating results or numbers.
- Use LaTeX for mathematical symbols and parameter names in figures.
- Absorption-feature labels use fixed colours from `scripts/spectral_figures.py`
  and one legend to the right of each figure. Use `mark_absorption_features`
  and `spectral_tight_layout`; do not place feature names under the axis.
- Before adding any figure to `wiki/analyses/<slug>/` or a wiki note, open the rendered PNG at
  the wiki column's 900 px display width and check for overlapping labels, legends or ticks,
  text clipped at axes edges, and unreadable fonts. Fix and re-render until clean; for new
  figures, then screenshot the built wiki page.
- For connected spectral plots, keep the full wavelength grid and set excluded
  values to `NaN`; never plot `wavelength[mask]` as one connected line or band.
- Run full Ceridwen fits on Vast.ai CUDA GPUs; use local quick tests only.
- Always use the BlackJAX NSS nested sampler for Ceridwen fits, never NUTS.
- Keep raw data immutable. Produce processed data through documented scripts or
  functions.
- Do not use hashes or checksums to verify file transfers.
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
- `wiki/` is a Codex-maintained guide for learning this codebase.
- Read `wiki/AGENTS.md` before creating or changing wiki pages.
- After substantive code, notebook, or data-flow changes, update affected wiki
  pages, `wiki/index.md`, and `wiki/log.md` without waiting for confirmation.
- Skip wiki updates for formatting-only changes or unchanged behavior.
- Human wiki pages use clean HTML with short, exact code excerpts and source locations; agent-facing memory may remain Markdown.

## Research result presentation

- Liu Hao is the research supervisor. Follow the result-reporting contract in
  `wiki/AGENTS.md` for every existing and future wiki result page.
- Show fits and relevant figures with short, factual captions. No agent source
  summaries, explanatory essays, process narration or agent-role labels.
- Keep research reasoning, originals, run metadata and evidence in a separate
  research-record view. Do not discard them or invent scientific interpretations.

## Recording research

- Before executing or delegating a new scientific experiment, read
  `wiki/research/README.md` and create or reuse its question and experiment record.
- Retain Liu Hao's original chat text. Lightly edit displayed wording only for
  spelling, punctuation and phrasing. Preserve meaning, uncertainty and emphasis.
  Never invent a prediction, explanation, interpretation or decision.
- Keep the original available beside edited wording. Keep separate thoughts
  separate. Preserve ambiguous wording when editing would require guessing.
- Record agent execution plans, actual configurations, evidence and factual results
  separately. Include the experiment ID and record path in handoffs.
- Append subsequent user amendments, interpretation and decisions with their dates.
  Mark an experiment reviewed only when his interpretation is recorded.
- Existing authorization in chat is sufficient. Ask only about missing research
  decisions that materially affect execution, not for repeated permission.
- Integrate existing Ceridwen results into the same questions and experiments.
  Use documented evidence, with origin existing and status recorded. Do not invent
  historical reasoning or demand missing metadata. Retain notebooks and result paths.

## Research priorities

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
