#!/usr/bin/env python3
"""Mirror the built notebook to the TrueNAS host that serves it when the Mac is off.

`wiki/public/` goes to `<DEST>/public/`, compared by checksum because every
build rewrites every page with a new timestamp. Each `/wiki/f/<path>` link in
the built pages names one project file or directory; those go to `<DEST>/files/`.
The NAS hands a request for a linked file it does not hold yet to the Mac's
wiki server. Deployment files: `scripts/truenas-wiki/`.
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

ROOT = Path("/Users/liuhao/Downloads/Astro project")
PUBLIC = ROOT / "wiki/public"
REMOTE = "truenas"                                  # Host entry in ~/.ssh/config
DEST = "/mnt/apps/applications/astro-wiki"
LINK = re.compile(r"/wiki/f/([^\"' )<>#?]+)")
LOCK = Path.home() / "Library/Caches/astro-wiki-publish.lock"
STAMP = Path.home() / "Library/Caches/astro-wiki-publish.stamp"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20"]
RSYNC = ["/usr/bin/rsync", "-rlz", "--timeout=300", "-e", " ".join(SSH)]


def say(text: str) -> None:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), text, flush=True)


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
    """One build of `wiki/public` plus the size and time of every linked file."""
    digest = hashlib.sha1()
    built = PUBLIC.stat()
    digest.update(b"%d %d\n" % (built.st_ino, built.st_mtime_ns))
    for relative in paths:
        target = ROOT / relative
        members = [target] if target.is_file() else sorted(
            member for member in target.rglob("*") if member.is_file())
        for member in members:
            status = member.stat()
            digest.update(("%s %d %d\n" % (member, status.st_size, status.st_mtime_ns)).encode())
    return digest.hexdigest()


def publish(paths: list[str]) -> int:
    code = subprocess.run(RSYNC + ["-c", "--delete", str(PUBLIC) + "/",
                                   "%s:%s/public/" % (REMOTE, DEST)]).returncode
    if code:
        return code
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8") as listing:
        listing.write("\n".join(paths) + "\n")
        listing.flush()
        code = subprocess.run(RSYNC + ["-t", "--files-from=" + listing.name, str(ROOT) + "/",
                                       "%s:%s/files/" % (REMOTE, DEST)]).returncode
    if code:
        return code
    # macOS rsync ignores --chmod; nginx reads these files as another user.
    code = subprocess.run(SSH + [REMOTE, "chmod", "-R", "u=rwX,go=rX",
                                 DEST + "/public", DEST + "/files"]).returncode
    say("published %d linked paths" % len(paths))
    return code


def main() -> int:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            say("another publication is running")
            return 0
        for attempt in range(3):                    # a build may swap wiki/public mid-copy
            try:
                paths = linked_files()
                state = signature(paths)
                if STAMP.exists() and STAMP.read_text() == state:
                    return 0                        # nothing new since the last publication
                code = publish(paths)
                if code == 0 and signature(paths) == state:
                    STAMP.write_text(state)
                    return 0
            except FileNotFoundError:
                code = 1
            say("wiki/public changed or rsync exit %d; attempt %d" % (code, attempt + 1))
            time.sleep(10)
        return code or 1


if __name__ == "__main__":
    sys.exit(main())
