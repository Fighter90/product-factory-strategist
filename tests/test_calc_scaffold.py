"""Тесты каркаса calcs.json (pfs calc scaffold). Запуск: python3 -m unittest tests.test_calc_scaffold -v"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-scaffold-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import calc, project  # noqa: E402


def make_docs(pdir: Path, files: dict[str, str]) -> None:
    out = pdir / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out / name).write_text(text, encoding="utf-8")


ECON_04 = """# 04 · Продуктовая стратегия — Тестовый сервис

## Аудитория

Соискатели и их семьи [C001].

## Выбранное направление

Семейный пакет с уведомлениями [C002].

## Экономика направления (формулы на допущениях [C003])

- Юнит (платящий): ARPU 350 ₽/мес; переменные затраты 30%; CAC 700 ₽; churn 6%/мес [C003].
- Валовая маржа 70% от выручки; средний чек 1 200 ₽; заказов на активного 2 в месяц [C004].
- Take rate платформы 12%; конверсия активного в заказ 4%/мес [C004].
- MAU на старте 50 000, рост MAU 8%/мес [C005].
"""

SIT_02 = """# 02 · Ситуация

## Короткий ответ

Рынок — коридор 1,2–2,4 млрд ₽/год [C009]; отток растёт [C001].

## Что известно

- Доля TAM 60% от PAM [C010]; SAM 40% [C010]; SOM 5% от SAM за 3 года [C010].
"""

PLAN_06 = """# 06 · План проверки — бета 90 дней

## Ожидаемое изменение

Запуск беты: удержание M1 с 32% до 40% [C006]; к неделе 12 — 5 000 платящих.

## С чем сравниваем

База — публичные ориентиры freemium-конверсии 2–5% [C007].

## Критерии решения

- Продолжить: churn платящих ≤ 8%/мес [C008].
"""

REVIEW_07 = """# 07 · Контроль качества

- Проверка пройдена [C011].
"""


class ScaffoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Scaffold тест", "Почему падает удержание?", slug="sc1")
        make_docs(cls.pdir, {"04_product_strategy.md": ECON_04, "02_situation.md": SIT_02,
                             "06_validation_plan.md": PLAN_06, "07_quality_review.md": REVIEW_07})
        cls.cfg, cls.found, cls.total = calc.scaffold(cls.pdir)

    def test_finds_most_numbers(self):
        # критерий приёмки PRO-35: на проекте с 04/06 найдено ≥ 70% чисел
        self.assertEqual(self.total, 17)
        self.assertGreaterEqual(self.found / self.total, 0.7)

    def test_unit_econ_from_04(self):
        ue = self.cfg["unit_econ"]
        self.assertEqual(ue["arpu"], 350)
        self.assertEqual(ue["vc_share"], 0.3)
        self.assertEqual(ue["cac"], 700)
        self.assertEqual(ue["churn_month"], 0.06)  # 04 приоритетнее 06 (там 8%)
        self.assertIn("[C003]", ue["_notes"]["arpu"])  # найденный C-тег в note

    def test_growth_from_04(self):
        g = self.cfg["growth"]
        self.assertEqual(g["mau_start"], 50000)
        self.assertEqual(g["mau_growth_month"], 0.08)
        self.assertEqual(g["conv_order"], 0.04)
        self.assertEqual(g["orders_per_active"], 2.0)
        self.assertEqual(g["aov"], 1200)
        self.assertEqual(g["take_rate"], 0.12)
        self.assertEqual(g["margin"], 0.7)

    def test_market_from_02(self):
        m = self.cfg["market"]
        self.assertEqual(m["pam"], 1.8e9)  # середина коридора 1,2–2,4 млрд
        self.assertEqual(m["tam_share"], 0.6)
        self.assertEqual(m["sam_share"], 0.4)
        self.assertEqual(m["som_share"], 0.05)
        self.assertIn("[C009]", m["_notes"]["pam"])

    def test_cohort_retention_slots_and_null_sizes(self):
        c = self.cfg["cohort"]
        self.assertIsNone(c["sizes"])  # не найдено — null
        self.assertIn("sizes", c["_hints"])  # подсказка, где взять
        self.assertEqual(c["retention"][0], 1.0)  # M0 — вход когорты
        self.assertEqual(c["retention"][1], 0.4)  # цель «с 32% до 40%» — целевое
        self.assertIn("[C006]", c["_notes"]["retention"])

    def test_calc_all_works_with_nulls(self):
        paths = calc.run(self.pdir, "all")
        self.assertEqual(len(paths), 4)
        for p in paths:
            with zipfile.ZipFile(p) as z:
                self.assertIsNone(z.testzip())

    def test_existing_values_preserved(self):
        (self.pdir / "calcs.json").write_text(
            '{"unit_econ": {"arpu": 999, "note": "моё"}}', encoding="utf-8")
        cfg, _, _ = calc.scaffold(self.pdir)
        self.assertEqual(cfg["unit_econ"]["arpu"], 999)
        self.assertEqual(cfg["unit_econ"]["note"], "моё")
        self.assertNotIn("arpu", cfg["unit_econ"]["_notes"])
        (self.pdir / "calcs.json").unlink()  # вернуть состояние после scaffold


class ScaffoldUntaggedTests(unittest.TestCase):
    def test_untagged_numbers_become_null(self):
        pdir = project.create("Scaffold без тегов", "Вопрос?", slug="sc2")
        make_docs(pdir, {"04_product_strategy.md": "# 04\n## Экономика\n- ARPU 500 ₽; CAC 900 ₽\n"})
        cfg, found, total = calc.scaffold(pdir)
        ue = cfg["unit_econ"]
        self.assertIsNone(ue["arpu"])  # число без C/S-тега не переносится
        self.assertIsNone(ue["cac"])
        self.assertIn("arpu", ue["_hints"])
        self.assertEqual(found, 0)


class RetentionGenitiveTests(unittest.TestCase):
    """Склонённые формы «удержания/удержанию/удержании» тоже заполняют слоты M."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Scaffold удержание склонения", "Вопрос?", slug="sc3")
        make_docs(cls.pdir, {"06_validation_plan.md": """# 06 · План проверки

## Критерии решения

- Цель удержания M3 — не ниже 35% [C022].
- По удержанию M6 — не ниже 25% [C023].
- Об удержании M9 — 20% [C024].
"""})
        cls.cfg, _, _ = calc.scaffold(cls.pdir)

    def test_genitive_dative_prepositional_fill_slots(self):
        ret = self.cfg["cohort"]["retention"]
        self.assertEqual(ret[3], 0.35)   # «удержания M3»
        self.assertEqual(ret[6], 0.25)   # «удержанию M6»
        self.assertEqual(ret[9], 0.20)   # «удержании M9»
        self.assertIn("[C022]", self.cfg["cohort"]["_notes"]["retention"])


class CorridorTests(unittest.TestCase):
    """Коридор «60–70%» → середина для всех долевых параметров, не только pam/conv_order."""

    @classmethod
    def setUpClass(cls):
        cls.pdir = project.create("Scaffold коридоры", "Вопрос?", slug="sc4")
        make_docs(cls.pdir, {
            "04_product_strategy.md": """# 04 · Продуктовая стратегия

## Экономика

- MAU на старте 20 000 [C018]; рост MAU 3–5%/мес [C019].
- Переменные затраты 20–25% [C020]; churn платящих 6–8%/мес [C021].
- Take rate платформы 10–12% [C022]; валовая маржа 60–70% [C023].
""",
            "02_situation.md": """# 02 · Ситуация

## Размер рынка

- TAM 60–70% от PAM [C024]; SAM 30–40% [C025]; SOM 3–5% от SAM за 3 года [C026].
"""})
        cls.cfg, _, _ = calc.scaffold(cls.pdir)

    def test_growth_corridors_take_midpoint(self):
        g = self.cfg["growth"]
        self.assertEqual(g["mau_growth_month"], 0.04)  # 3–5% → 4%
        self.assertEqual(self.cfg["unit_econ"]["vc_share"], 0.225)    # 20–25% → 22,5%
        self.assertEqual(self.cfg["unit_econ"]["churn_month"], 0.07)  # 6–8% → 7%
        self.assertEqual(g["take_rate"], 0.11)   # 10–12% → 11%
        self.assertEqual(g["margin"], 0.65)      # 60–70% → 65%

    def test_market_share_corridors_take_midpoint(self):
        m = self.cfg["market"]
        self.assertEqual(m["tam_share"], 0.65)  # 60–70% → 65%
        self.assertEqual(m["sam_share"], 0.35)  # 30–40% → 35%
        self.assertEqual(m["som_share"], 0.04)  # 3–5% → 4%


class MergeAndParseTests(unittest.TestCase):
    def test_merge_skips_none_and_underscores(self):
        merged = calc._merge(calc.DEFAULTS["unit_econ"], {"arpu": None, "cac": 5, "_hints": {"x": "y"}})
        self.assertEqual(merged["arpu"], 199)  # null → пример с пометкой ПРИМЕР
        self.assertEqual(merged["cac"], 5)
        self.assertNotIn("_hints", merged)

    def test_merge_retention_positional_and_sizes(self):
        merged = calc._merge(calc.DEFAULTS["cohort"], {"retention": [None, 0.5], "sizes": [10, None, 30]})
        self.assertEqual(merged["retention"][0], 1.0)  # пропущенный слот → пример
        self.assertEqual(merged["retention"][1], 0.5)  # найденный — на своём месте
        self.assertEqual(merged["retention"][2], 0.42)
        self.assertEqual(merged["sizes"], [10, 6000, 30])  # null → пример на своей позиции, порядок не сдвигается
        wb = calc.cohort(merged)  # книга собирается, когорты не теряются и не сдвигаются
        size_rows = [r[0] for r in wb.sheets[0].rows if str(r[0]).startswith("Размер когорты")]
        self.assertEqual(size_rows, ["Размер когорты 1 (вход в M0)",
                                     "Размер когорты 2 (вход в M1)",
                                     "Размер когорты 3 (вход в M2)"])

    def test_merge_sizes_longer_than_example_kept(self):
        merged = calc._merge(calc.DEFAULTS["cohort"], {"sizes": [10, 20, 30, 40, 50, 60, None, 80]})
        # позиции 0–5 в пределах примера сохранены; null в хвосте за пределами примера
        # заполнить нечем (примера там нет) — он отбрасывается, книга собирается
        self.assertEqual(merged["sizes"], [10, 20, 30, 40, 50, 60, 80])

    def test_num_parses_spaces_and_comma(self):
        self.assertEqual(calc._num("1 200"), 1200)
        self.assertEqual(calc._num("1,5"), 1.5)
        self.assertEqual(calc._num("2 603"), 2603)

    def test_grab_and_normalize(self):
        raw, unit = calc._grab("рынок — коридор 1,2–2,4 млрд ₽/год", calc.PARAM_SPECS["market"][0]["re"][0])
        self.assertEqual((raw, unit), (1.8, "млрд"))
        self.assertEqual(calc._normalize(raw, unit, pct=False), 1.8e9)
        self.assertEqual(calc._normalize(60, "%", pct=True), 0.6)
        self.assertEqual(calc._normalize(60, "", pct=True), 0.6)  # «TAM 60» без % — тоже доля


if __name__ == "__main__":
    unittest.main()
