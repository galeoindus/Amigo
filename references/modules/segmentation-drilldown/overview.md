# Module guide: Segmentation Drilldown

> Integrated capability: find which dimensions / versions / geos / plans drove a metric movement. Contribution analysis, Pareto, hierarchical drilldown, Simpson's paradox. Load on "who drove this", "where did it drop", "which segment".

# Segmentation drilldown

Most business root-cause work happens here. Fleet-wide numbers are the start, not the answer.

Rank slices with the script on already-fetched tables.

## Amigo runtime

```text
python scripts/segmentation-drilldown/contribution_analysis.py --input /tmp/slices.json
```

Rows: `dimension`, `before`, `after`. Rank by **share of total delta**, not by percent change of tiny bases.

## Method

```text
conversion down 12%
    -> platform
Android down 21%   iOS flat   Web flat
    -> app_version (on Android)
v6.7 down 38%
    -> country (on Android v6.7)
India down 45%   US down 7%
```

One dimension at a time. After each split, recompute contribution. Do not chain filters until the table shows that slice owns the move.

## Techniques

- Hierarchical drilldown (one dimension per level)
- Top movers by contribution to the total delta
- Pareto: 2–3 slices explain >=70% of |delta|
- Relative vs absolute contribution (a large % on a small base may own little of the move)
- Simpson: overall fell but every platform rose -> **mix shift**; report segment weights alongside rates

## Decompose the sub-measures too

For a ratio (rate = numerator / denominator), a slice can move because its **numerator** moved, its **denominator** moved, or its **weight** in the mix moved. When a slice looks important, split it into numerator effect, denominator effect, and mix effect before calling it the driver. A slice that gained weight while its rate was flat is a mix story, not a performance story.

## STOP

- A 12-way group-by
- Ranking by percent change of a tiny N
- Declaring a root cause from one dimension without the complementary slice
- Grouping by raw user id
- Reporting a rate without the segment weights that produced the aggregate
