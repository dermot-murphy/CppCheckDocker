#!/usr/bin/env python3
"""Render the image-size history CSV as an SVG chart.

Reads ``image_size_history.csv`` (columns: ``timestamp, commit, branch,
size_bytes``) and writes ``image_size_trend.svg``. Two panels stacked:

- top: size in MiB versus commit date (chronological drift view),
- bottom: size in MiB versus commit index (per-merge view).

Both panels draw the SR-060 ceiling (200 MiB) as a red dashed reference
line so drift toward the gate is visible at a glance. Points are coloured
by branch (``develop`` vs ``main``) so integration and release lines can
be compared.

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


def _plot_series(ax, rows, xkey: str) -> None:
    seen = set()
    for r in rows:
        style = BRANCH_STYLE.get(r["branch"], OTHER_STYLE)
        label = None
        if style["label"] not in seen:
            label = style["label"]
            seen.add(style["label"])
        ax.plot(
            r[xkey],
            r["size_mib"],
            marker=style["marker"],
            color=style["color"],
            linestyle="",
            markersize=6,
            label=label,
        )
    ax.axhline(
        SR060_MIB,
        color="#d62728",
        linestyle="--",
        linewidth=1.0,
        label=f"SR-060 ceiling ({SR060_MIB} MiB)",
    )
    ax.set_ylabel("Runtime image size (MiB)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)


def render(rows: list[dict], out_path: Path) -> None:
    fig, (ax_time, ax_idx) = plt.subplots(2, 1, figsize=(10, 7), sharey=True)

    _plot_series(ax_time, rows, xkey="ts")
    ax_time.set_title("CppCheckDocker runtime image size over time")
    ax_time.set_xlabel("Merge date (UTC)")
    ax_time.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate(rotation=30)

    _plot_series(ax_idx, rows, xkey="idx")
    ax_idx.set_title("Same data by merge index")
    ax_idx.set_xlabel("Merge index (chronological)")

    max_mib = max((r["size_mib"] for r in rows), default=0)
    ax_time.set_ylim(0, max(SR060_MIB * 1.1, max_mib * 1.1))

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
