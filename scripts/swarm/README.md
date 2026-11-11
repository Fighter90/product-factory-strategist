# Swarm — автономный конвейер Linear → Done

Порт конвейера `career-ops/web-ui/scripts/swarm` (ru-README первоисточника) под репозиторий
product-factory-strategist (Python CLI без зависимостей).

## Конвейер

```
Linear PRO (метка `swarm`, state Todo)
  → оркестратор забирает задачу (In Progress + комментарий)
  → EXECUTOR (opencode run, роль roles/executor.md) — red-first тест + правка + коммит на ветке swarm/pro-xx
  → TESTER — детерминированные гейты: python3 -m unittest discover -s tests + pfs doctor
    (фейл → заметки возвращаются исполнителю, до --rounds раз)
  → REVIEWER (opencode run) — VERDICT: ACCEPT / RETURN (возврат на доработку)
  → DOCUMENTER (opencode run) — CHLOG_FIXED / CHLOG_NOTES / STORY
  → RELEASE MANAGER — gh pr create → squash-merge → version patch в pyproject →
    запись в CHANGELOG.md + qa/SWARM-QA-<ID>.md → tag vX.Y.Z → push →
    watch Pages workflow → prod-QA (4 страницы strategyproduct.ru = 200)
  → Linear Done (комментарий с уликами) → ветка удалена
```

Linear-операции детерминированны (GraphQL fetch из node, без LLM-clerk) — надёжнее и дешевле.
Ключ: env `SWARM_LINEAR_KEY` или файл `~/.swarm_linear_key` (в репо не хранится).

## Запуск

```bash
node scripts/swarm/orchestrator.mjs --dry-run          # проверить очередь, ничего не менять
node scripts/swarm/orchestrator.mjs --max 1            # один полный цикл
node scripts/swarm/orchestrator.mjs --max 15           # всю очередь
node scripts/swarm/orchestrator.mjs --no-release       # стоп после ACCEPT + документ
SWARM_PIN_ISSUE=PRO-31 node scripts/swarm/orchestrator.mjs  # прибить конкретную задачу (параллельный запуск)
```

## Подготовка очереди

```bash
python3 scripts/swarm/prep_linear.py   # метка swarm на PRO-26…PRO-40 + Backlog → Todo
```

## Безопасность

- single-instance lock: `.task-board/lock` (эксклюзивное создание)
- грязное дерево (кроме untracked и `projects/.active`) → аборт до выбора задачи
  (auto-stash не используется: он молча уносил бы WIP человека — решение review PRO-64 round 3)
- две проваленные попытки (gates/review) → задача паркуется в Backlog; счётчик
  `.task-board/attempts.json` переживает перезапуски роя, но затухает через 7 дней
  (TTL), а старый формат записей (число без ts) считается истёкшим; успех сбрасывает счётчик
- работа на detached `origin/main`, ветки `swarm/<identifier>`
- reflog-спасение потерянных коммитов исполнителя (уроки run-5/run-6 career-ops)
- фейл на любом шаге → комментарий в задаче; Life-cycle Linear принадлежит оркестратору
- логи: `.task-board/log/cycle-*.log`
