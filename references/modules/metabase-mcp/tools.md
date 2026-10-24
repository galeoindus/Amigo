# Metabase MCP tools

Args below match the official MCP manifest (Agent API metadata + MCP schema overrides). Worked payloads (fictional shop, not a real instance): [examples.md](examples.md).

## Discovery

### `search`

Find tables, metrics, cards, dashboards, collections.

```json
{"term_queries": ["orders"], "semantic_queries": ["paid orders last month"]}
```

At least one of `term_queries` or `semantic_queries`. Rank is Reciprocal Rank Fusion, **not** a schema. Same table name exists in multiple databases (`sessions` is often auth cookies or payment checkout, not the product event table). Confirm `database_id` / `database_schema` before querying.

### `read_resource`

Up to **5** `metabase://` URIs per call. List URIs return ≤25 items and set `truncated` / `total`.

```json
{"uris": ["metabase://table/102", "metabase://table/102/fields"]}
```

**Navigation:** `metabase://databases` · `metabase://collections` (`?tree=true`) · `metabase://user/recent-items`

**Database:** `metabase://database/{id}` · `/tables` · `/models` · `/schemas` · `/schemas/{schemaName}/tables`

**Collection:** `metabase://collection/{id}` (`id` may be `"root"` / `"trash"`) · `/items` · `/subcollections`

**Entity:** `metabase://table/{id}` (`/fields`, `/fields/{field_id}`, `/derived`) · `metabase://model/{id}` (`/fields`, `/sources`) · `metabase://question/{id}` (`/fields`, `/sources`) · `metabase://metric/{id}` (`/dimensions`) · `metabase://transform/{id}` (`/sources`, `/target`) · `metabase://dashboard/{id}` (`/items`)

FK columns on `/fields` are tagged `fk_target_fully_qualified_name="schema.table.field"`. That is the only join `construct_query` will auto-wire.

These URIs are **not** query sources. Never put `metabase://…` in `source-table`.

A second URI namespace is MCP resources (not this tool): `metabase://docs/construct-query.md` via `resources/read`.

## Query

### `construct_query`

Build MBQL 5. Returns `{query_handle: "<uuid>"}`. Does not run the query.

```json
{
  "query": {
    "lib/type": "mbql/query",
    "stages": [{
      "lib/type": "mbql.stage/mbql",
      "source-table": ["Sample Database", "PUBLIC", "ORDERS"],
      "aggregation": [["count", {}]],
      "limit": 100
    }]
  },
  "prompt": "how many orders?"
}
```

`prompt` is optional: the user’s exact original message, unsummarized. Grammar: [construct-query.md](construct-query.md).

Input errors are HTTP 400 with `error` / `path` / `candidates` (`unknown-database`, `unknown-table`, `unknown-field`, `unknown-card`, `missing-source-in-first-stage`, `ambiguous-fk`, `no-fk-path`, `uri-in-source-table`). Read the message and retry.

### `query`

Construct-and-execute, or page. Body is **one of**:

| Field | When |
|---|---|
| `query` | Fresh MBQL 5 object (same shape as `construct_query`) |
| `query_handle` | UUID from `construct_query` — preferred over raw `query` |
| `continuation_token` | Next page from a previous `query` response |

`query` and `continuation_token` are mutually exclusive. Per-page size = the query’s `limit` (default 200, hard-capped 200). Total cap 2_000 rows. HTTP 202 streaming — check `status` in the body (`completed` / `failed`), not just the status code.

### `execute_query`

Run a previously constructed MBQL handle.

```json
{"query_handle": "<uuid>"}
```

Also accepts `query` as the base64 string from Agent API `/v2/construct-query`. Prefer the handle. Native (SQL) handles are **rejected** — use `execute_sql`.

Row limits: 2_000 simple, 10_000 aggregated.

### `execute_sql`

Raw SQL. Requires native-query permission on that database. Instance setting `mcp-execute-sql-enabled` can disable it (default on).

```json
{"database_id": 9, "sql": "SELECT count(*) FROM orders WHERE status = 'paid'"}
```

One statement. Same streaming response shape as `execute_query`. Skip unless MBQL cannot express the question.

### `construct_native_query`

Build a native SQL query and store it. Returns `query_handle` for `create_question` only. **Does not execute.** `execute_query` / `query` reject native handles.

### `execute_question`

Run a saved question by integer `id`. Parameterized questions error. Same row metadata as `execute_query`.

### `visualize_query` / `render_drill_through`

Inline chart in clients that advertise MCP Apps UI (`text/html;profile=mcp-app`). `visualize_query` takes a `query_handle` (or constructed query). `render_drill_through` renders a drill from an inline viz. Bar / line / table only. If the client lacks Apps UI, the tool errors — fall back to `execute_query` and describe the rows.

## Write

Patch semantics on all `update_*`. `archived: true` is a reversible soft delete. `collection_id` moves the entity.

| Tool | Notes |
|---|---|
| `create_question` | `name`, `query` = handle from `construct_query` or `construct_native_query`, optional `display`, `description`, `collection_id`. Native save needs native-query permission. |
| `update_question` | Optional `query` handle to replace the dataset. |
| `create_metric` | Handle from `construct_query`. Query must have **one aggregation** and at most one date grouping. |
| `update_metric` | Replacement `query` must still be a valid metric. |
| `create_dashboard` | Optional `question_ids` — auto-positioned on the grid. |
| `update_dashboard` | Metadata + optional `dashcards` mutations (`add`, `add_heading`, `add_text`, `update_text`, `remove`, `move`). |
| `create_collection` | Optional `parent_collection_id`. |

Do not call write tools unless the user asked to save, rename, move, or delete.

## Auth / scopes (when connecting a client)

| Scope | Tools |
|---|---|
| `agent:search` | `search` |
| `agent:resource:read` | `read_resource` |
| `agent:query:construct` | `construct_query` |
| `agent:query` | `query` |
| `agent:query:execute` | `execute_query` |
| `agent:sql:construct` | `construct_native_query` |
| `agent:sql:execute` | `execute_sql` |
| `agent:question:*` | create / update / execute question |
| `agent:metric:*` | create / update metric |
| `agent:dashboard:*` | create / update dashboard |
| `agent:collection:create` | `create_collection` |

The work agent already has the MCP bound. Do not reconfigure OAuth from this skill.
