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
from datetime import datetime, timedelta
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


class SnapshotNotOlderThanFinish(unittest.TestCase):
    """«at» снимка свежести демо не старше последней записи pfs finish в журнале.

    Ревью PRO-63 круг 6: .export_state.json говорил «at: 16:58:53», а последняя
    запись finish в журнале — 19:37:52. pfs finish всегда переснимает реестр
    (export.save_state внутри finish.run), поэтому снимок, старше последнего
    finish, означает потерянный снимок той сборки. Допуск 2 с — на границу
    секунды между save_state и записью журнала при реальном прогоне."""

    _TOLERANCE_S = 2

    @staticmethod
    def _last_finish_ts(entries: list[dict]) -> str:
        finishes = [e for e in entries
                    if str(e.get("msg", "")).startswith("Собран финальный пакет")]
        assert finishes, "в журнале демо нет записей pfs finish"
        return str(finishes[-1]["ts"])

    def test_snapshot_at_is_not_older_than_last_finish_entry(self):
        entries = [json.loads(line)
                   for line in (DEMO / "log.jsonl").read_text(encoding="utf-8").splitlines()
                   if line.strip()]
        finish_ts = datetime.fromisoformat(self._last_finish_ts(entries))
        snap = export.read_state(DEMO)
        self.assertIsNotNone(snap, "в демо нет снимка свежести .export_state.json")
        snap_at = datetime.fromisoformat(str(snap["at"]))
        self.assertGreaterEqual(
            snap_at, finish_ts - timedelta(seconds=self._TOLERANCE_S),
            f"снимок свежести ({snap_at.isoformat()}) старше последней записи finish "
            f"({finish_ts.isoformat()}) — снимок той сборки потерян; "
            f"ожидалось «at» времени finish (см. tools/pfs/finish.py: save_state)")


class DeckExcludesUnitEconThresholdLine(unittest.TestCase):
    """Строка «Вывод (умозаключение): … до CAC ≈ $90,62 …» FAQ-3 НЕ попадает в деку.

    Ревью PRO-63 круг 6: правка этой строки в круге 5 (€90,62→$90,62) не изменила
    deck.html — проверить, что это не рассинхрон six-pager/deck, а свойство рендера:
    слайд берёт первые 6 тезисов раздела (_MAX_POINTS), и строка порогов стоит
    дальше кэпа. Если тезисы FAQ-3 перестроят так, что строка войдёт в рендер,
    тест упадёт — и валюту/формат строки тогда нужно проверять и в деке."""

    def test_threshold_line_is_beyond_deck_thesis_cap(self):
        from tools.pfs import export as exp
        text = (DEMO / "outputs" / "SIX_PAGER.md").read_text(encoding="utf-8")
        section = text.split("## FAQ-3", 1)[1].split("\n## ", 1)[0]
        theses = exp._points(section)
        self.assertLessEqual(len(theses), exp._MAX_POINTS)
        hits = [t for t in theses if "CAC ≈ $90,62" in t or "CAC ≈ €90,62" in t]
        self.assertEqual(hits, [],
                         "строка порогов юнит-экономики вошла в рендер деки — "
                         "deck.html надо пересобрать и проверить содержимое строки")


class ReportCurrencyMatchesModel(unittest.TestCase):
    """FAQ-3 юнит-экономики демо — пороги ДОЛЛАРОВОЙ модели (C016: paid $29, CAC $60).
    Ревью PRO-63 круг 5: в строке «Вывод (умозаключение)» был евро «CAC ≈ €90,62» —
    чужая валюта против «$» в том же абзаце. Порог — в самом тексте, не в файле:
    генератор (export._unit_econ_block) и пересборка обязаны держать валюту модели."""

    def test_threshold_line_uses_model_currency(self):
        text = (DEMO / "outputs" / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("CAC ≈ $", text,
                      "порог CAC в юнит-экономике демо должен быть в валюте модели ($)")
        self.assertNotIn("CAC ≈ €", text,
                         "евро в долларовой модели демо — чужая валюта (регресс генератора)")


class SixPagerEnSynced(unittest.TestCase):
    """Предупреждение «SIX_PAGER_EN.md отстал от RU» на демо отсутствует — механика:
    чек (check.en_sync_warnings) сравнивает множество тегов RU минус EN и не менялся
    с PRO-29; предупреждение исчезло не ослаблением чека, а состоянием файлов: 10-теговый
    разрыв закрыт ещё на main (PRO-43, коммит e62379c), а [C013], появившийся в RU при
    пересборке демо (круг 1), добавлен в EN в круге 2. Инвариант закреплён тестом."""

    def test_en_six_pager_covers_all_ru_tags(self):
        from tools.pfs import check
        self.assertEqual(check.en_sync_warnings(DEMO), [],
                         "EN-six-pager демо отстал от RU по тегам — чистый клон покажет "
                         "«SIX_PAGER_EN.md отстал от RU»")


if __name__ == "__main__":
    unittest.main()
