---
name: validation-plan
description: Шаг 7. План проверки стратегии — ожидаемое изменение, с чем сравниваем, срок наблюдения, нежелательные последствия (контрметрики), критерии продолжить/изменить/остановить. Используй после стратегии и при подготовке пилота или эксперимента.
---

# План проверки (06_validation_plan.md)

Шаблон: `knowledge/templates/validation_plan.md`. Карты: `M-mvp-pilots`, `M-product-metrics`, `M-quant-methods`,
`M-success-metrics`, `M-pmf-scaling`.

Для каждой ключевой гипотезы стратегии (3–5 штук, самые рискованные — первыми):
1. **Ожидаемое изменение** — метрика, направление, величина (диапазон), единица, период; почему ожидаем [C###].
2. **С чем сравниваем** — контрольная группа / A/B / до-после с поправкой на сезонность / синтетический контроль;
   базовое значение [C###] и как его получить, если неизвестно.
3. **Срок наблюдения** — сколько нужно, чтобы эффект проявился (цикл использования, оплата, продление) и набралась
   выборка (оценка размера выборки: карта `M-quant-methods`).
4. **Нежелательные последствия** — контрметрики (каннибализация, отток, нагрузка на поддержку, жалобы, бренд),
   пороги, при которых останавливаем.
5. **Критерии решения** — заранее: «продолжаем, если …; меняем, если …; останавливаем, если …».
6. Тип проверки (MVP/пилот/фейковая дверь/опрос/интервью), стоимость, ответственный.
`pfs check` → `pfs step validation done`.

## English

# Validation plan (06_validation_plan.md)

Template: `knowledge/templates/validation_plan.md` (`knowledge/templates/en/validation_plan.md` for `lang: en`).
Maps: `M-mvp-pilots`, `M-product-metrics`, `M-quant-methods`, `M-success-metrics`, `M-pmf-scaling`.

For each key strategy hypothesis (3–5 items, the riskiest first):
1. **Expected change** — metric, direction, magnitude (range), unit, period; why we expect it [C###].
2. **Comparison baseline** — control group / A/B / before-after adjusted for seasonality / synthetic control;
   the base value [C###] and how to get it if unknown.
3. **Observation window** — how long until the effect shows (usage, payment, renewal cycle) and the sample fills up
   (sample-size estimate: map `M-quant-methods`).
4. **Counter-metrics** — cannibalization, churn, support load, complaints, brand; the thresholds at which we stop.
5. **Decision criteria** — fixed in advance: "continue if …; change if …; stop if …".
6. Test type (MVP/pilot/fake door/survey/interviews), cost, owner.
`pfs check` → `pfs step validation done`.
