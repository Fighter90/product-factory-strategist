"""Маршрутизация запроса: сценарий работы → методические карты → модели по шагам.

Детерминированный классификатор по ключевым словам (бесплатно и воспроизводимо). Если уверенность
низкая — агент задаёт уточняющий вопрос или вызывает субагента router на дешёвой модели.
Ошибочный выбор исправляется: pfs route --override <сценарий> (фиксируется в журнале).
"""
from __future__ import annotations

import re
from pathlib import Path

from . import core, models

SCENARIOS = {
    "retention": {
        "title": "Падает удержание / растёт отток",
        "keywords": ["удержан", "отток", "churn", "retention", "уходят", "отписыва", "возвращаемост", "когорт", "продлен", "подписчик", "не продлева"],
        "cards": ["M-product-metrics", "M-success-metrics", "M-problem-design", "M-jtbd", "M-cjm", "M-in-depth-interviews",
                  "M-quant-methods", "M-unit-economics", "M-goals-drivers-bets"],
        "decision_questions": ["Где в пути пользователя теряется ценность (когорты, шаги воронки)?",
                               "Это продукт, цена, конкуренты или внешний фактор?",
                               "Какие сегменты уходят, а какие остаются, и чем они отличаются?"],
    },
    "go_to_market": {
        "title": "Кому и как продавать новый сервис",
        "keywords": ["кому продавать", "запуск", "вывод на рынок", "go-to-market", "gtm", "сегмент", "целев", "новый сервис",
                     "аудитори", "канал продаж", "пилот", "продавать"],
        "cards": ["M-customers", "M-audience-research", "M-market-sizing", "M-competitors", "M-jtbd", "M-business-models",
                  "M-mvp-pilots", "M-monetization", "M-growth-frameworks"],
        "decision_questions": ["Какой сегмент имеет самую острую задачу и доступен через наши каналы?",
                               "Каков реалистичный SOM, а не TAM?", "Чем нас заменяют сейчас (альтернативы по JTBD)?"],
    },
    "messaging": {
        "title": "Что сказать аудитории, чтобы она поняла ценность",
        "keywords": ["сообщени", "коммуникац", "позиционир", "ценност", "понял", "донести", "месседж", "usp", "утп", "бренд", "реклам", "что сказать", "объяснить", "не понимают"],
        "cards": ["M-usp", "M-product-communication", "M-jtbd", "M-audience-research", "M-marketing-research",
                  "M-competitors", "M-cjm", "M-loyalty-metrics"],
        "decision_questions": ["Какой барьер мешает: непонимание, недоверие, цена, привычка?",
                               "Какое обещание продукт реально выполняет (подтверждения)?",
                               "В какой ситуации человек принимает решение и через какой канал?"],
    },
    "monetization": {
        "title": "Цена, тарифы, модель монетизации",
        "keywords": ["цена", "тариф", "монетиз", "подписк", "платн", "бесплатн", "arpu", "ltv", "выручк", "pricing"],
        "cards": ["M-monetization", "M-unit-economics", "M-traction-model", "M-benchmarking", "M-competitors", "M-quant-methods"],
        "decision_questions": ["Какая value metric связана с ценностью для клиента?", "Сойдётся ли юнит-экономика (LTV/CAC)?",
                               "Что произойдёт с каннибализацией и оттоком?"],
    },
    "growth": {
        "title": "Продукт не растёт / стратегия роста",
        "keywords": ["не растёт", "не растет", "рост", "стратеги", "драйвер", "north star", "nsm", "масштаб", "okr", "роадмап"],
        "cards": ["M-strategy-growth", "M-success-metrics", "M-goals-drivers-bets", "M-growth-frameworks", "M-external-environment",
                  "M-competitors", "M-outcome-roadmap", "M-risks", "M-pmf-scaling"],
        "decision_questions": ["Какой драйвер роста даёт наибольший вклад в NSM?", "Есть ли PMF в ключевом сегменте?",
                               "Какие внешние факторы меняют потолок рынка?"],
    },
    "keep_or_kill": {
        "title": "Развивать, оставить или закрыть направление",
        "keywords": ["закрыть", "свернуть", "оставить", "продолжать ли", "окупает", "убыточ", "kill", "сократить"],
        "cards": ["M-unit-economics", "M-traction-model", "M-pmf-scaling", "M-risks", "M-strategy-growth", "M-decision-daci"],
        "decision_questions": ["Какой вклад направления в выручку/удержание ядра (включая косвенный)?",
                               "Что потеряем при закрытии и как это измерить?", "Какие условия сделали бы продолжение оправданным?"],
    },
}

STEP_TASKS = [("intake", "intake"), ("sources", "desk_research"), ("research", "desk_research"),
              ("situation", "situation"), ("options", "options"), ("options (red team)", "red_team"),
              ("strategy", "strategy"), ("validation", "validation_plan"), ("review", "judge")]


def classify(request: str) -> list[tuple[str, int]]:
    low = request.lower()
    scores = []
    for sid, sc in SCENARIOS.items():
        score = sum(1 for kw in sc["keywords"] if kw in low)
        if score:
            scores.append((sid, score))
    return sorted(scores, key=lambda x: -x[1])


def route(request: str, override: str | None = None, economy: bool = False, pdir: Path | None = None) -> dict:
    ranked = classify(request)
    if override:
        if override not in SCENARIOS:
            raise core.PfsError(f"Сценарий: {', '.join(SCENARIOS)}")
        primary, confidence = override, "override"
        if pdir:
            core.log(pdir, "route", f"Сценарий исправлен вручную: {ranked[0][0] if ranked else '—'} → {override}")
    elif not ranked:
        primary, confidence = "growth", "low"
    else:
        primary = ranked[0][0]
        top = ranked[0][1]
        second = ranked[1][1] if len(ranked) > 1 else 0
        confidence = "high" if top >= 2 and top > second else ("medium" if top > second else "low")
    secondary = [s for s, _ in ranked if s != primary][:2]
    cards: list[str] = []  # основной сценарий целиком + по 3 карты смежных
    for s in [primary] + secondary:
        for c in (SCENARIOS[s]["cards"] if s == primary else SCENARIOS[s]["cards"][:3]):
            if c not in cards:
                cards.append(c)
    plan = []
    for step, task in STEP_TASKS:
        m = models.pick(task, economy=economy)
        plan.append({"step": step, "task": task, "model": m["model"], "effort": m["effort"]})
    res = {"scenario": primary, "title": SCENARIOS[primary]["title"], "confidence": confidence,
           "secondary": secondary, "cards": cards, "decision_questions": SCENARIOS[primary]["decision_questions"],
           "model_plan": plan}
    if pdir:
        core.log(pdir, "route", f"Сценарий: {primary} ({confidence}); доп.: {', '.join(secondary) or '—'}")
    return res


def route_text(res: dict) -> str:
    out = [f"Сценарий: {res['scenario']} — {res['title']} (уверенность: {res['confidence']})"]
    if res["secondary"]:
        out.append(f"Смежные сценарии: {', '.join(res['secondary'])}")
    if res["confidence"] == "low":
        out.append("⚠ Низкая уверенность: задайте руководителю уточняющий вопрос о цели или исправьте: --override <сценарий>")
    out.append("Методические карты (читать в этом порядке): " + ", ".join(res["cards"]))
    out.append("Вопросы, которые могут изменить решение:")
    out += [f"  - {q}" for q in res["decision_questions"]]
    out.append("План моделей по шагам:")
    out += [f"  {p['step']:<20} {p['model']:<20} effort={p['effort']}" for p in res["model_plan"]]
    return "\n".join(out)
