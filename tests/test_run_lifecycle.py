"""PRO-54: готовность прогона, точки остановки, нумерация 1–12, автопрогон.

- `pfs finish` собирает six-pager RU и EN всегда, без вопроса пользователя
  (EN раньше требовал флаг --en — агент его не звал, six-pager не собирался).
- `pfs next` после завершения шагов процесса — «Процесс завершён…» без автозапуска
  (monitoring — отдельный режим, «продолжи» больше не нужен).
- Нумерация шагов 1–12 в выводе CLI: status (бар и текущий шаг), next, step, list.
- `PFS_AUTOPILOT=1` — режим автопрогона для QA и CI: паузы принимает
  рекомендованный вариант, всё логируется (kind autopilot).

Запуск: python3 -m unittest tests.test_run_lifecycle -v
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

TMP = tempfile.mkdtemp(prefix="pfs-test-lifecycle-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from pathlib import Path  # noqa: E402

from tools.pfs import claims, cli, core, finish, project, sources  # noqa: E402


def run_cli(argv):
    buf = io.StringIO()
    args = cli.build_parser().parse_args(argv)
    with redirect_stdout(buf):
        args.f(args)
    return buf.getvalue()


def make_docs(pdir: Path) -> None:
    """Минимум для строгого затвора pfs finish: 02 и 04 с валидными ссылками (как в test_finish)."""
    out = pdir / "outputs"
    (out / "02_situation.md").write_text(
        "# 02 · Ситуация\n\n## Короткий ответ\n\nРынок 40 млрд [C001].\n\n"
        "## Что известно\n\n- Рынок 40 млрд [C001].\n\n"
        "## Чего мы не знаем\n\n- Доля рынка конкурентов.\n\n"
        "## Вопросы, которые могут изменить решение\n\n- Платёжеспособность сегмента?\n",
        encoding="utf-8")
    (out / "04_product_strategy.md").write_text(
        "# 04 · Стратегия\n\n## Аудитория\n\nСоискатели [C001].\n\n"
        "## Альтернативы\n\n- Вариант A: оставить как есть.\n- Вариант B: семейный пакет.\n"
        "- Вариант C: закрыть направление.\n\n"
        "## Выбранное направление\n\nСемейный пакет [C001].\n\n"
        "## Осознанные отказы\n\n- Не выходим в B2B.\n\n"
        "## Экономика\n\nARPU 350, CAC 600 [C001].\n",
        encoding="utf-8")


class FinishAlwaysBuildsSixPager(unittest.TestCase):
    """Критерий PRO-54: six-pager собирается в finish всегда, без вопроса пользователя."""

    def setUp(self):
        slug = "lc-finish-" + self.id().rsplit(".", 1)[-1][:40]
        self.pdir = project.create("Жизненный цикл", "Почему падает удержание?", slug=slug)
        sources.add(self.pdir, text="Публичный отчёт: рынок 40 млрд", title="Рынок")
        claims.add(self.pdir, "Рынок 40 млрд", "fact", ["S001"], grade="B")
        make_docs(self.pdir)

    def test_default_run_builds_en_six_pager_without_flag(self):
        res = finish.run(self.pdir, no_deck=True)
        names = {p.name for p in res["artifacts"]}
        self.assertIn("SIX_PAGER_EN.md", names)
        self.assertIn("SIX_PAGER_EN.docx", names)
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER_EN.md").exists())
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER_EN.docx").exists())
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER.md").exists())  # RU не пострадала

    def test_no_en_flag_skips_en_version(self):
        res = finish.run(self.pdir, no_deck=True, en=False)
        names = {p.name for p in res["artifacts"]}
        self.assertNotIn("SIX_PAGER_EN.md", names)
        self.assertFalse((self.pdir / "outputs" / "SIX_PAGER_EN.md").exists())

    def test_cli_finish_default_builds_en(self):
        rc = cli.main(["--project", self.pdir.name, "finish", "--no-deck"])
        self.assertEqual(rc, 0)
        self.assertTrue((self.pdir / "outputs" / "SIX_PAGER_EN.md").exists())

    def test_cli_finish_no_en_flag(self):
        rc = cli.main(["--project", self.pdir.name, "finish", "--no-deck", "--no-en"])
        self.assertEqual(rc, 0)
        self.assertFalse((self.pdir / "outputs" / "SIX_PAGER_EN.md").exists())


class NextAfterFinish(unittest.TestCase):
    """PRO-54 п.5: `pfs next` после finish — процесс завершён, без автозапуска."""

    @staticmethod
    def _finish_steps(pdir):
        for sid in project.STAGE_IDS:
            if sid != "monitoring":  # monitoring по определению не закрывается
                project.set_step(pdir, sid, "done")

    def test_next_after_process_done_shows_finished_banner(self):
        pdir = project.create(f"Завершён {id(self)}", "Почему падает удержание?", slug=f"lc-done{id(self)}")
        self._finish_steps(pdir)
        out = run_cli(["next"])
        self.assertIn("Процесс завершён", out)
        self.assertIn("мониторинг, правки, презентация", out)
        self.assertIn("без автозапуска", out)
        self.assertNotIn("Долгов нет", out)  # баннер завершения вместо строки «долгов нет»

    def test_next_before_finish_keeps_usual_text(self):
        pdir = project.create(f"В работе {id(self)}", "Почему падает удержание?", slug=f"lc-wip{id(self)}")
        out = run_cli(["next"])
        self.assertNotIn("Процесс завершён", out)
        self.assertIn("Долгов нет", out)

    def test_next_finished_banner_in_en(self):
        pdir = project.create(f"Done EN {id(self)}", "Why is retention dropping?", slug=f"lc-en{id(self)}", lang="en")
        self._finish_steps(pdir)
        out = run_cli(["next"])
        self.assertIn("Process complete", out)
        self.assertIn("monitoring, edits, presentation", out)


class StepNumbering(unittest.TestCase):
    """PRO-54 п.4: нумерация «Шаг 1/12 … 12/12» в выводе CLI (было «Шаг 0/12» у агента)."""

    def setUp(self):
        self.pdir = project.create(f"Нумерация {id(self)}", "Почему падает удержание?", slug=f"lc-num{id(self)}")

    def test_status_shows_one_based_step(self):
        out = run_cli(["status"])
        self.assertIn("Текущий шаг: 1/12 intake", out)
        self.assertIn("1·intake", out)  # бар шагов с номерами

    def test_next_shows_one_based_step(self):
        out = run_cli(["next"])
        self.assertIn("Шаг: 1/12 intake", out)

    def test_step_marks_with_number(self):
        run_cli(["step", "intake", "done"])  # обычный порядок: intake закрывается раньше sources
        out = run_cli(["step", "sources", "done", "--next", "Составить план исследования"])
        self.assertIn("Шаг 2/12 sources → done", out)
        self.assertIn("Текущий: 3/12 research", out)

    def test_list_shows_numbered_stage(self):
        out = run_cli(["list"])
        self.assertIn("1/12", out)


class AutopilotMode(unittest.TestCase):
    """PRO-54 п.6: PFS_AUTOPILOT=1 — паузы принимает рекомендация, всё логируется."""

    def setUp(self):
        self.pdir = project.create(f"Автопилот {id(self)}", "Почему падает удержание?", slug=f"lc-auto{id(self)}")

    def _log_kinds(self):
        return [e["kind"] for e in core.read_jsonl(self.pdir / "log.jsonl")]

    def test_ask_records_autopilot_pause(self):
        with mock.patch.dict(os.environ, {"PFS_AUTOPILOT": "1"}):
            out = run_cli(["ask", "Какой вариант?", "--options", "A,B"])
        self.assertIn("PFS_AUTOPILOT", out)
        state = project.load_state(self.pdir)
        self.assertTrue(state["awaiting_human"]["autopilot"])
        self.assertIn("autopilot", self._log_kinds())

    def test_answer_logged_as_autopilot(self):
        with mock.patch.dict(os.environ, {"PFS_AUTOPILOT": "1"}):
            run_cli(["ask", "Какой вариант?", "--options", "A,B"])
            run_cli(["answer", "A"])
        self.assertIn("autopilot", self._log_kinds())

    def test_status_shows_autopilot_mode(self):
        with mock.patch.dict(os.environ, {"PFS_AUTOPILOT": "1"}):
            out = run_cli(["status"])
        self.assertIn("автопрогона", out)
        self.assertIn("PFS_AUTOPILOT", out)

    def test_without_env_default_behaviour(self):
        os.environ.pop("PFS_AUTOPILOT", None)
        out = run_cli(["ask", "Какой вариант?", "--options", "A,B"])
        self.assertIn("Вопрос записан", out)
        self.assertNotIn("PFS_AUTOPILOT", out)
        state = project.load_state(self.pdir)
        self.assertFalse(state["awaiting_human"].get("autopilot"))
        self.assertNotIn("autopilot", self._log_kinds())


if __name__ == "__main__":
    unittest.main()
