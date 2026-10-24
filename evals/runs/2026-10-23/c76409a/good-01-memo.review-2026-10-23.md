# Sign-off review: good-01-memo.md, profile strategy, stage 3
**Verdict:** Release with fixes
**In one line:** The memo answers the question, every figure ties and every input is sourced, but its stop rule cannot tell new Saturday visitors from existing ones arriving later; fix that, then send.
**Question:** Should the board approve a six-month trial of Saturday afternoon hours at Eastgate Library? (given)
**Answer the draft gives:** "Approve the trial. It costs $8,411, fits inside the unspent hours-extension budget, and stops at the end of March if afternoon visits stay low."
**Assumptions:** Profile `strategy` detected from the decision request, costs and options; not confirmed, because the user could not be asked. Stage 3 (final) assumed by default. The seats ran one at a time in order, not as subagents, because the subagent limit was reached.

## Findings
| # | Severity | Seat | Where | Problem | Consequence | Fix |
|---|---|---|---|---|---|---|
| 1 | Major | Logic | Stop rule; Why ("41 percent of Saturday visitors arrive in the last hour before closing") | The memo does not say whether success means more Saturday visitors or the same visitors arriving later, and the stop rule counts only afternoon visits against a fixed bar of 26.5 per hour. By the memo's own figures, 41 percent of 212 is about 87 visitors in the last hour; if they only move into the three new hours, that is about 29 per hour (87 / 3), above the bar, with no new visitors at all. The memo offers the stop rule as its answer to overstated survey demand, but as written it cannot tell new demand from shifted demand. | At the April meeting the board could read a passed stop rule as new demand and keep funding hours that only spread the same 212 Saturday visitors over a longer day. | Add total Saturday visits against the 212 baseline as a second test in the stop rule, or state in the Recommendation that existing visitors moving into the afternoon counts as success. |
| 2 | Minor | Skeptic (CFO) | Stop rule; Comparison | The 26.5 bar comes from the full-year average (September 2025 to August 2026) but is tested on January to March Saturdays, and the memo does not say which Saturdays the "average" covers. Westbrook's 63 percent is the level it "reached" within three months, with no Westbrook morning rate given, so the claim that Eastgate's bar "sits below that result on purpose" is not shown on matching terms. | | Name the Saturdays the end-of-March average covers, and add the January to March 2026 Saturday average from the gate counter export and Westbrook's morning rate beside the 63 percent. |
| 3 | Minor | Skeptic (CFO) | Cost table ("3 staff x 3 extra hours"); Risks ("Shifts rotate so no one works more than two long Saturdays a month") | The memo does not say how many staff share the rotation, or whether the 234 extra hours are paid at the $31.50 loaded rate or at a premium. About 4.3 Saturdays a month at 3 staff each is about 13 long shifts a month, which at two per person needs at least 7 people. The budget headroom is $3,589 ($12,000 minus $8,411). | | Add the number of staff in the Saturday rotation and the pay basis for the extra hours under the staff agreement. |
| 4 | Minor | Logic | Options considered | A shorter extension, closing at 15:00 or 16:00, is a credible cheaper option and is neither named nor ruled out; the memo does not say why the trial adds three hours rather than one or two. | | Add one line to Options considered on why the trial closes at 17:00 rather than earlier. |
| 5 | Minor | Logic | Recommendation; Stop rule | The memo says what happens at the end of March and that a report comes in April, but not what happens when the trial ends on 26 June 2027: whether hours return to 14:00, and when the board decides on permanent hours. | | Add what happens after 26 June 2027 and the meeting at which the board will decide on permanent hours. |
| 6 | Minor | Evidence | Cost ("The FY2027 budget has $12,000 unspent in the hours-extension line") | The unspent balance has no as-of date, and the trial starts almost three months after the memo's date. | | Add the date of the $12,000 balance. |
| 7 | Minor | Outsider (non-specialist) | Cost table ("loaded rate"); Stop rule ("Mornings average 53 visitors per hour") | "Loaded rate" is not explained, and the "morning" rate is the 10:00 to 14:00 average, which includes two afternoon hours. | | Add a short gloss for "loaded rate" and name the 10:00 to 14:00 window where the morning rate first appears. |

## Numbers that do not tie
None.

## Missing outside view
- Uptake (the stop-rule bar): the only comparison is Westbrook's 63 percent (Westbrook gate counter report, December 2024). It is sourced but was not verified this session, and its baseline and measurement window are not given; see finding 2.
- New versus shifted demand: no comparison shows whether total Saturday visits rose at Westbrook, or anywhere else, when hours were extended; see finding 1.
- Survey intent: no base rate converts the 46 percent "would use" answer into visits. The memo says so openly and uses a stop rule instead of a forecast, so this is not a finding.
- Cost: staff and building costs are bottom-up estimates (HR rate card FY2027; facilities estimate, September 2026) with no past actual to compare against. The $3,589 headroom in the budget line absorbs a moderate miss, so this is not a finding.

## Premortem
1. Patrons learn of the new hours late, January and February afternoons stay quiet, and the March average misses 26.5 before demand has built, so a trial that would have worked stops at the halfway point. (internal)
2. The afternoons fill mainly with visitors who used to arrive between 13:00 and 14:00, so the bar is met while total Saturday visits stay near 212, and the board in April cannot see what the $8,411 bought.
3. Eastgate cannot put three staff on each long Saturday within the two-a-month cap, so shifts go unfilled or are paid at a premium, and the trial is cut short or overruns its budget line. (internal)

## What is good and must survive
- The "Decision requested" line names the exact hours, the 26 Saturdays and the dates, and the board's decision is an explicit "Approve".
- The Recommendation gives the cost, the budget source, the stop point, the owner and the report date in three sentences.
- Every figure ties: 234 hours x $31.50 = $7,371, $40 x 26 = $1,040, total $8,411, the same in all three places; 212 / 4 = 53, half is 26.5; 13 of 26 Saturdays is about $4,200; 1.5 x $7,371 = $11,056.50.
- Each input carries a source and a date: gate counter export (1 September 2026), August 2026 patron survey (380 responses), HR rate card FY2027, facilities estimate (September 2026), budget book page 14, Westbrook report (December 2024).
- The stop rule is a number derived in the text, with the spend at the stop point, and the memo says openly that survey answers overstate real visits.
- Options considered rules out Sunday opening (costed) and weekday evenings (18 visitors per hour) with a reason each.
