# Sign-off review: job-01-resume.md and job-01-cover-letter.md, profile job-search, stage 3
**Verdict:** Return
**In one line:** Not as sent: the letter and resume disagree on Corvid revenue per email ($0.48 vs $0.42) and on the Corvid start date (2020 vs Mar 2021), and the application shows no holdout testing and does not account for the time since Jun 2024.
**Question:** Will this application earn a first interview for the Fenwick Trail Supply role (Senior Manager, Lifecycle Marketing)? (given)
**Answer the draft gives:** Yes: an eight-year lifecycle and CRM marketer who rebuilt Braze journeys, led a team of three and launched SMS to 210,000 subscribers is ready to "bring the same approach to Fenwick's loyalty members."
**Assumptions:** Profile `job-search` was detected from the content and not confirmed, because the user could not be asked. Stage 3 (final) by default. The resume and cover letter are reviewed as one submission, with job-01-jd.md as the target role. The time since the last role is measured to the review date, 2026-10-23, taken as the send date. The seats ran sequentially because the subagent limit was reached, so the lead had already built the number inventory before the seats ran.

## Findings
| # | Severity | Seat | Where | Problem | Consequence | Fix |
|---|---|---|---|---|---|---|
| 1 | Blocker | Lead | Resume, Corvid bullet 1; cover letter, paragraph 2 | Revenue per email at Corvid is "$0.42" in the resume and "$0.48" in the letter. The letter has the larger figure. | A hiring manager who reads both sees the letter raise the resume's own number and doubts every other figure, and the candidate cannot defend both on a screening call. | Reconcile revenue per email to the one figure the candidate can document and use it in both documents. |
| 2 | Blocker | Lead | Resume, Corvid dates; cover letter, paragraph 2 | The resume gives Corvid as "Mar 2021 to Jun 2024"; the letter says "From 2020 to 2024". A 2020 start would also overlap Tansy & Rye, which the resume runs to Feb 2021, and nothing explains an overlap. | A recruiter or background check finds the letter adding up to 14 months at Corvid, overlapping the previous job, and reads it as padding the leadership tenure the JD screens on (3+ years leading people). | Reconcile the Corvid dates to one range and state it as month and year in both documents. |
| 3 | Major | Decision (hiring manager) | JD "What you bring", bullet 3; whole resume and letter | Neither document shows holdout, control-group or incrementality evidence. The closest is "A/B testing" in Skills, and the revenue figures are attributed ("email-attributed revenue"). The JD lists "proving incrementality with holdout or control groups" as a must-have and makes quarterly incremental-revenue reporting to the CMO a core duty. The terms are also missing word for word, so keyword screens miss them. | The hiring manager needs someone to report incremental revenue to the CMO each quarter, finds no proof the candidate has measured it, and advances candidates who show it. | Add the holdout or control-group test and its measured lift to the bullet whose result it proved, if one was run; if none was, Name what the A/B testing in Skills tested and found in one bullet, and claim no holdouts. |
| 4 | Major | Skeptic (recruiter) | Resume, Experience, after Corvid "Jun 2024"; cover letter, paragraph 2 | Nothing is listed or explained after Jun 2024, about 28 months as of 2026-10-23. The letter's "to 2024" does not address it. | The recruiter sees more than two unexplained years since the last role and screens the candidate out or spends the first call on the gap. | Add one line that accounts for Jun 2024 to the present. |
| 5 | Major | Evidence | Resume, Corvid bullets 1 and 3, and the Corvid role as a whole | The Corvid results have no baseline, period or scope: "revenue per email rose to $0.42" (from what, over what period, across which journeys) and "Cut unsubscribe rate by 30 percent" (from what rate, over what period). The role gives no list size, audience or revenue to compare with Fenwick's 2.4 million members, and "Rebuilt" does not separate the candidate's work from the team of three's. | The hiring manager cannot tell how much the most recent role improved anything or whether its program came near Fenwick's size, so the resume's lead achievement carries little weight and a non-specialist reads $0.42 as trivial. | Add the starting value, period and scope to the revenue-per-email and unsubscribe bullets, the Corvid list or audience size, and the candidate's own part in the rebuild. |
| 6 | Minor | Decision (hiring manager) | Cover letter, paragraphs 1 and 4 | The opening says why the audience appeals ("the kind of audience where lifecycle work pays off fastest"), not why this candidate fits, and the proof waits until paragraph 2. The close offers "the same approach" but never names it. | | Move the Braze journey rebuild and team leadership into the opening paragraph, and Name the approach the closing paragraph refers to. |
| 7 | Minor | Decision (hiring manager) | Resume, headline, summary and Corvid bullet 2 | The JD requires "3+ years leading people". The headline says "leader", but the summary says "marketer" and leaves out people leadership. "Led a team of three" gives no period within a tenure of 3 years 3 months. | | Add people leadership to the summary and the span of the team lead to the Corvid team bullet. |
| 8 | Minor | Skeptic (recruiter) | Cover letter, paragraph 2 | "I led lifecycle marketing at Corvid" gives no title, while the resume and any reference check say "Senior Lifecycle Manager". | | Name the title Senior Lifecycle Manager in the letter's Corvid sentence. |
| 9 | Minor | Evidence | Resume, Tansy & Rye bullet 2; cover letter, paragraph 3 | "Grew email-attributed revenue from $2.1M in FY2019 to $3.4M in FY2020" names no driver and no candidate share. | | Add what drove the growth and the candidate's share of it. |
| 10 | Minor | Logic | Resume, Tansy & Rye bullets | The role opens with a promotional calendar ("three sends a week to 1.1 million subscribers"). The revenue growth bullet, closer to the target role, sits second. | | Move the revenue growth bullet to the top of the Tansy & Rye role. |
| 11 | Minor | Outsider (non-specialist) | Resume: "Braze", "Klaviyo", "replenishment journeys", "in-house sender" | Tool and program names appear without saying what they are on first use. | | Add a short plain description of each on first use. |

## Numbers that do not tie
| Number | Location A | Location B | Difference |
|---|---|---|---|
| Corvid revenue per email | $0.42 (Resume, Corvid bullet 1) | $0.48 (Cover letter, paragraph 2) | $0.06 |
| Corvid start date | Mar 2021 (Resume, Corvid dates) | 2020 (Cover letter, paragraph 2) | The letter's start is 3 to 14 months earlier (it gives a year only) |

## Missing outside view
For this profile, the outside reference is the job description. These requirements have no evidence, or only partial evidence, in either document:
- Proving incrementality with holdout or control groups (must-have): no evidence; Skills lists only "A/B testing". Raised as finding 3.
- 3+ years leading people (must-have): the only evidence is "Led a team of three" at Corvid, a role of 3 years 3 months with no period given for the team. Raised as finding 7.
- SQL for self-serve analysis (must-have): named in Skills only, and no bullet shows it in use. Not a finding, because the term is present and no decision rests on more than that.
- Loyalty program experience (preferred): no evidence, although the letter closes on "Fenwick's loyalty members". Not a finding: it is preferred only, and the candidate cannot be asked to claim it.
- Duties with no matching evidence: push messaging, winback and browse-abandonment journeys, leading an analyst and a copywriter, and quarterly reporting to a CMO. Not findings: none is a must-have, and none can be added unless true.
- Per the profile, no applicant-pool, salary or market comparison is made.

## Premortem
1. The hiring manager screens for someone who has run holdout tests and reported incremental revenue, finds only attributed revenue and "A/B testing" in a skills list, and advances candidates who show incrementality. (internal)
2. The recruiter cannot trust the record: nothing is listed after Jun 2024, the letter moves the Corvid start to 2020, and revenue per email changes from $0.42 to $0.48 between documents, so the application is set aside before a call. (internal)
3. An applicant tracking system filters on "holdout", "incrementality" or "loyalty", and since none of them appears, no person reads the application.

## What is good and must survive
- The headline and summary name lifecycle and CRM marketing for consumer brands in the JD's own terms, so the top third makes the target role clear.
- Braze leads the first bullet of the most recent role, matching a JD must-have.
- The SMS result is complete and identical in both documents: launched, 210,000 subscribers, nine months.
- The Tansy & Rye revenue result gives both endpoints and fiscal years, and the letter's "in a year" ties to it.
- The resume dates use one month-year format, with no gaps between the three roles.
- The letter names Fenwick Trail Supply, the exact role title and the 2.4 million loyalty members, so it cannot be sent unchanged to another employer.
- The Klaviyo migration states a concrete outcome (no loss of list) rather than a forced metric.

## What fixed looks like
Both documents give one revenue-per-email figure and one Corvid date range in month and year, with no overlap with Tansy & Rye. Reconciling those two Blockers alone moves the verdict to Release with fixes. To reach Release, the application must also:
- account for Jun 2024 to the present in one line;
- give the Corvid results their starting value, period and scope, plus the program's size;
- show the candidate's real testing evidence against the holdout requirement, or name the A/B testing that was done and claim no holdouts.
