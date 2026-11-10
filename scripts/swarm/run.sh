#!/usr/bin/env bash
# Канонический запуск роя ИЗ РЕПОЗИТОРИЯ: перед стартом синхронизирует сам себя
# (fetch + detach на origin/main — файлы scripts/swarm в рабочей копии становятся
# последней версией с main) и запускает оркестратор из репо-пути.
#
# Usage: ./scripts/swarm/run.sh [--max N] [--dry-run] [--no-release] [--rounds N]
# Ключ Linear: env SWARM_LINEAR_KEY или ~/.swarm_linear_key.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# защита: лок этого репо = очередь уже работает (pgrep ловил чужие оркестраторы — убран)
if [ -e .task-board/lock ]; then
  echo "Ошибка: .task-board/lock существует — очередь этого репо работает (или залип после kill: удалите файл)." >&2
  exit 2
fi

git fetch origin -q
git checkout -q --detach origin/main
chmod +x scripts/swarm/run.sh 2>/dev/null || true
exec node scripts/swarm/orchestrator.mjs "$@"
