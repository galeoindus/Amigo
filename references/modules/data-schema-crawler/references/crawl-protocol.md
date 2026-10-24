# Crawl protocol

Fan-out cap: 8 dashboards, 20 cards, 12 events, 6 services, 1 sample query each. Prefer saved artifacts over raw SQL.

## Metabase

Order: `list_databases` → `list_dashboards` → rank (`scripts/metabase_harvest.py`) → `get_dashboard` for top 8 (cards are nested — **do not** `list_cards` unfiltered) → `execute_card` on 3 gold cards with default filters (last 7 days).

Extract from each card:

- display name, description, database id
- native SQL **or** MBQL aggregation + breakouts
- default filters (date, app_id, tenant)
- the metric the title implies

Do **not** `execute_query` with unbounded `SELECT *`. If you must run SQL: `LIMIT 20`, always `WHERE` a time column, never scan a fact table without a date predicate.

If the current Metabase connector exposes supported search/field/query endpoints, prefer those for discovery; keep raw SQL for a small number of narrowly scoped verification queries. Current Metabase Agent API behavior (versioned endpoints, permission-scoped requests, up to 200 rows per request with continuation tokens) applies only when that Agent API is actually the connected interface; do not project it onto arbitrary MCP wrappers.

Whatever Metabase connector the user bound, treat the instance as unknown and
`list_databases` first. What you are looking for, in order:

| Look for | Why it matters |
|---|---|
| a fresh transactional replica (Postgres/MySQL) | source of truth for volume and revenue |
| an aggregate store (Redshift/ClickHouse/BigQuery) | fast rollups, but may lag |
| the platform's own internal DB | usually NOT product data — do not report from it |

Record the id→meaning map in `semantic-schema.md`. Never assume a database id
means the same thing across two instances.

## Mixpanel

Run `python scripts/harvest_plan.py mixpanel` and follow that order. It is tuned to harvest the full event list, the top board's layout, and one sampled insight in **5–6 calls** — not fifty.

1. `Get-Projects` (not Get-Business-Context first — that needs org or project id).
2. `Get-Events(project_id, include_details=true, query=<job keyword>)` — one dense list. Never per-event Get-Events.
3. `Search-Entities` with `entity_types=['dashboard','insights','funnels','retention']` (not `report`).
4. `Get-Dashboard(include_layout=true)` on the top board — report ids are in the layout. Skip N× Get-Report for discovery.
5. `List-Properties(resource_type='Event', events=[top 8])` — capital **E**. One table of properties.
6. `Get-Report` **one** gold insight to verify rows exist.

Distill:

- **Events** as facts (name, when it fires, required properties) — cap 12
- **User properties** as dimensions
- **Funnels** as named metrics (do not rebuild a funnel the user already saved)

Never query "all events" without a date range. Mixpanel will timeout and burn quota.

If tools are missing, unauthorized, or return 401: ask the user for the smallest useful export or for authorization through the host-supported flow, and mark facts `<unverified>`. Do not invent an event taxonomy.

## SigNoz

Walk (`scripts/signoz_harvest.py "<symptom>"`):

1. Services / APM list — keep 6 in-scope
2. Named dashboards — **read widget queries before guessing metric names** (saves 3–5 wrong calls)
3. Alert rules if exposed — reuse `condition.compositeQuery`
4. One traces or metrics query copied from the widget. Pin `serviceName` + time window. Two query shapes coexist; do not translate.

Distill:

- **SLIs**: latency p50/p99, error rate, saturation
- **Identity keys**: `service.name`, `gen_ai.agent.name`, `trace_id`, `deployment.environment`
- **Join keys back to product analytics**: `session_id` / `trace_id` / `user_id`, plus whatever the instance's own span attributes expose

Cap: 6 services. Internal noise services (otel-collector, redis) stay off the schema unless the job is platform SRE.

## PostHog / Amplitude

Same high-level shape as Mixpanel: events → properties → saved insights → one sample. Validate vendor-specific tools, names, pagination, and filters. Map their nouns onto the same schema headings (metrics / dimensions / entities) so the runtime skill does not fork per vendor.

## Spreadsheets / files

If the user uploaded a workbook and no warehouse is connected:

1. Profile sheets, column types, date formats, row counts
2. Halt on ambiguous dates (day-first vs month-first) — ask, never guess
3. Write the schema from the file, mark source as `upload:{filename}`

## Recursion stop conditions

Stop a branch when any of:

- you already have a named metric covering the question
- the object is a duplicate of one you opened (same SQL / same event)
- you hit the fan-out cap
- the user said the area is out of scope

Then distill. Do not keep listing.
