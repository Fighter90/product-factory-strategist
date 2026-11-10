#!/usr/bin/env bash
# Установка Strategist CLI (pfs) как глобальной команды.
# Приоритет: uv tool install -e (живое обновление из репо) → venv + symlink в ~/.local/bin.
set -euo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || dirname "$0")/.."

if command -v uv >/dev/null 2>&1; then
  echo "→ uv tool install -e . (editable: обновления main подхватываются сами)"
  uv tool install -e . --force
elif command -v python3 >/dev/null 2>&1; then
  echo "→ uv не найден: venv ~/.pfs-venv + symlink"
  python3 -m venv ~/.pfs-venv
  ~/.pfs-venv/bin/pip install --upgrade pip >/dev/null
  ~/.pfs-venv/bin/pip install -e .
  mkdir -p ~/.local/bin
  ln -sf ~/.pfs-venv/bin/pfs ~/.local/bin/pfs
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "⚠ добавьте в PATH: export PATH=\"\$HOME/.local/bin:\$PATH\"";; esac
else
  echo "Нужен uv (https://docs.astral.sh/uv/) или python3." >&2; exit 1
fi
echo ""
pfs --help | head -3
echo "Готово: pfs — глобальная команда. Проекты: <репо>/projects (или env PFS_PROJECTS_DIR)."
