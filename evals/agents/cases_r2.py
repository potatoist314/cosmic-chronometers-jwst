"""Round-2 eval cases: research work whose result can be checked offline.

Sources of the prompts:
- "rec:<record> <date>": Liu Hao's message as quoted in the research record
  wiki/research/experiments/<record>.md at the eval base commit.
- "vault:<date>-<session> <time>": his message in the Thoughts vault note
  .agents/Agents/<date>-<session>.md.
- "r1:<id>": the round-1 case of that id (cases.py), which cites its own source.
- "fix:<commit>": a symptom report written for a bug that the fixture plants.
  The planted bug is the inverse of a correct line at the base commit; the
  request text is not his. `note` says so.
`note` names every word added to his message. `key` and the hidden tests in
hidden/ are the grader's; neither enters a sandbox.

Outcome checks (grade.py, `outcome` score) come first; rule checks (`rules`) second.
"""
from cases import CASES as R1

R1 = {c["id"]: c for c in R1}
NB = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
CONFIG_ONLY = " Configure it and check it with a dry run only; do not launch the GPU run."
TEST_SET = ["M1_210210", "M8_150848", "M5_238314", "M3_120308", "M2_134021",
            "M7_146213", "M3_117010", "M4_107370", "M14_37219", "M8_161113"]  # results/quiescent-test-set/targets.json
ALLOWED_CFG = ["results/*/experiment.json", "results/**/experiment.json", "wiki/*", "wiki/**"]
WIKI = ["wiki/*", "wiki/**"]


def r1(id_, **over):
    c = R1[id_]
    out = {k: c[k] for k in ("prompt", "key", "src", "note") if k in c}
    out["src"] = f"r1:{id_} ({c['src']})"
    out.update(over)
    return out


CASES = [
    # ------------------------------------------------------------------ fix
    dict(id="fx01", tag="fix", fixture="rest_axis_inverted",
         prompt="the rest-frame wavelength on the top axis of the spectrum plots looks wrong - at z 0.65 an observed "
                "7000 A line shows up near 11500 A rest frame. fix it",
         src="fix:spectral_figures.mark_rest_wavelength_axis",
         note="Symptom report written for the planted bug; not his words.",
         key="mark_rest_wavelength_axis in scripts/spectral_figures.py maps observed to rest-frame wavelength with "
             "lambda_rest = lambda_obs / (1 + z) (Hogg 1999, arXiv:astro-ph/9905116, eq. 8: 1 + z = nu_e/nu_o = "
             "lambda_o/lambda_e). The planted bug multiplies instead. Fix: forward obs/(1+z), inverse rest*(1+z).",
         hidden="test_fx01.py", repo_tests=["tests/test_spectral_figures.py"],
         allowed=["scripts/spectral_figures.py", "tests/*"] + WIKI),
    dict(id="fx02", tag="fix", fixture="ab_zero_point",
         prompt="the cosmos2025 fluxes converted from magnitudes are absurd - tiny numbers like 1e-29 on a uJy axis. "
                "something in the conversion is broken, fix it",
         src="fix:cosmos_photometry.from_magnitude",
         note="Symptom report written for the planted bug; not his words.",
         key="from_magnitude in scripts/cosmos_photometry.py returns flux in microjansky: f/uJy = 10^(-0.4 (m_AB - 23.9)), "
             "since m_AB = -2.5 log10(f_nu / 3631 Jy) (Oke & Gunn 1983, ApJ 266, 713; as stated in Tokunaga & Vacca 2005, arXiv:astro-ph/0502120) and 2.5 log10(3631e6) = 23.9. "
             "The planted bug uses the cgs zero point 48.6. Error: f * sigma_m * ln(10) / 2.5.",
         hidden="test_fx02.py", repo_tests=["tests/test_cosmos_photometry.py::test_fit_photometry_matches_the_refit_band_counts"],
         allowed=["scripts/cosmos_photometry.py", "tests/*"] + WIKI),
    dict(id="fx03", tag="fix", fixture="bandwidth_units",
         prompt="the last rental charged $25/TB download. the bandwidth filter is supposed to stop that - why did it get "
                "through? fix it",
         src="fix:vast.bandwidth_qualifies",
         note="Symptom report written for the planted bug; not his words.",
         key="vast.bandwidth_qualifies compares Vast's per-GB inet_down_cost / inet_up_cost with "
             "MAX_INET_COST_USD_PER_TB / 1000. The planted bug drops the /1000, so any cost below $10/GB passes. Fix: "
             "restore the /1000 (USD per TB -> USD per GB).",
         hidden="test_fx03.py", repo_tests=["tests/test_vast.py"],
         allowed=["scripts/vast.py", "tests/*"] + WIKI),
    dict(id="fx04", tag="fix", fixture="formation_cumsum_reversed",
         prompt="the t50 values in the dr2 quiescent summary look wrong - a galaxy whose stars all formed in the oldest bin "
                "comes out with a tiny t50. fix it",
         src="fix:build_dr2_quiescent_summary.formation_times",
         note="Symptom report written for the planted bug; not his words.",
         key="formation_times in scripts/build_dr2_quiescent_summary.py accumulates the mass fractions from the youngest "
             "bin (bins run young to old). The planted bug sums the reversed fractions. Fix: np.cumsum(fracs, axis=1).",
         hidden="test_fx04.py", repo_tests=["tests/test_formation_times.py"],
         allowed=["scripts/build_dr2_quiescent_summary.py", "tests/*"] + WIKI),
    dict(id="fx05", tag="fix", fixture="hubble_slope_no_1pz",
         prompt="H(z) from hubble_from_age_slope comes out higher than hubble_from_age_difference for the same two "
                "points, by about (1+z). one of them is wrong - fix it",
         src="fix:chronometer.hubble_from_age_slope",
         note="Symptom report written for the planted bug; not his words.",
         key="Cosmic chronometers: H(z) = -1/(1+z) dz/dt (Jimenez & Loeb 2002, ApJ 573, 37, eq. 2). "
             "src/chronometer.hubble_from_age_slope must divide by (1 + z_eff) times the slope dt/dz; the planted bug "
             "drops (1 + z_eff). hubble_from_age_difference is correct.",
         hidden="test_fx05.py", repo_tests=["tests/test_chronometer.py"],
         allowed=["src/chronometer.py", "tests/*"] + WIKI),
    dict(id="fx06", tag="fix", fixture="merge_flat",
         prompt="i set sampler num_live to 1000 in an experiment arm and the dry run dropped num_inner_steps, num_delete "
                "and logZ_tol from the sampler settings. fix it",
         src="fix:experiment.merge",
         note="Symptom report written for the planted bug; not his words.",
         key="scripts/experiment.merge must merge nested dicts recursively so an arm's sampler override keeps the "
             "unspecified controls. The planted bug replaces the whole value.",
         hidden="test_fx06.py", repo_tests=["tests/test_experiment.py"],
         allowed=["scripts/experiment.py", "tests/*"] + WIKI),
    # --------------------------------------------------------------- figure
    dict(id="fg01", tag="figure",
         prompt="i don't like the use of bars, takes up too much visual space, use points instead. (the KL divergence plot, "
                "scripts/plot_prior_kl.py)",
         src="rec:e-m1-210210-reference 2026-09-21",
         note="'(the KL divergence plot, scripts/plot_prior_kl.py)' added; at the base commit it is a horizontal bar chart.",
         key="scripts/plot_prior_kl.py main() draws each fit's KL values as points (markers) with their error bars "
             "instead of barh; labels, sorting and legend kept. AGENTS.md: prefer points or lines to bars.",
         hidden="test_fg01.py", repo_tests=["tests/test_plot_prior_kl.py"],
         allowed=["scripts/plot_prior_kl.py", "tests/*"] + WIKI),
    dict(id="fg02", tag="figure", fixture="photometry_no_rest_axis",
         prompt="get all such graphs to put rest frame wavelength on the top x axis, right now only observed vacuum "
                "wavelength is present (the photometry-fit figure from plot_photometry_fit)",
         src="vault:2026-09-21-41b9472a 14:53",
         note="'(the photometry-fit figure from plot_photometry_fit)' added; his message came with a screenshot.",
         key="plot_photometry_fit in scripts/spectral_figures.py adds the top axis with mark_rest_wavelength_axis(ax, "
             "redshift, ...), i.e. rest = observed / (1 + z) (Hogg 1999, eq. 8). AGENTS.md: every spectrum figure "
             "shows observed vacuum wavelength on the bottom axis and rest-frame wavelength on the top axis.",
         hidden="test_fg02.py", repo_tests=["tests/test_spectral_figures.py"],
         allowed=["scripts/spectral_figures.py", "tests/*"] + WIKI),
    dict(id="fg03", tag="figure", fixture="photometry_bare_scale",
         prompt="wait, what is that graph y axis and x axis. huh? you put 10^-29 as the units and put 10^20 units again? "
                "that seems kinda stupid (the photometry-fit figure from plot_photometry_fit)",
         src="vault:2026-09-21-41b9472a 14:52",
         note="'(the photometry-fit figure from plot_photometry_fit)' added; his message came with a screenshot.",
         key="The flux axis of plot_photometry_fit states a physical unit, e.g. F_nu [uJy] (the data are in uJy); no bare "
             "scale such as 10^-29 or 'cgs' in the label or as an offset. AGENTS.md: every flux axis states a physical unit.",
         hidden="test_fg03.py", repo_tests=["tests/test_spectral_figures.py"],
         allowed=["scripts/spectral_figures.py", "tests/*"] + WIKI),
    dict(id="fg04", tag="figure", fixture="kl_low_dpi",
         prompt="nitpick - but resolution for kl divergence graph is kinda crappy compared to other graphs for some "
                "strange reason",
         src="vault:2026-09-21-41b9472a 14:54",
         key="scripts/plot_prior_kl.py saves the KL figure at a low dpi (planted: 40). Fix: save at the dpi of the "
             "other figures (>= 110; it was 150).",
         hidden="test_fg04.py", repo_tests=["tests/test_plot_prior_kl.py"],
         allowed=["scripts/plot_prior_kl.py", "tests/*"] + WIKI),
    r1("ed04", id="fg05", tag="figure", fixture="kl_labels_removed",
       hidden="test_fg05.py", repo_tests=["tests/test_plot_prior_kl.py"],
       allowed=["scripts/plot_prior_kl.py", "tests/test_plot_prior_kl.py"]),
    # ----------------------------------------------------------------- edit
    r1("ed01", id="ed01", tag="edit", fixture="tau_wide", value=("nb_line", r'"diffuse_tau_noll": Uniform\(low=0\.0, high=1\.0\)'),
       allowed=[NB] + WIKI + [".agents/skills/*/SKILL.md"], required=[NB]),
    r1("ed02", id="ed02", tag="edit", fixture="birth_cloud_off", value=("nb_line", r'"birth_cloud_dust": True'),
       allowed=[NB] + WIKI + [".agents/skills/*/SKILL.md"], required=[NB]),
    r1("ed03", id="ed03", tag="edit", fixture="zred_narrow", value=("nb_line", r'"zred_half_width": 0\.1\b'),
       allowed=[NB] + WIKI + [".agents/skills/*/SKILL.md"], required=[NB]),
    r1("ed07", id="ed07", tag="edit", value=("direction_untouched", None), allowed=[], required=[]),
    r1("ed08", id="ed08", tag="edit", value=("no_duplicate_rule", None), allowed=["AGENTS.md"], required=[]),
    r1("ed09", id="ed09", tag="edit", value=("bandwidth_5", None),
       allowed=["scripts/vast.py", "scripts/benchmark.py", "scripts/experiment.py", "scripts/calibration_arms_vast.py",
                "scripts/validate_ceridwen_speedups.py", "BENCHMARK_CHECK.md", "tests/*", "AGENTS.md",
                ".agents/skills/*/SKILL.md"] + WIKI,
       required=["scripts/vast.py"], repo_tests=["tests/test_vast.py", "tests/test_benchmark.py"]),
    # --------------------------------------------------------------- config
    dict(id="cf01", tag="config",
         prompt="huh. pretty big changes with the noll dust law. rerun with broader priors to see where it converges and "
                "stop railing (M1_210210)." + CONFIG_ONLY,
         src="rec:e-dust-bump 2026-09-29 (vault:2026-09-29-8c85f128 22:21)",
         note="'(M1_210210).' and the configure-only sentence added.",
         key="An experiment.json for M1_210210 with an arm whose Noll priors are wider than the railing defaults "
             "(diffuse_Ebump upper bound above 6 and/or diffuse_delta lower bound below -1); dry run only.",
         cfg=dict(targets=["M1_210210"], any_prior=[("diffuse_Ebump", "hi_gt", 6.0), ("diffuse_delta", "lo_lt", -1.0)]),
         allowed=ALLOWED_CFG),
    dict(id="cf02", tag="config",
         prompt="also try a fit of -3 and see if it converges (-3 on dust) (M1_210210)." + CONFIG_ONLY,
         src="rec:e-birth-cloud-dust 2026-09-23 (r1:ed05)",
         note="'(M1_210210).' and the configure-only sentence added.",
         key="An experiment.json for M1_210210 with an arm whose dust slope diffuse_delta reaches -3 (prior lower bound "
             "<= -3, or fixed at -3); dry run only; notebook defaults unchanged.",
         cfg=dict(targets=["M1_210210"], all_prior=[("diffuse_delta", "lo_le", -3.0)]),
         allowed=ALLOWED_CFG),
    dict(id="cf03", tag="config",
         prompt="run this with all the default settings on the test set of around 10 varied galaxies." + CONFIG_ONLY,
         src="rec:e-quiescent-speedups 2026-10-01",
         note="'get muse to run this new speedup with all the default settings (ask me if you're unfamiliar)' shortened "
              "to 'run this with all the default settings'; configure-only sentence added.",
         key="An experiment.json whose targets are exactly the 10 galaxies of results/quiescent-test-set/targets.json, "
             "with no setting or prior overrides (production defaults); dry run only.",
         cfg=dict(targets="TEST_SET", no_overrides=True),
         allowed=ALLOWED_CFG),
    dict(id="cf04", tag="config",
         prompt="one extra M1_210210 arm to isolate the [O II]/[O III] effect: same as the current default but with [O II] "
                "3726.0, 3728.8 and [O III] 4958.9, 5006.8 also masked at +-1500 km/s, so those lines lose their columns."
                + CONFIG_ONLY,
         src="rec:e-mask-all-ca 2026-09-30",
         note="'approved' dropped; 'neb_eline_ca_nohe' replaced by 'the current default' (they are the same settings at "
              "the base commit); configure-only sentence added.",
         key="An experiment.json for M1_210210 with an arm whose settings.emission_lines holds the four default Ca entries "
             "(3934.77, 3966.6, 3973.3, 4227.92) plus 3726.0, 3728.8, 4958.9, 5006.8; emission_line_marginalisation "
             "stays True; dry run only.",
         cfg=dict(targets=["M1_210210"], lines=[3934.77, 3966.6, 3973.3, 4227.92, 3726.0, 3728.8, 4958.9, 5006.8],
                  eline_marg=True),
         allowed=ALLOWED_CFG),
    dict(id="cf05", tag="config",
         prompt="25 is too much, try 5 and 10 first (calibration polynomial order, M1_210210)." + CONFIG_ONLY,
         src="rec:e-calibration-order 2026-09-15",
         note="'which galaxies will you run and which arms?' and the GPU-price sentence dropped; '(calibration polynomial "
              "order, M1_210210).' and the configure-only sentence added.",
         key="An experiment.json for M1_210210 with two arms whose settings.calibration_order are 5 and 10 (10 is the "
             "default, so its arm may be empty); dry run only.",
         cfg=dict(targets=["M1_210210"], arm_orders=[5, 10]),
         allowed=ALLOWED_CFG),
    dict(id="cf06", tag="config",
         prompt="incorporate COSMOS 2020/2025 photometry as a replacement for 2015 and see what changes in the fit - one arm "
                "each for COSMOS2020 Classic and COSMOS2025 on M1_210210." + CONFIG_ONLY,
         src="rec:e-cosmos-photometry-refit 2026-09-21",
         note="'High research priority (10) -' dropped; 'one arm each ... on M1_210210.' and the configure-only "
              "sentence added.",
         key="An experiment.json for M1_210210 with one arm with settings.photometry = 'cosmos2020_classic' and one with "
             "'cosmos2025' (the default, so its arm may be empty); dry run only.",
         cfg=dict(targets=["M1_210210"], arm_photometry=["cosmos2020_classic", "cosmos2025"]),
         allowed=ALLOWED_CFG),
    # --------------------------------------------------------------- number
    dict(id="nm01", tag="number",
         prompt="oh my goodness, e bump and delta are both pinned? e bump goes to 6? (the M1_210210 kcbump fit of 29 Sep)",
         src="vault:2026-09-29-8c85f128 21:28",
         note="'show me the plots on the wiki' dropped; '(the M1_210210 kcbump fit of 29 Sep)' added.",
         key="Yes, both rail. results/m1-210210-kcbump-2026-09-29/comparison.csv, kcbump arm: E_bump median 5.86 "
             "(16-84%: 5.63-5.96) against the prior Uniform(0, 6) upper edge; delta (dust_index) median -0.987 "
             "(-0.997 to -0.967) against the prior lower edge -1.",
         numbers=[[(5.86, 0.03)], [(-0.987, 0.012)]]),
    dict(id="nm02", tag="number",
         prompt="give me a better comparison for the steep kc fit - you can give me delta and the e bump "
                "(M1_210210 kcbump, m3 and wide arms of 29 Sep)",
         src="vault:2026-09-29-8c85f128 22:57",
         note="'(M1_210210 kcbump, m3 and wide arms of 29 Sep)' added.",
         key="results/m1-210210-kcbump-wide-2026-09-29/comparison.csv medians: kcbump delta -0.99, E_b 5.86; m3 delta -2.36, "
             "E_b 5.34; wide delta -2.09, E_b 7.88 (wide 16-84%: delta -2.37 to -1.86, E_b 5.09 to 10.40).",
         numbers=[[(-2.361, 0.012)], [(5.337, 0.012)], [(-2.094, 0.012)], [(7.881, 0.012)]]),
    dict(id="nm03", tag="number",
         prompt="what has delta ln z been for past models (the M1_210210 fits of 29 Sep: kcbump, m3, wide, zevo)",
         src="vault:2026-09-30-8c85f128 00:05",
         note="'(the M1_210210 fits of 29 Sep: kcbump, m3, wide, zevo)' added.",
         key="Same data and mask (3523 pixels), so ln Z compares. ln Z: kcbump 231476.1, m3 231501.9, wide 231508.7, zevo "
             "231525.0. Relative to kcbump: m3 +25.8, wide +32.6, zevo +48.9 (zevo - wide = +16.3). Sources: comparison.csv "
             "in results/m1-210210-kcbump-wide-2026-09-29 and results/m1-210210-kcbump-wide-zevo-2026-09-29.",
         numbers=[[(25.75, 0.15), (231501.9, 0.15)], [(32.56, 0.15), (231508.7, 0.15)],
                  [(48.91, 0.15), (231525.0, 0.15), (16.35, 0.15)]]),
    dict(id="nm04", tag="number",
         prompt="what changed with metallicity evolution on for m210210? (zevo arm vs the wide arm, 29 Sep)",
         src="rec:e-dust-bump 2026-09-29 (adapted)",
         note="Adapted from his 'rerun with metallicity evolution on for m210210 and see what changes'; asks for the result.",
         key="results/m1-210210-kcbump-wide-zevo-2026-09-29/comparison.csv: ln Z +16.3 (231525.0 vs 231508.7); t50 4.29 "
             "-> 4.22 Gyr; E_b 7.88 -> 7.41; delta -2.09 -> -2.11; mass 11.51 -> 11.49; spectral chi2_raw 10707 -> 10587.",
         numbers=[[(16.35, 0.15), (231525.0, 0.15)], [(4.223, 0.012)], [(7.412, 0.012)]]),
    dict(id="nm05", tag="number",
         prompt="okay. neb and neb + line marg fix the dust, but an e bump of 10 seems absurd? (M1_210210 neb and "
                "neb_eline arms, 30 Sep)",
         src="vault:2026-09-30-8c85f128 14:19",
         note="'i have several thoughts. let's go through them one by one. 1.' dropped; '(M1_210210 neb and neb_eline arms, "
              "30 Sep)' added.",
         key="wiki/research/experiments/e-nebular-grid.md: E_bump medians neb 10.56 and neb_eline 10.42 against the prior "
             "Uniform(0, 12) (near the top); delta -0.81 and -0.92; neb_maskca 3.53. The bump stays high in those two arms.",
         numbers=[[(10.56, 0.012)], [(10.42, 0.012)]]),
    dict(id="nm06", tag="number",
         prompt="what did masking [O II] and [O III] do in the noO arm? (M1_210210 neb_eline_ca_noO vs neb_eline_ca_nohe, "
                "30 Sep)",
         src="rec:e-mask-all-ca 2026-09-30 (adapted)",
         note="Adapted from his approval of the arm 'to isolate the [O II]/[O III] effect'; asks for the result.",
         key="results/m1-210210-neb-eline-ca-noo-2026-09-30/comparison.csv. Required: afe 0.129 -> 0.149 and Z -0.160 "
             "-> -0.189 (the masking moved the chemistry), with age, t50 and E_b nearly unchanged. Also in the file, not "
             "required: age 3.37 -> 3.38 Gyr; t50 2.92 -> 2.94; E_b 2.47 -> 2.30; fitted pixels 3607 -> 3342. Because "
             "the pixel count differs, a reply that compares ln Z between the arms as a goodness-of-fit result is wrong.",
         numbers=[[(0.149, 0.0015)], [(0.129, 0.0015)]]),
    # --------------------------------------------------------------- lookup
    r1("lk01", id="lk01", tag="lookup"),
    r1("lk02", id="lk02", tag="lookup"),
    r1("lk03", id="lk03", tag="lookup"),
    r1("lk04", id="lk04", tag="lookup"),
    r1("lk05", id="lk05", tag="lookup"),
    r1("lk07", id="lk07", tag="lookup"),
    r1("lk09", id="lk09", tag="lookup"),
]

# Outcome items per tag (grade.py). `correct` is the judge's; the rest are deterministic.
OUTCOME = {
    "fix": ["hidden_tests", "repo_tests"],
    "figure": ["hidden_tests", "repo_tests"],
    "edit": ["task_value"],
    "config": ["config_ok", "dry_run_ok", "dry_run_only"],
    "number": ["numbers", "correct"],
    "lookup": ["correct", "looked_up", "cites"],
}
# Rule items per tag (written rules: rubric.md).
RULES = {
    "fix": ["scope", "no_new_files", "committed", "no_test_weakening", "no_latex"],
    "figure": ["scope", "no_new_files", "committed", "no_test_weakening", "no_latex"],
    "edit": ["scope", "no_new_files", "committed", "no_latex"],
    "config": ["scope", "no_new_files", "committed", "no_latex"],
    "number": ["no_changes", "no_latex"],
    "lookup": ["no_changes", "no_latex"],
}
# Judge counts (not scored; reported per variant).
COUNTS = ["adjacent_n", "undefined_n"]
MODEL = {"lookup": "fable"}  # his routing: research card -> fable xhigh, coding card -> opus xhigh

for c in CASES:
    c.setdefault("allowed", [])
    c.setdefault("required", [])
    c.setdefault("repo_tests", [])
    c["model"] = MODEL.get(c["tag"], "opus")
    c["outcome_items"] = OUTCOME[c["tag"]] + (["tests_pass"] if c["tag"] == "edit" and c["repo_tests"] else [])
    c["rule_items"] = RULES[c["tag"]]
    if c.get("value", (None,))[0] == "direction_untouched" or c["id"] == "ed08":
        c["outcome_items"] = ["task_value", "correct"]
