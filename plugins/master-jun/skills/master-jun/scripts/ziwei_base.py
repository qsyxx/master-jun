#!/usr/bin/env python3
"""Compute the auditable Zi Wei Dou Shu base: life/body palaces and direction."""

import argparse
import json

BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
STEMS = list("甲乙丙丁戊己庚辛壬癸")
YANG_STEMS = set("甲丙戊庚壬")


def calculate(lunar_month, hour_branch, year_stem, sex):
    month_palace = BRANCHES[(BRANCHES.index("寅") + lunar_month - 1) % 12]
    hour_offset = BRANCHES.index(hour_branch)
    life = BRANCHES[(BRANCHES.index(month_palace) - hour_offset) % 12]
    body = BRANCHES[(BRANCHES.index(month_palace) + hour_offset) % 12]
    forward = (year_stem in YANG_STEMS and sex == "男") or (year_stem not in YANG_STEMS and sex == "女")
    return {"month_anchor": month_palace, "life_palace": life, "body_palace": body,
            "major_cycle_direction": "顺" if forward else "逆",
            "calculation": "寅起正月顺至生月；自生月宫起子时，逆数安命、顺数安身",
            "status": "BASE_ONLY", "boundary": "未安十四主星、四化与大限；不得据此冒充完整紫微命盘。"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lunar-month", type=int, required=True, choices=range(1, 13))
    p.add_argument("--hour-branch", required=True, choices=BRANCHES)
    p.add_argument("--year-stem", required=True, choices=STEMS)
    p.add_argument("--sex", required=True, choices=("男", "女"))
    a = p.parse_args()
    print(json.dumps(calculate(a.lunar_month, a.hour_branch, a.year_stem, a.sex), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
