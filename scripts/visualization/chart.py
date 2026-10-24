#!/usr/bin/env python3
"""Draw and audit one chart from retrieved rows.

Types: line, bar, hbar, funnel, hist.
"""

from __future__ import annotations

import argparse
import json
import math
import textwrap
from typing import Any

PALETTE = ["#3333CC", "#8B9FD4", "#C5E17A", "#E8C97A", "#F4B4B4"]
HIGHLIGHT = "#E6651B"
INK = "#141414"
MUTED = "#666666"
GRID = "#E5E5E5"


def _rows(path: str) -> list[dict[str, Any]]:
    payload = json.loads(open(path, encoding="utf-8").read())
    return payload if isinstance(payload, list) else payload["rows"]


def _number(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number if math.isfinite(number) else math.nan


def audit_rows(
    rows: list[dict[str, Any]], x: str, y: str, *, series: str = ""
) -> dict[str, int]:
    """Report omissions and duplicate x values before plotting."""
    if not rows:
        raise ValueError("no rows to plot")
    required = (x, y, series) if series else (x, y)
    if any(any(key not in row for key in required) for row in rows):
        raise ValueError(f"every row must contain {required!r}")
    missing = 0
    for row in rows:
        missing += math.isnan(_number(row[y]))
    keys = [(row[series], row[x]) if series else row[x] for row in rows]
    return {
        "row_count": len(rows),
        "plotted_count": len(rows) - missing,
        "missing_y_count": missing,
        "duplicate_x_count": len(keys) - len(set(keys)),
    }


def audit_png(path: str) -> dict[str, int]:
    """Reject blank or undersized output with Pillow."""
    from PIL import Image, ImageStat

    with Image.open(path) as image:
        width, height = image.size
        if width < 1200 or height < 720:
            raise ValueError(f"chart is too small: {width}x{height}")
        if not any(ImageStat.Stat(image.convert("RGB")).var):
            raise ValueError("chart is blank")
    return {"width": width, "height": height}


def render(
    rows: list[dict[str, Any]],
    *,
    chart_type: str,
    x: str,
    y: str,
    out: str,
    title: str,
    subtitle: str = "",
    source: str = "",
    series: str = "",
    x_label: str = "",
    y_label: str = "",
    y_suffix: str = "",
) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data_audit = audit_rows(rows, x, y, series=series)
    if data_audit["missing_y_count"] and chart_type != "line":
        raise ValueError("missing y values are only supported as gaps in line charts")
    if series and chart_type not in ("line", "bar"):
        raise ValueError("--series is supported for line and bar charts")

    fig, ax = plt.subplots(figsize=(12, 7.2), dpi=120)
    xs = [row[x] for row in rows]
    ys = [_number(row[y]) for row in rows]
    color = PALETTE[0]
    groups: dict[str, list[dict[str, Any]]] = {}
    if series:
        for row in rows:
            groups.setdefault(str(row[series]), []).append(row)
    else:
        groups[""] = rows
    if chart_type == "line":
        for index, (label, group) in enumerate(groups.items()):
            ax.plot(
                [row[x] for row in group],
                [_number(row[y]) for row in group],
                color=PALETTE[index % len(PALETTE)],
                linewidth=2.5,
                linestyle="-" if index == 0 else "--",
                marker="o" if len(group) <= 40 else None,
                markersize=4,
                label=label or None,
            )
    elif chart_type == "bar":
        categories = list(dict.fromkeys(xs))
        width = 0.78 / len(groups)
        colors = (
            [PALETTE[1], HIGHLIGHT]
            if len(groups) == 2
            else [PALETTE[index % len(PALETTE)] for index in range(len(groups))]
        )
        for index, (label, group) in enumerate(groups.items()):
            values = {row[x]: _number(row[y]) for row in group}
            positions = [
                pos - 0.39 + width / 2 + index * width
                for pos in range(len(categories))
            ]
            bar_values = [values[category] for category in categories]
            bars = ax.bar(
                positions,
                bar_values,
                width=width,
                color=colors[index],
                label=label or None,
            )
            ax.bar_label(
                bars,
                labels=[f"{value:,.1f}{y_suffix}" for value in bar_values],
                padding=3,
                color=INK,
                fontsize=9,
            )
        ax.set_xticks(range(len(categories)), categories)
    elif chart_type == "hbar":
        order = sorted(range(len(ys)), key=lambda i: ys[i])
        ax.barh([xs[i] for i in order], [ys[i] for i in order], color=color)
    elif chart_type == "funnel":
        order = list(range(len(ys)))
        ax.barh(
            [xs[i] for i in reversed(order)],
            [ys[i] for i in reversed(order)],
            color=color,
        )
    elif chart_type == "hist":
        ax.hist(ys, bins=min(20, max(5, len(ys) // 5)), color=color)
        ax.set_xlabel(y)
    else:
        raise SystemExit(f"unknown --type {chart_type}")
    if chart_type != "hist":
        ax.set_xlabel(x_label or x)
        ax.set_ylabel(y_label or y)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    if series:
        ax.legend(loc="upper right", frameon=False)
    title_text = textwrap.fill(title, width=76)
    subtitle_text = textwrap.fill(subtitle, width=116) if subtitle else ""
    source_text = textwrap.fill(f"Source: {source}", width=150) if source else ""
    title_lines = title_text.count("\n") + 1
    subtitle_lines = subtitle_text.count("\n") + 1 if subtitle_text else 0
    subtitle_y = 0.96 - title_lines * 0.055
    top = subtitle_y - subtitle_lines * 0.035 - 0.035
    source_lines = source_text.count("\n") + 1 if source_text else 0
    bottom = 0.09 + source_lines * 0.025
    fig.subplots_adjust(left=0.1, right=0.97, top=top, bottom=bottom)
    fig.text(
        0.1,
        0.97,
        title_text,
        color=INK,
        fontsize=18,
        fontweight="bold",
        ha="left",
        va="top",
    )
    if subtitle_text:
        fig.text(
            0.1,
            subtitle_y,
            subtitle_text,
            color=MUTED,
            fontsize=10,
            ha="left",
            va="top",
        )
    if source_text:
        fig.text(0.1, 0.02, source_text, color=MUTED, fontsize=8, ha="left")
    fig.savefig(out)
    plt.close(fig)
    return {"data": data_audit, "image": audit_png(out)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--x", required=True)
    parser.add_argument("--y", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--series", default="")
    parser.add_argument("--x-label", default="")
    parser.add_argument("--y-label", default="")
    parser.add_argument("--y-suffix", default="")
    args = parser.parse_args()
    try:
        audit = render(
            _rows(args.input),
            chart_type=args.type,
            x=args.x,
            y=args.y,
            out=args.out,
            title=args.title,
            subtitle=args.subtitle,
            source=args.source,
            series=args.series,
            x_label=args.x_label,
            y_label=args.y_label,
            y_suffix=args.y_suffix,
        )
    except ImportError:
        raise SystemExit("matplotlib is not installed in this sandbox") from None
    print(json.dumps({"ok": True, "out": args.out, "audit": audit}))


if __name__ == "__main__":
    main()
