"""Research records, existing evidence and meaning-preserving message display."""

import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
import research_figures


EXPERIMENT_STATES = {
    "planned": "Planned", "running": "Running", "results-ready": "Results ready",
    "reviewed": "Reviewed", "stopped": "Stopped", "recorded": "Recorded",
}
QUESTION_STATES = {"open": "Open", "paused": "Paused", "answered": "Answered"}
RUN_STATES = {"planned", "running", "complete", "failed"}
SECTIONS = {
    "direction": ("Your words",),
    "question": ("Context", "Your words", "References", "Decisions"),
    "experiment": ("Context", "Before delegation", "Execution plan", "Amendments", "Runs",
                   "Figures", "Measurements", "Results", "Caveats", "References", "Your interpretation", "Next decision"),
}
MESSAGE_SECTIONS = {"Your words", "Before delegation", "Amendments", "Decisions",
                    "Your interpretation", "Next decision"}
ID = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
LINK = re.compile(r'!?\[[^\]]*\]\(([^\s)]+)\)|(?:href|src)="([^"]+)"')
esc = html.escape


def refs(record, field):
    return [value.strip() for value in record.get(field, "").split(",") if value.strip()]


def parse(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n") or "\n---\n" not in raw[4:]:
        raise ValueError("missing frontmatter")
    head, body = raw[4:].split("\n---\n", 1)
    record = {"path": path, "sections": {}, "raw": raw}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            record[key.strip()] = value.strip()
    kind = record.get("kind")
    if kind not in SECTIONS:
        raise ValueError("kind must be direction, question or experiment")
    # A heading inside a fenced message is part of the user's text, not structure.
    current, fence = None, False
    for line in body.splitlines(keepends=True):
        if line.startswith("```"):
            fence = not fence
        if line.startswith("## ") and not fence:
            current = line[3:].strip()
            if current not in SECTIONS[kind] or current in record["sections"]:
                raise ValueError("unknown or repeated section: " + current)
            record["sections"][current] = ""
        elif current:
            record["sections"][current] += line
        elif line.strip():
            raise ValueError("content must belong to a named section")
    for name in SECTIONS[kind]:
        content = record["sections"].get(name, "").strip()
        if name in MESSAGE_SECTIONS or name in {"Runs", "Figures"}:
            if not content:
                value = []
            else:
                block = re.fullmatch(r"```json\s*\n(.*)\n```", content, re.S)
                if not block:
                    raise ValueError(name + " must contain a fenced JSON array")
                value = json.loads(block[1])
                if not isinstance(value, list) or any(not isinstance(v, dict) for v in value):
                    raise ValueError(name + " must be an array of objects")
            record["sections"][name] = value
        else:
            record["sections"][name] = content
    return record


def load(directory):
    records, faults = [], []
    paths = [directory / "direction.md"]
    for kind in ("questions", "experiments"):
        paths.extend(sorted((directory / kind).glob("*.md")))
    for path in paths:
        if not path.exists():
            continue
        try:
            record = parse(path)
            expected = "direction" if path.name == "direction.md" else path.parent.name[:-1]
            if record["kind"] != expected:
                raise ValueError("kind does not match its source directory")
            records.append(record)
        except (ValueError, KeyError) as exc:
            faults.append("%s: %s" % (path, exc))
    return records, faults


def asset_url(target, base, project):
    """Project-relative evidence links use the existing read-only file route."""
    parsed = urlsplit(target)
    if parsed.scheme in ("https", "http") and parsed.netloc:
        return target
    if target.startswith("#"):
        return target
    if parsed.scheme or parsed.netloc or target.startswith("/"):
        raise ValueError("use a project-relative file or an http(s) URL: " + target)
    path = (project / unquote(parsed.path)).resolve()
    try:
        relative = path.relative_to(project.resolve())
    except ValueError as exc:
        raise ValueError("evidence leaves the project: " + target) from exc
    if not path.is_file():
        raise ValueError("missing evidence file: " + target)
    if relative.parent == Path("wiki/notes") and relative.suffix == ".md":
        return base + "/n/" + quote(relative.stem) + "/" + (
            "#" + parsed.fragment if parsed.fragment else "")
    return base + "/f/" + quote(relative.as_posix()) + (
        "#" + parsed.fragment if parsed.fragment else "")


def validate(records, project):
    faults, ids = [], set()
    by_id = {r.get("id"): r for r in records}
    for r in records:
        prefix = str(r["path"]) + ": "

        def fail(message):
            faults.append(prefix + message)

        def evidence(target):
            if not isinstance(target, str):
                fail("evidence reference must be a string")
                return
            try:
                asset_url(target, "", project)
            except (ValueError, TypeError) as exc:
                fail(str(exc))

        ident = r.get("id", "")
        if not ID.fullmatch(ident) or ident in ids:
            fail("id must be unique, lowercase letters, digits and hyphens")
        ids.add(ident)
        if r["kind"] != "direction" and r["path"].stem != ident:
            fail("filename must match id")
        if not r.get("title"):
            fail("title is required")
        try:
            date.fromisoformat(r.get("date", ""))
        except ValueError:
            fail("date must be YYYY-MM-DD")
        s = r["sections"]
        existing = r.get("origin", "new") == "existing"
        if r.get("origin", "new") not in {"new", "existing"}:
            fail("origin must be new or existing")
        for slug in refs(r, "source_notes"):
            if not ID.fullmatch(slug):
                fail("source_notes must contain note slugs")
            else:
                evidence("wiki/notes/" + slug + ".md")
        for group in refs(r, "result_groups"):
            path = (project / group).resolve()
            if not path.is_relative_to(project.resolve()) or not path.is_dir():
                fail("result_groups must reference existing project directories: " + group)
        if existing and (not s.get("Context") or not s.get("References")):
            fail("existing records require documented context and source references")
        if existing and not LINK.search(s.get("References", "")):
            fail("existing records require a source link")
        for name in MESSAGE_SECTIONS & s.keys():
            for message in s[name]:
                if not isinstance(message.get("text"), str) or not message["text"].strip():
                    fail(name + ": text must contain the original user message")
                try:
                    date.fromisoformat(message.get("date", ""))
                except (TypeError, ValueError):
                    fail(name + ": date must be YYYY-MM-DD")
                if message.get("source"):
                    evidence(message["source"])
                if "source_ref" in message and not isinstance(message["source_ref"], str):
                    fail(name + ": source_ref must be a string")
                if "display_text" in message and (not isinstance(message["display_text"], str) or not message["display_text"].strip()):
                    fail(name + ": display_text must be a nonempty string")
        if r["kind"] == "direction":
            if not s["Your words"]:
                fail("direction requires your original words")
            continue
        states = QUESTION_STATES if r["kind"] == "question" else EXPERIMENT_STATES
        if r.get("status") not in states:
            fail("status must be " + ", ".join(states))
        if r["kind"] == "question":
            if not existing and not s["Your words"]:
                fail("question requires your original words")
            if r.get("status") == "answered" and not s["Decisions"]:
                fail("answered question requires your recorded decision")
        else:
            parent = by_id.get(r.get("question"), {})
            if parent.get("kind") != "question":
                fail("question must reference an existing question id")
            for target in refs(r, "related_questions"):
                if by_id.get(target, {}).get("kind") != "question" or target == r.get("question"):
                    fail("related_questions must reference another question: " + target)
            for target in filter(None, r.get("follow_up", "").split(",")):
                target = target.strip()
                if by_id.get(target, {}).get("kind") != "experiment" or target == ident:
                    fail("follow_up must reference another experiment: " + target)
            if not existing and not s["Before delegation"]:
                fail("experiment requires your before-delegation words")
            runs, seen = s["Runs"], set()
            for run in runs:
                run_id = run.get("id", "")
                if not isinstance(run_id, str) or not ID.fullmatch(run_id) or run_id in seen:
                    fail("run id must be valid and unique within the experiment")
                if isinstance(run_id, str):
                    seen.add(run_id)
                if run.get("status") not in RUN_STATES:
                    fail("run status must be planned, running, complete or failed")
                if run.get("status") != "planned" and not existing:
                    for field in ("arm", "code", "model", "config", "data"):
                        if not isinstance(run.get(field), str) or not run[field].strip():
                            fail("run %s needs %s" % (run.get("id"), field))
                    if type(run.get("seed")) is not int:
                        fail("run %s needs an integer seed" % run.get("id"))
                    for field in ("config", "data"):
                        if run.get(field):
                            evidence(run[field])
                if existing:
                    for field in ("config", "data"):
                        if run.get(field):
                            evidence(run[field])
                artifacts = run.get("artifacts", [])
                if not isinstance(artifacts, list) or any(not isinstance(a, dict) for a in artifacts):
                    fail("run artifacts must be an array of label/path objects")
                    continue
                for a in artifacts:
                    if not isinstance(a.get("label"), str) or not a["label"] or not isinstance(a.get("path"), str):
                        fail("each artifact needs a label and path")
                    else:
                        evidence(a["path"])
                if existing and not artifacts and not run.get("config"):
                    fail("existing run requires an artifact or source configuration")
                if run.get("status") == "complete" and not existing:
                    if not any(isinstance(a.get("path"), str) and urlsplit(a["path"]).path.endswith(".ipynb") for a in artifacts):
                        fail("completed run needs its executed notebook artifact")
                if run.get("status") == "failed" and not existing and (not isinstance(run.get("error"), str) or not run["error"]):
                    fail("failed run needs its error recorded")
            status = r.get("status")
            if status == "recorded" and not existing:
                fail("recorded status is only for existing research")
            if status == "recorded" and not s["Results"]:
                fail("recorded experiment requires documented results")
            running = any(run.get("status") == "running" for run in runs)
            if status == "planned" and any(run.get("status") != "planned" for run in runs):
                fail("planned experiment contains an attempted run")
            if status in {"planned", "stopped", "results-ready", "reviewed", "recorded"} and running:
                fail("experiment status contradicts a running run")
            if status in {"running", "results-ready", "reviewed"} and not s["Execution plan"]:
                fail("an executed experiment needs its execution plan")
            if status == "running" and not runs:
                fail("running experiment needs a run record")
            if status in {"results-ready", "reviewed"}:
                if not s["Results"] or not any(run.get("status") == "complete" for run in runs):
                    fail("results require a completed run and recorded results")
            if status == "reviewed" and not s["Your interpretation"]:
                fail("reviewed requires your recorded interpretation")
        for name, content in s.items():
            if isinstance(content, str):
                for match in LINK.finditer(content):
                    evidence(match[1] or match[2])
    return faults + research_figures.validate(records, project, asset_url)


def route(r, base):
    return base + ("/q/" if r["kind"] == "question" else "/e/") + r["id"] + "/"


def messages_html(messages):
    blocks = []
    for m in messages:
        source = ('<a href="%s">Chat reference</a>' % esc(m["_source_url"])) if m.get("_source_url") else ""
        if m.get("source_ref"):
            source += '<span>%s</span>' % esc(m["source_ref"])
        original = '<blockquote class="verbatim">%s</blockquote>' % esc(m["text"])
        edited = m.get("display_text")
        content = ('<p class="edited-message">%s</p><details class="original-message">'
                   '<summary>Original wording</summary>%s</details>' % (esc(edited), original)
                   if edited and edited != m["text"] else original)
        label = "Liu Hao · lightly edited" if edited and edited != m["text"] else "Liu Hao"
        blocks.append('<figure class="user-message"><figcaption><span>%s</span>'
                      '<time datetime="%s">%s</time>%s</figcaption>%s</figure>'
                      % (label, esc(m["date"]), esc(m["date"]), source, content))
    return "".join(blocks) or '<p class="empty">Not recorded</p>'


def record_rows(records, base):
    rows = []
    for r in records:
        status = (QUESTION_STATES if r["kind"] == "question" else EXPERIMENT_STATES)[r["status"]]
        rows.append('<li class="research-row" data-status="%s"><span class="d">%s</span>'
                    '<div><a class="t" href="%s">%s</a><span class="record-id">%s</span></div>'
                    '<span class="research-status %s">%s</span></li>' % (
                        r["status"], esc(r["date"]), route(r, base), esc(r["title"]),
                        esc(r["id"]), r["status"], status))
    return '<ul class="research-list">%s</ul>' % "".join(rows) if rows else '<p class="empty">None yet</p>'


def note_backlinks(slug, records, base):
    linked = [r for r in records if slug in refs(r, "source_notes")]
    if not linked:
        return ""
    return '<section class="research-links"><h2>Research entries</h2>%s</section>' % record_rows(linked, base)


def write_pages(records, notes, scratch, base, builder):
    """Build a shared question and experiment structure, preserving source routes."""
    project = builder.PROJECT
    records = sorted(records, key=lambda r: (r["date"], r["id"]), reverse=True)
    questions = [r for r in records if r["kind"] == "question"]
    experiments = [r for r in records if r["kind"] == "experiment"]
    by_id = {r["id"]: r for r in records}
    for r in records:
        for name in MESSAGE_SECTIONS & r["sections"].keys():
            for m in r["sections"][name]:
                if m.get("source"):
                    m["_source_url"] = asset_url(m["source"], base, project)

    def md(content):
        def replace(m):
            target = m[1] or m[2]
            return m[0].replace(target, asset_url(target, base, project))
        return builder.markdown(LINK.sub(replace, content), base)

    def section(title, content, attribution=""):
        return '<section class="research-section"><h2 id="%s">%s</h2>%s%s</section>' % (
            builder.slugify(title), esc(title),
            '<p class="attribution">%s</p>' % esc(attribution) if attribution else "", content)

    def page(path, title, body):
        dest = scratch / path / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(builder.shell(title + " · " + builder.SITE_NAME, base,
                                     body, builder.rail_sections(notes, base)), encoding="utf-8")

    def page_top(kind, title):
        return '<div class="eyebrow">%s</div><h1>%s</h1>' % (esc(kind), esc(title))

    search = []
    for r in questions + experiments:
        s = r["sections"]
        body = page_top("Question" if r["kind"] == "question" else "Experiment", r["title"])
        states = QUESTION_STATES if r["kind"] == "question" else EXPERIMENT_STATES
        body += '<div class="record-meta"><span class="record-id">%s</span><span class="research-status %s">%s</span></div>' % (
            esc(r["id"]), r["status"], states[r["status"]])
        existing = r.get("origin") == "existing"
        if existing:
            body += '<p class="attribution">Existing research · organised from saved records</p>'
        if s["Context"]:
            body += section("Context", md(s["Context"]), "Agent · source summary")
        if r["kind"] == "question":
            if s["Your words"] or not existing:
                body += section("Your reasoning", messages_html(s["Your words"]))
            if s["References"]:
                body += section("References", md(s["References"]))
            body += section("Experiments", record_rows([e for e in experiments if e["question"] == r["id"] or r["id"] in refs(e, "related_questions")], base))
            if s["Decisions"] or not existing:
                body += section("Decisions", messages_html(s["Decisions"]))
        else:
            parent = by_id[r["question"]]
            body += '<p class="parent-question"><a href="%s">%s</a></p>' % (route(parent, base), esc(parent["title"]))
            body += '<p><a href="%s">View results</a></p>' % route(r, base)
            body += '<nav class="record-sections" aria-label="Experiment sections">' + "".join(
                '<a href="#%s">%s</a>' % (builder.slugify(name), name) for name in SECTIONS["experiment"]
                if name not in {"Figures", "Measurements"} and (s[name] or (not existing and name not in {"Context", "Caveats", "References"}))) + '</nav>'
            if s["Before delegation"] or not existing:
                body += section("Before delegation", messages_html(s["Before delegation"]))
            if s["Execution plan"] or not existing:
                body += section("Execution plan", md(s["Execution plan"]) or '<p class="empty">Not recorded</p>', "Agent · execution plan")
            if s["Amendments"] or not existing:
                body += section("Amendments", messages_html(s["Amendments"]))
            run_html = []
            for run in s["Runs"]:
                details = []
                for field in ("arm", "code", "model", "seed"):
                    if field in run:
                        details.append('<dt>%s</dt><dd>%s</dd>' % (field.title(), esc(str(run[field]))))
                for field in ("config", "data"):
                    if run.get(field):
                        details.append('<dt>%s</dt><dd><a href="%s">%s</a></dd>' % (
                            field.title(), esc(asset_url(run[field], base, project)), esc(run[field])))
                artifacts = "".join('<li><a href="%s">%s</a></li>' % (
                    esc(asset_url(a["path"], base, project)), esc(a["label"])) for a in run.get("artifacts", []))
                error = '<pre class="run-error">%s</pre>' % esc(run["error"]) if run.get("error") else ""
                run_html.append('<details class="run"><summary><span>%s</span><span class="research-status">%s</span></summary>'
                                '<dl class="kv">%s</dl><ul>%s</ul>%s</details>' % (
                                    esc(run["id"]), esc(run["status"].title()), "".join(details), artifacts, error))
            runs_section = section("Runs", "".join(run_html) or '<p class="empty">None yet</p>', "Agent · execution records")
            if not existing:
                body += runs_section
            body += section("Results", md(s["Results"]) or '<p class="empty">Not recorded</p>', "Agent · measured results")
            if s["Caveats"]:
                body += section("Caveats", md(s["Caveats"]))
            if existing and run_html:
                body += '<details class="saved-runs"><summary>Runs · %d</summary>%s</details>' % (len(run_html), runs_section)
            if s["References"]:
                body += section("References", md(s["References"]))
            for name in ("Your interpretation", "Next decision"):
                if s[name] or not existing:
                    body += section(name, messages_html(s[name]))
            related = [by_id[key] for key in refs(r, "related_questions")]
            if related:
                body += section("Related questions", record_rows(related, base))
            follow = [by_id[key.strip()] for key in r.get("follow_up", "").split(",") if key.strip()]
            if follow:
                body += section("Follow-up experiments", record_rows(follow, base))
        path = ("q/" if r["kind"] == "question" else "e/") + r["id"]
        page(path + ("/record" if r["kind"] == "experiment" else ""), r["title"], '<article class="prose research-record">' + body + '</article>')
        if r["kind"] == "experiment":
            report = '<h1>%s</h1><div class="report-links"><a href="%s">%s</a><a href="%srecord/">Research record</a></div>' % (
                esc(r["title"]), route(parent, base), esc(parent["title"]), route(r, base))
            report += research_figures.render(r, project, scratch, base, asset_url, md)
            page(path, r["title"], '<article class="prose result-report">' + report + '</article>')
        search.append({"t": r["title"], "u": route(r, base), "d": r["date"],
                       "s": r["kind"].title(), "g": r["id"] + " " + r["status"],
                       "x": r["raw"]})

    direction = next((r for r in records if r["kind"] == "direction"), None)
    body = page_top("Ceridwen", "Research")
    if direction:
        content = messages_html(direction["sections"]["Your words"])
        body += section("Research direction", content)
        search.append({"t": direction["title"], "u": base + "/#research-direction", "d": direction["date"],
                       "s": "Direction", "g": "research", "x": direction["raw"]})
    overview = []
    for q in questions:
        if q["status"] != "open":
            continue
        linked = [e for e in experiments if e["question"] == q["id"] or q["id"] in refs(e, "related_questions")]
        overview.append('<li><h3><a href="%s">%s</a></h3>%s<a class="attribution" href="%s">Experiments · %d</a></li>' % (
            route(q, base), esc(q["title"]), md(q["sections"]["Context"]), route(q, base), len(linked)))
    body += section("Research questions", '<ul class="question-overview">%s</ul>' % "".join(overview) if overview else '<p class="empty">None yet</p>')
    recorded = [e for e in experiments if e["status"] == "recorded"]
    if recorded:
        body += section("Existing results", record_rows(recorded[:6], base) + '<p><a href="%s/experiments/">All experiments · %d</a></p>' % (base, len(experiments)))
    body += section("Results awaiting interpretation", record_rows([e for e in experiments if e["status"] == "results-ready"], base))
    body += section("Ongoing experiments", record_rows([e for e in experiments if e["status"] in {"planned", "running"}], base))
    body += '<div class="foot"><a href="%s/questions/">All questions</a><a href="%s/experiments/">All experiments</a></div>' % (base, base)
    page("", "Research", '<div class="prose">' + body + '</div>')

    for name, rows, states in (("Questions", questions, QUESTION_STATES), ("Experiments", experiments, EXPERIMENT_STATES)):
        control = '<label class="status-filter">Status <select id="research-status"><option value="">All statuses</option>'
        control += "".join('<option value="%s">%s</option>' % item for item in states.items()) + '</select></label>'
        body = page_top("Research", name) + control + record_rows(rows, base)
        body += '<p id="filter-empty" class="empty" hidden>No matches</p><script src="%s/research.js" defer></script>' % base
        page(name.lower(), name, '<div class="prose">' + body + '</div>')

    reference = [n for n in notes if n["section"] not in {"Analyses", "Paper drafts", "Archive"} and n["status"] != "obsolete"]
    earlier = [n for n in notes if n not in reference]
    for path, title, rows in (("reference", "Reference", reference), ("earlier", "Source notes", earlier)):
        body = page_top("Library", title)
        if path == "earlier":
            body += '<p><a href="%s/themes/">Earlier experiment boards</a></p>' % base
        body += builder.feed_rows(rows, base) if rows else '<p class="empty">None yet</p>'
        page(path, title, '<div class="prose">' + body + '</div>')
    (scratch / "research.js").write_text(FILTER_JS, encoding="utf-8")
    (scratch / "figures.js").write_text(research_figures.JS, encoding="utf-8")
    research_figures.notebook.cache_clear()
    return search


FILTER_JS = """(() => {
  const filter = document.getElementById('research-status');
  const rows = [...document.querySelectorAll('.research-row')];
  if (!filter) return;
  const update = () => {
    rows.forEach(row => { row.hidden = !!filter.value && row.dataset.status !== filter.value; });
    document.getElementById('filter-empty').hidden = rows.some(row => !row.hidden) || !rows.length;
  };
  filter.addEventListener('change', update);
  update();
})();
"""

CSS = """
.research-section{margin-top:30px}
.research-section h2{font-size:1.25rem;border-top:1px solid var(--rule);padding-top:18px;margin-bottom:14px}
.user-message{margin:14px 0 24px}
.user-message figcaption{font-family:system-ui,sans-serif;font-size:.75rem;color:var(--ink-2);display:flex;gap:12px;flex-wrap:wrap}
.edited-message{white-space:pre-wrap;overflow-wrap:anywhere}
.original-message summary{font-family:system-ui,sans-serif;font-size:.8rem;color:var(--ink-2);cursor:pointer}
.research-links{margin:20px 0}
.question-overview{list-style:none;padding:0}
.question-overview li{padding:12px 0;border-bottom:1px solid var(--rule)}
.question-overview h3{margin:0;font-size:1.1rem}
.question-overview p{font-size:.95rem;margin:8px 0}
.saved-runs{margin-top:25px}
.saved-runs>summary{cursor:pointer;font-family:system-ui,sans-serif;font-size:.9rem}
.verbatim{white-space:pre-wrap;overflow-wrap:anywhere;border-left:2px solid var(--accent);margin:10px 0 0;padding:4px 0 4px 18px;font-size:1.1rem}
.research-list{padding:0;margin:0;list-style:none}
.research-row{display:grid;grid-template-columns:90px minmax(0,1fr) auto;gap:14px;align-items:start;padding:16px 0;border-bottom:1px solid var(--rule)}
.research-row[hidden],#filter-empty[hidden]{display:none}
.research-row .t{font-size:1.08rem;color:var(--ink)}
.record-id{display:block;font-family:ui-monospace,monospace;font-size:.72rem;color:var(--ink-2);overflow-wrap:anywhere}
.research-status{display:inline-block;font-family:system-ui,sans-serif;font-size:.72rem;border:1px solid var(--rule);border-radius:3px;padding:3px 7px;white-space:nowrap;color:var(--ink-2)}
.research-status.results-ready{border-color:var(--accent);color:var(--accent)}
.research-status.running{border-color:var(--accent-2);color:var(--accent-2)}
.record-meta{display:flex;align-items:center;gap:14px;margin:4px 0 18px}
.record-sections{display:flex;flex-wrap:wrap;gap:8px 18px;padding:14px 0;border-block:1px solid var(--rule);font-family:system-ui,sans-serif;font-size:.78rem}
.attribution,.empty{font-family:system-ui,sans-serif;font-size:.8rem;color:var(--ink-2)}
.run{margin:10px 0;border:1px solid var(--rule);padding:12px 16px}
.run summary{font-family:ui-monospace,monospace;font-size:.8rem;cursor:pointer}
.run summary .research-status{margin-left:12px}
.run dd,.run a,.research-record p,.research-record li{overflow-wrap:anywhere}
.run-error{white-space:pre-wrap}
.status-filter{display:flex;align-items:center;gap:12px;margin:20px 0;font-family:system-ui,sans-serif;font-size:.8rem}
.status-filter select{background:var(--paper);color:var(--ink);border:1px solid var(--rule);border-radius:3px;padding:8px;font:inherit}
a:focus-visible,select:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
@media(max-width:760px){.research-row{grid-template-columns:1fr auto;gap:6px 12px}.research-row .d{grid-column:1/-1}.verbatim{font-size:1rem}.record-sections{line-height:1.8}}
@media print{nav.side,.record-sections,.status-filter{display:none}.frame{display:block}.run{break-inside:avoid}.verbatim{color:#000}}
"""
CSS += research_figures.CSS
