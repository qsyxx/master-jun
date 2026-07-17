#!/usr/bin/env python3
"""Audit a verified four-pillar chart: hidden stems, ten gods, roots, relations."""

import argparse
import json

STEMS = list("甲乙丙丁戊己庚辛壬癸")
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
ELEMENT = dict(zip(STEMS, ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]))
YANG = set("甲丙戊庚壬")
HIDDEN = {"子": "癸", "丑": "己癸辛", "寅": "甲丙戊", "卯": "乙", "辰": "戊乙癸", "巳": "丙戊庚", "午": "丁己", "未": "己丁乙", "申": "庚壬戊", "酉": "辛", "戌": "戊辛丁", "亥": "壬甲"}
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
CLASH = {"子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥"}
COMBINE = {"子": "丑", "寅": "亥", "卯": "戌", "辰": "酉", "巳": "申", "午": "未"}
HARM = {"子": "未", "丑": "午", "寅": "巳", "卯": "辰", "申": "亥", "酉": "戌"}
TRIADS = [set(x) for x in ("申子辰", "亥卯未", "寅午戌", "巳酉丑")]


def ten_god(day, other):
    same_polarity = (day in YANG) == (other in YANG)
    de, oe = ELEMENT[day], ELEMENT[other]
    if de == oe: return "比肩" if same_polarity else "劫财"
    if GENERATES[de] == oe: return "食神" if same_polarity else "伤官"
    if GENERATES[oe] == de: return "偏印" if same_polarity else "正印"
    if CONTROLS[de] == oe: return "偏财" if same_polarity else "正财"
    return "七杀" if same_polarity else "正官"


def inspect_chart(pillars):
    for p in pillars:
        if len(p) != 2 or p[0] not in STEMS or p[1] not in BRANCHES:
            raise ValueError(f"invalid pillar: {p}")
    day = pillars[2][0]
    branches = [p[1] for p in pillars]
    relations = []
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = branches[i], branches[j]
            if CLASH.get(a) == b or CLASH.get(b) == a: relations.append({"type": "冲", "between": a + b})
            if COMBINE.get(a) == b or COMBINE.get(b) == a: relations.append({"type": "六合", "between": a + b})
            if HARM.get(a) == b or HARM.get(b) == a: relations.append({"type": "害", "between": a + b})
    for triad in TRIADS:
        if triad.issubset(set(branches)): relations.append({"type": "三合", "between": "".join(b for b in BRANCHES if b in triad)})
    return {
        "input_mode": "verified_pillars", "pillars": pillars, "day_master": day,
        "visible_ten_gods": ["日主" if i == 2 else ten_god(day, p[0]) for i, p in enumerate(pillars)],
        "hidden_stems": [{"branch": p[1], "stems": [{"stem": s, "ten_god": ten_god(day, s)} for s in HIDDEN[p[1]]]} for p in pillars],
        "roots": [p[1] for p in pillars if day in HIDDEN[p[1]]], "branch_relations": relations,
        "boundary": "本脚本只校验结构，不由公历生日推四柱，也不自动定格局、旺衰或喜忌。",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pillars", nargs=4, metavar=("YEAR", "MONTH", "DAY", "HOUR"))
    a = p.parse_args()
    print(json.dumps(inspect_chart(a.pillars), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
