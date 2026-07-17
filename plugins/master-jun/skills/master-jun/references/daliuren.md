# 大六壬工作规范

## 排盘顺序

1. Verify civil date/time, timezone, lunar date, solar term, day ganzhi, and hour branch.
2. Determine 月将 by solar-term convention; state the convention.
3. Place 月将加占时 and construct heaven/earth plates.
4. Apply stem lodging and construct four lessons.
5. Determine 贼克、比用、涉害、遥克、昴星、别责、八专、伏吟、反吟 in the accepted order.
6. Derive three transmissions, then verify void, clash, punishment, combination, tomb, break, and advance/retreat sequences.
7. Place nobleman and twelve heavenly generals using the declared day/night and forward/reverse convention.
8. Add year fate/行年 only when birth-year data and school convention are available.

## Verification requirements

- Use `scripts/daliuren_core.py` for the plate, four lessons, nine-method selection, three transmissions,旬空, and heavenly generals.
- Do not trust a single OCR table or a single online calculator for a fragile chart.
- For 涉害、别责、八专 and nonstandard day/night rules, verify against a second method or reference.
- If the calendar basis or a school-sensitive rule is unverified, publish the computed result but label the affected transmission or general placement provisional.

## Interpretation order

1. 日干: asker/current agency.
2. 日支: matter, environment, counterpart, or position depending on the question.
3. 干支上神 and four lessons: immediate relations.
4. 初中末传: activation, development, outcome.
5. 天将: manner and social expression, not a standalone verdict.
6. 旺相休囚、旬空、月破、日冲, and seasonal support.
7. 类神: office, wealth, documents, movement, sponsor, competitor.
8. Known facts and question-specific semantics.

## Career semantics

- 官鬼 can indicate office, authority, pressure, assessment, or institutional constraint.
- 财 can indicate compensation, resources, business results, or what the asker controls.
- 父母 can indicate documents, approval, title, policy, sponsor, or organizational protection.
- 兄弟 can indicate peers, competition, budget sharing, or allies.
- 子孙 can indicate output, relief, product, subordinates, or reduced official pressure.
- 青龙/六合/贵人 often support resources and coordination; 白虎/螣蛇/朱雀/玄武 can indicate pressure, ambiguity, speech, politics, or hidden process. Interpret by context.
- 空亡 in an already-confirmed internal offer often means timing, paperwork, headcount, or unfinalized wording rather than nonexistence.

## Timing

- Give a window supported by transmissions, fill/冲空, relevant branches, process reality, and the user's deadline.
- Do not turn every branch into a precise date. Prefer observable milestones.
# Deterministic engine conventions

The bundled `scripts/daliuren_core.py` implements the common nine-method order and exposes its selection reason. It is suitable for reproducible calculation, but calendar inputs remain external and must be verified.

- Four lessons use the standard stem lodging table: 甲寅、乙辰、丙戊巳、丁己未、庚申、辛戌、壬亥、癸丑.
- Selection order: 伏吟/反吟 special handling; 贼克/元首; 比用; 涉害; 遥克; 昴星; 别责; 八专.
- 涉害 currently uses the published 孟仲季 simplification, with equal-depth resolution by 刚日前、柔日后. Label this convention in user-facing output because full涉归本家 depth counting and school variants may differ.
- 伏吟 uses the transmitted stem formulas where available and the刑/自刑/冲 rules otherwise. 反吟无克 accepts the standard井栏六日 only.
- Nobleman convention: 甲戊庚丑未、乙己子申、丙丁亥酉、壬癸巳卯、辛午寅; first is day, second night. If nobleman lands on 亥子丑寅卯辰, generals proceed forward; otherwise reverse.
- Never infer the month general, day pillar, or day/night period from guesswork. Feed verified values, and calculate adjacent variants when uncertain.
