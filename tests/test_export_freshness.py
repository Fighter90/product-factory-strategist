"""Свежесть экспорта: снимок реестра в outputs/.export_state.json и предупреждение
«реестр изменился после последнего экспорта» при `pfs status` и повторном экспорте.

Запуск: python3 -m unittest discover -s tests -v
"""
import os
import tempfile
import unittest

TMP = tempfile.mkdtemp(prefix="pfs-test-fresh-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import claims, core, export, project, sources  # noqa: E402


def fresh(slug):
    return project.create(f"Свежесть {slug}", "Почему падает удержание подписчиков?", slug=slug)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.pdir = fresh(self.id().rsplit(".", 1)[-1][:50])

    def test_snapshot_written_and_no_warning_right_after_export(self):
        pdir = self.pdir
        sources.add(pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        export.build(pdir)
        export.save_state(pdir)
        snap = export.read_state(pdir)
        self.assertEqual(snap["claims"], 1)
        self.assertEqual(snap["sources"], 1)
        self.assertEqual(export.freshness_warnings(pdir), [])
        self.assertNotIn("⚠", project.status_text(pdir))

    def test_no_snapshot_no_warning(self):
        # Экспорта ещё не было — предупреждений нет и status не падает.
        self.assertEqual(export.freshness_warnings(self.pdir), [])
        self.assertNotIn("⚠", project.status_text(self.pdir))

    def test_claims_change_warns_and_reexport_clears(self):
        pdir = self.pdir
        claims.add(pdir, "Первая гипотеза", "hypothesis", [], grade="D")
        export.build(pdir)
        export.save_state(pdir)
        self.assertEqual(export.freshness_warnings(pdir), [])
        claims.add(pdir, "Вторая гипотеза", "hypothesis", [], grade="D")
        claims.add(pdir, "Третья гипотеза", "hypothesis", [], grade="D")
        warns = export.freshness_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("⚠", warns[0])
        self.assertIn("реестр изменился после последнего экспорта", warns[0].lower())
        self.assertIn("+2 claims", warns[0])
        self.assertIn("pfs export", warns[0])  # подсказка: чем пересобрать
        self.assertIn("⚠", project.status_text(pdir))
        # Повторный экспорт обновляет снимок — предупреждение уходит.
        export.build(pdir)
        export.save_state(pdir)
        self.assertEqual(export.freshness_warnings(pdir), [])
        self.assertNotIn("⚠", project.status_text(pdir))

    def test_sources_change_warns(self):
        pdir = self.pdir
        export.build(pdir)
        export.save_state(pdir)
        sources.add(pdir, text="Свежее исследование рынка", title="Исследование")
        warns = export.freshness_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("+1 sources", warns[0])

    def test_excel_rebuilt_warns(self):
        pdir = self.pdir
        export.build(pdir)
        export.save_state(pdir)
        att = pdir / "outputs" / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        (att / "unit_economics.xlsx").write_bytes(b"PK\x03\x04 dummy")
        warns = export.freshness_warnings(pdir)
        self.assertIn("Excel пересобран", warns[0])

    def test_calcs_json_edited_warns(self):
        pdir = self.pdir
        export.build(pdir)
        export.save_state(pdir)
        (pdir / "calcs.json").write_text('{"unit_econ": {"arpu": 10}}', encoding="utf-8")
        warns = export.freshness_warnings(pdir)
        self.assertIn("Excel пересобран", warns[0])

    def test_claim_retract_warns_without_count_change(self):
        # Отзыв утверждения (как и rebase) ПЕРЕПИСЫВАЕТ claims.jsonl на месте: число строк
        # не меняется, но Приложение A собранного отчёта уже врёт — предупреждение обязательно.
        pdir = self.pdir
        c = claims.add(pdir, "Рынок растёт на 20%", "hypothesis", [], grade="D")
        export.build(pdir)
        export.save_state(pdir)
        self.assertEqual(export.freshness_warnings(pdir), [])
        claims.retract(pdir, c["id"], "источник оказался недостоверным")
        warns = export.freshness_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("⚠", warns[0])
        self.assertIn("claims.jsonl", warns[0])  # содержимое изменилось без +/− по строкам
        self.assertNotIn("claims+", warns[0])
        self.assertIn("⚠", project.status_text(pdir))
        # Повторный экспорт снимает предупреждение.
        export.build(pdir)
        export.save_state(pdir)
        self.assertEqual(export.freshness_warnings(pdir), [])

    def test_sources_inplace_rewrite_warns(self):
        # pfs source refresh перезаписывает строку sources.jsonl на месте (без дубля):
        # число источников то же, таблица источников в отчёте устарела — предупреждение.
        pdir = self.pdir
        s, _created = sources.add(pdir, text="Отчёт за 2025 год", title="Отчёт")
        export.build(pdir)
        export.save_state(pdir)
        self.assertEqual(export.freshness_warnings(pdir), [])
        rows = core.read_jsonl(pdir / "sources.jsonl")  # то же, что делает sources.refresh
        for r in rows:
            if r["id"] == s["id"]:
                r["title"] = "Отчёт за 2026 год (обновлён)"
                r["retrieved"] = core.now()
        core.write_jsonl(pdir / "sources.jsonl", rows)
        warns = export.freshness_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("⚠", warns[0])
        self.assertIn("sources.jsonl", warns[0])
        self.assertNotIn("+1 sources", warns[0])

    def test_combined_changes_in_one_warning(self):
        pdir = self.pdir
        export.build(pdir)
        export.save_state(pdir)
        claims.add(pdir, "Ещё гипотеза", "hypothesis", [], grade="D")
        sources.add(pdir, text="Ещё источник", title="Источник")
        att = pdir / "outputs" / "attachments"
        att.mkdir(parents=True, exist_ok=True)
        (att / "growth_model.xlsx").write_bytes(b"PK\x03\x04 dummy")
        warns = export.freshness_warnings(pdir)
        self.assertEqual(len(warns), 1)
        self.assertIn("+1 claims, +1 sources, Excel пересобран", warns[0])


if __name__ == "__main__":
    unittest.main()
