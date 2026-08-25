# Astro Project Working Agreement

This file defines how Codex should support the project in this folder.
Treat these instructions as active until the user explicitly changes them.


## Answering style

- **2–3 lines.** Answer the question asked, nothing adjacent to it.
- **The user sets research direction.** Implement requested work directly.
- Flag a major error in research direction, or something genuinely missed. Nothing else.
- No filler, no recaps, no restating the plan, no unrequested tables or summaries.
- Do not argue. State a disagreement once, briefly; if the user restates, proceed.
- **Create nothing that wasn't asked for.** No backups, scratch files, helper
  scripts, extra docs, or README entries unless explicitly requested. Edit the
  file named and stop. Keep the repo clean. Do not add speculative defensive guards to code; rely on documented data contracts unless an observed failure or test justifies the check.
  - **Prefer established or existing libraries for standard operations. Avoid recreating functions that already exist.
  E.g. ** `milespy`,`astropy`, `scipy`, `specutils`, `spectres` and the other installed packages already implement many standard operations. Confirm their behavior before replacing them with hand-written code.
  `All written or modified Python code and notebooks must pass the project’s configured Ruff checks before completion; fix every diagnostic rather than suppressing it.`


## Repository and reproducibility conventions

- Use notebooks as the primary files for explanation,
  exploration, and presentation.
- Notebook markdown cells are terse bullet points, roughly ten words each,
  saying what an otherwise unclear line of code does. No fluff, or restating results or numbers.
- Use LaTeX for mathematical symbols and parameter names in figures.
- Run full Ceridwen fits on Vast.ai CUDA GPUs; use local quick tests only.
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
