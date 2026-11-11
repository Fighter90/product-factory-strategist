"""pfs finish — командная цепочка до финального пакета (PRO-31).

Порядок критичен: Excel ДО REPORT (Приложение E полно) и ДО SIX_PAGER (таблица
приложений полна), снимок реестра — ПОСЛЕ сборки, дека — из готового SIX_PAGER.
Повторный вызов идемпотентен. Флаги: no_deck, en (EN-черновик six-pager).
PRO-41: предупреждения о несвежем реестре печатаются ровно один раз.

Запуск: python3 -m unittest tests.test_finish -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-finish-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import claims, cli, core, export, finish, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

EXCEL = {"unit_economics.xlsx", "growth_model.xlsx", "cohort_retention.xlsx", "market_sizing.xlsx"}


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Короткий ответ\n\nРынок 40 млрд [C001].\n\n"
        "## Что известно\n\n- Рынок 40 млрд [C001].\n\n"
        "## Чего мы не знаем\n\n- Доля рынка конкурентов.\n\n"
        "## Вопросы, которые могут изменить решение\n\n- Платёжеспособность сегмента?\n",
        encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# 04 · Стратегия\n\n## Аудитория\n\nСоискатели [C001].\n\n"
        "## Альтернативы\n\n- Вариант A: оставить как есть.\n- Вариант B: семейный пакет.\n"
        "- Вариант C: закрыть направление.\n\n"
        "## Выбранное направление\n\nСемейный пакет [C001].\n\n"
        "## Осознанные отказы\n\n- Не выходим в B2B.\n\n"
        "## Экономика\n\nARPU 350, CAC 600 [C001].\n",
        encoding="utf-8")


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
        self.assertEqual(len(res["artifacts"]), 9)
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

    def test_summary_of_rebuild_does_not_advise_rebuild(self):
        # PRO-63 п.3: сводка finish говорит «снято свежей пересборкой» и в том же
        # предложении не может требовать «Пересоберите» — сообщения противоречат друг другу.
        export.build(self.pdir)
        export.save_state(self.pdir)
        claims.add(self.pdir, "Ещё основание", "hypothesis", [], grade="D")  # реестр устарел
        res = finish.run(self.pdir)
        summary = finish.summary_text(res)
        self.assertIn("снято свежей пересборкой", summary)
        self.assertNotIn("Пересоберите", summary)
        self.assertNotIn("⚠", summary)
        # и после сборки предупреждений больше нет
        self.assertEqual(export.freshness_warnings(self.pdir), [])

    def test_no_deck_flag_skips_deck_only(self):
        res = finish.run(self.pdir, no_deck=True)
        self.assertFalse((self.pdir / "outputs" / "presentations" / "deck.html").exists())
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER.docx").exists())
        self.assertEqual(len(res["artifacts"]), 8)

    def test_no_deck_log_entry_explains_skip(self):
        # Ревью PRO-63 (круг 2, п.2): финальный finish демо шёл с --no-deck, в журнале
        # остался пакет без deck.html — без пояснения это выглядит как регресс сборки деки.
        # Запись журнала сама объясняет пропуск: «(без деки: --no-deck)».
        finish.run(self.pdir, no_deck=True)
        entries = core.read_jsonl(self.pdir / "log.jsonl")
        entry = [e for e in entries if e.get("tool") == "pfs finish"][-1]
        self.assertIn("--no-deck", entry["msg"])
        # и обычный запуск пояснение не содержит
        finish.run(self.pdir)
        entry = [e for e in core.read_jsonl(self.pdir / "log.jsonl")
                 if e.get("tool") == "pfs finish"][-1]
        self.assertNotIn("--no-deck", entry["msg"])

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

    def test_en_unit_econ_table_is_english(self):
        # Ревью PRO-31 (п.3): заголовок таблицы юнит-экономики и подписи строк идут через _t —
        # EN-черновик не оставляет русского заголовка «Формула | Расчёт | Результат».
        core.write_json(self.pdir / "calcs.json",
                        {"unit_econ": {"arpu": 350, "vc_share": 0.2, "cac": 600,
                                       "churn_month": 0.03, "note": "ARPU и CAC — оценка [C001]"}})
        finish.run(self.pdir, en=True)
        en = (self.pdir / "outputs" / "SIX_PAGER_EN.md").read_text(encoding="utf-8")
        self.assertIn("| Formula | Calculation | Result |", en)
        self.assertNotIn("Формула | Расчёт | Результат", en)
        self.assertIn("Average paying lifetime = 1 / churn", en)
        ru = (self.pdir / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        self.assertIn("| Формула | Расчёт | Результат |", ru)  # RU не пострадала

    def test_six_pager_faq1_fallback_ru_text_unchanged(self):
        # Ревью PRO-31 (п.2): RU-заглушка FAQ-1 — исходный текст («…буллетами с жирными заголовками»),
        # ключ в _EN совпадает с ним дословно, поэтому EN-черновик переводит именно его.
        key = ("> Раздел появится после шага «situation» (02_situation.md): объём и динамика рынка "
               "диапазонами, ключевые тренды буллетами с жирными заголовками.")
        self.assertIn(key, export._EN)
        (self.pdir / "outputs" / "02_situation.md").unlink()  # нет секций → срабатывает заглушка
        ru = export.build_six_pager(self.pdir, with_calcs=False).read_text(encoding="utf-8")
        en = export.build_six_pager(self.pdir, with_calcs=False, lang="en").read_text(encoding="utf-8")
        self.assertIn("буллетами с жирными заголовками", ru)
        self.assertIn("key trends as bold bullets", en)

    def test_strict_gate_blocks_build_on_check_errors(self):
        out = self.pdir / "outputs"
        (out / "06_validation_plan.md").write_text(
            "# 06 · План проверки\n\n## Ожидаемое изменение\n\nУдержание с 32% до 40% [C099].\n",
            encoding="utf-8")  # ссылка на несуществующее утверждение — ошибка check
        with self.assertRaises(PfsError) as ctx:
            finish.run(self.pdir)
        self.assertIn("автопроверка", str(ctx.exception))
        self.assertIn("C099", str(ctx.exception))
        # пакет не собран
        self.assertFalse((out / "REPORT.md").exists())
        self.assertFalse((out / "attachments" / "unit_economics.xlsx").exists())

    def test_check_warnings_do_not_block_build(self):
        # Ревью PRO-31 (п.4): затвор строгий — останавливают ТОЛЬКО ошибки check (эквивалент
        # `pfs check --strict`, где --strict это «ошибки → код 1»); предупреждения сборке не мешают.
        claims.add(self.pdir, "Гипотеза без оснований", "hypothesis", [])
        res = finish.run(self.pdir)  # сборка прошла, несмотря на предупреждение
        self.assertTrue(any("без оснований" in w for w in res["check"]["warnings"]))
        self.assertFalse(res["check"]["errors"])
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())

    def test_summary_reports_missing_docs(self):
        res = finish.run(self.pdir)
        # project.create кладёт только 00_brief.md; тест добавил 02 и 04
        self.assertIn("03_options.md", res["missing_docs"])
        self.assertIn("06_validation_plan.md", res["missing_docs"])
        self.assertNotIn("02_situation.md", res["missing_docs"])
        text = finish.summary_text(res)
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
        rc = cli.main(["--project", self.pdir.name, "finish", "--no-deck"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())

    def test_cli_finish_prints_stale_warning_once(self):
        # PRO-41: cmd_finish печатал предупреждения о несвежем реестре дважды —
        # сырой цикл по res["stale_warnings"] и повтор внутри summary_text.
        # PRO-63: в сводке finish только факты («снято свежей пересборкой»), без
        # противоречащего советa «Пересоберите» — пересборка уже выполнена.
        export.build(self.pdir)
        export.save_state(self.pdir)
        claims.add(self.pdir, "Ещё гипотеза", "hypothesis", [], grade="D")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(["--project", self.pdir.name, "finish", "--no-deck"])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("+1 claims", out)  # предупреждение присутствует в выводе
        self.assertEqual(out.count("+1 claims"), 1)  # ровно один раз на вызов
        self.assertNotIn("Реестр изменился после последнего экспорта", out)
        self.assertIn("снято свежей пересборкой", out)
        self.assertNotIn("Пересоберите", out)


if __name__ == "__main__":
    unittest.main()
