"""Генератор МОДЕЛЬНЫХ данных подписки для демонстрации расчёта когорт.

НЕ реальные данные оператора. Параметры заданы допущениями демо-сценария:
- до 2025-09 месячный отток платящих ~6–7%; после маркировки звонков и бесплатной базовой защиты у всех
  операторов (осень 2025) отток в первые 2 месяца новых когорт растёт до ~18–22%;
- семейные подключения (оплата за родственника) уходят примерно вдвое реже.
Воспроизведение: python3 analysis/gen_synthetic_subscriptions.py > analysis/synthetic_subscriptions.csv
"""
import random

random.seed(42)
print("subscriber_id,month,plan")
uid = 0
for start in range(0, 18):  # 2025-01 … 2026-06
    y, m = 2025 + start // 12, start % 12 + 1
    for _ in range(300 if start < 9 else 220):
        uid += 1
        family = random.random() < 0.25
        cur = start
        while cur < 22:  # наблюдаем до 2026-10
            cy, cm = 2025 + cur // 12, cur % 12 + 1
            print(f"u{uid},{cy}-{cm:02d}-15,{'family' if family else 'solo'}")
            age = cur - start
            base = 0.065 if start < 8 else (0.20 if age < 2 else 0.08)
            churn = base * (0.5 if family else 1.0)
            if random.random() < churn:
                break
            cur += 1
