# Eval job-01: a metric and a date range that differ across documents

| Field | Value |
|---|---|
| Profile | job-search |
| Stage | 3 |
| Inputs | `evals/inputs/job-01-resume.md`, `evals/inputs/job-01-cover-letter.md` |
| Target role | `evals/inputs/job-01-jd.md` |
| Expected verdict | Return |

## Prompt

> Run sign-off-review on evals/inputs/job-01-resume.md and evals/inputs/job-01-cover-letter.md together, against the job description in evals/inputs/job-01-jd.md. The question: will this application earn a first interview for the Fenwick Trail Supply role?

## Planted defects

| # | Defect | Where | Expected severity | Expected seat |
|---|---|---|---|---|
| D1 | Revenue per email is $0.42 in the resume and $0.48 in the cover letter. | Resume, Corvid; cover letter, paragraph 2 | Blocker, with a tie-out row | Lead |
| D2 | Corvid start date is Mar 2021 in the resume and 2020 in the cover letter, which also overlaps the Tansy & Rye role (to Feb 2021). | Resume, Corvid; cover letter, paragraph 2 | Blocker, with a tie-out row | Lead (Skeptic acceptable) |
| D3 | "Cut unsubscribe rate by 30 percent" has no baseline, timeframe or statement of the candidate's share. "Rose to $0.42" has no starting point. | Resume, Corvid | Major | Evidence |
| D4 | Nothing explains the time since Jun 2024 (about two years and four months by October 2026). | Resume | Major | Skeptic |
| D5 | JD requirements absent from both documents: holdout or incrementality testing, push, loyalty program work. | Resume; cover letter | Major or Minor | Skeptic or Decision |

The summary's "eight years" matches Jun 2016 to Jun 2024. It is not a defect.

## Must

- M1. The verdict is Return.
- M2. "Numbers that do not tie" has rows for revenue per email ($0.42 against $0.48) and for the Corvid start date (Mar 2021 against 2020).
- M3. Both mismatches are Blocker findings with fixes that tell the candidate to settle on the true figure.
- M4. The 30 percent unsubscribe claim is flagged for a missing baseline, timeframe or share.
- M5. The unexplained time since Jun 2024 is flagged.
- M6. At least one missing JD requirement (holdout testing, push or loyalty) is named, with a fix that adds it only where it is true.
- M7. The premortem includes an internal reason, such as positioning that is too broad or a number the candidate cannot defend in an interview.
- M8. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Invent metrics, employers, keywords or experience for the candidate.
- N2. Rewrite resume bullets or the cover letter.
- N3. Treat "eight years" as a mismatch.
