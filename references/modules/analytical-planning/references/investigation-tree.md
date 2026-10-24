# Investigation tree

Use when the user question is diagnostic ("why") rather than a lookup ("what is DAU").

```text
Clarify analytical objective
      ↓
Identify dependent metric (data-dictionary — never invent)
      ↓
Decompose metric (metric-reasoning)
      ↓
Determine comparison / baseline (time-series-analysis)
      ↓
Generate investigation tree
      ↓
Execute highest-information queries first
      ↓
Revise the plan when a result falsifies a branch
      ↓
Validate (analysis-validation)
      ↓
Visualize + recommend
```

## Anti-patterns

| Temptation | Do this instead |
|---|---|
| Query revenue by day immediately | Confirm magnitude + window first |
| "What's in Mixpanel?" | Inventory bound sources, then profile one entity |
| Twelve filters in query 1 | One split that kills half the tree |
| Declare root cause after one chart | Complementary slice + adversarial query |
