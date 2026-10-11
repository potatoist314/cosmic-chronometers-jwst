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


FIXTURES = {f.__name__: f for f in (tau_wide, birth_cloud_off, zred_narrow, kl_labels_removed)}


def apply(case, run):
    if case.get("fixture"):
        FIXTURES[case["fixture"]](run)
    return git(run, "rev-parse", "HEAD")
