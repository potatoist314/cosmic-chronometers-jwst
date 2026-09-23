#!/usr/bin/env python3
"""Synchronize direction.md before reading/editing it or publishing other sources.

The saved baseline is synchronization metadata, never a second authored roadmap.
Both sides changing from that baseline is an explicit conflict, not last-writer-wins.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "wiki"))
import activity
import direction


def exchange(request):
    import publish_wiki
    command = [*publish_wiki.SSH, publish_wiki.REMOTE, "sudo", "docker", "exec", "-i",
               publish_wiki.CONTAINER, "python3", "/srv/project/wiki/direction.py"]
    result = subprocess.run(command, input=json.dumps(request), capture_output=True, text=True, timeout=45)
    if result.returncode:
        raise activity.Conflict("Direction sync failed: " + (result.stdout or result.stderr).strip())
    return json.loads(result.stdout)


def synchronize(root=ROOT, remote=exchange, baseline_path=None):
    source = root / "wiki/research/direction.md"
    baseline_path = baseline_path or root / "wiki/public.cache/direction-sync.json"
    with activity.locked(root / "wiki/research/activity/.write.lock"):
        local = source.read_text(encoding="utf-8")
        result = remote({})
        server = result["source"]
        base = json.loads(baseline_path.read_text())["source"] if baseline_path.exists() else None
        if base is None and local != server:
            raise activity.Conflict("Direction sync needs an initial matching source. Local and server files are unchanged.")
        if local != server:
            if local == base:
                # Uncooperative local edits must not be replaced while SSH was running.
                if source.read_text(encoding="utf-8") != local:
                    raise activity.Conflict("Local direction changed during sync. Try again.")
                direction.atomic_write(source, server)
                local = server
            elif server == base:
                result = remote({"revision": result["revision"], "source": local})
                server = result["source"]
            else:
                raise activity.Conflict("Direction changed both locally and in the browser. Both versions are retained; reconcile them before publishing.")
        direction.atomic_write(baseline_path, json.dumps({"source": server}, ensure_ascii=False))
        return local


if __name__ == "__main__":
    try:
        synchronize()
        if "--save" in sys.argv:
            # The mark tells the prose check an agent wrote this save, not the browser editor.
            direction.save(ROOT / "wiki/research", {**json.load(sys.stdin), "by": "agent"})
            synchronize()
        if "--read" in sys.argv or "--save" in sys.argv:
            print(json.dumps(direction.snapshot(ROOT / "wiki/research"), ensure_ascii=False))
        else:
            print("Research direction is synchronized.")
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
