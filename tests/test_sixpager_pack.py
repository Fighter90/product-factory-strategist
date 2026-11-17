"""PRO-46: six-pager пишется по эталону из пакета данных, а не склеивается из документов.

Контракт:
1. `pfs export --six-pager` собирает пакет данных `outputs/six_pager_pack.json`
   (читаемая версия `six_pager_pack.md`): утверждения с силой A–D, источники,
   расчёты из calcs, варианты, выбор руководителя, инициативы, KPI, решения.
2. Каркас `outputs/SIX_PAGER.md` — FAQ-1…6 со слотами для six-pager-writer;
   документы 02/03/04/06 не вставляются: ни одна строка рабочего документа
   длиннее 200 символов не воспроизводится дословно (приёмка PRO-46).
3. Расчётные артефакты в каркасе остаются: юнит-экономика из calcs, матрица
   тактик из Outcome-роадмапа, KPI-таблицы из явной таблицы 06 — это данные,
   а не вставка документов.
4. Каркас со слотами не проходит `pfs check --six-pager` — цикл
   «написать → исправить до 0 ошибок» обязателен, пропустить нельзя.
5. Пакет не попадает в REPORT.md (рабочий вход писателя, не документ комитета).

Запуск: python3 -m unittest tests.test_sixpager_pack -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-sppack-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import claims, core, decisions, export, project, sixpager_lint, sources  # noqa: E402

# Строки-маркеры рабочих документов длиннее 200 символов: приёмка PRO-46 —
# ни одна из них не должна воспроизвестись в собранном six-pager дословно.
LONG_03 = ("- **Вариант B: переупаковка сервиса вокруг семейного пакета с уведомлениями близким, "
           "антиспам-фильтром и белым списком контактов:** переупаковка закрывает главный барьер "
           "сегмента 55+ — страх мошеннических звонков, следствие: рост конверсии в установку; "
           "риск: каннибализация базового тарифа.")
LONG_04 = ("- **Этап 1 — семейная безопасность (месяцы 1–2):** антиспам-фильтр по базе мошеннических "
           "номеров; уведомления близким при подозрительной активности; белый список контактов. "
           "**Результат (гейт):** доля жалоб на блокировки ниже 1%, иначе ослабить фильтр.")


def make_docs(pdir: Path) -> None:
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# Ситуация\n## Короткий ответ\nРынок 40 млрд [C001], отток растёт третий месяц.\n"
        "## Сегменты\n- абоненты 55+: пугают мошеннические звонки\n"
        "## Противоречия\n- данные источников противоречат\n"
        "## Чего мы не знаем\n- платёжеспособность сегмента\n", encoding="utf-8")
    (out / "03_options.md").write_text(
        "# Варианты\n## Рекомендация\nВариант B: переупаковка\n"
        f"## Вариант A: оставить как есть\n{LONG_03}\n"
        "## Вариант B: переупаковка\n## Вариант C: закрыть\n", encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# Стратегия\n## Аудитория\nабоненты 55+ и их семьи\n"
        "## Инициативы выбранного направления\n"
        f"{LONG_04}\n"
        "- **Этап 2 — монетизация (месяцы 2–3):** семейный тариф 350 ₽; пробный месяц."
        " **Результат (гейт):** конверсия в оплату выше 4%.\n"
        "## Метрики\nудержание M1 с 38% до 45% [C001]\n", encoding="utf-8")
    (out / "06_validation_plan.md").write_text(
        "# План\n## Ожидаемое изменение\nудержание M1 +7 п.п.\n"
        "## Критерии решения\nпродолжаем, если +3 п.п.\n"
        "## KPI\n"
        "| Плоскость | Метрика | Формула | База | Цель к сроку | Порог действия | Контр-метрика |\n"
        "|---|---|---|---|---|---|---|\n"
        "| Бизнес | Выручка | MAU × ARPU | 1,2 млн ₽ (2026-10-01, [S001]) | 1,8 млн ₽ к 180 дн | 1,4 млн ₽ | отток платящих |\n"
        "| Продукт | Удержание M1 | доля активных на 30-й день | 38% (2026-10-01, [S001]) | 45% к 90 дн | 41% | жалобы на фильтр |\n",
        encoding="utf-8")


class SixPagerPackTests(unittest.TestCase):
    """PRO-46: пакет данных + каркас со слотами вместо вставки документов."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Пакет six-pager", "Почему падает удержание?", slug="sppack")
        pdir, out = cls.pdir, cls.pdir / "outputs"
        sources.add(pdir, text="Отчёт: рынок 40 млрд, динамика 12% в год.",
                    title="Рынок (агрегатор)", url="https://example.com/market")       # S001
        claims.add(pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")                 # C001
        claims.add(pdir, "Семейный пакет снизит отток", "hypothesis", ["S001"], grade="C")  # C002
        make_docs(pdir)
        (pdir / "calcs.json").write_text(
            '{"unit_econ": {"arpu": 29, "vc_share": 0.25, "cac": 60, "churn_month": 0.08}}',
            encoding="utf-8")
        decisions.add(pdir, "Переупаковка вокруг семейного пакета", "Запускаем вариант B",
                      owner="CPO", grounds=["C001"], review_date="2027-01-01",
                      triggers=["конверсия ниже 3%"], commitments=["пилот|PM|2026-12-01"])
        project.ask_human(pdir, "Какой вариант выбираем?", ["A", "B", "C"])
        project.answer_human(pdir, "Вариант B: переупаковка")
        cls.path = export.build_six_pager(pdir, with_calcs=False)
        cls.text = cls.path.read_text(encoding="utf-8")
        cls.pack = core.read_json(pdir / "outputs" / "six_pager_pack.json")

    # ---------- 1. пакет данных ----------

    def test_pack_json_and_md_created(self):
        self.assertTrue((self.pdir / "outputs" / "six_pager_pack.json").exists())
        self.assertTrue((self.pdir / "outputs" / "six_pager_pack.md").exists())

    def test_pack_sections_present(self):
        for key in ("meta", "situation", "claims", "sources", "calcs", "options",
                    "choice", "initiatives", "kpi", "decisions"):
            self.assertIn(key, self.pack, f"в пакете нет раздела «{key}»")

    def test_pack_claims_carry_type_and_grade(self):
        c = next(c for c in self.pack["claims"] if c["id"] == "C001")
        self.assertEqual(c["kind"], "fact")
        self.assertEqual(c["grade"], "B")
        self.assertEqual(c["sources"], ["S001"])
        self.assertIn("Рынок 40 млрд", c["text"])

    def test_pack_sources_listed(self):
        s = next(s for s in self.pack["sources"] if s["id"] == "S001")
        self.assertEqual(s["title"], "Рынок (агрегатор)")

    def test_pack_calcs_carry_input_and_derived(self):
        self.assertEqual(self.pack["calcs"]["sections"]["unit_econ"]["arpu"], 29)
        # производные пересчитаны той же математикой, что Excel и кросс-чек
        self.assertAlmostEqual(self.pack["calcs"]["derived"]["ltv_cac"], 4.53, places=2)

    def test_pack_options_from_03(self):
        titles = [o["title"] for o in self.pack["options"]]
        self.assertTrue(any("Вариант A" in t for t in titles), titles)
        self.assertTrue(any("Вариант C" in t for t in titles), titles)

    def test_pack_choice_records_answer(self):
        self.assertTrue(any("Вариант B" in a for a in self.pack["choice"]["answers"]))

    def test_pack_initiatives_from_04(self):
        groups = self.pack["initiatives"]["groups"]
        # «Этап N — фокус (тайминг)»: имя и фокус разбираются как в матрице тактик (PRO-48)
        self.assertEqual([g["name"] for g in groups], ["Этап 1", "Этап 2"])
        self.assertIn("семейная безопасность", groups[0]["focus"])
        self.assertTrue(groups[0]["tactics"])
        self.assertTrue(groups[0]["gate"])

    def test_pack_kpi_planes(self):
        self.assertTrue(self.pack["kpi"]["Бизнес"])
        self.assertTrue(self.pack["kpi"]["Продукт"])

    def test_pack_decisions(self):
        self.assertEqual(self.pack["decisions"][0]["id"], "D001")

    def test_pack_md_is_readable_input(self):
        md = (self.pdir / "outputs" / "six_pager_pack.md").read_text(encoding="utf-8")
        for marker in ("S001", "D001", "Рынок 40 млрд", "Вариант B", "Бизнес"):
            self.assertIn(marker, md)

    # ---------- 2. каркас: слоты вместо вставки документов ----------

    def test_skeleton_faq_structure(self):
        for head in ("## FAQ-1", "## FAQ-2", "## FAQ-3", "## FAQ-4", "## FAQ-5", "## FAQ-6",
                     "### 1.1 Обзор рынка", "### 1.2 Ключевые конкуренты",
                     "### 2.1 Сегменты", "### 2.2 Барьеры на каждом этапе пути"):
            self.assertIn(head, self.text)

    def test_no_verbatim_long_lines_from_working_docs(self):
        # приёмка PRO-46: ни одна строка 03/04/06 длиннее 200 символов не вставлена дословно
        for fname in ("02_situation.md", "03_options.md", "04_product_strategy.md",
                      "06_validation_plan.md"):
            for line in (self.pdir / "outputs" / fname).read_text(encoding="utf-8").splitlines():
                if len(line) >= 200:
                    self.assertNotIn(line, self.text, f"{fname}: строка вставлена дословно")

    def test_skeleton_has_slots_pointing_to_pack(self):
        self.assertIn(export.SLOT_MARK, self.text, "слоты для six-pager-writer на месте")
        self.assertIn("six_pager_pack.md", self.text, "каркас показывает вход писателя")
        self.assertIn("six-pager-writer", self.text)
        self.assertIn("pfs check --six-pager", self.text, "обязательный цикл назван в каркасе")

    def test_skeleton_keeps_computed_artifacts(self):
        # юнит-экономика посчитана из calcs.json: CM = 29 × 0,75 = 21,75
        self.assertIn("21,75", self.text)
        self.assertIn("| Стратегическая инициатива | Фокус |", self.text)  # матрица тактик
        self.assertIn("**Бизнес**", self.text)  # KPI-таблицы
        self.assertIn("**Продукт**", self.text)

    def test_skeleton_fails_lint_until_written(self):
        # каркас со слотами обязан валить pfs check --six-pager: цикл «до 0 ошибок» нельзя пропустить
        res = sixpager_lint.run(self.pdir)
        self.assertTrue(res["errors"], "слоты не оставлены в ошибках линтера")
        self.assertTrue(res["points"].get("3"), "остатки шаблона (слоты) не пойманы")

    # ---------- 3. EN-версия из того же пакета ----------

    def test_en_skeleton_from_pack_not_docs(self):
        en = export.build_six_pager(self.pdir, with_calcs=False, lang="en").read_text(encoding="utf-8")
        self.assertIn(core.EN_DRAFT_MARK, en)
        self.assertIn("six_pager_pack.md", en, "EN-каркас указывает на тот же пакет")
        self.assertNotIn(LONG_03, en, "документы не вставляются и в EN")

    # ---------- 4. REPORT: пакет — рабочий файл, не документ комитета ----------

    def test_report_excludes_pack(self):
        # сам файл пакета не встраивается в REPORT (упоминание пути в каркасе — не встраивание)
        report = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertNotIn("# Пакет данных six-pager", report)


if __name__ == "__main__":
    unittest.main()
