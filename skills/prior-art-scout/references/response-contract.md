# Response Contract

Use this reference when preparing the final chat reply after a prior-art run.
The reply should be concise, decision-oriented, and traceable to source evidence.

## Quick Scan

Do not write files by default. Return a compact answer with these fields:

- `Verdict`: practical answer to whether strong similar work is visible.
- `Closest candidates`: top matches or "none found in checked sources".
- `Why similar / different`: one or two bullets on overlap and gaps.
- `Uncertainty`: source limits, failed checks, missing known candidates, or weak evidence.
- `Next source`: the single best next place to check if the user wants more confidence.

Keep confidence modest when sources are thin. Do not imply exhaustive search from bounded queries.

## Formal Gate

Do not treat the final chat reply as a substitute for JSON and Markdown report
artifacts. Link or name the generated artifacts and summarize the decision state:

- `Artifact path`: JSON and Markdown output paths, or why an artifact is missing.
- `Recommendation`: build, adopt, integrate, fork, borrow, review, or write-new guidance.
- `Decision confidence`: confidence in the recommendation.
- `Coverage confidence`: confidence in source coverage.
- `Go / Review / Hold`: dashboard status and the primary action.
- `Top comparison anchors`: the 3-5 candidates that most shape the decision.
- `Borrow / adopt / integrate signals`: reusable patterns, adapters, docs, or UX ideas.
- `Avoid / unknown signals`: blockers, stale projects, license gaps, security gaps, or missing evidence.
- `Blind spots`: unchecked sources, failed adapters, and known missing evidence.
- `Next validation`: the next bounded check before implementation or adoption.

Separate decision confidence from coverage confidence. High decision confidence
with low coverage confidence must explain why the decision can still be narrow,
reversible, or provisional.
