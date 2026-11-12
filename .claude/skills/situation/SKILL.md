---
name: situation
description: Шаг 3. Проверяемая картина ситуации — что известно и откуда, чего мы не знаем и почему, противоречия, вопросы, которые могут изменить решение. Используй после исследования, до вариантов.
---

# Картина ситуации (02_situation.md)

Шаблон: `knowledge/templates/situation.md`. Карты: `M-source-criticism`, `M-product-metrics`, `M-jtbd`.

1. Собери активные утверждения: `pfs claim list`.
2. Разделы документа:
   - **Короткий ответ** (3–5 строк): что происходит, насколько уверены (сила доказательств).
   - **Что известно** — факты, сгруппированные по вопросам плана, каждый с [C###] и силой A–D.
   - **Гипотезы и прогнозы** — отдельно от фактов, с тем, что их подтвердило бы/опровергло.
   - **Чего мы не знаем** — пробел, почему не знаем, как узнать, во что обойдётся, влияет ли на решение.
   - **Противоречия источников** — как разрешили или почему оставили открытыми.
   - **Вопросы, которые могут изменить решение** — топ-3.
3. Выводы, которые ты делаешь из нескольких фактов, — `pfs claim add … --kind inference --from C001,C005`.
4. `pfs check` → исправь ошибки (числа без тегов, ссылки на отозванные C###). `pfs step situation done`.

## English

# Situation map (02_situation.md)

Template: `knowledge/templates/situation.md` (`knowledge/templates/en/situation.md` for `lang: en`).
Maps: `M-source-criticism`, `M-product-metrics`, `M-jtbd`.

1. Collect the active claims: `pfs claim list`.
2. Document sections:
   - **Quick answer** (3–5 lines): what is happening, how confident we are (evidence grade).
   - **What we know** — facts grouped by plan question, each with [C###] and a grade A–D.
   - **Hypotheses and forecasts** — separate from facts, with what would confirm/refute them.
   - **What we don't know** — the gap, why we don't know, how to find out, what it costs, whether it affects the decision.
   - **Contradictions between sources** — how they were resolved or why they stay open.
   - **Questions that could change the decision** — top 3.
3. Conclusions you draw from several facts — `pfs claim add … --kind inference --from C001,C005`.
4. `pfs check` → fix errors (numbers without tags, links to retracted C###). `pfs step situation done`.
