# Eval grades, 2026-10-24, skill at 47b08be

Changes since `1de9f2f`: each finding is calibrated on its own, and another finding forcing Return never lowers it (`b51515f`); the Blocker example is checkable from the page; seat tie-break by most specific check, then lower seat number; the target-role file applies to job-search only; the README pointer is gone; seats get a review date; a refused seat launch runs inline and is noted (`47b08be`). `evals/pitch-01.md` M2 now accepts Major or Blocker for the 212 percent claim, with a fix that names the client with a baseline and timeframe or cuts the claim, and adds must-not N4 (rated Minor).

Method: cases ran two at a time; every case ran all five seats as parallel subagents (30 of 30). Each lead agent saw only an installed copy of the skill (`git archive HEAD SKILL.md references scripts`) and the case's input files, never the case file. Graded by hand against the case files.

**Result: 6 of 6 cases pass.**

## Summary

| Case | Verdict | Must | Must-not | Blocker | Major | Minor | Total | Tie rows |
|---|---|---|---|---|---|---|---|---|
| strategy-01 | Return | 8/8 | none | 1 | 9 | 4 | 14 | 1 |
| good-01 | Release with fixes | 5/5 | none | 0 | 2 | 15 | 17 | 0 |
| pitch-01 | Return | 7/7 | none | 2 | 9 | 3 | 14 | 0 |
| brief-01 | Return | 8/8 | none | 2 | 4 | 1 | 7 | 0 |
| job-01 | Return | 8/8 | none | 2 | 5 | 12 | 19 | 2 |
| plan-01 | Return | 7/7 | none | 3 | 10 | 2 | 15 | 0 |
| **All** | | 43/43 | none | 10 | 39 | 37 | 86 | 3 |

## Severity counts against 1de9f2f

Both runs used five parallel seats per case.

| Case | Blocker | Major | Minor | Total | 1de9f2f Blocker | Major | Minor | Total | Change in total |
|---|---|---|---|---|---|---|---|---|---|
| strategy-01 | 1 | 9 | 4 | 14 | 1 | 11 | 2 | 14 | 0 |
| good-01 | 0 | 2 | 15 | 17 | 0 | 2 | 11 | 13 | +4 |
| pitch-01 | 2 | 9 | 3 | 14 | 1 | 13 | 5 | 19 | -5 |
| brief-01 | 2 | 4 | 1 | 7 | 2 | 4 | 2 | 8 | -1 |
| job-01 | 2 | 5 | 12 | 19 | 2 | 5 | 7 | 14 | +5 |
| plan-01 | 3 | 10 | 2 | 15 | 3 | 10 | 3 | 16 | -1 |
| **All** | 10 | 39 | 37 | 86 | 9 | 45 | 30 | 84 | +2 |

Majors fell by 6 and Minors rose by 7. Blockers rose by one, in pitch-01, where the undefined 15 percent target is now a second Blocker beside the scope gap.

## Per case

**strategy-01.** M1 to M8 pass: tie row $1.4M vs $1.1M; Reconcile Blocker with the payback folded in (N1 avoided); benchmark unsourced with no replacement (finding 8); downside (2); owner (10); premortem internal (1).

**good-01.** M1 to M5 pass: no Blocker, no tie rows, every repeated figure checked and "about $4,200" accepted (N1 avoided). The stated survey bias is listed as a strength and "No finding" (N4 avoided). Majors: the stop rule can pass on shifted visitors; free alternatives not ruled out.

**pitch-01.** M1, M3 (finding 1, Blocker), M4 (8 exclusions, 12 price build-up), M5, M6 and M7 pass. M2 passes with a judgment call: the 212 percent claim is finding 3 (Major), and its fix reads "Name the client with written permission, or describe it specifically enough to check. Add the baseline, the period and Ostler & Finch's role, and state that the result may be cited. Cut the claim if permission is refused." The "describe it specifically enough to check" path is the pitch profile's own check 3.2 wording and still demands a baseline, a period and citability, so it is not a softened wording. N4 avoided (rated Major).

**brief-01.** M1 to M8 pass: anecdote-to-rule Blocker (1); uncontrolled 18 percent result as a second Blocker (2); 73 percent figure and "Studies show" unsourced, fix to source with the fetched URL or cut (3); counterargument met (2, 5); AI tells in one Minor to avoid-ai-writing (7). No search figures used.

**job-01.** M1 to M8 pass: tie rows for $0.42 vs $0.48 and Mar 2021 vs 2020, both Reconcile Blockers; 28-month gap (3); holdout evidence only if the candidate ran one (4); baselines (6). Finding 14 notes that "eight years" reads as covering SMS; it is a Minor about scope, not a mismatch, so N3 is avoided.

**plan-01.** M1 to M7 pass: delete-before-verify Blocker (1); chat-history schema Blocker (2); flags to be sourced from `--help` or the source file (6); done-when (7). The third Blocker (3: no connection details) again sits above the case file's expected severity for D6 and matches "a step a fresh executor cannot carry out".

## Unclear spots the lead agents reported (not yet addressed)

1. Merging keeps the highest severity and calibration then runs; whether calibration may lower a merged severity is implied by the order but never stated (6 runs).
2. The seat brief's TARGET ROLE template line has no instruction for other profiles; leads omitted it or wrote "not applicable" (4 runs).
3. A first review has no place to record why a seat's severity was changed or a seat finding dropped (3 runs).
4. Whether the fix verbs listed in SKILL.md are a closed list (2 runs).
5. "Answer the draft gives" fits memos better than applications and build plans (2 runs).
6. Whether "Missing outside view" lists gaps that are not findings (2 runs).
7. The build-plan profile calls a path spelled two ways an Evidence finding, but only the Lead sees the inventory (1 run).
