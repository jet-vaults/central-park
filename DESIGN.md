# Central Park Elad — Web Design System

Derived from the printed prospectus (`פרוספקט-אנגלית-12.pdf`, 13 spreads, 297×210 mm landscape).
The website is the digital continuation of that document. Everything below is measured from the PDF,
not invented.

## 1. What the prospectus does

- **Two-tone pacing.** Spreads alternate between charcoal (#2c2c2c) and warm cream (#f6f1e8 / #f5f2e8 with a
  faint paper texture). Photography is always full-bleed on exactly half of a spread; text owns the other half.
- **One accent, used sparingly.** Sand gold (#c6af7b) carries every headline and every hairline. Dusty rose
  (#c29284) appears only in the logo, the map pins and one ring set. Mid grey (#727272) is the third logo tone.
- **Geometry = circles.** The visual signature is the semicircle / concentric ring: thin gold rings behind
  headlines, huge rings bleeding off the page edge, solid half-discs anchored to the gutter, circular photo
  masks with a thin gold ring offset a few points outside the image, circular page numbers with a hairline
  running to the page edge.
- **Type is quiet.** Body copy is small (14 pt), light, justified into narrow two-column measures (~165 pt wide).
  Headlines are only ~2× body (30 pt) — hierarchy comes from colour (gold) and weight contrast, not size.
  Only two moments shout: the cover "ELAD" (96 pt) and the condensed "Luxury Living…" / "Your new home." (55 pt).
- **Whitespace is generous and asymmetric.** Text blocks start ~20 % down the page and stop well before the
  bottom; margins are wide (≈ 90 pt on 842 pt page = ~11 %).

## 2. Typography

| Role in PDF | Font (embedded) | Size | Colour |
|---|---|---|---|
| Body, captions | **Ploni DL 1.1 Regular** | 14 pt (12 pt in circles) | #2c2c2c on cream · #f6f1e8 on charcoal |
| Section headline | **Ploni DL 1.1 Bold** (often mixed with Regular on the 2nd line) | 30 pt | #c6af7b |
| Lead-in / list titles | Ploni Bold | 14–18 pt | #2c2c2c |
| Display statements | **Almoni Tzar DL 4.0 Bold** (condensed) | 55 pt | #c6af7b or #2c2c2c |
| Cover | Ploni Regular 51 pt + Ploni Bold 96 pt | | #2c2c2c |

Ploni and Almoni Tzar are commercial Fontef faces. They are **not** in the delivered files and not installed
on this machine; the PDF only embeds Latin subsets, so they cannot be reused for Hebrew.

**Web stack (until licensed files arrive):**

```
--font-sans: "Heebo", "Ploni", system-ui, sans-serif;   /* Heebo = Oded Ezer, same designer family as Ploni */
--font-display: var(--font-sans);                       /* swap to Almoni Tzar if licensed */
```
Heebo variable (wght 100–900) is self-hosted from `/assets/fonts/` in two subsets (hebrew, latin). Dropping
`ploni.woff2` / `almoni-tzar.woff2` into that folder and editing two `@font-face` rules restores the exact brand faces.

**Web scale** (fluid, `clamp()`; base 16 px ≈ PDF 14 pt):

```
--fs-body:    clamp(1rem, 0.95rem + 0.25vw, 1.125rem);      /* 16–18 */
--fs-small:   0.875rem;                                     /* captions, nav */
--fs-lead:    clamp(1.125rem, 1rem + 0.5vw, 1.375rem);      /* bold lead-ins */
--fs-h2:      clamp(2rem, 1.5rem + 1.6vw, 3rem);            /* 32–48, gold */
--fs-display: clamp(3rem, 2rem + 4vw, 6rem);                /* 48–96, hero */
line-height: 1.7 body · 1.15 headlines · 1 display
letter-spacing: 0 (Hebrew must not be tracked); Latin small-caps labels +0.08em
```

## 3. Colour tokens

```
--c-charcoal:  #2c2c2c;   /* dark ground + text on light */
--c-cream:     #f6f1e8;   /* light ground + text on dark */
--c-cream-2:   #f3eee3;   /* alternate light band */
--c-gold:      #c6af7b;   /* headlines, rings, hairlines */
--c-gold-soft: rgba(198,175,123,.45);
--c-rose:      #c29284;   /* logo, pins — accent only */
--c-grey:      #727272;   /* logo, muted UI */
--c-ink-soft:  rgba(44,44,44,.72);   /* secondary text on cream */
--c-paper-soft: rgba(246,241,232,.78); /* secondary text on charcoal */
```
Contrast: gold on charcoal 6.1:1 (headlines OK), gold on cream 1.9:1 → gold is **never** used for body text on cream;
on cream, gold is for ≥ 32 px headlines and decorative rings only.

## 4. Layout system

```
--w-max:     1440px;   /* content container */
--w-text:    36rem;    /* single text column, ~65 chars Hebrew */
--w-text-2:  46rem;    /* two-column measure */
--gutter:    clamp(1.25rem, 4vw, 5rem);   /* 20 → 80 px */
--space-1:   .5rem  --space-2: 1rem  --space-3: 1.5rem  --space-4: 2.5rem
--space-5:   4rem   --space-6: 6rem  --space-7: 8rem   --space-8: 12rem
--section-y: clamp(5rem, 8vw, 10rem);   /* vertical rhythm between sections */
--radius:    0;        /* the brand has NO rounded rectangles — only perfect circles */
--ring:      1px solid var(--c-gold);
```

Grid: 12 columns inside `--w-max`; split sections are 6/6 on desktop, image column may bleed to the viewport
edge (`margin-inline-end: calc(50% - 50vw)` on the outer side). Text column padding = `--gutter`.

Breakpoints: 1024 (split → stack), 768 (two-column text → one), 480 (hero type/hero height tighten).

## 5. Imagery rules

- Every image is `object-fit: cover` with an explicit `aspect-ratio` on its box; `object-position` set per image.
- Full-bleed bands: `aspect-ratio: 21/9` desktop, `4/3` mobile. Hero: `100svh` desktop, `min(100svh, 130vw)` mobile.
- Circle images: `aspect-ratio: 1; border-radius: 50%` + an offset gold ring (`outline: 1px solid gold; outline-offset: 10px`)
  exactly like the PDF's masks.
- Sources: AVIF + WebP via `<picture>`, widths 768/1280/1920/2560 (bleed), 640/1024/1600 (split), 480/800 (tiles).
  Hero is `fetchpriority="high"` + preloaded; everything else `loading="lazy" decoding="async"`.
- Never crop out building tops; skyline aerials keep the horizon in the upper third.

## 6. Motion rules

- Reveal = opacity 0→1 + translateY 24px→0, 900 ms, `cubic-bezier(.2,.7,.2,1)`, staggered 90 ms per child.
- Image reveal = clip-path inset from the leading edge (RTL: right) 100%→0 over 1200 ms, plus scale 1.06→1.
- Rings draw in via `stroke-dashoffset`, 1400 ms.
- Hero: logo (0 ms) → display line (250 ms) → subline (500 ms) → rings (400 ms) → scroll cue (1400 ms).
- Parallax only on full-bleed images, max 6 % travel, `transform` only, IntersectionObserver-gated.
- `prefers-reduced-motion: reduce` → all of the above disabled, content visible immediately.
- One IntersectionObserver, `threshold .18`, `rootMargin -10%`. No scroll-jacking, no libraries.

## 7. Components

`header` (transparent over hero → charcoal with hairline after 40 px scroll), `hero`, `section-split`,
`section-bleed`, `section-statement` (condensed display line over image, like spreads 2 & 12),
`ring-list` (circle list items, spread 4), `dot-list` (vertical hairline + dots, spread 6),
`circle-grid` (spread 10), `partners` (spread 12), `contact/footer` (back cover: logo, motif row, partners, disclaimer).
