"""PRO-66: числа README согласованы с генератором сайта.

Раунд ревью 2: README.md и README_EN.md публикуют число автотестов «tests/ (N)»,
а scripts/build_site.py::repo_numbers() подставляет то же число на лендинг
({{N_TESTS}}). Все три места обязаны называть одно число — расхождение
(README «420», сайт «459», qa-отчёт «459 зелёные») ловится тестом.
Плюс README_EN.md должен описывать новую структуру site/ (генератор,
en/index.html, site/ANALYTICS.md) зеркально русскому README.
"""
from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TESTS_CLAIM = re.compile(r"^tests/\s+\((\d+)\)", re.M)


def generator_test_count() -> int:
    """Ровно то число, которое генератор подставляет в {{N_TESTS}} на сайт."""
    spec = importlib.util.spec_from_file_location(
        "build_site_readme", ROOT / "scripts" / "build_site.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.repo_numbers()["N_TESTS"]


class TestReadmeTestCounts(unittest.TestCase):
    """Число тестов в README = число, которое генератор кладёт на сайт."""

    def _claim(self, name: str) -> int:
        text = (ROOT / name).read_text(encoding="utf-8")
        found = TESTS_CLAIM.findall(text)
        self.assertEqual(
            len(found), 1,
            f"в {name} ровно одна строка «tests/ (N)» со счётчиком, найдено: {found}")
        return int(found[0])

    def test_readme_ru_tests_count_matches_generator(self):
        self.assertEqual(self._claim("README.md"), generator_test_count())

    def test_readme_en_tests_count_matches_generator(self):
        self.assertEqual(self._claim("README_EN.md"), generator_test_count())


class TestReadmeEnSiteLayout(unittest.TestCase):
    """README_EN.md описывает структуру site/ зеркально README.md."""

    @classmethod
    def setUpClass(cls):
        cls.en = (ROOT / "README_EN.md").read_text(encoding="utf-8")

    def test_generator_documented(self):
        self.assertIn("scripts/build_site.py", self.en)

    def test_en_page_documented(self):
        self.assertIn("en/index.html", self.en)

    def test_analytics_doc_documented(self):
        self.assertIn("site/ANALYTICS.md", self.en)


if __name__ == "__main__":
    unittest.main()
