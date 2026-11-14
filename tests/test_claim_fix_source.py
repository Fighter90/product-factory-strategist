"""PRO-50: `pfs claim fix-source` — перепривязка утверждения к правильному источнику
с перепроверкой цитаты против текста нового источника: числа цитаты, которых нет ни
в одном новом источнике, отклоняют перепривязку без записи (цитата могла быть
выдумана); --quote заменяет цитату дословно из источника.

Запуск: python3 -m unittest tests.test_claim_fix_source -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-fixsource-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, core, project, sources  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class FixSourceTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"FixSrc {id(self)}", "Почему падает удержание подписчиков?",
                                   slug=f"fixsrc{id(self)}")

    def _own(self, rec):
        f = check.numeric_findings(self.pdir, {rec["id"]: claims.get(self.pdir, rec["id"])},
                                   {s["id"]: s for s in sources.load(self.pdir)})
        return [m for m in f["errors"] + f["warnings"] if m.startswith(f"{rec['id']}/")]

    def test_fix_source_rebinds_and_clears_divergence(self):
        """Перепривязка на источник, в тексте которого есть числа цитаты:
        расхождение исчезает, текст/тип/цитата не меняются."""
        bad, _ = sources.add(self.pdir, text="Отчёт о рынке без чисел о покрытии. " * 6, title="Сводка")
        good, _ = sources.add(self.pdir, text="Продукт доступен на 17 локалях. " * 6, title="Покрытие")
        c = claims.add(self.pdir, "Покрытие 17 локалей", "fact", [bad["id"]], grade="B",
                       quote="доступен на 17 локалях")
        rec = claims.fix_source(self.pdir, c["id"], good["id"])
        self.assertEqual(rec["sources"], [good["id"]])
        self.assertEqual(rec["text"], c["text"])
        self.assertEqual(rec["quote"], c["quote"])
        self.assertEqual(rec["kind"], "fact")
        self.assertFalse(self._own(rec), self._own(rec))

    def test_fix_source_can_update_quote(self):
        """Опционально цитата обновляется вместе с привязкой (источник обновился)."""
        s, _ = sources.add(self.pdir, text="Бейдж v1.271.2 · 7,922 automated tests. " * 4, title="Сайт")
        c = claims.add(self.pdir, "Релиз на сайте", "fact", [s["id"]], grade="B", quote="старый бейдж")
        rec = claims.fix_source(self.pdir, c["id"], s["id"], quote="v1.271.2 · 7,922 automated tests")
        self.assertEqual(rec["quote"], "v1.271.2 · 7,922 automated tests")

    def test_gate_refuses_quote_numbers_absent_from_new_source(self):
        """Цитата, числа которой нет в новом источнике, отклоняет перепривязку —
        реестр не меняется (цитата могла быть выдумана)."""
        s1, _ = sources.add(self.pdir, text="Тариф 17 евро в месяц. " * 6, title="Тарифы 17 евро")
        s2, _ = sources.add(self.pdir, text="Тариф 42 евро в месяц. " * 6, title="Тарифы 42 евро")
        c = claims.add(self.pdir, "Тариф 17 евро", "fact", [s1["id"]], grade="B",
                       quote="тариф 17 евро в месяц")
        with self.assertRaises(PfsError) as ctx:
            claims.fix_source(self.pdir, c["id"], s2["id"])
        self.assertIn("17", str(ctx.exception))
        self.assertEqual(claims.get(self.pdir, c["id"])["sources"], [s1["id"]])

    def test_fix_source_writes_history_and_log(self):
        """Правка привязки видна: history-запись в строке реестра и запись в журнал."""
        s1, _ = sources.add(self.pdir, text="данные без чисел " * 6, title="Первый")
        s2, _ = sources.add(self.pdir, text="другие данные без чисел " * 6, title="Второй")
        c = claims.add(self.pdir, "Наблюдение без чисел", "fact", [s1["id"]], grade="B")
        rec = claims.fix_source(self.pdir, c["id"], s2["id"])
        row = [r for r in core.read_jsonl(self.pdir / "claims.jsonl") if r["id"] == c["id"]][0]
        self.assertEqual(row["sources"], [s2["id"]])
        self.assertIn("fix_source", (row.get("history") or [{}])[-1])
        log = (self.pdir / "log.jsonl").read_text(encoding="utf-8")
        self.assertIn("перепривязка", log)

    def test_fix_source_rejects_unknown_source(self):
        s, _ = sources.add(self.pdir, text="данные без чисел " * 6, title="Один")
        c = claims.add(self.pdir, "Наблюдение без чисел", "fact", [s["id"]], grade="B")
        with self.assertRaises(PfsError):
            claims.fix_source(self.pdir, c["id"], "S099")

    def test_fix_source_rejects_inactive_claim(self):
        s, _ = sources.add(self.pdir, text="данные без чисел " * 6, title="Один")
        c = claims.add(self.pdir, "Наблюдение без чисел", "fact", [s["id"]], grade="B")
        claims.retract(self.pdir, c["id"], "не подтвердилось")
        with self.assertRaises(PfsError):
            claims.fix_source(self.pdir, c["id"], s["id"])

    def test_fix_source_keeps_fact_rules(self):
        """Факт остаётся фактом: без источников и на одних синтетических — нельзя."""
        s, _ = sources.add(self.pdir, text="данные без чисел " * 6, title="Публичный")
        syn, _ = sources.add(self.pdir, text="ответ ИИ-респондента " * 6, title="ИИ-респондент",
                             origin="synthetic")
        c = claims.add(self.pdir, "Наблюдение без чисел", "fact", [s["id"]], grade="B")
        with self.assertRaises(PfsError):
            claims.fix_source(self.pdir, c["id"], [])
        with self.assertRaises(PfsError):
            claims.fix_source(self.pdir, c["id"], syn["id"])


if __name__ == "__main__":
    unittest.main()
