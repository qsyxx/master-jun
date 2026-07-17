#!/usr/bin/env python3
"""Default six-palace Xiao Liuren calculator.

Inputs must already be verified lunar month/day and double-hour branch.
This script intentionally fixes one convention and prints it.
"""

import argparse

PALACES = ["大安", "留连", "速喜", "赤口", "小吉", "空亡"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def advance(start: int, count: int) -> int:
    if count < 1:
        raise ValueError("count must be >= 1")
    return (start + count - 1) % 6


def calculate(month: int, day: int, hour_branch: str):
    if not 1 <= month <= 12:
        raise ValueError("lunar month must be 1..12")
    if not 1 <= day <= 30:
        raise ValueError("lunar day must be 1..30")
    if hour_branch not in BRANCHES:
        raise ValueError("invalid hour branch")
    month_idx = advance(0, month)
    day_idx = advance(month_idx, day)
    hour_idx = advance(day_idx, BRANCHES.index(hour_branch) + 1)
    return PALACES[month_idx], PALACES[day_idx], PALACES[hour_idx]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", type=int, required=True, help="verified lunar month")
    parser.add_argument("--day", type=int, required=True, help="verified lunar day")
    parser.add_argument("--hour", required=True, choices=BRANCHES, help="double-hour branch")
    args = parser.parse_args()
    result = calculate(args.month, args.day, args.hour)
    print("convention=大安留连速喜赤口小吉空亡; starting palace counts as 1")
    print(f"month={result[0]} day={result[1]} hour={result[2]}")


if __name__ == "__main__":
    main()

