#!/usr/bin/env python3
"""Rank dimension slices by share of a metric delta.

Input JSON rows: {"dimension": str, "before": number, "after": number}
"""

from __future__ import annotations

import argparse
import json
from typing import Any


def contribution(rows: list[dict[str, Any]]) -> dict[str, Any]:
    parsed: list[dict[str, Any]] = []
    total_before = 0.0
    total_after = 0.0
    for row in rows:
        before = float(row["before"])
        after = float(row["after"])
        total_before += before
        total_after += after
        parsed.append(
            {
                "dimension": str(row["dimension"]),
                "before": before,
                "after": after,
                "delta": after - before,
            }
        )
    total_delta = total_after - total_before
    ranked = []
    for row in parsed:
        share = (row["delta"] / total_delta) if total_delta else None
        pct_change = (row["delta"] / row["before"]) if row["before"] else None
        ranked.append(
            {
                **row,
                "share_of_delta": None if share is None else round(share, 4),
                "pct_change": None if pct_change is None else round(pct_change, 4),
            }
        )
    ranked.sort(key=lambda r: abs(r["delta"]), reverse=True)
    pareto = 0.0
    k = 0
    if total_delta:
        for row in ranked:
            pareto += abs(row["delta"])
            k += 1
            if pareto / abs(total_delta) >= 0.7:
                break
    return {
        "total_before": total_before,
        "total_after": total_after,
        "total_delta": total_delta,
        "slices": ranked,
        "pareto_n": k,
        "note": (
            "Rank by share_of_delta, not pct_change of small bases. "
            "For ratios, decompose numerator, denominator and mix before naming a driver."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    payload = json.loads(open(args.input, encoding="utf-8").read())
    rows = payload if isinstance(payload, list) else payload["rows"]
    print(json.dumps(contribution(rows), indent=2))


if __name__ == "__main__":
    main()
