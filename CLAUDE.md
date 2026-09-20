# Astro Project Working Agreement

This file defines how Codex should support the project in this folder.
Treat these instructions as active until the user explicitly changes them.


## Answering style

- **2–3 lines.** Answer the question asked, nothing adjacent to it.
- Use plain-text equations in scientific and mathematical chat messages. Do not use rendered LaTeX.
- Use the `asd-ste100` skill whenever you explain a technical detail.
- **The user sets research direction.** Implement requested work directly.
- Flag a major error in research direction, or something genuinely missed. Nothing else.
- No filler, no recaps, no restating the plan, no unrequested tables or summaries.
- Do not argue. State a disagreement once, briefly; if the user restates, proceed.
- **Create nothing that wasn't asked for.** No backups, scratch files, helper
  scripts, extra docs, or README entries unless explicitly requested. Edit the
  file named and stop. Keep the repo clean. Do not add speculative defensive guards to code; rely on documented data contracts unless an observed failure or test justifies the check.
  - **Prefer established or existing libraries for standard operations. Avoid recreating functions that already exist.
  E.g. ** `milespy`,`astropy`, `scipy`, `specutils`, `spectres` and the other installed packages already implement many standard operations. Confirm their behavior before replacing them with hand-written code.


## Repository and reproducibility conventions

- Use notebooks as the primary files for explanation,
  exploration, and presentation.
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
- Experiments: follow `.agents/skills/running-ceridwen-experiments/SKILL.md`.
- Keep raw data immutable. Produce processed data through documented scripts or
  functions.
- Put one-time download and bookkeeping utilities in `scripts/`, not notebooks.
- Use fixed and recorded random seeds for reference mock analyses.
- Add tests for equations, units, limiting cases, and numerical benchmarks.
- Ensure each major result can be regenerated through a documented command or
  short, clearly ordered workflow.
- README targets newcomers; wiki HTML uses short, exact code excerpts; agent memory may stay Markdown.
- Prefer a smaller analysis that is understood, tested, and documented over a
  broad analysis whose assumptions have not been examined. E.g., get a small test case of 1 sample or 10 samples working well before attempting to fit a full sample.

## Research result presentation

- Liu Hao is the research supervisor. Follow the result-reporting contract in
  `wiki/AGENTS.md` for every existing and future wiki result page.
- Show fits and relevant figures with short, factual captions. No agent source
  summaries, explanatory essays, process narration or agent-role labels.
- Keep research reasoning, originals, run metadata and evidence in a separate
  research-record view. Do not discard them or invent scientific interpretations.

