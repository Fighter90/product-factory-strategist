#!/usr/bin/env python3
"""Подстановка счётчиков документации при релизе (PRO-63).

Считает фактические числа (автотесты, навыки, карты знаний, субагенты) и
подставляет их вместо устаревших в README.md, README_EN.md, docs/HELP.md,
docs/HELP_EN.md. Запуск вручную перед релизом или в release-скрипте:

    python3 scripts/update_counters.py           # обновить файлы
    python3 scripts/update_counters.py --check   # только проверить: 0 — актуально, 1 — разъехалось

Что подставляется:
- число тестов (`python3 -m unittest discover -s tests`) — строки с `unittest discover`;
- число навыков — каталоги `.claude/skills`;
- число карт знаний — `knowledge/methods/*.md` (RU) и `knowledge/methods_en/*.md` (EN-зеркала),
  рядом с словами «карт/карта» и «EN-зеркал/EN mirrors»;
- число субагентов — `.claude/agents/*.md`.

Родительный падеж подставляется по правилам русского языка (тест/теста/тестов).
stdlib only.
"""
from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["README.md", "README_EN.md", "docs/HELP.md", "docs/HELP_EN.md"]


def count_tests() -> int:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    return suite.countTestCases()


def count_dirs(path: Path) -> int:
    return sum(1 for p in path.iterdir() if p.is_dir()) if path.is_dir() else 0


def count_files(path: Path) -> int:
    return len(list(path.glob("*.md"))) if path.is_dir() else 0


def counts() -> dict:
    return {"tests": count_tests(),
            "skills": count_dirs(ROOT / ".claude" / "skills"),
            "cards_ru": count_files(ROOT / "knowledge" / "methods"),
            "cards_en": count_files(ROOT / "knowledge" / "methods_en"),
            "subagents": count_files(ROOT / ".claude" / "agents")}


def ru_plural(n: int, one: str, few: str, many: str) -> str:
    """1 тест / 2–4 теста / 5–20 тестов (с исключениями 11–14)."""
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def ru_form(n: int, base: str) -> str:
    """Словоформа для счётчика: тест(s)/навык(s)/карта(s)/субагент(s) и их косвенные формы."""
    forms = {
        "тестов": ("тест", "теста", "тестов"), "теста": ("тест", "теста", "тестов"),
        "навык": ("навык", "навыка", "навыков"), "навыка": ("навык", "навыка", "навыков"),
        "навыков": ("навык", "навыка", "навыков"),
        "карт": ("карта", "карты", "карт"), "карты": ("карта", "карты", "карт"),
        "карта": ("карта", "карты", "карт"),
        "субагентов": ("субагент", "субагента", "субагентов"),
        "субагента": ("субагент", "субагента", "субагентов"),
    }
    if base in forms:
        return ru_plural(n, *forms[base])
    return base  # неизменяемые («EN-зеркал» и составные) — словоформа не трогается


def sub_number(text: str, lookbehind: str, value: int) -> tuple[str, int]:
    r"""`\d+` сразу ПЕРЕД lookbehind → value (со словоформой для известных существительных)."""
    pattern = re.compile(r"(?P<n>\d+)(?P<ws>\s+)(?P<word>" + re.escape(lookbehind) + r")")
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        word = m.group("word")
        new = ru_form(value, word.split("-", 1)[-1]) if not word.startswith("EN-") else word
        new = ru_form(value, word) if word in ("тестов", "теста", "навык", "навыка", "навыков",
                                               "карт", "карты", "карта", "субагентов", "субагента") else new
        if m.group("n") != str(value) or new != word:
            changed += 1
        return f"{value}{m.group('ws')}{new}"

    return pattern.sub(repl, text), changed


def update_file(path: Path, c: dict) -> int:
    """Возвращает число замен; тесты — только на строках с `unittest discover`."""
    text = path.read_text(encoding="utf-8")
    total = 0
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        orig = line
        if "unittest discover" in line:
            word = "tests" if re.search(r"\d+\s+tests\b", line) else None
            if word:
                line, n = sub_number(line, "tests", c["tests"])
                total += n
            else:
                for w in ("тестов", "теста"):
                    if re.search(r"\d+\s+" + w, line):
                        line, n = sub_number(line, w, c["tests"])
                        total += n
                        break
        for word, val in (("навык", c["skills"]), ("навыка", c["skills"]), ("навыков", c["skills"]),
                          ("карт", c["cards_ru"]), ("карты", c["cards_ru"]), ("карта", c["cards_ru"]),
                          ("EN-зеркал", c["cards_en"]), ("EN mirrors", c["cards_en"]),
                          ("субагентов", c["subagents"]), ("субагента", c["subagents"]),
                          ("subagents", c["subagents"])):
            if re.search(r"\d+\s+" + re.escape(word), line):
                line, n = sub_number(line, word, val)
                total += n
        lines[i] = line
    new_text = "".join(lines)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return total


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    c = counts()
    print(f"Счётчики: тестов {c['tests']}, навыков {c['skills']}, карт RU {c['cards_ru']} "
          f"+ EN-зеркал {c['cards_en']}, субагентов {c['subagents']}")
    drift = 0
    for name in FILES:
        p = ROOT / name
        before = p.read_text(encoding="utf-8")
        n = update_file(p, c)
        after = p.read_text(encoding="utf-8")
        if check_only and after != before:
            drift += 1
            print(f"РАЗЪЕХАЛОСЬ: {name} ({n} замен)")
        elif n:
            print(f"{name}: замен {n}")
    if check_only:
        print("OK — счётчики актуальны" if not drift else f"FAIL — файлов с устаревшими счётчиками: {drift}")
        return 1 if drift else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
