# Module guide: Analytical Planning

> Integrated capability: Turn a vague business question into an investigation plan before any query. Use first on "why did X drop", "what happened", "investigate", RCA, or any open-ended KPI question. Do not skip for diagnostic work.

# Analytical planning

You are the planner. **Do not query yet.** Weak agents jump to `revenue by day`. You write the plan; other skills execute it.

Inspect first, then name the question, then query, then inspect the result, then follow up, then chart, then summarize.
This skill owns **question → plan** and which query is highest-information next.

## Panja runtime

- `skill_view` this skill. Load `references/investigation-tree.md` for the full tree template.
- Fetch via bound MCP tools. Do not invent Mixpanel/Metabase/SQL dialects here.
- Named metrics come from `data-dictionary`. If missing, stop.

## Output this block before the first query

```text
OBJECTIVE     <one sentence>
METRIC        <name + grain + dictionary definition>
BASELINE      <window vs what>
DECOMPOSITION <identity, or "rate = num/denom">
PLAN
  1. Magnitude + timing
  2. Verify definition + population + completeness
  3. Which identity component moved?
  4. Segment that component
  5. Hypotheses ranked likelihood × impact × testability
  6. Discriminating tests
  7. Confounders
  8. Validate (analysis-validation)
  9. One chart (visualization)
  10. Recommend next action
NEXT QUERY    <the single highest-information fetch>
```

## Highest-information first

1. Confirm the move (one number, two windows).
2. Split by identity components.
3. Split the moved component by 1–2 dimensions.
4. Only then: traces, releases, funnels, warehouse joins.

Never start with a 12-dimension group-by.

## STOP

- Querying before the OBJECTIVE block exists
- Yesterday vs day-before as the default baseline
- Asking the user for event/table names a connector can list
- Averaging two connectors to "split the difference"
