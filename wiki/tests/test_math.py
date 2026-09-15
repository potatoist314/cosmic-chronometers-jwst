"""Math survives Markdown, stays local, and does not alter literal evidence."""

import html
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WIKI))
import build


class MathTests(unittest.TestCase):
    def test_inline_math_is_not_markdown_or_a_link(self):
        equation = r"\(x_i * y_j * z_k + [a](b) < c\)"
        rendered = build.markdown(equation + " [Source](source.py)", "/wiki")
        self.assertIn(html.escape(equation, quote=False), rendered)
        self.assertNotIn("<em>", rendered)
        self.assertIn('href="/wiki/source.py"', rendered)
        self.assertNotIn('href="/wiki/b"', rendered)

    def test_math_bars_do_not_split_table_columns(self):
        table = "| Quantity | Value |\n| --- | --- |\n| " + r"\(|x|\)" + " | 2 |"
        rendered = build.markdown(table, "/wiki")
        self.assertEqual(rendered.count("<td>"), 2)
        self.assertIn(r"\(|x|\)", rendered)

    def test_multiline_display_math_and_following_text(self):
        equation = "\\[\n\\begin{aligned}\nx &= 1 \\\\\ny &= 2\n\\end{aligned}\n\\]"
        rendered = build.markdown("Before.\n" + equation + "\n\nAfter.", "/wiki")
        self.assertIn('<div class="display-math">' + html.escape(equation, quote=False) + '</div>', rendered)
        self.assertIn("<p>After.</p>", rendered)

    def test_code_currency_and_original_words_stay_literal(self):
        source = r"\(sigma_obs\)" + " costs $0.10 and $0.20"
        rendered = build.markdown("`" + source + "`\n\n```\n" + source + "\n```", "/wiki")
        self.assertIn("<code>" + source + "</code>", rendered)
        self.assertIn("<pre><code>" + source + "</code></pre>", rendered)
        import research
        message = research.messages_html([{"date": "2026-09-15", "text": source}])
        self.assertIn('<blockquote class="verbatim">' + source, message)
        js = (WIKI / "assets/math.js").read_text()
        self.assertIn("'verbatim'", js)
        self.assertIn("'original-message'", js)
        self.assertNotIn("left: '$'", js)
        details = build.markdown('<details class="notes"><summary>Original wording</summary>' + source + '</details>', '/wiki')
        self.assertIn('class="original-source notes"', details)
        self.assertIn('class="q no-math"', build.thread_html([{"q": source, "a": "Recorded."}]))

    def test_figure_alt_text_is_plain_and_caption_keeps_math(self):
        import research_figures
        caption = r"\([\alpha/\mathrm{Fe}]\) posterior"
        record = {"id": "example", "sections": {"Figures": [
            {"path": "plot.png", "view": "Posteriors", "caption": caption}], "Measurements": ""}}
        rendered = research_figures.render(record, WIKI, WIKI, "/wiki", lambda *args: "/wiki/plot.png",
                                          lambda text: text, build.math_text)
        self.assertIn('alt="[alpha/Fe] posterior"', rendered)
        self.assertIn('<figcaption>' + caption + '</figcaption>', rendered)

    def test_search_keeps_readable_abundance_names(self):
        self.assertEqual(build.math_text(r"\([\alpha/\mathrm{Fe}]\)"), "[alpha/Fe]")
        self.assertIn("sigma", build.plain(r"<td>\(\sigma_\star\)</td>"))

    def test_every_shared_page_loads_local_math_assets(self):
        for base in ("/wiki", ""):
            rendered = build.shell("Test", base, "<p>Text</p>", "")
            for asset in ("math.js", "math.css", "vendor/katex-0.18.7/katex.min.js",
                          "vendor/katex-0.18.7/katex.min.css",
                          "vendor/katex-0.18.7/contrib/auto-render.min.js"):
                self.assertIn(base + "/" + asset, rendered)
        vendor = WIKI / "assets/vendor/katex-0.18.7"
        fonts = re.findall(r"url\(([^)]+)\)", (vendor / "katex.min.css").read_text())
        self.assertTrue(fonts)
        self.assertTrue(all((vendor / name.strip('\"\'')).is_file() for name in fonts))

    def test_authored_math_compiles_with_vendored_katex(self):
        expressions = []
        paths = [*WIKI.glob("notes/*.md"), *WIKI.glob("research/questions/*.md"),
                 *WIKI.glob("research/experiments/*.md"), WIKI / "research/direction.md", WIKI / "themes.md"]
        def display_values(value):
            if isinstance(value, list):
                return "\n".join(display_values(item) for item in value)
            if isinstance(value, dict):
                return "\n".join(value.get(key, "") for key in ("caption", "display_text", "details", "title")
                                 if isinstance(value.get(key), str))
            return ""
        for path in paths:
            text = path.read_text()
            text = re.sub(r"```json\n(.*?)\n```", lambda m: display_values(json.loads(m[1])), text, flags=re.S)
            text = re.sub(r"```.*?```|<pre\b.*?</pre>|<code\b.*?</code>|`[^`]+`|</?[a-zA-Z][\w:-]*(?:\s+[^<>]*?)?\s*/?>", "", text, flags=re.S)
            for match in build.MATH.finditer(text):
                expressions.append([str(path.relative_to(WIKI)), html.unescape(match[0][2:-2])])
        self.assertGreater(len(expressions), 100)
        script = """
const katex = require(process.argv[1]);
const expressions = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const failures = [];
for (const [source, expression] of expressions) {
  try { katex.renderToString(expression, {throwOnError: true, trust: false, strict: 'error'}); }
  catch (error) { failures.push(source + ': ' + expression + '\\n' + error.message); }
}
if (failures.length) { console.error(failures.join('\\n')); process.exit(1); }
console.log(expressions.length + ' expressions compiled');
"""
        result = subprocess.run(["node", "-e", script, str(WIKI / "assets/vendor/katex-0.18.7/katex.min.js")],
                                input=json.dumps(expressions), text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
