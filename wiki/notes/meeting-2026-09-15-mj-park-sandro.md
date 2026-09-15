---
title: Meeting with MJ Park and Sandro
date: 2026-09-15
section: Meetings
theme: Single-fit accuracy
tags: [ceridwen, legac, meeting, research-direction]
job:
---

[Current priorities](/wiki/) · [Original handwriting](/wiki/f/reports/meeting-2026-09-15-mj-park-sandro.pdf) · [Original clarifications](/wiki/#roadmap-amendments).

<details open id="corrected-meeting-notes">
<summary>Meeting notes</summary>

### Metallicity

Resolve two questions first:

- Is Ceridwen fitting absolute metallicity or metallicity relative to solar?
- When Ceridwen uses the FSPS grid, does the metallicity represent total Z or Fe only?

These are very massive quiescent galaxies, log(M/M_sun) ≈ 11, but they appear extremely metal-poor. We expect at least roughly solar metallicity. Log Z is absolute, not solar!? So actually the error is not so bad. But alpha/Fe should still be +0.4?

### Calibration polynomial

Very high priority and expected to be a short fix. Polynomial modes must **not be shorter than 100 Å**.

The empirical rule of thumb is order ≈ wavelength range / 100, with no physical basis. Start with orders 5, 10, etc. Inspect the polynomial's shape. Too high an order can mimic spectral signals; too low an order can leave flux-calibration problems.

### Literature comparison

Compare established ages, metallicities and the methods used to infer them with Ceridwen. Include expected parameters for local elliptical galaxies, which should be the same population as the LEGA-C galaxies.

For local ellipticals, expect alpha/Fe ≈ 0.4 and roughly solar metallicity, with no significant chemical evolution.

Look at published LEGA-C Prospector fits, their velocity dispersions, ages, metallicities and SFH priors. Which methods are rigorous? This is high priority and can start independently of the fitting fixes.

### One strong spectrum

Pick one high-S/N spectrum with strong absorption features for a detailed comparison with the literature. This comes after resolving the metallicity issue.

### Velocity dispersion

Fit velocity dispersion as a broadening parameter, even though the LEGA-C value is already accurate.

### Photometric uncertainties

Investigate incorporating systematic uncertainties in the photometry. Medium priority; the implementation is difficult or uncertain.

### Rest-frame wavelength offsets

The absorption lines in the rest-frame plot do not seem to fall exactly at the expected wavelengths. Is the redshift wrong? This is a relatively minor issue.

### Mg b

Investigate the Mg b fit. This is also a relatively minor issue.

### Noise calibration

Investigate noise calibration. f_calib is hitting the prior's upper bound.

### Mass and metallicity

Plot mass–metallicity.

### Coordination

Post in a group Slack channel. Make a channel with Amanda, MJ and Sandro, and list every free parameter and prior.

More accurate age measurements would be very useful.

“Once confident you are…” [unfinished]

</details>

<details id="original-transcription-reviewed-in-chat">
<summary>Original transcription</summary>

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
- Margin note: “We want [models/modes?] not more than 100 Å.”

### Pages 3–4 — Metallicity clarification and remaining questions

- Black annotation: “log Z is absolute, not solar!? So actually the error is not so bad.”
- “Conversion +[8.95?]”
- But alpha/Fe should still be +0.4?
- “[She/Ste?] will change Ceridwen to solar metallicity.”
- In α-MC, “log Z solar” refers only to iron relative to hydrogen. Blue annotation: look into that.
- “Solar metallicity is only −0.8.”

### Pages 4–5 — Noise calibration

- f_calib: “90% hits upper bound.”
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

<details id="source-and-review">
<summary>Sources</summary>

- [Original handwritten notes](/wiki/f/reports/meeting-2026-09-15-mj-park-sandro.pdf), pages 1–8.
- Original request: “/Users/liuhao/Downloads/Untitled\ Notebook\ 2.pdf super helpful meeting today with mj park, sandro - help me transcribe my handwritten notes and clean them up and put them somewhere important on the wiki. let me review your transcription first before putting it in the wiki”
- [Original clarifications and priority decisions](/wiki/#roadmap-amendments), 15 September 2026.

</details>
