"""PRO-66 (раунд ревью 2): юнит-фикстуры и сквозная сборка scripts/build_site.py.

Требования ревью: фикстуры для render (экранирование, громкий BuildError на
незаполненных токенах), _num_tokens RU ↔ EN, demo_numbers на фикстуре
03_options.md, сквозная сборка во временную директорию (обе страницы, ноль
кириллицы в EN). Плюс два CSS-фикса: scroll-padding-top у html (якоря не
уходят под фиксированную pill-панель) и отсутствие кириллицы в исходнике
EN-страницы — проверка PRO-61 сканирует исходник, включая CSS-комментарии.
"""
from __future__ import annotations

import html as html_mod
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site.py"
CYR = re.compile(r"[\u0400-\u04FF]")


def load_module():
    """Импорт scripts/build_site.py как модуля без установки пакета."""
    spec = importlib.util.spec_from_file_location("build_site_unit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def visible_text(page: str) -> str:
    body = re.sub(r"<script\b.*?</script>", " ", page, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return html_mod.unescape(body)


def style_block(page: str) -> str:
    m = re.search(r"<style>(.*?)</style>", page, flags=re.S)
    assert m, "нет <style>-блока"
    return m.group(1)


# ---------- render(): экранирование и громкий отказ ----------

class TestRenderFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_dynamic_values_are_escaped(self):
        out = self.mod.render(
            "{{TEXT}}|{{C_DOM}}|{{D_LABEL}}",
            {"TEXT": "<b>&\"x", "C_DOM": "<script>alert(1)</script>", "D_LABEL": "a&b"})
        self.assertNotIn("<b>", out)
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;b&gt;&amp;&quot;x", out)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", out)
        self.assertIn("a&amp;b", out)

    def test_raw_keys_pass_through_unescaped(self):
        out = self.mod.render("{{CSS}}{{BRAND}}",
                              {"CSS": "a{b:c}", "BRAND": "<svg><rect/></svg>"})
        self.assertEqual(out, "a{b:c}<svg><rect/></svg>")

    def test_leftover_token_raises_build_error(self):
        with self.assertRaisesRegex(self.mod.BuildError, "незаполненные токены"):
            self.mod.render("ok {{FROZEN}} end", {"TEXT": "x"})

    def test_all_tokens_filled_is_silent(self):
        self.assertEqual(self.mod.render("a {{X}} b", {"X": "1"}), "a 1 b")


# ---------- _num_tokens(): RU ↔ EN дают одинаковый список чисел ----------

class TestNumTokens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = staticmethod(load_module()._num_tokens)

    def test_ru_form(self):
        self.assertEqual(
            self.f("Рынок $37,97 млрд (2025), CAGR 7,1% до 2033; 685 млн профилей; 60+ стран"),
            sorted(["37.97", "2025", "7.1", "2033", "685", "60"]))

    def test_en_form(self):
        self.assertEqual(
            self.f("Market: $37.97B (2025), 7.1% CAGR to 2033; 685M profiles; 60+ countries"),
            sorted(["37.97", "2025", "7.1", "2033", "685", "60"]))

    def test_ru_and_en_of_same_fact_are_equal(self):
        ru = "Мировой рынок: $37,97 млрд (2025), рост 7,1% в год; Indeed — 60+ стран"
        en = "Global market: $37.97B (2025), growing 7.1% a year; Indeed — 60+ countries"
        self.assertEqual(self.f(ru), self.f(en))


# ---------- demo_numbers() на фикстуре 03_options.md ----------

OPT_FIXTURE = (
    "## Вариант A. Оставить как есть — бесплатный OSS\n"
    "- Возражения red team: (1) первое; (2) второе; (3) третье\n"
    "- Скрытое допущение: что-то предполагается\n"
    "## Вариант B. Hosted freemium SaaS\n"
    "- Возражения red team: (1) a; (2) b; (3) c; (4) d; (5) e\n"
    "- Скрытое допущение: ещё одно\n"
    "- Экономика: paid $29/мес; переменные 25% → CM $21,75; LTV ≈ $272; LTV/CAC ≈ 4,5\n"
)


def write_fixture_demo(tmp: Path) -> Path:
    """Мини-проект демо со структурой projects/демо: claims, sources, D001, 03_options.md."""
    demo = tmp / "demo"
    (demo / "outputs").mkdir(parents=True)
    (demo / "sources").mkdir()
    claims = [
        {"id": "C001", "kind": "fact", "grade": "B", "text": "т", "sources": ["S001"]},
        {"id": "C002", "kind": "hypothesis", "grade": "C", "text": "г", "sources": ["S001"]},
    ]
    (demo / "claims.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in claims) + "\n", encoding="utf-8")
    (demo / "sources.jsonl").write_text(
        json.dumps({"id": "S001", "url": "https://example.com/a", "retrieved": "2026-01-15"},
                   ensure_ascii=False) + "\n", encoding="utf-8")
    (demo / "decisions.jsonl").write_text(
        json.dumps({"id": "D001", "decision": "Запустить вариант B: hosted freemium SaaS",
                    "review": {"date": "2027-02-10"}}, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (demo / "sources" / "S001.md").write_text("источник\n", encoding="utf-8")
    (demo / "outputs" / "03_options.md").write_text(OPT_FIXTURE, encoding="utf-8")
    for name in ("SIX_PAGER.md", "SIX_PAGER_EN.md"):
        (demo / "outputs" / name).write_text("## FAQ-1. Market\nMention of [C011] here.\n",
                                             encoding="utf-8")
    return demo


class TestDemoNumbersOnFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()
        tmp = Path(tempfile.mkdtemp(prefix="pfs-build-fixture-"))
        cls.mod.DEMO = write_fixture_demo(tmp)

    def test_counts_options_red_team_and_choice(self):
        n = self.mod.demo_numbers()
        self.assertEqual(n["D_OPT_LAST"], "B")
        self.assertEqual(n["D_OBJ"], 3 + 5, "сумма максимумов по вариантам")
        self.assertEqual(n["D_ASM"], 2, "по одному «Скрытое допущение» на вариант")
        self.assertEqual(n["D_CLAIMS"], 2)
        self.assertEqual(n["D_FACTS"], 1)
        self.assertEqual(n["D_SOURCES"], 1)
        self.assertEqual(n["D_LETTER"], "B")
        self.assertEqual(n["D_LABEL"], "Hosted freemium SaaS")
        self.assertEqual(n["D_LABEL_EN"], "Hosted freemium SaaS")
        self.assertEqual(n["REVIEW_RU"], "10.02.27")
        self.assertEqual(n["REVIEW_EN"], "2027-02-10")

    def test_broken_options_file_is_loud(self):
        mod = load_module()
        tmp = Path(tempfile.mkdtemp(prefix="pfs-build-fixture-bad-"))
        demo = write_fixture_demo(tmp)
        (demo / "outputs" / "03_options.md").write_text("нет вариантов\n", encoding="utf-8")
        mod.DEMO = demo
        with self.assertRaisesRegex(mod.BuildError, "Вариант"):
            mod.demo_numbers()


# ---------- CSS-фиксы раунда ревью ----------

class TestCssFixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_html_rule_has_scroll_padding_top(self):
        m = re.search(r"html\{([^}]*)\}", self.mod.CSS)
        self.assertIsNotNone(m, "нет правила html{...}")
        self.assertIn("scroll-padding-top:96px", m.group(1),
                      "якорная навигация должна останавливаться ниже фиксированной шапки")

    def test_css_has_no_cyrillic(self):
        # CSS общий для RU и EN — кириллица в нём утекла бы в исходник EN-страницы
        leaks = CYR.findall(self.mod.CSS)
        self.assertEqual(leaks, [], "кириллица в CSS (в т.ч. в комментариях): " + "".join(leaks[:20]))


# ---------- сквозная сборка во временную директорию ----------

class TestEndToEndBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = Path(tempfile.mkdtemp(prefix="pfs-build-e2e-"))
        r = subprocess.run([sys.executable, str(SCRIPT), "--out", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, f"сборка упала:\n{r.stdout}\n{r.stderr}"
        cls.ru = (tmp / "index.html").read_text(encoding="utf-8")
        cls.en = (tmp / "en" / "index.html").read_text(encoding="utf-8")

    def test_both_pages_written(self):
        self.assertIn('<html lang="ru">', self.ru)
        self.assertIn('<html lang="en">', self.en)
        self.assertIn('<link rel="canonical" href="https://strategyproduct.ru/en/">', self.en)

    def test_no_placeholder_tokens_left(self):
        for lang, page in (("ru", self.ru), ("en", self.en)):
            self.assertNotIn("{{", page, lang)

    def test_en_visible_text_has_no_cyrillic(self):
        leaks = CYR.findall(visible_text(self.en))
        self.assertEqual(leaks, [], "кириллица в видимом тексте EN: " + "".join(leaks[:20]))

    def test_en_raw_source_has_no_cyrillic(self):
        # проверка PRO-61 сканирует исходник страницы — комментарии тоже считаются
        leaks = CYR.findall(self.en)
        self.assertEqual(leaks, [], "кириллица в исходнике EN-страницы: " + "".join(leaks[:20]))

    def test_anchor_navigation_clears_fixed_nav(self):
        for lang, page in (("ru", self.ru), ("en", self.en)):
            m = re.search(r"html\{([^}]*)\}", style_block(page))
            self.assertIsNotNone(m, lang)
            self.assertIn("scroll-padding-top:96px", m.group(1), lang)


if __name__ == "__main__":
    unittest.main()
