# Lovable brief: документация-сайт «Стратег Фабрики продуктов» (RU/EN)

> Бриф для Lovable MCP (после OAuth: `/mcp` → lovable → Authenticate; create_project/send_message расходуют
> кредиты). Референс дизайна и контента: `site/index.html` в репозитории. Публиковать — на поддомене/странице
> strategyproduct.ru (DNS: A 185.199.108-111.153 → GitHub Pages; для Lovable-хостинга можно свой домен).

## Задача
Собрать одностраничный сайт-документацию агента «Стратег Фабрики продуктов» на двух языках (RU/EN,
переключатель + автоопределение по браузеру). Один экран = один смысл; стиль тёмный, премиальный,
без «AI-слопа».

## Секции (RU / EN контент — из site/index.html и docs/HELP*.md)
1. Hero: заголовок «От размытого запроса — до обоснованной стратегии»; подзаголовок про доказательность;
   CTA «Запустить за 5 минут» и «GitHub»; бейдж «ИИ-агент · доказательная стратегия · человек в контуре».
2. Статистика: 12 шагов · 72 карты из 7 курсов · 41 навык / 8 субагентов / 4 хука · 0 зависимостей · 87%.
3. Возможности (8 карточек): бриф, источники S###, доказательства C###, red team, стратегии, six-pager+Excel,
   сопровождение решения, прозрачность и стоимость.
4. Процесс 12 шагов с фазами Double Diamond и паузами человека.
5. Six-pager + Excel: FAQ-1…6, 4 книги на формулах, `pfs calc` / `pfs export --six-pager`.
6. Команды CLI (таблица из README) + вопросные блоки `pfs questions`.
7. Справка (Help): общение с агентом, calcs.json, six-pager за 5 шагов, resume, среды (Claude/Cursor/OpenCode/
   Linear/Lovable/Feynman/Higgsfield/officecli), пересмотр, безопасность, troubleshooting.
8. Footer: GitHub · README RU/EN · HELP RU/EN · strategyproduct.ru.

## Дизайн-токены (совпадают с site/index.html)
Фон #070b13; карточки rgba(20,28,46,.72) + blur; текст #eaf0fa; muted #9aa7bd; акценты #4fd1c5 → #8b7bff →
#38bdf8 (градиенты), warn #f6ad55, ok #48bb78; шрифт системный; код — «SF Mono»/monospace; радиусы 12–16px.
Эффекты: параллакс-орбы с blur(90px) и скоростями 0.06/0.12/0.09, сетка с radial-mask, звёзды, noise 3.5%,
reveal-on-scroll (IntersectionObserver), 3D-tilt карточек, счётчики, печатающийся терминал, прогресс-бар скролла.
Уважать `prefers-reduced-motion`.

## Технические требования
React + Tailwind (TanStack Start по умолчанию Lovable) или статика; i18n-словарь RU/EN в одном файле;
все числа — как в README (12/72/41/0/87%); ссылки на GitHub-доки абсолютные; без заглушек и lorem ipsum;
SEO: title/description RU+EN, og-теги; Lighthouse ≥ 95 по accessibility.

## Критерии приёмки
- Переключение RU/EN на всех секциях без перезагрузки; язык по умолчанию из браузера.
- Все 8 секций заполнены реальным контентом брифа; числа совпадают с README.
- Эффекты включены, reduced-motion работает; мобайл-адаптив.
- Деплой по кнопке Lovable; домен (опционально) — strategyproduct.ru.
