"""Минимальный MCP-сервер (stdio, JSON-RPC 2.0, построчно) поверх pfs. Без внешних зависимостей.

Подключение: .mcp.json в корне (Claude Code, Cursor и др. подхватывают автоматически).
Запуск вручную: python3 -m tools.pfs.mcp_server
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

from . import cli, core, data, participate, project, sources
from .core import PfsError

SERVER = {"name": "pfs-strategist", "version": "0.1.0"}


def _tool(name, desc, props, required=()):
    return {"name": name, "description": desc,
            "inputSchema": {"type": "object", "properties": props, "required": list(required), "additionalProperties": False}}


S = {"type": "string"}
TOOLS = [
    _tool("pfs_status", "Состояние активного проекта: шаги, следующее действие, вопросы к руководителю, стоимость", {}),
    _tool("pfs_route", "Определить сценарий запроса, методические карты и модели по шагам", {"request": S, "override": S}),
    _tool("pfs_kb_search", "Поиск по базе методических знаний (BM25)", {"query": S, "with_project": {"type": "boolean"}}, ["query"]),
    _tool("pfs_source_add", "Зарегистрировать источник: URL или путь к файлу (pdf, docx, xlsx, csv, html, md)",
          {"target": S, "title": S, "origin": {"type": "string", "enum": ["public", "own", "interview", "synthetic"]}, "published": S}, ["target"]),
    _tool("pfs_claim_add", "Записать утверждение в реестр (факт требует источник)",
          {"text": S, "kind": {"type": "string", "enum": ["fact", "hypothesis", "forecast", "assumption", "inference"]},
           "source": S, "derived_from": S, "confidence": {"type": "string", "enum": ["high", "medium", "low"]}, "quote": S},
          ["text", "kind"]),
    _tool("pfs_claims", "Таблица активных утверждений", {"kind": S}),
    _tool("pfs_check", "Контроль качества документов и реестра", {}),
    _tool("pfs_impact", "Какие выводы, документы и решения затронет изменение C### или S###", {"id": S}, ["id"]),
    _tool("pfs_decisions_due", "Что решать сейчас: просрочки, пересмотры, устаревшие основания", {}),
    _tool("pfs_models_pick", "Какую модель использовать для задачи", {"task": S}, ["task"]),
    _tool("pfs_next", "Что решать сейчас: шаг, ожидания человека, обязательства, пересмотры, открытые вопросы", {}),
    _tool("pfs_source_refresh", "Перезагрузить web-источник S###: текст изменился — старый уходит в sources/raw/, запись обновляется",
          {"sid": S, "max_chars": {"type": "integer"}}, ["sid"]),
    _tool("pfs_data_funnel", "Воронка по таблице (csv/xlsx): уникальные пользователи на каждом шаге",
          {"file": S, "steps": S, "user": S, "date": S, "sheet": S}, ["file", "steps"]),
    _tool("pfs_data_stats", "Описательная статистика столбца (n, среднее, медиана, stdev, перцентили, ci95); с group — по группам",
          {"file": S, "col": S, "group": S, "sheet": S}, ["file", "col"]),
    _tool("pfs_interview_guide", "Каркас гайда интервью: interviews/synthetic/guide_<персона>.md",
          {"persona": S, "topic": S}, ["persona", "topic"]),
    _tool("pfs_interview_save", "Зарегистрировать транскрипт ИИ-респондента как источник (origin=synthetic, только гипотезы)",
          {"path": S, "persona": S, "title": S}, ["path", "persona"]),
    _tool("pfs_media_add", "Зарегистрировать медиа-файл: копия в sources/raw/, описание — текстовый источник kind=media",
          {"path": S, "description": S, "title": S, "origin": {"type": "string", "enum": ["own"]}}, ["path", "description"]),
    _tool("pfs_ux_scaffold", "Каркас UX-анализа по чек-листу эвристик: analysis/ux_<S###>.md",
          {"source_id": S, "focus": S}, ["source_id"]),
]


def _argv(name: str, a: dict) -> list[str]:
    if name == "pfs_status":
        return ["status"]
    if name == "pfs_route":
        return ["route"] + ([a["request"]] if a.get("request") else []) + (["--override", a["override"]] if a.get("override") else [])
    if name == "pfs_kb_search":
        return ["kb", "search", a["query"]] + (["--with-project"] if a.get("with_project") else [])
    if name == "pfs_source_add":
        argv = ["source", "add", a["target"], "--origin", a.get("origin", "public")]
        for k in ("title", "published"):
            if a.get(k):
                argv += [f"--{k}", a[k]]
        return argv
    if name == "pfs_claim_add":
        argv = ["claim", "add", a["text"], "--kind", a["kind"], "--confidence", a.get("confidence", "medium")]
        for k, flag in (("source", "--source"), ("derived_from", "--from"), ("quote", "--quote")):
            if a.get(k):
                argv += [flag, a[k]]
        return argv
    if name == "pfs_claims":
        return ["claim", "list"] + (["--kind", a["kind"]] if a.get("kind") else [])
    if name == "pfs_check":
        return ["check"]
    if name == "pfs_impact":
        return ["impact", a["id"]]
    if name == "pfs_decisions_due":
        return ["decision", "due"]
    if name == "pfs_models_pick":
        return ["models", "pick", a["task"]]
    raise KeyError(name)


# Инструменты без CLI-команды: вызывают модули напрямую; проект — активный, как у остальных.
DIRECT = {"pfs_next", "pfs_source_refresh", "pfs_data_funnel", "pfs_data_stats",
          "pfs_interview_guide", "pfs_interview_save", "pfs_media_add", "pfs_ux_scaffold"}


def _pdir() -> Path:
    return core.project_dir(None)


def _ok(structured: dict, text: str) -> dict:
    return {"content": [{"type": "text", "text": text}], "structuredContent": structured, "isError": False}


def _direct(name: str, a: dict) -> dict:
    if name == "pfs_next":
        text = project.next_text(_pdir())
        return _ok({"text": text}, text)
    if name == "pfs_source_refresh":
        res = sources.refresh(_pdir(), a["sid"], int(a.get("max_chars") or 4000))
        if res["changed"]:
            text = (f"{res['sid']}: обновлён, знаков {res['old_chars']}→{res['new_chars']}, "
                    f"sha {res['old_sha8']}→{res['new_sha8']}"
                    + (f"; ⚠ внедрённых фраз: {res['flags']}" if res["flags"] else ""))
        else:
            text = f"{res['sid']}: текст источника не изменился"
        return _ok(res, text)
    if name == "pfs_data_funnel":
        res = data.funnel(Path(a["file"]), a["steps"], a.get("user") or "user_id", a.get("date"), a.get("sheet"))
        text = data.funnel_text(res)
        return _ok({"text": text, "res": res}, text)
    if name == "pfs_data_stats":
        res = data.stats(Path(a["file"]), a["col"], a.get("group"), a.get("sheet"))
        text = data.stats_text(res)
        return _ok({"text": text}, text)
    if name == "pfs_interview_guide":
        path = participate.guide(_pdir(), a["persona"], a["topic"])
        return _ok({"path": str(path)}, f"Гайд: {path}")
    if name == "pfs_interview_save":
        rec = participate.save_synthetic(_pdir(), Path(a["path"]), a["persona"], a.get("title"))
        return _ok({"sid": rec["id"], "title": rec["title"]},
                   f"{rec['id']} добавлен: {rec['title']} ({rec['chars']} зн.) — синтетика даёт только гипотезы")
    if name == "pfs_media_add":
        rec = participate.media(_pdir(), Path(a["path"]), a["description"], a.get("title"), a.get("origin") or "own")
        return _ok({"sid": rec["id"], "kind": rec["kind"]},
                   f"{rec['id']} добавлен: медиа {rec['title']} ({rec['kind']})")
    if name == "pfs_ux_scaffold":
        path = participate.ux_scaffold(_pdir(), a["source_id"], a.get("focus") or "")
        return _ok({"path": str(path)}, f"Каркас UX-анализа: {path}")
    raise KeyError(name)


def call(name: str, arguments: dict) -> dict:
    if name in DIRECT:
        try:
            return _direct(name, arguments or {})
        except PfsError as exc:
            return {"content": [{"type": "text", "text": f"Ошибка: {exc}"}], "isError": True}
    buf, err = io.StringIO(), io.StringIO()
    old_err = sys.stderr
    sys.stderr = err
    try:
        with redirect_stdout(buf):
            code = cli.main(_argv(name, arguments or {}))
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.stderr = old_err
    text = (buf.getvalue() + err.getvalue()).strip() or "ok"
    return {"content": [{"type": "text", "text": text}], "isError": code != 0}


def handle(msg: dict) -> dict | None:
    mid, method = msg.get("id"), msg.get("method")
    if method == "initialize":
        ver = (msg.get("params") or {}).get("protocolVersion", "2025-06-18")
        result = {"protocolVersion": ver, "capabilities": {"tools": {}}, "serverInfo": SERVER}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        p = msg.get("params") or {}
        try:
            result = call(p.get("name", ""), p.get("arguments") or {})
        except KeyError:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"Unknown tool {p.get('name')}"}}
    elif method == "ping":
        result = {}
    elif mid is None:  # уведомления (notifications/initialized и т.п.) — без ответа
        return None
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            resp = handle(json.loads(line))
        except Exception as exc:  # не роняем сервер из-за одного запроса
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(exc)}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
