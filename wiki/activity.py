"""Append-only research notes, ink originals, and explicit priority status events."""
from __future__ import annotations

import base64
import binascii
import fcntl
import html
import json
import math
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

ID = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
PNG = b"\x89PNG\r\n\x1a\n"
MAX_REQUEST = 24 * 1024 * 1024


class Conflict(ValueError):
    """A retry reused an ID or a status change used an outdated state."""


@contextmanager
def locked(path):
    """Coordinate browser writes, chat updates, and builds across processes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def targets(records):
    result = {}
    for record in records:
        if record["kind"] == "direction":
            for task in record["sections"]["Roadmap"]:
                result[("priority", task["id"])] = task
        elif record["kind"] == "question":
            result[("question", record["id"])] = record
    return result


def directory(root, kind, ident):
    if kind not in {"priority", "question"} or not isinstance(ident, str) or not ID.fullmatch(ident):
        raise ValueError("Unknown research target")
    return root / "activity" / kind / ident


def read(root, kind, ident):
    entries = [json.loads(p.read_text()) for p in directory(root, kind, ident).glob("*/event.json")
               if ID.fullmatch(p.parent.name)]
    return sorted(entries, key=lambda e: e["sequence"])


def state(entries):
    return next((e["state"] for e in reversed(entries) if e["action"] == "state"), "open")


def snapshot(root, kind, ident):
    entries = read(root, kind, ident)
    return {"entries": entries, "state": state(entries), "revision": len(entries)}


def figures(records):
    return {f'{r["id"]}:{i}': {"experiment": r["id"], "index": i, **f}
            for r in records if r["kind"] == "experiment"
            for i, f in enumerate(r["sections"]["Figures"])}


def png_bytes(value):
    if not isinstance(value, str) or not value.startswith("data:image/png;base64,"):
        raise ValueError("Preview must be PNG")
    try:
        data = base64.b64decode(value.split(",", 1)[1], validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid PNG preview") from exc
    if not data.startswith(PNG):
        raise ValueError("Invalid PNG preview")
    return data


def save(root, project, records, kind, ident, payload, *, origin="wiki"):
    """Save one immutable event. Call this function for chat updates too.

    A note never changes status. A state event contains no inferred conclusion.
    Request IDs make retries safe; supersedes links preserve note revisions.
    """
    import research
    import research_figures
    if (kind, ident) not in targets(records):
        raise ValueError("Unknown research target")
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), str) or not ID.fullmatch(payload["id"]):
        raise ValueError("A valid request ID is required")
    if origin not in {"wiki", "chat"}:
        raise ValueError("Unknown origin")
    target = directory(root, kind, ident)
    with locked(root / "activity" / ".write.lock"):
        entries = read(root, kind, ident)
        previous = next((e for e in entries if e["id"] == payload["id"]), None)
        if previous:
            request = json.loads((target / previous["id"] / "request.json").read_text())
            if request != payload or previous["origin"] != origin:
                raise Conflict("Request ID already used")
            return snapshot(root, kind, ident)
        action = payload.get("action")
        event = {"id": payload["id"], "sequence": len(entries) + 1,
                 "date": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
                 "origin": origin, "action": action}
        if payload.get("source_ref"):
            if not isinstance(payload["source_ref"], str):
                raise ValueError("Source reference must be text")
            event["source_ref"] = payload["source_ref"]
        if action == "state":
            if kind != "priority" or payload.get("state") not in {"open", "resolved"}:
                raise ValueError("Invalid priority state")
            if payload.get("expected_state") != state(entries):
                raise Conflict("Priority status changed; reload it")
            if payload["state"] == state(entries):
                raise Conflict("Priority already has this status")
            event.update(state=payload["state"], through_sequence=len(entries))
        elif action == "note":
            text = payload.get("text", "")
            if not isinstance(text, str) or len(text) > 100000:
                raise ValueError("Invalid note text")
            evidence = payload.get("evidence", [])
            if not isinstance(evidence, list) or len(evidence) > 100:
                raise ValueError("Invalid evidence links")
            for link in evidence:
                if not isinstance(link, str):
                    raise ValueError("Invalid evidence link")
                research.asset_url(link, "/wiki", project)
            event.update(text=text, evidence=evidence)
            if payload.get("supersedes"):
                if not any(e["id"] == payload["supersedes"] and e["action"] == "note" for e in entries):
                    raise ValueError("Original note does not exist")
                event["supersedes"] = payload["supersedes"]
            pages = payload.get("pages", [])
            if not isinstance(pages, list) or len(pages) > 30:
                raise ValueError("Use at most 30 sheets")
            if not text.strip() and not evidence and not any(p.get("strokes") for p in pages if isinstance(p, dict)):
                raise ValueError("Add text, ink, or evidence")
        else:
            raise ValueError("Unknown action")
        target.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".pending-", dir=target) as tmp:
            staging = Path(tmp)
            if action == "note":
                event["pages"] = []
                catalog = figures(records)
                for number, page in enumerate(pages):
                    if not isinstance(page, dict):
                        raise ValueError("Invalid sheet")
                    width, height = page.get("width"), page.get("height")
                    if any(type(v) is not int or not 100 <= v <= 6000 for v in (width, height)):
                        raise ValueError("Invalid sheet dimensions")
                    strokes = page.get("strokes")
                    if not isinstance(strokes, list) or len(strokes) > 20000:
                        raise ValueError("Invalid strokes")
                    for stroke in strokes:
                        if not isinstance(stroke, dict) or stroke.get("tool", "pen") not in {"pen", "eraser"}:
                            raise ValueError("Invalid drawing tool")
                        if stroke.get("tool", "pen") == "pen" and stroke.get("color") not in {"#17212b", "#2459b3", "#b52a37"}:
                            raise ValueError("Invalid ink colour")
                        sizes = {12, 24, 48} if stroke.get("tool") == "eraser" else {2, 4, 7}
                        if stroke.get("size") not in sizes:
                            raise ValueError("Invalid pen width")
                        points = stroke.get("points")
                        if not isinstance(points, list) or not 1 <= len(points) <= 100000:
                            raise ValueError("Invalid stroke points")
                        for point in points:
                            if (not isinstance(point, list) or len(point) != 3 or
                                any(type(v) not in {int, float} or not math.isfinite(v) for v in point) or
                                not (0 <= point[0] <= width and 0 <= point[1] <= height and 0 <= point[2] <= 1)):
                                raise ValueError("Invalid stroke point")
                    saved = {"width": width, "height": height, "strokes": strokes}
                    background = page.get("background")
                    if background:
                        if not isinstance(background, str):
                            raise ValueError("Invalid figure reference")
                        # A revision reuses the immutable background of an earlier sheet.
                        if background.startswith("saved:"):
                            old_id, page_id = background[6:].split(":")
                            old = next((e for e in entries if e["id"] == old_id), None)
                            if old is None or not page_id.isdigit() or int(page_id) >= len(old.get("pages", [])):
                                raise ValueError("Unknown saved figure")
                            old_page = old["pages"][int(page_id)]
                            if "background_path" not in old_page:
                                raise ValueError("Sheet has no background")
                            saved.update({k: old_page[k] for k in ("background_path", "figure")})
                        else:
                            if background not in catalog:
                                raise ValueError("Unknown figure")
                            figure = catalog[background]
                            if "path" in figure:
                                research.asset_url(figure["path"], "/wiki", project)
                                source = project / unquote(figure["path"])
                                suffix, data = source.suffix.lower(), source.read_bytes()
                            else:
                                suffix, data = ".png", research_figures.image_bytes(project, figure)
                            name = f"background-{number}{suffix}"
                            (staging / name).write_bytes(data)
                            saved.update(background_path=(target / event["id"] / name).relative_to(project).as_posix(), figure=figure)
                    name = f"sheet-{number}.png"
                    (staging / name).write_bytes(png_bytes(page.get("preview")))
                    saved["preview"] = (target / event["id"] / name).relative_to(project).as_posix()
                    event["pages"].append(saved)
            (staging / "request.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            (staging / "event.json").write_text(json.dumps(event, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            for path in staging.iterdir():
                with path.open("rb") as stream:
                    os.fsync(stream.fileno())
            os.replace(staging, target / event["id"])
            with directory_fd(target) as fd:
                os.fsync(fd)
        research_figures.notebook.cache_clear()
        return snapshot(root, kind, ident)


@contextmanager
def directory_fd(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        yield fd
    finally:
        os.close(fd)


def history_html(entries, base, project):
    import research
    esc = html.escape
    blocks = []
    for e in reversed(entries):
        when = esc(e["date"][:19].replace("T", " ") + " UTC")
        if e["action"] == "state":
            label = "Marked resolved" if e["state"] == "resolved" else "Reopened"
            blocks.append(f'<article class="activity-event" id="event-{e["id"]}"><h3>{label}</h3><time>{when}</time></article>')
            continue
        content = f'<p class="verbatim">{esc(e["text"])}</p>' if e.get("text") else ""
        for link in e.get("evidence", []):
            content += f'<p><a href="{esc(research.asset_url(link, base, project))}">{esc(link)}</a></p>'
        for p in e.get("pages", []):
            src = base + "/f/" + quote(p["preview"])
            content += f'<a href="{src}"><img class="ink-preview" src="{src}" alt="Handwritten notes" loading="lazy"></a>'
            if p.get("figure"):
                content += '<p class="ink-source">' + esc(p["figure"]["caption"]) + '</p>'
        revision = f'<a href="#event-{esc(e["supersedes"])}">Earlier version</a>' if e.get("supersedes") else ""
        blocks.append(f'<article class="activity-event" id="event-{e["id"]}"><h3>Notes</h3><time>{when}</time>{revision}{content}'
                      f'<button type="button" data-edit-note="{e["id"]}">Revise note</button></article>')
    return "".join(blocks)


def editor_html(kind, ident, entries, base, project):
    esc = html.escape
    current = state(entries)
    status = (f'<div class="priority-state"><span data-current-state>{"Resolved" if current == "resolved" else "Open"}</span>'
              f'<button type="button" data-change-state>{"Reopen" if current == "resolved" else "Mark resolved"}</button></div>') if kind == "priority" else ""
    return f'''<section class="research-activity" data-kind="{kind}" data-id="{esc(ident)}" data-base="{esc(base)}">
{status}<p role="status" data-save-status></p>
<div class="activity-actions"><button type="button" data-open-writer>Write notes</button></div>
<details class="activity-text"><summary>Text and evidence</summary>
<label>Notes<textarea data-note-text rows="4"></textarea></label>
<label>Evidence links<textarea data-note-evidence rows="2" placeholder="One link per line"></textarea></label>
<button type="button" data-save-text>Save notes</button></details>
<h2>History</h2><div data-activity-history>{history_html(entries, base, project)}</div>
<dialog class="ink-dialog"><div class="ink-header"><h2>Research notes</h2><button type="button" data-close-writer>Close</button></div>
<div class="ink-workspace"><aside class="ink-context"><h3 data-context-title></h3><div data-context-content></div>
<label>Notes<textarea data-ink-text rows="5"></textarea></label>
<label>Evidence links<textarea data-ink-evidence rows="3"></textarea></label></aside>
<div class="ink-main"><div class="ink-toolbar">
<button type="button" data-tool="pen" aria-pressed="true">Pen</button>
<button type="button" data-tool="eraser" aria-pressed="false">Eraser</button>
<label hidden data-eraser-options>Size<select data-eraser-size><option value="12">Small</option><option value="24" selected>Medium</option><option value="48">Large</option></select></label>
<label>Colour<select data-color><option value="#17212b">Black</option><option value="#2459b3">Blue</option><option value="#b52a37">Red</option></select></label>
<label>Width<select data-width><option value="2">Fine</option><option value="4" selected>Medium</option><option value="7">Thick</option></select></label>
<button type="button" data-undo>Undo</button><button type="button" data-redo>Redo</button>
<label>Zoom<select data-zoom><option value="1">Fit</option><option value="1.5">150%</option><option value="2">200%</option></select></label>
</div><div class="ink-viewport" aria-label="Handwriting notebook"><div class="ink-sheets"></div></div>
<div class="ink-toolbar"><label>Sheet<select data-sheet></select></label><button type="button" data-add-sheet>Add sheet</button><span role="status" data-sheet-limit></span><button type="button" data-new-ink hidden>New note</button>
<label>Find figure<input type="search" data-figure-search placeholder="Target, view or caption"></label>
<label>Figure<select data-background><option value="">Blank sheet</option></select></label><button type="button" data-add-figure>Add figure sheet</button></div>
</div></div><div class="ink-footer"><span role="status" data-draft-status></span><button type="button" data-save-ink>Save annotation</button></div></dialog>
<script type="module" src="{esc(base)}/activity.js"></script></section>'''
