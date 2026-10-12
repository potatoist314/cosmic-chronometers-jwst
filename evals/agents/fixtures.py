"""Case fixtures: put a run sandbox in the state the request was made in, as one ordinary commit."""
import os
from pathlib import Path

from sandbox import GITCONFIG, git

NB = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"


def _replace(run, rel, old, new):
    p = Path(run) / rel
    text = p.read_text()
    assert text.count(old) == 1, (rel, old)
    p.write_text(text.replace(old, new))


def _commit(run, paths, message):
    env = {"GIT_CONFIG_GLOBAL": str(GITCONFIG), "GIT_CONFIG_NOSYSTEM": "1"}
    git(run, "add", *paths)
    git(run, "commit", "-q", "--no-verify", "-m", message, env=env)
    git(run, "update-ref", "refs/remotes/origin/absorption-mask", "HEAD")


def tau_wide(run):
    _replace(run, NB, r'\"diffuse_tau_noll\": Uniform(low=0.0, high=1.0),',
             r'\"diffuse_tau_noll\": Uniform(low=0.0, high=2.0),')
    _commit(run, [NB], "Widen the diffuse_tau_noll prior to Uniform(0, 2)")


def birth_cloud_off(run):
    _replace(run, NB, r'\"birth_cloud_dust\": True,', r'\"birth_cloud_dust\": False,')
    _commit(run, [NB], "Birth-cloud dust off by default")


def zred_narrow(run):
    _replace(run, NB, r'\"zred_half_width\": 0.1,', r'\"zred_half_width\": 0.05,')
    _commit(run, [NB], "Narrow the zred prior to catalogue z +/- 0.05")


def kl_labels_removed(run):
    _replace(run, "scripts/plot_prior_kl.py",
             '    "diffuse_tau_noll": r"$\\tau_{\\mathrm{dust}}$", "diffuse_delta": r"$\\delta_{\\mathrm{dust}}$",\n'
             '    "diffuse_Ebump": r"$E_{\\mathrm{bump}}$", "zh_beta_unit": r"$u_\\beta$",\n',
             '    "zh_beta_unit": r"$u_\\beta$",\n')
    _commit(run, ["scripts/plot_prior_kl.py"], "Prior-KL plot: label for zh_beta_unit")


# Round 2: each plant inverts one correct line of the base commit, committed as an ordinary refactor.
SF, CP, VAST, SUMMARY, CHRONO, EXP, KL = ("scripts/spectral_figures.py", "scripts/cosmos_photometry.py", "scripts/vast.py",
                                          "scripts/build_dr2_quiescent_summary.py", "src/chronometer.py",
                                          "scripts/experiment.py", "scripts/plot_prior_kl.py")


def rest_axis_inverted(run):
    _replace(run, SF, '"top", functions=(lambda obs: obs / (1 + zred), lambda rest: rest * (1 + zred))',
             '"top", functions=(lambda obs: obs * (1 + zred), lambda rest: rest / (1 + zred))')
    _commit(run, [SF], "spectral_figures: inline the rest-frame conversion")


def ab_zero_point(run):
    _replace(run, CP, "flux = 10 ** (-0.4 * (float(mag) - 23.9))", "flux = 10 ** (-0.4 * (float(mag) + 48.6))")
    _commit(run, [CP], "cosmos_photometry: AB conversion from the magnitude definition")


def bandwidth_units(run):
    _replace(run, VAST, "float(offer.get(field, math.inf)) < MAX_INET_COST_USD_PER_TB / 1000",
             "float(offer.get(field, math.inf)) < MAX_INET_COST_USD_PER_TB")
    _commit(run, [VAST], "vast: simplify the bandwidth filter")


def formation_cumsum_reversed(run):
    _replace(run, SUMMARY, "[np.zeros((len(fracs), 1)), np.cumsum(fracs, axis=1)], axis=1",
             "[np.zeros((len(fracs), 1)), np.cumsum(fracs[:, ::-1], axis=1)], axis=1")
    _commit(run, [SUMMARY], "formation_times: vectorise the cumulative sum")


def hubble_slope_no_1pz(run):
    _replace(run, CHRONO, "        / ((1.0 + z_eff) * age_slope_gyr_per_redshift)\n",
             "        / age_slope_gyr_per_redshift\n")
    _commit(run, [CHRONO], "chronometer: tidy hubble_from_age_slope")


def merge_flat(run):
    _replace(run, EXP, "result[key] = merge(base[key], value) if isinstance(base[key], dict) else value",
             "result[key] = value")
    _commit(run, [EXP], "experiment: flatter override merge")


def photometry_no_rest_axis(run):
    _replace(run, SF, '    top = mark_rest_wavelength_axis(ax, redshift, label=r"rest-frame vacuum wavelength [$\\mu$m]")\n'
                      "    set_plain_log_ticks(\n        top.xaxis,\n"
                      "        [tick for tick in (0.1, 0.15, 0.25, 0.4, 0.6, 1, 1.5, 2.5, 4)\n"
                      "         if x_low < tick * (1 + redshift) < x_high],\n    )\n", "")
    _commit(run, [SF], "Photometry figure: one wavelength axis")


def photometry_bare_scale(run):
    _replace(run, SF, 'ylabel=r"$F_\\nu$ [$\\mu$Jy]"', 'ylabel=r"$F_\\nu$ [$10^{-29}$ cgs]"')
    _commit(run, [SF], "Photometry figure: flux label")


def kl_low_dpi(run):
    _replace(run, KL, 'fig.savefig(OUT_DIR / f"kl-{TARGET}.png", dpi=150, bbox_inches="tight")',
             'fig.savefig(OUT_DIR / f"kl-{TARGET}.png", dpi=40, bbox_inches="tight")')
    _commit(run, [KL], "Prior-KL plot: smaller PNG")


FIXTURES = {f.__name__: f for f in (tau_wide, birth_cloud_off, zred_narrow, kl_labels_removed, rest_axis_inverted,
                                    ab_zero_point, bandwidth_units, formation_cumsum_reversed, hubble_slope_no_1pz,
                                    merge_flat, photometry_no_rest_axis, photometry_bare_scale, kl_low_dpi)}


def apply(case, run):
    if case.get("fixture"):
        FIXTURES[case["fixture"]](run)
    return git(run, "rev-parse", "HEAD")
