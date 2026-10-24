#!/usr/bin/env python3
"""Profile already-fetched JSON rows. No network/database access is performed."""
from __future__ import annotations
import argparse, json, math, statistics, re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_rows(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("rows") if isinstance(payload, dict) else None
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise SystemExit('input must be a JSON array of row objects or {"rows": [...]}')
    return rows


def is_missing(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def as_number(v: Any) -> float | None:
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        f = float(v)
    elif isinstance(v, str):
        try: f = float(v.strip().replace(",", ""))
        except ValueError: return None
    else: return None
    return f if math.isfinite(f) else None


def as_datetime(v: Any) -> datetime | None:
    if not isinstance(v, str) or len(v.strip()) < 8:
        return None
    value = v.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        # ISO-8601 is unambiguous. Do not guess day-first vs month-first formats.
        return datetime.fromisoformat(value)
    except ValueError:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            try: return datetime.strptime(value, "%Y-%m-%d")
            except ValueError: pass
    return None


def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values: raise ValueError("empty values")
    pos = (len(sorted_values) - 1) * p
    lo = int(math.floor(pos)); hi = int(math.ceil(pos))
    if lo == hi: return sorted_values[lo]
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (pos - lo)


def profile_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    names = list(dict.fromkeys(k for row in rows for k in row.keys()))
    out_cols = []
    for name in names:
        values = [row.get(name) for row in rows]  # absent keys are treated as missing
        missing = sum(is_missing(v) for v in values)
        present = [v for v in values if not is_missing(v)]
        numbers = [as_number(v) for v in present]
        valid_nums = sorted(x for x in numbers if x is not None)
        dates = [as_datetime(v) for v in present]
        valid_dates = [d for d in dates if d is not None]
        unique = len({json.dumps(v, sort_keys=True, ensure_ascii=False, default=str) for v in present})
        col: dict[str, Any] = {
            "name": name, "n": n, "present_n": len(present),
            "missing_n": missing, "null_pct": round(100 * missing / n, 2) if n else None,
            "nunique": unique,
        }
        numeric_threshold = max(1, math.ceil(0.8 * len(present)))
        datetime_threshold = max(1, math.ceil(0.8 * len(present)))
        identifierish = bool(re.search(r"(^|_)(id|key|code|zip|postal|phone|uuid)(_|$)", name.lower()))
        if valid_nums and len(valid_nums) >= numeric_threshold and not identifierish:
            xs = valid_nums; col["kind"] = "numeric"; col["numeric_n"] = len(xs)
            col["non_numeric_n"] = len(present) - len(xs)
            col.update({"min": xs[0], "q1": percentile(xs, .25), "p50": percentile(xs, .5),
                        "p90": percentile(xs, .9), "q3": percentile(xs, .75), "max": xs[-1],
                        "mean": round(statistics.fmean(xs), 6),
                        "stdev_sample": round(statistics.stdev(xs), 6) if len(xs) > 1 else None,
                        "iqr": percentile(xs, .75) - percentile(xs, .25)})
        elif valid_dates and len(valid_dates) >= datetime_threshold:
            aware = [d.utcoffset() is not None for d in valid_dates]
            col["kind"] = "datetime"; col["datetime_n"] = len(valid_dates)
            if all(aware) or not any(aware):
                col["min"] = min(valid_dates).isoformat()
                col["max"] = max(valid_dates).isoformat()
                col["timezone_awareness"] = "offset-aware" if all(aware) else "naive; timezone not inferred"
            else:
                col["timezone_awareness"] = "mixed-aware-and-naive; normalize before comparing min/max"
        else:
            col["kind"] = "categorical"
            counts = Counter(str(v) for v in present)
            col["top_values"] = [{"value": k, "n": count,
                                 "pct_of_present": round(100 * count / len(present), 2) if present else 0}
                                for k, count in counts.most_common(8)]
        out_cols.append(col)
    return {"row_count": n, "columns": out_cols,
            "notes": ["Already-fetched sample only; do not infer population totals from this output.",
                      "Missing fields are counted as missing. Numeric/date inference is heuristic and should be checked against domain meaning."]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="JSON array or {rows:[...]}")
    args = ap.parse_args()
    print(json.dumps(profile_rows(load_rows(args.input)), indent=2, ensure_ascii=False, allow_nan=False))

if __name__ == "__main__": main()
