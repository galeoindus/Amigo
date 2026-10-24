# Discovery protocol

Use this full protocol only for the exact entities a quantitative answer derives
from. For metadata-only discovery, use the bounded protocol in `SKILL.md` and
stop after the minimal candidate set is identified.

## Step 1 — Inventory

From bound MCP tools: list entities (tables / events / services / dashboards). Rank by the job. Defer the rest **in writing**.

## Step 2 — Sample

Preview 20–50 rows. Document: identifiers vs attributes, surprising values, types that don't match the name.

Push `LIMIT` as early as the connector allows. Never unbounded fact scans.

## Step 3 — Grain

One row per **what**? Verify uniqueness of the supposed primary key (full count, not only the sample).

## Step 4 — Profile

For each in-scope column: null %, nunique, min/max or top values, date range. Use `scripts/profile_dataset.py` on a fetched sample, then one cheap full-count for PK nulls/dupes if the connector allows.

## Step 5 — Relationships

Candidate FKs: orphan counts on the **full** set when possible. Sample-only joins hide orphans.

## Step 6 — Document immediately

Write into `data-dictionary` `references/semantic-schema.md` / `open-questions.md`:

```markdown
### Entity: {name}
- Row count / grain / PK (verified unique?)
- Freshness (max ts)
- Column table: type, null %, notes
- Data quality issues (quantified)
- Relationships + orphan counts
```

Soft deletes (`deleted_at`, `is_active`, `status`) are filters, not optional footnotes.
