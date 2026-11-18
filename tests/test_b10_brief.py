#!/usr/bin/env python3
"""QA B-10: ответы intake заполняют слоты 00_brief.md; check предупреждает о «?»."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

TMP = tempfile.mkdtemp(prefix="pfs-test-b10-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import check, cli, core, project  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


class BriefFillTests(unittest.TestCase):
    def test_intake_answer_fills_decision_slot(self):
        pdir = project.create("B10 fill", "ATS вопрос", slug="b10-fill")
        run_cli(["ask", "Какое решение принимаем по итогам работы?", "--options", "A,B"])
        run_cli(["answer", "Запуск ATS-скана как модуля продукта"])
        brief = (pdir / "outputs" / "00_brief.md").read_text(encoding="utf-8")
        self.assertIn("| Решение, которое будет принято по результату | Запуск ATS-скана "
                      "как модуля продукта (ответ руководителя, intake) |", brief)
        self.assertIn("| Ограничения (сроки, бюджет, регуляторика, бренд) | ? |", brief)

    def test_constraint_answer_fills_constraints(self):
        pdir = project.create("B10 constraints", "вопрос", slug="b10-cons")
        run_cli(["ask", "Какие жёсткие ограничения?", "--options", "A,B"])
        run_cli(["answer", "Соло-разработчик, локальный режим"])
        brief = (pdir / "outputs" / "00_brief.md").read_text(encoding="utf-8")
        self.assertIn("| Ограничения (сроки, бюджет, регуляторика, бренд) | Соло-разработчик, "
                      "локальный режим (ответ руководителя, intake) |", brief)

    def test_en_brief_filled(self):
        pdir = project.create("B10 en", "question", slug="b10-en", lang="en")
        run_cli(["ask", "What is the decision to be made?", "--options", "A,B"])
        run_cli(["answer", "Launch ATS module"])
        brief = (pdir / "outputs" / "00_brief.md").read_text(encoding="utf-8")
        self.assertIn("| Decision to be made from this work | Launch ATS module (intake answer) |", brief)

    def test_check_warns_open_slots_after_intake(self):
        pdir = project.create("B10 warn", "вопрос", slug="b10-warn")
        run_cli(["step", "intake", "done", "--next", "sources"])
        res = check.run(pdir)
        self.assertTrue(any("00_brief" in w for w in res["warnings"]),
                         str(res["warnings"][:3]))


if __name__ == "__main__":
    unittest.main()
