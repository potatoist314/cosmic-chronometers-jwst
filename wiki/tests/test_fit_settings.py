"""The settings component shows every key of the fit notebook once, from live values."""

import html
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

WIKI = Path(__file__).resolve().parents[1]
PROJECT = WIKI.parent
sys.path.insert(0, str(WIKI))
import fit_settings

NOTEBOOK = "notebooks/ceridwen_integrated_photometry_spectra.ipynb"
RUN = "results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb"
FOLDED = {"zred_half_width": "zred", "sigma_clip": "sigma_smooth"}


def rows(rendered):
    """{row name: row text} with tags removed."""
    found = {}
    for name, rest in re.findall(r'<div class="fs-row[^"]*"><dt>(.*?)</dt>(.*?)</div>', rendered):
        found[re.sub(r"<[^>]+>", "", name)] = re.sub(r"<[^>]+>", " ", rest)
    return found


class FitSettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cells = json.loads((PROJECT / NOTEBOOK).read_text())["cells"]
        cls.text = "".join(cells[2]["source"])
        cls.entries = fit_settings.parse(cls.text)
        cls.rendered = fit_settings.render(PROJECT, NOTEBOOK, 2, RUN)

    def name(self, key):
        if key in fit_settings.NAMES:
            return fit_settings.NAMES[key]
        return r"\(%s\)" % fit_settings.SYMBOLS[key] if key in fit_settings.SYMBOLS else key

    def test_every_key_is_rendered_once_hidden_or_folded(self):
        names = re.findall(r"<dt>(.*?)</dt>", self.rendered)
        for key in self.entries:
            shown = names.count(self.name(key)) + names.count("<code>%s</code>" % key)
            self.assertEqual(shown, 0 if key in fit_settings.HIDDEN or key in FOLDED else 1, key)
        self.assertEqual(len(names), len(self.entries) - len(fit_settings.HIDDEN) - len(FOLDED))

    def test_folded_settings_are_read_from_the_cell(self):
        found = rows(self.rendered)
        for setting, prior in FOLDED.items():
            value = fit_settings.number(str(self.entries[setting][1].value))
            self.assertRegex(found[self.name(prior)], r"(± |clipped at )%s\b" % re.escape(value))
        self.assertNotIn("ClippedNormal(", self.rendered)
        self.assertNotIn("Uniform(", self.rendered)

    def test_an_unmapped_key_renders_ungrouped(self):
        text = self.text.replace('    "sampler": {', '    "new_knob": 3,  # kept\n    "sampler": {', 1)
        last = fit_settings.component(text).rsplit("<section", 1)[1]
        self.assertNotIn("fs-label", last)
        self.assertIn("<code>new_knob</code>", last)
        self.assertIn("kept", last)

    def test_distribution_templates(self):
        found = rows(self.rendered)
        self.assertIn("Uniform [8, 13]", found[self.name("logmass")])
        self.assertIn(r"Student-t \(\mu\) 0, scale 0.3, \(\nu\) 2", found[self.name("logsfr_ratios")])
        self.assertIn("Normal, 0 ± 0.1", found["calibration_prior_sigma"])
        self.assertIn("Clipped normal 1 ± 0.3 on [0.2, 3]", found["spectrum_scaling"])

    def test_grid_ranges_come_from_the_run(self):
        found = rows(self.rendered)
        self.assertIn("Uniform [−2.5, 0.5]", found[self.name("Z")])
        self.assertIn("Uniform [−0.2, 0.6]", found[self.name("afe")])
        stdout = "".join("".join(o["text"]) for c in json.loads((PROJECT / RUN).read_text())["cells"]
                         for o in c.get("outputs", []) if o.get("name") == "stdout")
        raw = dict((key, (low, high)) for key, low, high in fit_settings.PRIOR_LINE.findall(stdout))["Z"]
        offset = float(re.search(r"\[Fe/H\] = Z \+ ([0-9.]+)", self.text)[1])
        for bound, shown in zip(raw, fit_settings.run_ranges(stdout)["Z"]):
            self.assertAlmostEqual(float(bound) + offset, float(shown), places=2)
        without = rows(fit_settings.render(PROJECT, NOTEBOOK, 2))
        self.assertIn("Uniform over the grid", without[self.name("Z")])
        self.assertIn("Uniform over the grid", without[self.name("afe")])

    def test_masked_lines_are_named_with_a_width_from_the_notebook(self):
        row = rows(self.rendered)["emission_lines"].replace("\u00a0", " ")
        self.assertIn(r"[O II] 3726/3729, H\(\beta\), [O III] 4959/5007", row)
        self.assertIn("masked ±19 to ±25", row)
        self.assertNotIn("3728.8", row)
        self.assertEqual(fit_settings.lines_html(fit_settings.ast.parse("[3869.0]").body[0].value, 1500.0)[0], "3869")

    def test_the_sampler_group_holds_only_the_sampler(self):
        last = self.rendered.rsplit("<section", 1)[1]
        self.assertIn(">Sampler</h3>", last)
        self.assertEqual(list(rows(last)), ["sampler"])
        self.assertNotIn("baked_runtime", self.rendered)

    def test_noise_floors_read_their_numbers_from_the_cell(self):
        group = self.rendered.split(">Noise floors</h3>", 1)[1].split("</section>", 1)[0]
        found = rows(group)
        self.assertEqual(list(found), ["Photometry", "Spectrum"])
        floor = self.entries["photometry_floor"][1].value
        self.assertIn("fixed %g%%, added in quadrature to each band" % (floor * 100), found["Photometry"])
        self.assertIn(r"\[\sigma_{\mathrm{tot}} = \sqrt{\sigma_{\mathrm{phot}}^2 + (%s\,F_{\mathrm{obs}})^2}\]" % floor,
                      found["Photometry"])
        low, high = (k.value.args[0].value for k in self.entries["log_f_calib"][1].keywords)
        self.assertIn("prior %g–%g%% log-uniform, added in quadrature to each pixel" % (low * 100, high * 100),
                      found["Spectrum"])
        self.assertIn(r"(f_{\mathrm{calib}}\,F_{\mathrm{model}})^2", found["Spectrum"])
        self.assertNotIn("log_f_calib", group)
        self.assertNotIn("fractional", group)

    def test_an_unfillable_slot_falls_back_to_the_generic_row(self):
        text = self.text.replace("Uniform(low=np.log(0.01), high=np.log(0.10))", "StudentT(mean=0.0, scale=1.0, df=2.0)")
        found = rows(fit_settings.component(text))
        self.assertIn("Student-t", found[r"\(%s\)" % fit_settings.SYMBOLS["log_f_calib"]])
        self.assertIn("fractional noise floor on the spectrum", found[r"\(%s\)" % fit_settings.SYMBOLS["log_f_calib"]])

    def test_the_dust_group_carries_its_law(self):
        dust = self.rendered.split(">Dust</h3>", 1)[1].split("</section>", 1)[0]
        equation = re.search(r"\\\[(.*?)\\\]", dust)[1]
        for key in ("diffuse_tau_kc", "diffuse_dust_index"):
            self.assertIn(fit_settings.SYMBOLS[key], equation)
            self.assertIn(self.name(key), dust.split("<dl>", 1)[1])
        self.assertIn('<a href="https://arxiv.org/abs/1308.1099">Kriek &amp; Conroy 2013</a>', dust)
        self.assertEqual(self.rendered.count("fs-eq-note"), 1)

    def test_symbols_compile_with_vendored_katex(self):
        script = ("const katex = require(process.argv[1]);"
                  "for (const e of JSON.parse(require('fs').readFileSync(0, 'utf8')))"
                  " katex.renderToString(e, {throwOnError: true, strict: 'error'});")
        math = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", self.rendered)
        math = [html.unescape(inline or display) for inline, display in math]
        result = subprocess.run(["node", "-e", script, str(WIKI / "assets/vendor/katex-0.18.7/katex.min.js")],
                                input=json.dumps(math), text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
