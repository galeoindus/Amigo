# Module guide: Analysis Validation

> Integrated capability: Critique the analysis before presenting. Population, baseline, denominators, seasonality, Simpson, tracking, competing explanations. Load before the final answer on any RCA or KPI claim.

# Analysis validation

Preview results, profile counts and nulls — schema alone is not enough. Evidence before cause. This skill is the last gate.

## Panja runtime

Run this **before** the user-facing answer. Load `references/checklist.md`.

## Four rounds

1. **Logic** — wrong metric, wrong test, identity not written
2. **Data handling** — eligible set, missingness, units, skip-filters
3. **Uncertainty** — every headline number has n / window / CI or "descriptive only"
4. **Cross-result** — complementary slice, adversarial query. If two connectors are bound (e.g., Mixpanel + Metabase), cross-check between them; if only one is bound, use a different breakdown or time window on the same source.

## Confidence

| Level | When |
|---|---|
| High | identity + change point + contribution ≥70% + adversarial query failed to kill it |
| Medium | contribution clear, mechanism unproven |
| Low | single chart, no complementary slice |

Never say "root cause" at Low.

## STOP

- Presenting a number not re-read against the dictionary
- Hiding a failed check
- Upgrading correlation to cause in the last paragraph
