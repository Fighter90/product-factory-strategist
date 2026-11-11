# Яндекс Метрика — ТЗ на разметку целей (PRO-66)

Разметка целей уже в HTML сгенерированных страниц (`site/index.html`, `site/en/index.html`).
Сам счётчик в репозитории **не хранится**: он подключается только при сборке.

## Подключение счётчика

```
python3 scripts/build_site.py --ym-id <ID счётчика>
```

- Без `--ym-id` страницы собираются без загрузчика Метрики — разметка целей при этом
  остаётся в HTML, события просто никуда не отправляются.
- `--ym-id` принимает только число. Значение передаёт владелец при сборке/деплое
  (например, секретом в CI); в git оно не попадает.
- При подключении в конец `<body>` вставляются: `window.YM_ID`, загрузчик
  `mc.yandex.ru/metrika/tag.js`, `ym(ID, "init", {clickmap, trackLinks, accurateTrackBounce})`
  и `<noscript>`-фолбэк с пикселем `mc.yandex.ru/watch/<ID>`.

## Цели

| Цель | Что считается | Где размечено |
|---|---|---|
| `cta_install_click` | клики по кнопкам «Запустить» / «Запустить за 5 минут» / «Установить» | `data-goal="cta_install_click"` — шапка, hero, финальный CTA (RU и EN) |
| `cta_demo_click` | клики «Смотреть демо» и «Открыть разбор» (ведёт на `demo.html`) | `data-goal="cta_demo_click"` — hero и секция «Демо» |
| `github_click` | переходы на репозиторий GitHub | `data-goal="github_click"` — финальный CTA |
| `lang_switch` | переключение языка RU ↔ EN | `data-goal="lang_switch"` на ссылках `.lang a` (на каждой странице ведёт на парную) |
| `copy_command` | копирование команды установки | кнопки `.copy` в секции «Установка»; JS отправляет `copy_command` с параметром `i` — индекс команды (`0` clone, `1` install, `2` doctor, `3` opencode) |
| `faq_open` | открытие вопроса в FAQ | JS-обработчик `toggle` на `<details>`; параметр `q` — первые 60 символов вопроса |

## Как работает разметка

- Кнопки и ссылки несут `data-goal="<цель>"`; общий JS-обработчик на каждой странице
  отправляет `ym(ID, 'reachGoal', <цель>)` по клику.
- `copy_command` и `faq_open` вешаются не через `data-goal`, а отдельными обработчиками
  (кнопки копирования и `<details>` соответственно) — тем же общим скриптом.
- Событие отправляется только если счётчик подключён: скрипт проверяет
  `window.ym && window.YM_ID`. Без `--ym-id` страницы работают без JS-ошибок.
- Без JS (или до загрузки скрипта) весь текст, числа и навигация доступны: аккордеон
  FAQ — нативные `<details>`, переключатель языка — обычные ссылки, команды — текст в `<code>`.

## Проверка после деплоя

1. Собрать с реальным ID, открыть сайт, метрика.яндекс.ру → счётчик → «Вебвизор/События».
2. Кликнуть каждую кнопку из таблицы и убедиться, что пришла соответствующая цель.
3. Скопировать команду установки — цель `copy_command` с параметром `i`.
4. Раскрыть вопрос FAQ — цель `faq_open`.
5. Переключить RU → EN — цель `lang_switch`.

---

## English summary

Analytics markup (Yandex Metrika) is already present in the generated pages. The counter
ID is **not** stored in the repository: pass it at build time via
`python3 scripts/build_site.py --ym-id <ID>` (e.g. from a CI secret). Without the flag the
pages build with no loader; goals are wired via `data-goal` attributes (`cta_install_click`,
`cta_demo_click`, `github_click`, `lang_switch`) and two dedicated handlers
(`copy_command` with an `i` parameter for the copied command index, `faq_open` with a `q`
parameter holding the question text). Events fire only when the counter is connected
(`window.ym && window.YM_ID`); everything works without JavaScript.
