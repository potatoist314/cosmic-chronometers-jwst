# Agent Note Index

Human entry point: `public/index.html`, served at `/wiki/` — Home.
Navigation: Home, Results, Literature, Meetings, Papers, Masking, Code & guides.
Home shows all priorities and planned/running work, with direction, questions and
amendments in the collapsed research record. `/wiki/roadmap/` is the Home alias.
Results: `/wiki/results/`, with saved visual reports and benchmarks first;
other experiment records and earlier analyses/boards remain accessible below.
Meetings: `/wiki/meetings/`. Papers: `/wiki/papers/`, including indexed local PDFs.
Code, notebooks and guides: `/wiki/code/`, followed by documentation and earlier history.
Reference for every prior, sample cut, preprocessing step, sampler setting and
derived quantity, beside the literature values: `notes/papers-quiescent-parameters.md`;
check against `notebooks/ceridwen_integrated_photometry_spectra.ipynb` when defaults change.
Legacy workflow routes: `/wiki/questions/` and `/wiki/experiments/`.
Result pages show fits and captions; full records live at `/wiki/e/<id>/record/`.
Governing presentation rules: `wiki/AGENTS.md`, All pages and Result reporting.
Scientific notation uses rendered LaTeX on every maintained page. See
`wiki/AGENTS.md`, Rendered scientific notation; `assets/math.js` and `math.css`
use locally served KaTeX, including for tables and dynamically inserted captions.
No agent commentary anywhere, including research records and earlier notes.
Retain factual content, technical explanations, concrete limitations and originals.
Research contract and templates: `research/README.md`, `research/templates/`.
User direction: `research/direction.md`, with optional light edits and retained originals.
Research priorities: Home and `/wiki/roadmap/`, from the single
Roadmap task list in `research/direction.md`. Priorities use 1–10, with 10 highest;
difficulty and dependencies remain separate. Unspecified work stays unscored.
Meeting: `notes/meeting-2026-09-15-mj-park-sandro.md` — corrected meeting notes,
original transcription and PDF, linked from Home and Meetings. Transcribe and
lightly rephrase only; never add commentary. Standing rule: `wiki/AGENTS.md`.
Meeting: `notes/meeting-2026-09-17-student-group.md` — student group meeting: questions after the updates and points raised, with the original transcription and handwriting.
Meeting: `notes/meeting-2026-09-17-jonah-powley.md` — Jonah Powley on Prospector fits of quiescent galaxies: SFH prior, abundances, dust and infrared, his setup, with the original transcription and handwriting.
Research source records: `research/questions/` and `research/experiments/`.
Priority detail pages: `/wiki/p/<id>/`, with independent resolution buttons and dated history.
`activity.py` stores immutable note revisions, ink and status events in `research/activity/`.
`assets/activity.js` and `assets/activity.css` provide writing sheets and figure markup.
Pencil writing uses scribble-to-erase and continuous finger scrolling.
Ink rendering caches finished strokes and batches incoming samples per display frame.
Browser drafts use IndexedDB; saved originals remain on the Mac across rebuilds.
Chat updates use the same `activity.save` contract in `research/README.md`.
Original analyses: `notes/*.md`, with links to their structured research entries.
Earlier experiment boards remain at `/wiki/themes/`; source notes at `/wiki/earlier/`.
Build with `python3 wiki/build.py`. Existing reasoning is not reconstructed.

## Research questions

- `research/questions/q-fitting-choices.md` — calibration, priors, masks and nuisance parameters
- `research/questions/q-mock-recovery.md` — mock recovery, including the planned quiescent injection
- `research/questions/q-sample-selection.md` — DR2 inputs and inferred quiescence
- `research/questions/q-population-results.md` — both DR2 runs, population relations and residuals
- `research/questions/q-compute.md` — repeatability, GPU campaigns and numerical comparisons

- `research/experiments/e-quiescent-mock.md` — approved intrinsic truth and physical explanation; 1%, 5%, and 10% noise cases planned, observing setup undecided

The 28 existing experiment entries cover all 11 analysis notes and all current
and archived Ceridwen result groups. `source_notes` provides backlinks;
`related_questions` shares one experiment across questions. `result_groups`
records coverage without moving evidence. Figure captions flag material
comparison issues; factual configurations and unit limitations remain in the record. Recorded status does not imply user review.

## Single-fit accuracy

- `notes/calibration-order.md` — Calibration polynomial order (2026-09-15)
- `notes/dr2-new-defaults.md` — DR2 quiescent refit with the new production defaults (2026-09-07)
- `notes/redshift-sigma-wiggle.md` — Free redshift and velocity dispersion in the DR2 fit (2026-09-06)
- `notes/fit-accuracy-knobs.md` — Fit-accuracy knobs after the calibration polynomial (2026-09-06)
- `notes/calibration-polynomial-dr2.md` — Calibration polynomial in the DR2 pipeline (2026-09-05 · t_ab2b8a0b)
- `notes/absorption-line-mask.md` — Absorption-line pixel mask (2026-09-02 · t_8f62974f)

## Masking

- `notes/jwst-image-masking.md` — handwritten JWST image-masking workflow, observing context, and seven-page transcription (2026-09-14)
- `/wiki/masking/` — dedicated image-masking category, linked from the sidebar

## Sample and data
- `notes/data-pipeline.md` — Data pipeline (2026-09-09 · old: _old/codebase/data-pipeline.html)
- `notes/sfms-quiescent.md` — Quiescent sample on the star-forming sequence (2026-09-07)
- `notes/dr2-quiescent-sample.md` — DR2 quiescent sample (2026-09-03 · t_d0d3a321)

## Population results

- `notes/stacked-chi2-and-median-pull.md` — Stacked χ², five stacking recipes and the per-feature pull (2026-09-10 · t_6417df23); includes the M11_216899 and M12_184916 spike spectra.
- `notes/per-galaxy-diagnostics-gallery.md` — Per-galaxy fit diagnostics, gallery (2026-09-05 · t_8a78968d)
- `notes/per-galaxy-fit-diagnostics.md` — Per-galaxy fit diagnostics (2026-09-05 · t_8a78968d)
- `notes/ceridwen-results.md` — Ceridwen common results board (2026-09-04 · t_44b5da5c)
- `notes/chronometer-notebook-figures.md` — Chronometer notebook figures (2026-08-20 · status: obsolete · obsolete · obsolete)

## Compute

- `notes/calibration-speedup.md` — Calibration polynomial speed-up (2026-09-15)
- `notes/ceridwen-checkpoint-spectrum-evolution.md` — Ceridwen checkpoint spectrum evolution (2026-09-04 · t_ed2b739d)
- `notes/vast-ai-gpu-workflow.md` — Vast.ai GPU workflow (2026-08-30 · t_2fc31190)
- `notes/modal-gpu-workflow.md` — Modal GPU workflow (2026-08-28 · old: _old/guides/modal-gpu-workflow.html · obsolete)

## Model and code reference

- `notes/default-fit-parameters.md` — Current default model (2026-09-15 · obsolete, superseded by `notes/papers-quiescent-parameters.md`)
- `notes/notebook-map.md` — Notebook map (2026-09-09 · old: _old/notebooks/notebook-map.html)
- `notes/ceridwen-observations-model.md` — Ceridwen: observations and SedModel (2026-09-06 · old: _old/codebase/ceridwen-observations-model.html)
- `notes/ceridwen-likelihood-sampling.md` — Ceridwen: likelihood and sampling (2026-09-06 · old: _old/codebase/ceridwen-likelihood-sampling.html)
- `notes/overview.md` — Ceridwen project overview (2026-09-01 · old: _old/overview.html)
- `notes/active-codebase-map.md` — Active Ceridwen codebase map (2026-09-01 · old: _old/codebase/active-codebase-map.html)
- `notes/ceridwen-ssp-csp.md` — Ceridwen: SSP grids to composite spectra (2026-08-30 · old: _old/codebase/ceridwen-ssp-csp.html)
- `notes/tests-as-documentation.md` — Tests as documentation (2026-08-25 · old: _old/codebase/tests-as-documentation.html)
- `notes/reading-order.md` — Reading order (2026-08-25 · old: _old/guides/reading-order.html · superseded by `overview`)
- `notes/python-patterns.md` — Python patterns (2026-08-25 · old: _old/guides/python-patterns.html)
- `notes/project-modules.md` — Project support modules (2026-08-25 · old: _old/codebase/project-modules.html · superseded by `active-codebase-map`)
- `notes/project-map.md` — Project map (2026-08-25 · old: _old/codebase/project-map.html · superseded by `active-codebase-map`)
- `notes/ceridwen-architecture.md` — Ceridwen architecture (2026-08-25 · old: _old/codebase/ceridwen-architecture.html)

## Background reading

- `notes/papers-spectral-fitting.md` — Papers: stellar-population fitting (2026-08-25 · source: papers/spectral fitting/README.md)
- `notes/papers-cosmic-chronometers.md` — Papers: cosmic chronometers (2026-08-25 · source: papers/README.md)
- `notes/papers-quiescent-parameters.md` — LEGA-C quiescent-galaxy literature values: every prior, sample cut, preprocessing step, sampler setting and derived quantity, plus Jonah Powley's Prospector priors (2026-09-17 · source: papers/quiescent populations/README.md)

## Log

- `notes/wiki-log.md` — Wiki log (2026-09-04 · status: obsolete · obsolete)

## Result presentation

- `research_figures.py` validates and renders explicit figure references.
- `research.py` renders visual reports separately from full research records.
- `Figures` maps saved images or notebook outputs to a target, arm and view.
- Generated notebook images live only under `public/research-images/`.
- Fits open first. Target selection stays fixed across SFH and posterior views.
- All 28 result pages retain their existing URLs and underlying records.

Absorption-feature plotting default: `scripts/spectral_figures.py` assigns fixed
colours and one right-side legend. Finish marked figures with
`spectral_tight_layout`; see `notes/notebook-map.md`.
