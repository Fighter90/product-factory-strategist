"""PRO-51: ARPU средневзвешенный по тарифам, CAC платящего во freemium, сценарии,
взвешенный скоринг вариантов и явная воронка с единицами шагов.

Кейс из аудита cvstart-EU: агент писал ARPU 25 (цена тарифа Unlimited) вместо
Σ(цена × доля) по карте M-unit-economics; LTV/CAC считался от «CAC 30», при том
что во freemium карта требует CAC_платящего = CAC / CR_free→paid; сравнение
вариантов складывало баллы как равные при качественных весах.

Запуск: python3 -m unittest tests.test_calc_mix_freemium -v
"""
import json
import os
import tempfile
import unittest
import zipfile

TMP = tempfile.mkdtemp(prefix="pfs-test-mix-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import calc, project, xlsx  # noqa: E402

MIX = {"tiers": [{"price": 12, "share": 0.7}, {"price": 25, "share": 0.3}]}
FREEMIUM = {"cac": 30, "cr_free_paid": 0.035}


def unit_params(**over):
    p = {"arpu": 25, "vc_share": 0.25, "cac": 30, "churn_month": 0.08}
    p.update(over)
    return p


class WeightedArpuTests(unittest.TestCase):
    """ARPU = Σ(цена × доля), а не цена топ-тарифа."""

    def test_weighted_arpu_from_tiers(self):
        d = calc.derived(unit_params(**MIX))
        self.assertAlmostEqual(d["arpu"], 15.9)   # 12×0,7 + 25×0,3
        self.assertNotEqual(d["arpu"], 25)        # не цена Unlimited

    def test_plain_arpu_without_tiers(self):
        d = calc.derived(unit_params())
        self.assertEqual(d["arpu"], 25)

    def test_ltv_uses_weighted_arpu(self):
        d = calc.derived(unit_params(**MIX))
        self.assertAlmostEqual(d["cm"], round(15.9 * 0.75, 6))
        self.assertAlmostEqual(d["ltv"], round(15.9 * 0.75 / 0.08, 6))

    def test_unit_econ_input_sheet_shows_tiers(self):
        wb = calc.unit_econ(unit_params(**MIX))
        rows = [tuple(r) for r in wb.sheets[0].rows]
        weighted = [r for r in rows if isinstance(r[0], str) and "средневзвеш" in r[0].lower()]
        self.assertTrue(weighted, "нет строки средневзвешенного ARPU")
        cell = weighted[0][1]
        self.assertAlmostEqual(cell["cached"] if isinstance(cell, dict) else cell, 15.9)


class FreemiumCacTests(unittest.TestCase):
    """CAC_платящего = CAC / CR_free→paid; LTV/CAC — от CAC платящего."""

    def test_cac_paying(self):
        d = calc.derived(unit_params(**FREEMIUM))
        self.assertAlmostEqual(d["cac_paying"], round(30 / 0.035, 6))

    def test_without_cr_cac_paying_is_cac(self):
        d = calc.derived(unit_params())
        self.assertEqual(d["cac_paying"], 30)

    def test_ltv_cac_uses_paying_cac(self):
        d = calc.derived(unit_params(**MIX, **FREEMIUM))
        want = round(d["ltv"] / d["cac_paying"], 6)
        self.assertAlmostEqual(d["ltv_cac"], want)
        self.assertLess(d["ltv_cac"], d["ltv"] / 30)  # не «LTV / CAC 30»

    def test_workbook_has_paying_cac_row(self):
        wb = calc.unit_econ(unit_params(**FREEMIUM))
        rows = [tuple(r) for r in wb.sheets[0].rows]
        paying = [r for r in rows if isinstance(r[0], str) and "платящего" in str(r[0])]
        self.assertTrue(paying, "нет строки CAC платящего")


class ScenarioSheetTests(unittest.TestCase):
    """Сценарии pessimistic / base / optimistic — один лист."""

    def test_three_scenarios_present(self):
        wb = calc.unit_econ(unit_params(**MIX, **FREEMIUM))
        names = [s.name for s in wb.sheets]
        self.assertIn("Сценарии", names)
        scen = wb.sheets[names.index("Сценарии")]
        labels = " | ".join(str(r[0]) for r in scen.rows)
        for word in ("пессимист", "баз", "оптимист"):
            self.assertIn(word, labels.lower())

    def test_scenario_multipliers_change_ltv(self):
        p = unit_params(**MIX, **FREEMIUM)
        p["scenarios"] = {"pessimistic": {"arpu": 0.8, "churn": 1.5, "cac": 1.3}}
        wb = calc.unit_econ(p)
        scen = wb.sheets[[s.name for s in wb.sheets].index("Сценарии")]
        base = calc.derived(p)
        pess = calc.derived(p, mult={"arpu": 0.8, "churn": 1.5, "cac": 1.3})
        self.assertAlmostEqual(pess["ltv"], base["arpu"] * 0.8 * 0.75 / (0.08 * 1.5), places=5)
        rows = [r for r in scen.rows if isinstance(r[0], str) and "пессимист" in str(r[0]).lower()]
        cached = [c.get("cached") for c in rows[0] if isinstance(c, dict) and "cached" in c]
        self.assertTrue(any(abs(v - pess["ltv"]) < 0.02 for v in cached),
                        f"кэш сценария не сходится с расчётом: {cached}")


class FunnelTests(unittest.TestCase):
    """Воронка задаётся в calcs.json явно: визиты, установки, экспорты — разные шаги."""

    FUNNEL = [
        {"name": "Визиты hosted", "unit": "визитов/мес", "value": 1000},
        {"name": "Активации (первый экспорт)", "unit": "активаций/мес", "share": 0.05},
        {"name": "Платящие", "unit": "платящих/мес", "share": 0.035},
    ]

    def test_growth_funnel_sheet_with_units(self):
        wb = calc.growth({**calc.DEFAULTS["growth"], "funnel": self.FUNNEL})
        names = [s.name for s in wb.sheets]
        self.assertIn("Воронка", names)
        sheet = wb.sheets[names.index("Воронка")]
        units = " | ".join(str(r[2]) for r in sheet.rows)
        self.assertIn("визитов/мес", units)
        self.assertIn("платящих/мес", units)

    def test_funnel_chain_values(self):
        wb = calc.growth({**calc.DEFAULTS["growth"], "funnel": self.FUNNEL})
        sheet = wb.sheets[[s.name for s in wb.sheets].index("Воронка")]
        vals = []
        for r in sheet.rows:
            if r and isinstance(r[0], str) and r[0] in {f["name"] for f in self.FUNNEL}:
                cell = r[3]
                vals.append(cell["cached"] if isinstance(cell, dict) else cell)
        self.assertEqual(vals, [1000, 50, 1.75])  # 1000 → ×0,05 → ×0,035

    def test_no_funnel_no_sheet(self):
        wb = calc.growth(dict(calc.DEFAULTS["growth"]))
        self.assertNotIn("Воронка", [s.name for s in wb.sheets])


OPTIONS = {
    "criteria": [
        {"name": "Рост аудитории", "weight": 2},
        {"name": "Реализуемость", "weight": 3, "gate_min": 3},
        {"name": "Скорость", "weight": 1},
    ],
    "options": [
        {"name": "A. Оставить как есть", "scores": [1, 5, 3]},
        {"name": "B. Агрессивный рост", "scores": [5, 2, 5]},
        {"name": "C. Волновой вход", "scores": [4, 3, 4]},
    ],
}


class OptionsScoringTests(unittest.TestCase):
    """Скоринг вариантов: числовые веса, взвешенная сумма, фильтры-пороги."""

    def test_weighted_total_differs_from_plain_sum(self):
        res = calc.options_scores(OPTIONS)
        plain = {r["name"]: sum(r["scores"]) for r in res}
        # при равных весах побеждает B (12 баллов), с весами и фильтром — C (21)
        self.assertEqual(max(plain, key=plain.get), "B. Агрессивный рост")
        ranked = [r["name"] for r in res if r["passes"]]
        self.assertEqual(ranked[0], "C. Волновой вход")
        c = next(r for r in res if r["name"].startswith("C"))
        self.assertEqual(c["total"], 4 * 2 + 3 * 3 + 4 * 1)

    def test_gate_filters_option(self):
        res = calc.options_scores(OPTIONS)
        b = next(r for r in res if r["name"].startswith("B"))
        self.assertFalse(b["passes"])
        self.assertIn("3", b["reason"])

    def test_workbook_and_md(self):
        pdir = project.create("Скоринг", "Какой вариант берём?", slug="opt1")
        (pdir / "calcs.json").write_text(json.dumps({"options": OPTIONS}, ensure_ascii=False),
                                         encoding="utf-8")
        paths = calc.run(pdir, "options")
        self.assertEqual(len(paths), 1)
        book = paths[0]
        self.assertEqual(book.name, "options_scoring.xlsx")
        with zipfile.ZipFile(book) as z:
            self.assertIsNone(z.testzip())
        self.assertIn("Скоринг", xlsx.sheet_names(book))
        md = pdir / "outputs" / "attachments" / "options_scoring.md"
        self.assertTrue(md.exists(), "md-таблица скоринга не записана")
        text = md.read_text(encoding="utf-8")
        self.assertIn("вес", text)                 # веса видны в заголовках колонок
        self.assertIn("отсеян", text.lower())   # фильтр виден
        self.assertLess(text.index("C. Волновой вход"), text.index("A. Оставить"))  # ранжирование

    def test_all_skips_options_without_section(self):
        pdir = project.create("Скоринг нет секции", "Вопрос?", slug="opt2")
        paths = calc.run(pdir, "all")
        self.assertFalse(any(p.name == "options_scoring.xlsx" for p in paths))


if __name__ == "__main__":
    unittest.main()
