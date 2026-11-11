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

# незакоммиченные хвосты убитых executor'ов (timeout-kill / SIGTERM) упаковываем
# в stash — восстановимо. ДО checkout: грязные tracked-файлы ломают сам
# переключение («локальные изменения будут перезаписаны»), а оркестратор по
# решению ревью (round 3 PRO-64) отказывается работать на грязном дереве.
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard | head -1)" ]; then
  git stash push --include-untracked -q -m "run.sh: auto-stash leftovers before orchestrator start" || true
  echo "run.sh: грязное дерево упаковано в stash (git stash list — восстановление)" >&2
fi

git fetch origin -q
git checkout -q --detach origin/main
chmod +x scripts/swarm/run.sh 2>/dev/null || true

exec node scripts/swarm/orchestrator.mjs "$@"
