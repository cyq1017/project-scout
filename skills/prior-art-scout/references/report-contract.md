# Report Contract

Formal Gate must write a human Markdown report and a machine JSON report.

## Markdown Sections

Required:

1. Executive Summary
2. Search Summary
3. Coverage Matrix
4. Similar Candidates
5. Overlap Matrix
6. What To Adopt / Integrate / Borrow
7. What To Avoid
8. Recommendation And Confidence
9. Coverage Confidence And Blind Spots
10. Useful Positioning
11. Risks And Unknowns
12. Suggested ADR / Backlog / Skill Updates

## JSON Fields

Recommended top-level shape:

```json
{
  "brief": {},
  "generated_at": "",
  "mode": "formal_gate",
  "summary": {},
  "decision": {
    "recommendation": "Borrow",
    "confidence": "Medium",
    "rationale": [],
    "confidence_reasons": []
  },
  "coverage": {
    "confidence": "Medium",
    "sources": [],
    "blind_spots": [],
    "stop_reason": ""
  },
  "search_log": [],
  "candidates": [],
  "overlap_matrix": [],
  "recommendations": [],
  "risks": [],
  "suggested_updates": []
}
```

Search log entries should be structured:

```json
{
  "source": "github|skills|web|manual|internal",
  "query": "",
  "result_count": 0,
  "used_count": 0,
  "status": "ok|empty|rate_limited|failed",
  "error": null
}
```

Do not store raw result dumps by default. Save raw dumps only when the user explicitly requests a complete audit trail.
