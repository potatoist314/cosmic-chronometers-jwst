---
title: Meeting with MJ Park and Sandro
date: 2026-09-15
section: Guides
theme: Single-fit accuracy
tags: [ceridwen, legac, meeting, research-direction]
job:
---

Meeting notes with Liu Hao's subsequent clarifications. [Current priorities](/wiki/roadmap/) · [Original handwriting](/wiki/f/reports/meeting-2026-09-15-mj-park-sandro.pdf) · [Original clarifications](/wiki/roadmap/#roadmap-amendments).

<details open>
<summary>Corrected meeting notes</summary>

### Metallicity

Resolve two questions first:

- Is Ceridwen fitting absolute metallicity or metallicity relative to solar?
- When Ceridwen uses the FSPS grid, does the metallicity represent total Z or Fe only?

The initial concern was that very massive quiescent galaxies, log(M/M_sun) ≈ 11, appeared extremely metal-poor. A subsequent handwritten annotation says that log Z is absolute rather than solar-relative, so the discrepancy may be less severe. The definition and grid mapping remain the questions to investigate; the annotation does not close them.

The original conversion number and the statement “solar metallicity is only −0.8” remain uncertain in the transcription below.

### Calibration polynomial

Very high priority and expected to be a short fix. Polynomial modes must **not be shorter than 100 Å**.

The meeting notes give the empirical rule of thumb, order ≈ wavelength range / 100, and suggest starting with orders 5, 10, etc. Inspect the polynomial's shape. Too high an order can mimic spectral signals; too low an order can leave flux-calibration problems.

### Literature comparison

Compare established ages, metallicities and the methods used to infer them with Ceridwen. Include expected parameters for local elliptical galaxies. Liu Hao expects them to represent the same population as the LEGA-C galaxies; investigate that comparison.

The handwritten expectations are alpha/Fe ≈ 0.4 and roughly solar metallicity for local ellipticals, with no significant chemical evolution. These are meeting expectations to examine, not a completed literature result.

Look at published LEGA-C Prospector fits, their age and metallicity estimates, and SFH priors. The notes ask which methods are rigorous. This task can start independently of the fitting fixes.

### One strong spectrum

Pick one high-S/N spectrum with strong absorption features for a detailed comparison with the literature. This comes after resolving the metallicity issue.

### Velocity dispersion

Fit velocity dispersion as a broadening parameter. The notes recommend this even though the LEGA-C value is already considered accurate.

### Photometric uncertainties

Investigate incorporating systematic uncertainties in the photometry. Medium priority; the implementation is difficult or uncertain.

### Rest-frame wavelength offsets

The absorption lines in the rest-frame plot do not seem to fall exactly at the expected wavelengths. This is a relatively minor issue. The original suggestion of a redshift offset remains a possibility, not a diagnosis.

### Mg b

Investigate the Mg b fit. This is also a relatively minor issue.

### Noise calibration

Investigate noise calibration and the concern that f_calib reaches the prior's upper bound. The exact meaning of the handwritten percentages is unresolved.

### Mass and metallicity

Plot mass–metallicity.

### Coordination

Post in a group Slack channel. The notes propose a channel with Amanda, MJ and Sandro, and listing every free parameter and prior.

The meeting also notes that more accurate age measurements would be valuable. The separate line “Once confident you are…” is unfinished.

</details>

<details>
<summary>Original transcription reviewed in chat</summary>

This retains the first transcription, including readings later clarified by Liu Hao. Brackets mark transcription uncertainty. The PDF preserves the handwriting, colour and layout.

### Pages 1–3 — Initial concerns

- Check whether “log Z solar” is correctly assigned. Right now, it is Fe only.
- These are very massive quiescent galaxies, log(M/M_sun) ≈ 11, but they appear extremely metal-poor. We expect at least roughly solar metallicity, log Z ≈ 0.
- I think there is an offset. Is the redshift wrong? The absorption lines do not seem to line up.
- Mg b is poorly fitted. Look into this.
- Local elliptical galaxies: alpha/Fe ≈ 0.4 and log Z solar ≈ 0. We expect LEGA-C galaxies to resemble present-day ellipticals, with no significant chemical evolution. This makes the results surprising.
- Are systematic uncertainties included in the photometry? Add calibration uncertainties.
- Has Ceridwen changed its metallicity definition?

### Pages 1–2 — Calibration polynomial

- Empirical rule of thumb: polynomial order ≈ wavelength range / 100. No physical basis.
- Start with orders 5, 10, etc.
- Check the polynomial itself to see how it curves.
- Too high an order mimics spectral signals. Too low an order leaves problems with flux calibration.
- Margin note: “We want [models/modes?] not more than 100 Å.” [Meaning needs clarification; retained without correcting the inequality.]

### Pages 3–4 — Metallicity clarification and remaining questions

- Black annotation: “log Z is absolute, not solar!? So actually the error is not so bad.”
- “Conversion +8.95?” [Number appears to read 8.95; please check.]
- But alpha/Fe should still be +0.4?
- “[She/Ste?] will change Ceridwen to solar metallicity.”
- In α-MC, “log Z solar” refers only to iron relative to hydrogen. Blue annotation: look into that.
- “Solar metallicity is only −0.8.” [Wording retained; the quantity being described is unclear.]

### Pages 4–5 — Noise calibration

- f_calib: “90% hits upper bound.” [Unclear what the 90% refers to.]
- “10% is too high for [other?] model.”
- It is hitting the upper bound of the prior.

### Pages 5–7 — Numbered next steps

- 1. Look into the polynomial.
- 2. Check metallicity to see whether it matches. Fix the metallicity definition.
- 3. Look into noise calibration.
- 4. Plot mass–metallicity.
- 5. Post in a Slack channel in the group.
- 6. In principle, more accurate age measurements would be very useful.
- 7. Pick one beautiful case: high S/N and strong absorption features. This would be a good case to compare against the literature.
- 8. Blue addition: fit velocity dispersion as a broadening parameter, even though LEGA-C is already accurate.
- 8. Separate black entry: “Once confident you are…” [Unfinished.]
- 9. Make a Slack channel with Amanda, MJ and Sandro. List all free parameters and priors.
- 10. Decide what to check against the literature:
   - Velocity dispersion.
   - Ages and published metallicities.
   - “Check against the [theory?].”
   - Star formation history prior?

### Pages 7–8 — Literature comparison

- Annotation attached to ages and metallicities: these have already been modelled in the literature using Prospector fits, in LEGA-C papers.
- These papers use many methods. Find which are rigorous.

</details>

<details>
<summary>Source and review</summary>

- [Original handwritten notes](/wiki/f/reports/meeting-2026-09-15-mj-park-sandro.pdf), pages 1–8. All pages were inspected visually.
- Original request: “/Users/liuhao/Downloads/Untitled\ Notebook\ 2.pdf super helpful meeting today with mj park, sandro - help me transcribe my handwritten notes and clean them up and put them somewhere important on the wiki. let me review your transcription first before putting it in the wiki”
- [Liu Hao's subsequent clarifications and priority decisions](/wiki/roadmap/#roadmap-amendments), 15 September 2026. The corrected section above incorporates these amendments.
- The numbered tasks, rather than scientific investigations or Slack actions, are what this page records.

</details>
