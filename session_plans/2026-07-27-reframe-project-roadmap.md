# Session: Reframe the project roadmap

- **Date:** 2026-07-27
- **Status:** completed
- **Goal:** Rewrite `PROJECT_ROADMAP.md` so the existing exercises are clearly
  an accelerated framework-building stage, followed by substantial analysis
  using realistic stellar-age constraints from the supervisor's JWST samples.

## Starting point

- The current roadmap spreads the initial reproduction, mock framework,
  systematics, and high-redshift forecast across the full period to early
  October.
- The supervisor described these as a “good first set of steps,” not the full
  project.
- Once the framework works, the intended next stage is to ingest realistic
  JWST stellar-age constraints and test whether the method is competitive at
  high redshift.

## Planned work

1. **Obtain critical strategy review**
   - Request `brutal` reviews from Claude Opus 5 at xhigh effort and GLM 5.2.
   - Ask both models to challenge the timeline, stage boundaries, dependencies,
     and claims that can responsibly be made before real JWST constraints arrive.

2. **Design the revised roadmap**
   - Compress the current five phases into an initial framework-building block.
   - Add explicit post-framework stages for JWST data handoff, ingestion and
     provenance, likelihood adaptation, systematics, high-redshift inference,
     competitiveness assessment, and supervisor iteration.
   - Keep dates concrete while labelling sample delivery as an external
     dependency.

3. **Edit and verify**
   - Update only `session_plans/PROJECT_ROADMAP.md`.
   - Confirm the supervisor's quoted intent is represented accurately.
   - Check Markdown formatting and ensure no unrelated dirty files are changed.

## Definition of done

The roadmap no longer presents the setup exercises as the whole project; the
framework is scheduled substantially earlier, and the remaining project time
is allocated to realistic JWST sample analysis and scientific interpretation.

## Working log

- GLM 5.2 completed a brutal review through the NVIDIA endpoint. It challenged
  the old timeline, required an explicit handoff gate, and separated mock
  validation from real-data competitiveness claims.
- Claude Opus 5 was requested with the `brutal` role and xhigh effort. The
  review timed out after 300 seconds, so no retry or substitute
  model was used and work continued under the configured fallback.
- The revised roadmap retains a bounded high-redshift mock as part of readiness,
  but moves the main scientific deliverable to real JWST sample analysis.
- GLM 5.2 reviewed the edited roadmap, agreed that the timeline and gates are
  materially improved, and recommended making the late-handoff fallback more
  visible. That correction was incorporated.

## Session close-out

- **Final status:** completed
- **Accomplished:** Reframed the old five-phase plan as an accelerated
  pre-travel framework stage, then added real JWST ingestion, inference,
  systematics, competitiveness, and supervisor-review stages.
- **Key decision:** Mock high-redshift work remains a bounded readiness test;
  only real JWST constraints can support a competitiveness claim.
- **External dependency:** Stages 3–5 remain gated on the supervisor's sample
  handoff.
- **Fallback:** A late handoff reduces the early-October outcome to ingestion
  and preliminary inference; competitiveness is deferred.
- **Files changed:** `session_plans/PROJECT_ROADMAP.md`
- **Not completed:** Claude Opus 5 did not return within the review timeout, so
  cross-model agreement could not be confirmed.
- **Exact next starting point:** Continue the current framework work against the
  Stage 1 exit gate, and confirm the exact travel and sample-handoff dates when
  available.
