"""PRO-66 (раунд ревью 2): критерий «0 языковых утечек» по всему сайту.

Старые страницы demo.html / help.html / materials.html остаются на прежней
двуязычной вёрстке (перенос в генератор — отдельная задача; скоуп зафиксирован
в Linear PRO-66). Тест закрепляет измерение: в EN-режиме на этих страницах нет
ни одного русского фрагмента — ни в тексте, ни в пользовательских атрибутах,
а заголовок, meta description и html@lang переключаются I18N/setLang при
выборе языка. Проверка PRO-61 против «105 утечек в EN-режиме».

code[lang=ru] в EN-режиме не скрывается намеренно (репозиторные пути не
переводятся, см. CSS demo.html) — сканер пропускает все lang="ru"-поддеревья.
"""
from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CYR = re.compile(r"[\u0400-\u04FF]")
LEGACY = ("demo.html", "help.html", "materials.html")
VISIBLE_ATTRS = ("alt", "aria-label", "placeholder", "title", "value")
VOID_TAGS = frozenset({"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"})


class EnModeScanner(HTMLParser):
    """Что увидит посетитель в EN-режиме: текст и атрибуты вне lang="ru"-поддеревьев."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ru_open: list[str] = []
        self.text_leaks: list[str] = []
        self.attr_leaks: list[str] = []

    def _hidden(self) -> bool:
        return bool(self.ru_open)

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        ru = d.get("lang") == "ru" and tag not in VOID_TAGS
        if ru:
            self.ru_open.append(tag)
        if self._hidden():
            return
        for key in VISIBLE_ATTRS:
            val = d.get(key) or ""
            for frag in CYR.findall(val):
                self.attr_leaks.append(f"{tag}@{key}:{frag}")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.ru_open and self.ru_open[-1] == tag:
            self.ru_open.pop()

    def handle_data(self, data):
        if self._hidden():
            return
        for frag in CYR.findall(data):
            self.text_leaks.append(frag[:30])


def load(name: str) -> str:
    return (ROOT / "site" / name).read_text(encoding="utf-8")


class TestLegacyPagesEnMode(unittest.TestCase):
    """EN-режим старых страниц: ни одного русского фрагмента, метаданные переключаются."""

    def test_en_mode_visible_text_has_no_cyrillic(self):
        for name in LEGACY:
            sc = EnModeScanner()
            sc.feed(load(name))
            self.assertEqual(sc.text_leaks, [], f"{name}: RU в видимом тексте EN-режима")

    def test_en_mode_visible_attributes_have_no_cyrillic(self):
        for name in LEGACY:
            sc = EnModeScanner()
            sc.feed(load(name))
            self.assertEqual(sc.attr_leaks, [], f"{name}: RU в атрибутах EN-режима")

    def test_title_and_meta_swap_per_language(self):
        # набор EN-заголовков/описаний в I18N без кириллицы + setLang их применяет
        for name in LEGACY:
            src = load(name)
            m = re.search(r"I18N = \{.*?en: \{ title: \"([^\"]+)\", desc: \"([^\"]+)\" \}",
                          src, flags=re.S)
            self.assertIsNotNone(m, f"{name}: нет EN-набора I18N")
            self.assertEqual(CYR.findall(m.group(1)), [], f"{name}: EN-title с кириллицей")
            self.assertEqual(CYR.findall(m.group(2)), [], f"{name}: EN-description с кириллицей")
            swap = re.search(r"function setLang\(l, save\)\{(.*?)\}", src, flags=re.S)
            self.assertIsNotNone(swap, f"{name}: нет setLang")
            body = swap.group(1)
            self.assertIn("document.documentElement.lang = l", body, name)
            self.assertIn("document.title = I18N[l].title", body, name)
            self.assertIn("meta[name=\"description\"]", body, name)
            # EN-набор применяется сразу при загрузке (до первой отрисовки)
            self.assertIn("setLang(saved ||", src, name)

    def test_generated_en_page_has_no_cyrillic(self):
        src = load(Path("en") / "index.html")
        self.assertEqual(CYR.findall(src), [], "кириллица в исходнике en/index.html")


if __name__ == "__main__":
    unittest.main()
