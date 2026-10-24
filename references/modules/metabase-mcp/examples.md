# Worked examples (fictional shop)

These payloads are **invented**. Database name `Acme Shop`, schema `public`, tables `customers` / `orders` / `order_items` / `products`. Table ids `101–104` are fake. Copy the **shape**, not the names — real names come from `search` / `read_resource` on whichever Metabase you are connected to.

Do not reuse table ids from a real Metabase instance here.

## 1. User asks: “How many paid orders last month?”

### Step A — `search`

```json
{
  "term_queries": ["orders"],
  "semantic_queries": ["paid orders last month"]
}
```

Suppose hits include `{type:"table", id:102, name:"orders", database_id:9, database_schema:"public"}` **and** `{type:"table", id:88, name:"orders", database_id:1}`. Rank is not a schema. Confirm database name with `read_resource`.

### Step B — `read_resource`

```json
{
  "uris": [
    "metabase://database/9",
    "metabase://table/102",
    "metabase://table/102/fields"
  ]
}
```

You learn: exact database name is `Acme Shop`; columns include `status`, `created_at`, `total`, `customer_id`; `customer_id` has `fk_target_fully_qualified_name="public.customers.id"`.

### Step C — `construct_query`

Pass the user’s original wording as `prompt`.

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

Response: `{"query_handle": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}`.

Wrong (400s):

```json
["field", {}, 399]
["field", ["Acme Shop", "public", "orders", "status"]]
["count"]
{"source-table": "metabase://table/102"}
```

### Step D — `execute_query` **or** `query`

```json
{"query_handle": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}
```

Body `status` must be `"completed"` (HTTP 202 is not enough). Example rows: `[["count"], [1284]]`.

Same question in one shot with `query` (omit `construct_query`):

```json
{"query": { "lib/type": "mbql/query", "stages": [ /* same stage as above */ ] }}
```

## 2. “Revenue by month, then keep months over $50k”

Filter is a constraint; “by month” is a breakout; “then keep” is a **second stage**.

```json
{
  "query": {
    "lib/type": "mbql/query",
    "stages": [
      {
        "lib/type": "mbql.stage/mbql",
        "source-table": ["Acme Shop", "public", "orders"],
        "filters": ["=", {}, ["field", {}, ["Acme Shop", "public", "orders", "status"]], "paid"],
        "aggregation": [["sum", {}, ["field", {}, ["Acme Shop", "public", "orders", "total"]]]],
        "breakout": [["field", {"temporal-unit": "month"},
                      ["field", {}, ["Acme Shop", "public", "orders", "created_at"]]]]
      },
      {
        "lib/type": "mbql.stage/mbql",
        "filters": [[">", {}, ["field", {}, "sum"], 50000]]
      }
    ]
  }
}
```

Later-stage column is the bare aggregation name `"sum"`, not `"Sum of Total"`.

## 3. Implicit join: “paid revenue by customer city”

`read_resource …/fields` showed one FK `orders.customer_id → customers.id`. Reference the related column directly:

```json
{
  "query": {
    "lib/type": "mbql/query",
    "stages": [{
      "lib/type": "mbql.stage/mbql",
      "source-table": ["Acme Shop", "public", "orders"],
      "filters": ["=", {}, ["field", {}, ["Acme Shop", "public", "orders", "status"]], "paid"],
      "aggregation": [["sum", {}, ["field", {}, ["Acme Shop", "public", "orders", "total"]]]],
      "breakout": [["field", {}, ["Acme Shop", "public", "customers", "city"]]]
    }]
  }
}
```

If that 400s with `no-fk-path` or `ambiguous-fk`, use an explicit join (or two queries and stitch). ClickHouse almost always has **no** Metabase FKs — skip this pattern.

### Explicit join (same question)

```json
"joins": [{
  "alias": "Cust",
  "strategy": "left-join",
  "stages": [{"lib/type": "mbql.stage/mbql",
              "source-table": ["Acme Shop", "public", "customers"]}],
  "conditions": [["=", {},
    ["field", {}, ["Acme Shop", "public", "orders", "customer_id"]],
    ["field", {"join-alias": "Cust"}, ["Acme Shop", "public", "customers", "id"]]]]
}],
"breakout": [["field", {"join-alias": "Cust"}, ["Acme Shop", "public", "customers", "city"]]]
```

Every joined-side field must carry `join-alias`.

## 4. List rows (not a metric)

“Show the last 20 orders for customer 42.” No aggregation — project `fields` + `order-by` + `limit`.

```json
{
  "query": {
    "lib/type": "mbql/query",
    "stages": [{
      "lib/type": "mbql.stage/mbql",
      "source-table": ["Acme Shop", "public", "orders"],
      "filters": ["=", {}, ["field", {}, ["Acme Shop", "public", "orders", "customer_id"]], 42],
      "fields": [
        ["field", {}, ["Acme Shop", "public", "orders", "id"]],
        ["field", {}, ["Acme Shop", "public", "orders", "created_at"]],
        ["field", {}, ["Acme Shop", "public", "orders", "total"]],
        ["field", {}, ["Acme Shop", "public", "orders", "status"]]
      ],
      "order-by": [["desc", {}, ["field", {}, ["Acme Shop", "public", "orders", "created_at"]]]],
      "limit": 20
    }]
  }
}
```

## 5. Page past 200 rows

First `query` response includes `continuation_token` when the page is full. Next call:

```json
{"continuation_token": "eyJxdWVyeSI6ey..."}
```

Do not send `query` and `continuation_token` together. Stop at 2_000 rows or aggregate instead of paging the raw table.

## 6. Two databases — two calls

`Acme Shop` has no employee emails. `Acme HR` does. You **cannot** put both names in one MBQL object.

1. Query Shop for `customer_id` / `email`.
2. Query HR `employees` filtered to those emails.
3. Stitch in the agent (compare as strings).

## 7. Raw SQL only when MBQL cannot

`SHOW TABLES`, engine-specific functions, or a CTE Metabase will not build. Then `execute_sql`:

```json
{"database_id": 9, "sql": "SELECT date_trunc('week', created_at), count(*) FROM orders WHERE status = 'paid' GROUP BY 1"}
```

Do not `construct_native_query` if you intend to **run** it — that handle is for `create_question` only.

## 8. Save (only if the user asked)

```json
{
  "name": "Paid orders last month",
  "query": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "display": "scalar",
  "description": "Count of orders with status=paid in the previous calendar month."
}
```

`query` here is the **handle** from `construct_query`, not the MBQL object.

## Trap: `search("sessions")`

On a busy instance this often ranks an auth `sessions` table or a payment `checkout_sessions` table ahead of the product event table. Always read `database_id` + schema from the hit, then `read_resource` the table, before counting.
