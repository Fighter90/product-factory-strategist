#!/usr/bin/env bash
# Канонический запуск роя ИЗ РЕПОЗИТОРИЯ: перед стартом синхронизирует сам себя
# (fetch + detach на origin/main — файлы scripts/swarm в рабочей копии становятся
# последней версией с main) и запускает оркестратор из репо-пути.
#
# Usage: ./scripts/swarm/run.sh [--max N] [--dry-run] [--no-release] [--rounds N]
# Ключ Linear: env SWARM_LINEAR_KEY или ~/.swarm_linear_key.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# защита: не наступать на работающую очередь (её воркеры пишут в эту же рабочую копию)
if pgrep -f "orchestrator.mjs" >/dev/null 2>&1 || pgrep -f "opencode run.*$(basename '$PWD')" >/dev/null 2>&1; then
  echo "Ошибка: очередь роя уже работает — дождитесь завершения или остановьте её." >&2
  exit 2
fi

git fetch origin -q
git checkout -q --detach origin/main
chmod +x scripts/swarm/run.sh 2>/dev/null || true
exec node scripts/swarm/orchestrator.mjs "$@"
