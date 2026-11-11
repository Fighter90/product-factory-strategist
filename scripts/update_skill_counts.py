#!/usr/bin/env python3
"""Счётчики навыков в документах — единое число из .claude/skills (PRO-65).

Обновляет общее число навыков и размеры групп (базовые / product-skills /
личная библиотека / интеграции) в README, HELP, SUBMISSION, COMPLIANCE и
статическом site/help.html. Лендинг (site/index.html, site/en/index.html)
считает числа сам — scripts/build_site.py, запускать отдельно.

Числа, которые паттерн не знает (списки имён), скрипт не трогает: их правит
человек вместе с составом навыков.

Запуск:
    python3 scripts/update_skill_counts.py --check   # показать устаревшие
    python3 scripts/update_skill_counts.py --write   # переписать файлы

Только стандартная библиотека.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".claude" / "skills"

# Канонические группы (PRO-65): базовые по шагам процесса + плагин product-skills.
BASE = [
    "strategist", "intake", "research", "situation", "options", "strategy",
    "validation-plan", "decision-support", "six-pager", "data-analysis",
    "interviews", "ux-review", "deep-research",
]
PRODUCT = [
    "roadmap-okr", "growth-effects", "product-navigator", "auction-monetization",
    "product-bets", "pestle-analysis", "model-validation", "risk-management",
    "product-context-strategy", "traction-modeling", "unit-economics",
    "solution-design", "monetization-models", "mvp-pilot-launch", "growth-frameworks",
    "business-models", "competitor-analysis", "team-org-structure", "market-sizing",
    "analytical-reports", "cannibalization", "product-metrics", "benchmarking",
    "scaling-communication", "growth-drivers", "trend-analysis", "problem-design",
]
INTEGRATIONS = ["sdd", "deck", "premortem"]

# Файлы с числовыми счётчиками (именные списки правятся вручную).
TARGETS = [
    "README.md",
    "README_EN.md",
    "docs/SUBMISSION.md",
    "docs/HELP.md",
    "docs/HELP_EN.md",
    "docs/COMPLIANCE.md",
    "site/help.html",
]


def loaded_skills():
    return sorted(p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md"))


def counts():
    loaded = set(loaded_skills())
    base = len([s for s in BASE if s in loaded])
    product = len([s for s in PRODUCT if s in loaded])
    integr = len([s for s in INTEGRATIONS if s in loaded])
    total = len(loaded)
    personal = total - base - product - integr
    return {"total": total, "base": base, "product": product,
            "personal": personal, "integrations": integr}


def ru_plural(n, one, few, many):
    """Русская форма существительного по числу: 121 навык, 3 интеграции, 100 навыков."""
    n = n % 100
    if 11 <= n <= 14:
        return many
    n %= 10
    if n == 1:
        return one
    if 2 <= n <= 4:
        return few
    return many


def build_rules(c):
    """(regex, replace-функция) для каждого числового счётчика."""
    N, B, P, L, I = c["total"], c["base"], c["product"], c["personal"], c["integrations"]
    rules = []

    def add(pattern, repl):
        rules.append((re.compile(pattern), repl))

    # --- общее число навыков ---
    add(r"(?<![\w.])(\d+) навык(?:а|ов)?(?![\wа-яё])",
        lambda m: f"{N} {ru_plural(N, 'навык', 'навыка', 'навыков')}")
    add(r"(?<![\w.])(\d+) skills(?!\w)", lambda m: f"{N} skills")
    add(r"(skills: )(\d+)", lambda m: f"skills: {N}")
    add(r"(Структура \()(\d+)(\))", lambda m: f"Структура ({N})")
    add(r"(Навыки |Skills )\((\d+)\)", lambda m: f"{m.group(1)}({N})")
    add(r"(\d+)( in total)", lambda m: f"{N} in total")
    add(r"(\| Навыки \| )(\d+)( \|)", lambda m: f"{m.group(1)}{N}{m.group(3)}")
    add(r"(ls \.claude/skills \\?\| wc -l *`? *→ )(\d+)", lambda m: f"{m.group(1)}{N}")
    add(r"(ls \.claude/skills \\?\| wc -l\s+# )(\d+)", lambda m: f"{m.group(1)}{N}")
    add(r"(`\.claude/skills/` \()(\d+)(\))", lambda m: f"{m.group(1)}{N}{m.group(3)}")
    add(r"(\.claude/skills/ +\()(\d+)(\) +базовые )(\d+)"
        r"( · product-skills )(\d+)( · личная )(\d+)( · интеграции )(\d+)",
        lambda m: f"{m.group(1)}{N}{m.group(3)}{B} · product-skills {P} · личная {L} · интеграции {I}")
    add(r"(skills/ \()(\d+)(: base )(\d+)( · product-skills )(\d+)",
        lambda m: f"{m.group(1)}{N}: base {B} · product-skills {P}")
    # README_EN.md: "(121 in total, in three groups…)" — «skills — … (N in total»
    add(r"(skills — packaged instruction sets \()(\d+)( in total)", lambda m: f"{m.group(1)}{N}{m.group(3)}")

    # --- группы: пары «название + число» (с круглыми скобками или без) ---
    def group(name, value):
        add(rf"({name})\((\d+)\)", lambda m: f"{m.group(1)}({value})")
        add(rf"({name})(\d+)(?![\d.)])", lambda m: f"{m.group(1)}{value}")

    group("Базовые", B)
    group("Base", B)
    group("Product-skills", P)
    group("product-skills", P)
    group("Личная библиотека", L)
    group("Personal library", L)
    group("personal library", L)
    group("Интеграции", I)
    group("Integrations", I)

    # HELP.md: «базовые 13 по шагам процесса · 27 product-skills · 75 из личной библиотеки · 6 интеграций»
    add(r"базовые (\d+) по шагам процесса · (\d+) product-skills · (\d+) из личной библиотеки · (\d+) интеграци\w*",
        lambda m: f"базовые {B} по шагам процесса · {P} product-skills · {L} из личной библиотеки · "
                  f"{I} {ru_plural(I, 'интеграция', 'интеграции', 'интеграций')}")
    # README.md (mermaid): «базовые 13 + product-skills 27 + личная 74 + интеграции 6»
    add(r"базовые (\d+) \+ product-skills (\d+) \+ личная (\d+) \+ интеграции (\d+)",
        lambda m: f"базовые {B} + product-skills {P} + личная {L} + интеграции {I}")
    # site/help.html: «личная библиотека ~59» / «a personal library of ~59»
    add(r"(личная библиотека ~)(\d+)", lambda m: f"{m.group(1)}{L}")
    add(r"(personal library of ~)(\d+)", lambda m: f"{m.group(1)}{L}")
    return rules


def _process_text(text, rules):
    """Возвращает (новый текст, список строк «паттерн: ожидалось/было»)."""
    stale = []
    for rx, repl in rules:
        def check(m, repl=repl, rx=rx):
            new = repl(m)
            if new != m.group(0):
                stale.append(f"{rx.pattern!r}: «{m.group(0)}» → «{new}»")
            return new
        text = rx.sub(check, text)
    return text, stale


def stale_findings():
    c = counts()
    rules = build_rules(c)
    findings = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.is_file():
            findings.append(f"{rel}: файл отсутствует")
            continue
        _, stale = _process_text(path.read_text(encoding="utf-8"), rules)
        findings.extend(f"{rel}: {s}" for s in stale)
    return findings


def write_files():
    c = counts()
    rules = build_rules(c)
    changed = []
    for rel in TARGETS:
        path = ROOT / rel
        if not path.is_file():
            continue
        new_text, stale = _process_text(path.read_text(encoding="utf-8"), rules)
        if stale:
            path.write_text(new_text, encoding="utf-8")
            changed.append(rel)
    return changed


def main(argv=None):
    ap = argparse.ArgumentParser(description="Счётчики навыков в документах (PRO-65)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="только показать расхождения")
    g.add_argument("--write", action="store_true", help="переписать файлы")
    args = ap.parse_args(argv)
    c = counts()
    print(f".claude/skills: всего {c['total']} = базовые {c['base']} + product-skills "
          f"{c['product']} + личная {c['personal']} + интеграции {c['integrations']}")
    if args.check:
        findings = stale_findings()
        if findings:
            print(f"Устаревшие счётчики ({len(findings)}):")
            for f in findings:
                print(f"  - {f}")
            return 1
        print("Все известные счётчики актуальны.")
        return 0
    changed = write_files()
    print("Переписано: " + (", ".join(changed) if changed else "ничего (всё актуально)"))
    return 0 if not stale_findings() else 1


if __name__ == "__main__":
    sys.exit(main())
