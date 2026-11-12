"""Учёт стоимости: токены из транскриптов Claude Code + сессий OpenCode + ручные записи
(поиск, время человека). PRO-62: подписочные планы (zai-coding-plan) показывают фактическую
оплату $0, но с ненулевым «эквивалентом по API-ценам», пометкой «подписочный план»,
разбивкой по шагам процесса (intake…monitoring), кэшем, временем сессий и повторами."""
from __future__ import annotations

import json
import math
from pathlib import Path

from . import core, i18n

# Подписочные провайдеры: оплата планом, а не за токен — фактическая цена $0,
# в отчёте показываем эквивалент по API-ценам и пометку «подписочный план» (PRO-62).
PLAN_PROVIDERS = {"zai-coding-plan"}

# Тарифицируемые составляющие токенов; служебные поля строки модели — не токены.
TOKEN_KEYS = ("input", "output", "cache_write", "cache_read")
NON_TOKEN_KEYS = ("messages", "plan", "plan_provider")

# Реестровые *.jsonl в корне проекта (PRO-30): транскриптами сессий не считаются.
REGISTRY_JSONL = {"claims.jsonl", "sources.jsonl", "decisions.jsonl", "log.jsonl"}
TRANSCRIPT_PATTERNS = ("*_session.json", "*.jsonl")  # OpenCode session.json и Claude Code jsonl


def pricing() -> dict:
    return core.read_json(core.CONFIG / "pricing.json", {"models": {}, "usd_rub": 95.0})


def _price_for(model: str, p: dict) -> dict:
    models = p.get("models", {})
    if model in models:
        return models[model]
    for key, val in models.items():  # claude-opus-5-5-xxxx → claude-opus-5-5; glm-5.3-flash → glm-5.3
        if model.startswith(key):
            return val
    return models.get(p.get("fallback_model", ""), {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0})


def model_cost(model: str, t: dict, p: dict | None = None) -> float:
    """Стоимость токенов одной модели по прайсу (USD). План-модели считаются так же —
    это эквивалент по API-ценам; «фактическая оплата $0» обеспечивается на уровне price()."""
    pr = _price_for(model, p or pricing())
    return sum((t.get(k) or 0) * pr.get(k, 0) for k in TOKEN_KEYS) / 1_000_000


def price(per_model: dict, include_plan: bool = False) -> float:
    """Фактическая оплата (include_plan=False: план-модели = $0) или эквивалент
    по API-ценам (include_plan=True: план-модели по прайсу, PRO-62)."""
    p = pricing()
    usd = 0.0
    for model, t in per_model.items():
        if t.get("plan") and not include_plan:
            continue  # подписка: фактическая цена $0
        usd += model_cost(model, t, p)
    return usd


def _ms_to_iso(ms) -> str | None:
    if not ms:
        return None
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def _ts_key(ts: str | None) -> str | None:
    """Нормализация ISO-времени к UTC-строке: метки из разных источников приходят
    с разными смещениями («+03:00» из core.now() и «Z» из транскриптов), лексикографическое
    сравнение сырых строк при этом ошибается."""
    if not ts:
        return None
    try:
        from datetime import datetime, timezone
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")) \
            .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return str(ts)


def _retry_runs(messages: list) -> int:
    """Повторы: assistant-ответы подряд (без user между ними) сверх первого в серии."""
    n, prev_asst = 0, False
    for m in messages:
        if not isinstance(m, dict):
            continue
        if m.get("type") == "assistant":
            if prev_asst:
                n += 1
            prev_asst = True
        elif m.get("type") == "user":
            prev_asst = False
    return n


def _retry_models(rows: list) -> dict:
    """Токены повторов по моделям (для стоимости повторов; PRO-62)."""
    out: dict[str, dict] = {}
    for r in rows:
        if not r.get("retry"):
            continue
        acc = out.setdefault(r["model"], {k: 0 for k in TOKEN_KEYS})
        for k in TOKEN_KEYS:
            acc[k] += r.get(k, 0) or 0
    return out


_NO_RETRIES = {"messages": 0, "models": {}}


def _parse_opencode(data: dict, since: str | None = None, until: str | None = None) -> dict:
    per, _rows, _minutes, _retries, _end = _parse_opencode_full(data, since, until)
    return per


def _parse_opencode_full(data: dict, since: str | None = None, until: str | None = None):
    """OpenCode session.json → (по моделям, строки сообщений для разбивки по шагам,
    минуты сессии, повторы, время конца сессии).

    Итог info.tokens отсутствует (частичный экспорт) — складываем tokens из
    assistant-сообщений и запоминаем время каждого сообщения: шаг процесса
    определяется по моменту сообщения (PRO-62). Итог есть — берём его один раз
    (агрегат OpenCode обновляется по ходу работы, tokens сообщений не суммируются
    с итогом), а разбивка по шагам падает на конец сессии. reasoning тарифицируется
    как output.
    """
    info = data.get("info") or {}
    tokens = info.get("tokens") or {}
    cache = tokens.get("cache") or {}
    model = info.get("model") or {}
    start_ms = (info.get("time") or {}).get("created")
    end_ms = (info.get("time") or {}).get("updated")
    start, end = _ms_to_iso(start_ms), _ms_to_iso(end_ms)
    if (since and end and end < since) or (until and start and start > until):
        return {}, [], 0.0, dict(_NO_RETRIES), None  # сессия целиком вне окна задачи
    provider = model.get("providerID")
    mid = model.get("id") or "unknown"
    messages = [m for m in data.get("messages", []) if isinstance(m, dict)]
    minutes = round(((end_ms or 0) - (start_ms or 0)) / 60_000, 1)
    retries = {"messages": _retry_runs(messages), "models": {}}
    if not (tokens.get("input") or tokens.get("output") or tokens.get("reasoning")
            or cache.get("read") or cache.get("write")):
        per: dict[str, dict] = {}
        rows: list[dict] = []
        prev_asst = False
        for m in messages:
            if m.get("type") == "user":
                prev_asst = False
                continue
            if m.get("type") != "assistant" or not isinstance(m.get("tokens"), dict):
                continue
            t = m["tokens"]
            c = t.get("cache") or {}
            mdl = m.get("model") if isinstance(m.get("model"), dict) else {}
            row = {"ts": _ms_to_iso((m.get("time") or {}).get("created")),
                   "model": mdl.get("id") or "unknown",
                   "input": t.get("input", 0) or 0,
                   "output": (t.get("output", 0) or 0) + (t.get("reasoning", 0) or 0),
                   "cache_write": c.get("write", 0) or 0,
                   "cache_read": c.get("read", 0) or 0,
                   "retry": prev_asst}
            prev_asst = True
            rows.append(row)
            acc = per.setdefault(row["model"],
                                 {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "messages": 0})
            for k in TOKEN_KEYS:
                acc[k] += row[k]
            acc["messages"] += 1
            if mdl.get("providerID") in PLAN_PROVIDERS:
                acc["plan"] = 1
                acc["plan_provider"] = mdl["providerID"]
        retries["models"] = _retry_models(rows)
        return per, rows, minutes, retries, end
    per = {mid: {"input": tokens.get("input", 0) or 0,
                 "output": (tokens.get("output", 0) or 0) + (tokens.get("reasoning", 0) or 0),
                 "cache_write": cache.get("write", 0) or 0,
                 "cache_read": cache.get("read", 0) or 0,
                 "messages": sum(1 for m in messages if m.get("type") == "assistant")}}
    if provider in PLAN_PROVIDERS:
        per[mid]["plan"] = 1  # подписка: фактическая цена $0, пометка «plan» + эквивалент
        per[mid]["plan_provider"] = provider
    return per, [], minutes, retries, end  # агрегат: разбивки по сообщениям нет


def parse_detail(path: Path, since: str | None = None, until: str | None = None) -> tuple:
    """parse_transcript + детали отчёта PRO-62: (по моделям, строки сообщений
    {ts, model, input, output, cache_write, cache_read, retry} для разбивки по шагам,
    минуты сессии, повторы {messages, models}, время конца сессии)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        whole = json.loads(text)
    except json.JSONDecodeError:
        whole = None
    if isinstance(whole, dict) and isinstance(whole.get("info"), dict) and isinstance(whole.get("messages"), list):
        return _parse_opencode_full(whole, since, until)
    seen: set[str] = set()
    per_model: dict[str, dict] = {}
    rows: list[dict] = []
    stamps: list[str] = []
    files = [text]
    sub = path.with_suffix("") / "subagents"  # транскрипты субагентов лежат рядом
    if sub.is_dir():
        files += [f.read_text(encoding="utf-8", errors="replace") for f in sorted(sub.glob("*.jsonl"))]
    prev_asst = False
    for content in files:
        for line in content.splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = row.get("message") if isinstance(row, dict) else None
            if not isinstance(msg, dict) or not isinstance(msg.get("usage"), dict):
                continue
            ts = str(row.get("timestamp") or "")
            if ts and ((since and ts < since) or (until and ts > until)):
                continue  # учитываем только сообщения внутри окна задачи
            mid = msg.get("id") or row.get("uuid")
            if mid in seen:
                continue
            seen.add(mid)
            u = msg["usage"]
            mdl = msg.get("model", "unknown")
            m = per_model.setdefault(mdl, {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "messages": 0})
            m["input"] += u.get("input_tokens", 0) or 0
            m["output"] += u.get("output_tokens", 0) or 0
            m["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0
            m["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
            m["messages"] += 1
            rtype = row.get("type")
            is_retry = bool(ts and rtype == "assistant" and prev_asst)
            if rtype == "assistant":
                prev_asst = True
            elif rtype == "user":
                prev_asst = False
            if ts:
                rows.append({"ts": ts, "model": mdl,
                             "input": u.get("input_tokens", 0) or 0,
                             "output": u.get("output_tokens", 0) or 0,
                             "cache_write": u.get("cache_creation_input_tokens", 0) or 0,
                             "cache_read": u.get("cache_read_input_tokens", 0) or 0,
                             "retry": is_retry})
                stamps.append(ts)
    retries = {"messages": sum(1 for r in rows if r.get("retry")), "models": _retry_models(rows)}
    return per_model, rows, 0.0, retries, (max(stamps) if stamps else None)


def parse_transcript(path: Path, since: str | None = None, until: str | None = None) -> dict:
    """Суммирует usage по моделям. Форматы: Claude Code jsonl (message.usage) и OpenCode session.json
    (единый JSON-объект info.tokens). Одно сообщение может занимать несколько строк — считаем по message.id один раз."""
    return parse_detail(path, since, until)[0]


# ---------- разбивка по шагам процесса (PRO-62) ----------

def _step_bounds(pdir: Path) -> list[tuple[str, str]]:
    """Границы шагов: события kind=step из log.jsonl (`pfs step …`), отсортированные по времени."""
    bounds = [(_ts_key(r.get("ts")) or str(r.get("ts")), str(r["step"]))
              for r in core.read_jsonl(pdir / "log.jsonl")
              if r.get("kind") == "step" and r.get("step") and r.get("ts")]
    return sorted(bounds)


def _step_at(bounds: list[tuple[str, str]], ts: str | None) -> str:
    """Шаг, активный в момент ts; до первой отметки — intake (первый шаг процесса)."""
    cur = "intake"
    for bts, stp in bounds:
        if ts and bts <= ts:
            cur = stp
        else:
            break
    return cur


def step_breakdown(pdir: Path, per_model: dict, rows: list, fallback_ts: str | None = None) -> dict:
    """Токены сессии по шагам процесса (intake…monitoring; PRO-62): каждое сообщение
    транскрипта — к шагу, активному на момент сообщения; когда разбивки по сообщениям
    нет (агрегат OpenCode), сессия целиком относится к шагу на момент fallback_ts
    (конец сессии). Пустые шаги не записываются."""
    bounds = _step_bounds(pdir)
    out: dict[str, dict] = {}

    def cell(stp: str, model: str) -> dict:
        return out.setdefault(stp, {}).setdefault(model, {k: 0 for k in TOKEN_KEYS})

    if rows:
        for r in rows:
            c = cell(_step_at(bounds, r.get("ts") or fallback_ts), r["model"])
            for k in TOKEN_KEYS:
                c[k] += r.get(k, 0) or 0
    else:
        stp = _step_at(bounds, fallback_ts) if fallback_ts else (bounds[-1][1] if bounds else "intake")
        for model, t in per_model.items():
            c = cell(stp, model)
            for k in TOKEN_KEYS:
                c[k] += (t or {}).get(k, 0) or 0
    return {stp: models for stp, models in out.items()
            if any(any((c or {}).get(k) for k in TOKEN_KEYS) for c in models.values())}


def _fmt(n) -> str:
    """Число с пробелами-разрядителями для отчёта."""
    return f"{n:,}".replace(",", " ")


def _plural(n: int, one: str, few: str, many: str) -> str:
    """Русская форма существительного после числа: 1 сообщение, 2 сообщения, 5 сообщений."""
    n = abs(n) % 100
    if 11 <= n <= 14:
        return many
    n %= 10
    if n == 1:
        return one
    if 2 <= n <= 4:
        return few
    return many


# ---------- запись сессии и сводка ----------

def record_session(pdir: Path, session_id: str, transcript: Path, since: str | None = None,
                   until: str | None = None) -> dict:
    """Идемпотентно: повторный вызов перезаписывает запись сессии, а не суммирует её дважды.

    Один чат может охватывать несколько задач, поэтому по умолчанию учитываются только сообщения
    после создания проекта (since = project.json → created).
    PRO-62: вместе с фактической оплатой (usd, план = $0) записываются эквивалент
    по API-ценам (usd_equivalent), разбивка по шагам (by_step), минуты сессии и повторы.
    """
    meta = core.read_json(pdir / "project.json", {})
    window = meta.get("cost_window", {})
    if not since:
        since = window.get("since") or (_utc(meta["created"]) if meta.get("created") else None)
    until = until or window.get("until")
    per_model, rows, minutes, retries, end_iso = parse_detail(transcript, since, until)
    rec = {"models": per_model,
           "usd": round(price(per_model), 4),
           "usd_equivalent": round(price(per_model, include_plan=True), 4),
           "by_step": step_breakdown(pdir, per_model, rows, end_iso),
           "time_minutes": minutes,
           "retries": {"messages": retries.get("messages", 0), "models": retries.get("models", {}),
                       "usd_equivalent": round(price(retries.get("models", {}), include_plan=True), 4)},
           "updated": core.now(),
           "stage": core.read_json(pdir / "state.json", {}).get("stage"),
           "since": since, "until": until}
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    prev = data["sessions"].get(session_id)
    if prev and all(prev.get(k) == v for k, v in rec.items() if k != "updated"):
        return prev  # ничего не изменилось — файл не трогаем (нет лишних изменений в git)
    data["sessions"][session_id] = rec
    core.write_json(pdir / "costs.json", data)
    return rec


def set_window(pdir: Path, since: str | None = None, until: str | None = None) -> dict:
    """Зафиксировать окно учёта: после until хук Stop не относит расходы чата к проекту."""
    meta = core.read_json(pdir / "project.json", {})
    w = meta.setdefault("cost_window", {})
    if since:
        w["since"] = since
    if until:
        w["until"] = until
    core.write_json(pdir / "project.json", meta)
    core.log(pdir, "cost", f"Окно учёта стоимости: {w}")
    return w


def set_plan_tariff(pdir: Path, month_usd: float) -> dict:
    """Указать фактический тариф подписки (USD/мес, PRO-62): сводка отдельно покажет
    долю подписки, отнесённую к проекту. Тариф конкретного плана — по умолчанию из
    config/pricing.json → plans → user_month_usd."""
    meta = core.read_json(pdir / "project.json", {})
    meta["plan_month_usd"] = float(month_usd)
    core.write_json(pdir / "project.json", meta)
    core.log(pdir, "cost", f"Тариф подписки: ${meta['plan_month_usd']:g}/мес")
    return {"plan_month_usd": meta["plan_month_usd"]}


def plan_share(pdir: Path, p: dict | None = None) -> dict:
    """Фактическая доля подписки (PRO-62): тариф указан — месячная цена, отнесённая
    к проекту пропорционально сроку учёта (окно cost_window или границы сессий;
    минимум один день подписки). Тариф не указан — {} (остаётся только эквивалент
    по API-ценам)."""
    meta = core.read_json(pdir / "project.json", {})
    cfg = (p or pricing()).get("plans", {}).get("zai-coding-plan", {})
    month = meta.get("plan_month_usd") or cfg.get("user_month_usd")
    if not month:
        return {}
    data = core.read_json(pdir / "costs.json", {"sessions": {}})
    window = meta.get("cost_window") or {}
    starts = [_ts_key(s.get("since")) for s in data["sessions"].values() if s.get("since")]
    ends = [e for e in (_ts_key(s.get("until")) or _ts_key(s.get("updated"))
                        for s in data["sessions"].values()) if e]
    start = _ts_key(window.get("since")) or (min(starts) if starts else None)
    end = _ts_key(window.get("until")) or (max(ends) if ends else None)
    days = 1
    if start and end:
        from datetime import datetime
        try:
            span = (datetime.fromisoformat(end.replace("Z", "+00:00"))
                    - datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds() / 86_400
            days = max(1, math.ceil(span))
        except ValueError:
            days = 1
    tier = next((name for name, val in (cfg.get("tiers_month_usd") or {}).items()
                 if abs(val - float(month)) < 0.01), "")
    return {"month_usd": float(month), "tier": tier, "days": days,
            "usd": round(float(month) * days / 30, 2)}


def add_manual(pdir: Path, what: str, usd: float = 0.0, human_minutes: float = 0.0) -> None:
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    data["manual"].append({"ts": core.now(), "what": what, "usd": usd, "human_minutes": human_minutes})
    core.write_json(pdir / "costs.json", data)
    core.log(pdir, "cost", f"{what}: ${usd:.2f}, человек {human_minutes:.0f} мин")


def summary(pdir: Path) -> dict:
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    p = pricing()
    manual_usd = sum(m.get("usd", 0) for m in data["manual"])
    usd = sum(s["usd"] for s in data["sessions"].values()) + manual_usd
    usd_eq = manual_usd  # ручные записи — факт = эквивалент
    tokens = 0
    by_model: dict[str, float] = {}
    by_model_tokens: dict[str, dict] = {}
    by_step: dict[str, dict] = {}
    time_minutes = 0.0
    retries_msgs = retries_tokens = 0
    retries_usd = 0.0
    plan_providers: set[str] = set()
    has_plan = False
    for s in data["sessions"].values():
        for model, t in s["models"].items():
            if not isinstance(t, dict):
                continue
            tokens += sum(v for k, v in t.items()
                          if k not in NON_TOKEN_KEYS and isinstance(v, (int, float)))
            label = f"{model} (plan)" if t.get("plan") else model
            if t.get("plan"):
                has_plan = True
                if t.get("plan_provider"):
                    plan_providers.add(str(t["plan_provider"]))
            # план-модели: в таблице моделей показываем эквивалент по API-ценам
            by_model[label] = by_model.get(label, 0.0) + model_cost(model, t, p)
            acc = by_model_tokens.setdefault(label, {k: 0 for k in TOKEN_KEYS})
            for k in TOKEN_KEYS:
                acc[k] += t.get(k, 0) or 0
        usd_eq += s.get("usd_equivalent", s.get("usd", 0.0))
        time_minutes += s.get("time_minutes") or 0.0
        r = s.get("retries") or {}
        retries_msgs += r.get("messages", 0) or 0
        rmodels = r.get("models") or {}
        retries_tokens += sum(sum(c.values()) for c in rmodels.values())
        retries_usd += price(rmodels, include_plan=True)
        for stp, models in (s.get("by_step") or {}).items():
            acc = by_step.setdefault(stp, {})
            for model, tk in models.items():
                dst = acc.setdefault(model, {k: 0 for k in TOKEN_KEYS})
                for k in TOKEN_KEYS:
                    dst[k] += (tk or {}).get(k, 0) or 0
    # записи до PRO-62 (без by_step): сессия целиком к шагу, зафиксированному при записи
    for s in data["sessions"].values():
        if s.get("by_step"):
            continue
        acc = by_step.setdefault(s.get("stage") or "intake", {})
        for model, t in s["models"].items():
            dst = acc.setdefault(model, {k: 0 for k in TOKEN_KEYS})
            for k in TOKEN_KEYS:
                dst[k] += (t or {}).get(k, 0) or 0
    human = sum(m.get("human_minutes", 0) for m in data["manual"])
    rate = p.get("usd_rub", 95.0)
    return {"usd": usd, "rub": usd * rate,
            "usd_equivalent": usd_eq, "rub_equivalent": usd_eq * rate,
            "tokens": tokens, "sessions": len(data["sessions"]),
            "by_model": by_model, "by_model_tokens": by_model_tokens,
            "by_step": by_step, "time_minutes": time_minutes, "human_minutes": human,
            "retries": {"messages": retries_msgs, "tokens": retries_tokens,
                        "usd_equivalent": round(retries_usd, 4)},
            "plan": has_plan, "plan_providers": sorted(plan_providers),
            "plan_share": plan_share(pdir, p)}


def summary_text(pdir: Path, lang: str = "ru") -> str:
    """Отчёт `pfs cost` и Приложение D отчёта/six-pager: фактическая оплата и эквивалент
    по API-ценам, пометка «подписочный план», разбивка по моделям (с кэшем) и шагам
    процесса, время сессий и минуты человека, повторы и доля подписки (PRO-62).
    Язык — параметр (по умолчанию ru; PRO-57: pfs cost и REPORT — по языку проекта)."""
    s = summary(pdir)
    p = pricing()
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    out = [tr("cost_total", usd=s["usd"], rub=s["rub"], usd_eq=s["usd_equivalent"],
              rub_eq=s["rub_equivalent"], sessions=s["sessions"], tokens=_fmt(s["tokens"]),
              tmin=s["time_minutes"], hmin=s["human_minutes"])]
    if s["plan"]:
        prov = ", ".join(s["plan_providers"]) or tr("cost_plan_default")
        out.append(tr("cost_plan", prov=prov, usd=s["usd"], usd_eq=s["usd_equivalent"]))
    if s["by_model"]:
        out.append(tr("cost_by_models"))
        for m, v in sorted(s["by_model"].items(), key=lambda x: -x[1]):
            tk = s["by_model_tokens"].get(m, {})
            out.append(tr("cost_by_model_row", model=m, usd=v, tokens=_fmt(sum(tk.values())),
                          inp=_fmt(tk.get("input", 0)), outp=_fmt(tk.get("output", 0)),
                          cr=_fmt(tk.get("cache_read", 0)), cw=_fmt(tk.get("cache_write", 0))))
    if s["by_step"]:
        out.append(tr("cost_by_steps"))
        order = {sid: i for i, sid in enumerate(core.STAGE_IDS)}
        for stp in sorted(s["by_step"], key=lambda x: (order.get(x, len(order)), x)):
            models = s["by_step"][stp]
            tk = sum(sum((c or {}).get(k, 0) for k in TOKEN_KEYS) for c in models.values())
            stp_usd = sum(model_cost(m, c, p) for m, c in models.items())
            out.append(tr("cost_by_step_row", step=stp, tokens=_fmt(tk), usd=stp_usd))
    r = s["retries"]
    if r["messages"]:
        tail = (tr("cost_retries_tail_tokens", tokens=_fmt(r["tokens"])) if r["tokens"]
                else tr("cost_retries_tail_unknown"))
        if r["usd_equivalent"]:
            tail += tr("cost_retries_tail_equiv", usd=r["usd_equivalent"])
        word = (_plural(r["messages"], "сообщение", "сообщения", "сообщений") if lang == "ru"
                else ("message" if r["messages"] == 1 else "messages"))
        out.append(tr("cost_retries", n=r["messages"], word=word, tail=tail))
    share = s["plan_share"]
    if share:
        head = f"{share['tier']}, " if share.get("tier") else ""
        out.append(tr("cost_plan_share", head=head, month_usd=share["month_usd"],
                      days=share["days"], usd=share["usd"]))
    return "\n".join(out)


def _utc(iso: str) -> str:
    from datetime import datetime, timezone
    return datetime.fromisoformat(iso).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def find_transcript(pdir: Path, hint: str | None = None) -> Path:
    """Транскрипт сессии в корне проекта (PRO-30): формат детектится сам при разборе.

    hint — путь (относительный резолвится от каталога проекта, см. core.resolve_input),
    часть имени файла или None/пусто. Без hint — самый свежий кандидат из
    *_session.json (OpenCode) и *.jsonl (Claude Code) в корне проекта; реестровые
    *.jsonl (claims/sources/decisions/log) транскриптами не считаются — и при переборе,
    и при явно указанном пути (ревью round 3). По hint двусмысленность — ошибка со
    списком всех кандидатов (ревью round 3: без обрезки), не угадываем; равное mtime
    разбирается по имени файла (детерминированный выбор).
    """
    if hint and hint.strip():
        exact = core.resolve_input(hint.strip(), pdir)
        if exact.is_file():
            if exact.name not in REGISTRY_JSONL:
                return exact
            raise core.PfsError("«" + exact.name + "» — реестровый файл проекта "
                                "(claims/sources/decisions/log.jsonl), транскриптом сессии не считается")
    pats = (f"*{hint.strip()}*_session.json", f"*{hint.strip()}*.jsonl") if hint and hint.strip() else TRANSCRIPT_PATTERNS
    found: dict[Path, float] = {}
    for pat in pats:
        for p in pdir.glob(pat):
            if p.is_file() and p.name not in REGISTRY_JSONL:
                found[p] = p.stat().st_mtime
    cands = [p for p, _ in sorted(found.items(), key=lambda kv: (-kv[1], kv[0].name))]
    if not cands:
        raise core.PfsError("Транскрипт сессии в корне проекта не найден"
                            + (f" по «{hint.strip()}»" if hint and hint.strip() else "")
                            + " — ждём *_session.json (OpenCode) или *.jsonl (Claude Code). "
                              "Укажите файл явно: pfs cost --session <файл>")
    if len(cands) > 1 and hint and hint.strip():
        raise core.PfsError("В корне проекта несколько транскриптов по «" + hint.strip() + "»: "
                            + ", ".join(p.name for p in cands) + " — уточните: pfs cost --session <файл>")
    return cands[0]
