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
  }
]
```

## References

- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
