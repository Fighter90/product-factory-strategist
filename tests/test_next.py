"""Тесты pfs next («что решать сейчас»)."""
import os
import tempfile
import unittest
from contextlib import redirect_stdout
import io

TMP = tempfile.mkdtemp(prefix="pfs-test-next-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, decisions, project  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


class NextTests(unittest.TestCase):
    def test_next_basic_and_open_question(self):
        pdir = project.create("Next тест", "Почему падает удержание?", slug="nx")
        out = run_cli(["next"])
        self.assertIn("ЧТО РЕШАТЬ СЕЙЧАС", out)
        self.assertIn("Шаг:", out)
        self.assertIn("Долгов нет", out)
        project.add_open_question(pdir, "Запросить выгрузку оттока у аналитики")
        out2 = run_cli(["next"])
        self.assertIn("Открытые вопросы: 1", out2)
        self.assertIn("выгрузку оттока", out2)

    def test_next_overdue_and_review(self):
        pdir = project.create("Next overdue", "Что делать?", slug="nx2")
        sources = __import__("tools.pfs.sources", fromlist=["sources"])
        c = __import__("tools.pfs.claims", fromlist=["claims"])
        sources.add(pdir, text="данные для решения", title="d")
        cc = c.add(pdir, "Сегмент растёт", "fact", ["S001"])
        decisions.add(pdir, "Фокус", "Пилот", "PM", [cc["id"]],
                      review_date="2026-01-01",
                      commitments=["Запустить пилот|PM|2026-06-01"])
        out = run_cli(["next"])
        self.assertIn("Просроченные обязательства", out)
        self.assertIn("К пересмотру решений", out)


if __name__ == "__main__":
    unittest.main()
