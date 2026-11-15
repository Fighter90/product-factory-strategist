# cvstart.org — сайт проекта (лендинг + методология)

URL: https://cvstart.org/ (Astro-статик на GitHub Pages; 19 языковых версий с hreflang: en, ru, uk, es, pt-BR, fr, pl, de, it, tr, da, ar(RTL), hi, ta, ja, ko, vi, zh-CN, zh-TW).

## Продукт (по лендингу)
- «Career-ops UI» — дашборд над AI-пайплайном поиска работы career-ops: скан ~129 джоб-бордов (124 EN + 5 RU: hh.ru, Habr Career, GeekJob, GetMatch, Trudvsem) без LLM; AI-оценка каждой вакансии 0.0–5.0 против резюме; генерация резюме и cover letters под вакансию; трекер заявок с follow-up.
- 100% локально: сервер на 127.0.0.1, данные — markdown/YAML на машине; без облака и телеметрии.
- «Bring your own model»: 18 LLM-провайдеров (BYOK) или keyless «copy-the-prompt».
- Сравнение с платными: Jobscan $49,95/мес, Teal $29, Huntr $40, Rezi $29 — «$0 forever (MIT)».
- Позиционирование: «Unofficial UI — not affiliated with career-ops».

## Структура сайта
/ (лендинг, 19 локалей), /help/, /methodology/, /changelog/ (11 записей), /license/.

## Ограничения (по лендингу)
- Приложение не хостится публично — только локальная установка (нужен родительский репозиторий career-ops).
- Windows — только через WSL.
