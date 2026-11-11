# Swarm QA — PRO-64 (сквозной прогон в OpenCode RU/EN и сравнение с обычным чатом)

Story: юнит-тесты зелёные, но регрессии реального прогона ловились только руками. Рой собрал
приёмочный контур: разбор лога `opencode run --auto --format json` и отчёт E2E — `tools/pfs/e2e.py`
(regress-тест `tests/test_e2e.py`, red-first), раннер `scripts/e2e_opencode.sh` (свежий клон →
автопрогон [PRO-54] → ворота `pfs finish` + `check --strict` + six-pager →
`qa/E2E-<дата>-<задача>-<lang>.md`),
набор 3 новых задач × RU/EN в `qa/tasks/`, команда `/pfs-e2e` и раздел в `docs/HELP.md`/`HELP_EN.md`,
сравнение с обычным чатом по методике/рубрике с честными ограничениями — `docs/demo/comparison.md`
(+ снимок документов агента `docs/demo/agent_antispam_outputs/`, починен `docs/demo/compare.py`).

> build · glm-5.3-flash

- Гейты: unittest 459 зелёные (включая 9 новых в `tests/test_e2e.py`), `pfs doctor` OK, CLI `--help` OK.
- Реальные прогоны 2026-11-11 (логи на Mac пользователя, разбор новым парсером): RU-антиспам —
  137 шагов, 25,9 мин, 186k/64k токенов, `pfs finish` да, check --strict 0 ошибок, six-pager собран,
  остановки 4 (все закрыты агентом) → `qa/E2E-2026-11-11-antispam-ru.md` ✅. EN-budget-app — 128 шагов,
  31,8 мин → `qa/E2E-2026-11-11-budget-app-en.md` ✅.
- Честно не доделано (требует живых прогонов вне сессии): 4 из 6 прогонов матрицы 3×2
  (antispam-en, budget-app-ru, price-increase-ru/en) — запускаются `/pfs-e2e` или скриптом;
  графы «человек» в рубрике `docs/demo/comparison.md` — заполняются вручную.
- Spot check: парсер повторяет разбор приёмочного скрипта 2026-11-11 (step-finish = шаги, токены
  input/output+reasoning); вердикт отчёта = три ворота (finish, check --strict, six-pager); скрипт
  не ломает таблицу Markdown в отчёте (хвосты вывода чистятся от `|`).
