# Module guide: Metabase Mcp

> Integrated capability: How to use Metabase MCP tools (search, read_resource, construct_query, query, execute_query, execute_sql, execute_question). Protocol only — which table lives in the instance skill. Not Mixpanel, not SigNoz, not Supabase. Envelope A is table_id + t{table}-{index}; envelope B is MBQL 5 portable FKs.

# Metabase MCP

Official server: [MCP docs](https://www.metabase.com/docs/latest/ai/mcp). Endpoint `https://{host}/api/metabase-mcp` (legacy `/api/mcp` still aliases). Tools are generated from the [Agent API](https://www.metabase.com/docs/latest/ai/agent-api). Auth is OAuth 2.0 (or an API key / session when calling the Agent API directly). Results are scoped to the connecting user’s permissions.

This skill is **tool protocol only**. Which table to query lives in an instance skill. Do not guess table ids across instances.

Worked payloads (fictional `Acme Shop`, not any real instance): [examples.md](examples.md).

## Default loop

**First: `tool_search("construct_query")` only — never `"SQL"`.** `tool_search("… SQL")` ranks `supabase_execute_sql`. Ignore Supabase. Copy the live `construct_query` argument names. Metabase MCP servers do not all share one envelope. Do not send MBQL 5 into a `table_id` tool, or `table_id` into an MBQL `query` tool.

**Totals are aggregations.** Never use `query` to census a table (200 rows/page, often no `continuation_token`). `construct_query` + `aggregations` (`count`/`sum`) + `group_by`. `query` is for ≤200 sample rows after you have the count. Table lists come from the instance skill / `read_resource metabase://database/{id}/tables`, not `SHOW TABLES`.

Then:

1. **Pick the table** from the instance skill (preferred) or `search` + `read_resource`. Rank 1 is not a schema.
2. **Build** with whichever envelope the live tool declared (below).
3. **Run** `execute_query` using the key it actually returned (`query` opaque string, or `query_handle` uuid). Check body `status`, not only HTTP 202.
4. **Save (only if asked)**.

### Envelope A — simplified (`table_id` / `metric_id`)

What `tool_search` describes as: *provide table_id; filters, fields, aggregations, group_by, order_by, limit*. Field ids are `t{tableId}-{0-based-column-index}` from `read_resource metabase://table/{id}/fields` (or the instance skill’s `mcp_field_id`).

```json
{
  "table_id": 102,
  "aggregations": [{"function": "count"}],
  "filters": [
    {"field_id": "t102-3", "operation": "equals", "value": "paid"},
    {"field_id": "t102-4", "operation": "greater-than-or-equal", "value": "2026-08-01"},
    {"field_id": "t102-4", "operation": "less-than", "value": "2026-09-01"}
  ]
}
```

`construct_query` returns `{"query": "<opaque>"}`. Pass that string to `execute_query` as `{"query": "<opaque>"}`.

### Envelope B — MBQL 5 (`query` + `prompt`)

```json
{
  "prompt": "How many paid orders last month?",
  "query": {
    "lib/type": "mbql/query",
    "stages": [{
      "lib/type": "mbql.stage/mbql",
      "source-table": ["Acme Shop", "public", "orders"],
      "filters": ["and", {},
        ["=", {}, ["field", {}, ["Acme Shop", "public", "orders", "status"]], "paid"],
        ["time-interval", {}, ["field", {}, ["Acme Shop", "public", "orders", "created_at"]], -1, "month"]
      ],
      "aggregation": [["count", {}]]
    }]
  }
}
```

Returns `{query_handle: "<uuid>"}`. Run with `execute_query` `{query_handle}` or `query`. Grammar: [construct-query.md](construct-query.md). Per-tool args: [tools.md](tools.md).

## Tool map

| Job | Tool |
|---|---|
| Find tables / metrics / cards / dashboards | `search` |
| Inspect a database, table, fields, collection, question, metric | `read_resource` |
| Build query | `construct_query` → opaque `query` string **or** `query_handle` |
| Run query | `execute_query` (pass back whatever `construct_query` returned) |
| Page results | `query` + `continuation_token` |
| Run a saved question | `execute_question` |
| Run raw SQL | `execute_sql` (needs native-query permission) |
| Save SQL as a question without running it | `construct_native_query` → `create_question` |
| Inline chart | `visualize_query` (needs MCP Apps UI) |
| Drill an inline chart | `render_drill_through` |
| Create / rename / archive / move | `create_*` / `update_*` |

`construct_native_query` **does not execute**. Its handle is rejected by `execute_query` / `query`. To run SQL, use `execute_sql`.

## Hard rules

- **Match the live `construct_query` schema** (`tool_search`). Envelope A (`table_id` + `t{id}-{index}`) and envelope B (MBQL 5 portable FKs) both exist. Mixing them 400s.
- **MBQL / structured query, not SQL**, unless the question cannot be expressed that way (window-less SQL, engine-specific functions, `SHOW` / `information_schema`).
- **No integer warehouse field ids** (passing `399` as a field 400s). Envelope A uses `t{table}-{index}`. Envelope B uses `["field", {}, ["<exact database name>", "<schema-or-null>", "<table>", "<column>"]]`.
- **Exact database name** from `search` / `read_resource` / the instance skill. Near-misses → `unknown-database`.
- **No cross-database query.** Two databases = two tool calls; stitch ids in the agent.
- **Envelope B:** every clause is `["op", {options}, …args]` — the `{}` is required even when empty. No `database:` key. No `metabase://…` in `source-table`.
- **200 rows/page, 2_000 rows total** on `query`. Aggregated `execute_query` caps at 10_000. `read_resource` lists cap at 25 items (`truncated` / `total`). **Do not page for a total** — if there is no `continuation_token`, aggregate instead.
- **`tool_search("construct_query")` only.** Never search for `"SQL"`. If Supabase appears, ignore it. `execute_sql` is often missing; `SHOW TABLES` is not the table list.
- **Do not write** (create/update/archive) unless the user asked to save, move, or delete. Archive is a reversible soft delete (`archived: true`).
- **Parameterized saved questions** are not supported by `execute_question`.

## `field_id` vs portable FK

Envelope A field ids are positional: `t{table_id}-{0-based-column-index}` from `read_resource metabase://table/{id}/fields` (indexes drift when columns are added — on 400, re-read fields). Envelope B uses portable FKs, not those strings and not warehouse integer field ids.
