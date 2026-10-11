"""Isolated sandboxes for eval runs.

base template : local clone of the eval base commit + pinned ceridwen and sedpy_jax
                submodules + copies of the git-ignored inputs (venvs, data, papers).
variant template: base + the variant's AGENTS.md / CLAUDE.md / .agents/skills, folded
                into the base commit so the agent sees an ordinary history.
run sandbox   : APFS copy-on-write copy (cp -c) of a variant template + the case fixture.

Push is disabled in every repo (`git remote set-url --push origin DISABLED`); the
fetch URL is the public GitHub URL, which the Bash sandbox cannot reach.
"""
import os
import shutil
import subprocess
from pathlib import Path

MAIN = Path("/Users/liuhao/Downloads/Astro project")
ROOT = MAIN / "tmp/agent-hillclimb"
TEMPLATES = ROOT / "templates"
SANDBOXES = ROOT / "sandboxes"
BASE_COMMIT = "7354c90"
BRANCH = "absorption-mask"
GITHUB = "https://github.com/potatoist314/cosmic-chronometers-jwst.git"
SUBMODULES = {"ceridwen": "https://github.com/potatoist314/ceridwen.git",
              "external/sedpy_jax": "https://github.com/potatoist314/sedpy_jax.git"}
# Git-ignored inputs the project's agents normally find on disk.
COPIES = ["ceridwen/.venv", ".venv", "data/raw", "papers"]
LEVERS = ["AGENTS.md", "CLAUDE.md", ".agents/skills"]
GITCONFIG = Path(__file__).with_name("gitconfig.eval")


def git(cwd, *args, env=None, check=True):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=check,
                          env={**os.environ, **(env or {})}).stdout.strip()


def sandbox_env(home_tmp):
    """Environment for every eval process: no agent sockets, keys or git credentials."""
    keep = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "PATH", "SHELL") if k in os.environ}
    return {**keep, "LANG": "en_GB.UTF-8", "TERM": "dumb", "TMPDIR": str(home_tmp),
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(GITCONFIG),
            "GIT_TERMINAL_PROMPT": "0", "GIT_SSH_COMMAND": "/usr/bin/false"}


def make_base(worktree):
    base = TEMPLATES / "base"
    if (base / ".eval-ready").exists():
        return base
    if base.exists():
        shutil.rmtree(base)
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--no-checkout", "--no-tags", str(worktree), str(base)], check=True)
    git(base, "checkout", "-q", "-B", BRANCH, BASE_COMMIT)
    for ref in git(base, "for-each-ref", "--format=%(refname)", "refs/remotes").split():
        git(base, "update-ref", "-d", ref)
    git(base, "remote", "set-url", "origin", GITHUB)
    git(base, "remote", "set-url", "--push", "origin", "DISABLED")
    git(base, "update-ref", f"refs/remotes/origin/{BRANCH}", "HEAD")
    git(base, "branch", "--set-upstream-to", f"origin/{BRANCH}")
    for path, url in SUBMODULES.items():
        git(base, "submodule", "init", path)
        git(base, "config", f"submodule.{path}.url", str(MAIN / ".git/modules" / path))
        git(base, "-c", "protocol.file.allow=always", "submodule", "update", "-q", path)
        git(base, "config", f"submodule.{path}.url", url)
        sub = base / path
        git(sub, "remote", "set-url", "origin", url)
        git(sub, "remote", "set-url", "--push", "origin", "DISABLED")
    for rel in COPIES:
        src, dst = MAIN / rel, base / rel
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        # rsync keeps tracked files already checked out and adds the ignored ones.
        subprocess.run(["rsync", "-a", "--ignore-existing", f"{src}/", f"{dst}/"], check=True)
    # Venvs live beside the templates and are symlinked, so a run copy takes seconds.
    (TEMPLATES / "venvs").mkdir(exist_ok=True)
    for rel, name in ((".venv", "root-venv"), ("ceridwen/.venv", "ceridwen-venv")):
        shutil.move(str(base / rel), str(TEMPLATES / "venvs" / name))
        (base / rel).symlink_to(TEMPLATES / "venvs" / name)
    with open(Path(git(base / "ceridwen", "rev-parse", "--absolute-git-dir")) / "info/exclude", "a") as f:
        f.write(".venv\n")
    (base / ".git/info/exclude").write_text(".eval-ready\n.venv\n")
    (base / ".eval-ready").write_text(BASE_COMMIT + "\n")
    return base


def make_variant(variant, lever_dir):
    """Template for a variant; lever_dir holds that variant's AGENTS.md, CLAUDE.md, .agents/skills."""
    tmpl = TEMPLATES / variant
    if (tmpl / ".eval-variant").exists():
        return tmpl
    if tmpl.exists():
        shutil.rmtree(tmpl)
    subprocess.run(["cp", "-cR", str(TEMPLATES / "base"), str(tmpl)], check=True)
    for rel in LEVERS if lever_dir else []:
        src, dst = Path(lever_dir) / rel, tmpl / rel
        if src.is_dir():
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst, symlinks=True)  # .agents/skills/archify is a tracked symlink
        elif src.exists():
            shutil.copy2(src, dst)
    git(tmpl, "add", "-A", *LEVERS)
    if git(tmpl, "status", "--porcelain", "--untracked-files=no"):
        env = {"GIT_CONFIG_GLOBAL": str(GITCONFIG), "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_COMMITTER_DATE": git(tmpl, "log", "-1", "--format=%cI")}
        git(tmpl, "commit", "-q", "--amend", "--no-edit", "--no-verify", env=env)
        git(tmpl, "update-ref", f"refs/remotes/origin/{BRANCH}", "HEAD")
    (tmpl / ".git/info/exclude").write_text(".eval-ready\n.eval-variant\n.venv\n")
    (tmpl / ".eval-variant").write_text(variant + "\n")
    return tmpl


def make_run(variant, run_id):
    run = SANDBOXES / variant / run_id
    if run.exists():
        shutil.rmtree(run)
    run.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", "-cR", str(TEMPLATES / variant), str(run)], check=True)
    (run / "tmp").mkdir(exist_ok=True)  # git-ignored; TMPDIR of the run
    return run
