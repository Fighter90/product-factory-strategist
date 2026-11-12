---
name: options
description: Шаг 4–5. Не меньше трёх содержательно разных вариантов, включая «оставить как есть» и «закрыть/свернуть направление», с сильными возражениями, экономикой и условиями, при которых вариант верен; затем выбор руководителя. Используй после картины ситуации.
---

# Варианты и выбор (03_options.md)

Шаблон: `knowledge/templates/options.md`. Карты: `M-goals-drivers-bets`, `M-solution-design`, `M-business-models`,
`M-unit-economics`, `M-risks`, `M-strategy-growth`.

1. Сгенерируй 5–7 кандидатов, затем оставь 3–5 **содержательно разных** (разная ставка: сегмент, ценность, модель
   монетизации, канал, масштаб инвестиций), а не вариации одного. Обязательно:
   - `Вариант A: Оставить как есть` — что будет, если ничего не делать (базовый прогноз, а не «ноль»);
   - вариант выхода: закрыть/свернуть/передать направление.
2. Для каждого варианта (`## Вариант X: …`): суть; для кого и какую задачу решает; что должно быть правдой
   (ключевые допущения [C###]); ожидаемый эффект с диапазоном и типом (forecast); затраты и влияние на доходы;
   риски; **Возражения** (2–4 сильных, сформулированных так, как сказал бы умный скептик); что опровергло бы вариант.
3. Отдай документ субагенту `red-team`. Его возражения внеси в варианты; если возражение рушит вариант — скажи прямо.
4. Таблица сравнения по 4–6 критериям, вытекающим из цели брифа (не придумывай веса без основания — покажи их).
5. Рекомендация + условия, при которых рекомендация меняется. `pfs check`.
6. Выбор: `pfs ask "Какой вариант берём в стратегию?" --options "A,B,C,…"` → остановись → после ответа
   `pfs answer`, `pfs step choice done`.

## English

# Options and choice (03_options.md)

Template: `knowledge/templates/options.md` (`knowledge/templates/en/options.md` for `lang: en`).
Maps: `M-goals-drivers-bets`, `M-solution-design`, `M-business-models`, `M-unit-economics`, `M-risks`,
`M-strategy-growth`.

1. Generate 5–7 candidates, then keep 3–5 that are **meaningfully different** (a different bet: segment, value,
   monetization model, channel, investment scale), not variations of one. Mandatory:
   - `Option A: Keep as is` — what happens if we do nothing (the base forecast, not "zero");
   - an exit option: shut down / wind down / hand off the direction.
2. For each option (`## Option X: …`): the essence; for whom and which job it solves; what would have to be true
   (key assumptions [C###]); the expected effect with a range and type (forecast); costs and revenue impact;
   risks; **Objections** (2–4 strong ones, phrased the way a smart skeptic would); what would refute the option.
3. Hand the document to the `red-team` subagent. Fold its objections into the options; if an objection destroys an
   option — say so directly.
4. A comparison table on 4–6 criteria derived from the brief's goal (don't invent weights without grounds — show them).
5. Recommendation + the conditions under which the recommendation changes. `pfs check`.
6. The choice: `pfs ask "Which option goes into the strategy?" --options "A,B,C,…"` → stop → after the answer
   `pfs answer`, `pfs step choice done`.
