# Severity, calibration and verdict

## Severity

**Blocker.** As written, the draft would mislead its reader, or it cannot support the decision or purpose it exists for. Typical Blockers:
- the same figure stated with two values;
- no answer to the question;
- a headline claim the author could not back up if asked;
- a step a fresh executor cannot carry out, or a destructive step with no way back.

**Major.** A sharp reader would find a real weakness. It costs credibility, invites a second round or leaves a risk unpriced, but once fixed the draft can do its job.

**Minor.** The draft gets better, but no reader would decide differently.

## Consequence test

Every Blocker and Major carries one sentence naming who does what wrong, or what fails, if the draft goes out as it is. "Weakens the argument" and "reduces clarity" are not consequences. If you cannot write one, the finding is Minor.

## Calibration questions

Ask these of every Blocker and Major before setting the verdict.

1. If this stays, does a reader decide differently or get misled? If not, it is not a Blocker.
2. Would the intended reader notice it on a normal read? If only a specialist hunting for it would, lean Minor.
3. Is it the draft's problem or your preference? Drop preferences.
4. Does the draft state it, or did you derive it? A problem that rests only on your own arithmetic or inference is at most Major.
5. Is the same root cause already a finding? Merge.
6. Does the profile ask for this check at this stage? If not, drop it.

Errors in both directions count against the review. An inflated review trains the author to ignore it and sends back drafts that were ready. A deflated one lets a misleading draft go out.

## Verdict rules

Apply in order. The first rule that matches sets the verdict.

1. Any open Blocker: **Return**.
2. Any row in "Numbers that do not tie": **Return**. Every row also has a Blocker finding.
3. Any Major: **Release with fixes**. Majors alone never force Return, however many there are.
4. Otherwise: **Release**. Minor findings stay listed and are optional.

## Tie-out rules

- **Mismatch (Blocker, with a tie-out row).** The draft states one quantity twice with values that cannot both be true: a saving of $1.4M in the summary and $1.1M in the table, or a date range that differs between a resume and a cover letter.
- **Not a mismatch.** Consistent rounding ($1.4M and $1,400,000). Values labelled with different scopes or periods (FY2026 and FY2027). A range that contains the point value stated elsewhere.
- **Recalculation (at most Major, no tie-out row).** The draft states a total and its parts do not sum, or a rate does not follow from its inputs. Show the arithmetic, for example: "Rows sum to $940K (520 + 410 + 95 - 85); the table total says $1.1M." If that stated total also appears elsewhere with a different value, that part is a mismatch.
- **Scope.** Every document passed in for review. For job-search, a resume metric that differs from the cover letter is a Blocker.
- **Columns.** Number names the quantity. Location A and Location B give the value and where it appears. Difference gives the gap in the draft's own unit.

## False alarms (all profiles)

Do not raise these as findings.

- Length. A short draft that answers its question is complete.
- Uncertainty the draft states openly, such as a range, a confidence level or a named unknown. It counts in the draft's favor. Flag only uncertainty the draft hides.
- A missing framework, matrix or named model. Ask for structure only where the reader cannot follow without it.
- House style, formatting taste, word choice and AI tells. These go to avoid-ai-writing as one Minor finding at most.
- A section the profile does not require.
- More evidence for a claim nothing depends on.
- A counterargument section for a claim that is already narrow.
- Something the draft already covers elsewhere. Search the draft before you flag a gap.

## The ten mechanical rules

`scripts/check_report.py` enforces these. When you cannot run it, check them by hand.

1. The header line parses and names a known profile and a stage of 1, 2 or 3.
2. The verdict is Return, Release with fixes or Release.
3. Every severity is Blocker, Major or Minor, and every seat is valid for the profile. Stages 1 and 2 allow only the Decision, Logic and Lead seats.
4. Every Blocker and Major has a non-empty Consequence cell.
5. Any Blocker, or any data row under "Numbers that do not tie", means the verdict is Return.
6. A Return verdict has a non-empty "What fixed looks like".
7. The premortem has exactly three numbered items, and at least one contains `(internal)`.
8. "What is good and must survive" has at least one list item.
9. No Fix cell starts with consider, you may, you might or perhaps, in any case.
10. No em dash (U+2014) anywhere in the review.

The script also flags a missing header line or section, and, in a re-review, a prior finding marked open or partly fixed that is not carried into Findings under its old number.
