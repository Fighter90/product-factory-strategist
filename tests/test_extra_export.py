"""Доп. тесты export: REPORT целиком, приложения, _grab, тезисы и экранирование слайдов.

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-xexp-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, decisions, export, project, sources  # noqa: E402
from tools.pfs.xlsx import Workbook  # noqa: E402


def fresh(slug):
    return project.create(f"Отчёт {slug}", "Почему падает удержание подписчиков?", slug=slug)


class ReportBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xrep")
        pdir = cls.pdir
        sources.add(pdir, text="Публичный отчёт о рынке 40 млрд", title="Рынок")
        cls.claim = claims.add(pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        cls.dec = decisions.add(pdir, "Фокус на регионе", "Пилот в одном регионе", "CPO", [cls.claim["id"]],
                                metrics=["Удержание M1: 38% -> 45% @2027-03-01"],
                                review_date="2027-01-01", commitments=["Запустить пилот|PM|2027-02-01"])
        (pdir / "outputs" / "99_extra.md").write_text("# Дополнение\nЗаметки команды.\n", encoding="utf-8")
        cls.report = export.build(pdir)
        cls.text = cls.report.read_text(encoding="utf-8")

    def test_report_name_and_header(self):
        self.assertEqual(self.report, self.pdir / "outputs" / "REPORT.md")
        self.assertTrue(self.text.startswith("# Отчёт xrep: стратегия и обоснование"))
        self.assertIn("Почему падает удержание подписчиков?", self.text)  # бриф вошёл в отчёт

    def test_report_applications(self):
        self.assertIn("# Приложение A. Реестр утверждений", self.text)
        self.assertIn(self.claim["id"], self.text)
        self.assertIn("# Приложение B. Источники", self.text)
        self.assertIn("| S001 | Рынок | — | public |", self.text)
        self.assertIn("# Приложение C. Решения и обязательства", self.text)
        self.assertIn(self.dec["id"], self.text)
        self.assertIn("38% → 45% к 2027-03-01", self.text)  # показатели решения в таблице
        self.assertIn("# Приложение D. Прозрачность", self.text)
        self.assertIn("## Дополнение", self.text)         # не-ORDER документ попал после основных
        self.assertIn("Заметки команды", self.text)
        self.assertNotIn("Приложение E", self.text)       # Excel ещё не собраны — приложения нет

    def test_attachments_appendix_e(self):
        self.assertIsNone(export.attachments_table(self.pdir))
        att = self.pdir / "outputs" / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        (att / "unit_economics.xlsx").write_bytes(b"PK\x03\x04 dummy")
        table = export.attachments_table(self.pdir)
        self.assertIn("| Файл | Листы | Что редактировать |", table)
        self.assertIn("unit_economics.xlsx", table)
        self.assertNotIn("growth_model.xlsx", table)
        text = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertIn("# Приложение E. Excel-расчёты", text)


class GrabAndDeckHelpersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xgrab")
        (cls.pdir / "outputs" / "02_situation.md").write_text(
            "# Ситуация\n## Короткий ответ\nОтток растёт третий месяц подряд.\n"
            "## Что известно\n- рынок 40 млрд\n", encoding="utf-8")

    def test_grab_extracts_named_sections_only(self):
        body = export._grab(self.pdir, "02_situation.md", ("Короткий ответ",))
        self.assertTrue(body.startswith("### Короткий ответ"))
        self.assertIn("Отток растёт третий месяц подряд", body)
        self.assertNotIn("рынок 40 млрд", body)  # соседняя секция не затянута

    def test_grab_without_match_returns_none(self):
        # целые документы собирает _insert_doc; _grab без совпадений — None
        self.assertIsNone(export._grab(self.pdir, "02_situation.md", ("Нет такого раздела",)))
        self.assertIsNone(export._grab(self.pdir, "нет_файла.md", ()))

    def test_grab_never_matches_document_h1(self):
        # дефект «### Рынок» + копия всего документа: имя секции не должно матчать H1
        (self.pdir / "outputs" / "02b.md").write_text(
            "# Ситуация по рынку удержания\n## Короткий ответ\nтут короткий ответ\n",
            encoding="utf-8")
        self.assertIsNone(export._grab(self.pdir, "02b.md", ("Рынок",)))

    def test_grab_cuts_only_on_section_boundaries(self):
        body1 = "очень длинный текст первой секции " * 30
        body2 = "текст второй секции " * 40
        (self.pdir / "outputs" / "08_long.md").write_text(
            "# Длинный\n## Первая\n" + body1 + "\n## Вторая\n" + body2, encoding="utf-8")
        body = export._grab(self.pdir, "08_long.md", ("Первая", "Вторая"), cap=100)
        self.assertNotIn("обрезано", body)  # маркеров обрезки нет
        self.assertIn("очень длинный текст первой секции", body)  # секция атомарна
        self.assertNotIn("Вторая", body)  # не влезла в cap — не вставляется вовсе

    def test_insert_doc_demotes_headings_and_dedups_after_grab(self):
        (self.pdir / "outputs" / "09_doc.md").write_text(
            "# Варианты: тест\n## Вариант A: первый\n### Возражения\n- возражение\n"
            "## Рекомендация\nвыбор B\n", encoding="utf-8")
        reg: dict = {}
        grabbed = export._grab(self.pdir, "09_doc.md", ("Рекомендация",), reg=reg)
        self.assertIn("### Рекомендация", grabbed)
        doc = export._insert_doc(self.pdir, "09_doc.md", reg=reg)
        self.assertIn("### Варианты: тест", doc)      # H1 → ###
        self.assertIn("#### Вариант A: первый", doc)  # H2 → ####
        self.assertIn("##### Возражения", doc)        # H3 → #####
        self.assertNotIn("Рекомендация", doc)         # уже вставлена через _grab
        self.assertIsNone(export._insert_doc(self.pdir, "09_doc.md", reg=reg))  # всё вставлено
        self.assertIsNone(export._insert_doc(self.pdir, "нет_файла.md"))
        self.assertIn("# Варианты: тест", export._insert_doc(self.pdir, "09_doc.md"))  # без reg — целиком

    def test_points_rules_and_slide_escaping(self):
        pts = export._points("- один\n> два\n| три | четыре |\n\nПервое предложение. Второе предложение.")
        self.assertEqual(pts, ["один", "два", "три", "Первое предложение."])  # списки, цитаты, 1-й столбец таблицы
        self.assertEqual(export._points("повтор\nповтор"), ["повтор"])         # дубль подряд схлопывается
        self.assertEqual(len(export._points("\n".join(f"- п{i}" for i in range(9)))), 6)  # максимум 6
        long = export._points("ж" * 300)[0]
        self.assertEqual(len(long), 160)
        self.assertTrue(long.endswith("…"))
        slide = export._slide("Титул", ["<b>жир</b>"])
        self.assertIn("<h2>Титул</h2>", slide)
        self.assertIn("&lt;b&gt;жир&lt;/b&gt;", slide)  # HTML в тезисах экранируется
        self.assertNotIn("<li><b>", slide)
        self.assertNotIn("<ul>", export._slide("Пусто", []))


class SixPagerAssemblyTests(unittest.TestCase):
    """Сборка six-pager: без дублей секций, без маркеров обрезки, понижение чужих H1,
    полные сноски, матрица тактик из Outcome-роадмапа, KPI-таблица из 06,
    note и чувствительность из calcs.json."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xsp")
        pdir = cls.pdir
        out = pdir / "outputs"
        (out / "02_situation.md").write_text(
            "# Ситуация по рынку удержания\n## Короткий ответ\nрынок 40 млрд, отток [C001]\n"
            "## Что известно\n### Q1 — размер рынка\n- 40 млрд [C001]\n"
            "## Сегменты (discovery)\n- абоненты 55+\n## Противоречия источников\n- источники расходятся\n",
            encoding="utf-8")
        (out / "03_options.md").write_text(
            "# Варианты: удержание\n## Вариант A: оставить как есть\n### Возражения\n- отток продолжится\n"
            "## Вариант B: переупаковка\n### Возражения\n- дороже разработка\n## Рекомендация\nвариант B\n",
            encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Продуктовая стратегия: удержание\n## Аудитория\nабоненты 55+ и семьи\n"
            "## Выбранное направление\nOutcome-роадмап (результаты, не фичи):\n"
            "- **Этап 1 (мес 0–3):** семейный пакет; уведомления о звонках. **Результат к дню 90:** удержание +5 п.п.\n"
            "- **Этап 2 (мес 3–6):** гейт для лояльности.\n"
            "## Метрики\nудержание M1 45% [C001]\n", encoding="utf-8")
        (out / "06_validation_plan.md").write_text(
            "# План проверки\n## Ожидаемое изменение (сводно)\n\n"
            "| # | Гипотеза | Метрика | Ожидание к решению |\n|---|---|---|---|\n"
            "| H1 | семейный пакет удерживает [C001] | удержание M1 | 38% → 45% к дню 90 |\n"
            "| H2 | региональные цены поднимают выручку [C002] | выручка/пользователь | ≥ +20% |\n\n"
            "## С чем сравниваем (сводно)\n"
            "- H1: база 38% до запуска пакета; внешний ориентир — отрасль.\n"
            "- H2: база — конверсия при единой цене; контрольная группа без скидки.\n"
            "## Критерии решения (сводно)\n\n"
            "| Проверка | Продолжить | Изменить | Остановить |\n|---|---|---|---|\n"
            "| H1 | ≥ 45% к дню 90 | 40–45% → гейт +30 дней | < 40% → откат |\n"
            "| H2 | выручка ≥ +20% | +5–20% → цена между | разницы нет → откат |\n",
            encoding="utf-8")
        (pdir / "calcs.json").write_text(
            '{"unit_econ": {"arpu": 29, "vc_share": 0.25, "cac": 60, "churn_month": 0.08, '
            '"note": "ARPU по коридору конкурентов [C057]"}}', encoding="utf-8")
        rows = []
        for i in range(1, 21):
            rows.append(json.dumps({
                "id": f"S{i:03d}", "title": f"Источник {i}", "url": f"https://example.com/{i}",
                "origin": "public", "retrieved": "2026-11-09T00:00:00",
                "published": "2026-10-01" if i == 1 else None, "path": ""}, ensure_ascii=False))
        (pdir / "sources.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")
        cls.text = export.build_six_pager(pdir, with_calcs=False).read_text(encoding="utf-8")

    def test_no_duplicated_sections(self):
        self.assertEqual(self.text.count("рынок 40 млрд, отток [C001]"), 1)
        self.assertEqual(self.text.count("### Короткий ответ"), 1)
        self.assertNotIn("## Короткий ответ", self.text.splitlines())  # чужих H2 нет
        self.assertNotIn("### Рынок\n", self.text)         # пустых секций-призраков нет
        self.assertEqual(self.text.count("### Аудитория"), 1)  # из 04 в FAQ-2, без повтора в FAQ-4

    def test_no_truncation_markers_and_full_options(self):
        self.assertNotIn("обрезано", self.text)
        self.assertIn("- отток продолжится", self.text)    # возражения варианта A целиком
        self.assertIn("- дороже разработка", self.text)    # возражения варианта B целиком

    def test_foreign_h1_and_h2_demoted(self):
        lines = self.text.splitlines()
        self.assertNotIn("# Варианты: удержание", lines)
        self.assertNotIn("# Продуктовая стратегия: удержание", lines)
        self.assertNotIn("# План проверки", lines)
        self.assertIn("### Варианты: удержание", self.text)            # H1 → ###
        self.assertIn("#### Вариант A: оставить как есть", self.text)  # H2 → ####
        self.assertIn("##### Возражения", self.text)                   # H3 → #####

    def test_dedup_between_grab_and_whole_insert(self):
        # «Аудитория» из 04 забрана в FAQ-2 (короткий faq2) → в целевой вставке 04 её нет
        self.assertEqual(self.text.count("#### Аудитория"), 0)
        self.assertEqual(self.text.count("абоненты 55+ и семьи"), 1)

    def test_full_footnotes(self):
        for i in range(1, 21):
            self.assertIn(f"**S{i:03d}** — Источник {i} — https://example.com/{i}", self.text)
        self.assertIn("— 2026-10-01", self.text)  # дата публикации, когда известна
        self.assertNotIn("ещё", self.text)

    def test_unit_econ_note_and_sensitivity(self):
        self.assertIn("Допущения: ARPU по коридору конкурентов [C057]", self.text)
        # пороги LTV/CAC ≥ 3: churn 21,75/(3·60) = 12,08 %/мес; CAC 271,875/3 = 90,62;
        # доля переменных 1 − 180/271,875 = 33,79 %
        self.assertIn("держится до churn ≈ 12,08 %/мес", self.text)
        self.assertIn("до CAC ≈ €90,62", self.text)
        self.assertIn("до доли переменных расходов ≈ 33,79 %", self.text)
        self.assertNotIn("укажите теги", self.text)  # note есть — плейсхолдер не нужен

    def test_tactics_matrix_from_roadmap(self):
        self.assertIn("Матрица тактик (из Outcome-роадмапа 04_product_strategy.md):", self.text)
        self.assertIn("| Этап 1 (мес 0–3) | семейный пакет | — |", self.text)
        self.assertIn("**Результат:** удержание +5 п.п. |", self.text)
        self.assertIn("| Этап 2 (мес 3–6) | гейт для лояльности | — |", self.text)

    def test_kpi_table_from_validation_plan(self):
        self.assertIn("| Плоскость | Гипотеза | Метрика | База → цель к сроку | Порог действия (остановить) |",
                      self.text)
        self.assertIn("| Продукт | H1 — семейный пакет удерживает [C001] | удержание M1 | "
                      "база 38% до запуска пакета → 38% → 45% к дню 90 | < 40% → откат |", self.text)
        self.assertIn("| Бизнес | H2 — региональные цены поднимают выручку [C002]", self.text)
        self.assertIn("разницы нет → откат |", self.text)


class ReportAppendicesTests(unittest.TestCase):
    """Приложение A — все claims из claims.jsonl; приложение E — все книги из attachments."""

    def test_appendix_a_lists_every_claim(self):
        pdir = fresh("xacl")
        for i in range(1, 6):
            sources.add(pdir, text=f"Источник {i}", title=f"Src {i}")
        ids = [claims.add(pdir, f"Утверждение {i}", "fact", [f"S{i:03d}"], grade="B")["id"]
               for i in range(1, 6)]
        appendix = export.build(pdir).read_text(encoding="utf-8").split("# Приложение A")[1]
        appendix = appendix.split("# Приложение B")[0]
        rows = [l for l in appendix.splitlines() if l.startswith("| C")]
        self.assertEqual(len(rows), len(ids))
        for cid in ids:
            self.assertIn(f"| {cid} |", appendix)

    def test_attachments_table_lists_all_books(self):
        pdir = fresh("xatt")
        att = pdir / "outputs" / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        wb = Workbook()
        wb.sheet("Ввод").row("Параметр", "Значение")
        wb.save(att / "custom_calc.xlsx")
        table = export.attachments_table(pdir)
        self.assertIn("| custom_calc.xlsx | Ввод | — |", table)  # листы читаются из книги
        (att / "broken.xlsx").write_bytes(b"PK\x03\x04 dummy")   # сломанная книга не роняет
        table = export.attachments_table(pdir)
        self.assertIn("| broken.xlsx | — | — |", table)
        self.assertIn("custom_calc.xlsx", table)
        self.assertIsNone(export.attachments_table(fresh("xatt-empty")))


if __name__ == "__main__":
    unittest.main()
