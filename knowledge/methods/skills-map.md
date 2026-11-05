---
id: M-skills-map
title: Карта методов: вопрос руководителя продукта → какие карты и в каком порядке
course: skills
sources: ["product-skills: product-navigator (карта навыков, комбинации под типовые задачи, переходы между фазами)", "Скиллсет продакта (xlsx учебной программы): 9 категорий компетенций, шкала самооценки 0–5, карта дисциплин"]
stages: [intake, research, options, strategy, validation, after-decision]
tags: [навигация, маршрут, карта-навыков, порядок-карт, типовые-задачи]
related: [M-strategy-growth, M-external-environment, M-customers, M-competitors, M-goals-drivers-bets, M-landscapes, M-risks, M-outcome-roadmap, M-success-metrics, M-team, M-product-context, M-jtbd, M-problem-design, M-solution-design, M-roadmap, M-mvp-pilots, M-pmf-scaling, M-product-communication, M-product-metrics, M-decision-daci, M-delivery, M-research-types, M-audience-research, M-brief-hypotheses, M-loyalty-metrics, M-in-depth-interviews, M-interview-analysis, M-quant-methods, M-usp, M-marketing-research, M-ux-frameworks, M-cjm, M-usability-testing, M-ux-heuristics, M-dogfooding, M-ux-backlog, M-workshops, M-ai-in-research, M-synthetic-respondents, M-design-thinking, M-market-sizing, M-unit-economics, M-traction-model, M-cannibalization, M-monetization, M-growth-frameworks, M-business-models, M-benchmarking, M-source-criticism, M-trends-scenarios]
---

# Карта методов: вопрос → карты → порядок

## Когда применять
Руководитель продукта задаёт расплывчатый вопрос («продукт не растёт», «нужно защитить проект», «стоит ли входить в рынок»), и агенту надо выбрать, какие карты читать и в каком порядке. Начинать отсюда, если маршрут неочевиден; если задача чёткая («посчитай TAM», «построй трекшн-модель») — идти сразу в нужную карту.

## Суть
Три принципа маршрута (из карты навыков product-navigator):
1. Сначала контекст и стадия, затем рынок и среда, затем проблема/решение, затем цели и метрики, затем моделирование и экономика, затем план и запуск, затем масштабирование; по каждой теме можно возвращаться на любой фазе.
2. Рыночный анализ и моделирование применимы на любой стадии жизненного цикла продукта; меняется глубина (IDEA — оценки сверху, SCALE — полная валидация).
3. Любая внешняя цифра, попадающая в расчёт, проходит [[M-source-criticism]] и получает класс A–D; допущения без источника помечаются явно.

Назначение чужих карт указано по названию id; при расхождении приоритет у `knowledge/INDEX.md`.

### Навыки product-skills → карты
| Навык | Карта |
|---|---|
| product-context-strategy | [[M-product-context]], [[M-strategy-growth]] |
| business-models | [[M-business-models]] |
| risk-management | [[M-risks]] |
| growth-frameworks | [[M-growth-frameworks]] |
| market-sizing | [[M-market-sizing]] |
| competitor-analysis | [[M-competitors]] |
| pestle-analysis | [[M-external-environment]] |
| benchmarking | [[M-benchmarking]] |
| trend-analysis | [[M-trends-scenarios]] |
| analytical-reports | [[M-source-criticism]] |
| problem-design | [[M-problem-design]] (+ [[M-research-types]], [[M-jtbd]]) |
| solution-design | [[M-solution-design]] |
| product-metrics | [[M-product-metrics]], [[M-success-metrics]] |
| growth-drivers, product-bets | [[M-goals-drivers-bets]] |
| traction-modeling, growth-effects, model-validation | [[M-traction-model]] |
| unit-economics | [[M-unit-economics]] |
| cannibalization | [[M-cannibalization]] |
| monetization-models, auction-monetization | [[M-monetization]] |
| roadmap-okr | [[M-outcome-roadmap]], [[M-roadmap]] |
| mvp-pilot-launch | [[M-mvp-pilots]] |
| team-org-structure | [[M-team]] |
| scaling-communication | [[M-pmf-scaling]], [[M-product-communication]] |

### Скиллсет продакта (учебная программа) → карты
Официальная матрица компетенций программы: 9 категорий, каждая — набор поведенческих индикаторов; самооценка по шкале 0–5 (0 — не владею … 5 — могу научить других) против желаемой оценки и оценки со стороны. Использовать как второй вход маршрутизации: если руководитель формулирует запрос через компетенцию («научиться планировать», «прокачать аналитику») — идти по строке таблицы.

| Категория скиллсета | О чём индикаторы | Карты |
|---|---|---|
| Структура, перевод «сложного в простое» | Структурирование в таблицы/схемы, декомпозиция задач, лаконичный статус и риски, выделение важных фактов, видение «сверху вниз» | [[M-source-criticism]], [[M-product-communication]], [[M-problem-design]], [[M-solution-design]] |
| Менеджмент и коммуникации | Аргументированность, пауза в конфликте, активное слушание, презентация идеями/документами/прототипами, выбор канала (встреча/почта/чат) | [[M-product-communication]], [[M-decision-daci]], [[M-workshops]] |
| Планирование и организация работ | Оценка ресурсов/зависимостей/рисков, слежение за роадмапом, работа с изменениями и эскалация, организация команды | [[M-roadmap]], [[M-delivery]], [[M-team]], [[M-risks]] |
| Качество и скорость дискавери | Решения на данных дискавери, реакция на рынок, JTBD / User Story Mapping / CJM, исследования и инновации | [[M-research-types]], [[M-jtbd]], [[M-cjm]], [[M-problem-design]] |
| Аналитика и метрики | Input→output, физический смысл данных и влияние на бизнес, traction model, учёт шума/сезонности, дерево метрик, дашборды и SQL | [[M-product-metrics]], [[M-traction-model]], [[M-quant-methods]] |
| Формирование и управление PnL | Экономика продукта, LTV/CAC, окупаемость, монетизационные решения | [[M-unit-economics]], [[M-monetization]] |
| Улучшение клиентского опыта | Пользователь на первом месте, сбор обратной связи, touchpoints и UX, CX-показатели (CSAT, обращения в поддержку, отток), осознанный скоуп MLP | [[M-cjm]], [[M-usability-testing]], [[M-loyalty-metrics]], [[M-ux-backlog]], [[M-mvp-pilots]] |
| Продуктовый менеджмент и стратегия | Анализ конкурентов, бэклог спринта, презентация видения, квартальные планы и роадмап, end vision и УТП, анализ рынка | [[M-competitors]], [[M-product-context]], [[M-strategy-growth]], [[M-outcome-roadmap]], [[M-usp]], [[M-market-sizing]] |
| ML-модели и AI в продуктах | Запуск продуктов с ML/DS, донесение техсложности руководителю, понимание принципов программирования и ограничений, язык с техэкспертами | Пробел базы: отдельной карты нет; частично [[M-solution-design]] (реализуемость, TDR-вопросы) и [[M-ai-in-research]] (AI в исследовании). При запросе — честно назвать пробел и собрать гипотезы из смежных карт |

Карта дисциплин программы (для контекста, не маршрут): 1 модуль — продуктовый менеджмент, анализ данных, коммуникации, CX; 2 модуль — корпоративные финансы (под PnL); 3 модуль — стратегии роста, бизнес-модели и юнит-экономика, анализ рынка, управление проектами; 2 курс — ML/AI в продуктах, платформенные решения. Цели по компетенциям ведутся по структуре «компетенция → цель → что сделаю → как пойму, что выполнено → срок».

## Процедура
1. Сформулировать вопрос руководителя одним предложением и найти ближайшую строку в таблице ниже; если нет — собрать маршрут по этапам процесса.
2. Задать 3–5 вопросов контекста (продукт и домен; задача сейчас; что уже сделано; какие данные есть; B2B/B2C, стадия рынка) — пропустить уже известное. Это [[M-product-context]] / [[M-brief-hypotheses]].
3. Пройти карты маршрута по порядку; каждая карта даёт артефакт, который входит в следующую.
4. На каждом шаге фиксировать: вход (данные и их класс), выход (артефакт), открытые вопросы.
5. Перед выводом — шаг проверки (источники, модель, риски) и явный список допущений.
6. Критерий перехода к следующей фазе: артефакт текущей фазы готов, ключевые допущения имеют план проверки.

### Типовые вопросы → маршрут
| Вопрос руководителя | Карты по порядку |
|---|---|
| Хочу запустить новый продукт | [[M-product-context]] → [[M-market-sizing]] → [[M-competitors]] → [[M-business-models]] → [[M-growth-frameworks]] → [[M-problem-design]] → [[M-solution-design]] → [[M-mvp-pilots]] |
| Стоит ли входить в рынок / сегмент | [[M-market-sizing]] → [[M-source-criticism]] → [[M-competitors]] → [[M-external-environment]] → [[M-business-models]] (Viability) → [[M-unit-economics]] → [[M-risks]] |
| Стратегия на год | [[M-product-context]] → [[M-strategy-growth]] → [[M-market-sizing]] → [[M-competitors]] → [[M-goals-drivers-bets]] → [[M-outcome-roadmap]] → [[M-risks]] |
| Продукт не растёт | [[M-product-metrics]] → [[M-goals-drivers-bets]] → [[M-problem-design]] → [[M-benchmarking]] → [[M-goals-drivers-bets]] (ставки) → [[M-growth-frameworks]] |
| Защитить проект перед руководством | [[M-product-context]] → [[M-business-models]] → [[M-market-sizing]] → [[M-traction-model]] (с валидацией) → [[M-risks]] → [[M-product-communication]] |
| Планирую квартал | [[M-goals-drivers-bets]] → [[M-outcome-roadmap]] → [[M-team]] → [[M-risks]] |
| Понять конкурентов | [[M-competitors]] → [[M-landscapes]] → [[M-benchmarking]] → [[M-market-sizing]] |
| Выбрать метрики / NSM | [[M-product-metrics]] → [[M-success-metrics]] → [[M-goals-drivers-bets]] → [[M-benchmarking]] |
| Выбрать фреймворк роста | [[M-growth-frameworks]] → [[M-product-metrics]] → [[M-goals-drivers-bets]] |
| Готовимся к масштабированию | [[M-pmf-scaling]] → [[M-market-sizing]] → [[M-team]] → [[M-risks]] → [[M-outcome-roadmap]] |
| Построить трекшн-модель | [[M-traction-model]] → [[M-unit-economics]] → [[M-monetization]] → [[M-cannibalization]] (если есть база) → [[M-benchmarking]] → [[M-source-criticism]] |
| Проверить / провалидировать модель | [[M-traction-model]] (разделы валидации и эффектов) → [[M-benchmarking]] → [[M-source-criticism]] → [[M-cannibalization]] |
| Выбрать модель монетизации или цену | [[M-monetization]] → [[M-unit-economics]] → [[M-traction-model]] → (конкуренция за ресурс) аукцион в [[M-monetization]] |
| Посчитать юнит-экономику | [[M-unit-economics]] → [[M-benchmarking]] → [[M-traction-model]] |
| Запуск нового продукта/тарифа на существующую базу | [[M-cannibalization]] → [[M-unit-economics]] → [[M-traction-model]] → [[M-benchmarking]] |
| Бизнес-модель: PLG или SLG, подписка или комиссия | [[M-business-models]] → [[M-monetization]] → [[M-growth-frameworks]] |
| Проверить цифру или аналитический отчёт | [[M-source-criticism]] → [[M-benchmarking]] |
| Куда движется рынок, какие сценарии | [[M-external-environment]] → [[M-trends-scenarios]] → [[M-source-criticism]] → [[M-risks]] |
| Понять пользователей и проблему (Discover) | [[M-research-types]] → [[M-audience-research]] / [[M-in-depth-interviews]] → [[M-interview-analysis]] → [[M-jtbd]] → [[M-problem-design]] |
| Выбрать и проверить решение (Define) | [[M-solution-design]] → [[M-mvp-pilots]] → [[M-success-metrics]] → [[M-risks]] |
| Улучшить UX | [[M-ux-frameworks]] → [[M-cjm]] → [[M-usability-testing]] / [[M-ux-heuristics]] → [[M-ux-backlog]] |
| Позиционирование и коммуникация | [[M-usp]] → [[M-marketing-research]] → [[M-product-communication]] |
| Лояльность, NPS | [[M-loyalty-metrics]] → [[M-success-metrics]] |
| Спор между стейкхолдерами, решение | [[M-decision-daci]] → [[M-workshops]] → [[M-risks]] |

### По этапам процесса агента
| Этап | Карты |
|---|---|
| intake (вводные) | [[M-product-context]], [[M-brief-hypotheses]], [[M-strategy-growth]] |
| research (исследование) | [[M-external-environment]], [[M-market-sizing]], [[M-competitors]], [[M-customers]], [[M-benchmarking]], [[M-source-criticism]], [[M-trends-scenarios]], [[M-research-types]] |
| options (варианты) | [[M-problem-design]], [[M-solution-design]], [[M-business-models]], [[M-growth-frameworks]], [[M-monetization]], [[M-unit-economics]] |
| strategy (стратегия) | [[M-strategy-growth]], [[M-goals-drivers-bets]], [[M-traction-model]], [[M-outcome-roadmap]], [[M-cannibalization]] |
| validation (проверка) | [[M-traction-model]] (валидация), [[M-source-criticism]], [[M-benchmarking]], [[M-risks]], [[M-mvp-pilots]] |
| after-decision (после решения) | [[M-roadmap]], [[M-delivery]], [[M-success-metrics]], [[M-product-metrics]], [[M-pmf-scaling]], [[M-product-communication]] |

### По стадии продукта: что анализировать и моделировать
| Стадия | Рынок и среда | Моделирование и экономика |
|---|---|---|
| IDEA | [[M-market-sizing]], [[M-external-environment]], [[M-competitors]], [[M-business-models]], [[M-growth-frameworks]] | top-down из [[M-traction-model]], первая прикидка [[M-unit-economics]] |
| DISCOVERY | [[M-competitors]] (догфудинг), [[M-benchmarking]], [[M-trends-scenarios]] | [[M-unit-economics]] |
| MVP | [[M-benchmarking]] (цели), [[M-competitors]], [[M-risks]] | bottom-up из [[M-traction-model]], [[M-unit-economics]], [[M-monetization]] |
| GROWTH | [[M-market-sizing]] (следующий сегмент), [[M-trends-scenarios]], [[M-goals-drivers-bets]] | полная [[M-traction-model]], эффекты, [[M-cannibalization]] |
| SCALE | [[M-market-sizing]] (новые рынки), [[M-external-environment]], [[M-pmf-scaling]] | валидация модели, [[M-monetization]] (включая аукцион), [[M-unit-economics]] |

## Шаблон / чек-лист
Маршрут для ответа руководителю:
| # | Карта | Зачем (вопрос) | Вход (данные, класс A–D) | Выход (артефакт) | Статус |
|---|---|---|---|---|---|
Чек-лист перед выдачей: цель и горизонт зафиксированы · маршрут объяснён пользователем в 2–3 фразах · каждая внешняя цифра с источником и классом · допущения вынесены списком · есть минимум один независимый шаг проверки (бенчмарк, триангуляция, валидация модели, риски) · указаны открытые вопросы, способные изменить вывод.

## Типичные ошибки
- Начинать с моделирования без рынка и источников; или бесконечно собирать рыночные данные без решения.
- Брать все карты подряд вместо минимального маршрута под вопрос.
- Не вернуться на раннюю карту, когда вывод опровергает исходные допущения (маршрут итеративен).
- Смешивать модель роста и фреймворк метрик: см. [[M-growth-frameworks]] и [[M-product-metrics]].
- Считать UE и модель до выбора бизнес-модели и монетизации ([[M-business-models]], [[M-monetization]]).

## Вопросы, которые могут изменить решение
- Какое решение примет руководитель по итогам и к какому сроку?
- Какая стадия у продукта (IDEA…SCALE) и есть ли операционные данные?
- Есть ли у пользователя данные, которые заменят внешние источники?
- Какие допущения дорого проверять и стоит ли вместо этого запустить пилот ([[M-mvp-pilots]])?
- Нужна ли защита перед инвесторами или внутренним комитетом (тогда добавить [[M-source-criticism]] и валидацию модели)?

## Связанные карты
[[M-product-context]], [[M-strategy-growth]], [[M-market-sizing]], [[M-traction-model]], [[M-unit-economics]], [[M-monetization]], [[M-business-models]], [[M-growth-frameworks]], [[M-benchmarking]], [[M-source-criticism]], [[M-trends-scenarios]], [[M-cannibalization]], [[M-risks]]
