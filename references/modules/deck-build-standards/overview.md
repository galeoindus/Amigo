# Deck build standards

Use this guide alongside `../brand-for-pptx/overview.md`. It defines checkable content and quality rules; the brand module supplies the Amigo visual system and assets. A user's existing brand or required template takes precedence over Amigo defaults.

## Planning gate

Establish the audience, decision/action, story, evidence, and approximate length before styling. For high-stakes or large presentations, show the outline for approval before a full build. For small or low-risk requests, proceed with a concise outline and clearly flag assumptions rather than blocking needlessly.

## Layout standards

- **Title slide:** title, optional concise subtitle, date/author only when useful. Avoid clutter.
- **Content slides:** a short assertion headline in the top zone; supporting body and source note below.
- **One main message per slide.** One chart is the default; combine visuals only when comparison is the point and readability remains clear.
- Every chart, diagram, or infographic must include labels and enough data/explanation to make its meaning intelligible without narration.
- Keep body copy left-aligned unless the content or chosen design calls for another alignment. Use sentence case and a clear typographic hierarchy.
- Keep bullets short; use a table, diagram, or second slide when detail cannot fit legibly. Never shrink text just to preserve a slide count.
- Allow responsive space when titles wrap; do not let heading, subtitle, chart, source note, or footer overlap.

## Chart rules

- Label axes, units, date range, denominator/sample size where relevant, and filters/caveats.
- Do not truncate bar chart axes unless there is a clearly disclosed and defensible reason; zero-baseline bars are the default for magnitude comparison.
- Order categories by value unless time or natural order matters.
- Label small sets of bars directly when that improves scanability. Use small multiples or normalization instead of deceptive dual-axis charts.
- State the chart's takeaway in the title or nearby text. Do not invent charts or values; distinguish observed data from illustrative examples.
- For estimates, state the estimation method and uncertainty when relevant. Every consequential number needs a traceable source.

## Source notes

Use a compact format such as:

`Source: <origin>, <specific dataset/report/page>, <period or accessed date>; filters: <material filters>`

Cite each slide containing externally sourced facts or data. On a slide with several numbers, one note may cover a clearly identified table/data series; avoid implying that illustrative values are observed facts.

## Amigo visual system

Use the color, typography, layout, logo, and shape guidance in `../brand-for-pptx/references/`. Apply user-provided brand assets when requested. Use Amigo assets only when an Amigo identity is appropriate; don't force logos, footers, gradient covers, or decorative shapes onto user-branded work. Do not assume fonts are installed or embedded; verify render fidelity and use appropriate multilingual fallbacks.

## Accessibility and visual QA

- Give every slide a meaningful title, visible or appropriately hidden for accessibility.
- Keep reading order logical; use editable text and built-in slide layouts where possible.
- Provide alt text/description for meaningful visuals when supported; label charts in text, not by color alone.
- Check contrast and readability at presentation size. Do not rely on color alone to communicate status or categories.
- Inspect every rendered slide for clipping, overlap, illegible labels, missing glyphs, placeholder text, inconsistent margins, broken links, missing citations and unexpected slide order.
- Run at least one render → inspect → fix → re-render pass. If visual rendering/checker tools are unavailable, say so and use the best available structural checks.

## Pre-delivery checklist

Report pass/fail/blocked for the checks that can be evaluated:

1. Does the headline-only sequence convey the full argument?
2. Does each slide have one primary message and a meaningful title?
3. Does every factual number have a traceable source/period or a clear illustrative label?
4. Are all placeholders resolved?
5. Are bullets, typography, and slide count appropriate for the audience?
6. Are charts labelled with units, periods, and relevant denominators/filters?
7. Are visuals explained with labels, data, or nearby text?
8. Is reading order logical, contrast adequate, and color not the sole signal?
9. Are there collisions, text overflow, cropped content, or font substitutions?
10. Was the deck rendered and visually inspected after at least one fix cycle?

Never hide a failed or untested check. Distinguish a check that passed from one that could not be run.
