# Report Schema

## Markdown Report

Default path:

```text
docs/research/YYYY-MM-prior-art-map.md
```

Required sections:

1. Executive Summary
2. Positioning Brief
3. Search Summary
4. Source Requirements
5. Coverage Matrix
6. Similar Projects
7. Overlap Matrix
8. What To Borrow
9. What To Avoid
10. Build / Adopt / Fork / Plugin Recommendation
11. Coverage Confidence And Blind Spots
12. Differentiation Map
13. Differentiation Is Not Enough: Useful Positioning
14. Risks And Unknowns
15. Suggested ADR / Backlog Updates

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
