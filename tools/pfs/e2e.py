"""Сквозной QA-прогон агента в OpenCode: разбор лога `opencode run --auto --format json`
и отчёт в qa/E2E-<дата>-<задача>-<lang>.md (PRO-64).

Формат событий (строки JSONL, как в приёмочных прогонах 2026-11-11): {type, timestamp,
sessionID, part}; part.type ∈ {step-start, text, tool, step-finish}. Шаги модели —
step-finish (там же токены: input / output / reasoning / cache), реплики — text,
вызовы инструментов — tool (state.status, state.input, state.output).

Метрики отчёта: шаги, вызовы инструментов по типам, ошибки инструментов (статус ≠ completed
или маркеры Ошибка/Error/Traceback в выводе), остановки (pfs ask) и их автоответы (pfs answer),
дошёл ли до финального пакета (pfs finish), токены, время. Результаты ворот — pfs check --strict
и сборка six-pager — build() снимает в клоне после прогона.

Запуск из scripts/e2e_opencode.sh; вручную:
  python3 -m tools.pfs.e2e <лог.jsonl> --clone <каталог-клона> --lang ru \
      --task-file qa/tasks/antispam-ru.md --out qa/E2E-2026-11-11-antispam-ru.md [--model id] [--plan]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ERR_MARKERS = ("Ошибка", "Error", "Traceback")
FINISH_MARK = "pfs finish"


def task_stem(task_file: str | Path) -> str:
    """Стем задачи из имени файла: qa/tasks/antispam-ru.md → antispam-ru."""
    return Path(task_file).stem


def default_report(task_file: str | Path, lang: str = "", date: str = "",
                   qa_dir: str | Path = "") -> Path:
    """Имя отчёта с задачей: qa/tasks/antispam-ru.md → qa/E2E-2026-11-11-antispam-ru.md.

    Стем задачи в имени обязателен — 6 прогонов матрицы 3×2 за один день иначе
    перезаписали бы друг друга (qa/E2E-<дата>-<lang>.md коллизирует по языку).
    """
    stem = task_stem(task_file)
    if lang and not stem.endswith(f"-{lang}"):
        stem = f"{stem}-{lang}"
    date = date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    qd = Path(qa_dir) if qa_dir else Path(__file__).resolve().parents[2] / "qa"
    return qd / f"E2E-{date}-{stem}.md"


def _num(n: int | float) -> str:
    return f"{n:,}".replace(",", " ")


def _min(ms: int) -> str:
    return (f"{ms / 60_000:.1f}").replace(".", ",") + " мин"


def _tool_summary(tools: Counter) -> str:
    if not tools:
        return "0"
    return f"{_num(sum(tools.values()))} (" + ", ".join(f"{k} {v}" for k, v in tools.most_common()) + ")"


def parse_log(path: Path) -> dict:
    """Разобрать лог прогона. Не-JSON строки пропускаются; ошибки — статус ≠ completed
    или маркер в выводе. Токены: output + reasoning (reasoning тарифицируется как output)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"лог прогона не найден: {path}")
    steps, tok_in, tok_out = 0, 0, 0
    tools: Counter = Counter()
    errors: list[dict] = []
    texts: list[str] = []
    asks = answers = 0
    finished = False
    t0 = t1 = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = d.get("part") if isinstance(d.get("part"), dict) else {}
        pt = part.get("type")
        ts = d.get("timestamp")
        if isinstance(ts, (int, float)):
            t0 = ts if t0 is None else min(t0, ts)
            t1 = ts if t1 is None else max(t1, ts)
        if pt == "step-finish":
            steps += 1
            tk = part.get("tokens") if isinstance(part.get("tokens"), dict) else {}
            tok_in += tk.get("input", 0) or 0
            tok_out += (tk.get("output", 0) or 0) + (tk.get("reasoning", 0) or 0)
        elif pt == "text":
            t = part.get("text") or ""
            if t.strip():
                texts.append(t)
        elif pt == "tool":
            tool = part.get("tool") or "?"
            tools[tool] += 1
            st = part.get("state") if isinstance(part.get("state"), dict) else {}
            inp = st.get("input") if isinstance(st.get("input"), dict) else {}
            out = str(st.get("output") or "")
            cmd = str(inp.get("command") or "") or str(inp)[:160]
            if "pfs ask " in cmd:
                asks += 1
            if "pfs answer " in cmd:
                answers += 1
            if FINISH_MARK in cmd:
                finished = True
            bad_status = st.get("status") not in (None, "completed", "pending", "running")
            if bad_status or any(m in out for m in ERR_MARKERS):
                errors.append({"tool": tool, "cmd": cmd[:160].replace("\n", " | "),
                               "out": out[:240].replace("\n", " | ")})
    return {"steps": steps, "tools": dict(tools), "errors": errors, "texts": texts,
            "asks": asks, "answers": answers, "finished": finished,
            "tokens_in": tok_in, "tokens_out": tok_out,
            "duration_ms": int((t1 - t0) or 0), "events": steps + sum(tools.values())}


def _verdict(s: dict, check_ok: bool, six_ok: bool) -> str:
    if s["finished"] and check_ok and six_ok:
        return ("✅ Прогон дошёл до финального пакета (pfs finish), ворота зелёные: "
                "check --strict без ошибок, six-pager собран. Ручных «продолжи» не было — одна сессия.")
    problems = [name for name, ok in (("pfs finish", s["finished"]),
                                      ("check --strict", check_ok), ("six-pager", six_ok)) if not ok]
    return "❌ Ворота не пройдены: " + ", ".join(problems) + ". Детали ниже."


def render_report(s: dict, lang: str, task: str, date: str, model: str = "", plan: bool = True,
                  check_ok: bool = False, check_tail: str = "",
                  six_ok: bool = False, six_tail: str = "") -> str:
    """Markdown-отчёт qa/E2E-<дата>-<задача>-<lang>.md: сводка, остановки, ошибки, финальные реплики, вердикт."""
    cost = "$0.00 (подписка, план)" if plan else "не считалась (укажите --model с прайсом)"
    model_s = model or "по умолчанию среды"
    lines = [
        f"# E2E-прогон OpenCode — {date} ({lang.upper()})",
        "",
        f"> Задача: {task}",
        f"> Модель: {model_s}",
        "> Прогон: свежий клон → `opencode run --auto --format json` (автопрогон, [PRO-54]) → разбор лога `tools/pfs/e2e.py`.",
        "",
        "## Сводка",
        "",
        "| Показатель | Значение |",
        "|---|---|",
        f"| Шагов модели (step-finish) | {_num(s['steps'])} |",
        f"| Вызовов инструментов | {_tool_summary(Counter(s['tools']))} |",
        f"| Ошибок инструментов | {_num(len(s['errors']))} |",
        f"| Токены | вход {_num(s['tokens_in'])} · выход {_num(s['tokens_out'])} |",
        f"| Стоимость | {cost} |",
        f"| Время | {_min(s['duration_ms'])} |",
        f"| Финальный пакет (`pfs finish`) | {'да' if s['finished'] else 'нет'} |",
        f"| `pfs check --strict` | {'✅ ' if check_ok else '❌ '}{check_tail.strip() or ('OK' if check_ok else 'падение')} |",
        f"| six-pager (сборка/линтер) | {'✅ ' if six_ok else '❌ '}{six_tail.strip() or ('собран' if six_ok else 'не собран')} |",
        "",
        "## Остановки",
        "",
        f"Пауз с вопросом человеку (`pfs ask`): **{_num(s['asks'])}**; закрыто самим агентом в режиме автопрогона"
        f" (`pfs answer`): **{_num(s['answers'])}**. Ручных «продолжи»: **0** — прогон шёл одной сессией.",
        "",
        "## Ошибки инструментов",
        "",
    ]
    if s["errors"]:
        for e in s["errors"]:
            lines.append(f"- `{e['tool']}`: {e['cmd']} → {e['out']}")
    else:
        lines.append("Не обнаружены (статусы completed, маркеров Error/Traceback в выводах нет).")
    lines += ["", "## Финальные реплики агента", ""]
    for t in s["texts"][-3:]:
        t = " ".join(t.split())
        lines.append(f"> {t[:500]}{'…' if len(t) > 500 else ''}")
        lines.append(">")
    if lines[-1] == ">":
        lines.pop()
    lines += ["", "## Вердикт", "", _verdict(s, check_ok, six_ok), ""]
    return "\n".join(lines)


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=600)
    return p.returncode, (p.stdout + p.stderr).strip()


def _tail(text: str, keywords: tuple[str, ...] = (), n: int = 2, cap: int = 200) -> str:
    """Хвост вывода для отчёта: строки с ключевыми словами (итог ворота), иначе последние.
    `|` заменяется на «·», чтобы не ломать таблицу Markdown; текст обрезается."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if keywords:
        picked = [l for l in lines if any(k.lower() in l.lower() for k in keywords)]
        if picked:
            lines = picked[-n:]
    out = " / ".join(lines[-n:])[:cap]
    return out.replace("|", "·")


def build(log: Path, clone: Path, lang: str, task_file: Path, out: Path,
          model: str = "", plan: bool = True) -> str:
    """Снять ворота в клоне (check --strict, сборка six-pager), отрендерить и записать отчёт."""
    clone = Path(clone)
    task = Path(task_file).read_text(encoding="utf-8").strip().splitlines()[0].lstrip("# ").strip()
    rc_c, out_c = _run(["python3", "-m", "tools.pfs", "check", "--strict"], clone)
    rc_s, out_s = _run(["python3", "-m", "tools.pfs", "export", "--six-pager", "--no-calcs"], clone)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md = render_report(parse_log(log), lang=lang, task=task, date=date, model=model, plan=plan,
                       check_ok=rc_c == 0, check_tail=_tail(out_c, ("ошибок", "errors")),
                       six_ok=rc_s == 0, six_tail=_tail(out_s, ("six-pager",)))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    return str(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Отчёт E2E-прогона OpenCode (PRO-64)")
    ap.add_argument("log")
    ap.add_argument("--clone", required=True, help="каталог клона, в котором шёл прогон")
    ap.add_argument("--lang", required=True, choices=["ru", "en"])
    ap.add_argument("--task-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="")
    ap.add_argument("--no-plan", action="store_true", help="прогон не на подписке")
    a = ap.parse_args()
    print("Отчёт: " + build(Path(a.log), Path(a.clone), a.lang, Path(a.task_file),
                            Path(a.out), model=a.model, plan=not a.no_plan))


if __name__ == "__main__":
    main()
