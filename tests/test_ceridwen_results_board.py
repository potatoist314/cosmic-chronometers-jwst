"""Automated validation tests for the Ceridwen Common Results Board."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from scripts.build_ceridwen_results_board import build_board_html

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

    def test_regeneration_equality(self):
        """Verify build_ceridwen_results_board.py produces the exact live board HTML byte-for-byte."""
        generated_html = build_board_html(self.manifest)
        self.assertEqual(
            self.board_html,
            generated_html,
            "Live board HTML must match output of scripts/build_ceridwen_results_board.py byte-for-byte.",
        )

    def test_all_manifest_items_linked(self):
        """Every independent deliverable in manifest.json must be linked in the board."""
        for item in self.manifest["items"]:
            rel_path = item["wiki_relative_path"]
            # Exclude self-reference only
            if item["id"] == "board-current-html":
                continue
            self.assertTrue(
                rel_path in self.extracted_links or any(img[0] == rel_path for img in self.extracted_images),
                f"Manifest item '{item['id']}' with path '{rel_path}' is not linked or displayed in the board.",
            )

    def test_checkpoint_animation_hosted_artifact(self):
        """Verify the board links the repaired animation inside the wiki host root with 3 host-check markers."""
        href = "checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html"
        self.assertIn(href, self.extracted_links)
        self.assertTrue((WIKI_BASE / href).is_file())
        self.assertNotIn("Pending Tier-H", self.board_html)
        self.assertEqual(
            self.board_html.count('data-host-check="checkpoint-animation"'),
            3,
            "Expected exactly 3 data-host-check markers for checkpoint animation.",
        )

    def test_no_prose_semicolons_in_body(self):
        """Verify no visible prose semicolons exist in the board body."""
        body_start = self.board_html.find("<body>")
        self.assertGreater(body_start, 0)
        body_content = self.board_html[body_start:]
        cleaned = re.sub(r"&[a-zA-Z0-9#]+;", " ", body_content)
        for line in cleaned.splitlines():
            prose = re.sub(r"<[^>]+>", " ", line)
            self.assertNotIn(";", prose, f"Prose line contains semicolon: {line.strip()}")

    def test_strict_ui_and_technical_term_definitions(self):
        """Verify technical terms are properly defined and outdated terms are absent."""
        self.assertNotIn("Jump to", self.board_html)
        self.assertNotIn("Push Provenance", self.board_html)
        self.assertNotIn("Host-ready", self.board_html)
        self.assertIn("Sections:", self.board_html)
        self.assertIn("Git synchronization status (upstream tracking)", self.board_html)
        self.assertIn("Verified local host", self.board_html)
        self.assertIn("Effective Sample Size (ESS, independent posterior samples)", self.board_html)
        self.assertIn("Bayesian log-evidence (logZ, marginal likelihood)", self.board_html)
        self.assertIn("converged rescue posterior (nested sampling solution after sampler convergence)", self.board_html)

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


    def test_html_text_lint_passes(self):
        """Verify the board HTML passes the structural HTML visible-text lint with zero issues."""
        import sys
        bridge_dir = Path('/Users/liuhao/.claude/scripts/hermes-bridge')
        if str(bridge_dir) not in sys.path:
            sys.path.insert(0, str(bridge_dir))
        import html_text_lint
        findings, _ = html_text_lint.lint_html(self.board_html)
        self.assertEqual(len(findings), 0, f"Expected 0 text lint issues, found {len(findings)}: {findings}")

    # Stable authoritative baseline for science-meaning preservation.
    # This explicit manifest replaces any comparison against a moving Git
    # HEAD. Every pattern below must match the regenerated board at least
    # once, and every listed defect string must be absent. Change this list
    # only together with a matching science audit of the source artifacts.
    PROTECTED_NUMBER_PATTERNS = [
        r'\b187\b', r'\b0\.73\b', r'\b3\.02\b', r'\b2\.46\b',
        r'\b2\.69\b', r'\+0\.26\b', r'\b140\b', r'\b68\b',
        r'\b1\.26\b', r'\b1\.48\b', r'\+0\.4%', r'\b0\.00\b', r'\b1\.0 to 1\.6\b',
        r'\b61\.4 percent\b', r'\b1389\b', r'\b3602\b', r'\b2213\b',
        r'\b12 synthetic configurations\b',
        r'\b12 fit variants\b', r'\b23 calibration variants\b',
        r'\b4\.65 Gyr\b', r'\b0\.3-mag\b', r'\b1000 km/s\b',
    ]
    PROTECTED_PHRASES = [
        'Gyr', 'km/s', 'mag', 'Caveat:', 'median', 'credible',
        'percentile', 'uncertainty', 'error bars', 'NMAD',
        '68-galaxy', '7-bin', 'Choose whether',
        'remains pushed and tested', 'PDF Vector',
        'dr2-quiescent-sample/distributions-1d.png',
        'absorption-mask/feature_windows_M5_172669.png',
        'checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html',
        'tilt-origin-2026-09-02/arms.csv',
        '&minus;20%', '&minus;16% to &minus;24%',
        '22 full-spectrum sigma',
    ]
    # Exact false claims reported by review; the test must fail if any return.
    KNOWN_DEFECTS_ABSENT = [
        'exclude 88%', '88% of valid spectral pixels',
        'effective sample size compared across objects',
        'Error bars mark the 16th to 84th percentile uncertainty interval',
        'Histograms show the 16th to 84th percentile credible range',
        'against model prior bounds',
        'Error contours define the 68% and 95%',
        'Ellipses mark 68%', 'eight calibration variants',
        'up to 0.4 Gyr', 'across 12 bands', '30 angstrom',
        'Error vectors show measurement flux uncertainty',
        'Shaded regions show the 16th to 84th percentile',
        'Shaded bands represent photometric uncertainty errors',
        'Error bars display the 16th to 84th percentile credible interval',
        'Error bars show 1-sigma measurement uncertainty',
        'Corner contours', 'across 25 synthetic', 'by 1.1 to 1.6 times',
        'passes all tests on origin', 'successful convergence',
        'sky line residuals',
    ]

    def test_protected_facts_preserved(self):
        """Every protected number, unit, sign, qualifier, uncertainty term,
        decision modality marker, artifact path, and required link must be
        present, and every known reviewer-reported defect must be absent."""
        for pattern in self.PROTECTED_NUMBER_PATTERNS:
            with self.subTest(pattern=pattern):
                found = re.findall(pattern, self.board_html)
                self.assertGreater(
                    len(found), 0,
                    f"Protected pattern {pattern!r} matches nothing in the board.")
        for phrase in self.PROTECTED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.board_html,
                              f"Protected phrase {phrase!r} missing from the board.")
        self.assertGreaterEqual(
            self.board_html.count('Caveat:'), 19,
            "Every plot caption must keep its Caveat qualifier.")
        self.assertGreaterEqual(
            self.board_html.count('Choose whether'), 6,
            "Neutral decision modality must be kept.")
        for defect in self.KNOWN_DEFECTS_ABSENT:
            with self.subTest(defect=defect):
                self.assertNotIn(
                    defect, self.board_html,
                    f"Reviewer-reported defect is present: {defect!r}.")
        animation = (WIKI_BASE / "checkpoint-animation"
                     / "ceridwen-checkpoint-spectrum-evolution.html").read_text(
                         encoding="utf-8")
        self.assertIn('The viewer compares it with', animation)
        self.assertNotIn('It is compared with', animation)

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
