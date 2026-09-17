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
    "id": "calibration-polynomial",
    "title": "Investigate the calibration polynomial",
    "priority": 9,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#calibration-polynomial",
    "details": "Polynomial modes must not be shorter than 100 \\(\\text{\\AA}\\). Inspect the polynomial and the empirical order rule.",
    "effort": "Expected short fix"
  },
  {
    "id": "literature-comparison",
    "title": "Compare published methods, ages and metallicities",
    "priority": 8,
    "source": "wiki/notes/meeting-2026-09-15-mj-park-sandro.md#literature-comparison",
    "details": "Include expected parameters for local elliptical galaxies and their relationship to the LEGA-C population. Compare established inference methods with Ceridwen. Can start independently."
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
  }
]
```

## References

- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
