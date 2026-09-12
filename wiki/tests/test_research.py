"""Prospective research workflow: exact messages, evidence and lifecycle checks."""

import importlib.util
import json
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
        parent = self.root / (kind + "s")
        parent.mkdir(parents=True, exist_ok=True)
        path = parent / (ident + ".md")
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
        return {"id": "baseline-seed-1", "arm": "baseline", "status": "complete",
                "config": "results/e-low-dust/config.json", "code": "fixture-version",
                "model": "fixture-grid-v1", "data": "results/e-low-dust/sample.csv", "seed": 1,
                "artifacts": [{"label": "Executed analysis", "path": "results/e-low-dust/analysis.ipynb"}]}

    def completed(self, status="results-ready", interpretation=None):
        run = self.evidence()
        sections = {"Before delegation": [self.message], "Execution plan": "Compare the two fixed configurations.",
                    "Runs": [run], "Results": "Age shift: 0.12 Gyr. [Table](results/e-low-dust/measurements.csv).",
                    "Your interpretation": interpretation or []}
        self.write("experiment", "e-low-dust", status, sections, question="q-dust")
        return sections

    def build(self, base="/wiki"):
        out = self.project / "public"
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.notes, out, base, self.root), 0)
        return out

    def test_planned_experiment_has_no_fabricated_results(self):
        self.assertEqual(self.faults(), [])
        out = self.build()
        body = (out / "e/e-low-dust/index.html").read_text()
        self.assertIn("Not recorded", body)
        self.assertNotIn("Agent · synthesis", body)
        self.assertNotIn("Chat reference", body)
        self.assertIn("e-low-dust", (out / "q/q-dust/index.html").read_text())

    def test_exact_words_survive_results_interpretation_and_amendment(self):
        sections = self.completed("reviewed", [{"date": "2026-09-13", "text": "inconclusive. keep this open."}])
        sections["Amendments"] = [{"date": "2026-09-13", "text": "correction: use the other sample\n"}]
        sections["Next decision"] = [{"date": "2026-09-13", "text": "try another seed."}]
        self.write("experiment", "e-low-dust", "reviewed", sections, question="q-dust")
        self.assertEqual(self.faults(), [])
        out = self.build()
        parser = Quotes()
        parser.feed((out / "e/e-low-dust/index.html").read_text())
        self.assertEqual(parser.values, [self.original, "correction: use the other sample\n", "inconclusive. keep this open.", "try another seed."])
        self.assertNotIn("<b>literal</b>", (out / "e/e-low-dust/index.html").read_text())

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
        body = (self.build() / "e/e-low-dust/index.html").read_text()
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
        self.assertIn("e-low-dust", (out / "index.html").read_text())

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
        self.assertTrue((out / "e/e-low-dust/index.html").is_file())

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


if __name__ == "__main__":
    unittest.main()
