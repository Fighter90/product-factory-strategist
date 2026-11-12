"""Сборка итогового отчёта: документы + реестр утверждений + источники + решения + стоимость."""
from __future__ import annotations

import hashlib
import html as html_mod
import re
from pathlib import Path

from . import calc, check, claims as claims_mod, core, cost, decisions, i18n, sources as src_mod
from .xlsx import sheet_names

ORDER = ["00_brief.md", "01_research_plan.md", "02_situation.md", "03_options.md", "04_product_strategy.md",
         "05_comms_strategy.md", "06_validation_plan.md", "07_quality_review.md"]

STATE = ".export_state.json"


# ---------- свежесть экспорта: снимок реестра на момент сборки ----------

def _registry_snapshot(pdir: Path) -> dict:
    """Снимок реестра на момент экспорта: числа строк, sha256 содержимого реестров
    и mtimes расчётов (calcs.json и outputs/attachments/*.xlsx). Хеш ловит правки
    на месте (retract/rebase/supersede, source refresh), которые число строк не меняют."""
    calcs = pdir / "calcs.json"
    att_mtime = max((p.stat().st_mtime for p in (pdir / "outputs" / "attachments").glob("*.xlsx")),
                    default=None)
    return {"at": core.now(),
            "claims": len(core.read_jsonl(pdir / "claims.jsonl")),
            "sources": len(core.read_jsonl(pdir / "sources.jsonl")),
            "claims_sha": _file_sha(pdir / "claims.jsonl"),
            "sources_sha": _file_sha(pdir / "sources.jsonl"),
            "calcs_mtime": calcs.stat().st_mtime if calcs.exists() else None,
            "attachments_mtime": att_mtime}


def _file_sha(path: Path) -> str | None:
    """sha256 файла реестра или None, если файла нет."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def read_state(pdir: Path) -> dict | None:
    """Снимок из последнего экспорта или None, если экспорта ещё не было."""
    snap = core.read_json(pdir / "outputs" / STATE)
    return snap if isinstance(snap, dict) else None


def save_state(pdir: Path) -> dict:
    """Зафиксировать снимок реестра в outputs/.export_state.json (после успешной сборки)."""
    snap = _registry_snapshot(pdir)
    core.write_json(pdir / "outputs" / STATE, snap)
    return snap


def _excel_changed(pdir: Path, snap: dict) -> bool:
    """calcs.json или книги в outputs/attachments изменились после последнего экспорта."""
    calcs = pdir / "calcs.json"
    if (calcs.stat().st_mtime if calcs.exists() else None) != snap.get("calcs_mtime"):
        return True
    att_mtime = max((p.stat().st_mtime for p in (pdir / "outputs" / "attachments").glob("*.xlsx")),
                    default=None)
    return att_mtime != snap.get("attachments_mtime")


def freshness_warnings(pdir: Path) -> list[str]:
    """Предупреждение об устаревшем отчёте: реестр изменился после последнего экспорта
    (по числу строк ИЛИ по содержимому — отзыв/замещение/refresh пишут файл на месте).
    [] — снимка нет или с момента сборки ничего не поменялось."""
    snap = read_state(pdir)
    if not snap:
        return []
    parts = []
    d_claims = len(core.read_jsonl(pdir / "claims.jsonl")) - int(snap.get("claims") or 0)
    d_sources = len(core.read_jsonl(pdir / "sources.jsonl")) - int(snap.get("sources") or 0)
    if d_claims:
        parts.append(f"{d_claims:+d} claims")
    elif snap.get("claims_sha") and _file_sha(pdir / "claims.jsonl") != snap["claims_sha"]:
        parts.append("изменено содержимое claims.jsonl")
    if d_sources:
        parts.append(f"{d_sources:+d} sources")
    elif snap.get("sources_sha") and _file_sha(pdir / "sources.jsonl") != snap["sources_sha"]:
        parts.append("изменено содержимое sources.jsonl")
    if _excel_changed(pdir, snap):
        parts.append("Excel пересобран")
    if not parts:
        return []
    return ["⚠ Реестр изменился после последнего экспорта: " + ", ".join(parts)
            + " — приложения REPORT/SIX_PAGER устарели. Пересоберите: `pfs export`."]


def build(pdir: Path) -> Path:
    lang = i18n.lang_of(pdir)
    tr = lambda key, **kw: i18n.t(lang, key, **kw)
    meta = core.read_json(pdir / "project.json", {})
    parts = [tr("report_title", title=meta.get("title")), "",
             tr("report_built", ts=core.now()[:16]), ""]
    outs = pdir / "outputs"
    for name in ORDER + sorted(p.name for p in outs.glob("*.md") if p.name not in ORDER and p.name != "REPORT.md"):
        p = outs / name
        if p.exists():
            body = p.read_text(encoding="utf-8")
            note = tr("report_sixpager_note", spec=i18n.SIX_PAGER_SPEC[lang]) if p.name == "SIX_PAGER.md" else ""
            parts += [note + body.replace("\n# ", "\n## ") if not body.startswith("# ") else "#" + body, "", "---", ""]
    active = [c for c in claims_mod.load(pdir)]
    parts += [tr("appx_a_claims"), "", claims_mod.table(active), ""]
    parts += [tr("appx_b_sources"), "", tr("appx_sources_header"), "|---|---|---|---|---|"]
    for s in src_mod.load(pdir):
        parts.append(f"| {s['id']} | {s['title'].replace('|', '/')} | {s.get('url') or s.get('path') or '—'} | {s['origin']} | {s['retrieved'][:10]} |")
    decs = decisions.load(pdir)
    if decs:
        parts += ["", tr("appx_c_decisions"), "", decisions.table(decs)]
    qc = check.run(pdir)
    parts += ["", tr("appx_d_transparency"), "", "```", cost.summary_text(pdir, lang),
              check.report_text(qc, lang), "```"]
    att = attachments_table(pdir)
    if att:
        parts += ["", tr("appx_e_excel"), "", att]
    path = outs / "REPORT.md"
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", "Собран outputs/REPORT.md", tool="pfs export")
    return path


# ---------- six-pager (FAQ-1…FAQ-6) с Excel-приложениями ----------

ATTACHMENTS = [
    ("unit_economics.xlsx", "ARPU, VC, CAC, отток"),
    ("growth_model.xlsx", "MAU, рост, конверсия, AOV, take rate"),
    ("cohort_retention.xlsx", "размеры когорт, кривая удержания"),
    ("market_sizing.xlsx", "PAM, доли воронки, факторы среды"),
]


def attachments_table(pdir: Path) -> str | None:
    """Маркдаун-таблица ВСЕХ книг из outputs/attachments/*.xlsx или None, если пусто.
    Листы читаются из самих книг; для стандартных расчётов — подсказка, что править."""
    books = sorted((pdir / "outputs" / "attachments").glob("*.xlsx"))
    if not books:
        return None
    hints = dict(ATTACHMENTS)
    rows = []
    for p in books:
        try:
            sheets = " · ".join(sheet_names(p)) or "—"
        except Exception:
            sheets = "—"
        rows.append(f"| {p.name} | {sheets} | {hints.get(p.name, '—')} |")
    return "| Файл | Листы | Что редактировать |\n|---|---|---|\n" + "\n".join(rows)


def _split_sections(text: str) -> list[dict]:
    """Markdown → блоки по строкам-заголовкам ^#+ ({level, title, lines}); текст до первого
    заголовка — блок уровня 0. Вложенные секции — отдельные блоки, поэтому дерево
    собирается функцией _subtree, а не вложенностью lines."""
    blocks: list[dict] = [{"level": 0, "title": "", "lines": []}]
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            blocks.append({"level": len(m.group(1)), "title": m.group(2).strip(), "lines": []})
        else:
            blocks[-1]["lines"].append(line)
    return blocks


def _subtree(blocks: list[dict], i: int) -> list[int]:
    """Блок i и вложенные в него секции (глубже по уровню, до такой же/выше)."""
    out, lvl = [i], blocks[i]["level"]
    for j in range(i + 1, len(blocks)):
        if blocks[j]["level"] <= lvl:
            break
        out.append(j)
    return out


def _shift(level: int, delta: int) -> str:
    """Маркер заголовка уровня level, сдвинутого на delta (в пределах #…######)."""
    return "#" * max(1, min(level + delta, 6))


def _render_subtree(blocks: list[dict], i: int, delta: int) -> str:
    """Секция i вместе с вложенными; все заголовки поддерева сдвинуты на delta."""
    chunks = []
    for j in _subtree(blocks, i):
        b = blocks[j]
        body = "\n".join(b["lines"]).strip()
        head = f"{_shift(b['level'], delta)} {b['title']}" if b["level"] else ""
        chunks.append(f"{head}\n\n{body}" if head and body else (head or body))
    return "\n\n".join(chunks)


def _norm_title(s: str) -> str:
    """Нормализация заголовка/колонки: без «(…)», регистра и знаков — только слова/числа."""
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    return re.sub(r"[^a-zа-яё0-9+]+", " ", s).strip()


def _title_matches(title: str, name: str) -> bool:
    """Заголовок соответствует имени секции: точное совпадение нормализованных названий
    или токены имени — подпоследовательность токенов заголовка («Сегменты» ⊂
    «Сегменты (discovery)», «Чего не знаем» ⊂ «Чего мы не знаем»)."""
    t, n = _norm_title(title).split(), _norm_title(name).split()
    if not t or not n or len(n) > len(t):
        return False
    if t == n:
        return True
    it = iter(t)
    return all(tok in it for tok in n)


def _grab(pdir: Path, fname: str, sections: tuple[str, ...], cap: int = 6000,
          require_section: bool = False, reg: dict | None = None) -> str | None:
    """Именованные секции документа: заголовки уровня ≥ 2 (H1 документа не матчится),
    каждая секция атомарна и рендерится с «###» (вложенность сдвигается вместе с ней).
    cap уменьшает ЧИСЛО секций, но не режет текст внутри — маркеров «обрезано» нет.
    reg — реестр вставленного (fname → номера блоков) против дублей с _insert_doc.
    Совпадений нет — None; целые документы собирает _insert_doc."""
    path = pdir / "outputs" / fname
    if not path.exists():
        return None
    blocks = _split_sections(path.read_text(encoding="utf-8"))
    used = reg.setdefault(fname, set()) if reg is not None else set()
    chunks: list[str] = []
    for nm in sections:
        for i, b in enumerate(blocks):
            if i in used or b["level"] < 2 or not _title_matches(b["title"], nm):
                continue
            used.update(_subtree(blocks, i))
            chunks.append(_render_subtree(blocks, i, 3 - b["level"]))
            break
    if require_section and not chunks:
        return None
    out: list[str] = []
    total = 0
    for k, ch in enumerate(chunks):
        if k and cap and total + len(ch) + 2 > cap:
            break  # резать только по границам секций
        out.append(ch)
        total += len(ch) + 2
    return "\n\n".join(out) if out else None


def _insert_doc(pdir: Path, fname: str, demote: int = 2, reg: dict | None = None) -> str | None:
    """Целый документ для вставки в six-pager: заголовки понижены на demote уровней
    (# → ###, ## → ####, ### → #####), секции, уже попавшие в вывод через _grab или
    предыдущие вставки, не дублируются — вставляются только не вошедшие.
    Нет файла или нечего вставлять — None."""
    path = pdir / "outputs" / fname
    if not path.exists():
        return None
    blocks = _split_sections(path.read_text(encoding="utf-8"))
    used = reg.setdefault(fname, set()) if reg is not None else set()
    chunks: list[str] = []
    for i, b in enumerate(blocks):
        if i in used:
            continue
        used.add(i)
        body = "\n".join(b["lines"]).strip()
        if b["level"] == 0:
            if body:
                chunks.append(body)
        else:
            chunks.append(f"{_shift(b['level'], demote)} {b['title']}" + (f"\n\n{body}" if body else ""))
    return "\n\n".join(chunks) or None


def _flat(v) -> str:
    """Любое значение → компактная строка (строки как есть; dict → 'k: x'; None/пустое → '')."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, dict):
        return ", ".join(f"{k}: {x}" for k, x in v.items() if x not in (None, "", []))
    if isinstance(v, (list, tuple)):
        return ", ".join(_flat(x) for x in v if x not in (None, "", []))
    return str(v)


def _sources_footnotes(pdir: Path) -> str | None:
    """ПОЛНЫЙ нумерованный список источников: ID — название — URL/файл — дата публикации.
    Без ограничений и отсылок «ещё N — sources.jsonl»."""
    rows = core.read_jsonl(pdir / "sources.jsonl")
    if not rows:
        return None
    lines = []
    for i, r in enumerate(rows, 1):
        link = _flat(r.get("url")) or _flat(r.get("path"))
        pub = _flat(r.get("published"))[:10]
        line = f"{i}. **{r.get('id', f'S{i:03d}')}** — {_flat(r.get('title'))}"
        if link:
            line += f" — {link}"
        if pub:
            line += f" — {pub}"
        lines.append(line)
    return "\n".join(lines)


# ---------- i18n скелета six-pager (RU по умолчанию; EN — черновик, PRO-31) ----------
# Переводятся только фиксированные строки-скелет, которые генерирует инструмент.
# Содержимое документов 00–07 остаётся на языке автора — полный синхронный перевод
# по спецификации SIX_PAGER_PROMPT.md делает агент, не CLI (вне возможностей stdlib).

_EN: dict[str, str] = {
    "# {title}: six-pager": "# {title}: Six-pager (EN draft)",
    "> Собрано {ts} командой `pfs export --six-pager` по спецификации "
    "`knowledge/templates/SIX_PAGER_PROMPT.md` (формат референса стратегии роста: "
    "FAQ-1…6 с нумерованными подпунктами, матрицей тактик и KPI в двух плоскостях). "
    "Теги [C###]/[S###] — происхождение чисел; сноски-источники — в конце документа.":
        "> Assembled {ts} by `pfs export --six-pager` per the spec `knowledge/templates/"
        "SIX_PAGER_PROMPT.md` (growth-strategy reference format: FAQ-1…6 with numbered "
        "sub-items, a tactics matrix, KPI in two planes). Tags [C###]/[S###] mark where "
        "numbers come from; source footnotes are at the end. Skeleton only: sections sourced "
        "verbatim from documents 00–07 are marked [RU source — translate] for the translator.",
    "**Запрос:** {q}": "**Request:** {q}",
    "## FAQ-1. Анализ текущего состояния": "## FAQ-1. Current state analysis",
    "### 1.1 Обзор рынка: тренды, вызовы и возможности":
        "### 1.1 Market overview: trends, challenges and opportunities",
    "> Раздел появится после шага «situation» (02_situation.md): объём и динамика "
    "рынка диапазонами, ключевые тренды буллетами с жирными заголовками.":
        "> This section appears after the «situation» step (02_situation.md): market size "
        "and dynamics as ranges, key trends as bold bullets.",
    "### 1.2 Ключевые конкуренты и анализ их стратегий роста и промо-механик":
        "### 1.2 Key competitors: growth and promo mechanics",
    "Сравнительная таблица групп конкурентов (заполните после конкурентного анализа):":
        "Comparative table of competitor groups (fill in after competitive analysis):",
    "| | Группа 1 | Группа 2 | Группа 3 |": "| | Group 1 | Group 2 | Group 3 |",
    "| **Ключевые преимущества** | … | … | … |": "| **Key advantages** | … | … | … |",
    "| **Стратегия роста и промо-механики** | … | … | … |":
        "| **Growth and promo mechanics** | … | … | … |",
    "| **Риски для компании** | … — Высокий/Средний/Низкий | … | … |":
        "| **Risks for the company** | … — High/Medium/Low | … | … |",
    "> **Вывод (умозаключение):** окно возможностей и его срок — заполните по данным 1.1–1.2.":
        "> **Conclusion (inference):** the opportunity window and its horizon — fill from 1.1–1.2.",
    "## FAQ-2. User Persona. Кто является целевой аудиторией?":
        "## FAQ-2. User Persona. Who is the target audience?",
    "### 2.1 Сегменты": "### 2.1 Segments",
    "> Добавьте сегменты/персоны в 02_situation.md.": "> Add segments/personas to 02_situation.md.",
    "Таблица персон (заполните):": "Persona table (fill in):",
    "| | Сегмент 1 | Сегмент 2 | Сегмент 3 |": "| | Segment 1 | Segment 2 | Segment 3 |",
    "| **Кто они?** | … | … | … |": "| **Who are they?** | … | … | … |",
    "| **Что используют сегодня и почему?** | … | … | … |":
        "| **What do they use today and why?** | … | … | … |",
    "| **С какими трудностями сталкиваются?** | … | … | … |":
        "| **What difficulties do they face?** | … | … | … |",
    "| **Общие трудности** | … | … |": "| **Common difficulties** | … | … |",
    "### 2.2 Барьеры на каждом этапе пути": "### 2.2 Barriers at each journey stage",
    "| Этап пути | Барьер сегодня | Что делает продукт |":
        "| Journey stage | Barrier today | What the product does |",
    "| Привлечение | … | … |": "| Acquisition | … | … |",
    "| Выбор / использование | … | … |": "| Choice / usage | … | … |",
    "| Оплата | … | … |": "| Payment | … | … |",
    "| Постоплатный опыт | … | … |": "| Post-payment experience | … | … |",
    "Что сдерживает от старта или продления? (заполните по сегментам):":
        "What holds back signup or renewal? (fill in per segment):",
    "| Сегмент | Сдерживающий фактор | Чем снимается |":
        "| Segment | Blocking factor | How it is removed |",
    "| Сегмент 1 | … | … |": "| Segment 1 | … | … |",
    "> **Вывод (умозаключение):** сегментация по барьеру входа; лестница тиров "
    "обслуживает все барьеры; приоритизация — по ёмкости/CAC/конкуренции (расчёт — выше).":
        "> **Conclusion (inference):** segment by the entry barrier; the tier ladder serves "
        "all barriers; prioritize by capacity/CAC/competition (calculation above).",
    "## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.":
        "## FAQ-3. Strategic initiatives. Justify each one briefly.",
    "> Раздел появится после шага «options» (03_options.md).":
        "> This section appears after the «options» step (03_options.md).",
    "### Инициативы выбранного направления (драйверы)":
        "### Initiatives of the chosen direction (drivers)",
    "Сформулируйте 3–4 инициативы по схеме: «**Первый драйвер** — …», «**Второй драйвер** — …», "
    "далее «Ключевые направления» (буллеты) и пошаговый расчёт эффекта. Закройте "
    "выводом-умозаключением.":
        "Formulate 3–4 initiatives as: «**First driver** — …», «**Second driver** — …», then "
        "«Key directions» (bullets) and a step-by-step effect calculation. Close with an "
        "inference-conclusion.",
    "Юнит-экономика — расчёт пошагово:": "Unit economics — step-by-step:",
    "## FAQ-4. Тактики. Детализируйте каждую инициативу до конкретных тактик.":
        "## FAQ-4. Tactics. Detail each initiative into concrete tactics.",
    "> Добавьте тактики по каждой инициативе в 04_product_strategy.md.":
        "> Add tactics for each initiative to 04_product_strategy.md.",
    "Матрица тактик (из Outcome-роадмапа 04_product_strategy.md):":
        "Tactics matrix (from the outcome roadmap 04_product_strategy.md):",
    "Матрица тактик (заполните):": "Tactics matrix (fill in):",
    "| Инициатива 1 | … | … | … |": "| Initiative 1 | … | … | … |",
    "| Инициатива 2 | … | … | … |": "| Initiative 2 | … | … | … |",
    "## FAQ-5. Высокоуровневый план реализации": "## FAQ-5. High-level implementation plan",
    "> Раздел появится после шага «validation» (06_validation_plan.md).":
        "> This section appears after the «validation» step (06_validation_plan.md).",
    "Ожидаемое распределение вклада инициатив в общий результат (сумма 100%):":
        "Expected contribution of initiatives to the outcome (must sum to 100%):",
    "- __% — Инициатива 1;": "- __% — Initiative 1;",
    "- __% — Инициатива 2;": "- __% — Initiative 2;",
    "- __% — Инициатива 3.": "- __% — Initiative 3.",
    "Порядок тактик: высокий → средний → базовый приоритет. Тайминг — к сезонам рынка. "
    "Параллельные треки: комьюнити/партнёрства — вне основной линии.":
        "Tactic order: high → medium → base priority. Timing follows market seasons. Parallel "
        "tracks: community/partnerships — off the main line.",
    "## FAQ-6. Метрики успеха. KPI в двух плоскостях":
        "## FAQ-6. Success metrics. KPI in two planes",
    "> Добавьте метрики успеха в 04/06 документы — таблица KPI соберётся "
    "автоматически из сводных таблиц 06_validation_plan.md.":
        "> Add success metrics to the 04/06 documents — the KPI table is assembled "
        "automatically from the summary tables of 06_validation_plan.md.",
    "KPI в двух направлениях: **1) Бизнес** — деньги и база (выручка/MRR, платящие, "
    "конверсия в оплату, доля тарифов, фактический LTV/CAC); **2) Продукт** — активация, "
    "время до первой ценности, число действий до результата, churn, CSAT/NPS. "
    "У каждого KPI: база → цель к сроку → порог действия. Контр-метрики — по одной "
    "на удар red team.":
        "KPI in two planes: **1) Business** — money and base (revenue/MRR, paying users, "
        "payment conversion, plan mix, actual LTV/CAC); **2) Product** — activation, "
        "time to first value, actions to result, churn, CSAT/NPS. Each KPI: baseline → target "
        "by deadline → action threshold. Counter-metrics — one per red-team hit.",
    "## Источники (сноски)": "## Sources (footnotes)",
    "## Приложения (Excel)": "## Appendices (Excel)",
    "> Ещё нет: `pfs calc all`.": "> Not yet: `pfs calc all`.",
    "> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
    "Детализация по спецификации — knowledge/templates/SIX_PAGER_PROMPT.md. "
    "Полная версия с доказательствами — REPORT.md.":
        "> Formulas recalculate on open (Excel / Numbers / LibreOffice). Detailing per the "
        "spec: knowledge/templates/SIX_PAGER_PROMPT.md. Full evidence version — REPORT.md.",
    # юнит-экономика — все записи ниже живые: их читает _unit_econ_block (таблица формул
    # и чувствительность); записей-синонимов (ключ → тот же ключ) здесь нет.
    "Допущения: {note}": "Assumptions: {note}",
    "Допущения [укажите теги]: ARPU, переменные, CAC, churn — лист «Ввод» unit_economics.xlsx.":
        "Assumptions [add C-tags]: ARPU, variable costs, CAC, churn — the «Ввод» sheet of unit_economics.xlsx.",
    "| Формула | Расчёт | Результат |": "| Formula | Calculation | Result |",
    "CM = ARPU × (1 − доля переменных)": "CM = ARPU × (1 − variable share)",
    "Средняя жизнь платящего = 1 / churn": "Average paying lifetime = 1 / churn",
    "**{x} мес**": "**{x} mo**",
    "**{x}** (критерий ≥ 3)": "**{x}** (target ≥ 3)",
    "Окупаемость CAC = CAC / CM": "CAC payback = CAC / CM",
    "**Вывод (умозаключение):** LTV/CAC ≥ 3 держится до churn ≈ {churn} %/мес, "
    "до CAC ≈ €{cac}, до доли переменных расходов ≈ {vc} % "
    "(каждый порог — при прочих равных; сетка — лист «Чувствительность»).":
        "**Conclusion (inference):** LTV/CAC ≥ 3 holds up to churn ≈ {churn} %/mo, "
        "CAC ≈ €{cac}, variable-cost share ≈ {vc} % "
        "(each threshold — all else equal; grid — the «Чувствительность» sheet).",
    "**Вывод (умозаключение):** запас прочности модели — какой допуск выдерживает "
    "каждое допущение (см. лист «Чувствительность»).":
        "**Conclusion (inference):** safety margin — which deviation each assumption survives "
        "(see the «Чувствительность» sheet).",
    # решение
    "**Решение {did}** — {title}.": "**Decision {did}** — {title}.",
    " Обязательство: {commit}.": " Commitment: {commit}.",
    "промежуточный пересмотр {date}; триггер: {trig}": "interim review {date}; trigger: {trig}",
    "промежуточный пересмотр {date}": "interim review {date}",
    # матрица тактик и KPI
    "| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |":
        "| Strategic initiative | Focus | User needs and expectations | Decisions (tactics) |",
    " **Результат:** {gate}": " **Outcome:** {gate}",
    "| Плоскость | Гипотеза | Метрика | База → цель к сроку | Порог действия (остановить) |":
        "| Plane | Hypothesis | Metric | Baseline → target by deadline | Action threshold (stop) |",
    "Бизнес": "Business",
    "Продукт": "Product",
    "база — 06_validation_plan.md": "baseline — 06_validation_plan.md",
}


def _t(s: str, lang: str = "ru") -> str:
    """Строка скелета six-pager: RU как есть, EN — из словаря _EN (нет записи — RU как есть)."""
    return _EN.get(s, s) if lang == "en" else s


RU_SOURCE = "[RU source — translate]"


def _mark_ru(text: str | None, lang: str, fname: str) -> str | None:
    """EN-каркас: секция, вставленная из документа 00–07 дословно, помечается маркером
    «[RU source — translate]» (переводит агент, не CLI); RU-версия и заглушки-скелет
    без маркера. Маркер идёт строкой-цитатой ПЕРЕД контентом с именем файла-источника."""
    if lang != "en" or not text:
        return text
    return f"> {RU_SOURCE} {fname}\n\n{text}"


def _unit_econ_block(pdir: Path, lang: str = "ru") -> str | None:
    """Пошаговая юнит-экономика из calcs.json (unit_econ): CM, LTV, LTV/CAC, окупаемость."""
    cfg = core.read_json(pdir / "calcs.json", {}).get("unit_econ") or {}
    arpu, vc = cfg.get("arpu"), cfg.get("vc_share")
    cac, churn = cfg.get("cac"), cfg.get("churn_month")
    vals = (arpu, vc, cac, churn)
    if not all(isinstance(v, (int, float)) for v in vals) or not arpu or not churn or not cac:
        return None

    def n(x: float) -> str:
        return f"{x:.2f}".replace(".", ",")

    cm = arpu * (1 - vc)
    ltv = cm / churn
    ratio = ltv / cac
    payback = cac / cm
    life = 1 / churn
    rows = [
        (_t("CM = ARPU × (1 − доля переменных)", lang),
         f"{n(arpu)} × (1 − {n(vc)}) = {n(arpu)} × {n(1 - vc)}", f"**CM = {n(cm)}**"),
        (_t("Средняя жизнь платящего = 1 / churn", lang), f"1 / {n(churn)}",
         _t("**{x} мес**", lang).format(x=n(life))),
        (_t("LTV = CM / churn", lang), f"{n(cm)} / {n(churn)}", f"**LTV = {n(ltv)}**"),
        (_t("LTV/CAC", lang), f"{n(ltv)} / {n(cac)}", _t("**{x}** (критерий ≥ 3)", lang).format(x=n(ratio))),
        (_t("Окупаемость CAC = CAC / CM", lang), f"{n(cac)} / {n(cm)}",
         _t("**{x} мес**", lang).format(x=n(payback))),
    ]
    table = _t("| Формула | Расчёт | Результат |", lang) + "\n|---|---|---|\n" + \
        "\n".join(f"| {f} | {c} | {r} |" for f, c, r in rows)
    note = _flat(cfg.get("note"))
    head = (_t("Допущения: {note}", lang).format(note=note) if note else
            _t("Допущения [укажите теги]: ARPU, переменные, CAC, churn — лист «Ввод» unit_economics.xlsx.", lang))
    # Чувствительность к критерию LTV/CAC ≥ 3: порог по каждому допущению при прочих равных.
    if cm > 0 and ltv > 0:
        sens = _t("**Вывод (умозаключение):** LTV/CAC ≥ 3 держится до churn ≈ {churn} %/мес, "
                  "до CAC ≈ €{cac}, до доли переменных расходов ≈ {vc} % "
                  "(каждый порог — при прочих равных; сетка — лист «Чувствительность»).",
                  lang).format(churn=n(cm / (3 * cac) * 100), cac=n(ltv / 3),
                               vc=n((1 - 3 * cac / ltv) * 100))
    else:
        sens = _t("**Вывод (умозаключение):** запас прочности модели — какой допуск выдерживает "
                  "каждое допущение (см. лист «Чувствительность»).", lang)
    return f"{head}\n\n{table}\n\n{sens}"


def _decision_block(pdir: Path, lang: str = "ru") -> str | None:
    """Последнее зафиксированное решение D### — обязательство, срок, пересмотр."""
    rows = core.read_jsonl(pdir / "decisions.jsonl")
    if not rows:
        return None
    d = rows[-1]
    did = d.get("id", "D###")
    title = _flat(d.get("title"))
    commit = _flat(d.get("commitment"))
    rv = d.get("review")
    if isinstance(rv, dict):
        date = _flat(rv.get("date"))
        trig = _flat(rv.get("triggers") or rv.get("trigger"))
        review = _t("промежуточный пересмотр {date}; триггер: {trig}", lang).format(date=date, trig=trig) \
            if trig else _t("промежуточный пересмотр {date}", lang).format(date=date)
    else:
        review = _flat(rv)
    out = _t("**Решение {did}** — {title}.", lang).format(did=did, title=title)
    if commit:
        out += _t(" Обязательство: {commit}.", lang).format(commit=commit)
    if review:
        out += f" {review[0].upper() + review[1:]}."
    return out


def _table_rows(text: str, headers: tuple[str, ...]) -> list[list[str]]:
    """Строки markdown-таблицы, чья шапка содержит колонки headers подряд и по порядку.
    Разделитель |---| пропускается; строка с другим числом колонок заканчивает таблицу."""
    want = [_norm_title(h) for h in headers]
    rows: list[list[str]] = []
    header_seen, width = False, 0
    for ln in text.splitlines():
        if not ln.strip().startswith("|"):
            if header_seen and rows:
                break
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if not header_seen:
            norm = [_norm_title(c) for c in cells]
            for k in range(len(norm) - len(want) + 1):
                if norm[k:k + len(want)] == want:
                    header_seen, width = True, len(cells)
                    break
            continue
        if len(cells) != width:
            break
        rows.append(cells)
    return rows


_BUSINESS = ("выручк", "mrr", "платящ", "ltv", "cac", "оплат", "тариф", "arpu", "цен")


def _kpi_table(pdir: Path, lang: str = "ru") -> str | None:
    """Таблица KPI двух плоскостей (Бизнес/Продукт) из сводных таблиц 06_validation_plan.md:
    «Ожидаемое изменение» (гипотеза → метрика → цель), «С чем сравниваем» (база) и
    «Критерии решения» (порог остановки). Сводных таблиц нет — None (заглушка-структура)."""
    path = pdir / "outputs" / "06_validation_plan.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    rows = _table_rows(text, ("Гипотеза", "Метрика", "Ожидание к решению"))
    if not rows:
        return None
    thresholds = {r[0]: (r[3] if len(r) > 3 else "—")
                  for r in _table_rows(text, ("Проверка", "Продолжить", "Изменить", "Остановить"))}
    bases = {m.group(1): m.group(2) for m in re.finditer(r"^-\s*(H\d+)\s*:\s*(.+)$", text, flags=re.M)}

    def cell(s: str) -> str:
        return s.replace("|", "/")

    out = [_t("| Плоскость | Гипотеза | Метрика | База → цель к сроку | Порог действия (остановить) |", lang),
           "|---|---|---|---|---|"]
    for r in rows:
        if len(r) < 4:
            continue
        hid, hyp, metric, target = r[0], r[1], r[2], r[3]
        base = bases.get(hid, _t("база — 06_validation_plan.md", lang)).split(";")[0].strip()
        if re.fullmatch(r"H\d+", hid.strip()):
            hyp = f"{hid.strip()} — {hyp}"
        plane = _t("Бизнес", lang) if any(w in f"{metric} {hyp}".lower() for w in _BUSINESS) else _t("Продукт", lang)
        out.append(f"| {plane} | {cell(hyp)} | {cell(metric)} | {cell(base)} → {cell(target)} | "
                   f"{cell(thresholds.get(hid, '—'))} |")
    return "\n".join(out)


_INITIATIVE = re.compile(r"^-\s*\*\*(.+?):\*\*\s*(.+)$")


def _tactics_matrix(pdir: Path, lang: str = "ru") -> str | None:
    """Матрица тактик из Outcome-роадмапа 04_product_strategy.md: буллеты вида
    «- **Этап N (…):** тактики … **Результат …:** …» раскладываются в канонические
    колонки «Инициатива | Фокус | Потребности | Решения (тактики)». Похоже на роадмап
    меньше двух этапов — None (честная заглушка)."""
    path = pdir / "outputs" / "04_product_strategy.md"
    if not path.exists():
        return None
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _INITIATIVE.match(line.strip())
        if not m:
            continue
        label, body = m.group(1).strip(), m.group(2).strip()
        if not _norm_title(label).startswith(("этап", "инициатив", "драйвер")):
            continue
        parts = re.split(r"\*\*Результат[^*]*\*\*:?\s*", body, maxsplit=1)
        gate = parts[1].strip() if len(parts) > 1 else ""
        rows.append((label, parts[0].strip(), gate))
    if len(rows) < 2:
        return None

    def cell(s: str) -> str:
        return s.replace("|", "/")

    out = [_t("| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |", lang),
           "|---|---|---|---|"]
    for label, tactics, gate in rows:
        focus = re.split(r"[.;]", tactics)[0].strip() or "—"
        solutions = tactics + (_t(" **Результат:** {gate}", lang).format(gate=gate) if gate else "")
        out.append(f"| {cell(label)} | {cell(focus)} | — | {cell(solutions)} |")
    return "\n".join(out)


def build_six_pager(pdir: Path, with_calcs: bool = True, lang: str = "ru") -> Path:
    """Six-pager в структуре референса стратегии роста: FAQ-1…FAQ-6 с нумерованными
    подпунктами (1.1/1.2 обзор рынка и конкуренты; 2.1/2.2 персоны и барьеры по этапам),
    юнит-экономикой с чувствительностью, матрицей тактик и KPI в двух плоскостях
    (бизнес/продукт). Документы 03/04/06 вставляются целиком с понижением заголовков
    на 2 уровня; секции, уже попавшие в вывод через _grab, повторно не вставляются;
    резка — только по границам секций. Сноски-источники — полный список sources.jsonl.
    lang="en" — EN-черновик: скелет инструмента на английском (_EN), содержимое
    документов 00–07 вставляется дословно с пометкой «[RU source — translate]»
    (переводит агент, не CLI) → outputs/SIX_PAGER_EN.md.
    Спецификация детализации: knowledge/templates/SIX_PAGER_PROMPT.md."""
    if with_calcs:
        calc.run(pdir, "all")
    meta = core.read_json(pdir / "project.json", {})
    parts = [_t("# {title}: six-pager", lang).format(title=meta.get("title")), "",
             _t("> Собрано {ts} командой `pfs export --six-pager` по спецификации "
                "`knowledge/templates/SIX_PAGER_PROMPT.md` (формат референса стратегии роста: "
                "FAQ-1…6 с нумерованными подпунктами, матрицей тактик и KPI в двух плоскостях). "
                "Теги [C###]/[S###] — происхождение чисел; сноски-источники — в конце документа.",
                lang).format(ts=core.now()[:16]), "",
             _t("**Запрос:** {q}", lang).format(q=meta.get("question", "")), ""]
    reg: dict[str, set[int]] = {}  # вставленные секции (fname → номера блоков) — против дублей

    def grab(fname: str, sections: tuple[str, ...], cap: int = 6000, require_section: bool = False):
        return _grab(pdir, fname, sections, cap, require_section, reg)

    faq1 = _mark_ru(grab("02_situation.md", ("Короткий ответ", "Что известно", "Рынок", "Тренды",
                                             "Противоречия", "Чего не знаем"), 8000), lang, "02_situation.md")
    parts += [_t("## FAQ-1. Анализ текущего состояния", lang), "",
              _t("### 1.1 Обзор рынка: тренды, вызовы и возможности", lang), "",
              faq1 or _t("> Раздел появится после шага «situation» (02_situation.md): объём и динамика "
                         "рынка диапазонами, ключевые тренды буллетами с жирными заголовками.", lang), "",
              _t("### 1.2 Ключевые конкуренты и анализ их стратегий роста и промо-механик", lang), "",
              _mark_ru(grab("02_situation.md", ("Конкуренты", "Конкурентный анализ"), 3000, True),
                       lang, "02_situation.md")
              or _t("Сравнительная таблица групп конкурентов (заполните после конкурентного анализа):", lang), "",
              _t("| | Группа 1 | Группа 2 | Группа 3 |", lang),
              "|---|---|---|---|",
              _t("| **Ключевые преимущества** | … | … | … |", lang),
              _t("| **Стратегия роста и промо-механики** | … | … | … |", lang),
              _t("| **Риски для компании** | … — Высокий/Средний/Низкий | … | … |", lang), "",
              _t("> **Вывод (умозаключение):** окно возможностей и его срок — заполните по данным 1.1–1.2.", lang), ""]
    faq2 = grab("02_situation.md", ("Сегменты", "Персоны", "Аудитория"), 3000)
    faq2_src = "02_situation.md"
    if not faq2 or len(faq2) < 120:
        faq2 = grab("04_product_strategy.md", ("Аудитория",), 3000)
        faq2_src = "04_product_strategy.md"
    faq2 = _mark_ru(faq2, lang, faq2_src)
    parts += [_t("## FAQ-2. User Persona. Кто является целевой аудиторией?", lang), "",
              _t("### 2.1 Сегменты", lang), "",
              faq2 or _t("> Добавьте сегменты/персоны в 02_situation.md.", lang), "",
              _t("Таблица персон (заполните):", lang), "",
              _t("| | Сегмент 1 | Сегмент 2 | Сегмент 3 |", lang),
              "|---|---|---|---|",
              _t("| **Кто они?** | … | … | … |", lang),
              _t("| **Что используют сегодня и почему?** | … | … | … |", lang),
              _t("| **С какими трудностями сталкиваются?** | … | … | … |", lang),
              _t("| **Общие трудности** | … | … |", lang), "",
              _t("### 2.2 Барьеры на каждом этапе пути", lang), "",
              _t("| Этап пути | Барьер сегодня | Что делает продукт |", lang),
              "|---|---|---|",
              _t("| Привлечение | … | … |", lang),
              _t("| Выбор / использование | … | … |", lang),
              _t("| Оплата | … | … |", lang),
              _t("| Постоплатный опыт | … | … |", lang), "",
              _t("Что сдерживает от старта или продления? (заполните по сегментам):", lang), "",
              _t("| Сегмент | Сдерживающий фактор | Чем снимается |", lang),
              "|---|---|---|",
              _t("| Сегмент 1 | … | … |", lang), "",
              _t("> **Вывод (умозаключение):** сегментация по барьеру входа; лестница тиров "
                 "обслуживает все барьеры; приоритизация — по ёмкости/CAC/конкуренции (расчёт — выше).", lang), ""]
    doc03 = _mark_ru(_insert_doc(pdir, "03_options.md", reg=reg), lang, "03_options.md")
    parts += [_t("## FAQ-3. Стратегические инициативы. Кратко обоснуйте каждую.", lang), "",
              doc03 or _t("> Раздел появится после шага «options» (03_options.md).", lang), "",
              _t("### Инициативы выбранного направления (драйверы)", lang), "",
              _t("Сформулируйте 3–4 инициативы по схеме: «**Первый драйвер** — …», «**Второй драйвер** — …», "
                 "далее «Ключевые направления» (буллеты) и пошаговый расчёт эффекта. Закройте "
                 "выводом-умозаключением.", lang), ""]
    ue = _unit_econ_block(pdir, lang)
    if ue:
        parts += [_t("Юнит-экономика — расчёт пошагово:", lang), "", ue, ""]
    doc04 = _mark_ru(_insert_doc(pdir, "04_product_strategy.md", reg=reg), lang, "04_product_strategy.md")
    matrix = _tactics_matrix(pdir, lang)
    parts += [_t("## FAQ-4. Тактики. Детализируйте каждую инициативу до конкретных тактик.", lang), "",
              doc04 or _t("> Добавьте тактики по каждой инициативе в 04_product_strategy.md.", lang), ""]
    if matrix:
        parts += [_t("Матрица тактик (из Outcome-роадмапа 04_product_strategy.md):", lang), "", matrix, ""]
    else:
        parts += [_t("Матрица тактик (заполните):", lang), "",
                  _t("| Стратегическая инициатива | Фокус | Потребности и ожидания пользователя | Решения (тактики) |", lang),
                  "|---|---|---|---|",
                  _t("| Инициатива 1 | … | … | … |", lang),
                  _t("| Инициатива 2 | … | … | … |", lang), ""]
    doc06 = _mark_ru(_insert_doc(pdir, "06_validation_plan.md", reg=reg), lang, "06_validation_plan.md")
    parts += [_t("## FAQ-5. Высокоуровневый план реализации", lang), "",
              doc06 or _t("> Раздел появится после шага «validation» (06_validation_plan.md).", lang), "",
              _t("Ожидаемое распределение вклада инициатив в общий результат (сумма 100%):", lang), "",
              _t("- __% — Инициатива 1;", lang),
              _t("- __% — Инициатива 2;", lang),
              _t("- __% — Инициатива 3.", lang), "",
              _t("Порядок тактик: высокий → средний → базовый приоритет. Тайминг — к сезонам рынка. "
                 "Параллельные треки: комьюнити/партнёрства — вне основной линии.", lang), ""]
    dec = _decision_block(pdir, lang)
    if dec:
        parts += [dec, ""]
    faq6 = grab("04_product_strategy.md", ("Метрики", "Показатели"), 3000)
    faq6_src = "04_product_strategy.md"
    if not faq6:
        faq6 = grab("06_validation_plan.md", ("Ожидаемое изменение", "Критерии решения"), 3000)
        faq6_src = "06_validation_plan.md"
    faq6 = _mark_ru(faq6, lang, faq6_src)
    kpi = _kpi_table(pdir, lang)
    parts += [_t("## FAQ-6. Метрики успеха. KPI в двух плоскостях", lang), ""]
    if faq6:
        parts += [faq6, ""]
    if kpi:
        parts += [kpi, ""]
    elif not faq6 and doc04 is None and doc06 is None:
        parts += [_t("> Добавьте метрики успеха в 04/06 документы — таблица KPI соберётся "
                     "автоматически из сводных таблиц 06_validation_plan.md.", lang), ""]
    parts += [_t("KPI в двух направлениях: **1) Бизнес** — деньги и база (выручка/MRR, платящие, "
                 "конверсия в оплату, доля тарифов, фактический LTV/CAC); **2) Продукт** — активация, "
                 "время до первой ценности, число действий до результата, churn, CSAT/NPS. "
                 "У каждого KPI: база → цель к сроку → порог действия. Контр-метрики — по одной "
                 "на удар red team.", lang), ""]
    src = _sources_footnotes(pdir)
    if src:
        parts += [_t("## Источники (сноски)", lang), "", src, ""]
    parts += [_t("## Приложения (Excel)", lang), "",
              attachments_table(pdir) or _t("> Ещё нет: `pfs calc all`.", lang), "",
              "", _t("> Формулы пересчитываются при открытии (Excel / Numbers / LibreOffice). "
                     "Детализация по спецификации — knowledge/templates/SIX_PAGER_PROMPT.md. "
                     "Полная версия с доказательствами — REPORT.md.", lang)]
    path = pdir / "outputs" / ("SIX_PAGER_EN.md" if lang == "en" else "SIX_PAGER.md")
    core.atomic_write(path, "\n".join(parts) + "\n")
    core.log(pdir, "action", f"Собран outputs/{path.name} (формат референса)", tool="pfs export --six-pager")
    return path


_MAX_POINTS = 6   # тезисов на слайд
_POINT_CAP = 160  # символов на тезис



_DECK_CSS = """
  :root { --bg: #070b13; --fg: #e8eef8; --a1: #4fd1c5; --a2: #8b7bff; --dim: #9aa7bd; }
  * { box-sizing: border-box; }
  html { scroll-snap-type: y mandatory; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  section.slide { width: 100vw; height: auto; aspect-ratio: 16/9; min-height: 100vh;
                  max-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always;
                  display: flex; flex-direction: column; justify-content: center; gap: .6em;
                  padding: clamp(24px, 6vw, 80px); overflow: hidden;
                  border-bottom: 1px solid rgba(139, 123, 255, .18); }
  h1, h2 { margin: 0; line-height: 1.15; font-weight: 700;
           background: linear-gradient(90deg, var(--a1), var(--a2));
           -webkit-background-clip: text; background-clip: text; color: transparent; }
  h1 { font-size: clamp(28px, 5vw, 56px); }
  h2 { font-size: clamp(22px, 3.6vw, 40px); }
  ul { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: .45em;
       font-size: clamp(15px, 2vw, 24px); }
  li::marker { color: var(--a1); }
  p { margin: 0; font-size: clamp(15px, 2vw, 24px); color: var(--fg); }
  .query { color: var(--dim); font-size: clamp(16px, 2.2vw, 26px); }
  .query b { color: var(--a1); }
"""





def _slide(title: str, points: list[str], cls: str = "") -> str:
    """Секция-слайд: заголовок + один тезис — один пункт."""
    body = ""
    if points:
        items = "".join(f"<li>{html_mod.escape(p)}</li>" for p in points)
        body = f"<ul>{items}</ul>"
    k = f' class="{cls}"' if cls else ""
    return f'<section class="slide"{k}>\n<h2>{html_mod.escape(title)}</h2>\n{body}\n</section>'


_DECK_CSS = """
  :root { --bg: #070b13; --fg: #e8eef8; --a1: #4fd1c5; --a2: #8b7bff; --dim: #9aa7bd; }
  * { box-sizing: border-box; }
  html { scroll-snap-type: y mandatory; }
  body { margin: 0; background: var(--bg); color: var(--fg);
         font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  section.slide { width: 100vw; height: auto; aspect-ratio: 16/9; min-height: 100vh;
                  max-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always;
                  display: flex; flex-direction: column; justify-content: center; gap: .6em;
                  padding: clamp(24px, 6vw, 80px); overflow: hidden;
                  border-bottom: 1px solid rgba(139, 123, 255, .18); }
  h1, h2 { margin: 0; line-height: 1.15; font-weight: 700;
           background: linear-gradient(90deg, var(--a1), var(--a2));
           -webkit-background-clip: text; background-clip: text; color: transparent; }
  h1 { font-size: clamp(28px, 5vw, 56px); }
  h2 { font-size: clamp(22px, 3.6vw, 40px); }
  ul { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: .45em;
       font-size: clamp(15px, 2vw, 24px); }
  li::marker { color: var(--a1); }
  p { margin: 0; font-size: clamp(15px, 2vw, 24px); color: var(--fg); }
  .query { color: var(--dim); font-size: clamp(16px, 2.2vw, 26px); }
  .query b { color: var(--a1); }
"""


def _points(body: str) -> list[str]:
    """Тезисы слайда: маркеры списков и первые предложения абзацев (≤6, ≤160 символов)."""
    pts: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or set(line) <= set("-|: "):
            continue
        if line.startswith("|"):  # строка таблицы — первый столбец
            line = [c.strip() for c in line.strip("|").split("|")][0]
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^>\s?", "", line)
        sentence = re.split(r"(?<=[.!?…])\s+", line)[0]
        if len(sentence) > _POINT_CAP:
            sentence = sentence[:_POINT_CAP - 1].rstrip() + "…"
        if sentence and (not pts or sentence != pts[-1]):
            pts.append(sentence)
        if len(pts) >= _MAX_POINTS:
            break
    return pts



def build_deck(pdir: Path) -> Path:
    """HTML-дека 16:9 из outputs/SIX_PAGER.md (тёмная тема, один тезис на слайд)."""
    src = pdir / "outputs" / "SIX_PAGER.md"
    if not src.exists():
        raise core.PfsError("Сначала соберите six-pager: pfs export --six-pager")
    text = src.read_text(encoding="utf-8")
    meta = core.read_json(pdir / "project.json", {})
    q = re.search(r"^\*\*Запрос:\*\*\s*(.+)$", text, flags=re.M)
    query = q.group(1).strip() if q else meta.get("question", "")
    h1 = re.search(r"^#\s+(.+)$", text, flags=re.M)
    title = h1.group(1).strip() if h1 else meta.get("title", "Six-pager")
    sections = re.split(r"^##\s+", text, flags=re.M)[1:]
    slides = ['<section class="slide title-slide">\n'
              f"<h1>{html_mod.escape(title)}</h1>\n"
              f'<p class="query"><b>Запрос:</b> {html_mod.escape(query)}</p>\n</section>']
    for sec in sections:
        head, _, body = sec.partition("\n")
        head = head.strip()
        if head:
            slides.append(_slide(head, _points(body)))
    doc = ("<!doctype html>\n<html lang=\"ru\">\n<head>\n<meta charset=\"utf-8\">\n"
           f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
           f"<title>{html_mod.escape(title)}</title>\n<style>{_DECK_CSS}</style>\n"
           f"</head>\n<body>\n" + "\n".join(slides) + "\n</body>\n</html>\n")
    path = pdir / "outputs" / "presentations" / "deck.html"
    core.atomic_write(path, doc)
    core.log(pdir, "action", "Собран outputs/presentations/deck.html", tool="pfs export --deck")
    return path
