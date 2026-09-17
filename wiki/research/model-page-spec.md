# Model page spec

Date: 2026-09-17 · Status: built · Page: wiki/notes/model.md · Routes: /wiki/model/, /wiki/literature/, /wiki/n/model/

## Purpose

> i have a nice vision of the wiki of just being able to take in at a glance on a single page of every assumption and setting that has gone into the model.

The page is the one place that lists every setting and assumption of the production Ceridwen fit of the LEGA-C DR2 quiescent sample.

## Decisions

| Topic | Decision | Liu Hao's words (2026-09-17) |
|---|---|---|
| Home | Reshape the existing Literature page; no second page | "Reshape the Literature page" |
| Row content | Value, reason, alternatives tested, known-problem flag | "Reason in point form and super fucking concise. Alternatives tested as well. Reasoning as well. known problem flag is also good" |
| Layout | Minimalist | "Just make it as minimalist as possible - i want no overcrowding and just the pure eseentials" |
| Row density | Value and short reason visible; tested and problem bullets on click | "Value + short reason visible" |
| Literature values | Separate section below the settings | "Separate section below" |
| Scope | Includes assumptions nobody chose, marked inherited | "Yes, marked 'inherited'" |
| Name | Model, its own nav entry, replaces Literature in the nav | "'Model' as its own nav entry" |
| Flag rule | Evidence in our results only | "Evidence in our results only" |
| Upkeep | Rule in wiki/AGENTS.md; no automated check | "Rule in AGENTS.md only" |
| Groups | All four | |
| Route | New /wiki/model/; /wiki/literature/ and /wiki/n/papers-quiescent-parameters/ keep working | "New route /wiki/model/, keep old working" |
| Prospector table | In the literature section, collapsed | "Literature section below" |

## Row contract

```text
Setting | Value | Why (at most 6 words) | !
  on click: why · tested (with link) · problem (with link) · source
  tag: inherited (nobody on this project chose it)
```

- Why holds a recorded reason only (a decision by Liu Hao, a meeting point, an experiment result, a paper). Empty when none is recorded; never invented.
- Bullets are fragments, not sentences.
- Every tested and problem bullet links to its note, experiment record or meeting note.
- Symbols use rendered LaTeX.
- A row with nothing behind it has no disclosure control.

## Flag rule

"!" marks a setting with a known problem. Allowed evidence: a result in this repository, or a point recorded in a meeting note. A paper disagreeing with the value is not a flag; it goes in the literature section. Each flag links to its evidence.

Flags at build time:

- tau_dust prior: median 0.187-0.199 in 6 of 6 reference galaxies at orders 3 and 10.
- Dust slope prior: within 0.03 of the -1.0 bound in 4 of 6 at order 10; follows the bound to -2.0 when widened.
- [alpha/Fe] prior: within 0.03 of the -0.2 grid edge in 2 of 6 at orders 3 and 10.
- f_calib prior: M12_98104 at 9.98% at orders 3 and 10; 15 Sep 2026 meeting: "90% hits upper bound".

## Groups and row inventory

### 1. Sample and data

- parent match
- NUVrJ passive
- weak [O II]
- no emission detected
- clean photometry
- one spectrum per object
- pixel rule
- units
- resolution
- emission-line mask
- telluric mask
- fitted pixels
- photometry (COSMOS2015 total)
- photometric error floor

### 2. Stellar model, SFH and dust

- isochrones
- spectral library
- IMF
- abundance scale
- grid nodes
- log M prior
- [Fe/H] prior
- [alpha/Fe] prior
- abundances constant with age
- SFH nodes
- SFH prior
- redshift
- velocity dispersion
- dust law
- tau_dust prior
- dust slope prior
- components switched off

### 3. Calibration, noise and sampler

- calibration polynomial
- spectrum scaling
- f_calib
- likelihood
- nested sampler
- seeds
- pass rule
- posterior draws

### 4. Derived quantities and cosmology

- bin masses
- mass-weighted age
- t20, t50, t80
- [Fe/H] conversion
- f_calib units
- summaries
- cosmology

`## Literature` follows the four groups on the page: comparison figure, paper values per parameter, Jonah Powley's Prospector priors (collapsed), other redshifts, references.

## Implementation

- The note is `wiki/notes/model.md` with section Literature.
- `wiki/research.py` writes the same body to `model/index.html` and `literature/index.html`.
- `wiki/build.py` nav entry Model.
- Each group is one raw HTML `<dl class="model-group">`, each row a `<div class="model-row">` or, when it has bullets, a `<details class="model-row">`.
- No JavaScript.
- Styles in the CSS string of `wiki/research.py`.
- `wiki/notes/papers-quiescent-parameters.md` stays as an obsolete stub with `superseded_by: model`.
- Figure directory `wiki/analyses/model/`.

## Upkeep

Any change to a prior, switch, mask, data source, sampler setting or derived-quantity definition updates its row in the same commit; the rule lives in `wiki/AGENTS.md`.