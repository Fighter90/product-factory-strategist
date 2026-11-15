"""PRO-32: pfs next и stop-хук напоминают про комитет-пакет (six-pager) после review."""
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

TMP = tempfile.mkdtemp(prefix="pfs-test-nxsp-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, core, project  # noqa: E402

SIX_ACTION = ("Собрать комитет-пакет: pfs calc scaffold → pfs calc all → pfs export "
              "--six-pager (spec: knowledge/templates/SIX_PAGER_PROMPT.md)")
HOOKS_DIR = Path(__file__).resolve().parents[1] / ".claude" / "hooks"


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


def mark_through(pdir, last):
    """Отметить шаги done до last включительно."""
    for sid in core.STAGE_IDS[:core.STAGE_IDS.index(last) + 1]:
        project.set_step(pdir, sid, "done")


def run_stop_hook(payload):
    """Запустить .claude/hooks/stop.py как это делает Claude Code (stdin→stdout)."""
    sys.path.insert(0, str(HOOKS_DIR))
    spec = importlib.util.spec_from_file_location("pfs_stop_hook", HOOKS_DIR / "stop.py")
    mod = importlib.util.module_from_spec(spec)
    try:  # guard(main) на уровне модуля: изолируем импортный прогон от теста
        with redirect_stdout(io.StringIO()):
            with patch.object(sys, "stdin", io.StringIO("{}")):
                spec.loader.exec_module(mod)
    except SystemExit:
        pass
    out = io.StringIO()
    with redirect_stdout(out):
        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
            mod.main()
    return out.getvalue()


class NextSixPagerTests(unittest.TestCase):
    def test_monitoring_without_six_pager_is_first_item(self):
        pdir = project.create("Комитет nx", "Что делать?", slug="nxsp-a")
        mark_through(pdir, "monitoring")
        out = run_cli(["next"])
        lines = out.splitlines()
        idx = next(i for i, l in enumerate(lines) if l.startswith("Шаг:"))
        self.assertTrue(lines[idx + 1].endswith(SIX_ACTION), lines[idx + 1])
        self.assertIn("📋", lines[idx + 1])
        self.assertNotIn("Долгов нет", out)

    def test_decision_stage_also_suggests(self):
        pdir = project.create("Комитет dec", "Что делать?", slug="nxsp-b")
        mark_through(pdir, "review")  # review завершён → шаг decision
        self.assertEqual(project.load_state(pdir).get("stage"), "decision")
        out = run_cli(["next"])
        self.assertIn(SIX_ACTION, out)

    def test_six_pager_present_no_suggestion(self):
        pdir = project.create("Комитет sp", "Что делать?", slug="nxsp-c")
        mark_through(pdir, "monitoring")
        (pdir / "outputs" / "SIX_PAGER.md").write_text("# Six-pager\n", encoding="utf-8")
        self.assertNotIn(SIX_ACTION, run_cli(["next"]))

    def test_early_stage_no_suggestion(self):
        project.create("Комитет early", "Что делать?", slug="nxsp-d")
        self.assertNotIn(SIX_ACTION, run_cli(["next"]))


class StopHookSixPagerTests(unittest.TestCase):
    def test_finished_without_six_pager_reminds(self):
        pdir = project.create("Комитет hook", "Что делать?", slug="nxsp-h1")
        mark_through(pdir, "monitoring")
        out = run_stop_hook({"session_id": "t1"})
        self.assertIn("SIX_PAGER", out)
        self.assertIn("pfs export --six-pager", out)

    def test_finished_with_six_pager_silent(self):
        pdir = project.create("Комитет hook2", "Что делать?", slug="nxsp-h2")
        mark_through(pdir, "monitoring")
        (pdir / "outputs" / "SIX_PAGER.md").write_text("# Six-pager\n", encoding="utf-8")
        self.assertEqual(run_stop_hook({"session_id": "t2"}), "")

    def test_unfinished_silent(self):
        project.create("Комитет hook3", "Что делать?", slug="nxsp-h3")
        self.assertEqual(run_stop_hook({"session_id": "t3"}), "")


if __name__ == "__main__":
    unittest.main()
