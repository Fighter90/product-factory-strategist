#!/usr/bin/env python3
"""QA B-06/B-07/B-08: нормализация чисел кросс-чека — тысячные запятые, RU-десятичные,
сценарные числа не бьют по calcs.json."""

import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-num-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import calc as calc_mod, check, claims, core, project, sources  # noqa: E402


class ParseNumberTests(unittest.TestCase):
    def test_thousands_and_decimals(self):
        f = calc_mod.parse_number
        self.assertEqual(f("22 500"), 22500.0)   # RU тысячи пробелом
        self.assertEqual(f("13,195"), 13195.0)   # EN тысячи запятой (B-08)
        self.assertEqual(f("1,234.5"), 1234.5)   # EN формат
        self.assertEqual(f("8,9"), 8.9)          # RU десятичная (B-06)
        self.assertEqual(f("8.9"), 8.9)
        self.assertEqual(f("42,635"), 42635.0)   # запятая+3 цифры — тысячный разряд
        self.assertEqual(f("7,81"), 7.81)        # RU десятичная, 2 знака

    def test_numbers_token_uses_parse_number(self):
        nums = check._numbers("LTV = 13,195, конверсия 8,9% и 1,234.5")
        self.assertIn(13195.0, nums)
        self.assertIn(8.9, nums)
        self.assertIn(1234.5, nums)


class ScenarioCrossCheckTests(unittest.TestCase):
    def _proj_with_calcs(self, slug):
        pdir = project.create("Num cross", "вопрос", slug=slug)
        sources.add(pdir, text="CAC 450, конверсия 2%", title="Юнит-экономика")
        claims.add(pdir, "CAC платящего = 22 500 при конверсии 2% [C001]", "fact", ["S001"],
                   quote="CAC 450, конверсия 2%")
        core.atomic_write(pdir / "calcs.json", __import__("json").dumps({
            "unit_econ": {"arpu": 900, "vc_share": 0.2, "cac": 450, "churn_month": 0.08,
                          "cr_free_paid": 0.02}}, ensure_ascii=False))
        return pdir

    def test_status_quo_line_not_flagged(self):
        """B-07: «статус-кво CAC = 22 500» — сценарное сравнение, не ошибка calcs."""
        pdir = self._proj_with_calcs(f"nc-sq-{id(self)}")
        (pdir / "outputs" / "03_options.md").write_text(
            "# Options\n\n## Вариант A\n\nCAC платящего в статус-кво = 22 500 ₽ при конверсии 2%.\n",
            encoding="utf-8")
        errs = check.calcs_mismatch_errors(pdir)
        self.assertEqual([e for e in errs if "22" in e], [],
                         "сценарное число поймано как ошибка: %s" % errs)

    def test_plain_calc_mismatch_still_caught(self):
        """Гард-рейл: реальное расхождение с calcs.json по-прежнему ошибка."""
        pdir = self._proj_with_calcs(f"nc-mm-{id(self)}")
        (pdir / "outputs" / "03_options.md").write_text(
            "# Options\n\n## Вариант B\n\nCAC платящего = 9 999 ₽ в расчёте экономики.\n",
            encoding="utf-8")
        errs = check.calcs_mismatch_errors(pdir)
        self.assertTrue(any("err" in e or "не сходится" in e or "mismatch" in e.lower() for e in errs),
                         "ожидали ошибку кросс-чека, получили: %s" % errs)

    def test_en_thousands_not_flagged(self):
        """B-08: «LTV = 13,195» (EN тысячи) в EN-проекте сходится с calcs."""
        pdir = project.create("EN num", "growth question", slug=f"nc-en-{id(self)}", lang="en")
        sources.add(pdir, text="ARPU 900, churn 8% monthly", title="Unit economics")
        claims.add(pdir, "LTV = 13,195 [C001]", "fact", ["S001"], quote="ARPU 900, churn 8% monthly")
        core.atomic_write(pdir / "calcs.json", __import__("json").dumps({
            "unit_econ": {"arpu": 900, "vc_share": 0.2, "cac": 450, "churn_month": 0.08}},
            ensure_ascii=False))
        (pdir / "outputs" / "03_options.md").write_text(
            "# Options\n\n## Option B\n\nLTV = 9,000 in the base calculation.\n", encoding="utf-8")
        errs = check.calcs_mismatch_errors(pdir)
        self.assertEqual([e for e in errs if "LTV" in e], [],
                         "EN-тысячи пойманы как расхождение: %s" % errs)


if __name__ == "__main__":
    unittest.main()
