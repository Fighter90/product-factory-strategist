"""PRO-51: кросс-чек производных чисел юнит-экономики — `pfs check` пересчитывает
ARPU (при тарифах), LTV, LTV/CAC, CAC платящего и окупаемость из calcs.json и
сверяет их с числами в 03/04/06 и six-pager. Расхождение — ошибка.

Кейс cvstart-EU: «ARPU 25» (цена Unlimited) и «LTV 234 / LTV/CAC 7,81»
(от смешанного CAC) дожили до документа комитета, хотя противоречили расчёту.

Запуск: python3 -m unittest tests.test_calc_crosscheck -v
"""
import json
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-cross-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, project  # noqa: E402

UE = {"arpu": 25, "vc_share": 0.25, "cac": 30, "churn_month": 0.08}
# derived: CM 18,75; жизнь 12,5; LTV 234,38; LTV/CAC 7,81; окупаемость 1,60


def make(slug, calcs, docs):
    pdir = project.create("Кросс-чек", "Почему падает удержание?", slug=slug)
    out = pdir / "outputs"
    out.mkdir(parents=True, exist_ok=True)
    (pdir / "calcs.json").write_text(json.dumps({"unit_econ": calcs}, ensure_ascii=False),
                                     encoding="utf-8")
    for name, text in docs.items():
        (out / name).write_text(text, encoding="utf-8")
    return pdir


def errs(pdir):
    return check.run(pdir)["errors"]


class CrosscheckTests(unittest.TestCase):
    def test_mismatched_ltv_is_error(self):
        pdir = make(f"cx{id(self):x}", UE,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- LTV = 250 [C001].\n"})
        e = [x for x in errs(pdir) if "04_product_strategy.md" in x and "LTV" in x]
        self.assertTrue(e, errs(pdir))
        self.assertIn("250", e[0])

    def test_matching_ltv_quiet(self):
        pdir = make(f"cy{id(self):x}", UE,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- LTV = 234,38 [C001].\n"})
        self.assertFalse([x for x in errs(pdir) if "LTV" in x], errs(pdir))

    def test_integer_rounding_quiet(self):
        pdir = make(f"cz{id(self):x}", UE,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- LTV ≈ 234 [C001].\n"})
        self.assertFalse([x for x in errs(pdir) if "LTV" in x], errs(pdir))

    def test_ratio_mismatch_is_error(self):
        pdir = make(f"ca{id(self):x}", UE,
                    {"03_options.md": "# 03\n\n## Сравнение\n\nLTV/CAC 9,9 по расчёту.\n"})
        e = [x for x in errs(pdir) if "03_options.md" in x and "LTV/CAC" in x]
        self.assertTrue(e, errs(pdir))
        self.assertIn("9.9", e[0])

    def test_benchmark_line_quiet(self):
        pdir = make(f"cb{id(self):x}", UE,
                    {"06_validation_plan.md": "# 06\n\n## Критерии\n\n- Продолжить: LTV/CAC >= 3 [C001].\n"})
        self.assertFalse([x for x in errs(pdir) if "LTV/CAC" in x], errs(pdir))

    def test_scenario_and_only_words_skipped(self):
        docs = {"04_product_strategy.md":
                "# 04\n\n## Экономика\n\n- Сценарий Pro-only: ARPU 12 [C001]; "
                "оптимист: LTV 300 [C002].\n"}
        calcs = dict(UE, tiers=[{"price": 12, "share": 0.7}, {"price": 25, "share": 0.3}])
        pdir = make(f"cc{id(self):x}", calcs, docs)
        self.assertFalse([x for x in errs(pdir) if "ARPU" in x or "LTV" in x], errs(pdir))

    def test_tier_mix_mismatch_is_error(self):
        calcs = dict(UE, tiers=[{"price": 12, "share": 0.7}, {"price": 25, "share": 0.3}])
        pdir = make(f"cd{id(self):x}", calcs,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- ARPU 25 [C001].\n"})
        e = [x for x in errs(pdir) if "ARPU" in x and "calcs.json" in x]
        self.assertTrue(e, errs(pdir))
        self.assertIn("15.9", e[0])

    def test_tier_mix_match_quiet(self):
        calcs = dict(UE, tiers=[{"price": 12, "share": 0.7}, {"price": 25, "share": 0.3}])
        pdir = make(f"ce{id(self):x}", calcs,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- ARPU ≈ 15,90 [C001].\n"})
        self.assertFalse([x for x in errs(pdir) if "ARPU" in x], errs(pdir))

    def test_freemium_paying_cac_mismatch_is_error(self):
        calcs = dict(UE, cr_free_paid=0.035)
        pdir = make(f"cf{id(self):x}", calcs,
                    {"04_product_strategy.md": "# 04\n\n## Экономика\n\n- CAC платящего 30 [C001].\n"})
        e = [x for x in errs(pdir) if "CAC платящего" in x and "calcs.json" in x]
        self.assertTrue(e, errs(pdir))
        self.assertIn("857.14", e[0])

    def test_freemium_paying_cac_match_quiet(self):
        calcs = dict(UE, cr_free_paid=0.035)
        pdir = make(f"cg{id(self):x}", calcs,
                    {"04_product_strategy.md":
                     "# 04\n\n## Экономика\n\n- CAC платящего ≈ 857,14; LTV/CAC платящего 0,27 [C001].\n"})
        self.assertFalse([x for x in errs(pdir) if "платящего" in x], errs(pdir))

    def test_six_pager_scanned(self):
        pdir = make(f"ch{id(self):x}", UE,
                    {"SIX_PAGER.md": "# six-pager\n\nLTV = 999.\n"})
        self.assertTrue([x for x in errs(pdir) if "SIX_PAGER.md" in x], errs(pdir))

    def test_no_calcs_no_errors(self):
        pdir = project.create("Кросс-чек пусто", "Вопрос?", slug=f"ci{id(self):x}")
        self.assertFalse([x for x in errs(pdir) if "calcs" in x], errs(pdir))


if __name__ == "__main__":
    unittest.main()
