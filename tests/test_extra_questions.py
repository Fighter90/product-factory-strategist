"""Доп. тесты вопросных блоков (`pfs questions <шаг|id>`) и целостности конфига блоков.

Запуск: python3 -m unittest discover -s tests -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-xq-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, core  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        args = cli.build_parser().parse_args(argv)
        args.f(args)
    return buf.getvalue()


class QuestionsCliTests(unittest.TestCase):
    def test_stage_prints_all_blocks_with_recommendation(self):
        out = run(["questions", "intake"])
        self.assertIn("[intake/intake-decision]", out)
        self.assertIn("Какое решение принимаем по итогам работы?", out)
        self.assertIn("выбор направления развития ←рекомендуется", out)  # recommended: 1
        self.assertIn("Зачем:", out)
        for block_id in ("intake-success", "intake-constraints"):
            self.assertIn(block_id, out)
        self.assertTrue("Задать руководителю: pfs ask" in out or "Ask the lead: pfs ask" in out)  # D6: язык проекта

    def test_block_found_by_id_from_any_stage(self):
        out = run(["questions", "strategy-promise"])
        self.assertIn("[strategy/strategy-promise]", out)
        self.assertIn("Какое ОДНО сообщение должно остаться в голове аудитории?", out)
        self.assertIn("спокойствие/безопасность", out)
        self.assertNotIn("intake-decision", out)  # печатается только запрошенный блок
        with self.assertRaises(PfsError):
            run(["questions", "нет-такого-блока"])

    def test_overview_skips_private_keys(self):
        out = run(["questions"])
        self.assertIn("Вопросные блоки по шагам:", out)
        self.assertIn("intake: intake-decision, intake-success, intake-constraints", out)
        self.assertNotIn("_comment", out)  # служебные ключи конфига не печатаются
        self.assertIn("Подсказка: pfs questions <шаг|id>", out)


class QuestionBlocksConfigTests(unittest.TestCase):
    def test_blocks_are_consistent_and_stages_valid(self):
        blocks = core.read_json(core.CONFIG / "question_blocks.json")
        self.assertTrue(blocks)
        seen_ids = set()
        for stage, items in blocks.items():
            if stage.startswith("_"):
                continue
            self.assertIn(stage, core.STAGE_IDS, stage)  # ключ блока — существующий шаг процесса
            self.assertTrue(items, stage)
            for b in items:
                self.assertTrue(b["id"])
                self.assertNotIn(b["id"], seen_ids)  # id блоков уникальны во всём конфиге
                seen_ids.add(b["id"])
                self.assertTrue(b.get("q", "").strip())
                self.assertGreaterEqual(len(b.get("options", [])), 2)
                rec = b.get("recommended")
                if rec is not None:
                    self.assertTrue(0 <= rec < len(b["options"]), b["id"])

    def test_step_known_block_ids_resolvable(self):
        blocks = core.read_json(core.CONFIG / "question_blocks.json")
        out = run(["questions", "choice"])
        for b in blocks["choice"]:
            self.assertIn(b["id"], out)


class QuestionBlocksEnTests(unittest.TestCase):
    """PRO-132: EN-варианты блоков в служебном ключе _en — покрытие и выбор по lang проекта."""

    def test_en_mirror_covers_all_ru_stages(self):
        blocks = core.read_json(core.CONFIG / "question_blocks.json")
        en = blocks.get("_en")
        self.assertIsInstance(en, dict)
        ru_stages = {k for k in blocks if not k.startswith("_")}
        self.assertEqual(set(en), ru_stages)  # у каждого RU-этапа есть EN-вариант
        for stage, items in en.items():
            self.assertEqual([b["id"] for b in items], [b["id"] for b in blocks[stage]], stage)
            for b in items:
                self.assertTrue(b.get("q", "").strip())
                self.assertGreaterEqual(len(b.get("options", [])), 2)
                rec = b.get("recommended")
                if rec is not None:
                    self.assertTrue(0 <= rec < len(b["options"]), b["id"])

    def test_en_project_prints_en_blocks(self):
        from tools.pfs import project
        project.create("EN questions", "question", slug="en-questions", lang="en")
        self.addCleanup(core.clear_active)
        out = run(["questions", "intake"])
        self.assertIn("[intake/intake-decision]", out)
        self.assertIn("What decision are we making as a result of this work?", out)
        self.assertIn("Why:", out)
        self.assertNotIn("Какое решение принимаем", out)
        self.assertNotIn("Зачем:", out)
        out_sources = run(["questions", "sources"])
        self.assertIn("[sources/sources-allowed]", out_sources)
        self.assertIn("Which materials may be used as sources?", out_sources)


if __name__ == "__main__":
    unittest.main()
