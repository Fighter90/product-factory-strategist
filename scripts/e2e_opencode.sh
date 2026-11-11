#!/usr/bin/env bash
# Сквозной QA-прогон агента в OpenCode (PRO-64).
#
# Использование:
#   scripts/e2e_opencode.sh <ru|en> <файл-задачи> [--model provider/model] [--no-plan] [--keep]
#   scripts/e2e_opencode.sh <ru|en> <файл-задачи> --from-log <лог.jsonl> --clone <каталог>
#                            (пересобрать отчёт из готового прогона, без запуска opencode)
#
# Что делает: свежий клон репозитория во временный каталог → `opencode run --auto
# --format json` с задачей и суффиксом автопрогона ([PRO-54]: вопросы pfs ask агент
# закрывает сам рекомендованным вариантом, работа идёт до pfs finish, без «продолжи»)
# → разбор лога (tools/pfs/e2e.py) → отчёт qa/E2E-<дата>-<задача>-<lang>.md в исходном
# репозитории (стем задачи в имени обязателен: 6 прогонов за день иначе перезаписали бы
# друг друга). Ворота отчёта: pfs finish, pfs check --strict, сборка six-pager.
# Код выхода 0 = всё зелёное.
# Набор задач: qa/tasks/<задача>-<ru|en>.md (3 задачи × 2 языка). Ручной/ночной запуск:
# команда /pfs-e2e в OpenCode или цикл по файлам задач (см. docs/HELP.md, раздел 8).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
LANG_CODE="${1:-}"; shift || true
[ "$LANG_CODE" = "ru" ] || [ "$LANG_CODE" = "en" ] || { echo "Использование: e2e_opencode.sh <ru|en> <файл-задачи> [флаги]" >&2; exit 2; }
TASK="${1:-}"; shift || true
[ -n "$TASK" ] && [ -f "$TASK" ] || { echo "Второй аргумент — файл задачи (например, qa/tasks/antispam-$LANG_CODE.md)" >&2; exit 2; }
TASK="$(cd "$(dirname "$TASK")" && pwd)/$(basename "$TASK")"

MODEL=""; FROM_LOG=""; CLONE=""; KEEP=0; OUT=""; PLAN_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --model) MODEL="$2"; shift 2 ;;
    --from-log) FROM_LOG="$2"; shift 2 ;;
    --clone) CLONE="$2"; shift 2 ;;
    --no-plan) PLAN_ARGS=(--no-plan); shift ;;
    --keep) KEEP=1; shift ;;
    --out) OUT="$2"; shift 2 ;;
    *) echo "Неизвестный флаг: $1" >&2; exit 2 ;;
  esac
done

# Суффикс автопрогона ([PRO-54]): агент не останавливается перед человеком.
AUTOPILOT_RU="Режим автопрогона QA [PRO-54]: веди задачу до финального пакета (pfs finish) без ожидания человека. На каждом вопросе pfs ask сразу отвечай сам рекомендованным вариантом (pfs answer) с пометкой «автопрогон QA»; выбор варианта и решение фиксируй так же сам. Ничего не запускай в фоновом режиме и не жди «продолжи»."
AUTOPILOT_EN="QA autopilot mode [PRO-54]: take the task to the final package (pfs finish) without waiting for a human. For every pfs ask, immediately answer it yourself with the recommended option (pfs answer) marked as 'QA autopilot'; record the option choice and the decision yourself the same way. Do not run anything in the background and do not wait for 'continue'."

if [ "$LANG_CODE" = "ru" ]; then
  PROMPT="$(cat "$TASK")

---

$AUTOPILOT_RU"
else
  PROMPT="$(cat "$TASK")

---

$AUTOPILOT_EN"
fi

DATE="$(date +%F)"
if [ -n "$OUT" ]; then
  REPORT="$OUT"
else
  # qa/E2E-<дата>-<задача>-<lang>.md — имя считает tools/pfs/e2e.py (default_report)
  REPORT="$(cd "$REPO" && python3 -c "from tools.pfs.e2e import default_report; print(default_report('$TASK', '$LANG_CODE', '$DATE'))")"
fi

if [ -n "$FROM_LOG" ]; then
  [ -f "$FROM_LOG" ] || { echo "--from-log: файл не найден: $FROM_LOG" >&2; exit 2; }
  [ -n "$CLONE" ] && [ -d "$CLONE" ] || { echo "--from-log требует --clone <каталог прогона>" >&2; exit 2; }
  LOG="$FROM_LOG"
  echo "→ отчёт из готового прогона: $LOG"
else
  TMPROOT="$(mktemp -d "${TMPDIR:-/tmp}/pfs-e2e-$LANG_CODE.XXXXXX")"
  CLONE="$TMPROOT/clone"
  LOG="$TMPROOT/e2e-$LANG_CODE.jsonl"
  cleanup() { [ "$KEEP" = 1 ] && echo "→ артефакты прогона сохранены: $TMPROOT" || rm -rf "$TMPROOT"; }
  trap cleanup EXIT
  echo "→ свежий клон: $CLONE"
  git clone -q "$REPO" "$CLONE"
  echo "→ opencode run --auto --format json (это долго: 20–40 мин)"
  RC=0
  ( cd "$CLONE" && opencode run --auto --archived --format json \
      ${MODEL:+"--model" "$MODEL"} --title "e2e-$LANG_CODE" "$PROMPT" \
      >"$LOG" 2>"$TMPROOT/stderr.txt" ) || RC=$?
  [ "$RC" = 0 ] || echo "⚠ opencode run завершился с кодом $RC — отчёт всё равно собирается по логу" >&2
fi

echo "→ разбор лога и ворота (check --strict, six-pager) в клоне"
( cd "$REPO" && python3 -m tools.pfs.e2e "$LOG" --clone "$CLONE" --lang "$LANG_CODE" \
    --task-file "$TASK" --out "$REPORT" ${MODEL:+--model "$MODEL"} "${PLAN_ARGS[@]+"${PLAN_ARGS[@]}"}" )

echo ""
grep -A2 "^## Вердикт" "$REPORT" | tail -1
echo "Отчёт: $REPORT"
grep -q "Прогон дошёл до финального пакета" "$REPORT" && echo "E2E: OK" || { echo "E2E: ворота не пройдены" >&2; exit 1; }
