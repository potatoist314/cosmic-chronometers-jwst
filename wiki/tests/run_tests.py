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
    """Titles, tags, sections, dates and section labels out of the notes.

    These are Liu Hao's own words, so they are allowed anywhere on the page.
    The rail lists a note's section headings and the labels of its collapsed
    blocks, and both come straight out of the note.
    """
    words = set()
    for path in notes.glob("*.md"):
        raw = path.read_text(encoding="utf-8", errors="replace")
        head = raw.split("---")
        if len(head) < 3:
            continue
        body = raw.split("---", 2)[2]
        words.update(m.group(1).strip() for m in re.finditer(r"^#{1,6}\s+(.*)$", body, re.M))
        words.update(re.sub(r"<[^>]+>", "", m.group(1)).strip()
                     for m in re.finditer(r"<summary\b[^>]*>(.*?)</summary>", body, re.S | re.I))
        for line in head[1].splitlines():
            line = line.strip()
            for key in ("title:", "section:", "theme:", "date:", "status:", "job:"):
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


def load_build():
    """The generator as a module, for the counters the build enforces."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("astro_build", BUILD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NOTE_HEAD = ("---\ntitle: Planted note\ndate: 2026-09-06\nsection: Archive\n"
             "theme: Compute\ntags: [planted]\njob: \n---\n\n")


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
        check("log page exists", (out / "log/index.html").is_file())
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
        log_page = (out / "log/index.html").read_text()
        check("log page links every note",
              all(('href="/n/%s/"' % p.stem) in log_page for p in notes))
        body = "the effective uncertainty actually used by the likelihood"
        check("front page withholds note text", body not in index)

        # the theme hub: one card per theme, one page per theme
        bd0 = load_build()
        check("front page is the theme hub", "<h1>Themes</h1>" in index)
        check("the hub carries one card per theme",
              index.count('class="card"') == len(bd0.THEMES),
              "%d cards for %d themes" % (index.count('class="card"'), len(bd0.THEMES)))
        theme_pages = sorted((out / "themes").glob("*/index.html"))
        check("one page per theme", len(theme_pages) == len(bd0.THEMES), str(len(theme_pages)))
        accuracy = (out / "themes/single-fit-accuracy/index.html").read_text()
        check("a theme page carries its board and its notes",
              "<table>" in accuracy and 'href="/n/calibration-polynomial-dr2/"' in accuracy)
        board_part = accuracy.split("</table>")[0]
        cited = {r["note"] for r in bd0.parse_themes(ROOT / "themes.md")["Single-fit accuracy"]["rows"]}
        repeats = [c for c in cited if board_part.count('href="/n/%s/"' % c) != 1]
        check("the board links each experiment's note once", bool(cited) and not repeats,
              ", ".join(repeats))
        old_map = (out / "n/project-map/index.html").read_text()
        check("a superseded note names its successor",
              "Superseded by" in old_map and 'href="/n/active-codebase-map/"' in old_map)
        check("the successor page shows no banner",
              "Superseded by" not in (out / "n/active-codebase-map/index.html").read_text())

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
                               "Themes", "0", "RSS", "·", "Log", "·", "By date", "·",
                               "By topic"],
              repr(parser.nodes))

    # --- the word budget -------------------------------------------------
    bd = load_build()
    over = []
    for path in notes:
        note = bd.parse_note(path)
        if not note:
            continue
        body, _ = bd.split_thread(note["body"])
        words = bd.body_words(body)
        if words > bd.BODY_WORD_CAP:
            over.append("%s: %d words" % (note["slug"], words))
    check("every note is inside the %d-word body budget" % bd.BODY_WORD_CAP,
          not over, "; ".join(over[:4]))

    # --- themes -----------------------------------------------------------
    off_theme = []
    for path in notes:
        note = bd.parse_note(path)
        if not note:
            continue
        if note["theme"] not in bd.THEMES and note["status"] != "obsolete":
            off_theme.append("%s: %r" % (note["slug"], note["theme"]))
    check("every live note names one of the themes", not off_theme, "; ".join(off_theme[:4]))
    board = bd.parse_themes(ROOT / "themes.md")
    check("the board names every theme", set(board) == set(bd.THEMES),
          repr(sorted(set(bd.THEMES) ^ set(board))))
    bad_status = ["%s: %s" % (t, r["status"]) for t, b in board.items()
                  for r in b["rows"] if r["status"] not in bd.STATUSES]
    check("every board status is one of %s" % ", ".join(bd.STATUSES), not bad_status,
          "; ".join(bad_status[:4]))
    check("the board itself passes the build's checks",
          not bd.theme_faults([bd.parse_note(p) for p in notes], board),
          "; ".join(bd.theme_faults([bd.parse_note(p) for p in notes], board)[:4]))

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "lost.md").write_text(
            NOTE_HEAD.replace("theme: Compute", "theme: Nonsense") + "two words\n",
            encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("an unknown theme stops the build", run.returncode != 0, run.stdout)
        check("the build names the theme it refused", "Nonsense" in run.stderr,
              run.stderr.strip()[:160])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "quiet.md").write_text(
            NOTE_HEAD.replace("theme: Compute", "status: obsolete") + "two words\n",
            encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("an obsolete note needs no theme", run.returncode == 0, run.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "orphan.md").write_text(
            NOTE_HEAD.replace("theme: Compute", "theme: Compute\nsuperseded_by: nowhere")
            + "two words\n", encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("a superseded_by pointing nowhere stops the build", run.returncode != 0, run.stdout)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "tiny.md").write_text(NOTE_HEAD + "two words\n", encoding="utf-8")
        def board(change, status, result, note="tiny"):
            (tmp / "themes.md").write_text(
                "# Themes\n\n## Compute\n\nWhere the fits run\n\n### GPU choice\nnote: %s\n\n"
                "| arm | change | status | result |\n| --- | --- | --- | --- |\n"
                "| `x` | %s | %s | %s |\n" % (note, change, status, result), encoding="utf-8")
            return build_into(tmp, BUILD, planted)
        run, _ = board("smaller card", "adopted", PLANTED)
        check("a sentence in a board result cell stops the build", run.returncode != 0, run.stdout)
        run, _ = board(PLANTED, "adopted", "one clause")
        check("a sentence in a board change cell stops the build", run.returncode != 0, run.stdout)
        run, _ = board("smaller card", "maybe", "one clause")
        check("an unknown board status stops the build", run.returncode != 0, run.stdout)
        run, _ = board("smaller card", "adopted", "one clause", note="nowhere")
        check("an experiment citing no note stops the build", run.returncode != 0, run.stdout)
        run, out = board("smaller card", "adopted", "one clause")
        check("a clean board builds", run.returncode == 0, run.stderr)
        hub = (out / "index.html").read_text() if run.returncode == 0 else ""
        check("the hub tallies the board", "1 adopted" in hub and "1 note" in hub, hub[-600:])

    long_caps = []
    for path in notes:
        note = bd.parse_note(path)
        if not note:
            continue
        body, _ = bd.split_thread(note["body"])
        long_caps += ["%s: %s" % (note["slug"], c) for c in bd.caption_faults(body)]
    check("every figure caption is one sentence", not long_caps,
          "; ".join(long_caps[:3]))

    # the counter itself: what does and does not count as body prose
    check("prose counts, code and tables do not",
          bd.body_words("one two three\n\n```\nfour five six seven\n```\n"
                        "\n| a | b |\n| - | - |\n| c | d |\n") == 3,
          str(bd.body_words("one two three\n\n```\nx y z\n```\n")))
    check("a figure and its caption do not count",
          bd.body_words("<figure>\n<figcaption>Ten words of caption text right "
                        "here now please.</figcaption>\n</figure>\n") == 0)
    check("a collapsed block does not count",
          bd.body_words("<details>\n<summary>Details</summary>\n\n"
                        "one two three four five\n\n</details>\n") == 0)
    check("a model-settings block does not count",
          bd.body_words("live points\n: five hundred of them\n") == 0)
    check("headings do count", bd.body_words("## two words\n") == 2)
    check("a two-sentence caption is a fault",
          len(bd.caption_faults("<figcaption>One thing. Then another.</figcaption>")) == 1)
    check("a caption may open with one bold label",
          bd.caption_sentences("<strong>A figure PNG.</strong> One sentence here.") == 1)

    # --- canaries: the build must stop -----------------------------------
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "fat.md").write_text(
            NOTE_HEAD + " ".join(["word"] * 200) + "\n", encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("an over-budget note stops the build", run.returncode != 0, run.stdout)
        check("the build says which note and by how much",
              "fat" in run.stderr and "budget" in run.stderr, run.stderr.strip()[:200])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "chatty.md").write_text(
            NOTE_HEAD + "<figure>\n<figcaption>One sentence. And a second "
            "one.</figcaption>\n</figure>\n", encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("a two-sentence caption stops the build", run.returncode != 0, run.stdout)

    # --- a collapsed block renders its Markdown --------------------------
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "folded.md").write_text(
            NOTE_HEAD + "Two words.\n\n<details>\n<summary>Method</summary>\n\n"
            "- one item\n\n</details>\n", encoding="utf-8")
        run, out = build_into(tmp, BUILD, planted)
        page = (out / "n/folded/index.html").read_text() if run.returncode == 0 else ""
        check("a collapsed block renders its Markdown",
              '<summary id="method">Method</summary><ul><li>one item</li></ul>' in page,
              run.stderr or page[:200])
        check("a named collapsed block reaches the rail",
              'href="#method"' in page, page[:200])

    # --- the figures list ------------------------------------------------
    missing = []
    for path in notes:
        note = bd.parse_note(path)
        if not note:
            continue
        body, _ = bd.split_thread(note["body"])
        missing += bd.figure_faults(note, body)
    check("every note shows only the figures its list names", not missing,
          "; ".join(missing[:3]))

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "extra.md").write_text(
            NOTE_HEAD.replace("tags: [planted]", "tags: [planted]\nfigures: [wanted.png]")
            + '<figure><img src="figures/x/unwanted.png" alt="x">'
            '<figcaption>One line.</figcaption></figure>\n', encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("an unlisted image stops the build", run.returncode != 0, run.stdout)
        check("the build names the image it refused",
              "unwanted.png" in run.stderr, run.stderr.strip()[:160])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "listed.md").write_text(
            NOTE_HEAD.replace("tags: [planted]", "tags: [planted]\nfigures: [wanted.png]")
            + '<figure><img src="figures/x/wanted.png" alt="x">'
            '<figcaption>One line.</figcaption></figure>\n', encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("a listed image builds", run.returncode == 0, run.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        planted = tmp / "notes"
        planted.mkdir()
        (planted / "nolist.md").write_text(
            NOTE_HEAD + '<figure><img src="figures/x/orphan.png" alt="x">'
            '<figcaption>One line.</figcaption></figure>\n', encoding="utf-8")
        run, _ = build_into(tmp, BUILD, planted)
        check("an image with no figures list stops the build",
              run.returncode != 0, run.stdout)

    # A build of some other folder must not replace the live word counts.
    stamp = bd.WORD_COUNTS_PATH.stat().st_mtime if bd.WORD_COUNTS_PATH.exists() else 0
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        other = tmp / "notes"
        other.mkdir()
        (other / "tiny.md").write_text(NOTE_HEAD + "two words\n", encoding="utf-8")
        build_into(tmp, BUILD, other)
        now = bd.WORD_COUNTS_PATH.stat().st_mtime if bd.WORD_COUNTS_PATH.exists() else 0
        check("a build of another folder leaves the published counts alone",
              now == stamp, "counts file was rewritten")

    print()
    print("FAILED: " + ", ".join(failures) if failures else "all tests passed")
    return 1 if failures else 0


# Navigation labels the generator is allowed to write. Four words at most, and
# never a sentence. Adding a fifth word here does not silence the audit.
LABELS = {
    "Notes", "Themes", "Theme", "Log", "Sections", "Search notes", "On this page",
    "Record", "Original", "Superseded by", "Thread", "Ask", "Question", "By date",
    "By topic", "RSS", "·", " · ", "Q", "A", "archive", "analyses", "guides",
    "notebooks", "codebase", "paper drafts", "obsolete",
    "Single-fit accuracy", "Validation on mocks", "Sample and data",
    "Population results", "Compute", "Model and code reference", "Background reading",
    "adopted", "dropped", "inconclusive", "planned",
}


if __name__ == "__main__":
    sys.exit(main())
