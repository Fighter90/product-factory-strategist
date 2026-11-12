---
name: intake
description: Шаг 0. Постановка задачи — превращает размытый запрос руководителя продукта в бриф: вопрос, решение, цель, получатель, ограничения, данные. Используй в начале любого нового проекта стратега или когда пользователь меняет задачу.
---

# Постановка задачи (intake)

Карты: `M-brief-hypotheses`, `M-product-context`, `M-problem-design`.

1. Перечитай запрос дословно. Выдели: объект (продукт/сервис), симптом, неявную гипотезу автора, решение, которое
   за этим стоит («что будет сделано по итогам»).
2. Заполни `outputs/00_brief.md` тем, что уже известно. Неизвестное оставь «?».
3. Задай **не больше 3 вопросов** — только те, без ответа на которые следующий шаг пойдёт не туда. Приоритет:
   (а) какое решение и кем будет принято; (б) кто получатель и в каком формате; (в) какие данные/материалы есть
   (метрики, исследования, интерфейсы) и какие ограничения (сроки, бюджет, регуляторика, бренд).
   Каждый вопрос — с вариантами и твоим предположением по умолчанию: «Если не ответите, считаю, что …».
   Запиши: `pfs ask "<вопросы>" --options "..."`.
4. Получив ответ: `pfs answer "…"`, обнови бриф, перечисли **допущения** (`pfs claim add … --kind assumption`).
5. Зарегистрируй материалы пользователя: `pfs source add <файл> --origin own`.
6. Покажи бриф одним экраном и попроси подтверждения. Затем `pfs step intake done --next "Собрать источники и составить план исследования"`.

Нельзя: начинать исследование без подтверждённого вопроса; задавать вопросы, ответ на которые можно найти самому.

## English

# Intake (problem framing)

Maps: `M-brief-hypotheses`, `M-product-context`, `M-problem-design`.

1. Re-read the request verbatim. Extract: the object (product/service), the symptom, the author's implicit
   hypothesis, and the decision behind it ("what will be done with the result").
2. Fill `outputs/00_brief.md` with what is already known. Leave "?" for the unknowns.
3. Ask **no more than 3 questions** — only those without which the next step goes the wrong way. Priority:
   (a) which decision, and who makes it; (b) who receives the result and in what format; (c) what data/materials
   exist (metrics, research, interfaces) and what the constraints are (deadline, budget, regulation, brand).
   Each question comes with options and your default assumption: "If you don't answer, I will assume …".
   Record it: `pfs ask "<questions>" --options "..."`.
4. On the answer: `pfs answer "…"`, update the brief, list the **assumptions** (`pfs claim add … --kind assumption`).
5. Register the user's materials: `pfs source add <file> --origin own`.
6. Show the brief on one screen and ask for confirmation. Then
   `pfs step intake done --next "Collect sources and draft the research plan"`.

Never: start research without a confirmed question; ask questions you could answer yourself.
