# Report Schema

## Markdown Report

Default path:

```text
docs/research/YYYY-MM-prior-art-map.md
```

Required sections:

1. Executive Summary
2. Similar Projects
3. Overlap Matrix
4. What To Borrow
5. What To Avoid
6. Build / Adopt / Fork / Plugin Recommendation
7. Differentiation Is Not Enough: Useful Positioning
8. Risks And Unknowns
9. Suggested ADR / Backlog Updates

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
  "candidates": [],
  "overlap_matrix": [],
  "recommendations": [],
  "risks": [],
  "suggested_updates": []
}
```

Candidate entries include normalized repository metadata, scoring evidence, and a recommendation. Scores are deterministic floats from `0.0` to `1.0`.
