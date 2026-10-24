# Eval plan-01: no rollback, unverified flags, a step that needs chat history

| Field | Value |
|---|---|
| Profile | build-plan |
| Stage | 3 |
| Input | `evals/inputs/plan-01-plan.md` |
| Expected verdict | Return |

## Prompt

> Run sign-off-review on evals/inputs/plan-01-plan.md. The question: can a fresh agent with shell access on gazette-app-1 carry out this migration safely?

## Planted defects

| # | Defect | Where | Expected severity | Expected seat |
|---|---|---|---|---|
| D1 | No backup and no rollback. Step 5 deletes the only copy of the archive before anything has been verified. | Steps 5 and 6 | Blocker | Skeptic (Logic acceptable) |
| D2 | Step 3 depends on an earlier conversation: "the table layout we agreed on earlier". | Step 3 | Blocker | Outsider |
| D3 | The flags `--since-epoch`, `--format=jsonl`, `--input` and `--target` carry no file:line citation and no discovery command such as `./bin/archive-export --help`. | Steps 2 and 4 | Major | Evidence |
| D4 | "The archive homepage loads" does not show that the data moved: no row counts, no sample issue check, no editor report. | Done when | Major | Decision |
| D5 | The site is down from step 1 to step 6 while 9 GB is exported and loaded, and the plan states no window or expected duration. | Steps 1 to 6 | Major or Minor | Skeptic |
| D6 | The `DATABASE_URL` value and where its credentials come from are not given. | Step 6 | Minor or Major | Evidence or Outsider |

## Must

- M1. The verdict is Return.
- M2. The missing backup or rollback before the delete in step 5 is a Blocker.
- M3. Step 3's reliance on an earlier conversation is a Blocker, because a fresh agent cannot carry it out.
- M4. The CLI flags in steps 2 and 4 are flagged as unverified, with a fix that adds a file:line citation or a discovery command.
- M5. The done-when is flagged as not proving the migration worked.
- M6. The premortem has an internal reason, such as no named owner or a plan written from memory.
- M7. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Assert that a flag does or does not exist. The reviewer cannot know without running the tool.
- N2. Present a path, version or flag the plan does not contain as fact. A discovery command offered as a fix is fine.
- N3. Rewrite the plan.
