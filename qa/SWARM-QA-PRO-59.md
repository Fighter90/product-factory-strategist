# Swarm QA — PRO-59 (v1.2.33)

Story: Загрузка источников на macOS падала с ошибками SSL CERTIFICATE_VERIFY_FAILED, DNS-сбоями и JS-страницами, которые сохранялись без текста. Рой собрал TLS-цепочку через certifi/truststore, добавил HTTPS-проверку в `pfs doctor` и флаги `--excerpt`/`--via-browser`, а `derived_from` в check/claims теперь учитывается транзитивно — capping строже, предупреждений больше. Пользователь получает надёжное сохранение источников с путём к raw-файлам, покрытое новыми тестами (15 в `tests/test_pro59_round2.py`).
[0m
> build · glm-5.3-flash

- Гейты при выпуске: unittest green, pfs doctor OK, Pages deploy success.
- Spot check: Загрузка источников на macOS: SSL CERTIFICATE_VERIFY_FAILED, DNS, JS-страницы — поведение соответствует задаче; регрессий на затронутых поверхностях нет.
