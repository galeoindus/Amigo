# Module guide: Metric Reasoning

> Integrated capability: governed metric semantics — identities, measures vs dimensions vs entities, rates vs counts. Load when a KPI moved, two sources disagree, or someone says "conversion", "active users", or "revenue" without a definition. Do not casually redefine a KPI.

# Metric reasoning

Query a **named metric** from `../data-dictionary/` first. If it is not there, say so — do not freelance a definition.

## Amigo runtime

- Load `references/identities.md` when decomposing a move.
- Connectors fetch; this skill only reasons about algebra and grain.

## Metric contract

A metric is not a name; it is a contract. Before using or comparing one, be able to state:

```
Name:
Decision it informs:
Entity / grain:            (user, order, session, account, service)
Event set / measure:       (the exact events or numeric fact)
Numerator / denominator:   (for every rate)
Window + time zone:        (rolling vs calendar; explicit zone)
Exclusions:                (internal, test, bots, null ids)
Identity policy:           (how devices/accounts resolve to one entity)
Freshness:                 (when the data was last complete)
Owner / version:           (who governs it, and which definition version)
```

"MAU" is not a definition. "Unique production accounts that completed one of three key actions in the trailing 30 days, UTC" is. If any line is unknown, label the metric `inferred` or `placeholder` — never present it as governed.

## Vocabulary (source-agnostic)

| Term | Meaning |
|---|---|
| Entity | Grain / join key (user, order, session, service) |
| Dimension | Filter or group-by (country, plan, version) |
| Measure | Numeric fact at a grain (order_amount, event_count) |
| Simple metric | One aggregation of one measure |
| Ratio | num metric / denom metric — **eligible population must be named** |
| Derived | Expression over metrics (revenue = customers × orders/customer × AOV) |

## Decision flow

1. Is the metric in the data dictionary? Query that definition.
2. If the question needs a missing dimension, **say the definition is incomplete** — do not silently change the KPI.
3. Only then write a one-off query, and record the gap in `../data-dictionary/references/open-questions.md`.

## Denominator effects

A rate can rise while the count falls. Always report **numerator count, denominator count, and the rate** together for any rate question. A rate with no visible denominator is not evidence.

## Two sources disagree

Do not average. Name the source of truth from the data dictionary's `source-map.md`. Typical: warehouse for volume, product analytics for funnels/retention, observability for latency/errors.

## STOP

- Inventing an "active user" window
- Presenting a mean on a skewed measure without a median
- Mixing product-analytics and warehouse events into one number
- Redefining a dictionary metric "just this once"
- Quoting a rate without its numerator and denominator
