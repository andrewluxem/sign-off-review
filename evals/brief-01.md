# Eval brief-01: a stat with no URL and an anecdote turned into a rule

| Field | Value |
|---|---|
| Profile | brief-post |
| Stage | 3 |
| Input | `evals/inputs/brief-01-post.md` |
| Expected verdict | Return |

## Prompt

> Run sign-off-review on evals/inputs/brief-01-post.md. The question: what should a retention marketer change on Monday, and why?

## Planted defects

| # | Defect | Where | Expected severity | Expected seat |
|---|---|---|---|---|
| D1 | One retailer, one weekly promotion and one month of opens become "move every campaign to 6 a.m." | Paragraph 4; What to do on Monday | Blocker | Logic |
| D2 | "73 percent of marketers say ..." has no source and no URL. | Paragraph 3 | Major | Evidence |
| D3 | "Studies show ..." names no study. | Paragraph 3 | Major, or merged into D2 | Evidence |
| D4 | The post makes a broad claim and meets no counterargument: no control or comparison for the 18 percent, opens as the only measure, a possible one-month novelty effect, and audiences whose habits differ. | Whole post | Major | Skeptic |
| D5 | Line-level AI tells ("In today's fast-paced digital landscape", "The lesson is simple"). | Paragraphs 4 and 5 | Minor at most, handed to avoid-ai-writing | Outsider |

## Must

- M1. The verdict is Return.
- M2. The leap from one retailer's one-month result to "move every campaign" is a Blocker.
- M3. The 73 percent statistic is flagged for having no source URL, with a fix to add the fetched source or cut the claim.
- M4. "Studies show" is flagged as a vague attribution, separately or merged with M3.
- M5. The missing counterargument is flagged, since the claim is broad.
- M6. Line-level prose problems are handed to avoid-ai-writing in at most one Minor finding, and no sentence is rewritten in the review.
- M7. "Missing outside view" names the lack of a comparison or control for the 18 percent lift and supplies no figure of its own.
- M8. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Supply a statistic or URL for send-time effects that was not fetched this session and cited.
- N2. Rewrite the headline, the opening or any paragraph.
- N3. Rate the AI-tell sentences above Minor.
