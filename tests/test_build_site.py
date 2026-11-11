"""PRO-66: юнит-фикстуры и сквозная сборка scripts/build_site.py.

Раунд ревью 2: (1) фикстуры render (экранирование, громкий BuildError на
незаполненных токенах), _num_tokens RU ↔ EN, demo_numbers на фикстуре
03_options.md — включая жёсткие переносы red-team-блока, извлечение D001 и
метки выбранного варианта, excel_numbers() с anchored-числами и сверкой с
Excel-приложением, repo_numbers() с громким отказом на отсутствующих и пустых
каталогах; (2) сквозная сборка во временную директорию (обе страницы, ноль
кириллицы в EN). Плюс два CSS-фикса: scroll-padding-top у html (якоря не
уходят под фиксированную pill-панель) и отсутствие кириллицы в исходнике
EN-страницы — проверка PRO-61 сканирует исходник, включая CSS-комментарии.
"""
from __future__ import annotations

import html as html_mod
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
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


def write_fixture_demo(tmp: Path, options_md: str | None = None,
                       letter: str = "B") -> Path:
    """Мини-проект демо со структурой projects/демо: claims, sources, D001, 03_options.md.

    letter — выбранный в D001 вариант; должен существовать среди заголовков 03_options.md.
    """
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
        json.dumps({"id": "D001", "decision": f"Запустить вариант {letter}: hosted freemium SaaS",
                    "review": {"date": "2027-02-10"}}, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (demo / "sources" / "S001.md").write_text("источник\n", encoding="utf-8")
    (demo / "outputs" / "03_options.md").write_text(options_md or OPT_FIXTURE, encoding="utf-8")
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


# ---------- жёсткие переносы red-team-блока на фикстуре ----------

OPT_WRAPPED = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
               "- Возражения red team: (1) рынок уже показал спрос на бесплатные\n"
               "  генераторы резюме; (2) копирование чужого текста недостоверно;\n"
               "  (3) без дискриминанта не отличить от обычного чата\n"
               "- Скрытое допущение: бесплатный OSS закрывает только часть задач\n")


class TestWrappedRedTeamOnFixture(unittest.TestCase):
    """demo_numbers(): «Возражения red team» перенесены на строки продолжения.

    Ревью PRO-66: жёсткий перенос кладёт подпункты (2)…(N) на строки продолжения;
    захват только первой строки молча занижает D_OBJ.
    """

    def setUp(self):
        self.mod = load_module()

    def _demo(self, md: str) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="pfs-build-wrapped-"))
        self.mod.DEMO = write_fixture_demo(tmp, options_md=md, letter="A")

    def test_wrapped_objections_counted(self):
        self._demo(OPT_WRAPPED)
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_OBJ"], 3,
                         "подпункты (2) и (3) на строках продолжения должны считаться")
        self.assertEqual(nums["D_ASM"], 1)

    def test_wrapped_capture_stops_at_next_bullet(self):
        md = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
              "- Возражения red team: (1) первое возражение\n"
              "  продолжение первого пункта без пометок\n"
              "- Скрытое допущение: срок пересмотра (2027-02-10) помечен в скобках\n")
        self._demo(md)
        nums = self.mod.demo_numbers()
        self.assertEqual(nums["D_OBJ"], 1, "(2027…) из «Скрытого допущения» — не возражение")
        self.assertEqual(nums["D_ASM"], 1)

    def test_wrapped_without_numbers_is_loud(self):
        md = ("## Вариант A. Оставить как есть — бесплатный OSS\n"
              "- Возражения red team: возражения есть,\n"
              "  но нумерации нет ни на одной строке переноса\n"
              "- Скрытое допущение: что-то\n")
        self._demo(md)
        with self.assertRaisesRegex(self.mod.BuildError, "нумерованных"):
            self.mod.demo_numbers()


# ---------- excel_numbers(): anchored-числа и сверка с Excel-приложением ----------

def write_unit_economics_xlsx(path: Path, values: list[str]) -> None:
    """Минимальный xlsx: worksheets с <v>-значениями — достаточно для сверки чисел."""
    with zipfile.ZipFile(path, "w") as z:
        cells = "".join(f'<c r="B{i}"><v>{v}</v></c>' for i, v in enumerate(values, 2))
        z.writestr("xl/worksheets/sheet1.xml",
                   f"<worksheet><sheetData>{cells}</sheetData></worksheet>")


OPT_XLSX = ("## Вариант B. Hosted freemium SaaS\n"
            "- Экономика: paid $29/мес; переменные 25% → CM $21,75; "
            "LTV ≈ $272; LTV/CAC ≈ 4,5\n")


class TestExcelNumbersAnchored(unittest.TestCase):
    r"""excel_numbers(): «$1 234» не обрезается до «1», значения сверяются с Excel.

    Ревью PRO-66: `[\d,]+` на «$1 234» захватывал «1» — молчаливая порча числа на
    сайте. Плюс валидация: числа 03_options.md должны сходиться с приложением
    unit_economics.xlsx (по точности документа: «$272» ↔ 271.88 в книге).
    """

    def setUp(self):
        self.mod = load_module()
        self.tmp = Path(tempfile.mkdtemp(prefix="pfs-build-xlsx-"))

    def _demo(self, md: str, xlsx_values: list[str] | None = None,
              with_xlsx: bool = True) -> None:
        demo = self.tmp / "demo"
        (demo / "outputs" / "attachments").mkdir(parents=True)
        (demo / "outputs" / "03_options.md").write_text(md, encoding="utf-8")
        if with_xlsx:
            write_unit_economics_xlsx(
                demo / "outputs" / "attachments" / "unit_economics.xlsx",
                xlsx_values or ["29", "0.25", "21.75", "271.88", "4.53"])
        self.mod.DEMO = demo

    def test_spaced_thousands_captured_whole(self):
        self._demo(OPT_XLSX.replace("$29", "$1 234").replace("$21,75", "$1 234,50")
                   .replace("$272", "$1 234"),
                   ["1234", "1234.50", "1234", "4.5"])
        self.assertEqual(
            self.mod.excel_numbers(),
            {"XL_PRICE": "1 234", "XL_CM": "1 234,50",
             "XL_LTV": "1 234", "XL_RATIO": "4,5"},
            "пробельный разделитель тысяч не должен обрезаться до первой цифры")

    def test_md_values_must_match_excel_attachment(self):
        self._demo(OPT_XLSX, ["39", "0.25", "21.75", "271.88", "4.53"])
        with self.assertRaisesRegex(self.mod.BuildError, "unit_economics.xlsx"):
            self.mod.excel_numbers()

    def test_md_values_round_match_excel(self):
        # в документе «$272», в книге 271.88 — сверка по точности документа
        self._demo(OPT_XLSX)
        self.assertEqual(self.mod.excel_numbers()["XL_LTV"], "272")

    def test_missing_xlsx_is_loud(self):
        self._demo(OPT_XLSX, with_xlsx=False)
        with self.assertRaisesRegex(self.mod.BuildError, "Excel"):
            self.mod.excel_numbers()


# ---------- repo_numbers(): громкий отказ на отсутствующих и пустых каталогах ----------

class TestRepoNumbersLoud(unittest.TestCase):
    """repo_numbers(): отсутствующий или пустой каталог — BuildError, не тихий ноль.

    Ревью PRO-66: len(list(glob)) молча возвращал 0, если каталога нет или он пуст,
    и сайт показывал «0 карт» / «0 навыков» вместо падения сборки.
    """

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="pfs-build-repo-"))

    def _make_root(self, name: str) -> Path:
        root = self.tmp / name
        files = (("knowledge/methods", "M-a.md", "x"),
                 ("knowledge/methods_en", "M-a-en.md", "x"),
                 (".claude/skills/s1", "SKILL.md", "x"),
                 (".claude/agents", "a.md", "x"),
                 (".claude/hooks", "h.py", "x"),
                 ("tests", "test_x.py", "def test_x(self):\n    pass\n"))
        for rel, fname, body in files:
            d = root / rel
            d.mkdir(parents=True, exist_ok=True)
            (d / fname).write_text(body, encoding="utf-8")
        return root

    def _mod_with_root(self, root: Path):
        mod = load_module()
        mod.ROOT = root
        return mod

    def test_counts_a_minimal_repo(self):
        n = self._mod_with_root(self._make_root("ok")).repo_numbers()
        self.assertEqual(n, {"N_MAPS": 1, "N_MAPS_EN": 1, "N_SKILLS": 1,
                             "N_AGENTS": 1, "N_HOOKS": 1, "N_TESTS": 1})

    def test_missing_dir_is_loud(self):
        root = self._make_root("missing")
        shutil.rmtree(root / "knowledge" / "methods")
        mod = self._mod_with_root(root)
        with self.assertRaisesRegex(mod.BuildError, "knowledge/methods"):
            mod.repo_numbers()

    def test_empty_dir_is_loud(self):
        root = self._make_root("empty")
        (root / ".claude" / "hooks" / "h.py").unlink()
        mod = self._mod_with_root(root)
        with self.assertRaisesRegex(mod.BuildError, "hooks"):
            mod.repo_numbers()

    def test_missing_tests_dir_is_loud(self):
        root = self._make_root("notests")
        shutil.rmtree(root / "tests")
        mod = self._mod_with_root(root)
        with self.assertRaisesRegex(mod.BuildError, "tests"):
            mod.repo_numbers()

    def test_empty_tests_dir_is_loud(self):
        root = self._make_root("emptytests")
        (root / "tests" / "test_x.py").unlink()
        mod = self._mod_with_root(root)
        with self.assertRaisesRegex(mod.BuildError, "tests"):
            mod.repo_numbers()


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


# ---------- раунд ревью 3 (PRO-66): дословный запрос как токен сборки ----------

class TestVerbatimRequestToken(unittest.TestCase):
    """Дословный запрос руководителя — второй аргумент `pfs new`, он хранится в
    project.json демо-проекта. Терминал и проза секции демо получают ОДИН токен
    на язык, поэтому расхождение «с/без на весь мир» (замечание ревью) невозможно
    по построению."""

    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_ru_matches_project_json(self):
        pj = json.loads((ROOT / "projects" / "демо" / "project.json").read_text(encoding="utf-8"))
        self.assertEqual(self.mod.demo_request()["RQ_RU"], pj["question"].strip())

    def test_en_translation_numbers_match_repo(self):
        req = self.mod.demo_request()

        def nums(s):
            return sorted(t.replace(",", ".") for t in re.findall(r"\d[\d,.]*", s))

        self.assertEqual(nums(req["RQ_EN"]), nums(req["RQ_RU"]))

    def test_en_translation_carries_urls_from_request(self):
        en = self.mod.demo_request()["RQ_EN"]
        self.assertIn("https://cvstart.org/", en)
        self.assertIn("https://github.com/Fighter90/career-ops-ui", en)

    def test_missing_project_is_loud(self):
        tmp = Path(tempfile.mkdtemp(prefix="pfs-rq-loud-"))
        self.mod.DEMO = tmp
        try:
            with self.assertRaisesRegex(self.mod.BuildError, "project.json"):
                self.mod.demo_request()
        finally:
            self.mod.DEMO = ROOT / "projects" / "демо"

    def test_empty_question_is_loud(self):
        tmp = Path(tempfile.mkdtemp(prefix="pfs-rq-empty-"))
        (tmp / "project.json").write_text(json.dumps({"question": "  "}), encoding="utf-8")
        self.mod.DEMO = tmp
        try:
            with self.assertRaisesRegex(self.mod.BuildError, "пустой question"):
                self.mod.demo_request()
        finally:
            self.mod.DEMO = ROOT / "projects" / "демо"


if __name__ == "__main__":
    unittest.main()
