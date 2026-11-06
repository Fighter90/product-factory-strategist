#!/usr/bin/env python3
"""Синтетическая воронка hosted-беты CVStart (ДЕМО, seed=7).
12 недель: посетители лендинга → регистрация → активация (1 резюме) → оплата.
НЕ реальные данные; origin=synthetic."""
import csv, random
random.seed(7)
rows=[]; vis=3000; sign=0.055; act=0.62; paid=0.028
for w in range(1,13):
    vis = int(vis*1.22)
    s = int(vis*sign); a = int(s*act); pr = int(a*paid*(1+0.06*w))
    mrr = pr*29
    rows.append([f"нед.{w}", vis, s, a, pr, mrr])
with open("projects/демо/analysis/synthetic_funnel.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["week","visitors","signups","activated","paid","mrr_usd"]); w.writerows(rows)
print("воронка:", len(rows), "недель; MRR нед.12 =", rows[-1][5], "USD")
