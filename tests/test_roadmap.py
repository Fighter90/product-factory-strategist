"""Роудмапы в xlsx (pfs roadmap, PRO-70): два формата быстрых гибких роудмапов
из Google Sheets — «по проектам» и «по фичам/по проектам», данные из 04 или
roadmap.json, заливка отрезков цветом статуса, интеграция в поток (pfs step
strategy done, pfs export). Запуск: python3 -m unittest tests.test_roadmap -v
"""
import datetime as dt
import io
import json
import os
import re
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-roadmap-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, core, project, roadmap  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402
from tools.pfs.xlsx import Workbook, sheet_names  # noqa: E402

STRATEGY_04 = """# 04 · Продуктовая стратегия — Семейный трекер

## Выбранное направление

Семейный пакет [C001].

## Outcome-роадмап

- **Этап 1 (бета):** уведомления о смене статуса; семейный доступ. **Результат:** удержание M1 ≥ 40% [C002].
- **Этап 2 (монетизация):** платные тарифы; оплата картой. **Результат:** ARPU 350 ₽ [C003].
"""


def make_04(pdir: Path) -> None:
    out = pdir / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "04_product_strategy.md").write_text(STRATEGY_04, encoding="utf-8")


def _q(d: dt.date, k: int = 0) -> str:
    """Метка квартала с поправкой на k кварталов вперёд: Q4 2026."""
    t = d.year * 12 + d.month - 1 + 3 * k
    return f"Q{t % 12 // 3 + 1} {t // 12}"


class StrategyRoadmapTests(unittest.TestCase):
    """Этапы outcome-роадмапа 04 → проекты, тактики → фичи; кварталы по умолчанию."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Роудмап из стратегии", "Почему падает удержание?", slug="rm-strat")
        make_04(cls.pdir)
        cls.path = roadmap.run(cls.pdir)
        cls.spec, cls.source = roadmap.load_spec(cls.pdir)
        cls.wb = roadmap.build_workbook(cls.spec, None)

    def test_creates_valid_xlsx_with_two_formats(self):
        self.assertEqual(self.path, self.pdir / "outputs" / f"roadmap-{self.pdir.name}.xlsx")
        self.assertTrue(self.path.exists())
        with zipfile.ZipFile(self.path) as z:
            self.assertIsNone(z.testzip())
        self.assertEqual(sheet_names(self.path), ["Проекты", "Фичи по проектам", "Легенда"])

    def test_source_is_strategy_04(self):
        self.assertEqual(self.source, "04_product_strategy.md")

    def test_projects_sheet_rows_from_stages(self):
        sh = self.wb.sheets[0]
        head = [c["v"] for c in sh.rows[0][:11]]
        self.assertEqual(head[:2], ["Проект", "Инициатива"])
        stage1 = next(r for r in sh.rows[1:] if r[0] == "Этап 1 (бета)")
        self.assertEqual(stage1[1], "Роудмап из стратегии")  # Инициатива — название проекта
        self.assertEqual(stage1[9], {"v": "план", "fill": "blue", "bold": True})  # Статус
        self.assertIn("Результат", stage1[10])  # Комментарий: вор этапа
        stage2 = next(r for r in sh.rows[1:] if r[0] == "Этап 2 (монетизация)")
        self.assertEqual(stage2[9]["fill"], "blue")

    def test_default_periods_are_sequential_quarters_from_current(self):
        today = dt.date.today()
        sh = self.wb.sheets[0]
        labels = [c["v"] for c in sh.rows[0][11:]]
        self.assertEqual(labels, [_q(today), _q(today, 1)])
        stage1 = next(r for r in sh.rows[1:] if r[0] == "Этап 1 (бета)")
        self.assertEqual(stage1[11], {"fill": "blue"})       # первый квартал — бар этапа 1
        self.assertIsNone(stage1[12])
        stage2 = next(r for r in sh.rows[1:] if r[0] == "Этап 2 (монетизация)")
        self.assertIsNone(stage2[11])
        self.assertEqual(stage2[12], {"fill": "blue"})       # второй квартал — бар этапа 2

    def test_features_sheet_groups_by_project(self):
        sh = self.wb.sheets[1]
        head = [c["v"] for c in sh.rows[0][:9]]
        self.assertEqual(head[:2], ["Проект", "Фича"])
        groups = [r[0] for r in sh.rows[1:]]
        self.assertEqual(groups, ["Этап 1 (бета)", "Этап 1 (бета)", "Этап 2 (монетизация)", "Этап 2 (монетизация)"])
        names = [r[1] for r in sh.rows[1:]]
        self.assertEqual(names, ["уведомления о смене статуса", "семейный доступ",
                                 "платные тарифы", "оплата картой"])
        durations = [r[5] for r in sh.rows[1:]]
        self.assertEqual(durations, [13, 13, 13, 13])  # квартал ≈ 13 недель

    def test_legend_explains_colors_and_source(self):
        text = "\n".join(" ".join(str(c.get("v") if isinstance(c, dict) else c) for c in row if c is not None)
                         for row in self.wb.sheets[2].rows)
        for word in ("зелёный", "жёлтый", "синий", "красный", "roadmap.json", "04_product_strategy.md"):
            self.assertIn(word, text)


class SpecRoadmapTests(unittest.TestCase):
    """roadmap.json: даты, статусы, команды, риски; месяцы и недели; длительность."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Роудмап из спецификации", "Вопрос?", slug="rm-spec")
        spec = {
            "granularity": "month",
            "projects": [
                {"name": "Проект 1", "team": "Core", "status": "done", "priority": "Высокий",
                 "features": [
                     {"name": "Фича A", "start": "2026-01-05", "end": "2026-01-18"},
                     {"name": "Фича B", "start": "2026-02", "end": "2026-03", "status": "in progress", "risk": "риск"},
                 ]},
                {"name": "Проект 2", "start": "2026-05", "end": "2026-06",
                 "features": [{"name": "Фича C", "status": "не начато"}]},
                {"name": "Проект 3", "features": [{"name": "Без дат", "status": "что-то странное"}]},
            ],
        }
        (cls.pdir / "roadmap.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        cls.spec, cls.source = roadmap.load_spec(cls.pdir)
        cls.path = roadmap.run(cls.pdir)
        cls.wb = roadmap.build_workbook(cls.spec, None)

    def test_source_is_spec_file(self):
        self.assertEqual(self.source, "roadmap.json")

    def test_inheritance_and_project_dates_from_features(self):
        p1 = self.spec["projects"][0]
        self.assertEqual((p1["start"], p1["end"]), ("2026-01-05", "2026-03-31"))  # min/max по фичам
        p2 = self.spec["projects"][1]
        self.assertEqual((p2["start"], p2["end"]), ("2026-05", "2026-06"))
        self.assertEqual(p1["status"], "done")
        f_a = p1["features"][0]
        self.assertEqual((f_a["team"], f_a["status"]), ("Core", "done"))  # наследуют проект

    def test_month_period_columns(self):
        labels = [c["v"] for c in self.wb.sheets[0].rows[0][11:]]
        self.assertEqual(labels, ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"])

    def test_status_fills_on_project_rows(self):
        r1 = next(r for r in self.wb.sheets[0].rows[1:] if r[0] == "Проект 1")
        self.assertEqual(r1[9], {"v": "done", "fill": "green", "bold": True})
        self.assertEqual(r1[11], {"fill": "green"})  # январь покрыт
        self.assertIsNone(r1[14])                    # апрель — вне отрезка
        r3 = next(r for r in self.wb.sheets[0].rows[1:] if r[0] == "Проект 3")
        self.assertEqual(r3[9]["fill"], "gray")      # неизвестный статус — серый

    def test_feature_rows_duration_and_risk(self):
        sh = self.wb.sheets[1]
        fa = next(r for r in sh.rows[1:] if r[1] == "Фича A")
        self.assertEqual(fa[5], 2)                    # 13 дней → 2 недели
        self.assertEqual(fa[2], "Core")
        fb = next(r for r in sh.rows[1:] if r[1] == "Фича B")
        self.assertEqual(fb[5], 9)                    # 2026-02-01…2026-03-31
        self.assertEqual(fb[7], "риск")
        fc = next(r for r in sh.rows[1:] if r[1] == "Фича C")
        self.assertEqual((fc[3], fc[4]), ("2026-05-01", "2026-06-30"))  # даты проекта
        fd = next(r for r in sh.rows[1:] if r[1] == "Без дат")
        self.assertEqual((fd[3], fd[4], fd[5]), ("", "", ""))  # без дат — пусто, не падаем

    def test_spec_granularity_week(self):
        wb = roadmap.build_workbook(self.spec, "week")
        labels = [c["v"] for c in wb.sheets[0].rows[0][11:]]
        self.assertTrue(all(re.fullmatch(r"\d{4}-W\d{2}", x) for x in labels), labels)


class CliIntegrationTests(unittest.TestCase):
    """pfs roadmap / pfs step strategy done / pfs export — генерация роудмапа."""

    def test_cli_roadmap_creates_file(self):
        pdir = project.create("Роудмап CLI", "Вопрос?", slug="rm-cli")
        make_04(pdir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "roadmap"])
        self.assertEqual(rc, 0)
        self.assertTrue((pdir / "outputs" / f"roadmap-{pdir.name}.xlsx").exists())
        self.assertIn("Роудмап", buf.getvalue())

    def test_cli_roadmap_spec_option(self):
        pdir = project.create("Роудмап CLI spec", "Вопрос?", slug="rm-cli-spec")
        spec = {"projects": [{"name": "П", "start": "2026-01", "end": "2026-01",
                              "features": [{"name": "Ф"}]}]}
        (pdir / "my-roadmap.json").write_text(json.dumps(spec), encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "roadmap", "--spec", "my-roadmap.json"])
        self.assertEqual(rc, 0)
        self.assertTrue((pdir / "outputs" / f"roadmap-{pdir.name}.xlsx").exists())

    def test_step_strategy_done_generates_roadmap(self):
        pdir = project.create("Роудмап шаг strategy", "Вопрос?", slug="rm-step")
        make_04(pdir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "step", "strategy", "done", "--note", "согласовано"])
        self.assertEqual(rc, 0)
        self.assertTrue((pdir / "outputs" / f"roadmap-{pdir.name}.xlsx").exists())
        self.assertIn("Роудмап", buf.getvalue())
        # другие шаги роудмап не трогают
        pdir2 = project.create("Роудмап шаг intake", "Вопрос?", slug="rm-step2")
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            cli.main(["--project", pdir2.name, "step", "intake", "done"])
        self.assertNotIn("Роудмап", buf2.getvalue())

    def test_step_strategy_done_without_data_mentions_how_to_fix(self):
        pdir = project.create("Роудмап шаг без 04", "Вопрос?", slug="rm-step3")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "step", "strategy", "done"])
        self.assertEqual(rc, 0)  # шаг отмечен, роудмап собрать нечего
        self.assertIn("Роудмап не собран", buf.getvalue())

    def test_export_runs_roadmap(self):
        pdir = project.create("Роудмап export", "Вопрос?", slug="rm-export")
        make_04(pdir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "export"])
        self.assertEqual(rc, 0)
        self.assertIn("Роудмап", buf.getvalue())
        self.assertTrue((pdir / "outputs" / f"roadmap-{pdir.name}.xlsx").exists())

    def test_no_data_is_a_clear_error(self):
        pdir = project.create("Роудмап пусто", "Вопрос?", slug="rm-empty")
        with self.assertRaises(PfsError):
            roadmap.run(pdir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "roadmap"])
        self.assertEqual(rc, 2)

    def test_cli_roadmap_missing_spec_is_rc2(self):
        # явно указанный несуществующий --spec — rc=2 с сообщением, без traceback;
        # 04 на месте: без проверки откат прошёл бы «успешно»
        pdir = project.create("Роудмап CLI нет spec", "Вопрос?", slug="rm-cli-nospec")
        make_04(pdir)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", pdir.name, "roadmap", "--spec", "no-such.json"])
        self.assertEqual(rc, 2)


class RoadmapValidationTests(unittest.TestCase):
    """Ошибки входа: битые даты, перевёрнутый диапазон, спецификация без проектов."""

    def test_bad_date(self):
        with self.assertRaises(PfsError):
            roadmap.parse_date("январь 2026")

    def test_calendar_invalid_dates_are_pfs_error(self):
        # даты по формату, но недопустимые по календарю — чистая PfsError, а не ValueError
        for bad in ("2026-02-31", "31.04.2026", "29.02.2025", "0000-Q1", "0000-05"):
            with self.assertRaises(PfsError, msg=bad):
                roadmap.parse_date(bad)
            with self.assertRaises(PfsError, msg=f"{bad} (as_end)"):
                roadmap.parse_date(bad, as_end=True)

    def test_date_formats(self):
        self.assertEqual(roadmap.parse_date("2026-Q2"), dt.date(2026, 4, 1))
        self.assertEqual(roadmap.parse_date("2026-03"), dt.date(2026, 3, 1))
        self.assertEqual(roadmap.parse_date("2026-03-05"), dt.date(2026, 3, 5))
        self.assertEqual(roadmap.parse_date("2026"), dt.date(2026, 1, 1))
        self.assertEqual(roadmap.parse_date("05.03.2026"), dt.date(2026, 3, 5))

    def test_inverted_range(self):
        with self.assertRaises(PfsError):
            roadmap.make_periods(dt.date(2026, 5, 1), dt.date(2026, 1, 1), "month")

    def test_spec_without_projects(self):
        pdir = project.create("Роудмап без проектов", "Вопрос?", slug="rm-nop")
        (pdir / "roadmap.json").write_text("{}", encoding="utf-8")
        with self.assertRaises(PfsError):
            roadmap.run(pdir)

    def test_spec_bad_json_shape(self):
        pdir = project.create("Роудмап битый json", "Вопрос?", slug="rm-bad")
        (pdir / "roadmap.json").write_text("[]", encoding="utf-8")
        with self.assertRaises(PfsError):
            roadmap.run(pdir)

    def test_broken_json_spec_is_pfs_error(self):
        # битый JSON спецификации — чистая PfsError, а не traceback JSONDecodeError
        pdir = project.create("Роудмап ломаный json", "Вопрос?", slug="rm-broken")
        (pdir / "roadmap.json").write_text("{bad json", encoding="utf-8")
        with self.assertRaises(PfsError):
            roadmap.run(pdir)

    def test_missing_explicit_spec_is_hard_error(self):
        # --spec указан явно, файла нет — жёсткая PfsError, а не тихий откат к 04
        pdir = project.create("Роудмап нет spec", "Вопрос?", slug="rm-nospec")
        make_04(pdir)  # 04 на месте: без проверки откат прошёл бы «успешно»
        with self.assertRaises(PfsError):
            roadmap.load_spec(pdir, "no-such-roadmap.json")

    def test_directory_as_spec_is_pfs_error(self):
        pdir = project.create("Роудмап каталог как spec", "Вопрос?", slug="rm-dirspec")
        (pdir / "outputs").mkdir(parents=True, exist_ok=True)
        with self.assertRaises(PfsError):
            roadmap.load_spec(pdir, "outputs")

    def test_strategy_without_stages(self):
        pdir = project.create("Роудмап 04 без этапов", "Вопрос?", slug="rm-nostage")
        out = pdir / "outputs"
        out.mkdir(parents=True, exist_ok=True)
        (out / "04_product_strategy.md").write_text("# 04\n\n## Выбранное направление\n\nПакет [C001].\n",
                                                   encoding="utf-8")
        with self.assertRaises(PfsError):
            roadmap.run(pdir)


class XlsxFillStyleTests(unittest.TestCase):
    """Заливки в xlsx-писателе: стили определены, базовые индексы 0–3 не изменились."""

    def test_fill_cell_carries_style_and_saves(self):
        wb = Workbook()
        sh = wb.sheet("Т", widths={1: 10})
        sh.row({"v": "план", "fill": "blue", "bold": True}, "обычный",
               {"v": 0.5, "pct": True}, {"v": "сделано", "fill": "green"})
        p = wb.save(Path(TMP) / "fill-style.xlsx")
        with zipfile.ZipFile(p) as z:
            styles = z.read("xl/styles.xml").decode("utf-8")
            sheet = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
        self.assertEqual(sheet.count('s="11"'), 1)  # синий + жирный = 4 + 3*2 + 1
        self.assertEqual(sheet.count('s="4"'), 1)   # зелёный обычный = 4 + 0*2
        self.assertIn('<fills count="7">', styles)   # none, gray125 + 5 цветов
        self.assertIn('<cellXfs count="14">', styles)  # 4 базовых + 10 заливок

    def test_unknown_fill_raises(self):
        with self.assertRaises(ValueError):
            Workbook().sheet("Т")._cell_xml({"v": "x", "fill": "purple"}, 1, 1)

    def test_base_styles_untouched(self):
        # старые книги не изменились: обычный/жирный/процент/жирный% — те же индексы
        self.assertEqual(Workbook().sheet("Т")._cell_xml({"v": 0.5, "pct": True}, 1, 1),
                         '<c r="A1" s="2"><v>0.5</v></c>')


if __name__ == "__main__":
    unittest.main()
