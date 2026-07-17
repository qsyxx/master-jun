#!/usr/bin/env python3
"""Summarize frozen divination case outcomes without rewriting misses."""

import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", help="case JSON file or directory")
    a = p.parse_args()
    root = Path(a.path)
    files = [root] if root.is_file() else sorted(root.glob("*.json"))
    counts = {"hit": 0, "partial": 0, "miss": 0, "pending": 0, "unscored": 0}
    timing = []
    by_method = {}
    for file in files:
        data = json.loads(file.read_text(encoding="utf-8")); outcomes = data.get("outcomes", [])
        latest = outcomes[-1] if outcomes else None
        status = latest.get("status") if latest else "unscored"; counts[status] += 1
        method = data.get("forecast", {}).get("method", "unknown")
        by_method.setdefault(method, {k: 0 for k in counts}); by_method[method][status] += 1
        if latest and latest.get("timing_error_days") is not None: timing.append(abs(latest["timing_error_days"]))
    scored = counts["hit"] + counts["partial"] + counts["miss"]
    result = {"cases": len(files), "scored": scored, "counts": counts, "by_method": by_method,
              "hit_rate_excluding_partial": round(counts["hit"] / scored, 3) if scored else None,
              "mean_absolute_timing_error_days": round(sum(timing) / len(timing), 2) if timing else None,
              "note": "样本量与选择偏差必须同时报告；此统计不证明术数具有科学预测效力。"}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
