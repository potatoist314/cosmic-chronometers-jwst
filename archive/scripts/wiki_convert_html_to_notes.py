#!/usr/bin/env python3
"""One-time conversion of the old HTML wiki into `wiki/notes/*.md`.

Reads the preserved pages under `wiki/_old/` and writes one Markdown note per
page. Nothing is summarised or rewritten: headings, paragraphs, lists, tables,
code, and figures cross over as they stand. The per-note metadata below is
bookkeeping (title, date, section, tags, job id), taken from each page's
`wiki-updated` meta tag and from the Hermes bridge log that recorded which card
produced the page.

Run once:

    /usr/bin/python3 scripts/wiki_convert_html_to_notes.py

Standard library only.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OLD = WIKI / "_old"
NOTES = WIKI / "notes"

# source page -> (slug, title, section, tags, job card, status)
# `job` is the Hermes card whose worker produced the page, from logs/bridge.log.
# An empty job means the page predates the bridge or came from local work.
PAGES = [
    ("overview.html", "overview", "Ceridwen project overview",
     "Guides", ["ceridwen", "overview"], "", ""),
    ("guides/reading-order.html", "reading-order", "Reading order",
     "Guides", ["ceridwen", "reading"], "", ""),
    ("guides/python-patterns.html", "python-patterns", "Python patterns",
     "Guides", ["python", "jax"], "", ""),
    ("guides/vast-ai-gpu-workflow.html", "vast-ai-gpu-workflow", "Vast.ai GPU workflow",
     "Guides", ["gpu", "vast-ai", "ceridwen"], "t_2fc31190", ""),
    ("guides/modal-gpu-workflow.html", "modal-gpu-workflow", "Modal GPU workflow",
     "Guides", ["gpu", "modal", "ceridwen"], "", ""),

    ("analyses/dr2-quiescent-sample.html", "dr2-quiescent-sample", "DR2 quiescent sample",
     "Analyses", ["dr2-quiescent-sample", "ceridwen", "figures"], "t_d0d3a321", ""),
    ("analyses/ceridwen-results.html", "ceridwen-results", "Ceridwen common results board",
     "Analyses", ["ceridwen", "results"], "t_44b5da5c", ""),
    ("analyses/absorption-line-mask.html", "absorption-line-mask", "Absorption-line pixel mask",
     "Analyses", ["absorption-mask", "ceridwen"], "t_8f62974f", ""),
    ("analyses/ceridwen-gpu-benchmarks.html", "ceridwen-gpu-benchmarks", "Ceridwen GPU benchmarks",
     "Archive", ["gpu", "benchmarks"], "t_d89d040c", "obsolete"),
    ("analyses/checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html",
     "ceridwen-checkpoint-spectrum-evolution", "Ceridwen checkpoint spectrum evolution",
     "Notebooks", ["ceridwen", "checkpoints", "animation"], "t_ed2b739d", ""),

    ("codebase/project-map.html", "project-map", "Project map",
     "Codebase", ["repository"], "", ""),
    ("codebase/project-modules.html", "project-modules", "Project support modules",
     "Codebase", ["repository"], "", ""),
    ("codebase/ceridwen-architecture.html", "ceridwen-architecture", "Ceridwen architecture",
     "Codebase", ["ceridwen"], "", ""),
    ("codebase/ceridwen-ssp-csp.html", "ceridwen-ssp-csp", "Ceridwen: SSP grids to composite spectra",
     "Codebase", ["ceridwen", "ssp"], "", ""),
    ("codebase/ceridwen-likelihood-sampling.html", "ceridwen-likelihood-sampling",
     "Ceridwen: likelihood and sampling",
     "Codebase", ["ceridwen", "blackjax", "nested-sampling"], "", ""),
    ("codebase/ceridwen-observations-model.html", "ceridwen-observations-model",
     "Ceridwen: observations and SedModel",
     "Codebase", ["ceridwen"], "", ""),
    ("codebase/data-pipeline.html", "data-pipeline", "Data pipeline",
     "Codebase", ["legac", "dr2", "data"], "", ""),
    ("codebase/tests-as-documentation.html", "tests-as-documentation", "Tests as documentation",
     "Codebase", ["tests"], "", ""),
    ("codebase/active-codebase-map.html", "active-codebase-map", "Active Ceridwen codebase map",
     "Codebase", ["ceridwen", "repository"], "", ""),

    ("notebooks/notebook-map.html", "notebook-map", "Notebook map",
     "Notebooks", ["notebooks"], "", ""),
]

# Pages whose whole point is a self-contained interactive viewer. Their markup
# is JavaScript, not prose, so the note frames the preserved page instead of
# flattening it.
INTERACTIVE = {
    "active-codebase-map": ("2026-09-01", 8, "codebase/active-codebase-map.html"),
    "ceridwen-checkpoint-spectrum-evolution":
        ("2026-09-04", 12, "analyses/checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html"),
}

def esc(text: str) -> str:
    """Attribute-safe text."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def inline_html(md: str) -> str:
    """Render the inline Markdown a caption may carry: code, bold, links."""
    out = esc(md)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "figcaption", "dt", "dd",
         "td", "th", "pre", "caption"}
SKIP_TREE = {"script", "style", "nav", "svg"}


class ToMarkdown(HTMLParser):
    """Flatten one old wiki page into Markdown, preserving what it says."""

    def __init__(self, page_dir: str):
        super().__init__(convert_charrefs=True)
        self.page_dir = page_dir      # dir of the ORIGINAL page, for image paths
        self.out: list[str] = []      # finished blocks
        self.buf: list[str] = []      # text of the block being built
        self.skip = 0                 # depth inside a skipped subtree
        self.pre = False              # inside <pre>
        self.list_stack: list[str] = []
        self.li_index: list[int] = []
        self.row: list[str] = []      # cells of the current table row
        self.table: list[list[str]] = []
        self.in_table = False
        self.head_row = False
        self.href = ""
        self.link_start = 0
        self.figure = None            # cells of the <figure> being built
        self.first_h1 = True

    # -- helpers ---------------------------------------------------------
    def text(self) -> str:
        s = "".join(self.buf)
        self.buf = []
        if self.pre:
            return s
        return re.sub(r"[ \t]*\n[ \t]*", " ", re.sub(r"[ \t]+", " ", s)).strip()

    def emit(self, block: str) -> None:
        if block.strip():
            self.out.append(block.rstrip())

    def image_path(self, src: str) -> str:
        """Rewrite a page-relative image path to a build-stable `figures/` path."""
        if src.startswith(("http://", "https://", "data:")):
            return src
        target = (Path(self.page_dir) / src).resolve()
        try:
            rel = target.relative_to(WIKI).as_posix()
        except ValueError:
            try:
                return "/wiki/f/" + target.relative_to(ROOT).as_posix()
            except ValueError:
                return src           # points outside the repository; leave it
        return "figures/" + re.sub(r"^(analyses|codebase|guides|notebooks)/", "", rel, count=1)

    def link_path(self, href: str) -> str:
        """Point a link at a file the built site can actually serve."""
        if href.startswith(("http://", "https://", "mailto:", "#")):
            return href
        target = (Path(self.page_dir) / href).resolve()
        try:
            rel = target.relative_to(WIKI).as_posix()
        except ValueError:
            try:
                return "/wiki/f/" + target.relative_to(ROOT).as_posix()
            except ValueError:
                return href          # points outside the repository; leave it
        if rel.endswith(".html"):                     # another old page
            return "../" + target.stem + "/"
        return "figures/" + re.sub(r"^(analyses|codebase|guides|notebooks)/", "", rel, count=1)

    # -- parser ----------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip:
            if tag in SKIP_TREE:
                self.skip += 1
            return
        if tag in SKIP_TREE:
            self.skip = 1
            return
        if tag == "br":
            self.buf.append("\n" if self.pre else " ")
        elif tag == "img":
            src = self.image_path(a.get("src", ""))
            alt = a.get("alt", "")
            img = '<img src="%s" alt="%s">' % (esc(src), esc(alt))
            if self.figure is not None:
                self.figure.append(img)
            else:
                self.emit("<figure>%s</figure>" % img)
        elif tag == "figure":
            self.figure = []
        elif tag == "pre":
            self.pre = True
            self.buf = []
        elif tag in ("code", "kbd", "samp") and not self.pre:
            self.buf.append("`")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag == "a":
            self.href = self.link_path(a.get("href", ""))
            self.link_start = len(self.buf)
            self.buf.append("[")
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self.li_index.append(0)
        elif tag == "li":
            self.buf = []
        elif tag == "table":
            self.in_table, self.table = True, []
        elif tag == "tr":
            self.row, self.head_row = [], False
        elif tag in ("td", "th"):
            self.buf = []
            self.head_row = self.head_row or tag == "th"
        elif tag in BLOCK:
            self.buf = []

    def handle_endtag(self, tag):
        if self.skip:
            if tag in SKIP_TREE:
                self.skip -= 1
            return
        if tag == "pre":
            body = self.text().strip("\n")
            self.pre = False
            self.emit("```\n%s\n```" % body)
        elif tag in ("code", "kbd", "samp"):
            self.buf.append("`")
        elif tag in ("strong", "b"):
            self.buf.append("**")
        elif tag in ("em", "i"):
            self.buf.append("*")
        elif tag == "a":
            label = "".join(self.buf[self.link_start + 1:]).strip()
            del self.buf[self.link_start:]
            self.buf.append("[%s](%s)" % (label, self.href) if label and self.href else label)
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
                self.li_index.pop()
            if not self.list_stack:
                self.out.append("")
        elif tag == "li":
            body = self.text()
            if body:
                depth = max(len(self.list_stack) - 1, 0)
                if self.list_stack and self.list_stack[-1] == "ol":
                    self.li_index[-1] += 1
                    marker = "%d." % self.li_index[-1]
                else:
                    marker = "-"
                self.out.append("%s%s %s" % ("  " * depth, marker, body))
        elif tag in ("td", "th"):
            self.row.append(self.text().replace("|", "\\|"))
        elif tag == "tr":
            if self.row:
                first = not self.table
                self.table.append(self.row)
                if first:
                    self.table.append(["---"] * len(self.row))
        elif tag == "table":
            self.in_table = False
            if self.table:
                self.emit("\n".join("| " + " | ".join(r) + " |" for r in self.table))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            body = self.text()
            if tag == "h1" and self.first_h1:
                self.first_h1 = False           # the title lives in the frontmatter
                return
            level = min(int(tag[1]) + 1, 6)
            self.emit("%s %s" % ("#" * level, body))
        elif tag == "figcaption":
            caption = self.text()
            if self.figure is not None:
                self.figure.append("<figcaption>%s</figcaption>" % inline_html(caption))
            else:
                self.emit(caption)
        elif tag == "figure":
            parts, self.figure = self.figure or [], None
            self.emit("<figure>\n%s\n</figure>" % "\n".join(parts))
        elif tag == "dt":
            self.emit("**%s**" % self.text())
        elif tag == "dd":
            self.emit(self.text())
        elif tag in BLOCK:
            self.emit(self.text())

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)

    def markdown(self) -> str:
        body, prev_list = [], False
        for block in self.out:
            is_list = bool(re.match(r"^\s*(-|\d+\.) ", block))
            if body and not (is_list and prev_list):
                body.append("")
            body.append(block)
            prev_list = is_list
        text = "\n".join(body)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def main_html(raw: str) -> str:
    """The page body: what sits inside <main>, or the whole document."""
    m = re.search(r"<main\b[^>]*>(.*?)</main>", raw, re.S)
    return m.group(1) if m else raw


def meta_date(raw: str, default: str) -> str:
    m = re.search(r'name="wiki-updated"\s+content="([0-9-]+)"', raw)
    return m.group(1) if m else default


def frontmatter(slug, title, date, section, tags, job, status, extra=None):
    lines = ["---", "title: %s" % title, "date: %s" % date, "section: %s" % section,
             "tags: [%s]" % ", ".join(tags), "job: %s" % job]
    if status:
        lines.append("status: %s" % status)
    for key, value in (extra or {}).items():
        lines.append("%s: %s" % (key, value))
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def convert() -> int:
    NOTES.mkdir(parents=True, exist_ok=True)
    written = 0
    for source, slug, title, section, tags, job, status in PAGES:
        path = OLD / source
        if not path.is_file():
            print("missing: %s" % source, file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        extra = {"old": "_old/" + source}
        if slug in INTERACTIVE:
            date, height, target = INTERACTIVE[slug]
            extra["embed"] = "_old/" + target
            extra["embed_height"] = str(height)
            body = ""
        else:
            date = meta_date(raw, "2026-08-25")
            parser = ToMarkdown(page_dir=str((WIKI / source).parent))
            parser.feed(main_html(raw))
            body = parser.markdown()
        note = frontmatter(slug, title, date, section, tags, job, status, extra) + body
        (NOTES / (slug + ".md")).write_text(note, encoding="utf-8")
        written += 1
        print("%-42s -> notes/%s.md  (%d chars)" % (source, slug, len(body)))
    print("converted %d pages" % written)
    return 0


if __name__ == "__main__":
    sys.exit(convert())
