"""Check-in pages: one page per meeting, figures first.

A check-in source is `research/checkins/<date>.md`. Draft one from the records:

    python3 wiki/checkins.py 2026-09-21 --since 2026-09-17

The draft lists `experiments` in its frontmatter. Each one shows its title, its first
figure with the record's caption, and at most three rows of its first Measurements table.
Reorder or delete IDs to curate the page.

A source can also carry sections of hand-written items. `## Your words` holds the
original messages. Every other section is a fenced JSON array of items:
`text`, optional `points`, optional `link`, and one of `figure` (`<experiment>:<index>`),
`image` (`path`, or `notebook`, `cell`, `output`) or `code` (`notebook`, `cell`, `from`, `until`).
`research.write_pages` renders the pages during the wiki build.
"""
import argparse
import html
import json
import re
import sys
from datetime import date as Date
from pathlib import Path

import research
import research_figures

esc = html.escape
RESULT_STATES = {"results-ready", "reviewed"}
BULLETS = 3
UNIT = re.compile(r"\s+\[([^\]]+)\]\s*$")
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def parse(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n") or "\n---\n" not in raw[4:]:
        raise ValueError("missing frontmatter")
    head, body = raw[4:].split("\n---\n", 1)
    checkin = {"path": path, "sections": {}}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            checkin[key.strip()] = value.strip()
    if checkin.get("kind") != "checkin" or checkin.get("date") != path.stem:
        raise ValueError("kind must be checkin and date must match the file name")
    Date.fromisoformat(checkin["date"])
    checkin["experiments"] = research.refs(checkin, "experiments")
    for name, block in re.findall(r"^## (.+?)\n+```json\s*\n(.*?)\n```", body, re.M | re.S):
        checkin["sections"][name.strip()] = json.loads(block)
    return checkin


def load(directory):
    return [parse(path) for path in sorted((directory / "checkins").glob("*.md"))]


def table_rows(measurements):
    """Rows of the first Markdown table, without its header: (label, [values])."""
    rows = []
    for line in measurements.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            rows.append((cells[0], [c for c in cells[1:] if c]))
        elif rows:
            break
    return rows[2:]


def bullets(record):
    """First rows whose label occurs in Results; otherwise whose first number does."""
    rows = [r for r in table_rows(record["sections"]["Measurements"]) if r[1]]
    results = record["sections"]["Results"]
    chosen = [r for r in rows if UNIT.sub("", r[0]) in results]
    if not chosen:
        numbers = set(NUMBER.findall(results))
        chosen = [r for r in rows if (NUMBER.findall(r[1][0]) or [None])[0] in numbers]
    return chosen[:BULLETS]


def draft(directory, day, since):
    """Experiments with results dated from `since` that no earlier check-in lists."""
    records, faults = research.load(directory)
    if faults:
        raise ValueError("\n".join(faults))
    listed = {e for c in load(directory) if c["date"] < day for e in c["experiments"]}
    chosen = sorted((r["date"], r["id"]) for r in records
                    if r["kind"] == "experiment" and r["status"] in RESULT_STATES
                    and since <= r["date"] <= day and r["id"] not in listed
                    and (r["sections"]["Figures"] or r["sections"]["Measurements"]))
    return "---\nkind: checkin\ndate: %s\nsince: %s\nexperiments: %s\n---\n" % (
        day, since, ", ".join(i for _, i in chosen))


def long_date(day):
    d = Date.fromisoformat(day)
    return "%d %s" % (d.day, d.strftime("%B %Y"))


def rows_html(checkins, base):
    return '<ul class="feed">%s</ul>' % "".join(
        '<li><span class="d">%s</span><span><a class="t" href="%s/checkins/%s/">Check-in, %s</a></span></li>'
        % (esc(c["date"]), base, esc(c["date"]), esc(long_date(c["date"])))
        for c in reversed(checkins))


def inline(text):
    """Escaped text; KaTeX renders the explicit TeX spans in the browser."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(text, quote=False))


def fact(label, values):
    unit = UNIT.search(label)
    cells = [inline(re.sub(r"-(?=\d)", "−", v)) for v in values]
    if unit:
        cells[-1] += ' <span class="u">%s</span>' % inline(unit[1])
    return '<li><span class="q">%s</span> <span class="vals">%s</span></li>' % (
        inline(UNIT.sub("", label)),
        ' <span class="ar">→</span> '.join('<span class="v">%s</span>' % c for c in cells))


def snippet(project, code):
    """Lines of one notebook cell, from the line starting `from` up to the one starting `until`."""
    cell = json.loads((project / code["notebook"]).read_text(encoding="utf-8"))["cells"][code["cell"]]
    lines = "".join(cell["source"]).splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(code.get("from", "")))
    stop = next((i for i, line in enumerate(lines) if i > start and line.startswith(code["until"])),
                len(lines)) if code.get("until") else len(lines)
    return "\n".join(lines[start:stop]).rstrip()


def item_html(item, by_id, project, scratch, base, builder):
    media = ""
    if item.get("figure") or item.get("image"):
        figure = item.get("image")
        if item.get("figure"):
            experiment, index = item["figure"].rsplit(":", 1)
            figure = by_id[experiment]["sections"]["Figures"][int(index)]
        src = research_figures.image_url(figure, project, scratch, base, research.asset_url)
        media = '<figure><a href="%s"><img src="%s" alt="%s" loading="lazy"></a></figure>' % (
            esc(src), esc(src), esc(builder.math_text(item["text"])))
    elif item.get("code"):
        media = builder.markdown("```python\n%s\n```" % snippet(project, item["code"]), base)
    text = inline(item["text"])
    if item.get("link"):
        text = '<a href="%s">%s</a>' % (esc(research.asset_url(item["link"], base, project)), text)
    facts = '<ul class="facts"><li class="lead">%s</li>%s</ul>' % (
        text, "".join("<li>%s</li>" % inline(point) for point in item.get("points", [])))
    if not media:
        return '<div class="item nomedia">%s</div>' % facts
    return '<div class="item pair%s">%s%s</div>' % (" code" if item.get("code") else "", media, facts)


def write_pages(records, scratch, base, builder, rail):
    project = builder.PROJECT
    by_id = {r["id"]: r for r in records if r["kind"] == "experiment"}
    checkins = load(getattr(builder, "RESEARCH", project / "wiki/research"))
    for checkin in checkins:
        title = "Check-in, " + long_date(checkin["date"])
        body = '<header class="ci-head"><h1>%s</h1><a class="brand" href="%s/">%s</a></header>' % (
            esc(title), base, esc(builder.SITE_NAME))
        for position, experiment in enumerate(checkin["experiments"]):
            if experiment not in by_id:
                raise ValueError("%s: unknown experiment %s" % (checkin["path"], experiment))
            record = by_id[experiment]
            figures = record["sections"]["Figures"]
            facts = '<ul class="facts">%s</ul>' % "".join(
                fact(label, values) for label, values in bullets(record))
            heading = '<h2><a href="%s">%s</a></h2>' % (research.route(record, base), esc(record["title"]))
            if figures:
                src = research_figures.image_url(figures[0], project, scratch, base, research.asset_url)
                body += ('<section class="exp%s">%s<div class="pair"><figure><img src="%s" alt="%s"%s>'
                         '<figcaption>%s</figcaption></figure>%s</div></section>') % (
                    "" if position else " first", heading, esc(src),
                    esc(builder.math_text(figures[0]["caption"])),
                    ' loading="lazy"' if position else "",
                    inline(figures[0]["caption"]), facts)
            else:
                body += '<section class="exp nofig">%s%s</section>' % (heading, facts)
        for name, items in checkin["sections"].items():
            if name != "Your words":
                body += '<section class="exp items"><h2>%s</h2>%s</section>' % (esc(name), "".join(
                    item_html(item, by_id, project, scratch, base, builder) for item in items))
        if checkin["sections"].get("Your words"):
            body += '<details class="research-history"><summary>Research record</summary>%s</details>' % (
                research.messages_html(checkin["sections"]["Your words"]))
        dest = scratch / "checkins" / checkin["date"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(builder.shell(title + " · " + builder.SITE_NAME, base,
                                      '<article class="prose checkin">%s</article>' % body, rail,
                                      extra_head="<style>%s</style>\n" % CSS), encoding="utf-8")
    return checkins


CSS = """
.frame{display:block;max-width:1400px}
nav.side{display:none}
main{max-width:none;padding:0 48px 60px}
.ci-head{height:64px;display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding-top:20px}
.ci-head h1{font-size:1.45rem;line-height:1.2;margin:0;letter-spacing:-.01em}
.ci-head .brand{font-size:.95rem;font-weight:400;color:var(--ink-2)}
.exp{border-top:1px solid var(--rule);padding:16px 0 30px}
.exp h2{font-size:1.45rem;font-weight:400;line-height:1.2;margin:0 0 12px;letter-spacing:-.01em}
.exp h2 a{color:var(--ink)}
.exp h2 a:hover{color:var(--accent)}
.exp figure{margin:0;max-width:none}
.exp figure img{display:block;width:auto;height:auto;max-width:100%;max-height:calc(100vh - 150px);background:#fff;border:1px solid var(--rule)}
.exp.first figure img{max-height:calc(100vh - 214px)}
.exp figcaption{font-size:.9rem;color:var(--ink-2);margin-top:8px;max-width:none}
.pair{display:grid;grid-template-columns:minmax(0,1fr) 250px;column-gap:44px;align-items:start}
.pair figure{display:table}
.pair figcaption{display:table-caption;caption-side:bottom}
.facts{list-style:none;margin:0;padding:0;font-size:1.08rem;line-height:1.5;font-variant-numeric:tabular-nums}
.facts li{padding:0 0 14px}
.facts .q,.facts .vals{display:block}
.facts .q,.facts .u{color:var(--ink-2)}
.facts .v{white-space:nowrap}
.pair .facts .v{display:block}
.pair .facts .ar{display:none}
.pair .facts .v~.v::before{content:"\\2192\\00a0";color:var(--ink-3)}
.nofig .facts li{padding-bottom:8px}
.checkin .facts li{max-width:none;margin-bottom:0}
.items h2{margin-bottom:0}
.item{padding:20px 0 28px}
.item+.item{border-top:1px solid var(--rule)}
.items .item:last-child{padding-bottom:0}
.items .pair{grid-template-columns:minmax(0,1fr) 310px}
.item figure a{display:block}
.item figure img{max-height:calc(100vh - 60px)}
.item pre{margin:0;max-width:none;overflow-x:auto;font-size:.72rem;line-height:1.55}
.item .facts{font-variant-numeric:normal}
.item .facts li{position:relative;padding:0 0 8px 1em;font-size:1rem;line-height:1.45;color:var(--ink-2)}
.item .facts li::before{content:"";position:absolute;left:.1em;top:.62em;width:4px;height:4px;border-radius:50%;background:var(--ink-3)}
.item .facts li.lead{padding:0 0 10px;font-size:1.15rem;line-height:1.35;color:var(--ink)}
.item .facts li.lead::before{content:none}
.item .facts li:last-child{padding-bottom:0}
.nomedia .facts{max-width:60ch}
.checkin .research-history{margin-top:0;padding-top:12px}
a:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:4px}
@media(max-width:1000px){
  .pair{display:block}
  .pair .facts{margin-top:12px}
  .items .pair{display:flex;flex-direction:column-reverse;gap:14px}
  .items .pair .facts{margin-top:0;max-width:60ch}
  .items .pair>pre,.items .pair>figure{max-width:100%}
}
@media(max-width:760px){main{padding:0 20px 48px}.ci-head{height:auto;padding:18px 0 14px;flex-wrap:wrap}}
"""


def main(argv):
    parser = argparse.ArgumentParser(description="Draft research/checkins/<date>.md")
    parser.add_argument("date")
    parser.add_argument("--since", help="default: the previous check-in's date")
    args = parser.parse_args(argv)
    directory = Path(__file__).resolve().parent / "research"
    since = args.since or max(c["date"] for c in load(directory) if c["date"] < args.date)
    path = directory / "checkins" / (args.date + ".md")
    if path.exists():
        sys.exit("%s exists" % path)
    path.parent.mkdir(exist_ok=True)
    path.write_text(draft(directory, args.date, since), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
