#!/usr/bin/env python3
"""Create immutable forecast records and append later outcomes for calibration."""

import argparse
import datetime as dt
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("--file", required=True); new.add_argument("--case-id", required=True)
    new.add_argument("--question", required=True); new.add_argument("--method", required=True)
    new.add_argument("--basis", required=True); new.add_argument("--verdict", required=True)
    new.add_argument("--confidence", choices=("低", "中", "高"), default="中")
    new.add_argument("--falsifier", required=True); new.add_argument("--timing")
    outcome = sub.add_parser("outcome")
    outcome.add_argument("--file", required=True); outcome.add_argument("--status", required=True, choices=("hit", "partial", "miss", "pending"))
    outcome.add_argument("--observed", required=True); outcome.add_argument("--timing-error-days", type=float)
    a = p.parse_args()
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    if a.command == "new":
        if Path(a.file).exists(): raise SystemExit("refusing to overwrite an existing forecast record")
        data = {"schema": 1, "case_id": a.case_id, "created_at": now,
                "forecast": {"question": a.question, "method": a.method, "basis": a.basis, "verdict": a.verdict,
                             "confidence": a.confidence, "timing": a.timing, "falsifier": a.falsifier},
                "outcomes": []}
    else:
        data = load(a.file)
        data["outcomes"].append({"recorded_at": now, "status": a.status, "observed": a.observed, "timing_error_days": a.timing_error_days})
    save(a.file, data)


if __name__ == "__main__":
    main()
