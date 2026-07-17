#!/usr/bin/env python3
"""Normalize Chinese event times and expose double-hour sensitivity."""

import argparse
import datetime as dt
import json
import math
import re
from zoneinfo import ZoneInfo

BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")


def branch_at(minutes):
    # 子时 begins at 23:00; each branch spans 120 minutes.
    return BRANCHES[((minutes - 23 * 60) % 1440) // 120]


def equation_of_time(day_of_year):
    b = math.radians(360 * (day_of_year - 81) / 364)
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)


def resolve(reference, expression=None, clock=None, tolerance=0, longitude=None):
    ref = dt.datetime.fromisoformat(reference)
    if ref.tzinfo is None:
        ref = ref.replace(tzinfo=ZoneInfo("Asia/Shanghai"))
    target_date = ref.date()
    source = "explicit/reference date"
    if expression:
        offsets = {"前天": -2, "昨天": -1, "今天": 0, "明天": 1, "后天": 2}
        matched = next((k for k in offsets if k in expression), None)
        if matched:
            target_date += dt.timedelta(days=offsets[matched])
            source = f"relative expression '{matched}' resolved from reference"
        else:
            m = re.search(r"(20\d{2})[-年/.](\d{1,2})[-月/.](\d{1,2})", expression)
            if m:
                target_date = dt.date(*map(int, m.groups()))
                source = "explicit date in expression"
    if not clock:
        return {"date": target_date.isoformat(), "time": None, "source": source, "precision": "date_only", "branch_candidates": BRANCHES}
    hour, minute = map(int, clock.split(":"))
    civil_minutes = hour * 60 + minute
    correction = 0.0
    if longitude is not None:
        correction = 4 * (longitude - 120.0) + equation_of_time(target_date.timetuple().tm_yday)
    center = (civil_minutes + correction) % 1440
    samples = [(center + delta) % 1440 for delta in (-tolerance, 0, tolerance)]
    candidates = list(dict.fromkeys(branch_at(int(x)) for x in samples))
    boundary_distance = min((center - (23 * 60 + 120 * i)) % 1440 for i in range(12))
    boundary_distance = min(boundary_distance, 120 - boundary_distance)
    return {
        "date": target_date.isoformat(), "time": clock, "timezone": str(ref.tzinfo), "source": source,
        "precision": f"±{tolerance}min" if tolerance else "minute supplied",
        "branch_candidates": candidates, "boundary_sensitive": len(candidates) > 1,
        "nearest_branch_boundary_minutes": round(boundary_distance, 1),
        "true_solar_correction_minutes": round(correction, 1) if longitude is not None else None,
        "warnings": (["经度修正含均时差近似值；正式排盘仍应由可靠历法复核"] if longitude is not None else []) +
                    (["误差跨越时辰边界，应并排两课，不可擅取其一"] if len(candidates) > 1 else []),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reference", required=True, help="ISO timestamp with timezone if known")
    p.add_argument("--expression", help="昨天/今天 or explicit Chinese date")
    p.add_argument("--time", dest="clock", help="HH:MM civil time")
    p.add_argument("--tolerance", type=int, default=0, help="estimated ± minutes")
    p.add_argument("--longitude", type=float, help="east longitude for approximate true-solar correction")
    a = p.parse_args()
    print(json.dumps(resolve(a.reference, a.expression, a.clock, a.tolerance, a.longitude), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
