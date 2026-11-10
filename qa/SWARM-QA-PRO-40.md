# Swarm QA — PRO-40 (v1.2.5)

Story: `pfs cost` умел считать расходы только по транскриптам Claude Code, поэтому работа агента в среде OpenCode выпадала из учёта затрат. Рой добавил в `pfs cost` парсер OpenCode-сессий, покрыл его тестами и обновил справку (HELP.md / HELP_EN.md). Теперь руководитель видит сессии из OpenCode в отчёте стоимости — токены, расходы и Приложение D — наравне с сессиями Claude Code.
[0m
> build · glm-5.3-flash

- Гейты при выпуске: unittest green, pfs doctor OK, Pages deploy success.
- Spot check: pfs cost: парсер OpenCode-сессий — поведение соответствует задаче; регрессий на затронутых поверхностях нет.
