# Module guide: Root Cause Analysis

> Integrated capability: hypothesis generation, ranking, discriminating tests, elimination. Load for "why did X happen". Orchestrates the other analyst modules; it does not query connectors itself.

# Root cause analysis

You orchestrate. Other modules compute. MCP tools fetch.

Classify the signal, gather evidence, then name a cause with confidence. Use on any metric movement (product, warehouse, telemetry).

## Amigo runtime

- Load `../analytical-planning/overview.md` if the plan block is missing.
- Use `../segmentation-drilldown/overview.md` to find which slice owns the move.
- When the surviving hypothesis is "prod broke" (release, error, latency), query observability MCP tools directly if bound. If no observability tool is bound, state that the hypothesis cannot be confirmed from available tools and record it in `../data-dictionary/references/open-questions.md`.
- Load `references/evidence-language.md` before the user-facing answer.

## Loop

```text
Observed change -> quantify -> change point -> decompose identity
  -> candidate dimensions -> hypotheses
  -> rank likelihood x impact x testability
  -> run the test that would KILL the top hypothesis
  -> reject/support -> competing explanation
  -> validate -> confidence + next action
```

## Change point

A movement has a **when**. Align it to a candidate cause before blaming it: a release, a config change, a pricing change, a campaign, a tracking change, or a seasonality boundary. If the change point does not line up with the candidate, that candidate is not the cause yet. Segment the window on both sides of the change point, not "yesterday vs the day before".

## Testable hypotheses

Bad: "maybe tracking broke."
Good: "`message.sent` dropped in the product-analytics source while the warehouse `messages` table did not -> client tracking, not real traffic."

Each hypothesis names: predicted evidence, killing query, and a complementary slice that must agree if it is true.

## Competing explanations (always try)

Seasonality / bad baseline · mix shift · tracking change · whale/tenant concentration · denominator collapse · release / error / latency if observability tools exist.

## STOP

- Treating the first confirming chart as the "root cause"
- Blaming a deploy without change-point alignment to a release
- Causal language at low confidence (see `../analysis-validation/overview.md`)
- Naming a cause before running one test that could have killed it
