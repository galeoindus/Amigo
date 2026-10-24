# Module guide: Statistical Inference

> Integrated capability: significance, confidence intervals, effect sizes, experiment validity. Load only when comparing rates/groups or analyzing an A/B test — not on every KPI question. Math runs in the scripts.

# Statistical inference

Use the test-selection table, then review before concluding. Do not run fancy statistics on every question. Math runs in this module's `proportion_test.py`.

## Amigo runtime

```text
python scripts/statistical-inference/proportion_test.py --input /tmp/ab.json
```

Input: `{ "control_success", "control_n", "treatment_success", "treatment_n" }`.
Output: rates, absolute/relative lift, a **Newcombe** 95% interval on the difference (default), an Agresti–Caffo interval, the Wald interval for reference, and the two-proportion z p-value. Interpret in this module; do not hand-compute intervals.

## When to load

- Explicit A/B / experiment
- "is this significant"
- Comparing two conversion rates with known n

Otherwise descriptive + segmentation is enough.

## Test selection

| Data | Test |
|---|---|
| Two independent proportions (A/B primary) | two-proportion z / `proportion_test.py` |
| Two proportions, small counts (<5 per cell) | Fisher's exact (say you need scipy; else report exact caveat) |
| Paired / matched binary data (same users both arms) | McNemar (not a two-sample z) |
| Two groups, skewed numeric | Mann–Whitney (needs scipy) or bootstrap |
| Categorical association (r x c) | chi-square; note the 2x2 case equals the z-test squared |

## Intervals for a difference of proportions

The plain **Wald** interval (estimate +/- 1.96 x SE) has poor coverage — it is too narrow at small n and for proportions near 0 or 1, and its limits can fall outside [-1, 1]. Prefer:

- **Newcombe's hybrid** (default here): combine the two Wilson score intervals per arm. Always inside [-1, 1]; near-nominal coverage.
- **Agresti–Caffo**: add one success and one failure to each arm, then use the Wald formula. Simple and much safer than plain Wald.

State which interval you used. If one or more cells is below ~5, prefer an exact test and say so.

## Experiments

Control, treatment, primary metric, guardrails, sample-ratio mismatch, novelty effect. Do not call a 2-day spike an experiment. Confirm the randomization unit matches the analysis unit.

## Review before conclusion (4 rounds, adapted)

1. Wrong test / trivial test / math error
2. Data handling (missing, units, eligible set, sample-ratio mismatch)
3. Uncertainty present on every headline number (effect size + interval + n)
4. Consistency with other results this turn

## STOP

- p-hacking extra slices after seeing p
- Multiple testing without saying so
- Reporting p alone without effect size, interval and n
- A causal claim from an underpowered test
- Using a paired test on unpaired data (or vice versa)
