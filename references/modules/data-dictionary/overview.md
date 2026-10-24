# Module guide: Data Dictionary

> Integrated capability: Governed semantic layer for this agent — entities, metrics, grains, joins, source of truth. Read before every number. Never invent a metric that is not in references/semantic-schema.md.

# Data dictionary

This skill is **data knowledge**, not analyst knowledge. Other skills teach how to think. This folder is what is true **here**.

Query a named metric, not a remembered table.

## Every turn that needs a number

1. Read `references/semantic-schema.md`. If the metric is missing or `placeholder`, say so. Do not invent.
2. Honor `source-map.md` for which connector is source of truth (volume vs funnel vs telemetry).
3. Apply skip-filters (internal, test, bots) from the schema.
4. Prefer a playbook entry in `query-playbook.md` (saved card / insight) over novel SQL.
5. If the user names a table/event you don't have: "I haven't crawled that. Open Builder and ask me to learn it."

## Files

| Path | Role |
|---|---|
| `references/semantic-schema.md` | entities, metrics, dimensions, grains, caveats |
| `references/query-playbook.md` | canonical questions → how to answer |
| `references/source-map.md` | connector IDs actually used |
| `references/open-questions.md` | unresolved definitions |

Builder (`data-schema-crawler`) writes these. You only **read** them at runtime unless the user is in a build session.

## Never

- Mix Mixpanel and Metabase into one number
- Use a column the profile showed as 17% null as a join key without saying so
- Treat this skill as a Mixpanel or Postgres manual — connectors are tools
