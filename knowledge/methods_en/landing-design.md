---
id: M-landing-design
lang: en
title: Landing page design — typography with personality, bold colour systems, atmospheric backgrounds, animation patterns, anti-patterns
course: pm-approaches-en
sources: ["EN mirror of the RU card; original sources listed there"]
stages: [strategy, delivery]
tags: [landing-page, design, typography, colour, composition, animation, visual-direction]
related: [M-double-diamond, M-product-communication, M-usp]
---

# Landing Page Design with Personality

**When applied:** creating or redesigning a product landing page; improving the aesthetics
of existing pages; choosing a visual direction before development.

**Core.**

1. **Typography with personality.** Not Inter, and not Arial. A display font for headlines
   (Space Grotesk, Clash Display, Outfit), a body font for the text (DM Sans, Manrope).
   One display + one body = a system.

2. **A palette with character.** One dominant brand colour + a contrasting accent for
   the CTA + neutrals with character (warm, not grey). The palette is set in CSS variables.

3. **Composition.** Intentional asymmetry (not everything centred); dramatic scale
   (XXL headlines); generous whitespace; breaking out of the grid.

4. **Animations.** On load — staggered reveals (fade + slide, delays of 50–150 ms).
   On scroll — animation-timeline: view() for reveal-on-enter. On hover — translateY/scale,
   transitions of 300–500 ms. Respect prefers-reduced-motion.

5. **Backgrounds.** Not flat: mesh gradients, noise (an SVG texture at 3% opacity), blobs,
   structural lines.

6. **Details.** Thin borders (50% opacity), coloured shadows (not black), selective
   glassmorphism, a single icon set, a highlight line along the top edge of a card.

**Anti-patterns:** generic template design; timid colours; everything centred; uniform
spacing; monotonous typography; flat backgrounds; identical animations.

**Directions:** Minimalist · Brutalist · Luxury · Playful · Editorial · Dark editorial —
pick one and hold it to the end.

**Sources:** claudable-design (the Claudeable project), generalized for the agent.
