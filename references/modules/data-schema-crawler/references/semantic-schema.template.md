# Semantic schema

Company: `<placeholder>`
Product / scope: `<placeholder>`
Timezone: `<placeholder>`
Audience: `<placeholder>`
Last crawled: `<placeholder>`

## Entities

| Entity | Grain | Primary key | Source |
|---|---|---|---|
| `<user>` | `<placeholder>` | `<placeholder>` | `<placeholder>` |

## Metrics

| Name | Formula / definition | Grain | Window | Source (dashboard/card/event) | Status |
|---|---|---|---|---|---|
| `<placeholder>` | `<placeholder>` | `<placeholder>` | `<placeholder>` | `<placeholder>` | placeholder |

Status is `verified` (sampled), `inferred` (from a dashboard title, not sampled), or `placeholder`.

## Dimensions

| Name | Type | Known values / enum | Caveats |
|---|---|---|---|
| `<placeholder>` | string | `<placeholder>` | `<placeholder>` |

## Joins

- `<entity A>.<key> = <entity B>.<key>` — `<why / when it breaks>`

## Forbidden / landmines

- `<PII columns, unbounded scans, lookalike metrics>`

## When in doubt, skip

- `<internal tenants, staff email domain, test apps, …>`
