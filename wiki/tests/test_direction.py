"""Authoring and publication use isolated canonical sources, never the live roadmap."""
import json
import shutil
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
sys.path[:0] = [str(WIKI), str(WIKI.parent / "scripts")]
import activity
import build
import direction
import research
import serve_wiki as server
import sync_wiki_direction as sync
import publish_wiki as publisher


class DirectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "local"
        self.root = self.project / "wiki/research"
        self.root.mkdir(parents=True)
        sections = {"Your words": [{"date": "2026-09-12", "text": "Maybe alpha enhancement?\n  Keep my spacing.",
                                    "display_text": "Maybe alpha enhancement? Keep my spacing."}],
                    "Roadmap": [{"id": "metals", "title": "Check metallicity", "priority": 10,
                                 "source": "wiki/research/direction.md"},
                                {"id": "spectra", "title": "Check spectra", "priority": None,
                                 "source": "wiki/research/direction.md", "depends_on": ["metals"]}],
                    "Amendments": [{"date": "2026-09-13", "text": "Original priorities."}]}
        raw = "---\nkind: direction\nid: research-direction\ntitle: Research direction\ndate: 2026-09-12\n---\n"
        for name, entries in sections.items():
            raw += "\n## " + name + "\n\n```json\n" + json.dumps(entries) + "\n```\n"
        raw += "\n## References\n\n"
        (self.root / "direction.md").write_text(raw)

    def payload(self, **kwargs):
        return {"id": "save-one", "revision": direction.snapshot(self.root)["revision"],
                "kind": "priority", "title": "Check abundances", "priority": 8, **kwargs}

    def test_create_edit_history_retry_and_noop(self):
        original = direction.snapshot(self.root)
        payload = self.payload(details="Is this iron?", effort="Small", depends_on=["metals"])
        first = direction.save(self.root, payload)
        new = first["priorities"][-1]
        self.assertEqual(new["id"], "p-save-one")
        self.assertEqual(new["depends_on"], ["metals"])
        self.assertEqual(first, direction.save(self.root, payload))
        edited = direction.save(self.root, self.payload(id="save-two", target=new["id"], priority=None))
        self.assertEqual(edited["history"][-1]["before"], new)
        self.assertEqual(edited["history"][:-2], original["history"])
        self.assertEqual(edited["history"][-1]["text"], "Check abundances")
        self.assertEqual(edited, direction.save(self.root, self.payload(id="noop", target=new["id"], priority=None)))

    def test_direction_originals_multiline_and_heading(self):
        original = direction.snapshot(self.root)["direction"][0]
        edited = direction.save(self.root, self.payload(kind="direction", target=original["id"],
                               title="Abundances", text="Could this work?\n\n  I am not sure. "))
        self.assertEqual(edited["direction"][0]["text"], "Could this work?\n\n  I am not sure. ")
        self.assertNotIn("display_text", edited["direction"][0])
        self.assertEqual(edited["history"][-1]["before"]["text"], original["text"])
        self.assertEqual(edited["history"][-1]["before"]["display_text"], original["display_text"])
        created = direction.save(self.root, self.payload(id="add-direction", kind="direction", title="Next question", text="What about age?"))
        self.assertEqual(len(created["direction"]), 2)
        self.assertEqual(created["direction"][-1]["title"], "Next question")
        self.assertEqual(direction.snapshot(self.root), created)

    def test_validation_leaves_source_unchanged(self):
        before = (self.root / "direction.md").read_bytes()
        invalid = [{"title": ""}, {"priority": 11}, {"priority": True}, {"priority": "9"},
                   {"depends_on": ["missing"]}, {"target": "metals", "depends_on": ["spectra"]},
                   {"title": "word " * 31}, {"kind": "direction", "text": "  "},
                   {"kind": "direction", "text": 123}, {"target": "missing"}]
        for fields in invalid:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                direction.save(self.root, self.payload(**fields))
            self.assertEqual((self.root / "direction.md").read_bytes(), before)

    def test_two_sessions_only_one_save_and_retry_id_cannot_change(self):
        a = self.payload()
        b = {**a, "id": "save-two", "title": "Different wording"}
        def attempt(payload):
            try:
                return direction.save(self.root, payload)
            except activity.Conflict:
                return "conflict"
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(attempt, [a, b]))
        self.assertEqual(results.count("conflict"), 1)
        self.assertEqual(len(direction.snapshot(self.root)["priorities"]), 3)
        winner = a if results[0] != "conflict" else b
        with self.assertRaises(activity.Conflict):
            direction.save(self.root, {**winner, "title": "Retry changed"})

    def test_resolution_and_notes_unchanged(self):
        records, _ = research.load(self.root)
        activity.save(self.root, self.project, records, "priority", "metals", {"id": "note-one", "action": "note", "text": "Still uncertain."})
        activity.save(self.root, self.project, records, "priority", "metals", {"id": "state-one", "action": "state", "state": "resolved", "expected_state": "open"})
        before = activity.snapshot(self.root, "priority", "metals")
        direction.save(self.root, self.payload(target="metals"))
        self.assertEqual(activity.snapshot(self.root, "priority", "metals"), before)
        self.assertEqual(direction.snapshot(self.root)["states"]["metals"], "resolved")

    def remote_fixture(self):
        remote = Path(self.temp.name) / "remote/wiki/research"
        shutil.copytree(self.root, remote)
        exchange = lambda payload: direction.source_exchange(remote, payload)
        sync.synchronize(self.project, exchange)
        return remote, exchange

    def test_browser_save_then_publish_pulls_canonical_and_preserves_history(self):
        remote, exchange = self.remote_fixture()
        saved = direction.save(remote, self.payload(kind="direction", text="My browser direction.", title="New section"))
        sync.synchronize(self.project, exchange)
        self.assertEqual(direction.snapshot(self.root), saved)
        # Local agents use the same revision-checked save after synchronization.
        direction.save(self.root, self.payload(id="local-one"))
        sync.synchronize(self.project, exchange)
        self.assertEqual((remote / "direction.md").read_bytes(), (self.root / "direction.md").read_bytes())
        with patch.object(publisher, "run") as run:
            self.assertEqual(publisher.push_some([publisher.DIRECTION]), 0)
            run.assert_not_called()
        self.assertIn("--exclude=/research/direction.md", publisher.SOURCE_EXCLUDES)

    def test_save_then_actual_build_keeps_direction_priority_and_activity(self):
        (self.project / "wiki/notes").mkdir()
        (self.project / "wiki/themes.md").write_text("")
        direction.save(self.root, self.payload())
        direction.save(self.root, self.payload(id="direction-new", kind="direction", text="My exact question?\n  Still uncertain."))
        direction.save(self.root, self.payload(id="priority-edit", target="p-save-one", title="Revised priority", priority=None))
        records, _ = research.load(self.root)
        activity.save(self.root, self.project, records, "priority", "p-save-one", {"id": "saved-note", "action": "note", "text": "Preserve this annotation."})
        activity.save(self.root, self.project, records, "priority", "p-save-one", {"id": "saved-resolution", "action": "state", "state": "resolved", "expected_state": "open"})
        before = direction.snapshot(self.root)
        notes = activity.snapshot(self.root, "priority", "p-save-one")
        output = self.project / "wiki/public"
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.project / "wiki/notes", output, "", self.root), 0)
        self.assertEqual(direction.snapshot(self.root), before)
        self.assertEqual(activity.snapshot(self.root, "priority", "p-save-one"), notes)
        home = (output / "index.html").read_text()
        detail = (output / "p/p-save-one/index.html").read_text()
        self.assertIn("Revised priority", home)
        self.assertIn("My exact question?", home)
        self.assertIn("Revised priority", detail)
        self.assertIn("Preserve this annotation.", detail)
        self.assertIn("Marked resolved", detail)

    def test_both_changed_conflict_and_publish_race_retain_both(self):
        remote, exchange = self.remote_fixture()
        a = self.payload()
        direction.save(remote, a)
        direction.save(self.root, {**a, "id": "local-two", "title": "Local words"})
        local, server_source = (self.root / "direction.md").read_bytes(), (remote / "direction.md").read_bytes()
        with self.assertRaises(activity.Conflict):
            sync.synchronize(self.project, exchange)
        self.assertEqual((self.root / "direction.md").read_bytes(), local)
        self.assertEqual((remote / "direction.md").read_bytes(), server_source)

    def test_remote_change_between_read_and_publish_cas(self):
        remote, exchange = self.remote_fixture()
        base = direction.snapshot(remote)["revision"]
        direction.save(self.root, self.payload())
        def raced(payload):
            if "source" in payload:
                direction.save(remote, {"id": "browser-race", "revision": base, "kind": "direction", "text": "New browser words"})
            return exchange(payload)
        with self.assertRaises(activity.Conflict):
            sync.synchronize(self.project, raced)
        self.assertEqual(direction.snapshot(remote)["direction"][-1]["text"], "New browser words")
        self.assertEqual(direction.snapshot(self.root)["priorities"][-1]["title"], "Check abundances")

    def test_raw_sync_cannot_remove_history(self):
        old = (self.root / "direction.md").read_text()
        direction.save(self.root, self.payload())
        with self.assertRaises(activity.Conflict):
            direction.source_exchange(self.root, {"revision": direction.snapshot(self.root)["revision"], "source": old})
        raw, parts = direction.read(self.root)
        parts["Roadmap"][0]["title"] = "Stale editor wording"
        stale = direction.section(raw, "Roadmap", parts["Roadmap"])
        with self.assertRaises(activity.Conflict):
            direction.source_exchange(self.root, {"revision": direction.revision(raw), "source": stale})

    def test_http_save_reload_validation_conflict_and_origin(self):
        handler = type("FixtureHandler", (server.AstroWikiHandler,), {"project_root": self.project, "log_message": lambda *args: None})
        httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(httpd.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(httpd.shutdown)
        host = f"http://127.0.0.1:{httpd.server_port}"
        def post(payload, origin=host):
            request = urllib.request.Request(host + "/api/direction", data=json.dumps(payload).encode(), headers={"Origin": origin, "Content-Type": "application/json"})
            return urllib.request.urlopen(request)
        payload = self.payload()
        with self.assertRaises(urllib.error.HTTPError) as e:
            post(payload, "https://other.example")
        self.assertEqual(e.exception.code, 403)
        e.exception.close()
        with patch.object(server.publication, "request"), post(payload) as response:
            saved = json.load(response)
        with urllib.request.urlopen(host + "/api/direction") as response:
            self.assertEqual(json.load(response), saved)
        # A new detail route works before any static publication completes.
        with urllib.request.urlopen(host + "/p/p-save-one/") as response:
            self.assertIn("Check abundances", response.read().decode())
        with self.assertRaises(urllib.error.HTTPError) as e:
            post({**payload, "id": "stale"})
        self.assertEqual(e.exception.code, 409)
        e.exception.close()
        with self.assertRaises(urllib.error.HTTPError) as e:
            post(self.payload(id="invalid", priority=0))
        self.assertEqual(e.exception.code, 400)
        e.exception.close()


if __name__ == "__main__":
    unittest.main()
