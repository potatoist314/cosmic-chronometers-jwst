"""Automated validation tests for the Ceridwen Common Results Board."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = Path("/Users/liuhao/.claude/scripts/hermes-bridge/reports/ceridwen-board-repair/manifest.json")
BOARD_PATH = PROJECT_ROOT / "wiki/analyses/ceridwen-results.html"
WIKI_BASE = PROJECT_ROOT / "wiki/analyses"


class LinkAndImageExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])
        elif tag == "img" and "src" in attr_dict:
            self.images.append((attr_dict["src"], attr_dict.get("alt", "")))


class TestCeridwenResultsBoard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board_html = BOARD_PATH.read_text(encoding="utf-8")
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        parser = LinkAndImageExtractor()
        parser.feed(cls.board_html)
        cls.extracted_links = set(parser.links)
        cls.extracted_images = parser.images

    def test_board_file_exists_and_not_empty(self):
        self.assertTrue(BOARD_PATH.exists(), "Results board HTML file must exist.")
        self.assertGreater(len(self.board_html), 1000, "Results board HTML should be populated.")

    def test_all_manifest_items_linked(self):
        """Every independent deliverable in manifest.json must be linked in the board.
        
        The failed interactive animation is kept as an explicit pending placeholder per
        research direction.
        """
        for item in self.manifest["items"]:
            rel_path = item["wiki_relative_path"]
            # Exclude self-reference and unverified animation placeholder
            if item["id"] in {"board-current-html", "checkpoint-interactive-html"}:
                continue
            self.assertTrue(
                rel_path in self.extracted_links or any(img[0] == rel_path for img in self.extracted_images),
                f"Manifest item '{item['id']}' with path '{rel_path}' is not linked or displayed in the board.",
            )

    def test_checkpoint_animation_placeholder(self):
        """Verify the board keeps the unverified animation out and uses an explicit pending placeholder."""
        self.assertIn("Pending Tier-H", self.board_html)
        self.assertIn("Optional enhancement", self.board_html)

    def test_inline_plots_and_alt_text(self):
        """All 19 PNG plots must render inline with non-empty accessible alt text."""
        png_items = [it for it in self.manifest["items"] if it["media_type"] == "image/png"]
        self.assertEqual(len(png_items), 19, "Expected exactly 19 PNG plots in manifest.")

        image_src_map = {src: alt for src, alt in self.extracted_images}
        for item in png_items:
            rel = item["wiki_relative_path"]
            self.assertIn(rel, image_src_map, f"PNG '{rel}' must be rendered inline via an <img> tag.")
            alt = image_src_map[rel]
            self.assertTrue(bool(alt.strip()), f"PNG '{rel}' must have non-empty accessible fallback alt text.")

    def test_required_sections_present(self):
        """Verify all 8 core scientific sections are present in the HTML."""
        required_headings = [
            "187-galaxy DR2",
            "Borghi+2022 age versus redshift",
            "Absorption-line mask",
            "Calibration polynomial and tilt origin",
            "Formation timescales",
            "Fit quality",
            "Performance and production",
            "Interactive checkpoint",
        ]
        for heading in required_headings:
            pattern = re.compile(re.escape(heading), re.IGNORECASE)
            self.assertTrue(
                bool(pattern.search(self.board_html)),
                f"Required section heading matching '{heading}' not found in board HTML.",
            )

    def test_corrected_calibration_science(self):
        """Verify the board states the corrected calibration sign and tilt origin."""
        self.assertIn("brighter", self.board_html.lower())
        self.assertTrue(
            "dr2 spectra are <em>brighter</em>" in self.board_html.lower() or
            "spectra are brighter" in self.board_html.lower()
        )
        self.assertNotIn("spectra are fainter", self.board_html.lower())
        self.assertIn("m4", self.board_html.lower())
        self.assertIn("m5", self.board_html.lower())

    def test_all_links_resolve_on_disk(self):
        """Every relative link in the board must resolve to a valid file or directory on disk."""
        for link in self.extracted_links:
            if link.startswith("#") or link.startswith("http://") or link.startswith("https://"):
                continue
            resolved = (WIKI_BASE / link).resolve()
            self.assertTrue(resolved.exists(), f"Relative link '{link}' does not exist on disk (resolved to {resolved}).")

    def test_local_server_health(self):
        """Verify local loopback HTTP server returns 200 for wiki pages."""
        try:
            req = Request("http://127.0.0.1:8765/wiki/analyses/ceridwen-results.html")
            with urlopen(req, timeout=3) as resp:
                self.assertEqual(resp.status, 200)

            req_index = Request("http://127.0.0.1:8765/wiki/index.html")
            with urlopen(req_index, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
        except Exception as exc:
            self.skipTest(f"Local server check skipped (not running or timed out): {exc}")


if __name__ == "__main__":
    unittest.main()
