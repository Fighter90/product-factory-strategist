"""PRO-47: линтер содержания six-pager — проверка документа комитета, а не только тегов.

Сломанный six-pager проходил `pfs check --strict` со счётом 100/100: проверка смотрела
на теги [C###] у чисел и обязательные заголовки рабочих документов, но не на то, что
читает комитет. Контракт выпуска:
1. tests/fixtures/six_pager_good.md (эталон структуры по SIX_PAGER_PROMPT.md) — 0 ошибок.
2. Текущие six-pager проектов демо и cvstart-EU — не меньше 10 ошибок по пунктам 3–6.
3. Каждый пункт спецификации 1–8 ловится отдельной проверкой; пункт 9 — предупреждения.
4. Пороги и списки — config/quality_gate.json → "sixpager" (не в коде).
5. Подключение: pfs check --six-pager; автоматически в --strict (если файл есть);
   затвор pfs finish падает на ошибках линтера; обычный pfs check не меняется.

Запуск: python3 -m unittest tests.test_sixpager_lint -v
"""
import os
import shutil
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-splint-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, cli, core, finish, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402
from tools.pfs import sixpager_lint  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
GOOD = (REPO / "tests" / "fixtures" / "six_pager_good.md").read_text(encoding="utf-8")
GATE = core.read_json(core.CONFIG / "quality_gate.json")


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Что известно\n\n- Рынок 40 млрд [C001].\n", encoding="utf-8")
    (out / "03_options.md").write_text(
        "# 03 · Варианты\n\n## Вариант A: оставить как есть\n\n## Вариант B: платный тариф\n"
        "## Вариант C: закрыть\n", encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# 04 · Стратегия\n\n## Аудитория\n\nФрилансеры [C001].\n", encoding="utf-8")


class SixPagerLintTests(unittest.TestCase):
    """Пункты 1–9 спецификации PRO-47 на эталоне и его мутациях."""

    def setUp(self):
        slug = "splint-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("Six-pager линт", "Как монетизировать TimeTrack?",
                                   slug=slug)
        (self.pdir / "outputs" / "SIX_PAGER.md").write_text(GOOD, encoding="utf-8")

    def write(self, text: str) -> None:
        (self.pdir / "outputs" / "SIX_PAGER.md").write_text(text, encoding="utf-8")

    def run_lint(self) -> dict:
        return sixpager_lint.run(self.pdir)

    def errs(self) -> list[str]:
        return self.run_lint()["errors"]

    def points(self, *nums: int) -> int:
        pt = self.run_lint()["points"]
        return sum(pt.get(str(n), 0) for n in nums)

    # ---------- эталон ----------

    def test_good_fixture_passes_with_zero_errors_and_warnings(self):
        res = self.run_lint()
        self.assertEqual(res["errors"], [], f"эталон должен проходить чисто: {res['errors']}")
        self.assertEqual(res["warnings"], [], f"эталон без предупреждений: {res['warnings']}")
        self.assertTrue(res["checked"])

    # ---------- пункт 1: структура ----------

    def test_point1_structure_missing_faq_and_order(self):
        self.write(GOOD.replace("## FAQ-4. Тактики. Детализируйте каждую инициативу "
                                "до конкретных тактик.\n", ""))
        errs = "\n".join(self.errs())
        self.assertIn("FAQ-4", errs, "пропуск FAQ-4 ловится")
        self.assertIn("нет раздела", errs)
        # порядок: дубликат FAQ-3 после FAQ-5 — «разделы не по порядку»
        self.write(GOOD.replace("## FAQ-6. Метрики успеха. KPI в двух плоскостях",
                                "## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.\n\n"
                                "## FAQ-6. Метрики успеха. KPI в двух плоскостях"))
        self.assertTrue(any("не по порядку" in e for e in self.errs()),
                        f"нарушение порядка FAQ ловится: {self.errs()}")

    def test_point1_subpoints_missing(self):
        self.write(GOOD.replace("### 1.1 Обзор рынка: тренды, вызовы и возможности\n", "")
                       .replace("### 2.2 Барьеры на каждом этапе пути\n", ""))
        errs = "\n".join(self.errs())
        self.assertIn("1.1", errs, "нет подпункта 1.1")
        self.assertIn("2.2", errs, "нет подпункта 2.2")

    def test_point1_working_doc_headings_flagged(self):
        self.write(GOOD.replace("### Инициативы выбранного направления (драйверы)",
                                "### 03 · Варианты — тестовый документ\n\n"
                                "#### Вариант A. Оставить как есть\n\n"
                                "### Инициативы выбранного направления (драйверы)"))
        errs = "\n".join(self.errs())
        self.assertIn("рабочего документа", errs, "заголовки рабочих документов ловятся")
        self.assertIn("03 · Варианты", errs)
        self.assertIn("Вариант A", errs)

    # ---------- пункт 2: объём ----------

    def test_point2_volume_over_limit(self):
        limit = GATE["sixpager"]["max_words"]
        self.write(GOOD.replace("## Источники (сноски)",
                                " ".join(["слово"] * (limit + 100)) + "\n\n## Источники (сноски)"))
        errs = "\n".join(self.errs())
        self.assertIn("объём", errs, "переполнение объёма ловится")
        self.assertIn(str(limit), errs, "в сообщении назван порог из quality_gate.json")

    def test_point2_volume_excludes_tables_and_appendices(self):
        # PRO-46: бюджет основного текста — без таблиц и сносок; таблицы (матрица,
        # KPI, конкуренты) и разделы после «Источники» в объём не считаются
        limit = GATE["sixpager"]["max_words"]
        tables = "\n".join("| Ключ " + "слово " * 20 + "|\n" + "|---|\n" + "| значение " + "слово " * 20 + "|\n"
                           for _ in range(60))
        self.write(GOOD.replace("## Источники (сноски)",
                                tables + "\n\n## Источники (сноски)\n\n[^1]: " + "слово " * 500))
        self.assertEqual([e for e in self.errs() if "объём" in e], [],
                         "таблицы и сноски не считаются в объёме основного текста")

    # ---------- пункт 3: остатки шаблона ----------

    def test_point3_template_leftovers_flagged(self):
        self.write(GOOD + "\nТаблица персон (заполните):\n\n"
                   "| | Сегмент 1 | Сегмент 2 |\n|---|---|---|\n"
                   "| **Кто они?** | … | … |\n\n"
                   "- __% — Инициатива 1;\n\n"
                   "Допущения [укажите теги]: ARPU.\n\n"
                   "KPI в двух направлениях: **1) Бизнес** — деньги и база.\n")
        errs = "\n".join(self.errs())
        for marker in ("заполните", "Сегмент 1", "…", "__%", "Инициатива 1",
                       "укажите теги", "KPI в двух направлениях"):
            self.assertIn(marker, errs, f"остаток шаблона «{marker}» не пойман")

    # ---------- пункт 4: таблицы ----------

    def test_point4_empty_cell_in_required_column(self):
        self.write(GOOD.replace(
            "| Автотрекинг | сбор часов без ручного ввода | не думать про таймер, приватность |",
            "| Автотрекинг | сбор часов без ручного ввода | — |"))
        errs = "\n".join(self.errs())
        self.assertIn("Потребности", errs, "«—» в столбце «Потребности» ловится")
        self.assertIn("пусто", errs)

    def test_point4_duplicate_column_and_ragged_row(self):
        self.write(GOOD + "\n| Один | Дубль |\n|---|---|\n| значение | значение |\n"
                   "| второе | второе |\n\n| Раз | Два |\n|---|---|\n| только одна |\n")
        errs = "\n".join(self.errs())
        self.assertIn("повторяет соседний", errs, "столбец-дубль ловится")
        self.assertIn("ячеек", errs, "рваная строка таблицы ловится")

    def test_point4_glue_cell(self):
        self.write(GOOD + "\n| Ситуация | Реакция |\n|---|---|\n"
                   "| сделали шаг. → цель достигнута | решение принято |\n")
        errs = "\n".join(self.errs())
        self.assertIn("склейка", errs, "склейка «текст. → цель» в ячейке ловится")

    # ---------- пункт 5: служебные ID ----------

    def test_point5_service_ids_without_decoding(self):
        self.write(GOOD + "\nпо плану D003 сделать\n"
                   "проверим H3 на старте\n"
                   "веха M4 закрыта\n"
                   "декомпозиция WBS P2\n"
                   "см. [02, Q4]\n"
                   "файл 02_situation.md\n"
                   "поток C→A\n"
                   "гипотезы C0xx\n"
                   "(по данным 03, Q2)\n")
        errs = "\n".join(self.errs())
        for marker in ("D003", "H3", "M4", "WBS P2", "02, Q4", "02_situation.md",
                       "C→A", "C0xx", "03, Q2"):
            self.assertIn(marker, errs, f"служебный ID «{marker}» без расшифровки не пойман")
        # расшифрованный D001 из эталона («Решение D001 — …») не ловится — см. эталон-тест

    # ---------- пункт 6: арифметика ----------

    def test_point6_contributions_do_not_sum_to_100(self):
        self.write(GOOD.replace("- 35% — маржинальные отчёты", "- 30% — маржинальные отчёты")
                       .replace("- 25% — онбординг и импорт", "- 20% — онбординг и импорт"))
        errs = "\n".join(self.errs())
        self.assertIn("в сумме", errs, "сумма вкладов ≠ 100% ловится")
        self.assertIn("90", errs, "в сообщении названа фактическая сумма")

    def test_point6_metric_mismatch_between_sections(self):
        self.write(GOOD.replace("## FAQ-6. Метрики успеха. KPI в двух плоскостях",
                                "ARPU 31 для командного тарифа.\n\n"
                                "## FAQ-6. Метрики успеха. KPI в двух плоскостях"))
        errs = "\n".join(self.errs())
        self.assertIn("ARPU", errs, "расхождение ARPU между разделами ловится")
        self.assertIn("29", errs)
        self.assertIn("31", errs)

    def test_point6_calculation_does_not_add_up(self):
        self.write(GOOD.replace("**CM = 21,75**", "**CM = 30,00**"))
        errs = "\n".join(self.errs())
        self.assertIn("не сходится", errs, "ошибка в формула → подстановка → результат ловится")
        self.assertIn("29", errs, "в сообщении видна подстановка")

    # ---------- пункт 7: сноски ----------

    def test_point7_footnote_listed_but_not_cited(self):
        self.write(GOOD.replace("## Приложения (Excel)",
                   "9. **S009** — Лишний источник — https://example.com/x\n\n"
                   "## Приложения (Excel)"))
        errs = "\n".join(self.errs())
        self.assertIn("S009", errs, "непроцитированная сноска ловится")
        self.assertIn("не процитированы", errs)

    def test_point7_cited_but_not_listed(self):
        self.write(GOOD.replace(
            "1. **S001** — Обзор рынка тайм-трекеров: объём и динамика "
            "— https://example.com/timetracking-market\n", ""))
        errs = "\n".join(self.errs())
        self.assertIn("S001", errs, "цитируемая сноска без записи в списке ловится")
        self.assertIn("нет в списке", errs)

    def test_point7_pro49_footnote_definitions_are_citations(self):
        # PRO-46: текст пишет writer по спецификации (PRO-49) — маркеры [^N] в тексте,
        # определения `[^N]: **S###** …` внизу. Сырых тегов [S###] в теле нет, но
        # источники определений — цитированные: такой документ проходит пункт 7.
        body = ("Рынок тайм-трекеров оценивается в 3–5 млрд $ при росте 11–14% в год[^1].\n\n"
                "## Источники (сноски)\n\n"
                "[^1]: **S001** — example.com — Обзор рынка тайм-трекеров — 2026-05-01 — "
                "https://example.com/timetracking-market — сила B\n")
        self.write(body)
        self.assertEqual([e for e in self.errs() if "S001" in e], [],
                         "определение [^N]: **S###** — цитирование: лишних сносок нет")
        # определение САМО является записью списка: «нет в списке» не ловится
        self.write(body + "\n## Приложения\n\n| Файл |\n|---|\n")
        self.assertNotIn("нет в списке", "\n".join(self.errs()))

    def test_point7_pro49_markers_without_sources_are_not_footnote_errors(self):
        # маркер [^9] без S### и без определения — не сноска-источник: пункт 7 молчит
        self.write(GOOD + "\nВывод следует из расчёта[^9].\n")
        self.assertEqual([e for e in self.errs() if "сноск" in e.lower()], [])

    # ---------- пункт 8: язык ----------

    def test_point8_cyrillic_in_en_version(self):
        (self.pdir / "outputs" / "SIX_PAGER_EN.md").write_text(
            "# Demo: Six-pager (EN)\n\nMarket is fine.\n\nРынок большой.\n",
            encoding="utf-8")
        errs = "\n".join(self.errs())
        self.assertIn("SIX_PAGER_EN.md", errs, "кириллица в EN-версии ловится")
        self.assertIn("кириллица", errs)

    def test_point8_banned_terms_in_ru_version(self):
        self.write(GOOD + "\nФидбек соберём асап.\n")
        errs = "\n".join(self.errs())
        self.assertIn("фидбек", errs, "англицизм вне белого списка глоссария ловится")
        self.assertIn("асап", errs)

    # ---------- пункт 9: предупреждения ----------

    def test_point9_long_paragraph_and_wide_table_are_warnings(self):
        self.write(GOOD + "\n" + " ".join(["слово"] * 130) + "\n"
                   "\n|a|b|c|d|e|f|g|\n|---|---|---|---|---|---|---|\n"
                   "|1|2|3|4|5|6|7|\n")
        res = self.run_lint()
        self.assertEqual(res["errors"], [], "пункт 9 — предупреждения, не ошибки")

    def test_point9_long_paragraph_and_wide_table_are_warnings(self):
        self.write(GOOD + "\n" + " ".join(["слово"] * 130) + "\n"
                   "\n|a|b|c|d|e|f|g|\n|---|---|---|---|---|---|---|\n"
                   "|1|2|3|4|5|6|7|\n")
        res = self.run_lint()
        self.assertEqual(res["errors"], [], "пункт 9 — предупреждения, не ошибки")
        warns = "\n".join(res["warnings"])
        self.assertIn("абзац", warns, "длинный абзац — предупреждение")
        self.assertIn("столбцов", warns, "широкая таблица — предупреждение")

    def test_point9_footnote_definitions_are_not_prose(self):
        # PRO-46: подряд идущие определения сносок — не абзац документа: даже
        # длинный список сносок не даёт ложного «абзац больше N слов»
        defs = "\n".join(f"[^{k}]: **S{k:03d}** — example.com — " + "описание источника " * 8
                         for k in range(1, 6))
        self.write(GOOD.replace("1. **S001** — Обзор рынка тайм-трекеров: объём и динамика "
                                "— https://example.com/timetracking-market",
                                "[^1]: **S001** — example.com — " + "описание источника " * 8)
                   + "\n" + defs.split("\n", 1)[1] + "\n")
        res = self.run_lint()
        self.assertEqual([w for w in res["warnings"] if "абзац" in w], [],
                         "определения сносок — не абзац: предупреждения о длине нет")

    # ---------- конфиг ----------

    def test_thresholds_and_lists_live_in_quality_gate(self):
        sp = GATE.get("sixpager")
        self.assertIsInstance(sp, dict, "в quality_gate.json нет блока sixpager")
        self.assertEqual(sp["max_words"], 3500)
        self.assertEqual(sp["warn_paragraph_words"], 120)
        self.assertEqual(sp["warn_table_cols"], 6)
        for lang in ("ru", "en"):
            sec = sp["sections"][lang]
            self.assertEqual(len(sec["faq"]), 6, f"{lang}: шесть секций FAQ")
            self.assertIn("1.1", sec["subpoints"]["FAQ-1"])
            self.assertTrue(sec["template_markers"], f"{lang}: маркеры шаблона в конфиге")
        self.assertTrue(sp["service_id_patterns"], "паттерны служебных ID в конфиге")


class WrittenRealSixPagersTests(unittest.TestCase):
    """Приёмка PRO-46: six-pager демо и cvstart-EU НАПИСАНЫ six-pager-writer'ом
    по пакету данных (а не склеены из документов 02/03/04/06) — проходят линтер
    без ошибок по пунктам 3–6 (остатки шаблона, таблицы, служебные ID, арифметика).
    Если проекта или документа нет в репозитории — тест пропускается."""

    def check_doc(self, pdir_name: str) -> None:
        src = REPO / "projects" / pdir_name / "outputs" / "SIX_PAGER.md"
        if not src.exists():
            self.skipTest(f"нет {src}")
        scratch = tempfile.mkdtemp(prefix="pfs-test-spreal-")
        os.environ["PFS_PROJECTS_DIR"] = scratch
        try:
            pdir = project.create("Реальный six-pager", "проверка содержания", slug="real-sp")
        finally:
            os.environ["PFS_PROJECTS_DIR"] = TMP
        (pdir / "outputs" / "SIX_PAGER.md").write_text(
            src.read_text(encoding="utf-8"), encoding="utf-8")
        res = sixpager_lint.run(pdir)
        pts_3_6 = sum(res["points"].get(str(n), 0) for n in (3, 4, 5, 6))
        self.assertEqual(pts_3_6, 0,
                         f"{pdir_name}: написанный документ не должен иметь ошибок "
                         f"по пунктам 3–6, получили {pts_3_6}: {res['errors'][:10]}")

    def test_demo_six_pager_written_passes(self):
        self.check_doc("демо")

    def test_cvstart_eu_six_pager_written_passes(self):
        self.check_doc("вывод-проекта-на-европейский-рынок-cvstart-org")


class SixPagerWiringTests(unittest.TestCase):
    """Подключение: check --six-pager / --strict, затвор pfs finish; обычный check не меняется."""

    def setUp(self):
        # база — копия демо: рабочие документы проходят проверки структуры,
        # ломаем только six-pager (предмет этого теста)
        slug = "spwire-" + self.id().rsplit(".", 1)[-1][:40]
        self.projects = Path(tempfile.mkdtemp(prefix=slug))
        shutil.copytree(REPO / "projects" / "демо", self.projects / "демо")
        (self.projects / ".active").write_text("демо", encoding="utf-8")
        self._old_projects_dir = os.environ.get("PFS_PROJECTS_DIR")
        os.environ["PFS_PROJECTS_DIR"] = str(self.projects)
        self.pdir = self.projects / "демо"
        self.write_broken()

    def tearDown(self):
        if self._old_projects_dir is None:
            os.environ.pop("PFS_PROJECTS_DIR", None)
        else:
            os.environ["PFS_PROJECTS_DIR"] = self._old_projects_dir
        shutil.rmtree(self.projects, ignore_errors=True)

    def write_broken(self) -> None:
        (self.pdir / "outputs" / "SIX_PAGER.md").write_text(
            GOOD.replace("**Вывод (умозаключение):** экономика сходится, следовательно "
                         "платный тариф запускаем на личном сегменте.",
                         "Таблица персон (заполните): см. D003"),
            encoding="utf-8")

    def test_default_check_ignores_six_pager_content(self):
        res = check.run(self.pdir)
        lint_errors = [e for e in res["errors"]
                       if "остаток шаблона" in e or "лишний заголовок" in e
                       or "нет раздела FAQ" in e or "не по порядку" in e]
        self.assertFalse(lint_errors,
                         "обычный pfs check не проверяет содержание six-pager")

    def test_sixpager_flag_and_strict_turn_lint_on(self):
        res = check.run(self.pdir, sixpager=True)
        self.assertTrue(res.get("sixpager_checked"))
        self.assertTrue([e for e in res["errors"] if e.startswith("SIX_PAGER.md")],
                        "с флагом --six-pager ошибки содержания появляются")

    def test_cli_six_pager_flag_exits_nonzero_on_errors(self):
        def run_flag():
            args = cli.build_parser().parse_args(["--project", self.pdir.name,
                                                  "check", "--six-pager"])
            args.f(args)
        with self.assertRaises(SystemExit) as ctx:
            run_flag()
        self.assertEqual(ctx.exception.code, 1)
        # без флагов — нулевой код выхода
        rc = cli.main(["--project", self.pdir.name, "check", "--json"])
        self.assertEqual(rc, 0)

    def test_finish_gate_blocks_on_broken_six_pager(self):
        with self.assertRaises(PfsError) as ctx:
            finish.run(self.pdir)
        self.assertIn("SIX_PAGER.md", str(ctx.exception),
                      "затвор finish называет ошибки линтера six-pager")
        # нет файла — затвор пропускает линтер и собирает пакет
        (self.pdir / "outputs" / "SIX_PAGER.md").unlink()
        res = finish.run(self.pdir)
        self.assertTrue((self.pdir / "outputs" / "REPORT.md").exists())


if __name__ == "__main__":
    unittest.main()
