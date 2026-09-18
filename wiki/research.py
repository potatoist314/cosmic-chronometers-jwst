"""Research records, existing evidence and meaning-preserving message display."""

import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
import research_figures
import activity


EXPERIMENT_STATES = {
    "planned": "Planned", "running": "Running", "results-ready": "Results ready",
    "reviewed": "Reviewed", "stopped": "Stopped", "recorded": "Recorded",
}
QUESTION_STATES = {"open": "Open", "paused": "Paused", "answered": "Answered"}
RUN_STATES = {"planned", "running", "complete", "failed"}
SECTIONS = {
    "direction": ("Your words", "Roadmap", "Amendments", "References"),
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
        if name in MESSAGE_SECTIONS or name in {"Runs", "Figures", "Roadmap"}:
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
            tasks = s["Roadmap"]
            task_ids = [task.get("id") for task in tasks]
            seen_tasks = set()
            for task in tasks:
                task_id = task.get("id")
                if not isinstance(task_id, str) or not ID.fullmatch(task_id):
                    fail("roadmap task id must use lowercase letters, digits and hyphens")
                elif task_id in seen_tasks:
                    fail("roadmap task ids must be unique")
                else:
                    seen_tasks.add(task_id)
                if not isinstance(task.get("title"), str) or not task["title"].strip():
                    fail("roadmap task requires a title")
                priority = task.get("priority")
                if priority is not None and (type(priority) is not int or not 1 <= priority <= 10):
                    fail("roadmap priority must be an integer from 1 to 10, or null")
                evidence(task.get("source"))
                for field in ("details", "effort"):
                    if field in task and not isinstance(task[field], str):
                        fail("roadmap " + field + " must be a string")
                dependencies = task.get("depends_on", [])
                if not isinstance(dependencies, list) or any(
                    not isinstance(dep, str) or dep not in task_ids or dep == task_id
                    for dep in dependencies
                ):
                    fail("roadmap dependencies must reference other task ids")
            for match in LINK.finditer(s["References"]):
                evidence(match[1] or match[2])
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


def roadmap_html(tasks, base, project, states=None, resolved=False):
    """Render the full user-ranked task list on Home and its legacy route."""
    by_id = {task["id"]: task for task in tasks}
    states = states or {}
    rows = []
    for task in sorted(tasks, key=lambda task: -(task.get("priority") or 0)):
        if (states.get(task["id"], "open") == "resolved") != resolved:
            continue
        priority = task.get("priority")
        score = str(priority) + "/10" if priority is not None else "Unscored"
        details = '<p>%s</p>' % esc(task["details"]) if task.get("details") else ""
        dependency = ", ".join('<a href="%s/#%s">%s</a>' % (
            base, esc(dep), esc(by_id[dep]["title"])) for dep in task.get("depends_on", []))
        constraints = ('<p><span class="attribution">After:</span> %s</p>' % dependency if dependency else "")
        if task.get("effort"):
            constraints += '<p><span class="attribution">Difficulty:</span> %s</p>' % esc(task["effort"])
        # The tick box under the score resolves or reopens the task from Home without a reload.
        done = ('<label class="roadmap-done"><input type="checkbox"%s><span class="visually-hidden">Resolved</span></label>'
                % (" checked" if resolved else ""))
        rows.append('<tr id="%s" data-priority-id="%s"><td class="roadmap-score">%s%s</td><td><a href="%s/p/%s/">%s</a>%s%s <a class="roadmap-source" href="%s">Source</a></td></tr>' % (
            esc(task["id"]), esc(task["id"]), score, done, base, esc(task["id"]),
            esc(task["title"]), details, constraints, esc(asset_url(task["source"], base, project))))
    empty = '<p class="empty">No priorities recorded</p>' if not rows else ""
    return (empty + '<p class="roadmap-status" role="status"></p><table class="roadmap"><caption>Research priorities · 10 highest</caption>'
            '<thead><tr><th scope="col">Priority</th><th scope="col">Task</th></tr></thead>'
            '<tbody>%s</tbody></table>' % "".join(rows))


def note_backlinks(slug, records, base):
    linked = [r for r in records if slug in refs(r, "source_notes")]
    if not linked:
        return ""
    return '<section class="research-links"><h2>Research entries</h2>%s</section>' % record_rows(linked, base)


def write_pages(records, notes, scratch, base, builder):
    """Build a shared question and experiment structure, preserving source routes."""
    project = builder.PROJECT
    research_dir = getattr(builder, "RESEARCH", project / "wiki/research")
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

    def section(title, content):
        return '<section class="research-section"><h2 id="%s">%s</h2>%s</section>' % (
            builder.slugify(title), esc(title), content)

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
        if s["Context"]:
            body += section("Context", md(s["Context"]))
        if r["kind"] == "question":
            if s["Your words"] or not existing:
                body += section("Your reasoning", messages_html(s["Your words"]))
            if s["References"]:
                body += section("References", md(s["References"]))
            body += section("Experiments", record_rows([e for e in experiments if e["question"] == r["id"] or r["id"] in refs(e, "related_questions")], base))
            if s["Decisions"] or not existing:
                body += section("Decisions", messages_html(s["Decisions"]))
            entries = activity.read(research_dir, "question", r["id"])
            body += activity.editor_html("question", r["id"], entries, base, project)
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
                body += section("Execution plan", md(s["Execution plan"]) or '<p class="empty">Not recorded</p>')
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
            runs_section = section("Runs", "".join(run_html) or '<p class="empty">None yet</p>')
            if not existing:
                body += runs_section
            body += section("Results", md(s["Results"]) or '<p class="empty">Not recorded</p>')
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
            report += research_figures.render(r, project, scratch, base, asset_url, md, builder.math_text)
            page(path, r["title"], '<article class="prose result-report">' + report + '</article>')
        search.append({"t": r["title"], "u": route(r, base), "d": r["date"],
                       "s": r["kind"].title(), "g": r["id"] + " " + r["status"],
                       "x": r["raw"] + " " + (" ".join(e.get("text", "") for e in activity.read(research_dir, "question", r["id"])) if r["kind"] == "question" else "")})

    direction = next((r for r in records if r["kind"] == "direction"), None)
    tasks = direction["sections"]["Roadmap"] if direction else []
    states = {task["id"]: activity.state(activity.read(research_dir, "priority", task["id"])) for task in tasks}
    for task in tasks:
        entries = activity.read(research_dir, "priority", task["id"])
        content = page_top("Priority", task["title"])
        score = str(task["priority"]) + "/10" if task.get("priority") is not None else "Unscored"
        content += '<p>%s · <a href="%s">Original source</a></p>' % (score, esc(asset_url(task["source"], base, project)))
        if task.get("details"):
            content += '<p>%s</p>' % esc(task["details"])
        if task.get("effort"):
            content += '<p>Difficulty: %s</p>' % esc(task["effort"])
        if task.get("depends_on"):
            content += '<p>After: ' + ", ".join('<a href="%s/p/%s/">%s</a>' % (
                base, esc(dep), esc(next(t["title"] for t in tasks if t["id"] == dep))) for dep in task["depends_on"]) + '</p>'
        content += activity.editor_html("priority", task["id"], entries, base, project)
        page("p/" + task["id"], task["title"], '<article class="prose research-record">' + content + '</article>')
        search.append({"t": task["title"], "u": base + "/p/" + task["id"] + "/", "d": direction["date"],
                       "s": "Priority", "g": states[task["id"]],
                       "x": task.get("details", "") + " " + " ".join(e.get("text", "") for e in entries)})
    body = '<h1>Home</h1>' + section("Current priorities", roadmap_html(tasks, base, project, states))
    body += '<details class="resolved-priorities"><summary>Resolved</summary>' + roadmap_html(tasks, base, project, states, True) + '</details>'
    body += '<script type="module" src="%s/activity.js"></script>' % base
    body += section("Planned and running", record_rows([e for e in experiments if e["status"] in {"planned", "running"}], base))
    content = ""
    if direction:
        s = direction["sections"]
        content += section("Research direction", messages_html(s["Your words"]))
        if s["References"]:
            content += section("Meeting notes", md(s["References"]))
        if s["Amendments"]:
            content += '<section id="roadmap-amendments"><h2>Decisions and original wording</h2>%s</section>' % messages_html(s["Amendments"])
        search.append({"t": "Home", "u": base + "/", "d": direction["date"],
                       "s": "Home", "g": "research priorities roadmap direction", "x": direction["raw"]})
    content += section("Questions", record_rows(questions, base))
    body += '<details class="research-history"><summary>Research record</summary>%s</details>' % content
    home = '<article class="prose research-record">' + body + '</article>'
    for path in ("", "roadmap"):
        page(path, "Home", home)

    saved = [e for e in experiments if e["sections"]["Figures"] or e["sections"]["Measurements"]]
    body = '<h1>Results</h1>' + record_rows(saved, base)
    other = [e for e in experiments if e not in saved]
    body += '<details class="research-history"><summary>Other experiment records</summary>%s</details>' % record_rows(other, base)
    analyses = [n for n in notes if n["section"] == "Analyses"]
    body += '<details class="research-history"><summary>Earlier analyses and boards</summary>%s<p><a href="%s/themes/">Experiment boards</a></p></details>' % (
        builder.feed_rows(analyses, base), base)
    page("results", "Results", '<div class="prose">' + body + '</div>')

    for name, rows, states in (("Questions", questions, QUESTION_STATES), ("Experiments", experiments, EXPERIMENT_STATES)):
        control = '<label class="status-filter">Status <select id="research-status"><option value="">All statuses</option>'
        control += "".join('<option value="%s">%s</option>' % item for item in states.items()) + '</select></label>'
        body = page_top("Research", name) + control + record_rows(rows, base)
        body += '<p id="filter-empty" class="empty" hidden>No matches</p><script src="%s/research.js" defer></script>' % base
        page(name.lower(), name, '<div class="prose">' + body + '</div>')

    for name in ("Meetings", "Masking"):
        rows = [n for n in notes if n["section"] == name]
        body = '<h1>%s</h1>' % name
        body += builder.feed_rows(rows, base) if rows else '<p class="empty">None yet</p>'
        page(name.lower(), name, '<div class="prose">' + body + '</div>')

    papers = [n for n in notes if n["section"] == "Paper drafts"]
    body = '<h1>Papers</h1>' + section("Reading notes", builder.feed_rows(papers, base) if papers else '<p class="empty">None yet</p>')
    catalog = project / "papers/README.md"
    pdfs = []
    if catalog.is_file():
        for filename, citation in re.findall(r"^\| `([^`]+\.pdf)` \| ([^|]+) \|", catalog.read_text(encoding="utf-8"), re.M):
            path = project / "papers" / filename
            if not path.is_file():
                # Older catalog rows predate the chronometer subdirectory.
                matches = list((project / "papers").rglob(Path(filename).name))
                if len(matches) != 1:
                    raise ValueError("paper catalog entry has no unique local PDF: " + filename)
                path = matches[0]
            url = asset_url(quote(path.relative_to(project).as_posix()), base, project)
            title = Path(filename).stem
            citation = html.unescape(citation.strip())
            pdfs.append('<li><a href="%s">%s</a><p class="attribution">%s</p></li>' % (esc(url), esc(title), esc(citation)))
            search.append({"t": title, "u": url, "d": "", "s": "Paper", "g": citation, "x": filename + " " + citation})
    body += section("Local PDFs", '<ul class="paper-list">%s</ul>' % "".join(pdfs) if pdfs else '<p class="empty">None yet</p>')
    if catalog.is_file():
        body += '<p><a href="%s">Original catalog</a></p>' % esc(asset_url("papers/README.md", base, project))
    page("papers", "Papers", '<div class="prose">' + body + '</div>')

    literature = [n for n in notes if n["section"] == "Literature" and n["status"] != "obsolete"]
    body = '<h1>Model</h1>'
    for n in literature:
        body += '<section class="research-section">%s</section>' % builder.markdown(n["body"], base)
        search.append({"t": n["title"], "u": base + "/model/", "d": n["date"],
                       "s": "Model", "g": " ".join(n["tags"]), "x": n["body"]})
    if not literature:
        body += '<p class="empty">None yet</p>'
    # /literature/ is the earlier address of the same page.
    for path in ("model", "literature"):
        page(path, "Model", '<div class="prose">' + body + '</div>')

    body = '<h1>Code &amp; guides</h1>'
    default_model = next((n for n in notes if n["slug"] == "default-fit-parameters"
                          and n["status"] != "obsolete" and not n["superseded_by"]), None)
    if default_model:
        body += '<section class="default-model"><h2><a href="%s/n/%s/">%s</a></h2>%s</section>' % (
            base, default_model["slug"], esc(default_model["title"]),
            builder.markdown(default_model["body"], base))
    for name, label in (("Codebase", "Code"), ("Notebooks", "Notebooks"), ("Guides", "Guides")):
        rows = [n for n in notes if n["section"] == name and n["status"] != "obsolete" and not n["superseded_by"] and n is not default_model]
        body += section(label, builder.feed_rows(rows, base) if rows else '<p class="empty">None yet</p>')
    older = [n for n in notes if n["section"] == "Archive" or (
        n["section"] in {"Codebase", "Notebooks", "Guides"} and (n["status"] == "obsolete" or n["superseded_by"]))]
    body += '<details class="research-history"><summary>Earlier documentation and history</summary>%s<p><a href="%s/log/">Note history</a></p></details>' % (
        builder.feed_rows(older, base), base)
    page("code", "Code & guides", '<div class="prose">' + body + '</div>')

    masking = [n for n in notes if n["section"] == "Masking"]
    reference = [n for n in notes if n["section"] not in {"Analyses", "Masking", "Paper drafts", "Literature", "Archive"} and n["status"] != "obsolete"]
    earlier = [n for n in notes if n not in reference and n not in masking]
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
.default-model{margin:28px 0 42px}
.default-model>h2{margin:0 0 8px;font-size:1.55rem}
.default-model>h2 a{color:var(--ink)}
.default-model-meta,.default-model-sources{font-family:system-ui,sans-serif;color:var(--ink-2);font-size:.76rem;line-height:1.7;max-width:none}
.default-model-sources{margin:18px 0 0}
.default-parameter-table{width:100%;table-layout:fixed;font-size:.95rem;margin:18px 0 28px;line-height:1.5}
.default-parameter-table th,.default-parameter-table td{padding:14px 14px 14px 0;overflow-wrap:anywhere}
.default-parameter-table th:last-child,.default-parameter-table td:last-child{padding-right:0}
.default-parameter-table thead th:nth-child(1){width:28%}
.default-parameter-table thead th:nth-child(2){width:28%}
.default-parameter-table tbody th{font:inherit;font-weight:500;letter-spacing:0;text-transform:none;color:var(--ink)}
.default-parameter-table th code{display:block;font-size:.7rem;line-height:1.5;font-weight:400;color:var(--ink-2);margin-top:5px}
.default-parameter-table small{display:block;color:var(--ink-2);font-size:.83rem;margin-top:5px}
.default-fixed-table thead th:nth-child(2){width:auto}
@media(max-width:760px){
  .default-parameter-table,.default-parameter-table tbody,.default-parameter-table tr,.default-parameter-table th,.default-parameter-table td{display:block;min-width:0;width:100%}
  .default-parameter-table thead{position:absolute;width:1px;height:1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
  .default-parameter-table tr{padding:16px 0;border-bottom:1px solid var(--rule)}
  .default-parameter-table tbody th,.default-parameter-table td{border:0;padding:0}
  .default-parameter-table td{margin-top:12px}
  .default-parameter-table td::before{content:attr(data-label);display:block;font-family:system-ui,sans-serif;font-size:.7rem;color:var(--ink-2);margin-bottom:3px}
  .default-parameter-table th code{margin-top:2px}
}
.model-group{margin:10px 0 34px;max-width:none}
.model-row{display:block;margin:0;padding:0;border:0;border-bottom:1px solid var(--rule)}
details.model-row>summary,div.model-row{display:grid;grid-template-columns:minmax(0,11rem) minmax(0,1fr) minmax(0,12rem) .8rem;column-gap:18px;align-items:baseline;padding:9px 0;margin:0;font:inherit;font-size:.93rem;line-height:1.45;letter-spacing:0;text-transform:none;color:var(--ink);list-style:none}
details.model-row>summary{cursor:pointer}
details.model-row>summary::-webkit-details-marker{display:none}
details.model-row>summary:hover .model-s,details.model-row[open]>summary .model-s{color:var(--accent-2)}
details.model-row[open]>summary{margin-bottom:0}
.model-s{font-weight:500}
.model-v{overflow-wrap:anywhere}
.model-w{color:var(--ink-2);font-size:.85rem}
.model-f{text-align:right}
.model-flag{color:var(--accent);font-weight:700}
.model-tag{font-family:system-ui,sans-serif;font-size:.62rem;font-weight:400;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);margin-left:6px;white-space:nowrap}
.model-row>ul{list-style:none;margin:0;padding:2px 0 12px calc(11rem + 18px);font-size:.88rem;line-height:1.5;color:var(--ink-2);max-width:none}
.model-row>ul li{margin:3px 0;padding:0 0 0 4.85rem;text-indent:-4.85rem}
.model-row>ul li .katex,.model-row>ul li code{text-indent:0}
.model-row>ul i{font-style:normal;font-family:system-ui,sans-serif;font-size:.64rem;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);display:inline-block;min-width:4.6rem;text-indent:0}
@media(max-width:760px){
  details.model-row>summary,div.model-row{grid-template-columns:minmax(0,1fr) .8rem;row-gap:2px}
  .model-s,.model-v,.model-w{grid-column:1}
  .model-f{grid-column:2;grid-row:1}
  .model-row>ul{padding-left:0}
}
.roadmap{width:100%;table-layout:fixed;border-collapse:collapse}
.roadmap caption{text-align:left;font-family:system-ui,sans-serif;font-size:.8rem;color:var(--ink-2);padding:8px 0}
.roadmap th,.roadmap td{text-align:left;vertical-align:top;padding:12px 8px;border-bottom:1px solid var(--rule);overflow-wrap:anywhere}
.roadmap th:first-child{width:96px;white-space:nowrap}
.roadmap-score{font-variant-numeric:tabular-nums;font-weight:600;white-space:nowrap}
.roadmap td p{margin:6px 0 0;font-size:.9rem}
.research-section{margin-top:30px}
.research-section h2{font-size:1.25rem;border-top:1px solid var(--rule);padding-top:18px;margin-bottom:14px}
.research-history{margin-top:30px}
.research-history>summary{cursor:pointer}
.paper-list{list-style:none;padding:0}
.paper-list li{padding:14px 0;border-bottom:1px solid var(--rule);overflow-wrap:anywhere}
.paper-list p{margin:6px 0 0}
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
