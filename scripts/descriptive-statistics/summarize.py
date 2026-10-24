#!/usr/bin/env python3
"""Descriptive statistics for one column of already-fetched JSON rows; stdlib only."""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path
from typing import Any


def percentile(xs: list[float], p: float) -> float:
    pos = (len(xs) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    return xs[lo] if lo == hi else xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def summarize(values: list[float]) -> dict[str, Any]:
    xs = sorted(v for v in values if math.isfinite(v))
    n = len(xs)
    if not n: return {"n": 0, "note": "No finite numeric values to summarize."}
    mean = statistics.fmean(xs); median = statistics.median(xs)
    q1, q3 = percentile(xs, .25), percentile(xs, .75)
    iqr = q3 - q1
    mad = statistics.median([abs(x - median) for x in xs])
    bowley = ((q3 + q1 - 2 * median) / iqr) if iqr else None
    return {
        "n": n, "min": xs[0], "q1": q1, "p50": median, "q3": q3,
        "p90": percentile(xs, .90), "max": xs[-1], "mean": round(mean, 6),
        "stdev_sample": round(statistics.stdev(xs), 6) if n > 1 else None,
        "variance_sample": round(statistics.variance(xs), 6) if n > 1 else None,
        "iqr": iqr, "median_absolute_deviation": mad,
        "bowley_skewness_hint": round(bowley, 6) if bowley is not None else None,
        "potential_outlier_count_iqr_rule": sum(x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr for x in xs) if iqr else 0,
        "outlier_note": "IQR rule flags candidates only; it does not prove an error and no rows are removed."
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--column", required=True)
    args = ap.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("rows") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise SystemExit('input must be a JSON array of row objects or {"rows": [...]}')
    values=[]; missing=0; invalid=0
    for row in rows:
        value = row.get(args.column)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing += 1; continue
        if isinstance(value, bool): invalid += 1; continue
        try: number = float(value.replace(",", "") if isinstance(value, str) else value)
        except (ValueError, TypeError): invalid += 1; continue
        if math.isfinite(number): values.append(number)
        else: invalid += 1
    out = summarize(values)
    out["column"] = args.column
    out["row_count"] = len(rows)
    out["missing_count"] = missing
    out["null_pct"] = round(100 * missing / len(rows), 2) if rows else None
    out["invalid_or_non_numeric_count"] = invalid
    out["exclusion_note"] = "Missing/invalid values are counted but not imputed; verify whether they are missing at random before interpreting summaries."
    print(json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False))

if __name__ == "__main__": main()
