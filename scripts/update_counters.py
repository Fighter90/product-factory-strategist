#!/usr/bin/env python3
"""Подстановка счётчиков документации при релизе (PRO-63, расширение PRO-65).

Считает фактические числа (автотесты, навыки, карты знаний, субагенты) и
подставляет их вместо устаревших в README.md, README_EN.md, docs/HELP.md,
docs/HELP_EN.md, site/index.html, site/help.html, docs/SUBMISSION.md.
Запуск вручную перед релизом или в release-скрипте:

    python3 scripts/update_counters.py           # обновить файлы
    python3 scripts/update_counters.py --check   # только проверить: 0 — актуально, 1 — разъехалось

Что подставляется:
- число тестов (`python3 -m unittest discover -s tests`) — строки с `unittest discover`
  и «голый» счётчик `tests/ (N)` в таблице структуры репозитория;
- число навыков — каталоги `.claude/skills`: словесные («121 навык», «121 skills in»),
  «голые» `skills/ (N` / `**Структура (N)** / «Навыки (N)» / «Skills (N)»,
  число ПОСЛЕ токена с якорем — SVG «>skills N<» и mermaid «skills: N»,
  трио `data-target="N"` в строке статистики сайта «навыков / субагентов / хуков»;
- число карт знаний — `knowledge/methods/*.md` (RU) и `knowledge/methods_en/*.md` (EN-зеркала),
  рядом с словами «карт/карта» и «EN-зеркал/EN mirrors»;
- число субагентов — `.claude/agents/*.md` (словесные и mermaid «subagents: N»).

Родительный падеж подставляется по правилам русского языка (тест/теста/тестов).
Словоформы перебираются от длинных к коротким и матчатся с границей слова (`\b`):
«навык» не матчит префикс «навыков», иначе дрифт счётчика через класс склонения
(«120 навыков» → 122) портил файл («122 навыкаов») навсегда, а --check после порчи
сообщал OK — преобразование было идемпотентным (PRO-63, ревью круг 3).
Единственное число «тест» тоже в переборе: без него счётчик замирал на значениях,
оканчивающихся на 1 («391 тест» не матчился ни «тестом», ни «теста» на следующем
прогоне), а --check сообщал OK по устаревшему документу (PRO-63, ревью круг 2).
Число ПОСЛЕ токена матчится только с якорем («>»/«:»): «>skills 121<» и «skills: 120»
обновляются, а «product-skills 27» (число группы) не задевается (PRO-65).
stdlib only.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["README.md", "README_EN.md", "docs/HELP.md", "docs/HELP_EN.md",
         "site/index.html", "site/help.html", "docs/SUBMISSION.md"]


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
        "тест": ("тест", "теста", "тестов"),
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
    r"""`\d+` сразу ПЕРЕД lookbehind → value (со словоформой для известных существительных).

    `\b` после словоформы: «навык» не матчится внутри «навыков» — подмена по префиксу
    оставляла хвост («122 навыкаов») и накапливалась при повторных прогонах."""
    pattern = re.compile(r"(?P<n>\d+)(?P<ws>\s+)(?P<word>" + re.escape(lookbehind) + r")\b")
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        word = m.group("word")
        new = ru_form(value, word.split("-", 1)[-1]) if not word.startswith("EN-") else word
        new = ru_form(value, word) if word in ("тестов", "теста", "тест", "навык", "навыка", "навыков",
                                               "карт", "карты", "карта", "субагентов", "субагента") else new
        if m.group("n") != str(value) or new != word:
            changed += 1
        return f"{value}{m.group('ws')}{new}"

    return pattern.sub(repl, text), changed


def sub_bare(text: str, token: str, value: int) -> tuple[str, int]:
    r"""«Голый» счётчик `(N` сразу ПОСЛЕ токена (`tests/`, `skills/`, «Структура») → value.

    Закрывающая часть скобки не трогается: `skills/ (120: base 13 …)` → `skills/ (121: …)`.
    """
    pattern = re.compile(re.escape(token) + r"(\s*)\((\d+)")
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        if m.group(2) != str(value):
            changed += 1
        return f"{token}{m.group(1)}({value}"

    return pattern.sub(repl, text), changed


def sub_after_anchored(text: str, anchor: str, value: int) -> tuple[str, int]:
    r"""Число ПОСЛЕ токена-якоря → value: SVG «>skills 121<», mermaid «skills: 120».

    Якорь («>» или «:») обязателен: без него «product-skills 27» и «Базовые 13»
    (числа групп внутри перечислений) задевались бы как счётчики навыков (PRO-65)."""
    pattern = re.compile(r"(" + re.escape(anchor) + r"\s*)(\d+)")
    changed = 0

    def repl(m: re.Match) -> str:
        nonlocal changed
        if m.group(2) != str(value):
            changed += 1
        return f"{m.group(1)}{value}"

    return pattern.sub(repl, text), changed


def sub_data_targets(text: str, values: dict[str, int]) -> tuple[str, int]:
    """Трио счётчиков сайта: `data-target="N"` в строке статистики
    «навыков / субагентов / хуков» → skills, subagents (хуки не считаются).

    Только эта строка: соседние data-target (шаги, карты, проценты) не трогаются."""
    if not ("навыков / субагентов" in text or "skills / subagents" in text):
        return text, 0
    pattern = re.compile(r'data-target="(\d+)"')
    order = [values.get("skills"), values.get("subagents")]
    state = {"i": 0, "changed": 0}

    def repl(m: re.Match) -> str:
        i = state["i"]
        state["i"] = i + 1
        if i >= len(order):
            return m.group(0)
        new = str(order[i])
        if m.group(1) != new:
            state["changed"] += 1
        return f'data-target="{new}"'

    return pattern.sub(repl, text), state["changed"]


def update_file(path: Path, c: dict, write: bool = True) -> tuple[str, int]:
    """Подстановка счётчиков в один файл. Возвращает (новый текст, число замен).

    write=False — dry-run (режим --check): файл на диске не меняется, результат
    сравнивается в памяти — гейт не должен молча править документы (PRO-63, ревью).
    Тесты подставляются только на строках с `unittest discover`."""
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
                for w in ("тестов", "теста", "тест"):
                    if re.search(r"\d+\s+" + re.escape(w) + r"\b", line):
                        line, n = sub_number(line, w, c["tests"])
                        total += n
                        break
        # Словоформы — от длинных к коротким: с границей слова (\b) порядок страхует от
        # подмены по префиксу («навыков» до «навык», «карты»/«карта» до «карт»).
        for word, val in (("навыков", c["skills"]), ("навыка", c["skills"]), ("навык", c["skills"]),
                          ("субагентов", c["subagents"]), ("субагента", c["subagents"]),
                          ("subagents", c["subagents"]),
                          ("карты", c["cards_ru"]), ("карта", c["cards_ru"]), ("карт", c["cards_ru"]),
                          ("EN-зеркал", c["cards_en"]), ("EN mirrors", c["cards_en"]),
                          ("skills", c["skills"])):
            if re.search(r"\d+\s+" + re.escape(word) + r"\b", line):
                line, n = sub_number(line, word, val)
                total += n
        # «Голые» счётчики структуры: tests/ (N) · skills/ (N… · **Структура (N)** · «Навыки (N)».
        for token, val in (("tests/", c["tests"]), ("skills/", c["skills"]),
                           ("Структура", c["skills"]), ("Навыки", c["skills"]),
                           ("Skills", c["skills"])):
            if re.search(re.escape(token) + r"\s*\(\d+", line):
                line, n = sub_bare(line, token, val)
                total += n
        # Число ПОСЛЕ якоря: SVG «>skills 121<», mermaid «skills: 120» / «subagents: 8».
        for anchor, val in ((">skills", c["skills"]), ("skills:", c["skills"]),
                            ("subagents:", c["subagents"])):
            if re.search(re.escape(anchor) + r"\s*\d+", line):
                line, n = sub_after_anchored(line, anchor, val)
                total += n
        # Трио data-target на строке статистики сайта («навыков / субагентов / хуков»).
        line, n = sub_data_targets(line, {"skills": c["skills"], "subagents": c["subagents"]})
        total += n
        lines[i] = line
    new_text = "".join(lines)
    if write and new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return new_text, total


def main(argv: list[str], root: Path = ROOT) -> int:
    check_only = "--check" in argv
    c = counts()
    print(f"Счётчики: тестов {c['tests']}, навыков {c['skills']}, карт RU {c['cards_ru']} "
          f"+ EN-зеркал {c['cards_en']}, субагентов {c['subagents']}")
    drift = 0
    for name in FILES:
        p = root / name
        old_text = p.read_text(encoding="utf-8")
        # --check — dry-run: ничего не пишем, разъехавшиеся файлы сравниваем в памяти.
        new_text, n = update_file(p, c, write=not check_only)
        if check_only:
            if new_text != old_text:
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
