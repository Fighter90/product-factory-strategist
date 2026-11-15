"""Общий код хуков. Хук никогда не роняет сессию: ошибки пишутся в hook_errors.log."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.pfs import core  # noqa: E402


def read_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def active_pdir():
    try:
        return core.project_dir()
    except core.PfsError:
        return None


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))


def guard(fn):
    try:
        fn()
    except Exception:
        with (ROOT / ".claude" / "hooks" / "hook_errors.log").open("a", encoding="utf-8") as fh:
            fh.write(core.now() + "\n" + traceback.format_exc() + "\n")
    sys.exit(0)
