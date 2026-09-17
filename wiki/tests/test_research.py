"""Research evidence, historical integration and original-message preservation."""

import base64
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

WIKI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WIKI))
import research

spec = importlib.util.spec_from_file_location("wiki_build", WIKI / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class Quotes(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.values = []

    def handle_starttag(self, tag, attrs):
        if tag == "blockquote":
            self.inside = True
            self.values.append("")

    def handle_endtag(self, tag):
        if tag == "blockquote":
            self.inside = False

    def handle_data(self, text):
        if self.inside:
            self.values[-1] += text


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        self.root = self.project / "wiki/research"
        self.notes = self.project / "wiki/notes"
        self.notes.mkdir(parents=True)
        self.original = "i think this might work...\n\n  keep  my spacing, **and Markdown** <b>literal</b> & α.\n" + "reason " * 70
        self.message = {"date": "2026-09-12", "text": self.original}
        self.write("question", "q-dust", "open", {"Your words": [self.message], "Decisions": []})
        self.write("experiment", "e-low-dust", "planned", {"Before delegation": [self.message]}, question="q-dust")

    def write(self, kind, ident, status, sections, **meta):
        parent = self.root if kind == "direction" else self.root / (kind + "s")
        parent.mkdir(parents=True, exist_ok=True)
        path = parent / ("direction.md" if kind == "direction" else ident + ".md")
        header = dict(kind=kind, id=ident, title=ident + " & <literal>", date="2026-09-12", status=status, **meta)
        text = "---\n" + "\n".join(k + ": " + v for k, v in header.items()) + "\n---\n"
        for name, value in sections.items():
            text += "\n## " + name + "\n\n"
            text += ("```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```\n") if isinstance(value, list) else value + "\n"
        path.write_text(text)
        return path

    def load(self):
        records, errors = research.load(self.root)
        self.assertEqual(errors, [])
        return records

    def faults(self):
        return research.validate(self.load(), self.project)

    def evidence(self):
        folder = self.project / "results/e-low-dust"
        folder.mkdir(parents=True, exist_ok=True)
        for name, content in (("config.json", '{"tau": [0, 0.2]}'),
                              ("sample.csv", "id\n1\n"), ("analysis.ipynb", '{"cells": []}'),
                              ("measurements.csv", "age_shift_Gyr\n0.12\n")):
            (folder / name).write_text(content)
        (folder / "fit.png").write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII="))
        return {"id": "baseline-seed-1", "arm": "baseline", "status": "complete",
                "config": "results/e-low-dust/config.json", "code": "fixture-version",
                "model": "fixture-grid-v1", "data": "results/e-low-dust/sample.csv", "seed": 1,
                "artifacts": [{"label": "Executed analysis", "path": "results/e-low-dust/analysis.ipynb"}]}

    def completed(self, status="results-ready", interpretation=None):
        run = self.evidence()
        sections = {"Before delegation": [self.message], "Execution plan": "Compare the two fixed configurations.",
                    "Runs": [run], "Results": "Age shift: 0.12 Gyr. [Table](results/e-low-dust/measurements.csv).",
                    "Your interpretation": interpretation or [],
                    "Figures": [{"path": "results/e-low-dust/fit.png", "view": "Fits", "caption": "Two fixed configurations."}]}
        self.write("experiment", "e-low-dust", status, sections, question="q-dust")
        return sections

    def build(self, base="/wiki"):
        out = self.project / "public"
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.notes, out, base, self.root), 0)
        for page in out.rglob("*.html"):
            body = page.read_text()
            for label in ("Agent · source summary", "Agent · execution plan",
                          "Agent · execution records", "Agent · measured results",
                          "Existing research · organised from saved records"):
                self.assertNotIn(label, body, str(page))
        return out

    def test_planned_experiment_has_no_fabricated_results(self):
        self.assertEqual(self.faults(), [])
        out = self.build()
        body = (out / "e/e-low-dust/record/index.html").read_text()
        self.assertIn("Not recorded", body)
        self.assertNotIn("Agent · synthesis", body)
        self.assertNotIn("Chat reference", body)
        self.assertIn("e-low-dust", (out / "q/q-dust/index.html").read_text())
        anchors = set(re.findall(r'href="#([^"]+)"', body))
        identifiers = set(re.findall(r'id="([^"]+)"', body))
        self.assertEqual(anchors - identifiers, set())

    def roadmap(self):
        (self.notes / "meeting.md").write_text(
            "---\ntitle: Meeting\ndate: 2026-09-15\nsection: Meetings\n"
            "theme: Single-fit accuracy\n---\n\n## Metallicity\n\nA question, not a result.\n")
        tasks = [
            {"id": "spectrum", "title": "Strong spectrum", "priority": 7,
             "source": "wiki/notes/meeting.md#metallicity", "depends_on": ["metallicity"]},
            {"id": "unscored", "title": "Unscored follow-up", "priority": None,
             "source": "wiki/notes/meeting.md"},
            {"id": "metallicity", "title": "Metallicity & definition", "priority": 10,
             "source": "wiki/notes/meeting.md#metallicity", "details": "Is this <total Z>?"},
            {"id": "literature", "title": "Literature", "priority": 7,
             "source": "wiki/notes/meeting.md", "effort": "Implementation uncertain"},
        ]
        sections = {"Your words": [self.message], "Roadmap": tasks,
                    "Amendments": [dict(self.message, text="keep this 1-10 scale\n  and my wording")],
                    "References": "[Meeting](wiki/notes/meeting.md)"}
        self.write("direction", "research-direction", "", sections)
        return sections

    def test_roadmap_preserves_scores_dependencies_and_original_amendments(self):
        self.roadmap()
        self.assertEqual(self.faults(), [])
        out = self.build()
        page = (out / "roadmap/index.html").read_text()
        home = (out / "index.html").read_text()
        self.assertEqual(re.findall(r'<tr id="([^"]+)"', page),
                         ["metallicity", "spectrum", "literature", "unscored"])
        self.assertEqual(re.findall(r'<tr id="([^"]+)"', home),
                         ["metallicity", "spectrum", "literature", "unscored"])
        self.assertEqual(home, page)
        self.assertIn('href="/wiki/#metallicity"', page)
        self.assertIn('href="/wiki/n/meeting/#metallicity"', home)
        self.assertIn("10/10", page)
        self.assertIn("Unscored follow-up", page)
        self.assertIn("Implementation uncertain", page)
        self.assertIn("Is this &lt;total Z&gt;?", page)
        quotes = Quotes()
        quotes.feed(page)
        self.assertEqual(quotes.values, [self.original, "keep this 1-10 scale\n  and my wording"])
        self.assertIn('href="/wiki/"', (out / "q/q-dust/index.html").read_text())
        self.assertIn('<details class="research-history"><summary>Research record</summary>', home)
        self.assertIn('id="roadmap-amendments"', home)
        self.assertTrue(any(item["u"] == "/wiki/" for item in json.loads((out / "search.json").read_text())))

    def test_priority_change_updates_both_views_from_one_record(self):
        sections = self.roadmap()
        sections["Roadmap"][0]["priority"] = 1
        self.write("direction", "research-direction", "", sections)
        out = self.build("")
        for path in ("index.html", "roadmap/index.html"):
            body = (out / path).read_text()
            self.assertEqual(re.findall(r'<tr id="([^"]+)"', body)[:3],
                             ["metallicity", "literature", "spectrum"])
            self.assertIn('href="/#metallicity"', body)
            self.assertIn("1/10", body)

    def test_roadmap_rejects_invalid_scores_and_dependencies(self):
        sections = self.roadmap()
        for priority in (0, 11, True, 2.5, "7"):
            with self.subTest(priority=priority):
                sections["Roadmap"][0]["priority"] = priority
                self.write("direction", "research-direction", "", sections)
                self.assertIn("roadmap priority must be an integer", "\n".join(self.faults()))
        sections["Roadmap"][0]["priority"] = 7
        for dependencies in (["missing"], ["spectrum"], "metallicity"):
            with self.subTest(dependencies=dependencies):
                sections["Roadmap"][0]["depends_on"] = dependencies
                self.write("direction", "research-direction", "", sections)
                self.assertIn("roadmap dependencies must reference", "\n".join(self.faults()))
        sections["Roadmap"][0]["depends_on"] = ["metallicity"]
        sections["Roadmap"].append(dict(sections["Roadmap"][0]))
        self.write("direction", "research-direction", "", sections)
        self.assertIn("roadmap task ids must be unique", "\n".join(self.faults()))

    def test_existing_direction_without_roadmap_still_builds(self):
        self.write("direction", "research-direction", "", {"Your words": [self.message]})
        self.assertEqual(self.faults(), [])
        out = self.build()
        self.assertIn("No priorities recorded", (out / "roadmap/index.html").read_text())
        quotes = Quotes()
        quotes.feed((out / "index.html").read_text())
        self.assertEqual(quotes.values, [self.original])

    def test_exact_words_survive_results_interpretation_and_amendment(self):
        sections = self.completed("reviewed", [{"date": "2026-09-13", "text": "inconclusive. keep this open."}])
        sections["Amendments"] = [{"date": "2026-09-13", "text": "correction: use the other sample\n"}]
        sections["Next decision"] = [{"date": "2026-09-13", "text": "try another seed."}]
        self.write("experiment", "e-low-dust", "reviewed", sections, question="q-dust")
        self.assertEqual(self.faults(), [])
        out = self.build()
        parser = Quotes()
        parser.feed((out / "e/e-low-dust/record/index.html").read_text())
        self.assertEqual(parser.values, [self.original, "correction: use the other sample\n", "inconclusive. keep this open.", "try another seed."])
        self.assertNotIn("<b>literal</b>", (out / "e/e-low-dust/record/index.html").read_text())

    def test_complete_run_cannot_review_itself(self):
        self.completed("reviewed")
        self.assertTrue(any("reviewed requires your recorded interpretation" in f for f in self.faults()))

    def test_multiple_arms_repeats_and_failure_remain_visible(self):
        sections = self.completed()
        baseline = sections["Runs"][0]
        repeat = dict(baseline, id="baseline-seed-2", seed=2)
        failure = dict(baseline, id="low-dust-seed-1", arm="low-dust", status="failed", error="Sampler did not finish.", artifacts=[])
        sections["Runs"] += [repeat, failure]
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        self.assertEqual(self.faults(), [])
        body = (self.build() / "e/e-low-dust/record/index.html").read_text()
        for text in ("baseline-seed-1", "baseline-seed-2", "low-dust-seed-1", "Failed", "Sampler did not finish.", "0.12 Gyr"):
            self.assertIn(text, body)

    def test_contradictory_run_status_is_rejected(self):
        sections = self.completed()
        sections["Runs"][0]["status"] = "running"
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        self.assertTrue(any("contradicts a running run" in f for f in self.faults()))

    def test_missing_parent_and_follow_up_are_named(self):
        self.write("experiment", "e-low-dust", "planned", {"Before delegation": [self.message]}, question="q-missing", follow_up="e-missing")
        faults = "\n".join(self.faults())
        self.assertIn("question must reference", faults)
        self.assertIn("e-missing", faults)

    def test_missing_evidence_blocks_publish_and_preserves_live_output(self):
        out = self.build()
        initial = (out / "index.html").read_text()
        self.completed()
        (self.project / "results/e-low-dust/measurements.csv").unlink()
        self.assertTrue(any("missing evidence file" in f for f in self.faults()))
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.notes, out, "/wiki", self.root), 1)
        self.assertEqual((out / "index.html").read_text(), initial)

    def test_source_reference_and_file_urls_preserve_escaping(self):
        source = self.project / "chat excerpt.txt"
        source.write_text(self.original)
        message = dict(self.message, source="chat%20excerpt.txt", source_ref="fixture message 1")
        self.write("question", "q-dust", "open", {"Your words": [message]})
        body = (self.build("") / "q/q-dust/index.html").read_text()
        self.assertIn('href="/f/chat%20excerpt.txt"', body)
        self.assertIn("fixture message 1", body)

    def test_search_includes_question_experiment_and_full_original_words(self):
        self.completed()
        out = self.build()
        index = json.loads((out / "search.json").read_text())
        self.assertEqual({r["s"] for r in index}, {"Question", "Experiment"})
        self.assertTrue(all("reason reason" in r["x"] for r in index))
        self.assertIn("results-ready", (out / "experiments/index.html").read_text())
        self.assertIn("e-low-dust", (out / "results/index.html").read_text())

    def test_templates_are_not_loaded_and_json_errors_are_actionable(self):
        templates = self.root / "templates"
        templates.mkdir()
        (templates / "invalid.md").write_text("not a record")
        self.assertEqual(len(self.load()), 2)
        path = self.root / "experiments/e-low-dust.md"
        path.write_text(path.read_text().replace('"text":', '"text"'))
        _, errors = research.load(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn("e-low-dust.md", errors[0])

    def test_cli_accepts_isolated_research_sources(self):
        out = self.project / "cli-public"
        result = subprocess.run([sys.executable, str(WIKI / "build.py"), "--notes", str(self.notes),
                                 "--research", str(self.root), "--out", str(out)],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((out / "e/e-low-dust/record/index.html").is_file())

    def test_invalid_metadata_types_produce_validation_errors(self):
        sections = self.completed()
        sections["Before delegation"][0]["source_ref"] = ["not a string"]
        sections["Runs"][0]["config"] = 42
        sections["Runs"][0]["artifacts"][0]["path"] = 42
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        faults = "\n".join(self.faults())
        self.assertIn("source_ref must be a string", faults)
        self.assertIn("evidence reference must be a string", faults)
        self.assertIn("each artifact needs a label and path", faults)

    def test_existing_http_server_delivers_run_evidence(self):
        self.completed()
        out = self.project / "wiki/public"
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.notes, out, "/wiki", self.root), 0)
        spec = importlib.util.spec_from_file_location("wiki_http", WIKI.parent / "scripts/serve_wiki.py")
        server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server)
        handler = type("FixtureHandler", (server.AstroWikiHandler,), {
            "project_root": self.project.resolve(), "log_message": lambda *args: None,
        })
        httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            host = "http://127.0.0.1:%s" % httpd.server_port
            with urllib.request.urlopen(host + "/wiki/f/results/e-low-dust/config.json", timeout=5) as response:
                self.assertEqual(json.load(response), {"tau": [0, 0.2]})
            with urllib.request.urlopen(host + "/wiki/f/results/e-low-dust/analysis.ipynb", timeout=5) as response:
                self.assertEqual(json.load(response), {"cells": []})
        finally:
            httpd.shutdown()
            thread.join()
            httpd.server_close()

    def test_missing_before_words_unknown_state_and_reused_run_ids(self):
        sections = self.completed()
        sections["Before delegation"] = []
        sections["Runs"] *= 2
        self.write("experiment", "e-low-dust", "adopted", sections, question="q-dust")
        faults = "\n".join(self.faults())
        self.assertIn("before-delegation words", faults)
        self.assertIn("status must be", faults)
        self.assertIn("unique within the experiment", faults)

    def test_legacy_note_and_routes_remain_accessible(self):
        (self.notes / "existing.md").write_text("---\ntitle: Existing analysis\ndate: 2026-09-01\nsection: Analyses\ntheme: Population results\n---\n\nOriginal evidence.\n")
        out = self.build()
        self.assertIn("Original evidence.", (out / "n/existing/index.html").read_text())
        self.assertIn("/wiki/n/existing/", (out / "earlier/index.html").read_text())
        self.assertTrue((out / "themes/population-results/index.html").is_file())
        self.assertTrue((out / "themes/index.html").is_file())

    def test_seven_sections_keep_all_notes_records_and_papers_reachable(self):
        self.roadmap()
        self.completed()
        self.write("experiment", "e-planned", "planned", {"Before delegation": [self.message]}, question="q-dust")
        placements = {"analysis": ("Analyses", "results"), "mask": ("Masking", "masking"),
                      "code": ("Codebase", "code"), "notebook": ("Notebooks", "code"),
                      "guide": ("Guides", "code"), "paper": ("Paper drafts", "papers"),
                      "archive": ("Archive", "code"), "values": ("Literature", "literature")}
        for slug, (category, _) in placements.items():
            (self.notes / (slug + ".md")).write_text(
                "---\ntitle: " + slug + "\ndate: 2026-09-15\nsection: " + category +
                "\ntheme: Single-fit accuracy\n---\n\nExisting content.\n")
        papers = self.project / "papers"
        papers.mkdir()
        (papers / "chronometer").mkdir()
        (papers / "chronometer/A & B.pdf").write_bytes(b"fixture PDF")
        (papers / "README.md").write_text(
            "| File | Citation | Role |\n| --- | --- | --- |\n"
            "| `A & B.pdf` | Author (2025), A&amp;A | **Current target** |\n")
        out = self.build()
        for slug, (_, destination) in placements.items():
            collection = (out / destination / "index.html").read_text()
            if destination == "literature":
                self.assertIn("Existing content.", collection)
                self.assertIn('/wiki/n/' + slug + '/', (out / "earlier/index.html").read_text())
            else:
                self.assertIn('/wiki/n/' + slug + '/', collection)
            self.assertIn("Existing content.", (out / "n" / slug / "index.html").read_text())
        self.assertIn('/wiki/n/meeting/', (out / "meetings/index.html").read_text())
        code = (out / "code/index.html").read_text()
        self.assertNotIn('/wiki/n/meeting/', code)
        self.assertIn('/wiki/log/', code)
        results = (out / "results/index.html").read_text()
        self.assertLess(results.index('/wiki/e/e-low-dust/'), results.index('Other experiment records'))
        self.assertGreater(results.index('/wiki/e/e-planned/'), results.index('Other experiment records'))
        self.assertIn('/wiki/themes/', results)
        self.assertIn('/wiki/e/e-planned/', (out / "index.html").read_text())
        catalog = (out / "papers/index.html").read_text()
        self.assertIn('/wiki/f/papers/chronometer/A%20%26%20B.pdf', catalog)
        self.assertIn('Author (2025), A&amp;A', catalog)
        self.assertNotIn('Current target', catalog)
        self.assertNotIn('/wiki/n/values/', (out / "reference/index.html").read_text())
        search = json.loads((out / "search.json").read_text())
        self.assertTrue(any(item["u"] == '/wiki/f/papers/chronometer/A%20%26%20B.pdf' for item in search))
        for legacy in ("roadmap", "questions", "experiments", "reference", "earlier", "themes", "log"):
            self.assertTrue((out / legacy / "index.html").is_file())
        expected = [("/wiki/", "Home"), ("/wiki/results/", "Results"), ("/wiki/literature/", "Literature"), ("/wiki/meetings/", "Meetings"),
                    ("/wiki/papers/", "Papers"), ("/wiki/masking/", "Masking"), ("/wiki/code/", "Code &amp; guides")]
        for page in out.rglob("index.html"):
            markup = page.read_text()
            navigation = re.search(r'<ul class="primary-nav">(.*?)</ul>', markup)[1]
            self.assertEqual(re.findall(r'<a href="([^"]+)">([^<]+)</a>', navigation), expected)
            self.assertNotIn("Liu Hao · DR2 quiescent galaxies", markup)

    def test_default_model_is_superseded_by_the_literature_page(self):
        for name in ("default-fit-parameters.md", "papers-quiescent-parameters.md"):
            (self.notes / name).write_text((WIKI / "notes" / name).read_text())
        for base in ("/wiki", ""):
            with self.subTest(base=base):
                out = self.build(base)
                code = (out / "code/index.html").read_text()
                old = (out / "n/default-fit-parameters/index.html").read_text()
                literature = (out / "literature/index.html").read_text()
                note = (out / "n/papers-quiescent-parameters/index.html").read_text()
                self.assertNotIn('class="default-model"', code)
                history = re.search(r'<details class="research-history">(.*?)</details>', code, re.S)[1]
                self.assertIn(base + "/n/default-fit-parameters/", history)
                self.assertIn('<div class="banner">Superseded by <a href="%s/n/papers-quiescent-parameters/">'
                              'Literature values: LEGA-C quiescent galaxies</a></div>' % base, old)
                self.assertEqual(len(re.findall(r'<table\b', literature)), 8)
                self.assertIn('id="references"', note)
                self.assertIn('<img src="%s/figures/papers-quiescent-parameters/literature-vs-ceridwen.png"' % base, note)
                search = json.loads((out / "search.json").read_text())
                self.assertTrue(any(item["u"] == base + "/n/papers-quiescent-parameters/" for item in search))

    def test_html_parameter_tables_share_markdown_table_budget_exemption(self):
        table = '<table><tbody><tr><td>' + 'value ' * 70 + '</td></tr></tbody></table>'
        self.assertEqual(build.body_words('Visible prose.\n' + table), 2)
        self.assertGreater(build.body_words('Visible prose.\n' + 'value ' * 70), build.BODY_WORD_CAP)

    def test_light_edit_preserves_original_and_does_not_render_markup(self):
        edited = "I think this might help, but I am not sure. <b>literal</b>"
        message = dict(self.message, display_text=edited)
        self.write("question", "q-dust", "open", {"Your words": [message]})
        body = (self.build() / "q/q-dust/index.html").read_text()
        parser = Quotes()
        parser.feed(body)
        self.assertEqual(parser.values, [self.original])
        self.assertIn("Liu Hao · lightly edited", body)
        self.assertIn("Original wording", body)
        self.assertIn("might help, but I am not sure. &lt;b&gt;literal&lt;/b&gt;", body)
        self.assertNotIn("<b>literal</b>", body)
        self.assertEqual(next(r for r in self.load() if r["kind"] == "question")["sections"]["Your words"][0]["text"], self.original)

    def historical(self):
        source = self.project / "old-result.csv"
        source.write_text("age_Gyr\n3.0\n")
        refs = "[Saved table](old-result.csv)."
        self.evidence()
        self.write("question", "q-history", "open", {
            "Context": "An existing comparison.", "References": refs,
        }, origin="existing")
        self.write("experiment", "e-history", "recorded", {
            "Context": "The source records the original comparison.",
            "References": refs, "Results": "Recorded age: 3.0 Gyr. " + refs,
            "Figures": [{"path": "results/e-low-dust/fit.png", "view": "Fits", "caption": "Saved historical fit."}],
            "Runs": [{"id": "old-fit", "arm": "original", "status": "complete",
                      "artifacts": [{"label": "Saved result", "path": "old-result.csv"}]}],
        }, origin="existing", question="q-history", related_questions="q-dust")

    def test_existing_evidence_needs_no_invented_brief_notebook_or_seed(self):
        self.historical()
        self.assertEqual(self.faults(), [])
        out = self.build()
        body = (out / "e/e-history/record/index.html").read_text()
        self.assertNotIn("Existing research · organised from saved records", body)
        self.assertIn("The source records the original comparison.", body)
        self.assertIn("Recorded age: 3.0 Gyr", body)
        self.assertNotIn("Before delegation", body)
        self.assertNotIn("Not recorded", body)
        self.assertIn("e-history", (out / "q/q-history/index.html").read_text())
        self.assertIn("e-history", (out / "q/q-dust/index.html").read_text())
        home = (out / "index.html").read_text()
        self.assertNotIn("e-history", home)
        self.assertIn("e-history", (out / "results/index.html").read_text())
        self.assertIn("e-history", (out / "experiments/index.html").read_text())
        search = json.loads((out / "search.json").read_text())
        self.assertTrue(any(r["s"] == "Experiment" and "e-history" in r["u"] for r in search))

    def test_existing_exceptions_do_not_relax_new_experiments(self):
        self.historical()
        record = next(r for r in self.load() if r.get("id") == "e-history")
        self.write("experiment", "e-history", "recorded", record["sections"], question="q-history")
        faults = "\n".join(self.faults())
        self.assertIn("recorded status is only for existing research", faults)
        self.assertIn("before-delegation words", faults)
        self.assertIn("executed notebook", faults)
        self.assertIn("integer seed", faults)

    def test_existing_record_still_needs_sources_and_cannot_review_itself(self):
        self.historical()
        record = next(r for r in self.load() if r.get("id") == "e-history")
        record["sections"]["References"] = "No evidence link."
        self.write("experiment", "e-history", "reviewed", record["sections"], question="q-history", origin="existing")
        faults = "\n".join(self.faults())
        self.assertIn("existing records require a source link", faults)
        self.assertIn("reviewed requires your recorded interpretation", faults)

    def test_source_notes_link_both_ways_and_missing_crosslinks_fail(self):
        self.historical()
        (self.notes / "source.md").write_text("---\ntitle: Source\ndate: 2026-09-01\nsection: Analyses\ntheme: Population results\n---\n\nSaved source.\n")
        r = next(r for r in self.load() if r.get("id") == "e-history")
        r["sections"]["References"] += " [Original note](wiki/notes/source.md)."
        self.write("experiment", "e-history", "recorded", r["sections"], question="q-history", origin="existing", source_notes="source")
        out = self.build()
        self.assertIn('href="/wiki/n/source/"', (out / "e/e-history/record/index.html").read_text())
        self.assertIn('href="/wiki/e/e-history/"', (out / "n/source/index.html").read_text())
        self.write("experiment", "e-history", "recorded", r["sections"], question="q-history", origin="existing", related_questions="q-missing", source_notes="missing")
        faults = "\n".join(self.faults())
        self.assertIn("related_questions", faults)
        self.assertIn("missing evidence file", faults)

    def test_display_edit_requires_a_nonempty_string(self):
        self.write("question", "q-dust", "open", {"Your words": [dict(self.message, display_text=[])]})
        self.assertIn("display_text must be a nonempty string", "\n".join(self.faults()))

    def test_result_page_shows_figures_and_keeps_reasoning_in_record(self):
        self.completed()
        out = self.build()
        report = (out / "e/e-low-dust/index.html").read_text()
        for unwanted in ("Agent ·", "Before delegation", "Execution plan", "source summary", "Age shift: 0.12"):
            self.assertNotIn(unwanted, report)
        self.assertIn('<img src="/wiki/f/results/e-low-dust/fit.png"', report)
        self.assertIn("Two fixed configurations.", report)
        self.assertIn('/wiki/e/e-low-dust/record/', report)
        record = (out / "e/e-low-dust/record/index.html").read_text()
        self.assertIn("Age shift: 0.12", record)
        self.assertIn(self.original.replace("<", "&lt;").replace(">", "&gt;").replace(" & ", " &amp; "), record)

    def notebook_figure(self):
        sections = self.completed()
        run = sections["Runs"][0]
        run["target"] = "M1_1"
        png = (self.project / "results/e-low-dust/fit.png").read_bytes()
        notebook = self.project / run["artifacts"][0]["path"]
        notebook.write_text(json.dumps({"cells": [{"cell_type": "code", "source": ["raise RuntimeError('Do not execute')"],
            "outputs": [{"output_type": "display_data", "data": {"image/png": base64.b64encode(png).decode()}}]}]}))
        sections["Figures"] = [{"notebook": run["artifacts"][0]["path"], "cell": 0, "output": 0,
            "run": run["id"], "target": run["target"], "arm": run["arm"], "view": "Fits", "caption": "M1_1: saved spectrum."}]
        return sections, png

    def test_saved_image_is_copied_exactly_without_execution(self):
        sections, png = self.notebook_figure()
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        self.assertEqual(self.faults(), [])
        out = self.build()
        image = out / "research-images/results/e-low-dust/analysis/c0-o0.png"
        self.assertEqual(image.read_bytes(), png)
        self.assertIn('research-images/results/e-low-dust/analysis/c0-o0.png', (out / "e/e-low-dust/index.html").read_text())

    def test_wrong_target_arm_notebook_and_output_are_rejected(self):
        sections, _ = self.notebook_figure()
        for field, bad, message in (("target", "M2_2", "target and arm"), ("arm", "other", "target and arm"),
                                     ("output", 9, "saved PNG"), ("run", "missing", "identified run")):
            original = sections["Figures"][0][field]
            sections["Figures"][0][field] = bad
            self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
            self.assertIn(message, "\n".join(self.faults()))
            sections["Figures"][0][field] = original

    def test_all_targets_stay_available_without_loading_hidden_images(self):
        sections = self.completed()
        sections["Figures"] = [dict(sections["Figures"][0], target=target, view=view)
                               for target in ("M1_1", "M2_2") for view in ("Fits", "SFH")]
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        body = (self.build() / "e/e-low-dust/index.html").read_text()
        self.assertIn('<option value="M2_2">', body)
        self.assertIn('<option value="SFH">', body)
        self.assertEqual(body.count('<img src='), 1)
        self.assertEqual(body.count('<img data-src='), 3)

    def test_completed_results_need_visuals_or_benchmark_measurements(self):
        sections = self.completed()
        sections["Figures"] = []
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        self.assertIn("result page needs figures", "\n".join(self.faults()))
        sections["Measurements"] = "| Metric | Value |\n| --- | --- |\n| Time | 1 s |"
        self.write("experiment", "e-low-dust", "results-ready", sections, question="q-dust")
        self.assertEqual(self.faults(), [])
        body = (self.build() / "e/e-low-dust/index.html").read_text()
        self.assertIn("<table>", body)
        self.assertNotIn("Agent ·", body)


class ExistingCorpusTests(unittest.TestCase):
    def test_existing_analyses_and_result_groups_are_integrated(self):
        records, faults = research.load(WIKI / "research")
        self.assertEqual(faults, [])
        self.assertEqual(research.validate(records, WIKI.parent), [])
        experiments = [r for r in records if r["kind"] == "experiment"]
        linked = {slug for r in experiments for slug in research.refs(r, "source_notes")}
        analyses = {p.stem for p in (WIKI / "notes").glob("*.md") if "\nsection: Analyses\n" in p.read_text()}
        self.assertEqual(analyses - linked, set())
        groups = {g for r in experiments for g in research.refs(r, "result_groups")}
        expected = {str(p.relative_to(WIKI.parent)) for parent in [WIKI.parent / "results", WIKI.parent / "archive/results"]
                    for p in parent.iterdir() if p.is_dir() and not p.name.startswith(".")}
        self.assertEqual(expected - groups, set())
        self.assertTrue(all(r["status"] == "recorded" for r in experiments if r.get("origin") == "existing"))


if __name__ == "__main__":
    unittest.main()
