# Eval grades, 2026-10-23, skill at 1de9f2f

The skill files at `1de9f2f` are identical to `c76409a`. This run repeats the `c76409a` run with the method fixed: cases ran two at a time, and every case ran all five seats as parallel subagents (30 of 30 seats). Each lead agent saw only an installed copy of the skill (`git archive HEAD SKILL.md references scripts`) and the case's input files, never the case file. Graded by hand against the case files.

**Result: 5 of 6 cases pass. pitch-01 fails M2 again.**

## Summary

| Case | Verdict | Must | Must-not | Blocker | Major | Minor | Total | Tie rows |
|---|---|---|---|---|---|---|---|---|
| strategy-01 | Return | 8/8 | none | 1 | 11 | 2 | 14 | 1 |
| good-01 | Release with fixes | 5/5 | none | 0 | 2 | 11 | 13 | 0 |
| pitch-01 | Return | **6/7** | none | 1 | 13 | 5 | 19 | 0 |
| brief-01 | Return | 8/8 | none | 2 | 4 | 2 | 8 | 0 |
| job-01 | Return | 8/8 | none | 2 | 5 | 7 | 14 | 2 |
| plan-01 | Return | 7/7 | none | 3 | 10 | 3 | 16 | 0 |
| **All** | | 42/43 | none | 9 | 45 | 30 | 84 | 3 |

## Failure

**pitch-01, M2** ("The 212 percent claim is a Blocker"). The review raises the claim as two Majors: finding 4 (no starting value, end value, period or comparator, and a different metric from the one promised) and finding 5 (client unnamed, not cleared for citing). The lead reports that the Evidence seat rated the claim Blocker and that calibration lowered it to Major after the scope problem became the single Blocker (finding 1). The verdict, Return, is as expected. The `c76409a` run failed the same criterion, with the claim also at Major.

## Per case

**strategy-01.** M1 to M8 pass: tie row $1.4M vs $1.1M; Reconcile Blocker with the payback folded in; benchmark unsourced with no replacement (finding 9); owner (6); downside (3, 4); premortem internal (1, 2).

**good-01.** M1 to M5 pass. N1 avoided ("about $4,200" checked as $4,205.50). N4 avoided (survey intent listed as "not a finding" and as a strength). Majors: the stop rule cannot tell new visitors from shifted ones; other Saturday windows are not ruled out.

**pitch-01.** M1, M3 (finding 1, Blocker), M4 (10, 12), M5, M6 and M7 pass. M2 fails as above.

**brief-01.** M1 to M8 pass: anecdote-to-rule Blocker (1); four unsourced external claims, including the 73 percent figure and "Studies show", as one Blocker (2); counterargument met through findings 4 to 6; AI tells in one Minor handed to avoid-ai-writing (8). One web search for the 73 percent figure found no origin, and no figure from it was used. Finding 1's fix describes what the scoped claim must contain without supplying wording, so N2 counts as avoided.

**job-01.** M1 to M8 pass: tie rows for $0.42 vs $0.48 and Mar 2021 vs 2020, both Reconcile Blockers; time since Jun 2024 (4); holdout testing missing, with a fix that applies only if a holdout was run (3); missing JD terms "only where the candidate has done it" (12). Some fixes name single-term swaps to match JD wording (finding 10); these are targeted instructions, not rewritten bullets, so N2 counts as avoided.

**plan-01.** M1 to M7 pass: backup and rollback Blocker (1); chat-history step Blocker (2); flags unverified with a `--help` fix (7); done-when (8). A third Blocker (3: no Postgres connection details) again sits above the case file's expected severity for D6, and again matches "a step a fresh executor cannot carry out".

## Unclear spots the lead agents reported (not yet addressed)

1. Merging keeps the highest severity, then calibration may lower it, and nothing says whether a finding is judged on its own or in light of the others (all 6 runs). This is the likely cause of the pitch-01 failure.
2. No tie-break when several seats' checks name the same root cause (6 runs).
3. The seat brief's "Open no file other than the draft and the target role" confuses seats on non-job-search profiles (5 runs).
4. The seat brief carries no review date, which gap and expiry checks need (2 runs).
5. "Missing outside view" has no format, and whether it lists gaps that are not findings is unstated (3 runs).
6. Seats get the severity definitions but not the calibration rules, so they rate high: one lead counted 9 Blockers in 31 seat rows (2 runs).
7. A first review has no rule for recording a severity change or a dropped seat finding (3 runs).
