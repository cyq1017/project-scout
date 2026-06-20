# Report Schema

## Markdown Report

Default path:

```text
docs/research/YYYY-MM-prior-art-map.md
```

Required sections:

1. Executive Summary
2. Positioning Brief
3. Decision Dashboard
4. Search Summary
5. Source Requirements
6. Coverage Matrix
7. Similar Projects
8. Overlap Matrix
9. What To Borrow
10. What To Avoid
11. Recommendation And Confidence
12. Coverage Confidence And Blind Spots
13. Differentiation Map
14. Differentiation Is Not Enough: Useful Positioning
15. Risks And Unknowns
16. Suggested ADR / Backlog Updates

## JSON Report

Default path:

```text
project-scout-report.json
```

Top-level fields:

```json
{
  "brief": {},
  "generated_at": "ISO-8601 timestamp",
  "summary": {
    "candidate_count": 0,
    "top_recommendation": "Borrow"
  },
  "decision": {},
  "decision_dashboard": {
    "status": "ready_for_manual_review",
    "go_no_go": "review",
    "primary_action": "",
    "review_queue": [],
    "open_questions": []
  },
  "coverage": {},
  "differentiation": {
    "positioning_brief": {
      "verdict": "No direct match recorded",
      "closest_alternatives": [],
      "differentiation_claim": "",
      "recommended_positioning": "",
      "decision": "Research More",
      "next_validation_steps": []
    },
    "candidate_roles": [],
    "similarity_clusters": [],
    "commodity_features": [],
    "unique_combination": [],
    "defensible_positioning": [],
    "claims_to_avoid": [],
    "borrow_integrate_compete_guidance": [],
    "readme_positioning_draft": ""
  },
  "search_log": [],
  "candidates": [],
  "overlap_matrix": [],
  "recommendations": [],
  "risks": [],
  "suggested_updates": []
}
```

Candidate entries include normalized candidate metadata, scoring evidence,
structured evidence records, and a recommendation. Scores are deterministic
floats from `0.0` to `1.0`.

The `differentiation` object is deterministic positioning support. It separates
features already visible in candidates from the proposed unique combination,
records claims to avoid, and drafts conservative README language. It is not a
claim that the project is unique or that the recorded search was exhaustive.
`positioning_brief.closest_alternatives` is a comparison-anchor list, not a
duplicate of the score-sorted candidate table. It prioritizes explicit
`attributes.layer` values such as direct or close-adjacent matches before broad
adjacent lexical matches, then falls back to score. Use it for positioning and
next-validation discussion.

The `decision_dashboard` object is a deterministic first-page action layer. It
turns decision confidence, coverage, blind spots, and unknown evidence records
into `go`, `review`, or `hold`, plus a primary action, review queue, and open
questions. It is not an automatic approval or roadmap mutation.

## Markdown Safety

Markdown report rendering treats candidate and source metadata as untrusted
input. Table/list content is escaped, local absolute paths are redacted to
`[local-path]/name`, and candidate links only render clickable `http` or
`https` URLs. Unsafe or malformed candidate URLs render as `about:blank`.
