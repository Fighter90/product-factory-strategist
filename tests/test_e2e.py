"""Тесты сквозного QA-прогона: разбор лога `opencode run --auto --format json` и отчёт E2E (PRO-64).

Формат событий — как в приёмочных прогонах 2026-11-11: строка JSONL = {type, timestamp, part};
part.type ∈ {step-start, text, tool, step-finish}; токены в step-finish (input/output/reasoning).

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-e2e-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import e2e  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def ev(ts, part):
    return {"type": part["type"].replace("-", "_"), "timestamp": ts,
            "sessionID": "ses_x", "part": part}


# Синтетический лог: 2 шага, 4 инструмента, вопрос+автоответ, 1 ошибка edit, pfs finish.
EVENTS = [
    ev(1_000, {"id": "p1", "type": "step-start"}),
    ev(2_000, {"id": "p2", "type": "text", "text": "Начинаю автопрогон QA."}),
    ev(3_000, {"id": "p3", "type": "tool", "tool": "shell",
               "state": {"status": "completed",
                         "input": {"command": 'python3 -m tools.pfs new "Спам" "Запрос"'},
                         "output": "Проект создан"}}),
    ev(4_000, {"id": "p4", "type": "tool", "tool": "shell",
               "state": {"status": "completed",
                         "input": {"command": 'python3 -m tools.pfs ask "Какой вариант?" --options "A,B"'},
                         "output": "Вопрос записан"}}),
    ev(5_000, {"id": "p5", "type": "tool", "tool": "shell",
               "state": {"status": "completed",
                         "input": {"command": 'python3 -m tools.pfs answer "A — автопрогон QA"'},
                         "output": "ok"}}),
    ev(6_000, {"id": "p6", "type": "tool", "tool": "edit",
               "state": {"status": "error", "input": {"filePath": "x.md"},
                         "output": "Error: no such file"}}),
    ev(7_000, {"id": "p7", "type": "step-finish",
               "tokens": {"input": 1000, "output": 100, "reasoning": 50, "cache": {"read": 10}}}),
    ev(8_000, {"id": "p8", "type": "step-finish",
               "tokens": {"input": 500, "output": 20, "reasoning": 0}}),
    ev(9_000, {"id": "p9", "type": "tool", "tool": "shell",
               "state": {"status": "completed",
                         "input": {"command": "python3 -m tools.pfs finish"},
                         "output": "Собран финальный пакет"}}),
]
# не-JSON строка в середине — разбор не должен падать
LOG_TEXT = "not-json-at-all\n" + "\n".join(json.dumps(e) for e in EVENTS) + "\n"
LOG = Path(TMP) / "run.jsonl"
LOG.write_text(LOG_TEXT, encoding="utf-8")


class ParseLogTests(unittest.TestCase):
    def setUp(self):
        self.s = e2e.parse_log(LOG)

    def test_steps_tokens_duration(self):
        self.assertEqual(self.s["steps"], 2)
        self.assertEqual(self.s["tokens_in"], 1500)
        self.assertEqual(self.s["tokens_out"], 170)  # (100+50) + 20
        self.assertEqual(self.s["duration_ms"], 8000)
        self.assertEqual(len(self.s["texts"]), 1)

    def test_tools_and_stops(self):
        self.assertEqual(self.s["tools"], {"shell": 4, "edit": 1})
        self.assertEqual(self.s["asks"], 1)
        self.assertEqual(self.s["answers"], 1)
        self.assertTrue(self.s["finished"])

    def test_error_captured(self):
        self.assertEqual(len(self.s["errors"]), 1)
        self.assertEqual(self.s["errors"][0]["tool"], "edit")
        self.assertIn("no such file", self.s["errors"][0]["out"])

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            e2e.parse_log(Path(TMP) / "nope.jsonl")


class RenderReportTests(unittest.TestCase):
    def setUp(self):
        self.s = e2e.parse_log(LOG)
        self.md = e2e.render_report(
            self.s, lang="ru", task="отток антиспам-услуги",
            date="2026-11-11", model="glm-5.3-flash", plan=True,
            check_ok=True, check_tail="Ошибок: 0", six_ok=True, six_tail="SIX_PAGER.md")

    def test_header_and_summary(self):
        self.assertIn("2026-11-11", self.md.splitlines()[0])
        self.assertIn("(RU)", self.md.splitlines()[0])
        self.assertIn("1 500", self.md)          # токены вход, с разрядами
        self.assertIn("170", self.md)            # токены выход
        self.assertIn("отток антиспам-услуги", self.md)
        self.assertIn("0,1 мин", self.md)        # 8000 мс = 0,13 мин → округление до 0,1 (запятая)
        self.assertIn("$0.00", self.md)          # подписка: план, $0
        self.assertIn("glm-5.3-flash", self.md)

    def test_stops_and_finish(self):
        self.assertIn("Остановки", self.md)
        self.assertIn("| 1 |", self.md)          # pfs ask: 1
        self.assertTrue(self.s["finished"])

    def test_gates_and_verdict(self):
        self.assertIn("check --strict", self.md)
        self.assertIn("six-pager", self.md)
        self.assertIn("✅", self.md)             # все ворота зелёные → зелёный вердикт

    def test_failing_gates_marked(self):
        md = e2e.render_report(e2e.parse_log(LOG), lang="en", task="x", date="2026-11-11",
                               check_ok=False, check_tail="boom", six_ok=True, six_tail="")
        self.assertIn("(EN)", md.splitlines()[0])
        self.assertIn("❌", md)


class TaskFilesTests(unittest.TestCase):
    """Набор из 3 новых задач на открытых данных, RU и EN (PRO-64, п.2)."""

    TASKS = ("antispam", "budget-app", "price-increase")

    def test_three_tasks_two_langs(self):
        for stem in self.TASKS:
            for lang in ("ru", "en"):
                p = ROOT / "qa" / "tasks" / f"{stem}-{lang}.md"
                self.assertTrue(p.is_file(), f"нет файла задач: {p.name}")
                self.assertGreater(len(p.read_text(encoding="utf-8").strip()), 40, p.name)


class ReportNamingTests(unittest.TestCase):
    """Имя отчёта с задачей: 6 прогонов матрицы не перезаписывают друг друга (ревью PRO-64).

    Без стема задачи отчёты qa/E2E-<дата>-<lang>.md коллизируют: budget-app-ru
    перезаписал бы отчёт antispam-ru того же дня.
    """

    def test_task_stem_from_path(self):
        self.assertEqual(e2e.task_stem("qa/tasks/antispam-ru.md"), "antispam-ru")
        self.assertEqual(e2e.task_stem(Path("/tmp/x/price-increase-en.md")), "price-increase-en")

    def test_default_report_task_qualified(self):
        p = e2e.default_report(Path("qa/tasks/antispam-ru.md"), "ru", date="2026-11-11")
        self.assertEqual(p.name, "E2E-2026-11-11-antispam-ru.md")

    def test_default_report_appends_lang_if_missing(self):
        p = e2e.default_report(Path("qa/tasks/custom.md"), "en", date="2026-11-11")
        self.assertEqual(p.name, "E2E-2026-11-11-custom-en.md")

    def test_six_matrix_names_unique(self):
        names = {e2e.default_report(Path(f"qa/tasks/{t}-{l}.md"), l, date="2026-11-11").name
                 for t in self.TASKS_ALL for l in ("ru", "en")}
        self.assertEqual(len(names), 6)

    TASKS_ALL = ("antispam", "budget-app", "price-increase")


class CommandFilesTests(unittest.TestCase):
    """Команды OpenCode: frontmatter должен быть открыт и закрыт (---) — иначе он не
    парсится и утекает в промпт команды (ревью PRO-64, pfs-e2e.md)."""

    def test_frontmatter_opened_and_closed(self):
        cmds = sorted((ROOT / ".opencode" / "command").glob("*.md"))
        self.assertGreaterEqual(len(cmds), 4)
        for p in cmds:
            lines = p.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0].strip(), "---", f"{p.name}: нет открывающего ---")
            self.assertTrue(any(l.strip() == "---" for l in lines[1:]),
                            f"{p.name}: нет закрывающего ---")
            self.assertIn("agent:", "\n".join(lines[:5]), f"{p.name}: нет agent: во frontmatter")


if __name__ == "__main__":
    unittest.main()
