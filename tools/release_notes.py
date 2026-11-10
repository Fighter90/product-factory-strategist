#!/usr/bin/env python3
"""Release-заметки из CHANGELOG.md (PRO-45).

Зачем: на push тега v* воркфлоу .github/workflows/release.yml создаёт объект
GitHub Release с секцией этой версии из CHANGELOG.md; 13 тегов v1.2.1–v1.2.13
были без Release — ручной прогон (workflow_dispatch) делает идемпотентный бэкфилл
по всем локальным тегам v*.

Зависимости — только stdlib; сеть и `gh` используются только в реальном режиме
`--backfill` (без `--dry-run`), поэтому логика полностью покрывается тестами.

Использование:
    python3 tools/release_notes.py v1.2.13            # секция версии на stdout
    python3 tools/release_notes.py --backfill --dry-run
    python3 tools/release_notes.py --backfill          # gh release create по всем тегам
    python3 tools/release_notes.py --changelog PATH v1.2.13
    python3 tools/release_notes.py --changelog PATH --backfill [--dry-run]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG_PATH = os.path.join(ROOT, "CHANGELOG.md")

# Заголовок секции: «## 1.2.13 — дата · название» или «## v1.2.13 — …».
_HEADING_RE = re.compile(r"^##\s+(v?\d+(?:\.\d+)*)\s*(?:[-—].*)?$")
_VERSION_RE = re.compile(r"^v?(\d+(?:\.\d+)*)$")
# ANSI-мусор, попавший в CHANGELOG (в т.ч. огрызки вида «[0m» без ESC).
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\[\d+m")


def normalize_tag(tag):
    """v1.2.13 -> 1.2.13; некорректный тег — без изменений."""
    tag = (tag or "").strip()
    return tag[1:] if tag.startswith("v") and _VERSION_RE.match(tag) else tag


def parse_version(tag):
    """'v1.2.13' -> (1, 2, 13); не версия (vnext, main) -> None."""
    m = _VERSION_RE.match((tag or "").strip())
    return tuple(int(x) for x in m.group(1).split(".")) if m else None


def _clean(text):
    return _ANSI_RE.sub("", text)


def extract_section(changelog_text, version):
    """Секция версии из текста CHANGELOG (от заголовка до следующего «## »).

    Первое вхождение (в CHANGELOG бывают дубли заголовков). ANSI-мусор
    вычищается. Секции нет -> None.
    """
    version = normalize_tag(version)
    lines = changelog_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        m = _HEADING_RE.match(line)
        if m and normalize_tag(m.group(1)) == version:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return _clean("\n".join(lines[start:end])).strip()


def section_for_tag(changelog_text, tag):
    return extract_section(changelog_text, tag)


def fallback_notes(tag):
    """Описание для версий без секции в CHANGELOG (например, v1.2.8)."""
    return (
        "# Release %s\n\n"
        "Отдельной секции для этой версии в CHANGELOG.md нет — изменения этой "
        "версии описаны в соседних секциях. Полный список изменений: "
        "[CHANGELOG.md](https://github.com/"
        "%s/blob/main/CHANGELOG.md)."
        % (tag, _gh_repo_slug())
    )


def _gh_repo_slug():
    """owner/repo из git remote origin (для ссылки в fallback-тексте)."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "OWNER/REPO"
    m = re.search(r"[:/]([^/:]+/[^/:]+?)(?:\.git)?$", url)
    return m.group(1) if m else "OWNER/REPO"


def sorted_version_tags(tags):
    """Теги-версии v* в порядке возрастания (числово, а не лексикографически)."""
    pairs = [(parse_version(t), t) for t in tags]
    return [t for v, t in sorted((p for p in pairs if p[0] is not None),
                                 key=lambda p: p[0])]


def list_git_tags():
    out = subprocess.run(["git", "tag"], cwd=ROOT,
                         capture_output=True, text=True, timeout=30)
    return [t for t in out.stdout.split() if t]


def release_exists(tag):
    out = subprocess.run(["gh", "release", "view", tag], cwd=ROOT,
                         capture_output=True, text=True, timeout=60)
    return out.returncode == 0


def backfill_plan(tags, changelog_text, existing_releases=()):
    """План бэкфилда: [(tag, notes, from_changelog)] без существующих Release.

    existing_releases передаётся снаружи (в реальном режиме — через `gh release
    view`), поэтому функция чистая и тестируется без сети.
    """
    plan = []
    for tag in sorted_version_tags(tags):
        if tag in existing_releases:
            continue
        notes = section_for_tag(changelog_text, tag)
        plan.append({
            "tag": tag,
            "notes": notes if notes else fallback_notes(tag),
            "from_changelog": notes is not None,
        })
    return plan


def create_release(tag, notes):
    """gh release create с заметками из временного файла."""
    fd, path = tempfile.mkstemp(prefix="pfs-release-", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(notes + "\n")
        return subprocess.run(
            ["gh", "release", "create", tag,
             "--title", tag, "--notes-file", path, "--verify-tag"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
    finally:
        if os.path.exists(path):
            os.remove(path)


def cmd_backfill(dry_run, changelog_path=CHANGELOG_PATH, tags=None):
    """Идемпотентный бэкфилл Releases по тегам-версиям.

    changelog_path — путь к CHANGELOG (проксируется из CLI-опции --changelog,
    чтобы бэкфилл не молча игнорировал её); tags — инъекция списка тегов
    (по умолчанию `git tag` репозитория), чтобы логику можно было проверить
    на чекауте без тегов.
    """
    if not os.path.exists(changelog_path):
        print("ошибка: %s не найден" % changelog_path, file=sys.stderr)
        return 1
    with open(changelog_path, encoding="utf-8") as f:
        changelog = f.read()
    plan = backfill_plan(tags if tags is not None else list_git_tags(), changelog)
    if not plan:
        print("бэкфилл не нужен: Releases уже созданы для всех тегов-версий")
        return 0
    failures = 0
    for item in plan:
        tag = item["tag"]
        if dry_run:
            src = "секция CHANGELOG" if item["from_changelog"] else "fallback (секции нет)"
            print("DRY-RUN: создам Release %s (%s)" % (tag, src))
            continue
        if release_exists(tag):
            print("skip: Release %s уже существует" % tag)
            continue
        out = create_release(tag, item["notes"])
        if out.returncode == 0:
            print("создан Release %s" % tag)
        else:
            failures += 1
            print("ошибка: Release %s не создан: %s"
                  % (tag, (out.stderr or "").strip()), file=sys.stderr)
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Release-заметки из CHANGELOG.md и бэкфилл GitHub Releases (PRO-45)")
    ap.add_argument("tag", nargs="?", help="тег версии, например v1.2.13")
    ap.add_argument("--changelog", default=CHANGELOG_PATH,
                    help="путь к CHANGELOG.md (по умолчанию — в корне репозитория)")
    ap.add_argument("--backfill", action="store_true",
                    help="создать Releases для всех локальных тегов v* (идемпотентно)")
    ap.add_argument("--dry-run", action="store_true",
                    help="показать план бэкфилда, ничего не создавать")
    args = ap.parse_args(argv)
    if args.backfill:
        return cmd_backfill(args.dry_run, changelog_path=args.changelog)
    if not args.tag:
        ap.error("укажите тег, например v1.2.13, или --backfill")
    if args.dry_run:
        ap.error("--dry-run используется только вместе с --backfill")
    if not os.path.exists(args.changelog):
        print("ошибка: %s не найден" % args.changelog, file=sys.stderr)
        return 1
    with open(args.changelog, encoding="utf-8") as f:
        notes = section_for_tag(f.read(), args.tag)
    if notes is None:
        print(fallback_notes(normalize_tag(args.tag)))
        print("warn: секции %s в CHANGELOG нет — выдан fallback-текст"
              % normalize_tag(args.tag), file=sys.stderr)
        return 0
    print(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
