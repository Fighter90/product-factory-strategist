---
name: research
description: Шаги 1–2. Сбор материалов и исследование — план от вопросов, которые могут изменить решение, поиск в открытых источниках, регистрация источников, выписка утверждений с типом и силой доказательства, честные пробелы. Используй после подтверждения брифа или когда появились новые материалы.
---

# Сбор материалов и исследование

Карты: `M-research-types`, `M-source-criticism`, `M-external-environment`, `M-competitors`, `M-market-sizing`,
`M-benchmarking` + карты сценария из `pfs route`.

## План (01_research_plan.md, шаблон `knowledge/templates/research_plan.md`)
1. Сформулируй 5–8 **вопросов, которые могут изменить решение** (если ответ «да» — делаем X, если «нет» — Y).
   Для каждого: какая гипотеза, какой метод (desk, данные, интервью, UX-разбор, расчёт), какой источник, что будет
   считаться ответом, цена/время. Вопросы, ответ на которые не меняет решения, — вычеркни.
2. `pfs step sources in_progress`.

## Сбор
3. Для каждого вопроса: поиск (WebSearch) → открыть 1–3 лучших результата → `pfs source add <url> --published <дата>`.
   Предпочитай первоисточники: регуляторы, официальные отчёты компаний, статистику, исследования с методологией.
   Много чтения — отдай субагенту `researcher` (он возвращает выписки, а не пересказ).
4. Из каждого источника — утверждения: `pfs claim add "<одна мысль, с числом, единицей, периодом>" --kind fact
   --source S### --grade A|B|C|D --quote "<короткая цитата ≤15 слов>"`. Прогнозы и оценки аналитиков — `forecast`.
5. Противоречия между источниками не сглаживай: запиши оба утверждения и `pfs question "Расхождение C004 vs C009: …"`.
6. Пробел (данных нет/закрыты/платные) → `pfs question "<пробел> — почему не знаем — как узнать"`.

## Проверка
7. По каждому вопросу плана — статус: отвечен (C###), частично, пробел. Если ≥2 ключевых вопроса — пробел, скажи
   руководителю, что это значит для решения, и предложи способ закрыть (данные, интервью, тест).
8. `pfs step research done --next "Собрать картину ситуации"`.

## English

# Sources and research

Maps: `M-research-types`, `M-source-criticism`, `M-external-environment`, `M-competitors`, `M-market-sizing`,
`M-benchmarking` + the scenario maps from `pfs route`. Template: `knowledge/templates/research_plan.md`
(`knowledge/templates/en/research_plan.md` for `lang: en` projects).

## Plan (01_research_plan.md)
1. Formulate 5–8 **questions that could change the decision** (if "yes" → we do X, if "no" → Y). For each: which
   hypothesis, which method (desk, data, interviews, UX review, calculation), which source, what counts as an answer,
   cost/time. Strike out questions whose answers cannot change the decision.
2. `pfs step sources in_progress`.

## Collection
3. For each question: search (WebSearch) → open 1–3 of the best results → `pfs source add <url> --published <date>`.
   Prefer primary sources: regulators, official company reports, statistics, research with a stated methodology.
   Heavy reading — hand to the `researcher` subagent (it returns extracts, not a retelling).
4. From each source — claims: `pfs claim add "<one thought, with a number, unit, period>" --kind fact
   --source S### --grade A|B|C|D --quote "<short quote ≤15 words>"`. Analyst forecasts and estimates — `forecast`.
5. Do not smooth over contradictions between sources: record both claims and `pfs question "C004 vs C009 discrepancy: …"`.
6. A gap (no data / closed / paid) → `pfs question "<gap> — why we don't know — how to find out"`.

## Verification
7. For each plan question — status: answered (C###), partial, gap. If ≥2 key questions are gaps, tell the leader what
   that means for the decision and propose a way to close them (data, interviews, a test).
8. `pfs step research done --next "Assemble the situation map"`.
