# Module guide: Product Analytics

> Integrated capability: funnels, retention, cohorts, activation, adoption, churn. Domain pack for product questions. Use with product-analytics connectors; do not duplicate root-cause analysis or charts. Defines the metric hierarchy, diagnostic order, and common traps a senior product analyst applies.

# Product analytics

This module names **product questions** and the metrics that answer them. `../root-cause-analysis/overview.md` owns why. `../segmentation-drilldown/overview.md` owns which slice. MCP tools (product analytics) fetch events; `../data-dictionary/overview.md` holds the governed definitions.

## Amigo runtime

```text
python scripts/product-analytics/funnel.py --input /tmp/events.json --steps signup,onboarding,activation
```

Rows: `user_id`, `event`, optional `ts`. Steps come from the data dictionary — do not invent activation. The script enforces step **order** when timestamps are present.

## Core principle: start with product value, not generic activity

Before calculating DAU, WAU, MAU, retention, or engagement, determine what behavior represents meaningful product value for **this** product.

- Messaging product: send/read meaningful messages.
- Collaboration product: create, edit, share, or collaborate on an artifact.
- Search product: successful search followed by a useful downstream action.
- AI assistant: successful task completion, accepted answer, artifact created, tool task completed.
- Marketplace: successful match, booking, transaction, or fulfilled order.
- B2B SaaS: account members completing the workflow the product is sold to enable.

An "active user" should mean a user who performed a **value-bearing event**, not merely opened the application. The "A" in DAU/WAU/MAU is a product decision, not a default. If no explicit definition exists, calculate both broad activity and core activity — label them clearly and never silently substitute one for the other. Prefer rolling windows (trailing 1/7/30 days) and say so; state the time zone.

## Metric hierarchy

Organize metrics into levels (focus metric, level-1 checks, level-2 drivers). When a top-level KPI changes, decompose it into the lower-level drivers before reporting.

## Canonical metric vocabulary

Never use an ambiguous metric without defining it. "D7 retention" could mean returns exactly on day 7, on or after day 7, at least once during days 1–7, or active within a rolling 7-day window. These are not interchangeable. Name the retention type, the birth event, the return event, the window unit (day/week/month), and whether the window is rolling or calendar.

## Always preserve the denominator

For every rate, report: numerator, denominator, time window, entity counted, qualifying event, filters, and cohort definition.

Example: `D7 retained activation cohort = 1,820 / 5,400 users = 33.7%, where the denominator is users who completed activation during the week of Aug 3 and the numerator is those who performed a core-value event exactly 7 days later.`

## Funnels

Ordered journey. Report step conversion, overall conversion, drop-off, time-to-convert, and segment comparison. A funnel is only meaningful if the steps are ordered and the eligible population is the same at the top. Never present an unordered set of events as a funnel.

## Retention / cohorts

Name the type (N-day exact, on-or-after / unbounded, rolling window). Acquisition vs behavior vs feature vs plan. Never mix an acquisition week with "users who did X this week" without saying so.

Cohort types and when to use each:

- **Signup cohorts** — best for onboarding/early retention.
- **Activation cohorts** — best when signup timing is far from first value.
- **First-purchase cohorts** — best for commerce repeat behavior.
- **Trial-start cohorts** — best for trial conversion.
- **Account-creation cohorts** — best for B2B account retention.
- **Release cohorts** — useful for changes associated with product versions.
- **Acquisition cohorts** — useful for quality by source.

When comparing cohort retention, ensure enough elapsed time exists. Never compare an incomplete D30 bucket with a completed D30 bucket. Recent cohorts have not had the same opportunity to return, so exclude incomplete periods or state the bias.

## Warehouse join

Volume is often **not** the product-analytics event. Check `../data-dictionary/references/source-map.md` for which connector is the source of truth (volume vs funnel vs telemetry). Do not average product-analytics and warehouse numbers into one figure.

## Diagnostic order for a metric drop

When asked "why did X drop?", follow this sequence (delegates the loop to `../root-cause-analysis/overview.md`, but this module owns the product-specific steps):

1. **Is it real?** — Check tracking, identity, ingestion, partial periods.
2. **Broad or concentrated?** — Break down by major segments.
3. **Composition or within-segment?** — The overall rate can fall because more users came from a low-performing segment (mix shift). Compare segment weights and within-segment rates.
4. **Which lifecycle component moved?** — For active users: new, retained, resurrected, churned. For revenue: new, expansion, contraction, churn.
5. **Which product step moved?** — Use funnels.
6. **What behavioral path changed?** — Use flows.
7. **What upstream quality metric changed?** — Errors, latency, crashes, task success.
8. **What external/product event coincides?** — Release, pricing change, campaign, notification change, seasonality, experiment.
9. **Can the hypothesis predict another observable?** — A good explanation should produce testable predictions.

## Common analytical traps

- Comparing a partial period with a complete one.
- Treating event totals as users.
- Redefining "active" between the numerator and the denominator.
- Reading a retention curve that has not flattened as if the product were healthy.
- Presenting "not retained this period" as "lost forever" — a user may return later.

## AI products add-on (Amigo / Indus)

This product is an AI assistant. Apply these metrics when the question is about AI product health:

- task-start -> successful completion
- answer acceptance
- regenerate / retry rate
- tool-call success
- latency
- fallback rate
- error rate
- task abandonment
- artifact creation
- user correction rate
- repeated successful use
- cost per successful task (when model-cost data is available)

Raw message count or token volume is **not** sufficient evidence of value. An AI product can show rising engagement while task success falls.

## Metric selection cheat sheet

| Question | Primary metric(s) |
|---|---|
| Are users getting value? | Activation rate, core-value event per active user |
| Is the product sticky? | Retention curve shape, DAU/MAU |
| Where do users drop? | Ordered funnel step conversion |
| Did a feature land? | Adoption rate, repeat use of the feature |
| Is the AI product working? | Task success, retry rate, tool-call success |

## Output routing

When the user asks for a deliverable (not just a chat answer), route to whichever output skill is bound for that format — a PDF report, a slide deck, a DOCX document, an HTML page, or a spreadsheet. For any chart inside a deliverable, use the visualization guidance first, then embed. Never ask the user about a missing format; bind what exists.

## STOP

- An app-open event presented as a warehouse session
- An unordered funnel
- A 2-day window presented as N-day retention
- Inventing an "active user" window not in the dictionary
- Presenting a mean on a skewed measure without a median
- Equating "more events" with "better product" without context
- Comparing an incomplete cohort bucket with a complete one
