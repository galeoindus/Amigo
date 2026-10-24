#!/usr/bin/env python3
"""Funnel step conversion from event rows.

Input rows: user_id, event, optional ts. --steps comma-separated ordered names.

A funnel is an ORDERED journey. When a `ts` is present the script counts a user
as reaching step N only if they performed step N at or after the time they
performed step N-1. When no timestamps are available it falls back to a
set-based (unordered) count and flags that the result is not order-verified.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from typing import Any


def _ordered_reached(events: list[tuple[float, str]], steps: list[str]) -> int:
    """Return 1 if the user completed all steps in order, else 0."""
    idx = 0
    last_ts = float("-inf")
    for ts, event in sorted(events):
        if event == steps[idx] and ts >= last_ts:
            last_ts = ts
            idx += 1
            if idx == len(steps):
                return 1
    return 0


def funnel(rows: list[dict[str, Any]], steps: list[str]) -> dict[str, Any]:
    has_ts = all("ts" in row and row["ts"] is not None for row in rows) and bool(rows)
    by_user: dict[str, list[tuple[float, str]]] = defaultdict(list)
    for i, row in enumerate(rows):
        ts = float(row["ts"]) if has_ts else float(i)
        by_user[str(row["user_id"])].append((ts, str(row["event"])))

    reached: list[dict[str, Any]] = []
    if has_ts:
        # Order-aware: a user reaches step k only if they completed the first k
        # steps in non-decreasing time order.
        remaining = set(by_user)
        for step in steps:
            remaining = {u for u in remaining if _ordered_reached(by_user[u], steps[: steps.index(step) + 1])}
            reached.append({"step": step, "users": len(remaining)})
    else:
        # Fallback: unordered set membership (flag it).
        seen = {u: {e for _, e in evs} for u, evs in by_user.items()}
        remaining = set(by_user)
        for step in steps:
            remaining = {u for u in remaining if step in seen[u]}
            reached.append({"step": step, "users": len(remaining)})

    out = []
    for i, item in enumerate(reached):
        prev = reached[i - 1]["users"] if i else len(by_user)
        cr = (item["users"] / prev) if prev else None
        out.append(
            {
                **item,
                "from_previous": prev,
                "step_conversion": None if cr is None else round(cr, 4),
                "drop_off": prev - item["users"],
            }
        )
    overall = (reached[-1]["users"] / len(by_user)) if reached and by_user else None
    return {
        "population": len(by_user),
        "order_verified": has_ts,
        "overall_conversion": None if overall is None else round(overall, 4),
        "steps": out,
        "note": (
            "Order verified against timestamps."
            if has_ts
            else "No timestamps found: counts are unordered set membership, not a true funnel."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--steps", required=True)
    args = parser.parse_args()
    payload = json.loads(open(args.input, encoding="utf-8").read())
    rows = payload if isinstance(payload, list) else payload["rows"]
    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    print(json.dumps(funnel(rows, steps), indent=2))


if __name__ == "__main__":
    main()
