#!/usr/bin/env python3
"""Статическая сборка сайта RU/EN — PRO-61.

Источники:
  site/src/<page>.html    — двуязычные шаблоны: пары элементов lang="ru"/lang="en",
                            плейсхолдеры {{KEY}} для чисел демо и aria-подписей,
                            маркер <!--LANGSWITCH--> для переключателя языка;
  site/i18n/{ru,en}.json  — словарь строк страниц: {page: {key: text}}, page = index,
                            demo, help, materials (+ "_ui" — подписи интерфейса);
                            извлекается из шаблонов командой сборки (--extract);
  projects/демо           — числа демо-проекта (источники, утверждения, экономика,
                            пороги, даты) подставляются при сборке, не руками.

Результат:
  <out>/<page>.html       — русская версия (hreflang x-default);
  <out>/en/<page>.html    — английская версия.
Обе версии статические: без body[data-lang] и JS-переключалки, счётчики
предзаполнены — краулеры, превью ссылок и WebFetch видят готовый текст одного языка.

API для тестов: load_demo_data(), extract_all(), build(out_dir=…, extract=…).
Запуск: python3 scripts/build_site.py [--out site] [--extract]
"""
import argparse
import datetime as dt
import html as html_mod
import json
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGES = ["index", "demo", "help", "materials"]
VOID_TAGS = {"meta", "link", "br", "hr", "img", "input", "source", "track", "wbr",
             "area", "base", "col", "embed", "param"}

# подписи интерфейса, которых нет в шаблонах (aria-метки схем, поиск, переключатель)
UI_STRINGS = {
    "ARIA_LANG": {"ru": "Язык", "en": "Language"},
    "ARIA_TIMELINE": {"ru": "Таймлайн 12 шагов", "en": "Timeline of the 12 steps"},
    "ARIA_STEPS": {"ru": "Алгоритм агента: 12 шагов", "en": "Agent algorithm: 12 steps"},
    "ARIA_ECON": {"ru": "Экономика платящего CVStart", "en": "CVStart paying-user economics"},
    "ARIA_FLOW": {"ru": "Схема: материалы — источники — утверждения — варианты — стратегии — решение",
                  "en": "Diagram: materials — sources — claims — options — strategies — decision"},
    "ARIA_HELPNAV": {"ru": "Разделы справки", "en": "Help sections"},
    "ARIA_SEARCH": {"ru": "Поиск по справке", "en": "Search the help"},
    "SEARCH_PH": {"ru": "Поиск по справке…", "en": "Search the help…"},
}


# ── форматирование чисел ────────────────────────────────────────────────

def _rnd(v, nd: int) -> str:
    """Округление half-up, чтобы совпадать с six-pager (271,875 → 271,88)."""
    q = Decimal(1).scaleb(-nd)
    return str(Decimal(str(v)).quantize(q, rounding=ROUND_HALF_UP))


def fmt(v, lang: str, nd: int = 2) -> str:
    s = _rnd(v, nd) if nd > 0 else _rnd(v, 0)
    return s.replace(".", ",") if lang == "ru" else s


# ── числа демо-проекта ──────────────────────────────────────────────────

def _jsonl(path: Path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _plan_numbers(demo: Path) -> dict:
    """Пороги и модель воронки — из outputs/06_validation_plan.md демо-проекта."""
    plan = (demo / "outputs" / "06_validation_plan.md").read_text(encoding="utf-8")
    m_cont = re.search(r"paid ≥ (\d+) к нед\. (\d+), activation ≥ (\d+)%, churn платящих ≤ (\d+)%", plan)
    m_stop = re.search(r"paid < (\d+) к нед\. \d+ при activation < (\d+)%", plan)
    m_change = re.search(r"paid < (\d+) к нед\. \d+ при activation ≥ (\d+)%", plan)
    m_high = re.search(r"paid (\d+)–(\d+)", plan)
    m_model = re.search(r"модель: (\d+)\), MRR ≥ \$([\d\s]+)", plan)
    m_mrr12 = re.search(r"\(MRR \$([\d\s]+)\)", plan)
    if not (m_cont and m_stop and m_change and m_high and m_model and m_mrr12):
        raise SystemExit("build_site: не удалось разобрать пороги из 06_validation_plan.md")
    paid_target, funnel_weeks, act_target, churn_max = (int(m_cont.group(i)) for i in range(1, 5))
    mrr_w12 = int(m_mrr12.group(1).replace(" ", "").replace("\u00a0", ""))
    return {
        "paid_target": paid_target,
        "funnel_weeks": funnel_weeks,
        "act_target": act_target,
        "churn_max": churn_max,
        "paid_low": int(m_stop.group(1)),
        "act_stop": int(m_stop.group(2)),
        "paid_change": int(m_change.group(1)),
        "act_change": int(m_change.group(2)),
        "paid_high": int(m_high.group(2)),
        "paid_w12": int(m_model.group(1)),
        "mrr_target": int(m_model.group(2).replace(" ", "").replace("\u00a0", "")),
        "mrr_w12": mrr_w12,
    }


def _claim_numbers(claims: list) -> dict:
    """Рынок и CAGR — из утверждений C005 (resume builders) и C011 (рекрутинг)."""
    def claim(cid):
        c = next((c for c in claims if c["id"] == cid), None)
        if c is None:
            raise SystemExit(f"build_site: в демо нет утверждения {cid}")
        return c["text"]
    m = re.search(r"\$([\d,]+)–([\d,]+) млрд", claim("C005"))
    g = re.search(r"CAGR ([\d,]+)%", claim("C005"))
    r = re.search(r"\$([\d,]+) млрд", claim("C011"))
    rc = re.search(r"CAGR ([\d,]+)%", claim("C011"))
    if not (m and g and r and rc):
        raise SystemExit("build_site: не удалось разобрать рынок/CAGR из C005/C011")
    f = lambda s: float(s.replace(",", "."))
    return {
        "market_lo": f(m.group(1)), "market_hi": f(m.group(2)), "ai_cagr": f(g.group(1)),
        "recruit_market": f(r.group(1)), "recruit_cagr": f(rc.group(1)),
    }


def _id_range(ids: list[str]) -> str:
    """Компактная запись ряда ID: сплошной ряд — «S001–S003», ряд с дыркой —
    явным перечислением «S001–S002, S004–S011» (PRO-63: нумерация с дыркой
    не должна показываться как сплошная)."""
    nums = sorted(int(x[1:]) for x in ids)
    runs: list[list[int]] = []
    for n in nums:
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    prefix = ids[0][0] if ids else "S"
    return ", ".join(f"{prefix}{a:03d}–{prefix}{b:03d}" if b > a else f"{prefix}{a:03d}"
                     for a, b in ((r[0], r[-1]) for r in runs))


def load_demo_data(repo: Path = REPO) -> dict:
    """Числа демо-проекта для подстановки в {{KEY}}: из sources/claims/calcs/decisions/06.

    Сайт не «набивается руками»: после пересборки демо (PRO-51/PRO-46) сборка сайта
    сама подхватит обновлённые цифры.
    """
    demo = repo / "projects" / "демо"
    sources = _jsonl(demo / "sources.jsonl")
    claims = _jsonl(demo / "claims.jsonl")
    calcs = json.loads((demo / "calcs.json").read_text(encoding="utf-8"))
    decisions = _jsonl(demo / "decisions.jsonl")
    d1 = decisions[0]

    ue = calcs["unit_econ"]
    arpu = float(ue["arpu"]); cac = float(ue["cac"]); churn = float(ue["churn_month"])
    vc_share = float(ue["vc_share"])
    cm = arpu * (1 - vc_share)                       # 21.75
    ltv = cm / churn                                 # 271.875 → 271,88
    ltv_cac = ltv / cac                              # 4.53
    payback = cac / cm                               # 2.8 мес

    s_ids = sorted(s["id"] for s in sources)
    c_ids = sorted(c["id"] for c in claims)
    commit_m = re.search(r"\d{4}-\d{2}-\d{2}", d1["commitments"][0]["due"])
    if not commit_m:
        raise SystemExit("build_site: в обязательстве D001 нет даты")
    commit = dt.date.fromisoformat(commit_m.group())
    review = dt.date.fromisoformat(d1["review"]["date"])
    weeks = round((review - commit).days / 7)

    m_price = re.search(r"Pro \$(\d+) / Unlimited \$(\d+)", d1.get("decision", ""))
    if not m_price:
        raise SystemExit("build_site: не удалось разобрать тарифы Pro/Unlimited из D001")

    plan = _plan_numbers(demo)
    data = {
        "sources_count": len(sources),
        "s_range": _id_range(s_ids),
        "claims_count": len(claims),
        "c_range": _id_range(c_ids),
        "arpu": arpu, "cac": cac, "churn": churn, "vc_share": vc_share,
        "cm": cm, "ltv": ltv, "ltv_cac": ltv_cac, "payback": payback,
        "vc_abs": arpu * vc_share,
        "decision_id": d1["id"],
        "commit_date": commit.isoformat(),
        "review_date": review.isoformat(),
        "beta_weeks": weeks,
        "pro_price": "$" + m_price.group(1),
        "unlimited_price": "$" + m_price.group(2),
        "arr_w12": int(Decimal(str(plan["mrr_w12"] * 12 / 1000)).quantize(Decimal(1), rounding=ROUND_HALF_UP)),
    }
    data.update(plan)
    data.update(_claim_numbers(claims))
    data["breakeven"] = math.ceil(data["mrr_target"] / cm) if cm else 0
    return data


def demo_placeholders(data: dict) -> dict:
    """{{KEY}} → (kind, value); рендер в render_value()."""
    return {
        "SOURCES_COUNT": ("int", data["sources_count"]),
        "S_RANGE": ("str", data["s_range"]),
        "CLAIMS_COUNT": ("int", data["claims_count"]),
        "C_RANGE": ("str", data["c_range"]),
        "ARPU": ("int", data["arpu"]),
        "CAC": ("int", data["cac"]),
        "VC_PCT": ("pct", data["vc_share"] * 100),
        "VC_NEG": ("vcneg", data["vc_abs"]),
        "CM": ("money", data["cm"]),
        "LTV": ("money", data["ltv"]),
        "LTV_CAC": ("num2", data["ltv_cac"]),
        "PAYBACK": ("num1", data["payback"]),
        "BREAKEVEN": ("int", data["breakeven"]),
        "DECISION_ID": ("str", data["decision_id"]),
        "COMMIT_DATE": ("str", data["commit_date"]),
        "REVIEW_DATE": ("str", data["review_date"]),
        "BETA_WEEKS": ("int", data["beta_weeks"]),
        "PAID_TARGET": ("int", data["paid_target"]),
        "PAID_LOW": ("int", data["paid_low"]),
        "PAID_CHANGE_LOW": ("int", data["paid_change"]),
        "PAID_HIGH": ("int", data["paid_high"]),
        "ACT_TARGET": ("int", data["act_target"]),
        "ACT_STOP": ("int", data["act_stop"]),
        "ACT_CHANGE": ("int", data["act_change"]),
        "CHURN_MAX": ("int", data["churn_max"]),
        "FUNNEL_WEEKS": ("int", data["funnel_weeks"]),
        "PAID_W12": ("int", data["paid_w12"]),
        "MRR_TARGET": ("mrr", data["mrr_target"]),
        "MRR_W12": ("mrr", data["mrr_w12"]),
        "ARR_W12": ("int", data["arr_w12"]),
        "MARKET": ("market", (data["market_lo"], data["market_hi"])),
        "AI_CAGR": ("pct", data["ai_cagr"]),
        "RECRUIT_MARKET": ("recruit", data["recruit_market"]),
        "RECRUIT_CAGR": ("pct", data["recruit_cagr"]),
        "PRO_PRICE": ("str", data["pro_price"]),
        "UNLIMITED_PRICE": ("str", data["unlimited_price"]),
    }


def render_value(kind, val, lang: str) -> str:
    if kind == "int":
        return fmt(val, lang, 0)
    if kind == "str":
        return val
    if kind == "pct":
        return fmt(val, lang, 1 if val % 1 else 0) + "%"
    if kind == "money":
        return "$" + fmt(val, lang, 2)
    if kind == "num2":
        return fmt(val, lang, 2)
    if kind == "num1":
        return fmt(val, lang, 1)
    if kind == "vcneg":
        return "-$" + fmt(val, lang, 2)
    if kind == "mrr":
        s = str(int(val))
        return ("$" + s[:-3] + " " + s[-3:]) if lang == "ru" and len(s) > 3 else ("$" + format(int(val), ","))
    if kind == "market":
        lo, hi = val
        return f"${fmt(lo, lang, 1)}–{fmt(hi, lang, 1)} " + ("млрд" if lang == "ru" else "B")
    if kind == "recruit":
        return "$" + fmt(val, lang, 2) + (" млрд" if lang == "ru" else "B")
    raise SystemExit(f"build_site: неизвестный тип значения {kind}")


# ── извлечение словаря строк из шаблонов ────────────────────────────────

class _PairExtractor(HTMLParser):
    """Собирает пары lang="ru"/lang="en" в порядке документа (тело страницы).

    title и meta description учитываются отдельно (_MetaExtractor), og:title и
    og:description пропускаются (дублируют мету). Элементы с классом ru-only /
    en-only — односторонний контент (например, таблица CLI только в RU, в EN —
    абзац-резюме) — в словарь не попадают. Ключи пар — "k001"…"kNNN".
    """

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ru, self.en = [], []
        self._cur = None      # (lang, bucket_list, parts)
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        lang = d.get("lang")
        cls = d.get("class", "")
        if self._cur is None:
            if (lang in ("ru", "en") and tag not in VOID_TAGS
                    and tag not in ("html", "title", "meta")
                    and "ru-only" not in cls and "en-only" not in cls):
                self._cur = (lang, self.ru if lang == "ru" else self.en, [])
                self._depth = 1
            return
        if tag not in VOID_TAGS:
            self._depth += 1

    def handle_startendtag(self, tag, attrs):
        # самозакрытый тег не меняет глубину и не содержит текста
        pass

    def handle_endtag(self, tag):
        if self._cur is not None and tag not in VOID_TAGS:
            self._depth -= 1
            if self._depth <= 0:
                lang, bucket, parts = self._cur
                bucket.append(re.sub(r"\s+", " ", html_mod.unescape("".join(parts))).strip())
                self._cur = None

    def handle_data(self, data):
        if self._cur is not None:
            self._cur[2].append(data)

    def handle_entityref(self, name):
        if self._cur is not None:
            self._cur[2].append(html_mod.unescape(f"&{name};"))

    def handle_charref(self, name):
        if self._cur is not None:
            self._cur[2].append(html_mod.unescape(f"&#{name};"))


class _MetaExtractor(HTMLParser):
    """title и meta[name=description] с lang — ключи title/description словаря."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.meta = {"ru": {}, "en": {}}
        self._t = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        lang = d.get("lang")
        if lang not in ("ru", "en"):
            return
        if tag == "title":
            self._t = lang
        elif tag == "meta" and d.get("name") == "description":
            self.meta[lang]["description"] = re.sub(r"\s+", " ", html_mod.unescape(d.get("content", ""))).strip()

    def handle_data(self, data):
        if self._t:
            self.meta[self._t]["title"] = re.sub(r"\s+", " ", data).strip()
            self._t = None

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = None


def extract_all(repo: Path = REPO) -> dict:
    """Словарь строк страниц из site/src: {"ru": {page: {key: text}}, "en": …}."""
    src_dir = repo / "site" / "src"
    out = {"ru": {"_ui": {}}, "en": {"_ui": {}}}
    for lang in ("ru", "en"):
        out[lang]["_ui"] = {k: v[lang] for k, v in UI_STRINGS.items()}
    for page in PAGES:
        src = (src_dir / f"{page}.html").read_text(encoding="utf-8")
        p = _PairExtractor()
        p.feed(src)
        p.close()
        m = _MetaExtractor()
        m.feed(src)
        m.close()
        if len(p.ru) != len(p.en):
            raise SystemExit(
                f"build_site: {page}: пары ru/en не совпадают ({len(p.ru)} vs {len(p.en)})")
        d_ru, d_en = {}, {}
        d_ru.update(m.meta["ru"]); d_en.update(m.meta["en"])
        for i, (ru_t, en_t) in enumerate(zip(p.ru, p.en), 1):
            d_ru[f"k{i:03d}"] = ru_t
            d_en[f"k{i:03d}"] = en_t
        out["ru"][page] = d_ru
        out["en"][page] = d_en
    return out


# ── фильтр языка (html.parser, сохраняет исходное форматирование) ───────

class LangFilter(HTMLParser):
    """Пропускает элементы чужого языка, сохраняет байты совпадающих.

    Локаль наследуется от ближайшего предка с lang; начатый пропуск длится до
    закрытия элемента (вложенные lang внутри чужого блока не «спасают»).
    <title>, meta description/og:title/og:description выбрасываются всегда —
    сборка вставляет их из словаря site/i18n.
    """

    def __init__(self, lang: str):
        super().__init__(convert_charrefs=False)
        self.lang = lang
        self.out = []
        self.stack = []  # (tag, skipping)

    def _skipping(self):
        return any(s for _, s in self.stack)

    @staticmethod
    def _own_lang(attrs):
        for k, v in attrs:
            if k == "lang":
                return v
        return None

    @staticmethod
    def _is_meta_drop(attrs):
        d = dict(attrs)
        return d.get("name") == "description" or d.get("property") in ("og:title", "og:description")

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            self.out.append(f'<html lang="{self.lang}">')
            self.stack.append(("html", False))
            return
        if tag in VOID_TAGS:
            if not self._skipping():
                own = self._own_lang(attrs)
                if (own is None or own == self.lang) and not self._is_meta_drop(attrs):
                    self.out.append(self.get_starttag_text())
            return
        if self._skipping():
            self.stack.append((tag, True))
            return
        own = self._own_lang(attrs)
        skip = (own is not None and own != self.lang) or tag == "title" or self._is_meta_drop(attrs)
        self.stack.append((tag, skip))
        if not skip:
            self.out.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if tag == "html":
            self.out.append(f'<html lang="{self.lang}">')
            return
        if self._skipping():
            return
        own = self._own_lang(attrs)
        if self._is_meta_drop(attrs):
            return
        if own is not None and own != self.lang:
            return
        self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            _, skip = self.stack.pop()
            if not skip:
                self.out.append(f"</{tag}>")
        elif not self._skipping():
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self._skipping():
            self.out.append(data)

    def handle_entityref(self, name):
        if not self._skipping():
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self._skipping():
            self.out.append(f"&#{name};")

    def handle_comment(self, data):
        # маркер переключателя проходит насквозь — заменяется после сериализации
        if not self._skipping():
            self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.out.append(f"<!{decl}>")

    def handle_pi(self, data):
        self.out.append(f"<?{data}>")


def switch_html(page: str, lang: str) -> str:
    if lang == "ru":
        return (f'<a href="{page}.html" class="on" aria-current="true">RU</a>'
                f'<a href="en/{page}.html">EN</a>')
    return (f'<a href="../{page}.html">RU</a>'
            f'<a href="{page}.html" class="on" aria-current="true">EN</a>')


def build_page(src: str, page: str, lang: str, meta: dict, domain: str, values: dict, ui: dict) -> str:
    p = LangFilter(lang)
    p.feed(src)
    p.close()
    html = "".join(p.out)

    head = (
        f"<title>{meta['title']}</title>\n"
        f'<meta name="description" content="{html_mod.escape(meta["description"], quote=True)}">\n'
        f'<meta property="og:title" content="{html_mod.escape(meta["title"], quote=True)}">\n'
        f'<meta property="og:description" content="{html_mod.escape(meta["description"], quote=True)}">\n'
        f'<link rel="canonical" href="https://{domain}/{"" if lang == "ru" else "en/"}{page}.html">\n'
        f'<link rel="alternate" hreflang="ru" href="https://{domain}/{page}.html">\n'
        f'<link rel="alternate" hreflang="en" href="https://{domain}/en/{page}.html">\n'
        f'<link rel="alternate" hreflang="x-default" href="https://{domain}/{page}.html">'
    )
    marker = '<meta charset="UTF-8">'
    if marker not in html:
        raise SystemExit(f"build_site: {page}: нет {marker}")
    html = html.replace(marker, marker + "\n" + head, 1)

    def repl(m):
        key = m.group(1)
        if key in values:
            return render_value(*values[key], lang)
        if key in ui:
            return ui[key]
        raise SystemExit(f"build_site: {page}: неизвестный плейсхолдер {{{{{key}}}}}")

    html = re.sub(r"\{\{([A-Z_0-9]+)\}\}", repl, html)
    html = html.replace("<!--LANGSWITCH-->", switch_html(page, lang))

    if lang == "en":
        # EN живёт в /en/: ассеты и ссылки на RU-дом уровнем выше
        html = re.sub(r'((?:src|href)=")assets/', r"\1../assets/", html)
        html = html.replace('href="index.html"', 'href="../index.html"')
    html = re.sub(r"\n{3,}", "\n\n", html)
    if "{{" in html or "LANGSWITCH" in html:
        raise SystemExit(f"build_site: {page}/{lang}: остались неразрешённые маркеры")
    return html


def build(out_dir=None, extract: bool = False, repo: Path = REPO) -> None:
    """Собирает RU- и EN-версии всех страниц.

    extract=True — дополнительно перезаписывает site/i18n/{ru,en}.json из шаблонов.
    """
    out = Path(out_dir) if out_dir else repo / "site"
    src_dir = repo / "site" / "src"
    i18n_dir = repo / "site" / "i18n"
    dicts = extract_all(repo)
    if extract:
        i18n_dir.mkdir(parents=True, exist_ok=True)
        for lang in ("ru", "en"):
            (i18n_dir / f"{lang}.json").write_text(
                json.dumps(dicts[lang], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    cname_f = repo / "site" / "CNAME"
    domain = cname_f.read_text(encoding="utf-8").strip() if cname_f.exists() else "strategyproduct.ru"
    values = demo_placeholders(load_demo_data(repo))
    for page in PAGES:
        src = (src_dir / f"{page}.html").read_text(encoding="utf-8")
        for lang in ("ru", "en"):
            meta = dicts[lang][page]
            html = build_page(src, page, lang, meta, domain, values, dicts[lang]["_ui"])
            dest = out / (f"en/{page}.html" if lang == "en" else f"{page}.html")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(html, encoding="utf-8")
            print(f"ok  {dest}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Статическая сборка сайта RU/EN из site/src + site/i18n")
    ap.add_argument("--out", default="site", help="каталог вывода (по умолчанию site/)")
    ap.add_argument("--extract", action="store_true",
                    help="перезаписать site/i18n/{ru,en}.json из шаблонов перед сборкой")
    ap.add_argument("--repo", default=str(REPO), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    repo = Path(args.repo)
    out = Path(args.out)
    if not out.is_absolute():
        out = repo / out
    build(out_dir=out, extract=args.extract, repo=repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
