"""Rank Metabase dashboards and pull cards from get_dashboard payloads.

Never call list_cards without a filter — a large instance returns thousands of
cards and none of them tell you which ones matter.

No instance values are hardcoded here. The "gold" dashboard (the one the business
treats as its source of truth), its id, and the database-id→meaning map come from
the clone's crawled `references/semantic-schema.md`. Pass the gold dashboard id
and name via GOLD_DASHBOARD_ID / GOLD_DASHBOARD_NAME when you have them; without
them ranking still works on name keywords alone.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

# Keyword sets per analysis job. Generic business vocabulary — extend from the
# crawl with the instance's own product nouns rather than editing this file.
JOB_NEEDLES = {
    "product": ("product", "activation", "session", "message", "adoption", "funnel"),
    "ops": ("ops", "latency", "error", "throughput", "uptime"),
    "exec": ("weekly", "kpi", "north star", "leadership", "exec"),
}


def _gold() -> dict:
    """The instance's source-of-truth dashboard, from the environment if known."""
    raw_id = os.environ.get("GOLD_DASHBOARD_ID")
    return {
        "dashboard_id": int(raw_id) if raw_id and raw_id.isdigit() else None,
        "name": os.environ.get("GOLD_DASHBOARD_NAME"),
        "note": (
            "Set GOLD_DASHBOARD_ID / GOLD_DASHBOARD_NAME from the crawl. The "
            "database-id -> meaning map and any rows to exclude (internal staff, "
            "test tenants) belong in references/semantic-schema.md, never here."
        ),
    }


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text() if path != "-" else sys.stdin.read())


def rank_dashboards(
    items: list[dict], job: str = "product", cap: int = 8
) -> list[dict]:
    gold = _gold()
    needles = JOB_NEEDLES.get(job, (job,))
    gold_name = (gold["name"] or "").lower()
    scored = []
    for d in items:
        name = (d.get("name") or d.get("title") or "").lower()
        score = 0
        if gold["dashboard_id"] is not None and d.get("id") == gold["dashboard_id"]:
            score += 50
        elif gold_name and gold_name in name:
            score += 50
        for n in needles:
            if n in name:
                score += 5
        if score:
            scored.append((score, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:cap]]


def cards_from_dashboard(payload: dict) -> list[dict]:
    """Cards out of a get_dashboard payload, across both response shapes."""
    cards = []
    dashcards = payload.get("dashcards") or payload.get("ordered_cards") or []
    for dc in dashcards:
        card = dc.get("card") or dc
        cid = card.get("id")
        if cid:
            cards.append(
                {
                    "id": cid,
                    "name": card.get("name"),
                    "database_id": (
                        card.get("database_id")
                        or (card.get("dataset_query") or {}).get("database")
                    ),
                    "display": card.get("display"),
                }
            )
    return cards


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(json.dumps(_gold(), indent=2))
        return 0
    cmd = argv[1]
    if cmd == "rank":
        data = _load(argv[2])
        items = (
            data
            if isinstance(data, list)
            else data.get("data") or data.get("dashboards") or []
        )
        job = argv[3] if len(argv) > 3 else "product"
        print(json.dumps(rank_dashboards(items, job), indent=2, default=str))
        return 0
    if cmd == "cards":
        print(json.dumps(cards_from_dashboard(_load(argv[2])), indent=2))
        return 0
    print("usage: metabase_harvest.py [rank dashboards.json job|cards dashboard.json]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
