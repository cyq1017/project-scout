# Positioning Discussion

Use this reference after candidate discovery and `project-scout` report
generation. The discussion layer interprets the report; it does not replace the
engine-backed report.

## Inputs

Read these report fields before giving advice:

- `decision.recommendation`
- `decision.confidence`
- `decision_dashboard.go_no_go`
- `coverage.confidence`
- `coverage.blind_spots`
- `differentiation.positioning_brief`
- `differentiation.candidate_roles`
- top candidate evidence and unknown evidence records

Use `differentiation.positioning_brief.closest_alternatives` as the primary
comparison-anchor list. Do not rely only on `candidates[0]`: the raw candidate
table is score-sorted, while the positioning layer may correctly promote a
lower-scoring direct or close-adjacent precedent over a broad lexical match.

## Discussion Outputs

Return concise sections when the user asks whether to continue, reposition, or
improve the idea:

1. **Current verdict**: direct match, close adjacent, broad adjacent, or not yet
   enough coverage.
2. **Wedge**: the smallest defensible combined workflow or audience claim.
3. **Claims to avoid**: uniqueness, breadth, automation, or integration claims
   not supported by primary evidence.
4. **Borrow / integrate / compete**: what to learn from top candidates and how
   to classify them.
5. **Counterargument**: the strongest reason not to build or not to position it
   this way.
6. **Next validation**: one or two concrete source or product checks.

## Quality Rules

- Cite report evidence and blind spots in the discussion.
- Treat `review` as a manual-review state, not permission to proceed.
- Treat popularity, stars, SEO rank, or social buzz as adoption hints, not proof.
- Prefer combination claims over unsupported uniqueness claims.
- If coverage is `Low`, recommend research work before positioning work.
- If `project-scout` is unavailable, state that the discussion is provisional
  and record the missing engine as a process gap.

## Useful Challenge Questions

- Which candidate would a skeptical user choose instead?
- What phrase would make the README overclaim?
- Which part of the idea is commodity?
- Which workflow combination is still defensible after comparing alternatives?
- What primary source would change the recommendation?
