#!/usr/bin/env python3
"""Two-proportion comparison for A/B experiment results.

Input JSON: { "control_success": int, "control_n": int,
               "treatment_success": int, "treatment_n": int }
Output: rates, absolute/relative lift, a Newcombe 95% interval on the
difference (default), an Agresti-Caffo interval, the Wald interval for
reference, and the two-proportion pooled z p-value.

Stdlib only (math). No scipy dependency.

Why not Wald alone? The Wald interval for a difference of proportions has
poor coverage at small n and for proportions near 0 or 1, and its limits can
leave [-1, 1]. Newcombe's hybrid (built from the two Wilson score intervals)
and Agresti-Caffo (add one success and one failure per arm) are near-nominal.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Any

Z_95 = 1.959963984540054


def _wilson(x: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Wilson score interval for a single proportion."""
    if n <= 0:
        return (0.0, 1.0)
    p = x / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (center - half, center + half)


def _wald_ci(p1: float, p2: float, n1: int, n2: int, z: float = Z_95) -> list[float]:
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p1 - p2
    return [round(diff - z * se, 6), round(diff + z * se, 6)]


def _newcombe(x1: int, n1: int, x2: int, n2: int, z: float = Z_95) -> list[float]:
    """Newcombe hybrid interval for p1 - p2 (always inside [-1, 1])."""
    l1, u1 = _wilson(x1, n1, z)
    l2, u2 = _wilson(x2, n2, z)
    p1, p2 = x1 / n1, x2 / n2
    diff = p1 - p2
    lower = diff - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = diff + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return [round(max(-1.0, lower), 6), round(min(1.0, upper), 6)]


def _agresti_caffo(x1: int, n1: int, x2: int, n2: int, z: float = Z_95) -> list[float]:
    """Agresti-Caffo interval: add one success and one failure to each arm."""
    n1a, n2a = n1 + 2, n2 + 2
    p1a, p2a = (x1 + 1) / n1a, (x2 + 1) / n2a
    se = math.sqrt(p1a * (1 - p1a) / n1a + p2a * (1 - p2a) / n2a)
    diff = x1 / n1 - x2 / n2
    return [round(diff - z * se, 6), round(diff + z * se, 6)]


def two_proportion_z(
    control_success: int,
    control_n: int,
    treatment_success: int,
    treatment_n: int,
) -> dict[str, Any]:
    if control_n <= 0 or treatment_n <= 0:
        return {"error": "sample sizes must be positive"}

    p_c = control_success / control_n
    p_t = treatment_success / treatment_n

    p_pooled = (control_success + treatment_success) / (control_n + treatment_n)
    se_pooled = math.sqrt(p_pooled * (1 - p_pooled) * (1 / control_n + 1 / treatment_n))

    if se_pooled == 0:
        z_stat = 0.0
        p_value = 1.0
    else:
        z_stat = (p_t - p_c) / se_pooled
        p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z_stat) / math.sqrt(2))))

    abs_lift = p_t - p_c
    rel_lift = (p_t - p_c) / p_c if p_c else None

    min_cell = min(
        control_success,
        control_n - control_success,
        treatment_success,
        treatment_n - treatment_success,
    )
    warnings: list[str] = []
    if min_cell < 5:
        warnings.append(
            "One or more cells has fewer than 5 expected counts; prefer Fisher's exact test."
        )
    if (control_n + treatment_n) < 20:
        warnings.append("Total sample below ~20; normal approximation is unreliable.")

    return {
        "control_rate": round(p_c, 6),
        "treatment_rate": round(p_t, 6),
        "absolute_lift": round(abs_lift, 6),
        "relative_lift": round(rel_lift, 6) if rel_lift is not None else None,
        "ci_95_newcombe": _newcombe(treatment_success, treatment_n, control_success, control_n),
        "ci_95_agresti_caffo": _agresti_caffo(
            treatment_success, treatment_n, control_success, control_n
        ),
        "ci_95_wald": _wald_ci(p_t, p_c, treatment_n, control_n),
        "z_stat": round(z_stat, 6),
        "p_value": round(p_value, 6),
        "control_n": control_n,
        "treatment_n": treatment_n,
        "control_success": control_success,
        "treatment_success": treatment_success,
        "significant_at_0.05": p_value < 0.05,
        "warnings": warnings,
        "note": "Report effect size + interval + n, not p alone.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Two-proportion comparison for A/B experiment results."
    )
    parser.add_argument("--input", required=True, help="Path to JSON input file")
    args = parser.parse_args()

    payload = json.loads(open(args.input, encoding="utf-8").read())
    result = two_proportion_z(
        control_success=int(payload["control_success"]),
        control_n=int(payload["control_n"]),
        treatment_success=int(payload["treatment_success"]),
        treatment_n=int(payload["treatment_n"]),
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
