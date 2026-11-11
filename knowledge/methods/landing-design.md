---
id: M-landing-design
title: Landing page design — typography with personality, bold colour systems, atmospheric backgrounds, animation patterns, anti-patterns
course: ux
stages: [strategy, delivery]
tags: [дизайн, лендинг, визуал]
related: [M-double-diamond, M-product-communication, M-usp]
---

# Дизайн лендинга с характером

**Когда применяется:** создание или редизайн лендинга продукта; улучшение эстетики
существующих страниц; выбор визуального направления перед разработкой.

**Ядро.**

1. **Типографика с характером.** Не Inter и не Arial. Display-шрифт для заголовков
   (Space Grotesk, Clash Display, Outfit), body-шрифт для текста (DM Sans, Manrope).
   Один display + один body = система.

2. **Палитра с характером.** Один доминирующий цвет бренда + контрастный акцент для
   CTA + нейтрали с характером (тёплые, не серые). Палитра задаётся в CSS-переменных.

3. **Композиция.** Намеренная асимметрия (не всё по центру); масштаб драматический
   (XXL заголовки); свободное пространство; выходы за сетку.

4. **Анимации.** Загрузка — staggered reveals (fade + slide, задержки 50–150 мс).
   Скролл — animation-timeline: view() для reveal-on-enter. Hover — translateY/scale,
   переходы 300–500 мс. Уважать prefers-reduced-motion.

5. **Фоны.** Не плоские: mesh-градиенты, noise (SVG texture 3% opacity), blobs,
   структурные линии.

6. **Детали.** Тонкие бордеры (50% opacity), цветные тени (не чёрные), selective
   glassmorphism, единый набор иконок, highlight-линия на верхнем крае карточки.

**Анти-паттерны:** генеричный шаблонный дизайн; робкие цвета; всё по центру;
одинаковые отступы; монотонная типографика; плоские фоны; одинаковые анимации.

**Направления:** Minimalist · Brutalist · Luxury · Playful · Editorial · Dark editorial —
выбрать одно и держать до конца.

**Источники:** claudable-design (Claudeable project), обобщено для агента.
