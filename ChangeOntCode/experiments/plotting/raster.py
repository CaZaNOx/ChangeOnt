from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
import math

import matplotlib.pyplot as plt

_COLOR_CYCLE = ("#4c78a8", "#f58518", "#e45756", "#72b7b2", "#54a24b", "#b279a2", "#ff9da6", "#9d755d", "#bab0ac")


def _ensure_parent(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)


def _coerce_float(value: float | int | None) -> float | None:
    try:
        val = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if math.isfinite(val):
        return val
    return None


def _assign_colors(size: int) -> List[str]:
    return [_COLOR_CYCLE[i % len(_COLOR_CYCLE)] for i in range(size)]


def bar_chart_png(
    out_path: Path,
    labels: Sequence[str],
    values: Sequence[float],
    title: str,
    ylabel: str,
) -> None:
    cleaned: List[Tuple[str, float]] = []
    for label, value in zip(labels, values):
        val = _coerce_float(value)
        if val is None:
            continue
        cleaned.append((str(label), val))
    _ensure_parent(out_path)
    if not cleaned:
        out_path.write_text("", encoding="utf-8")
        return
    labs, vals = zip(*cleaned)
    width = max(6, len(labs) * 0.5)
    fig, ax = plt.subplots(figsize=(width, 4), dpi=160)
    fig.patch.set_facecolor("#0d1521")
    ax.set_facecolor("#111b2f")
    colors = _assign_colors(len(vals))
    bars = ax.bar(range(len(vals)), vals, color=colors, edgecolor="#0b1a33", linewidth=1.25)
    ax.set_xticks(range(len(labs)))
    ax.set_xticklabels(labs, rotation=45, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", color="#2f3a52", alpha=0.7)
    for rect in bars:
        h = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            h,
            f"{h:.2f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color="#ffffff",
        )
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def line_chart_png(
    out_path: Path,
    series: Dict[str, Sequence[float]],
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    data: List[Tuple[str, List[float]]] = []
    for label, values in sorted(series.items()):
        cleaned_values: List[float] = []
        for value in values:
            coerced = _coerce_float(value)
            if coerced is not None:
                cleaned_values.append(coerced)
        if not cleaned_values:
            continue
        data.append((label, cleaned_values))
    _ensure_parent(out_path)
    if not data:
        out_path.write_text("", encoding="utf-8")
        return
    max_len = max(len(v) for _, v in data)
    width = max(6, min(12, max_len * 0.25))
    fig, ax = plt.subplots(figsize=(width, 4), dpi=160)
    fig.patch.set_facecolor("#0d1521")
    ax.set_facecolor("#0f1725")
    colors = _assign_colors(len(data))
    for idx, (label, values) in enumerate(data):
        xs = list(range(len(values)))
        ax.plot(xs, values, label=label, linewidth=2.5, color=colors[idx])
        ax.scatter(xs, values, s=16, color=colors[idx])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle=":", color="#2f3a52", alpha=0.75)
    ax.legend(frameon=False, fontsize="small")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
