---
name: claudable-landing
description: "Design principles and build workflow for distinctive, high-impact landing pages. Use when creating or improving landing pages, hero sections, marketing sites, or product pages. Covers typography with personality, bold colour systems, spatial composition, atmospheric backgrounds, and animation patterns. RU: дизайн-принципы и workflow для лендингов с характером — типографика, цвета, композиция, анимации, фоны."
invoke: auto
---

# Landing Design — Distinctive & High-Impact

> Sources: claudable-design + claudable-workflow + claudable-stack (Claudeable project).
> Adapted for the Стратег Фабрики продуктов agent (vanilla HTML/CSS/JS or React/Next).

## 1. Typography with Personality

**AVOID:** Inter, Arial, Roboto, Helvetica, system fonts as identity fonts
**PREFER:** Fonts that reinforce the brand character

| Role | Recommended |
|------|-------------|
| Display / Headlines | Clash Display, Cabinet Grotesk, Satoshi, Space Grotesk, Outfit |
| Body refined | DM Sans, Plus Jakarta Sans, Manrope, Nunito Sans |
| Serif elegant | Playfair Display, Fraunces, Libre Baskerville |
| Monospace modern | JetBrains Mono, Fira Code, IBM Plex Mono |

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap');

:root {
  --font-display: 'Space Grotesk', sans-serif;
  --font-body: 'DM Sans', sans-serif;
}
```

RU: типографика с характером — не Inter и не Arial. Display-шрифт для заголовков,
body-шрифт для текста. Один display + один body = система.

## 2. Bold Colour System

No timid palettes. Define:

- **One dominant colour** that identifies the brand
- **One contrasting accent** for CTAs and highlights
- **Neutral tones with personality** — not pure grey

```css
:root {
  --primary: 262 83% 58%;      /* vibrant violet */
  --accent: 43 96% 56%;        /* golden yellow */
  --background: 240 10% 3.9%;  /* blue-tinted black */
  --foreground: 0 0% 98%;      /* warm white */
  --muted: 240 5% 15%;         /* grey with character */
}
```

RU: один доминирующий цвет бренда + контрастный акцент для CTA + нейтрали с
характером (не чистые серые). Палитра задаётся в CSS-переменных.

## 3. Spatial Composition

- **Intentional asymmetry** — not everything centred
- **Dramatic scale** — XXL headlines, extreme size contrast
- **Negative space** — let the design breathe
- **Break the grid** — elements that overflow

```css
.hero-title {
  font-size: clamp(3rem, 10vw, 8rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.02em;
}
.hero-caption {
  position: absolute;
  bottom: 3rem;
  right: 3rem;
  max-width: 280px;
  font-size: 13px;
  color: var(--muted);
}
```

## 4. Animation Patterns

**On initial load:**
- Staggered reveals (delay each element by 0.05–0.15s)
- Fade + slide from different directions
- Clip-path reveals

**On interaction:**
- Hover states with movement (translateY, scale)
- Smooth transitions (300–500ms)
- Micro-interactions on buttons

**On scroll:**
- Scroll-driven animations (`animation-timeline: view()`)
- Parallax layers
- Reveal-on-enter for each section

```css
/* Scroll-driven reveal */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 20% exit 60%;
}
@keyframes reveal {
  to { opacity: 1; transform: translateY(0); }
}
```

RU: staggered reveals при загрузке, hover с движением, scroll-driven через
`animation-timeline: view()`. Уважать `prefers-reduced-motion`.

## 5. Atmospheric Backgrounds

No flat backgrounds. Add:

- **Subtle gradients** — mesh gradients, radial washes
- **Noise/grain** — SVG texture overlay at 0.03 opacity
- **Blobs/shapes** — abstract shapes behind content
- **Grid lines** — structural decorative lines

```css
.hero-bg {
  background:
    radial-gradient(ellipse at 20% 50%, hsl(var(--primary) / 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, hsl(var(--accent) / 0.1) 0%, transparent 50%),
    hsl(var(--background));
}
.hero-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/noise.svg');
  opacity: 0.03;
  pointer-events: none;
}
```

## 6. Premium Details

- **Subtle borders** — `border: 1px solid rgba(border, 0.5)`
- **Coloured shadows** — never pure black (`shadow-primary/5`)
- **Selective glassmorphism** — only where it serves hierarchy
- **Consistent iconography** — one icon set throughout
- **Highlight line** — 1px gradient at card top edge

```css
.card {
  border-radius: 16px;
  border: 1px solid rgba(var(--border-rgb), 0.5);
  background: rgba(var(--card-rgb), 0.5);
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 30px rgba(var(--primary-rgb), 0.05);
}
.card::before {
  content: '';
  position: absolute;
  inset: 0 0 auto;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(var(--primary-rgb), 0.5), transparent);
}
```

## 7. Aesthetic Direction — Choose ONE

| Style | Characteristics | Best for |
|-------|----------------|----------|
| **Minimalist** | White space, clean type, few colours | SaaS, portfolios |
| **Brutalist** | Raw, bold type, strong contrast | Agencies, creatives |
| **Luxury** | Elegant serif, smooth animation, dark mode | Premium, fashion |
| **Playful** | Vibrant colours, illustrations, micro-interactions | Consumer, startups |
| **Editorial** | Defined grid, clear hierarchy, magazine-like | Blogs, media |
| **Dark editorial** | Deep background, gradient accents, glow effects | Tech, AI products |

## 8. Development Order

1. **Layout** — header, footer, base structure
2. **Navigation** — main menu, mobile nav
3. **Hero section** — first impression
4. **Content sections** — one by one
5. **CTAs and forms** — conversion
6. **States** — loading, error, empty
7. **Animations** — polish last

## 9. Pre-Launch Checklist

- [ ] Responsive: mobile, tablet, desktop
- [ ] Favicon and meta tags
- [ ] Open Graph images
- [ ] Loading states
- [ ] 404 page
- [ ] Performance (Lighthouse > 90)
- [ ] Accessibility (contrast, alt texts)
- [ ] `prefers-reduced-motion` respected

## Anti-Patterns

1. **Generic design** — if it looks like a template, it's bad
2. **Timid colours** — don't be afraid of colour
3. **Everything centred** — use varied alignments
4. **Uniform spacing** — vary to create rhythm
5. **Monotonous type** — mix weights and sizes
6. **Flat backgrounds** — always add texture
7. **Identical animations** — vary timing and direction
