# extras/ — вне рамок агента

Здесь живут навыки, которые **не загружаются средой по умолчанию** (PRO-65). Среда читает
только `.claude/skills/`; чтобы вернуть навык, перенесите его папку обратно и обновите
`docs/SKILLS.md` и счётчики (`python3 scripts/update_skill_counts.py --write`).

Критерий отбора: каждый загружаемый навык должен быть привязан к шагу процесса агента или
к его сценарию. Число компонентов само по себе не преимущество.

## Почему вынесены (extras/skills/, 21 навык)

- **Биоинформатика и химия** — вне рамок продуктового стратега:
  `biopython`, `pydeseq2`, `rdkit`.
- **ML-статистика** — дублирует возможности `data-analysis`, `statistical-analysis`
  и `pfs data` для продуктовых задач: `scikit-learn`, `shap`, `statsmodels`, `seaborn`.
- **Научные документы** — формат научных публикаций, не продуктовых отчётов:
  `latex-posters`, `scientific-slides`, `scientific-schematics`, `citation-management`.
- **Литературный ресёрч по статьям** — заменяется `deep-research`/`research-lookup`
  с provenance: `paper-lookup`.
- **Режимы мышления вне процесса** — не привязаны к шагам и сценариям агента:
  `consciousness-council`, `dhdna-profiler`, `what-if-oracle`.
- **Интеграции вне рамок** — `hallmark` (дизайн-гейты для сторонних работ среды),
  `board-of-directors` (дублирует red-team на шаге options и premortem на decision),
  `rea` (reverse engineering бинарников/страниц — MCP-инструмент, не навык стратега).
- **Outbound-продажи** — роль продаж, не стратега: `cold-email`, `event-prospecting`,
  `directory-submissions`.

## venue-templates — не поставляется, указатели убиты

`venue-templates` (оформление работ под требования конференций и журналов) — единственный
навык, судьбу которого пришлось выяснять отдельно (ревью PRO-65, раунд 4): его папки нет
ни в `.claude/skills`, ни в `extras/skills`, и никогда не было в истории репозитория —
он поставлялся только в личной библиотеке автора среды, вне набора. Поэтому переносить
нечего: указатели на него в научных навыках (`literature-review`, `scientific-writing`,
включая комментарий в `scientific_report.sty`) убиты, а описываемые им файлы
(`venue_writing_styles.md` и др.) не поставляются. На счётчики (100 навыков) это не влияет.
