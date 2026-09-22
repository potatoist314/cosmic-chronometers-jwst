"""Atomic authoring of the single direction.md source and its dated revisions."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import activity
import research


def revision(raw):
    """Content identity for optimistic concurrency, not transfer verification."""
    return hashlib.sha256(raw.encode()).hexdigest()


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
            os.chmod(temporary, path.stat().st_mode & 0o777 if path.exists() else 0o644)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def section(raw, name, values):
    pattern = r"(^## " + re.escape(name) + r"\s*\n\s*```json\s*\n).*?(\n```[ \t]*(?=\n|$))"
    result, count = re.subn(pattern, lambda m: m[1] + json.dumps(values, ensure_ascii=False, indent=2) + m[2], raw, count=1, flags=re.M | re.S)
    if count != 1:
        raise ValueError("Direction section is missing: " + name)
    return result


def read(root):
    raw = (root / "direction.md").read_text(encoding="utf-8")
    record = research.parse_text(raw, root / "direction.md")
    return raw, record["sections"]


def snapshot(root):
    raw, parts = read(root)
    return {"revision": revision(raw), "priorities": parts["Roadmap"],
            "direction": [{**m, "id": m.get("id", "direction-" + str(i))}
                          for i, m in enumerate(parts["Your words"])],
            "history": parts["Amendments"],
            "states": {t["id"]: activity.state(activity.read(root, "priority", t["id"]))
                       for t in parts["Roadmap"]}}


def validate(raw, root):
    record = research.parse_text(raw, root / "direction.md")
    faults = research.validate([record], root.parent.parent)
    if faults:
        raise ValueError("; ".join(faults))
    return record


def text(value, label, limit, required=False):
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()):
        raise ValueError(f"{label} is required." if required and not value else f"Check {label.lower()}.")
    return value


def save(root, payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), str) or not activity.ID.fullmatch(payload["id"]):
        raise ValueError("A valid request ID is required.")
    with activity.locked(root / "activity/.write.lock"):
        raw, parts = read(root)
        prior = next((m for m in parts["Amendments"] if m.get("request_id") == payload["id"]), None)
        if prior:
            if prior.get("request") != payload:
                raise activity.Conflict("This save ID was already used.")
            return snapshot(root)
        if payload.get("revision") != revision(raw):
            raise activity.Conflict("This page changed after you opened the form. Your text is still in the form.")
        kind, target = payload.get("kind"), payload.get("target")
        if kind not in {"priority", "direction"}:
            raise ValueError("Choose a priority or direction entry.")
        name = "Roadmap" if kind == "priority" else "Your words"
        rows = parts[name]
        index = next((i for i, row in enumerate(rows)
                      if row.get("id", "direction-" + str(i)) == target), None) if target else None
        if target and index is None:
            raise ValueError("This entry no longer exists.")
        before = rows[index] if index is not None else None
        current = dict(before or {})
        now = datetime.now(timezone.utc)
        current["id"] = target or ("p-" if kind == "priority" else "d-") + payload["id"]
        if kind == "priority":
            current.update(title=text(payload.get("title"), "Title", 300, True),
                           details=text(payload.get("details", ""), "Details", 2000),
                           effort=text(payload.get("effort", ""), "Difficulty", 300))
            score = payload.get("priority")
            if score is not None and (type(score) is not int or not 1 <= score <= 10):
                raise ValueError("Choose a score from 1 to 10, or Unscored.")
            current["priority"] = score
            dependencies = payload.get("depends_on", [])
            ids = {t["id"] for t in parts["Roadmap"]}
            if not isinstance(dependencies, list) or any(not isinstance(d, str) or d not in ids or d == target for d in dependencies):
                raise ValueError("Choose existing priorities for dependencies.")
            current["depends_on"] = list(dict.fromkeys(dependencies))
            count = lambda t: len((t.get("title", "") + " " + t.get("details", "")).split())
            if count(current) > max(30, count(before or {})):
                raise ValueError("Keep the title and details to 30 words together.")
            current.setdefault("source", "wiki/research/direction.md")
            wording = current["title"] + ("\n\n" + current["details"] if current["details"] else "")
        else:
            current.update(title=text(payload.get("title", ""), "Heading", 160),
                           text=text(payload.get("text"), "Direction text", 50000, True))
            current.pop("display_text", None)
            current["date"] = now.date().isoformat()
            wording = current["text"]
        # Form defaults do not create a new revision when the content is unchanged.
        fields = ("title", "details", "effort", "priority", "depends_on") if kind == "priority" else ("title", "text")
        defaults = {"title": "", "details": "", "effort": "", "depends_on": [], "priority": None}
        if before and all(before.get(k, defaults.get(k)) == current.get(k, defaults.get(k)) for k in fields):
            return snapshot(root)
        if index is None:
            rows.append(current)
        else:
            rows[index] = current
        if kind == "priority":
            graph = {t["id"]: t.get("depends_on", []) for t in rows}
            def visit(node, trail):
                if node in trail:
                    raise ValueError("Dependencies cannot form a loop.")
                for dep in graph[node]:
                    visit(dep, trail | {node})
            for node in graph:
                visit(node, set())
        parts["Amendments"].append({"date": now.date().isoformat(), "saved_at": now.isoformat(),
                                    "text": wording, "kind": kind, "target": current["id"],
                                    "request_id": payload["id"], "request": payload,
                                    "before": before, "after": current})
        updated = section(section(raw, name, rows), "Amendments", parts["Amendments"])
        validate(updated, root)
        atomic_write(root / "direction.md", updated)
        return snapshot(root)


def source_exchange(root, request):
    """SSH-only source synchronization. The HTTP API never accepts raw source writes."""
    with activity.locked(root / "activity/.write.lock"):
        raw, parts = read(root)
        if "source" in request:
            if request.get("revision") != revision(raw):
                raise activity.Conflict("Direction changed during publication. Synchronize again.")
            candidate = request["source"]
            record = validate(candidate, root)
            amendments = record["sections"]["Amendments"]
            if amendments[:len(parts["Amendments"])] != parts["Amendments"]:
                raise activity.Conflict("Saved direction history must be retained.")
            # A stale local editor can retain new history while replacing current
            # wording. Accept only changes accounted for by appended revisions.
            expected = {name: list(parts[name]) for name in ("Your words", "Roadmap")}
            for amendment in amendments[len(parts["Amendments"]):]:
                kind = amendment.get("kind")
                if kind not in {"priority", "direction"}:
                    continue
                rows = expected["Roadmap" if kind == "priority" else "Your words"]
                target = amendment.get("target")
                index = next((i for i, row in enumerate(rows)
                              if row.get("id", "direction-" + str(i)) == target), None)
                before = rows[index] if index is not None else None
                after = amendment.get("after")
                if before != amendment.get("before") or not isinstance(after, dict) or after.get("id") != target:
                    raise activity.Conflict("Direction revisions do not match the saved wording.")
                if index is None:
                    rows.append(after)
                else:
                    rows[index] = after
            if any(expected[name] != record["sections"][name] for name in expected):
                raise activity.Conflict("Save direction changes through the revision-checked editor.")
            if candidate != raw:
                atomic_write(root / "direction.md", candidate)
            raw = candidate
        return {"source": raw, "revision": revision(raw)}


if __name__ == "__main__":
    try:
        print(json.dumps(source_exchange(Path(__file__).parent / "research", json.load(sys.stdin))))
    except (ValueError, activity.Conflict) as exc:
        print(json.dumps({"error": str(exc)}))
        sys.exit(1)
