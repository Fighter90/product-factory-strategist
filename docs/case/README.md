# Материалы кейса: «Стратег Фабрики продуктов» — задание, бриф, сверка

Эта папка содержит всё по демонстрационному проекту кейса МегаФона: исходное задание, бриф демо-проекта, итоговые стратегии и контрольную сверку соответствия.

## Состав

| Файл | Что это |
|---|---|
| `CASE_TASK.md` | Полное задание кейса «Стратег Фабрики продуктов» (дословно, с критериями оценки) |
| `BRIEF_CONNECTION_LOVED.md` | Бриф демо-проекта «Связь для близких и собственных устройств» — исходные материалы руководителя (учебный рынок, все числа из брифа) |
| `STRATEGY_RESPONSE.md` | **Главный документ**: стратегии — один документ из пяти частей, как требует бриф. Расчёты рядом с решениями; 82/82 требований брифа закрыты (контрольная сверка) |
| `COMPLIANCE_CHECK.md` | Контрольная таблица сверки «требование брифа → где закрыто в STRATEGY_RESPONSE» (50+ контрольных пунктов) |

## Полный пакет демо-проекта

`projects/связь-для-близких-и-собственных-устройств/` в корне репозитория:

- **Стратегии**: `outputs/BRIEF_RESPONSE.md` (5 частей) · `outputs/04_product_strategy.md` · `outputs/05_comms_strategy.md` · `outputs/06_validation_plan.md` (pre-registration)
- **Варианты и red team**: `outputs/03_options.md` — 5 вариантов A–E, 20 ударов (15 возражений + 5 скрытых допущений), пороги [C021–C026]
- **Реестры**: `claims.jsonl` (26 активных: 10 факт · 8 допущение · 4 гипотеза · 4 вывода) · `decisions.jsonl` (D001 accepted) · `sources/` (S001 бриф · S002–S003 синтетика · S004 wireframe)
- **Финансы**: `analysis/economics.py` → `economics_out.txt` (воспроизводимо) · `attachments/` (4 Excel на формулах)
- **e2e живые прогоны**: `qa/E2E-2026-11-19-svyaz-ru.md` (111 шагов модели, 7 пауз автопилотом) · `-en.md` (148 шагов, EN-интерфейс)
- **Сравнение с обычным чатом**: `docs/demo/comparison.md` (7 критериев) + `baseline_svyaz.md`

## Быстрая проверка жюри (5 команд)

```bash
git clone https://github.com/Fighter90/product-factory-strategist-agent.git && cd product-factory-strategist-agent
bash scripts/install.sh && python3 -m tools.pfs doctor   # 111 карт
python3 -m unittest discover -s tests                    # 969 тестов
python3 -m tools.pfs use связь-для-близких-и-собственных-устройств
python3 -m tools.pfs check --strict                      # 0 ошибок, 98/100
python3 analysis/economics.py --project связь-для-близких-и-собственных-устройств  # все числа сценария
```
