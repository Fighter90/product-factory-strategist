---
name: ph-trends
description: |
  Тренды Product Hunt → применение к продукту. Используй, когда руководитель говорит
  «тренды Product Hunt», «что сейчас запускают на PH», «что топовое в категории AI agents»,
  «примени тренды к нашему продукту», «к чему нам готовиться к запуску», «посмотри лидерборд PH»,
  или нужен срез рынка запусков: лидерборды недели/месяца, свежие AI-агенты, паттерны
  позиционирования, монетизации и демо. Источник — MCP-сервер producthunt
  (https://mcp.producthunt.com/mcp, OAuth, без API-ключа). Результат — 5–8 трендов с
  доказательствами и применения к продукту: каждое применение = гипотеза + шаг проверки,
  не факт. Запись в аккаунт PH (черновики запуска) — только по отдельной просьбе с подтверждением.
---

# ph-trends — тренды Product Hunt → применение к продукту

## Суть

Product Hunt — ежедневный срез того, что рынок запускает прямо сейчас: темы, монетизация,
позиционирование, формат демо. Скилл превращает этот срез в конкретные улучшения продукта
по переиспользуемому промту ниже. Правило качества: тренд без 2–3 примеров-доказательств —
не тренд; применение без метрики и шага проверки — не улучшение, а модное слово.

## Переиспользуемый промт («тренды → применение к продукту»)

Заполни первую строку и отдай агенту целиком — остальное он сделает сам:

```
Продукт: <название, ссылка, 1 абзац — что это, для кого, чем отличается>.
Задача: собрать тренды Product Hunt за последние 2–4 недели и выдать применения к продукту.

Шаг 1 — сбор (MCP producthunt):
- get_leaderboard за текущую и предыдущую неделю — кто выигрывает и с какой подачей;
- get_categories → выбери 2–3 категории, ближайшие к продукту; по каждой:
  get_products (highest_rated) — кто держит рейтинг, и search_launches — что запускают сейчас;
- отдельно отметь продукты со своим MCP-сервером (mcp_server_urls) — агентность как канал дистрибуции;
- ничего в аккаунте PH не менять: инструменты записи (launch-черновики) — вне этого запроса.

Шаг 2 — паттерны: сведи запуски в 5–8 трендов (тема, монетизация, позиционирование, каналы,
формат демо). Для каждого тренда — 2–3 примера со ссылками на запуски.

Шаг 3 — применение к продукту: для каждого тренда —
- применимость: высокая / средняя / не про нас — и почему именно;
- конкретное улучшение: что добавить / переформулировать / убрать (продукт или позиционирование);
- как проверить: гипотеза + шаг валидации (метрика, A/B, интервью, пилот).
  Не «добавим AI», а «что изменит какую метрику и как мы это увидим».

Шаг 4 — вердикт: топ-3 быстрых улучшения (дни, не недели), 1 стратегический вывод,
и анти-тренды: что модно, но нашему продукту не подходит (и почему).
Всё — гипотезы; «факт» — только то, что подтверждено данными.
```

## Алгоритм агента

1. **Проверь MCP.** Инструменты пространства `producthunt` (get_leaderboard, get_categories,
   get_products, search_launches, get_product_profile, find_alternatives). Нет подключения —
   не выдумывай данные: сообщи и дай установку (см. «Установка MCP» ниже).
2. **Собери** по шагу 1 промта. Ограничивайся публичными данными; профили и отзывы — через
   get_product_profile. Периоды называй явно (неделя = ISO-неделя текущего месяца).
3. **Сведи и примени** по шагам 2–4. Для «нашего продукта» используй бриф из вопроса или
   README/лендинг репозитория, если промт не задал продукт.
4. **Зафиксируй гипотезы**, если идёт работа в проекте pfs: `pfs claim add "…" --kind hypothesis`
   (применение тренда к продукту — всегда гипотеза до проверки; данные PH добавляй как источник:
   `pfs source add <url запуска>`). Без проекта — выведи таблицу в чат.

## Гигиена

- Данные PH публичные — их можно цитировать со ссылками. Запись в аккаунт (черновики запуска,
  обновления профиля) — только отдельная просьба руководителя + подтверждение перед сабмитом.
- Формат PH (голоса, бейджи) — сигнал витрины, не продуктовой ценности: не подменяй
  доказательства спроса рейтингом запуска.
- Анти-тренды обязательны: слепое копирование моды — каннибализация фокуса продукта.

## Установка MCP (если не подключён)

- OpenCode: `opencode mcp add producthunt --global --url https://mcp.producthunt.com/mcp`,
  затем `opencode mcp auth producthunt` (браузер, OAuth; без API-ключа).
- Claude Code: `claude mcp add --transport http --scope user producthunt https://mcp.producthunt.com/mcp`,
  затем в клиенте `/mcp` → producthunt → Authenticate.
- Репозиторий: сервер уже прописан в `.mcp.json` (`producthunt`, type http).

## English

**ph-trends — Product Hunt trends → application to the product.**

Trigger when the user says "Product Hunt trends", "what's launching on PH", "top AI agents
on PH", "apply trends to our product", or needs a launch-market scan: weekly/monthly
leaderboards, fresh AI-agent launches, positioning/pricing/demo patterns.

Reusable prompt: fill in the product line and paste the block above (steps: collect via the
producthunt MCP tools → 5–8 evidence-backed patterns → per-trend applicability + a concrete
improvement + a validation step → verdict with top-3 quick wins, one strategic takeaway,
and anti-trends). Everything is a hypothesis until validated; in a pfs project register it
via `pfs claim add … --kind hypothesis` and add launch URLs as sources.

Hygiene: public data only; account writes (launch drafts) require explicit confirmation;
launch votes are storefront signal, not demand evidence.
