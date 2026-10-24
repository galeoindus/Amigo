# Chart grammar

| What you're showing | Best chart | Alternatives |
|---|---|---|
| Trend over time | Line | Area if cumulative |
| Category comparison | Vertical bar | Horizontal if many labels |
| Ranking | Horizontal bar | Dot / slope for two periods |
| Part-to-whole | Stacked bar (≤6) | Treemap if hierarchical |
| Composition over time | Stacked area | 100% stacked bar |
| Distribution | Histogram | Box / violin for groups |
| Correlation (2 vars) | Scatter | Bubble for a third |
| Flow / funnel | Funnel / sequential bars | Sankey if many paths |
| Retention | Cohort heatmap | Line of retention curves |
| Multiple KPIs | Small multiples | Not one dual-axis mashup |

## Do not use

- Pie / donut with >5 slices (humans compare angles poorly)
- 3D (distorts)
- Dual axis with different units
- Stacked bar with many middle segments (use small multiples)
- Truncated y-axis that manufactures a crisis

## Accuracy and accessibility

- Bar charts start at zero. Line charts may use a non-zero baseline when the range of variation is the point — disclose it.
- Color encodes data; grey the rest; never red/green only; pattern or linestyle as a second cue.
- Title states the insight. Axes labeled with units. Source and window in the subtitle or footnote.
- Provide a table alternative when the PNG is the deliverable.
