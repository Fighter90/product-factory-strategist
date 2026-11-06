"""Доп. тесты решений: статусы, обязательства, rebase, due_text и таблица.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-xdec-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, decisions, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class DecisionStatusTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Решения {id(self)}", "Что делать?", slug=f"xdec{id(self)}")
        sources.add(self.pdir, text="данные для решения", title="d")
        c = claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"])
        self.d = decisions.add(self.pdir, "Фокус", "Пилот", "CPO", [c["id"]], review_date="2026-01-01")

    def rows(self):
        return decisions.load(self.pdir)

    def test_set_status_history_and_due_filtering(self):
        self.assertEqual(decisions.due(self.pdir, on="2026-06-01")["review_now"],
                         [f"{self.d['id']} «Фокус»: дата пересмотра 2026-01-01; триггеры: "])
        decisions.set_status(self.pdir, self.d["id"], "revisit", "новые данные")
        self.assertEqual(self.rows()[0]["status"], "revisit")
        self.assertEqual(self.rows()[0]["history"][-1]["status"], "revisit")
        self.assertEqual(len(decisions.due(self.pdir, on="2026-06-01")["review_now"]), 1)  # revisit тоже пересматриваем
        decisions.set_status(self.pdir, self.d["id"], "closed", "заменили другим решением")
        self.assertEqual(decisions.due(self.pdir, on="2026-06-01")["review_now"], [])  # закрытое не всплывает
        with self.assertRaises(PfsError):
            decisions.set_status(self.pdir, "D999", "closed", "нет такого")

    def test_update_commitment_note_and_unknown(self):
        d2 = decisions.add(self.pdir, "Второе", "Продолжаем", "PM", [claims.load(self.pdir)[0]["id"]],
                           commitments=["Запустить пилот|PM|2026-02-01"])
        decisions.update_commitment(self.pdir, d2["id"], "K1", "done", note="готово в спринте 14")
        k = self.rows()[-1]["commitments"][0]
        self.assertEqual(k["status"], "done")
        self.assertEqual(k["note"], "готово в спринте 14")
        self.assertIn("updated", k)
        self.assertEqual(decisions.due(self.pdir, on="2026-06-01")["overdue"], [])
        with self.assertRaises(PfsError):
            decisions.update_commitment(self.pdir, d2["id"], "K9", "done")
        with self.assertRaises(PfsError):
            decisions.update_commitment(self.pdir, "D999", "K1", "done")

    def test_commitment_without_due_not_overdue(self):
        d2 = decisions.add(self.pdir, "Третье", "Решение", "PM", [claims.load(self.pdir)[0]["id"]],
                           commitments=["Договориться с юридикой"])  # без «|кто|когда»
        k = self.rows()[-1]["commitments"][0]
        self.assertEqual(k["id"], "K1")
        self.assertEqual(k["owner"], None)
        self.assertEqual(k["due"], None)
        self.assertEqual(decisions.due(self.pdir, on="2999-12-31")["overdue"], [])
        self.assertEqual(d2["metrics"], [])


class RebaseAndTextTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Реbase {id(self)}", "Что делать?", slug=f"xrb{id(self)}")
        sources.add(self.pdir, text="старый отчёт", title="old")
        self.c = claims.add(self.pdir, "Сегмент растёт", "fact", ["S001"])
        self.d = decisions.add(self.pdir, "Фокус", "Пилот", "PM", [self.c["id"]])

    def rows(self):
        return decisions.load(self.pdir)

    def test_rebase_noop_keeps_record_clean(self):
        before = (self.pdir / "decisions.jsonl").read_text(encoding="utf-8")
        self.assertEqual(decisions.rebase(self.pdir, self.d["id"]), [])  # менять нечего
        self.assertEqual((self.pdir / "decisions.jsonl").read_text(encoding="utf-8"), before)
        self.assertNotIn("history", self.rows()[0])

    def test_rebase_retracted_ground_raises(self):
        claims.retract(self.pdir, self.c["id"], "ошибка в данных")
        with self.assertRaises(PfsError) as cm:
            decisions.rebase(self.pdir, self.d["id"])
        self.assertIn("отозвано", str(cm.exception))
        self.assertIn(self.d["id"], str(cm.exception))

    def test_due_text_and_table_rendering(self):
        self.assertIn("Нет просроченных обязательств", decisions.due_text(decisions.due(self.pdir)))
        project.ask_human(self.pdir, "Подтверждаете пилот?", ["да", "нет"])
        self.assertIn("РЕШИТЬ СЕЙЧАС: Подтверждаете пилот?",
                      decisions.due_text(decisions.due(self.pdir, on="2026-06-01")))
        d2 = decisions.add(self.pdir, "Фокус 2", "Пилот шире", "CPO", [self.c["id"]],
                           metrics=["Удержание M1: 38% -> 45% @2027-03-01"],
                           review_date="2026-01-01", triggers=["M1 < 40%"])
        t = decisions.table(decisions.load(self.pdir))
        self.assertIn("| ID | Решение | Ответственный | Основания | Показатели | Пересмотр | Статус |", t)
        self.assertIn(f"| {d2['id']} | Фокус 2: Пилот шире | CPO |", t)
        self.assertIn("Удержание M1: 38%→45% к 2027-03-01", t)
        self.assertIn("2026-01-01; M1 < 40%", t)


if __name__ == "__main__":
    unittest.main()
