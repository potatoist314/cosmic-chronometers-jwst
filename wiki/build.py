#!/usr/bin/env python3
"""Build the Astro lab notebook from `wiki/notes/*.md` into `wiki/public/`.

Standard library only, in the shape of `~/thoughts-site/build.py`.

The generator writes no prose. Every sentence on the finished site comes out of
a note. Chrome carries labels only, and `tests/run_tests.py` fails the build if
a text node outside a note body grows past four words or ends a sentence.

    python3 wiki/build.py [--notes DIR] [--out DIR] [--base /wiki]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote
from xml.sax.saxutils import escape as xesc

ROOT = Path(__file__).resolve().parent          # wiki/
PROJECT = ROOT.parent

SITE_NAME = "Astro Lab Notebook"
SITE_WHO = "Liu Hao · DR2 quiescent galaxies"
# Left rail order. A section with no note is not shown.
SECTIONS = ["Analyses", "Guides", "Notebooks", "Codebase", "Paper drafts", "Archive"]
BRIDGE = Path.home() / ".claude/scripts/hermes-bridge/bridge.py"


# ---------------------------------------------------------------- notes

def parse_note(path: Path) -> dict:
    """Frontmatter plus body. A note with no frontmatter is skipped."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}
    _, head, body = raw.split("---", 2)
    note = {"slug": path.stem, "body": body.strip(), "tags": [], "path": path}
    for line in head.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        note[key] = [t.strip() for t in value.strip("[]").split(",") if t.strip()] \
            if key == "tags" else value
    note.setdefault("title", path.stem)
    note.setdefault("date", "")
    note.setdefault("section", "Archive")
    note.setdefault("job", "")
    note.setdefault("status", "")
    return note


def split_thread(body: str):
    """The note body, and the Q/A pairs recorded under `## Thread`."""
    parts = re.split(r"^##\s+Thread\s*$", body, maxsplit=1, flags=re.M)
    if len(parts) == 1:
        return body, []
    turns, pending = [], {}
    for line in parts[1].splitlines():
        m = re.match(r"\*\*(Q|A)\*\*\s*(\d{4}-\d\d-\d\d)?\s*[·—-]?\s*(.*)", line.strip())
        if m:
            kind, date, text = m.group(1), m.group(2) or "", m.group(3)
            if kind == "Q":
                if pending:
                    turns.append(pending)
                pending = {"q": text, "date": date, "a": ""}
            elif pending:
                pending["a"] = text
        elif line.strip() and pending:
            key = "a" if pending.get("a") else "q"
            pending[key] = (pending[key] + " " + line.strip()).strip()
    if pending:
        turns.append(pending)
    return parts[0].rstrip(), turns


# ------------------------------------------------------------ markdown

def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")


def inline(text: str, base: str, source_dir: str = "") -> str:
    """Inline Markdown to HTML. Code spans are protected from every other rule."""
    spans: list[str] = []

    def stash(m):
        spans.append("<code>%s</code>" % esc(m.group(1)))
        return "\x00%d\x00" % (len(spans) - 1)

    text = INLINE_CODE.sub(stash, text)
    text = esc(text)
    text = IMAGE.sub(lambda m: image_tag(url(m.group(2), base, source_dir), m.group(1)), text)
    text = LINK.sub(lambda m: link_tag(url(m.group(2), base, source_dir), m.group(1)), text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def link_tag(href, label):
    return '<a href="%s">%s</a>' % (href, label) if href else label


def image_tag(src, alt):
    return '<img src="%s" alt="%s">' % (src, alt) if src else alt


def url(href: str, base: str, source_dir: str = ""):
    """Where a note-relative path points on the built site.

    None means the path leaves both the site and the project, so the caller
    drops the link and keeps the label. Nothing is invented."""
    if href.startswith(("http://", "https://", "mailto:", "#", "/")):
        return href
    if href.startswith("../"):
        rest = href[3:]
        return "%s/n/%s" % (base, rest) if not rest.startswith(("..", ".")) else None
    if source_dir:
        target = (PROJECT / source_dir / unquote(href)).resolve()
        try:
            return "/wiki/f/" + quote(target.relative_to(PROJECT).as_posix())
        except ValueError:
            return None
    return "%s/%s" % (base, href)


ATTR_URL = re.compile(r'\b(src|href)="([^"]+)"')


def rewrite_urls(block: str, base: str, source_dir: str = "") -> str:
    """Point a raw HTML block's relative paths at the site base."""
    def one(m):
        target = url(m.group(2), base, source_dir)
        return '%s="%s"' % (m.group(1), target) if target else '%s=""' % m.group(1)

    return ATTR_URL.sub(one, block)


def markdown(text: str, base: str, source_dir: str = "") -> str:
    """The Markdown subset the notes use."""
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):                       # fenced code
            i += 1
            body = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % esc("\n".join(body)))
            continue

        if re.match(r"^<(figure|div|iframe|table|dl|p|img)\b", stripped):   # raw HTML block
            block, depth = [], 0
            while i < len(lines):
                block.append(lines[i])
                depth += len(re.findall(r"<(figure|div|table|dl)\b", lines[i]))
                depth -= len(re.findall(r"</(figure|div|table|dl)>", lines[i]))
                i += 1
                if depth <= 0:
                    break
            out.append(rewrite_urls("\n".join(block), base, source_dir))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)         # heading
        if m:
            level = min(len(m.group(1)) + 1, 6)
            text_ = m.group(2)
            out.append('<h%d id="%s">%s</h%d>'
                       % (level, slugify(text_), inline(text_, base, source_dir), level))
            i += 1
            continue

        if stripped.startswith("|"):                         # table
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(table_html(rows, base, source_dir))
            continue

        if re.match(r"^(-|\d+\.)\s+", stripped):             # list
            tag = "ul" if stripped.startswith("-") else "ol"
            items = []
            while i < len(lines) and re.match(r"^\s*(-|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*(-|\d+\.)\s+", "", lines[i]))
                i += 1
            out.append("<%s>%s</%s>"
                       % (tag, "".join("<li>%s</li>" % inline(x, base, source_dir) for x in items), tag))
            continue

        if i + 1 < len(lines) and lines[i + 1].strip().startswith(": "):   # definition list
            pairs = []
            while i + 1 < len(lines) and lines[i + 1].strip().startswith(": "):
                pairs.append((lines[i].strip(), lines[i + 1].strip()[2:]))
                i += 2
                while i < len(lines) and not lines[i].strip():
                    i += 1
            out.append('<dl class="kv">%s</dl>' % "".join(
                "<dt>%s</dt><dd>%s</dd>" % (inline(t, base, source_dir), inline(d, base, source_dir)) for t, d in pairs))
            continue

        para = [stripped]                                    # paragraph
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^\s*(```|#{1,6}\s|\||-\s|\d+\.\s|<(figure|div|iframe|table|dl)\b|:\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(para), base, source_dir))
    return "\n".join(out)


def table_html(rows, base, source_dir=""):
    body = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    head, rest = (body[0], body[1:]) if len(body) > 1 else (None, body)
    html = ["<div class='scroll'><table>"]
    if head:
        html.append("<thead><tr>%s</tr></thead>"
                    % "".join("<th>%s</th>" % inline(c, base, source_dir) for c in head))
    html.append("<tbody>%s</tbody>" % "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c, base, source_dir) for c in r) for r in rest))
    html.append("</table></div>")
    return "".join(html)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", text).lower()).strip("-") or "x"


def plain(html_text: str) -> str:
    """Visible text of rendered HTML, for the search index."""
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", html_text, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


# ---------------------------------------------------------- resumability

_RESUME_CACHE: dict = {}


def resumable(job: str) -> bool:
    """True when the bridge can still resume the session that made this note."""
    if not job:
        return False
    if job not in _RESUME_CACHE:
        ok = False
        if BRIDGE.is_file():
            import subprocess
            try:
                r = subprocess.run(["/usr/bin/python3", str(BRIDGE), "ask", "--resolve", job],
                                   capture_output=True, text=True, timeout=30)
                ok = r.returncode == 0
            except Exception:
                ok = False
        _RESUME_CACHE[job] = ok
    return _RESUME_CACHE[job]


# ------------------------------------------------------------ templates

def shell(title, base, body, rail, extra_head="", desc=""):
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="stylesheet" href="%(base)s/style.css">
<link rel="icon" type="image/png" sizes="32x32" href="%(base)s/icons/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="%(base)s/icons/apple-touch-icon.png">
<link rel="manifest" href="%(base)s/site.webmanifest">
<link rel="alternate" type="application/rss+xml" href="%(base)s/feed.xml" title="%(name)s">
<meta name="application-name" content="%(name)s">
<meta name="apple-mobile-web-app-title" content="%(name)s">
<meta name="theme-color" content="#15181b">
%(desc)s%(extra)s</head><body>
<div class="frame">
<nav class="side">
  <a class="brand" href="%(base)s/">%(name)s<small>%(who)s</small></a>
  <form class="search" role="search" action="%(base)s/" onsubmit="return false">
    <input id="q" type="search" autocomplete="off" placeholder="Search notes" aria-label="Search notes">
  </form>
  <div id="results" class="results" hidden></div>
  %(rail)s
</nav>
<main>
%(body)s
</main>
</div>
<script src="%(base)s/search.js" defer></script>
</body></html>
""" % {"title": esc(title), "base": base, "name": SITE_NAME, "who": esc(SITE_WHO),
       "rail": rail, "body": body, "extra": extra_head,
       "desc": ('<meta name="description" content="%s">\n' % esc(desc)) if desc else ""}


def rail_sections(notes, base, current=""):
    counts = {}
    for n in notes:
        counts[n["section"]] = counts.get(n["section"], 0) + 1
    items = []
    if not counts:
        return ""
    for name in SECTIONS:
        if name not in counts:
            continue
        cls = " class=\"on\"" if name == current else ""
        items.append('<li%s><a href="%s/sections/#%s">%s</a><span class="n">%d</span></li>'
                     % (cls, base, slugify(name), esc(name), counts[name]))
    return '<div><h4>Sections</h4><ul>%s</ul></div>' % "".join(items)


def rail_note(note, base, headings):
    blocks = []
    if headings:
        blocks.append('<div><h4>On this page</h4><ul>%s</ul></div>' % "".join(
            '<li><a href="#%s">%s</a></li>' % (h_id, esc(h_text)) for h_id, h_text in headings))
    meta = ['<li><span>%s</span></li>' % esc(note["date"])]
    if note["job"]:
        meta.append('<li><span class="n">%s</span></li>' % esc(note["job"]))
    if note.get("old"):
        meta.append('<li><a href="%s/%s">Original</a></li>' % (base, note["old"]))
    blocks.append('<div><h4>Record</h4><ul class="rec">%s</ul></div>' % "".join(meta))
    return "".join(blocks)


def feed_rows(notes, base):
    rows = []
    for n in notes:
        kind = ("%s · %s" % (n["section"].lower(), n["status"])) if n["status"] \
            else n["section"].lower()
        cls = " obs" if n["status"] else ""
        rows.append(
            '<li><span class="d">%s</span><span><a class="t" href="%s/n/%s/">%s</a>'
            '<span class="k%s">%s</span></span></li>'
            % (esc(n["date"]), base, n["slug"], esc(n["title"]), cls, esc(kind)))
    return '<ul class="feed">%s</ul>' % "".join(rows)


# ---------------------------------------------------------------- build

def build(notes_dir: Path, out: Path, base: str) -> int:
    notes = [n for n in (parse_note(p) for p in sorted(notes_dir.glob("*.md"))) if n]
    notes.sort(key=lambda n: (n["date"], n["title"]), reverse=True)

    scratch = out.with_name(out.name + ".new")
    shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True)

    # assets
    shutil.copytree(ROOT / "assets/fonts", scratch / "fonts",
                    ignore=shutil.ignore_patterns("faces.json"))
    if (ROOT / "assets/icons").is_dir():
        shutil.copytree(ROOT / "assets/icons", scratch / "icons")
    figures = scratch / "figures"
    for src in ROOT.glob("analyses/**/*"):
        if src.is_file() and src.suffix.lower() in (".png", ".pdf", ".jpg", ".svg"):
            dest = figures / src.relative_to(ROOT / "analyses")
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
    if (ROOT / "_old").is_dir():
        shutil.copytree(ROOT / "_old", scratch / "_old", symlinks=False,
                        ignore=shutil.ignore_patterns("*.bak-*"))
    (scratch / "style.css").write_text(stylesheet(base), encoding="utf-8")
    (scratch / "search.js").write_text(SEARCH_JS.replace("__BASE__", base), encoding="utf-8")
    (scratch / "site.webmanifest").write_text(json.dumps({
        "name": SITE_NAME, "short_name": "Notebook", "start_url": base + "/",
        "display": "standalone", "background_color": "#15181b", "theme_color": "#15181b",
        "icons": [{"src": base + "/icons/icon.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=1), encoding="utf-8")

    index = []
    for pos, note in enumerate(notes):
        body_md, thread = split_thread(note["body"])
        if note.get("embed"):
            body_html = ('<div class="embed"><iframe src="%s/%s" title="%s" loading="lazy">'
                         '</iframe></div>' % (base, note["embed"], esc(note["title"])))
        else:
            body_html = markdown(body_md, base, os.path.dirname(note.get("source", "")))
        headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
        headings = [(h, re.sub(r"<[^>]+>", "", t)) for h, t in headings][:8]

        eyebrow = ['<span>%s</span>' % esc(note["section"])]
        eyebrow += ['<span class="tag">%s</span>' % esc(t) for t in note["tags"][:3]]
        eyebrow.append('<span>%s</span>' % esc(note["date"]))
        if note["status"]:
            eyebrow.append('<span class="k obs">%s</span>' % esc(note["status"]))

        pager = []
        if pos + 1 < len(notes):
            pager.append('<a href="%s/n/%s/">%s</a>'
                         % (base, notes[pos + 1]["slug"], esc(notes[pos + 1]["title"])))
        else:
            pager.append("<span></span>")
        if pos:
            pager.append('<a href="%s/n/%s/">%s</a>'
                         % (base, notes[pos - 1]["slug"], esc(notes[pos - 1]["title"])))
        else:
            pager.append("<span></span>")

        page = ('<div class="eyebrow">%s</div><h1>%s</h1><div class="prose">%s%s</div>%s'
                '<div class="foot">%s</div>'
                % ("".join(eyebrow), esc(note["title"]), body_html,
                   thread_html(thread), ask_box(note, base), "".join(pager)))
        dest = scratch / "n" / note["slug"]
        dest.mkdir(parents=True)
        (dest / "index.html").write_text(
            shell("%s · %s" % (note["title"], SITE_NAME), base, page,
                  rail_note(note, base, headings)), encoding="utf-8")
        index.append({"t": note["title"], "u": "%s/n/%s/" % (base, note["slug"]),
                      "d": note["date"], "s": note["section"],
                      "g": " ".join(note["tags"]),
                      "x": plain(body_html)[:4000]})

    (scratch / "search.json").write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")

    foot = ('<div class="foot"><span>%d</span><span><a href="%s/feed.xml">RSS</a> · '
            '<a href="%s/date/">By date</a> · <a href="%s/sections/">By topic</a></span></div>'
            % (len(notes), base, base, base))
    (scratch / "index.html").write_text(
        shell(SITE_NAME, base, "<h1>Notes</h1>" + feed_rows(notes, base) + foot,
              rail_sections(notes, base)), encoding="utf-8")

    by_date = []
    for year_month in sorted({n["date"][:7] for n in notes if n["date"]}, reverse=True):
        rows = [n for n in notes if n["date"].startswith(year_month)]
        by_date.append('<h2 id="%s">%s</h2>%s' % (year_month, year_month, feed_rows(rows, base)))
    (scratch / "date").mkdir()
    (scratch / "date/index.html").write_text(
        shell("By date · " + SITE_NAME, base, "<h1>By date</h1>" + "".join(by_date),
              rail_sections(notes, base)), encoding="utf-8")

    by_section = []
    for name in SECTIONS:
        rows = [n for n in notes if n["section"] == name]
        if rows:
            by_section.append('<h2 id="%s">%s</h2>%s' % (slugify(name), esc(name),
                                                         feed_rows(rows, base)))
    (scratch / "sections").mkdir()
    (scratch / "sections/index.html").write_text(
        shell("By topic · " + SITE_NAME, base, "<h1>By topic</h1>" + "".join(by_section),
              rail_sections(notes, base)), encoding="utf-8")

    (scratch / "feed.xml").write_text(rss(notes, base), encoding="utf-8")

    backup = out.with_name(out.name + ".old")
    shutil.rmtree(backup, ignore_errors=True)
    if out.exists():
        out.rename(backup)
    scratch.rename(out)
    shutil.rmtree(backup, ignore_errors=True)
    print("built %d notes" % len(notes))
    return 0


def thread_html(turns):
    if not turns:
        return ""
    rows = []
    for t in turns:
        rows.append('<div class="turn"><p class="q"><b>Q</b> <span class="d">%s</span> %s</p>'
                    '<p class="a"><b>A</b> %s</p></div>'
                    % (esc(t.get("date", "")), esc(t["q"]), esc(t["a"])))
    return '<div class="thread"><h2 id="thread">Thread</h2>%s</div>' % "".join(rows)


def ask_box(note, base):
    """The question box, shown only when that worker's session can be resumed."""
    if not resumable(note["job"]):
        return ""
    return ('<form class="ask" data-job="%s" data-note="%s">'
            '<input name="q" type="text" autocomplete="off" placeholder="Question" '
            'aria-label="Question" required>'
            '<button type="submit">Ask</button>'
            '<span class="state" hidden></span></form>' % (esc(note["job"]), esc(note["slug"])))


def rss(notes, base):
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for n in notes[:50]:
        try:
            when = datetime.strptime(n["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            when = when.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except ValueError:
            when = now
        link = "%s/n/%s/" % (base, n["slug"])
        items.append("<item><title>%s</title><link>%s</link><guid isPermaLink=\"false\">%s</guid>"
                     "<pubDate>%s</pubDate></item>"
                     % (xesc(n["title"]), xesc(link), xesc(n["slug"]), when))
    return ('<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0"><channel>'
            '<title>%s</title><link>%s/</link><description>%s</description>'
            '<lastBuildDate>%s</lastBuildDate>%s</channel></rss>\n'
            % (xesc(SITE_NAME), xesc(base), xesc(SITE_NAME), now, "".join(items)))


# --------------------------------------------------------------- assets

def font_faces(base: str) -> str:
    faces = json.loads((ROOT / "assets/fonts/faces.json").read_text())
    out = []
    for f in faces:
        family = "Newsreader" if f["file"].startswith("newsreader") else "JetBrains Mono"
        out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
                   "src:url(%s/fonts/%s) format('woff2');unicode-range:%s}"
                   % (family, f["style"], f["weight"], base, f["file"], f["range"]))
    return "\n".join(out)


def stylesheet(base: str) -> str:
    return font_faces(base) + """
:root{
  --ground:#f2f3f0; --paper:#fafaf8; --ink:#1c2024; --ink-2:#4b535b; --ink-3:#7d858d;
  --rule:#d9dcd6; --accent:#a83c3c; --accent-2:#3f5570; --wash:#e9ecef; --code:#eef0ec;
  --obsolete:#9a7b2a;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --ground:#15181b; --paper:#1b1f23; --ink:#e4e2dc; --ink-2:#aeb2b6; --ink-3:#7c8288;
  --rule:#2c3237; --accent:#d9736b; --accent-2:#8fa9c6; --wash:#22282d; --code:#20252a;
  --obsolete:#c9a44a;
}}
:root[data-theme="dark"]{
  --ground:#15181b; --paper:#1b1f23; --ink:#e4e2dc; --ink-2:#aeb2b6; --ink-3:#7c8288;
  --rule:#2c3237; --accent:#d9736b; --accent-2:#8fa9c6; --wash:#22282d; --code:#20252a;
  --obsolete:#c9a44a;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:Newsreader,Georgia,"Times New Roman",serif;font-size:18px;line-height:1.55;
  font-optical-sizing:auto}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
code,pre,.mono,.n,.d,.k,.eyebrow,.side h4,dt,.brand small,.search input,.ask input,.ask button{
  font-family:"JetBrains Mono",ui-monospace,Menlo,monospace}
.frame{max-width:1180px;margin:0 auto;background:var(--paper);border-left:1px solid var(--rule);
  border-right:1px solid var(--rule);display:grid;grid-template-columns:240px 1fr;min-height:100vh}
nav.side{border-right:1px solid var(--rule);padding:26px 22px;display:flex;flex-direction:column;
  gap:22px;font-size:.95rem;align-self:start;position:sticky;top:0;max-height:100vh;overflow:auto}
.brand{font-weight:500;font-size:1.15rem;letter-spacing:-.01em;line-height:1.1;color:var(--ink)}
.brand:hover{text-decoration:none}
.brand small{display:block;font-size:.72rem;color:var(--ink-3);letter-spacing:.08em;
  text-transform:uppercase;margin-top:6px}
.search{margin:0}
.search input,.ask input{width:100%;border:1px solid var(--rule);background:var(--ground);
  padding:7px 10px;color:var(--ink);font-size:.85rem;border-radius:0}
.search input::placeholder,.ask input::placeholder{color:var(--ink-3)}
.results{border:1px solid var(--rule);background:var(--ground);max-height:46vh;overflow:auto}
.results a{display:block;padding:7px 10px;border-bottom:1px solid var(--rule);color:var(--ink);
  font-size:.9rem}
.results a:last-child{border-bottom:0}
.results a:hover{background:var(--wash);text-decoration:none}
.results .d{display:block;font-size:.68rem;color:var(--ink-3)}
.side h4{margin:0 0 6px;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);font-weight:500}
.side ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.side li{display:flex;justify-content:space-between;gap:8px;color:var(--ink-2)}
.side li a{color:var(--ink-2)}
.side li.on a{color:var(--ink);font-weight:500}
.side li span.n{color:var(--ink-3);font-size:.72rem}
.side .rec li{color:var(--ink-3);font-size:.8rem}
main{padding:34px 48px 60px;max-width:900px;min-width:0}
.eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);
  display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.eyebrow .tag{color:var(--accent-2)}
h1{font-size:2.2rem;line-height:1.08;font-weight:400;letter-spacing:-.015em;margin:8px 0 18px;
  text-wrap:balance}
h2{font-size:1.35rem;font-weight:500;margin:34px 0 8px;letter-spacing:-.01em}
h3{font-size:1.12rem;font-weight:500;margin:26px 0 6px}
h4{font-size:1rem;font-weight:500;margin:20px 0 6px}
p{max-width:65ch;margin:0 0 1em}
.prose li{max-width:64ch;margin-bottom:.3em}
.feed{list-style:none;padding:0;margin:20px 0 0;border-top:1px solid var(--rule)}
.feed li{display:grid;grid-template-columns:96px 1fr;gap:18px;padding:14px 0;
  border-bottom:1px solid var(--rule);align-items:baseline}
.feed .d{font-size:.74rem;color:var(--ink-3);font-variant-numeric:tabular-nums}
.feed .t{font-size:1.08rem}
.feed .k{font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--accent-2);
  margin-left:10px}
.feed .k.obs,.eyebrow .k.obs{color:var(--obsolete)}
figure{margin:22px 0;max-width:760px}
figure img{width:100%;height:auto;background:var(--wash);border:1px solid var(--rule)}
figcaption{font-size:.9rem;color:var(--ink-2);margin-top:8px;max-width:65ch}
.embed{margin:20px 0;border:1px solid var(--rule);background:var(--wash)}
.embed iframe{width:100%;height:78vh;min-height:520px;border:0;display:block}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:6px 22px;font-size:.95rem;
  margin:14px 0 18px;max-width:620px}
.kv dt{color:var(--ink-3);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;
  padding-top:5px}
.kv dd{margin:0;font-variant-numeric:tabular-nums}
pre{background:var(--code);border:1px solid var(--rule);padding:12px 14px;font-size:.78rem;
  line-height:1.5;overflow-x:auto;max-width:760px;margin:12px 0 18px;color:var(--ink)}
p code,li code,td code,figcaption code,dd code{background:var(--code);font-size:.8em;padding:1px 4px}
.scroll{overflow-x:auto;max-width:100%;margin:14px 0 20px}
table{border-collapse:collapse;font-size:.86rem;min-width:100%}
th,td{border-bottom:1px solid var(--rule);padding:6px 12px 6px 0;text-align:left;
  vertical-align:top}
th{color:var(--ink-3);font-weight:500;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}
.thread{margin-top:38px}
.turn{border-left:2px solid var(--rule);padding:2px 0 2px 14px;margin:14px 0}
.turn .q{color:var(--ink);margin-bottom:.4em}
.turn .a{color:var(--ink-2)}
.turn .d{font-size:.72rem;color:var(--ink-3)}
.ask{display:flex;gap:8px;align-items:center;margin:18px 0 0;max-width:620px;flex-wrap:wrap}
.ask input{flex:1;min-width:180px}
.ask button{border:1px solid var(--rule);background:var(--wash);color:var(--ink);
  padding:7px 14px;font-size:.85rem;cursor:pointer}
.ask button:hover{background:var(--code)}
.ask .state{font-size:.75rem;color:var(--ink-3)}
.foot{margin-top:38px;padding-top:14px;border-top:1px solid var(--rule);display:flex;
  justify-content:space-between;font-size:.85rem;color:var(--ink-3);flex-wrap:wrap;gap:10px}
.foot a{color:var(--ink-2)}
@media (max-width:760px){
  .frame{grid-template-columns:1fr;border:0}
  nav.side{border-right:0;border-bottom:1px solid var(--rule);position:static;max-height:none}
  main{padding:24px 20px 48px}
  .feed li{grid-template-columns:1fr;gap:2px}
  h1{font-size:1.8rem}
  body{font-size:17px}
}
"""


SEARCH_JS = r"""
(function () {
  var base = "__BASE__", box = document.getElementById("q"),
      panel = document.getElementById("results"), data = null, timer = 0;
  if (!box || !panel) return;

  function load() {
    if (data) return Promise.resolve(data);
    return fetch(base + "/search.json").then(function (r) { return r.json(); })
      .then(function (j) { data = j; return j; });
  }
  function score(note, terms) {
    var t = note.t.toLowerCase(), g = note.g.toLowerCase(), x = note.x.toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) {
      var w = terms[i];
      if (t.indexOf(w) >= 0) s += 8;
      if (g.indexOf(w) >= 0) s += 4;
      var at = x.indexOf(w);
      if (at >= 0) s += 1;
      if (at < 0 && t.indexOf(w) < 0 && g.indexOf(w) < 0) return 0;
    }
    return s;
  }
  function render(rows) {
    panel.innerHTML = rows.map(function (n) {
      return '<a href="' + n.u + '">' + n.t + '<span class="d">' + n.d + " \u00b7 " + n.s + "</span></a>";
    }).join("");
    panel.hidden = rows.length === 0;
  }
  function run() {
    var query = box.value.trim().toLowerCase();
    if (query.length < 2) { panel.hidden = true; return; }
    load().then(function (all) {
      var terms = query.split(/\s+/), hits = [];
      for (var i = 0; i < all.length; i++) {
        var s = score(all[i], terms);
        if (s > 0) hits.push([s, all[i]]);
      }
      hits.sort(function (a, b) { return b[0] - a[0]; });
      render(hits.slice(0, 12).map(function (h) { return h[1]; }));
    });
  }
  box.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 90); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== box) { e.preventDefault(); box.focus(); }
    if (e.key === "Escape") { panel.hidden = true; box.blur(); }
  });

  var form = document.querySelector("form.ask");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var input = form.querySelector("input[name=q]"), state = form.querySelector(".state");
    var question = input.value.trim();
    if (!question || form.dataset.busy) return;
    form.dataset.busy = "1";
    state.hidden = false;
    state.textContent = "Asking";
    fetch(base + "/ask", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job: form.dataset.job, note: form.dataset.note, question: question })
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (j.ok) { location.reload(); return; }
      state.textContent = j.state || "Failed";
      form.dataset.busy = "";
    }).catch(function () {
      state.textContent = "Failed";
      form.dataset.busy = "";
    });
  });
})();
"""


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", type=Path, default=ROOT / "notes")
    ap.add_argument("--out", type=Path, default=ROOT / "public")
    ap.add_argument("--base", default="/wiki")
    args = ap.parse_args(argv[1:])
    return build(args.notes.resolve(), args.out.resolve(), args.base.rstrip("/"))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
