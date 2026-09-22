"""Real browser authoring on a disposable wiki.

Set WIKI_PLAYWRIGHT to the installed playwright package directory to run.
WIKI_BROWSER optionally selects a headless Chromium executable.
WIKI_SCREENSHOTS optionally retains responsive screenshots outside the repository.
"""
import os
import shutil
import subprocess
import threading
import unittest
from unittest.mock import patch

import test_direction as fixtures

WIKI, build, server = fixtures.WIKI, fixtures.build, fixtures.server


@unittest.skipUnless(os.environ.get("WIKI_PLAYWRIGHT"), "Set WIKI_PLAYWRIGHT for browser checks")
class DirectionBrowserTests(unittest.TestCase):
    def setUp(self):
        fixtures.DirectionTests.setUp(self)
        (self.project / "wiki/notes").mkdir()
        (self.project / "wiki/themes.md").write_text("")
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.project / "wiki/notes", self.project / "wiki/public", "", self.root), 0)

    def test_browser_save_cancel_validation_conflict_and_responsive_forms(self):
        local_project = self.project.parent / "publisher"
        local_root = local_project / "wiki/research"
        shutil.copytree(self.root, local_root)
        exchange = lambda request: fixtures.direction.source_exchange(self.root, request)
        fixtures.sync.synchronize(local_project, exchange)
        handler = type("BrowserFixtureHandler", (server.AstroWikiHandler,), {
            "project_root": self.project, "log_message": lambda *args: None})
        httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(httpd.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(httpd.shutdown)
        env = {**os.environ, "WIKI_TEST_URL": f"http://127.0.0.1:{httpd.server_port}"}
        # Keep static output stale: reload correctness must come from the save API.
        with patch.object(server.publication, "request"):
            result = subprocess.run(["node", str(WIKI / "tests/test_direction_browser.mjs")],
                                    env=env, text=True, capture_output=True, timeout=180)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        saved = fixtures.direction.snapshot(self.root)
        fixtures.sync.synchronize(local_project, exchange)
        self.assertEqual((local_root / "direction.md").read_bytes(), (self.root / "direction.md").read_bytes())
        with patch.object(build, "PROJECT", self.project):
            self.assertEqual(build.build(self.project / "wiki/notes", self.project / "wiki/public", "", self.root), 0)
        self.assertEqual(fixtures.direction.snapshot(self.root), saved)
        self.assertIn("First browser wording", (self.project / "wiki/public/index.html").read_text())


if __name__ == "__main__":
    unittest.main()
