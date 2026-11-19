"""PRO-130: REGRESS-DEMO — охрана результатов критического аудита демо «Связь для близких».

Аудит «с разных сторон» (issue PRO-130) нашёл и этот файл закрепляет:

1. Математика: разрывы неблагоприятного хода согласованы во всех документах и
   совпадают с пересчётом скриптом analysis/economics.py —
   прибыль 285 − 280,5 = −4,5 млн руб.; активные 8 000 − 6 400 = −1 600;
   «владельцы» 2 000 − 1 000 = −1 000. Устаревшие числа (−2,5 млн, −1 200)
   запрещены в 04/SIX_PAGER RU+EN/six_pager_pack/BRIEF_RESPONSE/REPORT.
2. Теги: ни один документ демо не ссылается тегом [C###] (в т.ч. комбинированным
   [C012,C018]) на замещённое/отозванное утверждение; в основаниях решений и
   derived_from активных утверждений неактивных ID тоже нет.
3. Воспроизводимость: analysis/economics_out.txt повторяет вывод скрипта
   посимвольно по ключевым числам (десятичные запятые заметки не ломаются
   форматированием тысяч «6 75» вместо «6,75»).

Запуск: python3 -m unittest tests.test_demo_audit_guard -v
"""
import json
import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEMO = REPO / "projects" / "связь-для-близких-и-собственных-устройств"

# Документы, в которых печатаются разрывы неблагоприятного хода (профит, млн руб.)
GAP_DOCS = ["04_product_strategy.md", "06_validation_plan.md", "BRIEF_RESPONSE.md",
            "SIX_PAGER.md", "SIX_PAGER_EN.md", "six_pager_pack.md", "REPORT.md"]

# Комбинированные теги: [C013,C018], [C018,S001] — одиночный [C###] и перечисления
_TAG = re.compile(r"\[([^\]\n]*)\]")
_CID = re.compile(r"\bC\d{3,}\b")


def _doc(name: str) -> str:
    return (DEMO / "outputs" / name).read_text(encoding="utf-8")


def _inactive_claim_ids() -> set[str]:
    """ID утверждений с статусом != active (superseded/retracted)."""
    out = set()
    for line in (DEMO / "claims.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            c = json.loads(line)
            if c.get("status") != "active":
                out.add(c["id"])
    return out


class UnfavorableGapMathTests(unittest.TestCase):
    """Разрывы неблагоприятного хода = цель − прогноз, одинаковые везде (PRO-130, математика)."""

    STALE_MARKERS = ("−2,5 млн", "-2,5 млн", "RUB 2.5M short",  # прибыль: 285−280,5=4,5, не 2,5
                     "−1 200", "-1 200")                         # активные: 8 000−6 400=1 600

    def test_no_stale_gap_numbers(self):
        offenders = []
        for name in GAP_DOCS:
            text = _doc(name)
            for marker in self.STALE_MARKERS:
                if marker in text:
                    offenders.append(f"{name}: «{marker}»")
        self.assertEqual(offenders, [],
                         "устаревшие разрывы неблагоприятного хода (верно: −4,5 млн и −1 600): "
                         + "; ".join(offenders))

    def test_correct_gaps_present(self):
        # прибыль: «Разрывы в неблагоприятном ходе: прибыль −4,5 млн» в 04/SIX_PAGER/pack
        for name in ("04_product_strategy.md", "six_pager_pack.md", "REPORT.md"):
            self.assertIn("−4,5 млн", _doc(name), f"{name}: нет корректного разрыва прибыли −4,5 млн")
        # активные: «активные −1 600» в BRIEF_RESPONSE/04/06
        for name in ("BRIEF_RESPONSE.md", "04_product_strategy.md", "06_validation_plan.md"):
            self.assertIn("−1 600", _doc(name), f"{name}: нет корректного разрыва активных −1 600")


class EconomicsScriptTests(unittest.TestCase):
    """Пересчёт ключевых чисел скриптом и совпадение с сохранённым выводом (PRO-130)."""

    def test_script_reproduces_key_numbers(self):
        out = subprocess.run(["python3", "analysis/economics.py"], cwd=DEMO,
                             capture_output=True, text=True, timeout=60).stdout
        for expected in ("12 000 доп. оплаченных месяцев",        # 6 млн / 500 руб.
                         "+6.75", "285.75",                        # 5 500×3×500−1,5 млн
                         "+4.50", "283.50",                        # 4 000×3−1,5 млн
                         "+1.50", "280.50",                        # 3 000×2−1,5 млн
                         "62.5%", "66.7%",                         # 5 000/8 000 и 8 000/12 000
                         "прирост 5 500", "4 000"):                # 12 000−6 500 и 12 000−8 000
            self.assertIn(expected, out, f"economics.py не печатает «{expected}»")

    def test_saved_output_matches_script_decimals(self):
        """Сохранённый economics_out.txt не ломает десятичные запятые заметки прогноза."""
        saved = (DEMO / "analysis" / "economics_out.txt").read_text(encoding="utf-8")
        self.assertIn("вклад нетто 6,75 / 1,5 млн", saved,
                      "economics_out.txt: «6,75 / 1,5» превращено форматированием тысяч в «6 75 / 1 5»")
        self.assertNotIn("6 75", saved, "economics_out.txt: сломанная десятичная запятая «6 75»")


class NoInactiveClaimTagsTests(unittest.TestCase):
    """Ни одного тега/основания на замещённое или отозванное утверждение (PRO-130, теги)."""

    def test_outputs_and_docs_have_no_inactive_tags(self):
        """Скобочные теги [C###] и перечисления [C###,C###] — только на активные утверждения."""
        inactive = _inactive_claim_ids()
        offenders = []
        docs = sorted(DEMO.glob("*.md")) + sorted((DEMO / "outputs").glob("*.md"))
        for doc in docs:
            for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
                for tag in _TAG.findall(line):
                    hit = sorted(set(_CID.findall(tag)) & inactive)
                    if hit:
                        offenders.append(f"{doc.relative_to(DEMO)}:{i}: [{tag}] → {', '.join(hit)}")
        self.assertEqual(offenders, [],
                         "теги ссылаются на замещённые/отозванные утверждения:\n" + "\n".join(offenders))

    def test_calcs_and_pack_json_have_no_inactive_refs(self):
        """calcs.json и six_pager_pack.json: теги в записках и grounds — только активные.

        Легальны только записи реестра: «"id": "C###"» и строка утверждений пакета."""
        inactive = _inactive_claim_ids()
        offenders = []
        for rel in ("calcs.json", "outputs/six_pager_pack.json"):
            text = (DEMO / rel).read_text(encoding="utf-8")
            for tag in _TAG.findall(text):
                hit = sorted(set(_CID.findall(tag)) & inactive)
                if hit:
                    offenders.append(f"{rel}: [{tag}] → {', '.join(hit)}")
            for m in re.finditer(r'"grounds":\s*\[([^\]]*)\]', text):
                hit = sorted(set(_CID.findall(m.group(1))) & inactive)
                if hit:
                    offenders.append(f"{rel}: grounds {m.group(1)} → {', '.join(hit)}")
        self.assertEqual(offenders, [], "JSON-артефакты ссылаются на неактивные утверждения:\n"
                         + "\n".join(offenders))


class RegistryBasesActiveTests(unittest.TestCase):
    """Основания решений и выводов не опираются на неактивные утверждения (PRO-130, реестры)."""

    def _claims(self) -> dict[str, dict]:
        rows = {}
        for line in (DEMO / "claims.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                c = json.loads(line)
                rows[c["id"]] = c
        return rows

    def test_decision_grounds_are_active(self):
        claims = self._claims()
        offenders = []
        for line in (DEMO / "decisions.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            stale = [g for g in d.get("grounds", []) if claims.get(g, {}).get("status") != "active"]
            if stale:
                offenders.append(f"{d['id']}: {', '.join(stale)}")
        self.assertEqual(offenders, [], "основания решений неактивны: " + "; ".join(offenders))

    def test_active_claim_bases_are_active(self):
        claims = self._claims()
        offenders = []
        for cid, c in claims.items():
            if c.get("status") != "active":
                continue
            stale = [b for b in c.get("derived_from", []) if claims.get(b, {}).get("status") != "active"]
            if stale:
                offenders.append(f"{cid}: {', '.join(stale)}")
        self.assertEqual(offenders, [], "активные утверждения опираются на неактивные: "
                         + "; ".join(offenders))


if __name__ == "__main__":
    unittest.main()
