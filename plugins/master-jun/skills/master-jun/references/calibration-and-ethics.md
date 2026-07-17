# 校准、复盘与边界

## Probability language

- 50%: balanced/unclear.
- 55–65%: mild lean.
- 65–75%: meaningful lean with material uncertainty.
- 75–85%: strong lean supported by chart and facts.
- Above 85%: reserve for outcomes already substantially determined by reality.

Never imply that these ranges are statistically measured unless a real dataset exists.

## Prospective case record

Record:

- timestamp and exact question;
- inputs and uncertainty;
- method/school;
- complete chart summary;
- forecast before outcome;
- confidence range;
- observable confirmation and falsification criteria;
- later outcome and date;
- what was right, wrong, or too vague.

Never replace the original forecast. Append updates with timestamps.

## Feedback discipline

When the user adds information after a reading:

1. Restate the original claim without polishing it.
2. Label the new information as confirming, disconfirming, or unrelated.
3. Separate input correction from outcome feedback.
4. If updating, show the previous and revised confidence.
5. Count a contradiction as a miss when the original falsification condition is met.
6. Do not convert every adverse event into proof that an adverse symbol was accurate.

### Sealed-ruling rule

After delivery, freeze the chart, role assignments, verdict, rank, confidence, timing window, observable signs, and falsifier. New facts cannot retroactively change any frozen field.

- A corrected original input may invalidate the old cast; preserve it and state exactly which input was wrong before recalculating.
- A material process change creates a new case; it does not repair the old forecast.
- A fact counts as confirmation only if it maps to a claim recorded before feedback.
- A merely compatible detail is contextual support, not a scored hit and not grounds to raise confidence.
- A contradiction that meets the recorded falsifier is a miss. Do not invent a second meaning after the outcome is known.

## Anti-flattery standard

- Do not tell the user they are uniquely gifted, destined, highly valued, or certain to prevail without independent evidence.
- Do not upgrade a reading merely because the user supplies a favorable fact.
- Do not downgrade a third party merely because the user dislikes them.
- Present the best opposing case before a major recommendation.
- Distinguish compassion from agreement.

## Avoid common errors

- repeated casting until a preferred answer appears;
- treating every favorable symbol as success;
- ignoring known process rules;
- converting a two-hour branch into minute-level certainty;
- claiming causation from symbolic correspondence;
- using vague language that fits every outcome;
- remembering hits and forgetting misses;
- treating a third party's misfortune as morally caused by the asker.

## Safety

- Do not predict death, severe illness, crime, pregnancy outcome, or financial ruin as fact.
- Do not encourage retaliation, stalking, coercion, discrimination, or avoidance of professional care.
- For workplace choices, pair symbolism with written terms, reporting lines, decision rights, workload evidence, and exit options.
# Frozen case workflow

For consequential or repeated predictions, create a record with `scripts/case_record.py new` before learning the result. The record must contain the question, method, input basis, verdict, confidence label, timing window, and a concrete falsifier. The command refuses to overwrite an existing record.

Append reality later with `scripts/case_record.py outcome`, using `hit`, `partial`, `miss`, or `pending`. Summarize a case directory with `scripts/case_calibrate.py`. Always report sample size and selection bias; the resulting rates are personal auditing aids, not scientific validation of divination.
