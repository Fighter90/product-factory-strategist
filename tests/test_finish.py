"""pfs finish — командная цепочка до финального пакета (PRO-31).

Порядок критичен: Excel ДО REPORT (Приложение E полно) и ДО SIX_PAGER (таблица
приложений полна), снимок реестра — ПОСЛЕ сборки, дека — из готового SIX_PAGER.
Повторный вызов идемпотентен. Флаги: no_deck, en (EN-черновик six-pager).

Запуск: python3 -m unittest tests.test_finish -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-finish-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import claims, cli, core, export, finish, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

EXCEL = {"unit_economics.xlsx", "growth_model.xlsx", "cohort_retention.xlsx", "market_sizing.xlsx"}


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Короткий ответ\n\nРынок 40 млрд [C001].\n", encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# 04 · Стратегия\n\n## Аудитория\n\nСоискатели [C001].\n", encoding="utf-8")


class FinishTests(unittest.TestCase):
    def setUp(self):
        slug = "finish-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("Финиш тест", "Почему падает удержание?", slug=slug)
        sources.add(self.pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        make_docs(self.pdir)

    def test_full_package_in_right_order(self):
        res = finish.run(self.pdir)
        # 1. Все четыре Excel-книги собраны
        att = self.pdir / "outputs" / "attachments"
        self.assertEqual({p.name for p in att.glob("*.xlsx")}, EXCEL)
        # 2. REPORT собран ПОСЛЕ Excel: Приложение E со всеми книгами (регрессия PRO-31)
        report = (self.pdir / "outputs" / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("Приложение E", report)
        for name in sorted(EXCEL):
            self.assertIn(name, report.split("Приложение E", 1)[1])
        # 3. SIX_PAGER: таблица приложений со всеми книгами
        sp = (self.pdir / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        for name in sorted(EXCEL):
            self.assertIn(name, sp)
        # 4. DOCX обеих версий и дека из готового six-pager
        self.assertTrue((self.pdir / "outputs" / "REPORT.docx").exists())
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER.docx").exists())
        deck = self.pdir / "outputs" / "presentations" / "deck.html"
        self.assertTrue(deck.exists())
        self.assertIn("Финиш тест: six-pager", deck.read_text(encoding="utf-8"))
        # 5. Артефакты в результате
        self.assertEqual(len(res["artifacts"]), 8)
        # 6. Снимок реестра зафиксирован ПОСЛЕ сборки — предупреждений о несвежести нет
        self.assertEqual(export.freshness_warnings(self.pdir), [])

    def test_idempotent(self):
        r1 = finish.run(self.pdir)
        r2 = finish.run(self.pdir)
        self.assertEqual({p.name for p in r1["artifacts"]}, {p.name for p in r2["artifacts"]})
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())
        self.assertEqual(export.freshness_warnings(self.pdir), [])
        # дублей в журнале нет, только по записи на вызов
        entries = core.read_jsonl(self.pdir / "log.jsonl")
        self.assertEqual(sum(1 for e in entries if e.get("tool") == "pfs finish"), 2)

    def test_no_deck_flag_skips_deck_only(self):
        res = finish.run(self.pdir, no_deck=True)
        self.assertFalse((self.pdir / "outputs" / "presentations" / "deck.html").exists())
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER.docx").exists())
        self.assertEqual(len(res["artifacts"]), 7)

    def test_en_flag_builds_en_draft_and_keeps_ru(self):
        finish.run(self.pdir, en=True)
        en = (self.pdir / "outputs" / "SIX_PAGER_EN.md").read_text(encoding="utf-8")
        self.assertIn("Six-pager (EN draft)", en)
        self.assertIn("## FAQ-1. Current state analysis", en)
        self.assertIn("## Sources (footnotes)", en)
        self.assertIn("## Appendices (Excel)", en)
        self.assertIn("unit_economics.xlsx", en)  # приложения тоже в EN-версии
        ru = (self.pdir / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        self.assertIn("## FAQ-1. Анализ текущего состояния", ru)  # RU не пострадала
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER_EN.docx").exists())

    def test_strict_gate_blocks_build_on_check_errors(self):
        claims.add(self.pdir, "Факт без источника", "fact", [], grade="B")  # ошибка check
        with self.assertRaises(PfsError) as ctx:
            finish.run(self.pdir)
        self.assertIn("автопроверка", str(ctx.exception))
        # пакет не собран
        self.assertFalse((self.pdir / "outputs" / "REPORT.md").exists())
        self.assertFalse((self.pdir / "outputs" / "attachments" / "unit_economics.xlsx").exists())

    def test_summary_reports_missing_docs(self):
        res = finish.run(self.pdir)
        # project.create кладёт только 00_brief.md; тест добавил 02 и 04
        self.assertIn("03_options.md", res["missing_docs"])
        self.assertIn("06_validation_plan.md", res["missing_docs"])
        self.assertNotIn("02_situation.md", res["missing_docs"])
        text = finish.summary_text(res, self.pdir)
        self.assertIn("Собрано", text)
        self.assertIn("Нет документов", text)
        self.assertIn("03_options.md", text)

    def test_stale_registry_warns_before_rebuild(self):
        export.build(self.pdir)
        export.save_state(self.pdir)
        claims.add(self.pdir, "Ещё гипотеза", "hypothesis", [], grade="D")
        res = finish.run(self.pdir)  # предупреждение снято свежей сборкой
        self.assertEqual(len(res["stale_warnings"]), 1)
        self.assertIn("+1 claims", res["stale_warnings"][0])
        self.assertEqual(export.freshness_warnings(self.pdir), [])

    def test_cli_finish_exit_zero(self):
        rc = cli.main(["finish", "--project", self.pdir.name, "--no-deck"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
