"""PRO-51: расчёты против базы знаний — ARPU по топ-тарифу, CAC 0 и 30 одновременно,
невзвешенная сумма баллов, перепутанные единицы воронки.

Красные тесты до реализации (зафиксированы до патчей: 31 тест, 11 failures + 13 errors):
- ARPU средневзвешенный по миксу тарифов (`tiers: [{price, share}]`), а не цена Unlimited;
- freemium: явный `cr_free_paid`, LTV/CAC считается от CAC платящего = CAC / CR;
- сценарии pessimistic / base / optimistic в одном листе;
- скоринг вариантов: числовые веса, взвешенная сумма, фильтры-пороги, `pfs calc options`;
- воронка из calcs.json с явными единицами шагов;
- кросс-чек: производное число в тексте, не сходящееся с calcs.json — ошибка check.

Запуск: python3 -m unittest tests.test_calc_options_scoring -v
"""
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-pro51-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import calc, check, export, project  # noqa: E402
from tools.pfs.xlsx import sheet_names  # noqa: E402

TIERS = [{"name": "Pro", "price": 9, "share": 0.6},
         {"name": "Unlimited", "price": 21, "share": 0.4}]  # ARPU = 5,4 + 8,4 = 13,8

CALCS_MIX = {
    "unit_econ": {
        "tiers": TIERS, "vc_share": 0.2, "cac": 100, "cr_free_paid": 0.05, "churn_month": 0.1,
    },
}


def xml_of(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        return "".join(z.read(n).decode("utf-8")
                       for n in z.namelist() if n.startswith("xl/worksheets/"))


class WeightedArpuTests(unittest.TestCase):
    """ARPU из микса тарифов: Σ(цена × доля), а не цена топ-тарифа."""

    def test_unit_metrics_arpu_is_share_weighted(self):
        m = calc.unit_metrics({"tiers": TIERS, "vc_share": 0.2, "cac": 100, "churn_month": 0.1})
        self.assertAlmostEqual(m["arpu"], 13.8)          # не 21 (Unlimited)
        self.assertAlmostEqual(m["cm"], 13.8 * 0.8)
        self.assertAlmostEqual(m["ltv"], 13.8 * 0.8 / 0.1)

    def test_plain_arpu_without_tiers_unchanged(self):
        m = calc.unit_metrics({"arpu": 25, "vc_share": 0.25, "cac": 30, "churn_month": 0.08})
        self.assertAlmostEqual(m["arpu"], 25)
        self.assertAlmostEqual(m["ltv"], 25 * 0.75 / 0.08)  # 234,375 — прежняя формула

    def test_workbook_lists_tiers_and_weighted_arpu(self):
        wb = calc.unit_econ(dict(CALCS_MIX["unit_econ"]))
        xml = "".join(s.xml() for s in wb.sheets)
        self.assertIn("Pro", xml)
        self.assertIn("Unlimited", xml)
        self.assertIn("13.8", xml)  # средневзвешенный ARPU — кэш формулы

    def test_share_labels_visible_in_workbook(self):
        wb = calc.unit_econ(dict(CALCS_MIX["unit_econ"]))
        xml = wb.sheets[0].xml()
        self.assertIn("доля", xml.lower())


class FreemiumCacTests(unittest.TestCase):
    """Freemium: CAC платящего = CAC / CR_free→paid — конверсия реально применяется."""

    PARAMS = {"arpu": 200, "vc_share": 0.25, "cac": 100, "cr_free_paid": 0.05, "churn_month": 0.05}

    def test_cac_paying_is_cac_over_cr(self):
        m = calc.unit_metrics(dict(self.PARAMS))
        self.assertAlmostEqual(m["cac_paying"], 2000.0)

    def test_ltv_cac_uses_paying_cac(self):
        m = calc.unit_metrics(dict(self.PARAMS))
        ltv = 200 * 0.75 / 0.05  # 3000
        self.assertAlmostEqual(m["ltv_cac"], ltv / 2000)  # 1,5, а не 30

    def test_workbook_shows_paying_cac_row(self):
        wb = calc.unit_econ(dict(self.PARAMS))
        xml = "".join(s.xml() for s in wb.sheets)
        self.assertIn("платящ", xml.lower())
        self.assertIn("2000", xml)

    def test_without_cr_behaviour_unchanged(self):
        m = calc.unit_metrics({"arpu": 200, "vc_share": 0.25, "cac": 100, "churn_month": 0.05})
        self.assertIsNone(m["cac_paying"])
        self.assertAlmostEqual(m["ltv_cac"], 3000 / 100)


class ScenarioSheetTests(unittest.TestCase):
    """Сценарии pessimistic / base / optimistic — в одном листе, а не смешение допущений."""

    PARAMS = {"arpu": 200, "vc_share": 0.25, "cac": 100, "cr_free_paid": 0.05,
              "churn_month": 0.05,
              "scenarios": {"pessimistic": {"churn_month": 0.10, "cr_free_paid": 0.02},
                            "base": {},
                            "optimistic": {"churn_month": 0.03, "cr_free_paid": 0.10}}}

    def test_scenarios_sheet_exists(self):
        wb = calc.unit_econ(dict(self.PARAMS))
        names = [s.name for s in wb.sheets]
        self.assertIn("Сценарии", names)

    def test_three_scenarios_with_own_values(self):
        wb = calc.unit_econ(dict(self.PARAMS))
        xml = "".join(s.xml() for s in wb.sheets)
        self.assertIn("Пессимистичный", xml)
        self.assertIn("Оптимистичный", xml)
        # pessimistic: CAC платящего 100/0,02 = 5000; optimistic: 100/0,1 = 1000
        self.assertIn("5000", xml)
        self.assertIn("1000", xml)

    def test_no_scenarios_no_sheet(self):
        wb = calc.unit_econ({"arpu": 200, "vc_share": 0.25, "cac": 100, "churn_month": 0.05})
        self.assertNotIn("Сценарии", [s.name for s in wb.sheets])


class OptionsScoringTests(unittest.TestCase):
    """Скоринг вариантов: числовые веса, взвешенная сумма, фильтры-пороги."""

    P = {
        "note": "тест",
        "criteria": [{"name": "реализуемость", "weight": 3, "filter": 3},
                     {"name": "эффект на удержание", "weight": 2}],
        "variants": [{"name": "A — оставить как есть", "scores": [3, 3]},
                     {"name": "B — платный тариф", "scores": [4, 2]},
                     {"name": "C — расширение", "scores": [2, 3]}],
    }
    # Невзвешенно: A 6, B 6, C 5 — ничья; взвешенно: A 15, B 16, C отсеян фильтром.

    def test_weighted_totals(self):
        totals = calc.options_totals(dict(self.P))
        self.assertEqual([t[0] for t in totals][0:2], ["A — оставить как есть", "B — платный тариф"])
        self.assertAlmostEqual(totals[0][1], 15)  # 3×3 + 3×2
        self.assertAlmostEqual(totals[1][1], 16)  # 4×3 + 2×2

    def test_threshold_filter_eliminates_variant(self):
        totals = calc.options_totals(dict(self.P))
        name, total, reason = totals[2]
        self.assertAlmostEqual(total, 12)  # 2×3 + 3×2
        self.assertIsNotNone(reason)
        self.assertIn("реализуемость", reason)

    def test_passing_variant_has_no_reason(self):
        totals = calc.options_totals(dict(self.P))
        self.assertIsNone(totals[0][2])
        self.assertIsNone(totals[1][2])

    def test_markdown_table_shows_weights_and_weighted_sum(self):
        table = calc.options_table(dict(self.P))
        self.assertIn("Вес", table)
        self.assertIn("16", table)
        self.assertIn("взвеш", table.lower())
        self.assertIn("отсеян", table.lower())

    def test_options_workbook_has_comparison_sheet(self):
        wb = calc.options(dict(self.P))
        self.assertIn("Сравнение", [s.name for s in wb.sheets])

    def test_run_options_writes_xlsx_and_table(self):
        pdir = project.create("Скоринг", "Что делаем?", slug=f"opt{id(self)}")
        import json
        (pdir / "calcs.json").write_text(json.dumps({"options": self.P}, ensure_ascii=False),
                                         encoding="utf-8")
        paths = calc.run(pdir, "options")
        names = {p.name for p in paths}
        self.assertIn("options_scoring.xlsx", names)
        self.assertIn("options_scoring.md", names)
        xlsx = next(p for p in paths if p.suffix == ".xlsx")
        self.assertIn("Сравнение", sheet_names(xlsx))
        md = next(p for p in paths if p.suffix == ".md").read_text(encoding="utf-8")
        self.assertIn("16", md)

    def test_options_not_built_by_all(self):
        pdir = project.create("Скоринг all", "Что делаем?", slug=f"optall{id(self)}")
        self.assertEqual(len(calc.run(pdir, "all")), 4)


class FunnelTests(unittest.TestCase):
    """Единицы воронки: визиты, установки, регистрации, экспорты — явные шаги из calcs.json."""

    FUNNEL = {"steps": [{"name": "визиты", "value": 1000},
                        {"name": "установки", "value": 500},
                        {"name": "регистрации", "value": 150},
                        {"name": "экспорты CV", "value": 50}]}

    def test_growth_workbook_has_funnel_sheet(self):
        p = dict(calc.DEFAULTS["growth"])
        p["funnel"] = self.FUNNEL
        wb = calc.growth(p)
        names = [s.name for s in wb.sheets]
        self.assertIn("Воронка", names)

    def test_funnel_steps_and_conversions(self):
        p = dict(calc.DEFAULTS["growth"])
        p["funnel"] = self.FUNNEL
        wb = calc.growth(p)
        xml = "".join(s.xml() for s in wb.sheets)
        for step in ("визиты", "установки", "регистрации", "экспорты CV"):
            self.assertIn(step, xml)
        # конверсии только между соседними шагами: 50%, 30%, 33,3%
        self.assertIn("0.5", xml)
        self.assertIn("0.3", xml)
        self.assertIn("0.3333333333", xml)

    def test_no_funnel_no_sheet(self):
        wb = calc.growth(dict(calc.DEFAULTS["growth"]))
        self.assertNotIn("Воронка", [s.name for s in wb.sheets])

    def test_funnel_read_from_calcs_json(self):
        import json
        pdir = project.create("Воронка", "Что делаем?", slug=f"funnel{id(self)}")
        (pdir / "calcs.json").write_text(json.dumps({"funnel": self.FUNNEL}), encoding="utf-8")
        path = calc.run(pdir, "growth")[0]
        self.assertIn("Воронка", sheet_names(path))


class CalcsCrosscheckTests(unittest.TestCase):
    """Производное число в тексте не сходится с calcs.json — ошибка check, не предупреждение."""

    def setUp(self):
        import json
        self.pdir = project.create(f"Кросс-чек {id(self)}", "Почему падает удержание?",
                                   slug=f"cross{id(self)}")
        (self.pdir / "calcs.json").write_text(json.dumps({
            "unit_econ": {"tiers": TIERS, "vc_share": 0.25, "cac": 30,
                          "cr_free_paid": 0.02, "churn_month": 0.08},
        }, ensure_ascii=False), encoding="utf-8")
        # пересчёт: ARPU 13,8; CM 10,35; LTV 129,375; CAC платящего 1500; LTV/CAC 0,086
        out = self.pdir / "outputs"
        out.mkdir(exist_ok=True)

    def _write(self, name: str, text: str) -> None:
        (self.pdir / "outputs" / name).write_text(text, encoding="utf-8")

    def _errors(self):
        return check.run(self.pdir)["errors"]

    def test_mismatched_ltv_cac_is_error(self):
        self._write("04_product_strategy.md",
                    "## Экономика\n- LTV/CAC 7,81 — экономика сходится [C001].\n")
        errs = [e for e in self._errors() if "calcs.json" in e]
        self.assertTrue(errs, self._errors())
        self.assertIn("LTV/CAC", errs[0])
        self.assertIn("7,81", errs[0])

    def test_mismatched_ltv_is_error(self):
        self._write("04_product_strategy.md",
                    "## Экономика\n- LTV ≈ €234 при ARPU €25 [C001].\n")
        errs = [e for e in self._errors() if "calcs.json" in e]
        self.assertTrue(errs, self._errors())
        self.assertIn("LTV", errs[0])

    def test_matching_numbers_are_quiet(self):
        self._write("04_product_strategy.md",
                    "## Экономика\n- LTV ≈ 129 [C001]; LTV/CAC 0,09 при CAC платящего 1 500 [C002].\n")
        self.assertFalse([e for e in self._errors() if "calcs.json" in e], self._errors())

    def test_freemium_paying_cac_mismatch_is_error(self):
        self._write("06_validation_plan.md",
                    "## Критерии\n- CAC платящего 30 — привлекаем платных пользователей [C001].\n")
        errs = [e for e in self._errors() if "calcs.json" in e]
        self.assertTrue(errs, self._errors())
        self.assertIn("CAC платящего", errs[0])

    def test_checked_in_03_and_six_pager(self):
        self._write("03_options.md", "## Сравнение\n- эффект: LTV/CAC 7,81 [C001].\n")
        self._write("SIX_PAGER.md", "FAQ-3: LTV/CAC = 7,81.\n")
        errs = [e for e in self._errors() if "calcs.json" in e]
        self.assertEqual(len(errs), 2, errs)

    def test_no_calcs_json_no_errors(self):
        pdir = project.create("Без calcs", "Вопрос?", slug=f"nocalcs{id(self)}")
        (pdir / "outputs").mkdir(exist_ok=True)
        (pdir / "outputs" / "04_product_strategy.md").write_text(
            "## Экономика\n- LTV/CAC 99 [C001].\n", encoding="utf-8")
        self.assertFalse([e for e in check.run(pdir)["errors"] if "calcs.json" in e])

    def test_ltv_slash_cac_paying_label_is_not_cac(self):
        # «LTV/CAC платящего ≈ 0,16» — это LTV/CAC, а не CAC платящего
        self._write("04_product_strategy.md",
                    "## Экономика\n- LTV/CAC платящего ≈ 0,16 при CAC платящего 1 500 [C001].\n")
        self.assertFalse([e for e in self._errors() if "calcs.json" in e], self._errors())

    def test_le_threshold_and_formula_operand_skipped(self):
        self._write("06_validation_plan.md",
                    "## Критерии\n- вывод: фактический 0,16 при CAC платящего 1 500 — для ≥ 3 нужен "
                    "CAC платящего ≤ 59 при этом LTV [C001].\n")
        self.assertFalse([e for e in self._errors() if "calcs.json" in e], self._errors())

    def test_enumeration_number_after_label_skipped(self):
        self._write("SIX_PAGER.md",
                    "FAQ-6: фактический LTV/CAC); 2) Продукт — активация и churn.\n")
        self.assertFalse([e for e in self._errors() if "calcs.json" in e], self._errors())

    def test_criterion_threshold_not_flagged(self):
        # «LTV/CAC ≥ 3» — критерий, а не производное число
        self._write("04_product_strategy.md", "## Экономика\n- критерий LTV/CAC ≥ 3 [C001].\n")
        self.assertFalse([e for e in self._errors() if "calcs.json" in e], self._errors())


class ExportBlockConsistencyTests(unittest.TestCase):
    """Six-pager считает юнит-экономику из тех же tiers/cr_free_paid, что и Excel."""

    def setUp(self):
        import json
        self.pdir = project.create(f"Экспорт микс {id(self)}", "Вопрос?", slug=f"mix{id(self)}")
        (self.pdir / "calcs.json").write_text(json.dumps(CALCS_MIX, ensure_ascii=False),
                                              encoding="utf-8")

    def test_block_uses_weighted_arpu_and_paying_cac(self):
        block = export._unit_econ_block(self.pdir)
        self.assertIsNotNone(block)
        self.assertIn("13,80", block)          # взвешенный ARPU, не 21
        self.assertIn("CAC платящего", block)  # freemium: конверсия применяется
        self.assertIn("2000,00", block)
        # LTV = 13,8 × 0,8 / 0,1 = 110,4
        self.assertIn("**LTV = 110,40**", block)

    def test_plain_params_block_unchanged(self):
        import json
        pdir = project.create("Экспорт plain", "Вопрос?", slug=f"plain{id(self)}")
        (pdir / "calcs.json").write_text(
            json.dumps({"unit_econ": {"arpu": 29, "vc_share": 0.25, "cac": 60, "churn_month": 0.08}}),
            encoding="utf-8")
        block = export._unit_econ_block(pdir)
        self.assertIn("21,75", block)
        self.assertIn("**LTV = 271,88**", block)
        self.assertIn("**4,53**", block)


if __name__ == "__main__":
    unittest.main()
