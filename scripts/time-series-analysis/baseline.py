#!/usr/bin/env python3
"""WoW + trailing weekday baseline + 20% anomaly flags.

Input rows: date column + value column (ISO dates).
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from typing import Any


def _parse_date(value: str) -> datetime:
    raw = value[:10]
    return datetime.strptime(raw, "%Y-%m-%d")


def analyze_series(
    rows: list[dict[str, Any]], date_col: str, value_col: str
) -> dict[str, Any]:
    points = []
    for row in rows:
        points.append((_parse_date(str(row[date_col])), float(row[value_col])))
    points.sort(key=lambda p: p[0])
    by_day = {d.date().isoformat(): v for d, v in points}

    wow = []
    anomalies = []
    weekday_history: dict[int, list[float]] = {i: [] for i in range(7)}
    for day, value in points:
        key = day.date().isoformat()
        prev_week = (day - timedelta(days=7)).date().isoformat()
        wow_delta = None
        if prev_week in by_day and by_day[prev_week] != 0:
            wow_delta = (value - by_day[prev_week]) / by_day[prev_week]
        hist = weekday_history[day.weekday()]
        baseline = sum(hist[-4:]) / len(hist[-4:]) if hist else None
        flag = None
        if baseline not in (None, 0) and abs((value - baseline) / baseline) > 0.2:
            flag = round((value - baseline) / baseline, 4)
            anomalies.append({"date": key, "value": value, "vs_weekday_mean": flag})
        wow.append(
            {
                "date": key,
                "value": value,
                "wow": None if wow_delta is None else round(wow_delta, 4),
                "weekday_mean_4": None if baseline is None else round(baseline, 4),
            }
        )
        hist.append(value)

    latest = wow[-1] if wow else None
    return {"points": wow, "latest": latest, "anomalies_gt_20pct": anomalies}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--date-col", default="date")
    parser.add_argument("--value-col", default="value")
    args = parser.parse_args()
    payload = json.loads(open(args.input, encoding="utf-8").read())
    rows = payload if isinstance(payload, list) else payload["rows"]
    print(json.dumps(analyze_series(rows, args.date_col, args.value_col), indent=2))


if __name__ == "__main__":
    main()
