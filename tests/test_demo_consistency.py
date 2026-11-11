"""Инварианты зафиксированного демо-проекта (PRO-63, ревью круг 4).

Демо показывается как эталон (README, сайт, доки), поэтому его закоммиченное
состояние обязано быть согласованным само по себе, без пересборки на месте:

1. Последняя запись `pfs finish` в журнале объясняет отсутствие deck.html
   маркером «(без деки: --no-deck)» — иначе журнал выглядит как регресс
   сборки деки (ревью: запись 12:05:38 без маркера противоречила CHANGELOG).
2. deck.html побайтово равен пересборке из зафиксированного SIX_PAGER.md —
   «deck пересобран из финального six-pager» становится проверяемым фактом,
   а не утверждением в CHANGELOG; правка SIX_PAGER.md без пересборки деки
   отныне падает тестом. Правки SIX_PAGER, не меняющие рендер (строка
   «Собрано», пункты за шапкой слайда ≤6), диффа не дают — и это норма.
3. Снимок свежести (.export_state.json) соответствует файлам на диске —
   чистый клон демо не даёт ложного «⚠ Реестр изменился после последнего
   экспорта» (критерий готовности PRO-63).

Запуск: python3 -m unittest tests.test_demo_consistency -v
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-demo-consistency-")
os.environ["PFS_PROJECTS_DIR"] = TMP

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "projects" / "демо"

from tools.pfs import export  # noqa: E402


class FinishLogMarksNoDeck(unittest.TestCase):
    def test_last_finish_entry_explains_missing_deck(self):
        entries = [json.loads(line)
                   for line in (DEMO / "log.jsonl").read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        finishes = [e for e in entries
                    if str(e.get("msg", "")).startswith("Собран финальный пакет")]
        self.assertTrue(finishes, "в журнале демо нет записей pfs finish")
        msg = finishes[-1]["msg"]
        # Пакет либо содержит deck.html, либо явно помечен «без деки» —
        # отсутствие deck.html без пояснения читается как регресс сборки.
        self.assertTrue("deck.html" in msg or "(без деки: --no-deck)" in msg, msg)


class DeckMatchesSixPager(unittest.TestCase):
    def test_deck_html_equals_rebuild_from_committed_six_pager(self):
        with tempfile.TemporaryDirectory() as d:
            pdir = Path(d) / "демо"
            (pdir / "outputs").mkdir(parents=True)
            shutil.copy(DEMO / "outputs" / "SIX_PAGER.md", pdir / "outputs" / "SIX_PAGER.md")
            shutil.copy(DEMO / "project.json", pdir / "project.json")
            built = export.build_deck(pdir)
            committed = DEMO / "outputs" / "presentations" / "deck.html"
            self.assertTrue(committed.exists(), "deck.html не закоммичен")
            self.assertEqual(built.read_bytes(), committed.read_bytes(),
                             "deck.html не равен пересборке из зафиксированного SIX_PAGER.md")


class FreshnessSnapshotMatchesFiles(unittest.TestCase):
    def test_no_stale_registry_facts_on_committed_demo(self):
        self.assertEqual(export.freshness_facts(DEMO), [],
                         "снимок экспорта демо не соответствует файлам — чистый клон "
                         "получит ложное «⚠ Реестр изменился»")
        self.assertEqual(export.freshness_warnings(DEMO), [])


if __name__ == "__main__":
    unittest.main()
