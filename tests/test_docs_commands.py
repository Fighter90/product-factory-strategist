"""PRO-63: автотест документации — команды из README/HELP/INSTALL/AGENTS работают как написано.

Каждый блок кода восьми файлов (README.md, README_EN.md, AGENTS.md, AGENTS_EN.md,
docs/HELP.md, docs/HELP_EN.md, docs/INSTALL.md, docs/INSTALL_EN.md) парсится на команды
`pfs`, нормализуется (шпаргалочные сокращения: `[опции]`, альтернативы `a|b`, несколько
команд в строке, плейсхолдеры `<slug>`/`S###`) и прогоняется в песочнице: PFS_PROJECTS_DIR
с копией демо-проекта, фикстуры-файлы (csv/jsonl/md/png) в рабочем каталоге.

Команда считается сломанной, если она печатает usage-ошибку argparse или Python-Traceback.
Осмысленный отказ `Ошибка: …` (PfsError) — не ошибка теста: документация описывает команды,
а не содержимое папки пользователя (несуществующий `~/Downloads/report.pdf` честно отклоняется).

Пропускаются (с причиной в отчёте): сетевые команды (source fetch/refresh, source add <url>)
и команды, переписывающие файлы репозитория вне песочницы (models use/sync → config/models.json
и .claude/agents, kb index → knowledge/INDEX.md).

Запуск: python3 -m unittest tests.test_docs_commands -v
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SANDBOX = Path(tempfile.mkdtemp(prefix="pfs-test-docs-"))
PROJECTS = SANDBOX / "projects"
WORK = SANDBOX / "work"  # cwd запуска: здесь фикстуры-файлы из примеров документации

DOC_FILES = ["README.md", "README_EN.md", "AGENTS.md", "AGENTS_EN.md",
             "docs/HELP.md", "docs/HELP_EN.md", "docs/INSTALL.md", "docs/INSTALL_EN.md"]

# Сеть и записи в репозиторий вне песочницы — вне зоны ответственности этого теста.
SKIP = {
    ("source", "fetch"): "сеть",
    ("source", "refresh"): "сеть",
    ("models", "use"): "перезаписывает config/models.json репозитория",
    ("models", "sync"): "перезаписывает .claude/agents репозитория",
    ("kb", "index"): "перезаписывает knowledge/INDEX.md репозитория",
}

# Плейсхолдеры документации → рабочие значения песочницы. Порядок важен.
SUBS = [
    (r"<url\|файл>", "док.md"), (r"<url\|file>", "док.md"),
    (r"<файл\.md>", "doc.md"), (r"<file\.md>", "doc.md"),
    (r"<slug>", "демо"), (r"\bslug\b", "демо"),
    (r"<шаг\|блок>", "research"), (r"<step\|block>", "research"),
    (r"<шаг>", "research"), (r"<step>", "research"),
    (r"<задача>", "red_team"), (r"<task>", "red_team"),
    (r"<название>", "Название"), (r"<title>", "Название"),
    (r"<запрос дословно>", "Почему падает удержание?"),
    (r"<запрос>", "Почему падает удержание?"),
    (r"<request verbatim>", "Why is retention falling?"),
    (r"<профиль>", "cursor-mixed"),
    (r"<jsonl>", "session.jsonl"),
    (r"<url>", "https://example.com/doc"),
    (r"S\d{3}|S###", "S001"),
    (r"C\d{3}|C###", "C001"),
    (r"D\d{3}|D###", "D001"),
    (r"…", "тест"),
    (r"<[^<>]+>", "тест"),
]


# ---------- парсер документации: блоки → строки → варианты команд ----------

def _strip_comment(line: str) -> str:
    """Хвостовой комментарий ` # …` вне кавычек."""
    out, q = [], False
    for i, ch in enumerate(line):
        if ch == '"':
            q = not q
        if ch == "#" and not q and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _split_quoted(text: str, sep: str) -> list[str]:
    """Разбивка по sep (например ` | ` или ` / `) вне кавычек."""
    parts, buf, q, i = [], [], False, 0
    while i < len(text):
        if not q and text.startswith(sep, i):
            parts.append("".join(buf))
            buf = []
            i += len(sep)
            continue
        ch = text[i]
        if ch == '"':
            q = not q
        buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return [p.strip() for p in parts if p.strip()]


def _drop_optionals(seg: str) -> str:
    """Удаление `[…]` вне кавычек (шпаргалочная запись необязательных опций)."""
    out, q, depth = [], False, 0
    for ch in seg:
        if depth:
            if ch == "]":
                depth -= 1
            continue
        if ch == '"':
            q = not q
        if ch == "[" and not q:
            depth += 1
            out.append(" ")
            continue
        out.append(ch)
    return "".join(out)


def _tokens(line: str) -> list[str]:
    toks, cur, q = [], "", False
    for ch in line:
        if ch == '"':
            q = not q
            cur += ch
        elif ch.isspace() and not q:
            if cur:
                toks.append(cur)
                cur = ""
        else:
            cur += ch
    if cur:
        toks.append(cur)
    return toks


def _unquoted_pipe(tok: str) -> bool:
    q = False
    for ch in tok:
        if ch == '"':
            q = not q
        elif ch == "|" and not q:
            return True
    return False


def _expand_alternatives(seg: str, cap: int = 8) -> list[str]:
    """`in_progress|done` → оба варианта (альтернативы без кавычек; кап на комбинации)."""
    toks = _tokens(seg)
    groups = [t.split("|") if _unquoted_pipe(t) else [t] for t in toks]
    total = 1
    for g in groups:
        total *= len(g)
    if total > cap:
        groups = [g[:1] for g in groups]
    out = [""]
    for g in groups:
        out = [f"{acc} {alt}".strip() for acc in out for alt in g]
    return out


def _substitute(seg: str) -> str:
    for pat, repl in SUBS:
        seg = re.sub(pat, repl, seg)
    return seg


def _split_multi(chunk: str) -> list[str]:
    """Несколько команд в одной строке: `a | b`, `a / b`. Часть без `pfs` продолжает
    предыдущую: подкоманда (`pfs decision due | list` → `pfs decision list`) или
    аргумент (`pfs impact C003 | S002` → `pfs impact S002`); для простых команд —
    другая команда верхнего уровня (`pfs list / status` → `pfs status`)."""
    parts = _split_quoted(chunk, " | ") if " | " in chunk else _split_quoted(chunk, " / ")
    cmds, base = [], None
    for part in parts:
        toks = _tokens(part)
        bare = toks[0] == "pfs" or (toks[0] == "python3" and len(toks) >= 3
                                    and toks[1] == "-m" and toks[2] == "tools.pfs")
        if bare:
            cmds.append(part)
            cmd = toks[1] if toks[0] == "pfs" and len(toks) > 1 else (toks[3] if len(toks) > 3 else None)
            base = ["pfs"] if (cmd in SIMPLE or not cmd) else ["pfs", cmd]
        elif cmds and base:
            first = _tokens(part)[0] if _tokens(part) else ""
            if len(base) == 1 or (base[1] in SIMPLE and first in TOP_LEVEL):
                cmds.append("pfs " + part)
            else:
                cmds.append(" ".join(base) + " " + part)
    return cmds


TOP_LEVEL = {  # что может стоять сразу после `pfs`
    "new", "use", "list", "status", "step", "ask", "answer", "question", "gap", "source",
    "claim", "check", "review", "impact", "decision", "log", "cost", "kb", "data",
    "interview", "media", "ux", "route", "models", "export", "calc", "docx", "next",
    "questions", "finish", "doctor",
}
# команды без подкоманд: продолжение `a / b` — соседняя команда верхнего уровня
SIMPLE = {"new", "use", "list", "status", "step", "ask", "answer", "question", "check",
          "review", "log", "cost", "next", "questions", "finish", "doctor", "docx", "route"}


def doc_commands(path: Path):
    """(строка, исходник, [argv, …]) для каждой команды `pfs` в блоках кода файла."""
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    ln = 0
    while ln < len(lines):
        raw = lines[ln]
        ln += 1
        if re.match(r"^\s*```", raw):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        line = _strip_comment(raw.strip())
        while line.endswith("\\") and ln < len(lines):  # команда продолжается на следующей строке
            ln += 1
            line = line[:-1].rstrip() + " " + _strip_comment(lines[ln - 1].strip())
        if not (line.startswith("pfs ") or line.startswith("python3 -m tools.pfs")
                or line in ("pfs", "python3 -m tools.pfs")):
            continue
        for chunk in re.split(r" {2,}|\t", line):  # шпаргалка: две команды в одной строке
            chunk = chunk.strip()
            if not chunk:
                continue
            for cmd in _split_multi(chunk):
                cmd = _substitute(cmd)
                cmd = _drop_optionals(cmd)
                argvs = []
                for variant in _expand_alternatives(cmd):
                    toks = [t.strip('"') for t in _tokens(variant)]
                    tail = toks[3:] if toks[0] == "python3" else toks[1:]
                    # тот же интерпретатор, что гоняет тест: на 3.9 argparse не глотает
                    # позиционный аргумент после опций — тест обязан это ловить (PRO-63)
                    argv = [sys.executable, "-m", "tools.pfs"] + tail
                    reason = _skipped(argv)
                    argvs.append((argv, reason))
                argvs = [a for a in argvs if a[1] is None] or \
                        ([(argvs[0][0], argvs[0][1])] if argvs else [])
                if argvs:
                    yield ln, raw.strip(), argvs


def _skipped(argv: list[str]) -> str | None:
    body = argv[3:]  # [python3, -m, tools.pfs, ...]
    if body[:1] in (["fetch"], ["refresh"]):
        return "сеть"
    if body[:1] == ["source"]:
        prev = None
        for t in body[2:]:
            if t.startswith(("http://", "https://")) and prev != "--url":
                return "сеть"
            prev = t
    key = tuple(body[:2])
    if key in SKIP:
        return SKIP[key]
    return None


# ---------- песочница и прогон ----------

PNG_1PX = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d4944415478da63fcffff3f030005fe02fea72d7f530000000049454e44ae426082")

FIXTURES = {
    "events.csv": ("user_id,dt,event,revenue,segment\n"
                   "u1,2025-01-05,visit,0,new\nu1,2025-01-06,signup,0,new\nu1,2025-02-01,pay,120,new\n"
                   "u2,2025-01-20,visit,0,ret\nu2,2025-01-21,signup,0,ret\nu2,2025-03-01,pay,90,ret\n"
                   "u3,2025-02-10,visit,0,new\nu3,2025-02-11,signup,0,new\n"),
    "claims.jsonl": ('{"text": "Дока-тест: рынок 40 млрд", "kind": "hypothesis", "grade": "D"}\n'
                     '{"text": "Дока-тест: люди готовы платить", "kind": "hypothesis", "grade": "D"}\n'),
    "transcript.md": "ИИ-респондент (синтетика): гипотезы про барьеры доверия.\n",
    "interview.md": "Интервью руководителя: выбор варианта B.\n",
    "doc.md": "# Дока-док\n\nТекст для Markdown → Word.\n",
    "f.md": "Выписка из первоисточника для --text-file.\n",
    "док.md": "Выписка: рынок 40 млрд.\n",
    "session.jsonl": "",
    "скрин.png": PNG_1PX,
    "screenshot.png": PNG_1PX,
}


def _prepare_sandbox() -> None:
    PROJECTS.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "projects" / "демо", PROJECTS / "демо")
    (PROJECTS / ".active").write_text("демо\n", encoding="utf-8")
    WORK.mkdir(parents=True, exist_ok=True)
    for name, body in FIXTURES.items():
        p = WORK / name
        if isinstance(body, str):
            p.write_text(body, encoding="utf-8")
        else:
            p.write_bytes(body)


def _run(argv: list[str]) -> subprocess.CompletedProcess:
    env = {"PFS_PROJECTS_DIR": str(PROJECTS), "PYTHONPATH": str(ROOT),
           "PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", ""),
           "LANG": os.environ.get("LANG", "en_US.UTF-8")}
    return subprocess.run(argv, capture_output=True, text=True, timeout=180, cwd=str(WORK), env=env)


_RESULTS: list[tuple[str, int, str, list[str], str]] = []


def _classify(fname: str, ln: int, src: str, argv: list[str], reason: str | None) -> None:
    if reason is not None:
        _RESULTS.append((fname, ln, src, argv, reason))
        return
    res = _run(argv)
    if "Traceback (most recent call last)" in res.stderr:
        _RESULTS.append((fname, ln, src, argv, "traceback:\n" + res.stderr.strip()[-800:]))
    elif re.search(r"(?m)^usage:", res.stderr):
        _RESULTS.append((fname, ln, src, argv, f"usage-ошибка argparse (rc={res.returncode}):\n"
                                               + res.stderr.strip()[-500:]))
    else:
        _RESULTS.append((fname, ln, src, argv, "ok"))


def _run_all() -> list[tuple[str, int, str, list[str], str]]:
    """Один прогон всех уникальных команд; (файл, строка, исходник, argv, статус).

    Повтор команды (встречается в нескольких доках) выполняется один раз.
    """
    if _RESULTS:
        return _RESULTS
    _prepare_sandbox()
    seen: set[tuple] = set()
    for fname in DOC_FILES:
        for ln, src, argvs in doc_commands(ROOT / fname):
            argv, reason = argvs[0]
            key = tuple(argv)
            if key in seen:
                continue
            seen.add(key)
            _classify(fname, ln, src, argv, reason)
    return _RESULTS


class DocsCommandsTests(unittest.TestCase):
    """Команды из документации не падают с usage-ошибкой argparse и без Traceback."""

    @classmethod
    def setUpClass(cls):
        cls.results = _run_all()

    def test_docs_have_commands(self):
        """Санити парсера: документация реально содержит команды, пропусков — меньшинство."""
        self.assertGreater(len(self.results), 80, "парсер не нашёл команды в документации")
        skipped = [r for r in self.results if r[4] != "ok"]
        self.assertLess(len(skipped), len(self.results) / 2, "больше половины команд пропущено")

    def test_no_usage_errors_or_tracebacks(self):
        bad = [(f, ln, src, why) for f, ln, src, argv, why in self.results
               if why.startswith(("traceback", "usage"))]
        report = "\n".join(f"- {f}:{ln} `{src}`\n  {why}" for f, ln, src, why in bad)
        self.assertFalse(bad, f"команды из документации падают ({len(bad)}):\n{report}")

    def test_interview_guide_topic_optional(self):
        """HELP/AGENTS: `--topic` у interview guide необязателен (PRO-63 п.1)."""
        res = _run([sys.executable, "-m", "tools.pfs", "--project", "демо",
                    "interview", "guide", "--persona", "Родитель 7–12"])
        self.assertNotIn("Traceback", res.stderr, res.stderr)
        self.assertEqual(res.returncode, 0, f"rc={res.returncode}: {res.stdout} {res.stderr}")
        self.assertTrue((PROJECTS / "демо" / "interviews" / "synthetic" /
                         "guide_родитель-7-12.md").exists(), "гайд не создан")

    def test_counters_match_reality(self):
        """PRO-63: счётчики в доках («N тестов», «N навыков», «N карт») подставляет
        scripts/update_counters.py; --check выходит с 0, если они актуальны."""
        res = subprocess.run([sys.executable, str(ROOT / "scripts" / "update_counters.py"), "--check"],
                             capture_output=True, text=True, timeout=300, cwd=str(ROOT))
        self.assertEqual(res.returncode, 0, f"счётчики разъехались:\n{res.stdout}\n{res.stderr}")


if __name__ == "__main__":
    unittest.main()
