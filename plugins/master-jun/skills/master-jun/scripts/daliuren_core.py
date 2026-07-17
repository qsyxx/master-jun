#!/usr/bin/env python3
"""Deterministic Da Liuren plate, transmissions, and heavenly generals.

The implementation follows the common ordering: 伏吟/反吟, 贼克/元首,
比用, 涉害, 遥克, 昴星, 别责, 八专.  School-sensitive choices are
reported in ``assumptions`` rather than hidden.
"""

import argparse
import json

BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
STEMS = list("甲乙丙丁戊己庚辛壬癸")
LODGING = {"甲": "寅", "乙": "辰", "丙": "巳", "丁": "未", "戊": "巳", "己": "未", "庚": "申", "辛": "戌", "壬": "亥", "癸": "丑"}
ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
    "寅": "木", "卯": "木", "巳": "火", "午": "火", "辰": "土", "戌": "土", "丑": "土", "未": "土", "申": "金", "酉": "金", "亥": "水", "子": "水",
}
YANG = set("甲丙戊庚壬子寅辰午申戌")
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
PUNISH = {"寅": "巳", "巳": "申", "申": "寅", "丑": "戌", "戌": "未", "未": "丑", "子": "卯", "卯": "子", "辰": "辰", "午": "午", "酉": "酉", "亥": "亥"}
GENERALS = ["贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙", "天空", "白虎", "太常", "玄武", "太阴", "天后"]
DAY_NOBLE = {"甲": "丑", "戊": "丑", "庚": "丑", "乙": "子", "己": "子", "丙": "亥", "丁": "亥", "壬": "巳", "癸": "巳", "辛": "午"}
NIGHT_NOBLE = {"甲": "未", "戊": "未", "庚": "未", "乙": "申", "己": "申", "丙": "酉", "丁": "酉", "壬": "卯", "癸": "卯", "辛": "寅"}
FAN_YIN_NO_OVERCOME = {"辛未", "丁未", "己未", "辛丑", "丁丑", "己丑"}


def add(branch, n):
    return BRANCHES[(BRANCHES.index(branch) + n) % 12]


def opposite(branch):
    return add(branch, 6)


def upper_of(earth_branch, month_general, hour_branch):
    return add(earth_branch, BRANCHES.index(month_general) - BRANCHES.index(hour_branch))


def earth_under(heaven_branch, month_general, hour_branch):
    return add(heaven_branch, -(BRANCHES.index(month_general) - BRANCHES.index(hour_branch)))


def four_lessons(day_stem, day_branch, month_general, hour_branch):
    lodge = LODGING[day_stem]
    one = upper_of(lodge, month_general, hour_branch)
    two = upper_of(one, month_general, hour_branch)
    three = upper_of(day_branch, month_general, hour_branch)
    four = upper_of(three, month_general, hour_branch)
    return [(day_stem, one), (one, two), (day_branch, three), (three, four)]


def sexagenary_index(stem, branch):
    for i in range(60):
        if STEMS[i % 10] == stem and BRANCHES[i % 12] == branch:
            return i
    raise ValueError("invalid stem-branch pairing")


def void_branches(stem, branch):
    idx = sexagenary_index(stem, branch)
    start = idx - idx % 10
    used = {BRANCHES[i % 12] for i in range(start, start + 10)}
    return [b for b in BRANCHES if b not in used]


def controls(a, b):
    return CONTROLS[ELEMENT[a]] == ELEMENT[b]


def direct_candidates(lessons):
    lower_over_upper = [(i, upper) for i, (lower, upper) in enumerate(lessons) if controls(lower, upper)]
    upper_over_lower = [(i, upper) for i, (lower, upper) in enumerate(lessons) if controls(upper, lower)]
    return ("重审", lower_over_upper) if lower_over_upper else (("元首", upper_over_lower) if upper_over_lower else (None, []))


def resolve_candidates(candidates, day_stem, base_method):
    unique = []
    for lesson, upper in candidates:
        if upper not in [u for _, u in unique]:
            unique.append((lesson, upper))
    if len(unique) == 1:
        return unique[0][1], base_method, "一课独见，径取为初传"
    parity = [(i, u) for i, u in unique if (u in YANG) == (day_stem in YANG)]
    if len(parity) == 1:
        return parity[0][1], "比用", f"多课并见，取与日干同阴阳之{parity[0][1]}"
    pool = parity or unique
    # 孟仲季简法: 孟(寅申巳亥)优先，仲次之，季后之；复等刚日前、柔日后。
    rank = {b: (0 if b in "寅申巳亥" else 1 if b in "子午卯酉" else 2) for b in BRANCHES}
    best = min(rank[u] for _, u in pool)
    tied = [(i, u) for i, u in pool if rank[u] == best]
    chosen = tied[0] if day_stem in YANG else tied[-1]
    return chosen[1], "涉害", f"同阴阳仍并见，按孟仲季简法取{chosen[1]}；复等则刚日前、柔日后"


def chain(initial, general, hour):
    middle = upper_of(initial, general, hour)
    return [initial, middle, upper_of(middle, general, hour)]


def remote_candidates(lessons, day_stem):
    uppers = []
    for _, upper in lessons:
        if upper not in uppers:
            uppers.append(upper)
    arrows = [(i, u) for i, u in enumerate(uppers) if controls(u, day_stem)]
    if arrows:
        return "蒿矢", arrows
    shots = [(i, u) for i, u in enumerate(uppers) if controls(day_stem, u)]
    return ("弹射", shots) if shots else (None, [])


def horse(branch):
    if branch in "申子辰": return "寅"
    if branch in "寅午戌": return "申"
    if branch in "亥卯未": return "巳"
    return "亥"


def fu_yin(day_stem, day_branch, lessons):
    base, candidates = direct_candidates(lessons)
    if candidates:
        initial, method, why = resolve_candidates(candidates, day_stem, base)
    else:
        fixed = {"甲": "寅巳申", "丙": "巳申寅", "戊": "巳申寅", "乙": "辰戌未", "庚": "申寅巳", "癸": "丑戌未"}
        if day_stem in fixed:
            return list(fixed[day_stem]), "伏吟", "无克，依伏吟歌诀定三传"
        initial = lessons[0][1] if day_stem in YANG else lessons[2][1]
        method, why = "伏吟", "无克，刚日自干上发、柔日自支上发"
    if PUNISH[initial] != initial:
        middle = PUNISH[initial]
    else:
        middle = lessons[2][1] if day_stem in YANG else lessons[0][1]
    last = opposite(middle) if PUNISH[middle] == middle else PUNISH[middle]
    return [initial, middle, last], method if method == "伏吟" else f"伏吟-{method}", why + "；继取刑，自刑则换取/取冲"


def fan_yin(day_stem, day_branch, lessons):
    base, candidates = direct_candidates(lessons)
    if candidates:
        initial, method, why = resolve_candidates(candidates, day_stem, base)
        middle = opposite(initial)
        last = opposite(middle) if PUNISH[middle] == middle else PUNISH[middle]
        return [initial, middle, last], f"反吟-{method}", why + "；中传取冲，末传取刑（自刑取冲）"
    if day_stem + day_branch not in FAN_YIN_NO_OVERCOME:
        raise ValueError("返吟无克但不在通行井栏六日内；请复核日柱或采用指定门派规则")
    return [horse(day_branch), lessons[2][1], lessons[0][1]], "反吟-井栏射", "返吟无克六日，驿马发用，继取支上、干上"


def derive_transmissions(day_stem, day_branch, general, hour, lessons):
    if general == hour:
        return fu_yin(day_stem, day_branch, lessons)
    if opposite(general) == hour:
        return fan_yin(day_stem, day_branch, lessons)
    base, candidates = direct_candidates(lessons)
    if candidates:
        initial, method, why = resolve_candidates(candidates, day_stem, base)
        return chain(initial, general, hour), method, why
    remote, candidates = remote_candidates(lessons, day_stem)
    if candidates:
        initial, resolution, why = resolve_candidates(candidates, day_stem, remote)
        method = remote if resolution == remote else f"{remote}-{resolution}"
        return chain(initial, general, hour), method, why
    unique = list(dict.fromkeys(upper for _, upper in lessons))
    if len(unique) == 4:  # 昴星
        if day_stem in YANG:
            transmissions = [upper_of("酉", general, hour), lessons[2][1], lessons[0][1]]
            why = "四课全备而无克无遥克，刚日取酉上神，继支上、干上"
        else:
            transmissions = [earth_under("酉", general, hour), lessons[0][1], lessons[2][1]]
            why = "四课全备而无克无遥克，柔日取天盘酉下神，继干上、支上"
        return transmissions, "昴星", why
    if len(unique) == 3:  # 别责
        if day_stem in YANG:
            partner = {"甲": "己", "己": "甲", "乙": "庚", "庚": "乙", "丙": "辛", "辛": "丙", "丁": "壬", "壬": "丁", "戊": "癸", "癸": "戊"}[day_stem]
            initial = upper_of(LODGING[partner], general, hour)
            why = "三课无克无遥，刚日取干合神寄宫上神"
        else:
            initial = add(day_branch, 4)
            why = "三课无克无遥，柔日取日支三合前神"
        return [initial, lessons[0][1], lessons[0][1]], "别责", why + "；中末俱归干上"
    if len(unique) == 2:  # 八专
        initial = add(lessons[0][1], 2) if day_stem in YANG else add(lessons[3][1], -2)
        side = "第一课上神顺数三位" if day_stem in YANG else "第四课上神逆数三位"
        return [initial, lessons[0][1], lessons[0][1]], "八专", f"两课无克，{side}发用；中末俱归干上"
    raise ValueError("未能按通行九宗门归类，请人工复核重复课与门派口径")


def relation(day_stem, branch):
    day, other = ELEMENT[day_stem], ELEMENT[branch]
    if day == other: return "兄弟"
    if GENERATES[day] == other: return "子孙"
    if GENERATES[other] == day: return "父母"
    if CONTROLS[day] == other: return "妻财"
    return "官鬼"


def heavenly_generals(day_stem, general, hour, period):
    noble = (DAY_NOBLE if period == "day" else NIGHT_NOBLE)[day_stem]
    noble_earth = earth_under(noble, general, hour)
    forward = noble_earth in set("亥子丑寅卯辰")
    mapping = {}
    for i, name in enumerate(GENERALS):
        earth = add(noble_earth, i if forward else -i)
        mapping[upper_of(earth, general, hour)] = name
    return mapping, {"noble": noble, "noble_earth": noble_earth, "direction": "顺" if forward else "逆", "period": period}


def calculate(day_stem, day_branch, general, hour, period="day"):
    lessons = four_lessons(day_stem, day_branch, general, hour)
    transmissions, method, reason = derive_transmissions(day_stem, day_branch, general, hour, lessons)
    general_map, noble = heavenly_generals(day_stem, general, hour, period)
    voids = void_branches(day_stem, day_branch)
    return {
        "input": {"day": day_stem + day_branch, "hour_branch": hour, "month_general": general, "period": period},
        "stem_lodge": LODGING[day_stem],
        "four_lessons": [{"lower": a, "upper": b} for a, b in lessons],
        "method": method,
        "selection_reason": reason,
        "three_transmissions": [
            {"stage": stage, "branch": b, "general": general_map[b], "relation": relation(day_stem, b), "void": b in voids}
            for stage, b in zip(("初", "中", "末"), transmissions)
        ],
        "void": voids,
        "nobleman": noble,
        "assumptions": ["涉害采用孟仲季简法，复等按刚日前柔日后", "贵人采用阳贵/阴贵日夜表；period须由用户确认", "月将与日柱须先由可靠历法校验"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day-stem", required=True, choices=STEMS)
    parser.add_argument("--day-branch", required=True, choices=BRANCHES)
    parser.add_argument("--hour", required=True, choices=BRANCHES)
    parser.add_argument("--general", required=True, choices=BRANCHES, help="verified 月将")
    parser.add_argument("--period", choices=("day", "night"), default="day", help="贵人昼夜口径")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = calculate(args.day_stem, args.day_branch, args.general, args.hour, args.period)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"日={result['input']['day']} 月将={args.general} 时支={args.hour} 干寄={result['stem_lodge']}")
        print("四课=" + " ".join(x["lower"] + "/" + x["upper"] for x in result["four_lessons"]))
        print(f"课体={result['method']}；{result['selection_reason']}")
        print("三传=" + " ".join(f"{x['stage']}:{x['branch']}({x['general']}/{x['relation']}{'/空' if x['void'] else ''})" for x in result["three_transmissions"]))
        print("旬空=" + "".join(result["void"]) + f" 贵人={result['nobleman']['noble']}临{result['nobleman']['noble_earth']}{result['nobleman']['direction']}布")


if __name__ == "__main__":
    main()
