# Eval grades, 2026-10-23, skill at c76409a

Each case ran in Claude Code as a fresh lead agent that saw only an installed copy of the skill (`git archive HEAD SKILL.md references scripts`) and the case's input files, never the case file. Graded by hand against the case files.

**Result: 5 of 6 cases pass. pitch-01 fails M2.**

## Summary

| Case | Verdict | Must | Must-not | Blocker | Major | Minor | Total | Tie rows | Seats ran as |
|---|---|---|---|---|---|---|---|---|---|
| strategy-01 | Return | 8/8 | none | 1 | 9 | 5 | 15 | 1 | 5 parallel subagents |
| good-01 | Release with fixes | 5/5 | none | 0 | 1 | 6 | 7 | 0 | sequential (limit hit) |
| pitch-01 | Return | **6/7** | none | 2 | 13 | 3 | 18 | 0 | 4 subagents + 1 inline |
| brief-01 | Return | 8/8 | none | 2 | 5 | 2 | 9 | 0 | 2 subagents + 3 inline |
| job-01 | Return | 8/8 | none | 2 | 3 | 6 | 11 | 2 | sequential (limit hit) |
| plan-01 | Return | 7/7 | none | 3 | 9 | 4 | 16 | 0 | 5 parallel subagents |
| **All** | | 42/43 | none | 10 | 40 | 26 | 76 | 3 | |

Method caveat: the six leads were launched at once, and their seat launches hit the session's concurrent-subagent limit. Only strategy-01 and plan-01 ran all five seats as parallel subagents. The others fell back, fully or partly, to the skill's sequential mode. In sequential mode the lead has already built the number inventory before playing the seats.

## Failure

**pitch-01, M2** ("The 212 percent claim is a Blocker"). The review raises the claim as two Majors: finding 7 (unnamed client, not cleared for citing, unclear share of the work) and finding 8 (no baseline, period or comparison, and a different metric from the one promised). Every element M2 asks for is cited, but at Major. The Decision seat's notes show it rated the claim Major as well. The review's two Blockers went to the 15 percent outcome the scope cannot produce, and to the 15 percent figure having no baseline. The verdict, Return, is as expected.

## Per case

**strategy-01.** M1 to M8 pass: tie row $1.4M vs $1.1M; Reconcile Blocker with the payback folded in (N1 avoided); benchmark flagged with no replacement (finding 7); owner (2); downside (5); premortem internal (1). Same counts as the first pass at 334149e.

**good-01.** M1 to M5 pass: no Blocker, no tie rows, strengths name the sourced figures, the stop rule and the stated survey bias. N1 avoided ("about $4,200" accepted). N4 avoided (survey intent listed as "not a finding"). Its one Major (the stop rule cannot tell new visitors from shifted ones) is fair.

**pitch-01.** M1, M3 (finding 1, Blocker), M4 (11, 13), M5, M6 and M7 pass. M2 fails as above.

**brief-01.** M1 to M8 pass: anecdote-to-rule Blocker (1); 73 percent stat without a source (2, rated Blocker, above the case file's expected Major); "Studies show" (7); the counterargument is met through findings 1, 3 and 4; AI tells in one Minor handed to avoid-ai-writing (9). The lead ran one web search for the 73 percent figure, found no origin and reported no figures from the results.

**job-01.** M1 to M8 pass: tie rows for $0.42 vs $0.48 and Mar 2021 vs 2020, both Reconcile Blockers; baseline gap (5); time since Jun 2024 (4); holdout testing missing, with a fix that applies only if a holdout was actually run (3). N3 avoided ("eight years" accepted).

**plan-01.** M1 to M7 pass: backup and rollback Blocker (1); chat-history step Blocker (2); flags unverified with a `--help` pre-flight fix (6); done-when (5). A third Blocker (3: no database target or `DATABASE_URL` value) sits above the case file's expected Minor or Major for D6, but it matches the skill's "a step a fresh executor cannot carry out".

## Unclear spots the lead agents reported (not yet addressed)

1. SKILL.md says "Details in the README", but the installed skill has no README (3 runs).
2. Nothing covers a subagent tool that exists but refuses launches, and sequential mode cannot keep the inventory from the seats because step 2 runs before step 3 (4 runs).
3. The seat brief's TARGET ROLE line confuses seats on other profiles (2 runs).
4. No tie-break when several seats' checks name the same root cause (5 runs).
5. The seat brief carries no review date, which gap and expiry checks need (2 runs).
6. "Missing outside view" has no format, and it is unclear whether a firm's own case result counts as a benchmark to fetch (3 runs).
7. A first review has no rule for recording why a seat's severity was changed (2 runs).
