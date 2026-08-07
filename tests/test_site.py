from html.parser import HTMLParser
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.attributes.append((tag, dict(attrs)))

    def handle_data(self, data):
        value = " ".join(data.split())
        if value:
            self.text.append(value)


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


if __name__ == "__main__":
    unittest.main()
