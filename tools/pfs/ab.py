"""A/B-эксперименты по базе знаний (PRO-71): `pfs ab` собирает три артефакта одного теста.

1. Дизайн-документ по шаблону `M-ab-test-design-template` — секции заполняются из гипотез
   стратегии (реестр C###) и 06_validation_plan.md; MDE/выборка/длительность считаются по
   формулам `M-ab-testing` и `M-quant-methods` (n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p)).
2. Отчёт по чек-листу `M-ab-test-checklist`: блоки 1–4 проверяются до запуска
   (до отдачи документа), блоки 5–7 заложены структурой секции «Результаты»;
   незакрытые пункты перечисляются явно.
3. Контекст AI-ревьюера — системный промпт по каркасу `M-ai-experiment-review-context`,
   заполненный под конкретный продукт (project.json, гипотезы, источники).

Документы не перезаписываются: повторный вызов возвращает существующие файлы,
правки агента не затираются (как `pfs interview guide` и `pfs ux scaffold`).
"""
from __future__ import annotations

import math
import re
from pathlib import Path
from statistics import NormalDist

from . import claims, core, i18n, sources
from .core import PfsError

# Заголовок «Гипотеза N: …» / «Hypothesis N: …» в 06_validation_plan.md
PLAN_HYP = re.compile(r"^#{1,6}\s+(?:Гипотеза|Hypothesis)\s+\d+:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
HEAD = re.compile(r"^(#{1,6})\s")


# ---------- статистика по M-ab-testing / M-quant-methods ----------

def sample_size(baseline: float, mde: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Размер выборки на группу: n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p); округление вверх
    (вниз округляет в пользу пропуска эффекта — M-ab-testing)."""
    if not 0 < baseline < 1:
        raise PfsError(f"baseline: доля 0<p<1, получено {baseline}")
    if not 0 < mde < 1:
        raise PfsError(f"mde: абсолютная доля 0<MDE<1, получено {mde}")
    if not 0 < alpha < 1:
        raise PfsError(f"alpha: 0<α<1, получено {alpha}")
    if not 0.5 <= power < 1:
        raise PfsError(f"power: 0.5≤мощность<1, получено {power}")
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    return math.ceil((z_a + z_b) ** 2 * 2 * baseline * (1 - baseline) / mde ** 2)


def duration_days(n_group: int, traffic: float, share: float = 0.5) -> int:
    """Дней до набора: n / (суточный трафик × доля на группу), кратно полным неделям —
    тест держат не меньше недели, чтобы накрыть недельный цикл поведения (M-ab-testing)."""
    if traffic <= 0:
        raise PfsError(f"traffic: суточный трафик должен быть > 0, получено {traffic}")
    share = min(max(share, 0.01), 1.0)
    days = math.ceil(n_group / (traffic * share))
    return max(7, math.ceil(days / 7) * 7)


# ---------- гипотезы: реестр C### и заголовки 06 ----------

def claim_hypotheses(pdir: Path) -> list[dict]:
    """Активные гипотезы и прогнозы стратегии из реестра утверждений."""
    return [c for c in claims.load(pdir)
            if c["kind"] in ("hypothesis", "forecast") and c["status"] == "active"]


def plan_hypotheses(pdir: Path) -> list[str]:
    """Заголовки «Гипотеза N: …» из 06_validation_plan.md."""
    path = pdir / "outputs" / "06_validation_plan.md"
    if not path.exists():
        return []
    return [m.group(1).strip() for m in PLAN_HYP.finditer(path.read_text(encoding="utf-8"))]


def pick_hypothesis(pdir: Path, hypothesis: str | None = None) -> dict | None:
    """Гипотеза эксперимента: C### из реестра (по умолчанию первая активная гипотеза/прогноз);
    реестр пуст — первый заголовок из 06; нет и его — None (план собирается с заглушкой)."""
    if hypothesis:
        c = claims.get(pdir, hypothesis)
        if c["status"] != "active":
            raise PfsError(f"{hypothesis} отозвано/замещено — выберите активную гипотезу (pfs claim list)")
        return {"id": c["id"], "text": c["text"]}
    rows = claim_hypotheses(pdir)
    if rows:
        return {"id": rows[0]["id"], "text": rows[0]["text"]}
    plan = plan_hypotheses(pdir)
    if plan:
        return {"id": None, "text": plan[0]}
    return None


# ---------- разделы 06 по языку проекта (config/quality_gate.json) ----------

def _plan_sections(pdir: Path) -> dict[str, str]:
    """Тела ключевых разделов 06: ожидаемое изменение, база сравнения, срок, критерии."""
    cfg_all = core.read_json(core.CONFIG / "quality_gate.json", {})
    lang = i18n.lang_of(pdir)
    block = cfg_all.get(lang) if isinstance(cfg_all.get(lang), dict) and "documents" in cfg_all.get(lang, {}) \
        else cfg_all.get("ru", cfg_all)
    names = (block.get("documents", {}).get("06_validation_plan.md", {}) or {}).get("required_sections", [])
    # порядок зафиксирован в quality_gate: [0] ожидаемое изменение, [1] база сравнения,
    # [2] срок наблюдения, [4] критерии решения
    keys = ["expected", "compare", "window", "counter", "criteria"]
    path = pdir / "outputs" / "06_validation_plan.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return {key: _section(text, name) if name else "" for key, name in zip(keys, names)}


def _section(text: str, name: str) -> str:
    """Тело раздела с заголовком `name` (любой уровень #) до следующего заголовка."""
    out, inside = [], False
    for ln in text.splitlines():
        if HEAD.match(ln):
            inside = ln.split(None, 1)[1].strip().lower() == name.strip().lower()
            continue
        if inside:
            out.append(ln)
    return "\n".join(out).strip()


# ---------- тексты документов (язык проекта, PRO-57) ----------

T = {
    "ru": {
        "design_title": "# Дизайн A/B-теста: {metric}",
        "design_head": ("> Шаблон: `M-ab-test-design-template` (knowledge/methods/ab-test-design-template.md) · "
                        "Статистика и ловушки: `M-ab-testing` · Формулы выборки: `M-quant-methods` ·\n"
                        "> Чек-лист запуска: `M-ab-test-checklist` (knowledge/methods/ab-test-checklist.md) → "
                        "analysis/{checklist} ·\n"
                        "> Ревью плана и выводов: `M-ai-experiment-review-context` → analysis/{review}\n>\n"
                        "> Пороги, длительность и правила решений фиксируются ДО старта. Секция «Результаты»\n"
                        "> заполняется только после набора данных; [квадратные скобки] — заполните вручную."),
        "biz": "## Бизнес",
        "about": "**О продукте:** {title}. Вопрос стратегии: {question}",
        "problem": "**Проблема:** [что не устраивает сейчас: цифра воронки, жалобы, поведение пользователей]",
        "goal": "**Цель эксперимента:** [на какой вопрос ответит тест; связь с целью продукта или квартальной целью]",
        "hyp": "**Гипотеза:** {hyp}",
        "hyp_none": "**Гипотеза:** [если сделаем <изменение> для <сегмента>, то <метрика> изменится на <X>, "
                    "потому что <причина> — сформулируйте и добавьте в реестр: pfs claim add … --kind hypothesis]",
        "effect": "**Оценка потенциального эффекта:** {effect}",
        "effect_none": "**Оценка потенциального эффекта:** [эффект в метрике/деньгах с допущениями; "
                       "заполните из 06 «Ожидаемое изменение»]",
        "metrics": "## Метрики",
        "target": "### Целевая",
        "proxy": "### Прокси",
        "guard": "### Защитная",
        "metric_name": "**Название:** {name}",
        "metric_none": "**Название:** [что считаем; для доли и ratio — числитель и знаменатель]",
        "metric_type": "**Тип метрики:** [конверсионная / непрерывная / ratio]",
        "metric_period": "**Период расчёта:** [до конца теста / N дней от попадания в выборку]",
        "metric_test": "**Стат. тест:** [z-test / t-test / t-test по бакетам]",
        "metric_why": "**Почему важна:** [какое изменение повлияет на решение]",
        "decision": "## Механизм принятия решений",
        "decision_none": ("[Пороги по целевой и защитной метрикам: что делаем при успехе, при неясном результате "
                          "(фиксируем вывод, не раскатываем), при просадке защитной больше порога — откат немедленно.]"),
        "decision_from_06": "Правила из 06 «Критерии решения»: {criteria}",
        "impl": "## Реализация теста",
        "split": "**Система сплитования:** {split}",
        "split_none": "**Система сплитования:** [система и ссылка на настройку; для своего сплита — результаты проверки]",
        "split_id": "**Идентификатор сплитования:** [по какому ID делите на группы]",
        "split_mech": "**Механика сплитования:** [аудитория, платформы, версии; когда назначается группа и с какого события человек в тесте]",
        "variants": "**Отличия в вариациях:** [что происходит в контроле и тестовых группах; скриншоты/макеты]",
        "script": "**Скрипт:** [SQL/код, восстанавливающий участников, группы и момент попадания]",
        "compare_06": "**База сравнения (из 06):** {compare}",
        "testing": "## Проверка гипотез",
        "h01": "**Нулевая и альтернативная гипотезы:** H₀: {metric} в группах не отличается; "
               "H₁: отличается не меньше чем на MDE",
        "alpha": "**Уровень значимости:** α = {alpha} (двусторонний)",
        "power": "**Мощность:** {power} (β = {beta})",
        "mde": "**MDE:** {mde} (абсолютные доли) — [обоснуйте размер: минимальный эффект, окупающий изменение]",
        "mde_none": "**MDE:** [задайте минимальный эффект и пересчитайте выборку: pfs ab --baseline <p> --mde <d>]",
        "n": "**Размер выборки:** {n} пользователей на группу (p = {baseline}, MDE = {mde}, α = {alpha}, мощность {power})",
        "n_formula": "  Формула `M-ab-testing`: n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p); z_α = {z_a:.2f}, z_β = {z_b:.2f}.",
        "n_none": ("**Размер выборки:** [заполните] формула `M-ab-testing`: n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p); "
                   "рассчитайте, задав baseline и MDE: pfs ab --baseline <p> --mde <d>"),
        "days": "**Длительность теста:** {days} дн. при трафике {traffic:g}/сут и доле на группу {share:g} "
                "(кратно полной неделе — накрыть недельный цикл)",
        "days_none": "**Длительность теста:** n / (суточный трафик × доля на группу); держите кратно "
                     "полным неделям. Рассчитайте: pfs ab --traffic <N>",
        "results": "## Результаты эксперимента",
        "results_note": ("*Структура — блоки 5–7 чек-листа `M-ab-test-checklist`; заполняется только "
                         "после набора данных.*"),
        "b5": "### Блок 5. Что запустили фактически",
        "b5_items": "- Ссылка на карточку теста; фактические даты, вариации и размеры групп против дизайна; объяснение отклонений и перезапусков.\n"
                    "- SRM: доли групп против плана; качество событий и аномалии — разобрать до интерпретации эффекта.",
        "b6": "### Блок 6. Как посчитан результат",
        "b6_items": "- Восстановление групп по ключу сплитования; единица анализа, окна и определения метрик; дедуп и фильтры с причинами.\n"
                    "- Для каждой ключевой метрики: значения групп, абсолютный и относительный эффект, ДИ, p-value (с поправкой из дизайна).\n"
                    "- Плановые сравнения отделены от разведочных; код/отчёт воспроизводит расчёт.",
        "b7": "### Блок 7. Что решили и что дальше",
        "b7_items": "- Решение по заранее заданным правилам «Механизма принятия решений» (не подгонка под результат).\n"
                    "- Следующий шаг, владелец и срок; при раскатке — что мониторим.",
        "conclusions": "## Выводы",
        "concl": "**Вывод:** [что показал тест и какое решение принято; сверка с правилами «Механизма принятия решений»]",
        "cta": "**Call to action:** [кто и что сделает, срок; что измеряем после раскатки, чтобы подтвердить эффект]",
        "chk_title": "# Чек-лист запуска A/B-теста (M-ab-test-checklist)",
        "chk_head": ("> План: outputs/{design} · Карта: knowledge/methods/ab-test-checklist.md\n"
                     "> Блоки 1–4 проверяются до запуска (до отдачи документа); блоки 5–7 — структура\n"
                     "> секции «Результаты» плана, заполняется после набора данных. Незакрытые пункты — в конце."),
        "chk_pre": "## До запуска",
        "chk_post": "## Блоки 5–7 (структура секции «Результаты» — после набора данных)",
        "chk_b1": "### Блок 1. Проблема, гипотеза, польза",
        "chk_b2": "### Блок 2. Метрики и правила решений",
        "chk_b3": "### Блок 3. Группы, аудитория, экспозиция",
        "chk_b4": "### Блок 4. Выборка и длительность",
        "chk_hyp": "Гипотеза сформулирована (X → M → Z%): «{hyp}»",
        "chk_hyp_open": "Гипотеза сформулирована (X → M → Z%) — задайте: pfs claim add … --kind hypothesis",
        "chk_effect": "Польза в деньгах/заказах оценена (06 «Ожидаемое изменение» заполнено)",
        "chk_effect_open": "Польза в деньгах/заказах не оценена — заполните «Ожидаемое изменение» в 06 и «Оценку эффекта» в плане",
        "chk_target": "Целевая метрика названа: «{metric}» (числитель/знаменатель — в плане)",
        "chk_target_open": "Целевая метрика не названа — задайте: pfs ab --metric \"<метрика>\"",
        "chk_guard": "Защитная метрика и порог недопустимого вреда заданы: «{guardrail}»",
        "chk_guard_open": "Защитная метрика и порог недопустимого вреда не заданы — pfs ab --guardrail \"<метрика и порог>\"",
        "chk_rules": "Правила решения зафиксированы до старта (успех/отказ/неясный результат)",
        "chk_rules_open": "Правила решения не зафиксированы — pfs ab --rules \"<порог успеха; отказ; неясный результат>\"",
        "chk_split": "Система сплитования и идентификатор указаны: «{split}»",
        "chk_split_open": "Система сплитования и идентификатор не указаны — pfs ab --split-system \"<система, ID>\"",
        "chk_sample": "MDE и размер выборки рассчитаны: p = {baseline}, MDE = {mde} → {n} на группу (α = {alpha}, мощность {power})",
        "chk_sample_open": "MDE и размер выборки не рассчитаны — pfs ab --baseline <p> --mde <d>",
        "chk_days": "Длительность рассчитана по трафику: {days} дн. (кратно неделе)",
        "chk_days_open": "Длительность по трафику не рассчитана — pfs ab --traffic <N>",
        "chk_b5_done": "Блок 5. Что запустили фактически — структура в плане (факт против дизайна, SRM)",
        "chk_b6_done": "Блок 6. Как посчитан результат — структура в плане (группы, эффект, ДИ, p-value, поправка)",
        "chk_b7_done": "Блок 7. Выводы и действия — структура в плане (решение по правилам, владелец, срок)",
        "chk_open": "## Незакрытые пункты (закройте до запуска)",
        "chk_open_empty": "Незакрытых пунктов блоков 1–4 нет — план можно отдавать на ревью.",
        "rev_title": "# Контекст AI-ревьюера эксперимента (системный промпт)",
        "rev_head": ("> Каркас: `M-ai-experiment-review-context` (knowledge/methods/ai-experiment-review-context.md) ·\n"
                     "> План: outputs/{design} · Чек-лист: analysis/{checklist} ·\n"
                     "> Обучение агента на своих примерах: `M-genai-evals` (золотой набор, LLM-as-judge, guardrails)"),
        "rev_role_h": "## Роль",
        "rev_role": ("Ты помогаешь автору найти существенные проблемы в плане или выводах A/B-эксперимента. "
                     "Решение принимает команда: ты не одобряешь и не отменяешь тест."),
        "rev_ctx_h": "## Контекст продукта",
        "rev_ctx_product": "- Продукт: {title}",
        "rev_ctx_question": "- Вопрос стратегии: {question}",
        "rev_ctx_hyp": "- Гипотеза эксперимента: {hyp}",
        "rev_ctx_metric": "- Целевая метрика: {metric}",
        "rev_ctx_guard": "- Защитная метрика: {guardrail}",
        "rev_ctx_decision": "- Кто принимает решение: [заполните]",
        "rev_ctx_reviewer": "- Кто ревьюит находки агента: [заполните]",
        "rev_ctx_sources": "- Доступные агенту источники: {sources}",
        "rev_vocab_h": "## Словарь показателей",
        "rev_vocab": ("- Целевая: {metric} — точное определение (числитель/знаменатель), единица анализа, окно "
                      "наблюдения, источник и базовый период, связь с решением и допустимые границы: [заполните]\n"
                      "- Защитная: {guardrail} — определение и порог недопустимого вреда: [заполните]\n"
                      "- Известные задержки и ограничения данных: [заполните]"),
        "rev_rules_h": "## Правила проверки (12 правил — по карте `M-ai-experiment-review-context`)",
        "rev_rules": (
            "1. Сначала восстанови вопрос команды, аудиторию, варианты, единицу рандомизации и правило решения; отметь, чего не хватает.\n"
            "2. Отделяй подтверждённые данные от допущений и предположений; не выдумывай источники, числа, параметры и выполненные проверки.\n"
            "3. Для каждой существенной находки указывай конкретное поле или фрагмент доступного источника; объясняй влияние на вывод и как исправить.\n"
            "4. Не считай документ или ссылку прочитанными, если содержимое тебе недоступно; запроси нужный фрагмент.\n"
            "5. Различай назначение группы, доступность изменения и фактический exposure; исключение участников по поведению после назначения требует обоснования.\n"
            "6. Проверяй определения метрик, единицы, окна и связь с гипотезой; рост кликов и близость покупки к просмотру не доказывают инкрементальную покупку.\n"
            "7. Выбирай метод анализа под вопрос и структуру данных; не требуй один и тот же метод снижения дисперсии для всех тестов.\n"
            "8. Отличай бизнес-значимый эффект от чувствительности дизайна; проверяй, для какой аудитории посчитаны baseline и требуемая выборка.\n"
            "9. Не делай вывод «нет эффекта» из отсутствия значимости; для заявлений о безопасности нужны мощность и граница недопустимого вреда.\n"
            "10. Проверяй выборку, доли групп (SRM), качество событий и отклонения от плана до интерпретации; значимость не чинит ошибку данных.\n"
            "11. Ранние остановки и дополнительные сравнения оценивай по заранее согласованному методу; не предлагай закончить тест на первом удобном p-value.\n"
            "12. Существенные риски и спорные решения передавай человеку; уверенность формулировки — не мера качества ответа."),
        "rev_err_h": "## Примеры ошибок, которые надо ловить",
        "rev_errs": (
            "- A. Гипотеза обещает покупки, а в плане только клики — определи итоговую метрику и её связь с решением.\n"
            "- B. Группы посчитаны по разным числам — сначала сверь источники групп, события, окна и исключения.\n"
            "- C. В группе есть участники, но изменение им недоступно — проверь exposure и согласованный подход к анализу.\n"
            "- D. После запуска оставили только активных — риск отбора по пост-назначенческому поведению.\n"
            "- E. Покупателей в прогнозе назвали дополнительными заказами — восстанови единицы и обоснуй инкрементальность."),
        "rev_fmt_h": "## Формат ответа",
        "rev_fmt": ("Короткое заключение о готовности материалов к ревью человеком; затем только существенные находки: "
                    "проблема и серьёзность; источник или конкретный фрагмент; возможное влияние на вывод; "
                    "предлагаемое исправление; что должен проверить человек. Отдельно — недостающие данные, без "
                    "которых ревью не завершить. Один риск — одной формулировкой, без повторов."),
        "sources_none": "[заполните: реестр пуст — pfs source list]",
        "sources_more": " (+ ещё {n})",
        "metric_default": "целевая метрика",
        "guard_default": "не задана",
    },
    "en": {
        "design_title": "# A/B Test Design: {metric}",
        "design_head": ("> Template: `M-ab-test-design-template` (knowledge/methods_en/ab-test-design-template.md) · "
                        "Statistics and traps: `M-ab-testing` · Sample formulas: `M-quant-methods` ·\n"
                        "> Launch checklist: `M-ab-test-checklist` (knowledge/methods_en/ab-test-checklist.md) → "
                        "analysis/{checklist} ·\n"
                        "> Review of plan and conclusions: `M-ai-experiment-review-context` → analysis/{review}\n>\n"
                        "> Thresholds, duration and decision rules are fixed BEFORE launch. The Results section\n"
                        "> is filled only after the data is collected; [square brackets] — fill in manually."),
        "biz": "## Business",
        "about": "**Product:** {title}. Strategy question: {question}",
        "problem": "**Problem:** [what is wrong today: a funnel number, complaints, user behavior]",
        "goal": "**Experiment goal:** [which question the test answers; link to the product or quarterly goal]",
        "hyp": "**Hypothesis:** {hyp}",
        "hyp_none": "**Hypothesis:** [if we change <X> for <segment>, <metric> moves by <Z>, because <reason> — "
                    "add it to the registry: pfs claim add … --kind hypothesis]",
        "effect": "**Estimated potential effect:** {effect}",
        "effect_none": "**Estimated potential effect:** [effect in metric/money with assumptions; "
                       "fill from 06 Expected change]",
        "metrics": "## Metrics",
        "target": "### Target",
        "proxy": "### Proxy",
        "guard": "### Guardrail",
        "metric_name": "**Name:** {name}",
        "metric_none": "**Name:** [what we count; for a share or ratio — numerator and denominator]",
        "metric_type": "**Metric type:** [conversion / continuous / ratio]",
        "metric_period": "**Calculation window:** [until the end of the test / N days from exposure]",
        "metric_test": "**Statistical test:** [z-test / t-test / bucketed t-test]",
        "metric_why": "**Why it matters:** [which change of this metric affects the decision]",
        "decision": "## Decision mechanism",
        "decision_none": ("[Thresholds for target and guardrail metrics: what we do on success, on an inconclusive "
                          "result (record the conclusion, do not roll out), and when the guardrail breaches its "
                          "harm boundary (immediate rollback).]"),
        "decision_from_06": "Rules from 06 Decision criteria: {criteria}",
        "impl": "## Implementation",
        "split": "**Splitting system:** {split}",
        "split_none": "**Splitting system:** [system and link to settings; for a custom split — validation results]",
        "split_id": "**Splitting identifier:** [which ID divides users into groups]",
        "split_mech": "**Splitting mechanics:** [audience, platforms, versions; when a group is assigned and from which event a user is in the test]",
        "variants": "**Differences between variants:** [control vs test groups; screenshots/mockups]",
        "script": "**Script:** [SQL/code restoring participants, groups and exposure moment]",
        "compare_06": "**Comparison baseline (from 06):** {compare}",
        "testing": "## Hypothesis testing",
        "h01": "**Null and alternative hypotheses:** H₀: {metric} does not differ between groups; "
               "H₁: differs by at least the MDE",
        "alpha": "**Significance level:** α = {alpha} (two-sided)",
        "power": "**Power:** {power} (β = {beta})",
        "mde": "**MDE:** {mde} (absolute share) — [justify the size: the minimal effect that pays for the change]",
        "mde_none": "**MDE:** [set the minimal effect and recompute the sample: pfs ab --baseline <p> --mde <d>]",
        "n": "**Sample size:** {n} users per group (p = {baseline}, MDE = {mde}, α = {alpha}, power {power})",
        "n_formula": "  Formula from `M-ab-testing`: n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p); z_α = {z_a:.2f}, z_β = {z_b:.2f}.",
        "n_none": ("**Sample size:** [fill in] formula from `M-ab-testing`: n = (z_α+z_β)²·2σ²/MDE², σ² = p(1−p); "
                   "compute it by setting baseline and MDE: pfs ab --baseline <p> --mde <d>"),
        "days": "**Test duration:** {days} days at {traffic:g}/day traffic and {share:g} share per group "
                "(whole weeks — cover the weekly behavior cycle)",
        "days_none": "**Test duration:** n / (daily traffic × share per group); keep it in whole weeks. "
                     "Compute: pfs ab --traffic <N>",
        "results": "## Experiment results",
        "results_note": ("*Structure — blocks 5–7 of the `M-ab-test-checklist`; filled only after the data "
                         "is collected.*"),
        "b5": "### Block 5. What was actually launched",
        "b5_items": "- Link to the experiment card; actual dates, variants and group sizes vs the design; deviations and restarts explained.\n"
                    "- SRM: group shares vs the plan; event quality and anomalies — analyzed before interpreting the effect.",
        "b6": "### Block 6. How the result was computed",
        "b6_items": "- Groups restored by the assignment key; unit of analysis, windows and metric definitions; dedup and filters with reasons.\n"
                    "- For each key metric: group values, absolute and relative effect, CI, p-value (with the correction planned in the design).\n"
                    "- Planned comparisons separated from exploratory analysis; code/report reproduces the calculation.",
        "b7": "### Block 7. What we decided and what is next",
        "b7_items": "- Decision per the pre-agreed rules of the Decision mechanism (not fitted to the result).\n"
                    "- Next step, owner and deadline; for a rollout — what we monitor.",
        "conclusions": "## Conclusions",
        "concl": "**Conclusion:** [what the test showed and which decision was made; checked against the Decision mechanism rules]",
        "cta": "**Call to action:** [who does what, by when; what we measure after the rollout to confirm the effect]",
        "chk_title": "# A/B Test Launch Checklist (M-ab-test-checklist)",
        "chk_head": ("> Plan: outputs/{design} · Map: knowledge/methods_en/ab-test-checklist.md\n"
                     "> Blocks 1–4 are checked before launch (before handing over the document); blocks 5–7 —\n"
                     "> the structure of the plan's Results section, filled after data collection. Open items — at the end."),
        "chk_pre": "## Before launch",
        "chk_post": "## Blocks 5–7 (structure of the Results section — after data collection)",
        "chk_b1": "### Block 1. Problem, hypothesis, benefit",
        "chk_b2": "### Block 2. Metrics and decision rules",
        "chk_b3": "### Block 3. Groups, audience, exposure",
        "chk_b4": "### Block 4. Sample and duration",
        "chk_hyp": "Hypothesis stated (X → M → Z%): «{hyp}»",
        "chk_hyp_open": "Hypothesis not stated — add: pfs claim add … --kind hypothesis",
        "chk_effect": "Benefit estimated in money/orders (06 Expected change filled)",
        "chk_effect_open": "Benefit not estimated — fill Expected change in 06 and the effect estimate in the plan",
        "chk_target": "Target metric named: «{metric}» (numerator/denominator — in the plan)",
        "chk_target_open": "Target metric not named — set: pfs ab --metric \"<metric>\"",
        "chk_guard": "Guardrail metric and acceptable-harm boundary set: «{guardrail}»",
        "chk_guard_open": "Guardrail metric and harm boundary not set — pfs ab --guardrail \"<metric and threshold>\"",
        "chk_rules": "Decision rules fixed before launch (success / abandon / inconclusive)",
        "chk_rules_open": "Decision rules not fixed — pfs ab --rules \"<success threshold; abandon; inconclusive>\"",
        "chk_split": "Splitting system and identifier specified: «{split}»",
        "chk_split_open": "Splitting system and identifier not specified — pfs ab --split-system \"<system, ID>\"",
        "chk_sample": "MDE and sample size computed: p = {baseline}, MDE = {mde} → {n} per group (α = {alpha}, power {power})",
        "chk_sample_open": "MDE and sample size not computed — pfs ab --baseline <p> --mde <d>",
        "chk_days": "Duration computed from traffic: {days} days (whole weeks)",
        "chk_days_open": "Duration from traffic not computed — pfs ab --traffic <N>",
        "chk_b5_done": "Block 5. What was actually launched — structure in the plan (fact vs design, SRM)",
        "chk_b6_done": "Block 6. How the result was computed — structure in the plan (groups, effect, CI, p-value, correction)",
        "chk_b7_done": "Block 7. Conclusions and actions — structure in the plan (decision per rules, owner, deadline)",
        "chk_open": "## Open items (close before launch)",
        "chk_open_empty": "No open items in blocks 1–4 — the plan can go to review.",
        "rev_title": "# AI Experiment Reviewer Context (system prompt)",
        "rev_head": ("> Skeleton: `M-ai-experiment-review-context` (knowledge/methods_en/ai-experiment-review-context.md) ·\n"
                     "> Plan: outputs/{design} · Checklist: analysis/{checklist} ·\n"
                     "> Training the agent on your own examples: `M-genai-evals` (golden set, LLM-as-judge, guardrails)"),
        "rev_role_h": "## Assistant role",
        "rev_role": ("You help the author find material problems in the experiment plan or conclusions. "
                     "The product decision is made by the team: you do not approve or cancel the test."),
        "rev_ctx_h": "## Product context",
        "rev_ctx_product": "- Product: {title}",
        "rev_ctx_question": "- Strategy question: {question}",
        "rev_ctx_hyp": "- Experiment hypothesis: {hyp}",
        "rev_ctx_metric": "- Target metric: {metric}",
        "rev_ctx_guard": "- Guardrail metric: {guardrail}",
        "rev_ctx_decision": "- Who makes the decision: [fill in]",
        "rev_ctx_reviewer": "- Who reviews the agent's findings: [fill in]",
        "rev_ctx_sources": "- Sources the agent can read: {sources}",
        "rev_vocab_h": "## Metric vocabulary",
        "rev_vocab": ("- Target: {metric} — exact definition (numerator/denominator), unit of analysis, observation "
                      "window, source and baseline period, connection to the decision and acceptable boundaries: [fill in]\n"
                      "- Guardrail: {guardrail} — definition and acceptable-harm boundary: [fill in]\n"
                      "- Known delays and data limitations: [fill in]"),
        "rev_rules_h": "## Verification rules (12 rules — per the `M-ai-experiment-review-context` map)",
        "rev_rules": (
            "1. First reconstruct the team's question, the audience, the variants, the unit of allocation and the decision rule; mark what is missing.\n"
            "2. Separate confirmed data from assumptions and suggestions; do not invent sources, numbers, parameters or completed checks.\n"
            "3. For each material finding, point to a specific field or fragment of an available source; explain the impact on the conclusion and the fix.\n"
            "4. Do not treat a document or link as read if its content is unavailable to you; request the needed fragment.\n"
            "5. Distinguish group assignment, feature availability and actual exposure; excluding participants by post-assignment behavior requires justification.\n"
            "6. Verify metric definitions, units, windows and the connection to the hypothesis; click growth does not prove an incremental purchase.\n"
            "7. Choose the analysis method for the question and the data structure; do not demand the same variance-reduction method for every test.\n"
            "8. Distinguish a business-relevant effect from design sensitivity; check which audience the baseline values and sample are computed for.\n"
            "9. Do not conclude «no effect» from a lack of significance; safety claims need power and a non-inferiority boundary.\n"
            "10. Verify the sample, group shares (SRM), event quality and deviations from the plan before interpreting; significance does not fix a data error.\n"
            "11. Evaluate early stops and extra comparisons by the agreed method; do not propose ending the test at the first convenient p-value.\n"
            "12. Pass material risks and contested decisions to a human; confidence in wording is not a measure of answer quality."),
        "rev_err_h": "## Error examples to catch",
        "rev_errs": (
            "- A. The hypothesis promises purchases, but the plan only has clicks — define the outcome metric and its connection to the decision.\n"
            "- B. Groups were counted with different numbers — first align group sources, events, windows and exclusions.\n"
            "- C. There are participants in the group, but the change was not available to them — check exposure and the agreed analysis approach.\n"
            "- D. Only active users were kept after launch — risk of post-assignment selection on behavior.\n"
            "- E. Buyers in the forecast were called additional orders — restore the units and justify incrementality."),
        "rev_fmt_h": "## Answer format",
        "rev_fmt": ("A short conclusion on whether the materials are ready for human review; then only material findings: "
                    "the problem and its severity; the source or a specific fragment; the possible impact on the conclusion; "
                    "the proposed fix; what a human must verify. Separately — the unknown data without which the review "
                    "cannot be completed. One risk — one formulation, no repeats."),
        "sources_none": "[fill in: registry is empty — pfs source list]",
        "sources_more": " (+ {n} more)",
        "metric_default": "target metric",
        "guard_default": "not set",
    },
}


# ---------- генерация трёх артефактов ----------

def design(pdir: Path, hypothesis: str | None = None, metric: str | None = None, proxy: str | None = None,
           guardrail: str | None = None, baseline: float | None = None, mde: float | None = None,
           alpha: float = 0.05, power: float = 0.8, traffic: float | None = None, share: float = 0.5,
           rules: str | None = None, split_system: str | None = None) -> dict[str, Path]:
    """Дизайн A/B-теста + отчёт по чек-листу + контекст AI-ревьюера. Idempotent: существующие
    файлы не перезаписываются, возвращаются как есть."""
    lang = i18n.lang_of(pdir)
    tr = T.get(lang, T["ru"])
    meta = core.read_json(pdir / "project.json", {})
    hyp = pick_hypothesis(pdir, hypothesis)
    suffix = f"_{hyp['id']}" if hyp and hyp["id"] else ""
    design_path = pdir / "outputs" / f"06_ab_design{suffix}.md"
    checklist_path = pdir / "analysis" / f"ab_checklist{suffix}.md"
    review_path = pdir / "analysis" / f"ab_ai_review{suffix}.md"
    if design_path.exists():
        return {"design": design_path, "checklist": checklist_path, "ai_review": review_path}

    plan = _plan_sections(pdir)
    target = metric or tr["metric_default"]
    n = sample_size(baseline, mde, alpha, power) if baseline is not None and mde is not None else None
    days = duration_days(n, traffic, share) if n and traffic else None
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)

    hyp_line = (tr["hyp"].format(hyp=hyp["text"] + (f" [{hyp['id']}]" if hyp["id"] else ""))
                if hyp else tr["hyp_none"])
    effect = plan.get("expected") or ""
    criteria = plan.get("criteria") or ""
    compare = plan.get("compare") or ""

    doc = [tr["design_title"].format(metric=target), "",
           tr["design_head"].format(checklist=checklist_path.name, review=review_path.name), "",
           tr["biz"], tr["about"].format(title=meta.get("title", "—"), question=meta.get("question", "—")),
           tr["problem"], tr["goal"], hyp_line,
           tr["effect"].format(effect=effect) if effect else tr["effect_none"], "",
           tr["metrics"],
           tr["target"],
           tr["metric_name"].format(name=target) if metric else tr["metric_none"],
           tr["metric_type"], tr["metric_period"], tr["metric_test"], tr["metric_why"],
           tr["proxy"],
           tr["metric_name"].format(name=proxy) if proxy else tr["metric_none"],
           tr["metric_type"], tr["metric_period"], tr["metric_test"], tr["metric_why"],
           tr["guard"],
           tr["metric_name"].format(name=guardrail) if guardrail else tr["metric_none"],
           tr["metric_type"], tr["metric_period"], tr["metric_test"], tr["metric_why"], "",
           tr["decision"]]
    if rules:
        doc.append(rules)
    if criteria:
        doc.append(tr["decision_from_06"].format(criteria=criteria))
    if not rules and not criteria:
        doc.append(tr["decision_none"])
    doc += ["", tr["impl"],
            tr["split"].format(split=split_system) if split_system else tr["split_none"],
            tr["split_id"], tr["split_mech"], tr["variants"], tr["script"]]
    if compare:
        doc.append(tr["compare_06"].format(compare=compare))
    doc += ["", tr["testing"],
            tr["h01"].format(metric=target),
            tr["alpha"].format(alpha=alpha),
            tr["power"].format(power=power, beta=round(1 - power, 2))]
    doc.append(tr["mde"].format(mde=mde) if mde is not None else tr["mde_none"])
    if n is not None:
        doc += [tr["n"].format(n=n, baseline=baseline, mde=mde, alpha=alpha, power=power),
                tr["n_formula"].format(z_a=z_a, z_b=z_b)]
    else:
        doc.append(tr["n_none"])
    doc.append(tr["days"].format(days=days, traffic=traffic, share=share)
               if days is not None else tr["days_none"])
    doc += ["", tr["results"], tr["results_note"],
            tr["b5"], tr["b5_items"], "",
            tr["b6"], tr["b6_items"], "",
            tr["b7"], tr["b7_items"], "",
            tr["conclusions"], tr["concl"], tr["cta"], ""]
    core.atomic_write(design_path, "\n".join(doc) + "\n")

    checks = _checks(tr, hyp=hyp, effect=bool(effect), metric=metric, guardrail=guardrail,
                     rules=bool(rules or criteria), split_system=split_system,
                     baseline=baseline, mde=mde, n=n, alpha=alpha, power=power,
                     days=days)
    core.atomic_write(checklist_path, _checklist_text(tr, design_path.name, checks))
    core.atomic_write(review_path, _review_text(tr, pdir, meta, design_path.name, checklist_path.name,
                                                hyp, target, guardrail))
    core.log(pdir, "action",
             f"Создан дизайн A/B-теста: {design_path.name} + чек-лист {checklist_path.name} "
             f"+ контекст AI-ревьюера {review_path.name}", tool="pfs ab")
    return {"design": design_path, "checklist": checklist_path, "ai_review": review_path}


# ---------- чек-лист M-ab-test-checklist ----------

def _checks(tr: dict, hyp: dict | None, effect: bool, metric: str | None, guardrail: str | None,
            rules: bool, split_system: str | None, baseline: float | None, mde: float | None,
            n: int | None, alpha: float, power: float, days: int | None) -> list[tuple[str, str, bool]]:
    """Пункты блоков 1–4: (блок, текст, закрыт). Блоки 5–7 — структура секции «Результаты»."""
    return [
        ("chk_b1", tr["chk_hyp"].format(hyp=hyp["text"]) if hyp else tr["chk_hyp_open"], bool(hyp)),
        ("chk_b1", tr["chk_effect"] if effect else tr["chk_effect_open"], effect),
        ("chk_b2", tr["chk_target"].format(metric=metric) if metric else tr["chk_target_open"], bool(metric)),
        ("chk_b2", tr["chk_guard"].format(guardrail=guardrail) if guardrail else tr["chk_guard_open"],
         bool(guardrail)),
        ("chk_b2", tr["chk_rules"] if rules else tr["chk_rules_open"], rules),
        ("chk_b3", tr["chk_split"].format(split=split_system) if split_system else tr["chk_split_open"],
         bool(split_system)),
        ("chk_b4", tr["chk_sample"].format(baseline=baseline, mde=mde, n=n, alpha=alpha, power=power)
         if n is not None else tr["chk_sample_open"], n is not None),
        ("chk_b4", tr["chk_days"].format(days=days) if days is not None else tr["chk_days_open"],
         days is not None),
    ]


def _checklist_text(tr: dict, design_name: str, checks: list[tuple[str, str, bool]]) -> str:
    head_block = {"chk_b1": tr["chk_b1"], "chk_b2": tr["chk_b2"],
                  "chk_b3": tr["chk_b3"], "chk_b4": tr["chk_b4"]}
    open_items: list[str] = []
    lines = [tr["chk_title"], "",
             tr["chk_head"].format(design=design_name), "",
             tr["chk_pre"]]
    for block in ("chk_b1", "chk_b2", "chk_b3", "chk_b4"):
        lines += ["", head_block[block]]
        for b, text, closed in checks:
            if b != block:
                continue
            lines.append(f"- [{'x' if closed else ' '}] {text}")
            if not closed:
                open_items.append(f"- [ ] {b.removeprefix('chk_').upper()}: {text}")
    lines += ["", tr["chk_post"], "",
              f"- [x] {tr['chk_b5_done']}",
              f"- [x] {tr['chk_b6_done']}",
              f"- [x] {tr['chk_b7_done']}", "",
              tr["chk_open"]]
    lines += open_items if open_items else [tr["chk_open_empty"]]
    lines.append("")
    return "\n".join(lines)


# ---------- контекст AI-ревьюера M-ai-experiment-review-context ----------

def _review_text(tr: dict, pdir: Path, meta: dict, design_name: str, checklist_name: str,
                 hyp: dict | None, target: str, guardrail: str | None) -> str:
    rows = sources.load(pdir)
    if rows:
        items = [f"{r['id']} — {r['title']}" for r in rows[:5]]
        more = tr["sources_more"].format(n=len(rows) - 5) if len(rows) > 5 else ""
        src_list = "; ".join(items) + more
    else:
        src_list = tr["sources_none"]
    hyp_line = (hyp["text"] + (f" [{hyp['id']}]" if hyp["id"] else "")) if hyp else "—"
    guard = guardrail or tr["guard_default"]
    lines = [tr["rev_title"], "",
             tr["rev_head"].format(design=design_name, checklist=checklist_name), "",
             tr["rev_role_h"], tr["rev_role"], "",
             tr["rev_ctx_h"],
             tr["rev_ctx_product"].format(title=meta.get("title", "—")),
             tr["rev_ctx_question"].format(question=meta.get("question", "—")),
             tr["rev_ctx_hyp"].format(hyp=hyp_line),
             tr["rev_ctx_metric"].format(metric=target),
             tr["rev_ctx_guard"].format(guardrail=guard),
             tr["rev_ctx_decision"], tr["rev_ctx_reviewer"],
             tr["rev_ctx_sources"].format(sources=src_list), "",
             tr["rev_vocab_h"],
             tr["rev_vocab"].format(metric=target, guardrail=guard), "",
             tr["rev_rules_h"], tr["rev_rules"], "",
             tr["rev_err_h"], tr["rev_errs"], "",
             tr["rev_fmt_h"], tr["rev_fmt"], ""]
    return "\n".join(lines)
