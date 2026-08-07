from html.parser import HTMLParser
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
FN_HTML_EXISTS = (ROOT / "fn/index.html").is_file()
FN_SCRIPT_EXISTS = (ROOT / "fn/finland.js").is_file()


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = []
        self.text = []
        self.links = []
        self._active_link = None
        self._ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.attributes.append((tag, attributes))
        if tag in {"style", "script"}:
            self._ignored_depth += 1
        if tag == "a":
            self._active_link = {"href": attributes.get("href"), "text": []}

    def handle_data(self, data):
        value = " ".join(data.split())
        if value and not self._ignored_depth:
            self.text.append(value)
            if self._active_link is not None:
                self._active_link["text"].append(value)

    def handle_endtag(self, tag):
        if tag in {"style", "script"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "a" and self._active_link is not None:
            self.links.append(
                (self._active_link["href"], " ".join(self._active_link["text"]))
            )
            self._active_link = None


def parse(relative_path: str) -> DocumentParser:
    parser = DocumentParser()
    parser.feed((ROOT / relative_path).read_text(encoding="utf-8"))
    return parser


class SharedAssetTests(unittest.TestCase):
    def test_shared_assets_exist(self):
        self.assertTrue((ROOT / "assets/site.css").is_file())
        self.assertTrue((ROOT / "assets/ambient.js").is_file())

    def test_ambient_script_is_safe_without_optional_effect_elements(self):
        harness = """
global.window = {
  innerWidth: 1200,
  innerHeight: 800,
  scrollY: 0,
  matchMedia: () => ({ matches: false }),
  addEventListener: () => {},
  requestAnimationFrame: () => {},
};
global.document = {
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => [],
};
global.IntersectionObserver = class {
  observe() {}
};
require('./assets/ambient.js');
"""
        result = subprocess.run(
            ["node", "-e", harness],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class FinlandPageTests(unittest.TestCase):
    def test_finland_route_exists(self):
        self.assertTrue(FN_HTML_EXISTS)
        self.assertTrue(FN_SCRIPT_EXISTS)

    @unittest.skipUnless(FN_HTML_EXISTS, "Finland route not implemented yet")
    def test_finland_is_paused_without_opening_claims_or_signup(self):
        document = parse("fn/index.html")
        visible_text = " ".join(document.text)
        classes = {
            class_name
            for _, attributes in document.attributes
            for class_name in attributes.get("class", "").split()
        }

        self.assertIn("Concept currently paused", visible_text)
        for forbidden in ("Coming Soon", "Winter 2026", "Notify Me", "5,000", "Immersive Halls"):
            self.assertNotIn(forbidden, visible_text)
        self.assertNotIn("form", [tag for tag, _ in document.attributes])
        self.assertNotIn("stats", classes)

    @unittest.skipUnless(FN_HTML_EXISTS, "Finland route not implemented yet")
    def test_finland_preserves_assets_navigation_and_languages(self):
        document = parse("fn/index.html")
        hrefs = [attributes.get("href") for tag, attributes in document.attributes if tag == "a"]
        stylesheets = [attributes.get("href") for tag, attributes in document.attributes if tag == "link"]
        scripts = [attributes.get("src") for tag, attributes in document.attributes if tag == "script"]
        images = [attributes.get("src") for tag, attributes in document.attributes if tag == "img"]
        languages = {
            attributes["data-lang"]
            for tag, attributes in document.attributes
            if tag == "button" and "data-lang" in attributes
        }

        self.assertIn("../", hrefs)
        self.assertIn("../assets/site.css", stylesheets)
        self.assertIn("../assets/ambient.js", scripts)
        self.assertIn("finland.js", scripts)
        self.assertIn("../IMG_1055.PNG", images)
        self.assertIn("../IMG_1054.PNG", images)
        self.assertEqual(languages, {"en", "fi", "sv", "de", "fr", "ja", "zh", "ru"})

    @unittest.skipUnless(FN_SCRIPT_EXISTS, "Finland translations not implemented yet")
    def test_finland_language_switch_updates_paused_status(self):
        harness = """
const nodes = [
  { dataset: { i18n: 'tagline' }, textContent: '' },
  { dataset: { i18n: 'status' }, textContent: '' },
];
global.window = {};
global.localStorage = { getItem: () => null, setItem: () => {} };
global.document = {
  documentElement: { lang: 'en' },
  querySelectorAll: (selector) => selector === '[data-i18n]' ? nodes : [],
  getElementById: () => null,
  addEventListener: () => {},
};
require('./fn/finland.js');
window.setLang('fi');
process.stdout.write(JSON.stringify({ lang: document.documentElement.lang, status: nodes[1].textContent }));
"""
        result = subprocess.run(
            ["node", "-e", harness],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            '{"lang":"fi","status":"Konsepti on tällä hetkellä tauolla"}',
        )


class GatewayTests(unittest.TestCase):
    def test_gateway_offers_two_equal_project_links(self):
        document = parse("index.html")
        project_links = [
            (href, text)
            for href, text in document.links
            if href in {"brian-head/", "fn/"}
        ]

        self.assertCountEqual(
            project_links,
            [("brian-head/", "Explore Project"), ("fn/", "Explore Project")],
        )
        visible_text = " ".join(document.text)
        self.assertIn("Brian Head", visible_text)
        self.assertIn("Finland", visible_text)

    def test_gateway_is_neutral_and_uses_shared_experience(self):
        document = parse("index.html")
        visible_text = " ".join(document.text)
        stylesheets = [attributes.get("href") for tag, attributes in document.attributes if tag == "link"]
        scripts = [attributes.get("src") for tag, attributes in document.attributes if tag == "script"]
        images = [attributes for tag, attributes in document.attributes if tag == "img"]

        self.assertNotIn("Coming Soon", visible_text)
        self.assertNotIn("Concept currently paused", visible_text)
        self.assertNotIn("Proposed for Brian Head", visible_text)
        self.assertIn("assets/site.css", stylesheets)
        self.assertIn("assets/ambient.js", scripts)
        self.assertIn("assets/brian-head-concept.webp", [image.get("src") for image in images])
        self.assertTrue(all(image.get("alt") for image in images))


if __name__ == "__main__":
    unittest.main()
