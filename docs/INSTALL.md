# Установка и тестирование Strategist CLI (pfs)

Требования: macOS/Linux, [uv](https://docs.astral.sh/uv/) **или** Python 3.9+; внешних
зависимостей у CLI нет — только стандартная библиотека. Windows не целевая платформа
(блокировка источников деградирует в no-op).

## Способ 1 — uv (рекомендуется)

```bash
git clone https://github.com/Fighter90/product-factory-strategist.git
cd product-factory-strategist
uv tool install -e .
```

Editable-режим: обновления `main` (`git pull`) подхватываются без переустановки.
Обновление самой установки: `uv tool upgrade product-factory-strategist --force` или
повторный `uv tool install -e . --force`.

## Способ 2 — install.sh (сам выбирает путь)

```bash
./scripts/install.sh
```

uv есть → `uv tool install -e .`; uv нет → venv `~/.pfs-venv` + symlink
`~/.local/bin/pfs` (нужен `~/.local/bin` в PATH).

## Способ 3 — вручную (PEP 668)

Системный python (Homebrew/uv) запрещает `pip install` в глобальное окружение
(PEP 668). Обходы: venv (способ 2) или `pip3 install --break-system-packages -e .`
(на свой риск, не рекомендуется).

## Первые команды

```bash
pfs new "<название>" "<запрос дословно>"   # новый проект
pfs list / status / next                  # проекты, где остановились, что решать
pfs --project <slug> check --strict       # контроль качества документов
pfs finish                                # финальный пакет одной цепочкой
pfs                                       # без аргументов — шпаргалка (rc=0)
```

Папка проектов: `<репо>/projects` по умолчанию; переопределяется `PFS_PROJECTS_DIR`.
Paths (knowledge, config) резолвятся от расположения пакета — cwd не важен.

## Обновление

Editable-установки (uv tool -e, pip -e): `git pull origin main` — достаточно.
Не-editable: повторный `pip install .` / `uv tool install --force`.

## Удаление

```bash
uv tool uninstall product-factory-strategist   # или: rm ~/.pfs-venv ~/.local/bin/pfs
```

## Тестирование

```bash
python3 -m unittest discover -s tests          # вся сюита (277+ тестов, чистый stdlib)
python3 -m unittest tests.test_finish -v       # один файл
pfs doctor                                     # установка и окружение: python, pypdf, БЗ, реестры
pfs --project <slug> check --strict            # quality gate документов (ошибки → rc≠0)
./scripts/install.sh && pfs doctor             # проверка установки
```

Тесты ничего не устанавливают и не требуют сети: каждый файл поднимает свой
`PFS_PROJECTS_DIR` во временном каталоге.

## Troubleshooting

| Симптом | Причина и решение |
|---|---|
| `pfs: command not found` | не установлен — `./scripts/install.sh`; `~/.local/bin` вне PATH — добавьте `export PATH="$HOME/.local/bin:$PATH"` |
| `ModuleNotFoundError: No module named 'tools'` | запуск `python3 -m tools.pfs` вне репо без установки — установите (выше) или запускайте из корня репо |
| `error: externally-managed-environment` | PEP 668 — используйте uv/venv (способы 1–2), не `pip` в системное окружение |
| `Ошибка: Проект 'X' не найден` | неверный `PFS_PROJECTS_DIR` или запуск из другого каталога: `pfs list` покажет, что видит CLI |
| `Error: .task-board/lock существует` | работает другой экземпляр роя; после kill удалите файл |
| check: 9X/100 | предупреждения не блокируют; `--strict` блокирует только ошибки |
