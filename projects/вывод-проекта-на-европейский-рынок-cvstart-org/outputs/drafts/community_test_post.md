# Черновик комьюнити-теста H4 (GitHub Discussions, перед этапом 2)

> Цель: проверить общественный контракт «OSS free forever + hosted за деньги» на текущем ядре (96 звёзд) ДО написания кода hosted [C054]. Критерии решения — в 06_validation_plan H4: реакция нейтральная/позитивная → этап 2; бунт → монетизация откладывается.

## Категория: Announcements / Discussions

## Заголовок
`Keeping career-ops-ui free and open — and what a hosted version would (and wouldn't) change`

## Текст поста (черновик EN)

```
TL;DR: The MIT-licensed, local-first career-ops-ui stays exactly as it
is — free, forever, no strings. Separately, I'm exploring a hosted
version as a paid convenience, and I want your reaction before I write
a line of code for it.

What stays free forever (unchanged, in writing):
- Everything you use today: local-first, your CV never leaves your
  machine, BYOK with 18 LLM providers, no telemetry, MIT license.
- All current features. No feature moves behind a paywall.

What the hosted version would be (a draft, not a promise):
- For people who can't or won't run the local setup (WSL, parent repo,
  CLI comfort zone are real barriers — I know, I wrote the docs).
- Same engine, no auto-renewals: annual plan, cancel anytime, reminder
  email before renewal (no auto-charges) — or one-time credit packs —
  your choice. No "€2.95 trial →
  €24.95 every 4 weeks" patterns. I know what this market does [the
  competitors' pricing pages are public], and it's the opposite of
  what I want to build.
- The local app remains the reference implementation. Hosted would be
  a convenience layer, not the product.

What I'm asking:
1. Does this break the trust you have in the project? Say so directly —
   👎 reactions and blunt comments are the point of this thread.
2. Which part feels most off: pricing model (credits vs subscription),
   the word "hosted" itself, or something I haven't thought of?
3. If you'd pay for hosted at all — what would be fair? (No promise,
   collecting signals.)

I'll read everything for two weeks and post a summary before any
development starts.
```

## Как публиковать и мерить

1. Опубликовать в Discussions (не issue), закрепить на 14 дней.
2. Метрики: суммарная тональность реакций, «unstar» за 14 дней (база: 0), число негативных issue-волн, содержание комментариев.
3. Порог остановки (> 3 жёстких негативных волн или отток ≥ 10% звёзд) → пересборка контракта, монетизация откладывается [06_validation_plan H4].
4. После сводки — решение: этап 2 стартует / контракт пересобирается (кредиты vs подписка).

## Связь с фактами

- Текущее состояние «$0 forever (MIT)» [C005]; позиционирование против автопродлений конкурентов [C052][C053]; запрет «гарантии ATS» — не упоминаем результат, только прозрачность [C061].
