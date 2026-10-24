# Amigo typography

> Merged from the `pptx-master` brand spec. Load only when you need exact font names or sizes.

## Families

**Display: Season Mix** — headings and captions only. Regular weight only.

**Sans-serif: Matter** — body text, sub headings, eyebrow tags, labels, UI. Weights: Thin, Light, Regular, Medium, SemiBold, Bold, Heavy, Black. Plus Matter SemiMono for code/data.

Weight comes from font-name selection (e.g. "Matter SemiBold"), never the bold attribute. No italics, underlines, strikethrough, or highlights.

If the Amigo brand fonts are not installed, fall back to Aptos (or Arial / Noto Sans) and verify render fidelity. For Hindi and other Indic copy, confirm the chosen font has glyph coverage and inspect shaping after render.

## Size table (design px -> PPTX pt)

| Element | Font | Design (px) | PPTX (pt) | XML sz |
|---|---|---|---|---|
| Cover / hero title | Season Mix | 64px | 48pt | 4800 |
| Slide title | Season Mix | 48px | 36pt | 3600 |
| Section title | Season Mix | 36px | 27pt | 2700 |
| H2 small | Season Mix | 32px | 24pt | 2400 |
| Sub heading | Matter | 28px | 21pt | 2100 |
| Eyebrow tag | Matter | 24px | 12pt | 1200 |
| Body large | Matter | 18px | 13.5pt | 1350 |
| Footer text | Matter | 16px | 8pt | 800 |
| Body medium | Matter | 15px | 11.25pt | 1125 |
| Body small | Matter / SemiMono | 14px | 10.5pt | 1050 |
| Body x-small | Matter | 12px | 9pt | 900 |

## Logo

| File | Colour | Use |
|---|---|---|
| Amigo Wordmark Black | `#131313` | Light backgrounds (most content slides) |
| Amigo Wordmark White | `#FFFFFF` | Over a dark/saturated area (title/closing) |
| Amigo Monogram Black | `#131313` | Light backgrounds, small spaces |
| Amigo Monogram Black-1 | `#FFFFFF` | Over a dark/saturated area |

Rules: default to the wordmark unless space is limited. On content slides the monogram may use a `#999999` tint. Never stretch, rotate, or recolour. Do not place a logo where it loses contrast.
