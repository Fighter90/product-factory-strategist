"""Охраны видео-конвейера PRO-124 (scripts/video_gen.py + video/scenarios/*.json).

Red-first: тесты падают, если из сценариев демо «Связь для близких» исчезают
ключевые цифры брифа/демо, если остаются устаревшие числа, если плейсхолдеры
{{…}} не заполняются значениями по умолчанию или если project_vars() перестаёт
выводить числа из артефактов проекта (claims/decisions/log/outputs/economics).

Только чистые функции движка — без say/ffmpeg/PIL, работает на любой машине.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from video_gen import default_vars, project_vars, substitute  # noqa: E402

SCEN_DIR = ROOT / "video" / "scenarios"
SCENARIOS = [
    "svyaz-overview-ru.json",
    "svyaz-overview-en.json",
    "svyaz-walkthrough-ru.json",
    "svyaz-walkthrough-en.json",
    "svyaz-walkthrough-full-ru.json",
    "svyaz-walkthrough-full-en.json",
]


def load_scenario(name):
    return json.loads((SCEN_DIR / name).read_text(encoding="utf-8"))


def scenario_text(name):
    """Сырой текст всех beat'ов сценария (с плейсхолдерами)."""
    scen = load_scenario(name)
    return " \n ".join(
        (b.get("text") or b.get("out") or b.get("cmd", "")) for b in scen["beats"]
    )


class ScenarioKeyFiguresTests(unittest.TestCase):
    """Ключевые цифры брифа/демо обязаны присутствовать в сценариях."""

    def test_walkthrough_ru_has_three_key_figures(self):
        text = scenario_text("svyaz-walkthrough-ru.json")
        self.assertIn("{{boundary_months}} мес", text, "граница решения из брифа (12 000 мес)")
        self.assertIn("{{target_mln}} млн", text, "целевой сценар прибыли (285,75 млн)")
        self.assertIn("минус три п.п.", text, "порог проверки −3 п.п. (12% → 9%)")

    def test_walkthrough_en_has_three_key_figures(self):
        text = scenario_text("svyaz-walkthrough-en.json")
        self.assertIn("{{boundary_months}} months", text)
        self.assertIn("{{target_mln}}M", text)
        self.assertIn("minus three percentage points", text)

    def test_overviews_have_boundary(self):
        for name in ("svyaz-overview-ru.json", "svyaz-overview-en.json"):
            with self.subTest(name=name):
                self.assertIn("{{boundary_months}}", scenario_text(name))

    def test_full_scenarios_have_claims_breakdown(self):
        self.assertIn("{{claims_total}} утверждений", scenario_text("svyaz-walkthrough-full-ru.json"))
        self.assertIn("{{c_fact}} фактов", scenario_text("svyaz-walkthrough-full-ru.json"))
        self.assertIn("{{claims_total}} claims", scenario_text("svyaz-walkthrough-full-en.json"))
        self.assertIn("{{c_inf}} inferences", scenario_text("svyaz-walkthrough-full-en.json"))

    def test_no_stale_numbers_in_scenarios(self):
        """Числа, исправленные по факту демо, не должны вернуться (PRO-124)."""
        stale = ["918", "42 карт", "42 cards", "285,8", "285.8", "10 допущений",
                 "10 assumptions", "6 выводов", "6 inferences"]
        for name in SCENARIOS:
            raw = (SCEN_DIR / name).read_text(encoding="utf-8")
            for s in stale:
                with self.subTest(scenario=name, stale=s):
                    self.assertNotIn(s, raw)


class SubstitutionTests(unittest.TestCase):
    """Плейсхолдеры заполняются значениями по умолчанию без остатка."""

    def test_all_placeholders_filled_by_defaults(self):
        for name in SCENARIOS:
            with self.subTest(scenario=name):
                scen = load_scenario(name)
                _, _, missing = substitute(scen["beats"], scen.get("title", ""),
                                           default_vars(scen.get("lang", "ru")))
                self.assertEqual(missing, [], "незаполненные плейсхолдеры")

    def test_unknown_placeholder_is_reported_and_kept(self):
        beats = [{"speaker": "pfs", "text": "итог {{no_such_var}} руб."}]
        out, _, missing = substitute(beats, "", {})
        self.assertEqual(missing, ["no_such_var"])
        self.assertIn("{{no_such_var}}", out[0]["text"])

    def test_ru_and_en_formats_differ(self):
        ru = default_vars("ru")
        en = default_vars("en")
        self.assertEqual(ru["target_mln"], "285,75")
        self.assertEqual(en["target_mln"], "285.75")
        self.assertIn("12", ru["boundary_months"].replace("\u00a0", "").replace(" ", ""))
        self.assertEqual(ru["boundary_months"].replace("\u00a0", " "), "12 000")
        self.assertEqual(en["boundary_months"], "12,000")


class ProjectVarsTests(unittest.TestCase):
    """project_vars() выводит числа из артефактов проекта-фикстуры."""

    def _fixture(self, tmp: Path) -> Path:
        p = tmp / "proj"
        (p / "analysis").mkdir(parents=True)
        (p / "outputs").mkdir(parents=True)
        claims = [
            {"id": "C001", "kind": "fact", "status": "active"},
            {"id": "C002", "kind": "fact", "status": "active"},
            {"id": "C003", "kind": "assumption", "status": "active"},
            {"id": "C004", "kind": "hypothesis", "status": "active"},
            {"id": "C005", "kind": "inference", "status": "superseded"},
        ]
        (p / "claims.jsonl").write_text(
            "\n".join(json.dumps(c) for c in claims), encoding="utf-8")
        (p / "decisions.jsonl").write_text(
            json.dumps({"id": "D001", "status": "accepted"}), encoding="utf-8")
        (p / "outputs" / "07_quality_review.md").write_text(
            "0 ошибок (98/100)\n", encoding="utf-8")
        (p / "log.jsonl").write_text(
            json.dumps({"msg": "Собран финальный пакет: a.xlsx, b.md, c.docx, d.html"},
                       ensure_ascii=False),
            encoding="utf-8")
        (p / "analysis" / "economics.py").write_text(
            "print('Цель +6 млн → 12 000 доп. оплаченных месяцев × 500 руб.')\n"
            "print('вклад нетто +6.75 млн → прибыль 285.75 млн (цель 285)')\n",
            encoding="utf-8")
        return p

    def test_vars_derived_from_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._fixture(Path(td))
            ru = project_vars(p, "ru")
            self.assertEqual(ru["claims_total"], "4")          # superseded не считается
            self.assertEqual(ru["c_fact"], "2")
            self.assertEqual(ru["c_inf"], "0")                 # ноль выводов — тоже значение
            self.assertEqual(ru["decision_id"], "D001")
            self.assertEqual(ru["score"], "98/100")
            self.assertEqual(ru["artifacts"], "4")
            self.assertEqual(ru["target_mln"], "285,75")
            self.assertEqual(ru["boundary_months"], "12\u00a0000")
            en = project_vars(p, "en")
            self.assertEqual(en["target_mln"], "285.75")
            self.assertEqual(en["boundary_months"], "12,000")

    def test_missing_project_dir_is_tolerated(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(project_vars(Path(td) / "nope", "ru"), {})


class EngineContractTests(unittest.TestCase):
    """Контракт CLI: параметр ПУТЬ К ПРОЕКТУ (--project) присутствует (PRO-124)."""

    def test_help_mentions_project_argument(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "video_gen.py"), "--help"],
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(r.returncode, 0)
        self.assertIn("--project", r.stdout)


if __name__ == "__main__":
    unittest.main()
