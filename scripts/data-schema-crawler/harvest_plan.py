"""Minimal MCP call sequences. Run after tools/list. Print, then execute in order.

Goal: fewer round-trips, denser payloads. Do not N× list/get.
"""

from __future__ import annotations

import json
import sys

# Example call order and argument notes from a source pack; validate against the connected server's live tool schema before use. The
# project/workspace ids come from Get-Projects at run time — never hardcode them.
MIXPANEL = [
    {
        "tool": "Get-Projects",
        "arguments": {},
        "why": "project_id + workspace_id in one shot",
    },
    {
        "tool": "Get-Events",
        "arguments": {
            "project_id": "<from Get-Projects>",
            "include_details": True,
            "query": "<job keyword>",
        },
        "why": "one call returns every event matching the keyword — hundreds in a single payload. Never list events one-by-one.",
    },
    {
        "tool": "Search-Entities",
        "arguments": {
            "project_id": "<id>",
            "query": "<job keyword>",
            "entity_types": ["dashboard", "insights", "funnels", "retention"],
            "limit": 20,
        },
        "why": "boards + saved reports together. entity_types must be this enum, not 'report'.",
    },
    {
        "tool": "Get-Dashboard",
        "arguments": {
            "project_id": "<id>",
            "dashboard_id": "<top board>",
            "include_layout": True,
        },
        "why": "layout embeds every report id+name. Skip N Get-Report for discovery.",
    },
    {
        "tool": "List-Properties",
        "arguments": {
            "project_id": "<id>",
            "resource_type": "Event",
            "events": ["<top 8 event names>"],
        },
        "why": "resource_type is Event not event. Pass up to 8 names; one table of properties.",
    },
    {
        "tool": "Get-Report",
        "arguments": {
            "project_id": "<id>",
            "bookmark_id": "<one gold insight>",
            "skip_results": False,
        },
        "why": "sample one saved insight to verify data exists. Prefer this over a novel Run-Query during crawl.",
    },
]

METABASE = [
    {
        "tool": "list_databases",
        "arguments": {},
        "why": "ids + engines. Stop here if 401.",
    },
    {
        "tool": "list_dashboards",
        "arguments": {},
        "why": "rank by name; do NOT list_cards(all).",
    },
    {
        "tool": "get_dashboard",
        "arguments": {"dashboard_id": "<top 8>"},
        "why": "cards ride on the dashboard. 8 dashboards → 8 calls, not 200 cards.",
    },
    {
        "tool": "execute_card",
        "arguments": {"card_id": "<3 gold cards>", "max_rows": 50},
        "why": "sample only. Date filters from the card defaults.",
    },
]

SIGNOZ = [
    {
        "tool": "list dashboards / services",
        "arguments": {},
        "why": "pick 6 in-scope services.",
    },
    {
        "tool": "get dashboard widgets",
        "arguments": {"dashboard": "<symptom match>"},
        "why": "widget queries contain the real metric names. Guessing http.server.duration vs durationNano wastes 3-5 calls.",
    },
    {
        "tool": "query_range copied from widget",
        "arguments": {"filter": "serviceName = <svc>"},
        "why": "one query. Always pin service + time window.",
    },
]

SENTRY = [
    {
        "tool": "list projects / issues",
        "arguments": {"query": "is:unresolved", "limit": 20},
        "why": "dense issue list, then one issue detail.",
    },
]


def plan(connector: str) -> list[dict]:
    key = connector.strip().lower()
    if "mixpanel" in key:
        return MIXPANEL
    if "metabase" in key:
        return METABASE
    if "signoz" in key or "new relic" in key or "newrelic" in key:
        return SIGNOZ
    if "sentry" in key:
        return SENTRY
    return [
        {
            "error": f"unknown connector {connector}",
            "known": ["mixpanel", "metabase", "signoz", "sentry"],
        }
    ]


def main(argv: list[str]) -> int:
    name = argv[1] if len(argv) > 1 else "mixpanel"
    print(
        json.dumps(
            {"connector": name, "max_calls": len(plan(name)), "steps": plan(name)},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
