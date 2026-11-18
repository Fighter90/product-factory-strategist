# Руководство администратора — Стратег Фабрики продуктов

> Для администратора/девопса, который разворачивает, настраивает и сопровождает агента.
> Пользователю: [USER_GUIDE_RU.md](USER_GUIDE_RU.md). Сопровождение: [SUPPORT_RU.md](SUPPORT_RU.md).

## 1. Архитектура развёртывания

Три репозитория:

| Репозиторий | Видимость | Содержимое | Папка после установки |
|---|---|---|---|
| `product-factory-strategist-agent` | public | CLI `pfs`, скиллы, субагенты, хуки, тесты | корень |
| `product-factory-strategist-base` | public | 111 методических карт RU/EN, шаблоны, рубрики, инбокс дистилляции | `knowledge/` |
| `product-factory-strategist-site` | public | лендинг, демо, справка — strategyproduct.ru | деплоится на GitHub Pages |

`knowledge/` в репозитории агента — клон базы, в `.gitignore` (контент живёт в базе).

## 2. Установка

```bash
git clone https://github.com/Fighter90/product-factory-strategist-agent.git
cd product-factory-strategist-agent
bash scripts/install.sh
```

Скрипт: клонирует все три репозитория, ставит `pfs` глобально (uv tool → venv+symlink fallback),
проверяет базу и окружение (`pfs doctor`). Токены не нужны — все репозитории публичные.

Требования: Python 3.9+ (uv рекомендован), git, сетевой доступ к github.com.
Опционально: pdftotext (poppler) для чтения PDF, pypdf.

Составные части doctor: режим установки (editable/venv/source), версия пакета, путь до `pfs`,
здоровье PATH, projects dir, версия Python, pdftotext/pypdf, certifi/TLS-цепочка
(certifi → truststore → `SSL_CERT_FILE`), число карт в базе, активный проект.

## 3. Конфигурация

| Файл | Назначение |
|---|---|
| `config/quality_gate.json` | правила гейта: обязательные разделы документов, запрещённые термины, порог слов, KPI-колонки |
| `config/models.json` | задачи LLM (route, extract, judge, editor…) и модели под них; `pfs models` |
| `.env` (не коммитится) | `LINEAR_API_KEY` (MCP), опциональные ключи OpenAlex/SemanticScholar |
| `.env.example` | плейсхолдеры — копировать в `.env` |

Секреты НЕ коммитятся: `.env` в `.gitignore`, `.env.example` — только плейсхолдеры.
Сквозной прогон агента подтверждает отсутствие реальных ключей в дереве и истории.

## 4. Гейты качества

```bash
python3 -m unittest discover -s tests   # сюита (874+ тестов)
python3 -m tools.pfs doctor             # окружение
pfs check --strict                      # документы: ошибки останавливают
pfs check --six-pager                   # линтер документа комитета
```

Строгий гейт проверяет: теги C###/S### у чисел, разделы документов (Возражения по вариантам,
Альтернативы, Подтверждение + Соответствие обещаний, KPI двух плоскостей), цитаты утверждений
против текста источников, gap-синхронизацию 01↔02, EN-стиль six-pager.

Счётчики (тесты, навыки, карты) обновляются скриптом:

```bash
python3 scripts/update_skill_counts.py --write
```

## 5. Рой (Swarm): конвейер разработки

Проект разрабатывает сам себя. Конвейер: Linear (Todo + метка `swarm`) → Orchestrator
→ Executor (GLM-воркер, worktree, до 3 раундов с фидбеком гейтов) → Tester (детерминированные
гейты) → Reviewer (GLM, ACCEPT/RETURN) → Documenter → Release Manager → Linear Done.

Файлы роя:

| Путь | Назначение |
|---|---|
| `scripts/swarm/orchestrator.mjs` | конвейер задачи: pick → develop → gates → review → release |
| `scripts/swarm/roles/*.md` | промпты ролей |
| `.task-board/attempts.json` | счётчик попыток (2, потом park) |
| `.task-board/claimed.json` | активные клеймы; клейм > 90 мин → requeue |
| `.task-board/wt-pro-XX/` | изолированные worktree задач |
| `.task-board/lock` | single-instance lock оркестратора |

Инфраструктура: supervisor (launchd) рестартует оркестратор; blocked executor'ы упаковываются
в stash; потерянные коммиты — reflog-rescue с нейтральным авторством; гейты красные → вывод
возвращается воркеру.

## 6. Релизы

- Main — всегда зелёный: гейты обязательны до пуша.
- CHANGELOG.md обновляется documenter'ом роя.
- Счётчики (`tests/ (N)`, навыки, карты) — только `scripts/update_skill_counts.py --write`.
- docx-версии документации: `python3 -m tools.pfs docx <md> --out docs/docx/<имя>.docx`.
- Сайт: пуш в `product-factory-strategist-site` → GitHub Pages деплоит автоматически
  (strategyproduct.ru: 8 страниц × RU/EN).

## 7. Безопасность

- Реестры (`claims.jsonl`, `sources/`, `decisions.jsonl`) — только через CLI; хук `pre_guard`
  блокирует прямые правки, чтение вне репозитория — ask.
- Данные не покидают машину: сетевые вызовы — только source fetch/add по URL и LLM-провайдер.
- Институциональные термы, бренды и персональные данные не упоминаются: «внешние источники».
- Сканирование секретов: `lin_api_*`, `sk-*`, `ghp_*`, пароли, `.env` — в дереве и всей истории 0.
- Перепись истории (filter-repo) выполнена; доступ к до-переписным коммитам по SHA
  на стороне GitHub может сохраняться до сборки мусора.

## 8. Диагностика и ремонт

| Симптом | Действие |
|---|---|
| `pfs` не найден | `./scripts/install.sh`; PATH: `~/.local/bin` или uv tool |
| SSL: CERTIFICATE_VERIFY_FAILED | doctor показывает TLS-цепочку; macOS: Install Certificates.command; uv tool: `uv tool install --force --with certifi …` |
| Глобальный pfs указывает на чужой чекаут | переустановка из актуального чекаута; doctor печатает путь до кода агента |
| Оркестратор мёртв | supervisor рестартует; вручную: `bash scripts/swarm/run.sh` |
| Очередь пуста | нет Todo+swarm задач в Linear — создайте задачу |
| Задача в Backlog, не берётся | пикер берёт Todo — переведите статус |
