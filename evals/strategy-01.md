# Eval strategy-01: the summary saving disagrees with the savings table

| Field | Value |
|---|---|
| Profile | strategy |
| Stage | 3 |
| Input | `evals/inputs/strategy-01-memo.md` |
| Expected verdict | Return |

## Prompt

> Run sign-off-review on evals/inputs/strategy-01-memo.md. The question: should Brindlewood close the Boise distribution center and serve its stores from Reno by 30 June 2027?

## Planted defects

| # | Defect | Where | Expected severity | Expected seat |
|---|---|---|---|---|
| D1 | The annual saving is $1.4M in the summary and $1.1M in the savings table total. | Summary; savings table | Blocker, with a tie-out row | Lead (Skeptic acceptable) |
| D2 | "Pays back in under six months" holds only at $1.4M. At the table's $1.1M, $600K pays back in about 6.5 months (600 / 1,100 x 12). | Summary | At most Major, or folded into D1 | Lead or Skeptic |
| D3 | "Industry benchmarks show ... 20 to 30 percent" has no source, and it is used to call the savings conservative. | After the savings table | Major, or listed under Missing outside view | Evidence or Lead |
| D4 | No named owner: "The team will manage the transition." | Recommendation | Major | Decision |
| D5 | The peak-season in-stock risk is unpriced: no revenue at risk and no trigger to reverse ("will monitor"). | Risks | Major | Skeptic |

The 22 percent rent rise ($520.5K to $635K, about $115K a year) and Reno's headroom (61 percent capacity at 71 percent of units rises to about 86 percent) are consistent. They are not defects.

## Must

- M1. The verdict is Return.
- M2. "Numbers that do not tie" has a row for the annual saving: $1.4M (summary) against $1.1M (savings table), difference $0.3M.
- M3. Findings include a Blocker for that mismatch, with a fix that tells the author to settle on one figure (Reconcile or another instruction verb).
- M4. The 20 to 30 percent benchmark is flagged as unsourced, as a finding or under Missing outside view, and the review supplies no replacement figure.
- M5. The missing owner for the transition is flagged.
- M6. The unpriced peak-season downside is flagged.
- M7. The premortem has three reasons, and at least one is tagged (internal).
- M8. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Rate the payback recalculation as a separate Blocker, or add it as a tie-out row.
- N2. Invent an industry benchmark, or cite a source the memo does not contain and the reviewer did not fetch.
- N3. Rewrite memo sentences or propose new wording for the summary.
- N4. Flag the memo for its length or for lacking a framework.
