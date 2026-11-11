"""PRO-63: «голые» счётчики структуры репозитория под контролем update_counters.

Словесные счётчики («373 теста», «121 навыков») scripts/update_counters.py подставлял
с самого начала; голые числа в таблице «Структура репозитория» — `tests/ (N)`,
`skills/ (N…`, `**Структура (N)**`, «N skills in» — скриптом не подставлялись и
уезжали при каждом релизе (355 при 373 тестах, 120 при 121 навыке).

Тесты: подстановка на образцах + `--check` зелёный на реальных README/README_EN.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location(
        "update_counters", ROOT / "scripts" / "update_counters.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class BareCounterSubstitution(unittest.TestCase):
    """update_file заменяет голые счётчики после tests/, skills/ и «Структура»."""

    def setUp(self):
        self.mod = _load()
        self.c = self.mod.counts()

    def _apply(self, text: str) -> str:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "README.md"
            p.write_text(text, encoding="utf-8")
            self.mod.update_file(p, self.c)
            return p.read_text(encoding="utf-8")

    def test_bare_tests_counter_ru_structure_line(self):
        out = self._apply("tests/               (999)\n")
        self.assertIn(f"tests/               ({self.c['tests']})", out)
        self.assertNotIn("(999)", out)

    def test_bare_tests_counter_en_inline(self):
        out = self._apply("tests/ (999) · demo: демо — CVStart (100/100)\n")
        self.assertIn(f"tests/ ({self.c['tests']})", out)
        self.assertIn("(100/100)", out)  # чужие скобки не тронуты

    def test_bare_skills_counter_ru_structure_line(self):
        out = self._apply(".claude/skills/      (999)  базовые 13\n")
        self.assertIn(f".claude/skills/      ({self.c['skills']})", out)

    def test_bare_skills_counter_en_colon_form(self):
        out = self._apply("  skills/ (999: base 13 · product-skills 27)\n")
        self.assertIn(f"skills/ ({self.c['skills']}:", out)

    def test_structura_counter_ru(self):
        out = self._apply("**Структура (999):** четыре группы.\n")
        self.assertIn(f"**Структура ({self.c['skills']}):**", out)

    def test_skills_in_word_counter_en(self):
        out = self._apply("999 skills in `.claude/skills/`, four groups:\n")
        self.assertIn(f"{self.c['skills']} skills in", out)


class RealDocsCurrent(unittest.TestCase):
    """`update_counters.py --check` зелёный: реальные README не отстали."""

    def test_check_passes(self):
        self.assertEqual(_load().main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
