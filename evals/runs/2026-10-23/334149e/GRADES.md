# Eval grades, 2026-10-23

Skill version: commit `334149e`. Each case ran in Claude Code as a fresh agent that saw only an installed copy of the skill (`SKILL.md`, `references/`, `scripts/`) and the input file, never the case file. Both runs used five parallel seat subagents. Graded by hand against the case files.

## strategy-01: Return

| Criterion | Result | Evidence in the review |
|---|---|---|
| M1 verdict Return | pass | Verdict line |
| M2 tie-out row $1.4M vs $1.1M, $0.3M | pass | Numbers that do not tie |
| M3 Blocker with a settle-on-one-figure fix | pass | Finding 1, "Reconcile the saving to one figure" |
| M4 benchmark flagged unsourced, no replacement | pass | Finding 7; Missing outside view |
| M5 missing owner flagged | pass | Finding 9 |
| M6 unpriced peak downside flagged | pass | Finding 3 |
| M7 three premortem reasons, one internal | pass | Items 1 and 2 tagged (internal) |
| M8 validator exits 0 | pass | `check_report.py`: ok |
| N1 payback recalculation as its own Blocker or tie row | not present | Folded into finding 1 |
| N2 invented benchmark | not present | |
| N3 rewritten memo sentences | not present | Fixes are instructions |
| N4 length or framework complaint | not present | |

Watch item: 1 Blocker, 9 Majors, 5 Minors. Each Major maps to a strategy check, but the count is high.

## good-01: Release with fixes

| Criterion | Result | Evidence in the review |
|---|---|---|
| M1 verdict Release or Release with fixes | pass | Release with fixes |
| M2 no Blocker | pass | Logic seat's Blocker capped at Major by calibration question 4 |
| M3 no tie-out rows | pass | "None." |
| M4 a specific strength survives | pass | Stop rule, sourced cost table, stated survey bias |
| M5 validator exits 0 | pass | `check_report.py`: ok |
| N1 rounding treated as a mismatch | not present | "$4,206 ... matches about $4,200" |
| N2 length, framework or market-analysis demand | not present | |
| N3 invented benchmark | not present | |
| N4 stated survey bias counted as a weakness | not present | Listed under What is good |

Watch item: 3 Majors, 12 Minors. The Majors are fair (the stop rule can pass on visitors who only arrive later; the Saturday pay basis is unsourced; other Saturday windows are not ruled out).

## Clarifications made after these runs

Both lead agents reported unclear spots. Commits `0a58af8` and the one that adds this file address them: tie-out Blockers stay with `Lead`, seats learn the recalculation cap, an optional `**Assumptions:**` line, outside-view gaps cite existing findings, step 7 runs in order, and seats open no file but the draft.
