# MBQL 5 for `construct_query` / `query`

Source: Metabase `construct_notebook_query` prompt / MCP resource `metabase://docs/construct-query.md`.

The `query` value is a JSON **object** (never a quoted string). Database is inferred from the first stage’s `source-table` / `source-card`. No top-level `database:`.

## Minimal

```json
{
  "lib/type": "mbql/query",
  "stages": [{
    "lib/type": "mbql.stage/mbql",
    "source-table": ["Sample Database", "PUBLIC", "ORDERS"],
    "aggregation": [["count", {}]],
    "breakout": [["field", {"temporal-unit": "month"},
                  ["Sample Database", "PUBLIC", "ORDERS", "CREATED_AT"]]]
  }]
}
```

Two rules that 400 most often:

1. Every clause is `["op", {options}, …args]` — `{}` is required. Bad: `["count"]`, `["field", ["DB","SCH","TBL","COL"]]`.
2. Every column is a 4-segment portable FK: `["<exact database name>", "<schema-or-null>", "<table>", "<column>"]`. Schemaless DBs use `null` in the schema slot. JSON-unfolded fields append segments (`traits`, `email`, …).

## Stage

First stage: exactly one of `source-table` or `source-card`. Later stages omit it and consume the previous stage.

Optional keys: `filters`, `aggregation`, `breakout`, `expressions`, `fields`, `joins`, `order-by`, `limit`, `page`.

`source-table` is a 3-segment name `["DB", "schema", "table"]`, **not** a `metabase://` URI.

`source-card` is the card’s 21-char `portable_entity_id` from `search` / `read_resource`. Never invent it. Card columns are referenced by **output machine name** (`["field", {}, "total"]`), not portable FK.

## Fields

```json
["field", {}, ["Acme Shop", "public", "orders", "status"]]
```

Options: `temporal-unit`, `join-alias` (required on every joined-side ref), `source-field` (portable FK of the FK column when implicit join is ambiguous), `binning`.

Later-stage refs use a string name: `["field", {}, "count"]`. Aggregation output names are the **bare function** (`sum`, `count`, `max`, then `max_2`). A month breakout of `CREATED_AT` is still named `CREATED_AT`.

## Filters / aggregations / order

```json
"filters": [["and", {},
  [">", {}, ["field", {}, ["DB", "public", "orders", "total"]], 100],
  ["=", {}, ["field", {}, ["DB", "public", "orders", "status"]], "paid"]]]
```

```json
"aggregation": [["sum", {}, ["field", {}, ["DB", "public", "orders", "total"]]], ["count", {}]]
"order-by": [["desc", {}, ["aggregation", {}, 0]]]
```

A constraint is a **filter**, not a breakout. “by / per / over time” → `breakout`. Absolute dates (`in 2024`) → range filter; relative language (`last 30 days`) → `time-interval` / `relative-datetime`.

## Joins

**Implicit:** reference a related table’s field. Works only when `read_resource …/fields` shows exactly one FK to that table. Multiple FKs → `ambiguous-fk` (retry with `source-field`). No FK → `no-fk-path`. ClickHouse typically has **no** Metabase FKs — do not join; run two queries and stitch.

**Explicit:**

```json
"joins": [{
  "alias": "Products",
  "strategy": "left-join",
  "stages": [{"lib/type": "mbql.stage/mbql",
              "source-table": ["Sample Database", "PUBLIC", "PRODUCTS"]}],
  "conditions": [["=", {},
    ["field", {}, ["Sample Database", "PUBLIC", "ORDERS", "PRODUCT_ID"]],
    ["field", {"join-alias": "Products"},
     ["Sample Database", "PUBLIC", "PRODUCTS", "ID"]]]]
}]
```

Strategies: `left-join` (default), `right-join`, `inner-join`, `full-join`. Conditions: only `=` `!=` `<` `<=` `>` `>=`. Every joined-side field must carry `join-alias`.

## Metrics / measures / segments

- Metric: `source-table` = the metric’s **base table**; `aggregation`: `["metric", {}, "<portable_entity_id>"]`. Never put a metric in `source-table`.
- Measure: `["measure", {}, "<portable_entity_id>"]` in `aggregation`.
- Segment: `["segment", {}, "<portable_entity_id>"]` in `filters`.

Copy `portable_entity_id` verbatim from `read_resource`. Never invent it.

## Multi-stage

Post-aggregation filter: stage 0 aggregates + breakout; stage 1 filters `["field", {}, "count"]`. Re-aggregate the same way. Joins/expressions/filters are valid in later stages.

## Operator catalog (canonical names)

Aggregations: `count`, `cum-count`, `sum`, `cum-sum`, `avg`, `min`, `max`, `median`, `percentile`, `distinct`, `distinct-where`, `count-where`, `sum-where`, `share`, `stddev`, `var`, `metric`, `measure`.

Filters: `and` `or` `not` · `=` `!=` `in` `not-in` · `<` `<=` `>` `>=` `between` `inside` · `is-null` `not-null` `is-empty` `not-empty` · `starts-with` `ends-with` `contains` `does-not-contain` (`{"case-sensitive": false}`) · `time-interval` `during` `relative-time-interval` · `segment`.

Expressions: `+` `-` `*` `/` `abs` `power` `sqrt` `exp` `log` `ceil` `floor` `round` `integer` `float` · `concat` `substring` `replace` `regex-match-first` `split-part` `length` `trim` `ltrim` `rtrim` `upper` `lower` `host` `domain` `text` · `case`/`if` `coalesce` · `datetime-add` `datetime-subtract` `datetime-diff` `interval` `get-year` `get-month` `get-day` `get-hour` `get-day-of-week` `now` `today` `relative-datetime` `absolute-datetime`. Do **not** subtract dates with `-`.

Temporal units: `day` `week` `month` `quarter` `year` `hour` `minute` · extraction `day-of-week` `day-of-month` `hour-of-day` …

Order: `["asc", {}, ref]` / `["desc", {}, ref]`.

## Do not

- `["count"]` without `{}`
- Numeric warehouse field ids (`399`) or notebook `t102-3` strings inside MBQL 5 field slots
- `metabase://table/102` as `source-table`
- Cross-database portable FKs in one query
- `visualization` nested inside `query` (it is a sibling of `query` on some clients)
- Clause heads `[aggregate,…]` `[filter,…]` — those are stage **keys**, not ops
- Typos: write `count-where` not `count-if`; `distinct` not `count-distinct`; `datetime-diff` not `temporal-diff`
