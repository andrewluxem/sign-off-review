# Eval pitch-01: an unattributed client result with no baseline

| Field | Value |
|---|---|
| Profile | pitch |
| Stage | 3 |
| Input | `evals/inputs/pitch-01-proposal.md` |
| Expected verdict | Return |

## Prompt

> Run sign-off-review on evals/inputs/pitch-01-proposal.md. The question: should Pellucid Pet Foods hire Ostler & Finch for this engagement?

## Planted defects

| # | Defect | Where | Expected severity | Expected seat |
|---|---|---|---|---|
| D1 | "We grew a national pet retailer's email revenue 212 percent": the client is unnamed with no statement that it may be cited, and there is no baseline, no timeframe and no account of the firm's share of the work. It is the only proof in the proposal. | What you get | Major or Blocker | Evidence |
| D2 | The promised 15 percent lift in repeat purchase rate does not follow from a scope that ends at a recommendations deck and builds nothing. The 15 percent has no baseline, and 12 weeks is too short to observe it. | What you get; How we work | Major (Blocker acceptable) | Logic or Decision |
| D3 | The $48,000 fee has no price logic: no breakdown, no exclusions (build, platform work, creative) and no statement of who does the work or for how many days. | Fee | Major | Skeptic |
| D4 | The team is described only as "strategists with analysts". No names or roles. | Why Ostler & Finch | Minor, or merged into D3 | Skeptic |

## Must

- M1. The verdict is Return.
- M2. The unattributed 212 percent result is a finding rated Major or Blocker, and its Fix requires either naming the client with a baseline and timeframe, or cutting the claim. A Fix that only softens the wording fails M2.
- M3. The gap between the promised 15 percent lift and a scope that ends at recommendations is flagged at Major or Blocker.
- M4. The fee's missing price logic or exclusions are flagged.
- M5. "Missing outside view" names the lack of any comparison for the 15 percent lift and supplies no benchmark figure of its own.
- M6. The premortem has at least one internal reason, such as a claim the firm cannot defend in the room.
- M7. `scripts/check_report.py` exits 0 on the review.

## Must not

- N1. Supply a benchmark repeat-purchase lift or an industry figure.
- N2. Rewrite the proposal's copy.
- N3. Flag the proposal for being short.
- N4. Rate the 212 percent claim Minor.
