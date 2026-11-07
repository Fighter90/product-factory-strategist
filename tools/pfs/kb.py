"""База знаний: поиск BM25 по формулировке, навигация по связям карт, генерация INDEX.md."""
from __future__ import annotations

import math
import re
from pathlib import Path

from . import core

WORD = re.compile(r"[a-zа-яё0-9]+", re.IGNORECASE)
STOP = set("и в во не что он на я с со как а то все она так его но да ты к у же вы за бы по только ее мне было вот от "
           "меня еще нет о из ему теперь когда даже ну ли если уже или ни быть был него до вас нибудь опять уж вам ведь "
           "там потом себя ничего ей может они тут где есть надо ней для мы тебя их чем была сам чтоб без будто чего раз "
           "тоже себе под будет ж тогда кто этот того потому этого какой совсем ним здесь этом один почти мой тем чтобы "
           "нее были куда зачем всех никогда можно при об другой хоть после над больше тот через эти нас про всего них "
           "какая много разве три эту моя впрочем хорошо свою этой перед иногда лучше чуть том нельзя такой им более "
           "всегда конечно всю между the a an of to in is for on and or".split())


def stem(w: str) -> str:
    w = w.lower().replace("ё", "е")
    return w[:6] if len(w) > 6 else w  # грубый, но устойчивый стемминг для русского


def tokens(text: str) -> list[str]:
    return [stem(w) for w in WORD.findall(text) if w.lower() not in STOP and len(w) > 1]


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    meta: dict = {}
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.split("#")[0].strip() if not v.strip().startswith('"') else v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k.strip()] = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k.strip()] = v.strip('"\'')
    return meta


def _chunks(path: Path, base: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = frontmatter(text)
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    out, head, buf = [], meta.get("title", path.stem), []
    for line in body.splitlines():
        if line.startswith("## "):
            if buf:
                out.append({"path": str(path.relative_to(base)), "id": meta.get("id", path.stem), "section": head,
                            "text": "\n".join(buf)})
            head, buf = line[3:].strip(), []
        else:
            buf.append(line)
    if buf:
        out.append({"path": str(path.relative_to(base)), "id": meta.get("id", path.stem), "section": head, "text": "\n".join(buf)})
    for ch in out:
        ch["tags"] = " ".join(meta.get("tags", []) if isinstance(meta.get("tags"), list) else [])
    return out


def search(query: str, project: Path | None = None, k: int = 8) -> list[dict]:
    docs = []
    for p in sorted(core.KNOWLEDGE.rglob("*.md")):
        docs += _chunks(p, core.ROOT)
    if project:
        for p in sorted((project / "sources").glob("S*.md")) + sorted((project / "outputs").glob("*.md")):
            docs += _chunks(p, core.ROOT if core.ROOT in p.parents else project)
    if not docs:
        return []
    toks = [tokens(d["section"] + " " + d["tags"] + " " + d["text"]) for d in docs]
    n, avg = len(docs), sum(len(t) for t in toks) / len(docs)
    df: dict[str, int] = {}
    for t in toks:
        for w in set(t):
            df[w] = df.get(w, 0) + 1
    q = tokens(query)
    res = []
    for d, t in zip(docs, toks):
        tf: dict[str, int] = {}
        for w in t:
            tf[w] = tf.get(w, 0) + 1
        score = 0.0
        for w in q:
            if w not in tf:
                continue
            idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
            score += idf * tf[w] * 2.2 / (tf[w] + 1.2 * (0.25 + 0.75 * len(t) / avg))
        if score > 0:
            snippet = next((l.strip() for l in d["text"].splitlines()
                            if any(stem(w) in tokens(l) for w in query.split())), d["text"].strip()[:160])
            res.append({**{k2: d[k2] for k2 in ("path", "id", "section")}, "score": round(score, 2), "snippet": snippet[:200]})
    return sorted(res, key=lambda r: -r["score"])[:k]


def cards() -> list[dict]:
    out = []
    for p in sorted((core.KNOWLEDGE / "methods").glob("*.md")):
        meta = frontmatter(p.read_text(encoding="utf-8"))
        meta["file"] = p.name
        out.append(meta)
    return out


def build_index() -> tuple[str, list[str]]:
    """INDEX.md: навигация по шагам процесса + проверка битых связей."""
    cs = cards()
    ids = {c.get("id") for c in cs}
    problems = []
    for c in cs:
        rel = c.get("related", []) if isinstance(c.get("related"), list) else []
        for r in rel:
            if r not in ids:
                problems.append(f"{c.get('id')} → {r}: карты нет")
        if not c.get("id"):
            problems.append(f"{c['file']}: нет id во frontmatter")
    stages = ["intake", "research", "options", "strategy", "validation", "after-decision"]
    titles = {"intake": "Постановка задачи", "research": "Исследование", "options": "Варианты",
              "strategy": "Стратегия", "validation": "План проверки", "after-decision": "После решения"}
    lines = ["# Навигация по методическим картам", "",
             "> Сгенерировано `python3 -m tools.pfs kb index`. Поиск: `python3 -m tools.pfs kb search \"запрос\"`.", ""]
    for st in stages:
        lines += [f"## {titles[st]} (`{st}`)", ""]
        for c in cs:
            if st in (c.get("stages") or []):
                lines.append(f"- [{c.get('title', c['file'])}](methods/{c['file']}) `{c.get('id')}` — {', '.join(c.get('tags', [])[:5]) if isinstance(c.get('tags'), list) else ''}")
        lines.append("")
    lines += ["## Все карты по курсам", ""]
    for course in ("strategy", "pm", "ux", "skills", "synthesis"):
        group = [c for c in cs if c.get("course") == course]
        if group:
            lines.append(f"**{course}**: " + ", ".join(f"[{c.get('id')}](methods/{c['file']})" for c in group))
            lines.append("")
    if problems:
        lines += ["## Битые связи", ""] + [f"- {p}" for p in problems]
    text = "\n".join(lines) + "\n"
    core.atomic_write(core.KNOWLEDGE / "INDEX.md", text)
    return text, problems


def card_path(card_id: str) -> Path:
    base = card_id[:-3] if card_id.endswith("-en") else card_id
    for c in cards():
        if c.get("id") == base:
            if card_id.endswith("-en"):
                f = core.KNOWLEDGE / "methods_en" / (base + "-en.md")
                if f.exists():
                    return f
            return core.KNOWLEDGE / "methods" / c["file"]
    raise core.PfsError(f"Карта {card_id} не найдена")

# Обязательные карты по шагам процесса (агент читает их перед шагом; pfs step печатает список).
STAGE_CARDS = {
    "intake": ["M-brief-hypotheses", "M-customers", "M-jtbd", "M-product-context"],
    "sources": ["M-source-criticism", "M-research-types"],
    "research": ["M-research-types", "M-quant-methods", "M-ab-testing", "M-sql-for-pm", "M-ai-in-research"],
    "discovery": ["M-jtbd", "M-audience-research", "M-in-depth-interviews", "M-customers", "M-product-frameworks"],
    "situation": ["M-source-criticism", "M-external-environment", "M-competitors", "M-trends-scenarios"],
    "options": ["M-strategy-growth", "M-goals-drivers-bets", "M-risks", "M-cannibalization",
                "M-product-frameworks", "M-lean-canvas", "M-double-diamond"],
    "choice": ["M-decision-daci", "M-product-frameworks"],
    "strategy": ["M-usp", "M-product-communication", "M-monetization", "M-unit-economics",
                 "M-traction-model", "M-platforms-types-criteria"],
    "validation": ["M-ab-testing", "M-success-metrics", "M-product-metrics", "M-forecasting-product"],
    "review": ["M-six-pager", "M-source-criticism"],
    "decision": ["M-decision-daci", "M-model-validation"],
    "monitoring": ["M-decision-daci", "M-loyalty-metrics"],
}


def cards_for(stage: str) -> list[str]:
    return STAGE_CARDS.get(stage, [])
