# Module guide: Visualization

> Integrated capability: choose and construct the one chart that explains a result: chart grammar, integrity rules and the artifact-quality gate for PNG/PDF/presentation deliverables. Use when attaching a chart, "show me a chart", or funnel/retention visuals. Not dashboard layout (see `../dashboard-design/overview.md`).


# Visualization

Ask: **what chart explains this result?** One chart per finding.

Chart selection lives in `references/chart-grammar.md`. Do not hide missing data, do not truncate axes to manufacture a crisis, name uncertainty, and do not rely on color as the only cue. Charting is its own expertise, not buried in SQL.

For any PNG, PDF, or presentation deliverable, read `references/artifact-quality.md` first. It defines the data audit, Amigo color grammar, and render-before-delivery gates.

## Amigo runtime

```text
python scripts/visualization/chart.py --input /tmp/rows.json --type line --x date --y value --out /tmp/chart.png --title "..." --subtitle "window · unit" --source "card/event/query id"
```

Types: `line`, `bar`, `hbar`, `funnel`, `hist`. Matplotlib. If missing, markdown table — not a broken image.
For comparisons, add `--series period`; this produces grouped bars or
solid/dashed aligned lines. Use `--x-label`, `--y-label`, and `--y-suffix` for
human labels. Prefer this deterministic script over custom Matplotlib. If the
requested layout is more complex, simplify to one supported single-axis chart.

## Integrity

- Never alter/hide/invent points to improve the figure
- Missing ≠ zero; use gaps
- Bars include zero unless you disclose a break
- Dual axes: prefer two aligned panels
- Title states the **finding**, not the chart type
- Source footnote (card/event/dashboard id)

## STOP

- Pie with >5 slices · 3D · visualizing every query · rainbow palettes (use the script palette)
