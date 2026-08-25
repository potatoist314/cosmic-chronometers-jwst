
 The user's contribution will be focused on overall research direction and methodology, yours is implementation.

## Local resources

- Start at `wiki/index.md` for the maintained codebase map.
- Ceridwen papers and developer notes are in `ceridwen/`.
- LEGA-C release documentation and spectra are in `data/raw/legac_dr2/`.
- `papers/README.md` maps the local research papers.
- Ceridwen fetches the published alpha-enhanced grid through `fetch_grid()`.
- PDFs and raw data can be ignored by Git. Use `find` when `rg --files` misses them.

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
  `All written or modified Python code and notebooks must pass the project’s configured Ruff checks before completion; fix every diagnostic rather than suppressing it.`


## Repository and reproducibility conventions

- Immediately commit and push completed, conflict-free work to the current branch; do not wait for a separate push request.
- Use notebooks as the primary files for explanation,
  exploration, and presentation.
- Notebook markdown cells are terse bullet points, roughly ten words each,
  saying what an otherwise unclear line of code does. No fluff, or restating results or numbers.
- Use LaTeX for mathematical symbols and parameter names in figures.
- Run full Ceridwen fits on Vast.ai CUDA GPUs; use local quick tests only.
- Always use the BlackJAX NSS nested sampler for Ceridwen fits, never NUTS.
- Keep raw data immutable. Produce processed data through documented scripts or
  functions.
- Put one-time download and bookkeeping utilities in `scripts/`, not notebooks.
- Use fixed and recorded random seeds for reference mock analyses.
- Add tests for equations, units, limiting cases, and numerical benchmarks.
- Prefer a smaller analysis that is understood, tested, and documented over a
  broad analysis whose assumptions have not been examined. E.g., get a small test case of 1 sample or 10 samples working well before attempting to fit a full sample.

## Codebase wiki

- `wiki/` is a Codex-maintained guide for learning this codebase.
- Read `wiki/AGENTS.md` before creating or changing wiki pages.
- After substantive code, notebook, or data-flow changes, update affected wiki
  pages, `wiki/index.md`, and `wiki/log.md` without waiting for confirmation.
- Skip wiki updates for formatting-only changes or unchanged behavior.
- Human wiki pages use clean HTML with short, exact code excerpts and source locations; agent-facing memory may remain Markdown.
