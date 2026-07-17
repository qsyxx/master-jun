# 八字与紫微斗数

## Required inputs

- birth date and whether it is Gregorian/lunar;
- exact birth time and uncertainty range;
- birthplace and timezone;
- sex/gender convention required by the chosen school;
- events for time rectification only when the user explicitly requests rectification.

## Bazi workflow

1. Verify four pillars using solar-term month boundaries and declared day-boundary rule.
2. Assess seasonal qi, roots,透干, combinations, clashes, dryness/moisture, and overall structure.
3. Compare pattern, useful-god,调候, and气势 approaches without forcing agreement.
4. Derive luck cycles with declared direction and start-age convention.
5. Tie claims to observable life themes; avoid deterministic claims about death, disease, or disaster.

## Zi Wei workflow

1. Verify lunar date, leap-month handling, birth-hour branch, and life/body palaces.
2. Fix the school and tables for main stars, auxiliaries, 四化, brightness, and decade direction.
3. Generate the chart deterministically; never place stars from memory when a table is available.
4. Read palace triads, opposite palace, transformations, decade/year overlays, and actual life context.
5. If birth time lies near a boundary, compare adjacent-hour charts and report sensitivity.

## Cross-system discipline

- Bazi and Ziwei may describe the same theme through different models; agreement is supportive, disagreement is information.
- Do not retrofit every past event. Ask for a small set of dated events and record misses.
# Engine boundary

Use `scripts/bazi_core.py` to audit a chart only after the four pillars are independently verified. It deliberately refuses to turn civil birth data into pillars: solar-term month boundaries, 23:00 day boundaries, true-solar correction, and historical time standards need a dedicated calendar source.

Use `scripts/ziwei_base.py` only to compute the transparent 命宫、身宫 and major-cycle direction base. Its `BASE_ONLY` marker means fourteen main stars, five-element bureau, four transformations, and major cycles have not been placed. Do not make star-based claims from that base.

