# Swarm QA — PRO-45 (v1.2.14)

Story: Раньше теги не сопровождались GitHub Release — заметки приходилось оформлять вручную, а для прошлых версий их не было вовсе. Рой добавил скрипт извлечения секций CHANGELOG, шаг публикации Release в `release.yml`, тесты workflow и бэкфилл релизов для v1.2.1–v1.2.13. Теперь каждый пуш тега автоматически создаёт Release с текстом из CHANGELOG, а история прошлых версий заполнена.
[0m
> build · glm-5.3-flash

- Гейты при выпуске: unittest green, pfs doctor OK, Pages deploy success.
- Spot check: ci: release.yml — GitHub Release из CHANGELOG на тег + бэкфилл v1.2.1–v1.2.13 — поведение соответствует задаче; регрессий на затронутых поверхностях нет.
