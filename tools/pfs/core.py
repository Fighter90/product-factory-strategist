"""Пути, состояние проекта и безопасная запись файлов."""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "knowledge"
CONFIG = ROOT / "config"


def projects_dir() -> Path:
    """Папка проектов; переопределяется PFS_PROJECTS_DIR (тесты, другая среда)."""
    return Path(os.environ.get("PFS_PROJECTS_DIR", ROOT / "projects"))


# Шаги рабочего процесса. human=True — агент обязан остановиться и спросить человека.
STAGES: tuple[dict[str, Any], ...] = (
    {"id": "intake", "title": "Постановка задачи", "human": True},
    {"id": "sources", "title": "Сбор материалов", "human": False},
    {"id": "research", "title": "Исследование и проверка гипотез", "human": False},
    {"id": "situation", "title": "Картина ситуации", "human": False},
    {"id": "options", "title": "Варианты и возражения", "human": False},
    {"id": "choice", "title": "Выбор варианта руководителем", "human": True},
    {"id": "strategy", "title": "Продуктовая и коммуникационная стратегия", "human": False},
    {"id": "validation", "title": "План проверки", "human": False},
    {"id": "review", "title": "Контроль качества", "human": False},
    {"id": "decision", "title": "Фиксация решения", "human": True},
    {"id": "monitoring", "title": "Сопровождение решения", "human": False},
)
STAGE_IDS = tuple(s["id"] for s in STAGES)


class PfsError(Exception):
    """Ошибка, понятная пользователю (печатается без трейсбека)."""


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def today() -> str:
    return datetime.now().date().isoformat()


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", text.strip().lower(), flags=re.UNICODE).strip("-")
    return s[:60] or "project"


def atomic_write(path: Path, text: str) -> None:
    """Запись через временный файл: обрыв посреди записи не портит данные."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".tmp-", suffix=path.suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    atomic_write(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def next_id(prefix: str, rows: list[dict]) -> str:
    nums = [int(r["id"][len(prefix):]) for r in rows if str(r.get("id", "")).startswith(prefix)
            and r["id"][len(prefix):].isdigit()]
    return f"{prefix}{(max(nums) + 1) if nums else 1:03d}"


# ---------- проект ----------

def active_slug() -> str | None:
    f = projects_dir() / ".active"
    if f.exists():
        slug = f.read_text(encoding="utf-8").strip()
        return slug or None
    return None


def set_active(slug: str) -> None:
    atomic_write(projects_dir() / ".active", slug + "\n")


def project_dir(slug: str | None = None) -> Path:
    slug = slug or active_slug()
    if not slug:
        raise PfsError("Нет активного проекта. Создайте: pfs new \"<название>\" или выберите: pfs use <slug>")
    p = projects_dir() / slug
    if not (p / "project.json").exists():
        raise PfsError(f"Проект '{slug}' не найден в {projects_dir()}")
    return p


def log(pdir: Path, kind: str, msg: str, **extra: Any) -> dict:
    """Журнал действий: что сделано, каким инструментом, на каком шаге."""
    row = {"ts": now(), "kind": kind, "msg": msg}
    row.update({k: v for k, v in extra.items() if v is not None})
    append_jsonl(pdir / "log.jsonl", row)
    return row
