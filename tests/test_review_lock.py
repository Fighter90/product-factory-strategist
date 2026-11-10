"""PRO-27: pfs review lock — фиксация снимка реестра после ревизии и предупреждение
«вердикт review устарел» при правках реестра после lock (pfs status / pfs check /
Приложение D отчёта); повторный lock после ревизии снимает предупреждение.

Пометка хранится в warnings сырой, без «⚠ » (однородный список для --json:
хуки, MCP pfs_check); префикс добавляют места текстового вывода
(report_text, status_text, cmd_export).

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-review-lock-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import check, claims, core, export, project, review, sources  # noqa: E402

RAW = "вердикт review устарел — реестр изменился после ревизии; повторите evidence-auditor"
WARN = "⚠ " + RAW  # так пометка выглядит в текстовых выводах — префикс на месте вывода


def make_project(slug):
    pdir = project.create(f"Ревизия {slug}", "Почему падает удержание подписчиков?", slug=slug)
    sources.add(pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
    claims.add(pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
    return pdir


class ReviewLockTests(unittest.TestCase):
    def setUp(self):
        self.pdir = make_project(self.id().rsplit(".", 1)[-1][:50])

    def test_no_lock_no_warning(self):
        # Lock ещё не выполнялся: предупреждений нет, файла снимка нет.
        pdir = self.pdir
        self.assertFalse((pdir / "outputs" / review.STATE).exists())
        self.assertEqual(review.stale_warnings(pdir), [])
        self.assertNotIn(WARN, check.report_text(check.run(pdir)))
        self.assertNotIn(WARN, project.status_text(pdir))

    def test_lock_writes_snapshot_and_no_warning_right_after(self):
        pdir = self.pdir
        snap = review.lock(pdir)
        self.assertTrue((pdir / "outputs" / review.STATE).exists())
        self.assertIn("at", snap)
        self.assertIsNotNone(snap["claims_sha"])
        self.assertIsNotNone(snap["sources_sha"])
        self.assertIn("02_situation.md", snap["documents"])  # документы 00–07 в снимке
        self.assertEqual(review.stale_warnings(pdir), [])
        self.assertNotIn(WARN, check.report_text(check.run(pdir)))
        self.assertNotIn(WARN, project.status_text(pdir))

    def test_claim_edit_after_lock_warns_everywhere(self):
        # Критерий приёмки: правка claims после lock → предупреждение в status/check/export.
        pdir = self.pdir
        review.lock(pdir)
        claims.add(pdir, "Гипотеза: рынок растёт", "hypothesis", [], grade="D")
        warns = review.stale_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertTrue(warns[0].startswith(RAW))  # ревью 2: сырое сообщение — без «⚠ »
        self.assertIn("claims.jsonl", warns[0])
        report = check.report_text(check.run(pdir))
        self.assertIn(WARN, report)
        self.assertNotIn("⚠ ⚠", report)  # префикс не задваивается
        self.assertIn(WARN, project.status_text(pdir))
        export.build(pdir)
        report = (pdir / "outputs" / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("# Приложение D. Прозрачность", report)
        d_block = report.split("# Приложение D. Прозрачность", 1)[1]
        self.assertIn(WARN, d_block)

    def test_json_warnings_stay_homogeneous(self):
        # Ревью 2: warnings в JSON (pfs check --json, MCP pfs_check) — без «⚠ »:
        # префикс добавляют только места текстового вывода, список однороден.
        pdir = self.pdir
        review.lock(pdir)
        claims.add(pdir, "Гипотеза: рынок растёт", "hypothesis", [], grade="D")
        core.atomic_write(pdir / "outputs" / "02_situation.md", "# 02 · Картина ситуации — правка")
        res = check.run(pdir)
        self.assertIn(RAW, " ".join(res["warnings"]))
        for w in res["warnings"]:
            self.assertNotIn("⚠", w)  # ни одна пометка не несёт префикс сама

    def test_document_edit_after_lock_warns(self):
        pdir = self.pdir
        review.lock(pdir)
        core.atomic_write(pdir / "outputs" / "02_situation.md", "# 02 · Картина ситуации — правка")
        warns = review.stale_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn(RAW, warns[0])
        self.assertIn("02_situation.md", warns[0])
        self.assertIn(WARN, project.status_text(pdir))

    def test_source_edit_after_lock_warns(self):
        pdir = self.pdir
        review.lock(pdir)
        sources.add(pdir, text="Свежее исследование рынка", title="Исследование")
        warns = review.stale_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("sources.jsonl", warns[0])

    def test_relock_after_review_clears_warning(self):
        # Критерий приёмки: после повторного review (повторного lock) предупреждение уходит.
        pdir = self.pdir
        review.lock(pdir)
        claims.add(pdir, "Гипотеза: рынок растёт", "hypothesis", [], grade="D")
        self.assertIn(WARN, project.status_text(pdir))
        review.lock(pdir)  # повторная ревизия → повторный lock
        self.assertEqual(review.stale_warnings(pdir), [])
        self.assertNotIn(WARN, check.report_text(check.run(pdir)))
        self.assertNotIn(WARN, project.status_text(pdir))

    def test_export_after_lock_then_edit_keeps_warning(self):
        # Экспорт НЕ снимает пометку (снимает только повторный lock).
        pdir = self.pdir
        review.lock(pdir)
        claims.add(pdir, "Гипотеза: рынок растёт", "hypothesis", [], grade="D")
        export.build(pdir)
        self.assertEqual(len(review.stale_warnings(pdir)), 1)
        self.assertIn(WARN, project.status_text(pdir))


if __name__ == "__main__":
    unittest.main()
