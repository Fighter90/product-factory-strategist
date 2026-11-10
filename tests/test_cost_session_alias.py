"""PRO-30: `pfs cost --session <файл>` — алиас --transcript с авто-детектом транскрипта в корне проекта.

Проблема из сессии: транскрипт (ses_*_session.json / *.jsonl) лежит в корне проекта, но cost
не посчитан — «$0.00, сессий 0» в Приложении D. `--session` был только меткой ID для
--transcript; сам по себе транскрипт не записывал. Теперь: --session <путь/часть имени>
записывает сессию (формат детектится сам: OpenCode session.json или Claude Code jsonl),
--session без значения — самый свежий транскрипт в корне проекта (реестровые *.jsonl —
claims/sources/decisions/log — транскриптами не считаются).

Запуск: python3 -m unittest tests.test_cost_session_alias -v
"""
from __future__ import annotations

import contextlib
import json
import os
import tempfile
import time
import unittest
from io import StringIO
from pathlib import Path

TMP = tempfile.mkdtemp(prefix="pfs-test-salias-")
os.environ["PFS_PROJECTS_DIR"] = TMP

from tools.pfs import cli, cost, export, project  # noqa: E402


def _run(argv):
    out, err = StringIO(), StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = cli.main(argv)
    return rc, out.getvalue(), err.getvalue()


def _future_ms(seconds: int = 60) -> int:
    """Сессия чуть позже создания проекта — попадает в окно учёта по умолчанию."""
    return int((time.time() + seconds) * 1000)


def opencode_session(provider="zai-coding-plan", model_id="glm-5.3-flash"):
    created = _future_ms()
    return {
        "info": {"id": "ses_e434df26", "model": {"id": model_id, "providerID": provider},
                 "tokens": {"input": 1000, "output": 500, "reasoning": 200,
                            "cache": {"read": 4000, "write": 0}},
                 "time": {"created": created, "updated": created + 1000}},
        "messages": [{"id": "msg_u", "type": "user", "text": "продолжи"},
                     {"id": "msg_a", "type": "assistant",
                      "model": {"id": model_id, "providerID": provider}, "content": []}],
    }


class SessionAliasTests(unittest.TestCase):
    def setUp(self):
        self.pdir = project.create(f"salias-{id(self)}", "Почему падает удержание?")
        self.slug = self.pdir.name

    def _session_file(self, name: str, data=None, mtime: float | None = None) -> Path:
        f = self.pdir / name
        f.write_text(json.dumps(data or opencode_session()), encoding="utf-8")
        if mtime is not None:
            os.utime(f, (mtime, mtime))
        return f

    def test_session_file_records_from_project_root(self):
        # относительный путь резолвится от каталога проекта; формат OpenCode детектится сам
        self._session_file("ses_x_session.json")
        rc, out, err = _run(["--project", self.slug, "cost", "--session", "ses_x_session.json"])
        self.assertEqual(rc, 0, err)
        self.assertIn("Сессия учтена", out)
        s = cost.summary(self.pdir)
        self.assertEqual(s["sessions"], 1)          # критерий: сессии ≥ 1
        self.assertGreater(s["tokens"], 0)          # критерий: токены > 0
        self.assertEqual(list(s["by_model"]), ["glm-5.3-flash (plan)"])

    def test_bare_session_autodetects_newest_transcript(self):
        old = self._session_file("ses_old_session.json", mtime=time.time() - 500)
        new = self._session_file("ses_new_session.json", mtime=time.time())
        rc, out, err = _run(["--project", self.slug, "cost", "--session"])
        self.assertEqual(rc, 0, err)
        self.assertIn("Сессия учтена", out)
        self.assertIn("ses_new_session", out)       # какой файл взят — видно в выводе
        sessions = cost.summary(self.pdir)["sessions"]
        self.assertEqual(sessions, 1)
        self.assertNotIn(old.name, (self.pdir / "costs.json").read_text(encoding="utf-8"))

    def test_registry_jsonl_not_mistaken_for_transcript(self):
        # реестровые *.jsonl (созданы project.create) — НЕ транскрипты; считаем только chat.jsonl
        chat = self.pdir / "chat.jsonl"
        usage = {"input_tokens": 300, "output_tokens": 100, "cache_read_input_tokens": 0}
        chat.write_text(json.dumps({"message": {"id": "m1", "model": "claude-opus-5-5", "usage": usage}}),
                        encoding="utf-8")
        rc, out, err = _run(["--project", self.slug, "cost", "--session"])
        self.assertEqual(rc, 0, err)
        self.assertIn("Сессия учтена", out)
        self.assertIn("chat.jsonl", out)
        s = cost.summary(self.pdir)
        self.assertEqual(s["sessions"], 1)
        self.assertGreater(s["tokens"], 300)        # input 300 + output 100 (+cache) — не нули из реестра

    def test_hint_matches_partial_name(self):
        self._session_file("ses_z9_session.json")
        rc, out, err = _run(["--project", self.slug, "cost", "--session", "ses_z9"])
        self.assertEqual(rc, 0, err)
        self.assertIn("Сессия учтена", out)
        self.assertEqual(cost.summary(self.pdir)["sessions"], 1)

    def test_ambiguous_hint_errors(self):
        self._session_file("ses_a_session.json")
        self._session_file("ses_a_chat.jsonl")
        rc, out, err = _run(["--project", self.slug, "cost", "--session", "ses_a"])
        self.assertEqual(rc, 2)
        self.assertIn("несколько", err)

    def test_no_transcript_found_errors(self):
        rc, out, err = _run(["--project", self.slug, "cost", "--session"])
        self.assertEqual(rc, 2)
        self.assertIn("не найден", err)

    def test_transcript_plus_session_label_regression(self):
        # прежний смысл --session (метка ID при --transcript) сохранён
        f = Path(TMP) / f"lbl{id(self)}.jsonl"
        f.write_text(json.dumps({"message": {"id": "m1", "model": "claude-opus-5-5",
                                             "usage": {"input_tokens": 100, "output_tokens": 50}}}), encoding="utf-8")
        rc, out, err = _run(["--project", self.slug, "cost", "--transcript", str(f), "--session", "mylabel"])
        self.assertEqual(rc, 0, err)
        data = cost.summary(self.pdir)
        self.assertEqual(data["sessions"], 1)
        self.assertIn("mylabel", (self.pdir / "costs.json").read_text(encoding="utf-8"))

    def test_plain_cost_without_flags_still_prints_summary(self):
        rc, out, err = _run(["--project", self.slug, "cost"])
        self.assertEqual(rc, 0, err)
        self.assertIn("сессий 0", out)

    def test_appendix_d_shows_recorded_session(self):
        # критерий: после записи через алиас Приложение D показывает сессии ≥ 1
        self._session_file("ses_d_session.json")
        _run(["--project", self.slug, "cost", "--session", "ses_d_session.json"])
        text = export.build(self.pdir).read_text(encoding="utf-8")
        self.assertIn("# Приложение D. Прозрачность", text)
        self.assertIn("сессий 1", text)


if __name__ == "__main__":
    unittest.main()
