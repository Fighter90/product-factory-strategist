"""Учёт стоимости: токены из транскриптов Claude Code + ручные записи (поиск, время человека)."""
from __future__ import annotations

import json
from pathlib import Path

from . import core

# Подписочные провайдеры: оплата планом, а не за токен — записываем токены с ценой $0 и пометкой «plan».
PLAN_PROVIDERS = {"zai-coding-plan"}


def pricing() -> dict:
    return core.read_json(core.CONFIG / "pricing.json", {"models": {}, "usd_rub": 95.0})


def _price_for(model: str, p: dict) -> dict:
    models = p.get("models", {})
    if model in models:
        return models[model]
    for key, val in models.items():  # claude-opus-5-5-xxxx → claude-opus-5-5
        if model.startswith(key):
            return val
    return models.get(p.get("fallback_model", ""), {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0})


def _ms_to_iso(ms) -> str | None:
    if not ms:
        return None
    from datetime import datetime, timezone
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def _parse_opencode_messages(messages: list) -> dict:
    """Итог info.tokens отсутствует (частичный экспорт) — складываем tokens из assistant-сообщений,
    модель и провайдер берём из message.model."""
    per: dict[str, dict] = {}
    for m in messages:
        if not isinstance(m, dict) or m.get("type") != "assistant" or not isinstance(m.get("tokens"), dict):
            continue
        t = m["tokens"]
        mdl = m.get("model") if isinstance(m.get("model"), dict) else {}
        c = t.get("cache") or {}
        row = per.setdefault(mdl.get("id") or "unknown",
                             {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "messages": 0})
        row["input"] += t.get("input", 0) or 0
        row["output"] += (t.get("output", 0) or 0) + (t.get("reasoning", 0) or 0)  # reasoning как output
        row["cache_write"] += c.get("write", 0) or 0
        row["cache_read"] += c.get("read", 0) or 0
        row["messages"] += 1
        if mdl.get("providerID") in PLAN_PROVIDERS:
            row["plan"] = 1
    return per


def _parse_opencode(data: dict, since: str | None = None, until: str | None = None) -> dict:
    """OpenCode session.json: авторитетный итог — info.tokens (агрегат сессии, OpenCode обновляет его
    по ходу работы), модель из info.model; tokens в assistant-сообщениях не суммируются с итогом.
    Если итога нет — расчёт по tokens из assistant-сообщений."""
    info = data.get("info") or {}
    tokens = info.get("tokens") or {}
    cache = tokens.get("cache") or {}
    model = info.get("model") or {}
    start = _ms_to_iso((info.get("time") or {}).get("created"))
    end = _ms_to_iso((info.get("time") or {}).get("updated")) or start
    if (since and end and end < since) or (until and start and start > until):
        return {}  # сессия целиком вне окна задачи
    if not (tokens.get("input") or tokens.get("output") or tokens.get("reasoning")
            or cache.get("read") or cache.get("write")):
        return _parse_opencode_messages(data.get("messages", []))
    per = {model.get("id") or "unknown": {
        "input": tokens.get("input", 0) or 0,
        "output": (tokens.get("output", 0) or 0) + (tokens.get("reasoning", 0) or 0),  # reasoning тарифицируется как output
        "cache_write": cache.get("write", 0) or 0,
        "cache_read": cache.get("read", 0) or 0,
        "messages": sum(1 for m in data.get("messages", []) if isinstance(m, dict) and m.get("type") == "assistant")}}
    if model.get("providerID") in PLAN_PROVIDERS:
        next(iter(per.values()))["plan"] = 1  # подписка: цена $0, пометка «plan»
    return per


def parse_transcript(path: Path, since: str | None = None, until: str | None = None) -> dict:
    """Суммирует usage по моделям. Форматы: Claude Code jsonl (message.usage) и OpenCode session.json
    (единый JSON-объект info.tokens). Одно сообщение может занимать несколько строк — считаем по message.id один раз."""
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        whole = json.loads(text)
    except json.JSONDecodeError:
        whole = None
    if isinstance(whole, dict) and isinstance(whole.get("info"), dict) and isinstance(whole.get("messages"), list):
        return _parse_opencode(whole, since, until)
    seen: set[str] = set()
    per_model: dict[str, dict] = {}
    files = [text]
    sub = path.with_suffix("") / "subagents"  # транскрипты субагентов лежат рядом
    if sub.is_dir():
        files += [f.read_text(encoding="utf-8", errors="replace") for f in sorted(sub.glob("*.jsonl"))]
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
            m = per_model.setdefault(msg.get("model", "unknown"),
                                     {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "messages": 0})
            m["input"] += u.get("input_tokens", 0) or 0
            m["output"] += u.get("output_tokens", 0) or 0
            m["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0
            m["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
            m["messages"] += 1
    return per_model


def price(per_model: dict) -> float:
    p = pricing()
    usd = 0.0
    for model, t in per_model.items():
        if t.get("plan"):
            continue  # подписка: цена $0
        pr = _price_for(model, p)
        usd += sum(t[k] * pr.get(k, 0) for k in ("input", "output", "cache_write", "cache_read")) / 1_000_000
    return usd


def _utc(iso: str) -> str:
    from datetime import datetime, timezone
    return datetime.fromisoformat(iso).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def record_session(pdir: Path, session_id: str, transcript: Path, since: str | None = None,
                   until: str | None = None) -> dict:
    """Идемпотентно: повторный вызов перезаписывает запись сессии, а не суммирует её дважды.

    Один чат может охватывать несколько задач, поэтому по умолчанию учитываются только сообщения
    после создания проекта (since = project.json → created).
    """
    meta = core.read_json(pdir / "project.json", {})
    window = meta.get("cost_window", {})
    if not since:
        since = window.get("since") or (_utc(meta["created"]) if meta.get("created") else None)
    until = until or window.get("until")
    per_model = parse_transcript(transcript, since, until)
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    prev = data["sessions"].get(session_id)
    if prev and prev.get("models") == per_model and prev.get("since") == since and prev.get("until") == until:
        return prev  # ничего не изменилось — файл не трогаем (нет лишних изменений в git)
    data["sessions"][session_id] = {"models": per_model, "usd": round(price(per_model), 4), "updated": core.now(),
                                    "stage": core.read_json(pdir / "state.json", {}).get("stage"), "since": since, "until": until}
    core.write_json(pdir / "costs.json", data)
    return data["sessions"][session_id]


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


def add_manual(pdir: Path, what: str, usd: float = 0.0, human_minutes: float = 0.0) -> None:
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    data["manual"].append({"ts": core.now(), "what": what, "usd": usd, "human_minutes": human_minutes})
    core.write_json(pdir / "costs.json", data)
    core.log(pdir, "cost", f"{what}: ${usd:.2f}, человек {human_minutes:.0f} мин")


def summary(pdir: Path) -> dict:
    data = core.read_json(pdir / "costs.json", {"sessions": {}, "manual": []})
    usd = sum(s["usd"] for s in data["sessions"].values()) + sum(m.get("usd", 0) for m in data["manual"])
    tokens = sum(sum(v for k, v in t.items() if k not in ("messages", "plan"))
                 for s in data["sessions"].values() for t in s["models"].values())
    by_model: dict[str, float] = {}
    p = pricing()
    for s in data["sessions"].values():
        for model, t in s["models"].items():
            if t.get("plan"):
                by_model[f"{model} (plan)"] = 0.0
                continue
            pr = _price_for(model, p)
            by_model[model] = by_model.get(model, 0) + sum(t[k] * pr.get(k, 0) for k in ("input", "output", "cache_write", "cache_read")) / 1e6
    human = sum(m.get("human_minutes", 0) for m in data["manual"])
    return {"usd": usd, "rub": usd * p.get("usd_rub", 95.0), "tokens": tokens, "sessions": len(data["sessions"]),
            "by_model": by_model, "human_minutes": human}


def summary_text(pdir: Path) -> str:
    s = summary(pdir)
    out = [f"Итого: ${s['usd']:.2f} (~{s['rub']:.0f} ₽) | сессий {s['sessions']} | токенов {s['tokens']:,} | время человека {s['human_minutes']:.0f} мин".replace(",", " ")]
    for m, v in sorted(s["by_model"].items(), key=lambda x: -x[1]):
        out.append(f"  {m:<24} ${v:.2f}")
    return "\n".join(out)
