"""Доп. тесты маршрутизации моделей: optional-задачи, эскалация, профили, субагенты.

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-xmodels-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import core, models, project  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


class ModelsPickTests(unittest.TestCase):
    def test_optional_task_demoted_unless_critical(self):
        r = models.pick("final_review")
        self.assertEqual(r["task"], "strategy")   # optional-задача без critical идёт по стратегии
        self.assertEqual(r["tier"], "deep")
        r_crit = models.pick("final_review", critical=True)
        self.assertEqual(r_crit["task"], "final_review")
        self.assertEqual(r_crit["tier"], "frontier")
        r_econ = models.pick("final_review", economy=True)  # экономия понижает deep→balanced
        self.assertEqual(r_econ["tier"], "balanced")

    def test_profile_unknown_raises_with_list(self):
        with self.assertRaises(PfsError) as cm:
            models.profile(models.load(), "нет-такого-профиля")
        self.assertIn("нет-такого-профиля", str(cm.exception))
        self.assertIn("claude", str(cm.exception))  # в сообщении перечислены доступные профили

    def test_table_lists_tasks_of_active_profile(self):
        t = models.table()
        self.assertIn("Профиль: claude", t)
        self.assertIn("| Задача | Уровень | Модель | Effort | Почему |", t)
        self.assertIn("| route | fast |", t)
        self.assertIn("| red_team | deep |", t)


class EscalateTests(unittest.TestCase):
    def test_escalate_moves_tier_and_logs(self):
        pdir = project.create("Эскалация", "Что делать?", slug="xesc")
        res = models.escalate(pdir, "judge", "спорная оценка по рубрике")
        self.assertEqual(res["tier"], "balanced")
        self.assertEqual(res["task"], "judge")
        self.assertTrue(res["why"].startswith("эскалация"))
        self.assertIn("спорная оценка по рубрике", res["why"])
        log = (pdir / "log.jsonl").read_text(encoding="utf-8")
        self.assertIn("Эскалация judge", log)
        self.assertIn("→", log)

    def test_escalate_at_top_tier_raises(self):
        top = {"task": "final_review", "tier": "frontier", "model": "m", "alias": "a",
               "effort": None, "why": None, "escalate_to": None}
        with mock.patch("tools.pfs.models.pick", return_value=top):
            with self.assertRaises(PfsError) as cm:
                models.escalate(None, "final_review", "выше некуда")
        self.assertIn("максимальный", str(cm.exception))


class ProfilesAndAgentsTests(unittest.TestCase):
    def test_sync_agents_rewrites_only_known_agents_with_model_line(self):
        agents = Path(tempfile.mkdtemp(prefix="pfs-test-xagents-"))
        alias = models.pick("desk_research")["alias"]
        (agents / "researcher.md").write_text("---\nname: researcher\nmodel: old-alias\n---\nТело.", encoding="utf-8")
        (agents / "data-analyst.md").write_text("---\nname: data-analyst\n---\nБез строки model.", encoding="utf-8")
        (agents / "note-taker.md").write_text("---\nname: note-taker\nmodel: что-то\n---\n", encoding="utf-8")
        changed = models.sync_agents(agents)
        self.assertTrue(any(c.startswith("researcher →") for c in changed), changed)
        researcher = (agents / "researcher.md").read_text(encoding="utf-8")
        self.assertIn(f"model: {alias}", researcher)
        self.assertNotIn("old-alias", researcher)
        self.assertNotIn("data-analyst", " ".join(changed))   # нет строки model — не тронут
        self.assertIn("Без строки model.", (agents / "data-analyst.md").read_text(encoding="utf-8"))
        self.assertNotIn("note-taker", " ".join(changed))     # неизвестный субагент не тронут
        self.assertEqual(models.sync_agents(agents), [])      # повтор — идемпотентен

    def test_use_profile_writes_copy_not_repo_config(self):
        cfg_copy = Path(tempfile.mkdtemp(prefix="pfs-test-xcfg-"))
        shutil.copy(core.CONFIG / "models.json", cfg_copy / "models.json")
        repo_before = (core.CONFIG / "models.json").read_text(encoding="utf-8")
        with mock.patch.object(core, "CONFIG", cfg_copy):
            models.use_profile("cursor-mixed")
            saved = json.loads((cfg_copy / "models.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["active_profile"], "cursor-mixed")
            with self.assertRaises(PfsError):
                models.use_profile("нет-такого")  # неизвестный профиль не пишется
            still = json.loads((cfg_copy / "models.json").read_text(encoding="utf-8"))
            self.assertEqual(still["active_profile"], "cursor-mixed")
        self.assertEqual((core.CONFIG / "models.json").read_text(encoding="utf-8"), repo_before)  # репо не тронут


if __name__ == "__main__":
    unittest.main()
