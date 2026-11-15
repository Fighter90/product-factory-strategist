---
name: strategy
description: Шаг 6. Согласованные продуктовая и коммуникационная стратегии по выбранному варианту — аудитория и задача, альтернативы, направление и осознанные отказы, экономика; ситуация аудитории, барьер, ключевое сообщение и его подтверждение, роль каналов; проверка, что обещания соответствуют продукту.
---

# Продуктовая и коммуникационная стратегия

Шаблоны: `knowledge/templates/product_strategy.md`, `knowledge/templates/comms_strategy.md`.
Карты: `M-strategy-growth`, `M-jtbd`, `M-competitors`, `M-success-metrics`, `M-unit-economics`, `M-outcome-roadmap`,
`M-usp`, `M-product-communication`, `M-audience-research`, `M-marketing-research`.

## 04_product_strategy.md
1. **Аудитория и её задача** (JTBD: ситуация → мотивация → ожидаемый результат), размер сегмента [C###].
2. **Альтернативы** — чем задачу решают сейчас (включая «ничего не делать» и непрямых конкурентов).
3. **Выбранное направление** — суть ставки, почему этот вариант (ссылка на 03_options), что делаем в 1-м/2-м/3-м этапе
   (outcome-роадмап: результат, а не фичи).
4. **Осознанные отказы** — что сознательно НЕ делаем и почему (сегменты, функции, каналы).
5. **Экономика** — связь пользы с затратами и доходами: драйверы выручки, затраты, юнит-экономика, диапазоны;
   прогнозы помечены как forecast.
6. **Метрики** — NSM/целевая метрика, дерево, контрметрики. **Риски** и их митигация.

## 05_comms_strategy.md (можно отдать субагенту `comms-strategist`)
1. **Аудитория и ситуация** — кто, в какой момент и где принимает решение.
2. **Барьер понимания или выбора** — непонимание, недоверие, цена, привычка, риск; на чём основан [C###].
3. **Ключевое сообщение** — одна фраза + 2–3 опорных тезиса.
4. **Подтверждение** — доказательства для каждого тезиса (факты продукта, данные, демонстрация).
5. **Роль каналов** — каждый канал: задача в пути (узнать/понять/попробовать/остаться), формат, метрика.
6. **Соответствие обещаний продукту** — таблица «Обещание | Чем подтверждено в продукте [C###] | Риск
   перепродать». Обещание без подтверждения — убрать или переписать.

Согласованность: аудитория, задача и метрики в двух документах совпадают; каждое обещание коммуникации опирается на
функцию/свойство из продуктовой стратегии. `pfs check` → `pfs step strategy done`.

**Роудмап (PRO-70):** вместе со стратегией соберите роудмап — `pfs step strategy done` делает это сам, либо
`pfs roadmap` вручную. Получается `outputs/roadmap-<slug>.xlsx` в двух листах-форматах быстрых гибких роудмапов
(Google Sheets): «Проекты» — по проектам, «Фичи по проектам» — фичи, сгруппированные по проектам; колонки периодов
(кварталы по умолчанию; `pfs roadmap --granularity week|month|quarter`), отрезки задач отмечены заливкой статуса
(зелёный — сделано, жёлтый — в работе, синий — план, красный — риск; расшифровка — лист «Легенда»). Данные берутся
из pfs-проекта: этапы outcome-роадмапа 04 → проекты, тактики → фичи (даты-план по кварталам); точные даты, команды,
приоритеты и статусы задаются в `projects/<slug>/roadmap.json` (передать: `pfs roadmap --spec файл`).

## English

# Product and communication strategy

Templates: `knowledge/templates/product_strategy.md`, `knowledge/templates/comms_strategy.md`
(`knowledge/templates/en/…` for `lang: en`). Maps: `M-strategy-growth`, `M-jtbd`, `M-competitors`,
`M-success-metrics`, `M-unit-economics`, `M-outcome-roadmap`, `M-usp`, `M-product-communication`,
`M-audience-research`, `M-marketing-research`.

## 04_product_strategy.md
1. **Audience and its job** (JTBD: situation → motivation → expected outcome), segment size [C###].
2. **Alternatives** — how the job is solved today (including "do nothing" and indirect competitors).
3. **Chosen direction** — the essence of the bet, why this option (link to 03_options), what we do in stage 1/2/3
   (an outcome roadmap: results, not features).
4. **Conscious trade-offs** — what we deliberately do NOT do and why (segments, features, channels).
5. **Economics** — how value links to costs and revenue: revenue drivers, costs, unit economics, ranges;
   forecasts marked as forecast.
6. **Metrics** — NSM/target metric, tree, counter-metrics. **Risks** and their mitigation.

## 05_comms_strategy.md (can be handed to the `comms-strategist` subagent)
1. **Audience and situation** — who makes the decision, at what moment and where.
2. **Barrier of understanding or choice** — confusion, distrust, price, habit, risk; what it rests on [C###].
3. **Key message** — one sentence + 2–3 supporting points.
4. **Proof** — evidence for each point (product facts, data, demonstration).
5. **Role of channels** — each channel: its job along the journey (learn/understand/try/stay), format, metric.
6. **Promises backed by the product** — a "Promise | What backs it in the product [C###] | Overselling risk" table.
   A promise without backing — remove or rewrite it.

Consistency: audience, job and metrics match across the two documents; every communication promise rests on a
feature/property from the product strategy. `pfs check` → `pfs step strategy done`.

**Roadmap (PRO-70):** build the roadmap together with the strategy — `pfs step strategy done` does it
automatically, or run `pfs roadmap` manually. It writes `outputs/roadmap-<slug>.xlsx` with two sheets in the quick
agile Google-Sheets roadmap format: «Проекты» (by projects) and «Фичи по проектам» (features grouped by projects);
period columns (quarters by default; `pfs roadmap --granularity week|month|quarter`) with task spans filled by the
status color (green — done, yellow — in progress, blue — planned, red — at risk; see the «Легенда» sheet). Data
comes from the pfs project: the outcome-roadmap stages of 04 become projects, tactics become features (plan dates
by sequential quarters); exact dates, teams, priorities and statuses go into `projects/<slug>/roadmap.json`
(pass a custom file: `pfs roadmap --spec <file>`).
