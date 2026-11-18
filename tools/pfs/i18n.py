"""i18n: язык проекта и словарь сообщений CLI (PRO-57).

Язык хранится в `projects/<slug>/project.json → lang` (`pfs new --lang en|ru`,
переключение активного проекта — `pfs lang en`). По умолчанию и для старых проектов
без поля lang — `ru`: их вывод не меняется. Для `en` сообщения status/next/check,
ошибки и отчёты печатаются на английском, а `pfs check` берёт EN-заголовки из
`config/quality_gate.json → "en"`.

RU-строки словаря дословно совпадают с прежними литералами — обратная совместимость.
"""
from __future__ import annotations

import json
from pathlib import Path

LANGS = ("ru", "en")

STR: dict[str, dict[str, str]] = {
    # ---------- check ----------
    "ru": {
        "check_header": "Контроль качества: {score}/100 | ошибок {errors}, предупреждений {warnings}",
        "check_passed": "✔ Без ошибок: {names}",
        "check_more_warnings": "… ещё {n} предупреждений",
        "err_no_section": "{name}: нет раздела «{sec}»",
        "err_unknown_claim": "{name}:{i}: ссылка на несуществующее {tid}",
        "err_claim_status": "{name}:{i}: {tid} {status} — обновите формулировку",
        "err_claim_superseded_by": "замена: {by}",
        "err_unknown_source": "{name}:{i}: ссылка на несуществующий источник {tid}",
        "err_unknown_decision": "{name}:{i}: ссылка на несуществующее решение {tid}",
        "err_too_few_options": "{name}: вариантов {n}, нужно не меньше {m}",
        "err_no_status_quo": "{name}: нет варианта «оставить как есть»",
        "err_option_section": "{name}: у варианта №{idx} нет раздела «{sec}»",
        "err_promise_table_empty": "{name}: таблица «обещание → чем подтверждено в продукте» пуста",
        "err_promise_no_tag": "{name}: обещание без подтверждения (нет C###/S###): «{row}»",
        "err_fact_no_source": "{cid}: факт без источника",
        "err_fact_synthetic": "{cid}: факт опирается только на синтетические ответы",
        "err_fact_grade_d": "{cid}: сила D не может быть фактом — переведите в допущение",
        "err_calcs_mismatch": "{name}:{i}: {metric} = {num} не сходится с calcs.json (пересчёт из calcs: ≈ {expected}) — исправьте число или calcs.json",
        "warn_doc_missing": "{name}: документа ещё нет",
        "warn_number_no_tag": "{name}:{i}: число без ссылки на C###/S###: «{line}»",
        "warn_brief_open": "00_brief.md: поля с «?» ({rows}) — ответы intake не заполнены; заполните бриф или отвечайте pfs answer на вопросы про решение/цель/ограничения",
        "warn_no_exit_option": "{name}: не рассмотрен вариант «закрыть/свернуть направление»",
        "warn_stale_grounds": "{cid}: основания {stale} замещены/отозваны — пересмотрите вывод (pfs claim supersede --from …)",
        "warn_no_grounds": "{cid}: {kind} без оснований — укажите, откуда она",
        "warn_injection": "Источники с фразами-инструкциями (проигнорированы как команды): {ids}",
        "warn_source_404": "Источники-страницы 404/403 («битая» ссылка, тело — страница ошибки, а не контент): "
                           "{ids} — замените живым источником или выпиской "
                           "(pfs source add --text-file <файл> --url <ссылка> --excerpt)",
        "warn_weak_content": "Источники с пометкой «мало содержательного текста» (навигационная оболочка или текст без предложений): {ids} — проверьте sources/<S###> и при необходимости замените выпиской (pfs source add --text-file --excerpt)",
        "warn_excerpt_only": "{cid}: опирается только на выписки ({sources}) — сила не выше C, перепроверьте "
                             "первоисточник (pfs source refresh <S###>) или добавьте публичный источник",
        "warn_en_sync": "SIX_PAGER_EN.md отстал от RU: нет источников/сносок {tags} — EN-версия пишется агентом "
                        "из того же пакета данных (spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_en_cyrillic": "SIX_PAGER_EN.md:{lines}: кириллица ({n} стр.): «{sample}» — EN-версия "
                            "пишется по-английски из того же пакета данных, RU-текст не вставляется "
                            "(spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_en_dec_comma": "SIX_PAGER_EN.md:{lines}: русская десятичная запятая ({n} стр.): "
                             "«{sample}» — в EN числа пишутся 1,234.5: точка — разделитель, "
                             "запятая отделяет тысячи",
        "warn_en_translate_marker": "SIX_PAGER_EN.md:{lines}: маркер «[RU source — translate]» "
                                    "({n} шт.): «{sample}» — EN-версия пишется, а не переводится "
                                    "(spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_num_title_mismatch": "{cid}/{sid}: числа заголовка источника ({tnums}) не совпадают с числами утверждения ({cnums}); число подтверждено текстом sources/{sid}.md — возможно, разные показатели",
        "warn_num_serious": "{cid}/{sid}: числа утверждения ({cnums}) не совпадают с числами заголовка источника ({tnums}) и отсутствуют в его тексте — серьёзное расхождение, сверьте утверждение с источником",
        "warn_quote_numbers": "{cid}/{sid}: числа из цитаты ({nums}) отсутствуют в тексте источника — проверьте цитату против sources/{sid}.md",
        "warn_banned_term": "{name}: «{term}» — жаргон/англицизм, по стайлгайду (STYLE_RU.md) пишите «{instead}»",
        "warn_abbrev_undecoded": "{name}: «{term}» без расшифровки при первом упоминании — напишите «{term} — {hint}»",
        # ---------- PRO-47: линтер содержания six-pager ----------
        "err_sp_no_section": "SIX_PAGER.md: нет раздела «{sec}» (эталон: knowledge/templates/SIX_PAGER_PROMPT.md)",
        "err_sp_bad_order": "SIX_PAGER.md: разделы FAQ не по порядку: {order}",
        "err_sp_extra_h2": "SIX_PAGER.md:{i}: лишний раздел H2: «{head}»",
        "err_sp_no_subpoint": "SIX_PAGER.md: в {faq} нет подпункта «{sub}»",
        "err_sp_working_heading": "SIX_PAGER.md:{i}: лишний заголовок из рабочего документа: «{head}»",
        "err_sp_words": "SIX_PAGER.md: объём основного текста {n} слов — больше порога {m}",
        "err_sp_template": "SIX_PAGER.md:{i}: остаток шаблона «{marker}»",
        "err_sp_dots_cell": "SIX_PAGER.md:{i}: таблица не заполнена (ячейки «…»)",
        "err_sp_ragged": "SIX_PAGER.md:{i}: в строке таблицы {n} ячеек, а в заголовке {m}",
        "err_sp_empty_required": "SIX_PAGER.md:{i}: пусто или «—» в столбце «{col}»",
        "err_sp_dup_col": "SIX_PAGER.md:{i}: столбец «{col}» дословно повторяет соседний",
        "err_sp_glue": "SIX_PAGER.md:{i}: склейка «текст. → …» в ячейке таблицы",
        "err_sp_service_id": "SIX_PAGER.md:{i}: служебный ID без расшифровки ({name}): {ids}",
        "err_sp_contrib_sum": "SIX_PAGER.md: вклад инициатив в сумме {n}% — должно быть {m}%",
        "err_sp_metric_mismatch": "SIX_PAGER.md: «{label}» различается между разделами: {values}",
        "err_sp_calc_mismatch": "SIX_PAGER.md:{i}: расчёт не сходится: {expr}, а в результате {res}",
        "err_sp_footnote_not_listed": "SIX_PAGER.md: в тексте есть сноски {ids}, которых нет в списке источников",
        "err_sp_footnote_not_cited": "SIX_PAGER.md: в списке источников лишние сноски (не процитированы в тексте): {ids}",
        "err_sp_no_footnotes": "SIX_PAGER.md: в тексте есть сноски {ids}, но нет раздела «Источники (сноски)»",
        "err_sp_cyrillic": "{name}:{lines}: кириллица ({n} стр.): «{sample}» — документ комитета пишется на языке своей версии",
        "err_sp_banned_term": "SIX_PAGER.md:{i}: «{term}» — англицизм вне белого списка глоссария, пишите «{instead}»",
        "warn_sp_long_para": "SIX_PAGER.md:{i}: абзац {n} слов — больше {m}, разбейте",
        "warn_sp_wide_table": "SIX_PAGER.md:{i}: таблица {n} столбцов — больше {m}",
        "kind_fact": "факт", "kind_hypothesis": "гипотеза", "kind_forecast": "прогноз",
        "kind_assumption": "допущение", "kind_inference": "вывод",
        # ---------- status ----------
        "status_project": "ПРОЕКТ: {title}  [{slug}]",
        "status_question": "Запрос: {question}",
        "status_steps": "Шаги: {bar}",
        "status_stage": "Текущий шаг: {stage} | Следующее действие: {next}",
        "status_autopilot": "Режим автопрогона (PFS_AUTOPILOT=1): на паузах принимается рекомендованный "
                            "вариант, каждая пауза и ответ логируются.",
        "status_awaiting": "⏸ ЖДЁМ РЕШЕНИЯ РУКОВОДИТЕЛЯ: {question}.{options}",
        "status_options": " Варианты: {options}",
        "status_open_questions": "Открытые вопросы: {items}",
        "status_counts": "Источники: {sources} | Утверждения: {claims} {by_kind} | Решения: {decisions}",
        "status_cost_plan": "Стоимость: ${usd:.2f} — подписочный план; эквивалент по API-ценам "
                            "${usd_eq:.2f} (~{rub_eq:.0f} ₽), токенов {tokens}",
        "status_cost": "Стоимость: ${usd:.2f} (~{rub:.0f} ₽), токенов {tokens}",
        "status_recent": "Последние действия:",
        "status_documents": "Документы: {docs}",
        # ---------- next ----------
        "next_header": "ЧТО РЕШАТЬ СЕЙЧАС — {title} [{slug}]",
        "next_stage": "Шаг: {stage} · Далее: {next}",
        "next_finished": "✔ Процесс завершён. Доступно: мониторинг, правки, презентация — "
                         "по запросу, без автозапуска.",
        "next_finish_hint": "📦 Финальный пакет не собран: pfs finish (check → Excel → REPORT → "
                            "six-pager RU/EN → DOCX → дека) — одно сообщение со ссылками закрывает прогон.",
        "next_sixpager": "📋 Собрать комитет-пакет: pfs calc scaffold → pfs calc all → pfs export "
                         "--six-pager (spec: {spec})",
        "next_waiting": "⏸ Ждём вашего ответа: {question}{options}",
        "next_overdue": "⏰ Просроченные обязательства: {n}",
        "next_stale_sources": "♻ Источники в основаниях решений не проверялись дольше {days} дн.:",
        "next_stale_grounds": "⚠ Устаревшие основания: {n} — pfs decision rebase / claim supersede",
        "next_review_now": "🔎 К пересмотру решений: {ids}",
        "next_review_soon": "📅 Пересмотр в ближайшие 14 дней: {items}",
        "next_open_questions": "❓ Открытые вопросы: {n}",
        "next_clear": "Долгов нет. Текущий шаг процесса — см. pfs status.",
        "next_refresh": "Обновить источники после изменений: pfs source refresh <S###>",
        # ---------- cli / ошибки ----------
        "error_prefix": "Ошибка: {msg}",
        "err_project_exists": "Проект '{slug}' уже существует — продолжите его: pfs use {slug} && pfs status",
        "err_unknown_step": "Неизвестный шаг '{step}'. Шаги: {stages}",
        "err_bad_status": "Статус: pending | in_progress | done | skipped",
        "new_created": "Создан проект {slug}. Следующий шаг: intake — уточнить запрос (см. {agents}).",
        "step_marked": "Шаг {step} → {status}. Текущий: {stage}. Далее: {next}",
        "step_cards": "Карты шага: {cards}",
        "err_not_tabular": "Файл не табличный — ожидается CSV/XLSX: {path} ({exc}). Пример: pfs data profile events.csv --save profile",
        "claims_table_header": "| ID | Тип | Утверждение | Источники / основания | Сила | Статус |",
        "decisions_table_header": "| ID | Решение | Ответственный | Основания | Показатели | Пересмотр | Статус |",
        "pack_claims_title": "## Утверждения (сила A–D)",
        "pack_claims_header": "| ID | Тип | Сила | Утверждение | Источники |",
        "pack_sources_title": "## Источники",
        "pack_sources_header": "| ID | Название | Где | Происхождение | Дата |",
        "route_scenario": "Сценарий: {scenario} — {title} (уверенность: {confidence})",
        "route_secondary": "Смежные сценарии: {secondary}",
        "route_low_conf": "⚠ Низкая уверенность: задайте руководителю уточняющий вопрос о цели или исправьте: --override <сценарий>",
        "route_cards": "Методические карты (читать в этом порядке): {cards}",
        "route_questions": "Вопросы, которые могут изменить решение:",
        "route_models": "План моделей по шагам:",
        "source_added": "Добавлен: {sid} — {title} ({chars} зн.){flag}",
        "source_dup": "Уже есть (повтор пропущен): {sid} — {title} ({chars} зн.){flag}",
        "source_fetch_added": "Добавлен: {sid} — {title} ({chars} зн.); канал: {via}; origin: {origin}{flag}",
        "source_fetch_dup": "Уже есть (повтор пропущен): {sid} — {title} ({chars} зн.); канал: {via}; origin: {origin}{flag}",
        "source_ext_warn": "⚠ Файл лежал вне проекта ({external}) — копия сохранена в {path}. Материал должен быть явно передан пользователем.",
        "claim_recorded": "{cid} [{kind}] записано",
        "batch_created": "Батч: создано {n}, дубликаты пропущены {m}",
        "batch_new": "Новые: {ids}",
        "decision_recorded": "{did} записано",
        "ask_recorded": "Вопрос записан. Агент ждёт ответа руководителя (pfs answer \"…\").",
        "answer_recorded": "Ответ записан.",
        "ask_hint": "Задать руководителю: pfs ask \"<вопрос>\" --options \"A,B,C\"",
        "roadmap_built": "Роудмап: {roadmap} (обе раскладки: «Проекты» и «Фичи по проектам»)",
        "roadmap_not_built": "Роудмап не собран: {exc}",
        "kind_fact": "факт",
        "kind_hypothesis": "гипотеза",
        "kind_forecast": "прогноз",
        "kind_assumption": "допущение",
        "kind_inference": "вывод",
        "ask_autopilot": "PFS_AUTOPILOT=1: пауза принимает рекомендованный вариант — ответьте сами "
                         "(pfs answer \"<вариант>\") и продолжайте без ожидания.",
        "lang_current": "Язык проекта: {lang} — инструкции: {agents}, шаблоны: {templates}, "
                        "проверки: {gate}",
        "lang_set": "Язык проекта: {lang} (было: {old}) — инструкции: {agents}, шаблоны: {templates}, "
                    "проверки: {gate}",
        # ---------- REPORT.md (pfs export) ----------
        "report_title": "# {title}: стратегия и обоснование",
        "report_built": "> Собрано {ts} командой `pfs export`. Теги [C###] — утверждения, "
                        "[S###] — источники, [D###] — решения (см. приложения).",
        "report_sixpager_note": "> Авто-черновик: собран командой `pfs export --six-pager`; "
                                "детализируйте по spec — {spec}.\n\n",
        "appx_a_claims": "# Приложение A. Реестр утверждений",
        "appx_b_sources": "# Приложение B. Источники",
        "appx_sources_header": "| ID | Название | Ссылка / файл | Происхождение | Получено |",
        "appx_c_decisions": "# Приложение C. Решения и обязательства",
        "appx_d_transparency": "# Приложение D. Прозрачность",
        "appx_e_excel": "# Приложение E. Excel-расчёты",
        # ---------- cost.summary_text ----------
        "cost_total": "Итого: фактически ${usd:.2f} (~{rub:.0f} ₽) "
                      "| эквивалент по API-ценам ${usd_eq:.2f} (~{rub_eq:.0f} ₽) "
                      "| сессий {sessions} | токенов {tokens} "
                      "| время сессий {tmin:.0f} мин "
                      "| время человека {hmin:.0f} мин",
        "cost_plan": "подписочный план ({prov}): фактическая оплата ${usd:.2f} — покрыта "
                     "подпиской; эквивалент по API-ценам ${usd_eq:.2f} — сколько "
                     "стоили бы те же токены по прайсу провайдера",
        "cost_plan_default": "подписка",
        "cost_by_models": "По моделям:",
        "cost_by_model_row": "  {model:<24} ${usd:.2f} | токены {tokens} "
                             "(вход {inp} · выход {outp} "
                             "· кэш {cr}/{cw})",
        "cost_by_steps": "По шагам:",
        "cost_by_step_row": "  {step:<12} токены {tokens} · эквивалент ${usd:.2f}",
        "cost_retries": "Повторы: {n} {word}{tail}",
        "cost_retries_tail_tokens": " · {tokens} токенов",
        "cost_retries_tail_unknown": " · токены неизвестны (агрегат сессии)",
        "cost_retries_tail_equiv": " · эквивалент ${usd:.2f}",
        "cost_plan_share": "доля подписки ({head}${month_usd:g}/мес × {days} дн): ${usd:.2f}",
        # ---------- finish.summary_text ----------
        "finish_built": "Собрано ({n}):",
        "finish_missing_docs": "Нет документов (заглушки в six-pager/REPORT): ",
        "finish_all_docs": "Документы 00–07: все на месте",
        "finish_stale": "До сборки реестр менялся — снято свежей пересборкой: ",
        "finish_gate_error": "pfs finish: автопроверка нашла ошибки — пакет не собран:\n- {errs}"
                             "\nИсправьте (pfs check) и повторите: pfs finish",
        # ---------- participate ----------
        "err_need_persona_topic": "Укажите персону и тему интервью",
        "err_guide_template_missing": "Шаблон гайда не найден: {tpl}",
        "guide_title": "# Гайд интервью: {topic}",
        "guide_meta": "- Персона: {persona}\n- Тема: {topic}\n- Дата: {date}",
        "guide_note": "> Каркас вопросов — заполните агентом до сессии. Ответы ИИ-респондентов\n"
                      "> (interviews/synthetic) дают только гипотезы и не доказывают спрос.",
        "ab_no_hypothesis": "⚠ В реестре нет активных гипотез и в 06 нет «Гипотеза N» — секция «Гипотеза» "
                            "оставлена заглушкой: сформулируйте (pfs claim add … --kind hypothesis) и перезапустите "
                            "на новом проекте или допишите документ вручную.",
    },
    "en": {
        "check_header": "Quality check: {score}/100 | errors {errors}, warnings {warnings}",
        "check_passed": "✔ No errors: {names}",
        "check_more_warnings": "… {n} more warnings",
        "err_no_section": "{name}: missing section \"{sec}\"",
        "err_unknown_claim": "{name}:{i}: reference to unknown {tid}",
        "err_claim_status": "{name}:{i}: {tid} is {status} — update the wording",
        "err_claim_superseded_by": "superseded by: {by}",
        "err_unknown_source": "{name}:{i}: reference to unknown source {tid}",
        "err_unknown_decision": "{name}:{i}: reference to unknown decision {tid}",
        "err_too_few_options": "{name}: {n} options found, at least {m} required",
        "err_no_status_quo": "{name}: no \"keep as is\" option",
        "err_option_section": "{name}: option #{idx} lacks the \"{sec}\" section",
        "err_promise_table_empty": "{name}: the \"promise → product backing\" table is empty",
        "err_promise_no_tag": "{name}: promise without backing (no C###/S###): \"{row}\"",
        "err_fact_no_source": "{cid}: fact without a source",
        "err_fact_synthetic": "{cid}: fact rests only on synthetic answers",
        "err_fact_grade_d": "{cid}: grade D cannot be a fact — make it an assumption",
        "err_calcs_mismatch": "{name}:{i}: {metric} = {num} does not match calcs.json (recomputed from calcs: ≈ {expected}) — fix the number or calcs.json",
        "warn_doc_missing": "{name}: document not written yet",
        "warn_number_no_tag": "{name}:{i}: number without a C###/S### tag: \"{line}\"",
        "warn_brief_open": "00_brief.md: fields with \"?\" ({rows}) — intake answers not filled; complete the brief or answer pfs ask questions about the decision/goal/constraints",
        "warn_no_exit_option": "{name}: the \"shut down / wind down the direction\" option is not considered",
        "warn_stale_grounds": "{cid}: grounds {stale} superseded/retracted — revisit the conclusion (pfs claim supersede --from …)",
        "warn_no_grounds": "{cid}: {kind} without grounds — state where it comes from",
        "warn_injection": "Sources containing instruction phrases (ignored as commands): {ids}",
        "warn_source_404": "Sources that returned a 404/403 page (broken link — the body is an error page, not "
                           "content): {ids} — replace with a live source or an excerpt "
                           "(pfs source add --text-file <file> --url <link> --excerpt)",
        "warn_weak_content": "Sources flagged low-content (nav shell or text without sentences): {ids} — check sources/<S###> and replace with an excerpt if needed (pfs source add --text-file --excerpt)",
        "warn_excerpt_only": "{cid}: rests only on excerpts ({sources}) — strength capped at C; re-verify the "
                             "original (pfs source refresh <S###>) or add a public source",
        "warn_en_sync": "SIX_PAGER_EN.md lags behind RU: missing source footnotes {tags} — the EN six-pager is "
                        "written by the agent from the same data package (spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_en_cyrillic": "SIX_PAGER_EN.md:{lines}: Cyrillic text ({n} lines): \"{sample}\" — the EN "
                            "six-pager is written in English from the same data package; RU text is never "
                            "pasted (spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_en_dec_comma": "SIX_PAGER_EN.md:{lines}: Russian decimal comma ({n} lines): \"{sample}\" — "
                             "EN numbers read 1,234.5: the dot is the decimal separator, the comma "
                             "separates thousands",
        "warn_en_translate_marker": "SIX_PAGER_EN.md:{lines}: marker \"[RU source — translate]\" ({n}): "
                                    "\"{sample}\" — the EN six-pager is written, not translated "
                                    "(spec: knowledge/templates/SIX_PAGER_PROMPT_EN.md)",
        "warn_num_title_mismatch": "{cid}/{sid}: numbers in the source title ({tnums}) do not match the claim numbers ({cnums}); the number is confirmed by the text of sources/{sid}.md — possibly different metrics",
        "warn_num_serious": "{cid}/{sid}: claim numbers ({cnums}) do not match the source title numbers ({tnums}) and are absent from its text — serious discrepancy, verify the claim against the source",
        "warn_quote_numbers": "{cid}/{sid}: numbers from the quote ({nums}) are absent from the source text — check the quote against sources/{sid}.md",
        "warn_banned_term": "{name}: '{term}' is banned jargon — write '{instead}' per the style guide",
        "warn_abbrev_undecoded": "{name}: '{term}' is not decoded at first mention — write '{term} — {hint}'",
        # ---------- PRO-47: six-pager content linter ----------
        "err_sp_no_section": "SIX_PAGER.md: missing section \"{sec}\" (reference: knowledge/templates/SIX_PAGER_PROMPT.md)",
        "err_sp_bad_order": "SIX_PAGER.md: FAQ sections out of order: {order}",
        "err_sp_extra_h2": "SIX_PAGER.md:{i}: extra H2 section: \"{head}\"",
        "err_sp_no_subpoint": "SIX_PAGER.md: {faq} lacks subpoint \"{sub}\"",
        "err_sp_working_heading": "SIX_PAGER.md:{i}: extra heading from a working document: \"{head}\"",
        "err_sp_words": "SIX_PAGER.md: main text is {n} words — over the {m}-word limit",
        "err_sp_template": "SIX_PAGER.md:{i}: template leftover \"{marker}\"",
        "err_sp_dots_cell": "SIX_PAGER.md:{i}: unfilled table («…» cells)",
        "err_sp_ragged": "SIX_PAGER.md:{i}: table row has {n} cells, header has {m}",
        "err_sp_empty_required": "SIX_PAGER.md:{i}: empty or «—» cell in the \"{col}\" column",
        "err_sp_dup_col": "SIX_PAGER.md:{i}: column \"{col}\" verbatim repeats its neighbour",
        "err_sp_glue": "SIX_PAGER.md:{i}: glued cell «text. → …»",
        "err_sp_service_id": "SIX_PAGER.md:{i}: service ID without decoding ({name}): {ids}",
        "err_sp_contrib_sum": "SIX_PAGER.md: initiative contributions sum to {n}% — must be {m}%",
        "err_sp_metric_mismatch": "SIX_PAGER.md: \"{label}\" differs between sections: {values}",
        "err_sp_calc_mismatch": "SIX_PAGER.md:{i}: calculation does not add up: {expr}, but the result says {res}",
        "err_sp_footnote_not_listed": "SIX_PAGER.md: footnotes {ids} are cited but missing from the source list",
        "err_sp_footnote_not_cited": "SIX_PAGER.md: extra footnotes in the source list (not cited in the text): {ids}",
        "err_sp_no_footnotes": "SIX_PAGER.md: footnotes {ids} are cited but there is no \"Sources (footnotes)\" section",
        "err_sp_cyrillic": "{name}:{lines}: Cyrillic text ({n} lines): \"{sample}\" — each committee document is written in its own language",
        "err_sp_banned_term": "SIX_PAGER.md:{i}: \"{term}\" is an anglicism outside the glossary whitelist — write \"{instead}\"",
        "warn_sp_long_para": "SIX_PAGER.md:{i}: paragraph of {n} words — over {m}, split it",
        "warn_sp_wide_table": "SIX_PAGER.md:{i}: table with {n} columns — over {m}",
        "kind_fact": "fact", "kind_hypothesis": "hypothesis", "kind_forecast": "forecast",
        "kind_assumption": "assumption", "kind_inference": "inference",
        "status_project": "PROJECT: {title}  [{slug}]",
        "status_question": "Request: {question}",
        "status_steps": "Steps: {bar}",
        "status_stage": "Current step: {stage} | Next action: {next}",
        "status_autopilot": "Autopilot mode (PFS_AUTOPILOT=1): pauses take the recommended option, "
                            "every pause and answer is logged.",
        "status_awaiting": "⏸ AWAITING THE LEADER'S DECISION: {question}.{options}",
        "status_options": " Options: {options}",
        "status_open_questions": "Open questions: {items}",
        "status_counts": "Sources: {sources} | Claims: {claims} {by_kind} | Decisions: {decisions}",
        "status_cost_plan": "Cost: ${usd:.2f} — subscription plan; API-price equivalent "
                            "${usd_eq:.2f} (~{rub_eq:.0f} ₽), tokens {tokens}",
        "status_cost": "Cost: ${usd:.2f} (~{rub:.0f} ₽), tokens {tokens}",
        "status_recent": "Recent activity:",
        "status_documents": "Documents: {docs}",
        "next_header": "WHAT TO DECIDE NOW — {title} [{slug}]",
        "next_stage": "Step: {stage} · Next: {next}",
        "next_finished": "✔ Process complete. Available on request: monitoring, edits, presentation — "
                         "nothing starts automatically.",
        "next_finish_hint": "📦 The final package is not built: pfs finish (check → Excel → REPORT → "
                            "six-pager RU/EN → DOCX → deck) — one message with links closes the run.",
        "next_sixpager": "📋 Assemble the committee pack: pfs calc scaffold → pfs calc all → pfs export "
                         "--six-pager (spec: {spec})",
        "next_waiting": "⏸ Waiting for your answer: {question}{options}",
        "next_overdue": "⏰ Overdue commitments: {n}",
        "next_stale_sources": "♻ Sources behind decisions not verified for over {days} days:",
        "next_stale_grounds": "⚠ Stale grounds: {n} — pfs decision rebase / claim supersede",
        "next_review_now": "🔎 Decisions to review: {ids}",
        "next_review_soon": "📅 Reviews due within 14 days: {items}",
        "next_open_questions": "❓ Open questions: {n}",
        "next_clear": "Nothing due. For the current process step see pfs status.",
        "next_refresh": "Refresh sources after changes: pfs source refresh <S###>",
        "error_prefix": "Error: {msg}",
        "err_project_exists": "Project '{slug}' already exists — continue it: pfs use {slug} && pfs status",
        "err_unknown_step": "Unknown step '{step}'. Steps: {stages}",
        "err_bad_status": "Status: pending | in_progress | done | skipped",
        "new_created": "Project {slug} created. Next step: intake — clarify the request (see {agents}).",
        "step_marked": "Step {step} → {status}. Current: {stage}. Next: {next}",
        "step_cards": "Step maps: {cards}",
        "err_not_tabular": "Not a tabular file — expected CSV/XLSX: {path} ({exc}). Example: pfs data profile events.csv --save profile",
        "claims_table_header": "| ID | Type | Claim | Sources / grounds | Grade | Status |",
        "decisions_table_header": "| ID | Decision | Owner | Grounds | Metrics | Review | Status |",
        "pack_claims_title": "## Claims (grade A–D)",
        "pack_claims_header": "| ID | Type | Grade | Claim | Sources |",
        "pack_sources_title": "## Sources",
        "pack_sources_header": "| ID | Title | Where | Origin | Date |",
        "route_scenario": "Scenario: {scenario} — {title} (confidence: {confidence})",
        "route_secondary": "Related scenarios: {secondary}",
        "route_low_conf": "⚠ Low confidence: ask the lead a clarifying question about the goal, or override: --override <scenario>",
        "route_cards": "Method maps (read in this order): {cards}",
        "route_questions": "Questions that could change the decision:",
        "route_models": "Model plan by step:",
        "source_added": "Added: {sid} — {title} ({chars} chars){flag}",
        "source_dup": "Already registered (duplicate skipped): {sid} — {title} ({chars} chars){flag}",
        "source_fetch_added": "Added: {sid} — {title} ({chars} chars); channel: {via}; origin: {origin}{flag}",
        "source_fetch_dup": "Already registered (duplicate skipped): {sid} — {title} ({chars} chars); channel: {via}; origin: {origin}{flag}",
        "source_ext_warn": "⚠ The file was outside the project ({external}) — a copy is saved to {path}. The material must be explicitly provided by the user.",
        "claim_recorded": "{cid} [{kind}] recorded",
        "batch_created": "Batch: created {n}, duplicates skipped {m}",
        "batch_new": "New: {ids}",
        "decision_recorded": "{did} saved",
        "ask_recorded": "Question saved. The agent awaits the lead's answer (pfs answer \"...\").",
        "answer_recorded": "Answer saved.",
        "ask_hint": "Ask the lead: pfs ask \"<question>\" --options \"A,B,C\"",
        "roadmap_built": "Roadmap: {roadmap} (both layouts: \"Projects\" and \"Features by project\")",
        "roadmap_not_built": "Roadmap not built: {exc}",
        "kind_fact": "fact",
        "kind_hypothesis": "hypothesis",
        "kind_forecast": "forecast",
        "kind_assumption": "assumption",
        "kind_inference": "inference",
        "ask_autopilot": "PFS_AUTOPILOT=1: the pause takes the recommended option — answer yourself "
                         "(pfs answer \"<option>\") and continue without waiting.",
        "lang_current": "Project language: {lang} — instructions: {agents}, templates: {templates}, "
                        "checks: {gate}",
        "lang_set": "Project language: {lang} (was: {old}) — instructions: {agents}, templates: {templates}, "
                    "checks: {gate}",
        # ---------- REPORT.md (pfs export) ----------
        "report_title": "# {title}: strategy and rationale",
        "report_built": "> Assembled {ts} by `pfs export`. Tags [C###] — claims, "
                        "[S###] — sources, [D###] — decisions (see appendices).",
        "report_sixpager_note": "> Auto-draft: assembled by `pfs export --six-pager`; detail it "
                                "per the spec — {spec}.\n\n",
        "appx_a_claims": "# Appendix A. Claims registry",
        "appx_b_sources": "# Appendix B. Sources",
        "appx_sources_header": "| ID | Title | Link / file | Origin | Retrieved |",
        "appx_c_decisions": "# Appendix C. Decisions and commitments",
        "appx_d_transparency": "# Appendix D. Transparency",
        "appx_e_excel": "# Appendix E. Excel workbooks",
        # ---------- cost.summary_text ----------
        "cost_total": "Total: actual ${usd:.2f} (~{rub:.0f} ₽) "
                      "| API-price equivalent ${usd_eq:.2f} (~{rub_eq:.0f} ₽) "
                      "| sessions {sessions} | tokens {tokens} "
                      "| session time {tmin:.0f} min "
                      "| human time {hmin:.0f} min",
        "cost_plan": "subscription plan ({prov}): actual payment ${usd:.2f} — covered by the "
                     "subscription; API-price equivalent ${usd_eq:.2f} — what the same tokens "
                     "would cost at the provider's list price",
        "cost_plan_default": "subscription",
        "cost_by_models": "By models:",
        "cost_by_model_row": "  {model:<24} ${usd:.2f} | tokens {tokens} "
                             "(input {inp} · output {outp} "
                             "· cache {cr}/{cw})",
        "cost_by_steps": "By steps:",
        "cost_by_step_row": "  {step:<12} tokens {tokens} · equivalent ${usd:.2f}",
        "cost_retries": "Retries: {n} {word}{tail}",
        "cost_retries_tail_tokens": " · {tokens} tokens",
        "cost_retries_tail_unknown": " · tokens unknown (session aggregate)",
        "cost_retries_tail_equiv": " · equivalent ${usd:.2f}",
        "cost_plan_share": "subscription share ({head}${month_usd:g}/mo × {days} d): ${usd:.2f}",
        # ---------- finish.summary_text ----------
        "finish_built": "Assembled ({n}):",
        "finish_missing_docs": "Missing documents (stubs in six-pager/REPORT): ",
        "finish_all_docs": "Documents 00–07: all present",
        "finish_stale": "The registry changed before the build — cleared by the fresh rebuild: ",
        "finish_gate_error": "pfs finish: the quality check found errors — the pack was not built:\n- {errs}"
                             "\nFix them (pfs check) and retry: pfs finish",
        # ---------- participate ----------
        "err_need_persona_topic": "Specify the interview persona and topic",
        "err_guide_template_missing": "Interview guide template not found: {tpl}",
        "guide_title": "# Interview guide: {topic}",
        "guide_meta": "- Persona: {persona}\n- Topic: {topic}\n- Date: {date}",
        "guide_note": "> Question skeleton — have the agent fill it in before the session. "
                      "AI-respondent answers (interviews/synthetic) yield hypotheses only and "
                      "do not prove demand.",
        "ab_no_hypothesis": "⚠ No active hypotheses in the registry and no Hypothesis N in 06 — the "
                            "Hypothesis section is a placeholder: state it (pfs claim add … --kind hypothesis) "
                            "and rerun on a fresh project, or edit the document by hand.",
    },
}

# Указатели на активные инструкции/шаблоны/проверки для выбранного языка
POINTERS = {
    "ru": {"agents": "AGENTS.md", "templates": "knowledge/templates/",
           "gate": "config/quality_gate.json → \"ru\" (RU-заголовки)"},
    "en": {"agents": "AGENTS_EN.md", "templates": "knowledge/templates/en/",
           "gate": "config/quality_gate.json → \"en\" (EN headings)"},
}

SIX_PAGER_SPEC = {"ru": "knowledge/templates/SIX_PAGER_PROMPT.md",
                  "en": "knowledge/templates/en/SIX_PAGER_PROMPT.md"}


def lang_of(pdir: Path | None) -> str:
    """Язык проекта из project.json → lang; по умолчанию и при любых сомнениях — ru."""
    if pdir is None:
        return "ru"
    try:
        meta = json.loads((Path(pdir) / "project.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "ru"
    return meta.get("lang") if meta.get("lang") in LANGS else "ru"


def active_lang() -> str:
    """Язык активного проекта (для сообщений до/вне pdir); нет проекта — ru."""
    from . import core  # ленивый импорт: core не импортирует i18n на верхнем уровне
    slug = core.active_slug()
    return lang_of(core.projects_dir() / slug) if slug else "ru"


def t(lang: str, key: str, /, **kw) -> str:
    """Сообщение на языке проекта; RU-фолбэк и RU-строки дословно как прежде."""
    tpl = (STR.get(lang) or STR["ru"]).get(key) or STR["ru"].get(key, key)
    return tpl.format(**kw) if kw else tpl


def pointers(lang: str) -> dict[str, str]:
    return POINTERS.get(lang, POINTERS["ru"])
