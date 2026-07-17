#!/usr/bin/env python3
"""Meihua Yishu lunar year-month-day-hour time casting, fixed convention."""

import argparse

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
TRIGRAMS = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 0: "坤"}


def calculate(year_branch: str, lunar_month: int, lunar_day: int, hour_branch: str):
    if year_branch not in BRANCHES or hour_branch not in BRANCHES:
        raise ValueError("invalid branch")
    if not 1 <= lunar_month <= 12 or not 1 <= lunar_day <= 30:
        raise ValueError("invalid lunar month/day")
    y = BRANCHES.index(year_branch) + 1
    h = BRANCHES.index(hour_branch) + 1
    upper_sum = y + lunar_month + lunar_day
    total = upper_sum + h
    upper = TRIGRAMS[upper_sum % 8]
    lower = TRIGRAMS[total % 8]
    moving = total % 6 or 6
    return y, h, upper_sum, total, upper, lower, moving


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year-branch", required=True, choices=BRANCHES)
    parser.add_argument("--month", type=int, required=True)
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--hour", required=True, choices=BRANCHES)
    args = parser.parse_args()
    y, h, upper_sum, total, upper, lower, moving = calculate(
        args.year_branch, args.month, args.day, args.hour
    )
    print("convention=year_branch+lunar_month+lunar_day; add hour for lower and moving line")
    print(f"year_number={y} hour_number={h} upper_sum={upper_sum} total={total}")
    print(f"upper={upper} lower={lower} moving_line={moving}")


if __name__ == "__main__":
    main()

