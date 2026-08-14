#!/usr/bin/env python3
"""Render the image-size history CSV as an SVG chart.

Reads ``image_size_history.csv`` (columns: ``timestamp, commit, branch,
size_bytes``) and writes ``image_size_trend.svg``. Three panels stacked:

- top: ``develop`` only, chronological, points joined,
- middle: ``main`` only, chronological, points joined,
- bottom: combined ``develop + main``, single chronological joined line
  with markers coloured by branch.

The per-branch panels prevent visual collision when ``develop`` and
``main`` sizes are identical (markers stacking on top of each other);
the combined panel preserves the release-vs-integration comparison.

All three panels draw the SR-060 ceiling (200 MiB) as a red dashed
reference line so drift toward the gate is visible at a glance.

Usage::

    python scripts/plot_image_size.py --csv image_size_history.csv --out image_size_trend.svg

Both arguments are optional; defaults resolve relative to the current
working directory.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

MIB = 1024 * 1024
SR060_MIB = 200
BRANCH_STYLE = {
    "develop": {"color": "#1f77b4", "marker": "o", "label": "develop"},
    "main": {"color": "#ff7f0e", "marker": "s", "label": "main"},
}
OTHER_STYLE = {"color": "#7f7f7f", "marker": "x", "label": "other"}
COMBINED_LINE_COLOR = "#555555"


def load(csv_path: Path) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open("r", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["size_mib"] = float(r["size_bytes"]) / MIB
            r["ts"] = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
            rows.append(r)
    rows.sort(key=lambda x: x["ts"])
    for idx, r in enumerate(rows, start=1):
        r["idx"] = idx
    return rows


def _draw_ceiling(ax) -> None:
    ax.axhline(
        SR060_MIB,
        color="#d62728",
        linestyle="--",
        linewidth=1.0,
        label=f"SR-060 ceiling ({SR060_MIB} MiB)",
    )


def _plot_single_branch(ax, rows: list[dict], branch: str) -> None:
    style = BRANCH_STYLE.get(branch, OTHER_STYLE)
    series = [r for r in rows if r["branch"] == branch]
    series.sort(key=lambda r: r["ts"])
    if series:
        ax.plot(
            [r["ts"] for r in series],
            [r["size_mib"] for r in series],
            marker=style["marker"],
            color=style["color"],
            linestyle="-",
            markersize=6,
            label=f"{style['label']} ({len(series)} pts)",
        )
    else:
        ax.text(
            0.5,
            0.5,
            f"No {branch} data yet",
            transform=ax.transAxes,
            ha="center",
            va="center",
            color="#888",
            fontsize=10,
        )
    _draw_ceiling(ax)
    ax.set_ylabel("Runtime image size (MiB)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)


def _plot_combined(ax, rows: list[dict]) -> None:
    if rows:
        ax.plot(
            [r["ts"] for r in rows],
            [r["size_mib"] for r in rows],
            color=COMBINED_LINE_COLOR,
            linestyle="-",
            linewidth=1.0,
            label="chronological",
        )
        seen: set[str] = set()
        for branch, style in list(BRANCH_STYLE.items()) + [("__other__", OTHER_STYLE)]:
            if branch == "__other__":
                group = [r for r in rows if r["branch"] not in BRANCH_STYLE]
            else:
                group = [r for r in rows if r["branch"] == branch]
            if not group:
                continue
            label = style["label"]
            if label in seen:
                label = None
            else:
                seen.add(label)
            ax.scatter(
                [r["ts"] for r in group],
                [r["size_mib"] for r in group],
                marker=style["marker"],
                color=style["color"],
                s=36,
                zorder=3,
                label=label,
            )
    _draw_ceiling(ax)
    ax.set_ylabel("Runtime image size (MiB)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)


def render(rows: list[dict], out_path: Path) -> None:
    fig, (ax_dev, ax_main, ax_all) = plt.subplots(3, 1, figsize=(10, 10), sharey=True)

    _plot_single_branch(ax_dev, rows, branch="develop")
    ax_dev.set_title("CppCheckDocker runtime image size - develop")
    ax_dev.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    _plot_single_branch(ax_main, rows, branch="main")
    ax_main.set_title("CppCheckDocker runtime image size - main")
    ax_main.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    _plot_combined(ax_all, rows)
    ax_all.set_title("CppCheckDocker runtime image size - develop + main (chronological)")
    ax_all.set_xlabel("Merge date (UTC)")
    ax_all.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    fig.autofmt_xdate(rotation=30)

    max_mib = max((r["size_mib"] for r in rows), default=0)
    ax_dev.set_ylim(0, max(SR060_MIB * 1.1, max_mib * 1.1))

    fig.tight_layout()
    fig.savefig(out_path, format="svg")
    plt.close(fig)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", default="image_size_history.csv", type=Path)
    ap.add_argument("--out", default="image_size_trend.svg", type=Path)
    args = ap.parse_args(argv)

    if not args.csv.exists():
        print(f"plot-image-size: CSV not found: {args.csv}", file=sys.stderr)
        return 1
    rows = load(args.csv)
    if not rows:
        print("plot-image-size: CSV has no rows; nothing to plot.", file=sys.stderr)
        return 1
    render(rows, args.out)
    print(f"plot-image-size: wrote {args.out} ({len(rows)} points)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
