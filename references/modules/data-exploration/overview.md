# Data exploration

**Schema describes structure; profiling describes observed data. Never confuse them.**

## When to use

Use before relying on an unfamiliar table/entity, after schema discovery, or when asked to profile a dataset, inspect nulls/cardinality/freshness, or understand the grain. Use metadata-only discovery for candidate finding; do not treat it as evidence for a metric value.

## Metadata-only discovery

1. Check the semantic dictionary, source map, connector context, and governed/saved metrics first.
2. Run one ranked and filtered search; inspect the top 1–3 candidates.
3. Use at most one discriminating follow-up if it could change the decision, then stop.
4. Return verified facts, the minimal candidate set, and unresolved gaps.

Names are not definitions. A numerator, denominator, grain, source role, or business definition needs a governed formula/query or explicit owner confirmation. If no verified candidate remains, say exactly what is missing; do not substitute a similarly named metric. Never populate or mutate a metric, dashboard, or dictionary unless explicitly requested.

Do not download catalogs, profile unused candidates, or run code merely to reformat connector output. Filter/project/limit at the source. Do not retry the same failed artifact path; use one narrower query or report the blocker.

## Quantitative profiling

Only when the question depends on actual values, use `references/discovery-protocol.md` and complete it for the exact entities supporting the answer. Scripts consume already-fetched, bounded samples; they do not connect to any database.

```bash
python scripts/data-exploration/profile_dataset.py --input /path/to/rows.json
```

Expected JSON is `{"rows": [{"column": "value"}]}` or a JSON array of row objects. As a default, pass no more than 10,000 rows to local profiling, and use source-side aggregates for full-population checks where the connector supports them. A sample is not a total.

## Required profile

- Grain: one row per what? Check candidate primary-key uniqueness across the full in-scope population when feasible.
- Missingness: report a rate and distinguish a null value from an absent field where possible.
- Cardinality and types: report distinct count; validate values rather than trusting column names.
- Numeric range/distribution: min/max, median, useful quantiles and spread; show units.
- Time fields: timezone, range, freshness versus now, and ambiguous date formats.
- Relationships: look for full-population orphan keys when feasible; a successful sample join does not prove the absence of orphans.
- Lifecycle fields: document soft deletes/status/active flags and their exact applied filters.
- Provenance: record source, sample size, extraction time, filters, and limits.

## Stop rules

Stop when requested decision is supported. Recurse at most once if one missing fact would materially change it. Do not claim a metric is verified merely because a schema file exists. Never delete outliers or coerce ambiguous dates to make results fit a story. Mark gaps and move on.
