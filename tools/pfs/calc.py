"""Excel-приложения к six-pager: юнит-экономика, модель роста, когорты, размер рынка.

Книги строятся по образцу учебных расчётов курса «Продуктовые бизнес-модели и
юнит-экономика»: лист «Ввод» с редактируемыми параметрами + расчётные листы на
формулах — Excel пересчитывает значения при открытии, руководитель и агент могут
менять допущения, не трогая формулы. В ячейках с формулами лежит кэш значения на
момент генерации, чтобы предпросмотр показывал число до пересчёта.

Параметры берутся из projects/<slug>/calcs.json (секция с именем расчёта);
отсутствующие — заполняются примером из DEFAULTS с пометкой «ПРИМЕР».
Каркас calcs.json собирает pfs calc scaffold из 02/04/06/07: каждое найденное
число — со своим C/S-тегом в _notes, ненайденное — null + подсказка в _hints.
Запуск: pfs calc [all|unit-econ|growth|cohort|market] → outputs/attachments/*.xlsx
"""
from __future__ import annotations

import re
from pathlib import Path

from . import core
from .xlsx import Workbook

DEFAULTS: dict[str, dict] = {
    "unit_econ": {
        "arpu": 199, "vc_share": 0.2, "cac": 600, "churn_month": 0.08,
        "note": "ПРИМЕР — замените на данные проекта в calcs.json; каждое значение подкрепите C###",
    },
    "growth": {
        "mau_start": 100000, "mau_growth_month": 0.05, "conv_order": 0.02,
        "orders_per_active": 1.5, "aov": 3500, "take_rate": 0.08, "margin": 0.6,
    },
    "cohort": {
        "sizes": [5000, 6000, 5500, 7000, 6500, 8000],
        "retention": [1.0, 0.55, 0.42, 0.35, 0.30, 0.27, 0.24, 0.22, 0.21, 0.20, 0.19, 0.18],
    },
    "market": {"pam": 120_000_000_000, "tam_share": 0.6, "sam_share": 0.3, "som_share": 0.05},
}

MONTHS = 12


# ---------- юнит-экономика ----------

def unit_econ(p: dict) -> Workbook:
    arpu, vc, cac, churn = p["arpu"], p["vc_share"], p["cac"], p["churn_month"]
    cm = arpu * (1 - vc)
    life = 1 / churn if churn else 0.0
    ltv = cm * life
    wb = Workbook()
    v = wb.sheet("Ввод", widths={1: 36, 2: 13, 3: 52})
    v.row("Параметр", "Значение", "Комментарий")
    v.row("ARPU — выручка с юнита, ₽/мес", arpu, "выручка на одного активного платящего")
    v.row("Доля переменных затрат (VC)", {"v": vc, "pct": True}, "себестоимость обслуживания, платежные комиссии")
    v.row("CAC — привлечение юнита, ₽", cac, "маркетинг и промо на одного нового юнита")
    v.row("Отток в месяц (churn)", {"v": churn, "pct": True}, "доля ушедших за месяц")
    v.row("Примечание", p.get("note", ""))
    u = wb.sheet("Юнит-экономика", widths={1: 34, 2: 13, 3: 44})
    u.row("Показатель", "Значение", "Как считается")
    u.row("Валовая маржа юнита (CM), ₽/мес", {"f": "'Ввод'!B2*(1-'Ввод'!B3)", "cached": round(cm, 2)},
          "ARPU × (1 − доля VC)")
    u.row("Средний срок жизни юнита, мес", {"f": "1/'Ввод'!B5", "cached": round(life, 2)}, "1 / отток")
    u.row("LTV, ₽", {"f": "B2*B3", "cached": round(ltv, 2)}, "CM × срок жизни")
    u.row("LTV / CAC", {"f": "B4/'Ввод'!B4", "cached": round(ltv / cac, 2) if cac else 0, "bold": True},
          "орентир: ≥ 3")
    u.row("Пейбек CAC, мес", {"f": "'Ввод'!B4/B2", "cached": round(cac / cm, 2) if cm else 0},
          "CAC / CM; ориентир ≤ 12 мес")
    u.row("Доля CAC в LTV", {"f": "'Ввод'!B4/B4", "cached": round(cac / ltv, 3) if ltv else 0, "pct": True},
          "расход на привлечение в lifetime-выручке юнита")
    s = wb.sheet("Чувствительность LTV/CAC", widths={1: 18})
    vcs = [0.1, 0.2, 0.3, 0.4, 0.5]
    churns = [0.04, 0.06, 0.08, 0.10, 0.12]
    header = ["Отток ↓ / VC →"] + [{"v": x, "pct": True, "bold": True} for x in vcs]
    s.row(*header)
    for ch in churns:
        row_no = len(s.rows) + 1  # номер добавляемой строки
        row = [{"v": ch, "pct": True, "bold": True}]
        for i in range(len(vcs)):
            col = col_ref(i + 2)  # B..F — доли VC в заголовке
            row.append({"f": f"'Ввод'!$B$2*(1-{col}$2)/($A{row_no}*'Ввод'!$B$4)",
                        "cached": round(arpu * (1 - vcs[i]) / (ch * cac), 2) if cac else 0})
        s.row(*row)
    return wb


def col_ref(n: int) -> str:
    from .xlsx import col_letter
    return col_letter(n)


# ---------- модель роста (traction) ----------

def growth(p: dict) -> Workbook:
    mau, g, conv, freq, aov, take, marg = (p["mau_start"], p["mau_growth_month"], p["conv_order"],
                                           p["orders_per_active"], p["aov"], p["take_rate"], p["margin"])
    wb = Workbook()
    v = wb.sheet("Ввод", widths={1: 40, 2: 13, 3: 46})
    v.row("Параметр", "Значение", "Комментарий")
    v.row("MAU на старте", mau)
    v.row("Рост MAU, %/мес", {"v": g, "pct": True})
    v.row("Конверсия активного в заказ, %/мес", {"v": conv, "pct": True})
    v.row("Заказов на активного, шт/мес", freq)
    v.row("Средний чек (AOV), ₽", aov)
    v.row("Take rate — доля платформы в GMV", {"v": take, "pct": True})
    v.row("Валовая маржа, % от выручки", {"v": marg, "pct": True})
    m = wb.sheet("Модель 12 мес", widths={1: 26})
    head = ["Показатель"] + [f"M{i}" for i in range(1, MONTHS + 1)] + ["Σ 12 мес"]
    m.row(*head)
    mau_vals, order_vals = [], []
    for i in range(MONTHS):
        mau_vals.append(mau * (1 + g) ** i)
        order_vals.append(mau_vals[i] * conv * freq)
    def month_row(title, row_no, per_month, total):
        cells = [title]
        for i in range(MONTHS):
            letter = col_ref(i + 2)
            prev = col_ref(i + 1)
            if row_no == 2:
                f = "'Ввод'!B2" if i == 0 else f"{prev}2*(1+'Ввод'!$B$3)"
            else:
                src = {3: "2", 4: "3", 5: "4", 6: "5"}[row_no]
                factors = {3: "*'Ввод'!$B$4*'Ввод'!$B$5", 4: "*'Ввод'!$B$6",
                           5: "*'Ввод'!$B$7", 6: "*'Ввод'!$B$8"}[row_no]
                f = f"{letter}{src}{factors}"
            cells.append({"f": f, "cached": round(per_month(i), 2)})
        cells.append({"f": f"SUM(B{row_no}:M{row_no})", "cached": round(total, 2), "bold": True})
        m.row(*cells)
    month_row("MAU, чел", 2, lambda i: mau_vals[i], sum(mau_vals))
    month_row("Заказы, шт", 3, lambda i: order_vals[i], sum(order_vals))
    month_row("GMV, ₽", 4, lambda i: order_vals[i] * aov, sum(order_vals) * aov)
    month_row("Выручка платформы, ₽", 5, lambda i: order_vals[i] * aov * take, sum(order_vals) * aov * take)
    month_row("Валовая маржа, ₽", 6, lambda i: order_vals[i] * aov * take * marg, sum(order_vals) * aov * take * marg)
    return wb


# ---------- когортное удержание ----------

def cohort(p: dict) -> Workbook:
    sizes = list(p["sizes"])[:MONTHS]
    ret = list(p["retention"])[:MONTHS] + [0.0] * max(0, MONTHS - len(p["retention"]))
    wb = Workbook()
    v = wb.sheet("Ввод", widths={1: 30})
    v.row("Месяц жизни", *[f"M{i}" for i in range(MONTHS)])
    v.row("Удержание, % от когорты", *[{"v": r, "pct": True, "bold": True} for r in ret])
    for i, sz in enumerate(sizes):
        v.row(f"Размер когорты {i + 1} (вход в M{i})", sz)
    c = wb.sheet("Когорты", widths={1: 24, 2: 10})
    c.row("Когорта", "Размер", *[f"M{i}" for i in range(MONTHS)])
    for ci, sz in enumerate(sizes):
        r = ci + 2
        cells = [f"Когорта {ci + 1}", {"f": f"'Ввод'!B{4 + ci}", "cached": sz}]
        for j in range(MONTHS):
            from .xlsx import col_letter
            ret_col = col_letter(j + 2)  # B..M в «Ввод»
            cells.append({"f": f"$B{r}*'Ввод'!{ret_col}$2", "cached": round(sz * ret[j], 1)})
        c.row(*cells)
    totals = ["Активные, все когорты", None]
    for j in range(MONTHS):
        letter = col_ref(j + 3)  # C..N в «Когорты»
        total = round(sum(sz * ret[j] for sz in sizes), 1)
        totals.append({"f": f"SUM({letter}2:{letter}{len(sizes) + 1})", "cached": total, "bold": True})
    c.row(*totals)
    k = wb.sheet("Метрики удержания", widths={1: 40, 2: 12, 3: 50})
    k.row("Показатель", "Значение", "Интерпретация")
    for label, idx in (("Retention M1", 1), ("Retention M3", 3), ("Retention M6", 6)):
        from .xlsx import col_letter
        rc = col_letter(idx + 2)
        k.row(label, {"f": f"'Ввод'!{rc}2", "cached": ret[idx], "pct": True},
              "ранний провал M1–M3 — проблема ценности; плато — привычка сформирована")
    return wb


# ---------- размер рынка ----------

def market(p: dict) -> Workbook:
    pam, tam, sam, som = p["pam"], p["tam_share"], p["sam_share"], p["som_share"]
    wb = Workbook()
    v = wb.sheet("Ввод", widths={1: 40, 2: 14, 3: 50})
    v.row("Параметр", "Значение", "Комментарий")
    v.row("PAM — рынок-родитель, ₽/год", pam, "внешние обзоры: численность × частота × цена")
    v.row("Доля TAM от PAM", {"v": tam, "pct": True}, "доля рынка, которую закрывает класс решений")
    v.row("Доля SAM от TAM", {"v": sam, "pct": True}, "целевые сегменты, каналы и гео")
    v.row("Доля SOM от SAM", {"v": som, "pct": True}, "реалистичная доля за 3 года при текущих ресурсах")
    v.row("Примечание", "SOM сверьте с bottom-up: модель роста не должна противоречить")
    f = wb.sheet("Воронка", widths={1: 38, 2: 18, 3: 52})
    f.row("Уровень", "₽/год", "Как считаем")
    f.row("PAM — все, кого касается проблема", {"f": "'Ввод'!B2", "cached": pam}, "рынок-родитель")
    f.row("TAM — доступно с нашим классом продукта",
          {"f": "B2*'Ввод'!B3", "cached": round(pam * tam)}, "PAM × доля")
    f.row("SAM — целевой сегмент и гео запуска",
          {"f": "B3*'Ввод'!B4", "cached": round(pam * tam * sam)}, "TAM × доля")
    f.row("SOM — реалистичный захват, 3 года",
          {"f": "B4*'Ввод'!B5", "cached": round(pam * tam * sam * som), "bold": True}, "SAM × доля")
    p_ = wb.sheet("PESTEL", widths={1: 20, 2: 34, 3: 12, 4: 14, 5: 12, 6: 26, 7: 30})
    p_.row("Фактор", "Что происходит", "Тренд ↑/↓/→", "Влияние −3…+3", "Вероятность", "Возможность / угроза", "Действие")
    for dom in ("Политико-правовые", "Экономические", "Социальные", "Технологические", "Экологические", "Рыночные и конкуренция"):
        p_.row(dom, "", "", "", "", "", "")
    return wb


# ---------- каркас calcs.json из документов ----------

DOCS = ("02_situation.md", "04_product_strategy.md", "06_validation_plan.md", "07_quality_review.md")
ECON_HEADING = re.compile(r"^#{1,6}\s+.*эконом", re.IGNORECASE)
NUMTOK = r"\d[\d\u00a0\u202f ]*(?:[.,]\d+)?"
TAG_RE = re.compile(r"\[(C|S)(\d{1,4})\]")
RET_ANCHOR = re.compile(r"(?:удержание\w*|retention\w*)[^%\d\[]{0,12}M\s*(?P<m>\d{1,2})", re.IGNORECASE)
RET_PCT = re.compile(rf"({NUMTOK})\s*%")
MULT = {"млрд": 1e9, "млн": 1e6, "тысяч": 1e3, "тыс": 1e3}

# Спецификации поиска: секция → ключи calcs.json. re — шаблоны с группами n (число)
# и опциональной u (единица: %, млрд, млн…); docs — документы по приоритету,
# econ_first — сначала раздел «Экономика» в 04, потом весь документ.
PARAM_SPECS: dict[str, list[dict]] = {
    "unit_econ": [
        dict(key="arpu", pct=False,
             re=[rf"ARPU[^%\d\[]{{0,12}}(?P<n>{NUMTOK})(?!\s*%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="ARPU с C-тегом из «Экономики» 04, напр.: «ARPU 350 ₽/мес [C001]»"),
        dict(key="vc_share", pct=True,
             re=[rf"(?:переменн\w*|себестоимост\w*|\bVC\b)[^%\d\[]{{0,40}}(?P<n>{NUMTOK})\s*(?P<u>%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="доля переменных затрат, % — «переменные затраты 25% [C001]»"),
        dict(key="cac", pct=False,
             re=[rf"\bCAC\b[^%\d\[]{{0,12}}(?P<n>{NUMTOK})\s*(?=₽|\$|руб)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="CAC с валютой — «CAC 700 ₽ [C001]»; LTV/CAC и окупаемость CAC не подходят"),
        dict(key="churn_month", pct=True,
             re=[rf"(?:churn|отток\w*)[^%\d\[]{{0,30}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="отток в месяц, % — «churn 8%/мес [C001]» или из критериев 06"),
    ],
    "growth": [
        dict(key="mau_start", pct=False,
             re=[rf"\bMAU\b[^%\d\[]{{0,25}}(?P<n>{NUMTOK})(?!\s*%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="MAU на старте — «MAU на старте 50 000 [C001]»"),
        dict(key="mau_growth_month", pct=True,
             re=[rf"(?:рост\w*[^%\d\[]{{0,20}}\bMAU\b|\bMAU\b[^%\d\[]{{0,20}}рост\w*)[^%\d\[]{{0,20}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="рост MAU, %/мес — «рост MAU 8%/мес [C001]»"),
        dict(key="conv_order", pct=True,
             re=[rf"конверс\w*[^%\d\[]{{0,60}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,8}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="конверсия активного в заказ, %/мес — «конверсия 4%/мес [C001]»; коридор → середина"),
        dict(key="orders_per_active", pct=False,
             re=[rf"заказ\w*[^%\d\[]{{0,30}}активн\w*[^%\d\[]{{0,20}}(?P<n>{NUMTOK})(?!\s*%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="заказов на активного, шт/мес — «заказов на активного 1,5 [C001]»"),
        dict(key="aov", pct=False,
             re=[rf"(?:средн\w*\s*чек\w*|\bAOV\b)[^%\d\[]{{0,15}}(?P<n>{NUMTOK})\s*(?=₽|\$|руб)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="средний чек с валютой — «средний чек 1 200 ₽ [C001]»"),
        dict(key="take_rate", pct=True,
             re=[rf"(?:take\s*rate|комисси\w+[^%\d\[]{{0,15}}платформ\w*)[^%\d\[]{{0,25}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="take rate платформы, % — «take rate 12% [C001]»"),
        dict(key="margin", pct=True,
             re=[rf"марж\w*[^%\d\[]{{0,40}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="валовая маржа, % — «валовая маржа 70% [C001]»"),
    ],
    "cohort": [
        dict(key="sizes", pct=False, re=[], docs=[],
             hint="размеры когорт по месяцам входа — перенесите из воронки 06 вручную, напр.: [150, 200, 260]"),
        dict(key="retention", pct=True, re=[], docs=[],
             hint="кривая удержания M0–M11 — цели M1/M3/M6 из 06 заполняют свои слоты, остальное допишите"),
    ],
    "market": [
        dict(key="pam", pct=False,
             re=[rf"(?:\bPAM\b|рынок\w*)[^%\d\[]{{0,50}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>тысяч\w*|тыс|млн|млрд)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="рынок-родитель (PAM) — «рынок — 1,2–2,4 млрд ₽/год [S001]»; коридор → середина"),
        dict(key="tam_share", pct=True,
             re=[rf"\bTAM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля TAM от PAM, % — «TAM 60% [C001]»"),
        dict(key="sam_share", pct=True,
             re=[rf"\bSAM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля SAM от TAM, % — «SAM 40% [C001]»"),
        dict(key="som_share", pct=True,
             re=[rf"\bSOM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK})\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля SOM от SAM, % — «SOM 5% [C001]»"),
    ],
}


def _num(text: str) -> float:
    """«1 200», «1,5», «2 603» → float."""
    t = text.replace("\u00a0", "").replace("\u202f", "").replace(" ", "").replace(",", ".")
    return float(t)


def _grab(line: str, pattern: str) -> tuple[float, str] | None:
    """Первое число по шаблону: (значение, единица). Коридор «2–5» → середина."""
    m = re.search(pattern, line, re.IGNORECASE)
    if not m:
        return None
    nums = [_num(t) for t in re.findall(NUMTOK, m.group("n"))]
    if not nums:
        return None
    raw = round(nums[0] if len(nums) == 1 else (nums[0] + nums[-1]) / 2, 6)
    return raw, (m.groupdict().get("u") or "")


def _normalize(raw: float, unit: str, pct: bool) -> float:
    """% → доля; «млрд/млн/тыс» → множитель; доля без % (60 → 0,6)."""
    if "%" in unit:
        raw /= 100
    elif pct and raw > 1:
        raw /= 100
    else:
        for word, mult in MULT.items():
            if unit.startswith(word):
                raw *= mult
                break
    return round(raw, 6)


def _ctag(line: str) -> str | None:
    """C-тег строки (приоритет) или S-тег — источник числа."""
    tags = TAG_RE.findall(line)
    if not tags:
        return None
    cs = [t for t in tags if t[0] == "C"]
    return ("C" + cs[-1][1]) if cs else ("S" + tags[-1][1])


def _econ_lines(lines: list[str]) -> list[str]:
    """Строки раздела «Экономика» в 04 — приоритетная зона поиска."""
    out, inside = [], False
    for ln in lines:
        if ln.startswith("#"):
            inside = bool(ECON_HEADING.match(ln))
            continue
        if inside:
            out.append(ln)
    return out


def _retention(docs: dict[str, list[str]]) -> tuple[list, str] | None:
    """Цели удержания из 06: «удержание M1 с 32% до 40%» → слот M1 = 0,4."""
    slots: dict[int, float] = {}
    notes: list[str] = []
    for name in ("06_validation_plan.md", "04_product_strategy.md"):
        for line in docs.get(name) or []:
            for m in RET_ANCHOR.finditer(line):
                mi = int(m.group("m"))
                if not 0 <= mi < MONTHS:
                    continue
                rest = line[m.end():].split("[")[0]
                pcts = RET_PCT.findall(rest)
                if not pcts:
                    continue
                val = _num(pcts[-1])  # «с 32% до 40%» — берём целевое
                if val > 1:
                    val /= 100
                slots[mi] = val
                tag = _ctag(line)
                if tag:
                    notes.append(f"{name} [{tag}]: M{mi}={val:g}")
    if not slots:
        return None
    vals: list = [1.0] + [None] * (MONTHS - 1)  # M0 — вход когорты = 100%
    for mi, v in slots.items():
        vals[mi] = v
    return vals, ("; ".join(notes[:3]) if notes else "цели удержания из 06/04")


def _merge(base: dict, cfg: dict | None) -> dict:
    """Слияние примера и секции calcs.json: null и _-ключи не ломают книги."""
    out = dict(base)
    for k, v in (cfg or {}).items():
        if k.startswith("_") or v is None:
            continue
        if isinstance(v, list):
            base_list = list(base.get(k) or [])
            if k == "retention" and base_list:
                out[k] = [(v[i] if i < len(v) and v[i] is not None else base_list[i])
                          for i in range(len(base_list))]
            else:
                cleaned = [x for x in v if x is not None]
                out[k] = cleaned if cleaned else base_list
        else:
            out[k] = v
    return out


def scaffold_stats(cfg: dict) -> tuple[int, int]:
    """Сколько параметров заполнено (не null) из скольких всего."""
    total = sum(len(specs) for specs in PARAM_SPECS.values())
    found = sum(1 for section, specs in PARAM_SPECS.items()
                for spec in specs if (cfg.get(section) or {}).get(spec["key"]) is not None)
    return found, total


def scaffold(pdir: Path) -> tuple[dict, int, int]:
    """Каркас calcs.json из 02/04/06/07: найденные числа — с C/S-тегом в _notes,
    ненайденные — null + подсказка в _hints. Заданные вручную значения не трогает."""
    docs: dict[str, list[str]] = {}
    for name in DOCS:
        p = pdir / "outputs" / name
        docs[name] = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
    econ = {name: _econ_lines(docs[name]) for name in DOCS}
    existing = core.read_json(pdir / "calcs.json", {}) or {}

    cfg: dict[str, dict] = {}
    for section in ("unit_econ", "growth", "cohort", "market"):
        old = {k: v for k, v in (existing.get(section) or {}).items() if not k.startswith("_")}
        sec: dict = {k: v for k, v in old.items() if v is not None}
        notes: dict[str, str] = {}
        hints: dict[str, str] = {}
        for spec in PARAM_SPECS[section]:
            key = spec["key"]
            if key in sec:
                continue  # задано вручную — не перетираем
            if key == "retention":
                got = _retention(docs)
                if got is not None:
                    sec[key], notes[key] = got
                else:
                    sec[key], hints[key] = None, spec["hint"]
                continue
            hit = False
            for doc, econ_first in spec["docs"]:
                lines = docs.get(doc) or []
                pools = ([econ[doc]] if econ_first and econ[doc] else []) + [lines]
                for pool in pools:
                    for line in pool:
                        for pat in spec["re"]:
                            grabbed = _grab(line, pat)
                            if grabbed is None:
                                continue
                            tag = _ctag(line)
                            if not tag:
                                continue  # число без источника не переносим
                            raw, unit = grabbed
                            sec[key] = _normalize(raw, unit, spec["pct"])
                            snippet = line.strip()
                            notes[key] = (f"{doc} [{tag}]: {snippet[:77]}…" if len(snippet) > 80
                                          else f"{doc} [{tag}]: {snippet}")
                            hit = True
                            break
                        if hit:
                            break
                    if hit:
                        break
                if hit:
                    break
            if not hit:
                sec[key], hints[key] = None, spec["hint"]
        if section == "unit_econ" and "note" not in sec:
            sec["note"] = ("каркас pfs calc scaffold из 02/04/06/07: найденные числа — с тегом в _notes; "
                           "null — заполните вручную, недостающее подставится примером с пометкой «ПРИМЕР»")
        if notes:
            sec["_notes"] = notes
        if hints:
            sec["_hints"] = hints
        cfg[section] = sec
    for k, v in existing.items():  # пользовательские секции не теряем
        if k not in cfg and not k.startswith("_"):
            cfg[k] = v
    core.write_json(pdir / "calcs.json", cfg)
    found, total = scaffold_stats(cfg)
    core.log(pdir, "action", f"Каркас calcs.json: {found}/{total} чисел найдено в 02/04/06/07",
             tool="pfs calc scaffold")
    return cfg, found, total


# ---------- реестр и запуск ----------

BUILDERS = {
    "unit-econ": (unit_econ, "unit_economics.xlsx"),
    "growth": (growth, "growth_model.xlsx"),
    "cohort": (cohort, "cohort_retention.xlsx"),
    "market": (market, "market_sizing.xlsx"),
}
KEYS_BY_SECTION = {"unit-econ": "unit_econ", "growth": "growth", "cohort": "cohort", "market": "market"}


def run(pdir: Path, which: str = "all") -> list[Path]:
    """Собрать Excel-приложения в outputs/attachments/ и записать в журнал."""
    if which != "all" and which not in BUILDERS:
        raise core.PfsError(f"какой расчёт: all, {', '.join(BUILDERS)}")
    cfg = core.read_json(pdir / "calcs.json", {})
    out = pdir / "outputs" / "attachments"
    out.mkdir(parents=True, exist_ok=True)
    keys = list(BUILDERS) if which == "all" else [which]
    paths = []
    for key in keys:
        fn, fname = BUILDERS[key]
        params = _merge(DEFAULTS[KEYS_BY_SECTION[key]], cfg.get(KEYS_BY_SECTION[key]))
        path = fn(params).save(out / fname)
        core.log(pdir, "action", f"Excel-приложение: outputs/attachments/{fname}", tool="pfs calc")
        paths.append(path)
    return paths
