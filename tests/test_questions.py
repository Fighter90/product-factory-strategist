"""Тесты `pfs questions` (обзор блоков) и route-детализации карт. Запуск: python3 -m unittest discover -s tests -v"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402
from tools.pfs import kb  # noqa: E402


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        args = cli.build_parser().parse_args(argv)
        args.f(args)
    return buf.getvalue()


class QuestionsTests(unittest.TestCase):
    def test_step_prints_blocks_and_hint(self):
        out = run(["questions", "options"])
        self.assertIn("options-criteria", out)
        self.assertIn("Задать руководителю", out)

    def test_no_block_prints_overview(self):
        out = run(["questions"])
        self.assertIn("intake-decision", out)
        self.assertIn("options-criteria", out)
        self.assertIn("pfs questions <шаг|id>", out)

    def test_unknown_block_raises(self):
        with self.assertRaises(PfsError):
            run(["questions", "no-such-block"])


class RouteStageCardsTests(unittest.TestCase):
    def test_route_text_has_stage_cards(self):
        out = run(["route", "тест удержания"])
        self.assertIn("Карты по шагам:", out)
        self.assertIn("intake: M-brief-hypotheses", out)
        stages = [ln.split(":")[0].strip() for ln in out.splitlines() if ln.startswith("  ") and ":" in ln]
        self.assertEqual(stages, list(kb.STAGE_CARDS))

    def test_route_json_untouched(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            args = cli.build_parser().parse_args(["route", "тест удержания", "--json"])
            args.f(args)
        out = buf.getvalue()
        data = json.loads(out)  # вывод остаётся чистым JSON
        self.assertIn("scenario", data)
        self.assertNotIn("Карты по шагам", out)


if __name__ == "__main__":
    unittest.main()
