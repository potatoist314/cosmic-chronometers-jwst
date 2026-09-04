#!/usr/bin/env python3
"""Safety tests for the Astro lab notebook.

One thing matters here. The site must speak only in Liu Hao's words: note
titles, note bodies, dates, tags, and short navigation labels. The generator
writes no prose of its own, and the checks below fail if any appears.

The model is `~/thoughts-site/tests/run_tests.py`. The rule is the same: every
visible text node outside a note body must be a label of at most four words and
must not end a sentence.

    python3 wiki/tests/run_tests.py [--plant]

`--plant` puts one generated sentence into a copy of the generator and shows
the audit catching it.
"""

import re
import subprocess
import sys
import tempfile
import xml.dom.minidom
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # wiki/
NOTES = ROOT / "notes"
BUILD = ROOT / "build.py"

# Words that belong to nobody in particular: navigation, section labels, dates.
# Anything longer than a label, outside a note body, is prose and fails.
MAX_LABEL_WORDS = 4
SENTENCE_END = re.compile(r"[.!?](\s|$)")

# A sentence the generator must never write. Planted by --plant and by the
# canary check, to prove the audit still bites.
PLANTED = "This note collects the figures and numbers that came out of the run."

failures = []


def check(name, condition, detail=""):
    print(("  ok   " if condition else "  FAIL ") + name +
          (" — " + detail if detail and not condition else ""))
    if not condition:
        failures.append(name)


class ChromeText(HTMLParser):
    """Every visible text node except the note bodies — the page's chrome."""

    SKIP = {"script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.skip_tag = ""     # the element we are inside and ignoring
        self.skip_depth = 0    # nesting of that same tag name, so we close the right one

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth += 1
        elif tag in self.SKIP or "prose" in classes:
            self.skip_tag, self.skip_depth = tag, 1

    def handle_endtag(self, tag):
        if self.skip_tag and tag == self.skip_tag:
            self.skip_depth -= 1
            if self.skip_depth == 0:
                self.skip_tag = ""

    def handle_data(self, data):
        if not self.skip_tag and data.strip():
            self.nodes.append(data.strip())


def author_words(notes: Path) -> set:
    """Titles, tags, sections and dates out of the notes — allowed anywhere."""
    words = set()
    for path in notes.glob("*.md"):
        head = path.read_text(encoding="utf-8", errors="replace").split("---")
        if len(head) < 3:
            continue
        for line in head[1].splitlines():
            line = line.strip()
            for key in ("title:", "section:", "date:", "status:", "job:"):
                if line.startswith(key):
                    words.add(line.split(":", 1)[1].strip())
            if line.startswith("tags:"):
                words.update(t.strip() for t in line.split(":", 1)[1].strip(" []").split(","))
            if line.startswith("section:"):
                words.add(line.split(":", 1)[1].strip().lower())
    return {w for w in words if w}


def site_identity(build_py: Path) -> set:
    """The site's own name and byline, which the generator carries as data."""
    text = build_py.read_text(encoding="utf-8")
    out = set()
    for key in ("SITE_NAME", "SITE_WHO"):
        m = re.search(r'^%s\s*=\s*"([^"]+)"' % key, text, re.M)
        if m:
            out.add(m.group(1))
    return out


def chrome_prose(page: str, allowed: set) -> list:
    """Sentence-length text the generator wrote itself. Should always be empty."""
    parser = ChromeText()
    parser.feed(page.split("<body>", 1)[-1])
    offenders = []
    for node in parser.nodes:
        if node in allowed:
            continue
        if len(node.split()) > MAX_LABEL_WORDS or SENTENCE_END.search(node):
            offenders.append(node)
    return offenders


def audit(out: Path, allowed: set, label: str) -> list:
    """No generator sentences on any page."""
    offenders = []
    for page in sorted(out.rglob("*.html")):
        if "_old" in page.relative_to(out).parts:      # preserved originals, not built
            continue
        for node in chrome_prose(page.read_text(encoding="utf-8", errors="replace"), allowed):
            offenders.append("%s: %r" % (page.relative_to(out), node))
    if label:
        check("%s: no generator prose outside note bodies" % label,
              not offenders, "; ".join(offenders[:4]))
    return offenders


def build_into(tmp: Path, build_py: Path, notes: Path) -> tuple:
    out = tmp / "public"
    run = subprocess.run([sys.executable, str(build_py), "--notes", str(notes),
                          "--out", str(out), "--base", ""],
                         capture_output=True, text=True)
    return run, out


def build_planted(tmp: Path, notes: Path) -> Path:
    """Build with one sentence of the generator's own prose in the chrome."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("astro_build_planted", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original = module.shell

    def planted_shell(title, base, body, rail, extra_head="", desc=""):
        page = original(title, base, body, rail, extra_head, desc)
        return page.replace("<main>", '<main>\n<p class="dek">' + PLANTED + "</p>", 1)

    module.shell = planted_shell
    out = tmp / "public"
    module.build(notes, out, "")
    return out


def main() -> int:
    if "--plant" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            out = build_planted(tmp, NOTES)
            offenders = audit(out, author_words(NOTES) | site_identity(BUILD) | LABELS, "")
            print("planted sentence: %r" % PLANTED)
            print("audit found %d offending chrome nodes; first three:" % len(offenders))
            for line in offenders[:3]:
                print("  " + line)
            print("\nFAILED: planted prose (expected)" if offenders else "\nNOT CAUGHT")
            return 1 if offenders else 2

    notes = sorted(NOTES.glob("*.md"))
    allowed = author_words(NOTES) | site_identity(BUILD) | LABELS

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        run, out = build_into(tmp, BUILD, NOTES)
        check("build exits cleanly", run.returncode == 0, run.stderr)
        check("build reports every note", "built %d notes" % len(notes) in run.stdout,
              run.stdout.strip())

        check("front page exists", (out / "index.html").is_file())
        check("note pages exist", len(list((out / "n").glob("*/index.html"))) == len(notes))
        check("by-date page exists", (out / "date/index.html").is_file())
        check("by-topic page exists", (out / "sections/index.html").is_file())
        check("feed exists", (out / "feed.xml").is_file())
        check("stylesheet exists", (out / "style.css").is_file())
        check("search index exists", (out / "search.json").is_file())
        check("search script is vendored", (out / "search.js").is_file())
        check("fonts shipped", len(list((out / "fonts").glob("*.woff2"))) == 10)
        check("no runtime CDN", not re.search(
            r"https?://(?!127\.0\.0\.1)[^\"')\s]+\.(?:js|css|woff2?)",
            (out / "index.html").read_text() + (out / "style.css").read_text()))
        check("dark mode declared", "prefers-color-scheme: dark" in (out / "style.css").read_text())
        check("phone width declared", "@media (max-width:760px)" in (out / "style.css").read_text())

        index = (out / "index.html").read_text()
        check("front page links every note",
              all(('href="/n/%s/"' % p.stem) in index for p in notes))
        body = "the effective uncertainty actually used by the likelihood"
        check("front page withholds note text", body not in index)

        # the thread box only where the note's own session can still answer
        muse_note = (out / "n/stacked-chi2-and-median-pull/index.html").read_text()
        gemini_note = (out / "n/ceridwen-checkpoint-spectrum-evolution/index.html").read_text()
        check("resumable note carries the question box", 'class="ask"' in muse_note)
        check("gemini note carries no question box and no notice",
              'class="ask"' not in gemini_note and "resume" not in gemini_note.lower())

        audit(out, allowed, "notebook")

        try:
            xml.dom.minidom.parse(str(out / "feed.xml"))
            check("feed is well-formed XML", True)
        except Exception as exc:            # noqa: BLE001
            check("feed is well-formed XML", False, str(exc))

        run2, _ = build_into(tmp, BUILD, NOTES)
        check("rebuild over existing output", run2.returncode == 0, run2.stderr)
        check("no leftover scratch dirs", not list(tmp.glob("public.*")))

    # the canary: one planted generator sentence must fail the audit
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        offenders = audit(build_planted(tmp, NOTES), allowed, "")
        check("a planted generator sentence fails the audit",
              any(PLANTED in o for o in offenders),
              "%d offenders, none planted" % len(offenders))

    # an empty notebook still builds a finished page: the masthead, and nothing else
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        empty = tmp / "notes"
        empty.mkdir()
        run, out = build_into(tmp, BUILD, empty)
        check("empty notebook builds", run.returncode == 0, run.stderr)
        parser = ChromeText()
        parser.feed((out / "index.html").read_text().split("<body>", 1)[-1])
        check("empty front page is the masthead and nothing else",
              parser.nodes == ["Astro Lab Notebook", "Liu Hao · DR2 quiescent galaxies",
                               "Notes", "0", "RSS", "·", "By date", "·", "By topic"],
              repr(parser.nodes))

    print()
    print("FAILED: " + ", ".join(failures) if failures else "all tests passed")
    return 1 if failures else 0


# Navigation labels the generator is allowed to write. Four words at most, and
# never a sentence. Adding a fifth word here does not silence the audit.
LABELS = {
    "Notes", "Sections", "Search notes", "On this page", "Record", "Original",
    "Thread", "Ask", "Question", "By date", "By topic", "RSS", "·", " · ",
    "Q", "A", "archive", "analyses", "guides", "notebooks", "codebase",
    "paper drafts", "obsolete",
}


if __name__ == "__main__":
    sys.exit(main())
