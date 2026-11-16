"""Автотест документации (PRO-63): каждая команда pfs из README/HELP/INSTALL/AGENTS
(RU и EN) запускается в песочнице на копии демо-проекта.

Критерии из задачи PRO-63:
- ни одна команда из доков не печатает usage-ошибку argparse и Traceback
  (дружелюбная PfsError с подсказкой — не дефект);
- нотация шпаргалки копируема: одна команда на строку, никаких `a | b`-альтернатив
  и `x / y / z` внутри одной строки (методология аудита: разбиение альтернатив,
  удаление [опций], подстановки <slug>→демо, S###→S001).

Сетевые команды и файлы пользователя (~/Downloads) пропускаются.
"""
import csv
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.pfs import export, finish

REPO = Path(__file__).resolve().parents[1]
DOCS = ["README.md", "README_EN.md", "AGENTS.md", "AGENTS_EN.md"] \
       + sorted(glob.glob(str(REPO / "docs" / "HELP*.md"))) \
       + sorted(glob.glob(str(REPO / "docs" / "INSTALL*.md")))

# сетевые команды и файлы пользователя — вне области теста
SKIP = ("~/Downloads", "source add http", "source fetch", "source refresh S",
        "--origin interview", "--origin synthetic", "--origin own")

# файлы-заглушки, на которые ссылаются примеры из доков (создаются в cwd песочницы)
STUB_CSV = [["dt", "user_id", "event", "revenue"],
            ["2026-01-01", "u1", "visit", ""], ["2026-01-02", "u1", "signup", "0"],
            ["2026-01-03", "u1", "pay", "1490"], ["2026-01-02", "u2", "visit", ""]]
STUBS = {
    "events.csv": STUB_CSV,
    "file.csv": STUB_CSV,
    "transcript.md": "Транскрипт ИИ-респондента (пример из документации).\n",
    "doc.md": "Выписка из источника (пример из документации).\n",
    "f.md": "Выписка из источника (пример из документации).\n",
    "скрин.png": "", "screenshot.png": "",  # media add: пустой файл годится для реестра
}


def _extract_commands() -> list[tuple[str, str]]:
    """(файл, строка-команда) из блоков кода документации, по одной команде на строку."""
    out = []
    for f in DOCS:
        text = (REPO / f).read_text(encoding="utf-8")
        for block in re.findall(r"```(?:bash|sh|shell)?\n(.*?)```", text, re.S):
            for line in block.split("\n"):
                s = line.strip()
                if s.startswith("pfs ") or s.startswith("python3 -m tools.pfs "):
                    out.append((f, s))
    return out


def _runnable(line: str) -> str | None:
    """Приводит строку дока к запускаемой команде; None — пропуск (сеть/файлы пользователя).

    Методология аудита PRO-63: разделение «две команды на строке», удаление [опций],
    подстановки <slug>→демо, S###/C###→реальные ID демо-реестра.
    """
    if any(p in line for p in SKIP):
        return None
    line = re.sub(r"\s+#.*$", "", line).strip()
    # альтернативы `pfs claim supersede … | retract …` — берём первую половину
    line = line.split(" | ")[0]
    # [опции] — убрать (методология аудита)
    line = re.sub(r"\[[^\[\]]*\]", "", line)
    # подстановки
    line = (line.replace("<slug>", "демо").replace("S###", "S001").replace("C###", "C001")
                .replace("C069", "C001").replace("S003", "S001")
                .replace("<файл.md>", "outputs/REPORT.md").replace("<file.md>", "outputs/REPORT.md")
                .replace("<шаг|блок>", "strategy").replace("<step|block>", "strategy")
                .replace("<шаг>", "strategy").replace("<step>", "strategy")
                .replace("<N>", "3").replace("<task>", "check").replace("<задача>", "check")
                .replace("<url>", "https://example.com/report").replace("<jsonl>", "x.jsonl")
                .replace("<ISO>", "2026-01-01"))
    line = re.sub(r"\s+", " ", line).strip()
    return line or None


class DocsCommandsTests(unittest.TestCase):
    """Команды из документации работают как написано (PRO-63)."""

    @classmethod
    def setUpClass(cls):
        cls.sandbox = tempfile.mkdtemp(prefix="pfs-docs-commands-")
        pdir = Path(cls.sandbox) / "проекты" / "демо"
        shutil.copytree(REPO / "projects" / "демо", pdir)
        (Path(cls.sandbox) / "проекты" / ".active").write_text("демо", encoding="utf-8")
        for name, rows in STUBS.items():
            p = Path(cls.sandbox) / name
            if name.endswith(".csv"):
                buf = io.StringIO()
                csv.writer(buf).writerows(rows)
                p.write_text(buf.getvalue(), encoding="utf-8")
            else:
                p.write_text(rows if rows else "", encoding="utf-8")
        # код репозитория (не установленный шим): PYTHONPATH → tools/ этого чекаута
        cls.env = dict(os.environ, PFS_PROJECTS_DIR=str(Path(cls.sandbox) / "проекты"),
                       PYTHONPATH=str(REPO))
        cls.exe = [sys.executable, "-m", "tools.pfs"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.sandbox, ignore_errors=True)

    def _run(self, cmd: str):
        # «pfs …» → python3 -m tools.pfs … из кода этого чекаута (шим на PATH может быть
        # установлен из другого каталога и тестировать не этот код)
        if cmd.startswith("pfs "):
            cmd = sys.executable + " -m tools.pfs " + cmd[4:]
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=60, cwd=self.sandbox, env=self.env)

    def _problems(self, r) -> str | None:
        out = (r.stdout or "") + (r.stderr or "")
        if "Traceback (most recent call last)" in out:
            return "Traceback"
        if r.returncode == 2 and ("usage:" in out.lower() or "invalid choice" in out):
            return "usage-error argparse"
        return None

    def test_no_line_holds_two_commands(self):
        """Нотация шпаргалки: одна команда на строку (PRO-63, п.9)."""
        bad = []
        for f, line in _extract_commands():
            body = re.sub(r"\s+#.*$", "", line).strip()
            rest = re.split(r"\s{2,}", body)[1:]
            if any(x.startswith("pfs ") or x.startswith("python3 -m tools.pfs") for x in rest):
                bad.append(f"{f}: {line[:80]}")
        self.assertFalse(bad, "в блоках кода документации по строке должна быть одна команда:\n"
                          + "\n".join(bad))

    def test_no_alternatives_or_slash_notation(self):
        """Нотация: без `a | b`-альтернатив и `x / y / z` внутри команды (PRO-63, п.9)."""
        bad = []
        for f, line in _extract_commands():
            body = re.sub(r"\s+#.*$", "", line).strip()
            if re.search(r"pfs [^#]*\s/\s", body) and "https://" not in body:
                bad.append(f"{f}: {line[:80]}")
            if re.search(r"pfs [^#]*\|\s*(retract|pfs|show|done|list|rebase|escalate)", body):
                bad.append(f"{f}: {line[:80]}")
        self.assertFalse(bad, "альтернативы и слэш-нотация в одной строке некопируемы:\n" + "\n".join(bad))

    def test_every_doc_command_runs_without_usage_error_or_traceback(self):
        """Каждая команда из доков: без usage-ошибки argparse и Traceback (PRO-63)."""
        problems = []
        ran = 0
        for f, line in _extract_commands():
            cmd = _runnable(line)
            if not cmd:
                continue
            r = self._run(cmd)
            ran += 1
            kind = self._problems(r)
            if kind:
                tail = ((r.stdout or "") + (r.stderr or "")).strip().split("\n")
                problems.append(f"{f}: {cmd[:90]}\n    [{kind}] {tail[-1][:140]}")
        self.assertGreater(ran, 80, "извлечено подозрительно мало команд — сломалось извлечение")
        self.assertFalse(problems, f"команд из доков с usage-ошибкой/Traceback: {len(problems)}\n"
                         + "\n".join(problems))

    def test_data_commands_missing_file_is_friendly(self):
        """pfs data * при отсутствии файла — понятная ошибка, не Traceback (PRO-63, п.2)."""
        for sub in ("profile", "cohort", "funnel", "stats"):
            if sub == "stats":
                cmd = "pfs data stats нет-такого-файла.csv --col revenue"
            elif sub == "cohort":
                cmd = "pfs data cohort нет-такого-файла.csv --user id --date dt"
            elif sub == "funnel":
                cmd = "pfs data funnel нет-такого-файла.csv --steps visit,pay --user id"
            else:
                cmd = "pfs data profile нет-такого-файла.csv"
            r = self._run(cmd)
            out = (r.stdout or "") + (r.stderr or "")
            self.assertNotIn("Traceback", out, f"{sub}: Traceback на отсутствующем файле")
            self.assertNotIn("usage:", out.lower(), f"{sub}: usage-ошибка на отсутствующем файле")
            self.assertIn("не найден", out.lower(), f"{sub}: нет понятного сообщения об ошибке")

    def test_interview_guide_without_topic(self):
        """pfs interview guide без --topic работает (--topic необязателен, PRO-63, п.1)."""
        r = self._run('pfs interview guide --persona "Родитель 7–12"')
        out = (r.stdout or "") + (r.stderr or "")
        self.assertNotIn("укажите тему", out, "guide требует --topic, хотя в доках он необязательный")
        self.assertIn("Гайд", out)

    # ---------- п.3: свежесть экспорта на чистом клоне (критерий готовности) ----------
    def test_demo_committed_export_state_has_no_stale_warnings(self):
        """Закоммиченное состояние экспорта демо: сравнение по содержимому, не по mtime —
        иначе на свежем клоне (mtime = время checkout) ложное «Реестр изменился» (PRO-63, п.3)."""
        self.assertEqual(export.freshness_warnings(REPO / "projects" / "демо"), [],
                         "в репозитории закоммичено состояние экспорта, которое даёт ложное "
                         "предупреждение на чистом клоне")

    def test_demo_finish_on_fresh_copy_has_no_registry_changed(self):
        """Критерий готовности: на чистом клоне pfs finish по демо без «Реестр изменился»."""
        copy = Path(tempfile.mkdtemp(prefix="pfs-democopy-")) / "демо"
        shutil.copytree(REPO / "projects" / "демо", copy)
        res = finish.run(copy, no_deck=True)
        summary = finish.summary_text(res)
        self.assertNotIn("Реестр изменился", summary, summary)
        self.assertNotIn("Пересоберите", summary)


if __name__ == "__main__":
    unittest.main()
