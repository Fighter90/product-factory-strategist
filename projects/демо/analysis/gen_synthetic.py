#!/usr/bin/env python3
"""Синтетический набор данных ужинов ROSE (ДЕМО, seed=42).
Генерирует таблицу вечеров для демонстрации анализа данных.
НЕ является реальными данными продукта; помечено origin=synthetic."""
import csv, random
random.seed(42)
venues = [("Бархат","Патриаршие пруды","Классика"),("Полночь","Цветной бульвар","Литературный"),
          ("Кадр","Хитровка","Кино"),("Полночь","Цветной бульвар","Джаз"),
          ("Винзавод","Курская","Искусство"),("Огонь","Сокольники","Природа"),
          ("Типография","Маяковская","Гастрономия"),("Погреб","Полянка","Вино"),
          ("Форре","Маросейка","Игры"),("Сад Камней","Хамовники","Бранч"),
          ("Акваф","Арбат","Вид на город"),("Сосенки","Серебряный бор","Ужин у огня")]
rows = []
for w in range(12):                      # 12 недель пилота
    for i in range(2):                   # 2 стола в неделю
        v = venues[(w*2+i) % len(venues)]
        no_show = 1 if random.random() < 0.08 else 0
        pairs = max(0, min(3, int(random.gauss(1.6, 0.7))))
        score = round(min(4.0, max(1.0, random.gauss(2.9, 0.45))), 1)
        repeat_share = round(random.uniform(0.35, 0.62), 2)
        rows.append([f"нед.{w+1}", f"стол-{w*2+i+1:02d}", v[0], v[2], 6-no_show, pairs, score, repeat_share])
with open("projects/демо/analysis/synthetic_tables.csv","w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["week","table","venue","interest","guests","mutual_pairs","avg_score","repeat_share"])
    w.writerows(rows)
print("CSV:", len(rows), "столов")
