"""Удержание M1/M2/M3 по тарифу (solo/family) до и после 2025-09 на МОДЕЛЬНЫХ данных.
Воспроизведение: python3 analysis/segment_retention.py analysis/synthetic_subscriptions.csv
"""
import csv
import sys
from collections import defaultdict

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
months = defaultdict(set)
plan = {}
for r in rows:
    y, m = int(r["month"][:4]), int(r["month"][5:7])
    months[r["subscriber_id"]].add(y * 12 + m - 1)
    plan[r["subscriber_id"]] = r["plan"]
cut = 2025 * 12 + 8  # 2025-09
groups = defaultdict(list)
for uid, ms in months.items():
    start = min(ms)
    groups[(plan[uid], "до 2025-09" if start < cut else "с 2025-09")].append((start, ms))
print("| Тариф | Когорты | Подписчиков | M1 | M2 | M3 |\n|---|---|---|---|---|---|")
for key in sorted(groups):
    g = groups[key]
    cells = []
    for k in (1, 2, 3):
        eligible = [ms for s, ms in g if s + k <= 2026 * 12 + 9]
        cells.append(f"{100 * sum(1 for ms in eligible if min(ms) + k in ms) / len(eligible):.1f}%")
    print(f"| {key[0]} | {key[1]} | {len(g)} | " + " | ".join(cells) + " |")
