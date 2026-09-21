"""The publish-time length check: roadmap items over 30 words and paragraphs over 60 stop the build."""

import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("wiki_build", WIKI / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

LONG = " ".join("w%d" % i for i in range(61))
NOTE = """---
title: Long
date: 2026-09-21
---

# Heading words are not counted at all

| a table | row |
| --- | --- |

```
%s fenced text is not counted
```

<details>
<summary>%s html block</summary>

- first item %s
- second item of the same list

Short paragraph.
%s
""" % (LONG, LONG, LONG, LONG)


class LengthTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.wiki = self.root / "wiki"
        (self.wiki / "notes").mkdir(parents=True)
        (self.wiki / "research/templates").mkdir(parents=True)
        (self.wiki / "notes/long.md").write_text(NOTE, encoding="utf-8")
        (self.wiki / "research/README.md").write_text(LONG + "\n", encoding="utf-8")
        (self.wiki / "research/templates/experiment.md").write_text(LONG + "\n", encoding="utf-8")
        self.records = [{"kind": "direction", "path": self.wiki / "research/direction.md", "sections": {"Roadmap": [
            {"id": "short", "title": "Five words in this title", "details": " ".join(["d"] * 25), "effort": LONG},
            {"id": "long", "title": "Five words in this title", "details": " ".join(["d"] * 26)}]}}]

    def test_paragraphs_skip_frontmatter_fences_tables_html_and_headings(self):
        found = build.paragraphs(NOTE)
        self.assertEqual([(line, text.split()[:2]) for line, text in found],
                         [(18, ["-", "first"]), (19, ["-", "second"]), (21, ["Short", "paragraph."])])

    def test_faults_name_the_task_or_line_and_the_cap(self):
        self.assertEqual(build.length_faults(self.wiki, self.records), [
            "wiki/research/direction.md: long: 31 words (cap 30)",
            "wiki/notes/long.md: 18: 64 words (cap 60)",
            "wiki/notes/long.md: 21: 63 words (cap 60)"])

    def test_baseline_passes_old_violations_until_they_grow(self):
        (self.wiki / build.LENGTH_BASELINE).write_text(
            "wiki/research/direction.md\tlong\t31\nwiki/notes/long.md\t- first item w0 w1 w2\t64\n"
            "wiki/notes/long.md\tShort paragraph. w0 w1 w2 w3\t62\n", encoding="utf-8")
        self.assertEqual(build.length_faults(self.wiki, self.records), ["wiki/notes/long.md: 21: 63 words (cap 60)"])

    def test_check_prints_every_fault_and_stops_the_build(self):
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as stop:
            build.check_lengths(self.wiki, self.records)
        self.assertEqual(stderr.getvalue().count("(cap "), 3)
        self.assertIn("3 length fault(s)", str(stop.exception))


if __name__ == "__main__":
    unittest.main()
