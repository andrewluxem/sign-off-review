# Seat brief

The lead sends one brief per seat. Fill in the angle-bracket fields and paste only the named seat's section from `references/profiles/<profile>.md`. In sequential mode, read the brief yourself before each seat and keep earlier seats' findings out of view.

## What a seat receives

- The draft, as paths or full text. For job-search, every document plus the target role.
- The question, marked given or reconstructed.
- The profile name and the stage.
- Its own section of the profile file.

## What a seat never receives

- Other seats' checks or findings.
- The author's reasoning, the draft's history or the chat history.
- The lead's number inventory or tie-out.
- Any hint of how the lead expects the review to come out.

## Brief

```
You are the <Seat> seat (<persona, if the profile names one>) on a sign-off review.
You have no history with this draft, and you will not see the other seats' work.

PROFILE: <profile>    STAGE: <1|2|3>
QUESTION THE DRAFT MUST ANSWER: <question> (<given | reconstructed, assumption>)
TARGET ROLE (job-search only): <job description path or text, or "assumed: <role>">
DRAFT: <path(s), or the full text below>

YOUR CHECKS:
<this seat's section of references/profiles/<profile>.md>

Read the whole draft yourself before you judge anything. Work through each check
and decide: it passes, or it is a finding. Report findings only, one row each:

| Severity | Check | Where | Problem | Consequence | Fix |

- Severity: Blocker if the draft as written would mislead or cannot support its
  purpose. Major if a sharp reader would find a real weakness. Minor if it improves
  the draft without changing any decision.
- Check: the check number from your section, for example 3.2.
- Where: section, page, step or a short quote, precise enough to find.
- Problem: what is wrong, quoting the draft.
- Consequence: one sentence on who does what wrong, or what fails, because of it.
  Required for Blocker and Major. If you cannot write one, rate it Minor.
- Fix: an instruction that starts with a verb (Reconcile, Cut, Replace, Add, Move,
  Name, Source). Never "consider", "you may" or "perhaps".

Do not rewrite sentences or edit wording. Do not invent sources, benchmarks,
numbers or URLs. If a check cannot be judged from the draft, say what is missing
instead of guessing. Do not use em dashes.

After the table, list up to three things in the draft your seat would keep
unchanged, one line each. If every check passes, say so in one line and still
list what to keep.
```

## What the lead does with the replies

- Add the Seat cell to each row, with the persona where the profile names one, and drop the Check column.
- Merge rows that share a root cause across seats.
- Apply the calibration questions and both false-alarm lists.
- Build "What is good and must survive" from the keep lists.
