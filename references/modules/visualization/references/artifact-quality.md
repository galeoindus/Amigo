# Artifact quality gate

Use the smallest truthful artifact. A concise answer or table is better when a chart adds no explanatory value.

## Data audit

Before drawing, verify the metric definition, grain, time window, unit, denominator, source id, and reconciliation to the reported headline. Count missing values and duplicate x-values. Missing is not zero; preserve it as a gap. Never silently aggregate duplicate periods or mix incompatible grains.

## Color analysis

Use the Amigo palette: primary `#3333CC`, secondary `#8B9FD4`, then `#C5E17A`, `#E8C97A`, and `#F4B4B4`; ink `#141414`, muted text `#666666`, grid `#E5E5E5`. Reserve editorial highlight `#E6651B` for one key annotation, not a second categorical palette.

- categorical: distinct Amigo colors, ordered by importance
- sequential: one light-to-dark hue for magnitude
- diverging: two hues around a labeled, meaningful midpoint
- never rely on red/green or color alone; add labels, markers, or line styles

## PNG

Use `scripts/chart.py`; do not hand-code a Matplotlib or Plotly layout. It
supports grouped bars and aligned multi-series lines through `--series`, wraps
titles/subtitles/sources, reserves footer space, and runs the Pillow size/blank
gate. If it cannot express the idea, simplify the chart instead of creating a
custom multi-panel figure. Use a finding-led title, window/unit subtitle,
labeled axes, direct labels where useful, and a source id. Supply the underlying
table with a delivered chart.

Programmatic pixel checks do not prove layout quality. After rendering, reject
any chart whose title, subtitle, legend, annotation, axis label, or source
touches/overlaps another element or the canvas edge. Keep titles under 90
characters, subtitles under 180, and sources under 220; move detail to chat.
Do not put “caused”, “drove”, “driven by”, or “the driver” in a chart unless a
causal design supports it. For arithmetic decomposition, say “largest measured
contribution” or name the observed step change.

## PDF

Use ReportLab Platypus and the Amigo typography/colors when the runtime provides them. Keep a weekly digest to one decision-oriented page unless detail requires more. Include definitions, window, sources, caveats, and page numbers. Run available deterministic PDF checks, then render every PDF page and inspect it at full size for clipping, overlaps, broken glyphs, unreadable charts, and split tables.

## Presentation

Reuse the Amigo presentation skill, templates, and assets when available. Prefer Season Mix for display and Matter for body text, with system-font fallbacks. Use narrative titles, one message per slide, cited data, and readable charts. Render all slides and inspect the montage and full-size pages for overlap, overflow, contrast, and inconsistent spacing.

Never deliver a file before its QA gate passes. A tool failure does not permit
a status message; repair and retry silently, then emit only the final answer.
