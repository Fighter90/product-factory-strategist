# Сопроводительная документация — Стратег Фабрики продуктов

> Сопровождение, обслуживание и развитие проекта. Пользователю: [USER_GUIDE_RU.md](USER_GUIDE_RU.md).
> Администратору: [ADMIN_GUIDE_RU.md](ADMIN_GUIDE_RU.md).

## 1. Версионирование и релизы

- Схема: `vMAJOR.MINOR.PATCH` (v1.2.x — текущая линия).
- Релизы выпускает release-manager роя: squash-merge в main, запись в CHANGELOG,
  счётчики через `scripts/update_skill_counts.py --write`, docx-пересборка.
- Теги v1.2.x — на коммите релиза (переписаны при filter-repo — авторство нейтральное).

## 2. Регулярное сопровождение

| Периодичность | Действие | Команда |
|---|---|---|
| Перед каждым пушем | гейты: сюита + doctor + strict | `python3 -m unittest discover -s tests && pfs check --strict` |
| После добавления/удаления теста | счётчики | `python3 scripts/update_skill_counts.py --write` |
| После правки README/HELP/SUBMISSION | docx-версии | `python3 -m tools.pfs docx <md> --out docs/docx/<имя>.docx` |
| Еженедельно | обновление базы: fetch + lint | `git -C knowledge pull && pfs kb lint` |
| После смены источников | сверка цитат | `pfs check --strict` (числовой кросс-чек) |

## 3. Обновление базы знаний

Процесс дистилляции (подробно — `knowledge/inbox/external-methodology/README.md`):

1. Внешние методологические материалы попадают в инбокс (сырые файлы не публикуются).
2. Методолог выделяет метод в карту `methods/<id>.md` + зеркало `methods_en/<id>.md`
   (frontmatter: id, lang, tags, related; разделы метода и критерии качества).
3. Паритет RU/EN проверяется `pfs kb lint` (разделы и объём).
4. `INDEX.md`/`INDEX_EN.md` обновляются `pfs kb index`.

Текущее состояние: 111 карт RU + 111 EN, шаблоны (включая six-pager PROMPT и
эталон-конспект), рубрики. Термы, бренды и персональные данные — 0.

## 4. Рой: обслуживание конвейера

| Аспект | Детали |
|---|---|
| Запуск | supervisor (launchd) или `bash scripts/swarm/run.sh` |
| Очередь | Linear: Todo + метка `swarm` (pick — первый по очереди) |
| Попытки | 2; после — park (не блокирует очередь) |
| Stuck | клейм In Progress > 90 мин → реqueue |
| Краш-хвосты | `blocked executor leftovers` в сташе — применить или выбросить |
| Потерянные коммиты | `git reflog` → cherry-pick (резкое авторство сбрасывается оркестратором) |
| Release | gh pr create; fallback — локальный squash-merge |
| Логи | `.task-board/*.log`, `/tmp/swarm-watchdog-run.log` |

Типовые сбои: executor не уложился в 25 мин (без коммитов — попытка не сгорает);
гейты красные → фидбек воркеру (до 3 раундов); issue в Backlog не берётся — перевести в Todo.

## 5. Известные ограничения

- **docx**: генератор без таблиц-стилей сложного уровня — сложные таблицы правятся вручную.
- **PDF**: не строится агентом (только чтение через pdftotext/pypdf); six-pager PDF — вручную.
- **gh pr create** после переименования репозитория падает (redirect) — release manager
  автоматически уходит в локальный squash-merge.
- **uv-tool окружение без pip**: `python -m pip install` не работает — используйте
  `uv tool install --force --with certifi …` (PRO-82).
- **filter-repo и GitHub**: до-переписные коммиты могут быть доступны по SHA до GC.
- **EN six-pager**: пишется writer'ом вручную; каркас-черновик содержит маркер EN draft.

## 6. Диагностика

```bash
pfs doctor                        # окружение: PATH, python, TLS-цепочка, база, проекты
python3 -m unittest discover -s tests   # сюита
python3 scripts/update_skill_counts.py --check  # счётчики без записи
pfs kb lint                       # целостность базы знаний
git log --all --oneline | head    # история (переписана: нейтральное авторство)
git stash list                    # хвосты прерванных executor'ов
```

Логи: `.task-board/*.log` (рой), `~/.local/share/opencode/log/` (воркеры),
`/tmp/swarm-watchdog-run.log` (супервизор).

## 7. Структура сопровождаемых артефактов

| Артефакт | Где | Обновление |
|---|---|---|
| Документы проекта 00–07 | `projects/<slug>/outputs/` | шаги процесса + pfs export |
| Six-pager RU/EN | `projects/<slug>/outputs/SIX_PAGER*.md` | writer-цикл + finish |
| Excel-приложения | `outputs/attachments/*.xlsx` | `pfs calc all` |
| Дека | `outputs/presentations/deck.html` | `pfs export --deck` |
| docx документации | `docs/docx/` | пересборка из md |
| Сайт | отдельный репозиторий → strategyproduct.ru | пуш → Pages |

## 8. Каналы

- Задачи и статус: Linear (команда PRO), метка `swarm` — через рой.
- Код и релизы: GitHub — три репозитория (agent, base, site).
- Сайт: strategyproduct.ru (GitHub Pages).
