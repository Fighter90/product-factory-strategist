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
    """PRO-46: документы — данные пакета (_section_bodies), не вставка в six-pager;
    тезисы слайда и экранирование без изменений."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xgrab")
        (cls.pdir / "outputs" / "02_situation.md").write_text(
            "# Ситуация\n## Короткий ответ\nОтток растёт третий месяц подряд.\n"
            "## Что известно\n### Q1 — размер рынка\n- рынок 40 млрд\n", encoding="utf-8")

    def test_section_bodies_extracts_level2_sections_as_data(self):
        bodies = export._section_bodies(self.pdir / "outputs" / "02_situation.md")
        self.assertEqual([b["title"] for b in bodies], ["Короткий ответ", "Что известно"])
        self.assertEqual(bodies[0]["text"], "Отток растёт третий месяц подряд.")
        self.assertIn("Отток растёт третий месяц подряд", bodies[0]["text"])
        self.assertNotIn("рынок 40 млрд", bodies[0]["text"])  # соседняя секция не склеена

    def test_section_bodies_nested_headings_stay_in_text(self):
        bodies = export._section_bodies(self.pdir / "outputs" / "02_situation.md")
        self.assertIn("### Q1 — размер рынка", bodies[1]["text"])  # вложенность — данные пакета
        self.assertIn("рынок 40 млрд", bodies[1]["text"])

    def test_section_bodies_ignores_document_h1(self):
        # H1 документа — не секция данных (прошлый дефект «### Рынок» + копия документа)
        (self.pdir / "outputs" / "02b.md").write_text(
            "# Ситуация по рынку удержания\n## Короткий ответ\nтут короткий ответ\n", encoding="utf-8")
        bodies = export._section_bodies(self.pdir / "outputs" / "02b.md")
        self.assertEqual([b["title"] for b in bodies], ["Короткий ответ"])

    def test_section_bodies_missing_file_is_empty(self):
        self.assertEqual(export._section_bodies(self.pdir / "outputs" / "нет_файла.md"), [])

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
    """PRO-46: сборка six-pager — пакет данных и каркас со слотами вместо вставки
    документов; расчётные артефакты (юнит-экономика с note и чувствительностью,
    матрица тактик, KPI-таблица из 06, сноски из тегов артефактов) на месте."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = fresh("xsp")
        pdir = cls.pdir
        out = pdir / "outputs"
        (out / "02_situation.md").write_text(
            "# Ситуация по рынку удержания\n## Короткий ответ\nрынок 40 млрд, отток [C001]\n"
            "## Что известно\n### Q1 — размер рынка\n- 40 млрд [C001]\n"
            "## Сегменты (discovery)\nJTBD: «Когда звонят мошенники, хочу защитить родителей — "
            "без ручной слежки»\n- абоненты 55+\n## Противоречия источников\n- источники расходятся\n",
            encoding="utf-8")
        (out / "03_options.md").write_text(
            "# Варианты: удержание\n## Вариант A: оставить как есть\n### Возражения\n- отток продолжится\n"
            "## Вариант B: переупаковка\n### Возражения\n- дороже разработка\n## Рекомендация\nвариант B\n",
            encoding="utf-8")
        (out / "04_product_strategy.md").write_text(
            "# Продуктовая стратегия: удержание\n## Аудитория\nабоненты 55+ и семьи\n"
            "## Выбранное направление\nOutcome-роадмап (результаты, не фичи):\n"
            "- **Инициатива 1 — пакет лояльности (мес 0–3):** семейный пакет; уведомления о звонках. "
            "**Результат к дню 90:** удержание +5 п.п.\n"
            "- **Инициатива 2 — удержание ценностью (мес 3–6):** гейт для лояльности; пересмотр тарифа.\n"
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
            "| H2 | выручка ≥ +20% | +5–20% → цена между | разницы нет → откат |\n"
            "## KPI\n\n"
            "| Плоскость | Метрика | Формула | База (дата, источник) | Цель к сроку | "
            "Порог действия (остановить) | Контр-метрика |\n"
            "|---|---|---|---|---|---|---|\n"
            "| Бизнес | Удержание M1 | доля активных на 30-й день | 38% (2026-11-01, [C001]) "
            "| 45% к дню 90 | ниже 40% → откат | активация |\n"
            "| Бизнес | Выручка на пользователя | выручка / пользователи | база до запуска "
            "(2026-11-01, [C002]) | ≥ +20% к дню 120 | разницы нет → откат | доля скидочных |\n",
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
        # PRO-49: в сноски попадают только процитированные источники — S001 (C001) и S002 (C002)
        claims.add(pdir, "рынок 40 млрд, отток растёт", "hypothesis", ["S001"], grade="B")
        claims.add(pdir, "региональные цены поднимают выручку", "hypothesis", ["S002"], grade="C")
        cls.text = export.build_six_pager(pdir, with_calcs=False).read_text(encoding="utf-8")

    def test_documents_not_pasted_slots_instead(self):
        # PRO-46: ни текста 02, ни структуры 03 целиком — вместо них слоты writer'у
        self.assertNotIn("рынок 40 млрд", self.text)
        self.assertNotIn("### Варианты: удержание", self.text)
        self.assertNotIn("#### Вариант A: оставить как есть", self.text)
        self.assertNotIn("- отток продолжится", self.text)
        self.assertNotIn("### Аудитория", self.text)
        self.assertIn(export.SLOT_MARK, self.text)
        self.assertIn("six_pager_pack.md", self.text)
        # данные не потеряны: они в пакете
        pack_md = (self.pdir / "outputs" / "six_pager_pack.md").read_text(encoding="utf-8")
        self.assertIn("рынок 40 млрд", pack_md)
        self.assertIn("- отток продолжится", pack_md)
        self.assertIn("абоненты 55+ и семьи", pack_md)

    def test_no_truncation_markers(self):
        self.assertNotIn("обрезано", self.text)
        self.assertNotIn("### Возражения", self.text)     # структура 03 не вставляется
        self.assertNotIn("# План проверки", self.text.splitlines())  # чужих H1 нет

    def test_full_footnotes_from_artifact_tags(self):
        # PRO-49/PRO-46: теги живут в явной KPI-таблице 06 (артефакте каркаса) —
        # сквозные сноски только из процитированных источников
        self.assertIn("38% (2026-11-01, [^1])", self.text)
        self.assertIn("база до запуска (2026-11-01, [^2])", self.text)
        self.assertIn("[^1]: **S001** — example.com — Источник 1 — 2026-10-01 — "
                      "https://example.com/1 — сила B", self.text)
        self.assertIn("[^2]: **S002** — example.com — Источник 2 — 2026-11-09 — "
                      "https://example.com/2 — сила C", self.text)
        self.assertNotIn("**S003**", self.text)  # непроцитированные не попадают в список
        self.assertNotIn("**S020**", self.text)
        self.assertNotIn("ещё", self.text)

    def test_unit_econ_note_and_sensitivity(self):
        self.assertIn("Допущения: ARPU по коридору конкурентов", self.text)
        self.assertNotIn("[C057]", self.text)  # неизвестный тег уходит из six-pager (реестр — REPORT.md)
        # пороги LTV/CAC ≥ 3: churn 21,75/(3·60) = 12,08 %/мес; CAC 271,875/3 = 90,62;
        # доля переменных 1 − 180/271,875 = 33,79 %
        self.assertIn("держится до churn ≈ 12,08 %/мес", self.text)
        self.assertIn("до CAC ≈ €90,62", self.text)
        self.assertIn("до доли переменных расходов ≈ 33,79 %", self.text)
        self.assertNotIn("укажите теги", self.text)  # note есть — плейсхолдер не нужен

    def test_tactics_matrix_from_roadmap(self):
        self.assertIn("Матрица тактик (раздел «Инициативы» пакета данных):", self.text)
        # PRO-48: одна исполняемая тактика в строке, фокус — направление (не повтор
        # решений), потребности — барьер из JTBD, гейт — у последней тактики
        self.assertIn("| Инициатива 1 | пакет лояльности | без ручной слежки | семейный пакет |", self.text)
        self.assertIn("| Инициатива 1 | пакет лояльности | без ручной слежки | "
                      "уведомления о звонках **Результат:** удержание +5 п.п. |", self.text)
        self.assertIn("| Инициатива 2 | удержание ценностью | без ручной слежки | гейт для лояльности |", self.text)
        self.assertNotIn("| … |", self.text.split("Матрица тактик (раздел")[1].split("## FAQ-5")[0])

    def test_kpi_explicit_table_only(self):
        # PRO-48: KPI не собирается из гипотез H1…H5 — только явная таблица 06
        # со столбцом «Плоскость»; склеенная ячейка «база → цель» и абзац-инструкция
        # шаблона удалены из вывода.
        kpi = export._kpi_table(self.pdir)
        self.assertIsNotNone(kpi)
        self.assertEqual(kpi.count("| Метрика | Формула |"), 1)  # в фикстуре одна плоскость — Бизнес
        self.assertNotIn("| Плоскость | Гипотеза |", self.text)
        self.assertNotIn("База → цель к сроку", self.text)
        self.assertNotIn("KPI в двух направлениях", self.text)


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
