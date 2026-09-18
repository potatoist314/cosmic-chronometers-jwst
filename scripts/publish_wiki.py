#!/usr/bin/env python3
"""Send the notebook's sources to the TrueNAS host that serves it, and build there.

The NAS holds a copy of the project tree at `<DEST>/files/`: `wiki/` without
`public/`, `scripts/serve_wiki.py`, and each project file or directory that a
`/wiki/f/<path>` link in the Mac's own build names. The word counter
`wiki/build.py` imports goes to `<DEST>/home/.claude/scripts/hermes-bridge/`.
After a copy the wiki container on the NAS rebuilds `files/wiki/public`, the
pages Tailscale Serve publishes at https://truenas-scale.tail5c940d.ts.net:8765/wiki/.

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
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
PUBLIC = WIKI / "public"
ACTIVITY = "wiki/research/activity"
SLOP_LINT = Path.home() / ".claude/scripts/hermes-bridge/slop_lint.py"
REMOTE = "truenas"                                  # Host entry in ~/.ssh/config
DEST = "/mnt/apps/applications/astro-wiki"
CONTAINER = "astro-wiki-server"                     # docker-compose.yml service
LINK = re.compile(r"/wiki/f/([^\"' )<>#?]+)")
LOCK = Path.home() / "Library/Caches/astro-wiki-publish.lock"
STAMP = Path.home() / "Library/Caches/astro-wiki-publish.stamp"
ACCESS_LOG = Path.home() / "Library/Logs/astro-wiki/nas-access.log"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20"]
RSYNC = ["/usr/bin/rsync", "-rlz", "--timeout=300", "-e", " ".join(SSH)]
SOURCE_EXCLUDES = ["--exclude=/public", "--exclude=/public.lock", "--exclude=__pycache__",
                   "--exclude=/research/activity"]


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


def signature(paths: list[str]) -> str:
    """Size and time of every wiki source, the server, the counter and every linked file."""
    digest = hashlib.sha1()
    sources = [member for member in WIKI.rglob("*")
               if member.is_file() and PUBLIC not in member.parents
               and "__pycache__" not in member.parts and member != WIKI / "public.lock"]
    for member in sorted(sources) + [ROOT / "scripts/serve_wiki.py", SLOP_LINT]:
        status = member.stat()
        digest.update(("%s %d %d\n" % (member, status.st_size, status.st_mtime_ns)).encode())
    for relative in paths:
        target = ROOT / relative
        members = [target] if target.is_file() else sorted(
            member for member in target.rglob("*") if member.is_file())
        for member in members:
            status = member.stat()
            digest.update(("%s %d %d\n" % (member, status.st_size, status.st_mtime_ns)).encode())
    return digest.hexdigest()


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


def build() -> int:
    """Rebuild the pages on the NAS, as the user the container runs as."""
    return run(SSH + [REMOTE, "sudo", "docker", "exec", CONTAINER,
                      "python3", "/srv/project/wiki/build.py"])


def main() -> int:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            say("another publication is running")
            return 0
        if pull():
            say("could not pull the research activity from the NAS")
            return 1
        for attempt in range(3):                    # a build may swap wiki/public mid-copy
            try:
                paths = linked_files()
                state = signature(paths)
                if STAMP.exists() and STAMP.read_text() == state:
                    return 0                        # nothing new since the last publication
                code = push(paths) or build()
                if code == 0 and signature(paths) == state:
                    STAMP.write_text(state)
                    say("published %d linked paths and rebuilt on the NAS" % len(paths))
                    return 0
            except FileNotFoundError:
                code = 1
            say("sources changed or exit %d; attempt %d" % (code, attempt + 1))
            time.sleep(10)
        return code or 1


if __name__ == "__main__":
    sys.exit(main())
