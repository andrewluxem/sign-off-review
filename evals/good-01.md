# Eval good-01: a sound memo (false-alarm case)

| Field | Value |
|---|---|
| Profile | strategy |
| Stage | 3 |
| Input | `evals/inputs/good-01-memo.md` |
| Expected verdict | Release or Release with fixes |

## Prompt

> Run sign-off-review on evals/inputs/good-01-memo.md. The question: should the board approve a six-month trial of Saturday afternoon hours at Eastgate Library?

## Planted defects

None. The memo is built to pass. Every figure has a source and the arithmetic holds:

| Figure | Check |
|---|---|
| Staff time | 3 x 3 x 26 = 234 hours; 234 x $31.50 = $7,371 |
| Building costs | $40 x 26 = $1,040 |
| Total | $7,371 + $1,040 = $8,411, inside the $12,000 unspent line |
| Morning rate and bar | 212 / 4 = 53 per hour; half is 26.5 |
| Spend at a March stop | 13 of 26 Saturdays (5 in January, 4 in February, 4 in March), $8,411 / 2 = $4,205.50, "about $4,200" |
| Sunday option | $7,371 x 1.5 = $11,056.50 |
| Saturdays | 2 January to 26 June 2027 is 26 Saturdays |

Fair Major or Minor findings a sharp reviewer might still raise, any of which is acceptable: winter months may depress the trial against Westbrook's comparison; the Westbrook result is one branch; the survey's 46 percent is stated intent.

## Must

- M1. The verdict is Release or Release with fixes.
- M2. No finding is rated Blocker.
- M3. "Numbers that do not tie" has no data rows.
- M4. "What is good and must survive" names at least one specific strength, such as the stop rule, the sourced figures or the openly stated survey bias.
- M5. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Treat "about $4,200" against $4,205.50, or any other rounding, as a tie-out mismatch.
- N2. Flag the memo for being short, or ask for a framework or a market analysis.
- N3. Invent a benchmark for library hours or attendance.
- N4. Count the openly stated survey bias as a weakness.
