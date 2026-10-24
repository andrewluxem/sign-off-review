# Evals

Six hand-run cases: one per profile, plus one false-alarm case. Each `<case>.md` gives the prompt, the input files, a table of planted defects with expected severity, and must and must-not criteria. The inputs live in `inputs/`.

Every company, person, product and number in this directory is invented. Any resemblance to a real organization is a coincidence.

| Case | Profile | Expected verdict | What it tests |
|---|---|---|---|
| `strategy-01` | strategy | Return | a summary figure that disagrees with the body table |
| `pitch-01` | pitch | Return | an unattributed client result with no baseline |
| `brief-01` | brief-post | Return | a stat with no URL; an anecdote turned into a rule |
| `job-01` | job-search | Return | a metric and a date range that differ between resume and cover letter |
| `plan-01` | build-plan | Return | no rollback, unverified flags, a step that needs chat history |
| `good-01` | strategy | Release or Release with fixes | a sound memo; no invented Blockers or tie-outs |

## Running a case

1. Start a fresh Claude Code session with the skill installed. The reviewer must not read the case file, only the inputs and the prompt.
2. Paste the case's prompt.
3. Move the review it writes next to the input into `runs/<date>/`, so later runs do not mistake it for a prior review.
4. Run `python3 scripts/check_report.py runs/<date>/<review>.md`.
5. Grade each must and must-not criterion by hand. A case passes when every must holds and no must-not occurs.

CI does not run the evals. It runs the unit tests and the validator selftest. The unit tests also run the validator on every review stored under `runs/`.
