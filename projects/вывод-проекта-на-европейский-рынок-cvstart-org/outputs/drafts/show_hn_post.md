# Черновик Show HN поста (P3, веха M2, день 60)

> Целевая аудитория — HN (tech-соискатели + OSS). Формат: Show HN, заголовок без маркетинговых слов, первым комментарием — автор с контекстом и честными ограничениями. Продукт уже на Product Hunt [C066] — в посте не упоминаем (HN это не любит), только факты.

## Заголовок (варианты для выбора перед публикацией)

1. `Show HN: I filtered 129 job boards and applied to only 68 — got 12 interviews (open-source, local-first)`
2. `Show HN: Open-source job-search filter — scores every listing 0–5 against your CV, never auto-applies`
3. `Show HN: Career-ops UI — a local dashboard that tells you which job posts not to apply to`

(Вариант 1 — личная история с числами из реального поиска основателя: она сильнее по правилам HN, но используйте её только если согласны раскрывать личные цифры публично.)

## Первый комментарий автора (черновик)

```
Author here. This started as a personal tool: I was sending CVs into
silence, so I built a filter — every listing gets scored 0.0–5.0 against
my CV on a transparent 0.0–5.0 rubric of five dimensions.

Honest limitations up front:
- It's a UI over the open-source career-ops CLI (unofficial, MIT). It
  must live inside the parent project — setup is one script, but it's
  not a standalone app yet. Windows = WSL only.
- Scoring is LLM judgement (BYOK: your own API key, 18 providers), not
  a formula. Every score cites evidence from the posting and your CV.
- Nothing is ever auto-submitted. The system's job is to stop you from
  applying, not to spray for you.
- 129 sources = 124 EN boards + 5 RU (hh.ru needs a RU IP). Scans run
  locally; your CV and applications never leave your machine — no
  accounts, no telemetry.
- 7,395 automated tests in CI. Site: cvstart.org, code on GitHub.

Happy to answer anything about the rubric, the false-positive problem
(listings that look great but aren't), or why I decided against
auto-apply even though everyone asked for it.
```

## Ответы на предсказуемую критику (подготовить заранее)

| Критика | Ответ |
|---|---|
| «LLM-скоринг — это гороскоп» | Рубрика опубликована, каждый скор цитирует доказательства из вакансии и CV — можно спорить с каждым пунктом; открытая методология vs закрытые формулы |
| «Ещё один resume-builder» | Это не builder: фильтр вакансий + трекер; конструктор — побочная функция; аналоги OSS (Reactive Resume [C032]) не сканируют борды |
| «129 бордов = спам-скрейпинг» | Скрейпинг публичных выдач со скорингом на своей машине; никаких аккаунтов и обходов |
| «Privacy = маркетинг» | BYOK, 0 телеметрии, MIT — проверяемо кодом; локальный режим не маркетинговое обещание, а архитектура [C004] |

## Метрика поста (в 06_validation_plan H-каналы)

- Переходы на cvstart.org/GitHub из треда; retention звёзд через 30 дней [C075 — базовые случаи: 656/240 пунктов у аналогов].
- Правило: не публиковать повторно; если не попал во front page — принять, не репостить (запрет HN).
