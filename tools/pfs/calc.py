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
Запуск: pfs calc [all|unit-econ|growth|cohort|market|options] → outputs/attachments/*.xlsx
(options дополнительно пишет md-таблицу скоринга рядом с книгой).
"""
from __future__ import annotations

import re
from pathlib import Path

from . import core
from .xlsx import Workbook

DEFAULTS: dict[str, dict] = {
    "unit_econ": {
        "arpu": 199, "vc_share": 0.2, "cac": 600, "churn_month": 0.08,
        "scenarios": {"pessimistic": {"arpu": 0.8, "churn": 1.5, "cac": 1.3},
                      "optimistic": {"arpu": 1.2, "churn": 0.7, "cac": 0.8}},
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
    "options": {
        "criteria": [
            {"name": "Влияние на цель брифа", "weight": 3},
            {"name": "Реализуемость", "weight": 2, "gate_min": 3},
            {"name": "Скорость эффекта", "weight": 1},
        ],
        "options": [
            {"name": "A. Оставить как есть", "scores": [3, 4, 2]},
            {"name": "B. Ставка на один канал", "scores": [4, 2, 4]},
            {"name": "C. Комбинация каналов", "scores": [3, 3, 3]},
            {"name": "D. Закрыть направление", "scores": [1, 5, 5]},
        ],
        "note": "ПРИМЕР — перенесите критерии из таблицы «Сравнение» 03_options.md; веса — числа "
                "(напр. 1–3), у фильтров-порогов задайте gate_min: итог = Σ(балл × вес), "
                "вариант ниже порога отсеивается до ранжирования",
    },
}

MONTHS = 12


# ---------- юнит-экономика ----------

def weighted_arpu(p: dict) -> float | None:
    """ARPU = Σ(цена тарифа × доля базы) по tiers [карта M-unit-economics: средневзвешенный
    по долям базы, не цена топ-тарифа]; без tiers — скаляр arpu."""
    tiers = [t for t in (p.get("tiers") or [])
             if isinstance(t.get("price"), (int, float)) and isinstance(t.get("share"), (int, float))]
    if tiers:
        return round(sum(t["price"] * t["share"] for t in tiers), 6)
    a = p.get("arpu")
    return round(a, 6) if isinstance(a, (int, float)) else None


def derived(p: dict, mult: dict | None = None) -> dict:
    """Производные метрики юнит-экономики из сырой секции calcs.json «unit_econ» —
    одна математика для книги Excel, блока six-pager и кросс-чека `pfs check`
    (PRO-51: текст и Excel не должны расходиться). ARPU — средневзвешенный по tiers;
    во freemium CAC платящего = CAC / CR_free→paid, LTV/CAC и окупаемость — от него.
    Чего-то не хватает — None: пример из DEFAULTS в проверку текста не подставляется.
    mult — множители сценария {arpu|churn|cac|cr: x}."""
    m = mult or {}
    d: dict = {"arpu": None, "cm": None, "life": None, "ltv": None, "cac": None,
               "cr": None, "cac_paying": None, "ltv_cac": None, "payback": None}
    vc = p.get("vc_share")
    arpu = weighted_arpu(p)
    if arpu is not None and isinstance(vc, (int, float)) and 0 <= vc < 1:
        arpu = arpu * m.get("arpu", 1.0)
        d["arpu"] = round(arpu, 6)
        d["cm"] = round(arpu * (1 - vc), 6)
    churn = p.get("churn_month")
    if isinstance(churn, (int, float)) and churn > 0 and d["cm"] is not None:
        churn = churn * m.get("churn", 1.0)
        d["life"] = round(1 / churn, 6)
        d["ltv"] = round(d["cm"] * d["life"], 6)
    cac = p.get("cac")
    if isinstance(cac, (int, float)) and cac > 0:
        cr = p.get("cr_free_paid")
        d["cac"] = round(cac * m.get("cac", 1.0), 6)
        if isinstance(cr, (int, float)) and 0 < cr <= 1:
            cr = min(cr * m.get("cr", 1.0), 1.0)
            d["cr"] = round(cr, 6)
            d["cac_paying"] = round(d["cac"] / cr, 6)
        else:
            d["cac_paying"] = d["cac"]
    if d["ltv"] and d["cac_paying"]:
        d["ltv_cac"] = round(d["ltv"] / d["cac_paying"], 6)
        if d["cm"]:
            d["payback"] = round(d["cac_paying"] / d["cm"], 6)
    return d


def unit_econ(p: dict) -> Workbook:
    """Книга юнит-экономики: «Ввод» (тарифы миксом, CR freemium) + «Юнит-экономика»,
    «Чувствительность LTV/CAC» и «Сценарии» (пессимист/база/оптимист — один лист).
    Формулы ссылаются на адреса строк «Ввод»; кэш значений — из derived()."""
    d = derived(p)
    freemium = d.get("cr") is not None
    tiers = [t for t in (p.get("tiers") or [])
             if isinstance(t.get("price"), (int, float)) and isinstance(t.get("share"), (int, float))]
    wb = Workbook()
    v = wb.sheet("Ввод", widths={1: 38, 2: 13, 3: 52})
    v.row("Параметр", "Значение", "Комментарий")
    addr: dict[str, str] = {}

    def put(label, val, comment="", key=None):
        v.row(label, val, comment)
        if key:
            addr[key] = f"$B${len(v.rows)}"
        return len(v.rows)

    tier_rows = []
    for i, t_ in enumerate(tiers, 1):
        name = t_.get("name") or f"Тариф {i}"
        put(f"{name} — цена, ₽/мес", t_["price"], "цена тарифа")
        tier_rows.append(len(v.rows))
        put(f"{name} — доля базы", {"v": t_["share"], "pct": True}, "доля юнитов на тарифе")
    if tiers:
        f_mix = "+".join(f"B{r}*B{r + 1}" for r in tier_rows)
        put("ARPU — средневзвешенный, ₽/мес", {"f": f_mix, "cached": d["arpu"]},
            "Σ(цена × доля) — не цена топ-тарифа [M-unit-economics]", key="arpu")
    else:
        put("ARPU — выручка с юнита, ₽/мес", p.get("arpu"),
            "выручка на одного активного платящего", key="arpu")
    put("Доля переменных затрат (VC)", {"v": p.get("vc_share", 0), "pct": True},
        "себестоимость обслуживания, платежные комиссии", key="vc")
    put("CAC — привлечение бесплатного юнита, ₽" if freemium else "CAC — привлечение юнита, ₽",
        p.get("cac"), "маркетинг и промо на одного нового юнита", key="cac")
    if freemium:
        put("Конверсия free → paid (CR)", {"v": d["cr"], "pct": True},
            "доля бесплатных юнитов, ставших платящими", key="cr")
        put("CAC платящего = CAC / CR, ₽", {"f": f"'Ввод'!{addr['cac']}/'Ввод'!{addr['cr']}",
                                            "cached": round(d["cac_paying"], 2)},
            "во freemium LTV/CAC и окупаемость считают от CAC платящего", key="cac_pay")
    put("Отток в месяц (churn)", {"v": p.get("churn_month", 0), "pct": True},
        "доля ушедших за месяц", key="churn")
    put("Примечание", p.get("note", ""))
    cac_cell = addr["cac_pay"] if freemium else addr["cac"]

    u = wb.sheet("Юнит-экономика", widths={1: 36, 2: 13, 3: 44})
    u.row("Показатель", "Значение", "Как считается")
    u.row("Валовая маржа юнита (CM), ₽/мес",
          {"f": f"'Ввод'!{addr['arpu']}*(1-'Ввод'!{addr['vc']})", "cached": round(d["cm"], 2)},
          "ARPU × (1 − доля VC)")
    u.row("Средний срок жизни юнита, мес",
          {"f": f"1/'Ввод'!{addr['churn']}", "cached": round(d["life"], 2)}, "1 / отток")
    u.row("LTV, ₽", {"f": "B2*B3", "cached": round(d["ltv"], 2)}, "CM × срок жизни")
    if freemium:
        u.row("CAC платящего (freemium), ₽",
              {"f": f"'Ввод'!{cac_cell}", "cached": round(d["cac_paying"], 2)}, "CAC / CR free→paid")
    u.row("LTV / CAC платящего" if freemium else "LTV / CAC",
          {"f": f"B4/'Ввод'!{cac_cell}", "cached": round(d["ltv_cac"], 2) if d["ltv_cac"] else 0,
           "bold": True}, "ориентир: ≥ 3")
    u.row("Пейбек CAC платящего, мес" if freemium else "Пейбек CAC, мес",
          {"f": f"'Ввод'!{cac_cell}/B2", "cached": round(d["payback"], 2) if d["payback"] else 0},
          "CAC / CM; ориентир ≤ 12 мес")
    u.row("Доля CAC платящего в LTV" if freemium else "Доля CAC в LTV",
          {"f": f"'Ввод'!{cac_cell}/B4", "cached": round(d["cac_paying"] / d["ltv"], 3) if d["ltv"] else 0,
           "pct": True}, "расход на привлечение в lifetime-выручке юнита")
    s = wb.sheet("Чувствительность LTV/CAC", widths={1: 18})
    vcs = [0.1, 0.2, 0.3, 0.4, 0.5]
    churns = [0.04, 0.06, 0.08, 0.10, 0.12]
    header = ["Отток ↓ / VC →"] + [{"v": x, "pct": True, "bold": True} for x in vcs]
    s.row(*header)
    arpu_v = d["arpu"] or 0
    for ch in churns:
        row_no = len(s.rows) + 1  # номер добавляемой строки
        row = [{"v": ch, "pct": True, "bold": True}]
        for i in range(len(vcs)):
            col = col_ref(i + 2)  # B..F — доли VC в заголовке
            row.append({"f": f"'Ввод'!{addr['arpu']}*(1-{col}$2)/($A{row_no}*'Ввод'!{cac_cell})",
                        "cached": round(arpu_v * (1 - vcs[i]) / (ch * d["cac_paying"]), 2)
                        if d["cac_paying"] else 0})
        s.row(*row)
    c = wb.sheet("Сценарии", widths={1: 16, 2: 9, 3: 9, 4: 9, 5: 9})
    names = (("пессимистичный", "pessimistic"), ("базовый", "base"), ("оптимистичный", "optimistic"))
    scen = p.get("scenarios") or {}
    head = (["Сценарий", "ARPU ×", "churn ×", "CAC ×"] + (["CR ×"] if freemium else [])
            + ["ARPU", "CM", "Срок жизни, мес", "LTV",
               "CAC платящего" if freemium else "CAC", "LTV/CAC"])
    c.row(*head)
    from .xlsx import col_letter
    for label, key in names:
        m = scen.get(key) or {}
        mult = {"arpu": float(m.get("arpu", 1.0)), "churn": float(m.get("churn", 1.0)),
                "cac": float(m.get("cac", 1.0)), "cr": float(m.get("cr", 1.0))}
        r = len(c.rows) + 1
        sd = derived(p, mult=mult)
        mc = {k: col_letter(2 + i) for i, k in enumerate(("arpu", "churn", "cac", "cr"))}
        cells = [label, {"v": mult["arpu"]}, {"v": mult["churn"]}, {"v": mult["cac"]}]
        if freemium:
            cells.append({"v": mult["cr"]})
        arpu_f = f"'Ввод'!{addr['arpu']}*{mc['arpu']}{r}"
        cm_f = arpu_f + f"*(1-'Ввод'!{addr['vc']})"
        life_f = f"1/('Ввод'!{addr['churn']}*{mc['churn']}{r})"
        ltv_f = f"{cm_f}*{life_f}"
        if freemium:
            cac_f = (f"('Ввод'!{addr['cac']}*{mc['cac']}{r})/"
                     f"('Ввод'!{addr['cr']}*{mc['cr']}{r})")
        else:
            cac_f = f"'Ввод'!{addr['cac']}*{mc['cac']}{r}"
        cells += [{"f": arpu_f, "cached": round(sd["arpu"] or 0, 2)},
                  {"f": cm_f, "cached": round(sd["cm"] or 0, 2)},
                  {"f": life_f, "cached": round(sd["life"] or 0, 2)},
                  {"f": ltv_f, "cached": round(sd["ltv"] or 0, 2)},
                  {"f": cac_f, "cached": round(sd["cac_paying"] or 0, 2)},
                  {"f": f"{ltv_f}/{cac_f}", "cached": round(sd["ltv_cac"] or 0, 2), "bold": True}]
        c.row(*cells)
    c.row("Примечание", "множители к значениям листа «Ввод»; сценарии — calcs.json → unit_econ.scenarios")
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
    funnel_sheet(p, wb)
    return wb


def funnel_sheet(p: dict, wb: Workbook) -> None:
    """PRO-51: явная воронка из calcs.json → growth.funnel — у каждой ступени своя
    единица (визиты ≠ установки ≠ регистрации ≠ экспорты: кейс cvstart-EU, где
    «1 000 визитов × 5% = 50 экспортов» соседствовал с «1 000+ установок/мес»).
    Первый шаг — абсолютное значение, дальше — доля от предыдущего."""
    funnel = p.get("funnel")
    if not funnel:
        return
    note = ""
    if isinstance(funnel, dict):
        note = funnel.get("note") or ""
        funnel = funnel.get("steps") or []
    if isinstance(p.get("funnel_note"), str):
        note = p["funnel_note"]
    steps = [f for f in funnel if f.get("name")]
    if not steps:
        return
    f = wb.sheet("Воронка", widths={1: 32, 2: 18, 3: 16, 4: 13})
    f.row("Шаг", "Доля от предыдущего", "Единица шага", "Значение/мес")
    prev_ref, prev_val = None, 0.0
    for st in steps:
        r = len(f.rows) + 1
        share = st.get("share")
        share_cell = {"v": share, "pct": True} if isinstance(share, (int, float)) else "—"
        if prev_ref is None:
            prev_val = float(st.get("value") or 0)
            val_cell = {"v": prev_val, "cached": prev_val}
        else:
            prev_val = round(prev_val * (share or 0), 6)
            val_cell = {"f": f"{prev_ref}*B{r}", "cached": prev_val}
        f.row(st["name"], share_cell, st.get("unit", "ед. шага"), val_cell)
        prev_ref = f"D{r}"
    f.row("Примечание", note or "визиты, установки, регистрации и экспорты — разные шаги: "
                                "у каждой ступени своя единица; числа — из calcs.json → growth.funnel", "", "")


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


# ---------- взвешенный скоринг вариантов (pfs calc options) ----------

def options_scores(p: dict) -> list[dict]:
    """Взвешенный скоринг: итог = Σ(балл × вес), не сумма баллов (PRO-51: cvstart-EU
    складывал баллы как равные при качественных весах «высокий/критический»).
    gate_min — фильтр-порог («реализуемость ≥ 3»): вариант ниже порога отсеивается
    до ранжирования. Возвращает варианты в порядке: прошедшие фильтр по убыванию
    итога, затем отсеянные."""
    crit = [c for c in (p.get("criteria") or []) if c.get("name")]
    weights = [float(c.get("weight", 1)) for c in crit]
    res = []
    for o in (p.get("options") or []):
        raw = [float(s) for s in (o.get("scores") or [])]
        scores = (raw + [0.0] * len(crit))[:len(crit)]
        fail = ""
        for i, c in enumerate(crit):
            gmin = c.get("gate_min")
            if isinstance(gmin, (int, float)) and scores[i] < gmin:
                fail = f"фильтр «{c['name']}»: {scores[i]:g} < {gmin:g}"
                break
        res.append({"name": o.get("name") or f"Вариант {len(res) + 1}", "scores": scores,
                    "total": round(sum(s * w for s, w in zip(scores, weights)), 6),
                    "passes": not fail, "reason": fail})
    res.sort(key=lambda r: (not r["passes"], -r["total"]))
    return res


def _opt_header(crit: list[dict]) -> list[str]:
    head = []
    for c in crit:
        h = f"{c['name']} (вес {float(c.get('weight', 1)):g})"
        if isinstance(c.get("gate_min"), (int, float)):
            h += f", фильтр ≥ {c['gate_min']:g}"
        head.append(h)
    return head


def options(p: dict) -> Workbook:
    """Книга скоринга вариантов: «Критерии» (веса и фильтры-пороги — редактируются)
    + «Скоринг» (баллы, взвешенная сумма формулой SUMPRODUCT по весам «Критериев»,
    отсеянные фильтром — без формулы). Параметры — calcs.json → options."""
    crit = [c for c in (p.get("criteria") or []) if c.get("name")]
    res = options_scores(p)
    wb = Workbook()
    k = wb.sheet("Критерии", widths={1: 36, 2: 10, 3: 18})
    k.row("Критерий", "Вес", "Фильтр (мин. балл)")
    for c in crit:
        gmin = c.get("gate_min")
        k.row(c["name"], float(c.get("weight", 1)),
              gmin if isinstance(gmin, (int, float)) else "—")
    if p.get("note"):
        k.row("Примечание", p["note"])
    s = wb.sheet("Скоринг", widths={1: 28})
    n = len(crit)
    from .xlsx import col_letter
    last = col_letter(1 + n)
    s.row(*(["Вариант"] + _opt_header(crit) + ["Взвешенная сумма: Σ(балл × вес)", "Фильтр / статус"]))
    for r in res:
        row_no = len(s.rows) + 1
        cells = [r["name"]] + [{"v": sc} for sc in r["scores"]]
        cells.append({"f": f"SUMPRODUCT('Критерии'!$B$2:$B${n + 1},B{row_no}:{last}{row_no})",
                      "cached": r["total"], "bold": True} if r["passes"] else "отсеян (фильтр)")
        cells.append(r["reason"] or "ранжирование")
        s.row(*cells)
    return wb


def options_md(p: dict) -> str:
    """Маркдаун-таблица скоринга рядом с options_scoring.xlsx: веса видны в заголовках,
    итог — взвешенная сумма, отсеянные — в конце таблицы."""
    crit = [c for c in (p.get("criteria") or []) if c.get("name")]
    res = options_scores(p)
    head = ["Вариант"] + _opt_header(crit) + ["**Σ(балл × вес)**", "Фильтр / статус"]
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in res:
        row = [r["name"]] + [f"{sc:g}" for sc in r["scores"]]
        row.append(f"**{r['total']:g}**" if r["passes"] else "отсеян")
        row.append(r["reason"] or "ранжирование")
        out.append("| " + " | ".join(row) + " |")
    if p.get("note"):
        out += ["", f"> {p['note']}"]
    return "\n".join(out) + "\n"


# ---------- каркас calcs.json из документов ----------

DOCS = ("02_situation.md", "04_product_strategy.md", "06_validation_plan.md", "07_quality_review.md")
ECON_HEADING = re.compile(r"^#{1,6}\s+.*эконом", re.IGNORECASE)
NUMTOK = r"\d[\d\u00a0\u202f ]*(?:[.,]\d+)?"
TAG_RE = re.compile(r"\[(C|S)(\d{1,4})\]")
RET_ANCHOR = re.compile(r"(?:удержани\w*|retention\w*)[^%\d\[]{0,12}M\s*(?P<m>\d{1,2})", re.IGNORECASE)
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
             re=[rf"(?:переменн\w*|себестоимост\w*|\bVC\b)[^%\d\[]{{0,40}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="доля переменных затрат, % — «переменные затраты 25% [C001]»; коридор → середина"),
        dict(key="cac", pct=False,
             re=[rf"\bCAC\b[^%\d\[]{{0,12}}(?P<n>{NUMTOK})\s*(?=₽|\$|руб)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="CAC с валютой — «CAC 700 ₽ [C001]»; LTV/CAC и окупаемость CAC не подходят"),
        dict(key="churn_month", pct=True,
             re=[rf"(?:churn|отток\w*)[^%\d\[]{{0,30}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="отток в месяц, % — «churn 8%/мес [C001]» или из критериев 06; коридор → середина"),
    ],
    "growth": [
        dict(key="mau_start", pct=False,
             re=[rf"\bMAU\b[^%\d\[]{{0,25}}(?P<n>{NUMTOK})(?!\s*%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="MAU на старте — «MAU на старте 50 000 [C001]»"),
        dict(key="mau_growth_month", pct=True,
             re=[rf"(?:рост\w*[^%\d\[]{{0,20}}\bMAU\b|\bMAU\b[^%\d\[]{{0,20}}рост\w*)[^%\d\[]{{0,20}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="рост MAU, %/мес — «рост MAU 8%/мес [C001]»; коридор → середина"),
        dict(key="conv_order", pct=True,
             re=[rf"конверс\w*[^%\d\[]{{0,60}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,8}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="конверсия активного в заказ, %/мес — «конверсия 4%/мес [C001]»; базлайны из "
                  "«С чем сравниваем» 06 не план (пропускаются); коридор → середина"),
        dict(key="orders_per_active", pct=False,
             re=[rf"заказ\w*[^%\d\[]{{0,30}}активн\w*[^%\d\[]{{0,20}}(?P<n>{NUMTOK})(?!\s*%)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="заказов на активного, шт/мес — «заказов на активного 1,5 [C001]»"),
        dict(key="aov", pct=False,
             re=[rf"(?:средн\w*\s*чек\w*|\bAOV\b)[^%\d\[]{{0,15}}(?P<n>{NUMTOK})\s*(?=₽|\$|руб)"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="средний чек с валютой — «средний чек 1 200 ₽ [C001]»"),
        dict(key="take_rate", pct=True,
             re=[rf"(?:take\s*rate|комисси\w+[^%\d\[]{{0,15}}платформ\w*)[^%\d\[]{{0,25}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="take rate платформы, % — «take rate 12% [C001]»; коридор → середина"),
        dict(key="margin", pct=True,
             re=[rf"марж\w*[^%\d\[]{{0,40}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("04_product_strategy.md", True), ("06_validation_plan.md", False)],
             hint="валовая маржа, % — «валовая маржа 70% [C001]»; коридор → середина"),
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
             re=[rf"\bTAM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля TAM от PAM, % — «TAM 60% [C001]»; коридор → середина"),
        dict(key="sam_share", pct=True,
             re=[rf"\bSAM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля SAM от TAM, % — «SAM 40% [C001]»; коридор → середина"),
        dict(key="som_share", pct=True,
             re=[rf"\bSOM\b[^%\d\[]{{0,40}}(?P<n>{NUMTOK}(?:[^%\d\[]{{0,4}}{NUMTOK})?)\s*(?P<u>%)?"],
             docs=[("02_situation.md", False), ("07_quality_review.md", False)],
             hint="доля SOM от SAM, % — «SOM 5% [C001]»; коридор → середина"),
    ],
}


def _num(text: str) -> float:
    """«1 200», «1,5», «2 603» → float."""
    t = text.replace("\u00a0", "").replace("\u202f", "").replace(" ", "").replace(",", ".")
    return float(t)


def _grab(line: str, pattern: str) -> tuple[float, str, int] | None:
    """Первое число по шаблону: (значение, единица, позиция числа в строке).
    Позиция (старт группы n) нужна, чтобы приписать числу ближайший C/S-тег:
    у числа в этой строке свой тег стоит сразу после него. Коридор «2–5» → середина."""
    m = re.search(pattern, line, re.IGNORECASE)
    if not m:
        return None
    nums = [_num(t) for t in re.findall(NUMTOK, m.group("n"))]
    if not nums:
        return None
    raw = round(nums[0] if len(nums) == 1 else (nums[0] + nums[-1]) / 2, 6)
    return raw, (m.groupdict().get("u") or ""), m.start("n")


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


def _ctag(line: str, pos: int = 0) -> str | None:
    """Тег (C при наличии, иначе S), ближайший к числу — pos это позиция числа
    из _grab. На multi-tag строке («…ARPU 350 ₽ [C001]; конверсия 4% [C002]»)
    последний тег или соседний приписали бы числу чужой источник.
    При равных дистанциях — тег раньше в строке."""
    tags = [(abs(m.start() - pos), m.start(), m.group(1) + m.group(2))
            for m in TAG_RE.finditer(line)]
    if not tags:
        return None
    cs = [t for t in tags if t[2].startswith("C")]
    return min(cs or tags)[2]


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


COMPARE_HEADING = re.compile(r"^#{1,6}\s+.*сравнива", re.IGNORECASE)


def _plan_lines(lines: list[str]) -> list[str]:
    """Строки вне разделов «С чем сравниваем» (06): базлайн — не план-значение,
    коридор freemium-конверсий из базлайна не должен стать conv_order."""
    out, inside = [], False
    for ln in lines:
        if ln.startswith("#"):
            inside = bool(COMPARE_HEADING.match(ln))
        if not inside:
            out.append(ln)
    return out


def _retention(docs: dict[str, list[str]]) -> tuple[list, str] | None:
    """Цели удержания из 06: «удержание M1 с 32% до 40%» → слот M1 = 0,4.
    Спан процентов ограничен ближайшей границей — следующий якорь, следующая
    ссылка на месяц (M<н>) или C/S-тег: иначе «удержание M1 …, M3 45%»
    записало бы 45% в слот M1."""
    slots: dict[int, float] = {}
    notes: list[str] = []
    for name in ("06_validation_plan.md", "04_product_strategy.md"):
        for line in docs.get(name) or []:
            anchors = list(RET_ANCHOR.finditer(line))
            for i, m in enumerate(anchors):
                mi = int(m.group("m"))
                if not 0 <= mi < MONTHS:
                    continue
                rest = line[m.end():]
                cuts = [len(rest)]
                if i + 1 < len(anchors):  # следующий якорь удержани*/retention*
                    cuts.append(max(0, anchors[i + 1].start() - m.end()))
                mref = re.search(r"M\s*\d", rest)  # ссылка на другой месяц в этой же строке
                if mref:
                    cuts.append(mref.start())
                br = rest.find("[")  # C/S-тег и прочее в скобках — за границей спана
                if br >= 0:
                    cuts.append(br)
                pcts = RET_PCT.findall(rest[:min(cuts)])
                if not pcts:
                    continue
                val = _num(pcts[-1])  # «с 32% до 40%» — берём целевое
                if val > 1:
                    val /= 100
                slots[mi] = val
                tag = _ctag(line, m.start())  # ближайший к якорю тег
                if tag:
                    notes.append(f"{name} [{tag}]: M{mi}={val:g}")
    if not slots:
        return None
    vals: list = [1.0] + [None] * (MONTHS - 1)  # M0 — вход когорты = 100%
    for mi, v in slots.items():
        vals[mi] = v
    return vals, ("; ".join(notes[:3]) if notes else "цели удержания из 06/04")


def _merge(base: dict, cfg: dict | None) -> dict:
    """Слияние примера и секции calcs.json: null и _-ключи не ломают книги.
    В списках null заполняется примером на своей позиции; null в хвосте за
    пределами примера заполнить нечем — список обрезается на нём, позиции
    никогда не сдвигаются (размер когорты 8 не становится размером когорты 7)."""
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
                merged = [(base_list[i] if i < len(base_list) and x is None else x)
                          for i, x in enumerate(v)]
                for i, x in enumerate(merged):
                    if x is None:  # null за пределами примера — обрезаем здесь, не сдвигая хвост
                        merged = merged[:i]
                        break
                out[k] = merged if merged else base_list
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
    ненайденные — null + подсказка в _hints. Числу приписывается ближайший к нему
    тег, разделы «С чем сравниваем» (06) пропускаются — базлайн не план-значение.
    Заданные вручную значения не трогает, их _notes/_hints сохраняет."""
    docs: dict[str, list[str]] = {}
    for name in DOCS:
        p = pdir / "outputs" / name
        docs[name] = p.read_text(encoding="utf-8").splitlines() if p.exists() else []
    econ = {name: _econ_lines(docs[name]) for name in DOCS}
    docs = {name: _plan_lines(lines) for name, lines in docs.items()}  # базлайны «С чем сравниваем» — не план
    existing = core.read_json(pdir / "calcs.json", {}) or {}

    cfg: dict[str, dict] = {}
    for section in ("unit_econ", "growth", "cohort", "market"):
        old_sec = existing.get(section) or {}
        old = {k: v for k, v in old_sec.items() if not k.startswith("_")}
        sec: dict = {k: v for k, v in old.items() if v is not None}
        old_notes: dict = old_sec.get("_notes") or {}
        old_hints: dict = old_sec.get("_hints") or {}
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
                            raw, unit, pos = grabbed
                            tag = _ctag(line, pos)  # ближайший к числу тег, не последний в строке
                            if not tag:
                                continue  # число без источника не переносим
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
        if notes or old_notes:  # provenance ручных и прошлых значений переживает повторный запуск
            kept = {k: v for k, v in old_notes.items()
                    if k in sec and k not in notes and sec.get(k) is not None}
            sec["_notes"] = {**kept, **notes}
        if hints or old_hints:  # пользовательскую подсказку всё ещё-null ключа не перетираем
            sec["_hints"] = {**hints,
                             **{k: v for k, v in old_hints.items() if k in sec and sec.get(k) is None}}
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
    "options": (options, "options_scoring.xlsx"),
}
KEYS_BY_SECTION = {"unit-econ": "unit_econ", "growth": "growth", "cohort": "cohort",
                   "market": "market", "options": "options"}


def run(pdir: Path, which: str = "all") -> list[Path]:
    """Собрать Excel-приложения в outputs/attachments/ и записать в журнал.
    options — взвешенный скоринг вариантов: книга + md-таблица рядом; в `all`
    собирается только когда в calcs.json заполнена секция options — пример-скоринг
    в проект без сравнения вариантов не подкладываем."""
    if which != "all" and which not in BUILDERS:
        raise core.PfsError(f"какой расчёт: all, {', '.join(BUILDERS)}")
    cfg = core.read_json(pdir / "calcs.json", {})
    out = pdir / "outputs" / "attachments"
    out.mkdir(parents=True, exist_ok=True)
    keys = list(BUILDERS) if which == "all" else [which]
    if which == "all":
        keys = [k for k in keys if k != "options" or cfg.get("options")]
    paths = []
    for key in keys:
        fn, fname = BUILDERS[key]
        params = _merge(DEFAULTS[KEYS_BY_SECTION[key]], cfg.get(KEYS_BY_SECTION[key]))
        path = fn(params).save(out / fname)
        extra = ""
        if key == "options":
            (out / "options_scoring.md").write_text(options_md(params), encoding="utf-8")
            extra = " + options_scoring.md"
        core.log(pdir, "action", f"Excel-приложение: outputs/attachments/{fname}{extra}", tool="pfs calc")
        paths.append(path)
    return paths
