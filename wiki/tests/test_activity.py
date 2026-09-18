"""Priority history, original ink preservation, and the live write contract."""
import base64
import importlib.util
import json
import re
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

WIKI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WIKI))
import activity
import research
import build

spec = importlib.util.spec_from_file_location("activity_server", WIKI.parent / "scripts/serve_wiki.py")
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)
PIXEL = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a0ioAAAAASUVORK5CYII="


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.root = self.project / "wiki/research"
        self.root.mkdir(parents=True)
        (self.project / "evidence.txt").write_text("Original evidence")
        (self.project / "fit.png").write_bytes(base64.b64decode(PIXEL))
        (self.project / "wiki/notes").mkdir()
        (self.project / "wiki/themes.md").write_text("")
        self.write("direction", "research-direction", {
            "Your words": [{"date": "2026-09-15", "text": "Keep the original question."}],
            "Roadmap": [{"id": "metallicity", "title": "Resolve the metallicity definition", "priority": 10,
                         "source": "evidence.txt", "details": "Is this total metallicity?"},
                        {"id": "spectrum", "title": "Select a strong spectrum", "priority": 7,
                         "source": "evidence.txt", "depends_on": ["metallicity"]}]})
        self.write("question", "q-metals", {"Your words": [{"date": "2026-09-15", "text": "Which abundance?"}]}, status="open")
        self.write("experiment", "e-fit", {"Context": "Saved fit", "References": "[Evidence](evidence.txt)",
                   "Results": "Saved fit", "Figures": [{"path": "fit.png", "caption": "Original fit.", "view": "Fits"}]},
                   status="recorded", origin="existing", question="q-metals")
        self.records, faults = research.load(self.root)
        self.assertEqual(faults, [])

    def write(self, kind, ident, sections, **meta):
        folder = self.root if kind == "direction" else self.root / (kind + "s")
        folder.mkdir(exist_ok=True)
        path = folder / ("direction.md" if kind == "direction" else ident + ".md")
        header = dict(kind=kind, id=ident, title=ident, date="2026-09-15", **meta)
        body = "---\n" + "".join(f"{k}: {v}\n" for k, v in header.items()) + "---\n"
        for title, content in sections.items():
            body += f"\n## {title}\n\n" + ("```json\n" + json.dumps(content) + "\n```" if isinstance(content, list) else content) + "\n"
        path.write_text(body)

    def save(self, payload, kind="priority", ident="metallicity", **kwargs):
        return activity.save(self.root, self.project, self.records, kind, ident, payload, **kwargs)

    def note(self, ident="note-1", **kwargs):
        return {"id": ident, "action": "note", "text": "Maybe [Fe/H], not certain.\n  Preserve this spacing. <script>x</script>", **kwargs}

    def sheet(self, background=None):
        return {"width": 1000, "height": 1300, "strokes": [{"color": "#17212b", "size": 4,
                "points": [[10, 20, 0.2], [30, 40, 0.8]]}],
                "preview": "data:image/png;base64," + PIXEL, **({"background": background} if background else {})}

    def test_annotation_and_resolution_are_independent_and_reopen_keeps_history(self):
        before = (self.root / "direction.md").read_bytes()
        note = self.note(pages=[self.sheet()], evidence=["evidence.txt"])
        self.assertEqual(self.save(note)["state"], "open")
        result = self.save({"id": "resolve-1", "action": "state", "state": "resolved", "expected_state": "open"})
        self.assertEqual(result["entries"][-1]["through_sequence"], 1)
        self.assertNotIn("text", result["entries"][-1])
        self.assertEqual(self.save(self.note("note-2"))["state"], "resolved")
        result = self.save({"id": "reopen-1", "action": "state", "state": "open", "expected_state": "resolved"})
        self.assertEqual(result["state"], "open")
        self.assertEqual(len(result["entries"]), 4)
        self.assertEqual(result["entries"][0]["text"], note["text"])
        self.assertEqual((self.root / "direction.md").read_bytes(), before)
        body = activity.history_html(result["entries"], "/wiki", self.project)
        self.assertIn("&lt;script&gt;", body)
        self.assertNotIn("<script>x", body)

    def test_resolution_requires_no_note_and_retries_are_idempotent(self):
        payload = {"id": "resolve-1", "action": "state", "state": "resolved", "expected_state": "open"}
        self.save(payload)
        self.assertEqual(len(self.save(payload)["entries"]), 1)
        with self.assertRaises(activity.Conflict):
            self.save({**payload, "state": "open"})
        with self.assertRaises(activity.Conflict):
            self.save({**payload, "id": "resolve-2"})
        with self.assertRaises(ValueError):
            self.save(payload, "question", "q-metals")

    def test_revisions_preserve_ink_and_snapshot_background(self):
        original = self.save(self.note(pages=[self.sheet("e-fit:0")]))["entries"][0]
        original_bytes = (self.project / original["pages"][0]["background_path"]).read_bytes()
        (self.project / "fit.png").write_bytes(b"Changed source")
        self.save(self.note("note-2", supersedes="note-1", pages=[self.sheet("saved:note-1:0")]))
        entries = activity.read(self.root, "priority", "metallicity")
        self.assertEqual(entries[0], original)
        self.assertEqual(entries[1]["supersedes"], "note-1")
        self.assertEqual((self.project / entries[1]["pages"][0]["background_path"]).read_bytes(), original_bytes)
        self.assertEqual(entries[0]["pages"][0]["strokes"], self.sheet()["strokes"])

    def test_partial_eraser_operations_preserve_original_ink_and_order(self):
        sheet = self.sheet("e-fit:0")
        original = self.save(self.note(pages=[sheet]))["entries"][0]
        eraser = {"tool": "eraser", "size": 24, "points": [[20, 20, 0.5], [20, 50, 0.5]]}
        later_ink = {"tool": "pen", "color": "#2459b3", "size": 2,
                     "points": [[10, 30, 0.2], [30, 30, 0.8]]}
        sheet["strokes"].extend([eraser, later_ink])
        sheet["background"] = "saved:note-1:0"
        result = self.save(self.note("note-2", supersedes="note-1", pages=[sheet]))
        self.assertEqual(result["state"], "open")
        self.assertEqual(result["entries"][0], original)
        self.assertEqual(result["entries"][1]["pages"][0]["strokes"], sheet["strokes"])
        self.assertEqual(result["entries"][1]["pages"][0]["background_path"],
                         original["pages"][0]["background_path"])

    def test_scribble_gesture_is_preserved_and_only_allowed_for_erasers(self):
        page = self.sheet()
        gesture = {"tool": "eraser", "gesture": "scribble", "size": 24,
                   "points": [[10, 20, 0.5], [50, 25, 0.5], [10, 30, 0.5]]}
        page["strokes"].append(gesture)
        result = self.save(self.note(pages=[page]))
        self.assertEqual(result["entries"][0]["pages"][0]["strokes"][-1], gesture)
        for tool, name in (("pen", "scribble"), ("eraser", "unknown")):
            page["strokes"][-1] = {**gesture, "tool": tool, "gesture": name,
                                    "color": "#17212b", "size": 4 if tool == "pen" else 24}
            with self.assertRaisesRegex(ValueError, "Invalid ink gesture"):
                self.save(self.note("bad-gesture", pages=[page]))

    def test_eraser_validation_uses_eraser_sizes(self):
        for size in (12, 24, 48):
            sheet = self.sheet()
            sheet["strokes"] = [{"tool": "eraser", "size": size, "points": [[10, 20, 0.5]]}]
            self.save(self.note(f"erase-{size}", pages=[sheet]))
        for tool, size in (("eraser", 4), ("pen", 24), ("unknown", 4)):
            sheet = self.sheet()
            sheet["strokes"][0].update(tool=tool, size=size)
            with self.assertRaises(ValueError):
                self.save(self.note(f"invalid-{tool}", pages=[sheet]))

    def test_long_notes_keep_interior_blank_sheets_and_enforce_limit(self):
        pages = [self.sheet() for _ in range(30)]
        pages[1]["strokes"] = []
        result = self.save(self.note(pages=pages))
        self.assertEqual(len(result["entries"][0]["pages"]), 30)
        self.assertEqual(result["entries"][0]["pages"][1]["strokes"], [])
        self.assertEqual(result["entries"][0]["pages"][-1]["strokes"], pages[-1]["strokes"])
        with self.assertRaisesRegex(ValueError, "at most 30"):
            self.save(self.note("too-long", pages=pages + [self.sheet()]))

    def test_readers_cannot_see_an_unpublished_staging_directory(self):
        staging = activity.directory(self.root, "priority", "metallicity") / ".pending-test"
        staging.mkdir(parents=True)
        (staging / "event.json").write_text('{"partially-written":')
        self.assertEqual(activity.read(self.root, "priority", "metallicity"), [])

    def test_failed_save_publishes_no_partial_event(self):
        with self.assertRaises(ValueError):
            self.save(self.note(pages=[self.sheet(), {**self.sheet(), "preview": "bad"}]))
        self.assertEqual(activity.read(self.root, "priority", "metallicity"), [])
        self.assertFalse(list(activity.directory(self.root, "priority", "metallicity").glob(".pending-*")))
        self.assertEqual(len(self.save(self.note())["entries"]), 1)

    def test_unknown_targets_invalid_points_and_paths_are_rejected(self):
        with self.assertRaises(ValueError):
            self.save(self.note(), ident="../direction")
        with self.assertRaises(ValueError):
            self.save(self.note(evidence=["../../outside"]))
        with self.assertRaises(ValueError):
            self.save(self.note(pages=[self.sheet("../../source")]))
        for bad in ([float('nan'), 0, 1], [0, 0, 5], [-1, 20, 0.5]):
            sheet = self.sheet()
            sheet["strokes"][0]["points"] = [bad]
            with self.assertRaises(ValueError):
                self.save(self.note(pages=[sheet]))

    def test_concurrent_chat_and_browser_notes_do_not_overwrite_each_other(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(lambda n: self.save(self.note(f"note-{n}"), origin="chat" if n % 2 else "wiki"), range(12)))
        entries = activity.read(self.root, "priority", "metallicity")
        self.assertEqual([e["sequence"] for e in entries], list(range(1, 13)))
        self.assertEqual(len({e["id"] for e in entries}), 12)
        self.assertEqual({e["origin"] for e in entries}, {"chat", "wiki"})

    def test_rebuild_retains_resolved_anchors_and_searches_notes(self):
        self.save(self.note())
        self.save({"id": "resolve-1", "action": "state", "state": "resolved", "expected_state": "open"})
        self.save(self.note("q-note"), "question", "q-metals")
        out = self.project / "wiki/public"
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.project / "wiki/notes", out, "/wiki", self.root), 0)
        home = (out / "index.html").read_text()
        self.assertEqual(home, (out / "roadmap/index.html").read_text())
        current, resolved = home.split('<summary>Resolved</summary>')
        self.assertIn('id="metallicity"', resolved)
        self.assertEqual(re.findall(r'<input type="checkbox"( checked)?>', resolved), [" checked"])
        self.assertEqual(set(re.findall(r'<input type="checkbox"( checked)?>', current)), {""})
        self.assertIn('href="/wiki/#metallicity"', home)
        self.assertIn('10/10', home)
        self.assertIn('Marked resolved', (out / "p/metallicity/index.html").read_text())
        self.assertIn('data-annotate-figure="e-fit:0"', (out / "e/e-fit/index.html").read_text())
        search = json.loads((out / "search.json").read_text())
        self.assertEqual(sum(self.note()["text"] in r["x"] for r in search), 2)

    def test_api_rejects_cross_origin_and_returns_saved_history(self):
        handler = type("FixtureHandler", (server.AstroWikiHandler,), {
            "project_root": self.project, "log_message": lambda *args: None})
        httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(httpd.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(httpd.shutdown)
        host = f"http://127.0.0.1:{httpd.server_port}"
        endpoint = host + "/api/activity/priority/metallicity"
        def request(origin, body):
            return urllib.request.Request(endpoint, data=json.dumps(body).encode(), headers={"Origin": origin, "Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(request("https://unrelated.example", self.note()))
        self.assertEqual(error.exception.code, 403)
        error.exception.close()
        oversized = request(host, self.note())
        oversized.add_header("Content-Length", str(activity.MAX_REQUEST + 1))
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(oversized)
        self.assertEqual(error.exception.code, 413)
        error.exception.close()
        with patch.object(server.publication, "request"):
            with urllib.request.urlopen(request(host, self.note(pages=[self.sheet()]))) as response:
                result = json.load(response)
        self.assertEqual(result["state"], "open")
        self.assertIn("&lt;script&gt;", result["html"])
        with urllib.request.urlopen(host + "/f/" + result["entries"][0]["pages"][0]["preview"]) as response:
            self.assertEqual(response.read(), base64.b64decode(PIXEL))
        with urllib.request.urlopen(endpoint) as response:
            self.assertEqual(json.load(response)["entries"], result["entries"])
        with urllib.request.urlopen(host + "/api/catalog") as response:
            catalog = json.load(response)
        self.assertEqual(len(catalog["targets"]), 3)
        self.assertEqual(catalog["figures"][0]["key"], "e-fit:0")


if __name__ == "__main__":
    unittest.main()
