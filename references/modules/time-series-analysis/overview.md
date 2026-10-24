# Module guide: Time Series Analysis

> Integrated capability: trends, seasonality, baselines, anomalies and change points. Use for WoW/MoM, "vs yesterday", spikes, "when did this start". Never default to adjacent-day comparison.


# Time series analysis

The comparison window **is** the analysis. A bad baseline manufactures a crisis.

## Amigo runtime

```text
python scripts/time-series-analysis/baseline.py --input /tmp/series.json --date-col date --value-col value
```

## Default baselines (pick one, say which)

| Question | Baseline |
|---|---|
| yesterday / today | same weekday last week **and** trailing 4-week weekday mean |
| this week | prior week, same timezone bounds |
| this month | prior month; YoY only if ≥13 months |
| on-call hours | same hour-of-week last week |

**Yesterday vs day-before is usually wrong** if weekends exist.

## Method

1. Series at the grain of the question.
2. Change point = first period outside the baseline band.
3. WoW/MoM on week-aligned windows.
4. Flag >20% vs chosen baseline or a 6-week trend break.
5. Rolling median (7d) to separate spike vs level shift.

One bad Tuesday is an outlier. Five consecutive Tuesdays below the 4-week Tuesday mean is a level shift.

## STOP

- CAGR on 3 weeks
- Smoothing away the spike the user asked about
- Comparing IST weeks to UTC weeks
