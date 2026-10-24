---
name: sign-off-review
description: One-pass sign-off review that decides whether a draft can go out. Five independent reviewer seats, a number tie-out, an outside-view check and a premortem produce a severity-ranked findings table and a verdict of Return, Release with fixes or Release, checked by a validator script. Profiles cover strategy memos and decks, consulting pitches and outreach, briefs and posts, job-search documents (resume, cover letter, LinkedIn About, interview stories) and build plans or agent prompts. Use when asked to "sign off on" a draft, "review this before I send it", "is this ready to go out", "red-team this memo", "pre-release review", or to gate a document with a release decision. Not for line editing (use avoid-ai-writing) or for iterating toward a quality bar (use gauntlet-loop, with this skill as its measurement critic).
---

# Sign-off review

Decide whether a draft can leave your hands and, if not, exactly what must change first. One pass produces the full findings list, ranked by severity, and a verdict that follows fixed rules. The review decides and instructs. It never rewrites the draft.

## Inputs

Ask only for what is missing, in one message. If the user does not answer, proceed and list each assumption on an `**Assumptions:**` line under the review header.

1. **Draft.** A path or pasted text: Markdown, plain text, or PDF and DOCX when the harness can read them. Several files are reviewed together as one submission.
2. **Question.** What the draft must answer, or the decision it supports. If missing, reconstruct it from the draft and mark it `(reconstructed, assumption)`.
3. **Profile.** Detect it from the content, then confirm in one line ("Reviewing as `pitch`; say if it is something else.").
4. **Stage.** `1` framing (question or thesis only), `2` outline or plan, `3` final. Default `3`.
5. **Target role** (job-search only). The job description or role title. Without it, the Decision seat states the role it assumed.

A prior review file for the same draft makes this a re-review (see below).

| Profile | Use for | Signals |
|---|---|---|
| `strategy` | memos, plans and decks asking for a decision | decision requested, options, costs, savings |
| `pitch` | consulting proposals, outreach to prospects | fee, scope, "why us", a named prospect |
| `brief-post` | newsletter briefs, LinkedIn posts | thesis, hook, reader takeaway, external facts |
| `job-search` | resume, cover letter, LinkedIn About, interview stories | roles with dates, metrics, a target role |
| `build-plan` | specs, run sheets, prompts for coding agents | steps, commands, paths, a done-when |

## Files

- `references/profiles/<profile>.md`: each seat's checks, tie-out scope, premortem prompts, profile false alarms.
- `references/severity.md`: severity, calibration, verdict rules, tie-out rules, general false alarms.
- `references/seat-brief.md`: the brief each seat receives.
- `scripts/check_report.py`: the validator for the finished review.

## Flow

### 1. Frame
Write down the question, the answer the draft gives (one sentence, quoted where possible) and whether they match. A draft that gives no answer gets a Blocker from the `Lead` seat before anything else runs.

### 2. Inventory the numbers
List every figure the draft states with its value, unit, location and stated source. For job-search the list spans every document passed in and also covers date ranges, titles and employer names. The inventory feeds step 4. Seats never see it.

### 3. Run the seats
Load the profile. Stage 3 runs all five seats: Decision, Logic, Evidence, Skeptic, Outsider. Stages 1 and 2 run Decision and Logic only.

- **Subagents available:** one subagent per seat, all at once, each briefed from `references/seat-brief.md` with the draft, the question, the profile name, the stage, the review date and that seat's section of the profile file. Nothing else: no other seat's checks or findings, no author reasoning, no chat history, no inventory.
- **No subagents:** run the seats one at a time, in order. Write down each seat's findings before starting the next, and never go back to change an earlier seat's findings.
- **A launch is refused:** run that seat in sequence as above, and note `seat N ran inline` on the Assumptions line.

Each seat returns finding rows and up to three things it would keep.

### 4. Tie out the numbers (Lead)
Compare the inventory with itself. When the draft states the same quantity with two values that cannot both be true after rounding, add a row to "Numbers that do not tie" and a Blocker finding whose fix starts with "Reconcile". Size does not matter. When only your own arithmetic disagrees with the draft (a column that does not sum, a rate that does not follow), it is at most Major, the Problem cell shows the arithmetic, and it gets no tie-out row. Edge cases: `references/severity.md`.

### 5. Outside view (Lead)
For each driver the conclusion rests on, ask what it is compared with: a base rate, a benchmark, a past result. On `brief-post` and `pitch`, check every benchmark the draft cites against a source fetched this session. List each missing or unverified comparison under "Missing outside view". Never supply a benchmark from memory. A gap becomes a finding only when a decision driver rests on it; if a seat already raised it, cite that finding's number instead of adding a row.

### 6. Premortem (Lead)
Assume the draft went out and failed its purpose. Write three reasons, most likely first. Tag at least one `(internal)`: a cause on the author's or client's own side. The profile lists prompts.

### 7. Consolidate and calibrate
Apply `references/severity.md`, in this order:
- Merge findings that share a root cause. Keep the highest severity and the seat whose check names the root cause, except that a mismatch with a tie-out row stays with `Lead`.
- Give every Blocker and Major a one-sentence consequence, or rate it Minor.
- Run the calibration questions on every Blocker and Major. Over-rating fails the review just as a missed Blocker does.
- Drop anything on the general or profile false-alarm lists.
- Write each fix as an instruction that starts with a verb: Reconcile, Cut, Replace, Add, Move, Name, Source. Never "consider".
- Order the table Blocker, Major, Minor, and number the rows from 1.
- Set the verdict by the rules, not by overall impression.
- List what is good and must survive: specific strengths the fixes must not break.
- If the verdict is Return, describe what fixed looks like: the end state that would change the verdict.

### 8. Write, save, validate
Fill in the template below. If the draft is a file, save the review next to it as `<stem>.review-YYYY-MM-DD.md`; for several files, use the first file's stem and name them all in the header. For pasted text, return the review in chat.

If you can run Python, run `python3 <skill dir>/scripts/check_report.py <review file>` (for a chat-only review, write it to a temporary file first). Fix every violation and rerun until it exits 0. If you cannot run Python, check the ten rules in `references/severity.md` by hand and say that you did.

## Output template

```
# Sign-off review: <document>, profile <profile>, stage <1|2|3>
**Verdict:** Return | Release with fixes | Release
**In one line:** <the reason for the verdict, for someone who reads nothing else>
**Question:** <question> (given | reconstructed, assumption)
**Answer the draft gives:** <one sentence>
**Assumptions:** <optional: profile, stage or role assumed without confirmation>

## Findings
| # | Severity | Seat | Where | Problem | Consequence | Fix |
|---|---|---|---|---|---|---|

## Numbers that do not tie
| Number | Location A | Location B | Difference |
|---|---|---|---|

## Missing outside view

## Premortem
1. <reason> (internal)
2. <reason>
3. <reason>

## What is good and must survive
- <strength>

## What fixed looks like
<only when the verdict is Return>
```

- **Seat cell:** `Decision`, `Logic`, `Evidence`, `Skeptic`, `Outsider` or `Lead`, optionally followed by the profile's persona in parentheses, as in `Skeptic (CFO)`. `Lead` marks findings from steps 1, 4 and 5.
- Under a section with nothing in it, write `None.` instead of an empty table.
- Leave out "What fixed looks like" unless the verdict is Return.
- Consequence may stay empty only on Minor rows.
- Line-level prose problems (AI tells, rhythm, word choice) get at most one Minor finding, with the fix "Run avoid-ai-writing on the revised draft." Do not rewrite sentences.

## Re-review
Given a prior review of the same draft:
1. Add `## Prior findings` after the header lines, with a table `| # | Status | Note |`. Status is `fixed`, `partly fixed` or `open`. Keep the prior numbers.
2. Carry every open or partly fixed item into Findings under its old number. Change its severity only with the reason stated in the Problem cell.
3. Run a short full pass with the stage's seats for new problems, numbered after the highest prior number.
4. Redo the tie-out, the outside view and the premortem on the new draft.

## Rules that do not bend
- Seats are independent. No seat sees another seat's findings.
- The same figure stated with two values is a Blocker and forces Return. Your own recalculation is at most Major.
- Blockers and Majors carry a consequence or become Minor.
- Fixes are instructions.
- Never invent a benchmark, source, URL, number or quote.
- No line editing. Prose cleanup belongs to avoid-ai-writing, after the fixes land.
- No em dashes in the review.

## Working with other skills
- **avoid-ai-writing:** run it after the author applies this review's fixes, never while a Return is unresolved. If it changes a number or a claim, run a re-review.
- **gauntlet-loop:** this skill can serve as gauntlet's measurement critic, with the bar "verdict is Release or Release with fixes under profile <profile>, and check_report.py exits 0". Each round, a fresh critic runs a full review, not a re-review, because gauntlet critics get no history. The orchestrator forwards only finding 1 to the builder, which keeps gauntlet's one-gap rule.
