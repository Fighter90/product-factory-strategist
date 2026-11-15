# Swarm QA — PRO-41 (v1.2.18)

Story: При завершении CLI печатал stale-предупреждения дважды — в `cmd_finish` и снова через `summary_text`. Рой убрал дублирующий вывод в `tools/pfs/cli.py` и добавил регресс-тест в `tests/test_finish.py`. Теперь предупреждения показываются ровно один раз, без каких-либо изменений в поведении `finish.run`.
[0m
> build · glm-5.3-flash

- Гейты при выпуске: unittest green, pfs doctor OK, Pages deploy success.
- Spot check: fix(finish): двойная печать stale-предупреждений в cmd_finish — поведение соответствует задаче; регрессий на затронутых поверхностях нет.
