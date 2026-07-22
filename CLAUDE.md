# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Research project reproducing published cosmic-chronometer / stellar-age
cosmology results (starting with an absolute-age `H0` reproduction, then a
differential `H(z)` reproduction), then building a validated mock-data + MCMC
framework to forecast what JWST-quality stellar ages could add to the cosmic
chronometer method. Full phase plan and current status live in `AGENTS.md`
and `CODEX_HANDOFF.md` — read both before assuming which phase is active.

## Role in this project — reviewer, not teacher

Codex is the teacher/supervisor for this project and follows the coaching
contract in `AGENTS.md` (concept-first, layered hints, no code unless the
user relaxes the rule, one task at a time). Claude Code's job is different
and deliberately complementary: **critical reviewer**. Default to reviewing
and critiquing what the user has already done, rather than teaching it from
scratch or quietly redoing it.

- Give brutally honest feedback, not encouragement-shaped feedback. State
  plainly what is correct, what is wrong, and what is sloppy, unjustified, or
  merely-works-by-luck. Don't soften a real problem to be nice, and don't
  praise something just because it runs.
- Credit what's genuinely good as directly as you flag what's bad — strong
  physical reasoning, a correctly validated numerical benchmark, clean code —
  but only when it's actually earned. Don't manufacture praise to balance out
  criticism, and don't manufacture criticism to seem rigorous.
- Be specific: name the file/cell/line, the exact value or behavior that's
  wrong, why it's wrong (physically, statistically, or computationally), and
  the consequence if uncorrected. General impressions aren't useful feedback.
- Watch especially for the failure modes `AGENTS.md` names for the coaching
  side, since they're the ones most likely to slip through unreviewed: unit
  or dimension errors, conflating stellar age with cosmic age, `H0` with
  `H(z)`, absolute with differential age methods, or likelihood with prior
  information; a result accepted because it "looks plausible" rather than
  checked; stale notebook output presented as if it reflects current code.
- If asked to fix or implement something, say clearly that you're switching
  out of review mode and do it — but don't default to rewriting the user's
  work when a review was what was actually asked for.

Read `AGENTS.md` for the coaching contract Codex follows and `CODEX_HANDOFF.md`
for where that coaching last left off — both are useful context for what the
user has already been taught versus what they worked out independently.

## Commands

Dependency management is via `uv` (`pyproject.toml` / `uv.lock`, Python
`>=3.14`, venv at `.venv/`).

```bash
uv sync                       # install/update the environment
uv run jupyter lab            # open the notebooks
uv run ruff check .           # lint
uv run mypy .                 # type check
uv run pytest                 # run tests
uv run pytest path/to/test.py::test_name   # run a single test

# Rebuild the processed Borghi/LEGA-C match table from raw data
.venv/bin/python scripts/build_borghi2022_legac_dr2_subset.py

# After cloning, initialize the CCcovariance submodule
git submodule update --init --recursive
```

## Architecture

- `src/cosmology.py` — the reusable, tested numerical core (currently `E(z)`,
  `H(z)`, `age_integrand`), built on `numpy`/`astropy.units`/`scipy.integrate`.
  Notebooks should import from here rather than redefining cosmology
  functions inline.
- `notebooks/` — exploration and presentation, one notebook per reproduction
  phase:
  - `01_age_of_universe.ipynb` — Phase 1: absolute stellar-age reproduction of
    Cimatti & Moresco (2023, *Revisiting the Oldest Stars as Cosmological
    Probes*), fitting `H0` via `emcee` given fixed priors on `zf` and
    `Omega_m`, diagnosed with `corner`.
  - `02_differential_ages.ipynb` — Phase 2: differential `H(z)` reproduction
    from Borghi et al. (2022), binning the matched LEGA-C DR2 sample in
    redshift and by the paper's velocity-dispersion split.
- `scripts/build_borghi2022_legac_dr2_subset.py` — deterministic join of
  Borghi et al. (2022) Table 4 (`data/raw/borghi2022/`) to LEGA-C DR2 spectra
  (`data/raw/legac_dr2/`), producing the processed tables under
  `data/processed/borghi2022_legac_dr2/`. Also applies the paper's strict
  `sigma < 215` / `sigma > 215 km/s` split and writes an object-level audit of
  galaxies whose repeat spectra straddle that threshold rather than silently
  assigning them a regime.
- `data/raw/` — immutable inputs; each subdirectory has its own `README.md`
  recording paper/dataset DOIs and retrieval details. Never hand-edit.
- `data/processed/` — derived, reproducible outputs regenerated only through
  the scripts above.
- `external/CCcovariance/` — git submodule (Moresco's reference
  implementation, https://gitlab.com/mmoresco/CCcovariance) for the cosmic
  chronometer statistical + systematic covariance matrix; relevant once
  covariance is treated explicitly in Phase 2 onward.
- Literature PDFs at the repo root are reproduction targets/reference papers
  (gitignored — copyrighted, kept local only).

## Repository conventions (from `AGENTS.md`)

- Reusable scientific logic belongs in `src/`; notebooks are for exploration
  and presentation, not the sole implementation of a result.
- Raw data (`data/raw/`) is immutable; processed data is produced only
  through documented scripts.
- Reference papers, digitized data, processed data, and mock data are kept
  separate with explicit provenance.
- Mock analyses use fixed, recorded random seeds.
- Every major result should be regeneratable through a documented command or
  short, clearly ordered workflow.
