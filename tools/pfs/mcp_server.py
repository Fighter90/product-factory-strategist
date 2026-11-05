"""Минимальный MCP-сервер (stdio, JSON-RPC 2.0, построчно) поверх pfs. Без внешних зависимостей.

Подключение: .mcp.json в корне (Claude Code, Cursor и др. подхватывают автоматически).
Запуск вручную: python3 -m tools.pfs.mcp_server
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout

from . import cli

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


def call(name: str, arguments: dict) -> dict:
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
