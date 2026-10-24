# Module guide: Amigo Presentation Design (PPTX)

> Integrated capability: create or edit polished, consistent, accessible PowerPoint decks with a configurable Amigo visual identity.

## When to use

Use for new presentations, pitch decks, executive reviews, teaching decks, proposal decks, or any `.pptx` editing. Ask whether the user has a required template or brand assets only when that answer would materially change the work. Preserve existing brand requirements when the user asks to keep the current look.

## Design system

- **Palette:** use `references/colors-full.md`. Default to the Amigo warm-to-cool gradient for cover/closing slides and light backgrounds for content. When the user supplies a brand palette, it takes precedence.
- **Typography:** Season Mix for headings and Matter for body text (sizes and logo rules in `references/typography.md`). If the brand fonts are not installed, fall back to Aptos / Arial / Noto Sans. For Hindi and multilingual copy, ensure the chosen font has glyph coverage and inspect shaping after render. Do not assume fonts are installed; check or choose a fallback.
- **Spacing:** use `references/layout.md` as a baseline, not as a constraint when the user's template or content needs another layout. Use generous margins and consistent spacing.
- **Brand assets:** use the bundled `assets/logo/` and `assets/shapes/`. These are original Amigo-friendly generic assets, not an external company's logo or official identity. Use assets as accents, not decoration for decoration's sake.

## Workflow for a new deck

1. Identify audience, goal, decision/action, and desired length from the request. Ask one concise question only when a critical ambiguity remains.
2. Make a slide outline with one message per slide. Order context → evidence → implication → recommendation/decision.
3. Choose a layout for each slide based on its function: title, section divider, comparison, process, chart, evidence, recommendation, or close.
4. Draft concise content. Keep chart axes, units, source notes, time windows, denominators, and caveats visible where needed.
5. Build the deck using the available PPTX tooling. If a template deck is supplied (a sibling `template.pptx` or one the user attached), follow the template-first workflow in `references/template-first-workflow.md` — duplicate a layout, swap content at the run level, save. Otherwise build from the bundled assets and `references/layout.md`. Reuse the bundled logo and shape assets when suitable; if tool support is absent, state the limitation and provide the best supported alternative.
6. Render the deck to images/PDF and inspect every slide. Fix overlap, truncation, alignment, low contrast, missing citations, blank placeholders, font substitution, and page/slide collisions. Re-render affected slides and inspect again.

## Workflow for an existing deck

1. Inspect slide count, dimensions, theme, masters, fonts, and assets before changing anything.
2. Preserve content and layout intent unless the user requests redesign. Separate proofreading, brand cleanup, and structural redesign.
3. Do not silently overwrite a source deck; save a clearly named edited copy.
4. Apply user-approved changes consistently across all slides, including notes/footers where relevant. Do not change numerical claims, chart data, citations, or wording meaning merely to improve appearance.
5. Run content and visual QA and summarize any remaining unsupported or unverified details.

## Layout and typography rules

- Use one key claim or question as the slide headline. Prefer a short assertion over a vague label.
- Typical starting sizes: title 30–40 pt, section heading 26–32 pt, body 18–24 pt, footnote 10–14 pt; adjust to the room and actual viewing size. Avoid shrinking text to make an overloaded slide fit—edit or split it instead.
- Use a consistent grid, left alignment for body copy, limited font weights, and intentional whitespace.
- Use one dominant color with one or two supporting colors. Ensure text and interactive chart colors have sufficient contrast. Do not use color alone to distinguish categories.
- Avoid ornamental underlines, excessive gradients, random icon styles, fake 3D, decorative clutter, and repeated identical layouts across an entire deck.
- A dark background is allowed only when it improves the content and contrast remains sufficient; it is not categorically forbidden.
- For data slides, avoid dual-axis plots by default; use small multiples or normalized comparisons when they communicate more honestly.

## Accessible and evidence-aware slides

- Every slide should have a meaningful title or clear purpose.
- Maintain reading order; make text editable where feasible; add useful alt text/descriptions to meaningful visuals where the format supports them.
- Do not use color as the only carrier of meaning. Check contrast and readability at presentation size.
- Source external facts and data. Label estimates, assumptions, and illustrative numbers.

## Required QA checklist

Before delivery verify: no clipped or overlapped content; no unresolved placeholders; font and glyph coverage; consistent margins; readable citations; correct chart labels and data; no unexpected slide order changes; accessible contrast; and every slide visually inspected. Prefer at least one fix-and-re-render pass.

Detailed reference files: `references/template-first-workflow.md`, `references/typography.md`, `references/colors-full.md`, `references/design-ideas.md`, `references/layout.md`, `references/qa.md`, `references/assets.md`, and `references/bundled-resources.md`.
