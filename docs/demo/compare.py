"""Сравнение агента с исходным способом (обычный чат с ИИ) по объективным, воспроизводимым признакам.

Запуск: python3 docs/demo/compare.py
Метрики считаются одинаково для обоих текстов; «проверяемость» = доля чисел, у которых есть ссылка на источник.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.pfs import claims, core, sources  # noqa: E402

NUM = re.compile(r"(?<![\w\[])\d[\d\s.,]*\s?(%|п\.п\.|₽|руб|млн|млрд|тыс)", re.I)
TAG = re.compile(r"\[(C|S)\d{3}\]")


def metrics(text: str) -> dict:
    lines = [l for l in text.splitlines() if l.strip()]
    nums = [l for l in lines if NUM.search(l)]
    tagged = [l for l in nums if TAG.search(l)]
    low = text.lower()
    options = len(re.findall(r"^#+\s*(вариант|опция|сценарий)\s", text, re.I | re.M))
    if not options:  # варианты нумерованным списком внутри раздела «Варианты»
        m = re.search(r"^#+[^\n]*вариант[^\n]*\n(.*?)(?=^#)", text, re.I | re.M | re.S)
        options = len(re.findall(r"^\s*(\d+[.)]|[-*])\s", m.group(1), re.M)) if m else 0
    return {
        "слов": len(text.split()),
        "строк с числами": len(nums),
        "из них со ссылкой на источник": len(tagged),
        "проверяемость чисел, %": round(100 * len(tagged) / len(nums)) if nums else 0,
        "вариантов (заголовков)": options,
        "есть «оставить как есть»": any(k in low for k in ("оставить как есть", "статус-кво", "ничего не менять")),
        "есть «закрыть/свернуть»": any(k in low for k in ("закрыть", "свернуть")),
        "возражения у вариантов": low.count("возражени"),
        "раздел «чего не знаем»/пробелы": any(k in low for k in ("чего мы не знаем", "пробел", "неизвестн")),
        "план проверки: база сравнения": any(k in low for k in ("с чем сравниваем", "контрольн", "a/b")),
        "план проверки: контрметрики": any(k in low for k in ("контрметрик", "нежелательные последствия")),
        "критерии решения заданы заранее": "критерии решения" in low or "стоп-сигнал" in low,
    }


def main() -> None:
    pdir = ROOT / "projects" / "demo-antispam"
    agent_text = "\n".join((pdir / "outputs" / n).read_text(encoding="utf-8") for n in
                           ("02_situation.md", "03_options.md", "04_product_strategy.md", "05_comms_strategy.md", "06_validation_plan.md")
                           if (pdir / "outputs" / n).exists())
    base_path = ROOT / "docs" / "demo" / "baseline_plain_chat.md"
    base_text = base_path.read_text(encoding="utf-8") if base_path.exists() else ""
    a, b = metrics(agent_text), metrics(base_text)
    print("| Признак | Агент | Обычный чат |\n|---|---|---|")
    for k in a:
        fa, fb = a[k], b[k]
        fmt = lambda v: ("да" if v else "нет") if isinstance(v, bool) else str(v)
        print(f"| {k} | {fmt(fa)} | {fmt(fb)} |")
    cl = claims.load(pdir)
    print(f"\nРеестр агента: источников {len(sources.load(pdir))}, утверждений {len(cl)} "
          f"(активных {sum(c['status'] == 'active' for c in cl)}, отозвано/замещено {sum(c['status'] != 'active' for c in cl)})")


if __name__ == "__main__":
    main()
