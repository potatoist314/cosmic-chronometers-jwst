#!/usr/bin/env python3
"""Send the notebook's sources to the TrueNAS host that serves it, and build there.

The NAS holds a copy of the project tree at `<DEST>/files/`: `wiki/` without
`public/`, `scripts/serve_wiki.py`, and each project file or directory that a
`/f/<path>` link in the Mac's own build names. The word counter
`wiki/build.py` imports goes to `<DEST>/home/.claude/scripts/hermes-bridge/`.
After a copy the wiki container on the NAS rebuilds `files/wiki/public`, the
pages Pangolin publishes at https://wiki.eclw.org/. `--watch` keeps running:
it polls the sources every second and publishes about a second after a save
settles, and pulls the NAS records every half hour in between.

Research activity is written on both sides: by the browser through the NAS
server and by agents in chat. Every run first pulls the NAS records into
`wiki/research/activity/` (records are append-only, so a union is a merge) and
pushes them back without deletion. The NAS access log comes down to
~/Library/Logs/astro-wiki/nas-access.log for the Review Inbox.
Deployment files: `scripts/truenas-wiki/`.
"""

from __future__ import annotations

import fcntl
import hashlib
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
PUBLIC = WIKI / "public"
CACHE = WIKI / "public.cache"
ACTIVITY = "wiki/research/activity"
SLOP_LINT = Path.home() / ".claude/scripts/hermes-bridge/slop_lint.py"
REMOTE = "truenas"                                  # Host entry in ~/.ssh/config
DEST = "/mnt/apps/applications/astro-wiki"
CONTAINER = "astro-wiki-server"                     # docker-compose.yml service
LINK = re.compile(r"[\"'(=]/f/([^\"' )<>#?]+)")
LOCK = Path.home() / "Library/Caches/astro-wiki-publish.lock"
STAMP = Path.home() / "Library/Caches/astro-wiki-publish.stamp"
ACCESS_LOG = Path.home() / "Library/Logs/astro-wiki/nas-access.log"
# One ssh connection is shared by every rsync and command of a publication.
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", "-o", "ControlMaster=auto",
       "-o", "ControlPath=" + str(Path.home() / "Library/Caches/astro-wiki-ssh-%C"),
       "-o", "ControlPersist=600"]
RSYNC = ["/usr/bin/rsync", "-rlz", "--timeout=300", "-e", " ".join(SSH)]
SOURCE_EXCLUDES = ["--exclude=/public*", "--exclude=__pycache__",     # public, .lock, .cache, .new, .old
                   "--exclude=/research/activity"]
POLL = 1.0                                          # seconds between looks in --watch
PULL_EVERY = 1800                                   # seconds between pulls of the NAS records


def say(text: str) -> None:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), text, flush=True)


def run(command: list[str]) -> int:
    return subprocess.run(command).returncode


def linked_files() -> list[str]:
    """Project paths the built pages link, as rsync `--files-from` lines."""
    found = set()
    for page in PUBLIC.rglob("*.html"):
        for match in LINK.finditer(page.read_text(encoding="utf-8", errors="ignore")):
            relative = unquote(match[1]).strip("/")
            target = (ROOT / relative).resolve()
            if ROOT in target.parents and target.exists():
                found.add(relative)
    return sorted(found)


def sources() -> list[Path]:
    found, pending = [], [WIKI]
    while pending:
        parent = pending.pop()
        with os.scandir(parent) as entries:
            for entry in entries:
                if entry.name == "__pycache__" or (parent == WIKI and entry.name.startswith("public")):
                    continue                        # public, .lock, .cache and a local build's .new, .old
                if entry.is_dir(follow_symlinks=False):
                    pending.append(Path(entry.path))
                else:
                    found.append(Path(entry.path))
    return sorted(found)


def snapshot(paths: list[str]) -> str:
    """One line per source, the server, the counter and every linked file: path, size, mtime.

    A `#` line marks the local build, whose links may name new files."""
    lines = []
    for member in sources() + [ROOT / "scripts/serve_wiki.py"]:
        status = member.stat()
        lines.append("%s\t%d\t%d" % (member.relative_to(ROOT).as_posix(), status.st_size, status.st_mtime_ns))
    status = SLOP_LINT.stat()
    lines.append("%s\t%d\t%d" % (SLOP_LINT, status.st_size, status.st_mtime_ns))
    for relative in paths:
        target = ROOT / relative
        members = [target] if target.is_file() else sorted(
            member for member in target.rglob("*") if member.is_file())
        for member in members:
            status = member.stat()
            lines.append("%s\t%d\t%d" % (member.relative_to(ROOT).as_posix(), status.st_size, status.st_mtime_ns))
    if PUBLIC.is_dir():
        lines.append("#public\t%d" % PUBLIC.stat().st_mtime_ns)
    return "\n".join(lines) + "\n"


def additions(published: str, state: str) -> list[str] | None:
    """Project files new or changed since the last publication; None when one went away."""
    before = {line.split("\t")[0]: line for line in published.splitlines() if not line.startswith("#")}
    after = {line.split("\t")[0]: line for line in state.splitlines() if not line.startswith("#")}
    changed = [path for path, line in after.items() if before.get(path) != line]
    if set(before) - set(after) or any(path.startswith("/") for path in changed):
        return None
    return changed


def pull() -> int:
    """Records the browser saved on the NAS, and the access log."""
    (ROOT / ACTIVITY).mkdir(parents=True, exist_ok=True)
    code = run(RSYNC + ["-t", "%s:%s/files/%s/" % (REMOTE, DEST, ACTIVITY), str(ROOT / ACTIVITY) + "/"])
    ACCESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    run(RSYNC + ["%s:%s/logs/access.log" % (REMOTE, DEST), str(ACCESS_LOG)])
    return code


def push(paths: list[str]) -> int:
    remote = "%s:%s/files/" % (REMOTE, DEST)
    steps = [
        RSYNC + ["-c", "--delete"] + SOURCE_EXCLUDES + [str(WIKI) + "/", remote + "wiki/"],
        RSYNC + ["-t", str(ROOT / ACTIVITY) + "/", remote + ACTIVITY + "/"],
        RSYNC + ["-c", str(ROOT / "scripts/serve_wiki.py"), remote + "scripts/serve_wiki.py"],
        RSYNC + ["-c", str(SLOP_LINT),
                 "%s:%s/home/.claude/scripts/hermes-bridge/slop_lint.py" % (REMOTE, DEST)],
    ]
    for step in steps:
        code = run(step)
        if code:
            return code
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as listing:
        listing.write("\n".join(paths) + "\n")
        listing.flush()
        code = run(RSYNC + ["-t", "--files-from=" + listing.name, str(ROOT) + "/", remote])
    if code:
        return code
    # macOS rsync ignores --chmod; nginx reads these files as another user.
    return run(SSH + [REMOTE, "chmod", "-R", "u=rwX,go=rX", DEST + "/files", DEST + "/home"])


def push_some(paths: list[str]) -> int:
    """The changed files alone; records first come down from the NAS, as they are written on both sides."""
    if any(path.startswith(ACTIVITY + "/") for path in paths):
        code = run(RSYNC + ["-t", "%s:%s/files/%s/" % (REMOTE, DEST, ACTIVITY), str(ROOT / ACTIVITY) + "/"])
        if code:
            return code
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as listing:
        listing.write("\n".join(paths) + "\n")
        listing.flush()
        code = run(RSYNC + ["-t", "--files-from=" + listing.name, str(ROOT) + "/", "%s:%s/files/" % (REMOTE, DEST)])
    return code


def build(paths: list[str] = ()) -> int:
    """Rebuild the pages on the NAS, as the user the container runs as; first open the given files."""
    command = "sudo docker exec %s python3 /srv/project/wiki/build.py" % CONTAINER
    if paths:                                       # macOS rsync ignores --chmod; nginx reads as another user
        command = "cd %s/files && chmod u=rwX,go=rX %s && %s" % (
            DEST, " ".join(shlex.quote(path) for path in paths), command)
    return run(SSH + [REMOTE, command])


def publish(everything: bool = True) -> int:
    """Copy what changed since the last publication and rebuild.

    A full publication pulls the NAS records first and syncs every tree; a
    partial one sends only the files whose size or time changed."""
    started = time.monotonic()
    if everything and pull():
        say("could not pull the research activity from the NAS")
        return 1
    for attempt in range(3):                        # a build may swap wiki/public mid-copy
        try:
            paths = linked_files()
            state = snapshot(paths)
            published = STAMP.read_text() if STAMP.exists() else ""
            if published == state:
                return 0                            # nothing new since the last publication
            changed = None if everything else additions(published, state)
            if changed == []:                       # a local build linked nothing new
                STAMP.write_text(state)
                return 0
            code = push(paths) or build() if changed is None else push_some(changed) or build(changed)
            after = snapshot(paths) if code == 0 else state
            if code == 0 and after == state:
                STAMP.write_text(state)
                say("published %s and rebuilt on the NAS in %.1f s" % (
                    "%d linked paths" % len(paths) if changed is None else "%d changed files" % len(changed),
                    time.monotonic() - started))
                return 0
            moved = sorted(set(after.splitlines()) ^ set(state.splitlines()))
        except FileNotFoundError:
            code, moved = 1, []
        say("exit %d, changed meanwhile: %s; attempt %d" % (
            code, " ".join(line.split("\t")[0] for line in moved[:4]) or "-", attempt + 1))
        time.sleep(POLL)
    return code or 1


def watch() -> int:
    """Publish whenever the sources have held still for one poll; sync everything every half hour."""
    say("watching the wiki sources")
    publish()
    paths, seen, pulled = linked_files(), "", time.monotonic()
    while True:
        time.sleep(POLL)
        try:
            state = snapshot(paths)
        except FileNotFoundError:
            continue
        if state != seen:                           # let a save or a build finish
            seen = state
            continue
        if time.monotonic() - pulled >= PULL_EVERY:
            publish()
            pulled = time.monotonic()
        elif not STAMP.exists() or STAMP.read_text() != state:
            publish(everything=False)
        else:
            continue
        paths = linked_files()
        seen = snapshot(paths)


def main(argv: list[str]) -> int:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            say("another publication is running")
            return 0
        return watch() if argv == ["--watch"] else publish()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
