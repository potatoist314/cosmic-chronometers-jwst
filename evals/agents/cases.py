"""Eval cases: Liu Hao's own requests to agents in the Astro project.

Source of every prompt: the Thoughts vault notes
.agents/Agents/<date>-<session>.md (Astro project sessions), quoted verbatim
except where `note` says a few words of context were added.
`key` is the grader's answer key. It never enters a sandbox.
"""

NB = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
CONFIG_ONLY = " Configure it for M1_210210 and check it with a dry run only; do not launch the GPU run."

# Rubric item ids applied per category (definitions and sources: rubric.md).
JUDGE = {
    "status": ["correct", "direct", "no_commentary", "plain"],
    "explain": ["correct", "direct", "no_commentary", "plain", "mental_model"],
    "lookup": ["correct", "direct", "no_commentary", "plain", "sourced"],
    "edit": ["correct", "direct", "no_commentary", "in_scope"],
}
# Deterministic checks applied per category (definitions: grade.py).
DET = {
    "status": ["no_changes", "lines", "no_latex"],
    "explain": ["no_changes", "lines", "no_latex"],
    "lookup": ["no_changes", "lines", "no_latex", "looked_up", "cites"],
    "edit": ["scope", "no_new_files", "committed", "lines"],
}

CASES = [
    # ---------------------------------------------------------------- status
    dict(id="st01", tag="status", src="2026-09-17-02b1f83f 18:10",
         prompt="does the default have velocity dispersion as a free parameter? does it have redshift?",
         key="Velocity dispersion: yes. sigma_smooth is sampled with a ClippedNormal prior centred on the LEGA-C DR2 "
             "stellar velocity dispersion, width = the DR2 error, clipped at +/- sigma_clip = 3 DR2 errors. "
             "Redshift: not in the current production default. The notebook has a zred prior (catalogue z +/- 0.1, "
             "zred_half_width), but emission_line_marginalisation is True by default and that removes zred from the "
             "priors (PRIORS.pop('zred')), so z is fixed at the catalogue redshift. An answer that says redshift is "
             "free in the default is wrong."),
    dict(id="st02", tag="status", src="2026-09-24-01a0d39a 14:28",
         prompt="the recent m210210 experiments - does the dust law have 2175 angstrom bump? is the bump enabled in the model",
         key="Yes. The fits use the Noll attenuation law with a Drude bump centred at 2175 A (FWHM 350 A, Kriek & Conroy "
             "2013 centre and width). The bump amplitude E_bump (diffuse_Ebump) is a free parameter, independent of the "
             "slope delta; production prior Uniform(0, 6). (Some 29-30 Sep M1_210210 arms sampled E_bump on Uniform(0, 12).)"),
    dict(id="st03", tag="status", src="2026-09-15-02b1f83f 18:45",
         prompt="What is the noise calibration parameter that the corner plots show?",
         key="f_calib (sampled as log_f_calib): a fractional noise floor on the spectrum, i.e. an extra uncertainty equal "
             "to f_calib times the model flux, combined with the LEGA-C pixel errors. Prior Uniform(ln 0.01, ln 0.10), "
             "i.e. 1-10%; the corner plot shows it in percent."),
    dict(id="st04", tag="status", src="2026-09-24-01a0d307 13:46",
         prompt="what photometry does the current cosmos2025 use? aperture, aperture auto, or the one with lephare band offsets?",
         key="None of the three: COSMOS2025 (Shuntov+25) total SE++ model fluxes with the calibrated errors. No zero-point "
             "(LePhare) offset is applied because the paper tabulates none; Milky Way E(B-V) is taken from COSMOS2020 "
             "Classic. Source: scripts/cosmos_photometry.py.",
         note="His message ended 'add this note to the wiki if not already there'; that part is dropped."),
    dict(id="st05", tag="status", src="2026-09-15-01a0a57f 15:38",
         prompt="where can i check the definition of the metallicity parameter or the definition of the parameters in the current fsps grid being used (c3k afe or somesuch?)?",
         key="Points to concrete locations: the PRIORS block of notebooks/ceridwen_integrated_photometry_spectra.ipynb "
             "(Z is log10 iron abundance; [Fe/H] = Z + 1.7328283), the grid file "
             "~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5 (built by scripts/build_nebular_grid.py from the "
             "amist_c3k_hr_krou_afe alpha-MC grid), and/or the Ceridwen grid-loading code (ceridwen/ceridwen/ssps) or "
             "wiki/notes/model.md. Any correct concrete file path for the Z definition passes.",
         note="His message ended 'If you can find the appropriate code snippets, open them in vs code'; dropped."),
    dict(id="st06", tag="status", src="2026-10-04-01a0fea0 18:19",
         prompt="What has not yet been done for astronomy, or what's open? It's I've been away for a while over the weekend, and just like tell me what what I have to resume doing.",
         key="Names the top open roadmap items from wiki/research/direction.md with their priority scores, e.g. priority 10: "
             "resolve the metallicity definition; science skills and workflows / wiki submission format; replace COSMOS2015 "
             "photometry with COSMOS2020/2025; priority 9: calibration polynomial, local elliptical ground truth, Conroy "
             "dust index railing and weak UV, emission lines model/mask/ignore, marginalise H-beta. Uses the roadmap's "
             "1-10 scores and does not invent new scores.",
         extra_det=["ran_direction_read"]),
    dict(id="st07", tag="status", src="2026-09-21-41b9472a 11:07",
         prompt="why do the notebooks mask emission lines again",
         key="The current production default no longer masks emission lines: emission_line_marginalisation=True gives the "
             "FSPS lines free non-negative fluxes, so line pixels leave the mask. The `emission_lines` setting now masks "
             "Ca II K, Ca II H and Ca I (+/- 1500 km/s) - absorption features, because the alpha-enhanced grid scales Ca "
             "with Mg/alpha while observed Ca tracks Fe, and the model Ca lines came out deeper than the data - plus the "
             "telluric A band. Must not claim that Balmer or [O III] lines are masked by default today."),
    dict(id="st08", tag="status", src="2026-09-24-01a0d307 13:38",
         prompt="where are the experiment jsons located?",
         key="Each experiment has results/<slug>/experiment.json (e.g. results/m1-210210-neb-eline-ca-nohe-2026-09-30/"
             "experiment.json); runs write their manifest under results/<slug>/run/. Format in the "
             "running-ceridwen-experiments skill.",
         note="His words were 'where are the jsons located?' after asking about the experiment workflow; 'experiment' added."),
    dict(id="st09", tag="status", src="2026-09-21-41b9472a 14:48",
         prompt="what is photometry_floor by the way? is this separate from the f calib, because that also adds a noise floor, no?",
         key="photometry_floor = 0.05: a fixed 5% of each band's flux added in quadrature to the catalogue photometric error. "
             "f_calib is separate: a sampled fractional noise floor on the spectrum (prior 1-10%). So yes, two separate "
             "noise floors, one for photometry (fixed) and one for the spectrum (free)."),
    # --------------------------------------------------------------- explain
    dict(id="ex01", tag="explain", src="2026-09-01-01a03844 11:34",
         prompt="what might a calibration vector polynomial be for ceridwen",
         key="A smooth multiplicative function of wavelength (Chebyshev polynomial; order 10 in production) applied to the "
             "model spectrum so that flux-calibration / slit-loss / continuum-shape mismatch between the LEGA-C spectrum "
             "and the model is absorbed, leaving the absorption features and the photometry to set the physics. Its "
             "coefficients have Gaussian priors and are marginalised analytically rather than sampled."),
    dict(id="ex02", tag="explain", src="2026-09-21-41b9472a 15:35",
         prompt='what does "chebyshev polynomial on the model spectrum, marginalised analytically" actually mean',
         key="The model spectrum is multiplied by a sum of Chebyshev polynomials a_0 T_0(x) + ... + a_n T_n(x) over the "
             "rescaled wavelength. Because the coefficients enter linearly and have Gaussian priors, for each model "
             "spectrum the likelihood can be integrated over all coefficient values exactly (a Gaussian integral / linear "
             "solve), so the sampler never samples them; the result is the likelihood averaged over all allowed "
             "polynomials, not just the best one."),
    dict(id="ex03", tag="explain", src="2026-09-22-01a0c8d8 13:01",
         prompt="how does marginalisation even work? i don't quite understand the concept",
         key="Marginalising a nuisance parameter = integrating (summing) the probability over all its values weighted by "
             "its prior, p(D|theta) = integral p(D|theta,phi) p(phi) dphi, so the answer no longer depends on that "
             "parameter. Example tie-in to Ceridwen: calibration polynomial coefficients or emission-line fluxes are "
             "integrated out (analytically, because they enter linearly) instead of being sampled."),
    dict(id="ex04", tag="explain", src="2026-09-07-ad9ebda3 13:16",
         prompt="Tell me more about the evidence as a measure of fit quality",
         key="Bayesian evidence Z = integral of likelihood x prior = the average likelihood over the prior; nested sampling "
             "returns ln Z. It compares models on the same data (Bayes factor = difference in ln Z), rewarding fit and "
             "penalising wasted prior volume (Occam). It is not an absolute goodness-of-fit, and ln Z values are only "
             "comparable when the data, mask and likelihood are the same."),
    dict(id="ex05", tag="explain", src="2026-09-14-01a0954f 13:47",
         prompt="Tell me more about representative posterior draw vs highest likelihood fit.",
         key="Highest-likelihood fit: the single parameter set that matches the data best, ignoring the prior and the "
             "uncertainty; can sit at an atypical spike or edge. Representative posterior draw: a random sample from the "
             "posterior, i.e. one plausible parameter set with typical properties; many draws map the uncertainty. For a "
             "mock 'truth', a posterior draw is a realistic galaxy, while the max-likelihood point can be atypical/overfit."),
    dict(id="ex06", tag="explain", src="2026-09-15-01a0a57f 15:53",
         prompt="A fitted Z of about −1.733 means the same iron-to-hydrogen ratio as the Sun -> help me understand this? do square brackets [] generally denote powers of 10? not super familiar with dex notation or such",
         key="[X/Y] = log10(N_X/N_Y)_star - log10(N_X/N_Y)_Sun: square brackets mean a logarithmic ratio relative to the Sun, "
             "not a power of 10 by themselves. 'dex' = one unit of log10, i.e. a factor of 10. Ceridwen's Z is log10 of the "
             "iron abundance on its own scale, with [Fe/H] = Z + 1.7328, so Z = -1.733 gives [Fe/H] = 0, i.e. solar."),
    dict(id="ex07", tag="explain", src="2026-09-24-01a0d307 13:36",
         prompt="clearly explain to me how the experiment and benchmark workflow work now",
         key="Experiment: write results/<slug>/experiment.json (targets, seed, settings, priors, arms) -> "
             "python3 scripts/experiment.py run <json> --gpu '<type>' --output results/<slug>/run (dry-run available) -> "
             "it rents the cheapest qualifying Vast GPU (reliability >99.5%, fallback 96%; bandwidth < $10/TB; host record "
             "ranking; $1 cap), uploads pinned source and grids, runs the notebook per arm/target, downloads, destroys the "
             "rental, rebuilds figures, then results are validated. Benchmark: python3 scripts/benchmark.py run '<GPU>' "
             "--spend-cap 1 measures likelihood calls/s with the same rental rules; hosts are recorded in "
             "scripts/vast_hosts.csv."),
    dict(id="ex08", tag="explain", src="2026-09-23-41b9472a 14:40",
         prompt="explain to me what was implemented for emission line marginalisation",
         key="SETTINGS['emission_line_marginalisation'] (now on by default): each FSPS nebular line becomes a column in the "
             "calibration solve with a free non-negative flux, solved analytically together with the polynomial, with "
             "fluxes shared with the photometry; redshift is fixed at the catalogue value; doublet ratios are tied "
             "([O III] 4959/5007, [Ne III], [N II]); FSPS's phantom [O II] 3867 is excluded; a line whose pixels the mask "
             "removes gets no flux. Record: wiki/research/experiments/e-emission-line-marginalisation.md."),
    dict(id="ex09", tag="explain", src="2026-09-14-01a0954f 13:43",
         prompt="Huh, that's kinda roundabout. Take observation -> obtain the highest likelihood fit -> take this highest likelihood fit as synthetic data? Wdym generate fresh synthetic data - is this synthetic data not just the existing fit? Why does it need to be re-generated?",
         key="The fit is a noiseless model spectrum. Synthetic (mock) data = that model plus a fresh random noise realisation "
             "at the observed errors (same mask, resolution, photometric bands). Fitting the noiseless fit itself would "
             "give zero residuals and test nothing; fitting several noisy realisations tests whether the fitter recovers "
             "the known true parameters and how much they scatter.",
         note="Context of the 2026-09-14 mock/injection discussion."),
    # ---------------------------------------------------------------- lookup
    dict(id="lk01", tag="lookup", src="2026-09-23-41b9472a 16:37",
         prompt="is oii a real 3867 a real physical emission line or not?",
         key="No. The NIST Atomic Spectra Database lists no forbidden [O II] line between 3860 and 3875 A, and FSPS's "
             "'[O II] 3867' has zero flux in every Cloudy model; the real forbidden line there is [Ne III] 3869. Ceridwen "
             "excludes it (EXCLUDED_LINES in ceridwen/ceridwen/likelihood/emission_lines.py)."),
    dict(id="lk02", tag="lookup", src="2026-09-30-8c85f128 15:47",
         prompt="what is g band (the G label on the spectrum plots)",
         key="The G band: an absorption feature near 4300 A, mainly from CH molecules (Fraunhofer's G). Measured by the Lick "
             "index G4300, central band 4281.375-4316.375 A (Worthey et al. 1994). In this project it is the 'G' label "
             "for G4300 in scripts/spectral_figures.py.",
         note="'(the G label on the spectrum plots)' added; his message came while reading the absorption labels."),
    dict(id="lk03", tag="lookup", src="2026-09-30-8c85f128 15:40",
         prompt="wait, what's the lega c spectrum range",
         key="Typical observed range about 6300-8800 A (VIMOS high-resolution red grating with GG475 filter), R ~ 2500, "
             "0.6 A per pixel (LEGA-C DR2 release description / van der Wel et al. 2021). At z 0.6-1.0 that is roughly "
             "3150-5500 A rest frame."),
    dict(id="lk04", tag="lookup", src="2026-09-30-8c85f128 15:47",
         prompt="what are ia 624 / ia 679 ib 709 etc in the plot",
         key="Subaru Suprime-Cam intermediate-band filters used in COSMOS (12 IA filters, Taniguchi et al. 2015); the "
             "number is the approximate central wavelength in nm (IA624 ~ 6232 A in scripts/cosmos_photometry.py). IA and "
             "IB are two naming conventions for the same family. They are bands of the photometry-fit plot."),
    dict(id="lk05", tag="lookup", src="2026-09-15-02b1f83f 18:52",
         prompt="does dr2 give an error bar for velocity dispersion?",
         key="Yes. LEGA-C DR2 gives SIGMA_STARS_PRIME with its uncertainty SIGMA_STARS_PRIME_err (km/s) for the stellar "
             "component (and SIGMA_GAS_PRIME with an error for the gas). Source: data/raw/legac_dr2/VizieR_ReadMe.txt / "
             "the DR2 catalogue. The fit uses it as the width of the sigma_smooth prior."),
    dict(id="lk06", tag="lookup", src="2026-09-24-01a0d39a 16:05",
         prompt="what's a usual range of eb (the dust bump amplitude)",
         key="Gives a sourced range: E_b about 3 for a Milky Way-like bump and ~0 (no bump) for SMC/Calzetti-like curves; "
             "fitted galaxy values typically ~0-3 (e.g. E_b = 1.26 in Buat et al. 2011-based studies); Kriek & Conroy 2013 "
             "found bump strength correlates with slope (steeper curves, stronger bumps). Any range is fine if it is "
             "attributed to a named primary source and is consistent with these.",
         note="'(the dust bump amplitude)' added; his message came in the E_b prior discussion."),
    dict(id="lk07", tag="lookup", src="2026-09-21-41b9472a 12:00",
         prompt="but does the model account for AGB ionisation, or just the classic UV ionisation (the nebular emission grid)",
         key="Only young-star ionisation. The FSPS nebular model (Byler et al. 2017, Cloudy) uses simple stellar populations "
             "younger than ~10 Myr as the ionising source; post-AGB / old-star ionisation is not included, and the "
             "project's nebular grid (scripts/build_nebular_grid.py) uses that FSPS model.",
         note="'(the nebular emission grid)' added."),
    dict(id="lk08", tag="lookup", src="2026-09-12-01a0954f 18:31",
         prompt="what's illustris? i need you to make the answer more concise and self contained",
         key="Illustris: a suite of cosmological hydrodynamical simulations of galaxy formation (Vogelsberger et al. 2014); "
             "the main run Illustris-1 follows dark matter, gas, stars and black holes in a ~106.5 Mpc box; used for "
             "predicted galaxy properties such as star formation histories."),
    dict(id="lk09", tag="lookup", src="2026-09-29-8c85f128 15:58",
         prompt="what's the noll dust bump?",
         key="The Noll et al. (2009) attenuation law: the Calzetti curve multiplied by a power law with slope delta, plus a "
             "Drude-profile bump at 2175 A with amplitude E_b. In this project: bump centre 2175 A, FWHM 350 A (Kriek & "
             "Conroy 2013), E_b free with prior Uniform(0, 6), delta Uniform(-1, 0.4)."),
    # ------------------------------------------------------------------ edit
    dict(id="ed01", tag="edit", src="2026-09-17-02b1f83f 18:03",
         prompt="change the tau dust prior back to (0,1)",
         fixture="tau_wide",
         key="Sets PRIORS['diffuse_tau_noll'] back to Uniform(low=0.0, high=1.0) in the production notebook and commits. "
             "Nothing else in the model changes.",
         allowed=[NB, "wiki/*", "wiki/**", ".agents/skills/*/SKILL.md"], required=[NB],
         value=("nb_line", r'"diffuse_tau_noll": Uniform\(low=0\.0, high=1\.0\)')),
    dict(id="ed02", tag="edit", src="2026-09-24-01a0d39a 16:13",
         prompt="i think i want birthcloud dust on as the default",
         fixture="birth_cloud_off",
         key="Sets SETTINGS['birth_cloud_dust'] = True in the production notebook and commits; no new option or code.",
         allowed=[NB, "wiki/*", "wiki/**", ".agents/skills/*/SKILL.md"], required=[NB],
         value=("nb_line", r'"birth_cloud_dust": True')),
    dict(id="ed03", tag="edit", src="2026-09-17-02b1f83f 18:12",
         prompt="give z a plus minus 0.1 wiggle and dont even make these opt in switches - just have this as default and note it appropriately",
         fixture="zred_narrow",
         key="Sets SETTINGS['zred_half_width'] = 0.1 (catalogue z +/- 0.1) in the production notebook, keeps zred in the "
             "default PRIORS, adds no new switch, and commits; a short note (comment, wiki log/model page) is fine.",
         allowed=[NB, "wiki/*", "wiki/**", ".agents/skills/*/SKILL.md"], required=[NB],
         value=("nb_line", r'"zred_half_width": 0\.1\b')),
    dict(id="ed04", tag="edit", src="2026-09-29-55dbf275 21:16",
         prompt="Add the three Noll labels to scripts/plot_prior_kl.py (LaTeX names).",
         fixture="kl_labels_removed",
         key="Adds LABELS entries for diffuse_tau_noll, diffuse_delta and diffuse_Ebump with LaTeX strings in "
             "scripts/plot_prior_kl.py and commits; nothing else.",
         allowed=["scripts/plot_prior_kl.py", "tests/test_plot_prior_kl.py"], required=["scripts/plot_prior_kl.py"],
         value=("kl_labels", None),
         note="A lead's message to a worker in his notes; 're-run the post-fit cells ... report medians' dropped."),
    dict(id="ed05", tag="edit", src="2026-09-23-41b9472a 14:21",
         prompt="also try a fit of -3 and see if it converges (-3 on dust)." + CONFIG_ONLY,
         key="Writes results/<slug>/experiment.json for M1_210210 with an arm whose dust slope (diffuse_delta) prior reaches "
             "-3 (or fixes it at -3), runs scripts/experiment.py with --dry-run only, does not edit notebook defaults, "
             "creates no extra notes/wiki pages, and commits the config.",
         allowed=["results/*/experiment.json", "results/**/experiment.json", "wiki/*", "wiki/**"],
         required=[], value=("exp_json", "delta_m3"), extra_det=["dry_run_only"],
         note="Configure-only suffix added so no GPU is rented."),
    dict(id="ed06", tag="edit", src="2026-09-29-8c85f128 22:21",
         prompt="huh. pretty big changes with the noll dust law. rerun with broader priors to see where it converges and stop railing." + CONFIG_ONLY,
         key="Writes results/<slug>/experiment.json for M1_210210 with an arm that widens the Noll dust priors that rail "
             "(diffuse_Ebump upper bound above 6 and/or diffuse_delta lower bound below -1), dry-run only, no default "
             "changes, no extra docs, commits the config.",
         allowed=["results/*/experiment.json", "results/**/experiment.json", "wiki/*", "wiki/**"],
         required=[], value=("exp_json", "broader_noll"), extra_det=["dry_run_only"],
         note="Configure-only suffix added so no GPU is rented."),
    dict(id="ed07", tag="edit", src="2026-09-17-03cccfbe 18:27",
         prompt="add another priority - setting up the mock spectra test suite, 6/10",
         key="The roadmap already has 'Set up the mock spectra test suite' at priority 6. Correct outcome: says it is "
             "already there (score 6) and adds no duplicate. wiki/research/direction.md must not be edited directly; the "
             "sync script (scripts/sync_wiki_direction.py) cannot reach the wiki server from this machine, which may be "
             "reported in one line.",
         allowed=[], required=[], value=("direction_untouched", None)),
    dict(id="ed08", tag="edit", src="2026-09-23-41b9472a 16:38",
         prompt="rule - for physical / astronomical scientific things, don't use memory - always look things up. applies for both overseer and workers",
         key="AGENTS.md already has 'Look up every physical or astronomical fact; never state one from memory ... Applies "
             "to leads and workers.' Correct outcome: says so and adds no duplicate rule (no change, or a minimal "
             "non-duplicating edit).",
         allowed=["AGENTS.md"], required=[], value=("no_duplicate_rule", None)),
    dict(id="ed09", tag="edit", src="2026-09-15-02b1f83f 17:27",
         prompt="keep bandwidth cost less than $5/tb in future, as a rule",
         key="Changes the bandwidth limit from $10/TB to $5/TB everywhere it is enforced and stated: "
             "MAX_INET_COST_USD_PER_TB = 5 in scripts/vast.py (offer filter), messages/docstrings, AGENTS.md and the two "
             "Vast skills (and wiki/notes/vast-ai-gpu-workflow.md); tests pass; commits.",
         allowed=["scripts/vast.py", "scripts/benchmark.py", "scripts/experiment.py", "scripts/calibration_arms_vast.py",
                  "tests/*", "AGENTS.md", ".agents/skills/*/SKILL.md", "wiki/*", "wiki/**"],
         required=["scripts/vast.py"], value=("bandwidth_5", None),
         tests=".venv/bin/python -m pytest -q -p no:cacheprovider tests/test_vast.py tests/test_benchmark.py",
         note="His words: 'keep it less than $5/tb in future, as a rule' after asking about a $/TB charge; 'bandwidth cost' added."),
]

for c in CASES:
    c["model"] = "opus" if c["tag"] == "edit" else "fable"
    c["judge_items"] = JUDGE[c["tag"]]
    c["det_items"] = DET[c["tag"]] + c.get("extra_det", [])
