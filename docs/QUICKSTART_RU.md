# Быстрый старт: полное тестирование агента от и до

Пошаговая инструкция: как проверить агента целиком — от чистой установки до финишного
пакета (six-pager RU/EN, Excel, дека) на двух языках. Каждый шаг — с командой и критерием.

> Короткая версия установки — [INSTALL.md](INSTALL.md). EN-версия гайда: [QUICKSTART_EN.md](QUICKSTART_EN.md). Все команды — в шпаргалке [README](../README.md).

## Шаг 0. Чистая установка (5 минут)

```bash
rm -rf ~/agent-test && mkdir ~/agent-test && cd ~/agent-test
git clone https://github.com/Fighter90/product-factory-strategist-agent.git agent
cd agent && bash scripts/install.sh    # 3 репо + pfs глобально + doctor
pfs doctor                             # PATH, Python, TLS, 111 карт, проекты
```

✅ критерий: «Установка завершена», doctor без ошибок, `pfs --help` показывает все команды.

## Шаг 1. RU-прогон: полный 12-шаговый цикл с данными

```bash
mkdir -p ~/agent-test/projects && export PFS_PROJECTS_DIR=~/agent-test/projects
pfs new "ATS: резюме джуниора проходит фильтры" "Резюме джуниоров не проходят ATS-фильтры (75% отсеиваются до рекрутера). Создать проверку совпадения ключевых слов и подсказки, чтобы проходимость выросла с 40% до 80%?"
pfs route growth
printf '# Данные: ATS и резюме\n\n- ATS используют 98%% Fortune 500.\n- Фильтр отсекает 75%% резюме до рекрутера.\n- Совпадение ключевых слов повышает проход в 2-3 раза.\n' > /tmp/src.md
pfs source add /tmp/src.md --origin public
pfs claim add "ATS отсекают 75% резюме до рекрутера" --kind fact --source S001 --grade B --quote "Фильтр отсекает 75% резюме до рекрутера"
pfs claim add "98% Fortune 500 используют ATS" --kind fact --source S001 --grade B --quote "ATS используют 98% Fortune 500"
pfs claim add "Совпадение ключевых слов повышает проход в 2-3 раза" --kind fact --source S001 --grade B --quote "Совпадение ключевых слов повышает проход в 2-3 раза"
pfs claim add "Джуниор-резюме покрывают 40% ключевых слов" --kind hypothesis --source S001 --grade B
pfs step intake done --next sources && pfs step sources done --next research
pfs step research done --next discovery && pfs step discovery done --next situation
pfs step situation done --next options && pfs step options done --next choice
pfs ask "Какой вариант?" --options "A: оставить,B: ATS-скан" && pfs answer "B: ATS-скан"
pfs step choice done --next strategy && pfs step strategy done --next validation
pfs step validation done --next review && pfs step review done --next decision
pfs decision add --title "ATS-скан" --decision "Модуль проверки совпадения ключевых слов" --owner PM --grounds C001,C003 --review 2027-03-01
pfs step decision done --next finish
```

✅ критерий: каждый шаг печатает «Карты шага», ошибок нет.

## Шаг 2. Документы 00–07 + гейт качества

Заполните 02/03/04/05/06 по шаблонам из `knowledge/templates/`:
03 — варианты + «Возражения» у каждого, 04 — «Альтернативы», «Выбранное», «Осознанные отказы»,
05 — «Подтверждение» таблицей с [C###] + «Соответствие обещаний продукту»,
06 — KPI-таблица с колонкой «Плоскость».

```bash
pfs check --strict    # цель: 0 ошибок
```

## Шаг 3. Two-step six-pager (PRO-46)

```bash
pfs export --six-pager          # шаг 1: пакет данных + каркас FAQ-1…6 со слотами
pfs check --six-pager           # шаг 2: линтер документа комитета; цикл «править → 0 ошибок»
```

✅ критерий: 0 ошибок; сноски [^N] соответствуют источникам; объём ≤ 3500 слов.

## Шаг 4. Финишный пакет

```bash
pfs finish    # REPORT, six-pager RU/EN (md/docx), 4 Excel, дека
ls projects/*/outputs/   # цель: 11 артефактов финиша (+ пакет данных и JSON-реестры — 18 файлов)
```

✅ критерий: REPORT.md, SIX_PAGER.md/.docx, SIX_PAGER_EN.md/.docx, 4 Excel, deck.html — все на месте.

## Шаг 5. EN-прогон (поочерёдно с RU)

```bash
pfs new --lang en "ATS resume scanner" "Junior resumes fail ATS filters. Build a keyword-match checker to raise pass rate from 40% to 80%?"
# повторить шаги на английском; проверить:
grep -c "[а-яА-Я]" projects/*/outputs/SIX_PAGER_EN.md   # цель: 0 кириллицы
```

## Шаг 6. Смоук всех команд CLI

Прогон каждой команды из шпаргалки (README, HELP) — по одной строке за раз:

```bash
pfs models && pfs "kb search тест" 2>/dev/null; pfs kb search "тест"
pfs data profile events.csv 2>/dev/null || true   # CSV/XLSX; нетабулярный файл — понятная ошибка, не Traceback
pfs interview guide --persona "Студент"
pfs media add скрин.png --desc "тест" 2>/dev/null || true
pfs ab --hypothesis "Гипотеза [C001]" --metric "конверсия"
pfs roadmap 2>/dev/null || true
pfs cost && pfs doctor
```

✅ критерий: ни одной usage-ошибки argparse, ни одного Traceback.

## Шаг 7. Полная сюита автотестов

```bash
python3 -m unittest discover -s tests   # цель: OK, 874+ теста
python3 scripts/update_skill_counts.py --check  # счётчики актуальны
```

## Шаг 8. MCP-серверы

В OpenCode: `/mcp` — статус каждого сервера «connected»
(`pfs-strategist` — инструменты агента; `linear`, `producthunt`, `lovable`, `rea` —
внешние серверы из `.mcp.json`: требуют OAuth/ключей в `.env` и настраиваются отдельно;
context7 и другие плагины среды — поверх, вне `.mcp.json`).

## Если что-то не сошлось

- Расхождение с «✅ критерием» — это баг: заведите задачу в Linear с меткой `swarm`,
  рой чинит и выпускает релиз.
- Типовые сбои и ремедиация — в [ADMIN_GUIDE_RU.md](ADMIN_GUIDE_RU.md), раздел «Диагностика».
