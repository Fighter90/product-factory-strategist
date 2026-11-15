"""Доп. тесты impact: транзитивный граф, строки документов, затронутые решения.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-ximp-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, decisions, impact, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class ImpactGraphTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"Импакт {id(self)}", "Что делать?", slug=f"ximp{id(self)}")
        s, _ = sources.add(self.pdir, text="отчёт о рынке", title="m")
        self.s = s["id"]
        self.c1 = claims.add(self.pdir, "Рынок 40 млрд", "fact", [self.s])["id"]
        self.c2 = claims.add(self.pdir, "Рынок достаточен", "inference", derived_from=[self.c1])["id"]
        self.c3 = claims.add(self.pdir, "Сегмент стоит входа", "inference", derived_from=[self.c2])["id"]

    def test_transitive_closure_from_source(self):
        res = impact.impact(self.pdir, self.s)
        self.assertEqual(res["claims"], [self.c1, self.c2, self.c3])  # вся цепочка выводов
        self.assertEqual(res["target"], self.s)
        text = impact.impact_text(res)
        self.assertIn(f"Влияние изменения {self.s}", text)
        self.assertIn("Утверждения (3)", text)
        self.assertIn("В документах ссылок нет.", text)  # пока нет упоминаний в документах

    def test_transitive_closure_from_claim_includes_self(self):
        res = impact.impact(self.pdir, self.c1)
        self.assertEqual(res["claims"], [self.c1, self.c2, self.c3])

    def test_doc_refs_lines_and_text(self):
        doc = self.pdir / "outputs" / "03_options.md"
        doc.write_text("# Варианты\n\n## Вариант A\nРынок 40 млрд [" + self.c1 + "] — растём.\n"
                       "Решение [" + "D001" + "] зафиксировано ниже.\n", encoding="utf-8")
        refs = impact.doc_refs(self.pdir)
        self.assertEqual(refs[self.c1], [("03_options.md", 4, f"Рынок 40 млрд [{self.c1}] — растём.")])
        self.assertIn("D001", refs)  # теги решений тоже индексируются
        self.assertEqual(refs["D001"][0][1], 5)
        res = impact.impact(self.pdir, self.c1)
        self.assertEqual(res["doc_lines"][0]["doc"], "03_options.md")
        self.assertEqual(res["doc_lines"][0]["line"], 4)
        text = impact.impact_text(res)
        self.assertIn("03_options.md:4 [" + self.c1 + "]", text)
        self.assertIn("Места в документах, которые нужно пересмотреть", text)

    def test_impact_lists_decisions_and_unknown_raises(self):
        d = decisions.add(self.pdir, "Фокус", "Пилот", "CPO", [self.c1])
        res = impact.impact(self.pdir, self.s)
        self.assertEqual(res["decisions"], [{"id": d["id"], "title": "Фокус", "owner": "CPO"}])
        text = impact.impact_text(res)
        self.assertIn("Решения с затронутыми основаниями", text)
        self.assertIn(d["id"], text)
        with self.assertRaises(PfsError):
            impact.impact(self.pdir, "C999")
        with self.assertRaises(PfsError):
            impact.impact(self.pdir, "S999")


if __name__ == "__main__":
    unittest.main()
