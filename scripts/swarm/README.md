# Swarm — автономный конвейер Linear → Done

Порт конвейера `career-ops/web-ui/scripts/swarm` (ru-README первоисточника) под репозиторий
product-factory-strategist (Python CLI без зависимостей).

## Конвейер

```
Linear PRO (метка `swarm`, state Todo)
  → оркестратор забирает задачу (In Progress + комментарий)
  → EXECUTOR (opencode run, роль roles/executor.md) — изолированный worktree
    .task-board/wt-<id> от свежего origin/main (PRO-81; ветка попытки
    переиспользуется): red-first тест + правка + коммит на ветке swarm/pro-xx —
    общий чекаут остаётся супервизору на detached origin/main
  → TESTER — детерминированные гейты: python3 -m unittest discover -s tests + pfs doctor,
    гоняются в worktree исполнителя (фейл → заметки возвращаются исполнителю, до --rounds раз)
  → REVIEWER (opencode run) — VERDICT: ACCEPT / RETURN (возврат на доработку)
  → DOCUMENTER (opencode run) — CHLOG_FIXED / CHLOG_NOTES / STORY
  → RELEASE MANAGER — ребейз ветки на свежий main (в worktree исполнителя;
    конфликты *.md разрешаются union-merge, обе стороны сохраняются) →
    push --force-with-lease → существующий PR ветки мержится
    (gh pr list --head → gh pr merge), нового PR не создаём при живом →
    squash-merge → версия = max(тегов v*) + patch
    (pyproject синхронизируется, коллизия тега проверяется) →
    запись в CHANGELOG.md (локальная дата) + qa/SWARM-QA-<ID>.md → tag vX.Y.Z →
    push → watch Pages workflow → prod-QA (4 страницы strategyproduct.ru = 200)
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
- две проваленные попытки (gates/review/pipeline-краш) → задача паркуется в Backlog;
  счётчик `.task-board/attempts.json` переживает перезапуски роя, но затухает через 7 дней
  (TTL), а старый формат записей (число без ts) считается истёкшим; успех сбрасывает счётчик
- краш-безопасность (PRO-68): любой выход после claim возвращает задачу в Todo, учёт
  попытки пишется, очередь продолжает движение (cleanup дерева, без rethrow); застрявшая
  In Progress с меткой swarm (клейм в `.task-board/claimed.json` старше `--stuck-min`,
  по умолчанию 30 минут, или без клейма) реqueue'ится в Todo при следующем pick
- работа на detached `origin/main`, ветки `swarm/<identifier>`; конфликт rebase в цикле
  разработки → ветка пересоздаётся на свежем main, конфликт релизного squash → union-
  разрешение *.md в живом ребейзе (невалидный `-X union` при `--squash` убран, PRO-68)
- изоляция исполнителя (PRO-81): для каждой задачи `git worktree add` в gitignored
  `.task-board/wt-<id>` от свежего origin/main (ветка попытки переиспользуется, протухший
  worktree краша сносится до add, knowledge/ кладётся симлинком на общий клон); executor
  пишет, гейты гонятся, ребейз/squash релиза исполняются в worktree (`git -C`/`cwd: WT`) —
  общий чекаут остаётся супервизору (параллельный прогон сюиты больше не гонится с
  пишущим воркером); по завершении (успех/blocked/cancel/review-fail/краш) worktree
  сносится — stash-цепочки «blocked leftovers» не нужны; guard живого воркера (PRO-73)
  признаёт cwd под ROOT, чтобы тик не сорвал ветку живого воркера в его worktree
- reflog-спасение потерянных коммитов исполнителя (уроки run-5/run-6 career-ops)
- guard живого воркера (PRO-73): каждый воркер пишет pid в `.task-board/worker.pid`;
  тик при живом `opencode run` этого репо (pid жив + команда + cwd) завершается
  до лока, pick и detach — свежезапущенный воркер (opencode грузится 10–30 с)
  больше не срывается `git checkout --detach origin/main`;
  pid-файл протухает по mtime через worker-timeout (25 мин) + grace (5 мин):
  run() убивает группу воркера по таймауту, поэтому файл старше границы не может
  описывать живого воркера — сирота погибшего ждущего экземпляра (живость pid
  консервативна: EPERM, переиспользование pid другим opencode этого репо)
  блокирует очередь не навсегда, а на остаток жизни воркера (ревью раунд 4)
- таймаут убивает воркера гарантированно (PRO-69, инцидент 12.11: ревьюер прожил
  83.7 мин при timeoutMs 12 мин — group-kill «прошёл» мимо цели, а прямой kill был
  только в catch-ветке): killTree — снапшот поддерева по ps ДО удара (после смерти
  корня сироты перерождаются на init), затем group-kill + прямой SIGKILL безусловно,
  затем эскалация по живым потомкам с проверкой живости; run() резолвится принудительно
  (finish(-1)) — воркер не живёт дольше timeout + 5 с («тест-пингвин»: sleep 600 при
  timeoutMs 2000 умирает, процесса нет в ps)
- воркер не переживает оркестратор (PRO-69, инциденты 19:0x/19:2x — осиротевшие
  воркеры воевали за дерево): живые воркеры реапятся при любом выходе (exit,
  SIGINT/SIGTERM/SIGHUP), pid-файл хранит pid владельца, и guard следующего тика
  убивает сироту мёртвого владельца тем же killTree, упаковывает хвосты executor'а
  в stash (`orphan worker … leftovers`) и продолжает тик. Ограничение остаётся:
  сирота постобработки не получает — вердикт в Linear не пишется, клейм висит
  In Progress до stuck-requeue (`--stuck-min`)
- фейл на любом шаге → комментарий в задаче; Life-cycle Linear принадлежит оркестратору
- логи: `.task-board/log/cycle-*.log`
