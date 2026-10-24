"""Distill Mixpanel MCP dumps into schema rows. Stdlib only.

Pipe the JSON body of Get-Events / Search-Entities / Get-Dashboard (the
second text part, after the security notice) into this script.

No instance values are hardcoded here. The company, product scope, timezone, event
prefix, and the project id are arguments; the "core events" for an instance come
from the crawl, not from this file. Landmines discovered during the crawl belong
in the generated `semantic-schema.md`, never hardcoded here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Generic job vocabulary. These are analysis intents, not one product's events —
# extend per instance from the crawl instead of editing this file.
JOB_KEYWORDS = {
    "activation": (
        "launched",
        "auth",
        "signup",
        "created",
        "first_",
        "onboard",
    ),
    "retention": ("retention", "dau", "wau", "mau", "returning"),
    "engagement": ("sent", "received", "opened", "viewed", "session"),
    "quality": ("failed", "error", "feedback", "failure", "crash"),
    "growth": ("invite", "share", "referral", "upgrade", "template"),
}


def _load(path_or_dash: str) -> Any:
    """Unwrap an MCP tool response down to its JSON body.

    MCP responses wrap the payload in `content[]` text parts (the first is a
    security notice), or expose it as `structured_content`. Handle both.
    """
    raw = sys.stdin.read() if path_or_dash == "-" else Path(path_or_dash).read_text()
    data = json.loads(raw)
    if isinstance(data, dict) and "content" in data:
        for part in data["content"]:
            text = ((part or {}).get("text") or "").strip()
            if text.startswith("{") or text.startswith("["):
                return json.loads(text)
    if isinstance(data, dict) and data.get("structured_content"):
        return data["structured_content"]
    return data


def events_from_get_events(payload: Any) -> list[str]:
    if isinstance(payload, dict) and "events" in payload:
        return [e["name"] for e in payload["events"] if e.get("name")]
    return []


def rank_events(
    names: list[str],
    job: str,
    cap: int = 12,
    prefix: str | None = None,
    core: tuple[str, ...] = (),
) -> list[str]:
    """Rank raw event names for one analysis job.

    `prefix` is the instance's own event namespace (found during the crawl) and
    `core` is the instance's known-important events — both optional, both passed
    in rather than baked in.
    """
    keys = JOB_KEYWORDS.get(job, (job,))
    scored: list[tuple[int, str]] = []
    for name in names:
        lower = name.lower()
        score = 0
        if name in core:
            score += 10
        for k in keys:
            if k in lower:
                score += 3
        if prefix and name.startswith(prefix):
            score += 1
        if score:
            scored.append((score, name))
    scored.sort(reverse=True)
    ranked = [n for _, n in scored]
    for c in core:
        if c not in ranked:
            ranked.append(c)
    out: list[str] = []
    for n in ranked:
        if n not in out:
            out.append(n)
        if len(out) >= cap:
            break
    return out


def reports_from_dashboard(payload: Any) -> list[dict]:
    """Saved reports out of a Get-Dashboard payload.

    Layout cells come through as `[id, "report", {id, name}]`; fall back to a
    plain recursive scan for `{id, name}` objects when that shape is absent.
    """
    reports: list[dict] = []
    layout = payload.get("layout") if isinstance(payload, dict) else None
    if not layout:
        return reports

    def walk(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict) and node.get("id") and node.get("name"):
            reports.append({"id": node["id"], "name": node["name"]})

    walk(layout)

    extra: list[dict] = []

    def walk_cells(node: Any) -> None:
        if (
            isinstance(node, list)
            and len(node) >= 3
            and node[1] == "report"
            and isinstance(node[2], dict)
        ):
            extra.append({"id": node[2].get("id"), "name": node[2].get("name")})
        elif isinstance(node, list):
            for item in node:
                walk_cells(item)

    walk_cells(layout)

    seen: set[Any] = set()
    out: list[dict] = []
    for r in extra or reports:
        rid = r.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            out.append(r)
    return out


def schema_markdown(
    *,
    company: str,
    product: str,
    timezone: str,
    audience: str,
    events: list[str],
    reports: list[dict],
    project_id: str,
) -> str:
    """A first-draft semantic schema. Every fact is either passed in or a
    placeholder the crawl must fill — the landmines section is prompts, not
    answers, because landmines are per-instance."""
    lines = [
        "# Semantic schema",
        "",
        f"Company: `{company}`",
        f"Product / scope: `{product}`",
        f"Timezone: `{timezone}`",
        f"Audience: `{audience}`",
        f"Last crawled: Mixpanel project `{project_id}`",
        "",
        "## Entities",
        "",
        "| Entity | Grain | Primary key | Source |",
        "|---|---|---|---|",
        "| user | person | `$user_id` / Mixpanel distinct_id | Mixpanel |",
        "| session | one visit / conversation | `<session key — from the crawl>` | Mixpanel client event |",
        "| account | tenant / workspace | `<org or account id>` | Mixpanel |",
        "",
        "## Metrics (prefer saved reports over hand-built queries)",
        "",
        "| Name | Formula / definition | Grain | Source | Status |",
        "|---|---|---|---|---|",
    ]
    for r in reports[:12]:
        lines.append(
            f"| {r['name']} | saved Mixpanel report `{r['id']}` | see report "
            f"| mixpanel insight `{r['id']}` | inferred |"
        )
    lines += [
        "",
        "## Events kept (capped)",
        "",
        "| Event | Why |",
        "|---|---|",
    ]
    for e in events:
        lines.append(f"| `{e}` | ranked for this job |")
    lines += [
        "",
        "## Forbidden / landmines *(fill from the crawl — these are the questions)*",
        "",
        "- Which client-side event is **not** the same as the warehouse's session row?",
        "  Name both and say which is source of truth.",
        "- Where does the client SDK undercount versus the database? Volume is usually",
        "  a warehouse question, not an analytics-tool question.",
        "- Which channels have no SDK at all (API, chat integrations, server jobs)?",
        "  Those cannot be compared against instrumented ones.",
        "- How are internal / staff / test accounts excluded, and does that filter",
        "  exist in both the analytics tool and the warehouse?",
        "",
        "## When in doubt, skip",
        "",
        "- Hidden or deprecated events.",
        "- Untitled or default-named boards.",
        "- Events outside the product's own namespace unless the job names them.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("events", help="rank events from a Get-Events dump")
    pe.add_argument("file")
    pe.add_argument("job", nargs="?", default="activation")
    pe.add_argument("--prefix", default=None, help="instance event namespace")
    pe.add_argument("--core", default="", help="comma-separated known-core events")

    pd = sub.add_parser("dashboard", help="list saved reports from a Get-Dashboard dump")
    pd.add_argument("file")

    ps = sub.add_parser("schema", help="draft semantic-schema.md")
    ps.add_argument("events_file")
    ps.add_argument("dashboard_file")
    ps.add_argument("--company", required=True)
    ps.add_argument("--product", required=True)
    ps.add_argument("--project-id", required=True)
    ps.add_argument("--timezone", default="UTC")
    ps.add_argument("--audience", default="PM / product")
    ps.add_argument("--job", default="activation")
    ps.add_argument("--prefix", default=None)
    ps.add_argument("--core", default="")

    a = p.parse_args(argv[1:])
    core = tuple(x.strip() for x in a.core.split(",") if x.strip()) if a.core else ()

    if a.cmd == "events":
        names = events_from_get_events(_load(a.file))
        ranked = rank_events(names, a.job, prefix=a.prefix, core=core)
        print(json.dumps({"n": len(names), "kept": ranked}, indent=2))
        return 0
    if a.cmd == "dashboard":
        print(json.dumps(reports_from_dashboard(_load(a.file)), indent=2))
        return 0
    if a.cmd == "schema":
        names = events_from_get_events(_load(a.events_file))
        print(
            schema_markdown(
                company=a.company,
                product=a.product,
                timezone=a.timezone,
                audience=a.audience,
                events=rank_events(names, a.job, prefix=a.prefix, core=core),
                reports=reports_from_dashboard(_load(a.dashboard_file)),
                project_id=a.project_id,
            )
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
