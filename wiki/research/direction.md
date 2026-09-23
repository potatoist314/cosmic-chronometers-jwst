---
kind: direction
id: research-direction
title: Research direction
date: 2026-09-15
---

## Your words

```json
[
  {
    "date": "2026-09-12",
    "text": "Like alpha enhanced SSP grids are the new thing i can introduce - and especially because I'm running on ceridwen, that's also new.",
    "display_text": "Alpha-enhanced SSP grids are the new thing I can introduce. Running on Ceridwen is also new."
  },
  {
    "id": "d-58012819-16b2-4ce5-be32-94713f7eb474",
    "title": "Use COSMOS2025 as the main photometry catalogue",
    "text": "Photometry is the brightness of a galaxy measured through a set of filters. COSMOS2025 is the 2025 photometry catalogue of the COSMOS field. Sandro Tacchella advised that we use COSMOS2025 as the main (fiducial) catalogue from now on.\n\nSandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
    "date": "2026-09-23"
  }
]
```

## Roadmap

```json
[
  {
    "id": "metallicity",
    "title": "Resolve the metallicity definition",
    "priority": 10,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#metallicity",
    "details": "Is Ceridwen fitting absolute or solar-relative metallicity? Does its FSPS grid represent total Z or Fe only? Most immediate investigation."
  },
  {
    "id": "science-skills-wiki-format",
    "title": "Set up science skills and workflows; outline the wiki submission format for agents",
    "priority": 10,
    "source": "wiki/research/direction.md",
    "details": "Set up appropriate science skills and workflow creation for this workspace. Outline a proper format for agents' wiki submissions."
  },
  {
    "id": "cosmos-2020-2025-photometry",
    "title": "Replace COSMOS2015 photometry with COSMOS 2020/2025",
    "priority": 10,
    "source": "wiki/research/questions/q-cosmos-photometry.md",
    "details": "Replace COSMOS2015 photometry with COSMOS 2020/2025 photometry in the Ceridwen fits and see what changes in the fit."
  },
  {
    "id": "calibration-polynomial",
    "title": "Investigate the calibration polynomial",
    "priority": 9,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#calibration-polynomial",
    "details": "Polynomial modes must not be shorter than 100 \\(\\text{\\AA}\\). Inspect the polynomial and the empirical order rule.",
    "effort": "Expected short fix"
  },
  {
    "id": "local-ellipticals-ground-truth",
    "title": "Pull local elliptical galaxies as relative 'ground truth' to compare outputs against",
    "priority": 9,
    "source": "wiki/research/direction.md"
  },
  {
    "id": "dust-index-railing-weak-uv",
    "title": "Look into why the Conroy dust index is railing and the UV is so weak",
    "priority": 9,
    "source": "wiki/research/direction.md"
  },
  {
    "id": "emission-lines-model-mask-ignore",
    "title": "Emission lines: model, mask or ignore",
    "priority": 9,
    "source": "wiki/research/questions/q-emission-lines.md",
    "details": "Decide whether the Ceridwen fits model, mask or ignore emission lines, on a physically justified reason."
  },
  {
    "id": "emission-line-marginalisation",
    "title": "Marginalise H-beta and other line emission",
    "priority": 9,
    "source": "wiki/research/questions/q-emission-lines.md",
    "details": "Account for H-beta and other line emission through marginalisation, which Liu Hao describes as fitting a Gaussian so the line needs no mask.",
    "effort": "Unsure what this is and how to implement it"
  },
  {
    "id": "literature-comparison",
    "title": "Compare published methods, ages and metallicities",
    "priority": 8,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#literature-comparison",
    "details": "Include expected parameters for local elliptical galaxies and their relationship to the LEGA-C population. Compare established inference methods with Ceridwen. Can start independently."
  },
  {
    "id": "alpha-fe-t50-vs-mass",
    "title": "Plot \\([\\alpha/\\mathrm{Fe}]\\) and \\(t_{50}\\) against stellar mass",
    "priority": 8,
    "source": "wiki/research/direction.md",
    "details": "Do plots of something like \\([\\alpha/\\mathrm{Fe}]\\) versus stellar mass, and \\(t_{50}\\) versus stellar mass. The physical justification is that you can constrain a relative trend given only a corner plot distribution if you can plot against some x axis."
  },
  {
    "id": "dr2-sample-new-settings",
    "title": "Refit the big DR2 sample with new settings",
    "priority": 8,
    "source": "wiki/research/experiments/e-afe-t50-vs-mass.md",
    "details": "Fit the new settings to the big DR2 sample to uncover large-scale trends across the sample, such as \\([\\alpha/\\mathrm{Fe}]\\) versus mass."
  },
  {
    "id": "rising-sfh-continuity-prior",
    "title": "Consider adding a rising SFH continuity prior",
    "priority": 8,
    "source": "wiki/research/direction.md",
    "details": "Paper: Turner et al. (2025), MNRAS 537:1826, arXiv:2410.05377, section 3.3. PDF in papers/spectral fitting/."
  },
  {
    "id": "strong-spectrum",
    "title": "Select one high-\\(\\mathrm{S/N}\\) spectrum with strong absorption features",
    "priority": 7,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#one-strong-spectrum",
    "details": "Choose one case for detailed fitting and literature comparison. Chosen 17 Sep 2026: M1_210210.",
    "depends_on": [
      "metallicity"
    ]
  },
  {
    "id": "ifu-surveys-spectra-photometry",
    "title": "Spectrum and photometry fitting: SDSS/MaNGA (spelling uncertain)",
    "priority": 7,
    "source": "wiki/research/questions/q-ifu-surveys.md",
    "details": "Look into fitting spectra and photometry for SDSS/MaNGA (spelling uncertain), which Liu Hao notes are IFU surveys and categorically different."
  },
  {
    "id": "metallicity-evolution-model",
    "title": "Simple parametric metallicity evolution model",
    "priority": 7,
    "source": "wiki/research/questions/q-metallicity-evolution.md",
    "details": "Try fitting a simple parametric metallicity evolution model with one free parameter or so, apart from just a fixed metallicity.",
    "effort": "Unsure on implementation"
  },
  {
    "id": "velocity-dispersion",
    "title": "Fit velocity dispersion as a broadening parameter",
    "priority": 6,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#velocity-dispersion"
  },
  {
    "id": "mock-spectra-test-suite",
    "title": "Set up the mock spectra test suite",
    "priority": 6,
    "source": "wiki/research/direction.md"
  },
  {
    "id": "photometric-systematics",
    "title": "Incorporate systematic photometric uncertainties",
    "priority": 5,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#photometric-uncertainties",
    "effort": "Difficult or implementation uncertain"
  },
  {
    "id": "wavelength-offsets",
    "title": "Check rest-frame absorption-line wavelength offsets",
    "priority": 3,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#rest-frame-wavelength-offsets",
    "details": "The lines do not seem to sit exactly at the expected wavelengths. Relatively minor issue."
  },
  {
    "id": "mg-b",
    "title": "Investigate Mg b fitting",
    "priority": 3,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#mg-b",
    "details": "Relatively minor issue."
  },
  {
    "id": "noise-calibration",
    "title": "Investigate noise calibration and \\(f_{\\mathrm{calib}}\\)",
    "priority": null,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#noise-calibration",
    "details": "Retain the concern about reaching the prior's upper bound; the handwritten percentages remain uncertain."
  },
  {
    "id": "mass-metallicity",
    "title": "Plot mass and metallicity",
    "priority": null,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#mass-and-metallicity"
  },
  {
    "id": "slack-coordination",
    "title": "Coordinate in a Slack channel",
    "priority": null,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#coordination",
    "details": "Amanda, MJ and Sandro."
  },
  {
    "id": "parameters-priors",
    "title": "Document all free parameters and priors",
    "priority": null,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#coordination"
  },
  {
    "id": "tau-dust-railing",
    "title": "Check \\(\\tau_{\\mathrm{dust}}\\) for railing under Uniform(0, 1)",
    "priority": null,
    "source": "wiki/notes/model.md",
    "details": "Check whether the \\(\\tau_{\\mathrm{dust}}\\) posterior rails at 1 after the prior changed from Uniform(0, 0.2) to Uniform(0, 1) on 17 Sep 2026. Previous medians: Uniform(0, 0.2), 0.187-0.199 for 6 of 6 reference galaxies, and Uniform(0, 2), 0.31-0.49 for those six galaxies, 0.45 across 187 galaxies."
  },
  {
    "id": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
    "title": "Check whether extra dust around young stars is on",
    "details": "dust1 is extra dust around young stars (birth-cloud dust). Check whether the Ceridwen fit switches it on.",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  },
  {
    "id": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
    "title": "Test the effect of a steeper dust curve",
    "details": "The dust curve sets how strongly dust dims each wavelength. Check whether a steeper curve changes the model's full spectrum (SED).",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  },
  {
    "id": "p-9c4708da-30a8-4268-8281-f50252096add",
    "title": "Confirm which dust curve the fit uses",
    "details": "Check whether the Ceridwen fit uses the dust curve of Kriek and Conroy (2013).",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  },
  {
    "id": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
    "title": "Allow dust slopes down to −3",
    "details": "The dust index is the slope of the dust curve. Refit with the index allowed down to −3. Check whether the fit converges.",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  },
  {
    "id": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
    "title": "Repeat the fit with older MIST models",
    "details": "The current models are alpha-enhanced: extra magnesium, oxygen and similar elements. Check whether the old MIST models without this show the same problem.",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  },
  {
    "id": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
    "title": "Check filter curves and Milky Way dust correction",
    "details": "Filter curves say which wavelengths each band sees. Check that they and the Milky Way dust correction match the catalogue photometry.",
    "effort": "",
    "priority": null,
    "depends_on": [],
    "source": "wiki/research/direction.md"
  }
]
```

## Amendments

```json
[
  {
    "date": "2026-09-15",
    "text": "okay, here are some clarifications. offset -> the absorption lines in the rest frame plot don't seem to be exactly at the correct wavelength (relatively minor issue). Look into Mg B fitting spectral line (again, relatively minor issue). I think i should develop a grading system from 1-10 on research priority and thigns to look into, this would fit well on the wiki. Look into expected parameters for local elliptical galaxies, which should be the same population as Lega C galaxies (medium-high priority). Incorporating systematic uncertainties in photometry (medium priority, but difficult or at least unsure how to implement). Metallicity definition (is ceridwen fitting absolute metallicity or solar metallicity, and when ceridwen uses the FSPS grid, is it modelling the metallicity returned as Z total or Fe only - very high priority, probably most immediate thing to look into). Calibration polynomial - very high priority; easy short fix as well. The 100 angstrom note -> we want frequency modes not shorter than 100 angstrom in the polynomial, is what was meant. The numbered next steps look good, fit velocity dispersion as broadening parameter is medium importance. picking one high S/N strong absorption feature spectra would be pretty high priority but must come after metallicity is fixed. The literature check on established ages and metallicities and the methods they use to do this, comparing to ceridwen is also high priority and not bound by anything",
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md",
    "display_text": "okay, here are some clarifications. offset -> the absorption lines in the rest frame plot don't seem to be exactly at the correct wavelength (relatively minor issue). Look into Mg B fitting spectral line (again, relatively minor issue). I think i should develop a grading system from 1-10 on research priority and thigns to look into, this would fit well on the wiki. Look into expected parameters for local elliptical galaxies, which should be the same population as Lega C galaxies (medium-high priority). Incorporating systematic uncertainties in photometry (medium priority, but difficult or at least unsure how to implement). Metallicity definition (is ceridwen fitting absolute metallicity or solar metallicity, and when ceridwen uses the FSPS grid, is it modelling the metallicity returned as Z total or Fe only - very high priority, probably most immediate thing to look into). Calibration polynomial - very high priority; easy short fix as well. The 100 angstrom note -> we want frequency modes not shorter than 100 angstrom in the polynomial, is what was meant. The numbered next steps look good, fit velocity dispersion as broadening parameter is medium importance. picking one high \\(\\mathrm{S/N}\\) strong absorption feature spectra would be pretty high priority but must come after metallicity is fixed. The literature check on established ages and metallicities and the methods they use to do this, comparing to ceridwen is also high priority and not bound by anything"
  },
  {
    "date": "2026-09-15",
    "text": "velocity dispersion should be 6. local ellipticals go together with literature comparison on methods. strong spectrum case can be 7. keep this 1-10 scale for all future research roadmap guidance and discussion - save this setup in the appropriate .md files",
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md"
  },
  {
    "date": "2026-09-15",
    "text": "Implement the plan.",
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md"
  },
  {
    "date": "2026-09-17",
    "text": "i want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectoy.",
    "display_text": "I want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectory."
  },
  {
    "date": "2026-09-17",
    "text": "change the tau dust prior back to (0,1)"
  },
  {
    "date": "2026-09-17",
    "text": "resume, although add it as a research note/roadmap, to check for railing"
  },
  {
    "date": "2026-09-17",
    "text": "add as a high research priority: setup appropriate science skills / workflow creation for this current workspace, and outline a proper format for wiki submissions for agents",
    "display_text": "Add as a high research priority: set up appropriate science skills / workflow creation for this current workspace, and outline a proper format for wiki submissions for agents."
  },
  {
    "date": "2026-09-17",
    "text": "10",
    "source_ref": "Score for the science skills and wiki submission format priority"
  },
  {
    "date": "2026-09-17",
    "text": "well, give z a plus minus 0.1 wiggle and dont even make these opt in switches - just have this as default and note it appropriately",
    "source_ref": "Redshift and stellar velocity dispersion as default free parameters"
  },
  {
    "date": "2026-09-17",
    "text": "another priority - 8/10 -> do plots of something like alpha/fe versus stellar mass, and t50 versus stellar mass . the physical justification is that you can constrain a relative trend given only a corner plot distribution if you can plot against some x axis",
    "display_text": "Another priority, 8/10: do plots of something like \\([\\alpha/\\mathrm{Fe}]\\) versus stellar mass, and \\(t_{50}\\) versus stellar mass. The physical justification is that you can constrain a relative trend given only a corner plot distribution if you can plot against some x axis."
  },
  {
    "date": "2026-09-17",
    "text": "add another priority - setting up the mock spectra test suite, 6/10",
    "display_text": "Add another priority: setting up the mock spectra test suite, 6/10."
  },
  {
    "date": "2026-09-17",
    "text": "another priority - pull local elliptical galaxies as relative 'ground truth' to compare my outputs against, 9/10",
    "display_text": "Another priority: pull local elliptical galaxies as relative 'ground truth' to compare my outputs against, 9/10."
  },
  {
    "date": "2026-09-17",
    "text": "8/10 priority - consider adding a rising sfh continuityi prior, and pull and download the turner 2015 paper into this project repo",
    "display_text": "8/10 priority: consider adding a rising SFH continuity prior, and pull and download the Turner 2015 paper into this project repo."
  },
  {
    "date": "2026-09-17",
    "text": "research priority to add - look into why conroy dust index is railing and UV is so weak - 9/10 priority",
    "display_text": "Research priority to add: look into why the Conroy dust index is railing and the UV is so weak. 9/10 priority."
  },
  {
    "date": "2026-09-21",
    "text": "okay, add this to one of the research priorities on the wiki, priority of 9, to either model, mask, or ignore emission lines, but with a physically justified reason.",
    "display_text": "Okay, add this to one of the research priorities on the wiki, priority of 9: to either model, mask, or ignore emission lines, but with a physically justified reason."
  },
  {
    "date": "2026-09-21",
    "text": "this seems really circular? using a model to decide what a sed model should do? or is there some independence i'm not seeing here",
    "display_text": "This seems really circular? Using a model to decide what an SED model should do? Or is there some independence I'm not seeing here?"
  },
  {
    "date": "2026-09-21",
    "text": "ugh. add this explanation to the wiki priority 9 item.",
    "display_text": "Ugh. Add this explanation to the wiki priority 9 item."
  },
  {
    "date": "2026-09-21",
    "text": "but does the model account for AGB ionisation, or just the classic UV ionisation",
    "display_text": "But does the model account for AGB ionisation, or just the classic UV ionisation?"
  },
  {
    "date": "2026-09-21",
    "text": "very annoying - add this new info to the wiki",
    "display_text": "Very annoying - add this new info to the wiki."
  },
  {
    "date": "2026-09-21",
    "text": "High research priority (10) - incorporate COSMOS 2020/2025 photometry as a replacement for 2015 and see what changes in the fit"
  },
  {
    "date": "2026-09-21",
    "text": "look into fitting spectra / phot for STSS/MANGA surveys (not sure if spelt correctly) - priority 7 (these are categorically different, are IFU surveys)",
    "display_text": "Look into fitting spectra / photometry for SDSS/MaNGA (spelling uncertain) surveys - priority 7 (these are categorically different, are IFU surveys)."
  },
  {
    "date": "2026-09-21",
    "text": "research priority 7 (but unsure on implementation) - try fitting a simple parametric metallicity evolution model with one free parameter or so, apart from just a fixed metallicity"
  },
  {
    "date": "2026-09-21",
    "text": "high priority but unsure implementation (priority 9) - try and account for h beta et cetera emission through marginalisation - not too sure what this is, but it fits some gaussian for the emission line to incorporate for its effect, so no longer need to mask the line (which contains information)",
    "display_text": "High priority but unsure implementation (priority 9): try and account for H-beta et cetera emission through marginalisation. Not too sure what this is, but it fits some Gaussian for the emission line to incorporate for its effect, so no longer need to mask the line (which contains information)."
  },
  {
    "date": "2026-09-21",
    "text": "moderate priority (8) - try fitting new settings to the big dr2 sample to uncover large scale trends (e.g. alpha fe versus mass) across the datasample",
    "display_text": "Moderate priority (8): try fitting new settings to the big DR2 sample to uncover large-scale trends (e.g. alpha/Fe versus mass) across the data sample."
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:39:15.941579+00:00",
    "text": "Sandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
    "kind": "direction",
    "target": "d-58012819-16b2-4ce5-be32-94713f7eb474",
    "request_id": "58012819-16b2-4ce5-be32-94713f7eb474",
    "request": {
      "id": "58012819-16b2-4ce5-be32-94713f7eb474",
      "revision": "20279ff26cef315885912be2c4c5b4c68fb80d8c4a9adefeb752a9d813f976b2",
      "kind": "direction",
      "title": "COSMOS2025 as the fiducial catalogue",
      "text": "Sandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\""
    },
    "before": null,
    "after": {
      "id": "d-58012819-16b2-4ce5-be32-94713f7eb474",
      "title": "COSMOS2025 as the fiducial catalogue",
      "text": "Sandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
      "date": "2026-09-23"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:39:24.853561+00:00",
    "text": "Check birth-cloud dust (dust1)\n\nCheck whether birth-cloud dust (dust1) is switched on in the Ceridwen fit.",
    "kind": "priority",
    "target": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
    "request_id": "cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
    "request": {
      "id": "cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
      "revision": "8e5bccde737b315de3c257b17c638d7d13d13e3c150ef6cf1e14fdc8eed33321",
      "kind": "priority",
      "title": "Check birth-cloud dust (dust1)",
      "details": "Check whether birth-cloud dust (dust1) is switched on in the Ceridwen fit.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
      "title": "Check birth-cloud dust (dust1)",
      "details": "Check whether birth-cloud dust (dust1) is switched on in the Ceridwen fit.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:39:32.364923+00:00",
    "text": "Test the SED effect of a steeper dust law\n\nCheck whether the steeper dust attenuation law changes the model SED.",
    "kind": "priority",
    "target": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
    "request_id": "89d4b013-04a4-4c68-ae69-f4a6fc890749",
    "request": {
      "id": "89d4b013-04a4-4c68-ae69-f4a6fc890749",
      "revision": "c33df3f9176aa2f07c02355cf107457ec7eafa6c9203195ecc87447fb7d33efb",
      "kind": "priority",
      "title": "Test the SED effect of a steeper dust law",
      "details": "Check whether the steeper dust attenuation law changes the model SED.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
      "title": "Test the SED effect of a steeper dust law",
      "details": "Check whether the steeper dust attenuation law changes the model SED.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:39:41.906333+00:00",
    "text": "Confirm the Kriek & Conroy dust prescription\n\nCheck whether the Ceridwen fit assumes the Kriek and Conroy dust attenuation prescription.",
    "kind": "priority",
    "target": "p-9c4708da-30a8-4268-8281-f50252096add",
    "request_id": "9c4708da-30a8-4268-8281-f50252096add",
    "request": {
      "id": "9c4708da-30a8-4268-8281-f50252096add",
      "revision": "b4f9282eab3ed074c125ec49ac8a3cf0d8cffa38c108c20b859c2391e8a92e48",
      "kind": "priority",
      "title": "Confirm the Kriek & Conroy dust prescription",
      "details": "Check whether the Ceridwen fit assumes the Kriek and Conroy dust attenuation prescription.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-9c4708da-30a8-4268-8281-f50252096add",
      "title": "Confirm the Kriek & Conroy dust prescription",
      "details": "Check whether the Ceridwen fit assumes the Kriek and Conroy dust attenuation prescription.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:39:51.559408+00:00",
    "text": "Refit with dust slopes down to −3\n\nRun the fit with the dust index allowed down to −3 and check whether it converges.",
    "kind": "priority",
    "target": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
    "request_id": "03df19b8-1627-4f43-a51d-1601bbadaf7a",
    "request": {
      "id": "03df19b8-1627-4f43-a51d-1601bbadaf7a",
      "revision": "22f9fdcc7ec7d34ba3e9872402b9f4b6c781e2bd770c20e7df5d1e3bbb317404",
      "kind": "priority",
      "title": "Refit with dust slopes down to −3",
      "details": "Run the fit with the dust index allowed down to −3 and check whether it converges.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
      "title": "Refit with dust slopes down to −3",
      "details": "Run the fit with the dust index allowed down to −3 and check whether it converges.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:40:06.004262+00:00",
    "text": "Repeat the fit with non-alpha-enhanced MIST models\n\nCheck whether the old MIST models (not alpha-enhanced) show the same problem.",
    "kind": "priority",
    "target": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
    "request_id": "1b7c64b9-ce3b-4c29-890e-d0f30c458412",
    "request": {
      "id": "1b7c64b9-ce3b-4c29-890e-d0f30c458412",
      "revision": "cca97b3fd091cfe37867915ed6082104380c8d728c9bcfcd99650c2392829923",
      "kind": "priority",
      "title": "Repeat the fit with non-alpha-enhanced MIST models",
      "details": "Check whether the old MIST models (not alpha-enhanced) show the same problem.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
      "title": "Repeat the fit with non-alpha-enhanced MIST models",
      "details": "Check whether the old MIST models (not alpha-enhanced) show the same problem.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T12:40:13.719484+00:00",
    "text": "Check filter curves and Galactic extinction\n\nCheck that the filter curves and Galactic extinction correction match the input photometry.",
    "kind": "priority",
    "target": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
    "request_id": "dae9a5c2-e688-47de-b53a-1cafffc201dd",
    "request": {
      "id": "dae9a5c2-e688-47de-b53a-1cafffc201dd",
      "revision": "bfbecb75af57559df7cdf706b959e2e1b91b4f7a384288153e624c7d71e16daa",
      "kind": "priority",
      "title": "Check filter curves and Galactic extinction",
      "details": "Check that the filter curves and Galactic extinction correction match the input photometry.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": null,
    "after": {
      "id": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
      "title": "Check filter curves and Galactic extinction",
      "details": "Check that the filter curves and Galactic extinction correction match the input photometry.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:32:27.080118+00:00",
    "text": "Photometry is the brightness of a galaxy measured through a set of filters. COSMOS2025 is the 2025 photometry catalogue of the COSMOS field. Sandro Tacchella advised that we use COSMOS2025 as the main (fiducial) catalogue from now on.\n\nSandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
    "kind": "direction",
    "target": "d-58012819-16b2-4ce5-be32-94713f7eb474",
    "request_id": "e080e382-ecd8-4036-a105-c0aaaf7e6046",
    "request": {
      "id": "e080e382-ecd8-4036-a105-c0aaaf7e6046",
      "revision": "6c5e52bf4accab70d8b48b6a5f0779933dc08a7f64d9216b3aaede571adbead6",
      "kind": "direction",
      "target": "d-58012819-16b2-4ce5-be32-94713f7eb474",
      "title": "Use COSMOS2025 as the main photometry catalogue",
      "text": "Photometry is the brightness of a galaxy measured through a set of filters. COSMOS2025 is the 2025 photometry catalogue of the COSMOS field. Sandro Tacchella advised that we use COSMOS2025 as the main (fiducial) catalogue from now on.\n\nSandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\""
    },
    "before": {
      "id": "d-58012819-16b2-4ce5-be32-94713f7eb474",
      "title": "COSMOS2025 as the fiducial catalogue",
      "text": "Sandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
      "date": "2026-09-23"
    },
    "after": {
      "id": "d-58012819-16b2-4ce5-be32-94713f7eb474",
      "title": "Use COSMOS2025 as the main photometry catalogue",
      "text": "Photometry is the brightness of a galaxy measured through a set of filters. COSMOS2025 is the 2025 photometry catalogue of the COSMOS field. Sandro Tacchella advised that we use COSMOS2025 as the main (fiducial) catalogue from now on.\n\nSandro Tacchella, Slack, 23 Sep 2026: \"Interesting... so I would use 2025 as fiducial catalog going forward.\"\n\nLiu Hao, 23 Sep 2026: \"list of research priorities to work on and add to wiki\"",
      "date": "2026-09-23"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:32:32.179024+00:00",
    "text": "Check whether extra dust around young stars is on\n\ndust1 is extra dust around young stars (birth-cloud dust). Check whether the Ceridwen fit switches it on.",
    "kind": "priority",
    "target": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
    "request_id": "297fe997-b2f1-4215-b6de-2c7c230af36b",
    "request": {
      "id": "297fe997-b2f1-4215-b6de-2c7c230af36b",
      "revision": "889e4007beb89a5207325121e936057fc77abc600a0c7bef794ef7734dce7c30",
      "kind": "priority",
      "target": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
      "title": "Check whether extra dust around young stars is on",
      "details": "dust1 is extra dust around young stars (birth-cloud dust). Check whether the Ceridwen fit switches it on.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
      "title": "Check birth-cloud dust (dust1)",
      "details": "Check whether birth-cloud dust (dust1) is switched on in the Ceridwen fit.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-cf330412-1d8f-4ca9-a439-ea16ef6fa6d7",
      "title": "Check whether extra dust around young stars is on",
      "details": "dust1 is extra dust around young stars (birth-cloud dust). Check whether the Ceridwen fit switches it on.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:32:35.614062+00:00",
    "text": "Test the effect of a steeper dust curve\n\nThe dust curve sets how strongly dust dims each wavelength. Check whether a steeper curve changes the model's full spectrum (SED).",
    "kind": "priority",
    "target": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
    "request_id": "6e9b183f-b6e3-4f77-8ebe-aa66f912202b",
    "request": {
      "id": "6e9b183f-b6e3-4f77-8ebe-aa66f912202b",
      "revision": "89f10b1e339789555cbc3188f46d31e45ad060abb4ed88e5d09a06304c685534",
      "kind": "priority",
      "target": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
      "title": "Test the effect of a steeper dust curve",
      "details": "The dust curve sets how strongly dust dims each wavelength. Check whether a steeper curve changes the model's full spectrum (SED).",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
      "title": "Test the SED effect of a steeper dust law",
      "details": "Check whether the steeper dust attenuation law changes the model SED.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-89d4b013-04a4-4c68-ae69-f4a6fc890749",
      "title": "Test the effect of a steeper dust curve",
      "details": "The dust curve sets how strongly dust dims each wavelength. Check whether a steeper curve changes the model's full spectrum (SED).",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:32:40.250639+00:00",
    "text": "Confirm which dust curve the fit uses\n\nCheck whether the Ceridwen fit uses the dust curve of Kriek and Conroy (2013).",
    "kind": "priority",
    "target": "p-9c4708da-30a8-4268-8281-f50252096add",
    "request_id": "b0f086f1-3403-440b-982b-5e08eff1b9c5",
    "request": {
      "id": "b0f086f1-3403-440b-982b-5e08eff1b9c5",
      "revision": "61f0dc9a45744c9ede887d0e405b11f3e37f4e7d3cc2bcf863fc694175c26e2c",
      "kind": "priority",
      "target": "p-9c4708da-30a8-4268-8281-f50252096add",
      "title": "Confirm which dust curve the fit uses",
      "details": "Check whether the Ceridwen fit uses the dust curve of Kriek and Conroy (2013).",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-9c4708da-30a8-4268-8281-f50252096add",
      "title": "Confirm the Kriek & Conroy dust prescription",
      "details": "Check whether the Ceridwen fit assumes the Kriek and Conroy dust attenuation prescription.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-9c4708da-30a8-4268-8281-f50252096add",
      "title": "Confirm which dust curve the fit uses",
      "details": "Check whether the Ceridwen fit uses the dust curve of Kriek and Conroy (2013).",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:32:43.738703+00:00",
    "text": "Allow dust slopes down to −3\n\nThe dust index is the slope of the dust curve. Refit with the index allowed down to −3. Check whether the fit converges.",
    "kind": "priority",
    "target": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
    "request_id": "9ce022fc-1fc4-44c7-8936-b3056e1bb6e5",
    "request": {
      "id": "9ce022fc-1fc4-44c7-8936-b3056e1bb6e5",
      "revision": "071df1f3420cdced10feb67c4cc3208e11521aaf20d924b75eb93eda78cf06be",
      "kind": "priority",
      "target": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
      "title": "Allow dust slopes down to −3",
      "details": "The dust index is the slope of the dust curve. Refit with the index allowed down to −3. Check whether the fit converges.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
      "title": "Refit with dust slopes down to −3",
      "details": "Run the fit with the dust index allowed down to −3 and check whether it converges.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-03df19b8-1627-4f43-a51d-1601bbadaf7a",
      "title": "Allow dust slopes down to −3",
      "details": "The dust index is the slope of the dust curve. Refit with the index allowed down to −3. Check whether the fit converges.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:33:01.287141+00:00",
    "text": "Repeat the fit with older MIST models\n\nThe current models are alpha-enhanced: extra magnesium, oxygen and similar elements. Check whether the old MIST models without this show the same problem.",
    "kind": "priority",
    "target": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
    "request_id": "b289e425-0cd8-47f3-8db0-787676852041",
    "request": {
      "id": "b289e425-0cd8-47f3-8db0-787676852041",
      "revision": "6e2a1587faf54b403829a38b28d3e98feff199710048396b9e5508e9846b04ab",
      "kind": "priority",
      "target": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
      "title": "Repeat the fit with older MIST models",
      "details": "The current models are alpha-enhanced: extra magnesium, oxygen and similar elements. Check whether the old MIST models without this show the same problem.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
      "title": "Repeat the fit with non-alpha-enhanced MIST models",
      "details": "Check whether the old MIST models (not alpha-enhanced) show the same problem.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-1b7c64b9-ce3b-4c29-890e-d0f30c458412",
      "title": "Repeat the fit with older MIST models",
      "details": "The current models are alpha-enhanced: extra magnesium, oxygen and similar elements. Check whether the old MIST models without this show the same problem.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  },
  {
    "date": "2026-09-23",
    "saved_at": "2026-09-23T13:33:05.713314+00:00",
    "text": "Check filter curves and Milky Way dust correction\n\nFilter curves say which wavelengths each band sees. Check that they and the Milky Way dust correction match the catalogue photometry.",
    "kind": "priority",
    "target": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
    "request_id": "1fb392ef-2a8c-48b3-945a-79ce255a12c5",
    "request": {
      "id": "1fb392ef-2a8c-48b3-945a-79ce255a12c5",
      "revision": "0c01a70aaac519dca210c60ce1f53c756f6a48ca9ee06732e368f98adde2b25e",
      "kind": "priority",
      "target": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
      "title": "Check filter curves and Milky Way dust correction",
      "details": "Filter curves say which wavelengths each band sees. Check that they and the Milky Way dust correction match the catalogue photometry.",
      "priority": null,
      "effort": "",
      "depends_on": []
    },
    "before": {
      "id": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
      "title": "Check filter curves and Galactic extinction",
      "details": "Check that the filter curves and Galactic extinction correction match the input photometry.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    },
    "after": {
      "id": "p-dae9a5c2-e688-47de-b53a-1cafffc201dd",
      "title": "Check filter curves and Milky Way dust correction",
      "details": "Filter curves say which wavelengths each band sees. Check that they and the Milky Way dust correction match the catalogue photometry.",
      "effort": "",
      "priority": null,
      "depends_on": [],
      "source": "wiki/research/direction.md"
    }
  }
]
```

## References

- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
