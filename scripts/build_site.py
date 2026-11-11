#!/usr/bin/env python3
"""Генератор лендинга strategyproduct.ru — PRO-66 (дизайн v3 «тёплый тёмный»).

Статическая генерация `/` (RU) и `/en/` (EN): полный текст в HTML, hreflang,
OG-картинки по языкам, числа — из репозитория (карты знаний, навыки, субагенты,
хуки, автотесты, демо-проект `projects/демо`). JS — только цели Метрики,
копирование команд и аналитика аккордеона; без JS видны все тексты и числа.

Только стандартная библиотека. Счётчик Метрики в репозиторий не пишется:
подключается флагом `--ym-id` (см. site/ANALYTICS.md).

Скоуп PRO-66: генератор собирает весь сайт в одной тёплой тёмной системе —
`/` и `/en/`, а также demo, help и materials (RU в корне, EN в `/en/`; решение
раунда ревью 3: раздел структуры задачи требует эти страницы «в той же системе»,
переносить их на отдельную задачу без решения владельца нельзя). Старые
двуязычные страницы с переключателем setLang удалены: у каждой страницы свой
язык, canonical и hreflang-пара, ноль утечек закреплён тестами
tests/test_subpages.py и tests/test_site_build.py.

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

# Метка выбранного варианта для EN-страницы. «03_options.md» пишется по-русски,
# поэтому D_LABEL из него нельзя подставлять на EN как есть — это утечка RU.
# Перевод держим картой по точному тексту метки: формулировка в документе
# изменилась — сборка падает громко, а не показывает русский текст на EN.
D_LABEL_EN_MAP = {
    "Оставить как есть": "Keep as is",
    "Hosted freemium SaaS": "Hosted freemium SaaS",
    "B2B white-label": "B2B white-label",
    "Open-core dual-license": "Open-core dual-license",
    "Закрыть коммерческую ветку": "Shut down the commercial track",
}
_CYRILLIC = re.compile(r"[\u0400-\u04FF]")


def _label_en(label: str) -> str:
    if label not in D_LABEL_EN_MAP:
        raise BuildError(
            f"Нет EN-перевода метки выбранного варианта: {label!r} — "
            f"добавьте её в D_LABEL_EN_MAP в scripts/build_site.py")
    en = D_LABEL_EN_MAP[label]
    if _CYRILLIC.search(en):
        raise BuildError(f"EN-метка варианта содержит кириллицу: {en!r}")
    return en


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

# Ревью PRO-66: отсутствующий или пустой каталог — это тихий ноль на сайте
# («0 карт», «0 навыков»), поэтому каждый источник чисел проверяется громко.
_COUNTED_DIRS = (
    ("knowledge/methods", "*.md", "карт методик", "N_MAPS"),
    ("knowledge/methods_en", "*.md", "EN-зеркал карт", "N_MAPS_EN"),
    (".claude/skills", "*/SKILL.md", "навыков", "N_SKILLS"),
    (".claude/agents", "*.md", "субагентов", "N_AGENTS"),
    (".claude/hooks", "*.py", "хуков", "N_HOOKS"),
)


def _count_dir(rel: str, pattern: str, what: str) -> int:
    d = ROOT / rel
    if not d.is_dir():
        raise BuildError(f"Нет каталога {rel} — {what} не посчитать")
    n = len(list(d.glob(pattern)))
    if n == 0:
        raise BuildError(f"В {rel} пусто: нет {what}")
    return n


def repo_numbers() -> dict:
    out = {key: _count_dir(rel, pattern, what)
           for rel, pattern, what, key in _COUNTED_DIRS}
    tests_dir = ROOT / "tests"
    if not tests_dir.is_dir():
        raise BuildError("Нет каталога tests — автотесты не посчитать")
    out["N_TESTS"] = _count_tests(tests_dir)
    return out


def _count_tests(tests_dir: Path) -> int:
    """Число тестовых функций по AST: строковый поиск «def test_» ловит и
    фикстуры-строки в самих тестах (как test_x в test_build_site.py)."""
    import ast

    n = 0
    for p in sorted(tests_dir.glob("test_*.py")):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as e:
            raise BuildError(f"{p}: не парсится — автотесты не посчитать: {e}") from e
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
                n += 1
    if n == 0:
        raise BuildError("В tests пусто: нет автотестов")
    return n


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

    # Red team считается по секциям вариантов: у каждого варианта должен быть
    # пункт списка «Возражения red team» с нумерованными подпунктами «(N)» и строка
    # «Скрытое допущение». Пункт может быть жёстко перенесён: подпункты (2)…(N)
    # оказываются на строках продолжения, поэтому захватываем весь блок до
    # следующего пункта списка / пустой строки — иначе тихое занижение счёта.
    # Отсутствие или испорченный формат — BuildError, а не тихий ноль.
    objections = 0
    assumptions = 0
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(options_md)
        sec = options_md[head.end():end]
        red_lines: list[str] = []
        for ln in sec.splitlines():
            if ln.startswith("- Возражения red team:"):
                red_lines.append(ln)
                continue
            if red_lines:
                # продолжение пункта — только строки с отступом; новый пункт
                # списка, пустая строка или заголовок заканчивают блок
                if not ln.strip() or not ln[:1].isspace() or ln.startswith("## "):
                    break
                red_lines.append(ln)
        if not red_lines:
            raise BuildError(f"Не найдено: строка «Возражения red team» в {options_path}")
        red = "\n".join(red_lines)
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
        "D_LABEL_EN": _label_en(label),
        "REVIEW_RU": f"{review[8:]}.{review[5:7]}.{review[2:4]}",
        "REVIEW_EN": review,
    }


# EN-переводы строковых полей D001 из decisions.jsonl (реестр пишется по-русски).
# Формулировка в реестре изменилась — сборка падает громко, а не показывает
# русский текст на EN-странице. Тот же приём, что D_LABEL_EN_MAP выше.
DEC_EN_MAP = {
    "title": {
        "Коммерческая версия CVStart: hosted freemium SaaS, глобально":
            "CVStart commercial version: hosted freemium SaaS, global",
    },
    "metric": {
        "платящие hosted-беты": "paying users of the hosted beta",
    },
    "commitment": {
        "hosted beta в 3 EN-гео (US/EU)": "hosted beta in 3 EN geos (US/EU)",
    },
    "trigger": {
        "paid < 20 к нед. 12 при activation < 35% -> закрыть коммерческую ветку "
        "(вариант E); падение звёзд GitHub > 30% после анонса облака -> пересобрать "
        "коммуникацию opt-in":
            "if paying users are below 20 by week 12 with activation below 35%, shut "
            "down the commercial track (option E); if GitHub stars fall by more than "
            "30% after the cloud announcement, rework the opt-in communication",
    },
}


def _en_mapped(section: dict, ru: str, what: str) -> str:
    if ru not in section:
        raise BuildError(
            f"Нет EN-перевода для {what}: {ru!r} — добавьте его в DEC_EN_MAP "
            f"в scripts/build_site.py")
    en = section[ru]
    if _CYRILLIC.search(en):
        raise BuildError(f"EN-перевод {what} содержит кириллицу: {en!r}")
    return en


def _date_ru(iso: str) -> str:
    return f"{iso[8:]}.{iso[5:7]}.{iso[2:4]}"


def demo_request() -> dict:
    """Дословный запрос руководителя — второй аргумент `pfs new`, он хранится в
    project.json демо-проекта. Терминал и проза секции демо получают ОДИН токен
    на язык (RQ_RU/RQ_EN), поэтому расхождение формулировок между местами
    невозможно по построению (замечание ревью раунда 3)."""
    pj = DEMO / "project.json"
    if not pj.exists():
        raise BuildError(f"Нет файла: {pj}")
    try:
        data = json.loads(_read(pj))
    except json.JSONDecodeError as e:
        raise BuildError(f"{pj}: не JSON: {e}") from e
    ru = (data.get("question") or "").strip()
    if not ru:
        raise BuildError(f"В {pj} пустой question — дословный запрос не взять")
    en = ("Develop a commercial version of the cvstart.org project (an open-source "
          "AI resume builder and job search: a scan of 129 job boards, AI scoring, "
          "CV Studio, a local pipeline, 19 languages) — resume creation and job "
          "search — and a strategy to take it to market worldwide. "
          "Product: https://cvstart.org/, repository: https://github.com/Fighter90/career-ops-ui")
    if _num_tokens(en) != _num_tokens(ru):
        raise BuildError(
            f"Числа EN-перевода дословного запроса расходятся с {pj.name}: "
            f"{_num_tokens(ru)} != {_num_tokens(en)} — обновите перевод "
            f"в scripts/build_site.py")
    return {"RQ_RU": ru, "RQ_EN": en}


# Карточки фактов рынка на странице demo: (утверждение, RU-значение, EN-значение).
# Значение должно присутствовать в тексте утверждения реестра по числовым
# токенам — реестр изменился, сборка падает громко (тот же приём, что TEXT_EN).
MARKET_FACTS = (
    ("C005", "$1,2–2,4 млрд", "$1.2–2.4B"),
    ("C005", "13,1%", "13.1%"),
    ("C006", "$8–40/мес", "$8–40/mo"),
    ("C008", "98%", "98%"),
    ("C009", "31–74%", "31–74%"),
    ("C011", "$37,97 млрд", "$37.97B"),
)


def market_facts() -> dict:
    claims = {c.get("id"): c for c in _jsonl(DEMO / "claims.jsonl")}
    out: dict = {}
    for i, (cid, ru, en) in enumerate(MARKET_FACTS):
        claim = claims.get(cid)
        if not claim:
            raise BuildError(f"В claims.jsonl нет {cid} — карточка факта рынка не соберётся")
        text = claim.get("text") or ""
        allowed = set(_num_tokens(text))
        for lang, value in (("RU", ru), ("EN", en)):
            missing = set(_num_tokens(value)) - allowed
            if missing:
                raise BuildError(
                    f"Значение карточки рынка {value!r} ({lang}) не сходится с текстом "
                    f"{cid}: лишние числа {sorted(missing)} — обновите MARKET_FACTS "
                    f"или реестр")
        sources = claim.get("sources") or []
        if not sources:
            raise BuildError(f"У {cid} нет источника — карточка факта рынка без цепочки")
        out[f"MF{i}_VALUE"] = ru
        out[f"MF{i}_VALUE_EN"] = en
        out[f"MF{i}_SRC"] = f"{sources[0]} → {cid}"
    return out


# Описание продукта демо на странице demo — текст утверждения C001 из реестра,
# а не пересказ руками. EN-перевод сверяется по числовым токенам (приём TEXT_EN).
PRODUCT_CLAIM = "C001"
PRODUCT_DESC_EN = ("The CVStart product (career-ops UI): a scan of ~129 job boards, "
                   "AI vacancy scoring 0.0–5.0, CV Studio (resume tuning, humanize, "
                   "ATS bullets), PDF/DOCX export, cover letters, a tracker, a job map, "
                   "mock interviews; 100% local; 18 BYOK LLM providers; ~7602 automated "
                   "tests; MIT license")


def product_facts() -> dict:
    claims = {c.get("id"): c for c in _jsonl(DEMO / "claims.jsonl")}
    claim = claims.get(PRODUCT_CLAIM)
    if not claim:
        raise BuildError(f"В claims.jsonl нет {PRODUCT_CLAIM} — описание продукта демо не взять")
    text = (claim.get("text") or "").strip()
    if not text:
        raise BuildError(f"У {PRODUCT_CLAIM} пустой текст")
    if _num_tokens(PRODUCT_DESC_EN) != _num_tokens(text):
        raise BuildError(
            f"Числа EN-перевода {PRODUCT_CLAIM} расходятся с реестром: "
            f"{_num_tokens(text)} != {_num_tokens(PRODUCT_DESC_EN)} — обновите "
            f"PRODUCT_DESC_EN в scripts/build_site.py")
    sources = claim.get("sources") or []
    if not sources:
        raise BuildError(f"У {PRODUCT_CLAIM} нет источника — описание без цепочки")
    return {"PRODUCT": text, "PRODUCT_EN": PRODUCT_DESC_EN, "PRODUCT_SRC": sources[0]}


def decision_details() -> dict:
    """D001 для страницы demo: основания, метрика, обязательство, триггер, пересмотр."""
    d001 = next((d for d in _jsonl(DEMO / "decisions.jsonl") if d.get("id") == "D001"), None)
    if not d001:
        raise BuildError("В decisions.jsonl нет D001")
    title = (d001.get("title") or "").strip()
    if not title:
        raise BuildError("У D001 пустой title")
    grounds = d001.get("grounds") or []
    if not grounds:
        raise BuildError("У D001 нет оснований (grounds) — страница demo без цепочки")
    metrics = d001.get("metrics") or []
    if not metrics or not (metrics[0].get("name") and metrics[0].get("target")):
        raise BuildError("У D001 нет метрики с именем и целью")
    metric = metrics[0]
    commitments = d001.get("commitments") or []
    if not commitments or not (commitments[0].get("what") and commitments[0].get("due")):
        raise BuildError("У D001 нет обязательства (что | когда)")
    commit = commitments[0]
    due_m = re.search(r"(\d{4}-\d{2}-\d{2})", commit.get("due") or "")
    if not due_m:
        raise BuildError(f"В дате обязательства D001 нет ISO-даты: {commit.get('due')!r}")
    triggers = d001.get("review", {}).get("triggers") or []
    if not triggers:
        raise BuildError("У D001 нет триггера пересмотра")

    commit_ru = commit["what"].strip()
    trigger_ru = " ".join(triggers[0].split())
    for what, ru, en in (("обязательства", commit_ru,
                          _en_mapped(DEC_EN_MAP["commitment"], commit_ru, "обязательства")),
                         ("триггера", trigger_ru,
                          _en_mapped(DEC_EN_MAP["trigger"], trigger_ru, "триггера"))):
        if _num_tokens(en) != _num_tokens(ru):
            raise BuildError(
                f"Числа EN-перевода {what} D001 расходятся с реестром: "
                f"{_num_tokens(ru)} != {_num_tokens(en)}")

    return {
        "D_TITLE": title,
        "D_TITLE_EN": _en_mapped(DEC_EN_MAP["title"], title, "заголовка D001"),
        "D_GROUNDS": " · ".join(grounds),
        "D_METRIC": metric["name"].strip(),
        "D_METRIC_EN": _en_mapped(DEC_EN_MAP["metric"], metric["name"].strip(), "метрики D001"),
        "D_TARGET": metric["target"].strip(),
        "D_BY_RU": _date_ru(metric["by"]) if re.match(r"^\d{4}-\d{2}-\d{2}$", metric.get("by") or "")
                   else metric.get("by", ""),
        "D_BY_EN": metric.get("by", ""),
        "D_COMMIT": commit_ru,
        "D_COMMIT_EN": _en_mapped(DEC_EN_MAP["commitment"], commit_ru, "обязательства"),
        "D_DUE_RU": _date_ru(due_m.group(1)),
        "D_DUE_EN": due_m.group(1),
        "D_TRIGGER": trigger_ru,
        "D_TRIGGER_EN": _en_mapped(DEC_EN_MAP["trigger"], trigger_ru, "триггера"),
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


# Число в тексте 03_options.md: цифры, пробельные разделители тысяч («$1 234»)
# и десятичная запятая/точка. Ревью PRO-66: прежний `[\d,]+` молча обрезал
# «$1 234» до «1», поэтому захват идёт целиком и якорится на явный ограничитель
# («/мес», «;», конец строки) — не на «первую не-цифру».
_NUM = r"([0-9][0-9\u00A0\u202F ]*(?:[.,][0-9]+)?)"


def _num_float(raw: str, what: str) -> float:
    """«1 234,50» → 1234.5; непонятный формат — громкий BuildError, не тихая порча."""
    s = raw.strip().replace("\u00A0", "").replace("\u202F", "").replace(" ", "")
    if "," in s:
        if s.count(",") != 1 or "." in s:
            raise BuildError(f"Непонятный формат числа «{what}»: {raw!r}")
        s = s.replace(",", ".")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", s):
        raise BuildError(f"Непонятный формат числа «{what}»: {raw!r}")
    return float(s)


def _num_decimals(raw: str) -> int:
    m = re.search(r"[.,]([0-9]+)\s*$", raw.strip())
    return len(m.group(1)) if m else 0


def _xlsx_values(path: Path) -> list[float]:
    """Все числа кэша значений Excel-приложения (числа считываются из <v> узлов)."""
    if not path.exists():
        raise BuildError(f"Нет Excel-приложения для сверки: {path}")
    import zipfile

    vals: list[float] = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.startswith("xl/worksheets/"):
                continue
            for v in re.findall(r"<v>([^<]+)</v>", z.read(name).decode("utf-8")):
                try:
                    vals.append(float(v.replace(",", ".")))
                except ValueError:
                    continue
    if not vals:
        raise BuildError(f"В {path.name} нет чисел для сверки")
    return vals


def excel_numbers() -> dict:
    md_path = DEMO / "outputs" / "03_options.md"
    md = _read(md_path)
    price = _require(re.search(r"paid \$" + _NUM + r"\s*/мес", md), "цена Pro", md_path)
    cm = _require(re.search(r"CM \$" + _NUM + r"\s*(?:;|$)", md), "вклад на покрытие", md_path)
    ltv = _require(re.search(r"LTV ≈ \$" + _NUM + r"\s*(?:;|$)", md), "LTV", md_path)
    ratio = _require(re.search(r"LTV/CAC ≈ " + _NUM + r"\s*(?:;|$)", md), "LTV/CAC", md_path)
    # Числа на сайте — витрина приложения «Ввод»: сверяем каждое с книгой по
    # точности документа («$272» ↔ 271.88). Расхождение = BuildError (PRO-63),
    # а не тихое расхождение сайта и Excel.
    pairs = (("цена Pro", price), ("вклад на покрытие", cm), ("LTV", ltv), ("LTV/CAC", ratio))
    xl_vals = _xlsx_values(DEMO / "outputs" / "attachments" / "unit_economics.xlsx")
    for what, raw in pairs:
        v = _num_float(raw, what)
        k = _num_decimals(raw)
        if not any(abs(round(x, k) - v) < 1e-9 for x in xl_vals):
            raise BuildError(
                f"«{what}» = {raw.strip()} из 03_options.md не найдено в unit_economics.xlsx "
                f"с точностью {k} знаков — обновите документ или Excel-приложение")
    return {"XL_PRICE": price.strip(), "XL_CM": cm.strip(),
            "XL_LTV": ltv.strip(), "XL_RATIO": ratio.strip()}


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
/* Warm dark v3: warm neutrals, one amber accent, pills, thin lines */
:root{
  --bg:#0B0A09; --bg2:#12100E; --card:#151311; --line:rgba(214,210,204,.10); --line2:rgba(214,210,204,.18);
  --text:#D6D2CC; --strong:#F1EEE9; --muted:#8C877F; --accent:#EE8A3C; --accent-ink:#1A0E05; --pill:#BDB9B3;
  --font:Inter,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:96px}
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

/* fixed pill header */
.nav{position:fixed;top:calc(14px + env(safe-area-inset-top,0px));left:0;right:0;z-index:50}
.nav .bar{position:relative;display:flex;align-items:center;gap:16px;height:56px;padding:0 8px 0 18px;border:1px solid var(--line2);border-radius:18px;background:rgba(11,10,9,.72);backdrop-filter:blur(14px)}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--strong);font-weight:600;font-size:16px;letter-spacing:-.01em;white-space:nowrap}
.brand svg{width:28px;height:28px;flex:none}
.links{display:flex;gap:22px;margin-left:auto;font-size:14px}
.links a{display:inline-flex;align-items:center;min-height:44px;padding:0 2px;text-decoration:none;color:var(--muted)}.links a:hover{color:var(--strong)}
.lang{display:flex;gap:2px;font-size:12px;font-weight:500}
.lang a,.lang b{display:inline-flex;align-items:center;justify-content:center;min-width:44px;min-height:44px;border-radius:10px;text-decoration:none;color:var(--muted)}
.lang b{color:var(--strong);font-weight:500}
.mlink{display:none}
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

/* pill buttons */
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

/* flow: request -> evidence registry -> result */
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

/* comparison with a plain chat */
.cmp{border-top:1px solid var(--line2)}
.cmp .row{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr) minmax(0,1.3fr);gap:24px;padding:20px 0;border-bottom:1px solid var(--line);align-items:baseline}
.cmp .row.hd{padding:12px 0}
.cmp .what{color:var(--strong);font-weight:500}
.cmp .yes{display:flex;gap:10px;align-items:baseline}.cmp .yes::before{content:"";flex:none;width:6px;height:6px;border-radius:50%;background:var(--accent);transform:translateY(-2px)}

/* bento grid of features */
.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px}
.card{grid-column:span 4;min-width:0;padding:26px;border:1px solid var(--line2);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:14px}
.card.w6{grid-column:span 6}.card.w8{grid-column:span 8}
.card .ic{width:36px;height:36px;border-radius:10px;border:1px solid var(--line2);display:flex;align-items:center;justify-content:center;color:var(--accent)}
.card .ic svg{width:18px;height:18px}
.card p{margin:0;color:var(--muted);font-size:15px}
.faqlist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.faqlist li{list-style:none;padding:10px 12px;border-radius:10px;background:var(--bg2);font-size:14px}
.faqlist b{color:var(--accent);font-weight:500;margin-right:8px}

/* process */
.phases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.ph{padding:22px;border:1px solid var(--line2);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:12px;min-width:0}
.ph ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.ph li{display:flex;align-items:center;gap:12px;font-size:15px}
.ph .n{flex:none;width:28px;height:28px;border-radius:50%;border:1px solid var(--line2);display:inline-flex;align-items:center;justify-content:center;font-size:12px;color:var(--muted)}
.ph li.h .n{border:1.5px solid var(--accent);color:var(--accent)}
/* badge on human-decision steps: the text comes from a per-language token to avoid leaks */
.ph li.h::after{content:"{{YOU}}";margin-left:auto;font-size:11px;color:var(--accent);letter-spacing:.08em;text-transform:uppercase}

/* evidence chain: terminal, claim, excel */
.proof{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:24px;align-items:start}
.proof-side{display:flex;flex-direction:column;gap:16px;min-width:0}
.term{border:1px solid var(--line2);border-radius:18px;background:#0D0C0A;overflow:hidden;min-width:0}
.term .bar{display:flex;gap:6px;padding:12px 16px;border-bottom:1px solid var(--line)}
.term .bar i{width:10px;height:10px;border-radius:50%;background:var(--line2)}
.term pre{margin:0;padding:18px 20px;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--text)}
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

/* architecture */
.stack{display:flex;flex-direction:column;max-width:760px;margin:0 auto;width:100%}
.layer{position:relative;display:flex;gap:16px;align-items:flex-start;padding:20px 24px;border:1px solid var(--line2);border-radius:16px;background:var(--card);min-width:0}
.layer+.layer{margin-top:26px}
.layer+.layer::before{content:"";position:absolute;left:50%;top:-27px;width:1px;height:26px;background:linear-gradient(180deg,var(--accent),var(--line2))}
.layer .n{flex:none;width:34px;height:34px;border-radius:10px;border:1px solid var(--line2);display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:13px}
.layer b{display:block;color:var(--strong);font-weight:500;font-size:16px;margin-bottom:4px}
.layer small{color:var(--muted);font-size:14px;line-height:1.5;display:block}

/* demo */
.demo{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line2);border:1px solid var(--line2);border-radius:18px;overflow:hidden;margin:0}
.stats div{background:var(--card);padding:22px;display:flex;flex-direction:column-reverse;gap:6px}
.stats b{font-size:30px;font-weight:500;color:var(--strong);letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.stats span{font-size:13px;color:var(--muted)}

/* install */
.inst{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:40px;align-items:start}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.cmd{display:flex;align-items:center;gap:10px;padding:6px 6px 6px 16px;border:1px solid var(--line2);border-radius:14px;background:var(--card)}
.cmd code{flex:1;min-width:0;overflow-x:auto;white-space:nowrap;font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--strong)}
.copy{flex:none;min-height:44px;padding:0 14px;border-radius:999px;border:1px solid var(--line2);background:transparent;color:var(--text);font:500 13px var(--font);cursor:pointer}
.copy:hover{border-color:var(--accent)}
blockquote{margin:6px 0 0;padding:18px 20px;border-radius:14px;background:var(--card);border:1px solid var(--line2);color:var(--strong)}

/* faq */
.faq{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px}
/* accordion styles are scoped to the FAQ section: the header details (mlink) is styled separately */
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;min-height:64px;padding:12px 0;color:var(--strong);font-size:18px;font-weight:500}
.faq summary::-webkit-details-marker{display:none}
.faq summary .pm{flex:none;width:30px;height:30px;border-radius:50%;border:1px solid var(--line2);display:inline-flex;align-items:center;justify-content:center;color:var(--accent);transition:transform .2s}
.faq details[open] summary .pm{transform:rotate(45deg)}
.faq details p{margin:0 0 22px;color:var(--muted);max-width:44em}

/* final CTA and footer */
.final{position:relative;overflow:hidden;text-align:center;border-bottom:0}
.final .box{position:relative;margin:0 auto;max-width:980px;padding:80px 28px;border:1px solid rgba(238,138,60,.4);border-radius:28px;background:radial-gradient(ellipse at 50% 0%,rgba(238,138,60,.16),rgba(11,10,9,0) 60%),var(--bg2);display:flex;flex-direction:column;align-items:center;gap:22px}
.procfig{margin:44px auto 0;max-width:760px}
.dosfig{margin:0 auto;width:100%;max-width:520px}
.procfig img,.dosfig img{display:block;width:100%;height:auto;border-radius:20px;border:1px solid var(--line2)}
footer{border-top:1px solid var(--line);padding:36px 0 calc(36px + env(safe-area-inset-bottom,0px));font-size:14px;color:var(--muted)}
footer .wrap{display:flex;flex-wrap:wrap;gap:20px;justify-content:space-between;align-items:center}
footer nav{display:flex;flex-wrap:wrap;gap:18px}footer a{text-decoration:none}footer nav a{display:inline-flex;align-items:center;min-height:44px;padding:0 2px}footer a:hover{color:var(--strong)}

/* subpages (demo, help, materials): same system, hero without video */
.subhero{padding:170px 0 72px;text-align:center;border-bottom:1px solid var(--line)}
.subhero .inner{position:relative;display:flex;flex-direction:column;align-items:center;gap:20px}
.subhero p.lead{max-width:44em;margin:0;color:var(--text);font-size:18px}
.links b{display:inline-flex;align-items:center;min-height:44px;padding:0 2px;color:var(--strong);font-weight:500}
p code,li code,dt code,dd code,blockquote code{font:500 .9em ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--strong);background:var(--bg2);border:1px solid var(--line2);border-radius:6px;padding:1px 6px}
.coverfig{margin:56px auto 0;max-width:980px}
.coverfig img{display:block;width:100%;height:auto;border-radius:20px;border:1px solid var(--line2)}

/* demo page: facts, options, decision */
.mgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.mcard{padding:24px;border:1px solid var(--line2);border-radius:18px;background:var(--card);display:flex;flex-direction:column;gap:10px;min-width:0}
.mcard b{font-size:24px;font-weight:500;color:var(--strong);letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.mcard span{color:var(--muted);font-size:14px;line-height:1.5}
.mcard i{font-style:normal;font-size:12px;color:var(--accent);letter-spacing:.04em}
.rows{border-top:1px solid var(--line2)}
.rows .row{display:grid;grid-template-columns:minmax(0,.72fr) minmax(0,1.28fr);gap:24px;padding:18px 0;border-bottom:1px solid var(--line);align-items:baseline}
.rows .row b{color:var(--strong);font-weight:500;font-size:16px}
.rows .row p{margin:0;color:var(--muted);font-size:15px}
.shots{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.shot{margin:0;border:1px solid var(--line2);border-radius:18px;background:var(--card);padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.shot img{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--line)}
.shot figcaption{color:var(--muted);font-size:13px;line-height:1.5}
.sixlist{display:grid;gap:8px;max-width:760px;margin:0 auto}
.sixlist li{list-style:none;display:flex;gap:14px;align-items:baseline;padding:12px 16px;border:1px solid var(--line);border-radius:12px;background:var(--bg2);font-size:14px;color:var(--muted)}
.sixlist b{flex:none;color:var(--accent);font-weight:500;min-width:64px}

@media (max-width:980px){
  .links{display:none}
  .mlink{display:block}
  .nav .bar{padding-right:6px}
  .flow{grid-template-columns:minmax(0,1fr);gap:14px}.core{margin:6px 0}
  .col.in .node::after,.col.out .node::before{display:none}
  .card,.card.w6,.card.w8{grid-column:1/-1}
  .phases{grid-template-columns:repeat(2,minmax(0,1fr))}
  .proof,.demo,.inst,.faq{grid-template-columns:minmax(0,1fr)}
  .mgrid,.shots{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:640px){
  section{padding:80px 0}
  .hero{min-height:640px;padding:130px 0 80px}
  .subhero{padding:140px 0 56px}
  .phases,.faqlist,.mgrid,.shots{grid-template-columns:minmax(0,1fr)}
  .cmp .row,.rows .row{grid-template-columns:minmax(0,1fr);gap:4px}.cmp .row.hd{display:none}
  .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
  .facts span{border-left:0;padding:2px 10px}
  .nav .bar{gap:8px}
  .bar .pill{display:none}
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
  document.querySelectorAll('details:not(.mlink)').forEach(function(d){
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

# Общий блок hreflang собирается по паре URL конкретной страницы (RU и EN
# варианты могут жить в разных каталогах: /demo.html ↔ /en/demo.html)
def _hreflangs(ru_url: str, en_url: str) -> str:
    return (f'<link rel="alternate" hreflang="ru" href="{ru_url}">\n'
            f'<link rel="alternate" hreflang="en" href="{en_url}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{ru_url}">')


def _page(lang_attrs: str, title: str, desc: str, canonical: str, hreflangs: str,
          og: str, body: str, tokens: dict) -> str:
    head = f"""<!doctype html>
<html lang="{lang_attrs}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{hreflangs}
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
    # шунт PRO-66: {{BRAND}} в body мог не замениться из-за порядка ключей маппинга
    body = body.replace("{{BRAND}}", BRAND_SVG)
    full = head + body + tail
    mapping = {"CSS": CSS, "JS": JS, "YM": tokens.pop("YM", "")}
    mapping.update(tokens)
    return render(full, mapping)


# Ключи, значения которых — уже готовая разметка/скрипты и не подлежат экранированию.
# Всё остальное (числа, TEXT/SEG/RQ, C_DOM/path, D_LABEL, USAGE, даты, KIND, A…) —
# пользовательские данные репозитория: экранируются html.escape.
RAW_KEYS = frozenset({"CSS", "JS", "YM", "BRAND", "NAV"})


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
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div>
        <h3>Данные и когорты</h3>
        <p>Профиль таблицы, когорты удержания, воронки и статистика — расчёты сохраняются и повторяются одной командой.</p>
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
        <pre><span class="p">$</span> pfs new "CVStart: платная версия" "{{{{RQ}}}}"
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
      <p>Задача руководителя дословно: «{{{{RQ}}}}» Числа — из проекта, не руками.</p>
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
      <article class="card">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div>
        <h3>Data and cohorts</h3>
        <p>Table profiles, retention cohorts, funnels and statistics — calculations are saved and rerun with one command.</p>
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
        <pre><span class="p">$</span> pfs new "CVStart: paid version" "{{{{RQ}}}}"
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
      <p>The product lead’s request, word for word: “{{{{RQ}}}}” Numbers come from the project, not from hands.</p>
      <div><a class="pill pill-b pill-sm" href="demo.html" data-goal="cta_demo_click">Open the walkthrough{ARROW}</a></div>
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
    <nav aria-label="Links"><a href="https://github.com/Fighter90/product-factory-strategist">GitHub</a><a href="help.html">Help</a><a href="materials.html">Demo materials</a><a href="https://github.com/Fighter90/product-factory-strategist/blob/main/CHANGELOG.md">Changelog</a></nav>
    <span>MIT · open source</span>
  </div>
</footer>
"""


# ---------------- подстраницы: demo, help, materials ----------------
# Решение раунда ревью 3: раздел структуры PRO-66 требует эти страницы «в той же
# системе» — они собираются тем же CSS, шапкой-пилюлей и токенами репозитория.
# RU в корне, EN в /en/; отдельный язык на файл вместо старого переключателя
# setLang (у каждой страницы свой canonical и hreflang-пара).

_SUB_LINKS = ("how", "features", "demo", "help", "materials")
_SUB_HREFS = {"how": "index.html#how", "features": "index.html#features",
              "demo": "demo.html", "help": "help.html", "materials": "materials.html"}
_SUB_LABELS = {
    "ru": {"how": "Как работает", "features": "Возможности", "demo": "Демо",
           "help": "Справка", "materials": "Материалы", "cta": "Запустить",
           "brand": "Стратег", "brand_label": "Стратег Фабрики продуктов — на главную",
           "nav_label": "Разделы", "menu_label": "Меню разделов"},
    "en": {"how": "How it works", "features": "Features", "demo": "Demo",
           "help": "Help", "materials": "Materials", "cta": "Start",
           "brand": "Strategist", "brand_label": "Product Factory Strategist — home",
           "nav_label": "Sections", "menu_label": "Sections menu"},
}


def _subnav(lang: str, current: str, pair: str) -> str:
    """Шапка-пилюля подстраницы: ссылки на разделы лендинга и соседние страницы,
    парный переключатель языка, CTA на установку. current — ключ активного пункта."""
    t = _SUB_LABELS[lang]
    other = "en" if lang == "ru" else "ru"
    links: list[str] = []
    panel: list[str] = []
    for key in _SUB_LINKS:
        label = t[key]
        href = _SUB_HREFS[key]
        if key == current:
            links.append('<b aria-current="page">{0}</b>'.format(label))
            panel.append('<a href="{0}" aria-current="page">{1}</a>'.format(href, label))
        else:
            links.append('<a href="{0}">{1}</a>'.format(href, label))
            panel.append('<a href="{0}">{1}</a>'.format(href, label))
    return f"""<header class="nav">
  <div class="wrap">
    <div class="bar">
      <a class="brand" href="index.html" aria-label="{t['brand_label']}">
        {BRAND_SVG}
        {t['brand']}
      </a>
      <nav class="links" aria-label="{t['nav_label']}">{''.join(links)}</nav>
      <div class="lang"><b aria-current="true">{lang.upper()}</b><a href="{pair}" hreflang="{other}" data-goal="lang_switch">{other.upper()}</a></div>
      <a class="pill pill-a pill-sm" href="index.html#install" data-goal="cta_install_click">{t['cta']}{ARROW}</a>
      <details class="mlink">
        <summary aria-label="{t['menu_label']}"><span class="b" aria-hidden="true"></span></summary>
        <nav class="mlink-panel" aria-label="{t['nav_label']}">{''.join(panel)}</nav>
      </details>
    </div>
  </div>
</header>"""


FOOTER_SUB_RU = """<footer>
  <div class="wrap">
    <span style="color:var(--strong);font-weight:500">Стратег Фабрики продуктов</span>
    <nav aria-label="Ссылки"><a href="https://github.com/Fighter90/product-factory-strategist">GitHub</a><a href="help.html">Справка</a><a href="materials.html">Материалы демо</a><a href="https://github.com/Fighter90/product-factory-strategist/blob/main/CHANGELOG.md">Changelog</a></nav>
    <span>MIT · открытый код</span>
  </div>
</footer>
"""

FOOTER_SUB_EN = """<footer>
  <div class="wrap">
    <span style="color:var(--strong);font-weight:500">Product Factory Strategist</span>
    <nav aria-label="Links"><a href="https://github.com/Fighter90/product-factory-strategist">GitHub</a><a href="help.html">Help</a><a href="materials.html">Demo materials</a><a href="https://github.com/Fighter90/product-factory-strategist/blob/main/CHANGELOG.md">Changelog</a></nav>
    <span>MIT · open source</span>
  </div>
</footer>
"""

# Ссылки на документы демо-проекта в GitHub (обе языковые версии страницы
# ведут на одни и те же файлы реестра — они двуязычные или языко-нейтральные).
GH = "https://github.com/Fighter90/product-factory-strategist"
GH_RAW = "https://raw.githubusercontent.com/Fighter90/product-factory-strategist/main"
DEMO_DIR = f"{GH}/blob/main/projects/%D0%B4%D0%B5%D0%BC%D0%BE"
DEMO_RAW = f"{GH_RAW}/projects/%D0%B4%D0%B5%D0%BC%D0%BE"

DEMO_BODY_RU = f"""
<a class="skip" href="#main">К содержимому</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Демо-проект · шаги 1–12</div>
    <h1 id="h1">CVStart: <span class="acc">от запроса руководителя</span> до решения с обязательствами</h1>
    <p class="lead">Сквозной прогон агента на живом open-source продукте cvstart.org: бриф, рынок resume builders, варианты с red team, six-pager RU и EN с четырьмя книгами Excel и решение D001. Все числа на странице — из файлов проекта, не руками.</p>
    <div class="facts"><span><b>{{{{D_SOURCES}}}}</b> источников</span><span><b>{{{{D_CLAIMS}}}}</b> утверждений</span><span>варианты <b>A–{{{{D_OPT_LAST}}}}</b></span><span><b>{{{{D_OBJ}}}} + {{{{D_ASM}}}}</b> ударов red team</span></div>
    <div class="ctas">
      <a class="pill pill-b" href="#brief">Задание руководителя{ARROW}</a>
      <a class="pill pill-a" href="materials.html" data-goal="cta_demo_click">Материалы прогона{ARROW}</a>
    </div>
    <figure class="coverfig">
      <picture>
        <source type="image/avif" srcset="{{{{A}}}}assets/dark-hero-paper.avif">
        <img src="{{{{A}}}}assets/dark-hero-paper.webp" width="1800" height="1012" alt="Тёмная бумага с рассыпанными частицами и янтарной нитью — обложка демо-разбора" loading="lazy" decoding="async">
      </picture>
    </figure>
  </div>
</section>

<section id="brief" aria-labelledby="brief-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Задание</div>
      <h2 id="brief-h">Задача руководителя <span class="acc">дословно</span></h2>
      <p>Второй аргумент pfs new — запрос без пересказа. Из него агент собирает бриф, показывает его на подтверждение и дальше работает по шагам 1–12.</p>
    </div>
    <div class="term" aria-label="Создание демо-проекта" style="max-width:760px;margin:0 auto">
      <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
      <pre><span class="p">$</span> pfs new "CVStart: платная версия" "{{{{RQ}}}}"
<span class="hi">Создан projects/демо · сценарий: вывод на рынок · дальше: intake</span></pre>
    </div>
    <div class="claim" style="max-width:760px;margin:24px auto 0">
      <div class="tags"><span class="tag a">шаг 1 · intake</span><span class="tag">00_brief.md</span></div>
      <p>Задача руководителя дословно: «{{{{RQ}}}}» Решение по результату брифа — выбор стратегии коммерциализации и глобального GTM. Ось сравнения: рост платящих подписчиков и ARR. Ограничения: open-source core остаётся MIT, соло-разработчик, доверие локального режима не ломается.</p>
    </div>
  </div>
</section>

<section id="product" aria-labelledby="product-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Продукт демо</div>
      <h2 id="product-h">Живой open-source продукт, <span class="acc">а не выдуманная витрина</span></h2>
      <p>{{{{PRODUCT}}}} Источник: {{{{PRODUCT_SRC}}}} · скриншоты продукта — из репозитория демо-проекта.</p>
    </div>
    <div class="shots">
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_ru.jpg" width="960" height="1600" alt="Лендинг cvstart.org в русской локали" loading="lazy" decoding="async"><figcaption>Лендинг в русской локали: позиционирование бесплатности, скан джоб-бордов, языки интерфейса.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_en.jpg" width="960" height="1600" alt="Лендинг cvstart.org в английской локали" loading="lazy" decoding="async"><figcaption>Тот же лендинг в английской локали — одна кодовая база, языковые версии с hreflang: отсюда волны локалей в стратегии.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_ru.jpg" width="1600" height="1000" alt="Дашборд поиска работы cvstart.org в русской локали" loading="lazy" decoding="async"><figcaption>Дашборд поиска работы: AI-скоринг вакансий против резюме — ядро продукта и точка входа в CV Studio.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_en.jpg" width="1600" height="1000" alt="Дашборд поиска работы cvstart.org в английской локали" loading="lazy" decoding="async"><figcaption>Английская версия дашборда: fit-скоринг против резюме, фильтры по джоб-бордам.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_map_en.jpg" width="1600" height="1487" alt="Карта вакансий cvstart.org" loading="lazy" decoding="async"><figcaption>Карта вакансий: география предложений поверх скана джоб-бордов.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_tracker_en.jpg" width="1600" height="1000" alt="Трекер заявок cvstart.org" loading="lazy" decoding="async"><figcaption>Трекер заявок с follow-up: воронка откликов удерживает пользователя между сессиями поиска.</figcaption></figure>
    </div>
  </div>
</section>

<section id="run" aria-labelledby="run-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Как работал агент</div>
      <h2 id="run-h">Двенадцать шагов. <span class="acc">Три решения за вами.</span></h2>
      <p>Агент вёл сам, останавливаясь только там, где решает человек: подтверждение брифа (шаг 1), выбор варианта (шаг 7), утверждение решения (шаг 11). Состояние — в файлах проекта, поэтому перерывы и смена среды не теряют работу.</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Исследовать</h3><ol><li class="h"><span class="n">1</span>Бриф</li><li><span class="n">2</span>Источники</li><li><span class="n">3</span>Исследование</li><li><span class="n">4</span>Сегменты</li></ol></div>
      <div class="ph"><h3>Определить</h3><ol><li><span class="n">5</span>Картина ситуации</li><li><span class="n">6</span>Варианты и red team</li><li class="h"><span class="n">7</span>Выбор</li></ol></div>
      <div class="ph"><h3>Разработать</h3><ol><li><span class="n">8</span>Стратегии</li><li><span class="n">9</span>План проверки</li><li><span class="n">10</span>Ревью качества</li></ol></div>
      <div class="ph"><h3>Довести</h3><ol><li class="h"><span class="n">11</span>Решение</li><li><span class="n">12</span>Мониторинг</li></ol></div>
    </div>
    <div class="rows" style="margin-top:44px">
      <div class="row"><b>Шаги 1–4 · исследовать</b><p>бриф с подтверждением, {{{{D_SOURCES}}}} источников без запрещённых доменов, {{{{D_CLAIMS}}}} утверждений с типом и силой, сегменты и персоны-гипотезы из синтетики.</p></div>
      <div class="row"><b>Шаги 5–7 · определить</b><p>картина ситуации с пробелами, варианты A–{{{{D_OPT_LAST}}}} со статус-кво и закрытием, red team: {{{{D_OBJ}}}} возражений и {{{{D_ASM}}}} скрытых допущений, выбор человека.</p></div>
      <div class="row"><b>Шаги 8–10 · разработать</b><p>продуктовая и коммуникационная стратегии, план проверки с порогами, независимое ревью качества, six-pager RU и EN с книгами Excel.</p></div>
      <div class="row"><b>Шаги 11–12 · довести</b><p>решение D001 с основаниями и датой пересмотра, мониторинг обязательств остаётся открытым после прогона.</p></div>
    </div>
  </div>
</section>

<section id="market" aria-labelledby="market-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Что нашёл</div>
      <h2 id="market-h">Рынок в цифрах <span class="acc">с источниками</span></h2>
      <p>Каждое число реестра — с типом, силой A–D и источником. Значения карточек сверяются с текстами утверждений при каждой сборке: реестр изменился — сборка падает, а не показывает устаревшее.</p>
    </div>
    <div class="mgrid">
      <article class="mcard"><b>{{{{MF0_VALUE}}}}</b><span>рынок resume builders, 2024–2025; оценки агрегаторов расходятся вдвое — рынок записан диапазонами</span><i>{{{{MF0_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF1_VALUE}}}}</b><span>CAGR AI-подсегмента resume builders — рост именно там, где CVStart</span><i>{{{{MF1_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF2_VALUE}}}}</b><span>семь прямых конкурентов (Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal, Rezi) — freemium с агрессивными автопродлениями</span><i>{{{{MF2_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF3_VALUE}}}}</b><span>компаний Fortune 500 используют ATS — резюме фильтрует робот до человека</span><i>{{{{MF3_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF4_VALUE}}}}</b><span>соискателей применяют AI в поиске работы — разброс опросов, записанный диапазоном</span><i>{{{{MF4_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF5_VALUE}}}}</b><span>мировой рынок онлайн-рекрутинга — база для расчёта адресуемого рынка</span><i>{{{{MF5_SRC}}}}</i></article>
    </div>
    <div class="claim" style="margin-top:24px">
      <div class="tags"><span class="tag">гипотеза · синтез, не факт</span></div>
      <p>Незанятая ниша — гипотеза [C013]: мультиязычный приватный AI-резюме-билдер с открытым кодом при западных конкурентах на английском и пяти языках. Персоны-гипотезы и воронка беты помечены origin=synthetic — это гипотезы и метод-иллюстрация, не доказанный спрос.</p>
    </div>
  </div>
</section>

<section id="options" aria-labelledby="options-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Шаги 6–7</div>
      <h2 id="options-h">Варианты и red team: <span class="acc">пять путей, ни одного тихого</span></h2>
      <p>Минимум три содержательно разных варианта, включая «оставить как есть» и «закрыть». Отдельный субагент атакует каждый; удары встроены в митигации и пороги плана проверки. Полная таблица с экономикой — в <a href="{DEMO_DIR}/outputs/03_options.md" target="_blank" rel="noopener">03_options.md</a>.</p>
    </div>
    <div class="rows">
      <div class="row"><b>A · статус-кво</b><p>бесплатный open-source без изменений. Удар red team: «дорогое хобби» — лицензия MIT позволяет форку монетизировать ваш труд.</p></div>
      <div class="row"><b>B · hosted freemium SaaS <span style="color:var(--accent)">← выбран</span></b><p>тиры Free (BYOK) / Pro / Unlimited, opt-in облако при локальном MIT-core, честный прайсинг без автопродлений, волны локалей. Удар: доверие сообщества к коммерциализации — митигации: BYOK-free, opt-in, честный прайсинг, пороги остановки.</p></div>
      <div class="row"><b>C · B2B white-label</b><p>хостинг резюме-билдера под брендом партнёра. Удар: у соло-разработчика нет продаж-компетенции — отложен.</p></div>
      <div class="row"><b>D · dual-license</b><p>платная коммерческая лицензия поверх open-source. Удар: юридически не работает поверх MIT — отклонён.</p></div>
      <div class="row"><b>E · закрыть коммерцию</b><p>продукт остаётся бесплатным OSS-проектом. Удар: отказ от актива на растущем рынке.</p></div>
    </div>
    <div class="claim" style="margin-top:24px">
      <div class="tags"><span class="tag a">выбор · шаг 7</span><span class="tag">вариант {{{{D_LETTER}}}} · {{{{D_LABEL}}}}</span></div>
      <p>Рекомендация агента — не «лучший вариант вообще», а лучший при ограничениях руководителя: MIT-core сохраняется, соло-ресурсы, доверие локального режима не ломается. Осознанные отказы: C — нет продаж-компетенции; D — не работает поверх MIT; E — отказ от растущего рынка; A — форк монетизирует труд.</p>
    </div>
  </div>
</section>

<section id="decision" aria-labelledby="decision-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Шаг 11 · решение</div>
      <h2 id="decision-h">D001: <span class="acc">{{{{D_TITLE}}}}</span></h2>
      <p>Решение фиксируется с основаниями, метрикой, обязательством, триггером пересмотра и датой — <code>pfs decision add</code> записывает его в decisions.jsonl, и дальше следят <code>pfs next</code> и <code>pfs decision due</code>.</p>
    </div>
    <div class="claim">
      <div class="tags"><span class="tag a">D001</span><span class="tag">основания: {{{{D_GROUNDS}}}}</span></div>
      <p>Метрика: {{{{D_METRIC}}}} — цель {{{{D_TARGET}}}} к {{{{D_BY_RU}}}}. Обязательство: {{{{D_COMMIT}}}} — к {{{{D_DUE}}}}. Пересмотр решения: {{{{REVIEW}}}}. Триггер: {{{{D_TRIGGER}}}}.</p>
    </div>
  </div>
</section>

<section id="econ" aria-labelledby="econ-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Экономика</div>
      <h2 id="econ-h">Юнит-математика платящего <span class="acc">в живых формулах</span></h2>
      <p>Юнит-допущения демо — [C016]; значения на листе «Ввод» книги unit_economics.xlsx можно поменять — формулы пересчитаются.</p>
    </div>
    <div class="xl" style="max-width:560px">
      <div class="label" style="margin-bottom:10px">Excel · лист «Ввод»</div>
      <table>
        <tr><td>Цена Pro</td><td>${{{{XL_PRICE}}}}/мес</td></tr>
        <tr><td>Переменные 25% → вклад на покрытие</td><td>${{{{XL_CM}}}}</td></tr>
        <tr><td>LTV</td><td>≈ ${{{{XL_LTV}}}}</td></tr>
        <tr><td>LTV / CAC</td><td>≈ {{{{XL_RATIO}}}}</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="sixpager" aria-labelledby="six-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Документ для комитета</div>
      <h2 id="six-h">Six-pager RU и EN <span class="acc">с книгами Excel</span></h2>
      <p>Отчёт в структуре FAQ-1…6: рынок, сегменты, варианты с red team, тактики, план и KPI. Числа прослеживаются до утверждений реестра; все форматы — на странице материалов.</p>
    </div>
    <ul class="sixlist">
      <li><b>FAQ-1</b><span>рынок и тренды: размер и коридоры оценок, ATS-гейт найма, подписочная усталость</span></li>
      <li><b>FAQ-2</b><span>сегменты, персоны и барьеры — гипотезы, проверяемые в бете</span></li>
      <li><b>FAQ-3</b><span>варианты A–{{{{D_OPT_LAST}}}} с возражениями red team и выбором {{{{D_LETTER}}}}</span></li>
      <li><b>FAQ-4</b><span>матрица тактик: BYOK-free, честная страница цены, CV Studio, трекер с follow-up</span></li>
      <li><b>FAQ-5</b><span>план: 90-дневная бета с порогами продолжить / изменить / остановить</span></li>
      <li><b>FAQ-6</b><span>KPI в двух плоскостях: бизнес и продукт</span></li>
    </ul>
    <div class="ctas" style="margin-top:28px;justify-content:center">
      <a class="pill pill-a" href="materials.html" data-goal="cta_demo_click">Открыть материалы{ARROW}</a>
      <a class="pill pill-b" href="{DEMO_RAW}/outputs/SIX_PAGER_RU.pdf" target="_blank" rel="noopener">SIX_PAGER_RU.pdf{ARROW}</a>
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
      <div class="eyebrow">Прогон занял один вечер человека</div>
      <h2 id="fin-h">Повторите на <span class="acc">своей задаче</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Установите агента и опишите свою задачу как есть — бриф, варианты и решение соберутся по тем же шагам 1–12.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Установить{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_RU}"""

DEMO_BODY_EN = f"""
<a class="skip" href="#main">Skip to content</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Demo project · steps 1–12</div>
    <h1 id="h1">CVStart: <span class="acc">from a product lead’s request</span> to a decision with commitments</h1>
    <p class="lead">An end-to-end run of the agent on a live open-source product, cvstart.org: a brief, the resume-builder market, red-teamed options, a RU and EN six-pager with four Excel workbooks, and decision D001. Every number on this page comes from the project files, not from hands.</p>
    <div class="facts"><span><b>{{{{D_SOURCES}}}}</b> sources</span><span><b>{{{{D_CLAIMS}}}}</b> claims</span><span>options <b>A–{{{{D_OPT_LAST}}}}</b></span><span><b>{{{{D_OBJ}}}} + {{{{D_ASM}}}}</b> red-team hits</span></div>
    <div class="ctas">
      <a class="pill pill-b" href="#brief">The brief{ARROW}</a>
      <a class="pill pill-a" href="materials.html" data-goal="cta_demo_click">Run materials{ARROW}</a>
    </div>
    <figure class="coverfig">
      <picture>
        <source type="image/avif" srcset="{{{{A}}}}assets/dark-hero-paper.avif">
        <img src="{{{{A}}}}assets/dark-hero-paper.webp" width="1800" height="1012" alt="Dark paper scattered with particles and an amber thread — the cover of the demo walkthrough" loading="lazy" decoding="async">
      </picture>
    </figure>
  </div>
</section>

<section id="brief" aria-labelledby="brief-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The brief</div>
      <h2 id="brief-h">The product lead’s task, <span class="acc">word for word</span></h2>
      <p>The second argument of pfs new is the request without paraphrasing. The agent turns it into a brief, shows it for approval and then runs steps 1–12.</p>
    </div>
    <div class="term" aria-label="Creating the demo project" style="max-width:760px;margin:0 auto">
      <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
      <pre><span class="p">$</span> pfs new "CVStart: paid version" "{{{{RQ}}}}"
<span class="hi">Created the demo project · scenario: go-to-market · next: intake</span></pre>
    </div>
    <div class="claim" style="max-width:760px;margin:24px auto 0">
      <div class="tags"><span class="tag a">step 1 · intake</span><span class="tag">00_brief.md</span></div>
      <p>The product lead’s request, word for word: “{{{{RQ}}}}” The decision the brief targets: pick a commercialization strategy and a global go-to-market plan. Comparison axis: growth in paying subscribers and ARR. Constraints: the open-source core stays MIT, a solo developer, and trust in the local mode is preserved.</p>
    </div>
  </div>
</section>

<section id="product" aria-labelledby="product-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The product in this demo</div>
      <h2 id="product-h">A live open-source product, <span class="acc">not a staged showcase</span></h2>
      <p>{{{{PRODUCT}}}} Source: {{{{PRODUCT_SRC}}}} · product screenshots come from the demo project repository.</p>
    </div>
    <div class="shots">
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_ru.jpg" width="960" height="1600" alt="cvstart.org landing page in the Russian locale" loading="lazy" decoding="async"><figcaption>The landing page in the Russian locale: free-to-use positioning, job-board scanning, interface languages.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_en.jpg" width="960" height="1600" alt="cvstart.org landing page in the English locale" loading="lazy" decoding="async"><figcaption>The same landing page in the English locale — one codebase, language versions with hreflang: hence the locale waves in the strategy.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_ru.jpg" width="1600" height="1000" alt="cvstart.org job-search dashboard in the Russian locale" loading="lazy" decoding="async"><figcaption>The job-search dashboard: AI vacancy scoring against your resume — the core of the product and the entry point into CV Studio.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_en.jpg" width="1600" height="1000" alt="cvstart.org job-search dashboard in the English locale" loading="lazy" decoding="async"><figcaption>The English version of the dashboard: fit scoring against your resume, job-board filters.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_map_en.jpg" width="1600" height="1487" alt="cvstart.org job map" loading="lazy" decoding="async"><figcaption>The job map: offer geography on top of the job-board scan.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_tracker_en.jpg" width="1600" height="1000" alt="cvstart.org application tracker" loading="lazy" decoding="async"><figcaption>The application tracker with follow-ups: the application funnel keeps users engaged between job-search sessions.</figcaption></figure>
    </div>
  </div>
</section>

<section id="run" aria-labelledby="run-h">
  <div class="wrap">
    <div class="head">
      <div class="label">How the agent worked</div>
      <h2 id="run-h">Twelve steps. <span class="acc">Three decisions are yours.</span></h2>
      <p>The agent drove the work on its own, stopping only where a human decides: confirming the brief (step 1), choosing an option (step 7), approving the decision (step 11). The state lives in project files, so breaks and tool changes lose nothing.</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Research</h3><ol><li class="h"><span class="n">1</span>Brief</li><li><span class="n">2</span>Sources</li><li><span class="n">3</span>Research</li><li><span class="n">4</span>Segments</li></ol></div>
      <div class="ph"><h3>Define</h3><ol><li><span class="n">5</span>Situation</li><li><span class="n">6</span>Options and red team</li><li class="h"><span class="n">7</span>Choice</li></ol></div>
      <div class="ph"><h3>Develop</h3><ol><li><span class="n">8</span>Strategies</li><li><span class="n">9</span>Validation plan</li><li><span class="n">10</span>Quality review</li></ol></div>
      <div class="ph"><h3>Deliver</h3><ol><li class="h"><span class="n">11</span>Decision</li><li><span class="n">12</span>Monitoring</li></ol></div>
    </div>
    <div class="rows" style="margin-top:44px">
      <div class="row"><b>Steps 1–4 · research</b><p>an approved brief, {{{{D_SOURCES}}}} sources with no blocked domains, {{{{D_CLAIMS}}}} claims with type and grade, segments and persona hypotheses from synthetic interviews.</p></div>
      <div class="row"><b>Steps 5–7 · define</b><p>a situation with honest gaps, options A–{{{{D_OPT_LAST}}}} including status quo and shut-down, a red team with {{{{D_OBJ}}}} objections and {{{{D_ASM}}}} hidden assumptions, the human choice.</p></div>
      <div class="row"><b>Steps 8–10 · develop</b><p>product and communication strategies, a validation plan with thresholds, an independent quality review, a RU and EN six-pager with Excel workbooks.</p></div>
      <div class="row"><b>Steps 11–12 · deliver</b><p>decision D001 with grounds and a review date, commitment monitoring left open after the run.</p></div>
    </div>
  </div>
</section>

<section id="market" aria-labelledby="market-h">
  <div class="wrap">
    <div class="head">
      <div class="label">What it found</div>
      <h2 id="market-h">The market in numbers, <span class="acc">with sources</span></h2>
      <p>Every number in the registry carries a type, an A–D grade and a source. Card values are cross-checked against claim texts on every build: if the registry changes, the build fails instead of showing stale numbers.</p>
    </div>
    <div class="mgrid">
      <article class="mcard"><b>{{{{MF0_VALUE}}}}</b><span>the resume-builder market, 2024–2025; aggregator estimates diverge twofold, so the market is recorded as ranges</span><i>{{{{MF0_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF1_VALUE}}}}</b><span>CAGR of the AI sub-segment of resume builders — growth exactly where CVStart plays</span><i>{{{{MF1_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF2_VALUE}}}}</b><span>seven direct competitors (Zety, resume.io, Novoresume, Kickresume, Enhancv, Teal, Rezi) — freemium with aggressive auto-renewals</span><i>{{{{MF2_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF3_VALUE}}}}</b><span>of Fortune 500 companies use an ATS — a robot filters resumes before a human sees them</span><i>{{{{MF3_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF4_VALUE}}}}</b><span>of job seekers use AI in their job search — a survey spread, recorded as a range</span><i>{{{{MF4_SRC}}}}</i></article>
      <article class="mcard"><b>{{{{MF5_VALUE}}}}</b><span>the global online recruiting market — the base for sizing the addressable market</span><i>{{{{MF5_SRC}}}}</i></article>
    </div>
    <div class="claim" style="margin-top:24px">
      <div class="tags"><span class="tag">hypothesis · synthesis, not fact</span></div>
      <p>The unoccupied niche is a hypothesis [C013]: a multilingual private open-source AI resume builder, while western competitors cover English plus five languages. Persona hypotheses and the beta funnel are tagged origin=synthetic — hypotheses and method illustrations, not proven demand.</p>
    </div>
  </div>
</section>

<section id="options" aria-labelledby="options-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Steps 6–7</div>
      <h2 id="options-h">Options and red team: <span class="acc">five paths, none silent</span></h2>
      <p>At least three substantively distinct options, including “keep as is” and “shut it down”. A dedicated subagent attacks each one; its hits are built into the mitigations and the thresholds of the validation plan. The full table with economics lives in <a href="{DEMO_DIR}/outputs/03_options.md" target="_blank" rel="noopener">03_options.md</a>.</p>
    </div>
    <div class="rows">
      <div class="row"><b>A · status quo</b><p>free open source, nothing changes. Red-team hit: “an expensive hobby” — the MIT license lets a fork monetize your work.</p></div>
      <div class="row"><b>B · hosted freemium SaaS <span style="color:var(--accent)">← chosen</span></b><p>Free (BYOK) / Pro / Unlimited tiers, an opt-in cloud on top of the local MIT core, honest pricing without auto-renewals, locale waves. Hit: community trust in commercializing an open-source core — mitigations: BYOK-free tier, opt-in cloud, honest pricing, stop thresholds.</p></div>
      <div class="row"><b>C · B2B white-label</b><p>hosting the resume builder under a partner’s brand. Hit: a solo developer has no sales capability — deferred.</p></div>
      <div class="row"><b>D · dual-license</b><p>a paid commercial license on top of open source. Hit: it does not hold up legally on top of MIT — rejected.</p></div>
      <div class="row"><b>E · shut down commerce</b><p>the product stays a free OSS project. Hit: walking away from an asset on a growing market.</p></div>
    </div>
    <div class="claim" style="margin-top:24px">
      <div class="tags"><span class="tag a">choice · step 7</span><span class="tag">option {{{{D_LETTER}}}} · {{{{D_LABEL}}}}</span></div>
      <p>The agent’s recommendation is not “the best option in general” — it is the best one under the product lead’s constraints: the MIT core stays, solo resources, trust in the local mode is preserved. Conscious rejections: C — no sales capability; D — invalid on top of MIT; E — walking away from a growing market; A — a fork monetizes the work.</p>
    </div>
  </div>
</section>

<section id="decision" aria-labelledby="decision-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Step 11 · decision</div>
      <h2 id="decision-h">D001: <span class="acc">{{{{D_TITLE}}}}</span></h2>
      <p>A decision is recorded with grounds, a metric, a commitment, a review trigger and a date — <code>pfs decision add</code> writes it to decisions.jsonl, and <code>pfs next</code> and <code>pfs decision due</code> watch it from then on.</p>
    </div>
    <div class="claim">
      <div class="tags"><span class="tag a">D001</span><span class="tag">grounds: {{{{D_GROUNDS}}}}</span></div>
      <p>Metric: {{{{D_METRIC}}}} — target {{{{D_TARGET}}}} by {{{{D_BY_EN}}}}. Commitment: {{{{D_COMMIT}}}} — by {{{{D_DUE}}}}. Decision review: {{{{REVIEW}}}}. Trigger: {{{{D_TRIGGER}}}}.</p>
    </div>
  </div>
</section>

<section id="econ" aria-labelledby="econ-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Economics</div>
      <h2 id="econ-h">Paying-user math <span class="acc">in live formulas</span></h2>
      <p>The demo’s unit assumptions are [C016]; you can change the values on the input sheet of unit_economics.xlsx and the formulas recalculate.</p>
    </div>
    <div class="xl" style="max-width:560px">
      <div class="label" style="margin-bottom:10px">Excel · input sheet</div>
      <table>
        <tr><td>Pro price</td><td>${{{{XL_PRICE}}}}/mo</td></tr>
        <tr><td>25% variable costs → contribution margin</td><td>${{{{XL_CM}}}}</td></tr>
        <tr><td>LTV</td><td>≈ ${{{{XL_LTV}}}}</td></tr>
        <tr><td>LTV / CAC</td><td>≈ {{{{XL_RATIO}}}}</td></tr>
      </table>
    </div>
  </div>
</section>

<section id="sixpager" aria-labelledby="six-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The committee document</div>
      <h2 id="six-h">A RU and EN six-pager <span class="acc">with Excel workbooks</span></h2>
      <p>The report follows the FAQ-1…6 structure: market, segments, red-teamed options, tactics, plan and KPIs. Numbers trace back to registry claims; all formats live on the materials page.</p>
    </div>
    <ul class="sixlist">
      <li><b>FAQ-1</b><span>market and trends: size and estimate ranges, the ATS hiring gate, subscription fatigue</span></li>
      <li><b>FAQ-2</b><span>segments, personas and barriers — hypotheses to test in the beta</span></li>
      <li><b>FAQ-3</b><span>options A–{{{{D_OPT_LAST}}}} with red-team objections and the {{{{D_LETTER}}}} choice</span></li>
      <li><b>FAQ-4</b><span>the tactic matrix: BYOK-free tier, an honest pricing page, CV Studio, a follow-up tracker</span></li>
      <li><b>FAQ-5</b><span>the plan: a 90-day beta with continue / adjust / stop thresholds</span></li>
      <li><b>FAQ-6</b><span>KPIs in two planes: business and product</span></li>
    </ul>
    <div class="ctas" style="margin-top:28px;justify-content:center">
      <a class="pill pill-a" href="materials.html" data-goal="cta_demo_click">Open the materials{ARROW}</a>
      <a class="pill pill-b" href="{DEMO_RAW}/outputs/SIX_PAGER_EN.pdf" target="_blank" rel="noopener">SIX_PAGER_EN.pdf{ARROW}</a>
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
      <div class="eyebrow">The run took one human evening</div>
      <h2 id="fin-h">Repeat it <span class="acc">on your own problem</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Install the agent and describe your task as it is — the brief, the options and the decision will come together through the same twelve steps.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Install{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_EN}"""

HELP_BODY_RU = f"""
<a class="skip" href="#main">К содержимому</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Справка</div>
    <h1 id="h1">Как пользоваться <span class="acc">агентом</span></h1>
    <p class="lead">Пишите обычным языком, как коллеге. Агент сам ведёт шаги 1–12, задаёт не больше трёх вопросов за раз и объясняет, чего ему не хватает. Ниже — управление, команды и ответы на частые вопросы.</p>
    <div class="ctas">
      <a class="pill pill-b" href="#phrases">Управляющие фразы{ARROW}</a>
      <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Установить{ARROW}</a>
    </div>
  </div>
</section>

<section id="points" aria-labelledby="points-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Главное</div>
      <h2 id="points-h">Вся суть <span class="acc">за одну минуту</span></h2>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>Доказательства, а не красота</h3><p>Каждое число и вывод: тип (факт, гипотеза, прогноз, допущение, вывод), сила A–D и источник. Цепочка S### → C### → D### прослеживается от ссылки до решения.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Двенадцать шагов, три решения за вами</h3><p>Агент ведёт сам: бриф → источники → исследование → ситуация → варианты → <b>выбор</b> → стратегии → проверка → ревью → <b>решение</b> → мониторинг.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 5h12M4 10h12M4 15h7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Варианты честные</h3><p>Минимум три содержательно разных, включая «оставить как есть» и «закрыть направление». Отдельный субагент red team атакует каждый.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Состояние — в файлах</h3><p>projects/&lt;slug&gt;/ хранит всё. Новый чат, другая среда, перерыв — работа продолжается с того же места, без повторов.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>Excel на формулах</h3><p>Четыре книги: юнит-экономика, рост, когорты, рынок. Лист «Ввод» держит параметры — правьте, формулы пересчитаются.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Прозрачность и цена</h3><p>Журнал каждого действия, основания выводов, стоимость в токенах и деньгах: <code>pfs cost</code>, <code>pfs next</code>, <code>pfs check --strict</code>.</p></article>
    </div>
  </div>
</section>

<section id="talk" aria-labelledby="talk-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Общение</div>
      <h2 id="talk-h">Три вида сообщений, <span class="acc">никогда больше трёх вопросов</span></h2>
    </div>
    <div class="rows">
      <div class="row"><b>Задача</b><p>«Почему падает удержание в приложении», «кому продавать новый сервис» — обычным языком, без команд.</p></div>
      <div class="row"><b>Ответы на вопросы</b><p>Выбирайте вариант или отвечайте свободно — ответ сохраняется и становится основанием следующих шагов.</p></div>
      <div class="row"><b>Команды-фразы</b><p>«стоп», «уточни: …», «собери six-pager» — управление процессом (таблица ниже).</p></div>
    </div>
    <p class="muted" style="max-width:46em;margin:18px 0 0">Хороший первый запрос называет решение, которое предстоит принять: «Помоги решить, выводить ли антиспам в платную подписку; вот бриф и выгрузка за полгода». Слабый запрос («сделай стратегию») тоже сработает — агент уточнит целевое решение, получателя и ограничения, прежде чем тратить ваши токены.</p>
  </div>
</section>

<section id="phrases" aria-labelledby="phrases-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Управление</div>
      <h2 id="phrases-h">Управляющие <span class="acc">фразы</span></h2>
    </div>
    <div class="rows">
      <div class="row"><b>«стоп»</b><p>пауза: состояние сохранено, агент замолчит до новой команды</p></div>
      <div class="row"><b>«уточни: …»</b><p>корректировка задачи; переделается только затронутое, источники не дублируются</p></div>
      <div class="row"><b>«переделай раздел X»</b><p>точечная переработка одного раздела документа</p></div>
      <div class="row"><b>«что решать сейчас»</b><p><code>pfs next</code>: текущий шаг, просроченные решения, устаревшие основания, открытые вопросы</p></div>
      <div class="row"><b>«что решать по срокам»</b><p><code>pfs decision due</code>: решения и обязательства с наступившей датой пересмотра</p></div>
      <div class="row"><b>«что затронет новый источник»</b><p><code>pfs impact</code>: какие выводы, строки документов и решения устареют</p></div>
      <div class="row"><b>«собери six-pager»</b><p><code>pfs calc all</code> + <code>pfs export --six-pager</code>: отчёт FAQ-1…6 и четыре книги Excel</p></div>
      <div class="row"><b>«пересчитай Excel»</b><p><code>pfs calc all</code> — книги пересобираются с текущим calcs.json</p></div>
      <div class="row"><b>«собери отчёт» / «собери деку»</b><p><code>pfs export</code> → REPORT.md; <code>pfs export --deck</code> → HTML-дека</p></div>
      <div class="row"><b>«сделай доку»</b><p><code>pfs docx файл.md</code> — Markdown в Word без зависимостей</p></div>
      <div class="row"><b>«проверь проект»</b><p><code>pfs check --strict</code> — контроль чисел, ссылок, вариантов</p></div>
      <div class="row"><b>«сколько стоило»</b><p><code>pfs cost</code> — токены и деньги по моделям</p></div>
    </div>
  </div>
</section>

<section id="quickstart" aria-labelledby="qs-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Быстрый старт</div>
      <h2 id="qs-h">Пять минут <span class="acc">до первой задачи</span></h2>
      <p>Нужны Python 3.9+ и одна из сред. Пакеты не устанавливаются — только стандартная библиотека. Секреты (ключи MCP) кладутся в <code>.env</code> — он не коммитится и не обязателен для базового цикла.</p>
    </div>
    <ol class="steps">
      <li><span class="label">1 · Скачайте репозиторий</span><div class="cmd"><code>git clone https://github.com/Fighter90/product-factory-strategist.git</code><button class="copy" type="button" data-copy="0" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">2 · Установите pfs</span><div class="cmd"><code>cd product-factory-strategist &amp;&amp; ./scripts/install.sh</code><button class="copy" type="button" data-copy="1" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">3 · Проверьте окружение</span><div class="cmd"><code>pfs doctor</code><button class="copy" type="button" data-copy="2" data-ok="Скопировано">Копировать</button></div></li>
      <li><span class="label">4 · Откройте папку в своей среде</span><div class="cmd"><code>opencode</code><button class="copy" type="button" data-copy="3" data-ok="Скопировано">Копировать</button></div></li>
    </ol>
  </div>
</section>

<section id="first" aria-labelledby="first-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Первый проект</div>
      <h2 id="first-h">Что произойдёт <span class="acc">после pfs new</span></h2>
    </div>
    <div class="proof">
      <div class="term" aria-label="Создание первого проекта">
        <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
        <pre><span class="p">$</span> pfs new "Название" "запрос дословно"
<span class="hi">Создан projects/&lt;slug&gt; · активный проект · дальше: intake</span></pre>
      </div>
      <div class="claim">
        <div class="tags"><span class="tag a">шаг 1 · intake</span><span class="tag">до трёх вопросов</span></div>
        <p>Агент определит сценарий маршрутизацией, задаст вопросный блок intake — до трёх вопросов с вариантами и рекомендацией — запишет бриф в <code>outputs/00_brief.md</code> и остановится до вашего подтверждения. Это первая из трёх пауз человека. Переключение проектов — <code>pfs use</code>, список — <code>pfs list</code>, состояние — <code>pfs status</code>.</p>
      </div>
    </div>
  </div>
</section>

<section id="cycle" aria-labelledby="cycle-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Устройство цикла</div>
      <h2 id="cycle-h">Двенадцать шагов <span class="acc">в четырёх фазах</span></h2>
      <p>Каждый шаг имеет обязательные карты знаний, вопросный блок, ворота качества и артефакт на выходе. Прогресс виден одной строкой: «Шаг N/12 · research · источники · дальше: ситуация».</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Исследовать · 1–4</h3><ol><li class="h"><span class="n">1</span>Бриф</li><li><span class="n">2</span>Источники</li><li><span class="n">3</span>Исследование</li><li><span class="n">4</span>Сегменты</li></ol></div>
      <div class="ph"><h3>Определить · 5–7</h3><ol><li><span class="n">5</span>Картина ситуации</li><li><span class="n">6</span>Варианты и red team</li><li class="h"><span class="n">7</span>Выбор</li></ol></div>
      <div class="ph"><h3>Разработать · 8–10</h3><ol><li><span class="n">8</span>Стратегии</li><li><span class="n">9</span>План проверки</li><li><span class="n">10</span>Ревью качества</li></ol></div>
      <div class="ph"><h3>Довести · 11–12</h3><ol><li class="h"><span class="n">11</span>Решение</li><li><span class="n">12</span>Мониторинг</li></ol></div>
    </div>
    <div class="rows" style="margin-top:44px">
      <div class="row"><b>Шаги 1–4 · исследовать</b><p>регистрация источников с дедупликацией и проверкой доменов, план от вопросов, которые могут изменить решение, утверждения с типом и цитатой, персоны и JTBD. Синтетика даёт только гипотезы.</p></div>
      <div class="row"><b>Шаги 5–7 · определить</b><p>что известно и откуда, чего не знаем; варианты с экономикой и возражениями red team; выбор человека — ответ становится основанием стратегий.</p></div>
      <div class="row"><b>Шаги 8–10 · разработать</b><p>продуктовая и коммуникационная стратегии с таблицей «обещание → подтверждение», план проверки из пяти обязательных разделов, независимая оценка по рубрике.</p></div>
      <div class="row"><b>Шаги 11–12 · довести</b><p>решение с основаниями, метрикой и датой пересмотра; мониторинг сроков и обновление выводов при новых данных.</p></div>
    </div>
  </div>
</section>

<section id="demo" aria-labelledby="demo-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Демо</div>
      <h2 id="demo-h">Посмотреть на живом прогоне: <span class="acc">CVStart</span></h2>
      <p>Полный сквозной прогон агента на живом open-source продукте: 12 шагов, варианты A–{{{{D_OPT_LAST}}}} с red team, six-pager RU и EN в трёх форматах, четыре книги Excel, решение D001. Проект — <code>projects/демо/</code> в репозитории.</p>
    </div>
    <div class="ctas" style="margin-bottom:28px">
      <a class="pill pill-a" href="demo.html" data-goal="cta_demo_click">Открыть демо-разбор{ARROW}</a>
      <a class="pill pill-b" href="materials.html" data-goal="cta_demo_click">Материалы прогона{ARROW}</a>
    </div>
    <div class="term" aria-label="Как повторить прогон">
      <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
      <pre><span class="p">$</span> pfs use демо     <span class="p"># переключиться на демо</span>
<span class="p">$</span> pfs next        <span class="p"># что решать сейчас</span>
<span class="p">$</span> pfs check --strict
<span class="p"># своя задача:</span>
<span class="p">$</span> pfs new "Название" "Запрос дословно"</pre>
    </div>
  </div>
</section>

<section id="envs" aria-labelledby="envs-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Среды</div>
      <h2 id="envs-h">Одна папка — <span class="acc">любая среда</span></h2>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 9l2 2 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Claude Code — полный опыт</h3><p>Откройте папку репозитория — подхватятся навыки, субагенты, хуки (контекст при старте, домены, фразы-инструкции, стоимость) и команды CLI. Просто напишите задачу.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="3.5" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Cursor, Codex, OpenCode, Windsurf, Copilot</h3><p>Все среды читают <code>AGENTS.md</code>. Начните с «прочитай AGENTS.md и выполни <code>pfs status</code>» — агент восстановит контекст и продолжит с того же шага.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="7" cy="10" r="3.5" stroke="currentColor" stroke-width="1.6"/><circle cx="13" cy="10" r="3.5" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>MCP-сервер</h3><p><code>pfs-strategist</code> работает во всех средах: те же инструменты через MCP — состояние, источники, утверждения, экспорт документов.</p></article>
    </div>
  </div>
</section>

<section id="faq" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="head" style="margin:0"><div class="label">Вопросы</div><h2 id="faq-h">Частые <span class="acc">вопросы</span></h2></div>
    <div>
      <details><summary>Как продолжить после перерыва?<span class="pm" aria-hidden="true">+</span></summary><p>Всё состояние — в файлах projects/&lt;slug&gt;/: state.json, claims.jsonl, decisions.jsonl, log.jsonl, sources/, outputs/. Новый чат в папке репозитория продолжает с того же шага; в среде без хуков напишите «прочитай AGENTS.md и выполни pfs status». Выполненные шаги не повторяются.</p></details>
      <details><summary>Как перенести проект между средами?<span class="pm" aria-hidden="true">+</span></summary><p>Проект — обычная папка: скопируйте projects/&lt;slug&gt;/ (или git push/pull) и откройте в другой среде. Секреты в .env не переносятся автоматически — перенесите руками и не коммитьте.</p></details>
      <details><summary>Какие данные использует агент?<span class="pm" aria-hidden="true">+</span></summary><p>Только открытые источники и материалы, которые вы передали сами. Разрешённые домены задаются в проекте и проверяются до запроса; команды из текстов источников агент не выполняет — помечает их как данные.</p></details>
      <details><summary>Что проверяет pfs check?<span class="pm" aria-hidden="true">+</span></summary><p>Факт без источника — ошибка; факт только на синтетике — ошибка; ссылка на несуществующий или отозванный C###/S###/D### — ошибка с подсказкой замены; число без тега в документе — предупреждение; меньше трёх вариантов или нет «оставить как есть» — ошибка; нет обязательного раздела плана проверки — ошибка.</p></details>
      <details><summary>Что делать с частыми ошибками?<span class="pm" aria-hidden="true">+</span></summary><p>«Факт без источника недопустим» — так и задумано: добавьте источник или запишите как гипотезу. «Домен не входит в разрешённые» — правьте allowed_sources в project.json. «Извлечено 0 знаков» — сайт рендерится JavaScript: сохраните текст вручную через --text-file.</p></details>
      <details><summary>Как расшифровывать C###, S###, D###?<span class="pm" aria-hidden="true">+</span></summary><p>S### — источник с цитатой и хешем, C### — утверждение с типом и силой A–D, D### — решение с основаниями и датой пересмотра. Шестистраничный отчёт комитета — six-pager, атака на варианты — red team.</p></details>
    </div>
  </div>
</section>

<section class="final" aria-labelledby="fin-h">
  <div class="wrap">
    <div class="box">
      <div class="eyebrow">Открытый код · MIT</div>
      <h2 id="fin-h">Дальше — <span class="acc">своя задача</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Глубже про шаги, субагентов, хуки и MCP — в README и docs репозитория. Для старта достаточно пяти минут установки.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Установить{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_RU}"""

HELP_BODY_EN = f"""
<a class="skip" href="#main">Skip to content</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Help</div>
    <h1 id="h1">How to work <span class="acc">with the agent</span></h1>
    <p class="lead">Write in plain language, as to a colleague. The agent drives steps 1–12 on its own, asks at most three questions at a time and explains what it is missing. Below: control, commands and answers to frequent questions.</p>
    <div class="ctas">
      <a class="pill pill-b" href="#phrases">Control phrases{ARROW}</a>
      <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Install{ARROW}</a>
    </div>
  </div>
</section>

<section id="points" aria-labelledby="points-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Key points</div>
      <h2 id="points-h">The whole gist <span class="acc">in one minute</span></h2>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>Evidence, not eloquence</h3><p>Every number and conclusion: a type (fact, hypothesis, forecast, assumption, inference), an A–D grade and a source. The chain S### → C### → D### is traceable from a link to a decision.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M10 6v4l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Twelve steps, three decisions are yours</h3><p>The agent drives: brief → sources → research → situation → options → <b>choice</b> → strategies → validation → review → <b>decision</b> → monitoring.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 5h12M4 10h12M4 15h7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Honest options</h3><p>At least three substantively distinct ones, including “keep as is” and “shut it down”. A dedicated red-team subagent attacks each.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>State lives in files</h3><p>projects/&lt;slug&gt;/ stores everything. A new chat, another tool, a break — work resumes where it stopped, with no repeats.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>Formula Excel</h3><p>Four workbooks: unit economics, growth, cohorts, market. The input sheet holds the parameters — change them and the formulas recalculate.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Transparency and cost</h3><p>An action log, grounds behind conclusions, cost in tokens and money: <code>pfs cost</code>, <code>pfs next</code>, <code>pfs check --strict</code>.</p></article>
    </div>
  </div>
</section>

<section id="talk" aria-labelledby="talk-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Communication</div>
      <h2 id="talk-h">Three kinds of messages, <span class="acc">never more than three questions</span></h2>
    </div>
    <div class="rows">
      <div class="row"><b>A task</b><p>“Why is in-app retention dropping”, “who should we sell the new service to” — plain language, no commands.</p></div>
      <div class="row"><b>Answers to its questions</b><p>Pick an option or reply freely — the answer is stored and grounds the next steps.</p></div>
      <div class="row"><b>Control phrases</b><p>“stop”, “clarify: …”, “build the six-pager” — process control (table below).</p></div>
    </div>
    <p class="muted" style="max-width:46em;margin:18px 0 0">A good first request names the decision to make: “Help me decide whether to launch antispam as a paid subscription; here is the brief and six months of data.” A weak one (“make me a strategy”) also works — the agent clarifies the decision, audience and constraints before spending your tokens.</p>
  </div>
</section>

<section id="phrases" aria-labelledby="phrases-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Control</div>
      <h2 id="phrases-h">Control <span class="acc">phrases</span></h2>
    </div>
    <div class="rows">
      <div class="row"><b>“stop”</b><p>pause: state saved, the agent stays quiet until a new command</p></div>
      <div class="row"><b>“clarify: …”</b><p>adjust the task; only the affected part is redone, sources are not duplicated</p></div>
      <div class="row"><b>“redo section X”</b><p>targeted rework of a single document section</p></div>
      <div class="row"><b>“what should I decide now”</b><p><code>pfs next</code>: current step, overdue decisions, stale grounds, open questions</p></div>
      <div class="row"><b>“what is due”</b><p><code>pfs decision due</code>: decisions and commitments whose review date has arrived</p></div>
      <div class="row"><b>“what will a new source affect”</b><p><code>pfs impact</code>: which conclusions, document lines and decisions go stale</p></div>
      <div class="row"><b>“build the six-pager”</b><p><code>pfs calc all</code> + <code>pfs export --six-pager</code>: the FAQ-1…6 report and four Excel workbooks</p></div>
      <div class="row"><b>“recalculate Excel”</b><p><code>pfs calc all</code> — workbooks rebuilt from the current calcs.json</p></div>
      <div class="row"><b>“build the report” / “build the deck”</b><p><code>pfs export</code> → REPORT.md; <code>pfs export --deck</code> → an HTML deck</p></div>
      <div class="row"><b>“make it a doc”</b><p><code>pfs docx file.md</code> — Markdown to Word, dependency-free</p></div>
      <div class="row"><b>“check the project”</b><p><code>pfs check --strict</code> — numbers, links, options</p></div>
      <div class="row"><b>“how much did it cost”</b><p><code>pfs cost</code> — tokens and money per model</p></div>
    </div>
  </div>
</section>

<section id="quickstart" aria-labelledby="qs-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Quick start</div>
      <h2 id="qs-h">Five minutes <span class="acc">to your first task</span></h2>
      <p>You need Python 3.9+ and one of the supported tools. No packages to install — the standard library only. Secrets (MCP keys) go to <code>.env</code> — it is git-ignored and not required for the basic loop.</p>
    </div>
    <ol class="steps">
      <li><span class="label">1 · Clone the repository</span><div class="cmd"><code>git clone https://github.com/Fighter90/product-factory-strategist.git</code><button class="copy" type="button" data-copy="0" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">2 · Install pfs</span><div class="cmd"><code>cd product-factory-strategist &amp;&amp; ./scripts/install.sh</code><button class="copy" type="button" data-copy="1" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">3 · Check your setup</span><div class="cmd"><code>pfs doctor</code><button class="copy" type="button" data-copy="2" data-ok="Copied">Copy</button></div></li>
      <li><span class="label">4 · Open the folder in your tool</span><div class="cmd"><code>opencode</code><button class="copy" type="button" data-copy="3" data-ok="Copied">Copy</button></div></li>
    </ol>
  </div>
</section>

<section id="first" aria-labelledby="first-h">
  <div class="wrap">
    <div class="head">
      <div class="label">First project</div>
      <h2 id="first-h">What happens <span class="acc">after pfs new</span></h2>
    </div>
    <div class="proof">
      <div class="term" aria-label="Creating a first project">
        <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
        <pre><span class="p">$</span> pfs new "Name" "the request verbatim"
<span class="hi">Created projects/&lt;slug&gt; · active project · next: intake</span></pre>
      </div>
      <div class="claim">
        <div class="tags"><span class="tag a">step 1 · intake</span><span class="tag">up to three questions</span></div>
        <p>The agent classifies the scenario, asks the intake question block — up to three questions with options and a recommendation — writes the brief to <code>outputs/00_brief.md</code> and stops for your approval. That is the first of three human pauses. Switch projects with <code>pfs use</code>, list them with <code>pfs list</code>, inspect state with <code>pfs status</code>.</p>
      </div>
    </div>
  </div>
</section>

<section id="cycle" aria-labelledby="cycle-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The cycle</div>
      <h2 id="cycle-h">Twelve steps <span class="acc">in four phases</span></h2>
      <p>Each step has mandatory knowledge cards, a question block, quality gates and an artifact. Progress shows in one line: “Step 3/12 · research · sources · next: situation”.</p>
    </div>
    <div class="phases">
      <div class="ph"><h3>Research · 1–4</h3><ol><li class="h"><span class="n">1</span>Brief</li><li><span class="n">2</span>Sources</li><li><span class="n">3</span>Research</li><li><span class="n">4</span>Segments</li></ol></div>
      <div class="ph"><h3>Define · 5–7</h3><ol><li><span class="n">5</span>Situation</li><li><span class="n">6</span>Options and red team</li><li class="h"><span class="n">7</span>Choice</li></ol></div>
      <div class="ph"><h3>Develop · 8–10</h3><ol><li><span class="n">8</span>Strategies</li><li><span class="n">9</span>Validation plan</li><li><span class="n">10</span>Quality review</li></ol></div>
      <div class="ph"><h3>Deliver · 11–12</h3><ol><li class="h"><span class="n">11</span>Decision</li><li><span class="n">12</span>Monitoring</li></ol></div>
    </div>
    <div class="rows" style="margin-top:44px">
      <div class="row"><b>Steps 1–4 · research</b><p>registering sources with dedup and domain checks, a plan built from questions that could change the decision, claims with type and quote, personas and JTBD. Synthetic data yields hypotheses only.</p></div>
      <div class="row"><b>Steps 5–7 · define</b><p>what is known and from where, what is not; options with economics and red-team objections; the human choice becomes the ground for the strategies.</p></div>
      <div class="row"><b>Steps 8–10 · develop</b><p>product and communication strategies with a “promise → product proof” table, a validation plan with five mandatory sections, an independent rubric review.</p></div>
      <div class="row"><b>Steps 11–12 · deliver</b><p>a decision with grounds, a metric and a review date; deadline monitoring and refreshing conclusions as new data arrives.</p></div>
    </div>
  </div>
</section>

<section id="demo" aria-labelledby="demo-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Demo</div>
      <h2 id="demo-h">See a live run: <span class="acc">CVStart</span></h2>
      <p>A full end-to-end run on a live open-source product: 12 steps, options A–{{{{D_OPT_LAST}}}} with red team, a RU and EN six-pager in three formats, four Excel workbooks, decision D001. The project lives in the <code>projects/</code> folder of the repository.</p>
    </div>
    <div class="ctas" style="margin-bottom:28px">
      <a class="pill pill-a" href="demo.html" data-goal="cta_demo_click">Open the walkthrough{ARROW}</a>
      <a class="pill pill-b" href="materials.html" data-goal="cta_demo_click">Run materials{ARROW}</a>
    </div>
    <div class="term" aria-label="How to repeat the run">
      <div class="bar" aria-hidden="true"><i></i><i></i><i></i></div>
      <pre><span class="p">$</span> pfs use demo     <span class="p"># switch to the demo project</span>
<span class="p">$</span> pfs next        <span class="p"># what to decide now</span>
<span class="p">$</span> pfs check --strict
<span class="p"># your own task:</span>
<span class="p">$</span> pfs new "Name" "The request verbatim"</pre>
    </div>
  </div>
</section>

<section id="envs" aria-labelledby="envs-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Tools</div>
      <h2 id="envs-h">One folder — <span class="acc">any tool</span></h2>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 9l2 2 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>Claude Code — the full experience</h3><p>Open the repository folder — skills, subagents, hooks (context at start, domains, instruction-like phrases, cost) and CLI commands are picked up automatically. Just write the task.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="3.5" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>Cursor, Codex, OpenCode, Windsurf, Copilot</h3><p>Every tool reads <code>AGENTS.md</code>. Start with “read AGENTS.md and run <code>pfs status</code>” — the agent restores the context and continues from the same step.</p></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="7" cy="10" r="3.5" stroke="currentColor" stroke-width="1.6"/><circle cx="13" cy="10" r="3.5" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>MCP server</h3><p><code>pfs-strategist</code> works in every tool: the same instruments over MCP — state, sources, claims, document export.</p></article>
    </div>
  </div>
</section>

<section id="faq" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="head" style="margin:0"><div class="label">FAQ</div><h2 id="faq-h">Frequently <span class="acc">asked</span></h2></div>
    <div>
      <details><summary>How do I resume after a break?<span class="pm" aria-hidden="true">+</span></summary><p>All state lives in projects/&lt;slug&gt;/: state.json, claims.jsonl, decisions.jsonl, log.jsonl, sources/, outputs/. A new chat in the repository folder resumes from the same step; in a tool without hooks, write “read AGENTS.md and run pfs status”. Completed steps are never repeated.</p></details>
      <details><summary>How do I move a project between tools?<span class="pm" aria-hidden="true">+</span></summary><p>A project is a plain folder: copy projects/&lt;slug&gt;/ (or git push/pull) and open it in another tool. Secrets in .env are not carried over automatically — move them by hand and never commit them.</p></details>
      <details><summary>What data does the agent use?<span class="pm" aria-hidden="true">+</span></summary><p>Only open sources and the materials you hand over yourself. Allowed domains are set per project and checked before each request; instructions found inside source texts are never executed — they are flagged as data.</p></details>
      <details><summary>What does pfs check verify?<span class="pm" aria-hidden="true">+</span></summary><p>A fact without a source — error; a fact resting only on synthetic data — error; a link to a missing or retracted C###/S###/D### — error with a replacement hint; a naked number in a document — warning; fewer than three options or no “keep as is” — error; a missing mandatory validation section — error.</p></details>
      <details><summary>What about frequent errors?<span class="pm" aria-hidden="true">+</span></summary><p>“A fact without a source is not allowed” — by design: add a source or record a hypothesis. “The domain is not in the allowed list” — edit allowed_sources in project.json. “Extracted 0 characters” — the page renders via JavaScript: save the text by hand with --text-file.</p></details>
      <details><summary>What do C###, S### and D### mean?<span class="pm" aria-hidden="true">+</span></summary><p>S### — a source with a quote and a hash, C### — a claim with a type and an A–D grade, D### — a decision with grounds and a review date. The committee’s six-page report is the six-pager; the option attack is the red team.</p></details>
    </div>
  </div>
</section>

<section class="final" aria-labelledby="fin-h">
  <div class="wrap">
    <div class="box">
      <div class="eyebrow">Open source · MIT</div>
      <h2 id="fin-h">Next — <span class="acc">your own task</span></h2>
      <p class="muted" style="margin:0;max-width:34em">For a deeper dive into steps, subagents, hooks and MCP, see the README and docs in the repository. Five minutes of setup is enough to start.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Install{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_EN}"""

MAT_BODY_RU = f"""
<a class="skip" href="#main">К содержимому</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Материалы демо</div>
    <h1 id="h1">Все материалы <span class="acc">прогона CVStart</span></h1>
    <p class="lead">Всё, что собрал агент на живом open-source продукте cvstart.org: six-pager комитета в двух языках и трёх форматах, четыре книги Excel с живыми формулами, скриншоты продукта, реестры источников и утверждений. Числа ниже — из файлов проекта.</p>
    <div class="facts"><span><b>{{{{D_SOURCES}}}}</b> источников</span><span><b>{{{{D_CLAIMS}}}}</b> утверждений</span><span>варианты <b>A–{{{{D_OPT_LAST}}}}</b></span><span>выбор: <b>{{{{D_LETTER}}}} · {{{{D_LABEL}}}}</b></span></div>
    <div class="ctas">
      <a class="pill pill-b" href="demo.html" data-goal="cta_demo_click">Демо-разбор{ARROW}</a>
      <a class="pill pill-a" href="#sixpager">Six-pager{ARROW}</a>
    </div>
  </div>
</section>

<section id="sixpager" aria-labelledby="six-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Документ для комитета</div>
      <h2 id="six-h">Six-pager: <span class="acc">FAQ-1…6 в трёх форматах</span></h2>
      <p>Итоговый отчёт прогона: состояние рынка, сегменты и персоны, варианты с red team, тактики, план беты и пороги решения. Собирается командой <code>pfs export --six-pager</code>; каждое число прослеживается до утверждений реестра.</p>
    </div>
    <div class="grid">
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>SIX_PAGER_RU</h3>
        <p>Русская версия: рынок resume builders, сегменты и персоны-гипотезы, варианты A–{{{{D_OPT_LAST}}}} с red team, тактики Free / Pro / Unlimited, план hosted-беты и пороги решения.</p>
        <div class="ctas">
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_RU.pdf" target="_blank" rel="noopener">PDF{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/SIX_PAGER_RU.docx" target="_blank" rel="noopener">DOCX{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_RU.md" target="_blank" rel="noopener">Markdown{ARROW}</a>
        </div>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>SIX_PAGER_EN</h3>
        <p>English version: the state of the resume-builder market, segment and persona hypotheses, options A–{{{{D_OPT_LAST}}}} with red team, Free / Pro / Unlimited tactics, the hosted-beta plan and decision thresholds.</p>
        <div class="ctas">
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_EN.pdf" target="_blank" rel="noopener">PDF{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/SIX_PAGER_EN.docx" target="_blank" rel="noopener">DOCX{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_EN.md" target="_blank" rel="noopener">Markdown{ARROW}</a>
        </div>
      </article>
    </div>
    <p class="muted" style="max-width:52em;margin:18px 0 0">Один источник — три формата: MD для чтения и правок, PDF для комитета, DOCX для правок руководителя. Плюс <a href="{DEMO_DIR}/outputs/SIX_PAGER.md" target="_blank" rel="noopener">SIX_PAGER.md</a> — черновик, который агент собирает сам; детализация — по промпт-спецификации <code>knowledge/templates/SIX_PAGER_PROMPT.md</code>.</p>
  </div>
</section>

<section id="excel" aria-labelledby="excel-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Расчёты</div>
      <h2 id="excel-h">Четыре книги <span class="acc">с живыми формулами</span></h2>
      <p>Книги в <code>outputs/attachments/</code>: редактируемые вводные на листе «Ввод» — формулы пересчитываются при открытии, допущения меняются на лету. Каждое значение «Ввода» прослеживается до утверждения реестра.</p>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>unit_economics.xlsx</h3><p>Вклад платящего ${{{{XL_CM}}}}, LTV ≈ ${{{{XL_LTV}}}}, LTV/CAC ≈ {{{{XL_RATIO}}}}, чувствительность к цене и оттоку.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/unit_economics.xlsx" target="_blank" rel="noopener">Открыть книгу{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>growth_model.xlsx</h3><p>Модель роста на 12 месяцев: воронка визиты → регистрации → активации → платящие → MRR; сверка с ожиданием беты.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/growth_model.xlsx" target="_blank" rel="noopener">Открыть книгу{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M3 10h14M10 3c2.5 2.2 2.5 11.8 0 14M10 3c-2.5 2.2-2.5 11.8 0 14" stroke="currentColor" stroke-width="1.2"/></svg></div><h3>cohort_retention.xlsx</h3><p>Когорты удержания по неделям: возвращаемость активированных и платящих, база для плана проверки.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/cohort_retention.xlsx" target="_blank" rel="noopener">Открыть книгу{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><circle cx="10" cy="10" r="3.6" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>market_sizing.xlsx</h3><p>Адресуемый рынок онлайн-рекрутинга: {{{{MF5_VALUE}}}} как база, консервативная граница коридора оценок, выход на SOM через конверсии.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/market_sizing.xlsx" target="_blank" rel="noopener">Открыть книгу{ARROW}</a></div></article>
    </div>
  </div>
</section>

<section id="shots" aria-labelledby="shots-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Продукт</div>
      <h2 id="shots-h">Скриншоты <span class="acc">cvstart.org</span></h2>
      <p>Живой open-source продукт, на котором агент вёл весь прогон: лендинг в двух локалях, дашборд поиска работы с AI-скорингом, карта вакансий и трекер заявок.</p>
    </div>
    <div class="shots">
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_ru.jpg" width="960" height="1600" alt="Лендинг cvstart.org в русской локали" loading="lazy" decoding="async"><figcaption>Лендинг в русской локали: позиционирование бесплатности, скан джоб-бордов, языки интерфейса.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_en.jpg" width="960" height="1600" alt="Лендинг cvstart.org в английской локали" loading="lazy" decoding="async"><figcaption>Тот же лендинг в английской локали — одна кодовая база, языковые версии с hreflang.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_ru.jpg" width="1600" height="1000" alt="Дашборд поиска работы cvstart.org в русской локали" loading="lazy" decoding="async"><figcaption>Дашборд: AI-скоринг вакансий против резюме — ядро продукта.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_en.jpg" width="1600" height="1000" alt="Дашборд поиска работы cvstart.org в английской локали" loading="lazy" decoding="async"><figcaption>Английская версия дашборда: fit-скоринг, фильтры по джоб-бордам.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_map_en.jpg" width="1600" height="1487" alt="Карта вакансий cvstart.org" loading="lazy" decoding="async"><figcaption>Карта вакансий: география предложений поверх скана джоб-бордов.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_tracker_en.jpg" width="1600" height="1000" alt="Трекер заявок cvstart.org" loading="lazy" decoding="async"><figcaption>Трекер заявок с follow-up: воронка откликов между сессиями поиска.</figcaption></figure>
    </div>
  </div>
</section>

<section id="evidence" aria-labelledby="ev-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Доказательная база</div>
      <h2 id="ev-h">Реестры прогона <span class="acc">в открытом доступе</span></h2>
      <p>Ничего не спрятано: полный реестр, источники с URL и утверждениями лежат в репозитории демо-проекта.</p>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div><h3>REPORT.md</h3><p>Полный документ прогона: бриф, картина ситуации, варианты, стратегии, план проверки, решение — с тегами C### у каждого числа.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/REPORT.md" target="_blank" rel="noopener">Открыть{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>sources/ — {{{{D_SOURCES}}}} источников</h3><p>Рыночные дайджесты с URL, датой извлечения и хешем; разрешённые домены заданы в project.json.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/sources" target="_blank" rel="noopener">Каталог источников{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>claims.jsonl — {{{{D_CLAIMS}}}} утверждений</h3><p>Каждое с типом (факт, гипотеза, прогноз, допущение, вывод), силой A–D и источником. Синтетика помечена origin=synthetic — это гипотезы, не доказанный спрос.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/claims.jsonl" target="_blank" rel="noopener">Реестр{ARROW}</a></div></article>
    </div>
    <div class="grid" style="margin-top:16px">
      <article class="card w6"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="4.5" stroke="currentColor" stroke-width="1.6"/><path d="M11.5 11.5 16 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>cvstart.org — сайт продукта</h3><p>Живой продукт демо: AI-конструктор резюме и дашборд поиска работы, локальный режим, открытый код.</p><div class="ctas"><a class="pill pill-b pill-sm" href="https://cvstart.org/" target="_blank" rel="noopener" data-goal="github_click">Открыть сайт{ARROW}</a></div></article>
      <article class="card w6"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 4h6v3H7zM4 13h5v3H4zM11 13h5v3h-5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M10 7v3M6.5 10h7" stroke="currentColor" stroke-width="1.4"/></svg></div><h3>career-ops-ui — репозиторий</h3><p>Исходный код продукта демо: скан джоб-бордов, AI-скоринг, CV Studio, трекер, карта вакансий.</p><div class="ctas"><a class="pill pill-b pill-sm" href="https://github.com/Fighter90/career-ops-ui" target="_blank" rel="noopener" data-goal="github_click">Открыть репозиторий{ARROW}</a></div></article>
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
      <div class="eyebrow">Всё то же — на вашей задаче</div>
      <h2 id="fin-h">Соберите такой пакет <span class="acc">для своего комитета</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Установите агента, опишите задачу — и получите такой же набор: реестры, стратегии, six-pager и книги Excel.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Установить{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_RU}"""

MAT_BODY_EN = f"""
<a class="skip" href="#main">Skip to content</a>

{{{{NAV}}}}

<main id="main">

<section class="subhero" id="top" aria-labelledby="h1">
  <div class="wrap inner">
    <div class="eyebrow">Demo materials</div>
    <h1 id="h1">Everything the CVStart run <span class="acc">produced</span></h1>
    <p class="lead">All the artifacts the agent assembled on the live open-source product cvstart.org: a committee six-pager in two languages and three formats, four Excel workbooks with live formulas, product screenshots, and the source and claim registries. The numbers below come from the project files.</p>
    <div class="facts"><span><b>{{{{D_SOURCES}}}}</b> sources</span><span><b>{{{{D_CLAIMS}}}}</b> claims</span><span>options <b>A–{{{{D_OPT_LAST}}}}</b></span><span>chosen: <b>{{{{D_LETTER}}}} · {{{{D_LABEL}}}}</b></span></div>
    <div class="ctas">
      <a class="pill pill-b" href="demo.html" data-goal="cta_demo_click">The walkthrough{ARROW}</a>
      <a class="pill pill-a" href="#sixpager">The six-pager{ARROW}</a>
    </div>
  </div>
</section>

<section id="sixpager" aria-labelledby="six-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The committee document</div>
      <h2 id="six-h">The six-pager: <span class="acc">FAQ-1…6 in three formats</span></h2>
      <p>The run’s final report: the state of the market, segments and personas, red-teamed options, tactics, the beta plan and decision thresholds. Assembled with the <code>pfs export --six-pager</code> command; every number traces back to a registry claim.</p>
    </div>
    <div class="grid">
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>SIX_PAGER_RU</h3>
        <p>The Russian version: the resume-builder market, segment and persona hypotheses, options A–{{{{D_OPT_LAST}}}} with red team, Free / Pro / Unlimited tactics, the hosted-beta plan and decision thresholds.</p>
        <div class="ctas">
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_RU.pdf" target="_blank" rel="noopener">PDF{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/SIX_PAGER_RU.docx" target="_blank" rel="noopener">DOCX{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_RU.md" target="_blank" rel="noopener">Markdown{ARROW}</a>
        </div>
      </article>
      <article class="card w6">
        <div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
        <h3>SIX_PAGER_EN</h3>
        <p>The English version: the state of the resume-builder market, segment and persona hypotheses, options A–{{{{D_OPT_LAST}}}} with red team, Free / Pro / Unlimited tactics, the hosted-beta plan and decision thresholds.</p>
        <div class="ctas">
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_EN.pdf" target="_blank" rel="noopener">PDF{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/SIX_PAGER_EN.docx" target="_blank" rel="noopener">DOCX{ARROW}</a>
          <a class="pill pill-b pill-sm" href="{DEMO_RAW}/outputs/SIX_PAGER_EN.md" target="_blank" rel="noopener">Markdown{ARROW}</a>
        </div>
      </article>
    </div>
    <p class="muted" style="max-width:52em;margin:18px 0 0">One source, three formats: MD for reading and editing, PDF for the committee, DOCX for the product lead’s edits. Plus <a href="{DEMO_DIR}/outputs/SIX_PAGER.md" target="_blank" rel="noopener">SIX_PAGER.md</a> — a draft the agent assembles itself; its depth follows the prompt spec in <code>knowledge/templates/SIX_PAGER_PROMPT.md</code>.</p>
  </div>
</section>

<section id="excel" aria-labelledby="excel-h">
  <div class="wrap">
    <div class="head">
      <div class="label">Calculations</div>
      <h2 id="excel-h">Four workbooks <span class="acc">with live formulas</span></h2>
      <p>The workbooks live in <code>outputs/attachments/</code>: editable inputs on the input sheet — formulas recalculate on open, assumptions change on the fly. Every input value traces back to a registry claim.</p>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="3.5" y="4.5" width="13" height="11" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 8.5h13M9.5 8.5v7" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>unit_economics.xlsx</h3><p>Per-paying-user contribution ${{{{XL_CM}}}}, LTV ≈ ${{{{XL_LTV}}}}, LTV/CAC ≈ {{{{XL_RATIO}}}}, sensitivity to price and churn.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/unit_economics.xlsx" target="_blank" rel="noopener">Open workbook{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 15V9M8 15V5M12 15v-4M16 15V7" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>growth_model.xlsx</h3><p>A 12-month growth model: the funnel visits → signups → activations → paying users → MRR, cross-checked against the beta expectation.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/growth_model.xlsx" target="_blank" rel="noopener">Open workbook{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><path d="M3 10h14M10 3c2.5 2.2 2.5 11.8 0 14M10 3c-2.5 2.2-2.5 11.8 0 14" stroke="currentColor" stroke-width="1.2"/></svg></div><h3>cohort_retention.xlsx</h3><p>Weekly retention cohorts: return rates of activated and paying users — the base for the validation plan.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/cohort_retention.xlsx" target="_blank" rel="noopener">Open workbook{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/><circle cx="10" cy="10" r="3.6" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>market_sizing.xlsx</h3><p>The addressable online-recruiting market: {{{{MF5_VALUE}}}} as the base, the conservative floor of the estimate range, and the path to SOM through conversion rates.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/attachments/market_sizing.xlsx" target="_blank" rel="noopener">Open workbook{ARROW}</a></div></article>
    </div>
  </div>
</section>

<section id="shots" aria-labelledby="shots-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The product</div>
      <h2 id="shots-h">cvstart.org <span class="acc">screenshots</span></h2>
      <p>The live open-source product the agent worked on throughout the run: a landing page in two locales, a job-search dashboard with AI scoring, a job map and an application tracker.</p>
    </div>
    <div class="shots">
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_ru.jpg" width="960" height="1600" alt="cvstart.org landing page in the Russian locale" loading="lazy" decoding="async"><figcaption>The landing page in the Russian locale: free-to-use positioning, job-board scanning, interface languages.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_landing_en.jpg" width="960" height="1600" alt="cvstart.org landing page in the English locale" loading="lazy" decoding="async"><figcaption>The same landing page in the English locale — one codebase, language versions with hreflang.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_ru.jpg" width="1600" height="1000" alt="cvstart.org job-search dashboard in the Russian locale" loading="lazy" decoding="async"><figcaption>The dashboard: AI vacancy scoring against your resume — the core of the product.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_dash_en.jpg" width="1600" height="1000" alt="cvstart.org job-search dashboard in the English locale" loading="lazy" decoding="async"><figcaption>The English version of the dashboard: fit scoring, job-board filters.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_map_en.jpg" width="1600" height="1487" alt="cvstart.org job map" loading="lazy" decoding="async"><figcaption>The job map: offer geography on top of the job-board scan.</figcaption></figure>
      <figure class="shot"><img src="{{{{A}}}}assets/cv_tracker_en.jpg" width="1600" height="1000" alt="cvstart.org application tracker" loading="lazy" decoding="async"><figcaption>The application tracker with follow-ups: the application funnel between job-search sessions.</figcaption></figure>
    </div>
  </div>
</section>

<section id="evidence" aria-labelledby="ev-h">
  <div class="wrap">
    <div class="head">
      <div class="label">The evidence base</div>
      <h2 id="ev-h">Run registries, <span class="acc">in the open</span></h2>
      <p>Nothing is hidden: the full report, sources with URLs and the claim registry live in the demo project repository.</p>
    </div>
    <div class="grid">
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M6 3h8l2 3v11H4V6l2-3Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div><h3>REPORT.md</h3><p>The run’s full document: brief, situation, options, strategies, validation plan, decision — with a C### tag on every number.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/outputs/REPORT.md" target="_blank" rel="noopener">Open{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 10h6M10 4v12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="10" cy="10" r="7.2" stroke="currentColor" stroke-width="1.6"/></svg></div><h3>sources/ — {{{{D_SOURCES}}}} sources</h3><p>Market digests with URLs, retrieval dates and hashes; the allowed domains are set in project.json.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/sources" target="_blank" rel="noopener">The source folder{ARROW}</a></div></article>
      <article class="card"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><rect x="4" y="3" width="12" height="14" rx="2.5" stroke="currentColor" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>claims.jsonl — {{{{D_CLAIMS}}}} claims</h3><p>Each with a type (fact, hypothesis, forecast, assumption, inference), an A–D grade and a source. Synthetic entries are tagged origin=synthetic — hypotheses, not proven demand.</p><div class="ctas"><a class="pill pill-b pill-sm" href="{DEMO_DIR}/claims.jsonl" target="_blank" rel="noopener">The registry{ARROW}</a></div></article>
    </div>
    <div class="grid" style="margin-top:16px">
      <article class="card w6"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="4.5" stroke="currentColor" stroke-width="1.6"/><path d="M11.5 11.5 16 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div><h3>cvstart.org — the product site</h3><p>The live product in this demo: an AI resume builder and job-search dashboard, a local mode, open source.</p><div class="ctas"><a class="pill pill-b pill-sm" href="https://cvstart.org/" target="_blank" rel="noopener" data-goal="github_click">Open the site{ARROW}</a></div></article>
      <article class="card w6"><div class="ic"><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M7 4h6v3H7zM4 13h5v3H4zM11 13h5v3h-5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M10 7v3M6.5 10h7" stroke="currentColor" stroke-width="1.4"/></svg></div><h3>career-ops-ui — the repository</h3><p>The demo product’s source code: job-board scanning, AI scoring, CV Studio, a tracker, a job map.</p><div class="ctas"><a class="pill pill-b pill-sm" href="https://github.com/Fighter90/career-ops-ui" target="_blank" rel="noopener" data-goal="github_click">Open the repository{ARROW}</a></div></article>
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
      <div class="eyebrow">The same package — for your task</div>
      <h2 id="fin-h">Build one <span class="acc">for your committee</span></h2>
      <p class="muted" style="margin:0;max-width:34em">Install the agent, describe the task — and get the same set: registries, strategies, a six-pager and Excel workbooks.</p>
      <div class="ctas">
        <a class="pill pill-a" href="index.html#install" data-goal="cta_install_click">Install{ARROW}</a>
        <a class="pill pill-b" href="{GH}" data-goal="github_click">GitHub{ARROW}</a>
      </div>
    </div>
  </div>
</section>

</main>

{FOOTER_SUB_EN}"""

# OG-картинки по языкам (ТЗ PRO-66, замечание ревью раунда 2): og-ru — фото-частицы
# из hero (dark-hero-paper), og-en — стопка документов из финального CTA
# (dossier-dark). Файлы реально разные, текста на фото нет: язык расшаренной
# ссылки соцсеть подписывает из og:title/og:description. Страницы demo/help/
# materials используют те же картинки (обложка demo — dark-hero-paper в webp/
# avif, см. DEMO_BODY_*; og:image — та же пара og-ru/og-en).
OG_IMAGES = {
    "ru": ("assets/og/og-ru.jpg", 1800, 1012),
    "en": ("assets/og/og-en.jpg", 1800, 1012),
}


def _og(lang: str, title: str, desc: str, canonical: str) -> str:
    rel, w, h = OG_IMAGES[lang]
    return f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="{'Стратег Фабрики продуктов' if lang == 'ru' else 'Product Factory Strategist'}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/{rel}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">"""


def build(out: Path, ym_id: str | None) -> list[Path]:
    tokens = {}
    tokens.update(repo_numbers())
    tokens.update(demo_numbers())
    tokens.update(claim_facts())
    tokens.update(excel_numbers())
    tokens.update(demo_request())
    tokens.update(market_facts())
    tokens.update(product_facts())
    tokens.update(decision_details())
    tokens["YM"] = YM_LOADER.replace("@ID@", ym_id) if ym_id else ""

    ru_title = "Стратег Фабрики продуктов — ИИ-агент для руководителя продукта"
    ru_desc = ("Агент проводит исследование и собирает стратегию, которую можно проверить: "
               "источник у каждого числа, разные варианты, six-pager для комитета и "
               "сопровождение решения.")
    en_title = "Product Factory Strategist — an AI agent for product leads"
    en_desc = ("The agent runs real research and builds a strategy you can check: a source for "
               "every number, genuinely different options, a committee six-pager and follow-up "
               "after the decision.")

    # Пер-языковые подстановки: KIND/TEXT/SEG/DATE/USAGE/REVIEW/YOU/RQ/MF*/D_* —
    # RU берёт значения реестра как есть, EN — переводы, сверенные по числам.
    def lang_map(lang: str) -> dict:
        en = lang == "en"
        m = dict(tokens)
        m.update({
            "KIND": tokens["KIND_EN" if en else "KIND_RU"],
            "TEXT": tokens["TEXT_EN" if en else "TEXT"],
            "SEG": tokens["SEG_EN" if en else "SEG_RU"],
            "DATE": tokens["DATE_EN" if en else "DATE_RU"],
            "USAGE": tokens["USAGE_EN" if en else "USAGE_RU"],
            "REVIEW": tokens["REVIEW_EN" if en else "REVIEW_RU"],
            "DOM": tokens["C_DOM"],
            "A": "../" if en else "",
            "BRAND": BRAND_SVG,
            "YOU": "you" if en else "вы",
            "RQ": tokens["RQ_EN" if en else "RQ_RU"],
            "PRODUCT": tokens["PRODUCT_EN" if en else "PRODUCT"],
            "PRODUCT_SRC": tokens["PRODUCT_SRC"],
            "D_TITLE": tokens["D_TITLE_EN" if en else "D_TITLE"],
            "D_METRIC": tokens["D_METRIC_EN" if en else "D_METRIC"],
            "D_COMMIT": tokens["D_COMMIT_EN" if en else "D_COMMIT"],
            "D_TRIGGER": tokens["D_TRIGGER_EN" if en else "D_TRIGGER"],
            "D_DUE": tokens["D_DUE_EN" if en else "D_DUE_RU"],
            "D_BY": tokens["D_BY_EN" if en else "D_BY_RU"],
        })
        if en:
            # метка выбранного варианта — EN-перевод, не текст русского 03_options.md
            m["D_LABEL"] = tokens["D_LABEL_EN"]
        for i in range(len(MARKET_FACTS)):
            m[f"MF{i}_VALUE"] = tokens[f"MF{i}_VALUE_EN"] if en else tokens[f"MF{i}_VALUE"]
        return m

    ru, en = lang_map("ru"), lang_map("en")

    # Шапки подстраниц: активный пункт и парный переключатель языка — raw-токен NAV
    ru["NAV"] = _subnav("ru", "demo", "en/demo.html")
    en["NAV"] = _subnav("en", "demo", "../demo.html")
    ru_demo = _page("ru", "Демо-разбор CVStart — от запроса до решения",
                    "Сквозной прогон агента на живом open-source продукте cvstart.org: "
                    "дословный запрос, рынок с источниками, варианты и red team, "
                    "six-pager RU и EN и решение D001 с обязательствами.",
                    f"{BASE}/demo.html", _hreflangs(f"{BASE}/demo.html", f"{BASE}/en/demo.html"),
                    _og("ru", "Демо-разбор CVStart — от запроса до решения",
                        "Дословный запрос, рынок с источниками, варианты и red team, "
                        "six-pager RU и EN и решение D001.", f"{BASE}/demo.html"),
                    DEMO_BODY_RU, ru)
    en_demo = _page("en", "CVStart demo walkthrough — from a request to a decision",
                    "An end-to-end run of the agent on the live open-source product "
                    "cvstart.org: the verbatim request, the market with sources, red-teamed "
                    "options, a RU and EN six-pager and decision D001 with commitments.",
                    f"{BASE}/en/demo.html", _hreflangs(f"{BASE}/demo.html", f"{BASE}/en/demo.html"),
                    _og("en", "CVStart demo walkthrough — from a request to a decision",
                        "The verbatim request, the market with sources, red-teamed options, "
                        "a six-pager in two languages and decision D001.",
                        f"{BASE}/en/demo.html"),
                    DEMO_BODY_EN, en)
    ru["NAV"] = _subnav("ru", "help", "en/help.html")
    en["NAV"] = _subnav("en", "help", "../help.html")
    ru_help = _page("ru", "Справка — Стратег Фабрики продуктов",
                    "Как пользоваться агентом: три вида сообщений, управляющие фразы, "
                    "быстрый старт, цикл из 12 шагов, среды и ответы на частые вопросы.",
                    f"{BASE}/help.html", _hreflangs(f"{BASE}/help.html", f"{BASE}/en/help.html"),
                    _og("ru", "Справка — Стратег Фабрики продуктов",
                        "Управляющие фразы, команды, цикл из 12 шагов и частые вопросы.",
                        f"{BASE}/help.html"),
                    HELP_BODY_RU, ru)
    en_help = _page("en", "Help — Product Factory Strategist",
                    "How to work with the agent: three kinds of messages, control phrases, "
                    "a quick start, the twelve-step cycle, supported tools and FAQ.",
                    f"{BASE}/en/help.html", _hreflangs(f"{BASE}/help.html", f"{BASE}/en/help.html"),
                    _og("en", "Help — Product Factory Strategist",
                        "Control phrases, commands, the twelve-step cycle and FAQ.",
                        f"{BASE}/en/help.html"),
                    HELP_BODY_EN, en)
    ru["NAV"] = _subnav("ru", "materials", "en/materials.html")
    en["NAV"] = _subnav("en", "materials", "../materials.html")
    ru_mat = _page("ru", "Материалы демо CVStart — six-pager, Excel, реестры",
                   "Все материалы прогона на cvstart.org: six-pager комитета в двух языках "
                   "и трёх форматах, четыре книги Excel, скриншоты продукта и реестры "
                   "источников и утверждений.",
                   f"{BASE}/materials.html",
                   _hreflangs(f"{BASE}/materials.html", f"{BASE}/en/materials.html"),
                   _og("ru", "Материалы демо CVStart — six-pager, Excel, реестры",
                       "Six-pager в двух языках и трёх форматах, книги Excel, реестры "
                       "источников и утверждений.", f"{BASE}/materials.html"),
                   MAT_BODY_RU, ru)
    en_mat = _page("en", "CVStart demo materials — six-pager, Excel, registries",
                   "Everything the CVStart run produced: a committee six-pager in two "
                   "languages and three formats, four Excel workbooks, product screenshots "
                   "and the source and claim registries.",
                   f"{BASE}/en/materials.html",
                   _hreflangs(f"{BASE}/materials.html", f"{BASE}/en/materials.html"),
                   _og("en", "CVStart demo materials — six-pager, Excel, registries",
                       "A six-pager in two languages and three formats, Excel workbooks, "
                       "the source and claim registries.", f"{BASE}/en/materials.html"),
                   MAT_BODY_EN, en)

    ru_page = _page("ru", ru_title, ru_desc, f"{BASE}/", _hreflangs(f"{BASE}/", f"{BASE}/en/"),
                    _og("ru", ru_title, ru_desc, f"{BASE}/"), RU_BODY, ru)
    en_page = _page("en", en_title, en_desc, f"{BASE}/en/", _hreflangs(f"{BASE}/", f"{BASE}/en/"),
                    _og("en", en_title, en_desc, f"{BASE}/en/"), EN_BODY, en)

    written = []
    for rel, content in ((Path("index.html"), ru_page),
                         (Path("en") / "index.html", en_page),
                         (Path("demo.html"), ru_demo),
                         (Path("en") / "demo.html", en_demo),
                         (Path("help.html"), ru_help),
                         (Path("en") / "help.html", en_help),
                         (Path("materials.html"), ru_mat),
                         (Path("en") / "materials.html", en_mat)):
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
