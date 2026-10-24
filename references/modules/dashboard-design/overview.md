# Module guide: Dashboard Design

> Integrated capability: KPI hierarchy, trustworthy dashboards, executive digests, and evidence-first data storytelling.

## Principle

Design the decision story before drawing charts. Every tile must answer a decision question or show a governed KPI; omit vanity charts. Start with anomalies, but do not mistake a spike for a cause.

## Default hierarchy

1. **Outcome:** product/business health and the user decision at stake.
2. **North-star and guardrails:** 3–6 governed metrics with definitions, units, grain, and source of truth.
3. **Funnel:** activation → retention → engagement → value/revenue, only where those stages are meaningful.
4. **Investigation cuts:** platform, geography, plan, acquisition, cohort, and segment—choose cuts that answer a hypothesis, not every dimension.

## Digest rules

- Use 4–6 governing metrics for a brief. Compare identical time windows and filters; show the prior period or an appropriate baseline.
- Lead with validated material changes and meaningful trend breaks. As a starting triage threshold, flag changes above 20%, but tune thresholds for variance, volume, seasonality, and business impact.
- Quiet metrics get one line; the main finding gets the space. State the action or decision implied.
- Every chart title should state the question or finding, not merely the chart type. Show units, time window, denominator, sample size where useful, and the data refresh time.

## Trust state

- **Validated:** metric definition, source, grain, filters, window, and reconciliation checked.
- **Provisional:** useful directionally but incomplete or inferred; label the limitation.
- **Blocked:** essential schema/permission/quality dependency is missing; do not publish as truth.

Never combine incompatible grains on one axis or silently join metrics from different sources of truth. Prefer small multiples over dual-axis charts. Do not treat “no data” as zero.

## Accessible visual design

Use color as a supplement, not the only signal; pair it with labels, shapes, or icons. Maintain readable contrast, keyboard-operable interactions, descriptive chart alternatives, and legible labels. See `../../research-notes.md` for the W3C accessibility reference.

## Output workflow

- **PowerPoint:** use [`../brand-for-pptx/overview.md`](../brand-for-pptx/overview.md).
- **Release/changelog report:** use [`../changelog-report/overview.md`](../changelog-report/overview.md).
- **Other formats:** use the file-generation tools available in the current environment; do not assume a separate PDF, DOCX, spreadsheet, or HTML skill is installed.
- Create charts with the available charting/visualization tools where possible instead of redrawing plots manually.

## Stop conditions

Do not publish 12 unrelated charts, an unexplained metric, mixed-grain comparisons, a dual-axis overview that obscures scale, or a dashboard made entirely of provisional tiles.
