"""SigNoz query helpers — dashboard-first, service-pinned.

Read dashboard widgets before guessing metric names. Always pin service + window.

Nothing here is instance-specific: the workspace URL, the k8s selector, the
in-scope service list, and the symptom→dashboard map all come from the clone's
crawled `references/semantic-schema.md` (written by the build interview) and are
passed in as arguments. If a value is unknown, crawl for it — do not guess, and
do not hardcode it back into this file.
"""

from __future__ import annotations

import json
import os
import sys

# Symptom keywords → the KIND of dashboard to look for. The crawl maps each of
# these to the workspace's actual dashboard names and stores them in
# semantic-schema.md; this table only says what to go looking for.
SYMPTOM_DASHBOARD_KIND = {
    "error": "HTTP / RPC error-rate dashboard",
    "p99": "endpoint latency dashboard",
    "latency": "endpoint latency dashboard",
    "cpu": "container/pod resource dashboard",
    "memory": "container/pod resource dashboard",
    "llm": "LLM or model-usage dashboard",
    "web": "frontend RUM dashboard",
    "auth": "authentication dashboard",
}

# Span/trace attributes worth trying as join keys back to product analytics.
# Generic names only — add the instance's own from the crawl.
CANDIDATE_JOIN_KEYS = ("session_id", "trace_id", "traceID", "user_id", "request_id")


def service_filter(service: str) -> dict:
    """Resource filter in the v3 `filters.items[]` shape."""
    return {
        "key": {
            "key": "serviceName",
            "dataType": "string",
            "type": "resource",
            "isColumn": True,
        },
        "op": "=",
        "value": service,
    }


def traces_p99(service: str) -> dict:
    """Trace p99 in the older v3 `filters.items[]` shape.

    Most existing dashboard widgets use this shape. Copy the widget's query
    rather than rewriting it.
    """
    return {
        "dataSource": "traces",
        "aggregateOperator": "p99",
        "aggregateAttribute": {
            "key": "durationNano",
            "dataType": "float64",
            "type": "tag",
            "isColumn": True,
        },
        "filters": {"op": "AND", "items": [service_filter(service)]},
    }


def k8s_cpu(container: str, k8s_selector: str | None = None) -> dict:
    """Container CPU in the newer string-expression shape.

    `k8s_selector` is an extra label predicate for the deployment's own grouping
    label (e.g. `app.kubernetes.io/part-of = '<value from the crawl>'`); omit it
    if the crawl did not find one.

    Do NOT mix this shape with `traces_p99`'s `filters.items[]` shape in one
    query — SigNoz rejects the mixed payload.
    """
    expression = (
        f"k8s.container.name = '{container}' AND k8s.deployment.name = '{container}'"
    )
    if k8s_selector:
        expression += f" AND {k8s_selector}"
    return {
        "dataSource": "metrics",
        "aggregations": [
            {
                "metricName": "container.cpu.utilization",
                "reduceTo": "avg",
                "spaceAggregation": "avg",
                "timeAggregation": "avg",
                "temporality": "",
            }
        ],
        "filter": {"expression": expression},
        "groupBy": [{"key": "k8s.pod.name", "dataType": "string", "type": "tag"}],
    }


def pick_dashboard_kind(question: str) -> str:
    q = question.lower()
    for needle, kind in SYMPTOM_DASHBOARD_KIND.items():
        if needle in q:
            return kind
    return "HTTP / RPC error-rate dashboard"


def main(argv: list[str]) -> int:
    """Usage: signoz_harvest.py <question...>

    Reads the instance's own values from the environment when present, so this
    script never carries them:
      SIGNOZ_SERVICE     the service to pin (required for a real query)
      SIGNOZ_K8S_SELECTOR  extra k8s label predicate, if the crawl found one
    """
    question = " ".join(argv[1:]) or "error rate last 6 hours"
    service = os.environ.get("SIGNOZ_SERVICE") or "<service — from semantic-schema.md>"
    selector = os.environ.get("SIGNOZ_K8S_SELECTOR")
    print(
        json.dumps(
            {
                "dashboard_kind": pick_dashboard_kind(question),
                "service": service,
                "candidate_join_keys": list(CANDIDATE_JOIN_KEYS),
                "traces_p99": traces_p99(service),
                "k8s_cpu": k8s_cpu(service, selector),
                "rules": [
                    "Read the dashboard widget's query and copy it; do not translate "
                    "v3 filters.items[] into the expression shape.",
                    "Pin service and time window on every query.",
                    "In-scope services, noise services, and the real dashboard names "
                    "live in references/semantic-schema.md — crawl, do not assume.",
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
