# Навыки агента: полный реестр

Навыки — повторяемые процедуры, которые агент подключает на шагах процесса. В репозитории теперь
**41 навык**: 13 базовых + 27 из плагина product-skills + новые интеграции. Карьерные файлы
(`SKILL_*_CAREER_OPS_UI.md`) сознательно не включены.

## Базовые (процесс агента)

| Навык | Шаг | Что делает |
|---|---|---|
| strategist | все | Точка входа: маршрут запроса, ведение процесса |
| intake | 0 | Бриф: ≤3 вопроса, допущения, подтверждение руководителем |
| research | 1–2 | План от вопросов, поиск, выписки в реестр |
| situation | 3 | Картина: известно/не знаем/противоречия |
| options | 4 | ≥3 варианта + возражения + red team |
| strategy | 6 | Продуктовая + коммуникационная стратегии |
| validation-plan | 7 | Карточка проверки: метрика, база, срок, контрметрики |
| data-analysis | 2 | Профиль таблиц, когорты, воспроизводимые скрипты |
| interviews | 2 | Гайды, анализ интервью, ИИ-респонденты (только гипотезы) |
| ux-review | 2 | Разбор интерфейсов/путей по материалу |
| decision-support | 9–10 | Запись решения, обязательства, пересмотр |
| six-pager | 8 | Фоновая сборка six-pager + Excel (см. ниже) |
| deep-research | 2 | Feynman: deepresearch/lit/compare с provenance |

## Плагин product-skills (27) — операционализация методов

Первичный источник методик базы знаний; каждый навык = процедура «как сделать» к карте «как думать».

roadmap-okr (роадмап+OKR) · growth-effects (оценка эффектов роста) · product-navigator (навигатор скилов)
· auction-monetization (аукционная монетизация) · product-bets (ставки) · pestle-analysis ·
model-validation · risk-management · product-context-strategy · traction-modeling · unit-economics ·
solution-design · monetization-models · mvp-pilot-launch · growth-frameworks · business-models ·
competitor-analysis · team-org-structure · market-sizing · analytical-reports · cannibalization ·
product-metrics · benchmarking · scaling-communication · growth-drivers · trend-analysis · problem-design

Согласование: если навык и карта знаний расходятся — приоритет у карты (методология) с пометкой в журнале.

## Интегрированные дополнительные

| Навык | Источник | Назначение |
|---|---|---|
| deck | officecli + Higgsfield + Lovable | Презентация комитета из SIX_PAGER.md: PPTX через officecli, HTML-fallback, визуалы через Higgsfield, web-версия через Lovable (OAuth) |
| sdd | sdd-system-prompt.md | Дисциплина разработки самого агента: спека → тест → гардрейлы |

## Установочные гайды (docs/)

- `docs/frontend-design-setup.md` — сетап фронтенда без AI-слопа (модель, генерация, стиль).
- `docs/claude-setup-mac.md` — установка окружения на macOS.

## Не включено (карьерное)

SKILL_UPDATE_CAREOPS_UI.md, SKILL_TEST_CAREER_OPS_UI.md; папка «Не рабочая сборка» (hotel-setup) — вне рамок агента.

## MCP для отчётов/презентаций (состояние)

- **Linear** — подключён (ключ в .env): задачи ведутся по программе.
- **Lovable** (`https://mcp.lovable.dev`) — прописан в .mcp.json (type http); только OAuth: в клиенте
  `/mcp` → lovable → Authenticate. После этого агент создаёт web-деку/лендинг по docs/lovable-brief.md.
- **Higgsfield** — подключён на уровне среды (визуалы слайдов, генерация изображений; расход кредитов — с вопросом).
- **officecli** — внешний CLI (`~/.local/bin/officecli`): docx/xlsx/pptx-манипуляции для деки и отчётов.
- **Feynman** (feynman.is) — CLI research-агент для глубокого ресёрча: skill `deep-research`.
