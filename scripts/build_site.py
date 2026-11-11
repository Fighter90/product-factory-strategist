#!/usr/bin/env python3
"""Генератор лендинга strategyproduct.ru — PRO-66 (дизайн v3 «тёплый тёмный»).

Статическая генерация `/` (RU) и `/en/` (EN): полный текст в HTML, hreflang,
OG-картинки по языкам, числа — из репозитория (карты знаний, навыки, субагенты,
хуки, автотесты, демо-проект `projects/демо`). JS — только цели Метрики,
копирование команд и аналитика аккордеона; без JS видны все тексты и числа.

Только стандартная библиотека. Счётчик Метрики в репозиторий не пишется:
подключается флагом `--ym-id` (см. site/ANALYTICS.md).

Скоуп PRO-66: эта система генерирует `/` (RU) и `/en/` (EN). Страницы site/demo.html,
site/help.html и site/materials.html остаются в прежней вёрстке — их перевод в новую
систему вынесен в отдельную задачу; тёмные фото, относящиеся к ним (обложка demo
на основе dark-hero-paper), подключаются вместе с конвертацией. Сейчас dark-hero-paper
используется как OG-картинка site/assets/og/og.jpg, dark-double-diamond и dossier-dark —
в разделах «Процесс» и финальном CTA лендинга.

Запуск: python3 scripts/build_site.py [--out site] [--ym-id 12345678]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "site"
DEMO = ROOT / "projects" / "демо"
BASE = "https://strategyproduct.ru"

CLAIM_ID = "C011"


class BuildError(Exception):
    """Недостающие или испорченные данные репозитория — сборка падает громко."""


def _read(path: Path) -> str:
    if not path.exists():
        raise BuildError(f"Нет файла: {path}")
    return path.read_text(encoding="utf-8")


def _jsonl(path: Path) -> list[dict]:
    rows = []
    for i, line in enumerate(_read(path).splitlines(), 1):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise BuildError(f"{path}: строка {i} не JSON: {e}") from e
    return rows


# ---------------- данные репозитория ----------------

def repo_numbers() -> dict:
    return {
        "N_MAPS": len(list((ROOT / "knowledge" / "methods").glob("*.md"))),
        "N_MAPS_EN": len(list((ROOT / "knowledge" / "methods_en").glob("*.md"))),
        "N_SKILLS": len(list((ROOT / ".claude" / "skills").glob("*/SKILL.md"))),
        "N_AGENTS": len(list((ROOT / ".claude" / "agents").glob("*.md"))),
        "N_HOOKS": len(list((ROOT / ".claude" / "hooks").glob("*.py"))),
        "N_TESTS": sum(
            len(re.findall(r"\bdef test_", p.read_text(encoding="utf-8")))
            for p in (ROOT / "tests").glob("test_*.py")
        ),
    }


def _require(m: "re.Match | None", what: str, where: Path) -> str:
    if not m:
        raise BuildError(f"Не найдено: {what} в {where}")
    return m.group(1)


def demo_numbers() -> dict:
    claims = _jsonl(DEMO / "claims.jsonl")
    kinds: dict[str, int] = {}
    for c in claims:
        kinds[c.get("kind", "?")] = kinds.get(c.get("kind", "?"), 0) + 1
    if not claims:
        raise BuildError("Реестр утверждений демо-проекта пуст")

    options_path = DEMO / "outputs" / "03_options.md"
    options_md = _read(options_path)
    heads = list(re.finditer(r"^## Вариант ([A-ZА-Я])\.", options_md, flags=re.M))
    if not heads:
        raise BuildError(f"В {options_path} нет заголовков «## Вариант X.»")
    letters = [m.group(1) for m in heads]

    # Red team считается по секциям вариантов: у каждого варианта должна быть строка
    # «Возражения red team» с нумерованными пунктами и строка «Скрытое допущение».
    # Отсутствие или испорченный формат — BuildError, а не тихий ноль.
    objections = 0
    assumptions = 0
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(options_md)
        sec = options_md[head.end():end]
        red = _require(re.search(r"^(- Возражения red team:.*$)", sec, flags=re.M),
                       "строка «Возражения red team»", options_path)
        nums = [int(x) for x in re.findall(r"\((\d+)\)", red)]
        if not nums:
            raise BuildError(
                f"В «Возражения red team» варианта {head.group(1)} нет нумерованных пунктов «(N)»")
        objections += max(nums)
        _require(re.search(r"^(- Скрытое допущени[ея])", sec, flags=re.M),
                 "строка «Скрытое допущение»", options_path)
        assumptions += 1

    d001 = next((d for d in _jsonl(DEMO / "decisions.jsonl") if d.get("id") == "D001"), None)
    if not d001:
        raise BuildError("В decisions.jsonl нет D001")
    letter_m = re.search(r"вариант ([A-ZА-Я])\b", d001.get("decision", ""))
    if not letter_m:
        raise BuildError("В решении D001 не найден выбранный вариант («вариант B …»)")
    letter = letter_m.group(1)
    if letter not in letters:
        raise BuildError(f"Выбранный вариант {letter} отсутствует среди вариантов {letters}")
    heading = _require(
        re.search(rf"^## Вариант {letter}\. (.+)$", options_md, flags=re.M),
        f"заголовок варианта {letter}", options_path)
    label = heading.split(" — ")[0].split(" (")[0].strip()
    review = d001.get("review", {}).get("date", "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", review):
        raise BuildError(f"У D001 нет даты пересмотра в формате YYYY-MM-DD: {review!r}")

    return {
        "D_SOURCES": len(list((DEMO / "sources").glob("S*.md"))),
        "D_CLAIMS": len(claims),
        "D_FACTS": kinds.get("fact", 0),
        "D_OPT_LAST": letters[-1],
        "D_OBJ": objections,
        "D_ASM": assumptions,
        "D_LETTER": letter,
        "D_LABEL": label,
        "REVIEW_RU": f"{review[8:]}.{review[5:7]}.{review[2:4]}",
        "REVIEW_EN": review,
    }


def claim_facts() -> dict:
    claims = _jsonl(DEMO / "claims.jsonl")
    claim = next((c for c in claims if c.get("id") == CLAIM_ID), None)
    if not claim:
        raise BuildError(f"В claims.jsonl нет {CLAIM_ID}")
    sources = claim.get("sources") or []
    if not sources:
        raise BuildError(f"У {CLAIM_ID} нет источника — нечего показывать как «цепочку доказательств»")
    sid = sources[0]
    src = next((s for s in _jsonl(DEMO / "sources.jsonl") if s.get("id") == sid), None)
    if not src:
        raise BuildError(f"Источник {sid} не найден в sources.jsonl")
    url = src.get("url") or ""
    dom = re.sub(r"^https?://(www\.)?", "", url).split("/")[0] if url else (src.get("path") or sid)
    retrieved = (src.get("retrieved") or "")[:10]

    kind = claim.get("kind", "")
    kind_ru = {"fact": "факт", "hypothesis": "гипотеза", "forecast": "прогноз",
               "assumption": "допущение", "inference": "вывод"}.get(kind)
    kind_en = {"fact": "fact", "hypothesis": "hypothesis", "forecast": "forecast",
               "assumption": "assumption", "inference": "inference"}.get(kind)
    if not kind_ru:
        raise BuildError(f"У {CLAIM_ID} неизвестный тип утверждения: {kind!r}")
    grade = claim.get("grade") or ""
    if not re.match(r"^[A-D]$", grade):
        raise BuildError(f"У {CLAIM_ID} нет силы доказательства A–D: {grade!r}")

    usage_ru = _sixpager_usage(DEMO / "outputs" / "SIX_PAGER.md")
    usage_en = _sixpager_usage(DEMO / "outputs" / "SIX_PAGER_EN.md")
    text = claim.get("text") or ""
    if not text:
        raise BuildError(f"У {CLAIM_ID} пустой текст")

    # Перевод утверждения для EN-страницы (в реестре только RU-текст) сверяется по числам:
    # если утверждение в реестре изменилось, а перевод — нет, сборка падает громко,
    # а не показывает на сайте расходящиеся числа.
    text_en = ("Global online recruitment market: $37.97B in 2025 with a 7.1% CAGR to 2033; "
               "Indeed — 60+ countries, 28 languages, 685M profiles; "
               "Bayt (MENA) — 59M+ profiles")
    if _num_tokens(text) != _num_tokens(text_en):
        raise BuildError(
            f"Числа перевода {CLAIM_ID} (TEXT_EN) расходятся с реестром: "
            f"{_num_tokens(text)} != {_num_tokens(text_en)} — обновите перевод в scripts/build_site.py")

    return {
        "C_ID": claim["id"],
        "C_SRC": sid,
        "C_DOM": dom,
        "DATE_RU": ".".join(reversed(retrieved.split("-"))) if retrieved else "",
        "DATE_EN": retrieved,
        "KIND_RU": kind_ru,
        "KIND_EN": kind_en,
        "GRADE": grade,
        "TEXT": text,
        "SEG_RU": text.split(";")[0].strip(),
        "TEXT_EN": text_en,
        "SEG_EN": text_en.split(";")[0].strip(),
        "USAGE_RU": usage_ru,
        "USAGE_EN": usage_en,
    }


def _num_tokens(s: str) -> list[str]:
    """Числовые токены текста в нормализованном виде: «37,97 млрд» → 37.97, «685M» → 685."""
    return sorted(t.replace(",", ".") for t in re.findall(r"\d[\d,.]*", s))


def _sixpager_usage(path: Path) -> str:
    """«FAQ-N · Раздел» — ближайший заголовок над строкой с упоминанием CLAIM_ID."""
    label = ""
    for line in _read(path).splitlines():
        m = re.match(r"^## (FAQ-\d+)[.:]?\s*(.*)$", line)
        if m:
            title = re.split(r"[.:]", m.group(2), maxsplit=1)[0].strip()
            label = f"{m.group(1)} · {title}" if title else m.group(1)
        if CLAIM_ID in line and label:
            return label
    raise BuildError(f"{CLAIM_ID} не найден под заголовком FAQ в {path}")


def excel_numbers() -> dict:
    md = _read(DEMO / "outputs" / "03_options.md")
    price = _require(re.search(r"paid \$([\d]+)/мес", md), "цена Pro", DEMO / "outputs" / "03_options.md")
    cm = _require(re.search(r"CM \$([\d,]+)", md), "вклад на покрытие", DEMO / "outputs" / "03_options.md")
    ltv = _require(re.search(r"LTV ≈ \$([\d,]+)", md), "LTV", DEMO / "outputs" / "03_options.md")
    ratio = _require(re.search(r"LTV/CAC ≈ ([\d,]+)", md), "LTV/CAC", DEMO / "outputs" / "03_options.md")
    return {"XL_PRICE": price, "XL_CM": cm, "XL_LTV": ltv, "XL_RATIO": ratio}


# ---------------- шаблоны ----------------

ARROW = ('<span class="arr"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
BRAND_SVG = ('<svg viewBox="0 0 40 40" fill="none" aria-hidden="true">'
             '<rect x="6.5" y="11.5" width="20" height="23" rx="4" stroke="#D6D2CC" stroke-width="1.6"/>'
             '<rect x="13.5" y="5.5" width="20" height="23" rx="4" fill="#0B0A09" stroke="#D6D2CC" stroke-width="1.6"/>'
             '<path d="M18 12.5h11M18 16.5h11M18 20.5h6" stroke="#D6D2CC" stroke-width="1.6" stroke-linecap="round"/>'
             '<circle cx="29" cy="24" r="3" fill="#EE8A3C"/></svg>')

CSS = """
/* Тёплый тёмный v3: тёплые нейтрали, один янтарный акцент, капсулы, тонкие линии */
:root{
  --bg:#0B0A09; --bg2:#12100E; --card:#151311; --line:rgba(214,210,204,.10); --line2:rgba(214,210,204,.18);
  --text:#D6D2CC; --strong:#F1EEE9; --muted:#8C877F; --accent:#EE8A3C; --accent-ink:#1A0E05; --pill:#BDB9B3;
  --font:Inter,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1160px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.eyebrow{font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.label{font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
h1,h2,h3{color:var(--strong);font-weight:500;text-wrap:balance;margin:0}
h1{font-size:clamp(40px,6.4vw,76px);line-height:1.05;letter-spacing:-.02em}
h2{font-size:clamp(28px,3.4vw,40px);line-height:1.1;letter-spacing:-.01em}
h3{font-size:20px;line-height:1.3}
.acc{color:var(--accent);font-weight:400}
.muted{color:var(--muted)}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:99;background:var(--strong);color:var(--bg);padding:8px 12px;border-radius:8px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:10px}

/* шапка-капсула */
.nav{position:fixed;top:calc(14px + env(safe-area-inset-top,0px));left:0;right:0;z-index:50}
.nav .bar{display:flex;align-items:center;gap:16px;height:56px;padding:0 8px 0 18px;border:1px solid var(--line2);border-radius:18px;background:rgba(11,10,9,.72);backdrop-filter:blur(14px)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--strong);font-weight:600;font-size:16px;letter-spacing:-.01em}
.brand svg{width:28px;height:28px;flex:none}
.links{display:flex;gap:22px;margin-left:auto;font-size:14px}
.links a{text-decoration:none;color:var(--muted)}.links a:hover{color:var(--strong)}
.lang{display:flex;gap:2px;font-size:12px;font-weight:500}
.lang a,.lang b{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;border-radius:10px;text-decoration:none;color:var(--muted)}
.lang b{color:var(--strong);font-weight:500}
.mlink{display:none;position:relative}
.mlink summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:center;width:44px;height:44px;border:1px solid var(--line2);border-radius:999px;color:var(--strong)}
.mlink summary::-webkit-details-marker{display:none}
.mlink .b{display:block;width:16px;height:2px;border-radius:1px;background:currentColor;position:relative}
.mlink .b::before,.mlink .b::after{content:"";position:absolute;left:0;width:16px;height:2px;border-radius:1px;background:currentColor}
.mlink .b::before{top:-5px}.mlink .b::after{top:5px}
.mlink[open] .b{background:transparent}
.mlink[open] .b::before{transform:translateY(5px) rotate(45deg)}
.mlink[open] .b::after{transform:translateY(-5px) rotate(-45deg)}
.mlink-panel{position:absolute;top:calc(100% + 10px);left:0;right:0;display:flex;flex-direction:column;padding:8px;border:1px solid var(--line2);border-radius:18px;background:var(--card);box-shadow:0 18px 44px rgba(0,0,0,.45)}
.mlink-panel a{display:flex;align-items:center;min-height:44px;padding:0 14px;border-radius:12px;text-decoration:none;color:var(--strong);font-weight:500;font-size:15px}
.mlink-panel a:hover{background:var(--bg2)}

/* кнопки-капсулы */
.pill{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 6px 0 20px;border-radius:999px;font-size:16px;font-weight:500;text-decoration:none;border:0;cursor:pointer;font-family:inherit;transition:filter .2s,background .2s}
.pill .arr{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:rgba(0,0,0,.18)}
.pill .arr svg{width:16px;height:16px}
.pill-a{background:var(--accent);color:var(--accent-ink)}.pill-a:hover{filter:brightness(1.08)}
.pill-b{background:var(--pill);color:#0A0908}.pill-b:hover{background:#D3CFC9}
.pill-sm{min-height:44px;font-size:14px;padding-left:16px}.pill-sm .arr{width:32px;height:32px}

/* hero */
.hero{position:relative;overflow:hidden;min-height:760px;display:flex;align-items:center;padding:150px 0 110px;text-align:center;border-bottom:1px solid var(--line)}
.hero video{position:absolute;left:50%;top:50%;width:min(1100px,140%);transform:translate(-50%,-48%);opacity:.85;mix-blend-mode:screen;pointer-events:none}
.hero .tint{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,#F6C089 0%,#EE8A3C 38%,#8C4A1E 75%);mix-blend-mode:multiply;pointer-events:none}
.hero .fade{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(11,10,9,.25) 0%,rgba(11,10,9,.7) 55%,var(--bg) 85%);pointer-events:none}
.hero .inner{position:relative;display:flex;flex-direction:column;align-items:center;gap:26px}
.hero p.lead{max-width:36em;margin:0;color:var(--text);font-size:18px}
.ctas{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.facts{display:flex;flex-wrap:wrap;justify-content:center;gap:0;margin-top:18px;font-size:13px;color:var(--muted)}
.facts span{padding:0 18px;border-left:1px solid var(--line2)}.facts span:first-child{border-left:0}
.facts b{color:var(--strong);font-weight:500}

section{padding:110px 0;border-bottom:1px solid var(--line)}
.head{display:flex;flex-direction:column;gap:14px;max-width:760px;margin-bottom:48px}
.head p{margin:0;color:var(--muted)}

/* схема: вход → реестр → результат */
.flow{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr) minmax(0,1fr);gap:0;align-items:center}
.col{display:flex;flex-direction:column;gap:12px}
.node{position:relative;display:flex;gap:12px;align-items:flex-start;padding:16px 18px;border:1px solid var(--line2);border-radius:14px;background:var(--card)}
.node .dot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--accent);margin-top:8px}
.node small{display:block;color:var(--muted);font-size:13px;line-height:1.45}
.node strong{font-weight:500;color:var(--strong);font-size:15px}
.col.in .node::after,.col.out .node::before{content:"";position:absolute;top:50%;width:44px;height:1px;background:linear-gradient(90deg,var(--line2),var(--accent))}
.col.in .node::after{right:-45px}.col.out .node::before{left:-45px;background:linear-gradient(90deg,var(--accent),var(--line2))}
.core{margin:0 44px;padding:30px 26px;border:1px solid rgba(238,138,60,.45);border-radius:20px;background:linear-gradient(180deg,#1A1511,#120F0D);text-align:center;display:flex;flex-direction:column;gap:14px}
.core .name{font-size:22px;font-weight:600;color:var(--strong);letter-spacing:-.01em}
.core ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.core li{font-size:12px;padding:5px 10px;border:1px solid var(--line2);border-radius:999px;color:var(--text)}

/* сравнение с обычным чатом */
.cmp{border-top:1px solid var(--line2)}
.cmp .row{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr) minmax(0,1.3fr);gap:24px;padding:20px 0;border-bottom:1px solid var(--line);align-items:baseline}
.cmp .row.hd{padding:12px 0}
.cmp .what{color:var(--strong);font-weight:500}
.cmp .yes{display:flex;gap:10px;align-items:baseline}.cmp .yes::before{content:"";flex:none;width:6px;height:6px;border-radius:50%;background:var(--accent);transform:translateY(-2px)}

/* бенто-сетка возможностей */
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}
.card{grid-column:span 4;min-width:0;padding:26px;border:1px solid var(--line2);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:14px}
.card.w6{grid-column:span 6}.card.w8{grid-column:span 8}
.card .ic{width:36px;height:36px;border-radius:10px;border:1px solid var(--line2);display:flex;align-items:center;justify-content:center;color:var(--accent)}
.card .ic svg{width:18px;height:18px}
.card p{margin:0;color:var(--muted);font-size:15px}
.faqlist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.faqlist li{list-style:none;padding:10px 12px;border-radius:10px;background:var(--bg2);font-size:14px}
.faqlist b{color:var(--accent);font-weight:500;margin-right:8px}

/* процесс */
.phases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.ph{padding:22px;border:1px solid var(--line2);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:12px;min-width:0}
.ph ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.ph li{display:flex;align-items:center;gap:12px;font-size:15px}
.ph .n{flex:none;width:28px;height:28px;border-radius:50%;border:1px solid var(--line2);display:inline-flex;align-items:center;justify-content:center;font-size:12px;color:var(--muted)}
.ph li.h .n{border:1.5px solid var(--accent);color:var(--accent)}
/* бейдж у шагов решения человека — текст задаётся пер-языковым токеном, чтобы не было утечек */
.ph li.h::after{content:"{{YOU}}";margin-left:auto;font-size:11px;color:var(--accent);letter-spacing:.08em;text-transform:uppercase}

/* цепочка доказательств: терминал, утверждение, excel */
.proof{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:24px;align-items:start}
.proof-side{display:flex;flex-direction:column;gap:16px;min-width:0}
.term{border:1px solid var(--line2);border-radius:18px;background:#0D0C0A;overflow:hidden;min-width:0}
.term .bar{display:flex;gap:6px;padding:12px 16px;border-bottom:1px solid var(--line)}
.term .bar i{width:10px;height:10px;border-radius:50%;background:var(--line2)}
.term pre{margin:0;padding:18px 20px;overflow-x:auto;font:13px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--text)}
.term .p{color:var(--muted)}.term .a{color:var(--strong)}.term .hi{color:var(--accent)}
.claim{border:1px solid rgba(238,138,60,.45);border-radius:18px;background:var(--card);padding:24px;display:flex;flex-direction:column;gap:14px}
.claim .tags{display:flex;gap:8px;flex-wrap:wrap}
.claim .tag{font-size:12px;padding:4px 10px;border-radius:999px;border:1px solid var(--line2);color:var(--muted)}
.claim .tag.a{border-color:rgba(238,138,60,.5);color:var(--accent)}
.claim p{margin:0;color:var(--text);font-size:15px}
.chain{display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:13px}
.chip{padding:8px 12px;border:1px solid var(--line2);border-radius:10px;background:var(--bg2);min-width:0}
.chip.a{border-color:rgba(238,138,60,.5)}
.chip em{font-style:normal;color:var(--accent)}
.xl{border:1px solid var(--line2);border-radius:18px;background:var(--card);padding:20px 24px}
.xl table{width:100%;border-collapse:collapse;font-size:14px}
.xl td{padding:9px 0;border-bottom:1px solid var(--line);color:var(--text)}
.xl tr:last-child td{border-bottom:0}
.xl td:last-child{text-align:right;color:var(--strong);font-variant-numeric:tabular-nums}

/* архитектура */
.stack{display:flex;flex-direction:column;max-width:760px;margin:0 auto;width:100%}
.layer{position:relative;display:flex;gap:16px;align-items:flex-start;padding:20px 24px;border:1px solid var(--line2);border-radius:16px;background:var(--card);min-width:0}
.layer+.layer{margin-top:26px}
.layer+.layer::before{content:"";position:absolute;left:50%;top:-27px;width:1px;height:26px;background:linear-gradient(180deg,var(--accent),var(--line2))}
.layer .n{flex:none;width:34px;height:34px;border-radius:10px;border:1px solid var(--line2);display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:13px}
.layer b{display:block;color:var(--strong);font-weight:500;font-size:16px;margin-bottom:4px}
.layer small{color:var(--muted);font-size:14px;line-height:1.5;display:block}

/* демо */
.demo{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line2);border:1px solid var(--line2);border-radius:18px;overflow:hidden;margin:0}
.stats div{background:var(--card);padding:22px;display:flex;flex-direction:column-reverse;gap:6px}
.stats b{font-size:30px;font-weight:500;color:var(--strong);letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.stats span{font-size:13px;color:var(--muted)}

/* установка */
.inst{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.cmd{display:flex;align-items:center;gap:10px;padding:6px 6px 6px 16px;border:1px solid var(--line2);border-radius:14px;background:var(--card)}
.cmd code{flex:1;min-width:0;overflow-x:auto;white-space:nowrap;font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--strong)}
.copy{flex:none;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--line2);background:transparent;color:var(--text);font:500 13px var(--font);cursor:pointer}
.copy:hover{border-color:var(--accent)}
blockquote{margin:6px 0 0;padding:18px 20px;border-radius:14px;background:var(--card);border:1px solid var(--line2);color:var(--strong)}

/* faq */
.faq{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px}
details{border-bottom:1px solid var(--line)}
summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;min-height:64px;padding:12px 0;color:var(--strong);font-size:18px;font-weight:500}
summary::-webkit-details-marker{display:none}
summary .pm{flex:none;width:30px;height:30px;border-radius:50%;border:1px solid var(--line2);display:inline-flex;align-items:center;justify-content:center;color:var(--accent);transition:transform .2s}
details[open] summary .pm{transform:rotate(45deg)}
details p{margin:0 0 22px;color:var(--muted);max-width:44em}

/* финал и футер */
.final{position:relative;overflow:hidden;text-align:center;border-bottom:0}
.final .box{position:relative;margin:0 auto;max-width:980px;padding:80px 28px;border:1px solid rgba(238,138,60,.4);border-radius:28px;background:radial-gradient(ellipse at 50% 0%,rgba(238,138,60,.16),rgba(11,10,9,0) 60%),var(--bg2);display:flex;flex-direction:column;align-items:center;gap:22px}
.procfig{margin:44px auto 0;max-width:760px}
.dosfig{margin:0 auto;width:100%;max-width:520px}
.procfig img,.dosfig img{display:block;width:100%;height:auto;border-radius:20px;border:1px solid var(--line2)}
footer{border-top:1px solid var(--line);padding:36px 0 calc(36px + env(safe-area-inset-bottom,0px));font-size:14px;color:var(--muted)}
footer .wrap{display:flex;flex-wrap:wrap;gap:20px;justify-content:space-between;align-items:center}
footer nav{display:flex;flex-wrap:wrap;gap:18px}footer a{text-decoration:none}footer a:hover{color:var(--strong)}

@media (max-width:980px){
  .links{display:none}
  .mlink{display:block}
  .nav .bar{padding-right:6px}
  .flow{grid-template-columns:minmax(0,1fr);gap:14px}.core{margin:6px 0}
  .col.in .node::after,.col.out .node::before{display:none}
  .card,.card.w6,.card.w8{grid-column:1/-1}
  .phases{grid-template-columns:repeat(2,minmax(0,1fr))}
  .proof,.demo,.inst,.faq{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:640px){
  section{padding:80px 0}
  .hero{min-height:640px;padding:130px 0 80px}
  .phases,.faqlist{grid-template-columns:minmax(0,1fr)}
  .cmp .row{grid-template-columns:minmax(0,1fr);gap:4px}.cmp .row.hd{display:none}
  .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
  .facts span{border-left:0;padding:2px 10px}
  .nav .bar{gap:8px}
}
@media (prefers-reduced-motion:reduce){.hero video{display:none}html{scroll-behavior:auto}}
"""

JS = """
(function(){
  function goal(name,params){if(window.ym&&window.YM_ID){window.ym(window.YM_ID,'reachGoal',name,params||{})}}
  document.querySelectorAll('[data-goal]').forEach(function(el){
    el.addEventListener('click',function(){goal(el.dataset.goal)});
  });
  document.querySelectorAll('.copy').forEach(function(b){
    b.addEventListener('click',function(){
      var t=b.parentNode.querySelector('code').textContent;
      var done=function(){var o=b.textContent;b.textContent=b.dataset.ok||'OK';setTimeout(function(){b.textContent=o},1600)};
      try{navigator.clipboard.writeText(t).then(done,done)}catch(e){done()}
      goal('copy_command',{i:b.dataset.copy});
    });
  });
  document.querySelectorAll('.mlink').forEach(function(d){
    d.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){d.removeAttribute('open')});
    });
  });
  document.querySelectorAll('details').forEach(function(d){
    d.addEventListener('toggle',function(){
      if(d.open){var s=d.querySelector('summary');goal('faq_open',{q:s?s.textContent.trim().slice(0,60):''})}
    });
  });
})();
"""

YM_LOADER = (
    "<script>window.YM_ID=@ID@;\n"
    "(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};"
    "m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,"
    "k.src=r,a.parentNode.insertBefore(k,a)})(window,document,'script',"
    "'https://mc.yandex.ru/metrika/tag.js','ym');\n"
    'ym(@ID@,"init",{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:false});\n'
    "</script>\n"
    '<noscript><img src="https://mc.yandex.ru/watch/@ID@" alt=""></noscript>'
)

# Общий блок hreflang для обеих страниц
HREFLANGS = (f'<link rel="alternate" hreflang="ru" href="{BASE}/">\n'
             f'<link rel="alternate" hreflang="en" href="{BASE}/en/">\n'
             f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')


def _page(lang_attrs: str, title: str, desc: str, canonical: str, og: str,
          body: str, tokens: dict) -> str:
    head = f"""<!doctype html>
<html lang="{lang_attrs}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{HREFLANGS}
<link rel="icon" href="{{{{A}}}}assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
{og}
<style>{{{{CSS}}}}</style>
</head>
<body>"""
    tail = """
<script>{{JS}}</script>
{{YM}}
</body>
</html>"""
    full = head + body + tail
    mapping = {"CSS": CSS, "JS": JS, "YM": tokens.pop("YM", "")}
    mapping.update(tokens)
    return render(full, mapping)


# Ключи, значения которых — уже готовая разметка/скрипты и не подлежат экранированию.
# Всё остальное (числа, TEXT/SEG, C_DOM/path, D_LABEL, USAGE, даты, KIND, A…) —
# пользовательские данные репозитория: экранируются html.escape.
RAW_KEYS = frozenset({"CSS", "JS", "YM", "BRAND"})


def render(template: str, mapping: dict) -> str:
    out = template
    for key, val in mapping.items():
        text = val if isinstance(val, str) else str(val)
        if key not in RAW_KEYS:
            text = html.escape(text, quote=True)
        out = out.replace("{{" + key + "}}", text)
    if "{{" in out:
        left = re.findall(r"\{\{(\w+)\}\}", out)
        raise BuildError(f"Остались незаполненные токены: {sorted(set(left))}")
    return out


RU_BODY = f"""
<a class="skip" href="#main">К содержимому</a>

<header class="nav">
  <div class="wrap">
    <div class="bar">
      <a class="brand" href="#top" aria-label="Стратег Фабрики продуктов — на главную">
        {{{{BRAND}}}}
        Стратег
      </a>
      <nav class="links" aria-label="Разделы">
        <a href="#how">Как работает</a><a href="#features">Возможности</a><a href="#demo">Демо</a><a href="#install">Установка</a><a href="#faq">Вопросы</a>
      </nav>
      <div class="lang"><b aria-current="true">RU</b><a href="en/" hreflang="en" data-goal="lang_switch">EN</a></div>
      <a class="pill pill-a pill-sm" href="#install" data-goal="cta_install_click">Запустить{ARROW}</a>
      <details class="mlink">
        <summary aria-label="Меню разделов"><span class="b" aria-hidden="true"></span></summary>
        <nav class="mlink-panel" aria-label="Разделы">
          <a href="#how">Как работает</a><a href="#features">Возможности</a><a href="#demo">Демо</a><a href="#install">Установка</a><a href="#faq">Вопросы</a>
        </nav>
      </details>
    </div>
  </div>
</header>

<main id="main">

<section class="hero" id="top" aria-labelledby="h1">
  <video src="{{{{A}}}}assets/hero-swarm-2.mp4" poster="{{{{A}}}}assets/hero-poster.webp" autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>
  <div class="tint" aria-hidden="true"></div><div class="fade" aria-hidden="true"></div>
  <div class="wrap inner">
    <div class="eyebrow">Исследование, а не текст про стратегию</div>
    <h1 id="h1">От размытого запроса<br><span class="acc">к стратегии,</span><br>которую можно проверить</h1>
    <p class="lead">Открытый ИИ-агент для руководителя продукта. У каждого числа есть источник, среди вариантов всегда есть «оставить как есть» и «закрыть», а решение сопровождается и после выбора.</p>
    <div class="ctas">
      <a class="pill pill-a" href="#install" data-goal="cta_install_click">Запустить за 5 минут{ARROW}</a>
      <a class="pill pill-b" href="#demo" data-goal="cta_demo_click">Смотреть демо{ARROW}</a>
    </div>
    <div class="facts"><span><b>12</b> шагов</span><span><b>3</b> решения за вами</span><span><b>{{{{N_MAPS}}}}</b> методических карт</span><span><b>0</b> внешних зависимостей</span></div>
  </div>
</section>

<section id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Как это устроено</div>
      <h2 id="how-h">Между запросом и решением <span class="acc">появляется слой доказательств</span></h2>
      <p>Агент собирает материалы, отделяет факты от гипотез и только потом предлагает варианты. Каждое утверждение остаётся в реестре со ссылкой на источник.</p>
    </div>
    <div class="flow">
      <div class="col in">
        <div class="node"><span class="dot"></span><div><strong>Запрос руководителя</strong><small>«Почему падает удержание?», «Кому продавать?»</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Ваши материалы</strong><small>документы, таблицы, интервью, скриншоты</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Открытые источники</strong><small>только разрешённые домены</small></div></div>
      </div>
      <div class="core">
        <div class="label" style="color:var(--accent)">Стратег</div>
        <div class="name">Реестр утверждений</div>
        <ul><li>факт</li><li>гипотеза</li><li>прогноз</li><li>допущение</li><li>вывод</li><li>сила A–D</li></ul>
        <p class="muted" style="margin:0;font-size:14px">Синтетические респонденты дают только гипотезы, не доказательства.</p>
      </div>
      <div class="col out">
        <div class="node"><span class="dot"></span><div><strong>Варианты и red team</strong><small>от трёх, включая «оставить» и «закрыть»</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Six-pager и Excel</strong><small>документ для комитета, RU и EN</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Решение и пересмотр</strong><small>основания, сроки, обязательства</small></div></div>
      </div>
    </div>
  </div>
</section>

<section aria-labelledby="cmp-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Зачем отдельный агент</div>
      <h2 id="cmp-h">Чем он отличается <span class="acc">от обычного чата</span></h2>
    </div>
    <div class="cmp">
      <div class="row hd label"><span>Что важно для решения</span><span>Обычный чат</span><span style="color:var(--accent)">Стратег</span></div>
      <div class="row"><span class="what">Источник у каждого числа</span><span class="muted">по просьбе, ссылки не проверяются</span><span class="yes">утверждение C### ведёт к источнику S### с цитатой</span></div>
      <div class="row"><span class="what">Факты отдельно от гипотез</span><span class="muted">смешаны в одном ответе</span><span class="yes">тип утверждения и сила доказательства A–D</span></div>
      <div class="row"><span class="what">Варианты, включая «оставить» и «закрыть»</span><span class="muted">обычно один ответ</span><span class="yes">не меньше трёх, red team атакует каждый</span></div>
      <div class="row"><span class="what">Расчёты</span><span class="muted">числа внутри текста</span><span class="yes">Excel с формулами и листом «Ввод»</span></div>
      <div class="row"><span class="what">Продолжение после перерыва</span><span class="muted">контекст теряется</span><span class="yes">состояние в файлах, новый чат продолжает с того же шага</span></div>
      <div class="row"><span class="what">Сколько стоил результат</span><span class="muted">неизвестно</span><span class="yes">токены по моделям и минуты человека</span></div>
    </div>
  </div>
</section>

<section id="features" aria-labelledby="feat-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Возможности</div>
      <h2 id="feat-h">Всё, чтобы решению <span class="acc">можно было верить</span></h2>
    </div>
    <div class="grid">
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div>
        <h3>Цепочка доказательств</h3>
        <p>Видно, на чём держится каждый вывод и что изменится, если обновится источник.</p>
      </article>
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 5h12M4 10h12M4 15h7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Варианты и red team</h3>
        <p>Отдельный субагент атакует каждый вариант до того, как вы его увидите.</p>
      </article>
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Расчёты на формулах</h3>
        <p>Юнит-экономика, модель роста, когорты и размер рынка в Excel. Входные данные можно поменять.</p>
      </article>
      <article class="card w8">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>Документ для комитета</h3>
        <p>Six-pager из шести ответов, которых ждёт комитет. RU и EN, MD, PDF, DOCX и четыре книги Excel.</p>
        <ul class="faqlist" style="margin:0;padding:0">
          <li><b>1</b>Рынок, тренды, конкуренты</li><li><b>2</b>Кто пользователи и что мешает</li>
          <li><b>3</b>Инициативы и обоснование</li><li><b>4</b>Тактики под потребности</li>
          <li><b>5</b>План, вклад, сезонность</li><li><b>6</b>KPI бизнеса и продукта</li>
        </ul>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>После решения</h3>
        <p>Решение хранит основания, обязательства и дату пересмотра. Новые данные показывают, какие выводы устарели.</p>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Журнал и стоимость</h3>
        <p>Что сделано, на каком основании и сколько стоило: токены по моделям и время людей.</p>
      </article>
    </div>
  </div>
</section>

<section id="process" aria-labelledby="proc-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Процесс</div>
      <h2 id="proc-h">Двенадцать шагов. <span class="acc">Три решения за вами.</span></h2>
      <p>Между точками решения агент работает сам и показывает прогресс строкой «Шаг N/12». «Стоп» ставит паузу, «уточни» меняет задачу.</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Исследовать</h3><ol><li class="h"><span class="n">1</span>Бриф</li><li><span class="n">2</span>Источники</li><li><span class="n">3</span>Исследование</li><li><span class="n">4</span>Сегменты</li></ol></div>
      <div class="ph"><h3>Определить</h3><ol><li><span class="n">5</span>Картина ситуации</li><li><span class="n">6</span>Варианты и red team</li><li class="h"><span class="n">7</span>Выбор</li></ol></div>
      <div class="ph"><h3>Разработать</h3><ol><li><span class="n">8</span>Стратегии</li><li><span class="n">9</span>План проверки</li><li><span class="n">10</span>Ревью качества</li></ol></div>
      <div class="ph"><h3>Довести</h3><ol><li class="h"><span class="n">11</span>Решение</li><li><span class="n">12</span>Мониторинг</li></ol></div>
    </div>
    <figure class="procfig">
      <picture>
        <source type="image/avif" srcset="{{{{A}}}}assets/dark-double-diamond.avif">
        <img src="{{{{A}}}}assets/dark-double-diamond.webp" width="1800" height="1350" alt="Двойной алмаз процесса: расходящиеся и сходящиеся линии, выложенные нитью на тёмной бумаге" loading="lazy" decoding="async">
      </picture>
    </figure>
  </div>
</section>

<section id="proof" aria-labelledby="proof-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Цепочка доказательств</div>
      <h2 id="proof-h">Фрагменты реальной работы <span class="acc">демо-проекта CVStart</span></h2>
      <p>Ниже — настоящие данные из реестра демо-проекта: сессия, утверждение с источником и расчёт. Ничего не нарисовано «для красоты».</p>
    </div>
    <div class="proof">
      <div class="term" aria-label="Фрагмент сессии агента в демо-проекте">
        <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
        <pre><span class="p">$</span> pfs new "CVStart: платная версия" "Разработать коммерческую версию cvstart.org и стратегию вывода на рынок"
<span class="a">Шаг 1/12 · intake</span> · бриф подтверждён · дальше: sources
<span class="a">Шаг 2/12 · sources</span> · {{{{D_SOURCES}}}} источников · 0 запрещённых доменов · дальше: research
<span class="p">$</span> pfs claim add "{{{{SEG}}}}" --kind fact --source {{{{C_SRC}}}} --grade {{{{GRADE}}}}
<span class="hi">{{{{C_ID}}}} · {{{{KIND}}}} · сила {{{{GRADE}}}} · цитата сохранена</span>
<span class="a">Шаг 3/12 · research</span> · {{{{D_CLAIMS}}}} утверждений в реестре · дальше: discovery
<span class="p">&gt;</span> стоп — пауза: состояние в файлах, новый чат продолжит с шага 3</pre>
      </div>
      <div class="proof-side">
        <div class="claim">
          <div class="tags"><span class="tag a">{{{{C_ID}}}} · {{{{KIND}}}}</span><span class="tag">сила {{{{GRADE}}}}</span><span class="tag">источник {{{{C_SRC}}}}</span></div>
          <p>{{{{TEXT}}}}</p>
          <div class="chain">
            <span class="chip a"><em>{{{{C_ID}}}}</em> · {{{{KIND}}}} · сила {{{{GRADE}}}}</span><span aria-hidden="true" class="muted">→</span>
            <span class="chip"><em>{{{{C_SRC}}}}</em> · {{{{DOM}}}} · {{{{DATE}}}}</span><span aria-hidden="true" class="muted">→</span>
            <span class="chip">six-pager · {{{{USAGE}}}}</span>
          </div>
        </div>
        <div class="xl">
          <div class="label" style="margin-bottom:10px">Excel · лист «Ввод»</div>
          <table>
            <tr><td>Цена Pro</td><td>${{{{XL_PRICE}}}}/мес</td></tr>
            <tr><td>Переменные 25% → вклад на покрытие</td><td>${{{{XL_CM}}}}</td></tr>
            <tr><td>LTV</td><td>≈ ${{{{XL_LTV}}}}</td></tr>
            <tr><td>LTV / CAC</td><td>≈ {{{{XL_RATIO}}}}</td></tr>
          </table>
          <p class="muted" style="margin:10px 0 0;font-size:13px">Значения можно поменять — формулы пересчитаются.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="demo" aria-labelledby="demo-h">
  <div class="wrap demo">
    <div class="head" style="margin:0">
      <div class="label">Демо-проект</div>
      <h2 id="demo-h">CVStart: <span class="acc">платная версия</span> и выход на рынок</h2>
      <p>Задача руководителя дословно: «Разработать коммерческую версию cvstart.org и стратегию вывода на рынок на весь мир». Числа — из проекта, не руками.</p>
      <div><a class="pill pill-b pill-sm" href="demo.html" data-goal="cta_demo_click">Открыть разбор{ARROW}</a></div>
    </div>
    <div>
      <!-- числа подставляет scripts/build_site.py из projects/demo -->
      <dl class="stats">
        <div><dt><span>источников</span></dt><dd style="margin:0"><b>{{{{D_SOURCES}}}}</b></dd></div>
        <div><dt><span>утверждений, из них факты — {{{{D_FACTS}}}}</span></dt><dd style="margin:0"><b>{{{{D_CLAIMS}}}}</b></dd></div>
        <div><dt><span>вариантов A–{{{{D_OPT_LAST}}}}, со статус-кво и закрытием</span></dt><dd style="margin:0"><b>A–{{{{D_OPT_LAST}}}}</b></dd></div>
        <div><dt><span>возражений и скрытых допущений red team</span></dt><dd style="margin:0"><b>{{{{D_OBJ}}}} + {{{{D_ASM}}}}</b></dd></div>
        <div><dt><span>выбор: {{{{D_LABEL}}}}</span></dt><dd style="margin:0"><b>{{{{D_LETTER}}}}</b></dd></div>
        <div><dt><span>пересмотр решения D001</span></dt><dd style="margin:0"><b>{{{{REVIEW}}}}</b></dd></div>
      </dl>
    </div>
  </div>
</section>

<section id="arch" aria-labelledby="arch-h">
  <div class="wrap">
    <div class="head" style="margin:0 auto 48px;text-align:center;align-items:center">
      <div class="label">Архитектура</div>
      <h2 id="arch-h">Гарантии — не в промптах, <span class="acc">а в коде и файлах</span></h2>
      <p>Автотесты CLI ({{{{N_TESTS}}}}) проверяют ядро после каждого изменения. Состояние проекта лежит в файлах рядом с кодом — работа переживает перерыв и переезд между средами.</p>
    </div>
    <div class="stack">
      <div class="layer"><span class="n">1</span><div><b>Среда · AGENTS.md</b><small>правила: источник у каждого числа, синтетика — только гипотезы, существенное решает человек · навыков: {{{{N_SKILLS}}}} · субагентов: {{{{N_AGENTS}}}} · хуков: {{{{N_HOOKS}}}}</small></div></div>
      <div class="layer"><span class="n">2</span><div><b>Ядро · tools/pfs</b><small>CLI и MCP: шаги 1–12, реестр утверждений, источники с sha256, экспорт six-pager · только стандартная библиотека Python</small></div></div>
      <div class="layer"><span class="n">3</span><div><b>Знания · knowledge/</b><small>{{{{N_MAPS}}}} карт методик на русском · {{{{N_MAPS_EN}}}} зеркал на английском · шаблоны документов и рубрики оценки</small></div></div>
      <div class="layer"><span class="n">4</span><div><b>Файлы проекта</b><small>state.json · claims.jsonl · sources/ — основания решений остаются читаемыми и после года перерыва</small></div></div>
    </div>
  </div>
</section>

<section id="install" aria-labelledby="inst-h">
  <div class="wrap inst">
    <div class="head" style="margin:0">
      <div class="label">Установка</div>
      <h2 id="inst-h">Пять минут <span class="acc">до первой задачи</span></h2>
      <p>Нужны Python 3.9+ и одна из сред: Claude Code, OpenCode, Cursor или Codex.</p>
      <blockquote>«Платная защита от спам-звонков теряет подписчиков. Что делать с продуктом и что говорить абонентам?»</blockquote>
    </div>
    <ol class="steps">
      <li><span class="label">1 · Скачайте репозиторий</span><div class="cmd"><code>git clone https://github.com/Fighter90/product-factory-strategist.git</code><button class="copy" type="button" data-copy="0" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">2 · Установите pfs</span><div class="cmd"><code>cd product-factory-strategist &amp;&amp; ./scripts/install.sh</code><button class="copy" type="button" data-copy="1" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">3 · Проверьте окружение</span><div class="cmd"><code>pfs doctor</code><button class="copy" type="button" data-copy="2" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">4 · Откройте папку в своей среде</span><div class="cmd"><code>opencode</code><button class="copy" type="button" data-copy="3" data-ok="Скопировано">Копировать</button></div></li>
    </ol>
  </div>
</section>

<section id="faq" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="head" style="margin:0"><div class="label">Вопросы</div><h2 id="faq-h">Частые <span class="acc">вопросы</span></h2></div>
    <div>
      <details><summary>Какие данные использует агент?<span class="pm" aria-hidden="true">+</span></summary><p>Только открытые источники и материалы, которые вы передали сами. Разрешённые домены задаются в проекте. Команды из текстов источников агент не выполняет.</p></details>
      <details><summary>Можно ли остановить и поправить работу?<span class="pm" aria-hidden="true">+</span></summary><p>Да. «Стоп» ставит паузу, «уточни: …» меняет задачу, ваши ручные правки агент читает и не затирает. Новый чат продолжает с того же шага.</p></details>
      <details><summary>Сколько стоит прогон?<span class="pm" aria-hidden="true">+</span></summary><p>Зависит от модели и объёма исследования. Токены по моделям и время людей видны командой pfs cost и в приложении к отчёту.</p></details>
      <details><summary>Чем это лучше обычного чата?<span class="pm" aria-hidden="true">+</span></summary><p>Агент ведёт процесс по шагам, хранит доказательства в реестре и проверяет документы. Обычный чат отвечает текстом, который трудно проверить и продолжить.</p></details>
      <details><summary>Работает ли на русском и английском?<span class="pm" aria-hidden="true">+</span></summary><p>Да: инструкции, база знаний и итоговые документы есть на обоих языках, язык выбирается при создании проекта.</p></details>
    </div>
  </div>
</section>

<section class="final" aria-labelledby="fin-h">
  <div class="wrap">
    <div class="box">
      <figure class="dosfig">
        <picture>
          <source type="image/avif" srcset="{{{{A}}}}assets/dossier-dark.avif">
          <img src="{{{{A}}}}assets/dossier-dark.webp" width="1800" height="1012" alt="Пакет решения: документы, собранные нитью в стопку, на тёмном фоне" loading="lazy" decoding="async">
        </picture>
      </figure>
      <div class="eyebrow">Открытый код · MIT</div>
      <h2 id="fin-h">Проверьте агента <span class="acc">на своей задаче</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Откройте папку в своей среде и опишите задачу как есть. Агент задаст до трёх вопросов и начнёт исследование.</p>
      <div class="ctas">
        <a class="pill pill-a" href="#install" data-goal="cta_install_click">Установить{ARROW}</a>
        <a class="pill pill-b" href="https://github.com/Fighter90/product-factory-strategist" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <span style="color:var(--strong);font-weight:500">Стратег Фабрики продуктов</span>
    <nav aria-label="Ссылки"><a href="https://github.com/Fighter90/product-factory-strategist">GitHub</a><a href="help.html">Справка</a><a href="materials.html">Материалы демо</a><a href="https://github.com/Fighter90/product-factory-strategist/blob/main/CHANGELOG.md">Changelog</a></nav>
    <span>MIT · открытый код</span>
  </div>
</footer>
"""

EN_BODY = f"""
<a class="skip" href="#main">Skip to content</a>

<header class="nav">
  <div class="wrap">
    <div class="bar">
      <a class="brand" href="#top" aria-label="Product Factory Strategist — home">
        {{{{BRAND}}}}
        Strategist
      </a>
      <nav class="links" aria-label="Sections">
        <a href="#how">How it works</a><a href="#features">Features</a><a href="#demo">Demo</a><a href="#install">Install</a><a href="#faq">FAQ</a>
      </nav>
      <div class="lang"><a href="../" hreflang="ru" data-goal="lang_switch">RU</a><b aria-current="true">EN</b></div>
      <a class="pill pill-a pill-sm" href="#install" data-goal="cta_install_click">Start{ARROW}</a>
      <details class="mlink">
        <summary aria-label="Sections menu"><span class="b" aria-hidden="true"></span></summary>
        <nav class="mlink-panel" aria-label="Sections">
          <a href="#how">How it works</a><a href="#features">Features</a><a href="#demo">Demo</a><a href="#install">Install</a><a href="#faq">FAQ</a>
        </nav>
      </details>
    </div>
  </div>
</header>

<main id="main">

<section class="hero" id="top" aria-labelledby="h1">
  <video src="{{{{A}}}}assets/hero-swarm-2.mp4" poster="{{{{A}}}}assets/hero-poster.webp" autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>
  <div class="tint" aria-hidden="true"></div><div class="fade" aria-hidden="true"></div>
  <div class="wrap inner">
    <div class="eyebrow">Research, not prose about strategy</div>
    <h1 id="h1">From a vague request<br><span class="acc">to a strategy</span><br>you can actually check</h1>
    <p class="lead">An open-source AI agent for product leads. Every number has a source, the options always include “keep as is” and “shut it down”, and the decision is tracked after you make it.</p>
    <div class="ctas">
      <a class="pill pill-a" href="#install" data-goal="cta_install_click">Start in 5 minutes{ARROW}</a>
      <a class="pill pill-b" href="#demo" data-goal="cta_demo_click">See the demo{ARROW}</a>
    </div>
    <div class="facts"><span><b>12</b> steps</span><span><b>3</b> decisions are yours</span><span><b>{{{{N_MAPS}}}}</b> method cards</span><span><b>0</b> external dependencies</span></div>
  </div>
</section>

<section id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head">
      <div class="label">How it works</div>
      <h2 id="how-h">Between the request and the decision <span class="acc">sits a layer of evidence</span></h2>
      <p>The agent gathers material, separates facts from guesses and only then proposes options. Every claim stays in a registry with a link to its source.</p>
    </div>
    <div class="flow">
      <div class="col in">
        <div class="node"><span class="dot"></span><div><strong>The product lead’s question</strong><small>“Why is retention falling?”, “Who should we sell to?”</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Your materials</strong><small>documents, spreadsheets, interviews, screenshots</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Open sources</strong><small>allowed domains only</small></div></div>
      </div>
      <div class="core">
        <div class="label" style="color:var(--accent)">Strategist</div>
        <div class="name">Claim registry</div>
        <ul><li>fact</li><li>hypothesis</li><li>forecast</li><li>assumption</li><li>inference</li><li>grade A–D</li></ul>
        <p class="muted" style="margin:0;font-size:14px">Synthetic respondents only ever produce hypotheses, never proof.</p>
      </div>
      <div class="col out">
        <div class="node"><span class="dot"></span><div><strong>Options and red team</strong><small>three or more, incl. “keep” and “shut down”</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Six-pager and Excel</strong><small>a committee document in RU and EN</small></div></div>
        <div class="node"><span class="dot"></span><div><strong>Decision and review</strong><small>grounds, deadlines, commitments</small></div></div>
      </div>
    </div>
  </div>
</section>

<section aria-labelledby="cmp-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Why a dedicated agent</div>
      <h2 id="cmp-h">How it differs <span class="acc">from a plain chat</span></h2>
    </div>
    <div class="cmp">
      <div class="row hd label"><span>What the decision needs</span><span>Plain chat</span><span style="color:var(--accent)">Strategist</span></div>
      <div class="row"><span class="what">A source for every number</span><span class="muted">on request, links unchecked</span><span class="yes">claim C### links to source S### with a quote</span></div>
      <div class="row"><span class="what">Facts kept apart from guesses</span><span class="muted">mixed into one answer</span><span class="yes">claim type plus evidence grade A–D</span></div>
      <div class="row"><span class="what">Options that include “keep” and “shut down”</span><span class="muted">usually a single answer</span><span class="yes">at least three, each attacked by a red team</span></div>
      <div class="row"><span class="what">Calculations</span><span class="muted">numbers inside prose</span><span class="yes">Excel with formulas and an input sheet</span></div>
      <div class="row"><span class="what">Picking up after a break</span><span class="muted">context is lost</span><span class="yes">state lives in files, a new chat resumes at the same step</span></div>
      <div class="row"><span class="what">What the result cost</span><span class="muted">unknown</span><span class="yes">tokens per model and human minutes</span></div>
    </div>
  </div>
</section>

<section id="features" aria-labelledby="feat-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Features</div>
      <h2 id="feat-h">Everything a decision needs <span class="acc">to be trusted</span></h2>
    </div>
    <div class="grid">
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div>
        <h3>Chain of evidence</h3>
        <p>See what every conclusion rests on and what changes when a source is updated.</p>
      </article>
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 5h12M4 10h12M4 15h7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Options and red team</h3>
        <p>A separate subagent attacks every option before you see it.</p>
      </article>
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Models built on formulas</h3>
        <p>Unit economics, a growth model, cohorts and market size in Excel, with editable inputs.</p>
      </article>
      <article class="card w8">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>A document for the committee</h3>
        <p>A six-pager built on the six answers a committee expects. RU and EN, MD, PDF, DOCX and four Excel workbooks.</p>
        <ul class="faqlist" style="margin:0;padding:0">
          <li><b>1</b>Market, trends, competitors</li><li><b>2</b>Who the users are, what blocks them</li>
          <li><b>3</b>Initiatives and the case for each</li><li><b>4</b>Tactics mapped to needs</li>
          <li><b>5</b>Plan, contribution, seasonality</li><li><b>6</b>Business and product KPIs</li>
        </ul>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>After the decision</h3>
        <p>The decision keeps its grounds, commitments and review date. New data shows which conclusions went stale.</p>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>
        <h3>Log and cost</h3>
        <p>What was done, on what grounds and at what cost: tokens per model and people’s time.</p>
      </article>
    </div>
  </div>
</section>

<section id="process" aria-labelledby="proc-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Process</div>
      <h2 id="proc-h">Twelve steps. <span class="acc">Three decisions are yours.</span></h2>
      <p>Between the decision points the agent works on its own and reports progress as “Step N/12”. Say “stop” to pause or “refine” to change the task.</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Discover</h3><ol><li class="h"><span class="n">1</span>Brief</li><li><span class="n">2</span>Sources</li><li><span class="n">3</span>Research</li><li><span class="n">4</span>Segments</li></ol></div>
      <div class="ph"><h3>Define</h3><ol><li><span class="n">5</span>Situation</li><li><span class="n">6</span>Options and red team</li><li class="h"><span class="n">7</span>Choice</li></ol></div>
      <div class="ph"><h3>Develop</h3><ol><li><span class="n">8</span>Strategies</li><li><span class="n">9</span>Validation plan</li><li><span class="n">10</span>Quality review</li></ol></div>
      <div class="ph"><h3>Deliver</h3><ol><li class="h"><span class="n">11</span>Decision</li><li><span class="n">12</span>Monitoring</li></ol></div>
    </div>
    <figure class="procfig">
      <picture>
        <source type="image/avif" srcset="{{{{A}}}}assets/dark-double-diamond.avif">
        <img src="{{{{A}}}}assets/dark-double-diamond.webp" width="1800" height="1350" alt="Double-diamond process: diverging and converging lines laid out with thread on dark paper" loading="lazy" decoding="async">
      </picture>
    </figure>
  </div>
</section>

<section id="proof" aria-labelledby="proof-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Chain of evidence</div>
      <h2 id="proof-h">Fragments of the real CVStart <span class="acc">demo project</span></h2>
      <p>Below is real data from the demo project registry: a session, a claim with its source and a calculation. Nothing is drawn “for beauty”.</p>
    </div>
    <div class="proof">
      <div class="term" aria-label="An excerpt of an agent session in the demo project">
        <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
        <pre><span class="p">$</span> pfs new "CVStart: paid version" "Build a commercial version of cvstart.org and take it to market worldwide"
<span class="a">Step 1/12 · intake</span> · brief confirmed · next: sources
<span class="a">Step 2/12 · sources</span> · {{{{D_SOURCES}}}} sources · 0 blocked domains · next: research
<span class="p">$</span> pfs claim add "{{{{SEG}}}}" --kind fact --source {{{{C_SRC}}}} --grade {{{{GRADE}}}}
<span class="hi">{{{{C_ID}}}} · {{{{KIND}}}} · grade {{{{GRADE}}}} · quote saved</span>
<span class="a">Step 3/12 · research</span> · {{{{D_CLAIMS}}}} claims in the registry · next: discovery
<span class="p">&gt;</span> stop — pause: the state lives in files, a new chat resumes at step 3</pre>
      </div>
      <div class="proof-side">
        <div class="claim">
          <div class="tags"><span class="tag a">{{{{C_ID}}}} · {{{{KIND}}}}</span><span class="tag">grade {{{{GRADE}}}}</span><span class="tag">source {{{{C_SRC}}}}</span></div>
          <p>{{{{TEXT}}}}</p>
          <div class="chain">
            <span class="chip a"><em>{{{{C_ID}}}}</em> · {{{{KIND}}}} · grade {{{{GRADE}}}}</span><span aria-hidden="true" class="muted">→</span>
            <span class="chip"><em>{{{{C_SRC}}}}</em> · {{{{DOM}}}} · {{{{DATE}}}}</span><span aria-hidden="true" class="muted">→</span>
            <span class="chip">six-pager · {{{{USAGE}}}}</span>
          </div>
        </div>
        <div class="xl">
          <div class="label" style="margin-bottom:10px">Excel · input sheet</div>
          <table>
            <tr><td>Pro price</td><td>${{{{XL_PRICE}}}}/mo</td></tr>
            <tr><td>25% variable costs → contribution margin</td><td>${{{{XL_CM}}}}</td></tr>
            <tr><td>LTV</td><td>≈ ${{{{XL_LTV}}}}</td></tr>
            <tr><td>LTV / CAC</td><td>≈ {{{{XL_RATIO}}}}</td></tr>
          </table>
          <p class="muted" style="margin:10px 0 0;font-size:13px">Change the inputs and the formulas recalculate.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="demo" aria-labelledby="demo-h">
  <div class="wrap demo">
    <div class="head" style="margin:0">
      <div class="label">Demo project</div>
      <h2 id="demo-h">CVStart: <span class="acc">a paid version</span> and a go-to-market plan</h2>
      <p>The product lead’s request, word for word: “Build a commercial version of cvstart.org and a strategy to take it to market worldwide.” Numbers come from the project, not from hands.</p>
      <div><a class="pill pill-b pill-sm" href="../demo.html" data-goal="cta_demo_click">Open the walkthrough{ARROW}</a></div>
    </div>
    <div>
      <!-- numbers are substituted by scripts/build_site.py from the demo project -->
      <dl class="stats">
        <div><dt><span>sources</span></dt><dd style="margin:0"><b>{{{{D_SOURCES}}}}</b></dd></div>
        <div><dt><span>claims, of them facts — {{{{D_FACTS}}}}</span></dt><dd style="margin:0"><b>{{{{D_CLAIMS}}}}</b></dd></div>
        <div><dt><span>options A–{{{{D_OPT_LAST}}}}, incl. status quo and shut-down</span></dt><dd style="margin:0"><b>A–{{{{D_OPT_LAST}}}}</b></dd></div>
        <div><dt><span>red-team objections and hidden assumptions</span></dt><dd style="margin:0"><b>{{{{D_OBJ}}}} + {{{{D_ASM}}}}</b></dd></div>
        <div><dt><span>chosen: {{{{D_LABEL}}}}</span></dt><dd style="margin:0"><b>{{{{D_LETTER}}}}</b></dd></div>
        <div><dt><span>review of decision D001</span></dt><dd style="margin:0"><b>{{{{REVIEW}}}}</b></dd></div>
      </dl>
    </div>
  </div>
</section>

<section id="arch" aria-labelledby="arch-h">
  <div class="wrap">
    <div class="head" style="margin:0 auto 48px;text-align:center;align-items:center">
      <div class="label">Architecture</div>
      <h2 id="arch-h">The guarantees live <span class="acc">in code and files</span>, not in prompts</h2>
      <p>CLI automated tests ({{{{N_TESTS}}}}) check the core after every change. The project state lives in files next to the code — work survives breaks and moves between tools.</p>
    </div>
    <div class="stack">
      <div class="layer"><span class="n">1</span><div><b>Environment · AGENTS.md</b><small>rules: a source for every number, synthetics produce hypotheses only, a human decides what matters · skills: {{{{N_SKILLS}}}} · subagents: {{{{N_AGENTS}}}} · hooks: {{{{N_HOOKS}}}}</small></div></div>
      <div class="layer"><span class="n">2</span><div><b>Core · tools/pfs</b><small>CLI and MCP: steps 1–12, the claim registry, sha256-stamped sources, six-pager export · Python standard library only</small></div></div>
      <div class="layer"><span class="n">3</span><div><b>Knowledge · knowledge/</b><small>{{{{N_MAPS}}}} method cards in Russian · {{{{N_MAPS_EN}}}} English mirrors · document templates and scoring rubrics</small></div></div>
      <div class="layer"><span class="n">4</span><div><b>Project files</b><small>state.json · claims.jsonl · sources/ — the grounds of decisions stay readable even after a year-long break</small></div></div>
    </div>
  </div>
</section>

<section id="install" aria-labelledby="inst-h">
  <div class="wrap inst">
    <div class="head" style="margin:0">
      <div class="label">Install</div>
      <h2 id="inst-h">Five minutes <span class="acc">to your first task</span></h2>
      <p>You need Python 3.9+ and one of Claude Code, OpenCode, Cursor or Codex.</p>
      <blockquote>“Our paid spam-call protection keeps losing subscribers. What should we do with the product, and what should we tell customers?”</blockquote>
    </div>
    <ol class="steps">
      <li><span class="label">1 · Clone the repository</span><div class="cmd"><code>git clone https://github.com/Fighter90/product-factory-strategist.git</code><button class="copy" type="button" data-copy="0" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">2 · Install pfs</span><div class="cmd"><code>cd product-factory-strategist &amp;&amp; ./scripts/install.sh</code><button class="copy" type="button" data-copy="1" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">3 · Check your setup</span><div class="cmd"><code>pfs doctor</code><button class="copy" type="button" data-copy="2" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">4 · Open the folder in your tool</span><div class="cmd"><code>opencode</code><button class="copy" type="button" data-copy="3" data-ok="Copied">Copy</button></div></li>
    </ol>
  </div>
</section>

<section id="faq" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="head" style="margin:0"><div class="label">FAQ</div><h2 id="faq-h">Frequently <span class="acc">asked</span></h2></div>
    <div>
      <details><summary>What data does the agent use?<span class="pm" aria-hidden="true">+</span></summary><p>Only open sources and the materials you give it. Allowed domains are set per project. The agent never follows instructions found inside source texts.</p></details>
      <details><summary>Can I stop it and make corrections?<span class="pm" aria-hidden="true">+</span></summary><p>Yes. “Stop” pauses the run, “refine: …” changes the task, and the agent reads your manual edits instead of overwriting them. A new chat resumes from the same step.</p></details>
      <details><summary>How much does a run cost?<span class="pm" aria-hidden="true">+</span></summary><p>It depends on the model and how much research the task needs. Tokens per model and people’s time are shown by pfs cost and in the report appendix.</p></details>
      <details><summary>Why not just use a chat?<span class="pm" aria-hidden="true">+</span></summary><p>The agent runs a step-by-step process, keeps evidence in a registry and checks its documents. A plain chat gives you text that is hard to verify or continue.</p></details>
      <details><summary>Does it work in Russian and English?<span class="pm" aria-hidden="true">+</span></summary><p>Yes. Instructions, the knowledge base and the final documents exist in both languages; you pick the language when you create a project.</p></details>
    </div>
  </div>
</section>

<section class="final" aria-labelledby="fin-h">
  <div class="wrap">
    <div class="box">
      <figure class="dosfig">
        <picture>
          <source type="image/avif" srcset="{{{{A}}}}assets/dossier-dark.avif">
          <img src="{{{{A}}}}assets/dossier-dark.webp" width="1800" height="1012" alt="Decision package: documents bundled with thread on a dark background" loading="lazy" decoding="async">
        </picture>
      </figure>
      <div class="eyebrow">Open source · MIT</div>
      <h2 id="fin-h">Try the agent <span class="acc">on your own problem</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Open the folder in your tool and describe the task as it is. The agent asks up to three questions and starts the research.</p>
      <div class="ctas">
        <a class="pill pill-a" href="#install" data-goal="cta_install_click">Install{ARROW}</a>
        <a class="pill pill-b" href="https://github.com/Fighter90/product-factory-strategist" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap">
    <span style="color:var(--strong);font-weight:500">Product Factory Strategist</span>
    <nav aria-label="Links"><a href="https://github.com/Fighter90/product-factory-strategist">GitHub</a><a href="../help.html">Help</a><a href="../materials.html">Demo materials</a><a href="https://github.com/Fighter90/product-factory-strategist/blob/main/CHANGELOG.md">Changelog</a></nav>
    <span>MIT · open source</span>
  </div>
</footer>
"""


# OG-картинка одна на оба языка: og-ru.jpg и og-en.jpg были побайтово одинаковы
# (ревью PRO-66), а сама картинка — языконезависимое фото. Текст расшаривающейся
# ссылки подставляет соцсеть из og:title/og:description, а не из картинки.
def _og(lang: str, title: str, desc: str, canonical: str) -> str:
    return f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="{'Стратег Фабрики продуктов' if lang == 'ru' else 'Product Factory Strategist'}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">"""


def build(out: Path, ym_id: str | None) -> list[Path]:
    tokens = {}
    tokens.update(repo_numbers())
    tokens.update(demo_numbers())
    tokens.update(claim_facts())
    tokens.update(excel_numbers())
    tokens["YM"] = YM_LOADER.replace("@ID@", ym_id) if ym_id else ""

    ru_title = "Стратег Фабрики продуктов — ИИ-агент для руководителя продукта"
    ru_desc = ("Агент проводит исследование и собирает стратегию, которую можно проверить: "
               "источник у каждого числа, разные варианты, six-pager для комитета и "
               "сопровождение решения.")
    en_title = "Product Factory Strategist — an AI agent for product leads"
    en_desc = ("The agent runs real research and builds a strategy you can check: a source for "
               "every number, genuinely different options, a committee six-pager and follow-up "
               "after the decision.")

    # Пер-языковые подстановки: KIND/TEXT/SEG/DATE/USAGE/REVIEW/YOU/префикс ассетов
    ru = dict(tokens)
    ru.update({"KIND": tokens["KIND_RU"], "TEXT": tokens["TEXT"], "SEG": tokens["SEG_RU"],
               "DATE": tokens["DATE_RU"], "USAGE": tokens["USAGE_RU"], "REVIEW": tokens["REVIEW_RU"],
               "DOM": tokens["C_DOM"], "A": "", "BRAND": BRAND_SVG, "YOU": "вы"})
    en = dict(tokens)
    en.update({"KIND": tokens["KIND_EN"], "TEXT": tokens["TEXT_EN"], "SEG": tokens["SEG_EN"],
               "DATE": tokens["DATE_EN"], "USAGE": tokens["USAGE_EN"], "REVIEW": tokens["REVIEW_EN"],
               "DOM": tokens["C_DOM"], "A": "../", "BRAND": BRAND_SVG, "YOU": "you"})

    ru_page = _page("ru", ru_title, ru_desc, f"{BASE}/", _og("ru", ru_title, ru_desc, f"{BASE}/"),
                    RU_BODY, ru)
    en_page = _page("en", en_title, en_desc, f"{BASE}/en/", _og("en", en_title, en_desc, f"{BASE}/en/"),
                    EN_BODY, en)

    written = []
    for rel, content in ((Path("index.html"), ru_page), (Path("en") / "index.html", en_page)):
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Генератор лендинга strategyproduct.ru (RU и EN)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"каталог вывода (по умолчанию {DEFAULT_OUT.relative_to(ROOT)})")
    ap.add_argument("--ym-id", default=None,
                    help="ID счётчика Яндекс Метрики; не хранится в репозитории (см. site/ANALYTICS.md)")
    args = ap.parse_args(argv)
    if args.ym_id and not args.ym_id.isdigit():
        print("Ошибка: --ym-id должен быть числом", file=sys.stderr)
        return 2
    try:
        written = build(args.out.resolve(), args.ym_id)
    except BuildError as e:
        print(f"Ошибка сборки: {e}", file=sys.stderr)
        return 1
    for p in written:
        try:
            shown = p.relative_to(ROOT)
        except ValueError:
            shown = p
        print(f"Записан {shown} ({p.stat().st_size} байт)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
