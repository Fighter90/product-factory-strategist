---
id: M-landing-design
lang: en
title: Landing page design — typography with personality, bold colour systems, atmospheric backgrounds, animation patterns, anti-patterns
course: pm-approaches-en
sources: ["EN summary of the RU methodology card; original sources listed in the RU card"]
stages: [strategy, delivery]
tags: [en, summary]
related: [M-double-diamond, M-product-communication, M-usp]
---

# Landing Page Design (EN summary)

**When:** creating or redesigning a product landing page; improving the aesthetics of existing pages; choosing a visual direction before development.

**Core:** 1) **Typography with personality** — not Inter/Arial; display font for headlines (Space Grotesk, Clash Display, Outfit), body font for text (DM Sans, Manrope); one display + one body = a system. 2) **Palette with character** — one dominant brand colour + contrasting accent for CTAs + neutrals with personality (warm, not pure grey); palette defined in CSS variables. 3) **Composition** — intentional asymmetry (not everything centred); dramatic scale (XXL headlines); negative space; grid breakouts. 4) **Animations** — staggered reveals on load (fade + slide, 50–150 ms delays); scroll via animation-timeline: view(); hover translateY/scale, transitions 300–500 ms; respect prefers-reduced-motion. 5) **Backgrounds** — not flat: mesh gradients, noise (SVG texture at 3% opacity), blobs, structural lines. 6) **Details** — subtle borders (50% opacity), coloured shadows (never pure black), selective glassmorphism, unified icon set, highlight line on card top edge.

**Anti-patterns:** generic template design; timid colours; everything centred; uniform spacing; monotonous type; flat backgrounds; identical animations.

**Directions:** Minimalist · Brutalist · Luxury · Playful · Editorial · Dark editorial — choose one and hold to the end.

**Sources:** claudable-design (Claudeable project), adapted for the agent.
