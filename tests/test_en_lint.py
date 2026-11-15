"""PRO-53: английский в выводе — линтер SIX_PAGER_EN.md и EN-каркас без RU-вставок.

Контракт выпуска:
1. Линтер (pfs check): в outputs/SIX_PAGER_EN.md нет кириллицы, русских десятичных
   запятых и маркера «[RU source — translate]» — нарушения дают предупреждения;
   тысячи через запятую (42,635) и EN-формат 1,234.5 линтер не трогает.
2. `pfs export --six-pager --en` собирает чисто английский каркас: EN-версию пишет
   six-pager-writer из того же пакета данных (документы 00–07 — вход, не вставка),
   поэтому RU-текста и маркеров перевода в собранном каркасе нет.
3. Числа юнит-экономики в EN-каркасе — EN-формат (1,234.5), в RU — русский (1234,50).
4. Каркас-черновик (pending-строки «> EN draft») не считается «отставшим» в
   сверке тегов RU↔EN; сверка работает для дописанного EN-документа.

Запуск: python3 -m unittest tests.test_en_lint -v
"""
import os
import re
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-enlint-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import check, claims, core, export, project, sources  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CYR = re.compile(r"[а-яёА-ЯЁ]")


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Короткий ответ\n\nРынок 40 млрд [C001].\n\n"
        "## Что известно\n\n- Рынок 40 млрд [C001].\n",
        encoding="utf-8")


class EnLintTests(unittest.TestCase):
    def setUp(self):
        slug = "enlint-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("EN линтер", "Почему падает удержание?", slug=slug)
        sources.add(self.pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        make_docs(self.pdir)

    def write_en(self, text: str) -> None:
        (self.pdir / "outputs" / "SIX_PAGER_EN.md").write_text(text, encoding="utf-8")

    def lint(self) -> list[str]:
        return [w for w in check.run(self.pdir)["warnings"] if "SIX_PAGER_EN.md" in w]

    def test_cyrillic_flagged(self):
        self.write_en("# Demo: Six-pager (EN)\n\nMarket is large [C001].\n\nРынок 40 млрд.\n")
        warns = self.lint()
        self.assertTrue(warns, "кириллица в SIX_PAGER_EN.md ловится линтером")
        self.assertIn("кириллиц", warns[0])

    def test_russian_decimal_comma_flagged_thousands_and_en_format_not(self):
        self.write_en("# Demo: Six-pager (EN)\n\nChurn is 8,5 percent monthly [C001].\n\n"
                      "DE has 42,635 unfilled vacancies; the price point is €1,234.5 [C001].\n")
        warns = self.lint()
        self.assertEqual(len(warns), 1, "флагуется только русская десятичная запятая")
        self.assertIn("8,5", warns[0])
        self.assertIn(":3", warns[0], "предупреждение цитирует строку нарушения")
        self.assertNotIn("42,635", warns[0], "тысячи через запятую — не нарушение")

    def test_translate_marker_flagged(self):
        self.write_en("# Demo: Six-pager (EN)\n\n> [RU source — translate] 02_situation.md\n\n"
                      "Market is large [C001].\n")
        warns = self.lint()
        self.assertTrue(any("RU source" in w for w in warns),
                        "маркер перевода в SIX_PAGER_EN.md ловится линтером")

    def test_built_skeleton_passes_lint_with_ru_docs_present(self):
        export.build_six_pager(self.pdir, with_calcs=False, lang="en")
        self.assertEqual(self.lint(), [],
                         "собранный EN-каркас чист: кириллицы, запятых и маркеров нет")

    def test_en_skeleton_is_pure_english(self):
        en = export.build_six_pager(self.pdir, with_calcs=False, lang="en").read_text(encoding="utf-8")
        self.assertIsNone(CYR.search(en), "в EN-каркасе нет кириллицы")
        self.assertNotIn("[RU source", en, "маркеры перевода не вставляются")
        self.assertNotIn("Рынок 40 млрд", en, "RU-контент документов 00–07 не вставляется")
        self.assertIn("> EN draft", en, "pending-строки показывают writer'у, что писать")
        ru = export.build_six_pager(self.pdir, with_calcs=False).read_text(encoding="utf-8")
        self.assertIn("Рынок 40 млрд [C001]", ru, "RU-версия не пострадала")

    def test_en_unit_econ_numbers_use_en_format(self):
        core.write_json(self.pdir / "calcs.json",
                        {"unit_econ": {"arpu": 1234.5, "vc_share": 0.2, "cac": 600,
                                       "churn_month": 0.03}})
        en = export.build_six_pager(self.pdir, with_calcs=False, lang="en").read_text(encoding="utf-8")
        self.assertIn("1,234.50", en, "десятичный разделитель — точка, тысячи — запятая")
        self.assertNotIn("1234,50", en)
        ru = export.build_six_pager(self.pdir, with_calcs=False).read_text(encoding="utf-8")
        self.assertIn("1234,50", ru, "RU-формат чисел не изменился")

    def test_draft_skeleton_not_flagged_as_lagging(self):
        export.build_six_pager(self.pdir, with_calcs=False)
        export.build_six_pager(self.pdir, with_calcs=False, lang="en")
        self.assertEqual(check.en_sync_warnings(self.pdir), [],
                         "каркас-черновик EN — не «отставшая» версия: его допишет writer")

    def test_written_en_missing_tag_warns_and_draft_exempts(self):
        export.build_six_pager(self.pdir, with_calcs=False)
        en_path = self.pdir / "outputs" / "SIX_PAGER_EN.md"
        # дописанный writer'ом EN: маркера каркаса нет, есть тег C001
        en_path.write_text("# Demo: Six-pager (EN)\n\nMarket is large [C001].\n", encoding="utf-8")
        self.assertEqual(check.en_sync_warnings(self.pdir), [])
        # в RU добавили драйвер C002, EN не переписан — check предупреждает
        claims.add(self.pdir, "Драйвер: семейный пакет даёт +5 п.п. удержания",
                   "hypothesis", ["S001"], grade="C")
        out = self.pdir / "outputs" / "03_options.md"
        out.write_text("# 03 · Варианты\n\n## Драйверы\n\n- **Первый драйвер:** пакет [C002]\n",
                       encoding="utf-8")
        export.build_six_pager(self.pdir, with_calcs=False)
        warns = check.en_sync_warnings(self.pdir)
        self.assertTrue(warns, "дописанный EN без нового тега — предупреждение")
        self.assertIn("C002", warns[0])
        # пересборка EN даёт каркас-черновик — предупреждение снято (EN переделывают)
        export.build_six_pager(self.pdir, with_calcs=False, lang="en")
        self.assertEqual(check.en_sync_warnings(self.pdir), [])


class EnDocsTests(unittest.TestCase):
    """Документы выпуска: STYLE_EN.md и EN-спецификация six-pager."""

    def test_style_en_exists_with_required_anchors(self):
        p = REPO / "knowledge" / "templates" / "STYLE_EN.md"
        self.assertTrue(p.exists(), "нет knowledge/templates/STYLE_EN.md")
        text = p.read_text(encoding="utf-8")
        self.assertTrue(text.lstrip().startswith("#"), "нет заголовка")
        self.assertGreater(len(text), 2000, "стайлгайд подозрительно короткий")
        for anchor in ("1,234.5", "€24.95", "y/y", "[RU source — translate]", "4/5"):
            self.assertIn(anchor, text, f"в STYLE_EN.md нет «{anchor}»")

    def test_prompt_en_authored_not_translated(self):
        p = REPO / "knowledge" / "templates" / "SIX_PAGER_PROMPT_EN.md"
        text = p.read_text(encoding="utf-8")
        self.assertIn("STYLE_EN.md", text, "EN-спецификация ссылается на стайлгайд")
        self.assertIn("1,234.5", text, "EN-спецификация фиксирует EN-формат чисел")
        self.assertIn("[RU source — translate]", text, "маркер упомянут как запрещённый")
        self.assertNotIn("complete synchronous translation", text,
                         "старый контракт «полного синхронного перевода» убран")
        self.assertIn("4/5", text, "вычитка редактором по рубрике «звучит по-английски» ≥ 4/5")


if __name__ == "__main__":
    unittest.main()
