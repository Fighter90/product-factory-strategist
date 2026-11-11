"""Тесты сквозного QA-прогона: разбор лога `opencode run --auto --format json` и отчёт E2E (PRO-64).

Формат событий — как в приёмочных прогонах 2026-11-11: строка JSONL = {type, timestamp, part};
part.type ∈ {step-start, text, tool, step-finish}; токены в step-finish (input/output/reasoning).

Запуск: python3 -m unittest discover -s tests -v
"""
import json
import os
import re
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


def _tool(tool, status, inp, out):
    """part события tool — как в логе opencode."""
    return {"id": "t", "type": "tool", "tool": tool,
            "state": {"status": status, "input": inp, "output": out}}


def _parse_events(parts, timestamps=True):
    """Лог из parts (обёрнутых в конверт события); timestamps=False — без тайстампов."""
    events = [{"type": p["type"].replace("-", "_"),
               **({"timestamp": 1000 * (i + 1)} if timestamps else {}),
               "part": p} for i, p in enumerate(parts)]
    p = Path(TMP) / "case.jsonl"
    p.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    return e2e.parse_log(p)


class ErrorDetectionTests(unittest.TestCase):
    """Ревью PRO-64 (раунд 3): маркеры Ошибка/Error/Traceback — по границе слова и
    только к shell-выводам. Вывод read/grep/sed с текстом «PfsError(…)» (код инструмента)
    — данные, а не ошибка выполнения; иначе «Ошибок инструментов» завышено
    (в budget-app-en 2026-11-11 было 8 вместо 5)."""

    def test_read_with_pfserror_in_output_not_error(self):
        s = _parse_events([_tool("read", "completed",
                                 {"path": "core.py"},
                                 "raise PfsError(f\"Проект '{slug}' не найден\")")])
        self.assertEqual(s["errors"], [])

    def test_grep_output_with_pfserror_not_error(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "grep -n PfsError tools/pfs/core.py"},
                                 "core.py:147: raise PfsError(f\"Проект не найден\")")])
        self.assertEqual(s["errors"], [])

    def test_shell_output_with_word_error_is_error(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "python3 -m tools.pfs status"},
                                 "Ошибка: Проект 'смоук-установки' не найден")])
        self.assertEqual(len(s["errors"]), 1)

    def test_shell_http_error_marker_is_error(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "python3 -m tools.pfs source add https://x"},
                                 "Не удалось загрузить https://x: HTTP Error 429: Too Many Requests")])
        self.assertEqual(len(s["errors"]), 1)

    def test_nonzero_status_is_error_even_without_marker(self):
        s = _parse_events([_tool("edit", "error",
                                 {"filePath": "x.md"}, "")])
        self.assertEqual(len(s["errors"]), 1)
        self.assertEqual(s["errors"][0]["tool"], "edit")


class InvocationDetectionTests(unittest.TestCase):
    """Ревью PRO-64 (раунд 3): finished/asks/answers — по факту вызова pfs в shell-команде
    (сегмент, начинающийся с `python3 -m tools.pfs …`), а не по подстроке в любом вводе:
    cat SKILL.md с текстом «pfs answer» и payload edit'а с «pfs finish» — не вызовы."""

    def setUp(self):
        self.s = e2e.parse_log(LOG)

    def test_finish_via_pipe_is_counted(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "python3 -m tools.pfs finish 2>&1 | tail -15"},
                                 "ok")])
        self.assertTrue(s["finished"])
        self.assertEqual((s["asks"], s["answers"]), (0, 0))

    def test_chained_ask_and_answer_counted_once(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": 'python3 -m tools.pfs ask "В?" --options "A,B" '
                                             '&& python3 -m tools.pfs answer "A"'},
                                 "ok")])
        self.assertEqual((s["asks"], s["answers"]), (1, 1))

    def test_multiline_step_then_ask_counted(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": 'python3 -m tools.pfs step choice in_progress 2>&1 | head -2\n'
                                             'python3 -m tools.pfs ask "Какой вариант?" --options "A,B"'},
                                 "ok")])
        self.assertEqual(s["asks"], 1)
        self.assertFalse(s["finished"])

    def test_cat_doc_with_pfs_answer_not_counted(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "cat .claude/skills/intake/SKILL.md | head -80"},
                                 "… `pfs answer` закрывает вопрос …")])
        self.assertEqual((s["asks"], s["answers"]), (0, 0))

    def test_edit_payload_with_finish_not_counted(self):
        s = _parse_events([_tool("edit", "completed",
                                 {"path": "plan.md",
                                  "newString": "запустить `python3 -m tools.pfs finish` в конце",
                                  "oldString": "старый текст"}, "ok")])
        self.assertFalse(s["finished"])

    def test_old_events_still_detected(self):
        self.assertEqual((self.s["asks"], self.s["answers"]), (1, 1))
        self.assertTrue(self.s["finished"])


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


class LangMixTests(unittest.TestCase):
    """Языковая консистентность реплик (ревью PRO-64): в EN-прогоне финальные
    реплики агента были на русском («квота-fрешmiум») — вердикт был ✅ без пометки.
    Теперь отчёт считает долю букв реплик не на языке прогона и ставит флаг."""

    def test_lang_of_ru_en_neutral(self):
        self.assertEqual(e2e.lang_of("Готово. Итоговый отчёт QA-автопилота: полный цикл пройден."), "ru")
        self.assertEqual(e2e.lang_of("Package built. Final verification of the whole package state."), "en")
        self.assertEqual(e2e.lang_of("`python3 -m tools.pfs finish` -> exit 0"), "en")  # нет букв кириллицы

    def test_lang_mix_foreign_share(self):
        mix = e2e.lang_mix(["Package built, gates are green.", "Package built again.",
                            "Готово. Итоговый отчёт QA-автопилота собран."], "en")
        self.assertEqual(mix["ru"], 1)           # одна русская реплика
        self.assertEqual(mix["en"], 2)
        self.assertGreater(mix["foreign_share"], 0.3)  # русская реплика длиннее → >30% букв
        self.assertTrue(mix["final_foreign"])    # она же — последняя (финальная сводка)

    def test_lang_mix_final_foreign_even_if_rare(self):
        """Финальная сводка на чужом языке — регресс, даже если её мало по буквам."""
        texts = ["Step done and verified carefully by the pilot.",
                 "Another step completed successfully."] * 4 + ["Готово. Итоговый отчёт собран."]
        mix = e2e.lang_mix(texts, "en")
        self.assertLess(mix["foreign_share"], 0.2)
        self.assertTrue(mix["final_foreign"])

    def test_lang_mix_all_own_no_flag_value(self):
        mix = e2e.lang_mix(["Готово, всё собрано.", "Цикл пройден."], "ru")
        self.assertEqual(mix["foreign_share"], 0.0)
        self.assertFalse(mix["final_foreign"])

    def test_lang_mix_empty(self):
        mix = e2e.lang_mix([], "en")
        self.assertEqual(mix["total"], 0)
        self.assertEqual(mix["foreign_share"], 0.0)


class LanguageConsistencyReportTests(unittest.TestCase):
    """Флаг языка в отчёте: сводка показывает расклад, вердикт помечает регресс,
    но зелёные ворота (finish/check/six-pager) остаются зелёными."""

    def setUp(self):
        self.s = e2e.parse_log(LOG)
        # добавляем русскую финальную реплику в EN-прогон — как в реальном budget-app-en
        self.s_en = dict(self.s)
        self.s_en["texts"] = list(self.s["texts"]) + [
            "Готово. Итоговый отчёт QA-автопилота: полный цикл 0→12 пройден, вариант F — квота-фриум."]

    def test_en_run_with_ru_replies_flagged(self):
        md = e2e.render_report(self.s_en, lang="en", task="Paid tier", date="2026-11-11",
                               check_ok=True, check_tail="OK", six_ok=True, six_tail="SIX_PAGER.md")
        self.assertIn("Язык реплик", md)                    # строка в сводке
        self.assertIn("⚠️", md)                             # флаг языковой консистентности
        self.assertIn("ru", md.split("Язык реплик")[1].split("\n")[0])
        self.assertIn("не на языке прогона", md)            # пояснение у вердикта

    def test_en_run_clean_no_warning(self):
        s = dict(self.s)
        s["texts"] = ["Package built. Gates are green.", "Final verification done."]
        md = e2e.render_report(s, lang="en", task="Paid tier", date="2026-11-11",
                               check_ok=True, check_tail="OK", six_ok=True, six_tail="SIX_PAGER.md")
        self.assertIn("Язык реплик", md)
        self.assertNotIn("не на языке прогона", md)

    def test_green_gates_stay_green_with_warning(self):
        """Флаг языка не должен превращать зелёные ворота в ❌: вердикт остаётся ✅."""
        md = e2e.render_report(self.s_en, lang="en", task="Paid tier", date="2026-11-11",
                               check_ok=True, check_tail="OK", six_ok=True, six_tail="SIX_PAGER.md")
        self.assertIn("✅ Прогон дошёл до финального пакета", md)


class NoTimestampLogTests(unittest.TestCase):
    """Ревью PRO-64 (раунд 3): в логе без тайстампов (t0/t1 None) parse_log не должен
    падать с TypeError на int((t1 - t0) or 0) — duration возвращается как None,
    а отчёт печатает «н/д» вместо времени."""

    def test_log_without_timestamps(self):
        s = _parse_events([_tool("shell", "completed",
                                 {"command": "python3 -m tools.pfs finish"}, "ok"),
                           {"id": "p", "type": "step-finish",
                            "tokens": {"input": 10, "output": 5}}],
                          timestamps=False)
        self.assertIsNone(s["duration_ms"])
        self.assertTrue(s["finished"])

    def test_render_report_with_no_duration(self):
        s = e2e.parse_log(LOG)
        s = dict(s, duration_ms=None)
        md = e2e.render_report(s, lang="ru", task="x", date="2026-11-11")
        self.assertIn("н/д", md)


class MojibakeTests(unittest.TestCase):
    """Битая кодировка в текстах репозитория (ревью PRO-64): ни U+FFFD ( replacement char ),
    ни двойной UTF-8 (mojibake кириллицы) в отслеживаемых текстовых файлах быть не должно."""

    MAX_BYTES = 5 * 1024 * 1024
    EXT = (".md", ".py", ".json", ".sh", ".yml", ".yaml", ".txt", ".html", ".css", ".js")

    def _tracked_texts(self):
        import subprocess
        files = subprocess.run(["git", "ls-files"], cwd=str(ROOT), capture_output=True,
                               text=True).stdout.split()
        for f in files:
            if f.endswith(self.EXT):
                yield ROOT / f

    def test_no_replacement_or_double_encoded_chars(self):
        bad = []
        dbl_cyr = re.compile("[\u00d0\u00d1][\u0080-\u00bf\u20ac\u2019]")
        for p in self._tracked_texts():
            if not p.is_file() or p.stat().st_size > self.MAX_BYTES:
                continue
            try:
                txt = p.read_text(encoding="utf-8")
            except UnicodeDecodeError as e:
                bad.append(f"{p.name}: not utf-8 ({e})")
                continue
            if "\ufffd" in txt:
                bad.append(f"{p.name}: U+FFFD replacement char")
            m = dbl_cyr.search(txt)
            if m:
                bad.append(f"{p.name}: double-encoded cyrillic near {txt[max(0, m.start()-20):m.start()+20]!r}")
        self.assertEqual(bad, [])


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
