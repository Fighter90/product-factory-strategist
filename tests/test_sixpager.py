"""Тесты six-pager и Excel-приложений. Запуск: python3 -m unittest discover -s tests"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-sp-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import calc, export, project  # noqa: E402
from tools.pfs.xlsx import Workbook, sheet_names  # noqa: E402


class XlsxWriterTests(unittest.TestCase):
    def test_workbook_formulas_and_styles(self):
        wb = Workbook()
        s = wb.sheet("Ввод", widths={1: 30})
        s.row("Параметр", "Значение")
        s.row("ARPU", 199)
        t = wb.sheet("Расчёт")
        t.row("CM", {"f": "'Ввод'!B2*0.8", "cached": 159.2, "bold": True})
        t.row("Доля", {"v": 0.2, "pct": True})
        t.row("Текст", "обычный")
        p = Path(TMP) / "book.xlsx"
        wb.save(p)
        with zipfile.ZipFile(p) as z:
            self.assertIsNone(z.testzip())
            xml = z.read("xl/worksheets/sheet2.xml").decode("utf-8")
        self.assertEqual(sheet_names(p), ["Ввод", "Расчёт"])
        self.assertIn("<f>'Ввод'!B2*0.8</f>", xml)
        self.assertIn("<v>159.2</v>", xml)
        self.assertIn('t="inlineStr"', xml)
        self.assertIn('s="2"', xml)  # процентный стиль

    def test_sheet_name_sanitized(self):
        wb = Workbook()
        wb.sheet("Лист / с * плохими:символами")
        p = Path(TMP) / "names.xlsx"
        wb.save(p)
        self.assertTrue(all(m not in sheet_names(p)[0] for m in "/:*?\\"))


class CalcAndSixPagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Six-pager тест", "Почему падает удержание?", slug="sp")
        out = cls.pdir / "outputs"
        (out / "02_situation.md").write_text(
            "# Ситуация\n## Короткий ответ\nОтток растёт, рынок 40 млрд [C001].\n"
            "## Что известно\n- факты из источников\n## Сегменты\n- абоненты 55+: пугают мошеннические звонки\n"
            "## Противоречия\n- данные источников противоречат\n", encoding="utf-8")
        (out / "03_options.md").write_text(
            "# Варианты\n## Рекомендация\nВариант B: переупаковка\n## Вариант A: оставить как есть\n"
            "### Возражения\n- отток продолжится\n## Вариант B: переупаковка\n## Вариант C: закрыть\n",
            encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Стратегия\n## Аудитория\nабоненты 55+ и их семьи\n## Тактики\n- семейный пакет с уведомлениями\n"
            "## Метрики\nудержание M1 с 38% до 45% [C001]\n", encoding="utf-8")
        (out / "06_validation_plan.md").write_text(
            "# План\n## Ожидаемое изменение\nудержание M1 +7 п.п.\n## Критерии решения\nпродолжаем, если +3 п.п.\n",
            encoding="utf-8")
        (cls.pdir / "calcs.json").write_text(
            '{"unit_econ": {"arpu": 29, "vc_share": 0.25, "cac": 60, "churn_month": 0.08}}',
            encoding="utf-8")
        (cls.pdir / "sources.jsonl").write_text(
            '{"id": "S001", "title": "Рынок (агрегатор)", "url": "https://example.com/market", '
            '"origin": "public", "retrieved": "2026-11-07T00:00:00", "path": ""}\n'
            '{"id": "S002", "title": "Внутренний файл", "url": "", '
            '"origin": "own", "retrieved": "2026-11-07T00:00:00", "path": "notes.md"}\n',
            encoding="utf-8")

    def test_calc_builds_four_valid_books(self):
        paths = calc.run(self.pdir, "all")
        self.assertEqual(len(paths), 4)
        names = {p.name for p in paths}
        self.assertEqual(names, {"unit_economics.xlsx", "growth_model.xlsx",
                                 "cohort_retention.xlsx", "market_sizing.xlsx"})
        for p in paths:
            with zipfile.ZipFile(p) as z:
                self.assertIsNone(z.testzip())
            self.assertIn("Ввод", " ".join(sheet_names(p)))
        # повтор — идемпотентен
        self.assertEqual(len(calc.run(self.pdir, "all")), 4)
        # выборочный пересчёт
        single = calc.run(self.pdir, "unit-econ")
        self.assertEqual(single[0].name, "unit_economics.xlsx")

    def test_unit_econ_has_formulas(self):
        p = calc.run(self.pdir, "unit-econ")[0]
        with zipfile.ZipFile(p) as z:
            xml = "".join(z.read(n).decode("utf-8")
                          for n in z.namelist() if n.startswith("xl/worksheets/"))
        self.assertIn("LTV", xml)
        self.assertIn("<f>", xml)

    def test_six_pager_structure(self):
        path = export.build_six_pager(self.pdir, with_calcs=True)
        text = path.read_text(encoding="utf-8")
        for head in ("FAQ-1", "FAQ-2", "FAQ-3", "FAQ-4", "FAQ-5", "FAQ-6",
                     "Приложения (Excel)", "unit_economics.xlsx", "growth_model.xlsx",
                     "### 1.1 Обзор рынка", "### 1.2 Ключевые конкуренты",
                     "### 2.1 Сегменты", "### 2.2 Барьеры на каждом этапе пути",
                     "Первый драйвер", "Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики)",
                     "KPI в двух плоскостях", "## Источники (сноски)",
                     "**S001** — Рынок (агрегатор) — https://example.com/market",
                     "**S002** — Внутренний файл"):
            self.assertIn(head, text)
        # юнит-экономика посчитана из calcs.json: CM = 29 * 0.75 = 21.75
        self.assertIn("21,75", text)
        self.assertIn("271,88", text)
        # без пересчёта Excel — текст собирается повторно
        path2 = export.build_six_pager(self.pdir, with_calcs=False)
        self.assertEqual(path.read_text(encoding="utf-8"), path2.read_text(encoding="utf-8"))

    def test_report_includes_attachments_appendix(self):
        report = export.build(self.pdir)
        self.assertIn("Приложение E", report.read_text(encoding="utf-8"))

    def test_six_pager_without_outputs_falls_back(self):
        pdir2 = project.create("Пустой", "Что делать?", slug="sp-empty")
        path = export.build_six_pager(pdir2, with_calcs=False)
        text = path.read_text(encoding="utf-8")
        self.assertIn("FAQ-1", text)
        self.assertIn("Раздел появится", text)  # заглушки вместо падения


if __name__ == "__main__":
    unittest.main()
