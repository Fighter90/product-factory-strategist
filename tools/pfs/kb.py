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
    lang_en = card_id.endswith("-en")
    base = card_id[:-3] if lang_en else card_id
    for c in cards():
        if c.get("id") == base:
            if lang_en:
                f = core.KNOWLEDGE / "methods_en" / c["file"]
                if f.exists():
                    return f
                raise core.PfsError(f"EN-версия карты {base} не найдена (methods_en/{c['file']})")
            return core.KNOWLEDGE / "methods" / c["file"]
    raise core.PfsError(f"Карта {card_id} не найдена")


# Канонический перевод заголовков H2: EN-зеркало обязано повторять последовательность
# разделов RU-карты, используя переводы из этой таблицы (PRO-60).
HEADINGS_RU_EN = {
    "Brand Health Tracking (BHT)": "Brand Health Tracking (BHT)",
    "Альтернативы, когда классический A/B невозможен": "Alternatives when a classic A/B is impossible",
    "Аукционы (краткий раздел)": "Auctions (short section)",
    "Вопросы, которые могут изменить решение": "Questions that can change the decision",
    "Как делать": "How to do it",
    "Как формулировать инсайт": "How to formulate an insight",
    "Кабинетные исследования и бенчмарк (занятие 2)": "Desk research and benchmark (session 2)",
    "Карта «фаза → фреймворки»": "Map of phase → frameworks",
    "Когда применять": "When to apply",
    "Метрические семейства": "Metric families",
    "Маппинг на процесс агента": "Mapping to the agent workflow",
    "Подводные камни": "Pitfalls",
    "Приоритизация — быстрый выбор метода": "Prioritization — choosing a method fast",
    "Приоритизация характеристик": "Feature prioritization",
    "Процедура": "Procedure",
    "Процедура (агент)": "Procedure (agent)",
    "Процедура (как использовать при построении обязательства)": "Procedure (use when building a commitment)",
    "Процедура (сборка дашборда)": "Procedure (dashboard assembly)",
    "Процедура («золотые» шаги дизайна)": "Procedure (golden design steps)",
    "Связи": "Connections",
    "Связанные карты": "Related maps",
    "Сила доказательств: что дают N интервью": "Evidence strength: what N interviews give",
    "Синтетические респонденты и ИИ": "Synthetic respondents and AI",
    "Суть": "Core idea",
    "Суть — 9 блоков, порядок заполнения важен": "Core idea — 9 blocks, fill-in order matters",
    "Типичные ошибки": "Typical mistakes",
    "Циклы проверки гипотез": "Hypothesis testing loops",
    "Шаблон (таблица: блок → гипотеза → откуда → проверка)": "Template (table: block → hypothesis → source → check)",
    "Шаблон (чек-лист)": "Template (checklist)",
    "Шаблон / чек-лист": "Template / checklist",
    "Шаблон / чек-лист (карточка ML-гипотезы)": "Template / checklist (ML hypothesis card)",
    "Шаблон / чек-лист (карточка запроса)": "Template / checklist (request card)",
    "Шаблон / чек-лист (план эксперимента)": "Template / checklist (experiment plan)",
    "Шаблон / чек-лист фазовых ворот": "Template / checklist of phase gates",
    "Этика и согласие": "Ethics and consent",
    "ИИ и синтетические респонденты при анализе": "AI and synthetic respondents in analysis",
    "Рекрутинг респондентов": "Respondent recruiting",
}

LINT_RATIO = 0.8  # EN-объём не меньше 80% от RU (PRO-60)
REQUIRED_FM = ("id", "title", "lang", "stages", "tags", "related")


def body(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)


def sections(body_text: str) -> list[str]:
    return [line[3:].strip() for line in body_text.splitlines() if line.startswith("## ")]


def wikilinks(body_text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", body_text)


def _lint_file(fm: dict, body_text: str, lang: str, name: str, known_ids: set[str]) -> list[str]:
    """Проверки одной карты: frontmatter, теги, пустые разделы, [[ссылки]], имена файлов."""
    problems: list[str] = []
    cid = str(fm.get("id", "") or "")
    label = f"{name} (EN)" if lang == "en" else name
    if name.startswith("M-"):
        problems.append(f"{label}: префикс M- в имени файла")
    if lang == "en" and name.endswith("-en.md"):
        problems.append(f"{label}: суффикс -en в имени EN-файла")
    if not cid:
        problems.append(f"{label}: нет id во frontmatter")
    else:
        if not cid.startswith("M-"):
            problems.append(f"{label}: id должен начинаться с M- (сейчас: {cid})")
        if lang == "en" and cid.endswith("-en"):
            problems.append(f"{cid}: id EN-карты не должен иметь суффикс -en")
    for key in REQUIRED_FM:
        val = fm.get(key)
        if val is None or val == "" or val == []:
            problems.append(f"{cid or label}: нет обязательного поля {key}")
    if fm.get("lang") != lang:
        problems.append(f"{label}: lang должен быть {lang} (сейчас: {fm.get('lang')})")
    tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
    for tag in sorted({t for t in tags if tags.count(t) > 1}):
        problems.append(f"{cid or label}: дубликат тега «{tag}»")
    current, filled = None, False
    for line in body_text.splitlines():
        if line.startswith("## "):
            if current is not None and not filled:
                problems.append(f"{cid or label}: пустой раздел «{current}»")
            current, filled = line[3:].strip(), False
        elif line.strip() and current is not None:
            filled = True
    if current is not None and not filled:
        problems.append(f"{cid or label}: пустой раздел «{current}»")
    for link in sorted(set(wikilinks(body_text))):
        if link not in known_ids:
            problems.append(f"{cid or label}: битая [[ссылка]] {link}")
    rel = fm.get("related") if isinstance(fm.get("related"), list) else []
    for r in rel:
        if r not in known_ids:
            problems.append(f"{cid or label}: related → {r}: карты нет")
    return problems


def lint() -> list[str]:
    """PRO-60: целостность базы знаний. Пустой список — база зелёная."""
    ru_files = {p.name: p for p in sorted((core.KNOWLEDGE / "methods").glob("*.md"))}
    en_files = {p.name: p for p in sorted((core.KNOWLEDGE / "methods_en").glob("*.md"))}
    parsed: dict[tuple[str, str], tuple[dict, str]] = {}
    known_ids: set[str] = set()
    for lang, files in (("ru", ru_files), ("en", en_files)):
        for name, path in files.items():
            fm = frontmatter(path.read_text(encoding="utf-8"))
            parsed[(lang, name)] = (fm, body(_raw(path)))
            known_ids.add(str(fm.get("id", "?")))
    problems: list[str] = []
    for (lang, name), (fm, body_text) in parsed.items():
        problems += _lint_file(fm, body_text, lang, name, known_ids)
    ru_names, en_names = set(ru_files), set(en_files)
    for name in sorted(ru_names - en_names):
        cid = parsed[("ru", name)][0].get("id", name)
        problems.append(f"{cid}: нет EN-версии (methods_en/{name})")
    for name in sorted(en_names - ru_names):
        problems.append(f"{name} (EN): нет RU-оригинала")
    for name in sorted(ru_names & en_names):
        rfm, rbody_text = parsed[("ru", name)]
        efm, ebody_text = parsed[("en", name)]
        cid = str(rfm.get("id", "") or name)
        if rfm.get("id") and efm.get("id") and rfm.get("id") != efm.get("id"):
            problems.append(f"{name}: id не совпадают (RU {rfm.get('id')} / EN {efm.get('id')})")
        ru_len, en_len = len(rbody_text), len(ebody_text)
        if ru_len and en_len / ru_len < LINT_RATIO:
            problems.append(f"{name}: EN-объём {round(en_len * 100 / ru_len)}% от RU (< {int(LINT_RATIO * 100)}%)")
        ru_h, en_h = sections(rbody_text), sections(ebody_text)
        if len(ru_h) != len(en_h):
            problems.append(f"{cid}: разделы EN не соответствуют RU ({len(ru_h)} → {len(en_h)})")
        else:
            for rh, eh in zip(ru_h, en_h):
                if rh not in HEADINGS_RU_EN:
                    problems.append(f"{cid}: нет перевода заголовка RU «{rh}»")
                    break
                if HEADINGS_RU_EN[rh] != eh:
                    problems.append(f"{cid}: заголовок EN «{eh}» ≠ ожидаемому «{HEADINGS_RU_EN[rh]}»")
                    break
        if "RU-версия" in ebody_text:
            problems.append(f"{name} (EN): строка «RU-версия» в теле — убрать")
    return problems


def _raw(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


STAGE_TITLES_EN = {"intake": "Problem statement", "research": "Research", "options": "Options",
                   "strategy": "Strategy", "validation": "Validation plan", "after-decision": "After the decision"}


def build_index_en() -> tuple[str, list[str]]:
    """INDEX_EN.md: английская навигация по зеркалам methods_en + проверка битых связей."""
    cs = []
    for p in sorted((core.KNOWLEDGE / "methods_en").glob("*.md")):
        meta = frontmatter(p.read_text(encoding="utf-8"))
        meta["file"] = p.name
        cs.append(meta)
    ids = {c.get("id") for c in cs}
    problems = []
    for c in cs:
        rel = c.get("related", []) if isinstance(c.get("related"), list) else []
        for r in rel:
            if r not in ids:
                problems.append(f"{c.get('id')} → {r}: card missing")
        if not c.get("id"):
            problems.append(f"{c['file']}: no id in frontmatter")
    lines = ["# Method cards: English mirrors (methods_en)", "",
             "> Generated by `python3 -m tools.pfs kb index`. Mirrors knowledge/INDEX.md;",
             " card language is set by the `lang: en` field, ids match the RU originals.", ""]
    for st in ("intake", "research", "options", "strategy", "validation", "after-decision"):
        lines += [f"## {STAGE_TITLES_EN[st]} (`{st}`)", ""]
        for c in cs:
            if st in (c.get("stages") or []):
                tags = ", ".join(c.get("tags", [])[:5]) if isinstance(c.get("tags"), list) else ""
                lines.append(f"- [{c.get('title', c['file'])}](methods_en/{c['file']}) `{c.get('id')}` — {tags}")
        lines.append("")
    lines += ["## All cards by course", ""]
    for course in ("strategy", "pm", "ux", "skills", "synthesis"):
        group = [c for c in cs if c.get("course") == course]
        if group:
            lines.append(f"**{course}**: " + ", ".join(f"[{c.get('id')}](methods_en/{c['file']})" for c in group))
            lines.append("")
    if problems:
        lines += ["## Broken links", ""] + [f"- {p}" for p in problems]
    text = "\n".join(lines) + "\n"
    core.atomic_write(core.KNOWLEDGE / "INDEX_EN.md", text)
    return text, problems


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
