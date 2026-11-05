"""Тесты HTML-деки из SIX_PAGER.md. Запуск: python3 -m unittest discover -s tests"""
import os
import re
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-deck-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import core, export, project  # noqa: E402

SIX_PAGER = """# Дека тест: six-pager

> Собрано 2026-11-05 командой `pfs export --six-pager`.

**Запрос:** Почему падает удержание?

## FAQ-1. Анализ текущего состояния

Отток растёт третий месяц подряд [C001].

- абоненты 55+ уходят из-за мошеннических звонков
- конкуренты запустили семейные пакеты

## FAQ-2. Метрики успеха

Удержание M1 с 38% до 45% к концу квартала [C001].

## Приложения (Excel)

> Ещё нет: `pfs calc all`.
"""


class DeckExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Дека тест", "Почему падает удержание?", slug="deck")
        (cls.pdir / "outputs" / "SIX_PAGER.md").write_text(SIX_PAGER, encoding="utf-8")

    def test_deck_created_at_expected_path(self):
        path = export.build_deck(self.pdir)
        self.assertIsInstance(path, Path)
        self.assertEqual(path, self.pdir / "outputs" / "presentations" / "deck.html")
        self.assertTrue(path.exists())
        # повтор — идемпотентен
        self.assertEqual(export.build_deck(self.pdir), path)

    def test_deck_contains_all_faq_titles_and_request(self):
        html = export.build_deck(self.pdir).read_text(encoding="utf-8")
        self.assertIn("Дека тест: six-pager", html)
        self.assertIn("<b>Запрос:</b> Почему падает удержание?", html)
        self.assertIn("FAQ-1. Анализ текущего состояния", html)
        self.assertIn("FAQ-2. Метрики успеха", html)
        self.assertIn("Приложения", html)
        # тезисы: и маркер списка, и первое предложение абзаца
        self.assertIn("абоненты 55+ уходят из-за мошеннических звонков", html)
        self.assertIn("Отток растёт третий месяц подряд", html)
        self.assertIn("Удержание M1 с 38% до 45%", html)

    def test_deck_has_no_lorem_and_is_standalone_dark_16x9(self):
        html = export.build_deck(self.pdir).read_text(encoding="utf-8")
        self.assertNotIn("lorem", html.lower())
        self.assertNotIn("<script", html.lower())  # standalone: только инлайн-CSS
        self.assertIn("#070b13", html)
        self.assertIn("#4fd1c5", html)
        self.assertIn("#8b7bff", html)
        self.assertIn("scroll-snap", html)
        self.assertIn("16/9", html)

    def test_theses_capped_at_six_and_truncated_to_160(self):
        long_line = "Очень длинный тезис про удержание, сегменты и драйверы роста " * 10  # одно предложение ~600 симв.
        items = "\n".join(f"- тезис номер {i}" for i in range(1, 9))
        (self.pdir / "outputs" / "SIX_PAGER.md").write_text(
            "# Тест лимитов\n\n**Запрос:** лимиты?\n\n## FAQ-1. Лимиты\n\n" + long_line + "\n\n" + items + "\n",
            encoding="utf-8")
        try:
            html = export.build_deck(self.pdir).read_text(encoding="utf-8")
        finally:
            (self.pdir / "outputs" / "SIX_PAGER.md").write_text(SIX_PAGER, encoding="utf-8")
        self.assertEqual(html.count("<li>"), 6)  # максимум 6 тезисов на слайд
        self.assertNotIn("тезис номер 6", html)  # 8 пунктов списка не влезли
        m = re.search(r"<li>(Очень длинный[^<]*)</li>", html)
        self.assertIsNotNone(m)
        self.assertTrue(m.group(1).endswith("…"))  # длинный тезис обрезан
        self.assertLessEqual(len(m.group(1)), 161)  # ≤160 символов


class DeckMissingSourceTests(unittest.TestCase):
    def test_build_deck_without_six_pager_raises(self):
        pdir = project.create("Без six-pager", "Что делать?", slug="deck-empty")
        with self.assertRaises(core.PfsError) as ctx:
            export.build_deck(pdir)
        self.assertIn("--six-pager", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
